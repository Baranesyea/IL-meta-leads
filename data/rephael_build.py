"""Assemble lead 2026-09-27-342 (Rephael Center) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/rephael_ads_2026-09-27-313.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# 1 and 3 were refused by the image filter (false positive), 7, 12, 19, 20 got stuck in the queue and were resubmitted;
# 1, 3 and 20 with these plainer scenes.
REGEN = {
    20: "A fully dressed man in his fifties standing next to the treatment table, stretching his back with a small relieved smile, soft daylight. He is alone in the frame.",
    1: "A fully dressed man in his late forties in a navy sweater sitting at a wooden kitchen table in the evening, reading a printed medical letter with a thoughtful calm expression, a cup of tea beside him, warm lamp light, seen from the side.",
    3: "A fully dressed woman in her fifties in a light jacket and trousers, sitting on the front steps of a quiet Tel Aviv apartment building and lacing her walking shoes, calm content expression, seen from the side.",
}
# people / hands / subject regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each image
PROTECT = {
    1: [[0.0, 0.3, 1.0, 1.0]],
    2: [[0.0, 0.3, 1.0, 1.0]],
    3: [[0.2, 0.4, 1.0, 1.0]],
    4: [[0.0, 0.25, 1.0, 1.0]],
    5: [[0.0, 0.3, 1.0, 1.0]],
    6: [[0.0, 0.25, 1.0, 1.0], [0.6, 0.0, 1.0, 0.3]],
    7: [[0.0, 0.35, 1.0, 1.0]],
    8: [[0.2, 0.35, 0.7, 1.0]],
    9: [[0.0, 0.35, 1.0, 1.0]],
    10: [[0.0, 0.35, 1.0, 1.0]],
    11: [[0.0, 0.3, 1.0, 1.0]],
    12: [[0.0, 0.35, 1.0, 1.0]],
    13: [[0.15, 0.3, 0.8, 1.0]],
    14: [[0.0, 0.4, 1.0, 1.0]],
    15: [[0.0, 0.2, 0.8, 1.0]],
    16: [[0.0, 0.3, 1.0, 1.0]],
    17: [[0.0, 0.35, 1.0, 1.0]],
    18: [[0.3, 0.3, 1.0, 1.0]],
    19: [[0.0, 0.35, 1.0, 1.0]],
    20: [[0.1, 0.3, 0.9, 1.0]],
}
LOOK = {}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="מרכז רפאל", name_en="Rephael Center", category="רפואה משלימה, פריצות דיסק וכאבי גב",
                        city="רמת אביב ג', תל אביב", owner_name="ד\"ר רפאל פרטר")
lead["contact"]["whatsapp"].update(confidence="high", kind="owner",
                                   kind_signals=["WhatsApp Business 'מרכז רפאל', checked by Eran 2026-09-29"])
# drop duplicate ad ids and ads without media
seen, cur = set(), []
for a in lead["current_ads"]:
    if a["ad_id"] in seen or not a.get("media"):
        continue
    seen.add(a["ad_id"]); cur.append(a)
lead["current_ads"] = cur
lead["research"] = plan.RESEARCH
lead["new_ads"] = []
for a in plan.A:
    a = dict(a)
    a.pop("refs"); prompt = a.pop("prompt")
    if a["ad_no"] in REGEN:
        prompt = plan.STYLE + REGEN[a["ad_no"]] + " " + plan.ONE + " " + plan.RULES
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
print("ok", len(lead["new_ads"]), "current", len(cur))
