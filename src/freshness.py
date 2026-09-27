"""Is the campaign still being worked on? (Eran's rule, 2026-09-27)

A page with more than 10 active ads where not one ad started in the last 30 days is a *great* lead: somebody built
and launched a campaign, and nobody has refreshed or optimised it since. We read every active ad of the page from
the Ad Library and store the newest and oldest start dates.

Limit: for Israeli commercial ads the Ad Library shows only ads that are running now. Ads that were switched off
are gone, so "when did the last ones stop" cannot be answered from public data.

Result: lead["meta"]["freshness"] = {active_seen, newest_start, oldest_start, days_since_newest, stale, checked}.
    python -m src.freshness <lead_id> ...
"""
from __future__ import annotations

import sys
from datetime import date, datetime, timezone

from . import db, web

MIN_ADS = 10          # the rule applies above this many active ads
STALE_DAYS = 30       # no ad started within this many days -> stale


def _day(ts) -> date | None:
    if ts in (None, ""):
        return None
    if isinstance(ts, (int, float)) or str(ts).isdigit():
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).date()
    try:
        return date.fromisoformat(str(ts)[:10])
    except ValueError:
        return None


def check(lead: dict, browser: web.AdLibraryBrowser, today: date | None = None) -> dict:
    today = today or date.today()
    count, ads = browser.page_ads(lead["meta"]["page_id"], max_ads=200, scrolls=20)
    starts = sorted(d for d in (_day(a.get("start_date")) for a in ads) if d)
    fr = {"active_count": count, "active_seen": len(ads), "checked": today.isoformat(),
          "newest_start": None, "oldest_start": None, "days_since_newest": None, "stale": False}
    if starts:
        fr.update(newest_start=starts[-1].isoformat(), oldest_start=starts[0].isoformat(),
                  days_since_newest=(today - starts[-1]).days)
        n = count or len(ads)
        fr["stale"] = n > MIN_ADS and fr["days_since_newest"] >= STALE_DAYS
    lead["meta"]["freshness"] = fr
    return fr


def run(ids: list[str]) -> None:
    with web.AdLibraryBrowser() as b:
        for lid in ids:
            lead = db.load_lead(lid)
            fr = check(lead, b)
            db.save_lead(lead)
            name = lead["business"].get("name_he") or lead["meta"].get("page_name")
            flag = "STALE (great lead)" if fr["stale"] else ""
            print(f"{lid}  ads={fr['active_count']} seen={fr['active_seen']}  newest={fr['newest_start']} "
                  f"({fr['days_since_newest']}d)  oldest={fr['oldest_start']}  {flag}  {name}")


if __name__ == "__main__":
    run(sys.argv[1:])
