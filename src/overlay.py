"""Hebrew typography on generated (text-free) images, rendered by Chromium.

Design directions (not one template with different photos): each is its own typographic system
built on Eran's fonts — Optimum Light/Regular/Black for all type, Idealist (handwriting) only for a
designer signature or short personal note.

  contrast  Black keyword line vs. Light line
  quiet     perfume-ad restraint: small Light text + handwritten signature
  stack     oversized Black stacked headline
  note      the designer's handwritten note + small product line
  cover     thin frame + masthead, magazine cover feel
  panel     solid colour panel next to the photo: text never touches the product
  label     museum label: small headline, hairline, detail list

find_zone() scores candidate text areas by visual detail on the real image, so text lands on empty
space; directions that need a big empty area fall back to `panel` when there isn't one.
"""
from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from PIL import Image, ImageFilter, ImageOps, ImageStat
from playwright.sync_api import sync_playwright

from .common import ROOT, load_config

SIZES = {"1:1": (1080, 1080), "4:5": (1080, 1350), "9:16": (1080, 1920)}
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True)
FONT_DIR = ROOT / "assets" / "fonts"

ZONES = {  # (x, y, w, h) as canvas fractions. RTL: text starts on the right.
    "top":          (0.08, 0.06, 0.84, 0.26),
    "bottom":       (0.08, 0.68, 0.84, 0.24),
    "top_right":    (0.40, 0.06, 0.54, 0.30),
    "top_left":     (0.06, 0.06, 0.54, 0.30),
    "bottom_right": (0.40, 0.64, 0.54, 0.28),
    "bottom_left":  (0.06, 0.64, 0.54, 0.28),
}
SAFE_916 = (250 / 1920, 340 / 1920)  # Stories/Reels UI

DIRECTIONS = {
    "contrast": dict(zones=["top_right", "top_left", "bottom_right", "bottom_left"], big=True),
    "quiet":    dict(zones=["bottom", "top"], big=False),
    "stack":    dict(zones=["top", "bottom"], big=True),
    "note":     dict(zones=["top", "bottom", "top_right", "top_left"], big=False),
    "cover":    dict(zones=["top", "bottom"], big=True),
    "panel":    dict(zones=[], big=False),
    "label":    dict(zones=["top_right", "top_left", "bottom_right", "bottom_left"], big=False),
}
ORDER = ["contrast", "quiet", "panel", "stack", "note", "cover", "label"]
BUSY = {True: 23.0, False: 31.0}   # max zone detail score for big / small type
MAX_PANELS = 4                       # per lead — panels are the safe fallback, not the look


def _canvas(img_path: str, w: int, h: int) -> Image.Image:
    return ImageOps.fit(Image.open(img_path).convert("RGB"), (w, h), Image.LANCZOS)


def _skin_ratio(im: Image.Image) -> float:
    """Share of skin-tone pixels (YCbCr rule) — faces/necks/hands must stay clear of text."""
    ycc = im.convert("YCbCr")
    px = list(ycc.getdata())
    if not px:
        return 0.0
    skin = sum(1 for y, cb, cr in px if 80 <= cb <= 125 and 138 <= cr <= 170 and y > 60)
    return skin / len(px)


def _zone_box(name: str, w: int, h: int, fmt: str) -> tuple[int, int, int, int]:
    x, y, zw, zh = ZONES[name]
    if fmt == "9:16":
        top, bottom = SAFE_916
        y = max(y, top)
        if y + zh > 1 - bottom:
            y = 1 - bottom - zh
    return int(x * w), int(y * h), int((x + zw) * w), int((y + zh) * h)


