"""Stage 1 — DISCOVER Israeli advertisers in the Meta Ad Library.

Backends (config.discovery.backend):
  mcp_import  Meta Ads MCP `ads_library_search` dumps saved by Claude Code into
              data/raw/discover/<date>_<keyword>.json. Verified 2026-09-25: the MCP
              DOES return active IL commercial ads (country=IL, currency ILS).
              It returns page_id / page_name / link title / dates, but no body text
              or landing URL — those come later (stage 3/4).
  apify       Apify Facebook Ads Library scraper (needs APIFY_TOKEN). Untested:
              api.apify.com is blocked in the current cloud environment.

Dump format (mcp_import):
  {"source": "meta_ads_mcp", "keyword": "...", "country": "IL", "fetched_at": "...",
   "estimated_total_count": 1701,
   "ads": [<ads_library_search ad objects>],
   "page_active_counts": {"<page_id>": <estimated_total_count for that page>}}  # optional
"""
from __future__ import annotations

import json
import os
from collections import OrderedDict
from pathlib import Path
from urllib.parse import quote

from .common import DATA, RAW_DISCOVER, get_logger, load_config, now_iso, today

log = get_logger("discover")
STATE_PATH = DATA / "keyword_state.json"


# ---------- keyword rotation ----------

def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"next_index": 0, "history": [], "ingested_files": []}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def next_keyword(cfg: dict, state: dict) -> str:
    kws = cfg["discovery"]["keywords"]
    return kws[state["next_index"] % len(kws)]


def advance_keyword(state: dict, keyword: str, source: str, advertisers: int,
                    keywords: list[str]) -> None:
    # Continue from the keyword after the one just used.
    if keyword in keywords:
        state["next_index"] = (keywords.index(keyword) + 1) % len(keywords)
    else:
        state["next_index"] += 1
    state["history"].append({"date": today(), "keyword": keyword, "source": source,
                             "advertisers": advertisers, "at": now_iso()})


# ---------- normalization ----------

def group_by_page(ads: list[dict], keyword: str, page_counts: dict | None = None) -> list[dict]:
    """Collapse ad rows into one advertiser record per page_id."""
    pages: "OrderedDict[str, dict]" = OrderedDict()
    for ad in ads:
        pid = str(ad.get("page_id") or "")
        if not pid:
            continue
        p = pages.setdefault(pid, {
            "page_id": pid,
            "page_name": ad.get("page_name") or "",
            "page_url": f"https://www.facebook.com/{pid}",
            "ad_ids": [],
            "sample_ads": [],
            "currencies": set(),
            "search_keyword": keyword,
        })
        p["ad_ids"].append(str(ad.get("id")))
        if ad.get("currency"):
            p["currencies"].add(ad["currency"])
        if len(p["sample_ads"]) < 5:
            p["sample_ads"].append({
                "ad_id": str(ad.get("id")),
                "link_title": ad.get("ad_creative_link_title") or "",
                "body": ad.get("body") or "",
                "landing_url": ad.get("landing_url") or "",
                "start_time": ad.get("ad_delivery_start_time"),
                "snapshot_url": ad.get("ad_snapshot_url")
                                or f"https://www.facebook.com/ads/library/?id={ad.get('id')}",
            })
    out = []
    for pid, p in pages.items():
        p["currencies"] = sorted(p["currencies"])
        p["ad_count_in_sample"] = len(p["ad_ids"])
        counts = page_counts or {}
        p["active_ads_count"] = int(counts.get(pid, p["ad_count_in_sample"]))
        p["active_ads_count_exact"] = pid in counts
        out.append(p)
    return out


# ---------- backends ----------

def from_mcp_dumps(state: dict) -> list[tuple[str, str, list[dict]]]:
    """Return [(file, keyword, advertisers)] for dumps not ingested yet."""
    RAW_DISCOVER.mkdir(parents=True, exist_ok=True)
    results = []
    for path in sorted(RAW_DISCOVER.glob("*.json")):
        if path.name in state["ingested_files"]:
            continue
        dump = json.loads(path.read_text(encoding="utf-8"))
        kw = dump.get("keyword", "")
        advs = group_by_page(dump.get("ads", []), kw, dump.get("page_active_counts"))
        log.info("dump %s keyword=%r ads=%d advertisers=%d",
                 path.name, kw, len(dump.get("ads", [])), len(advs))
        results.append((path.name, kw, advs))
    return results


def from_apify(keyword: str, cfg: dict) -> list[dict]:
    import httpx

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        raise RuntimeError("APIFY_TOKEN missing in .env")
    url = ("https://www.facebook.com/ads/library/?active_status=active&ad_type=all"
           f"&country={cfg['country']}&media_type=all&search_type=keyword_unordered"
           f"&q={quote(keyword)}")
    actor = cfg["discovery"]["apify_actor"]
    resp = httpx.post(
        f"https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items",
        params={"token": token},
        json={"urls": [{"url": url}], "count": cfg["discovery"]["max_ads_per_keyword"]},
        timeout=600,
    )
    resp.raise_for_status()
    ads = []
    for item in resp.json():
        snap = item.get("snapshot") or {}
        body = snap.get("body") or {}
        ads.append({
            "id": item.get("ad_archive_id") or item.get("adArchiveID") or item.get("id"),
            "page_id": item.get("page_id") or item.get("pageID") or snap.get("page_id"),
            "page_name": item.get("page_name") or item.get("pageName") or snap.get("page_name"),
            "ad_creative_link_title": snap.get("title") or "",
            "body": body.get("text") if isinstance(body, dict) else str(body or ""),
            "landing_url": snap.get("link_url") or "",
            "ad_delivery_start_time": item.get("start_date") or item.get("startDate"),
            "currency": item.get("currency") or "",
        })
    return group_by_page(ads, keyword)


# ---------- entry ----------

def run() -> list[dict]:
    """Discover new advertisers and register them in the DB as `discovered`."""
    from . import db

    cfg = load_config()
    state = load_state()
    backend = cfg["discovery"]["backend"]
    batches: list[tuple[str | None, str, list[dict]]] = []

    if backend == "mcp_import":
        batches = [(f, kw, a) for f, kw, a in from_mcp_dumps(state)]
        if not batches:
            kw = next_keyword(cfg, state)
            log.warning("No new MCP dumps in %s. Ask Claude Code to run ads_library_search "
                        "for keyword %r (country=IL, active) and save the dump.", RAW_DISCOVER, kw)
    elif backend == "apify":
        kw = next_keyword(cfg, state)
        batches = [(None, kw, from_apify(kw, cfg))]
    else:
        raise ValueError(f"unknown discovery backend {backend!r}")

    new = []
    for fname, kw, advertisers in batches:
        added = 0
        for adv in advertisers:
            if db.page_known(adv["page_id"]):
                continue
            lead = db.empty_lead(db.next_lead_id(), adv["page_id"], adv["page_name"], kw)
            lead["meta"].update({
                "active_ads_count": adv["active_ads_count"],
                "active_ads_count_exact": adv["active_ads_count_exact"],
                "ad_ids": adv["ad_ids"],
                "currencies": adv["currencies"],
                "sample_ads": adv["sample_ads"],
            })
            db.save_lead(lead)
            new.append(lead)
            added += 1
        log.info("keyword=%r: %d advertisers, %d new", kw, len(advertisers), added)
        if fname:
            state["ingested_files"].append(fname)
        advance_keyword(state, kw, backend, added, cfg["discovery"]["keywords"])
    save_state(state)
    return new
