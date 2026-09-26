"""Stav's page (REPORTS["stav-56f5e275"]) predates site_export: review copy + the review pairs, patched in place."""
import json, sys
sys.path.insert(0, ".")
from src.site_export import _read, _write, export_current

R = _read()
st = R["stav-56f5e275"]
lead = json.load(open("data/leads/2026-09-25-076.json"))
st["review"] = {
    "eyebrow": "עברנו על הקמפיין שלך",
    "title": ["הקמפיין שלך עובד.", "והוא יכול להכניס הרבה יותר."],
    "text": "המודעות שלך כבר מוכרות: חלקן רצות יותר משנה, וזה בדרך כלל סימן שהן מביאות כסף. עברנו עליהן, על האתר ועל הקולקציות. ככה זה נראה היום, וככה אנחנו היינו עושים את זה.",
    "issues_eyebrow": "מה היינו משנים",
    "issues": ["ארבעה דברים", "שהיינו משנים כבר מחר."],
}
# pairs: her ad running today -> the same product our way
st["compare"] = {"before": {"label": "רץ היום", "items": export_current(lead, "stav", [0, 2, 5, 3])},
                 "after": {"label": "ככה היינו עושים את זה", "ads": [1, 18, 5, 13]}}
_write(R)
