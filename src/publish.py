"""Stage 9 — PUBLISH: internal lead page (client page + dashboard come later)."""
from __future__ import annotations

import base64
import io

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import db
from .common import OUTPUT, ROOT, get_logger

log = get_logger("publish")
env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["j2", "html"]))


def _inline(rel_path: str | None, max_px: int = 520) -> str:
    """Downscaled JPEG data URI so the page is one self-contained file."""
    if not rel_path:
        return ""
    path = OUTPUT / rel_path
    if not path.exists():
        return ""
    try:
        from PIL import Image

        with Image.open(path) as im:
            im = im.convert("RGB")
            im.thumbnail((max_px, max_px))
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=78)
            data = buf.getvalue()
    except Exception:  # noqa: BLE001 — fall back to the original bytes
        data = path.read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(data).decode()


def render_internal(lead: dict) -> str:
    html = env.get_template("internal.html.j2").render(
        lead=lead, b=lead["business"], c=lead["contact"], m=lead["meta"],
        r=lead.get("research") or {}, inline=_inline)
    out = OUTPUT / lead["lead_id"] / "internal.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    log.info("internal page %s (%d KB)", out, len(html) // 1024)
    return str(out)


def run_internal(lead_ids: list[str]) -> list[str]:
    return [render_internal(db.load_lead(i)) for i in lead_ids]
