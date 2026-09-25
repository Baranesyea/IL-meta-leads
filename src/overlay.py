"""Hebrew text overlay on generated (text-free) images: HTML+CSS rendered by Chromium.

Two things keep the typography from looking the same on every ad and from covering the product:
  * STYLES — several typographic layouts; each ad gets one (varied within an angle).
  * find_zone() — scores candidate text zones by visual detail (edge density) on the actual
    image and puts the text in the emptiest allowed zone; text colour follows the zone's brightness.
"""
from __future__ import annotations

import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageFilter, ImageOps, ImageStat
from playwright.sync_api import sync_playwright

from .common import ROOT, load_config

SIZES = {"1:1": (1080, 1080), "4:5": (1080, 1350), "9:16": (1080, 1920)}
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True)
FONT_DIR = ROOT / "assets" / "fonts"

# Candidate text zones as fractions of the canvas: (x, y, w, h). RTL: "right" = start.
ZONES = {
    "top":          (0.08, 0.05, 0.84, 0.26),
    "bottom":       (0.08, 0.66, 0.84, 0.26),
    "top_right":    (0.46, 0.05, 0.48, 0.30),
    "top_left":     (0.06, 0.05, 0.48, 0.30),
    "bottom_right": (0.46, 0.63, 0.48, 0.30),
    "bottom_left":  (0.06, 0.63, 0.48, 0.30),
    "right_col":    (0.52, 0.10, 0.42, 0.62),
    "left_col":     (0.06, 0.10, 0.42, 0.62),
}
# Stories/Reels: keep clear of the top 250px and bottom 340px UI
SAFE_916 = (250 / 1920, 340 / 1920)

# Typographic styles. zones = where this style may sit; the emptiest one wins.
STYLES = {
    "editorial":  dict(zones=["top", "bottom"], align="center", size=78, sub=26, rule=False, band=False, frame=False),
    "corner":     dict(zones=["top_right", "top_left", "bottom_right", "bottom_left"], align="start", size=54, sub=22, rule=True, band=False, frame=False),
    "column":     dict(zones=["right_col", "left_col"], align="start", size=58, sub=22, rule=True, band=False, frame=False),
    "bigtype":    dict(zones=["top", "bottom"], align="start", size=118, sub=28, rule=False, band=False, frame=False),
    "band":       dict(zones=["bottom"], align="center", size=60, sub=24, rule=False, band=True, frame=False),
    "frame":      dict(zones=["top", "bottom"], align="center", size=64, sub=22, rule=False, band=False, frame=True),
}
BUSY = 22.0  # zone score above which a full-width text block would sit on the subject
ROTATION = ["editorial", "corner", "bigtype", "column", "band", "frame"]


def _canvas(img_path: str, w: int, h: int) -> Image.Image:
    im = Image.open(img_path).convert("RGB")
    return ImageOps.fit(im, (w, h), Image.LANCZOS)  # same crop as CSS object-fit: cover


