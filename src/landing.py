"""Landing-page check: where do the lead's current ads send people?

Groups the collected ads by the page they lead to (redirects resolved, tracking params
stripped), fetches each page once, classifies it (home / category / product / search /
whatsapp / facebook / other / broken) and flags the patterns worth telling the owner:

  home_many   several ads with different messages all land on the home page
  same_many   several ads with different messages land on one inner page
  broken      an ad leads to a page that errors or no longer exists
  offsite     an ad leads to WhatsApp / a Facebook canvas instead of the store

Result goes to lead["landing_audit"]; the Hebrew client copy is written per lead from it.
    python -m src.landing <lead_id> [<lead_id> ...]
"""
from __future__ import annotations

import json
import re
import sys
from collections import OrderedDict
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit

import httpx
from bs4 import BeautifulSoup

from . import db, web
from .common import get_logger

log = get_logger("landing")

TRACKING = re.compile(r"^(utm_|fbclid|gclid|mc_|_hs|ref$|srsltid|campaign|adset|ad_id|fb_)", re.I)
SHORTENERS = ("bit.ly", "tinyurl.com", "t.ly", "did.li", "rb.gy", "cutt.ly", "ow.ly", "l.facebook.com")


def _resolve(url: str) -> tuple[str, int | None]:
    """Follow redirects (short links included). Returns (final_url, status)."""
    try:
        with httpx.Client(headers={"User-Agent": web.UA}, timeout=25, follow_redirects=True) as c:
            r = c.get(url)
            return str(r.url), r.status_code
    except httpx.HTTPError as e:
        log.warning("resolve %s: %s", url[:80], e)
        return url, None


def normalize(url: str) -> str:
    s = urlsplit(url.strip())
    host = s.netloc.lower().removeprefix("www.")
    q = [(k, v) for k, v in parse_qsl(s.query, keep_blank_values=True) if not TRACKING.match(k)]
    path = unquote(s.path).rstrip("/") or "/"
    return urlunsplit(("https", host, path, urlencode(q), ""))


def kind_of(url: str, html: str | None, status: int | None) -> str:
    s = urlsplit(url)
    host, path, q = s.netloc.lower(), unquote(s.path).lower(), s.query.lower()
    if "whatsapp" in host or host.startswith("wa.me"):
        return "whatsapp"
    if "facebook.com" in host or host == "fb.com":
        return "facebook"
    if status and status >= 400:
        return "broken"
    if re.search(r"(^|&)(s|q|search)=", q):
        return "search"
    if re.search(r"/(product|products|items|item|p)/", path + "/") and path.count("/") >= 2:
        return "product"
    if re.search(r"/(product-category|collections|category|categories|shop|g|deal|manufacturer|brand)/", path + "/"):
        return "category"
    if path in ("", "/"):
        return "home"
    if html and ('"@type":"Product"' in html.replace(" ", "") or 'og:type" content="product' in html):
        return "product"
    return "other"


def page_info(url: str) -> dict:
    final, status = _resolve(url) if urlsplit(url).netloc.lower().removeprefix("www.") in SHORTENERS else (url, None)
    html = None
    got = web.get(final) if not any(h in final for h in ("whatsapp", "facebook.com", "fb.com")) else None
    if got:
        final, html = got
        status = status or 200
    elif status is None and not any(h in final for h in ("whatsapp", "facebook.com", "fb.com")):
        final, status = _resolve(final)
    title = h1 = ""
    if html:
        soup = BeautifulSoup(html, "html.parser")
        og = soup.find("meta", property="og:title")
        title = (og.get("content") if og else "") or (soup.title.get_text(strip=True) if soup.title else "")
        h = soup.find("h1")
        h1 = h.get_text(" ", strip=True)[:120] if h else ""
    return {"final_url": final, "status": status, "kind": kind_of(final, html, status),
            "title": title[:140], "h1": h1}


def _message(ad: dict) -> str:
    """The ad's opening line: what it promises. Used to count distinct messages per page."""
    for t in (ad.get("headline"), ad.get("primary_text")):
        t = (t or "").strip()
        if t and "{{" not in t:
            line = re.split(r"[\n.!?]", t)[0].strip()
            return re.sub(r"\s+", " ", line)[:90]
    return ""


def audit(lead: dict) -> dict:
    ads, seen = [], set()
    for a in lead.get("current_ads") or []:  # the same ad can be collected twice (once per version)
        if a.get("landing_url") and a["ad_id"] not in seen:
            seen.add(a["ad_id"])
            ads.append(a)
    groups: OrderedDict[str, dict] = OrderedDict()
    cache: dict[str, dict] = {}
    for a in ads:
        raw = a["landing_url"]
        if raw not in cache:
            cache[raw] = page_info(raw)
        info = cache[raw]
        key = normalize(info["final_url"])
        g = groups.setdefault(key, {"url": key, **info, "ads": [], "messages": []})
        g["ads"].append(a["ad_id"])
        m = _message(a)
        if m and m not in g["messages"]:
            g["messages"].append(m)
    gl = sorted(groups.values(), key=lambda g: -len(g["ads"]))
    findings = []
    for g in gl:
        n, k = len(g["ads"]), len(g["messages"])
        if g["kind"] == "home" and n >= 3 and k >= 2:
            findings.append({"type": "home_many", "url": g["url"], "ads": n, "messages": k})
        elif g["kind"] not in ("home", "broken", "whatsapp", "facebook") and n >= 4 and k >= 3:
            findings.append({"type": "same_many", "url": g["url"], "kind": g["kind"], "ads": n, "messages": k})
        if g["kind"] == "broken":
            findings.append({"type": "broken", "url": g["url"], "status": g["status"], "ads": n})
        if g["kind"] in ("whatsapp", "facebook"):
            findings.append({"type": "offsite", "url": g["url"], "kind": g["kind"], "ads": n})
    return {"ads_checked": len(ads), "pages": len(gl), "groups": gl, "findings": findings}


def run(lead_ids: list[str]) -> None:
    for lid in lead_ids:
        lead = db.load_lead(lid)
        res = audit(lead)
        lead["landing_audit"] = res
        db.save_lead(lead)
        print(f"\n{lid} {lead['business'].get('name_he') or lead['business'].get('name_en')}: "
              f"{res['ads_checked']} ads -> {res['pages']} pages")
        for g in res["groups"]:
            print(f"  {len(g['ads']):>2} ads  {len(g['messages']):>2} msgs  {g['kind']:<9} {g['status']}  {unquote(g['url'])[:90]}")
        for f in res["findings"]:
            print("  !", json.dumps(f, ensure_ascii=False))


if __name__ == "__main__":
    run(sys.argv[1:])
