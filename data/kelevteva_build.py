"""Assemble lead 2026-09-26-024 (Kelev Teva) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/kelevteva_ads_2026-09-26-024.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# ads 8, 20 and the hero regenerated: the model invented a bag / jar label for the Wiggle buffalo ears (the store only
# shows the chews) — now loose chews only. ad 6 regenerated without the dogs (text touched their heads);
# ad 2 regenerated with the hand from the side (the price line sat on the hand). ad 16 moved to 4:5 (flat band baked into the 9:16 top).
# product / face / hand / animal regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each image
PROTECT = {
    1: [[0.05, 0.3, 1.0, 0.95]],
    2: [[0.1, 0.32, 0.65, 1.0], [0.6, 0.3, 1.0, 0.56], [0.52, 0.66, 0.86, 1.0], [0.87, 0.0, 1.0, 0.62]],  # dog, hand, pouch, porch post
    3: [[0.0, 0.28, 1.0, 0.95]],
    4: [[0.0, 0.45, 1.0, 0.9]],
    5: [[0.05, 0.25, 0.95, 0.95]],
    6: [[0.05, 0.45, 0.95, 0.95]],
    7: [[0.05, 0.33, 0.95, 0.95]],
    8: [[0.0, 0.48, 1.0, 1.0]],
    9: [[0.0, 0.35, 1.0, 0.95]],
    10: [[0.05, 0.35, 0.95, 0.9]],
    11: [[0.0, 0.3, 1.0, 1.0]],
    12: [[0.0, 0.45, 1.0, 1.0]],
    13: [[0.0, 0.38, 0.9, 0.85]],
    14: [[0.25, 0.3, 0.95, 0.95]],
    15: [[0.0, 0.35, 0.9, 0.9]],
    16: [[0.0, 0.38, 1.0, 0.9]],
    17: [[0.0, 0.3, 1.0, 0.95]],
    18: [[0.2, 0.25, 0.75, 0.85]],
    19: [[0.05, 0.3, 0.95, 0.85]],
    20: [[0.25, 0.42, 1.0, 0.75]],
}
LOOK = {}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="כלב טבע", name_en="Kelev Teva", category="חנות בריאות לכלבים", city="מושב בית הלוי")
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
