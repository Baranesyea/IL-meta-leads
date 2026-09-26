"""Whose WhatsApp is it? Owner / small team vs. a customer-service line.

Eran works alone and mostly on autopilot, so a first message has to reach the person who decides. Public data can't
prove a number is the owner's, but the site around it says a lot. Signals (all from pages we already cache):

  service  the number is labelled customer service / hotline / reps ("שירות לקוחות", "מוקד", "נציג"),
           the business runs a *NNNN star number, a 1-800, or landlines, a support@ mailbox, several branches
  owner    the only phone on the site is this mobile, no hotline, no landline, a gmail/hello@ inbox,
           the owner's name or story on the site

Result: lead["contact"]["whatsapp"]["kind"] = "owner" | "unclear" | "service", plus "kind_signals".
    python -m src.wa_kind <lead_id> ...        (no ids = every lead that has a WhatsApp number)
"""
from __future__ import annotations

import re
import sys

from bs4 import BeautifulSoup

from . import db, web

SERVICE_NEAR = ("שירות לקוחות", "שרות לקוחות", "מוקד", "נציג", "צוות", "support")
HOURS_NEAR = ("שעות פעילות", "שעות הפעילות", "א'-ה'", "א׳-ה׳", "ימים א")
# facts found by hand (web search, about pages) — they override the heuristic
OVERRIDE = {
    "2026-09-25-015": ("service", "beauty salon (manicure, laser, tanning): a service business, not a product store"),
}


def _pages(lead: dict) -> list[str]:
    w = lead["contact"]["whatsapp"]
    site = (lead["business"].get("website") or "").rstrip("/")
    urls = [w.get("source") or "", site]
    urls += [site + p for p in ("/contact", "/contact-us", "/pages/contact", "/about", "/pages/about")]
    return [u for u in dict.fromkeys(urls) if u.startswith("http")]


def classify(lead: dict) -> tuple[str, list[str]]:
    if lead["lead_id"] in OVERRIDE:
        k, why = OVERRIDE[lead["lead_id"]]
        return k, [why]
    num = lead["contact"]["whatsapp"]["number_e164"][4:]           # 5XXXXXXXX
    near = re.compile(r"0?%s[-\s]?%s[-\s]?%s" % (num[:2], num[2:5], num[5:]))
    text = ""
    for u in _pages(lead):
        got = web.get(u)
        if got:
            text += " " + BeautifulSoup(got[1], "html.parser").get_text(" ", strip=True)
    svc, own = [], []
    for m in near.finditer(text):
        ctx = text[max(0, m.start() - 70):m.end() + 20]
        for w in SERVICE_NEAR:
            if w in ctx:
                svc.append(f"labelled '{w}' next to the number")
        if any(h in text[max(0, m.start() - 120):m.end() + 120] for h in HOURS_NEAR):
            svc.append("office hours next to the number")
    if re.search(r"\*\d{4}\b|\b\d{4}\*", text):
        svc.append("star number (" + re.search(r"\*\d{4}\b|\b\d{4}\*", text).group(0) + ")")
    if re.search(r"1-?800-?\d", text):
        svc.append("1-800 line")
    lands = set(re.findall(r"\b0(?:[2-489]|7[2-9])-?\d{3}-?\d{4}\b", text))
    if lands:
        svc.append(f"{len(lands)} landline(s)")
    if re.search(r"\b(support|service|sales)@", text, re.I):
        svc.append("support/sales mailbox")
    if re.search(r"סניפ(ים|י)|סניף ראשי|מחסן", text):
        svc.append("branches / warehouse")
    if re.search(r"[\w.]+@gmail\.com|hello@", text, re.I):
        own.append("gmail / hello@ inbox")
    mobiles = set(re.findall(r"\b05\d-?\d{3}-?\d{4}\b", text))
    if len(mobiles) <= 1 and not lands and not any(s.startswith("star") for s in svc):
        own.append("the only phone on the site")
    if lead["business"].get("owner_name"):
        own.append("owner named: " + lead["business"]["owner_name"])
    svc = list(dict.fromkeys(svc))
    strong = sum(1 for s in svc if s.startswith(("labelled", "star", "1-800")))
    if strong or len(svc) >= 3:
        kind = "service"
    elif not svc and own:
        kind = "owner"
    else:
        kind = "unclear"
    return kind, svc + own


def run(ids: list[str]) -> None:
    if not ids:
        import glob, json
        ids = [json.load(open(p))["lead_id"] for p in sorted(glob.glob("data/leads/*.json"))
               if (json.load(open(p))["contact"].get("whatsapp") or {}).get("number_e164")]
    for lid in ids:
        lead = db.load_lead(lid)
        kind, sig = classify(lead)
        lead["contact"]["whatsapp"].update(kind=kind, kind_signals=sig)
        db.save_lead(lead)
        name = lead["business"].get("name_he") or lead["meta"].get("page_name")
        print(f"{lid}  {kind:<8} {lead['status']:<10} {name}  |  {'; '.join(sig)}")


if __name__ == "__main__":
    run(sys.argv[1:])
