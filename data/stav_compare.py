"""Before/after row for Stav's page (REPORTS["stav-56f5e275"]["compare"]); the rest of her entry predates site_export."""
import json, sys
sys.path.insert(0, ".")
from src.site_export import _read, _write, export_current

R = _read()
st = R["stav-56f5e275"]
lead = json.load(open("data/leads/2026-09-25-076.json"))
st["compare"] = {"eyebrow": "היום מול מחר", "title": ["אותם תכשיטים.", "שפה אחרת לגמרי."],
                 "before": {"label": "היום", "note": "מודעות שרצות אצלך עכשיו",
                            "items": export_current(lead, st["hero_bg"].split("/")[2], [0, 2, 5, 3])},
                 "after": {"label": "איתנו", "note": "מתוך הקמפיין שבנינו בשבילך", "ads": [1, 18, 5, 13]}}
_write(R)
