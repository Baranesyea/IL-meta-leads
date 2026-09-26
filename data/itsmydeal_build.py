"""Assemble lead 2026-09-25-066 (It's My Deal) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/itsmydeal_ads_2026-09-25-051.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# ads 1,3,6,9,10,12,20 regenerated 2026-09-26 (text sat on wall/ceiling lines): boxes also fence off
# the lines themselves (e.g. ad 1 travertine edge, ad 12 alcove + wall corner) so text stays in the clean wall.
# product / face / hand regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each generated image
PROTECT = {
    1: [[0.08, 0.32, 0.78, 0.95]],
    2: [[0.35, 0.22, 0.68, 0.92]],
    3: [[0.1, 0.52, 0.95, 1.0]],
    4: [[0.08, 0.2, 0.92, 0.92]],
    5: [[0.2, 0.3, 0.85, 1.0]],
    6: [[0.0, 0.3, 1.0, 1.0]],
    7: [[0.0, 0.42, 0.95, 1.0]],
    8: [[0.2, 0.33, 0.8, 0.92]],
    9: [[0.2, 0.42, 0.85, 1.0], [0.1, 0.25, 0.95, 0.45]],
    10: [[0.0, 0.3, 1.0, 1.0], [0.6, 0.25, 0.9, 0.5]],
    11: [[0.3, 0.33, 0.62, 0.8], [0.6, 0.35, 1.0, 0.55]],
    12: [[0.05, 0.4, 1.0, 1.0]],
    13: [[0.15, 0.25, 0.85, 0.92]],
    14: [[0.25, 0.35, 0.9, 0.88]],
    15: [[0.28, 0.36, 0.78, 0.8]],
    16: [[0.4, 0.22, 0.6, 0.8], [0.0, 0.45, 1.0, 1.0]],
    17: [[0.1, 0.25, 0.9, 0.95]],
    18: [[0.05, 0.35, 0.95, 0.95]],
    19: [[0.5, 0.0, 0.84, 1.0], [0.475, 0.26, 0.57, 0.4], [0.68, 0.74, 1.0, 1.0]],
    20: [[0.08, 0.32, 0.92, 1.0]],
}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="מיי דיל", name_en="It's My Deal", category="מותגי טיפוח שיער מקצועיים")
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
