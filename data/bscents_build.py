"""Assemble lead 2026-09-25-066 (B-scents) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/bscents_ads_2026-09-25-066.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# ads 1,3,6,9,10,12,20 regenerated 2026-09-26 (text sat on wall/ceiling lines): boxes also fence off
# the lines themselves (e.g. ad 1 travertine edge, ad 12 alcove + wall corner) so text stays in the clean wall.
# product / face / hand regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each generated image
PROTECT = {
    1: [[0.41, 0.4, 0.58, 0.6], [0.0, 0.44, 0.48, 0.86], [0.0, 0.36, 1.0, 1.0]],
    2: [[0.36, 0.44, 0.74, 1.0], [0.16, 0.55, 0.32, 0.73]],
    3: [[0.36, 0.52, 0.65, 0.74], [0.28, 0.73, 0.58, 1.0], [0.0, 0.3, 1.0, 1.0]],
    4: [[0.33, 0.28, 0.66, 0.82], [0.6, 0.58, 1.0, 0.78]],
    5: [[0.4, 0.3, 0.56, 0.64], [0.2, 0.56, 1.0, 0.86]],
    6: [[0.54, 0.08, 1.0, 1.0], [0.39, 0.6, 0.51, 0.9]],
    7: [[0.0, 0.42, 1.0, 0.74]],
    8: [[0.0, 0.42, 0.58, 0.66], [0.0, 0.6, 0.85, 1.0]],
    9: [[0.2, 0.46, 0.39, 0.63], [0.5, 0.47, 1.0, 0.92], [0.0, 0.62, 1.0, 1.0]],
    10: [[0.69, 0.44, 0.89, 0.73], [0.1, 0.46, 0.58, 0.82], [0.9, 0.45, 1.0, 0.8], [0.0, 0.78, 1.0, 1.0]],
    11: [[0.38, 0.42, 0.68, 0.63], [0.0, 0.68, 1.0, 1.0]],
    12: [[0.5, 0.32, 0.82, 1.0], [0.78, 0.38, 0.96, 0.58], [0.0, 0.32, 0.62, 1.0], [0.64, 0.0, 1.0, 0.4]],
    13: [[0.28, 0.48, 0.78, 0.77], [0.65, 0.64, 1.0, 0.95], [0.1, 0.72, 1.0, 1.0]],
    14: [[0.22, 0.58, 0.42, 0.86], [0.0, 0.3, 0.22, 0.7]],
    15: [[0.28, 0.35, 0.7, 0.76], [0.05, 0.68, 1.0, 0.92]],
    16: [[0.16, 0.43, 0.82, 0.9]],
    17: [[0.36, 0.52, 0.62, 0.82], [0.0, 0.72, 1.0, 1.0]],
    18: [[0.0, 0.0, 0.46, 1.0], [0.3, 0.38, 0.58, 0.7], [0.42, 0.7, 0.72, 0.9]],
    19: [[0.2, 0.42, 0.75, 0.8]],
    20: [[0.38, 0.5, 0.62, 0.83], [0.58, 0.55, 1.0, 0.8], [0.0, 0.0, 0.45, 0.62]],
}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="בי סנטס", name_en="B-scents", category="בישום לבית, לרכב ולעסקים")
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
