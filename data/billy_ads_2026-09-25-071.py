"""Billy / בילי תכשיטים (lead 2026-09-25-071): research, 5 angles, 20 ads — image prompts + Hebrew copy.

Online fashion-jewelry store (Shopify, ~1,280 pieces): gold- and silver-tone necklaces, Star of David pendants,
tennis and clover bracelets, rings, earrings, anklets, men's pieces. Every piece ₪89; 4 for ₪199, 8 for ₪349;
order today, get it tomorrow.
Their ads: 12 ads, eight months running, all the same "4 for 199 / 8 for 349" text in neon yellow over AI-looking
sun-kissed models — and all 12 send people to the home page with 1,280 products.
Visual direction (new in the set): bright summer editorial — real pieces close up on sun-warmed skin, white-washed
walls with hard sunlight and palm shadows, white linen, sea-glass and sand tones; mix-and-match flat lays that show
what 4 pieces for ₪199 actually look like.
Ads speak to the customer in plural (their own ads do). Meta policy: no fake urgency, no "last day" claims.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-25-071"

REF = {
    "star_small": "3512fdfb-30f8-4e47-84a7-6bdee663d63d",   # small pavé Star of David pendant, gold tone, ₪89
    "star_bold": "649ac589-c843-48c1-8dc3-00ce2ea54082",    # bold designed Star of David pendant, gold tone, ₪89
    "coin_heart": "8108b640-0c74-4f5d-8232-acee3226dc78",   # link chain with white disc + heart, gold tone, ₪89
    "drops": "93b7346d-6fcb-4a3c-9c74-8272975925fd",        # necklace with 5 clear zircon drops, gold tone, ₪89
    "v_tennis": "c981b1c9-5108-4ae2-b51c-388413fed263",     # small pavé V tennis necklace, gold tone, ₪89
    "studs": "72907982-a460-4a0c-9d14-87a39ac3c4be",        # round polished disc stud earrings, gold tone, ₪89
    "tennis_coin": "842a09b8-3d5f-428d-81e6-de16da611e34",  # tennis bracelet with pavé disc, gold tone, ₪89
    "clover_white": "249939bc-b251-48cb-926d-2c5e188d83d3", # tennis bracelet with white clover, gold tone, ₪89
    "clover_black": "e2852fb6-935b-477b-a126-59827e743b75", # black clover station bracelet, gold tone, ₪89
    "heart_toggle": "07e05bad-4c14-47f8-834c-c511d22e8831", # chunky curb bracelet with pavé heart toggle, ₪89
    "ring_pave": "8ca2e2c3-7087-44c6-aef1-69659c05bd9e",    # dome ring with 6 rows of baguette zircons, ₪89
}

STYLE = ("Premium jewelry advertising photograph, bright summer editorial: hard Mediterranean sunlight with crisp "
         "shadows, white-washed plaster, white linen, sand and sea-glass tones, sun-warmed natural skin with real "
         "texture, macro detail on the metal and stones, shot on medium format, photorealistic, magazine quality. ")
FIDELITY = ("Jewelry must be exact matches of the reference photos: same chain type, pendant shape, stones and "
            "gold tone — do not redesign the pieces. No text, logos, watermarks or packaging text anywhere. People "
            "look natural, anatomically correct hands and fingers, no face unless stated. ")
TOP = ("COMPOSITION: the subject sits in the lower 60% of the frame; above it the same soft background simply continues, "
       "calm and empty — no objects, edges or lines. One continuous photograph — no borders, bands, panels or split "
       "frames.")


# the "lower 60%" wording made the model paste a flat band / inset across the top of several shots here
# (1, 2, 8, 14, 15, 16, hero_m) — regenerated with the wording that fixed it for Pet Best. It still kept the band
# on close-ups of people: 14, 16 and hero_m are cropped below it; 8 became a product-only shot.
ONE = ("COMPOSITION: one real photograph taken in one place, in one shot. The subject sits low in the frame; the top "
       "third is simply more of the same surface or wall, plain and softly lit. No collage, no inset photo, no "
       "pasted rectangle, no seams, no bands, no borders.")


def P(scene: str, air: str = TOP) -> str:
    return STYLE + scene + " " + air + " " + FIDELITY


RESEARCH = {
    "one_liner": "חנות תכשיטי אופנה אונליין עם כ-1,280 תכשיטים בגוון זהב וכסף: שרשראות, מגן דוד, צמידי טניס ותלתן, "
                 "טבעות, עגילים וצמידי רגל. כל תכשיט 89 ש״ח, 4 ב-199 ו-8 ב-349, מזמינים היום ומקבלים מחר. "
                 "מיצוב: תכשיט טרנדי במחיר שלא צריך לחשוב עליו פעמיים.",
    "hero_products": ["שרשראות מגן דוד — 89 ש״ח", "צמידי טניס ותלתן — 89 ש״ח", "שרשראות עדינות לשכבות — 89 ש״ח",
                      "מבצע 4 ב-199 / 8 ב-349"],
    "audience": [
        {"persona": "אוהבת השכבות", "who": "נשים 18–35", "cares": "להתחלף בתכשיטים לפי הלוק, בלי להוציא הון"},
        {"persona": "מחפשת המתנה", "who": "נשים וגברים 20–45", "cares": "מתנה יפה, מהר, במחיר שפוי"},
        {"persona": "מגן דוד", "who": "נשים 25–55", "cares": "תכשיט עם משמעות שאפשר לענוד כל יום"},
    ],
    "pains": ["\"תכשיט זהב אמיתי יקר מדי בשביל טרנד\"", "\"אני צריכה מתנה למחר\"", "\"אני לא יודעת מה הולך עם מה\"",
              "\"באתר יש אלף מוצרים ואני הולכת לאיבוד\""],
    "desires": ["לוק מושקע בלי מחיר של תכשיטן", "סט שלם ב-199", "מתנה שמגיעה מחר", "תכשיט עם משמעות"],
    "objections": ["\"זה ישחיר?\"", "\"זה ייראה זול?\"", "משלוח", "\"איך בוחרים 4 מתוך אלף\""],
    "current_ads_audit": "12 מודעות פעילות, רובן רצות שמונה חודשים, אז המבצע מוכר. אבל כולן אותה מודעה: אותו טקסט של 4 ב-199 "
                         "ו-8 ב-349 בצהוב ניאון, על דוגמניות שנראות כמו תמונות AI. אף מודעה לא מראה תכשיט מקרוב, אף מודעה "
                         "לא מדברת על מגן דוד או על מתנה, וכל 12 המודעות מובילות לדף הבית עם 1,280 מוצרים.",
    "gaps": ["כל המודעות מובילות לדף הבית", "אין תכשיט אחד בפוקוס", "המבצע לא מוסבר ויזואלית: איך נראים 4 תכשיטים",
             "מגן דוד ומתנות לא מקבלים מודעה", "המשלוח מהיום למחר קבור"],
    "angles": [
        {"id": "A1", "name": "4 ב-199: בונים סט", "idea": "מראים בדיוק מה מקבלים: ארבעה תכשיטים אמיתיים יחד, סט שלם במחיר של תכשיט אחד.", "persona": "אוהבת השכבות", "hook": "ארבעה תכשיטים. 199 ש״ח.", "why": "הופך את המבצע מטקסט לתמונה שרוצים."},
        {"id": "A2", "name": "מגן דוד", "idea": "תליוני מגן דוד עדינים ובולטים, לענידה יומיומית ולמתנה עם משמעות.", "persona": "מגן דוד", "hook": "קטן על הצוואר. גדול בלב.", "why": "קטגוריה עם ביקוש קבוע ורגש."},
        {"id": "A3", "name": "מתנה למחר", "idea": "מזמינים היום, מקבלים מחר: מתנה של הרגע האחרון שלא נראית כמו רגע אחרון.", "persona": "מחפשת המתנה", "hook": "שכחתם מתנה? מחר היא אצלכם.", "why": "כאב חוזר, ויתרון שכבר קיים."},
        {"id": "A4", "name": "שכבות", "idea": "שרשראות עדינות שנענדות יחד: וי טניס, טיפות ומטבע.", "persona": "אוהבת השכבות", "hook": "שרשרת אחת זה נחמד. שלוש זה לוק.", "why": "מעלה סל טבעית ל-4 ול-8."},
        {"id": "A5", "name": "יד מלאה", "idea": "צמידי טניס, תלתן ולב, וטבעת אחת בולטת: יד שלמה ב-199.", "persona": "אוהבת השכבות", "hook": "יד אחת. ארבעה תכשיטים.", "why": "ויזואל חזק ומוצרים שנמכרים יחד."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now", people=False):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=None, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=[], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 4 ב-199: בונים סט ----------
ad(1, "A1", "4:5", ["drops", "tennis_coin", "studs", "ring_pave"],
   P("Flat lay on white linen in hard sunlight with palm-leaf shadows: exactly four gold-tone pieces from the references "
     "arranged in a neat row — the five-drop necklace, the pavé disc tennis bracelet, the round stud earrings and the "
     "baguette dome ring.", air=ONE),
   "ארבעה תכשיטים.<br>199 ש״ח.", "כל תכשיט 89 · ארבעה ב-199",
   "זה מה שמקבלים ב-199 ש״ח: שרשרת, צמיד, עגילים וטבעת.\n\nבוחרים כל ארבעה תכשיטים מהאתר, ומשלמים 199 במקום 356.",
   "ארבעה תכשיטים. 199 ש״ח.", "4 תכשיטים ב-199", "4 ב-199")
ad(2, "A1", "1:1", ["v_tennis", "clover_white", "heart_toggle", "studs"],
   P("Four gold-tone pieces from the references laid out in a 2×2 grid on sun-warmed white plaster — the V tennis "
     "necklace, the white clover bracelet, the heart toggle bracelet and the disc studs — crisp shadows.", air=ONE),
   "סט שלם.<br>במחיר של אחד.", "4 ב-199 · 8 ב-349",
   "למה לבחור תכשיט אחד כשאפשר סט שלם?\n\nכל תכשיט באתר 89 ש״ח, וארבעה ביחד 199 ש״ח.",
   "סט שלם במחיר של אחד.", "4 תכשיטים ב-199", "4 ב-199")
ad(3, "A1", "4:5", ["drops", "v_tennis", "clover_white", "ring_pave"],
   P("Close-up of a woman's sun-kissed collarbone and one hand resting on it, wearing the five-drop necklace, the V "
     "tennis necklace, the white clover bracelet and the baguette dome ring from the references, white linen shirt "
     "open at the collar, hard sunlight. Face out of frame at the top."),
   "הלוק הזה?<br>199 ש״ח.", "שתי שרשראות · צמיד · טבעת",
   "שתי שרשראות, צמיד וטבעת. ככה נראים ארבעה תכשיטים ב-199 ש״ח.\n\nמזמינים היום, מקבלים מחר.",
   "הלוק הזה? 199 ש״ח.", "4 ב-199", "מהיום למחר", people=True)
ad(4, "A1", "9:16", ["drops", "v_tennis", "coin_heart", "tennis_coin", "clover_white", "clover_black", "studs", "ring_pave"],
   P("Eight gold-tone pieces from the references arranged in two neat rows on white linen in hard sunlight with "
     "palm shadows, like a curated jewelry tray."),
   "שמונה תכשיטים.<br>349 ש״ח.", "תכשיט לכל יום בשבוע",
   "שמונה תכשיטים ב-349 ש״ח. זה פחות מ-44 ש״ח לתכשיט.\n\nשרשראות, צמידים, עגילים וטבעות, בגוון זהב או כסף.",
   "שמונה תכשיטים. 349 ש״ח.", "8 תכשיטים ב-349", "8 ב-349")

# ---------- A2 מגן דוד ----------
ad(5, "A2", "4:5", ["star_small"],
   P("Macro close-up of the small pavé Star of David pendant from the reference resting on a woman's sun-warmed "
     "collarbone, fine gold-tone chain, soft white linen neckline, hard warm sunlight catching the stones. Face out "
     "of frame."),
   "קטן על הצוואר.<br>גדול בלב.", "מגן דוד משובץ · 89 ש״ח",
   "מגן דוד עדין ומשובץ, שנשאר על הצוואר כל יום.\n\n89 ש״ח, או חלק מ-4 תכשיטים ב-199.",
   "קטן על הצוואר. גדול בלב.", "שרשרת מגן דוד", "89 ש״ח", people=True)
ad(6, "A2", "1:1", ["star_bold"],
   P("The bold designed Star of David pendant from the reference lying on sun-warmed white plaster, its chain curving "
     "in a soft S, hard sunlight and a crisp shadow, a sprig of olive leaves beside it."),
   "מגן דוד.<br>בסטייל שלכם.", "מגן דוד מעוצב · 89 ש״ח",
   "מגן דוד בעיצוב בולט ונקי, שהולך גם עם טישרט וגם עם שמלה.\n\n89 ש״ח.",
   "מגן דוד, בסטייל שלכם.", "שרשרת מגן דוד מעוצב", "89 ש״ח")
ad(7, "A2", "4:5", ["star_small", "star_bold"],
   P("Two small white linen gift pouches on a sunlit white table, one open with the small pavé Star of David necklace "
     "and the other with the bold Star of David necklace from the references spilling out, olive branch, hard sunlight."),
   "מתנה עם<br>משמעות.", "מגן דוד · מתנה",
   "לאמא, לבת, לחברה הכי טובה. מגן דוד שאומר יותר ממילים.\n\n89 ש״ח לתכשיט, ומשלוח מהיום למחר.",
   "מתנה עם משמעות.", "מגן דוד למתנה", "מהיום למחר")
ad(8, "A2", "4:5", ["star_bold"],
   P("The bold Star of David necklace from the reference hanging from a small brass nail on a sun-warmed white-washed "
     "plaster wall, the pendant catching hard sunlight, a crisp palm-leaf shadow falling across the wall, the chain "
     "casting a thin shadow.", air=ONE),
   "יום יום.<br>כל יום.", "מגן דוד · 89 ש״ח",
   "תכשיט שלא מורידים. לא לים, לא לעבודה, לא לערב.\n\nמגן דוד מעוצב, 89 ש״ח.",
   "יום יום. כל יום.", "שרשרת מגן דוד", "89 ש״ח")

# ---------- A3 מתנה למחר ----------
ad(9, "A3", "4:5", ["heart_toggle"],
   P("Hands tying a thin white satin ribbon around a small sand-coloured gift box on a sunlit white table, the open "
     "box shows the heart toggle bracelet from the reference inside, hard sunlight and palm shadows. Only hands visible."),
   "שכחתם מתנה?<br>מחר היא אצלכם.", "מזמינים היום · מקבלים מחר",
   "יום הולדת מחר ואין מתנה? קורה לטובים ביותר.\n\nמזמינים היום עד הערב, ומקבלים מחר. כל תכשיט 89 ש״ח.",
   "שכחתם מתנה? מחר היא אצלכם.", "מתנה מהיום למחר", "מהיום למחר", people=True)
ad(10, "A3", "1:1", ["coin_heart"],
   P("The disc-and-heart link necklace from the reference coiled inside a small open sand-coloured gift box on white "
     "linen, hard sunlight, a dried flower beside it."),
   "מתנה שנראית<br>יקרה.", "89 ש״ח · משלוח למחר",
   "שרשרת עם לב ומטבע, שנראית הרבה יותר ממה שהיא עלתה.\n\n89 ש״ח, ומגיעה מחר.",
   "מתנה שנראית יקרה.", "שרשרת לב", "89 ש״ח")
ad(11, "A3", "4:5", ["clover_white", "studs"],
   P("Two small open gift boxes side by side on a sunlit white table, one with the white clover tennis bracelet and "
     "one with the disc stud earrings from the references, a handwritten blank card, palm shadows."),
   "שתי מתנות.<br>אותו מחיר.", "4 ב-199 · מתנות",
   "קונים מתנה לה, ומתנה לעצמכם. ארבעה תכשיטים ב-199 ש״ח.\n\nמזמינים היום, מקבלים מחר.",
   "שתי מתנות, אותו מחיר.", "מתנות ב-4 ב-199", "4 ב-199")
ad(12, "A3", "9:16", ["heart_toggle", "coin_heart"],
   P("A small sand-coloured gift box with a white satin ribbon on white-washed steps in hard sunlight, the heart "
     "toggle bracelet and the heart necklace from the references draped over the edge of the box."),
   "הזמנתם היום.<br>היא פותחת מחר.", "משלוח מהיום למחר",
   "מתנה שמגיעה בזמן, בלי לרוץ לקניון.\n\nכל תכשיט 89 ש״ח, ומשלוח מהיום למחר.",
   "הזמנתם היום, היא פותחת מחר.", "משלוח מהיר", "מהיום למחר")

# ---------- A4 שכבות ----------
ad(13, "A4", "4:5", ["v_tennis", "drops", "coin_heart"],
   P("Close-up of a woman's sun-kissed neck and collarbones wearing three layered gold-tone necklaces from the "
     "references — the V tennis, the five drops and the disc-and-heart chain — at three lengths, white linen, hard "
     "sunlight. Face out of frame."),
   "שרשרת אחת זה נחמד.<br>שלוש זה לוק.", "שכבות · 89 ש״ח לשרשרת",
   "הסוד של לוק שכבות: שלוש שרשראות עדינות באורכים שונים.\n\nשלוש שרשראות וצמיד? 4 ב-199.",
   "שרשרת אחת זה נחמד. שלוש זה לוק.", "לוק שכבות", "4 ב-199", people=True)
ad(14, "A4", "1:1", ["drops"],
   P("Macro close-up of the five clear zircon drops necklace from the reference on sun-warmed skin, light sparkling in "
     "the stones, soft white linen edge. Face out of frame.", air=ONE),
   "חמש טיפות<br>של אור.", "שרשרת טיפות · 89 ש״ח",
   "שרשרת עדינה עם חמש טיפות זירקון, שתופסת את האור בכל תנועה.\n\n89 ש״ח.",
   "חמש טיפות של אור.", "שרשרת טיפות", "89 ש״ח", people=True)
ad(15, "A4", "4:5", ["v_tennis", "drops", "coin_heart"],
   P("The V tennis, five-drop and disc-and-heart necklaces from the references laid out as nested curves on white "
     "linen in hard sunlight, showing three lengths, palm shadow across one corner.", air=ONE),
   "ככה בונים<br>שכבות.", "קצרה · בינונית · ארוכה",
   "קצרה צמודה, בינונית עם תליון, וארוכה עם טיפות. זה כל הסוד.\n\n89 ש״ח לשרשרת, 4 ב-199.",
   "ככה בונים שכבות.", "מדריך שכבות", "4 ב-199")
ad(16, "A4", "4:5", ["v_tennis", "studs"],
   P("Photographed from three metres away: a woman in a white linen shirt leaning against one large white-washed wall "
     "in hard sunlight, wearing the V tennis necklace and the disc stud earrings from the references, seen from the "
     "side with her face turned away so only her ear, jaw and neck show, palm shadows on the wall. She is small in the "
     "frame, in the lower-right third; the rest of the frame is the same continuous sunlit wall.", air=ONE),
   "פחות זה<br>יותר.", "שרשרת וי · עגילי עיגול",
   "לפעמים שרשרת אחת ועגילים עדינים זה כל מה שצריך.\n\nכל תכשיט 89 ש״ח.",
   "פחות זה יותר.", "שרשרת ועגילים", "89 ש״ח", people=True)

# ---------- A5 יד מלאה ----------
ad(17, "A5", "4:5", ["tennis_coin", "clover_black", "heart_toggle", "ring_pave"],
   P("A woman's sun-kissed wrist and hand resting on white linen, wearing three stacked gold-tone bracelets from the "
     "references — the pavé disc tennis, the black clover and the heart toggle — and the baguette dome ring, hard "
     "sunlight, crisp shadows. Only the hand and forearm visible."),
   "יד אחת.<br>ארבעה תכשיטים.", "199 ש״ח לכל הסט",
   "שלושה צמידים וטבעת אחת. יד שלמה ב-199 ש״ח.\n\nמזמינים היום, מקבלים מחר.",
   "יד אחת, ארבעה תכשיטים.", "4 ב-199", "4 ב-199", people=True)
ad(18, "A5", "1:1", ["clover_black"],
   P("The black clover station bracelet from the reference lying on sun-warmed white plaster, hard sunlight and a "
     "crisp palm-leaf shadow falling across it."),
   "התלתן<br>שכולן שואלות עליו.", "צמיד תלתן שחור · 89 ש״ח",
   "צמיד התלתן השחור, שהולך עם הכול.\n\n89 ש״ח.",
   "התלתן שכולן שואלות עליו.", "צמיד תלתן", "89 ש״ח")
ad(19, "A5", "4:5", ["ring_pave"],
   P("Macro close-up of a woman's hand with a natural nude manicure resting on white linen, wearing the baguette dome "
     "ring from the reference, light sparkling in the stones, hard sunlight. Only the hand visible."),
   "טבעת אחת<br>שעושה את הלוק.", "טבעת גבעה · 89 ש״ח",
   "טבעת בולטת עם שש שורות זירקונים, שהופכת כל יד ללוק.\n\n89 ש״ח.",
   "טבעת אחת שעושה את הלוק.", "טבעת זירקונים", "89 ש״ח", people=True)
ad(20, "A5", "9:16", ["tennis_coin", "clover_white", "clover_black", "heart_toggle"],
   P("Four gold-tone bracelets from the references stacked on a white ceramic bangle stand on a sunlit white table, "
     "hard sunlight and palm shadows, sand-coloured backdrop."),
   "הערימה שלכם<br>מתחילה כאן.", "צמידים · 4 ב-199",
   "טניס, תלתן לבן, תלתן שחור ולב. ארבעה צמידים ב-199 ש״ח.\n\nמזמינים היום, מקבלים מחר.",
   "הערימה שלכם מתחילה כאן.", "צמידים 4 ב-199", "4 ב-199")

HERO_PROMPT = P("Hero campaign photograph for a fashion jewelry store: a woman's sun-kissed collarbone and shoulder in a "
                "white linen shirt against a white-washed wall in hard Mediterranean sunlight, wearing the V tennis and "
                "five-drop necklaces from the references, her hand at her collarbone with the heart toggle bracelet and "
                "the baguette ring, palm shadows. The woman fills the left half of the frame; the right half is the "
                "same sunlit white wall, calm and empty. Face out of frame at the top.",
                "One continuous photograph — no borders, bands or panels.")
HERO_M_PROMPT = P("Hero campaign photograph for a fashion jewelry store, photographed from three metres away: a woman in "
                  "a white linen shirt standing against one large white-washed wall in hard sunlight, wearing the V "
                  "tennis and five-drop necklaces from the references, palm shadows. She is small in the frame, in the "
                  "lower half, cropped at the chin; everything above her is the same continuous sunlit wall.", air=ONE)

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "hero_m": HERO_M_PROMPT, "ref": REF}, sys.stdout,
              ensure_ascii=False, indent=1)