def find_zone(canvas: Image.Image, fmt: str, allowed: list[str], people: bool = False):
    """(zone, box, mean_luma, score) of the allowed zone with the least visual detail."""
    w, h = canvas.size
    small = canvas.resize((w // 4, h // 4))
    gray = small.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    best = None
    for name in allowed:
        box = _zone_box(name, w, h, fmt)
        sbox = tuple(v // 4 for v in box)
        lum = ImageStat.Stat(gray.crop(sbox))
        score = (ImageStat.Stat(edges.crop(sbox)).mean[0] + 0.35 * lum.stddev[0]
                 + (60 * _skin_ratio(small.crop(sbox)) if people else 0))  # skin looks "empty" to edges
        if best is None or score < best[3]:
            best = (name, box, lum.mean[0], score)
    return best


def _panel_side(canvas: Image.Image, fmt: str) -> tuple[str, str]:
    """Panel on the emptier side; object-position keeps the subject in the visible part."""
    w, h = canvas.size
    small = canvas.resize((w // 8, h // 8))
    edges = small.convert("L").filter(ImageFilter.FIND_EDGES)
    ew, eh = edges.size
    px = edges.load()
    tot = sx = sy = 0
    for y in range(eh):
        for x in range(ew):
            v = px[x, y]
            tot += v; sx += v * x; sy += v * y
    cx = (sx / tot / ew) if tot else 0.5
    cy = (sy / tot / eh) if tot else 0.5
    # bottom panel in every format: cropping top/bottom keeps the product, side panels cut it
    return "bottom", f"{int(cx * 100)}% {int(min(max(cy, 0.2), 0.8) * 100)}%"


def _palette(canvas: Image.Image) -> tuple[str, str]:
    """(paper, ink) for panels: a muted tone taken from the photo + contrasting ink."""
    q = canvas.resize((64, 64)).quantize(6)
    pal = q.getpalette()[:18]
    counts = sorted(q.getcolors(), reverse=True)
    r, g, b = pal[counts[0][1] * 3: counts[0][1] * 3 + 3]
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    # push toward a calm, printable tone
    if luma < 128:
        r, g, b = (int(v * 0.55) for v in (r, g, b))
        return f"rgb({r},{g},{b})", "#f3ebdd"
    r, g, b = (int(v + (245 - v) * 0.6) for v in (r, g, b))
    return f"rgb({r},{g},{b})", "#231a12"


def _fonts() -> dict:
    ov = load_config().get("overlay", {}).get("fonts", {})
    return {k: (FONT_DIR / v).resolve().as_uri() for k, v in ov.items()}


def choose_direction(canvas: Image.Image, fmt: str, preferred: list[str], people: bool = False,
                     allow_panel: bool = True) -> tuple[str, dict]:
    """First preferred direction whose best zone is empty enough; `panel` always fits.
    Without a panel allowance, take the overlay direction with the emptiest zone."""
    best = None
    for d in preferred:
        spec = DIRECTIONS[d]
        if not spec["zones"]:
            if allow_panel:
                return d, {}
            continue
        zone, box, luma, score = find_zone(canvas, fmt, spec["zones"], people)
        if score <= BUSY[spec["big"]]:
            return d, dict(zone=zone, box=box, luma=luma)
        margin = score - BUSY[spec["big"]]
        if best is None or margin < best[0]:
            best = (margin, d, dict(zone=zone, box=box, luma=luma))
    if allow_panel or best is None:
        return "panel", {}
    return best[1], best[2]


def render(jobs: list[dict]) -> list[str]:
    """jobs: {img, out, headline, sub, note, signature, brand, format, directions:[...]}"""
    fonts = _fonts()
    outs = []
    import os
    proxy = os.environ.get("HTTPS_PROXY")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium",
                              proxy={"server": proxy} if proxy else None)
        for j in jobs:
            fmt = j.get("format", "4:5")
            w, h = SIZES[fmt]
            canvas = _canvas(j["img"], w, h)
            # a single pre-chosen overlay direction is final (render_lead already weighed it)
            final = len(j["directions"]) == 1 and j["directions"][0] != "panel"
            direction, z = choose_direction(canvas, fmt, j["directions"], j.get("people", False),
                                            allow_panel=not final)
            box = z.get("box", (0, 0, w, h))
            top = box[1] < h / 2
            dark = z.get("luma", 0) < 128
            paper, ink = _palette(canvas)
            obj_pos, panel_side = "center", "right"
            if direction == "panel":
                panel_side, obj_pos = _panel_side(canvas, fmt)
            else:
                ink = "#f4ecdf" if dark else "#1f1812"
            # brand line colour from the strip where it sits
            by = int(h * 0.9) if top else int(h * 0.03)
            brand_dark = ImageStat.Stat(canvas.convert("L").crop((w // 3, by, 2 * w // 3, by + int(h * .06)))).mean[0] < 140
            html = env.get_template("overlay.html.j2").render(
                w=w, h=h, img=Path(j["img"]).resolve().as_uri(), fonts=fonts, direction=direction,
                headline=j["headline"], sub=j.get("sub"), note=j.get("note"), signature=j.get("signature"),
                brand=j.get("brand", ""), box=box, top=top, ink=ink, paper=paper, accent=ink,
                scrim_on=True, scrim="rgba(0,0,0,.32)" if dark else "rgba(255,250,242,.42)",
                brand_color="#f4ecdf" if brand_dark else "#231a12",
                obj_pos=obj_pos, panel_side=panel_side)
            tmp = Path(j["out"]).with_suffix(".html")
            Path(j["out"]).parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(tmp.resolve().as_uri())
            pg.wait_for_selector("body[data-ready='1']", timeout=15000)
            pg.wait_for_timeout(200)
            pg.screenshot(path=j["out"], clip={"x": 0, "y": 0, "width": w, "height": h})
            pg.close()
            tmp.unlink()
            j["direction"], j["zone"] = direction, z.get("zone", panel_side)
            outs.append(j["out"])
        b.close()
    return outs


def render_lead(lead: dict) -> list[str]:
    """Compose all new_ads[]: every angle gets 4 different directions, all 7 used across the set."""
    from .common import OUTPUT
    base = OUTPUT / lead["lead_id"]
    brand = lead["business"].get("name_he") or lead["meta"]["page_name"]
    signature = (lead["business"].get("owner_name") or "").split(" ")[0] or \
        load_config().get("overlay", {}).get("default_signature", "")
    jobs, ads, used, k = [], [], {}, 0
    for ad in lead["new_ads"]:
        raw = base / ad["image_raw"]
        if not raw.exists():
            continue
        taken = used.setdefault(ad["angle_id"], [])
        forced = ad.get("layout", {}).get("direction")
        rot = ORDER[k % len(ORDER):] + ORDER[:k % len(ORDER)]
        k += 1
        prefs = [forced] if forced else [d for d in rot if d not in taken]
        people = ad.get("has_people", False)
        n_panels = sum(1 for j in jobs if j["directions"] == ["panel"])
        direction, _ = choose_direction(_canvas(str(raw), *SIZES[ad["format"]]), ad["format"], prefs, people,
                                        allow_panel=n_panels < MAX_PANELS)
        taken.append(direction)
        jobs.append(dict(img=str(raw), out=str(base / ad["image"]), headline=ad["overlay"],
                         sub=ad.get("overlay_sub"), note=ad.get("note"), signature=signature,
                         brand=brand, format=ad["format"], directions=[direction], people=people))
        ads.append(ad)
    outs = render(jobs)
    for ad, j in zip(ads, jobs):
        ad.setdefault("layout", {}).update(rendered_direction=j["direction"], rendered_zone=j["zone"])
    return outs
