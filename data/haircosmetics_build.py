"""Assemble lead 2026-09-25-039 (Hair Cosmetics) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/haircosmetics_ads_2026-09-25-039.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# ads 8, 9, 13, 14 regenerated: 8 had an odd heat-orb on the wall, 9 a hair sheet that read as a rug,
# 13 an invented "BIOTOP" label, 14 a floating hand; 19 again with a flat wall (the text sat on an arch edge).
# product / face / hand regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each generated image
PROTECT = {
    1: [[0.3, 0.32, 0.72, 0.85]],
    2: [[0.2, 0.48, 0.9, 1.0]],
    3: [[0.33, 0.3, 0.85, 0.9]],
    4: [[0.3, 0.3, 0.7, 0.85]],
    5: [[0.25, 0.48, 0.88, 0.85]],
    6: [[0.42, 0.35, 0.62, 0.85]],
    7: [[0.05, 0.35, 0.9, 1.0]],
    8: [[0.38, 0.38, 0.68, 0.85]],
    9: [[0.28, 0.35, 0.78, 0.9]],
    10: [[0.2, 0.4, 0.78, 0.95]],
    11: [[0.25, 0.25, 0.62, 0.95]],
    12: [[0.2, 0.38, 0.9, 0.85]],
    13: [[0.3, 0.5, 0.78, 0.78]],
    14: [[0.35, 0.3, 1.0, 0.8]],
    15: [[0.18, 0.33, 0.8, 0.95]],
    16: [[0.25, 0.35, 0.72, 0.85]],
    17: [[0.2, 0.4, 0.85, 0.8]],
    18: [[0.32, 0.48, 0.75, 0.92]],
    19: [[0.0, 0.4, 0.9, 1.0]],
    20: [[0.2, 0.3, 0.85, 0.85]],
}

# pinned looks where the automatic choice lands on an architectural edge
LOOK = {}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="הייר קוסמטיקס", name_en="Hair Cosmetics", category="מוצרי שיער מקצועיים")
lead["research"] = plan.RESEARCH
lead["new_ads"] = []
for a in plan.A:
    a = dict(a)
    a.pop("refs"); prompt = a.pop("prompt")
    a["protect"] = PROTECT[a["ad_no"]]
    if a["ad_no"] in LOOK:
        a["layout"] = {"direction": LOOK[a["ad_no"]]}
    a["source_url"] = src.get(str(a["ad_no"]))
    a["model"] = "higgsfield/nano_banana_pro 2k"
    a["prompt"] = prompt
    lead["new_ads"].append(a)
lead["status"] = "researched"
lead.setdefault("timestamps", {})["researched"] = now_iso()
json.dump(lead, open(p, "w"), ensure_ascii=False, indent=1)
print("ok", len(lead["new_ads"]))
