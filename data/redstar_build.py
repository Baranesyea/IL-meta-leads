"""Assemble lead 2026-09-25-054 (Red Star) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/redstar_ads_2026-09-25-054.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# ad 9 regenerated (bare-shoulder crop too revealing for Meta -> white linen top), 15 twice (face cut at the eyes,
# then text landed on the cheek -> woman in the right half, left half plain wall); 13, 14 protect widened;
# hero_m regenerated without the stray hands.
# product / face / hand / animal regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each image
PROTECT = {
    1: [[0.0, 0.28, 1.0, 1.0]],
    2: [[0.1, 0.3, 0.95, 0.9]],
    3: [[0.2, 0.22, 0.8, 0.95]],
    4: [[0.0, 0.35, 1.0, 0.95]],
    5: [[0.3, 0.28, 0.75, 0.92]],
    6: [[0.15, 0.35, 1.0, 0.8]],
    7: [[0.0, 0.22, 0.75, 1.0], [0.7, 0.6, 1.0, 0.85]],
    8: [[0.2, 0.25, 0.85, 0.95]],
    9: [[0.0, 0.0, 0.45, 1.0], [0.4, 0.4, 1.0, 0.95]],
    10: [[0.3, 0.3, 0.7, 0.95]],
    11: [[0.0, 0.35, 1.0, 0.95]],
    12: [[0.2, 0.25, 0.85, 0.9]],
    13: [[0.5, 0.0, 1.0, 1.0]],
    14: [[0.1, 0.08, 0.95, 0.85]],
    15: [[0.57, 0.0, 1.0, 1.0]],
    16: [[0.0, 0.35, 1.0, 0.95]],
    17: [[0.0, 0.3, 1.0, 0.95]],
    18: [[0.0, 0.28, 0.95, 0.9]],
    19: [[0.0, 0.35, 1.0, 1.0]],
    20: [[0.2, 0.35, 0.85, 1.0]],
}
LOOK = {13: "contrast", 15: "contrast"}  # 13 regenerated a second time: bottle + dropper moved to the right third

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="רד סטאר", name_en="Red Star", category="חנות ביוטי אונליין", city="גבעתיים")
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
