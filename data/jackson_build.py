"""Assemble lead 2026-09-25-086 (Jackson Jewelry) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/jackson_ads_2026-09-25-086.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# ads 11, 15, 19 regenerated: at 9:16 the model baked a flat colour band into the top (11 and 19 twice), so 11 and
# 19 moved to 4:5; 11 also showed the lips. ad 9 regenerated with wall space on the left (text sat on the throat). ad 11's thin black film frame was cropped off the raw image.
# product / face / hand regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each generated image
PROTECT = {
    1: [[0.08, 0.45, 1.0, 0.9]],
    2: [[0.28, 0.38, 0.62, 0.66]],
    3: [[0.0, 0.35, 1.0, 0.92]],
    4: [[0.2, 0.38, 0.8, 0.68]],
    5: [[0.38, 0.55, 0.58, 0.82]],
    6: [[0.25, 0.3, 0.85, 0.9]],
    7: [[0.2, 0.4, 0.72, 0.82]],
    8: [[0.03, 0.45, 0.9, 0.8]],
    9: [[0.52, 0.0, 0.9, 0.2], [0.52, 0.15, 1.0, 0.32], [0.28, 0.32, 1.0, 1.0]],
    10: [[0.2, 0.42, 0.8, 0.85]],
    11: [[0.1, 0.25, 0.75, 1.0]],
    12: [[0.2, 0.45, 0.85, 0.95]],
    13: [[0.0, 0.45, 1.0, 0.9]],
    14: [[0.3, 0.43, 0.72, 0.75]],
    15: [[0.0, 0.33, 1.0, 1.0]],
    16: [[0.4, 0.43, 0.7, 0.82]],
    17: [[0.0, 0.3, 1.0, 0.9]],
    18: [[0.33, 0.42, 0.68, 0.78]],
    19: [[0.25, 0.0, 0.6, 0.12], [0.3, 0.35, 0.95, 0.85]],
    20: [[0.3, 0.53, 0.75, 0.74], [0.0, 0.25, 0.6, 0.55]],
}
LOOK = {9: "contrast"}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="ג׳קסון תכשיטים", name_en="Jackson Jewelry", category="תכשיטי זהב ויהלומים",
                        city="רמת גן")
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
