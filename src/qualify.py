"""Stage 3 — QUALIFY (hard gate): website, IG page, owner IG, WhatsApp.

Sources used (what this environment can reach):
  - Ad Library ad pages (Playwright, no login) -> landing URL -> website
  - The business website: home, landing page, About/Story/Contact pages, Linktree
Not used: Facebook page "About" (needs login) and Instagram profiles/bios
(scraping them is off-limits here) — so the owner's IG is only found when the
website names it. Those leads end up `unqualified` for Eran to complete by hand.

Also the final "sells a physical product" check (store platform / cart / ₪),
since stage 2 only had the page name and ad titles to go on.
"""
from __future__ import annotations

import re
from collections import Counter
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from . import db, web
from .common import get_logger

log = get_logger("qualify")

IG_LINK = re.compile(r"instagram\.com/([A-Za-z0-9_.]{2,30})/?", re.I)
IG_RESERVED = {"p", "reel", "reels", "explore", "stories", "accounts", "tv", "share", "direct",
               "about", "developer", "legal", "web", "instagram"}
IG_MENTION = re.compile(r"(?<![\w@.])@([A-Za-z0-9_.]{3,30})(?![\w@])")
WA_LINK = re.compile(r"(?:wa\.me/|api\.whatsapp\.com/send/?\?phone=|whatsapp://send\?phone=)(\+?[\d\-\s%20]{9,20})", re.I)
PHONE = re.compile(r"(?<!\d)(?:\+?972[\s\-]?|0)(5\d)[\s\-]?(\d{3})[\s\-]?(\d{4})(?!\d)")
FOUNDER_WORDS = ["מייסד", "מייסדת", "המייסדת", "הבעלים", "בעלת", "יזמית", "יוצרת המותג", "הקמתי",
                 "founder", "founded by", "owner", "created by", "נעים מאוד", "שמי ", "הסיפור שלי"]
PAGE_HINTS = ["about", "our-story", "story", "contact", "אודות", "הסיפור", "צור-קשר", "צרו-קשר",
              "קשר", "מי-אנחנו", "who-we-are"]
STORE_SIGNALS = {
    "shopify": ["cdn.shopify.com", "shopify.theme", "myshopify.com"],
    "woocommerce": ["woocommerce", "wc-add-to-cart", "add_to_cart"],
    "wix_stores": ["wixstores", "wix-ecommerce", "wixstatic.com"],
    "konimbo": ["konimbo"],
    "cart": ["הוספה לסל", "הוסף לסל", "הוספה לעגלה", "לסל הקניות", "add to cart", "add-to-cart",
             "הוסיפי לסל", "לקנייה", "לרכישה"],
}


def normalize_il_mobile(raw: str) -> str | None:
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("972"):
        digits = "0" + digits[3:]
    if re.fullmatch(r"05\d{8}", digits):
        return "+972" + digits[1:]
    return None


def _site_from_ads(lead: dict, browser: web.AdLibraryBrowser) -> tuple[str | None, list[str], list[dict]]:
    """Visit up to 3 of the page's ads; return (homepage, landing_urls, ad_texts)."""
    landings, texts = [], []
    for ad in lead["meta"].get("sample_ads", [])[:3]:
        try:
            html, text = browser.ad_snapshot(ad["ad_id"])
        except Exception as e:  # noqa: BLE001 — keep going on flaky pages
            log.warning("ad %s snapshot failed: %s", ad["ad_id"], e)
            continue
        links = web.outbound_links(html)
        landings += [u for u in links if u not in landings]
        texts.append({"ad_id": ad["ad_id"], "text": text[:4000], "links": links})
    hosts = Counter(db.normalize_domain(u) for u in landings if db.normalize_domain(u))
    if not hosts:
        return None, landings, texts
    host = hosts.most_common(1)[0][0]
    return f"https://{host}/", landings, texts


def _collect_pages(home: str, landings: list[str]) -> list[tuple[str, str]]:
    pages, seen = [], set()

    def add(url):
        if url in seen or len(pages) >= 8:
            return None
        seen.add(url)
        res = web.get(url)
        if res:
            pages.append(res)
        return res

    res = add(home)
    host = db.normalize_domain(home)
    for u in landings[:2]:
        if db.normalize_domain(u) == host:
            add(u)
    if res:
        soup = BeautifulSoup(res[1], "html.parser")
        for a in soup.find_all("a", href=True):
            href = urljoin(res[0], a["href"])
            label = (a.get_text(" ", strip=True) + " " + href).lower()
            if db.normalize_domain(href) == host and any(h in label for h in PAGE_HINTS):
                add(href.split("#")[0])
            elif "linktr.ee/" in href or "linkin.bio" in href:
                add(href)
    return pages


