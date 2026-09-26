"""Assemble lead 2026-09-25-066 (JewelryFactory) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/jewelryfactory_ads_2026-09-25-087.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# ads 1,3,6,9,10,12,20 regenerated 2026-09-26 (text sat on wall/ceiling lines): boxes also fence off
# the lines themselves (e.g. ad 1 travertine edge, ad 12 alcove + wall corner) so text stays in the clean wall.
# product / face / hand regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each generated image
PROTECT = {
    1: [[0.0, 0.36, 1.0, 0.75], [0.6, 0.5, 0.95, 0.9]],
    2: [[0.08, 0.28, 0.65, 0.62], [0.52, 0.5, 1.0, 0.82]],
    3: [[0.0, 0.36, 1.0, 0.72], [0.45, 0.68, 0.85, 1.0]],
    4: [[0.0, 0.0, 0.5, 0.35], [0.3, 0.25, 1.0, 0.65], [0.7, 0.6, 1.0, 1.0]],
    5: [[0.0, 0.33, 1.0, 1.0]],
    6: [[0.25, 0.15, 0.62, 0.5], [0.42, 0.35, 0.9, 0.82]],
    7: [[0.35, 0.35, 0.68, 0.82], [0.15, 0.0, 0.4, 0.42], [0.6, 0.0, 0.85, 0.42]],
    8: [[0.36, 0.0, 1.0, 1.0]],
    9: [[0.35, 0.0, 1.0, 0.45], [0.3, 0.45, 0.85, 0.72]],
    10: [[0.2, 0.35, 1.0, 0.65], [0.7, 0.0, 0.82, 0.4], [0.0, 0.62, 1.0, 1.0]],
    11: [[0.28, 0.36, 0.78, 0.75], [0.72, 0.4, 1.0, 0.62], [0.0, 0.0, 0.65, 0.22]],
    12: [[0.1, 0.35, 1.0, 0.92]],
    13: [[0.25, 0.4, 1.0, 0.72], [0.0, 0.0, 0.22, 0.3], [0.0, 0.72, 1.0, 1.0]],
    14: [[0.0, 0.32, 1.0, 1.0]],
    15: [[0.0, 0.46, 1.0, 0.75], [0.42, 0.0, 1.0, 0.47]],
    16: [[0.2, 0.08, 0.85, 0.55], [0.0, 0.18, 0.22, 0.42]],
    17: [[0.0, 0.42, 1.0, 1.0], [0.0, 0.0, 0.6, 0.3]],
    18: [[0.0, 0.4, 1.0, 0.92]],
    19: [[0.2, 0.44, 1.0, 1.0]],
    20: [[0.55, 0.0, 1.0, 0.22], [0.5, 0.0, 1.0, 1.0], [0.1, 0.72, 0.65, 1.0], [0.0, 0.68, 0.25, 1.0]],
}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="ג'ולרי פקטורי", name_en="JewelryFactory", category="תכשיטים ומתנות עם חריטה אישית")
lead["research"] = plan.RESEARCH
lead["new_ads"] = []
for a in plan.A:
    a = dict(a)
    a.pop("refs"); prompt = a.pop("prompt")
    a["protect"] = PROTECT[a["ad_no"]]
    a["source_url"] = src.get(str(a["ad_no"]))
    a["model"] = "higgsfield/nano_banana_pro 2k"
    a["prompt"] = prompt
    lead["new_ads"].append(a)
lead["status"] = "researched"
lead.setdefault("timestamps", {})["researched"] = now_iso()
json.dump(lead, open(p, "w"), ensure_ascii=False, indent=1)
print("ok", len(lead["new_ads"]))
