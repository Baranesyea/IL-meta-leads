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

from .common import ROOT, get_logger, load_config

log = get_logger()

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
    "mid_right":    (0.54, 0.00, 0.40, 0.28),   # beside the subject, at any height
    "mid_left":     (0.06, 0.00, 0.40, 0.28),
}
SAFE_916 = (250 / 1920, 340 / 1920)  # Stories/Reels UI

DIRECTIONS = {
    "contrast": dict(zones=["top_right", "top_left", "bottom_right", "bottom_left", "mid_right", "mid_left"], big=True),
    "quiet":    dict(zones=["bottom", "top"], big=False),
    "stack":    dict(zones=["top", "bottom"], big=True),
    "note":     dict(zones=["top", "bottom"], big=False),
    "cover":    dict(zones=["top", "bottom"], big=True),
    "panel":    dict(zones=[], big=False),
    "label":    dict(zones=["top_right", "top_left", "bottom_right", "bottom_left", "mid_right", "mid_left"], big=False),
}
ORDER = ["contrast", "quiet", "stack", "note", "cover", "label"]   # panel: legacy only, never chosen
BUSY = {True: 23.0, False: 31.0}   # max zone detail score for big / small type
MAX_PANELS = 0                       # Eran: a photo cut short by a colour strip is not premium — full bleed only


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


def _zone_boxes(name: str, w: int, h: int, fmt: str, protect=None) -> list[tuple[int, int, int, int]]:
    """Candidate text boxes (px) for a zone: the zone's column slid vertically over the canvas
    (top zones in the upper half, bottom zones in the lower half, mid zones anywhere), at full
    height first and shorter if needed, keeping clear of every protected region (product, faces,
    hands). Text lives in whatever space the photo leaves — never a strip cut off the photo."""
    x, y0, zw, zh0 = ZONES[name]
    top_m, bot_m = SAFE_916 if fmt == "9:16" else (0.05, 0.05)
    out = []
    for zh in (zh0, 0.22, 0.17, 0.14):
        if zh > zh0:
            continue
        ys = [top_m + i * 0.02 for i in range(int((1 - bot_m - zh - top_m) / 0.02) + 1)]
        for y in ys:
            if name.startswith("top") and y > 0.5 - zh / 2:
                continue
            if name.startswith("bottom") and y + zh / 2 < 0.5:
                continue
            box = (int(x * w), int(y * h), int((x + zw) * w), int((y + zh) * h))
            if all(_overlap(box, r, w, h) <= 0.02 for r in (protect or [])):
                out.append(box)
        if out:
            return out
    return []


