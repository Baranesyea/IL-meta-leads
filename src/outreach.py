"""WhatsApp-first outreach, step A: light research, no image generation (Eran, 2026-09-27).

For every lead that has a WhatsApp number we read all its active ads from the Ad Library page view and compute
the facts a first message can stand on: how many ads, how many different messages, where they lead (and whether
those pages work), how old the newest ad is, what the button does, video vs image. Claude then writes one
personal message per business from these facts (data/outreach/messages.json) and `push` sends them to the CRM
(LeadCRM, track "wa", status "research"). Pages and the 20 ads are built only after the business says yes.

    python -m src.outreach research <lead_id> ...     (no ids: every candidate)
    python -m src.outreach show <lead_id>              print the facts for writing the message
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date, datetime, timezone
from urllib.parse import urlparse

from . import db, web
from .common import get_logger

log = get_logger("outreach")
EXCLUDE = {"2026-09-27-150": "car dealership chain", "2026-09-27-171": "car service center (urgent)",
           "2026-09-27-075": "international brand (Kryolan)"}


# Local mirror of the CRM's "do not send" list (entity DoNotSend in Base44, the one the senders check). Refresh it from
# the CRM before building a new outreach batch; numbers on it never become candidates.
DNS_FILE = "data/outreach/do_not_send.json"


def do_not_send() -> set[str]:
    import os
    if not os.path.exists(DNS_FILE):
        return set()
    return {"".join(c for c in str(x.get("phone", "")) if c.isdigit()) for x in json.load(open(DNS_FILE))}


def candidates() -> list[str]:
    import glob
    out, blocked = [], do_not_send()
    for p in sorted(glob.glob("data/leads/*.json")):
        l = json.load(open(p))
        num = "".join(c for c in (l["contact"].get("whatsapp") or {}).get("number_e164") or "" if c.isdigit())
        if (num and num not in blocked and l["status"] not in ("rejected", "published")
                and l["lead_id"] not in EXCLUDE):
            out.append(l["lead_id"])
    return out


def _day(ts):
    if ts in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).date()
    except (TypeError, ValueError):
        return None


def _norm(u: str) -> str:
    if not u:
        return ""
    p = urlparse(u)
    return (p.netloc.replace("www.", "") + p.path.rstrip("/")).lower()


def research(lead: dict, browser: web.AdLibraryBrowser, today: date | None = None) -> dict:
    today = today or date.today()
    count, raw = browser.page_ads(lead["meta"]["page_id"], max_ads=80, scrolls=6)
    ads = []
    for a in raw:
        f = web.flatten_ad(a)
        f["start"] = _day(a.get("start_date"))
        ads.append(f)
    starts = sorted(d for d in (a["start"] for a in ads) if d)
    bodies = [(a.get("body") or "").strip() for a in ads]
    distinct = len({b[:120] for b in bodies if b})
    landings = Counter(_norm(web.unwrap(a.get("landing_url") or "")) for a in ads if a.get("landing_url"))
    status = {}
    for u in list(landings)[:6]:              # does each destination page actually load?
        if "whatsapp" in u or "wa.me" in u:
            status[u] = "whatsapp"
            continue
        try:
            res = browser.fetch("https://" + u)
            status[u] = "ok" if res else "fail"
        except Exception:  # noqa: BLE001
            status[u] = "fail"
    home_hits = sum(n for u, n in landings.items() if urlparse("https://" + u).path in ("", "/"))
    r = {
        "checked": today.isoformat(),
        "active_count": count, "seen": len(ads),
        "newest_start": starts[-1].isoformat() if starts else None,
        "oldest_start": starts[0].isoformat() if starts else None,
        "days_since_newest": (today - starts[-1]).days if starts else None,
        "longest_running_days": (today - starts[0]).days if starts else None,
        "distinct_texts": distinct,
        "ctas": Counter(a.get("cta_type") or "" for a in ads).most_common(),
        "videos": sum(1 for a in ads if a.get("videos")),
        "landings": landings.most_common(8), "landing_status": status, "home_share": home_hits,
        "samples": [{"start": a["start"].isoformat() if a["start"] else None, "cta": a.get("cta_type"),
                     "title": a.get("ad_creative_link_title"), "body": (a.get("body") or "")[:400],
                     "landing": a.get("landing_url")} for a in ads[:8]],
    }
    lead["outreach"] = {**(lead.get("outreach") or {}), "research": r}
    return r


def run(ids: list[str]) -> None:
    ids = ids or candidates()
    with web.AdLibraryBrowser() as b:
        for lid in ids:
            lead = db.load_lead(lid)
            try:
                r = research(lead, b)
            except Exception as e:  # noqa: BLE001
                log.warning("research failed for %s: %s", lid, e)
                continue
            db.save_lead(lead)
            name = lead["business"].get("name_he") or lead["meta"].get("page_name")
            print(f"{lid} ads={r['active_count']} texts={r['distinct_texts']} newest={r['days_since_newest']}d "
                  f"home={r['home_share']}/{r['seen']} fails={[u for u, s in r['landing_status'].items() if s == 'fail']} {name}",
                  flush=True)


def show(lid: str) -> None:
    lead = db.load_lead(lid)
    r = (lead.get("outreach") or {}).get("research")
    b = lead["business"]
    print(json.dumps({"name": b.get("name_he") or lead["meta"].get("page_name"), "site": b.get("website"),
                      "category": b.get("category"), "research": r}, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:]
    {"research": run, "show": lambda a: [show(x) for x in a]}[cmd](rest)
