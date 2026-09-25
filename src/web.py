"""Polite, cached fetching: httpx for regular sites, Playwright for the Ad Library."""
from __future__ import annotations

import hashlib
import json
import random
import re
import time
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

import httpx

from .common import DATA, get_logger

log = get_logger("web")
CACHE = DATA / "cache"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
CHROMIUM = "/opt/pw-browsers/chromium"
_client: httpx.Client | None = None


def _cache_path(key: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    return CACHE / (hashlib.sha1(key.encode()).hexdigest() + ".html")


def _sleep():
    time.sleep(random.uniform(1.0, 2.5))


def get(url: str) -> tuple[str, str] | None:
    """Return (final_url, html) or None. Cached forever (delete data/cache to refresh)."""
    global _client
    path = _cache_path(url)
    if path.exists():
        final, _, html = path.read_text(encoding="utf-8").partition("\n")
        return final, html
    _client = _client or httpx.Client(headers={"User-Agent": UA, "Accept-Language": "he-IL,he;q=0.9,en;q=0.8"},
                                      follow_redirects=True, timeout=25)
    _sleep()
    try:
        r = _client.get(url)
    except httpx.HTTPError as e:
        log.warning("GET %s failed: %s", url, e)
        return None
    ctype = r.headers.get("content-type", "html")
    if r.status_code >= 400 or not any(t in ctype for t in ("html", "json")):
        log.warning("GET %s -> %s", url, r.status_code)
        return None
    path.write_text(f"{r.url}\n{r.text}", encoding="utf-8")
    return str(r.url), r.text


class AdLibraryBrowser:
    """Renders facebook.com/ads/library/?id=<ad_id> pages (no login needed)."""

    def __enter__(self):
        from playwright.sync_api import sync_playwright
        import os

        self._pw = sync_playwright().start()
        proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        self._browser = self._pw.chromium.launch(
            executable_path=CHROMIUM if Path(CHROMIUM).exists() else None,
            proxy={"server": proxy} if proxy else None)
        self._ctx = self._browser.new_context(locale="he-IL", user_agent=UA)
        self.page = self._ctx.new_page()
        return self

    def __exit__(self, *exc):
        self._browser.close()
        self._pw.stop()

    def render(self, url: str) -> tuple[str, str] | None:
        """Fallback for sites that block plain HTTP clients (403/503). Cached like get()."""
        path = _cache_path(url)
        if path.exists():
            final, _, html = path.read_text(encoding="utf-8").partition("\n")
            return final, html
        _sleep()
        try:
            resp = self.page.goto(url, timeout=60000, wait_until="domcontentloaded")
            self.page.wait_for_timeout(3000)
        except Exception as e:  # noqa: BLE001
            log.warning("render %s failed: %s", url, e)
            return None
        if resp is None or resp.status >= 400:
            log.warning("render %s -> %s", url, resp.status if resp else "no response")
            return None
        html = self.page.content()
        path.write_text(f"{self.page.url}\n{html}", encoding="utf-8")
        return self.page.url, html

    def fetch_json(self, url: str):
        """JSON endpoint via httpx, falling back to Chromium for bot-protected stores."""
        res = get(url)
        if res:
            try:
                return json.loads(res[1])
            except ValueError:
                pass
        _sleep()
        try:
            resp = self.page.goto(url, timeout=60000, wait_until="domcontentloaded")
            if resp is None or resp.status >= 400:
                return None
            return json.loads(self.page.inner_text("body"))
        except Exception:  # noqa: BLE001
            return None

    def fetch(self, url: str) -> tuple[str, str] | None:
        return get(url) or self.render(url)

    # ---------- Ad Library search (no login) ----------

    LIB = "https://www.facebook.com/ads/library/"

    @staticmethod
    def _parse_ads(blob: str) -> list[dict]:
        dec = json.JSONDecoder()
        out = []
        for m in re.finditer(r'\{"ad_archive_id":"', blob):
            try:
                obj, _ = dec.raw_decode(blob, m.start())
            except ValueError:
                continue
            if isinstance(obj, dict) and obj.get("snapshot") is not None:
                out.append(obj)
        return out

    @staticmethod
    def _parse_count(blob: str) -> int | None:
        m = re.search(r'"search_results_connection":\{"count":(\d+)', blob)
        return int(m.group(1)) if m else None

    def _library_query(self, params: str, max_ads: int, scrolls: int = 8) -> tuple[int | None, list[dict]]:
        responses: list = []

        def on_response(resp):  # sync API: only collect here, read bodies in the main loop
            if "graphql" in resp.url:
                responses.append(resp)

        self.page.on("response", on_response)
        try:
            _sleep()
            self.page.goto(f"{self.LIB}?{params}", timeout=60000, wait_until="domcontentloaded")
            self.page.wait_for_timeout(6000)
            html = self.page.content()
            count = self._parse_count(html)
            ads = {a["ad_archive_id"]: a for a in self._parse_ads(html)}
            for _ in range(scrolls):
                if len(ads) >= max_ads:
                    break
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                self.page.wait_for_timeout(random.uniform(2500, 4000))
                for resp in responses:
                    try:
                        body = resp.text()
                    except Exception:  # noqa: BLE001
                        continue
                    if "ad_archive_id" in body:
                        ads.update({a["ad_archive_id"]: a for a in self._parse_ads(body)})
                responses.clear()
        finally:
            self.page.remove_listener("response", on_response)
        return count, list(ads.values())[:max_ads]

    def search(self, keyword: str, country: str = "IL", max_ads: int = 120) -> tuple[int | None, list[dict]]:
        params = (f"active_status=active&ad_type=all&country={country}&is_targeted_country=false"
                  f"&media_type=all&q={quote(keyword)}&search_type=keyword_unordered")
        return self._library_query(params, max_ads)

    def page_ads(self, page_id: str, country: str = "IL", max_ads: int = 30) -> tuple[int | None, list[dict]]:
        params = (f"active_status=active&ad_type=all&country={country}&is_targeted_country=false"
                  f"&media_type=all&search_type=page&view_all_page_id={page_id}")
        return self._library_query(params, max_ads, scrolls=1)

    def ad_snapshot(self, ad_id: str) -> tuple[str, str]:
        """Return (html, body_text) of the ad's Ad Library page. Cached."""
        key = f"adlib:{ad_id}"
        path = _cache_path(key)
        if path.exists():
            text, _, html = path.read_text(encoding="utf-8").partition("\n<!--SPLIT-->\n")
            return html, text
        _sleep()
        self.page.goto(f"https://www.facebook.com/ads/library/?id={ad_id}",
                       timeout=60000, wait_until="domcontentloaded")
        self.page.wait_for_timeout(5000)
        html = self.page.content()
        text = self.page.inner_text("body")
        path.write_text(f"{text}\n<!--SPLIT-->\n{html}", encoding="utf-8")
        return html, text


FB_REDIRECT = re.compile(r"l\.facebook\.com/l\.php\?u=([^&\"'\s]+)")
META_HOSTS = ("facebook.com", "fb.com", "meta.com", "instagram.com", "messenger.com",
              "threads.com", "threads.net", "meta.ai", "muse.ai", "whatsapp.com", "fb.me")


def outbound_links(html: str) -> list[str]:
    """Decode l.facebook.com redirect links, dropping Meta's own properties."""
    out = []
    for m in FB_REDIRECT.finditer(html):
        url = unquote(m.group(1).replace("&amp;", "&"))
        host = (urlparse(url).hostname or "").lower()
        if host and not any(host == h or host.endswith("." + h) for h in META_HOSTS):
            if url not in out:
                out.append(url)
    return out


def unwrap(url: str) -> str:
    if "l.facebook.com/l.php" in url:
        return unquote(parse_qs(urlparse(url).query).get("u", [url])[0])
    return url


def flatten_ad(a: dict) -> dict:
    """Ad Library GraphQL ad -> the flat shape the pipeline uses."""
    snap = a.get("snapshot") or {}
    cards = snap.get("cards") or []
    card = cards[0] if cards else {}
    body = (snap.get("body") or {}).get("text") if isinstance(snap.get("body"), dict) else snap.get("body")
    imgs = [i.get("original_image_url") for i in (snap.get("images") or []) if i.get("original_image_url")]
    imgs += [c.get("original_image_url") for c in cards if c.get("original_image_url")]
    vids = [{"thumb": v.get("video_preview_image_url"), "url": v.get("video_hd_url") or v.get("video_sd_url")}
            for v in (snap.get("videos") or []) + [c for c in cards if c.get("video_sd_url")]]
    return {
        "id": str(a.get("ad_archive_id")),
        "page_id": str(a.get("page_id") or snap.get("page_id")),
        "page_name": a.get("page_name") or snap.get("page_name") or "",
        "page_url": snap.get("page_profile_uri") or "",
        "page_like_count": snap.get("page_like_count"),
        "page_categories": snap.get("page_categories") or [],
        "ad_creative_link_title": snap.get("title") or card.get("title") or "",
        "body": body or card.get("body") or "",
        "link_description": snap.get("link_description") or card.get("link_description") or "",
        "landing_url": snap.get("link_url") or card.get("link_url") or "",
        "cta_type": snap.get("cta_type") or card.get("cta_type") or "",
        "cta_text": snap.get("cta_text") or card.get("cta_text") or "",
        "display_format": snap.get("display_format"),
        "ad_delivery_start_time": a.get("start_date"),
        "platforms": a.get("publisher_platform") or [],
        "collation_count": a.get("collation_count"),
        "images": imgs,
        "videos": [v for v in vids if v["url"] or v["thumb"]],
        "currency": a.get("currency") or "",
        "ad_snapshot_url": f"https://www.facebook.com/ads/library/?id={a.get('ad_archive_id')}",
    }
