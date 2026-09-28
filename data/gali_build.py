"""Assemble lead 2026-09-27-342 (Gali Ripui) from the plan: research + new_ads with hand-drawn protect boxes."""
import importlib.util, json, sys
sys.path.insert(0, ".")
from src.common import now_iso

spec = importlib.util.spec_from_file_location("plan", "data/gali_ads_2026-09-27-344.py")
plan = importlib.util.module_from_spec(spec); spec.loader.exec_module(plan)

# 6 showed the applicator like a bracelet on the ankle; 4, 7, 12, 16 came back with somebody else's hands or objects in the frame; regenerated with these scenes.
REGEN = {
    6: "A bright modern private clinic room with white walls and a soft blue accent wall. Close-up from the side: a patient lying on a white treatment table, the sole of her bare foot facing the camera and resting on a white cushion, a practitioner's hand pressing the round head of the handheld shockwave applicator from the reference photo against the bottom of her heel, the device's cable leading out of frame. Only the practitioner's hand and forearm are visible, no face.",
    4: "Night in a calm bedroom with a soft warm bedside lamp: a woman in her fifties asleep peacefully on her side under a white duvet, relaxed face, soft blue and white tones. She is alone in the room: no other people, no other hands or arms in the frame.",
    7: "A woman in her forties walking barefoot on the wet sand at the edge of the sea at sunrise, easy relaxed steps, soft golden light, seen from the side at a distance, Mediterranean beach, soft blue sky. She is the only person; nothing in the foreground, no hands, no objects close to the camera.",
    12: "A woman in her fifties playing padel on an outdoor court on a sunny morning, mid swing, relaxed and smiling, blue court and blue sky, seen from the side at a distance, her whole body and the racket visible. She is the only person in the frame; no other people, no hands, no devices in the foreground.",
    16: "A man in his fifties alone in a sunny home garden, bending down easily to pick ripe tomatoes into a wicker basket on the ground, relaxed posture, warm morning light, seen from the side, his whole body visible. He is the only person; no other people, hands or arms in the frame.",
}
# people / hands / subject regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each image
# people / hands / subject regions (canvas fractions x0,y0,x1,y1) — drawn by eye on each image
PROTECT = {
    1: [[0.3, 0.3, 0.85, 1.0]],
    2: [[0.0, 0.15, 1.0, 1.0]],
    3: [[0.35, 0.2, 0.85, 1.0], [0.35, 0.0, 0.6, 0.3]],
    4: [[0.0, 0.45, 1.0, 1.0]],
    5: [[0.35, 0.0, 0.65, 0.6], [0.4, 0.5, 1.0, 1.0]],
    6: [[0.0, 0.4, 1.0, 1.0]],
    7: [[0.3, 0.4, 0.45, 0.75]],
    8: [[0.1, 0.35, 1.0, 1.0]],
    9: [[0.35, 0.2, 0.8, 0.9]],
    10: [[0.0, 0.25, 1.0, 0.8]],
    11: [[0.2, 0.2, 1.0, 1.0]],
    12: [[0.1, 0.3, 0.95, 0.85]],
    13: [[0.3, 0.45, 0.65, 0.95]],
    14: [[0.0, 0.0, 0.15, 0.3], [0.0, 0.3, 1.0, 1.0], [0.75, 0.0, 1.0, 0.4]],
    15: [[0.0, 0.3, 1.0, 1.0]],
    16: [[0.0, 0.25, 0.9, 1.0]],
    17: [[0.0, 0.35, 1.0, 1.0]],
    18: [[0.2, 0.25, 1.0, 0.8]],
    19: [[0.0, 0.4, 1.0, 1.0]],
    20: [[0.1, 0.05, 0.7, 1.0]],
}
LOOK = {}

p = f"data/leads/{plan.LID}.json"
lead = json.load(open(p))
src = json.load(open(f"output/{plan.LID}/sources.json"))
lead["business"].update(name_he="גלי ריפוי", name_en="Gali Ripui", category="טיפול בכאבים אורתופדיים בגלי הלם",
                        city="אשקלון", owner_name="מיכל קצין")
lead["contact"]["whatsapp"].update(confidence="high", kind="owner",
                                   kind_signals=["WhatsApp profile 'מיכל', checked by Eran 2026-09-28; she asked for the report"])
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
