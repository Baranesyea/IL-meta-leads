"""Kelev Teva / כלב טבע (lead 2026-09-26-024): research, 5 angles, 20 ads — image prompts + Hebrew copy.

"The first health store for dogs" (Moshav Beit HaLevi): natural and frozen food (Hau & Miau, Henry's), 100% natural
chews (Wiggle buffalo ears, bully sticks), Henry's air-dried treats, Wilda Siberica organic grooming, CAMON joint
support, KONG toys, cat litter. Free shipping over 299, orders by phone / WhatsApp too.
Their ads: six versions of one AI-stock "free shipping over 299" banner + one product photo — no product, no story.
Visual direction (new in the set): warm natural editorial — real dogs in golden outdoor light (meadow, orchard,
farmhouse porch), weathered wood, linen and herbs; product still-lifes on raw wood with the ingredient beside it.
Ads speak to the customer in plural (their own ads do). Meta policy: no health claims beyond the product's own
description, no "is your dog sick?" questions.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-26-024"

REF = {
    "wilda_glow": "934a5ed3-539a-4734-a796-b14e73059377",    # Wilda Siberica organic Glow conditioner, orange pump bottle, ₪69
    "wilda_oil": "e3384f1f-f198-4be0-9715-48fdf971b669",     # Wilda Siberica Oil-Plex conditioner, green pump bottle, ₪69
    "clevercat": "99b3ea62-747d-40ae-81e5-b3209bb487ca",     # Clever Cat lavender clumping litter box 10 L, ₪89
    "buffalo": "acde0ce8-815d-49f5-8baf-468b37f2ee69",       # Wiggle buffalo ears (the chews themselves), ₪99 / ₪189
    "tuna": "57719dd2-946e-4158-8d56-b70383879f35",          # Henry's soft tuna fillet treat pouch, ₪21.90
    "beefcubes": "cdc23e74-d75f-46ff-a27b-f31cac5d0c5d",     # Henry's beef cubes pouch, ₪59
    "bully10": "1e19bba8-894a-4b8b-9b2a-fc1a78a49338",       # bully sticks 10 cm, black window bag, ₪69 / ₪129
    "bully30": "31f4d367-f343-4e75-a4de-8feac4ebe0e5",       # bully stick 30 cm, loose, ₪45
    "duck": "226a5c38-428c-474e-9426-9d24944228ed",          # Henry's duck fillet with pear pouch, ₪24.90
    "condro": "1419f4df-dfdb-44fc-bb3d-dd034bc2dfa2",        # CAMON Condrosalus joint tablets box, ₪189
    "bowl": "0b5bd7f8-f4c8-4cf4-a431-f718ac4a242d",          # ELSPET no-drip steel water bowl 4.5 L, ₪159
    "kong_chicken": "05143430-ccf5-4a0d-8928-271781dffc74",  # KONG Knots chicken rope toy, ₪49–119
    "kong_wubba": "e38854f8-ed6f-47c4-8dd8-c09f89c6debb",    # KONG Wubba Friends fox, ₪99
}

STYLE = ("Premium pet-lifestyle advertising photograph, warm natural editorial: golden late-afternoon light, "
         "weathered wood, linen and fresh herbs, healthy happy real dogs with soft natural fur, shallow depth of field, "
         "shot on medium format, photorealistic. ")
FIDELITY = ("Products must be exact matches of the reference photos: same packaging shapes, colours, labels and logo "
            "layout, same chew shapes — do not redesign them and do not add or change any text on them. No other text, "
            "signage, watermarks or logos anywhere in the image. Animals look natural and healthy, anatomically correct. ")
TOP = ("COMPOSITION: the subject sits in the lower 60% of the frame; above it the same soft background simply continues, "
       "calm and empty — no objects, edges or lines. One continuous photograph — no borders, bands, panels or split "
       "frames.")


def P(scene: str, air: str = TOP) -> str:
    return STYLE + scene + " " + air + " " + FIDELITY


RESEARCH = {
    "one_liner": "חנות בריאות אונליין לכלבים (וגם לחתולים): מזון טבעי וקפוא, חטיפי לעיסה טבעיים, טיפוח אורגני ותוספים. "
                 "₪12–189, משלוח חינם מעל ₪299, הזמנה גם בוואטסאפ. מיצוב: רק מה שבאמת בריא לכלב.",
    "hero_products": ["אוזן בופאלו של וויגל — ₪99 / ₪189", "בולי סטיק 100% טבעי — ₪45–129",
                      "חטיפי הנריס (טונה, קוביות בקר, ברווז) — ₪21.90–59", "מרכך אורגני ווילדה סיביריקה — ₪69",
                      "קונדרוסאלוס למפרקים — ₪189"],
    "audience": [
        {"persona": "ההורה המודע", "who": "נשים וגברים 25–50", "cares": "לתת לכלב רק מה שבריא, בלי תוספים וצבעים"},
        {"persona": "בעלי כלב אנרגטי", "who": "25–45", "cares": "משהו שיעסיק את הכלב ויציל את הרהיטים"},
        {"persona": "הכלב המבוגר", "who": "35–65", "cares": "מפרקים, ניידות ואיכות חיים בגיל מבוגר"},
    ],
    "pains": ["\"החטיפים בסופר מלאים ברכיבים שאני לא מכיר\"", "\"הכלב משתעמם והורס את הבית\"",
              "\"הכלב כבר לא קם כמו פעם\"", "\"שמפו רגיל מייבש לו את הפרווה\""],
    "desires": ["כלב בריא ושמח", "חטיף שאפשר לקרוא את הרכיבים שלו", "שקט בבית", "פרווה רכה ומבריקה"],
    "objections": ["\"טבעי זה יקר\"", "\"זה באמת 100% טבעי?\"", "משלוח", "\"הכלב שלי בררן\""],
    "current_ads_audit": "8 מודעות פעילות, שש מהן אותו באנר בגרסאות שונות: כלב וחתול מאוירים, קופסה ו'משלוח חינם מעל 299'. "
                         "המסר היחיד הוא משלוח. אין מוצר אחד בפוקוס, אין הסבר למה 'חנות בריאות', והוויזואל נראה כמו "
                         "סטוק שכל חנות יכולה להשתמש בו.",
    "gaps": ["המוצרים עצמם לא מופיעים", "הערך 'רק מה שבריא' לא מוסבר", "אין זווית לכלב המבוגר", "חטיפי הלעיסה "
             "הטבעיים — המוצר הכי ויזואלי — לא מקבלים במה", "אין שימוש בכלבים אמיתיים"],
    "angles": [
        {"id": "A1", "name": "רכיב אחד. זהו.", "idea": "חטיפים טבעיים עם רכיב אחד: טונה, בקר, ברווז ואגס. קוראים את הרכיבים ומבינים הכול.", "persona": "ההורה המודע", "hook": "חטיף עם רכיב אחד. זהו.", "why": "עונה ישירות על הפחד מרכיבים לא ברורים."},
        {"id": "A2", "name": "שעה של שקט", "idea": "חטיפי לעיסה טבעיים ארוכים: אוזן בופאלו ובולי סטיק. עסוק, רגוע, ובלי כימיקלים.", "persona": "בעלי כלב אנרגטי", "hook": "שעה של שקט. 100% טבעי.", "why": "כאב יומיומי ומוצר חוזר."},
        {"id": "A3", "name": "פרווה שמבריקה", "idea": "מרככים אורגניים של ווילדה סיביריקה: טיפוח טבעי לפרווה רכה ומבריקה.", "persona": "ההורה המודע", "hook": "פרווה שמבריקה. בלי כימיקלים.", "why": "מוצר טיפוח עם ויזואל יפה ומחיר נגיש."},
        {"id": "A4", "name": "החבר הוותיק", "idea": "לכלב המבוגר: תמיכה במפרקים, קערה נוחה וצעצוע רך.", "persona": "הכלב המבוגר", "hook": "הוא שמר עליכם שנים. עכשיו תורכם.", "why": "קהל רגשי שמוכן להשקיע, ומוצר במחיר גבוה."},
        {"id": "A5", "name": "חנות הבריאות של הכלב", "idea": "החנות עצמה: רק מוצרים שנבחרו בקפידה, משלוח מהיר, חינם מעל 299, הזמנה בוואטסאפ.", "persona": "כולם", "hook": "כל מה שבריא לכלב. במקום אחד.", "why": "בונה זהות לחנות ומעלה סל."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now", people=False):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=None, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=[], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 רכיב אחד. זהו. ----------
ad(1, "A1", "4:5", ["tuna"],
   P("The Henry's tuna fillet treat pouch from the reference standing on a weathered wooden board, a few soft tuna "
     "fillet treats beside it, a sprig of thyme, warm golden window light, soft cream linen backdrop."),
   "חטיף עם רכיב אחד.<br>זהו.", "פילה טונה · 21.90 ש״ח",
   "הפכו את השקית וקראו את הרכיבים: טונה. וזהו.\n\nחטיף פילה טונה מבושל ורך, בלי צבעים ובלי תוספות, שכלבים משתגעים עליו.\n\n21.90 ש״ח למארז.",
   "חטיף עם רכיב אחד. זהו.", "פילה טונה לכלבים", "21.90 ש״ח")
ad(2, "A1", "4:5", ["beefcubes"],
   P("A happy golden retriever sitting on a sunlit farmhouse porch, looking up attentively at a hand offering a single "
     "beef cube treat; the Henry's beef cubes pouch from the reference stands on the wooden porch floor beside the dog. "
     "Only the hand visible, no person."),
   "הוא יודע מה טוב.", "קוביות בקר · 59 ש״ח",
   "קוביות בקר מיובשות, רכיב אחד, בגודל מושלם לאילוף ולפינוק.\n\nמארז חיסכון של 150 גרם ב-59 ש״ח.",
   "הוא יודע מה טוב. קוביות בקר טבעיות.", "קוביות בקר", "59 ש״ח", people=True)
ad(3, "A1", "1:1", ["duck"],
   P("The Henry's duck fillet with pear pouch from the reference on a rustic wooden table, a halved fresh pear and a few "
     "dried duck fillet treats beside it, warm golden light, soft sage-green linen backdrop."),
   "ברווז ואגס.<br>זה כל הסיפור.", "חטיף ברווז · 24.90 ש״ח",
   "פילה ברווז מיובש עם אגס. שני רכיבים שאתם מכירים, בחטיף שהכלב שלכם יאהב.\n\n24.90 ש״ח.",
   "ברווז ואגס. זה כל הסיפור.", "חטיף ברווז ואגס", "24.90 ש״ח")
ad(4, "A1", "9:16", ["tuna", "beefcubes", "duck"],
   P("The three Henry's treat pouches from the references (tuna, beef cubes, duck with pear) standing in a row on a "
     "long weathered wooden shelf, a few loose treats in front, dried herbs, warm golden side light, soft cream wall."),
   "קוראים את הרכיבים.<br>ומבינים הכול.", "חטיפים טבעיים לכלבים",
   "בחנות שלנו אין חטיפים עם רשימת רכיבים של חצי עמוד.\n\nטונה, בקר, ברווז ואגס: חטיפים טבעיים, מיובשים בעדינות, שכלבים אוהבים ובעלים סומכים עליהם.",
   "קוראים את הרכיבים, ומבינים הכול.", "חטיפים טבעיים", "משלוח חינם מעל 299")

# ---------- A2 שעה של שקט ----------
ad(5, "A2", "4:5", ["buffalo"],
   P("A content border collie lying on a sunlit meadow, holding a Wiggle buffalo ear from the reference between its "
     "front paws and chewing it happily, warm golden light, soft green bokeh behind."),
   "שעה של שקט.<br>100% טבעי.", "אוזן בופאלו · מ-99 ש״ח",
   "כלב שלועס הוא כלב רגוע.\n\nאוזן בופאלו של וויגל: חטיף לעיסה טבעי לגמרי, שמעסיק את הכלב ושומר על השיניים.\n\n500 גרם ב-99 ש״ח, קילו ב-189.",
   "שעה של שקט. 100% טבעי.", "אוזן בופאלו טבעית", "מ-99 ש״ח", people=True)
ad(6, "A2", "1:1", ["bully30"],
   P("A single long 30 cm bully stick from the reference lying diagonally on a raw wooden board, warm golden raking "
     "light showing its natural texture, a sprig of rosemary, soft cream backdrop."),
   "30 ס״מ<br>של שקט.", "בולי סטיק · 45 ש״ח",
   "בולי סטיק 30 ס״מ, 100% טבעי, בלי ריח חזק ובלי תוספות.\n\nהלעיסה הארוכה שכל כלב צריך. 45 ש״ח ליחידה.",
   "30 ס״מ של שקט. בולי סטיק טבעי.", "בולי סטיק 30 ס״מ", "45 ש״ח")
ad(7, "A2", "4:5", ["bully10"],
   P("A french bulldog lying on a linen blanket on a wooden floor, happily chewing a short bully stick; the black bully "
     "stick bag from the reference stands beside it, warm afternoon window light."),
   "הספה שלכם<br>תודה לכם.", "בולי סטיק · 10 יח׳",
   "כלב משועמם מוצא לעצמו מה ללעוס. עדיף שזה יהיה בולי סטיק ולא הספה.\n\nמארז 10 בולי סטיק טבעיים ב-129 ש״ח.",
   "הספה שלכם תודה לכם.", "מארז בולי סטיק", "129 ש״ח", people=True)
ad(8, "A2", "9:16", ["buffalo", "bully30"],
   P("Rustic still life: a pile of Wiggle buffalo ears and a few long bully sticks from the references arranged on a "
     "weathered wooden crate, warm golden light, soft neutral linen backdrop."),
   "חטיפי לעיסה.<br>בלי שום דבר מיותר.", "אוזני בופאלו · בולי סטיק",
   "חטיפי לעיסה טבעיים לגמרי: אוזני בופאלו ובולי סטיק, מיובשים בלי תוספות.\n\nלכלבים קטנים וגדולים. משלוח חינם מעל 299 ש״ח.",
   "חטיפי לעיסה, בלי שום דבר מיותר.", "חטיפי לעיסה טבעיים", "משלוח חינם מעל 299")

# ---------- A3 פרווה שמבריקה ----------
ad(9, "A3", "4:5", ["wilda_glow"],
   P("The orange Wilda Siberica Glow conditioner pump bottle from the reference standing on a sunlit wooden bathroom "
     "shelf, sprigs of sea buckthorn with orange berries beside it, soft golden light, cream wall."),
   "פרווה שמבריקה.<br>בלי כימיקלים.", "מרכך אורגני · 69 ש״ח",
   "הפרווה של הכלב נוגעת בכם כל יום. כדאי שתהיה רכה.\n\nמרכך אורגני של ווילדה סיביריקה לברק ולרכות, בלי כימיקלים קשים.\n\n69 ש״ח.",
   "פרווה שמבריקה, בלי כימיקלים.", "מרכך אורגני לפרווה", "69 ש״ח")
ad(10, "A3", "4:5", ["wilda_glow"],
   P("A freshly groomed golden retriever with a glossy, soft, flowing coat sitting on a sunlit wooden porch, its coat "
     "catching the golden light; the orange Wilda Siberica bottle from the reference stands beside it on the boards."),
   "אחרי מקלחת.<br>ככה נראית פרווה.", "ווילדה סיביריקה",
   "יש כלבים שאחרי מקלחת נראים כמו אחרי מספרה.\n\nמרכך אורגני שמשאיר פרווה רכה, מבריקה וריחנית.\n\n69 ש״ח.",
   "אחרי מקלחת, ככה נראית פרווה.", "פרווה רכה ומבריקה", "69 ש״ח", people=True)
ad(11, "A3", "1:1", ["wilda_oil"],
   P("The green Wilda Siberica Oil-Plex conditioner bottle from the reference on a wooden tray with a small glass dish "
     "of golden oil and fresh green herbs, soft golden light, sage-green linen backdrop."),
   "לפרווה ארוכה<br>ומסתבכת.", "אויל פלקס · 69 ש״ח",
   "פרווה ארוכה נוטה להסתבך ולהתייבש.\n\nמרכך אויל־פלקס על בסיס שמנים, לפרווה ארוכה וקשה לסירוק.\n\n69 ש״ח.",
   "לפרווה ארוכה ומסתבכת.", "מרכך לפרווה ארוכה", "69 ש״ח")
ad(12, "A3", "9:16", ["wilda_glow", "wilda_oil"],
   P("The orange and the green Wilda Siberica conditioner bottles from the references standing side by side on a "
     "sunlit weathered wooden bench outdoors, wild flowers and herbs around them, warm golden light, soft meadow bokeh."),
   "טיפוח טבעי.<br>לכל סוג פרווה.", "ווילדה סיביריקה",
   "שני מרככים אורגניים: אחד לברק ולרכות, ואחד לפרווה ארוכה.\n\nטיפוח עדין ובטוח, בלי כימיקלים קשים. 69 ש״ח כל אחד.",
   "טיפוח טבעי לכל סוג פרווה.", "מרככים אורגניים", "69 ש״ח")

# ---------- A4 החבר הוותיק ----------
ad(13, "A4", "4:5", ["condro"],
   P("A calm senior labrador with a greying muzzle resting on a soft linen dog bed by a sunny window; the CAMON "
     "Condrosalus box from the reference stands on the wooden floor beside the bed, warm golden light."),
   "הוא שמר עליכם שנים.<br>עכשיו תורכם.", "קונדרוסאלוס · 189 ש״ח",
   "הכלב שלכם כבר לא קופץ על הספה כמו פעם?\n\nקונדרוסאלוס של CAMON מאיטליה: תוסף לתמיכה במפרקים של כלבים וחתולים, 60 טבליות.\n\n189 ש״ח.",
   "הוא שמר עליכם שנים. עכשיו תורכם.", "תמיכה במפרקים", "189 ש״ח", people=True)
ad(14, "A4", "1:1", ["bowl"],
   P("The ELSPET stainless steel no-drip water bowl from the reference on a wooden kitchen floor, a bearded schnauzer "
     "drinking from it neatly, dry floor around it, warm morning window light."),
   "בלי שלוליות.<br>בלי זקן רטוב.", "קערת שתייה · 159 ש״ח",
   "קערת שתייה חכמה שמונעת טפטוף והרטבה של הפה.\n\n4.5 ליטר, נירוסטה, ורצפה יבשה סוף־סוף. 159 ש״ח.",
   "בלי שלוליות, בלי זקן רטוב.", "קערה מונעת טפטוף", "159 ש״ח", people=True)
ad(15, "A4", "4:5", ["kong_wubba"],
   P("A senior golden retriever lying on a linen blanket, gently holding the KONG Wubba fox plush toy from the reference "
     "in its mouth, warm golden afternoon light, soft cosy interior."),
   "גם בגיל 12<br>מגיע לו צעצוע.", "קונג וובה · 99 ש״ח",
   "כלבים מבוגרים אוהבים לשחק, רק בעדינות.\n\nקונג וובה: צעצוע רך וחזק שנעים להחזיק בפה. 99 ש״ח.",
   "גם בגיל 12 מגיע לו צעצוע.", "צעצוע רך לכלב", "99 ש״ח", people=True)
ad(16, "A4", "4:5", ["condro", "bowl"],
   P("Still life on a weathered wooden floor by a sunny window: the ELSPET steel water bowl and the CAMON Condrosalus box "
     "from the references beside a folded linen dog blanket, warm golden light, calm and cosy."),
   "הבית של<br>החבר הוותיק.", "מפרקים · מים · מנוחה",
   "כל מה שכלב מבוגר צריך כדי להרגיש טוב: תמיכה במפרקים, מים נקיים ומקום רך לנוח.\n\nהכול בחנות אחת, עם משלוח מהיר.",
   "הבית של החבר הוותיק.", "לכלב המבוגר", "משלוח חינם מעל 299")

# ---------- A5 חנות הבריאות של הכלב ----------
ad(17, "A5", "4:5", ["kong_chicken", "buffalo", "tuna"],
   P("An open kraft delivery box on a sunlit wooden porch filled with the KONG chicken rope toy, Wiggle buffalo ears "
     "and the Henry's tuna pouch from the references, a curious beagle sniffing it happily, warm golden light."),
   "כל מה שבריא לכלב.<br>במקום אחד.", "משלוח חינם מעל 299 ש״ח",
   "חטיפים טבעיים, מזון בריא, טיפוח אורגני וצעצועים שנבחרו בקפידה.\n\nכלב טבע: חנות הבריאות לכלבים. משלוח מהיר לכל הארץ, וחינם מעל 299 ש״ח.",
   "כל מה שבריא לכלב, במקום אחד.", "חנות הבריאות לכלבים", "משלוח חינם מעל 299", people=True)
ad(18, "A5", "1:1", ["kong_chicken"],
   P("A playful jack russell terrier mid-leap on a sunlit green meadow catching the KONG chicken rope toy from the "
     "reference, warm golden light, soft bokeh."),
   "משחק שמחזיק.<br>גם מול הכלב שלכם.", "קונג תרנגולת · מ-49 ש״ח",
   "צעצוע חבל קשרים של קונג, שמחזיק משיכות, קפיצות ולעיסות.\n\nשלוש מידות, מ-49 ש״ח.",
   "משחק שמחזיק, גם מול הכלב שלכם.", "צעצוע קונג", "מ-49 ש״ח", people=True)
ad(19, "A5", "4:5", ["clevercat"],
   P("A relaxed grey british shorthair cat sitting on a sunlit wooden floor beside the Clever Cat lavender litter box "
     "from the reference, a sprig of lavender, warm soft light, calm clean home."),
   "גם לחתול<br>מגיע טבעי.", "חול מתגבש · לבנדר",
   "גם החתולים בבית ראויים לטוב ביותר.\n\nחול מתגבש של קלבר קט בניחוח לבנדר ובתוספת פחם פעיל, 10 ליטר. 89 ש״ח.",
   "גם לחתול מגיע טבעי.", "חול לחתולים", "89 ש״ח", people=True)
ad(20, "A5", "9:16", ["buffalo", "wilda_glow", "kong_chicken"],
   P("A rustic wooden shelf in a sunlit farmhouse shop: Wiggle buffalo ears in a glass jar, the orange Wilda Siberica "
     "bottle and the KONG chicken toy from the references, dried herbs, warm golden light, soft cream wall."),
   "הזמנה בוואטסאפ.<br>משלוח עד הבית.", "משלוח חינם מעל 299 ש״ח",
   "לא בא לכם לגלול? שלחו לנו הודעה בוואטסאפ ונעזור לכם לבחור.\n\nמשלוחים מהירים לכל הארץ, וחינם מעל 299 ש״ח.",
   "הזמנה בוואטסאפ, משלוח עד הבית.", "מזמינים בקלות", "משלוח חינם מעל 299")

HERO_PROMPT = P("Hero campaign photograph for a natural health store for dogs: a happy golden retriever lying in a "
                "sunlit golden meadow at sunset, holding a Wiggle buffalo ear from the reference between its paws, warm "
                "backlight glowing through its fur. The dog sits in the lower 60% of the frame; above it the soft golden "
                "sky and meadow bokeh continue, calm and empty.", "One continuous photograph — no borders, bands or panels.")
HERO_M_PROMPT = HERO_PROMPT

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "hero_m": HERO_M_PROMPT, "ref": REF}, sys.stdout,
              ensure_ascii=False, indent=1)
