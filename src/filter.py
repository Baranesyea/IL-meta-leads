"""Stage 2 — FILTER discovered advertisers.

Hard rejects (logged with reject_reason, never re-checked):
  - big chain / known brand (config.filter.brand_blocklist)
  - service / course / clinic / lead-gen signals (config.filter.service_keywords)
  - not Israeli (no ILS currency and no Hebrew anywhere)
  - fewer than min_active_ads active ads, or more than max_active_ads (big advertiser)
  - domain already in DB (only once a website is known)

Passing advertisers become `filtered`. The Ad Library data we have at this point
has no landing URL, so "sells a physical product" is only a *probable* verdict here
(product_score); stage 3 confirms it on the actual website (store / cart / ₪ prices)
and demotes to `rejected` if it turns out to be a service.
"""
from __future__ import annotations

import re

from . import db
from .common import get_logger, load_config

log = get_logger("filter")
HEBREW = re.compile(r"[֐-׿]")
LATIN = re.compile(r"^[\x00-\x7F]+$")


def _hits(text: str, words: list[str]) -> list[str]:
    """Latin words match on word boundaries; Hebrew words match as substrings
    (Hebrew glues prefixes like ה/ב/ל/ו to words)."""
    text_l = text.lower()
    found = []
    for w in words:
        wl = w.lower()
        if LATIN.match(wl):
            if re.search(rf"(?<![a-z0-9]){re.escape(wl)}(?![a-z0-9])", text_l):
                found.append(w)
        elif wl in text_l:
            found.append(w)
    return found


def evaluate(lead: dict, cfg: dict) -> tuple[bool, str | None, dict]:
    f = cfg["filter"]
    meta = lead["meta"]
    name = meta.get("page_name", "")
    titles = " | ".join(a.get("link_title", "") + " " + a.get("body", "")
                        for a in meta.get("sample_ads", []))
    text = f"{name} | {titles}"

    signals = {
        "brand_hits": _hits(name, f["brand_blocklist"]),
        "service_hits": _hits(text, f["service_keywords"]),
        "product_hits": _hits(text, f["product_keywords"]),
        "hebrew": bool(HEBREW.search(text)),
        "currencies": meta.get("currencies", []),
        "active_ads_count": meta.get("active_ads_count", 0),
        "active_ads_count_exact": meta.get("active_ads_count_exact", False),
    }
    signals["product_score"] = len(signals["product_hits"]) - 2 * len(signals["service_hits"])

    if signals["brand_hits"]:
        return False, f"big brand/chain: {', '.join(signals['brand_hits'])}", signals
    if signals["service_hits"] and signals["product_score"] <= 0:
        return False, f"service/course/lead-gen: {', '.join(signals['service_hits'])}", signals
    israeli = signals["hebrew"] or any(c in f["accepted_currencies"] for c in signals["currencies"])
    if not israeli:
        return False, "not Israeli (no Hebrew, no ILS)", signals
    if signals["currencies"] and not any(c in f["accepted_currencies"] for c in signals["currencies"]):
        return False, f"ads billed in {signals['currencies']} — likely foreign/advertorial", signals
    n = signals["active_ads_count"]
    if n < f["min_active_ads"]:
        return False, f"only {n} active ad(s)", signals
    if n > f["max_active_ads"]:
        return False, f"{n} active ads — too big", signals
    domain = db.normalize_domain(lead["business"].get("website"))
    if db.domain_known(domain, exclude_lead=lead["lead_id"]):
        return False, f"domain {domain} already in DB", signals
    return True, None, signals


def run() -> tuple[list[dict], list[dict]]:
    cfg = load_config()
    kept, rejected = [], []
    for lead in db.leads_by_status("discovered"):
        ok, reason, signals = evaluate(lead, cfg)
        lead["meta"]["filter"] = signals
        if ok:
            db.set_status(lead, "filtered")
            kept.append(lead)
            log.info("KEEP   %s %s (ads=%s, product_score=%s)", lead["lead_id"],
                     lead["meta"]["page_name"], signals["active_ads_count"], signals["product_score"])
        else:
            db.set_status(lead, "rejected", reason)
            rejected.append(lead)
            log.info("REJECT %s %s — %s", lead["lead_id"], lead["meta"]["page_name"], reason)
    return kept, rejected
