"""Hair Cosmetics / הייר קוסמטיקס (lead 2026-09-25-039): research, 5 angles, 20 ads — image prompts + Hebrew copy.

An online store for professional hair products (Paul Mitchell, G.Cosmetics, pH Health&Hair, Elian, B-YOU, Biotop 101).
Their own ads are already tidy (pink satin, BEST SELLER ribbons), so the gap is not polish but story: every ad is the
same product-on-satin template with a price. Their real audience is curly hair (glaze, foam) and damaged hair.
Visual direction (far from Stav's green jewellery, B-scents' hotel dusk, Asta-In's botanics, JewelryFactory's dark
leather and My Deal's bold colour-block): tone-on-tone sculptural studio — matte plaster plinths, arches and curved
walls in ONE soft tone per ad (clay, sand, sage, powder blue, charcoal), soft sculpted light, the product's own
texture (glossy gel ribbon, foam cloud, water beads) as the hero detail, and real women with defined curls.
Ads speak to the customer in feminine singular (their ads do); the men's pair speaks masculine.
Meta policy: no personal-attribute questions; results as "looks / feels", no medical claims.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-25-039"

# Higgsfield media ids of the store's product photos (haircosmetics.co.il)
REF = {
    "pm_glaze": "70987759-f83b-4244-aa67-d80cba068bd7",   # Paul Mitchell Super Sculpt glaze 1 L, white bottle
    "g_glaze": "beba447e-2e05-435c-a8b0-be089a583b9e",    # G.Cosmetics Silk & Cotton curl glaze 500 ml, silver bottle
    "pm_foam": "97af97ff-f95c-4174-90a0-b91512610c4b",    # Paul Mitchell sculpting foam 500 ml, white can
    "neuro": "993b8247-457b-450f-bc69-2e6e04865562",      # Paul Mitchell Neuro Repair HeatCTRL mask, blue tube
    "byou": "2fbfb6db-f408-45e4-afd7-f5883f012122",       # B-YOU keratin hair mask 500 ml, pale blue jar + box
    "elian": "7b140bb0-2cae-4d45-afea-dff54e1411e6",      # Elian keratin ampoule 10 ml
    "ph": "0fc5366a-6511-42e3-8754-bece4bc4cf7c",         # pH Protein+ / Micro Protein / Blonde+ trio
    "pomade": "5f0a84c7-cb99-4a1d-8715-ff82be50842a",     # Biotop 101 Pro Shaper pomade, mint jar
    "box": "714df9d3-bdc3-4b84-bbbc-fbf4ed07a20c",        # Summer Mystery Box, colourful printed box
}

STYLE = ("Premium beauty advertising photograph, tone-on-tone sculptural studio: matte plaster plinths, soft arches "
         "and curved walls all in one soft colour, gentle sculpted directional light with soft shadows, calm and "
         "expensive, shot on medium format, photorealistic. ")
FIDELITY = ("The products must be exact matches of the reference photos: same bottle, jar and tube shapes, colours, "
            "caps, labels and logo layout — do not redesign them and do not add or change any text on them. No other "
            "text, signage, watermarks or logos anywhere in the image. ")

TOP = ("COMPOSITION: the subject sits in the lower 60% of the frame; above it the same seamless wall simply continues, "
       "evenly lit and empty — no objects, edges or lines. One continuous photograph — no borders, bands, panels or "
       "split frames.")
SIDE = ("COMPOSITION: the subject sits on one side; the other 40% of the width is the same seamless wall, evenly lit and "
        "empty. One continuous photograph — no borders, bands, panels or split frames.")


def P(scene: str, air: str) -> str:
    return STYLE + scene + " " + air + " " + FIDELITY


RESEARCH = {
    "one_liner": "חנות אונליין למוצרי שיער מקצועיים (Paul Mitchell, pH, B-YOU, Elian, Biotop ועוד). ₪13–219 למוצר, "
                 "משלוח חינם מעל ₪199, קופסת הפתעות ב-₪199. מיצוב: המוצרים של הספרים, במחיר של אונליין.",
    "hero_products": ["גלייז סופר סקלפט של פול מיטשל 1 ליטר — ₪129", "גלייז לתלתלים Silk & Cotton — ₪49",
                      "מוס סקלפטינג של פול מיטשל — ₪119", "החלקה אורגנית pH ללא פורמלין — ₪219",
                      "מסכת קרטין B-YOU — ₪99", "אמפולת קרטין של אליאן — ₪13"],
    "audience": [
        {"persona": "בעלת התלתלים", "who": "נשים 18–40", "cares": "תלתלים מוגדרים, בלי פריז, שנשארים רכים ולא נוקשים"},
        {"persona": "השיער העייף", "who": "נשים 25–55", "cares": "שיקום אחרי צבע, החלקות ופן — רך, בריא, מבריק"},
        {"persona": "רוצה חלק בבית", "who": "נשים 25–45", "cares": "שיער חלק בלי לשבת שעות במספרה ובלי פורמלין"},
        {"persona": "הגבר המטופח", "who": "גברים 18–40", "cares": "ווקס ומוצרי עיצוב טובים, בלי להסתבך"},
    ],
    "pains": ["\"התלתלים יוצאים מפורקים ומלאי פריז\"", "\"הג'ל משאיר קראנץ' נוקשה\"", "\"השיער יבש ושבור מהחלקות\"",
              "\"החלקה במספרה עולה מלא ומריחה כימיקלים\""],
    "desires": ["תלתלים מוגדרים ורכים כל יום", "שיער רך ומבריק אחרי שיקום", "חלק בבית, בלי פורמלין",
                "המוצרים של הספרים, בלי לשלם כפול"],
    "objections": ["\"זה מקורי?\"", "\"איזה מוצר מתאים לתלתלים שלי?\"", "זמני משלוח", "\"החלקה בבית — זה בטוח?\""],
    "current_ads_audit": "15 מודעות פעילות, חלקן רצות יותר מחצי שנה — סימן שהקהל קונה. הביצוע מסודר (סאטן ורוד, "
                         "סרט BEST SELLER, מחיר גדול), אבל כל המודעות הן אותה תבנית: בקבוק על רקע, מחיר וכפתור. "
                         "אין אף מודעה שמראה תלתלים אמיתיים, אין 'לפני/אחרי' של תחושה, ואין סיבה לקנות דווקא אצלם.",
    "gaps": ["אין תוצאה על שיער אמיתי — רק בקבוקים", "קהל התלתלים הגדול מקבל מוצר ולא סיפור",
             "ההחלקה ללא פורמלין — יתרון ענק שקבור בשורה אחת", "קופסת ההפתעות והמבצע לגברים בעיצוב של פלאייר",
             "אין מודעה שעונה על 'זה מקורי?' ועל 'מה מתאים לי?'"],
    "angles": [
        {"id": "A1", "name": "תלתלים שמחזיקים", "idea": "הגלייז והמוס שכבר רצים אצלם הכי הרבה זמן, על תלתלים אמיתיים: הגדרה, ברק ורכות.", "persona": "בעלת התלתלים", "hook": "תלתלים מוגדרים. בלי קראנץ'.", "why": "המוצרים הכי חזקים שלהם, בשפה של התוצאה ולא של הבקבוק."},
        {"id": "A2", "name": "עזרה ראשונה לשיער", "idea": "מסכת קרטין, אמפולה ומסכת Neuro: שיקום לשיער יבש, צבוע ופגום.", "persona": "השיער העייף", "hook": "5 דקות. שיער אחר.", "why": "צורך רחב וחוזר, מוצרים במחיר כניסה נמוך (₪13–99)."},
        {"id": "A3", "name": "חלק. בלי פורמלין.", "idea": "ההחלקה האורגנית של pH, בבית, ברישיון משרד הבריאות.", "persona": "רוצה חלק בבית", "hook": "חלק ומבריק. בלי פורמלין.", "why": "יתרון שמוריד את החשש הכי גדול בקטגוריה ומצדיק ₪219."},
        {"id": "A4", "name": "גם לו מגיע", "idea": "מוצרי עיצוב לגברים, והווקס של Biotop במתנה מעל ₪199.", "persona": "הגבר המטופח", "hook": "הווקס עלינו.", "why": "קהל שני שכמעט לא מקבל תקציב, ומגדיל סל."},
        {"id": "A5", "name": "המותגים של הספרים", "idea": "החנות עצמה: מותגים מקצועיים מקוריים, משלוח חינם מעל ₪199 וקופסת הפתעות.", "persona": "כל הקהלים", "hook": "המוצרים של הספרים. עד הבית.", "why": "בונה זהות לחנות ולא רק למוצר, ומעלה את שווי ההזמנה."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now",
       people=False, note=None, verify=None):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=note, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=verify or [], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 תלתלים שמחזיקים ----------
ad(1, "A1", "4:5", ["pm_glaze"],
   P("The white Paul Mitchell Super Sculpt glaze bottle from the reference standing on a matte warm-clay plaster plinth, "
     "a thick glossy ribbon of clear gel curling around the base like a spiral curl, clay-coloured curved wall behind, "
     "soft sculpted light.", TOP),
   "תלתלים מוגדרים.<br>בלי קראנץ'.", "גלייז סופר סקלפט · 1 ליטר",
   "הגלייז של פול מיטשל נותן לתלתלים הגדרה, ברק ואחיזה, בלי להשאיר אותם קשים.\n\nבקבוק ענק של ליטר שמחזיק חודשים.\n\n129 ש״ח, משלוח חינם מעל 199.",
   "תלתלים מוגדרים, בלי קראנץ'. סופר סקלפט.",
   "גלייז לתלתלים · 1 ליטר", "129 ש״ח")
ad(2, "A1", "9:16", ["pm_glaze"],
   P("A woman with voluminous, defined, glossy dark spiral curls seen from behind at a three-quarter angle, soft clay "
     "plaster arch behind her, holding the white Paul Mitchell glaze bottle from the reference low at her side. Face "
     "turned away, not visible.", TOP),
   "התלתלים שלך.<br>רק מוגדרים יותר.", "גלייז מקצועי לתלתלים",
   "לא צריך לשנות את התלתלים. רק לתת להם את מה שהם צריכים.\n\nגלייז מקצועי שמגדיר כל תלתל, שומר על ברק ומונע פריז גם ביום לח.\n\nכל מוצרי התלתלים באתר.",
   "התלתלים שלך, רק מוגדרים יותר.",
   "תלתלים מוגדרים ורכים", "מוצרים לתלתלים", people=True)
ad(3, "A1", "1:1", ["g_glaze"],
   P("The silver G.Cosmetics Silk & Cotton glaze bottle from the reference on a matte blush-sand plaster plinth, beside it "
     "a single glossy dark curl of hair coiled on the plinth, blush-sand curved wall, soft light.", TOP),
   "הגלייז שכולן<br>קונות שוב.", "49 ש״ח · 500 מ״ל",
   "יש מוצרים שקונים פעם אחת, ויש כאלה שחוזרים אליהם.\n\nהגלייז לתלתלים של G.Cosmetics: גמישות, הגדרה ואחיזה טבעית, ב-49 ש״ח בלבד.",
   "הגלייז לתלתלים שכולן קונות שוב.",
   "גלייז לתלתלים", "49 ש״ח")
ad(4, "A1", "4:5", ["pm_foam"],
   P("The white Paul Mitchell sculpting foam can from the reference standing on a matte pale-rose plaster plinth, a soft "
     "cloud of dense white foam piled beside it, pale-rose curved wall, soft sculpted light.", TOP),
   "נפח ורכות.<br>באותו מוס.", "מוס סקלפטינג · 119 ש״ח",
   "רוצה תלתלים עם נפח, אבל רכים למגע?\n\nהמוס של פול מיטשל מעצב, מוסיף לחות ושומר על תלתלים קופצניים לאורך היום.\n\n119 ש״ח.",
   "נפח ורכות באותו מוס.",
   "מוס לתלתלים", "119 ש״ח")

# ---------- A2 עזרה ראשונה לשיער ----------
ad(5, "A2", "4:5", ["byou"],
   P("The pale-blue B-YOU keratin hair mask jar from the reference with its lid off beside it, a smooth glossy swirl of "
     "white mask cream visible on a small spatula resting on the jar, on a matte powder-blue plaster plinth, powder-blue "
     "curved wall, soft light.", TOP),
   "5 דקות.<br>שיער אחר.", "מסכת קרטין · 99 ש״ח",
   "שיער יבש, צבוע או אחרי החלקה? מתחילים מכאן.\n\nמסכת הקרטין של B-YOU חודרת לעומק השערה ומחזירה לחות, רכות וברק.\n\n500 מ״ל ב-99 ש״ח.",
   "5 דקות, שיער אחר. מסכת קרטין B-YOU.",
   "מסכת קרטין לשיער יבש", "99 ש״ח")
ad(6, "A2", "1:1", ["elian"],
   P("The Elian keratin ampoule from the reference standing upright on a matte ice-blue plaster block, clear water droplets "
     "on the glass, a few clear water beads on the block, ice-blue curved wall, crisp soft light.", TOP),
   "זריקת לחות.<br>ב-13 ש״ח.", "אמפולת קרטין של אליאן",
   "הטיפול הכי קטן באתר, והאהוב ביותר.\n\nאמפולת קרטין מרוכזת לשיקום מהיר של שיער עייף ופגום.\n\n13 ש״ח לאמפולה. שווה לקחת כמה.",
   "זריקת לחות לשיער, ב-13 ש״ח.",
   "אמפולת קרטין", "13 ש״ח")
ad(7, "A2", "9:16", ["byou", "elian"],
   P("Close crop of a woman's long, smooth, glossy chestnut hair falling over a bare shoulder, seen from behind, against a "
     "powder-blue plaster wall; the B-YOU mask jar and the Elian ampoule from the references stand on a small plaster "
     "ledge at the bottom of the frame. Face not visible.", TOP),
   "מיבש ושבור<br>לרך ומבריק.", "שגרת שיקום לשיער",
   "החלקות, צבע, פן ושמש. השיער עובר הרבה.\n\nשגרת שיקום פשוטה: מסכת קרטין פעם בשבוע ואמפולה כשצריך חיזוק.\n\nכל מוצרי השיקום באתר, משלוח חינם מעל 199.",
   "מיבש ושבור, לרך ומבריק.",
   "שגרת שיקום", "משלוח חינם מעל 199", people=True)
ad(8, "A2", "4:5", ["neuro"],
   P("The blue Paul Mitchell Neuro Repair tube from the reference lying diagonally on a matte slate-blue plaster plinth, "
     "a smooth squeeze of cream beside it, a soft warm glow of heat haze behind suggesting a hair dryer's warmth, "
     "slate-blue curved wall, soft light.", TOP),
   "לפני הפן.<br>לא אחרי.", "מסכת נוירו · הגנה מחום",
   "הפן, הפלאטה והמסלסל עושים את העבודה, ומשאירים שיער יבש.\n\nמסכת Neuro Repair של פול מיטשל נבנתה בדיוק בשביל זה: שיקום לשיער שחשוף לחום כל יום.",
   "לפני הפן, לא אחרי. Neuro Repair.",
   "מסכה לשיער חשוף לחום", "פול מיטשל")

# ---------- A3 חלק. בלי פורמלין. ----------
ad(9, "A3", "4:5", ["ph"],
   P("The three pH Protein+ bottles from the reference (blue, green, purple) standing in a row on a matte warm-white "
     "plaster plinth, a sheet of perfectly smooth glossy hair laid flat across the plinth in front of them, warm-white "
     "curved wall, soft clean light.", TOP),
   "חלק ומבריק.<br>בלי פורמלין.", "החלקה אורגנית · 219 ש״ח",
   "רוצה שיער חלק, אבל לא מוכנה לפורמלין?\n\nההחלקה האורגנית של pH עם מיקרו־פרוטאין, ברישיון משרד הבריאות, לכל סוגי השיער.\n\n219 ש״ח.",
   "חלק ומבריק, בלי פורמלין.",
   "החלקה ללא פורמלין", "219 ש״ח")
ad(10, "A3", "9:16", ["ph"],
   P("A woman with long, sleek, glass-smooth dark hair seen from behind, hair falling straight down her back, against a "
     "warm-white plaster arch; she holds the green pH Micro Protein bottle from the reference at her side. Face not "
     "visible.", TOP),
   "החלקה.<br>בבית שלך.", "ברישיון משרד הבריאות",
   "בלי לשבת שעות במספרה, ובלי ריח של כימיקלים.\n\nההחלקה של pH נעשית בבית, מתאימה לכל סוגי השיער ומשאירה שיער חלק, מבריק ורך.",
   "החלקה בבית שלך, בלי פורמלין.",
   "החלקה ביתית", "219 ש״ח", people=True)
ad(11, "A3", "1:1", ["ph"],
   P("The purple pH Blonde+ bottle from the reference on a matte soft-lilac plaster plinth, a lock of smooth glossy "
     "platinum-blonde hair draped over the plinth edge, soft-lilac curved wall, soft light.", TOP),
   "גם לבלונד.<br>גם לפגום.", "פי אייץ׳ בלונד פלוס",
   "שיער בהיר, צבוע או פגום צריך החלקה עדינה יותר.\n\nBlonde+ של pH נבנתה בדיוק לשיער כזה: חלק ומבריק, בלי להכביד.",
   "החלקה גם לבלונד, גם לפגום.",
   "החלקה לשיער בהיר", "219 ש״ח")
ad(12, "A3", "4:5", ["ph"],
   P("The three pH bottles from the reference arranged on three matte sand plaster blocks of "
     "different heights, like steps, a soft wave of sunlight crossing the sand curved wall, calm.", TOP),
   "שלושה סוגי שיער.<br>שלוש החלקות.", "רגיל · צבוע · בלונד",
   "לא כל שיער זהה, ולכן יש שלוש נוסחאות.\n\nשיער רגיל, שיער צבוע, ושיער בלונד או פגום: בוחרים את מה שמתאים לך ומקבלים חלק ובריא.",
   "שלושה סוגי שיער, שלוש החלקות.",
   "בוחרים לפי סוג שיער", "pH")

# ---------- A4 גם לו מגיע ----------
ad(13, "A4", "4:5", ["pomade"],
   P("The mint-green Biotop 101 pomade jar from the reference with its lid resting against it, on a matte charcoal "
     "plaster plinth, charcoal curved wall, a single warm raking light, masculine and minimal.", TOP),
   "הווקס<br>עלינו.", "מתנה בקנייה מעל 199 ש״ח",
   "גבר, הגיע הזמן להתפנק.\n\nקונה מוצרים ב-199 ש״ח ומעלה ומקבל את הווקס המקצועי של Biotop במתנה, עם הקוד MAN1.",
   "הווקס עלינו, בקנייה מעל 199.",
   "ווקס במתנה", "קוד MAN1")
ad(14, "A4", "1:1", ["pomade"],
   P("A man's hand with a little pomade on two fingertips, the open mint-green Biotop 101 jar from the reference below "
     "it on a matte charcoal plinth, charcoal wall, warm raking light. Only hand and jar in frame.", TOP),
   "תסרוקת שמחזיקה.<br>עד הערב.", "ווקס מקצועי לגברים",
   "אחיזה חזקה, מראה טבעי, ובלי ברק שמנוני.\n\nהווקס של Biotop, בדיוק מה שהספר שלך משתמש בו.",
   "תסרוקת שמחזיקה עד הערב.",
   "ווקס מקצועי", "Biotop", people=True)
ad(15, "A4", "9:16", ["pomade"],
   P("A man in a plain charcoal t-shirt seen from behind at a three-quarter angle, short neatly styled dark textured hair, "
     "against a charcoal plaster wall, the mint-green Biotop 101 jar from the reference on a plaster ledge at the bottom "
     "of the frame. Face turned away, not visible.", TOP),
   "גם לך<br>מגיע להתפנק.", "ווקס מתנה עם הקוד",
   "המוצרים לעיצוב שיער לגברים, במקום אחד.\n\nמעל 199 ש״ח הווקס של Biotop במתנה, והמשלוח חינם.",
   "גם לך מגיע להתפנק.",
   "מוצרי שיער לגברים", "משלוח חינם מעל 199", people=True)
ad(16, "A4", "4:5", ["pomade", "pm_glaze"],
   P("The mint-green Biotop 101 jar and the white Paul Mitchell glaze bottle from the references standing side by side on "
     "a matte stone-grey plaster plinth, a warm-grey curved wall, soft sculpted light, calm and balanced.", TOP),
   "הזמנה אחת.<br>לשניכם.", "מתנה לו · משלוח חינם",
   "היא מזמינה את הגלייז, הוא מקבל את הווקס.\n\nמעל 199 ש״ח המשלוח חינם, וקוד MAN1 מוסיף לו ווקס במתנה.",
   "הזמנה אחת לשניכם.",
   "הזמנה זוגית", "קוד MAN1")

# ---------- A5 המותגים של הספרים ----------
ad(17, "A5", "4:5", ["pm_glaze", "byou", "ph"],
   P("Editorial still life: the white Paul Mitchell glaze bottle, the B-YOU mask jar and the green pH bottle from the "
     "references on three matte sand plaster blocks of different heights, sand curved wall with a soft arch, soft "
     "sculpted light.", TOP),
   "המוצרים של הספרים.<br>עד הבית.", "מותגים מקצועיים ומקוריים",
   "פול מיטשל, pH, B-YOU, אליאן, Biotop ועוד.\n\nהמוצרים המקצועיים שהספרים עובדים איתם, מקוריים, במקום אחד.\n\nמשלוח חינם בכל רכישה מעל 199 ש״ח.",
   "המוצרים של הספרים, עד הבית.",
   "מותגים מקצועיים", "משלוח חינם מעל 199")
ad(18, "A5", "1:1", ["box"],
   P("The colourful Summer Mystery Box from the reference standing on a matte butter-yellow plaster plinth, its lid "
     "slightly lifted with soft light glowing from inside, butter-yellow curved wall, soft light, playful but premium.", TOP),
   "קופסה אחת.<br>שווה הרבה יותר.", "קופסת הפתעות · 199 ש״ח",
   "קופסת ההפתעות שלנו מלאה במוצרים שווים, ושווי המוצרים בה גבוה בהרבה מהמחיר.\n\n199 ש״ח, עד גמר המלאי.",
   "קופסה אחת, שווה הרבה יותר.",
   "קופסת הפתעות", "199 ש״ח")
ad(19, "A5", "9:16", ["box", "elian"],
   P("A woman's hands lifting the lid of the colourful Summer Mystery Box from the reference on a matte butter-yellow "
     "plinth, inside tissue paper and the tip of the Elian ampoule from the second reference peeking out, butter-yellow "
     "wall, soft light. Only hands and box in frame.", TOP),
   "מה יש<br>בקופסה?", "קופסת הפתעות · 199 ש״ח",
   "מוצרי שיער מקצועיים, בהפתעה, בשווי גבוה בהרבה מהמחיר.\n\nהדרך הכי כיפית להכיר מותגים חדשים.\n\n199 ש״ח, והמשלוח חינם.",
   "מה יש בקופסה? 199 ש״ח.",
   "קופסת הפתעות", "משלוח חינם", people=True)
ad(20, "A5", "4:5", ["pm_foam", "neuro", "byou"],
   P("A neat plain kraft shipping box with its flaps open on a matte clay plaster plinth, the white Paul Mitchell foam can, "
     "the blue Neuro tube and the B-YOU jar from the references standing in and beside it on white tissue, clay curved "
     "wall, soft light.", TOP),
   "מקורי.<br>ומגיע מהר.", "משלוח חינם מעל 199 ש״ח",
   "כל המוצרים באתר מקוריים, מהמותגים המקצועיים המובילים.\n\nמזמינים היום, והמשלוח מגיע עד הבית. מעל 199 ש״ח הוא עלינו.",
   "מקורי, ומגיע מהר.",
   "מוצרים מקוריים", "משלוח חינם מעל 199")

HERO_PROMPT = P("Hero campaign photograph for a professional hair-products store: a woman with big, glossy, defined dark "
                "spiral curls seen from behind at a three-quarter angle, curls catching soft light, against a warm clay "
                "plaster curved wall with a soft arch, holding the white Paul Mitchell glaze bottle from the reference low "
                "at her side. Face turned away, not visible.",
                "Tall vertical frame. The subject sits in the lower 55%; the upper 45% is the same clay plaster wall, "
                "evenly lit and empty. One continuous photograph — no borders, bands or panels.")

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "ref": REF}, sys.stdout, ensure_ascii=False, indent=1)
