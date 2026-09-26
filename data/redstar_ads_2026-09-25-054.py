"""Red Star / רד סטאר (lead 2026-09-25-054): research, 5 angles, 20 ads — image prompts + Hebrew copy.

Online beauty store (Givatayim office, Shopify): ~1,750 products from the big professional and pharmacy brands —
L'Oréal Professionnel, Kérastase, Moroccanoil, Schwarzkopf, CeraVe, Nuxe, Bali Body, Mimas. 10% off the first
order, free shipping over ₪199.
Their ads: a catalog carousel ("all the brands here, 10% off"), brand videos (Moroccanoil heat spray), and a row of
single-product catalog cards (white-background packshot + product description). Four of those product ads link to
product pages that return 404 (the handles changed on the site), four more send people to the home page.
Visual direction (new in the set): glossy beauty editorial with the store's own colour — deep lacquer red and warm
cream, soft studio light, satin, water and texture; real women with real hair for the result shots.
Ad copy speaks to the customer in feminine singular (their own ads do). Meta policy: no before/after body claims,
no "is your hair damaged?" questions about the person — talk about the hair/product instead.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-25-054"

REF = {
    "biphase": "56d6d4ba-8532-4b1f-a2ef-a6fa4138267e",     # L'Oréal Pro Absolut Repair Molecular bi-phase oil 90 ml, ₪199.90
    "absmask": "3c3bdafc-021d-43e2-9862-dd1b32ecc9fe",     # L'Oréal Pro Absolut Repair mask 500 ml (gold jar), ₪246.90
    "curlmask": "c4b6c3b7-6eb7-4eba-888a-276dfb9f88c7",    # L'Oréal Pro Curl Expression mask 500 ml (purple jar), ₪246.90
    "curlcream": "bb0e1a3b-7614-40ad-9a3c-f416c2e70978",   # Curl Expression moisturising cream 200 ml (purple tube), ₪164.90
    "curlmist": "2d2181d2-b4c8-4410-b28f-9ce2d8b546d4",    # Curl Expression caring water mist 190 ml (purple spray), ₪164.90
    "glaze": "3b831463-57c2-400f-b3e2-0168d1d063f1",       # Kérastase Gloss Absolu hydra-glaze cream mask 75 ml (pink jar), ₪89.90
    "elixir": "5e4b8ad9-46c2-4d1d-a930-5d22e9667a1e",      # Kérastase Elixir Ultime oil bottle (duo set 75+30 ml, ₪309.90)
    "balimousse": "c258ffa3-fcc7-4a25-9257-dd651e813872",  # Bali Body 1-hour express self-tan mousse 225 ml, ₪139.90
    "balimist": "a39f116c-bdb9-4d0e-8649-ede6f787f690",    # Bali Body face tan mist dark 100 ml (white bottle), ₪109.90
    "cerave": "aeb1a65e-d89b-4e06-8c76-5e107f00c0b3",      # CeraVe facial moisturising lotion 52 ml, ₪89.90
    "moroccan": "d23a62bb-c1da-40af-a3ed-bf07ed82562b",    # Moroccanoil treatment oil 100 ml (amber bottle, turquoise label)
}

STYLE = ("Premium beauty advertising photograph, glossy editorial: soft sculpted studio light, deep lacquer red and "
         "warm cream palette, satin, water droplets and creamy product textures, shallow depth of field, shot on "
         "medium format, photorealistic, magazine quality. ")
FIDELITY = ("Products must be exact matches of the reference photos: same bottle, jar and tube shapes, same colours, "
            "same labels and logo layout — do not redesign them and do not add or change any text on them. No other "
            "text, signage, watermarks or logos anywhere in the image. People look natural, real skin texture, "
            "anatomically correct hands. ")
TOP = ("COMPOSITION: the subject sits in the lower 60% of the frame; above it the same soft background simply continues, "
       "calm and empty — no objects, edges or lines. One continuous photograph — no borders, bands, panels or split "
       "frames.")


def P(scene: str, air: str = TOP) -> str:
    return STYLE + scene + " " + air + " " + FIDELITY


RESEARCH = {
    "one_liner": "חנות ביוטי אונליין עם כ-1,750 מוצרים מהמותגים המקצועיים והפארם הגדולים: לוריאל פרופסיונל, קרסטס, "
                 "מרוקן אויל, שוורצקופף, סרווה, באלי בודי. ₪20–570, 10% הנחה בקנייה ראשונה, משלוח חינם מעל ₪199. "
                 "מיצוב: כל המותגים הגדולים במקום אחד, במחיר של אונליין.",
    "hero_products": ["אבסולוט ריפר של לוריאל פרופסיונל (מסכה ושמן דו-פאזי) — ₪199.90–246.90",
                      "קרל אקספרשן לתלתלים — ₪164.90–246.90", "מרוקן אויל", "באלי בודי לשיזוף עצמי — ₪109.90–139.90",
                      "קרסטס גלוס אבסולו ואליקסיר אולטים — ₪89.90–309.90"],
    "audience": [
        {"persona": "המטפחת המקצועית", "who": "נשים 25–45", "cares": "מוצרי מספרה אמיתיים בבית, בלי לשלם מחיר של מספרה"},
        {"persona": "המתולתלת", "who": "נשים 18–40", "cares": "תלתלים מוגדרים, בלי פריז ובלי קראנץ'"},
        {"persona": "הזוהרת של הקיץ", "who": "נשים 20–40", "cares": "גוון שזוף ואחיד בלי שמש"},
    ],
    "pains": ["\"השיער נשרף מהפן ומהמחליק\"", "\"התלתלים יוצאים פריזיים\"", "\"בסופר אין את המותגים המקצועיים\"",
              "\"באתרים אחרים אני לא בטוחה שזה מקורי\"", "\"שיזוף עצמי יוצא כתום ומנומר\""],
    "desires": ["שיער רך ומבריק כמו אחרי מספרה", "תלתלים מוגדרים", "עור זוהר", "כל המותגים שלי בהזמנה אחת"],
    "objections": ["\"זה מקורי?\"", "\"למה לא לקנות בפארם?\"", "משלוח", "\"מוצר מקצועי יקר\""],
    "current_ads_audit": "15 מודעות פעילות, רובן רצות חודשיים עד ארבעה חודשים, אז יש ביקוש. יש קרוסלת קטלוג עם 10% הנחה, "
                         "סרטוני מותג של מרוקן אויל ושורה של כרטיסי מוצר: מוצר על רקע לבן ותיאור מהאתר. הבעיה הגדולה היא "
                         "לא בוויזואל: ארבע ממודעות המוצר מובילות לעמודים שכבר לא קיימים (404), כי הכתובות של המוצרים "
                         "השתנו באתר, וארבע נוספות שולחות לדף הבית. בנוסף, אין שום דבר שמראה תוצאה על שיער אמיתי, ואין "
                         "זהות לחנות עצמה.",
    "gaps": ["מודעות שמובילות לעמודים שלא קיימים", "מודעות מוצר שנוחתות בדף הבית", "אין תוצאה על שיער ועור אמיתיים",
             "אין זהות לחנות: למה לקנות דווקא ברד סטאר", "הקהל המתולתל הגדול לא מקבל סדרה משלו"],
    "angles": [
        {"id": "A1", "name": "תלתלים של מספרה", "idea": "סדרת קרל אקספרשן: מסכה, קרם ותרסיס. תלתלים מוגדרים ורכים, עם המוצרים שהספרית משתמשת בהם.", "persona": "המתולתלת", "hook": "תלתלים של מספרה. בבית.", "why": "קהל גדול, כאב ברור, ושלושה מוצרים שנמכרים יחד."},
        {"id": "A2", "name": "שיקום אחרי החום", "idea": "אבסולוט ריפר וקרסטס גלוס: שיקום לשיער שעבר פן, מחליק וצבע.", "persona": "המטפחת המקצועית", "hook": "הפן לקח. זה מחזיר.", "why": "המוצרים הכי נמכרים שלהם, ובעיה שכל אחת מכירה."},
        {"id": "A3", "name": "זוהר בלי שמש", "idea": "באלי בודי: שיזוף עצמי תוך שעה, לגוף ולפנים. גוון אחיד וטבעי.", "persona": "הזוהרת של הקיץ", "hook": "שזופה תוך שעה. בלי שמש.", "why": "מוצר עונתי ויזואלי מאוד, עם קהל צעיר."},
        {"id": "A4", "name": "הטקס של הערב", "idea": "רגע הטיפוח: שמן אליקסיר, שמן מרוקן אויל ולחות של סרווה. המוצרים הגדולים, בשגרה שלך.", "persona": "המטפחת המקצועית", "hook": "חמש דקות רק בשבילך.", "why": "זווית רגשית שמעלה סל ומציגה מותגי יוקרה."},
        {"id": "A5", "name": "כל המותגים. במקום אחד.", "idea": "רד סטאר עצמה: 1,750 מוצרים מקוריים, 10% הנחה בקנייה ראשונה, משלוח חינם מעל 199.", "persona": "כולן", "hook": "כל המותגים שלך. בהזמנה אחת.", "why": "בונה זהות לחנות ועונה על ההתנגדות 'למה פה'."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now", people=False):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=None, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=[], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 תלתלים של מספרה ----------
ad(1, "A1", "4:5", ["curlmask"],
   P("A young woman with voluminous defined dark curly hair, seen from behind and slightly to the side, standing against "
     "a warm cream studio wall, soft sculpted light making each curl shine; the purple Curl Expression mask jar from the "
     "reference stands on a small cream plinth beside her shoulder."),
   "תלתלים של מספרה.<br>בבית.", "קרל אקספרשן · לוריאל פרופסיונל",
   "המסכה שהספריות משתמשות בה לתלתלים יבשים, עכשיו אצלך בבית.\n\nקרל אקספרשן של לוריאל פרופסיונל מזינה, מגדירה ומשאירה את התלתלים רכים.\n\n500 מ״ל ב-246.90 ש״ח. משלוח חינם מעל 199.",
   "תלתלים של מספרה. בבית.", "מסכת קרל אקספרשן", "246.90 ש״ח", people=True)
ad(2, "A1", "1:1", ["curlcream"],
   P("The purple Curl Expression cream tube from the reference lying diagonally on glossy cream satin, a generous swirl "
     "of the white cream beside it showing its rich texture, soft sculpted light, deep lacquer red satin folds at the "
     "bottom edge."),
   "בלי פריז.<br>בלי קראנץ'.", "קרם לחות לתלתלים · 164.90 ש״ח",
   "קרם הלחות של קרל אקספרשן מגדיר את התלתל בלי להשאיר אותו קשה.\n\nמורחים על שיער רטוב, מסדרים באצבעות, ונותנים לתלתלים לעשות את שלהם.\n\n200 מ״ל ב-164.90 ש״ח.",
   "בלי פריז. בלי קראנץ'.", "קרם לחות לתלתלים", "164.90 ש״ח")
ad(3, "A1", "4:5", ["curlmist"],
   P("The purple Curl Expression spray bottle from the reference standing on a wet glossy surface, a fine mist cloud "
     "caught in the light above its nozzle, water droplets around, warm cream background, soft sculpted light."),
   "תלתלים של יום שני.<br>מתעוררים.", "תרסיס ללא שטיפה · 164.90 ש״ח",
   "בוקר אחרי, והתלתלים כבר לא מה שהיו? כמה התזות של התרסיס, קצת מגע באצבעות, והם חוזרים לחיים.\n\nקרל אקספרשן, 190 מ״ל, ב-164.90 ש״ח.",
   "תלתלים של יום שני. מתעוררים.", "תרסיס לתלתלים", "164.90 ש״ח")
ad(4, "A1", "9:16", ["curlmask", "curlcream", "curlmist"],
   P("The three purple Curl Expression products from the references (mask jar, cream tube, spray bottle) arranged as a "
     "trio on stepped cream plinths, a deep lacquer red satin drape behind the lowest plinth, soft sculpted light."),
   "שלושה צעדים.<br>תלתל אחד מושלם.", "סדרת קרל אקספרשן",
   "מסכה פעם בשבוע, קרם אחרי כל חפיפה, ותרסיס לבוקר שאחרי.\n\nכל סדרת קרל אקספרשן של לוריאל פרופסיונל, מקורית, במקום אחד. משלוח חינם מעל 199 ש״ח.",
   "שלושה צעדים, תלתל אחד מושלם.", "סדרת קרל אקספרשן", "משלוח חינם מעל 199")

# ---------- A2 שיקום אחרי החום ----------
ad(5, "A2", "4:5", ["biphase"],
   P("The L'Oréal Absolut Repair Molecular bi-phase oil bottle from the reference standing on a glossy deep lacquer red "
     "surface, its two golden layers glowing in the light, a few golden oil droplets beside it, warm cream background."),
   "הפן לקח.<br>זה מחזיר.", "שמן דו-פאזי · 199.90 ש״ח",
   "פן, מחליק ומסלסל עושים את שלהם. השמן הדו-פאזי של אבסולוט ריפר מחזיר לשיער ברק ורכות, בלי להכביד.\n\nמנערים, מרססים על שיער רטוב או יבש, וזהו.\n\n90 מ״ל ב-199.90 ש״ח.",
   "הפן לקח. זה מחזיר.", "שמן אבסולוט ריפר", "199.90 ש״ח")
ad(6, "A2", "1:1", ["absmask"],
   P("The gold Absolut Repair mask jar from the reference, lid off, on warm cream satin, a thick glossy swirl of the "
     "golden mask on a small spatula beside it, soft sculpted light, deep red satin fold in the background corner."),
   "מסכה אחת.<br>שיער אחר.", "אבסולוט ריפר · 500 מ״ל",
   "המסכה הכי נמכרת של לוריאל פרופסיונל לשיער יבש ופגום, במידה המקצועית.\n\nחמש דקות על השיער, ומרגישים את ההבדל כבר בייבוש.\n\n500 מ״ל ב-246.90 ש״ח.",
   "מסכה אחת, שיער אחר.", "מסכת אבסולוט ריפר", "246.90 ש״ח")
ad(7, "A2", "4:5", ["glaze"],
   P("A woman with long sleek glossy brown hair, seen from behind, her hair falling straight down her back and catching "
     "a soft highlight, against a warm cream wall; the pink Kérastase Gloss Absolu jar from the reference on a small "
     "cream ledge at her side."),
   "ברק של מספרה.<br>כל יום.", "קרסטס גלוס אבסולו",
   "מסכת הקרם של קרסטס מעניקה לשיער עבה ופריזי ברק עמוק ורכות, בלי להכביד.\n\n75 מ״ל ב-89.90 ש״ח. הדרך הכי קלה להכיר את קרסטס.",
   "ברק של מספרה. כל יום.", "מסכת גלוס אבסולו", "89.90 ש״ח", people=True)
ad(8, "A2", "1:1", ["biphase", "absmask"],
   P("The bi-phase oil bottle and the gold Absolut Repair mask jar from the references side by side on a glossy deep "
     "lacquer red surface, warm golden rim light, a few golden droplets, calm cream background."),
   "הזוג שמציל<br>שיער צבוע.", "אבסולוט ריפר · מסכה ושמן",
   "מסכה פעם בשבוע ושמן אחרי כל חפיפה. זה כל מה ששיער צבוע ומוחלק צריך.\n\nשני המוצרים הכי נמכרים של אבסולוט ריפר, מקוריים, עם משלוח חינם.",
   "הזוג שמציל שיער צבוע.", "מסכה ושמן אבסולוט ריפר", "משלוח חינם מעל 199")

# ---------- A3 זוהר בלי שמש ----------
ad(9, "A3", "4:5", ["balimousse"],
   P("A woman seen from behind at waist height, wearing a white linen tank top, her tanned arm and shoulder showing an "
     "even natural golden tan, soft warm afternoon light; the tall Bali Body express mousse can from the reference "
     "stands in the foreground on a warm sand-coloured stone ledge. Her head is out of frame at the top-left corner."),
   "שזופה תוך שעה.<br>בלי שמש.", "באלי בודי · 139.90 ש״ח",
   "מוס השיזוף של באלי בודי נותן גוון שזוף ואחיד תוך שעה אחת.\n\nמורחים עם כפפה, מחכים שעה, שוטפים. בלי כתמים ובלי גוון כתום.\n\n225 מ״ל ב-139.90 ש״ח.",
   "שזופה תוך שעה. בלי שמש.", "מוס שיזוף עצמי", "139.90 ש״ח", people=True)
ad(10, "A3", "1:1", ["balimist"],
   P("The white Bali Body face tan mist bottle from the reference standing on a warm sand-coloured stone, a fine mist "
     "catching golden light, dried palm leaf shadows falling across the scene, warm cream background."),
   "זוהר של חופשה.<br>על הפנים.", "ספריי שיזוף לפנים · 109.90 ש״ח",
   "כמה התזות על הפנים בערב, ובבוקר מתעוררים עם זוהר של אחרי חופשה.\n\nספריי השיזוף לפנים של באלי בודי, גוון כהה, 100 מ״ל ב-109.90 ש״ח.",
   "זוהר של חופשה, על הפנים.", "ספריי שיזוף לפנים", "109.90 ש״ח")
ad(11, "A3", "4:5", ["balimousse", "balimist"],
   P("The Bali Body mousse can and the white face mist bottle from the references on a warm sand-coloured stone ledge "
     "beside a folded cream linen towel and a sprig of dried palm, warm late-afternoon light and palm shadows."),
   "הקיץ לא חייב<br>להיגמר.", "באלי בודי · לגוף ולפנים",
   "גוף ופנים באותו גוון, בלי שמש ובלי שעות על החוף.\n\nמוס לגוף וספריי לפנים של באלי בודי. משלוח חינם מעל 199 ש״ח.",
   "הקיץ לא חייב להיגמר.", "שיזוף עצמי לגוף ולפנים", "משלוח חינם מעל 199")
ad(12, "A3", "9:16", ["balimousse"],
   P("The tall Bali Body mousse can from the reference standing on warm sand-coloured stone, a soft cloud of golden "
     "mousse foam beside it, strong warm sunlight and palm leaf shadows, warm cream wall."),
   "גוון אחיד.<br>בלי כתמים.", "מוס אקספרס · שעה אחת",
   "הסוד לשיזוף עצמי שנראה טבעי: מוס קליל, כפפה, ושעה של סבלנות.\n\nבאלי בודי אקספרס, 139.90 ש״ח. 10% הנחה בקנייה ראשונה.",
   "גוון אחיד, בלי כתמים.", "מוס שיזוף אקספרס", "139.90 ש״ח")

# ---------- A4 הטקס של הערב ----------
ad(13, "A4", "4:5", ["elixir"],
   P("The golden Kérastase Elixir Ultime bottle from the reference standing in the right third of the frame on a "
     "glossy deep lacquer red surface, a single drop of golden oil falling from a glass dropper just above its neck, "
     "warm rim light. The whole left half of the frame is the same calm warm cream background, empty.",
     air="One continuous photograph — no borders, bands, panels or split frames."),
   "טיפה אחת<br>של זהב.", "קרסטס אליקסיר אולטים",
   "השמן האייקוני של קרסטס: טיפה אחת על הקצוות, והשיער מקבל ברק ורכות לכל היום.\n\nמארז 75 ו-30 מ״ל ב-309.90 ש״ח. אחד לבית ואחד לתיק.",
   "טיפה אחת של זהב.", "אליקסיר אולטים", "309.90 ש״ח")
ad(14, "A4", "1:1", ["moroccan"],
   P("The amber Moroccanoil treatment oil bottle from the reference on warm cream satin beside a small brass tray, "
     "golden evening light from the side, a few drops of oil glowing on the satin."),
   "הריח שכולן<br>שואלות עליו.", "מרוקן אויל",
   "השמן שהתחיל את הכול. ריח שאי אפשר לטעות בו, ושיער רך ומבריק.\n\nכל סדרת מרוקן אויל המקורית אצלנו, עם משלוח חינם מעל 199 ש״ח.",
   "הריח שכולן שואלות עליו.", "שמן מרוקן אויל", "משלוח חינם מעל 199")
ad(15, "A4", "4:5", ["cerave"],
   P("Side profile of a young woman with her hair tied back, her whole face visible, gently applying a small dab of "
     "white lotion to her cheek with her fingertips, eyes closed, soft natural skin texture, warm cream bathroom light; "
     "the CeraVe facial moisturising lotion tube from the reference standing on the cream marble counter beside her. "
     "The woman and the tube fill only the right half of the frame; the whole left half is plain warm cream wall, "
     "calm and empty.", air="One continuous photograph — no borders, bands, panels or split frames."),
   "לחות שעור<br>באמת מבין.", "סרווה · 89.90 ש״ח",
   "תחליב הלחות של סרווה עם סרמידים וחומצה היאלורונית, לעור רגיל עד יבש.\n\nבלי בושם, מתאים לכל יום. 52 מ״ל ב-89.90 ש״ח.",
   "לחות שעור באמת מבין.", "תחליב לחות סרווה", "89.90 ש״ח", people=True)
ad(16, "A4", "4:5", ["elixir", "moroccan", "cerave"],
   P("An evening vanity: the Kérastase Elixir Ultime bottle, the Moroccanoil oil bottle and the CeraVe tube from the "
     "references arranged on a cream marble tray, a lit candle glow, a folded cream towel, deep red satin fold, warm "
     "evening light."),
   "חמש דקות<br>רק בשבילך.", "הטקס של הערב",
   "סוף יום. שמן על הקצוות, לחות על הפנים, ורגע של שקט.\n\nכל המותגים שאת אוהבת, מקוריים, בהזמנה אחת. משלוח חינם מעל 199 ש״ח.",
   "חמש דקות רק בשבילך.", "הטקס של הערב", "משלוח חינם מעל 199")

# ---------- A5 כל המותגים. במקום אחד. ----------
ad(17, "A5", "4:5", ["absmask", "glaze", "curlmask", "balimousse"],
   P("A glossy deep lacquer red shopping bag, open, overflowing onto cream satin with the gold Absolut Repair jar, the "
     "pink Kérastase jar, the purple Curl Expression jar and the Bali Body can from the references, soft studio light."),
   "כל המותגים שלך.<br>בהזמנה אחת.", "10% הנחה בקנייה הראשונה",
   "לוריאל פרופסיונל, קרסטס, מרוקן אויל, סרווה, באלי בודי ועוד. כ-1,750 מוצרים מקוריים במקום אחד.\n\n10% הנחה בקנייה הראשונה, ומשלוח חינם מעל 199 ש״ח.",
   "כל המותגים שלך, בהזמנה אחת.", "רד סטאר", "10% הנחה בקנייה ראשונה")
ad(18, "A5", "1:1", ["biphase", "elixir", "moroccan", "curlmist", "balimist"],
   P("Five beauty products from the references (the bi-phase oil, the Kérastase Elixir bottle, the Moroccanoil bottle, "
     "the purple spray and the white Bali mist) standing in a neat row on a glossy deep lacquer red shelf, warm cream "
     "wall, soft sculpted light."),
   "המדף של<br>המספרה. אצלך.", "מוצרים מקוריים בלבד",
   "המוצרים שאת רואה במספרה ובפארם, מקוריים, במחיר של אונליין.\n\nמשלוח חינם מעל 199 ש״ח.",
   "המדף של המספרה, אצלך.", "מוצרים מקוריים", "משלוח חינם מעל 199")
ad(19, "A5", "4:5", ["glaze", "cerave"],
   P("A woman's hands opening a glossy deep lacquer red delivery box on a cream bed sheet, inside tissue paper with the "
     "pink Kérastase jar and the CeraVe tube from the references, soft morning window light. Only hands visible."),
   "הזמנת היום.<br>מטפחת מחר.", "משלוח חינם מעל 199 ש״ח",
   "מזמינים באתר, והמוצרים מגיעים עד הבית.\n\nמשלוח חינם מעל 199 ש״ח, ו-10% הנחה על ההזמנה הראשונה.",
   "הזמנת היום, מטפחת מחר.", "משלוח עד הבית", "משלוח חינם מעל 199", people=True)
ad(20, "A5", "9:16", ["absmask", "curlmask", "glaze"],
   P("Three beauty jars from the references (gold Absolut Repair, purple Curl Expression, pink Kérastase Gloss) stacked "
     "in a sculptural pyramid on a cream plinth, a deep lacquer red backdrop curving behind the lower half, soft studio "
     "light."),
   "10% הנחה.<br>על ההזמנה הראשונה.", "רד סטאר · הבית של הביוטי",
   "פעם ראשונה ברד סטאר? 10% הנחה על כל ההזמנה, ומשלוח חינם מעל 199 ש״ח.\n\nכל המותגים הגדולים, מקוריים, במקום אחד.",
   "10% הנחה על ההזמנה הראשונה.", "רד סטאר", "10% הנחה בקנייה ראשונה")

HERO_PROMPT = P("Hero campaign photograph for an online beauty store: the gold Absolut Repair jar, the pink Kérastase "
                "jar, the Elixir Ultime bottle and the purple Curl Expression jar from the references arranged as an "
                "elegant still life on stepped cream plinths, a flowing deep lacquer red satin drape, soft sculpted "
                "light. The products sit in the lower 55% of the frame on the left half; above and to the right the "
                "warm cream backdrop continues, calm and empty.", "One continuous photograph — no borders, bands or panels.")
HERO_M_PROMPT = P("Hero campaign photograph for an online beauty store: the gold Absolut Repair jar, the pink Kérastase "
                  "jar and the Elixir Ultime bottle from the references arranged as an elegant still life on stepped "
                  "cream plinths, a flowing deep lacquer red satin drape, soft sculpted light, no hands and no people. "
                  "The products sit in the "
                  "lower 50% of the frame, centred; the top half is the same warm cream backdrop, calm and empty.",
                  "One continuous photograph — no borders, bands or panels.")

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "hero_m": HERO_M_PROMPT, "ref": REF}, sys.stdout,
              ensure_ascii=False, indent=1)
