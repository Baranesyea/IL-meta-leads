"""Assemble lead 2026-09-25-066 (Asta-In) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/astain_ads_2026-09-25-016.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# ads 1,3,6,9,10,12,20 regenerated 2026-09-26 (text sat on wall/ceiling lines): boxes also fence off
# the lines themselves (e.g. ad 1 travertine edge, ad 12 alcove + wall corner) so text stays in the clean wall.
# product / face / hand regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each generated image
PROTECT = {
    1: [[0.3, 0.36, 0.7, 0.9]],
    2: [[0.35, 0.28, 0.7, 0.86], [0.3, 0.78, 0.52, 0.92]],
    3: [[0.0, 0.3, 0.65, 0.56], [0.33, 0.6, 0.65, 0.88]],
    4: [[0.3, 0.33, 0.65, 0.76], [0.0, 0.55, 1.0, 0.9]],
    5: [[0.08, 0.5, 0.68, 0.82], [0.0, 0.0, 0.12, 0.6]],
    6: [[0.13, 0.38, 0.9, 0.8], [0.0, 0.35, 0.2, 0.7], [0.7, 0.3, 1.0, 0.55]],
    7: [[0.0, 0.28, 0.58, 0.78], [0.0, 0.72, 0.55, 1.0], [0.58, 0.7, 1.0, 0.9]],
    8: [[0.24, 0.3, 0.66, 0.76], [0.58, 0.24, 1.0, 0.5]],
    9: [[0.28, 0.35, 0.85, 1.0], [0.0, 0.5, 0.25, 1.0], [0.85, 0.5, 1.0, 1.0]],
    10: [[0.38, 0.35, 0.66, 0.86], [0.78, 0.48, 1.0, 0.82]],
    11: [[0.5, 0.3, 1.0, 1.0], [0.84, 0.0, 1.0, 0.8], [0.0, 0.66, 0.65, 0.86]],
    12: [[0.12, 0.2, 0.98, 0.9]],
    13: [[0.28, 0.36, 0.82, 0.92], [0.0, 0.52, 0.22, 0.82], [0.8, 0.52, 1.0, 0.9]],
    14: [[0.58, 0.08, 0.84, 0.74], [0.18, 0.58, 0.62, 0.87], [0.0, 0.4, 0.22, 0.62], [0.84, 0.5, 1.0, 0.82]],
    15: [[0.28, 0.4, 0.5, 0.8], [0.0, 0.74, 0.65, 0.9], [0.55, 0.25, 1.0, 0.62]],
    16: [[0.35, 0.27, 0.68, 0.84], [0.0, 0.5, 0.36, 0.72], [0.7, 0.55, 1.0, 1.0]],
    17: [[0.28, 0.44, 0.9, 0.82], [0.72, 0.0, 0.85, 0.5]],
    18: [[0.4, 0.33, 0.7, 0.8], [0.0, 0.5, 1.0, 1.0]],
    19: [[0.2, 0.36, 0.9, 0.86], [0.0, 0.4, 0.2, 0.62]],
    20: [[0.22, 0.45, 0.7, 0.74], [0.0, 0.34, 0.28, 0.72], [0.7, 0.46, 0.98, 0.7], [0.0, 0.78, 1.0, 1.0]],
}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="אסטאין", name_en="Asta-In", category="קוסמטיקה טבעית מאסטקסנטין")
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
