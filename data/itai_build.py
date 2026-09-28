"""Assemble lead 2026-09-27-342 (Itai Elbaz) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/itai_ads_2026-09-27-342.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# 7 came back with a second person's hands in the frame, 12 with the man walking a half-drawn bike: regenerated with
# these prompts.
REGEN = {
    7: "A woman in her thirties alone at a home office desk with an open laptop, turning her head slowly to the side with her own hand resting on her neck and shoulder, plants and a window behind her, soft afternoon light, calm expression. She is the only person in the photo; no other people, hands or arms in the frame.",
    12: "A man in his sixties in a light cycling jacket and helmet riding a normal road bicycle, seated on the saddle and pedaling, on a quiet country road between olive groves and hills in the Galilee on a Saturday morning, relaxed posture, golden light, seen from behind and slightly to the side at a distance, the whole bicycle clearly visible with two wheels on the road.",
}
# people / hands / subject regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each image
PROTECT = {
    1: [[0.15, 0.3, 1.0, 0.85]],
    2: [[0.0, 0.4, 1.0, 1.0], [0.0, 0.0, 0.35, 0.4]],
    3: [[0.15, 0.5, 1.0, 0.95]],
    4: [[0.0, 0.3, 1.0, 1.0]],
    5: [[0.35, 0.15, 0.75, 1.0]],
    6: [[0.0, 0.45, 1.0, 0.8]],
    7: [[0.0, 0.3, 0.7, 1.0], [0.4, 0.65, 1.0, 0.95]],
    8: [[0.0, 0.25, 1.0, 1.0], [0.0, 0.0, 0.15, 0.3]],
    9: [[0.35, 0.35, 0.7, 0.75]],
    10: [[0.0, 0.25, 1.0, 1.0]],
    11: [[0.45, 0.0, 1.0, 1.0]],
    12: [[0.5, 0.55, 0.85, 0.95]],
    13: [[0.45, 0.1, 0.95, 0.75], [0.0, 0.6, 1.0, 1.0]],
    14: [[0.1, 0.35, 1.0, 0.8]],
    15: [[0.1, 0.45, 1.0, 0.9]],
    16: [[0.0, 0.55, 0.9, 1.0]],
    17: [[0.1, 0.25, 1.0, 0.95]],
    18: [[0.0, 0.3, 1.0, 0.95]],
    19: [[0.0, 0.3, 1.0, 1.0]],
    20: [[0.1, 0.35, 0.8, 1.0]],
}
LOOK = {}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="איתי אלבז", name_en="Itay Elbaz", category="רפואה סינית ודיקור",
                        city="כרמיאל", owner_name="איתי אלבז")
lead["contact"]["whatsapp"].update(confidence="high", kind="owner",
                                   kind_signals=["WhatsApp profile 'איתי אלבז ~ רפואה סינית', checked by Eran 2026-09-28"])
# the Ad Library returned ad 1511015147207008 twice (second copy without media)
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
