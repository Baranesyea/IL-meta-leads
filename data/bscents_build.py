"""Assemble lead 2026-09-25-066 (B-scents) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/bscents_ads_2026-09-25-066.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# product / face / hand regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each generated image
PROTECT = {
    1: [[0.53, 0.42, 0.77, 0.64], [0.08, 0.42, 0.52, 0.88]],
    2: [[0.36, 0.44, 0.74, 1.0], [0.16, 0.55, 0.32, 0.73]],
    3: [[0.33, 0.46, 0.7, 0.72], [0.2, 0.74, 0.75, 0.97], [0.22, 0.33, 0.42, 0.47]],
    4: [[0.33, 0.28, 0.66, 0.82], [0.6, 0.58, 1.0, 0.78]],
    5: [[0.4, 0.3, 0.56, 0.64], [0.2, 0.56, 1.0, 0.86]],
    6: [[0.36, 0.28, 0.68, 1.0], [0.71, 0.55, 0.82, 0.85]],
    7: [[0.0, 0.42, 1.0, 0.74]],
    8: [[0.0, 0.42, 0.58, 0.66], [0.0, 0.6, 0.85, 1.0]],
    9: [[0.43, 0.38, 0.64, 0.56], [0.0, 0.55, 1.0, 1.0]],
    10: [[0.58, 0.4, 0.78, 0.68], [0.08, 0.46, 0.56, 0.95]],
    11: [[0.38, 0.42, 0.68, 0.63], [0.0, 0.68, 1.0, 1.0]],
    12: [[0.48, 0.22, 0.82, 0.76], [0.35, 0.21, 0.49, 0.42], [0.3, 0.7, 1.0, 1.0]],
    13: [[0.28, 0.48, 0.78, 0.77], [0.65, 0.64, 1.0, 0.95], [0.1, 0.72, 1.0, 1.0]],
    14: [[0.22, 0.58, 0.42, 0.86], [0.0, 0.3, 0.22, 0.7]],
    15: [[0.28, 0.35, 0.7, 0.76], [0.05, 0.68, 1.0, 0.92]],
    16: [[0.16, 0.43, 0.82, 0.9]],
    17: [[0.36, 0.52, 0.62, 0.82], [0.0, 0.72, 1.0, 1.0]],
    18: [[0.0, 0.0, 0.46, 1.0], [0.3, 0.38, 0.58, 0.7], [0.42, 0.7, 0.72, 0.9]],
    19: [[0.2, 0.42, 0.75, 0.8]],
    20: [[0.0, 0.0, 0.32, 1.0], [0.3, 0.33, 0.72, 0.72], [0.38, 0.58, 0.6, 0.88]],
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
