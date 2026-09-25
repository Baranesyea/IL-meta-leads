"""Polite, cached fetching: httpx for regular sites, Playwright for the Ad Library."""
from __future__ import annotations

import hashlib
import random
import re
import time
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

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
    if r.status_code >= 400 or "html" not in r.headers.get("content-type", "html"):
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
