"""Assemble lead 2026-09-25-002 (Kalahari Rose Israel) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/kalahari_ads_2026-09-25-002.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# first run, no regenerations.
# product / face / hand / animal regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each image
PROTECT = {
    1: [[0.0, 0.42, 1.0, 0.85]],
    2: [[0.1, 0.3, 1.0, 0.95]],
    3: [[0.2, 0.25, 0.95, 0.85]],
    4: [[0.45, 0.0, 1.0, 1.0], [0.2, 0.72, 0.55, 0.95]],
    5: [[0.35, 0.28, 0.85, 0.85], [0.55, 0.0, 1.0, 0.3]],
    6: [[0.0, 0.3, 1.0, 0.85]],
    7: [[0.0, 0.35, 1.0, 1.0]],
    8: [[0.25, 0.35, 0.85, 0.9]],
    9: [[0.1, 0.35, 1.0, 1.0]],
    10: [[0.5, 0.0, 1.0, 1.0], [0.0, 0.55, 0.6, 0.95]],
    11: [[0.1, 0.35, 1.0, 0.95]],
    12: [[0.1, 0.35, 1.0, 0.8]],
    13: [[0.0, 0.35, 1.0, 0.9]],
    14: [[0.5, 0.0, 1.0, 1.0], [0.0, 0.35, 0.6, 0.9]],
    15: [[0.0, 0.35, 1.0, 1.0]],
    16: [[0.1, 0.4, 0.95, 0.85]],
    17: [[0.0, 0.35, 1.0, 0.95]],
    18: [[0.0, 0.45, 1.0, 0.95]],
    19: [[0.0, 0.35, 1.0, 1.0]],
    20: [[0.0, 0.45, 1.0, 0.95]],
}
LOOK = {4: "contrast", 5: "contrast"}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="קלהרי רוז", name_en="Kalahari Rose Israel", category="קוסמטיקה טבעית", city="")
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
