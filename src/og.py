"""WhatsApp / social link previews for the client pages.

The site is a SPA: every /p/<slug> serves the same index.html (title "IL Meta", no og tags), and WhatsApp's crawler does
not run JS, so a /p/ link shows up bare. Base44 hosting does serve static .html files from public/, so for every client
page we write a static twin:

  public/og/<slug>.jpg     1200x630 screenshot of the live page's hero (our headline + the business name in the bar)
  public/s/<slug>.html     og:title / og:description / og:image, then a redirect to /p/<slug>

Eran sends https://il-meta.base44.app/s/<slug>.html (message2 and the share button use it too).
Run after a page is live:  python -m src.og [slug ...]   (no slugs = every page in data.js)
"""
import html
import json
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

WEB = Path(__file__).resolve().parent.parent / "web" / "base44"
SITE = "https://il-meta.base44.app"
CHROMIUM = "/opt/pw-browsers/chromium"


def reports() -> dict:
    s = (WEB / "src" / "reports" / "data.js").read_text()
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


def share_url(slug: str) -> str:
    return f"{SITE}/s/{slug}.html"


def texts(r: dict) -> tuple[str, str]:
    name = r["business"]["name"]
    return (f"הוכן במיוחד עבור {name}",
            f"עברנו על המודעות שלכם והכנו לכם {len(r['ads'])} מודעות חדשות. הדוח והמודעות, בחינם.")


def shoot(slugs: list[str]) -> None:
    out = WEB / "public" / "og"
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROMIUM if Path(CHROMIUM).exists() else None)
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        for slug in slugs:
            pg.goto(f"{SITE}/p/{slug}", wait_until="networkidle")
            pg.add_style_tag(content=".bar .share{display:none!important}")
            pg.wait_for_timeout(3000)  # hero fade-ins
            png = out / f"{slug}.png"
            pg.screenshot(path=str(png))
            Image.open(png).convert("RGB").save(out / f"{slug}.jpg", quality=82, optimize=True, progressive=True)
            png.unlink()
        b.close()


def share_page(slug: str, r: dict) -> str:
    title, desc = (html.escape(x) for x in texts(r))
    img, url, to = f"{SITE}/og/{slug}.jpg", share_url(slug), f"/p/{slug}"
    return f"""<!doctype html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:secure_url" content="{img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
<script>location.replace("{to}" + location.hash);</script>
<style>body{{margin:0;background:#0d0d0d;color:#eee;font:16px system-ui,sans-serif;display:grid;place-items:center;min-height:100vh}}a{{color:#eee}}</style>
</head>
<body><a href="{to}">{title}</a></body>
</html>
"""


def run(slugs: list[str] | None = None) -> list[str]:
    reps = reports()
    slugs = slugs or list(reps)
    shoot(slugs)
    d = WEB / "public" / "s"
    d.mkdir(parents=True, exist_ok=True)
    for slug in slugs:
        (d / f"{slug}.html").write_text(share_page(slug, reps[slug]))
    return [share_url(s) for s in slugs]


if __name__ == "__main__":
    for u in run(sys.argv[1:] or None):
        print(u)
