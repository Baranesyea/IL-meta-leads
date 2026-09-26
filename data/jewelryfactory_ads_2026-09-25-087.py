"""JewelryFactory / ג'ולרי פקטורי (lead 2026-09-25-087): research, 5 angles, 20 ads — image prompts + Hebrew copy.

Visual direction (far from Stav's green fine-jewellery, B-scents' hotel dusk and Asta-In's bright botanics):
masculine and warm — charcoal slate, dark leather, brushed steel, walnut, warm tungsten light, real hands and
wrists, gift moments. The women's line gets soft warm skin tones and cream silk.
Personalised pieces carry engraving: image models garble Hebrew, so engraved plates are shown turned slightly
away / in soft focus, never as a readable close-up; Latin names from the store photos (Rose, Juliana) may show.
Ads speak to the buyer (mostly women buying for him, men buying for her); the page addresses the business in plural.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-25-087"

# Higgsfield media ids of the store's real product photos (jewelryfactory.co.il)
REF = {
    "beads": "5067a556-87e0-48ba-b7e9-61fa837f6abb",     # black braided leather bracelet with steel name beads
    "titan": "833fe0bf-5142-46f3-9c6e-7749615db289",     # silver titanium link bracelet, engraved plate
    "plate": "132d7307-7f31-4322-8393-64e1247b26ef",     # black wrapped leather bracelet with engraved black plate
    "infinity": "499b1a2c-0c21-477f-82b3-ecf87d8d965a",  # gold infinity names bracelet (women)
    "rose": "c1bc6db8-190f-4889-8bb9-ca6703f6db93",      # gold name necklace "Rose" with butterfly
    "juliana": "d3a2f67b-343e-4021-9981-be39098f2996",   # gold script name necklace with heart
    "medal": "0e66a3c6-c292-476b-9bfb-f81c31968fc6",     # men's medallion necklace with Bible chip
    "bar": "9ba894eb-07d0-4ca7-a83b-10754f401e1b",       # gold bar pendant with Bible chip
    "heart": "d93b4aaf-1507-409d-8f9d-1b8be3d88f82",     # gold heart necklace with name beads
    "mesh": "8ab13b83-6cd4-4583-bdbe-ac5a4c3db1ee",      # black mesh titanium bracelet with chip
    "photo": "9f4e1e87-18b1-46c4-8b1e-147a86c09123",     # gold bracelet with photo-engraved heart + chip
}

STYLE = ("Premium editorial jewellery advertising photograph, warm and masculine luxury: charcoal slate, dark leather, "
         "brushed steel, walnut wood, warm tungsten light with deep soft shadows, real skin texture, shot on medium format, "
         "photorealistic, magazine campaign quality. ")
FIDELITY = ("The jewellery must be an exact match of the reference photo: same design, materials, colours, proportions, "
            "links, beads and clasp — do not redesign it. Any engraved lettering stays soft, small or turned slightly "
            "away; never invent new readable letters. No other text, signage, watermarks or logos anywhere in the image. ")


def P(scene: str, air: str) -> str:
    return STYLE + scene + " " + air + " " + FIDELITY


# the "air" must be part of the same photograph — an earlier wording ("one calm surface") made the model bake in
# flat blank bands / side panels (regenerated)
TOP = ("COMPOSITION: the subject sits in the lower 60% of the frame; above it the same scene simply continues as soft, "
       "out-of-focus, evenly lit background (the same wall, window light or sky), with no objects or hard lines in it. "
       "One continuous photograph — no borders, bands, panels, split frames or blank areas.")
SIDE = ("COMPOSITION: the subject sits on one side of the frame; the other 40% of the width is the same scene continuing "
        "as soft, out-of-focus, evenly lit background with no objects or hard lines. One continuous photograph — no "
        "borders, bands, panels, split frames or blank areas.")

RESEARCH = {
    "one_liner": "חנות אונליין לתכשיטים ומתנות עם חריטה אישית: צמידים ושרשראות לגבר ולאישה, תכשיטי שבב תנ״ך, "
                 "ארנקים ותמונות חרוטות. ייצור עצמי תוך 48 שעות. ₪199–799. מיצוב: מתנה אישית ומרגשת במחיר נגיש.",
    "hero_products": ["צמידי עור וטיטניום לגבר עם שמות וחריטה — ₪199", "תכשיטים עם שבב תנ״ך מיקרוסקופי — ₪399",
                      "שרשראות שם וצמידי אינפיניטי לאישה — ₪249–299", "סטים זוגיים ומשפחתיים — ₪799"],
    "audience": [
        {"persona": "מחפשת מתנה לגבר", "who": "נשים 25–55, בנות זוג ואמהות", "cares": "מתנה אישית שהוא באמת יענוד, לא עוד פריט"},
        {"persona": "קונה מתנה לאישה", "who": "גברים 25–50", "cares": "משהו מרגש ובטוח, עם השם שלה, בזמן לאירוע"},
        {"persona": "מתנה עם אמונה", "who": "משפחות מסורתיות, 30–65", "cares": "ברכה ושמירה, יודאיקה עם משמעות"},
    ],
    "pains": ["\"אין לי מושג מה לקנות לו\"", "\"כל המתנות נראות אותו דבר\"", "\"האירוע מחר ועוד אין מתנה\"",
              "\"מפחדת שהחריטה תצא לא טוב\""],
    "desires": ["לראות אותו מתרגש", "מתנה שנשארת שנים", "משהו אישי ששייך רק לו", "להספיק בזמן"],
    "objections": ["איכות וציפוי", "\"איך החריטה תיראה בפועל?\"", "זמני משלוח", "\"זה נראה זול בתמונות\""],
    "current_ads_audit": "15 מודעות פעילות, רובן מקטלוג: מוצר על רקע לבן, אייקונים וכיתוב עמוס, קולאז'ים. "
                         "המודעות רצות 140–290 יום, סימן שהמוצרים מוכרים והקהל קיים. אבל אין רגש, אין אנשים "
                         "ואין רגע של מתנה, והמוצרים נראים זולים יותר ממה שהם.",
    "gaps": ["אין צילום פרימיום של המוצר על אדם", "הרגע של נתינת המתנה לא מופיע", "ייצור תוך 48 שעות קבור בטקסט",
             "הקו לנשים והסטים הזוגיים כמעט לא מקבלים חשיפה", "אין מודעה אחת שמרגישה כמו מותג"],
    "angles": [
        {"id": "A1", "name": "השמות על היד שלו", "idea": "צמיד עם שמות הילדים או בת הזוג: מתנה לגבר שאין לו צורך בכלום.", "persona": "מחפשת מתנה לגבר", "hook": "השמות של הילדים. על היד שלו.", "why": "המוצר הכי נמכר, בזווית רגשית במקום קטלוג."},
        {"id": "A2", "name": "ברכה שהולכת איתו", "idea": "תכשיטי ברכה ושבב תנ״ך: אמונה ושמירה שנושאים כל יום.", "persona": "מתנה עם אמונה", "hook": "כל התנ״ך. בשבב אחד קטן.", "why": "מוצר ייחודי עם סיפור, שמצדיק ₪399."},
        {"id": "A3", "name": "בשבילה", "idea": "שרשראות שם, אינפיניטי ולב עם שמות: הקו לנשים בצילום רך וחם.", "persona": "קונה מתנה לאישה", "hook": "השם שלה. בזהב.", "why": "קהל שני שלם שכמעט לא מקבל תקציב היום."},
        {"id": "A4", "name": "מתנה אישית תוך 48 שעות", "idea": "חריטה בסדנה שלכם וייצור תוך 48 שעות: אמינות, איכות ומהירות.", "persona": "מחפשת מתנה לגבר", "hook": "לא מהמדף. מהסדנה.", "why": "עונה על 'איך זה ייראה' ועל 'יגיע בזמן?'."},
        {"id": "A5", "name": "רגעים שנשארים", "idea": "תמונה חרוטה, סטים זוגיים ומשפחתיים: מתנה לרגעים הגדולים.", "persona": "קונה מתנה לאישה", "hook": "הרגע שלכם. חרוט לתמיד.", "why": "מעלה את סל הקנייה לסטים של ₪799."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now",
       people=False, note=None, verify=None):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=note, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=verify or [], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 השמות על היד שלו ----------
ad(1, "A1", "4:5", ["beads"],
   P("A man's forearm resting on a walnut table in warm morning light, sleeve of a charcoal knit rolled up, wearing the "
     "black braided leather bracelet with steel name beads from the reference; a cup of black coffee beside his hand. "
     "Only forearm and hand in frame.", TOP),
   "השמות של הילדים.<br>על היד שלו.", "צמיד עור עם חריטה אישית",
   "יש גברים שאין להם צורך בכלום. חוץ מהדברים שבאמת חשובים להם.\n\nצמיד עור עם לוחיות פלדה וחריטה אישית של השמות שהוא הכי אוהב.\n\nייצור אישי תוך 48 שעות, 199 ש״ח.",
   "השמות של הילדים, על היד שלו. צמיד עור עם חריטה.",
   "המתנה שהוא לא יוריד", "199 ש״ח · חריטה אישית", people=True)
ad(2, "A1", "1:1", ["beads"],
   P("Still life on dark charcoal slate: the black braided leather bracelet with steel name beads from the reference "
     "coiled loosely, one warm raking light catching the steel beads, a folded crayon drawing by a child softly out of "
     "focus at the edge.", TOP),
   "הוא לא יוריד אותו.<br>אף פעם.", "עור איכותי · פלדת אל־חלד",
   "צמיד עור קלוע עם לוחיות מפלדת אל־חלד, ועליהן השמות שלכם בחריטת לייזר מדויקת.\n\nמתנה שנשארת על היד שלו, יום אחרי יום.\n\n199 ש״ח, משלוח מהיר לכל הארץ.",
   "הוא לא יוריד אותו. צמיד עור עם שמות.",
   "צמיד עם השמות שלכם", "משלוח 1–3 ימים")
ad(3, "A1", "9:16", ["beads"],
   P("A father's large hand holding a toddler's small hand on a sunny living-room rug, warm soft light; the father wears "
     "the black braided leather bracelet with steel name beads from the reference. Only hands and forearms in frame.", TOP),
   "לאבא שיש לו הכול.<br>חוץ מזה.", "חריטה אישית · 199 ש״ח",
   "מה קונים לאבא שיש לו הכול? את השמות של מי שהוא הכי אוהב.\n\nצמיד עור עם לוחיות חרוטות, מוכן אצלנו תוך 48 שעות.\n\nליום הולדת, לחג, או סתם כי מגיע לו.",
   "לאבא שיש לו הכול, חוץ מזה. צמיד עם שמות.",
   "מתנה לאבא עם משמעות", "מוכן תוך 48 שעות", people=True)
ad(4, "A1", "4:5", ["beads"],
   P("An open matte black gift box on dark leather, the black braided leather bracelet with steel name beads from the "
     "reference resting on black velvet inside, a black satin ribbon untied beside it, warm moody spotlight.", TOP),
   "מתנה שהוא<br>באמת יענוד.", "ייצור אישי תוך 48 שעות",
   "את מכירה את זה: קונים לו מתנה, והיא נשארת במגירה.\n\nצמיד עם חריטה אישית הוא מתנה שעונדים. כל יום.\n\nמגיע באריזת מתנה, ייצור תוך 48 שעות.",
   "מתנה שהוא באמת יענוד.",
   "לא עוד מתנה למגירה", "באריזת מתנה")

# ---------- A2 ברכה שהולכת איתו ----------
ad(5, "A2", "4:5", ["titan"],
   P("A man's wrist in a crisp white shirt cuff resting on the leather steering wheel of a car, warm late-afternoon light, "
     "wearing the silver titanium link bracelet from the reference, the engraved plate turned slightly away. Only hand and "
     "wrist in frame.", TOP),
   "ברכה<br>שהולכת איתו.", "צמיד טיטניום עם חריטה",
   "״יברכך ה׳ וישמרך״ חרוט על צמיד טיטניום, שהולך איתו לכל מקום.\n\nמתכת חזקה שלא מחלידה, וחריטה אישית שנשארת.\n\n199 ש״ח.",
   "ברכה שהולכת איתו. צמיד טיטניום עם חריטה.",
   "יברכך ה׳ וישמרך", "199 ש״ח")
ad(6, "A2", "1:1", ["medal"],
   P("Dramatic macro still life: the round medallion necklace with the tiny inset chip from the reference lying on dark "
     "charcoal linen, a single warm beam of light across the medallion, deep shadows.", TOP),
   "כל התנ״ך.<br>בשבב אחד קטן.", "שרשרת עם שבב תנ״ך",
   "בתוך השבב הזעיר שבתליון נמצאים כל 24 ספרי התנ״ך, בכתב מיקרוסקופי.\n\nשרשרת עם ברכה חרוטה ושבב תנ״ך, בכסף או בזהב.\n\n399 ש״ח.",
   "כל התנ״ך בשבב אחד קטן. שרשרת לגבר.",
   "כל התנ״ך, קרוב ללב", "כסף או זהב · 399 ש״ח")
ad(7, "A2", "9:16", ["bar"],
   P("The gold bar pendant with the small blue chip from the reference hanging on its chain, softly swinging, sharp against "
     "a deep warm blurred background of golden bokeh, elegant and quiet.", TOP),
   "שמירה.<br>קרוב ללב.", "תליון עם שבב תנ״ך",
   "תליון זהב עם ברכה חרוטה ושבב שמכיל את כל התנ״ך.\n\nמתנה של שמירה, לבן, לבעל או לאבא.\n\n399 ש״ח, באריזת מתנה.",
   "שמירה, קרוב ללב. תליון עם שבב תנ״ך.",
   "מתנה של שמירה", "באריזת מתנה")
ad(8, "A2", "4:5", ["plate"],
   P("A man in a dark denim jacket with his hand casually in his jeans pocket, warm golden-hour street light, wearing the "
     "black wrapped leather bracelet with the black engraved plate from the reference, plate turned slightly away. Crop "
     "from chest to hip, no face.", TOP),
   "יוצא לדרך?<br>שיהיה לו איתו.", "צמיד עור עם לוחית חרוטה",
   "לפני טיסה, לפני משימה, לפני התחלה חדשה.\n\nצמיד עור עם לוחית חרוטה, עם ברכה או מילים שרק שניכם מבינים.\n\n199 ש״ח, מוכן תוך 48 שעות.",
   "יוצא לדרך? שיהיה לו איתו.",
   "המילים שילוו אותו", "199 ש״ח", people=True)

# ---------- A3 בשבילה ----------
ad(9, "A3", "4:5", ["rose"],
   P("Close crop of a woman's collarbone and neckline in soft golden-hour light, wearing the gold script name necklace "
     "\"Rose\" with the small butterfly from the reference, a cream silk blouse, warm skin. Crop from the chin down, no "
     "face.", TOP),
   "השם שלה.<br>בזהב.", "שרשרת שם · ציפוי זהב 14K",
   "שרשרת עם השם שלה, בכתב יד עדין ובציפוי זהב 14K.\n\nמתנה שהיא תענוד כל יום, ותזכיר לה ממי קיבלה.\n\n249 ש״ח.",
   "השם שלה, בזהב. שרשרת שם בציפוי 14K.",
   "שרשרת עם השם שלה", "249 ש״ח", people=True)
ad(10, "A3", "1:1", ["infinity"],
   P("A woman's wrist and hand holding a white ceramic coffee cup at a sunlit café table, wearing the gold infinity names "
     "bracelet from the reference, soft warm morning light, cream knit sleeve.", TOP),
   "שני שמות.<br>לנצח.", "צמיד אינפיניטי · 299 ש״ח",
   "סימן האינסוף עם שני השמות שלכם, חרוטים בצמיד אחד.\n\nלבת הזוג, לאמא, או לחברה הכי טובה.\n\n299 ש״ח.",
   "שני שמות, לנצח. צמיד אינפיניטי.",
   "צמיד אינפיניטי עם שמות", "299 ש״ח", people=True)
ad(11, "A3", "9:16", ["heart"],
   P("The gold heart necklace with small name beads from the reference resting in an open cream jewellery box on ivory "
     "silk, soft warm window light, delicate and romantic.", TOP),
   "לב אחד.<br>כל המשפחה.", "שרשרת לב עם שמות",
   "לב זהב עם חרוזים קטנים, ועל כל אחד שם של מישהו שהיא אוהבת.\n\nמתנה מושלמת לאמא ולסבתא.\n\nבאריזת מתנה, ייצור תוך 48 שעות.",
   "לב אחד, כל המשפחה. שרשרת עם שמות.",
   "כל המשפחה בלב אחד", "באריזת מתנה")
ad(12, "A3", "4:5", ["juliana"],
   P("A woman's hands lifting the gold script name necklace with the small heart from the reference out of an open gift "
     "box on her lap, tissue paper and ribbon around, warm soft light. Only hands and lap in frame.", TOP),
   "הרגע שהיא פותחת<br>ומבינה.", "שרשרת שם עם לב",
   "יש מתנות שפותחים ואומרים תודה. ויש מתנות שפותחים ושותקים לרגע.\n\nשרשרת עם השם שלה ולב קטן, בציפוי זהב.\n\n249 ש״ח.",
   "הרגע שהיא פותחת ומבינה. שרשרת שם.",
   "המתנה שעוצרת לה את הנשימה", "249 ש״ח", people=True)

# ---------- A4 מתנה אישית תוך 48 שעות ----------
ad(13, "A4", "4:5", ["titan"],
   P("Macro of a fibre-laser engraving machine at work in a dark workshop: a fine bright laser point and a thin wisp of "
     "smoke on the steel plate of the silver titanium link bracelet from the reference, warm amber glow, sparks of light.", TOP),
   "חרוט במיוחד.<br>בשבילו.", "ייצור אישי תוך 48 שעות",
   "כל צמיד נחרט אצלנו, אחד־אחד, בלייזר מדויק.\n\nאתם בוחרים את המילים, ואנחנו דואגים שהן ייראו מושלם.\n\nייצור תוך 48 שעות, משלוח לכל הארץ.",
   "חרוט במיוחד בשבילו. ייצור תוך 48 שעות.",
   "חריטת לייזר מדויקת", "ייצור תוך 48 שעות")
ad(14, "A4", "1:1", ["rose"],
   P("A craftsperson's hands at a wooden jeweller's bench polishing the gold name necklace from the reference with a soft "
     "cloth, small tools around, warm lamp light, shallow depth of field. Only hands in frame.", TOP),
   "לא מהמדף.<br>מהסדנה.", "משלוח 1–3 ימים",
   "כל תכשיט אצלנו נעשה לפי הזמנה, עם השם או המילים שבחרתם.\n\nבודקים, מלטשים, אורזים, ושולחים.\n\nמשלוח לכל הארץ תוך 1–3 ימים.",
   "לא מהמדף, מהסדנה. תכשיטים בהתאמה אישית.",
   "נעשה בשבילכם", "משלוח 1–3 ימים", people=True)
ad(15, "A4", "9:16", ["beads"],
   P("A small matte black gift box tied with a black ribbon on a warm wooden doorstep in morning light, the black braided "
     "leather bracelet with steel name beads from the reference peeking out from the half-open lid.", TOP),
   "מתנה אישית.<br>אצלך תוך 48 שעות.", "משלוח לכל הארץ",
   "שכחת שהיום הולדת בשבוע הבא? זה קורה.\n\nמזמינים היום, ותוך 48 שעות המתנה האישית מוכנה ויוצאת אליך.\n\nצמידים, שרשראות וארנקים עם חריטה.",
   "מתנה אישית, אצלך תוך 48 שעות.",
   "עוד מספיקים", "ייצור תוך 48 שעות")
ad(16, "A4", "4:5", ["mesh"],
   P("The black mesh titanium bracelet with the small chip from the reference floating diagonally over a dark brushed "
     "steel surface, one clean rim light, precise and technical, deep shadows.", TOP),
   "טיטניום.<br>נבנה להישאר.", "צמיד טיטניום עם שבב",
   "צמיד רשת מטיטניום שחור, קל ונוח לכל היום, עם שבב שמכיל את כל התנ״ך.\n\nעיצוב נקי שמתאים לכל שעון ולכל סגנון.\n\n399 ש״ח.",
   "טיטניום, נבנה להישאר. צמיד עם שבב תנ״ך.",
   "צמיד טיטניום שחור", "399 ש״ח")

# ---------- A5 רגעים שנשארים ----------
ad(17, "A5", "4:5", ["photo"],
   P("A woman's wrist resting on a cream linen tablecloth in warm soft light, wearing the gold bracelet with the "
     "photo-engraved heart charm from the reference, a few dried flowers nearby. Only hand and wrist in frame.", TOP),
   "התמונה שלכם.<br>על היד שלה.", "צריבת תמונה אישית",
   "תמונה אהובה, חרוטה על לב זהב קטן בצמיד.\n\nהזוגיות, הילדים או רגע אחד שלא רוצים לשכוח.\n\n399 ש״ח.",
   "התמונה שלכם, על היד שלה.",
   "רגע אחד, לתמיד", "399 ש״ח", people=True)
ad(18, "A5", "1:1", ["beads", "infinity"],
   P("A couple's hands gently intertwined on a warm wooden table, his wrist wearing the black braided leather bracelet "
     "with steel name beads from the first reference, her wrist wearing the gold infinity names bracelet from the second "
     "reference, soft evening light. Only hands and wrists in frame.", TOP),
   "שניכם.<br>חרוטים.", "צמידים זוגיים",
   "צמיד בשבילו, צמיד בשבילה, והשמות שלכם על שניהם.\n\nמתנה ליום נישואין, לחתונה או לסתם יום שבא לחגוג.\n\nמ-199 ש״ח.",
   "שניכם, חרוטים. צמידים זוגיים עם שמות.",
   "צמידים זוגיים", "מ-199 ש״ח", people=True)
ad(19, "A5", "9:16", ["plate"],
   P("Dark moody men's gift flat lay on charcoal leather: the black wrapped leather bracelet with the engraved black plate "
     "from the reference, an open matte black gift box, a folded blank cream card, warm spotlight from above.", TOP),
   "יום הולדת.<br>יום נישואין.<br>סתם יום.", "מתנות לגבר",
   "לא צריך סיבה כדי לתת לו משהו שישמח אותו.\n\nצמידים, ארנקים ושרשראות עם חריטה אישית, באריזת מתנה.\n\nמזמינים היום, מקבלים תוך ימים.",
   "יום הולדת, יום נישואין, סתם יום. מתנות לגבר.",
   "מתנה לכל סיבה", "באריזת מתנה")
ad(20, "A5", "4:5", ["heart"],
   P("An elderly woman's hand holding a young girl's hand, the grandmother wearing the gold heart necklace with name beads "
     "from the reference visible at her collar, soft warm window light, gentle and tender. Crop from shoulders to hands, "
     "no faces.", TOP),
   "סבתא תענוד<br>את כולם.", "שרשרת לב עם שמות",
   "כל הנכדים, כל הילדים, בלב אחד קטן שהיא תענוד כל יום.\n\nמתנה שסבתא לא תשכח.\n\nבאריזת מתנה, ייצור תוך 48 שעות.",
   "סבתא תענוד את כולם. שרשרת לב עם שמות.",
   "המתנה לסבתא", "באריזת מתנה", people=True)

HERO_PROMPT = P("Hero campaign photograph for a personalised jewellery brand: a man's strong forearm resting on dark "
                "charcoal slate in one warm raking beam of light, wearing the black braided leather bracelet with steel "
                "name beads from the reference, deep dramatic shadows, rich warm tones. Only forearm and hand in frame.",
                "The upper 45% of the frame must be dark, calm and empty. Portrait 4:5.")

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "ref": REF}, sys.stdout, ensure_ascii=False, indent=1)
