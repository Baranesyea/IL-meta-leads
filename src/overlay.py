"""Hebrew text overlay on generated (text-free) images: HTML+CSS rendered by Chromium."""
from __future__ import annotations

import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

from .common import ROOT, load_config

SIZES = {"1:1": (1080, 1080), "4:5": (1080, 1350), "9:16": (1080, 1920)}
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True)


def render(jobs: list[dict]) -> list[str]:
    """jobs: {img, out, headline, sub, brand, format, pos(top|bottom), color, shade, size}"""
    ov = load_config().get("overlay", {})
    fonts = {k: dict(ov.get(k) or {}) for k in ("headline_font", "sub_font", "brand_font")}
    for f in fonts.values():
        if f.get("file"):
            f["file_uri"] = (ROOT / "assets" / "fonts" / f["file"]).resolve().as_uri()
    outs = []
    proxy = os.environ.get("HTTPS_PROXY")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                              proxy={"server": proxy} if proxy else None)
        for j in jobs:
            w, h = SIZES[j.get("format", "4:5")]
            html = env.get_template("overlay.html.j2").render(
                w=w, h=h, img=Path(j["img"]).resolve().as_uri(), headline=j["headline"], sub=j.get("sub"),
                brand=j.get("brand", ""), pos=j.get("pos", "top"), color=j.get("color", "#f4ead8"),
                shade=j.get("shade", "rgba(0,0,0,.45)"), size=j.get("size", 76),
                fonts=list(fonts.values()), hf=fonts["headline_font"], sf=fonts["sub_font"], bf=fonts["brand_font"],
                # keep text clear of the top UI zone on Stories/Reels
                top_px={"9:16": 250, "1:1": 80}.get(j.get("format", "4:5"), 96))
            tmp = Path(j["out"]).with_suffix(".html")
            Path(j["out"]).parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(tmp.resolve().as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(500)
            pg.screenshot(path=j["out"], clip={"x": 0, "y": 0, "width": w, "height": h})
            pg.close()
            tmp.unlink()
            outs.append(j["out"])
        b.close()
    return outs


def render_lead(lead: dict) -> list[str]:
    """Compose every new_ads[] image: raw generated image + Hebrew overlay."""
    from .common import OUTPUT
    base = OUTPUT / lead["lead_id"]
    brand = lead["business"].get("name_he") or lead["meta"]["page_name"]
    jobs = []
    for ad in lead["new_ads"]:
        raw = base / ad["image_raw"]
        if not raw.exists():
            continue
        lay = ad.get("layout", {})
        jobs.append(dict(img=str(raw), out=str(base / ad["image"]), headline=ad["overlay"],
                         sub=ad.get("overlay_sub"), brand=brand, format=ad["format"], pos=lay.get("pos", "top"),
                         color=lay.get("color"), shade=lay.get("shade"), size=lay.get("size", 76)))
    return render(jobs)
