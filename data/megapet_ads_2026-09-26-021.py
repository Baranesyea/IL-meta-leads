"""Mega Pet / מגה פט (lead 2026-09-26-021): research, 5 angles, 20 ads — image prompts + Hebrew copy.

Pet food and supplies store in Be'er Sheva (Yosef HaBurskai 1) with a central distribution warehouse in Ra'anana and
an online store (~1,100 products): Royal Canin, Acana, Pro Plan, Advance, Friskies, Hunt natural chews, Bark toys,
beds. Free fast shipping to the whole country, same day or within 24h around Be'er Sheva, orders by phone *6897 and WhatsApp.
Their ads: eight long "why us" texts (cat food, fleas, toys, dog food, puppy food, treats, beds) on stock-like
visuals — all eight send people to the home page — plus four recent deal flyers (Advance / Acana second bag 20% off,
Royal Canin pouches ₪79, 10% off flea products) that land on product and deal pages.
Visual direction (new in the set): bold colour-studio pet portraits — real dogs and cats on seamless saturated paper
backdrops (teal, mustard, coral, cobalt), crisp soft studio light, the product beside them. Punchy, premium, and very
different from what any pet store in Israel runs.
Ads speak to the customer in plural (their own ads do). Meta policy: no medical claims, no "does your dog have fleas?".
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-26-021"

REF = {
    "rc_pouch": "c32349bf-d1a4-45a7-affb-bc1483b4463a",   # Royal Canin cat pouches, 12-pack boxes; ₪94.8 (deal ₪79)
    "rc_puppy": "01aa88e1-80f9-4ecd-843d-597a80e88cc3",   # Royal Canin Junior Giant dry food bag (light blue), ₪329
    "rc_large": "145b5709-e6f8-4161-b3a1-b9b8d043cba6",   # Royal Canin Maxi Adult dry food bag (dark blue), ₪279
    "acana_cat": "fb03d616-a2c9-49ef-8f43-9f555bfd5914",  # Acana Indoor Entrée cat food bag (pink), ₪159
    "friskies": "73ad9dbf-6767-4855-b016-d697705f5822",   # Friskies Party Mix treats jar, ₪99
    "hunt_yak": "386ac480-3deb-447d-bb95-0a9ad0dcead0",   # HUNT bully stick & yak cheese pouch (dark bag), ₪169
    "bed": "e5e48cdf-a1d1-4346-8d75-da262d53c3f1",        # OB round plush donut bed (mocha), from ₪189
    "sloth": "0a73f93d-c33a-4f39-9b5c-190a87b363d5",      # BARK hide-and-seek sloth plush toy, ₪89
}

STYLE = ("Premium pet advertising photograph, bold colour-studio portrait: a seamless saturated paper backdrop in one "
         "strong colour, crisp soft studio light with a gentle shadow on the floor, healthy real animals with natural "
         "fur and bright eyes, clean minimal set, shot on medium format, photorealistic, magazine quality. ")
FIDELITY = ("Products must be exact matches of the reference photos: same bag, box, jar and toy shapes, same colours, "
            "same labels and logo layout — do not redesign them and do not add or change any text on them. No other "
            "text, signage, watermarks or logos anywhere in the image. Animals look natural and healthy, anatomically "
            "correct, with the right number of legs and ears. ")
TOP = ("COMPOSITION: the subject sits in the lower 60% of the frame; above it the same seamless coloured backdrop simply "
       "continues, calm and empty — no objects, edges or lines. One continuous photograph — no borders, bands, panels "
       "or split frames.")


def P(scene: str, air: str = TOP) -> str:
    return STYLE + scene + " " + air + " " + FIDELITY


RESEARCH = {
    "one_liner": "חנות מזון וציוד לחיות מחמד בבאר שבע עם מחסן הפצה ברעננה ואתר של כ-1,100 מוצרים: רויאל קנין, אקאנה, "
                 "פרו פלאן, אדוונס, פריסקיז, חטיפי האנט וצעצועי בארק. ₪6–329, משלוח חינם ומהיר לכל הארץ, באותו יום "
                 "באזור באר שבע, הזמנות גם ב-6897* ובוואטסאפ. מיצוב: המותגים המובילים, עד הבית, מהר.",
    "hero_products": ["רויאל קנין (מזון יבש ופאוצ'ים) — ₪79–329", "אקאנה לחתול — ₪159", "חטיפי לעיסה של האנט — ₪44–169",
                      "צעצועי בארק — ₪69–119", "מיטות פרוותיות — מ-₪169"],
    "audience": [
        {"persona": "בעלי כלב גדול", "who": "25–55", "cares": "שק מזון כבד שמגיע עד הבית, בלי לסחוב"},
        {"persona": "אנשי החתולים", "who": "20–50", "cares": "מזון איכותי ופינוקים שהחתול באמת אוכל"},
        {"persona": "הורים לגור", "who": "25–40", "cares": "להתחיל נכון: מזון לגור, צעצועים ומיטה"},
    ],
    "pains": ["\"לסחוב שק של 15 ק״ג מהחנות\"", "\"המזון נגמר בדיוק בשישי בערב\"", "\"הכלב הורס כל צעצוע תוך יום\"",
              "\"החתול בררן\"", "\"בחנות השכונתית אין את המותג שלנו\""],
    "desires": ["מזון שמגיע לפני שנגמר", "כלב עסוק ושמח", "חתול מפונק", "המותג הנכון במחיר טוב"],
    "objections": ["\"באתרים הגדולים זה זול יותר\"", "זמן משלוח", "\"זה מקורי?\"", "\"אני לא מכיר את החנות\""],
    "current_ads_audit": "14 מודעות פעילות. שמונה מהן רצות כבר ארבעה חודשים: טקסט ארוך של 'למה דווקא אצלנו' על חתולים, "
                         "פרעושים, צעצועים, מזון לגורים, חטיפים ומיטות, עם תמונות שנראות כמו סטוק. כל השמונה, עם שמונה "
                         "נושאים שונים, מובילות לדף הבית, כך שמי שלחץ על מיטה לכלב צריך לחפש אותה מחדש. ארבע מודעות המבצע "
                         "החדשות (אדוונס, אקאנה, פאוצ'ים ב-79, הדברה) עושות את זה נכון ומובילות לעמוד המוצר או המבצע.",
    "gaps": ["שמונה מודעות עם שמונה נושאים שונים מובילות לדף הבית", "אין חיה אמיתית אחת שנראית טוב",
             "המשלוח המהיר, היתרון הכי חזק מול החנות השכונתית, קבור בתוך רשימה", "אין פרסום לפי מותג, למרות שקונים לפי מותג",
             "הטקסטים ארוכים, והמסר הראשון לא עוצר גלילה"],
    "angles": [
        {"id": "A1", "name": "המותג שלהם, עד הבית", "idea": "רויאל קנין ואקאנה: המזון שהכלב והחתול כבר אוכלים, בלי לסחוב שק מהחנות.", "persona": "בעלי כלב גדול", "hook": "15 ק״ג. בלי לסחוב.", "why": "קונים מזון לפי מותג, והכאב של הסחיבה ברור."},
        {"id": "A2", "name": "פינוק לחתול", "idea": "פאוצ'ים של רויאל קנין במבצע ופריסקיז פארטי מיקס: הדברים שהחתול מחכה להם.", "persona": "אנשי החתולים", "hook": "החתול כבר שמע את הצנצנת.", "why": "קנייה חוזרת, מחיר נמוך ומבצע קיים."},
        {"id": "A3", "name": "עסוק ושמח", "idea": "חטיפי לעיסה של האנט וצעצועי בארק: שעה של עיסוק בלי שהבית ישלם על זה.", "persona": "הורים לגור", "hook": "הצעצוע שלו. לא הנעל שלכם.", "why": "כאב יומיומי ומוצרים ויזואליים."},
        {"id": "A4", "name": "מקום משלו", "idea": "מיטות פרוותיות עגולות: המקום שהכלב והחתול בוחרים לעצמם.", "persona": "כולם", "hook": "יש לו מקום משלו.", "why": "מוצר רגשי עם סל גבוה."},
        {"id": "A5", "name": "מגה פט, עד הבית", "idea": "החנות עצמה: המותגים המובילים, משלוח חינם ומהיר לכל הארץ, באזור באר שבע באותו יום או תוך 24 שעות.", "persona": "כולם", "hook": "נגמר המזון? מחר הוא אצלכם.", "why": "בונה זהות לחנות סביב היתרון החזק ביותר שלה."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now", people=False):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=None, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=[], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 המותג שלהם, עד הבית ----------
ad(1, "A1", "4:5", ["rc_large"],
   P("A proud german shepherd sitting upright beside the dark blue Royal Canin Maxi Adult bag from the reference, "
     "on a seamless deep cobalt blue paper backdrop, crisp soft studio light."),
   "15 ק״ג.<br>בלי לסחוב.", "רויאל קנין מקסי · 279 ש״ח",
   "שק מזון של כלב גדול לא אמור לעבור דרך הגב שלכם.\n\nרויאל קנין מקסי אדולט, ומשלוח חינם ומהיר עד הדלת.\n\n279 ש״ח.",
   "15 ק״ג. בלי לסחוב.", "רויאל קנין מקסי אדולט", "279 ש״ח", people=True)
ad(2, "A1", "4:5", ["rc_puppy"],
   P("A fluffy big-breed puppy (young bernese mountain dog) sitting with its paws on the light blue Royal Canin Junior "
     "Giant bag from the reference, head tilted, on a seamless warm mustard yellow paper backdrop."),
   "הוא יגדל מהר.<br>תנו לו להתחיל נכון.", "רויאל קנין ג'וניור ג'איינט",
   "גור מגזע ענק צריך מזון שבנוי בדיוק בשבילו.\n\nרויאל קנין ג'וניור ג'איינט, 329 ש״ח, עם משלוח חינם עד הבית.",
   "הוא יגדל מהר. תנו לו להתחיל נכון.", "מזון לגור מגזע ענק", "329 ש״ח", people=True)
ad(3, "A1", "1:1", ["acana_cat"],
   P("An elegant tabby cat sitting calmly beside the pink Acana Indoor bag from the reference, on a seamless soft coral "
     "paper backdrop, crisp studio light."),
   "חתול של בית.<br>מזון של בית.", "אקאנה אינדור · 159 ש״ח",
   "אקאנה אינדור לחתולים שחיים בבית: עוף והרינג כמרכיב ראשון, ומזון שמתאים לחתול מעוקר.\n\n159 ש״ח, משלוח חינם.",
   "חתול של בית. מזון של בית.", "אקאנה לחתול אינדור", "159 ש״ח", people=True)
ad(4, "A1", "4:5", ["rc_large", "rc_puppy", "acana_cat"],
   P("The three food bags from the references (dark blue Royal Canin Maxi, light blue Royal Canin Junior Giant, pink "
     "Acana) standing in a neat row on a seamless deep teal paper backdrop, a relaxed labrador lying in front of them."),
   "המותג שלהם.<br>עד הדלת.", "רויאל קנין · אקאנה · פרו פלאן",
   "הם כבר יודעים מה הם אוהבים. אתם רק צריכים שזה יגיע.\n\nכל המותגים המובילים, משלוח חינם ומהיר לכל הארץ.",
   "המותג שלהם, עד הדלת.", "המותגים המובילים", "משלוח חינם לכל הארץ", people=True)

# ---------- A2 פינוק לחתול ----------
ad(5, "A2", "4:5", ["friskies"],
   P("A curious ginger cat reaching up with one paw toward the Friskies Party Mix treats jar from the reference that "
     "stands on a small white cube, on a seamless bright teal paper backdrop."),
   "החתול כבר שמע<br>את הצנצנת.", "פריסקיז פארטי מיקס · 99 ש״ח",
   "יש צליל אחד שכל חתול מזהה מכל מקום בבית.\n\nצנצנת פריסקיז פארטי מיקס בטעמי ים, 99 ש״ח.",
   "החתול כבר שמע את הצנצנת.", "פריסקיז פארטי מיקס", "99 ש״ח", people=True)
ad(6, "A2", "1:1", ["rc_pouch"],
   P("The Royal Canin cat pouch boxes from the reference stacked neatly on a seamless soft lilac paper backdrop, a "
     "grey british shorthair cat peeking out from behind the stack."),
   "12 פאוצ'ים.<br>79 ש״ח.", "במקום 94.80 ש״ח",
   "הארוחה שהחתול מחכה לה, במחיר שמחכה לכם.\n\n12 פאוצ'ים של רויאל קנין ב-79 ש״ח במקום 94.80.",
   "12 פאוצ'ים ב-79 ש״ח.", "פאוצ'ים רויאל קנין", "79 ש״ח", people=True)
ad(7, "A2", "4:5", ["rc_pouch", "friskies"],
   P("A fluffy white persian cat lounging on a seamless warm mustard paper backdrop between the Royal Canin pouch boxes "
     "and the Friskies Party Mix jar from the references, looking straight at the camera."),
   "היא יודעת<br>מה מגיע לה.", "פינוקים לחתול",
   "פאוצ'ים, חטיפים ומעדנים לחתולים שיודעים בדיוק מה הם רוצים.\n\nמשלוח חינם ומהיר לכל הארץ.",
   "היא יודעת מה מגיע לה.", "פינוקים לחתול", "משלוח חינם", people=True)
ad(8, "A2", "9:16", ["friskies"],
   P("The Friskies Party Mix jar from the reference tipped slightly on its side on a seamless coral paper backdrop, a "
     "small scatter of colourful cat treats spilling out, a playful kitten paw entering from the side."),
   "חטיף אחד.<br>חבר לכל החיים.", "פריסקיז · 99 ש״ח",
   "רוצים שהחתול יבוא כשקוראים לו? יש לנו רעיון.\n\nפריסקיז פארטי מיקס, 99 ש״ח לצנצנת.",
   "חטיף אחד, חבר לכל החיים.", "חטיפים לחתול", "99 ש״ח", people=True)

# ---------- A3 עסוק ושמח ----------
ad(9, "A3", "4:5", ["hunt_yak"],
   P("A happy border collie lying on a seamless bright teal paper backdrop, holding a long natural bully stick between "
     "its front paws; the dark HUNT bully stick & yak cheese pouch from the reference stands beside it."),
   "שעה של לעיסה.<br>שעה של שקט.", "האנט בולי סטיק · 169 ש״ח",
   "בולי סטיק וגבינת יאק של האנט: חטיף לעיסה טבעי, בלי חומרים משמרים, שמעסיק את הכלב לאורך זמן.\n\n169 ש״ח.",
   "שעה של לעיסה, שעה של שקט.", "האנט בולי סטיק ויאק", "169 ש״ח", people=True)
ad(10, "A3", "1:1", ["sloth"],
   P("A playful golden retriever puppy tugging gently at the BARK sloth plush toy from the reference, on a seamless "
     "soft coral paper backdrop, crisp studio light."),
   "הצעצוע שלו.<br>לא הנעל שלכם.", "בארק סוני העצלן · 89 ש״ח",
   "צעצוע מחבואים של בארק: מסתירים בתוכו את הצעצועים הקטנים, והכלב עסוק בלמצוא אותם.\n\n89 ש״ח.",
   "הצעצוע שלו, לא הנעל שלכם.", "צעצוע בארק", "89 ש״ח", people=True)
ad(11, "A3", "4:5", ["sloth", "hunt_yak"],
   P("The BARK sloth toy and the HUNT pouch from the references arranged on a seamless deep cobalt paper backdrop, a "
     "jack russell terrier jumping playfully in the air above them, crisp studio light, motion frozen."),
   "אנרגיה?<br>יש לנו פתרון.", "צעצועים וחטיפי לעיסה",
   "כלב עם אנרגיה צריך איפה להוציא אותה.\n\nצעצועים שמחזיקים וחטיפי לעיסה טבעיים, במשלוח חינם עד הבית.",
   "אנרגיה? יש לנו פתרון.", "צעצועים לכלבים", "משלוח חינם", people=True)
ad(12, "A3", "9:16", ["hunt_yak"],
   P("The dark HUNT bully stick & yak cheese pouch from the reference standing on a seamless warm mustard paper "
     "backdrop, three natural bully sticks leaning against it, crisp studio light and a soft shadow."),
   "רכיב אחד.<br>בלי תוספות.", "חטיפי האנט · מ-44 ש״ח",
   "חטיפי האנט הם חטיפים טבעיים לגמרי: בולי סטיק, ריאות באפלו וזנב באפלו. בלי דגנים ובלי חומרים משמרים.\n\nמ-44 ש״ח.",
   "רכיב אחד, בלי תוספות.", "חטיפי לעיסה טבעיים", "מ-44 ש״ח")

# ---------- A4 מקום משלו ----------
ad(13, "A4", "4:5", ["bed"],
   P("A small cream pomeranian curled up asleep in the round plush mocha donut bed from the reference, on a seamless "
     "soft sage green paper backdrop, soft warm studio light."),
   "יש לו<br>מקום משלו.", "מיטה פרוותית עגולה · מ-189 ש״ח",
   "המיטה העגולה והפרוותית שכלבים וחתולים פשוט נעלמים בתוכה.\n\nבמגוון מידות, מ-189 ש״ח.",
   "יש לו מקום משלו.", "מיטה פרוותית עגולה", "מ-189 ש״ח", people=True)
ad(14, "A4", "1:1", ["bed"],
   P("A grey tabby cat stretching lazily inside the round plush mocha donut bed from the reference, on a seamless soft "
     "lilac paper backdrop, crisp soft studio light."),
   "הספה חזרה<br>להיות שלכם.", "מיטה לכלב ולחתול",
   "תנו להם מקום רך משלהם, והם יפסיקו לחפש את שלכם.\n\nמיטה פרוותית עגולה, מ-189 ש״ח.",
   "הספה חזרה להיות שלכם.", "מיטה פרוותית", "מ-189 ש״ח", people=True)
ad(15, "A4", "4:5", ["bed", "sloth"],
   P("A sleepy french bulldog resting its chin on the BARK sloth toy inside the round plush mocha donut bed from the "
     "references, on a seamless warm mustard paper backdrop."),
   "סוף יום.<br>לכולם.", "מיטה · צעצוע · שקט",
   "אחרי יום שלם של משחק, כל אחד צריך את הפינה שלו.\n\nמיטות וצעצועים לכלבים ולחתולים, במשלוח חינם עד הבית.",
   "סוף יום, לכולם.", "מיטות וצעצועים", "משלוח חינם", people=True)
ad(16, "A4", "4:5", ["bed"],
   P("Two round plush mocha donut beds from the reference side by side on a seamless deep teal paper backdrop, a dog "
     "sleeping in one and a cat sleeping in the other, crisp soft studio light."),
   "שלום בית.<br>סוף סוף.", "מיטה לכל אחד",
   "כשלכל אחד יש מיטה משלו, אף אחד לא רב על המקום.\n\nמיטה פרוותית עגולה, במגוון מידות, מ-189 ש״ח.",
   "שלום בית, סוף סוף.", "מיטה לכל אחד", "מ-189 ש״ח", people=True)

# ---------- A5 מגה פט, עד הבית ----------
ad(17, "A5", "4:5", ["rc_large", "friskies", "sloth"],
   P("An open kraft delivery box on a seamless bright teal paper backdrop, holding the dark blue Royal Canin bag, the "
     "Friskies jar and the BARK sloth toy from the references, a curious beagle and a tabby cat both sniffing it."),
   "נגמר המזון?<br>מחר הוא אצלכם.", "משלוח חינם ומהיר לכל הארץ",
   "מזמינים באתר, בטלפון או בוואטסאפ, והכול מגיע עד הדלת.\n\nמשלוח חינם ומהיר לכל הארץ, ובאזור באר שבע באותו יום או תוך 24 שעות.",
   "נגמר המזון? מחר הוא אצלכם.", "מגה פט", "משלוח חינם לכל הארץ", people=True)
ad(18, "A5", "1:1", ["rc_pouch", "acana_cat", "hunt_yak"],
   P("The Royal Canin pouch boxes, the pink Acana bag and the HUNT pouch from the references arranged in a bold "
     "graphic stack on a seamless coral paper backdrop, crisp studio light, no animals."),
   "כל המותגים.<br>חנות אחת.", "מגה פט · באר שבע",
   "רויאל קנין, אקאנה, פרו פלאן, אדוונס, פריסקיז והאנט. יותר מ-1,000 מוצרים לכלבים ולחתולים.\n\nמשלוח חינם לכל הארץ.",
   "כל המותגים, חנות אחת.", "המותגים המובילים", "משלוח חינם")
ad(19, "A5", "4:5", ["rc_puppy"],
   P("A delighted young labrador sitting at a front door threshold on a seamless mustard paper backdrop set, the light "
     "blue Royal Canin Junior Giant bag from the reference placed at the doorstep beside it, crisp studio light."),
   "הזמנתם היום.<br>זה כבר בדרך.", "באזור באר שבע · תוך 24 שעות",
   "גרים באזור באר שבע? ההזמנה מגיעה אליכם באותו יום או תוך 24 שעות.\n\nבשאר הארץ, משלוח חינם ומהיר.",
   "הזמנתם היום, זה כבר בדרך.", "משלוח מהיר", "באזור באר שבע", people=True)
ad(20, "A5", "4:5", ["rc_large", "rc_pouch"],
   P("A tall stack of the dark blue Royal Canin bag and the Royal Canin pouch boxes from the references on a seamless "
     "deep cobalt paper backdrop, a calm husky sitting beside the stack looking up at the camera."),
   "מתקשרים 6897*<br>ואנחנו דואגים לשאר.", "הזמנה בטלפון ובוואטסאפ",
   "לא בא לכם לגלול? מתקשרים ל-6897* או שולחים הודעה בוואטסאפ, ואנחנו נעזור לבחור.\n\nמשלוח חינם ומהיר לכל הארץ.",
   "מתקשרים 6897*, אנחנו דואגים לשאר.", "הזמנה בטלפון", "משלוח חינם", people=True)

HERO_PROMPT = P("Hero campaign photograph for a pet food and supplies store: a happy golden retriever and a tabby cat "
                "sitting side by side on a seamless deep teal paper backdrop, the dark blue Royal Canin Maxi bag and the "
                "Friskies jar from the references standing beside them, crisp soft studio light. The animals and "
                "products sit in the lower 60% of the frame on the left half; above and to the right the teal backdrop "
                "continues, calm and empty.", "One continuous photograph — no borders, bands or panels.")
HERO_M_PROMPT = P("Hero campaign photograph for a pet food and supplies store: a happy golden retriever and a tabby cat "
                  "sitting side by side on a seamless deep teal paper backdrop, the dark blue Royal Canin Maxi bag from "
                  "the reference beside them, crisp soft studio light. The animals sit in the lower 50% of the frame, "
                  "centred; the top half is the same teal backdrop, calm and empty.",
                  "One continuous photograph — no borders, bands or panels.")

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "hero_m": HERO_M_PROMPT, "ref": REF}, sys.stdout,
              ensure_ascii=False, indent=1)
