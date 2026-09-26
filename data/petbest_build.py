"""Assemble lead 2026-09-26-012 (Pet Best) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/petbest_ads_2026-09-26-012.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# ads 1, 3, 13, 14, 16 regenerated: a pasted-in room rectangle / seam across the top (the 'lower 60%' wording did it here);
# 8 and 20 had odd compositions. Re-prompted as 'one real photograph, top third plain wall'; 8, 16, 20 moved to 4:5.
# product / face / hand / animal regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each image
PROTECT = {
    1: [[0.15, 0.38, 0.85, 0.95]],
    2: [[0.0, 0.28, 1.0, 0.95]],
    3: [[0.0, 0.45, 1.0, 0.95]],
    4: [[0.0, 0.5, 1.0, 0.95]],
    5: [[0.0, 0.35, 0.95, 0.95]],
    6: [[0.2, 0.18, 0.9, 0.9]],
    7: [[0.0, 0.25, 1.0, 0.95]],
    8: [[0.1, 0.3, 0.85, 0.85]],
    9: [[0.3, 0.4, 1.0, 0.95]],
    10: [[0.2, 0.3, 1.0, 0.95]],
    11: [[0.0, 0.35, 1.0, 0.95]],
    12: [[0.15, 0.45, 1.0, 0.95]],
    13: [[0.0, 0.4, 1.0, 0.95], [0.2, 0.0, 0.58, 0.7]],
    14: [[0.15, 0.35, 0.95, 0.8]],
    15: [[0.0, 0.35, 0.9, 0.85], [0.0, 0.0, 0.3, 0.6], [0.68, 0.0, 0.82, 0.6], [0.6, 0.22, 0.85, 0.6]],  # door frames, olive tree
    16: [[0.15, 0.5, 1.0, 0.85]],
    17: [[0.0, 0.35, 1.0, 0.95], [0.88, 0.0, 1.0, 1.0]],  # window frame
    18: [[0.1, 0.25, 0.9, 0.95]],
    19: [[0.0, 0.35, 1.0, 0.95]],
    20: [[0.2, 0.4, 1.0, 0.8], [0.0, 0.0, 0.22, 1.0]],
}
LOOK = {}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="פט בסט", name_en="Pet Best", category="סופרמרקט לחיות מחמד", city="רמת ישי")
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