def detect_faces(canvas: Image.Image) -> list[tuple[float, float, float, float]]:
    """Backup face finder (Haar, frontal + both profiles) → fractional boxes, padded."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return []
    w, h = canvas.size
    g = np.array(canvas.convert("L"))
    boxes = []
    for name in ("haarcascade_frontalface_default.xml", "haarcascade_profileface.xml"):
        c = cv2.CascadeClassifier(cv2.data.haarcascades + name)
        for flip in (False, True):
            img = np.ascontiguousarray(np.fliplr(g)) if flip else g
            for x, y, fw, fh in c.detectMultiScale(img, 1.1, 6, minSize=(w // 8, w // 8)):
                if flip:
                    x = w - x - fw
                boxes.append((max(0, (x - .15 * fw) / w), max(0, (y - .2 * fh) / h),
                              min(1, (x + 1.15 * fw) / w), min(1, (y + 1.4 * fh) / h)))
            if name.startswith("haarcascade_frontal"):
                break
    return boxes


PROTECT_PAD = 0.02    # breathing room around product / faces: text never sits tight against the jewel


def _overlap(box, region, w, h, pad: float = PROTECT_PAD) -> float:
    """Share of the zone box covered by a fractional region (grown by `pad` on every side)."""
    x0, y0, x1, y1 = box
    rx0, ry0, rx1, ry1 = ((region[0] - pad) * w, (region[1] - pad) * h,
                          (region[2] + pad) * w, (region[3] + pad) * h)
    ix = max(0, min(x1, rx1) - max(x0, rx0))
    iy = max(0, min(y1, ry1) - max(y0, ry0))
    return ix * iy / max(1, (x1 - x0) * (y1 - y0))


def find_zone(canvas: Image.Image, fmt: str, allowed: list[str], people: bool = False, protect=None):
    """(zone, box, mean_luma, score) of the allowed zone with the least visual detail."""
    w, h = canvas.size
    small = canvas.resize((w // 4, h // 4))
    gray = small.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    best = None
    for name in allowed:
        boxes = _zone_boxes(name, w, h, fmt, protect)
        forced = not boxes
        if forced:   # no clear spot: the plain zone, flagged so callers only take it as a last resort
            boxes = _zone_boxes(name, w, h, fmt, None)[:1] or []
        for box in boxes:
            sbox = tuple(v // 4 for v in box)
            lum = ImageStat.Stat(gray.crop(sbox))
            score = (ImageStat.Stat(edges.crop(sbox)).mean[0] + 0.35 * lum.stddev[0]
                     + (60 * _skin_ratio(small.crop(sbox)) if people else 0))  # skin looks "empty" to edges
            # edge placement reads as deliberate layout; the exact middle of the frame does not
            score += 6 * (1 - abs((box[1] + box[3]) / 2 / h - 0.5) * 2)
            if forced:
                score += 1000
            if best is None or score < best[3]:
                best = (name, box, lum.mean[0], score)
    return best if best else (None, None, 0, 10_000)


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


LIGHT_INK, DARK_INK = "#f4ecdf", "#1f1812"
MIN_CONTRAST = {True: 4.5, False: 7.0}   # big Black type: WCAG AA; thin/script/small type: AAA
MAX_SCRIM = 0.82            # full-width gradient only — no boxes/plates behind text (Eran: "a compromise")


def _lin(v: float) -> float:
    v /= 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def _contrast(l1: float, l2: float) -> float:
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def legibility(canvas: Image.Image, box, big: bool = False) -> dict:
    """Measure the real pixels under the text box and pick the ink + the least cover that keeps the
    text at >= MIN_CONTRAST: a band-shaped scrim of the needed strength. Worst case = 90th/10th
    luminance percentile of the box (a few stray pixels don't force a heavy wash). Both inks are
    tried and the one needing less cover wins — the photo stays as untouched as possible."""
    g = canvas.convert("L").crop(tuple(int(v) for v in box)).resize((96, 96))
    px = sorted(g.getdata())
    lo, hi = px[int(len(px) * 0.10)], px[int(len(px) * 0.90)]
    mean = sum(px) / len(px)
    busy = ImageStat.Stat(g).stddev[0] > 38 or ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES).crop((2, 2, 94, 94))).mean[0] > 14

    def need(l_ink: float, worst: int, cover: int) -> float:
        for a in [x / 100 for x in range(0, 96, 2)]:
            v = worst * (1 - a) + cover * a       # sRGB-space compositing, like the browser
            if _contrast(l_ink, _lin(v)) >= MIN_CONTRAST[big]:
                return a
        return 0.95

    l_light = 0.2126 * _lin(0xf4) + 0.7152 * _lin(0xec) + 0.0722 * _lin(0xdf)
    l_dark = 0.2126 * _lin(0x1f) + 0.7152 * _lin(0x18) + 0.0722 * _lin(0x12)
    n_light = need(l_light, hi, 0)       # light ink: brightest pixels, darkened toward black
    n_dark = need(l_dark, lo, 246)       # dark ink: darkest pixels, lifted toward ivory
    light = n_light < n_dark or (n_light == n_dark and mean < 128)
    n = n_light if light else n_dark
    rgb = "0,0,0" if light else "250,246,238"
    alpha = round(min(max(n + 0.06, 0.14) + (0.08 if busy else 0), MAX_SCRIM), 2)
    return dict(ink=LIGHT_INK if light else DARK_INK, plate=False, plate_bg=None,
                scrim=f"rgba({rgb},{alpha})", luma=mean)


def brand_line(canvas: Image.Image, top: bool) -> str | None:
    """Colour for the small brand line (opposite edge to the text), or None to drop it when the
    strip is busy — Meta already shows the page name above every ad, a lost brand line costs nothing."""
    w, h = canvas.size
    y = int(h * 0.9) if top else int(h * 0.025)
    strip = canvas.convert("L").crop((w // 4, y, 3 * w // 4, y + int(h * 0.05))).resize((96, 16))
    edges = strip.filter(ImageFilter.FIND_EDGES).crop((2, 2, 94, 14))   # FIND_EDGES lights up the border
    if ImageStat.Stat(strip).stddev[0] > 22 or ImageStat.Stat(edges).mean[0] > 10:
        return None
    px = sorted(strip.getdata())
    lo, hi = px[int(len(px) * 0.05)], px[int(len(px) * 0.95)]
    light = _contrast(_lin(0xf4), _lin(hi))
    dark = _contrast(_lin(lo), _lin(0x1f))
    best = max(light, dark)
    if best < MIN_CONTRAST[False]:
        return None
    return LIGHT_INK if light >= dark else "#231a12"


def _fonts() -> dict:
    ov = load_config().get("overlay", {}).get("fonts", {})
    return {k: (FONT_DIR / v).resolve().as_uri() for k, v in ov.items()}


def choose_direction(canvas: Image.Image, fmt: str, preferred: list[str], people: bool = False,
                     allow_panel: bool = True, protect=None, force: bool = False) -> tuple[str, dict]:
    """First preferred direction whose best zone is empty enough; `panel` always fits.
    Without a panel allowance, take the overlay direction with the emptiest zone."""
    best = None
    for d in preferred:
        spec = DIRECTIONS[d]
        if not spec["zones"]:
            if allow_panel:
                return d, {}
            continue
        zone, box, luma, score = find_zone(canvas, fmt, spec["zones"], people, protect)
        if score >= 1000 and not force:
            continue
        if score <= BUSY[spec["big"]]:
            return d, dict(zone=zone, box=box, luma=luma)
        margin = score - BUSY[spec["big"]]
        if best is None or margin < best[0]:
            best = (margin, d, dict(zone=zone, box=box, luma=luma))
    if allow_panel or best is None:   # nothing clear of the subject → panel (never overlaps)
        return "panel", {}
    return best[1], best[2]


# main line of each look (what must read on a phone) + the box the text really occupies
MEASURE_JS = """() => {
  const main = {contrast: '.l1', stack: '.l', quiet: '.hl', cover: '.hl', label: '.hl', panel: '.hl', note: '.hand'};
  const d = document.querySelector('.ad').classList[1];
  const els = [...document.querySelectorAll(main[d] || '.hl')].filter(e => e.offsetParent && e.textContent.trim());
  const px = els.length ? Math.max(...els.map(e => parseFloat(getComputedStyle(e).fontSize))) : 0;
  let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1;
  document.querySelectorAll('.zone *, .pnl *').forEach(e => {
    if (!e.offsetParent) return;
    e.childNodes.forEach(t => {        // every text run, also inside a headline split by <br>
      if (t.nodeType !== 3 || !t.textContent.trim()) return;
      const rg = document.createRange(); rg.selectNodeContents(t);   // the letters, not the block
      const r = rg.getBoundingClientRect(); if (!r.width) return;
      x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom);
    });
  });
  return {main_px: px, text_box: x1 < 0 ? null : [x0, y0, x1, y1]};
}"""
MIN_MAIN_PX = {"note": 92}   # script needs more size to read
MIN_MAIN_PX_DEFAULT = 78     # on a 1080 canvas ≈ 28px on a phone-width feed


def crossing_lines(canvas: Image.Image, box) -> float:
    """How strongly a straight edge (a wall corner, ceiling line, window frame, shelf) runs through the
    text box: the largest share of one row or column of the box where the photo steps in brightness.
    Letters laid over such a line read broken on a phone even when the average contrast is fine."""
    import numpy as np
    w, h = canvas.size
    x0, y0, x1, y1 = (int(v) for v in box)
    x0, y0, x1, y1 = max(x0 - 12, 0), max(y0 - 12, 0), min(x1 + 12, w), min(y1 + 12, h)
    if x1 - x0 < 16 or y1 - y0 < 16:
        return 0.0
    g = np.asarray(canvas.convert("L").filter(ImageFilter.GaussianBlur(2)).crop((x0, y0, x1, y1)), dtype=float)
    dy = np.abs(g[4:, :] - g[:-4, :])       # soft architectural edges step over a few pixels
    dx = np.abs(g[:, 4:] - g[:, :-4])
    return float(max((dy > LINE_STEP).mean(1).max(), (dx > LINE_STEP).mean(0).max()))


LINE_STEP = 5          # brightness step (0-255) that reads as an edge behind thin type
MAX_LINE = 0.5         # above this the ad is flagged for a look at phone size (not a gate: soft wall
                       # shadows score high and diagonal soffits low — the eye decides, then regenerate)


def _legible(j: dict) -> bool:
    """Rendered main line big enough, and the text itself clear of every protected region."""
    m = j.get("measured") or {}
    if m.get("main_px", 0) < MIN_MAIN_PX.get(j.get("direction"), MIN_MAIN_PX_DEFAULT):
        return False
    w, h = SIZES[j.get("format", "4:5")]
    tb = m.get("text_box")
    return not (tb and any(_overlap(tb, r, w, h) > 0.02 for r in (j.get("protect") or [])))


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
                                            allow_panel=not final, protect=j.get("protect"), force=final)
            box = z.get("box", (0, 0, w, h))
            paper, ink = _palette(canvas)
            obj_pos, panel_side = "center", "right"
            leg = dict(plate=False, plate_bg=None, scrim="rgba(0,0,0,0)")
            if direction == "panel":
                panel_side, obj_pos = _panel_side(canvas, fmt)
            else:
                leg = legibility(canvas, box, DIRECTIONS[direction]["big"])   # measured contrast → ink + scrim strength
                ink = leg["ink"]
            top = (box[1] + box[3]) / 2 < h / 2
            plate = leg["plate"]
            brand_color = brand_line(canvas, top if direction != "panel" else False)
            params = dict(w=w, h=h, direction=direction,
                headline=j["headline"], sub=j.get("sub"), note=j.get("note"), signature=j.get("signature"),
                brand=j.get("brand", ""), box=box, top=top, ink=ink, paper=paper, accent=ink,
                scrim_on=True, scrim=leg["scrim"], plate_bg=leg["plate_bg"],
                brand_color=brand_color,
                obj_pos=obj_pos, panel_side=panel_side, plate=plate)
            j["params"] = {k: v for k, v in params.items()}          # exported for web rendering
            html = env.get_template("overlay.html.j2").render(img=Path(j["img"]).resolve().as_uri(),
                                                              fonts=fonts, **params)
            tmp = Path(j["out"]).with_suffix(".html")
            Path(j["out"]).parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(tmp.resolve().as_uri())
            pg.wait_for_selector("body[data-ready='1']", timeout=15000)
            pg.wait_for_timeout(200)
            j["measured"] = pg.evaluate(MEASURE_JS)
            if j["measured"].get("text_box"):
                j["measured"]["lines"] = round(crossing_lines(canvas, j["measured"]["text_box"]), 2)
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
        # least-used looks first (stable within the rotation) so the 20 ads spread across all directions
        count = {d: sum(1 for j in jobs if j["directions"] == [d]) for d in ORDER}
        prefs = [forced] if forced else sorted([d for d in rot if d not in taken], key=lambda d: count[d])
        # handwriting is only for a real personal note or signature (DESIGN_RULES) — no note, no "note" look
        if not ad.get("note"):
            prefs = [d for d in prefs if d != "note"] or ["contrast"]
        people = ad.get("has_people", False)
        canvas = _canvas(str(raw), *SIZES[ad["format"]])
        # hand-drawn protect boxes are authoritative; the Haar backup only fills in when there are none
        protect = list(ad.get("protect") or []) or (detect_faces(canvas) if people else [])
        n_panels = sum(1 for j in jobs if j["directions"] == ["panel"])
        direction, _ = choose_direction(canvas, ad["format"], prefs, people,
                                        allow_panel=n_panels < MAX_PANELS, protect=protect)
        if direction == "panel" and forced:                     # a hand-picked look wins, in its least-bad spot
            direction = forced
        looks = [d for d in ORDER if d != "note" or ad.get("note")]
        if direction == "panel" and n_panels >= MAX_PANELS:   # nothing clear among the unused looks
            direction, _ = choose_direction(canvas, ad["format"], looks, people, allow_panel=False,
                                            protect=protect)
        if direction == "panel" and n_panels >= MAX_PANELS:   # every zone touches the subject: least bad
            direction, _ = choose_direction(canvas, ad["format"], looks, people, allow_panel=False,
                                            protect=protect, force=True)
        taken.append(direction)
        jobs.append(dict(img=str(raw), out=str(base / ad["image"]), headline=ad["overlay"],
                         sub=ad.get("overlay_sub"), note=ad.get("note"), signature=signature,
                         brand=brand, format=ad["format"], directions=[direction], people=people,
                         protect=protect, has_note=bool(ad.get("note"))))
        ads.append(ad)
    outs = render(jobs)
    # re-try every ad whose rendered text came out too small or touching the product, with another look
    for _ in range(4):
        bad = [j for j in jobs if not _legible(j)]
        if not bad:
            break
        for j in bad:
            j.setdefault("tried", []).append(j["direction"])
            canvas = _canvas(j["img"], *SIZES[j["format"]])
            left = [d for d in ORDER if d not in j["tried"] and (d != "note" or j.get("has_note"))]
            if not left:
                continue
            d, _ = choose_direction(canvas, j["format"], left, j["people"], allow_panel=False, protect=j["protect"])
            if d == "panel":
                d, _ = choose_direction(canvas, j["format"], left, j["people"], allow_panel=False,
                                        protect=j["protect"], force=True)
            j["directions"] = [d]
        render([j for j in bad if j["directions"][0] not in j.get("tried", [])])
    for j in jobs:
        if not _legible(j):
            log.warning("ad %s: no look fits cleanly (%s)", Path(j["out"]).name, j.get("measured"))
        elif (j.get("measured") or {}).get("lines", 0) > MAX_LINE:
            log.warning("ad %s: an edge runs through the text (%s) - check at phone size",
                        Path(j["out"]).name, j["measured"]["lines"])
    for ad, j in zip(ads, jobs):
        ad.setdefault("layout", {}).update(rendered_direction=j["direction"], rendered_zone=j["zone"],
                                           render=j.get("params"))
    return outs
