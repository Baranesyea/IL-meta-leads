#!/usr/bin/env python3
"""Ad Lead Engine CLI.

  python run.py discover            stage 1 only
  python run.py filter              stage 2 only
  python run.py qualify [ids...]    stage 3 (default: all `filtered` leads)
  python run.py find                stages 1-5 (currently 1-3 are implemented)
  python run.py status [date]       list leads + status
  python run.py approve <id>
  python run.py reject <id> "reason"
  python run.py build [id]          stages 7-9 (not implemented yet)
  python run.py dashboard           (not implemented yet)
"""
from __future__ import annotations

import argparse
import sys

from dotenv import load_dotenv

from src import db
from src.common import ROOT, get_logger

log = get_logger("cli")


def cmd_discover(_):
    from src import discover
    new = discover.run()
    print(f"{len(new)} new advertisers discovered")


def cmd_filter(_):
    from src import filter as flt
    kept, rejected = flt.run()
    print(f"kept {len(kept)}, rejected {len(rejected)}")
    for lead in kept:
        m = lead["meta"]
        print(f"  {lead['lead_id']}  {m['page_name']}  ads={m['active_ads_count']}  "
              f"fb=https://www.facebook.com/{m['page_id']}")


def report_qualify(done):
    fields = ["website", "instagram_page", "owner_instagram", "whatsapp"]
    hits = {f: 0 for f in fields}
    for lead in done:
        c = lead["contact"]
        hits["website"] += bool(lead["business"].get("website"))
        hits["instagram_page"] += bool(c["instagram_page"]["url"])
        hits["owner_instagram"] += bool(lead.get("qualify", {}).get("owner_instagram_found"))
        hits["whatsapp"] += bool(c["whatsapp"]["number_e164"])
        print(f"  {lead['lead_id']}  {lead['status']:<11} {lead['meta']['page_name']}")
        print(f"      site={lead['business'].get('website') or '-'}  ig={c['instagram_page']['url'] or '-'}")
        print(f"      owner_ig={c['owner_instagram']['url'] or '-'}  wa={c['whatsapp']['number_e164'] or '-'}"
              f"  {lead.get('reject_reason') or ''}")
    n = len(done) or 1
    print("hit rate: " + ", ".join(f"{f} {v}/{len(done)} ({100 * v // n}%)" for f, v in hits.items()))


def cmd_qualify(args):
    from src import qualify
    report_qualify(qualify.run(args.lead_ids or None))


def cmd_find(args):
    """Stages 1-3, keyword after keyword, until today's target of qualified leads is reached."""
    from src import discover, filter as flt, qualify
    from src.common import load_config, today
    from src.web import AdLibraryBrowser

    cfg = load_config()
    target, max_kw = cfg["daily_target"], args.max_keywords
    with AdLibraryBrowser() as browser:
        for i in range(max_kw):
            have = len(db.leads_by_status("qualified", "researched", "approved", date=today()))
            if have >= target:
                break
            new = discover.run(browser)
            kept, rejected = flt.run(browser)
            done = qualify.run(browser=browser)
            ok = [l for l in done if l["status"] == "qualified"]
            print(f"[{i + 1}/{max_kw}] new={len(new)} filtered={len(kept)} rejected={len(rejected)} "
                  f"qualified={len(ok)} (today total {have + len(ok)}/{target})")
    report_qualify(db.leads_by_status("qualified", date=today()))
    log.info("stages 4-5 (collect/research) not implemented yet")


def cmd_status(args):
    for lead in db.leads_by_status(date=args.date):
        m = lead["meta"]
        extra = f"  — {lead['reject_reason']}" if lead.get("reject_reason") else ""
        print(f"{lead['lead_id']}  {lead['status']:<11} {m['page_name']}  "
              f"ads={m.get('active_ads_count')}{extra}")


def cmd_approve(args):
    lead = db.load_lead(args.lead_id)
    if lead["status"] != "researched":
        sys.exit(f"{args.lead_id} is '{lead['status']}', only 'researched' leads can be approved")
    db.set_status(lead, "approved")
    print(f"{args.lead_id} approved")


def cmd_reject(args):
    lead = db.load_lead(args.lead_id)
    db.set_status(lead, "rejected", args.reason)
    print(f"{args.lead_id} rejected: {args.reason}")


def not_yet(_):
    sys.exit("not implemented yet — see build order in CLAUDE.md")


def main():
    load_dotenv(ROOT / ".env")
    p = argparse.ArgumentParser(description="Ad Lead Engine")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("discover").set_defaults(func=cmd_discover)
    sub.add_parser("filter").set_defaults(func=cmd_filter)
    q = sub.add_parser("qualify")
    q.add_argument("lead_ids", nargs="*")
    q.set_defaults(func=cmd_qualify)
    fd = sub.add_parser("find")
    fd.add_argument("--max-keywords", type=int, default=8)
    fd.set_defaults(func=cmd_find)
    s = sub.add_parser("status")
    s.add_argument("date", nargs="?")
    s.set_defaults(func=cmd_status)
    a = sub.add_parser("approve")
    a.add_argument("lead_id")
    a.set_defaults(func=cmd_approve)
    r = sub.add_parser("reject")
    r.add_argument("lead_id")
    r.add_argument("reason")
    r.set_defaults(func=cmd_reject)
    b = sub.add_parser("build")
    b.add_argument("lead_id", nargs="?")
    b.set_defaults(func=not_yet)
    sub.add_parser("dashboard").set_defaults(func=not_yet)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