def find_zone(canvas: Image.Image, fmt: str, allowed: list[str]) -> tuple[str, tuple[int, int, int, int], float, float]:
    """Return (zone_name, box_px, mean_luma) of the allowed zone with the least visual detail."""
    w, h = canvas.size
    small = canvas.resize((w // 4, h // 4))
    edges = small.convert("L").filter(ImageFilter.FIND_EDGES)
    best = None
    for name in allowed:
        x, y, zw, zh = ZONES[name]
        if fmt == "9:16":
            top, bottom = SAFE_916
            y = max(y, top)
            if y + zh > 1 - bottom:
                y = 1 - bottom - zh
        box = (int(x * w), int(y * h), int((x + zw) * w), int((y + zh) * h))
        sbox = tuple(v // 4 for v in box)
        detail = ImageStat.Stat(edges.crop(sbox)).mean[0]
        luma_stat = ImageStat.Stat(small.convert("L").crop(sbox))
        # busy AND high-variance areas are where products and faces live
        score = detail + 0.35 * luma_stat.stddev[0]
        if best is None or score < best[0]:
            best = (score, name, box, luma_stat.mean[0])
    score, name, box, luma = best
    return name, box, luma, score


def _fonts() -> dict:
    ov = load_config().get("overlay", {})
    fonts = {k: dict(ov.get(k) or {}) for k in ("headline_font", "sub_font", "brand_font")}
    for f in fonts.values():
        if f.get("file"):
            f["file_uri"] = (FONT_DIR / f["file"]).resolve().as_uri()
    return fonts


def render(jobs: list[dict]) -> list[str]:
    """jobs: {img, out, headline, sub, brand, format, style?, color?}"""
    fonts = _fonts()
    outs = []
    proxy = os.environ.get("HTTPS_PROXY")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                              proxy={"server": proxy} if proxy else None)
        for j in jobs:
            fmt = j.get("format", "4:5")
            w, h = SIZES[fmt]
            style_name = j.get("style") or "editorial"
            st = STYLES[style_name]
            canvas = _canvas(j["img"], w, h)
            zone, box, luma, score = find_zone(canvas, fmt, j.get("zones") or st["zones"])
            # full-width styles only where that band is really empty; else fall back to a corner caption
            if style_name in ("band", "bigtype", "editorial", "frame") and score > BUSY and not j.get("zones"):
                style_name, st = "corner", STYLES["corner"]
                zone, box, luma, score = find_zone(canvas, fmt, st["zones"])
            j["style"] = style_name
            dark_bg = luma < 128
            # brand line sits at the opposite edge; pick its colour from that strip's brightness
            by = int(h * 0.9) if box[1] < h / 2 else int(h * 0.02)
            brand_dark = ImageStat.Stat(canvas.convert("L").crop((w // 3, by, 2 * w // 3, by + int(h * 0.07)))).mean[0] < 140
            color = j.get("color") or ("#f4ecdf" if dark_bg else "#231a12")
            html = env.get_template("overlay.html.j2").render(
                w=w, h=h, img=Path(j["img"]).resolve().as_uri(), headline=j["headline"], sub=j.get("sub"),
                brand=j.get("brand", ""), st=st, style=style_name, zone=zone, box=box, color=color,
                dark_bg=dark_bg, brand_dark=brand_dark, size=j.get("size") or st["size"],
                fonts=list(fonts.values()), hf=fonts["headline_font"], sf=fonts["sub_font"], bf=fonts["brand_font"])
            tmp = Path(j["out"]).with_suffix(".html")
            Path(j["out"]).parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(tmp.resolve().as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(400)
            pg.screenshot(path=j["out"], clip={"x": 0, "y": 0, "width": w, "height": h})
            pg.close()
            tmp.unlink()
            j["zone"] = zone
            outs.append(j["out"])
        b.close()
    return outs


def render_lead(lead: dict) -> list[str]:
    """Compose every new_ads[] image. Styles rotate so the 4 ads of an angle all look different."""
    from .common import OUTPUT
    base = OUTPUT / lead["lead_id"]
    brand = lead["business"].get("name_he") or lead["meta"]["page_name"]
    jobs, used = [], {}
    for ad in lead["new_ads"]:
        raw = base / ad["image_raw"]
        if not raw.exists():
            continue
        lay = ad.get("layout", {})
        taken = used.setdefault(ad["angle_id"], [])
        style, zones = lay.get("style"), lay.get("zones")
        if not style:
            w, h = SIZES[ad["format"]]
            canvas = _canvas(str(raw), w, h)
            a_idx = int(ad["angle_id"].lstrip("A") or 1) - 1
            order = ROTATION[a_idx:] + ROTATION[:a_idx]
            # first style not yet used in this angle whose best zone is empty enough for it
            for cand in [c for c in order if c not in taken] + ["corner", "column"]:
                zone, _, _, score = find_zone(canvas, ad["format"], STYLES[cand]["zones"])
                limit = BUSY if cand in ("band", "bigtype", "editorial", "frame") else BUSY + 8
                if score <= limit:
                    style, zones = cand, [zone]
                    break
            else:
                style = "corner"
        taken.append(style)
        jobs.append(dict(img=str(raw), out=str(base / ad["image"]), headline=ad["overlay"],
                         sub=ad.get("overlay_sub"), brand=brand, format=ad["format"], style=style,
                         size=lay.get("size_override"), zones=zones))
    outs = render(jobs)
    for ad, j in zip([a for a in lead["new_ads"] if (base / a["image_raw"]).exists()], jobs):
        ad.setdefault("layout", {})["rendered_style"] = j["style"]
        ad["layout"]["rendered_zone"] = j.get("zone")
    return outs
