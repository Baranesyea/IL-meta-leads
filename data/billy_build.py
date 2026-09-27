"""Assemble lead 2026-09-25-071 (Billy Jewelry) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/billy_ads_2026-09-25-071.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# regenerated with the ONE composition wording after pasted top bands: 1, 2, 15. Ads 13, 14, 16 and hero_m were cropped below a seam.
# ad 8 became a product-only shot (the necklace on a nail) after two people versions came back as collages.
# product / face / hand / animal regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each image
PROTECT = {
    1: [[0.0, 0.3, 1.0, 0.75]],
    2: [[0.0, 0.2, 1.0, 1.0]],
    3: [[0.2, 0.0, 0.7, 0.08], [0.1, 0.25, 0.9, 1.0]],
    4: [[0.0, 0.38, 1.0, 0.75]],
    5: [[0.15, 0.2, 0.9, 1.0]],
    6: [[0.0, 0.3, 1.0, 1.0]],
    7: [[0.0, 0.35, 1.0, 0.95]],
    8: [[0.35, 0.3, 0.7, 0.85]],
    9: [[0.0, 0.4, 1.0, 1.0]],
    10: [[0.1, 0.35, 1.0, 0.95]],
    11: [[0.0, 0.3, 1.0, 0.8]],
    12: [[0.0, 0.3, 1.0, 0.95]],
    13: [[0.05, 0.15, 0.95, 1.0]],
    14: [[0.2, 0.0, 0.75, 0.95]],
    15: [[0.15, 0.3, 1.0, 1.0]],
    16: [[0.55, 0.1, 1.0, 1.0]],
    17: [[0.3, 0.3, 1.0, 0.75]],
    18: [[0.0, 0.35, 1.0, 0.95]],
    19: [[0.0, 0.3, 1.0, 1.0]],
    20: [[0.2, 0.55, 1.0, 0.95]],
}
LOOK = {14: 'contrast'}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="בילי", name_en="Billy Jewelry", category="תכשיטי אופנה", city="")
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
