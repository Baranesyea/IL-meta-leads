"""Assemble lead 2026-09-26-021 (Mega Pet) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/megapet_ads_2026-09-26-021.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# first run, no regenerations; ads 4 and 20 moved to 4:5 before generating (animals in 9:16 tend to bake a band).
# product / face / hand / animal regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each image
PROTECT = {
    1: [[0.1, 0.3, 0.85, 0.95]],
    2: [[0.2, 0.25, 0.9, 0.95]],
    3: [[0.15, 0.35, 0.95, 0.95]],
    4: [[0.0, 0.45, 1.0, 0.95]],
    5: [[0.05, 0.28, 0.85, 0.95]],
    6: [[0.2, 0.28, 0.95, 0.85]],
    7: [[0.0, 0.55, 1.0, 0.95]],
    8: [[0.0, 0.55, 1.0, 0.9]],
    9: [[0.1, 0.35, 0.95, 0.95]],
    10: [[0.2, 0.4, 0.9, 0.95]],
    11: [[0.2, 0.2, 0.9, 0.95]],
    12: [[0.2, 0.35, 0.9, 0.9]],
    13: [[0.1, 0.45, 0.95, 0.9]],
    14: [[0.15, 0.4, 0.9, 0.85]],
    15: [[0.1, 0.35, 0.95, 0.85]],
    16: [[0.0, 0.45, 1.0, 0.8]],
    17: [[0.0, 0.38, 1.0, 0.95]],
    18: [[0.0, 0.35, 0.95, 0.95]],
    19: [[0.0, 0.35, 1.0, 1.0]],
    20: [[0.35, 0.2, 0.62, 1.0], [0.6, 0.35, 1.0, 1.0]],
}
LOOK = {}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="מגה פט", name_en="Mega Pet", category="מזון וציוד לחיות מחמד", city="באר שבע")
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