def _extract(pages: list[tuple[str, str]]) -> dict:
    ig_links: Counter = Counter()
    ig_src: dict[str, str] = {}
    wa, phones, emails, owner_cands = [], [], set(), []
    store_hits = set()
    prices = False
    for url, html in pages:
        low = html.lower()
        for name, sigs in STORE_SIGNALS.items():
            if any(s.lower() in low for s in sigs):
                store_hits.add(name)
        if "₪" in html or "&#8362;" in html:
            prices = True
        for m in IG_LINK.finditer(html):
            h = m.group(1).rstrip(".").lower()
            if h not in IG_RESERVED:
                ig_links[h] += 1
                ig_src.setdefault(h, url)
        for m in WA_LINK.finditer(html):
            n = normalize_il_mobile(m.group(1).replace("%20", ""))
            if n:
                wa.append((n, url))
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.select('a[href^="mailto:"]'):
            emails.add(a["href"][7:].split("?")[0].strip())
        text = soup.get_text(" ", strip=True)
        for m in PHONE.finditer(text):
            n = normalize_il_mobile(m.group(0))
            ctx = text[max(0, m.start() - 60): m.end() + 20].lower()
            if n:
                phones.append((n, url, "וואטסאפ" in ctx or "whatsapp" in ctx or "ווטסאפ" in ctx))
        # owner IG: @mentions or IG links near founder words
        for m in IG_MENTION.finditer(text):
            ctx = text[max(0, m.start() - 150): m.end() + 150]
            if any(w in ctx.lower() for w in FOUNDER_WORDS):
                owner_cands.append({"handle": m.group(1).rstrip(".").lower(), "source": url,
                                    "kind": "mention", "context": ctx.strip()})
        for a in soup.find_all("a", href=IG_LINK):
            h = IG_LINK.search(a["href"]).group(1).rstrip(".").lower()
            parent = a.find_parent(["p", "div", "section", "li"]) or a
            ctx = parent.get_text(" ", strip=True)[:400]
            if h not in IG_RESERVED and any(w in ctx.lower() for w in FOUNDER_WORDS):
                owner_cands.append({"handle": h, "source": url, "kind": "link", "context": ctx})
    return {"ig_links": ig_links, "ig_src": ig_src, "wa": wa, "phones": phones,
            "emails": sorted(emails), "owner_cands": owner_cands,
            "store_hits": sorted(store_hits), "prices": prices}


def qualify_lead(lead: dict, browser: web.AdLibraryBrowser) -> None:
    home, landings, ad_texts = _site_from_ads(lead, browser)
    lead["meta"]["ad_snapshots"] = ad_texts
    lead["meta"]["landing_urls"] = landings
    q = lead.setdefault("qualify", {})
    if not home:
        q["missing"] = ["website"]
        db.set_status(lead, "unqualified")
        log.info("UNQUAL %s — no landing URL found in ads", lead["lead_id"])
        return
    lead["business"]["website"] = home
    domain = db.normalize_domain(home)
    if db.domain_known(domain, exclude_lead=lead["lead_id"]):
        db.set_status(lead, "rejected", f"domain {domain} already in DB")
        return

    pages = _collect_pages(home, landings)
    x = _extract(pages)
    q.update({"pages_checked": [u for u, _ in pages], "store_signals": x["store_hits"],
              "prices_in_ils": x["prices"], "owner_candidates": x["owner_cands"][:5]})

    if pages and not x["store_hits"]:
        db.set_status(lead, "rejected", "website is not a store (no cart / store platform)")
        log.info("REJECT %s %s — not a store", lead["lead_id"], domain)
        return

    c = lead["contact"]
    # Instagram business page: the handle linked most on the site
    biz_handle = None
    if x["ig_links"]:
        biz_handle = x["ig_links"].most_common(1)[0][0]
        c["instagram_page"] = {"url": f"https://www.instagram.com/{biz_handle}/",
                               "source": x["ig_src"][biz_handle], "confidence": "high"}
    # Owner IG: a founder-context handle different from the business handle
    for cand in x["owner_cands"]:
        if cand["handle"] != biz_handle:
            c["owner_instagram"] = {"url": f"https://www.instagram.com/{cand['handle']}/",
                                    "source": cand["source"],
                                    "confidence": "high" if cand["kind"] == "link" else "medium"}
            break
    # WhatsApp: explicit wa.me link > number labelled WhatsApp > nothing
    if x["wa"]:
        n, src = Counter(x["wa"]).most_common(1)[0][0]
        c["whatsapp"] = {"number_e164": n, "source": src, "confidence": "high"}
    else:
        labelled = [(n, src) for n, src, is_wa in x["phones"] if is_wa]
        if labelled:
            c["whatsapp"] = {"number_e164": labelled[0][0], "source": labelled[0][1], "confidence": "medium"}
        elif x["phones"]:
            n, src, _ = x["phones"][0]
            q["mobile_not_labelled_whatsapp"] = {"number_e164": n, "source": src}
    if x["emails"]:
        lead["business"]["email"] = x["emails"][0]

    missing = []
    if not c["instagram_page"]["url"]:
        missing.append("instagram_page")
    if not c["owner_instagram"]["url"] or c["owner_instagram"]["confidence"] == "low":
        missing.append("owner_instagram")
    if not c["whatsapp"]["number_e164"] or c["whatsapp"]["confidence"] == "low":
        missing.append("whatsapp")
    q["missing"] = missing
    db.set_status(lead, "unqualified" if missing else "qualified")
    log.info("%s %s %s missing=%s", "QUALIFIED" if not missing else "UNQUAL", lead["lead_id"], domain, missing)


def run(lead_ids: list[str] | None = None) -> list[dict]:
    leads = [db.load_lead(i) for i in lead_ids] if lead_ids else db.leads_by_status("filtered")
    done = []
    with web.AdLibraryBrowser() as browser:
        for lead in leads:
            try:
                qualify_lead(lead, browser)
            except Exception:  # noqa: BLE001 — one bad site must not stop the run
                log.exception("qualify failed for %s", lead["lead_id"])
                continue
            done.append(lead)
    return done
