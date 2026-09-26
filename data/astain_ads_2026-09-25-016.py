"""Asta-In / אסטאין (lead 2026-09-25-016): research, 5 angles, 20 ads — image prompts + Hebrew copy.

Visual direction (far from Stav's dark jewellery and B-scents' warm hotel dusk): bright botanical-biotech —
white stone, clear water, fresh green, glass, morning light, and one recurring accent: the deep red of
astaxanthin (the algae's pigment). Clean, clinical-natural, airy.
Ads speak to the customer in feminine singular (their own ads do); the page addresses the business in plural.
Meta policy: no personal-attribute questions, no cure claims — "skin prone to blemishes", "supports", "balance".
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-25-016"

# Higgsfield media ids of the store's real product photos (astain.co.il)
REF = {
    "soap": "3c9256ac-c62d-4baa-a9ad-d6cc1e178427",      # facial peeling soap bar (yellow box)
    "oxy50": "cb4156aa-4d9c-4ecb-a42d-a766f0ba1f60",     # Oxy Asta 50 ml, box + airless bottle
    "serum": "6d27be7e-a605-4801-8ad4-2f28a81c6e6a",     # astaxanthin serum, box + airless bottle
    "cream": "65e55d03-6581-4bec-93d3-c51c94d1520f",     # facial cream airless bottle
    "toner": "4b5d3a1e-746d-44cd-a3e2-bd3d8e58e19f",     # toner spray bottle
    "shampoo": "97eba50f-a4ce-489a-aa52-2c2d68b759e5",
    "conditioner": "31d210e2-8ab7-4cfb-bd96-722d01f2337a",
    "mask": "77beec8e-e031-4056-9c04-fc80d2605f55",      # hair mask jar + box
    "lotion": "7d05e6b9-73c6-42d2-a23e-23bc337b81aa",    # body lotion airless
    "liquidsoap": "9b249da4-82e5-45a4-91ef-5e33010c6a17",
    "lip": "659da535-ba49-419c-90a3-4db5fd0375b7",       # lip balm + box
    "collagen": "5c89ae57-b48c-4b22-ae6c-7330f64f0637",  # Puremagics astaxanthin+collagen (owner company's brand)
    "curcumin": "892fdf2a-f950-4e94-83f4-fdd821653798",  # Puremagics astaxanthin+curcumin
    "oxy100": "3406c9d0-8a90-43f8-bdcb-6118673cc628",    # Oxy Asta 100 ml tall airless bottle
}

STYLE = ("Premium editorial beauty advertising photograph, bright botanical-biotech aesthetic: white stone, clear water, "
         "fresh green leaves, glass, soft morning daylight, airy and clean, one deep-red accent of natural astaxanthin where "
         "it fits, shot on medium format, photorealistic, magazine campaign quality. ")
FIDELITY = ("The products must be exact matches of the reference photos: same shape, proportions, colors, green stripe, "
            "logo and label layout — do not redesign them, do not add or change any text on them. No other text, "
            "signage, watermarks or logos anywhere in the image. ")


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
    "one_liner": "מותג קוסמטיקה טבעית של חברת ביוטכנולוגיה ישראלית שמגדלת בעצמה את האצה האדומה ומפיקה ממנה אסטקסנטין. "
                 "מתמקד בעור עם נטייה לפצעונים, לצד שיער, גוף ותוספים. ₪46–519. מיצוב: טבעי-מדעי, ישראלי, בינוני-גבוה.",
    "hero_products": ["ערכת 3 שלבים לעור נוטה לפצעונים: סבון מוצק, אוקסי אסטה וסרום — ₪492 (במקום ₪692)",
                      "סרום פעיל אסטקסנטין — ₪349", "אוקסי אסטה (משחת אוזון) — ₪249 / ₪379",
                      "מארזי שיער וגוף — ₪179 / ₪235; תוספי אסטקסנטין — ₪159"],
    "audience": [
        {"persona": "הצעירה עם העור הרגיש", "who": "נשים 16–30", "cares": "עור נקי בלי להסתיר במייקאפ, שגרה פשוטה, מוצר טבעי שעובד"},
        {"persona": "האמא שקונה לבת", "who": "נשים 40–55", "cares": "מוצר בטוח, טבעי ומאושר, שלא מייבש ולא מגרה"},
        {"persona": "הטבעונית המודעת", "who": "נשים 25–45", "cares": "רכיבים טבעיים, טבעוני, מיוצר בישראל, שקיפות"},
    ],
    "pains": ["\"אני מסתירה את הפנים עם מייקאפ\"", "\"ניסיתי הכול והעור רק מתייבש\"", "\"סימנים אחרי פצעונים שלא עוברים\"",
              "\"מוצרים חריפים שמגרים לי את העור\""],
    "desires": ["לצאת מהבית בלי מייקאפ", "עור רגוע ואחיד", "שגרה קצרה שמחזיקים בה", "מוצר טבעי שאפשר לסמוך עליו"],
    "objections": ["\"טבעי זה באמת עובד?\"", "מחיר הערכה (₪492)", "\"זה יתאים לעור שלי?\"", "\"עוד מותג שמבטיח\""],
    "current_ads_audit": "8 מודעות פעילות, כולן סרטוני UGC בסגנון טיקטוק (בנות מדברות למצלמה, צילום מסך מוואטסאפ, "
                         "קופסה ירוקה ביד). המסר החזק 'את לא צריכה להתאפר' רץ 30–38 יום בכמה גרסאות. אין אף ויזואל "
                         "מוצר מקצועי, והסיפור הכי חזק של המותג — החווה והאצה — לא מופיע בכלל.",
    "gaps": ["אין ויזואל פרימיום אחד", "סיפור החווה והאצה האדומה לא מסופר", "אמון: אישור משרד הבריאות, טבעוני ומיוצר "
             "בישראל כמעט לא מוצגים", "מארזי השיער, הגוף והתוספים לא מקבלים חשיפה", "אין הסבר של 3 השלבים בתמונה"],
    "angles": [
        {"id": "A1", "name": "מהאצה לעור", "idea": "הסיפור שאף מתחרה לא יכול להעתיק: האצה האדומה שגדלה בחווה שלכם בשפלה והופכת לסרום.", "persona": "הטבעונית המודעת", "hook": "מהחווה שלנו בשפלה. ישר לעור שלך.", "why": "אמון ובידול: מקור אמיתי ושקוף במקום עוד הבטחה."},
        {"id": "A2", "name": "שגרת 3 השלבים", "idea": "ניקוי, טיפול, איזון. שגרה קצרה וברורה שמסבירה את הערכה במבט אחד.", "persona": "הצעירה עם העור הרגיש", "hook": "3 שלבים. בוקר וערב.", "why": "פשטות מוכרת: לקוחה מבינה בדיוק מה היא קונה ואיך משתמשים."},
        {"id": "A3", "name": "בלי להסתיר", "idea": "המסר שכבר עובד לכם, 'את לא צריכה להתאפר', בשפה ויזואלית יוקרתית ואופטימית.", "persona": "הצעירה עם העור הרגיש", "hook": "הפנים שלך. בלי פילטר.", "why": "הרגש שמניע את הקנייה, בלי להצביע על הבעיה."},
        {"id": "A4", "name": "המדע שבטבע", "idea": "אסטקסנטין, אוזון, איזון PH: הרכיבים כגיבורים, בצילום נקי של מעבדה וטבע.", "persona": "האמא שקונה לבת", "hook": "נוגד חמצון עוצמתי. מהאצה האדומה.", "why": "עונה על 'טבעי זה באמת עובד?' ומצדיק מחיר."},
        {"id": "A5", "name": "טיפוח לכל הגוף", "idea": "שיער, גוף, שפתיים ותוספים: הרחבת הסל ללקוחות שכבר מכירות את המותג.", "persona": "הטבעונית המודעת", "hook": "מהשיער ועד הגוף.", "why": "הגדלת שווי הזמנה וקנייה חוזרת."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now",
       people=False, note=None, verify=None):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=note, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=verify or [], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 מהאצה לעור ----------
ad(1, "A1", "4:5", ["serum"],
   P("Inside a sunlit greenhouse of a microalgae farm: rows of tall transparent glass tubes filled with glowing red-orange "
     "algae culture, deeply out of focus in the background as soft red-orange bokeh (no visible roof beams or frames); in the foreground, the serum box and bottle from the reference stand on "
     "a clean white stone ledge, crisp and sharp, morning light.", TOP),
   "מהחווה שלנו בשפלה.<br>ישר לעור שלך.", "אסטקסנטין טבעי · מיוצר בישראל",
   "את האצה האדומה אנחנו מגדלים בעצמנו, בחווה שלנו במושב יד רמב״ם.\n\nממנה אנחנו מפיקים אסטקסנטין טבעי, נוגד חמצון עוצמתי, והוא הלב של כל מוצר של Asta-In.\n\nמהחווה ישר לעור שלך. בלי מתווכים ובלי הפתעות.\n\nסרום פעיל אסטקסנטין, 349 ש״ח.",
   "מהחווה שלנו בשפלה ישר לעור שלך. סרום אסטקסנטין טבעי.",
   "מהחווה שלנו לעור שלך", "סרום פעיל אסטקסנטין")
ad(2, "A1", "1:1", ["serum"],
   P("Macro still life: a single glossy deep-red drop of natural astaxanthin oil resting on a clear glass slab, the serum "
     "bottle from the reference standing sharp just behind it, fresh green leaves softly out of focus, bright white light.", TOP),
   "טיפה אדומה אחת.<br>כל הכוח של האצה.", "סרום פעיל אסטקסנטין",
   "הצבע האדום של האסטקסנטין הוא לא צבע מאכל. זה הפיגמנט של האצה עצמה.\n\nבסרום של Asta-In הוא מגיע יחד עם חומצה היאלורונית ושמנים בוטניים, להזנה, לחות ומראה רענן יותר.\n\nטבעוני, מיוצר בישראל, מאושר ע״י משרד הבריאות.",
   "טיפה אדומה אחת, כל הכוח של האצה. סרום אסטקסנטין.",
   "הסרום עם הכוח של האצה", "349 ש״ח · 50 מ״ל")
ad(3, "A1", "9:16", ["serum"],
   P("A researcher's hand in a white lab coat sleeve holding up a clear glass flask of vivid red algae culture against the "
     "light; the serum box and bottle from the reference stand sharp on the white lab bench below; bright clean laboratory "
     "with soft daylight, green plants softly out of focus. No face in frame.", TOP),
   "ביוטכנולוגיה ישראלית.<br>בבקבוק אחד.", "מאושר ע״י משרד הבריאות",
   "Asta-In שייך לחברת ביוטכנולוגיה ישראלית שמתמחה בגידול האצה Haematococcus pluvialis והפקת אסטקסנטין טבעי.\n\nאנחנו לא קונים חומר גלם. אנחנו מגדלים אותו, בודקים אותו ומפתחים ממנו את המוצרים.\n\nכל המוצרים טבעוניים, מאושרים ע״י משרד הבריאות ומיוצרים בישראל.",
   "ביוטכנולוגיה ישראלית, מהאצה ועד הבקבוק.",
   "מדע ישראלי, בבקבוק אחד", "מאושר ע״י משרד הבריאות", people=True)
ad(4, "A1", "4:5", ["serum", "cream"],
   P("The serum and facial cream bottles from the references standing on a smooth wet river stone half-covered with soft "
     "green moss, clear water gently rippling around the stone, fresh morning light, dew drops.", TOP),
   "טבעי. טבעוני.<br>ישראלי.", "לא נוסה על בעלי חיים",
   "רכיבים טבעיים, בלי ניסויים בבעלי חיים, בייצור ישראלי לפי תקני ISO, HACCP ו-GMP.\n\nכל מוצר של Asta-In מתחיל באצה שאנחנו מגדלים בעצמנו, ומסתיים בעור שלך.",
   "טבעי, טבעוני, ישראלי. קוסמטיקה מהאצה האדומה.",
   "טבעי, טבעוני, ישראלי", "משלוח חינם מעל 450 ש״ח")

# ---------- A2 שגרת 3 השלבים ----------
ad(5, "A2", "4:5", ["soap", "oxy50", "serum"],
   P("The three products from the references (the yellow soap bar box, the Oxy Asta box and bottle, the serum box and "
     "bottle) lined up left to right on a white marble bathroom ledge, a folded white cotton towel and a sprig of green "
     "eucalyptus beside them, soft morning window light.", TOP),
   "3 שלבים.<br>בוקר וערב.", "סבון · אוקסי אסטה · סרום",
   "שגרה של 3 שלבים לעור עם נטייה לפצעונים:\n\n1. ניקוי עדין עם סבון מוצק מועשר באוזון ואסטקסנטין.\n2. טיפול נקודתי עם אוקסי אסטה.\n3. איזון והזנה עם הסרום הפעיל.\n\nבוקר וערב, כמה דקות. הערכה המלאה ב-492 ש״ח במקום 692.",
   "3 שלבים, בוקר וערב. ערכה לעור עם נטייה לפצעונים.",
   "3 שלבים לעור רגוע", "492 ש״ח במקום 692")
ad(6, "A2", "1:1", ["soap", "oxy50", "serum"],
   P("Top-down flat lay on a pale sage-green stone surface: the three products from the references (soap bar in its box, "
     "the Oxy Asta bottle, the serum bottle) arranged in a calm row, a few eucalyptus leaves, clear water droplets, soft "
     "daylight with gentle shadows.", TOP),
   "שגרה אחת.<br>שלושה צעדים.", "ערכת 3 שלבים · 492 ש״ח",
   "לא צריך מדף מלא מוצרים. צריך שגרה נכונה.\n\nסבון, אוקסי אסטה וסרום: שלושה מוצרים שנבנו לעבוד יחד, לעור שנוטה לפצעונים, לאדמומיות ולשומניות.\n\n17 ביקורות, דירוג 4.94 מתוך 5.",
   "שגרה אחת, שלושה צעדים. ערכת Asta-In.",
   "הערכה שבנויה לעבוד יחד", "דירוג 4.94 מתוך 5")
ad(7, "A2", "4:5", ["soap"],
   P("A young woman in her early twenties at a bright white bathroom sink, eyes closed, gently washing her face with soft "
     "white foam, fresh and calm; the yellow soap bar box from the reference stands sharp on the ledge in the foreground. "
     "Natural skin, no makeup.", SIDE),
   "מתחילים בניקוי.<br>עדין.", "סבון מוצק מועשר באוזון",
   "השלב הראשון בשגרה: סבון מוצק בעבודת יד, מועשר באוזון, אסטקסנטין ושמנים טהורים.\n\nמנקה לעומק בלי לייבש, ומשאיר את העור רך ונקי.\n\n85 ש״ח, 100 גרם.",
   "סבון מוצק עם אוזון ואסטקסנטין. ניקוי עדין בלי לייבש.",
   "ניקוי שלא מייבש", "85 ש״ח · 100 גרם", people=True)
ad(8, "A2", "9:16", ["oxy50"],
   P("Close-up still life: a fingertip holding a tiny dab of smooth white cream just above the open Oxy Asta bottle from "
     "the reference, the product box standing beside it, clean white background with soft green reflections.", TOP),
   "טיפול נקודתי.<br>בדיוק איפה שצריך.", "אוקסי אסטה",
   "אוקסי אסטה משלבת גז אוזון ואסטקסנטין בנוסחה אחת, לטיפול נקודתי בעור בעייתי.\n\nמנקה, מטהרת ומרגיעה את האזור, בדיוק איפה שצריך.\n\n249 ש״ח, 50 מ״ל.",
   "טיפול נקודתי עם אוזון ואסטקסנטין. אוקסי אסטה.",
   "טיפול נקודתי חכם", "אוזון + אסטקסנטין")

# ---------- A3 בלי להסתיר ----------
ad(9, "A3", "4:5", ["serum"],
   P("Portrait of a young woman in her early twenties by a bright window, natural fresh skin with no makeup, laughing "
     "openly, hair loosely tied back, soft daylight; she holds the serum bottle from the reference low near her collarbone. "
     "Joyful, confident, real.", SIDE),
   "הפנים שלך.<br>בלי פילטר.", "שגרת טיפוח טבעית",
   "יש ימים שבא לך פשוט לצאת מהבית. בלי שכבה, בלי להסתיר.\n\nשגרת Asta-In בנויה בדיוק לזה: ניקוי, טיפול ואיזון, עם אסטקסנטין טבעי מהאצה האדומה.\n\nהערכה המלאה ב-492 ש״ח.",
   "הפנים שלך, בלי פילטר. שגרת טיפוח טבעית.",
   "פחות להסתיר, יותר לחיות", "ערכת 3 שלבים")
ad(10, "A3", "1:1", ["serum"],
   P("Still life on a white vanity: a closed foundation compact and a makeup brush pushed aside at the edge, slightly out "
     "of focus; the serum box and bottle from the reference stand sharp in the centre, a sprig of green leaves, bright "
     "morning light.", TOP),
   "פחות מייקאפ.<br>יותר עור.", "סרום פעיל אסטקסנטין",
   "המייקאפ יכול לחכות.\n\nהסרום הפעיל של Asta-In מזין את העור באסטקסנטין, חומצה היאלורונית ושמנים בוטניים, למראה רענן, חלק וקורן יותר.\n\n349 ש״ח במקום 399.",
   "פחות מייקאפ, יותר עור. סרום אסטקסנטין.",
   "המייקאפ יכול לחכות", "349 ש״ח במקום 399")
ad(11, "A3", "9:16", ["serum"],
   P("A young woman in a white robe in a sunlit bathroom, seen from the side, pressing a pump of serum from the bottle in "
     "the reference onto her fingertips, calm morning ritual, soft steam and daylight, natural skin.", TOP),
   "חמש דקות בבוקר.<br>זה כל הסוד.", "שגרת 3 שלבים",
   "שגרה טובה היא שגרה שמחזיקים בה.\n\nשלושה מוצרים, כמה דקות בבוקר ובערב. בלי שלבים מסובכים ובלי עשרה בקבוקים.\n\nערכת Asta-In לעור עם נטייה לפצעונים, 492 ש״ח.",
   "חמש דקות בבוקר, זה כל הסוד.",
   "שגרה שמחזיקים בה", "ערכת 3 שלבים", people=True)
ad(12, "A3", "4:5", ["serum"],
   P("Two young women in their early twenties laughing together outdoors in soft golden-hour sunlight in a green field, "
     "natural skin without makeup, light linen clothes; one holds the serum box from the reference casually. Candid, warm, "
     "premium lifestyle.", TOP),
   "עור רגוע.<br>ראש רגוע.", "טבעי · מיוצר בישראל",
   "כשהעור רגוע, הכול קל יותר.\n\nAsta-In נולד מאצה שגדלה בשפלה ומהרצון לתת לעור עם נטייה לפצעונים שגרה טבעית ועדינה.\n\nמשלוח חינם בקנייה מעל 450 ש״ח.",
   "עור רגוע, ראש רגוע. קוסמטיקה טבעית מהאצה.",
   "עור רגוע, ראש רגוע", "משלוח חינם מעל 450 ש״ח", people=True)

# ---------- A4 המדע שבטבע ----------
ad(13, "A4", "1:1", ["serum"],
   P("Clinical still life: the serum bottle from the reference standing beside a clear glass laboratory beaker of water "
     "into which a vivid deep-red cloud of astaxanthin is slowly swirling, bright white background, fresh green leaf "
     "reflections, precise and clean.", TOP),
   "נוגד חמצון עוצמתי.<br>מהאצה האדומה.", "אסטקסנטין טבעי",
   "אסטקסנטין הוא הפיגמנט שהופך את האצה האדומה לאדומה, ואחד מנוגדי החמצון המוערכים בטבע.\n\nהוא מסייע להגן על העור מפני נזקי סביבה, לחות וגמישות, ומראה זוהר ובריא יותר.\n\nאצלנו הוא מגיע ישר מהחווה.",
   "נוגד חמצון עוצמתי, מהאצה האדומה.",
   "למה דווקא אסטקסנטין?", "הרכיב שבלב המותג")
ad(14, "A4", "4:5", ["cream"],
   P("Macro beauty shot: a soft sculpted swirl of rich white face cream with a faint coral sheen on a white stone, the "
     "facial cream bottle from the reference standing sharp behind it, fresh green leaf, bright diffused light.", TOP),
   "מרקם שנספג.<br>ומשאיר את העור רך.", "קרם פנים טבעי",
   "קרם פנים עם אסטקסנטין טבעי ושמנים בוטניים.\n\nמרקם קליל שנספג מהר, מעניק לחות לאורך היום ומשאיר את העור רך ונעים.\n\nחלק מהמארז המשקם לפנים.",
   "קרם פנים עם אסטקסנטין. נספג מהר, משאיר עור רך.",
   "לחות שנספגת מהר", "מארז פנים משקם")
ad(15, "A4", "9:16", ["toner"],
   P("The toner spray bottle from the reference releasing a fine backlit mist, tiny droplets glowing in bright morning "
     "light, clean white and soft green background, fresh and airy.", TOP),
   "איזון PH.<br>בריסוס אחד.", "טונר מרגיע",
   "טונר מרגיע ומאזן PH, בין הניקוי לסרום.\n\nמרענן, מרגיע ומכין את העור לספוג את מה שבא אחריו.\n\n119 ש״ח.",
   "טונר מרגיע ומאזן PH. בריסוס אחד.",
   "רגע של רעננות", "119 ש״ח")
ad(16, "A4", "4:5", ["oxy100"],
   P("The tall Oxy Asta bottle from the reference standing in shallow crystal-clear water on white stone, streams of fine "
     "tiny bubbles rising around it, bright clean light with soft green reflections, fresh and precise.", TOP),
   "אוזון ואסטקסנטין.<br>בנוסחה אחת.", "אוקסי אסטה · 100 מ״ל",
   "האוזון ידוע בזכות תכונותיו המטהרות. האסטקסנטין בזכות ההגנה וההרגעה.\n\nבאוקסי אסטה הם עובדים יחד, לטיפוח עור בעייתי.\n\nעכשיו גם בגודל 100 מ״ל, 379 ש״ח.",
   "אוזון ואסטקסנטין בנוסחה אחת. אוקסי אסטה 100 מ״ל.",
   "שני כוחות, נוסחה אחת", "עכשיו גם 100 מ״ל")

# ---------- A5 טיפוח לכל הגוף ----------
ad(17, "A5", "4:5", ["shampoo", "conditioner", "mask"],
   P("The shampoo, conditioner and hair mask from the references on a pale stone shower bench, soft steam, water droplets "
     "on the bottles, a eucalyptus bundle hanging, bright spa-like daylight.", TOP),
   "גם לשיער<br>מגיע טבעי.", "מארז שיער · 179 ש״ח",
   "שמפו, מרכך ומסכה משקמת, כולם עם אסטקסנטין טבעי.\n\nבלי פרבנים ובלי SLS, לשיער רך, מלא ומוזן.\n\nמארז השיער ב-179 ש״ח.",
   "מארז שיער טבעי עם אסטקסנטין. 179 ש״ח.",
   "מארז שיער טבעי", "בלי פרבנים ובלי SLS")
ad(18, "A5", "1:1", ["lotion", "liquidsoap"],
   P("The body lotion and liquid soap bottles from the references on a folded white linen towel on the edge of a white "
     "stone bath, a few green leaves floating in clear water, calm evening spa light.", TOP),
   "ערב אחד.<br>רק בשבילך.", "מארז גוף · 235 ש״ח",
   "סבון נוזלי, פילינג וקרם גוף משקם, עם אסטקסנטין ושמנים טבעיים.\n\nערב אחד בשבוע רק בשבילך. העור ירגיש את זה כל השבוע.\n\nמארז הגוף ב-235 ש״ח.",
   "ערב אחד רק בשבילך. מארז גוף טבעי.",
   "מארז גוף משקם", "235 ש״ח")
ad(19, "A5", "4:5", ["lip"],
   P("Clean beauty still life: the lip balm and its box from the reference lying on a smooth white stone beside a single "
     "fresh red rose petal and a green leaf, bright soft daylight.", TOP),
   "לחות לשפתיים.<br>לכל היום.", "שפתון טיפולי · 46 ש״ח",
   "שפתון טיפולי עם אסטקסנטין ושמנים טבעיים.\n\nלחות והגנה לשפתיים לאורך כל היום, בגודל שנכנס לכל תיק.\n\n46 ש״ח.",
   "שפתון טיפולי טבעי. לחות לכל היום.",
   "הלחות שנכנסת לכל תיק", "46 ש״ח")
ad(20, "A5", "9:16", ["collagen", "curcumin"],
   P("The two supplement jars from the references on a sunlit white kitchen counter beside a clear glass of water and a "
     "few red capsules on a small ceramic dish, fresh green herbs in soft focus, bright morning light.", TOP),
   "טיפוח מבחוץ.<br>וגם מבפנים.", "תוספי אסטקסנטין",
   "האסטקסנטין שלנו לא נעצר בקרמים.\n\nתוספי תזונה עם אסטקסנטין וקולגן, או אסטקסנטין וכורכומין, מאותה אצה שאנחנו מגדלים בשפלה.\n\n159 ש״ח.",
   "טיפוח מבחוץ וגם מבפנים. תוספי אסטקסנטין.",
   "האסטקסנטין שלנו, מבפנים", "159 ש״ח")

HERO_PROMPT = P("Hero campaign photograph for a natural skincare brand: the serum box and bottle from the first reference "
                "standing on a smooth white stone in shallow crystal-clear water, a single deep-red cloud of astaxanthin "
                "gently swirling in the water beside it, soft green leaves at the lower edge, bright pure morning light.",
                "The upper 45% of the frame must be a calm, empty, softly lit pale background with nothing in it. Portrait 4:5.")

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "ref": REF}, sys.stdout, ensure_ascii=False, indent=1)
