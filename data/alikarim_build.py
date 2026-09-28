"""Assemble lead 2026-09-27-314 (Ali Karim) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/alikarim_ads_2026-09-27-314.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# 13, 14, 15, 19 came back with a pasted band across the top; regenerated with a plain "wide framing, one single
# photograph" wording instead of the "top third" composition line (REGEN below is the prompt that was used).
AIR = "Wide natural framing with open space above the subject. One single continuous photograph, no borders, no panels, no inset images, no split frame."
REGEN = {
    13: "A man in his sixties climbing old stone steps in a Galilee village street, one hand lightly on an iron rail, smiling slightly, warm afternoon light, bougainvillea on the stone wall, shot from a few steps below.",
    14: "A grandfather in his sixties kicking a ball with his six year old grandson in a sunny village yard under an olive tree, both laughing, natural movement, warm light, wide shot.",
    15: "A woman in her thirties stretching her leg on a wooden park bench before a run in an early morning park, athletic clothes, focused calm face, soft golden light between trees, wide shot.",
    19: "Close-up of a man's hand holding a smartphone above a wooden kitchen table next to a cup of coffee, the phone screen shows a blurred generic chat app with green bubbles and no readable text, soft morning window light, plants in the soft background.",
}
# people / hands / subject regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each image
PROTECT = {
    1: [[0.25, 0.3, 0.8, 1.0]],
    2: [[0.0, 0.25, 0.9, 1.0]],
    3: [[0.2, 0.35, 1.0, 1.0]],
    4: [[0.1, 0.25, 1.0, 0.95]],
    5: [[0.35, 0.25, 0.9, 1.0]],
    6: [[0.0, 0.2, 1.0, 0.85]],
    7: [[0.3, 0.1, 1.0, 1.0]],
    8: [[0.35, 0.55, 0.65, 0.95]],
    9: [[0.45, 0.4, 1.0, 1.0]],
    10: [[0.0, 0.35, 0.9, 1.0]],
    11: [[0.1, 0.35, 0.9, 1.0]],
    12: [[0.0, 0.45, 0.75, 0.95]],
    13: [[0.15, 0.35, 0.95, 1.0]],
    14: [[0.15, 0.2, 0.7, 0.8]],
    15: [[0.35, 0.35, 0.8, 1.0]],
    16: [[0.0, 0.3, 1.0, 1.0]],
    17: [[0.0, 0.5, 1.0, 1.0]],
    18: [[0.0, 0.5, 1.0, 0.95]],
    19: [[0.25, 0.55, 1.0, 1.0]],
    20: [[0.2, 0.3, 0.85, 1.0]],
}
LOOK = {}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="עלי כריים", name_en="Neuroflex clinic", category="פיזיותרפיה ואוסטאופתיה",
                        city="מג'ד אל כרום · באר שבע", owner_name="עלי כריים")
lead["contact"]["whatsapp"].update(confidence="high", kind="owner",
                                   kind_signals=["WhatsApp Business profile 'עלי כריים פיזיותרפיסט ואוסטאופאת', checked by Eran 2026-09-28"])
lead["research"] = plan.RESEARCH
lead["new_ads"] = []
for a in plan.A:
    a = dict(a)
    a.pop("refs"); prompt = a.pop("prompt")
    if a["ad_no"] in REGEN:
        prompt = plan.STYLE + REGEN[a["ad_no"]] + " " + AIR + " " + plan.RULES
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
