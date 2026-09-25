"""Stage 4 — COLLECT current ads + products for qualified leads.

Ads come from the Ad Library page view (Playwright, no login). Products come from
the store's public catalog endpoints when available (Shopify /products.json,
WooCommerce Store API), else from JSON-LD / og tags on the landing pages.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from . import db, web
from .common import OUTPUT, get_logger, load_config

log = get_logger("collect")
MAX_ADS = 15


def _download(url: str, dest: Path) -> str | None:
    if dest.exists():
        return str(dest)
    try:
        r = httpx.get(url, headers={"User-Agent": web.UA}, timeout=30, follow_redirects=True)
        r.raise_for_status()
    except httpx.HTTPError as e:
        log.warning("download %s failed: %s", url[:80], e)
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(r.content)
    return str(dest)


def _rel(path: str | None) -> str | None:
    return str(Path(path).relative_to(OUTPUT)) if path else None


def collect_ads(lead: dict, browser: web.AdLibraryBrowser) -> None:
    ads = lead["meta"].get("page_ads")
    if not ads:
        count, raw = browser.page_ads(lead["meta"]["page_id"], load_config()["country"])
        ads = [web.flatten_ad(a) for a in raw]
        lead["meta"]["page_ads"] = ads
        if count is not None:
            lead["meta"]["active_ads_count"] = count
    today = dt.date.today()
    out_dir = OUTPUT / lead["lead_id"] / "current_ads"
    current = []
    # Longest-running first: those are the likely winners worth studying
    for ad in sorted(ads, key=lambda a: a.get("ad_delivery_start_time") or 1e12)[:MAX_ADS]:
        start = ad.get("ad_delivery_start_time")
        start_d = dt.date.fromtimestamp(start) if start else None
        days = (today - start_d).days if start_d else 0
        media = []
        for i, url in enumerate(ad.get("images", [])[:2]):
            p = _download(url, out_dir / f"{ad['id']}_{i}.jpg")
            if p:
                media.append({"type": "image", "path": _rel(p)})
        for v in ad.get("videos", [])[:1]:
            p = _download(v["thumb"], out_dir / f"{ad['id']}_video.jpg") if v.get("thumb") else None
            media.append({"type": "video", "thumb": _rel(p), "url": v.get("url")})
        variations = ad.get("collation_count") or 1
        current.append({
            "ad_id": ad["id"], "start_date": start_d.isoformat() if start_d else "",
            "days_running": days, "platforms": ad.get("platforms", []), "variations": variations,
            "primary_text": ad.get("body", ""), "headline": ad.get("ad_creative_link_title", ""),
            "description": ad.get("link_description", ""), "cta": ad.get("cta_text") or ad.get("cta_type", ""),
            "landing_url": ad.get("landing_url", ""), "media": media,
            "likely_winner": days >= 30 or variations >= 3,
            "library_url": ad.get("ad_snapshot_url"),
        })
    lead["current_ads"] = current


# ---------- products ----------

def _shopify(home: str, browser) -> list[dict]:
    data = browser.fetch_json(urljoin(home, "/products.json?limit=30"))
    if not isinstance(data, dict):
        return []
    out = []
    for p in data.get("products", []):
        price = (p.get("variants") or [{}])[0].get("price", "")
        out.append({"name": p.get("title", ""), "price": f"₪{price}" if price else "",
                    "url": urljoin(home, f"/products/{p.get('handle')}"),
                    "image_urls": [i["src"] for i in p.get("images", [])[:3]]})
    return out


def _woocommerce(home: str, browser) -> list[dict]:
    data = browser.fetch_json(urljoin(home, "/wp-json/wc/store/v1/products?per_page=30"))
    if not isinstance(data, list):
        return []
    out = []
    for p in data if isinstance(data, list) else []:
        prices = p.get("prices") or {}
        raw = prices.get("price")
        minor = prices.get("currency_minor_unit", 2)
        price = f"₪{int(raw) / 10 ** minor:g}" if raw and str(raw).isdigit() else ""
        out.append({"name": BeautifulSoup(p.get("name", ""), "html.parser").get_text(),
                    "price": price, "url": p.get("permalink", ""),
                    "image_urls": [i["src"] for i in p.get("images", [])[:3]]})
    return out


def _jsonld(urls: list[str], browser) -> list[dict]:
    out = []
    for u in urls:
        res = browser.fetch(u)
        if not res:
            continue
        soup = BeautifulSoup(res[1], "html.parser")
        for tag in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(tag.string or "")
            except ValueError:
                continue
            items = data if isinstance(data, list) else data.get("@graph", [data])
            for it in items:
                if isinstance(it, dict) and it.get("@type") in ("Product", ["Product"]):
                    offers = it.get("offers") or {}
                    offers = offers[0] if isinstance(offers, list) else offers
                    img = it.get("image") or []
                    img = [img] if isinstance(img, str) else [i if isinstance(i, str) else i.get("url") for i in img]
                    out.append({"name": it.get("name", ""),
                                "price": f"₪{offers.get('price')}" if offers.get("price") else "",
                                "url": res[0], "image_urls": [i for i in img if i][:3]})
        if not any(p["url"] == res[0] for p in out):
            og = soup.find("meta", property="og:image")
            title = soup.find("meta", property="og:title")
            if og and og.get("content") and "/product" in res[0]:
                out.append({"name": title.get("content", "") if title else "", "price": "",
                            "url": res[0], "image_urls": [og["content"]]})
    return out


def collect_products(lead: dict, browser) -> None:
    home = lead["business"]["website"]
    landings = [a["landing_url"] for a in lead["current_ads"] if a.get("landing_url")]
    signals = lead.get("qualify", {}).get("store_signals", [])
    products = ((_woocommerce(home, browser) if "woocommerce" in signals else [])
                or (_shopify(home, browser) if "shopify" in signals else [])
                or _woocommerce(home, browser) or _shopify(home, browser))
    # Products the ads push go first
    ad_products = _jsonld([u for u in dict.fromkeys(landings)
                           if db.normalize_domain(u) == db.normalize_domain(home)][:6], browser)
    seen, merged = set(), []
    for p in ad_products + products:
        key = re.sub(r"\W", "", p["name"].lower())
        if key and key not in seen:
            seen.add(key)
            merged.append(p)
    out_dir = OUTPUT / lead["lead_id"] / "products"
    photos = 0
    for i, p in enumerate(merged[:20]):
        p["images"] = []
        if photos < 6:
            for j, url in enumerate(p.get("image_urls", [])[:2]):
                path = _download(url if url.startswith("http") else urljoin(home, url),
                                 out_dir / f"p{i:02d}_{j}.jpg")
                if path:
                    p["images"].append(_rel(path))
                    photos += 1
        p.pop("image_urls", None)
    lead["products"] = merged[:20]


def run(lead_ids: list[str] | None = None) -> list[dict]:
    leads = [db.load_lead(i) for i in lead_ids] if lead_ids else db.leads_by_status("qualified")
    done = []
    with web.AdLibraryBrowser() as browser:
        for lead in leads:
            try:
                collect_ads(lead, browser)
                collect_products(lead, browser)
            except Exception:  # noqa: BLE001
                log.exception("collect failed for %s", lead["lead_id"])
                continue
            lead["timestamps"]["collected"] = dt.datetime.now().isoformat(timespec="seconds")
            db.save_lead(lead)
            n_img = sum(len(p["images"]) for p in lead["products"])
            log.info("COLLECT %s ads=%d winners=%d products=%d photos=%d", lead["lead_id"],
                     len(lead["current_ads"]), sum(a["likely_winner"] for a in lead["current_ads"]),
                     len(lead["products"]), n_img)
            done.append(lead)
    return done
