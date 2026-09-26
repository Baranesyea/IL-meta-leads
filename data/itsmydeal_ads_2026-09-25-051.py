"""It's My Deal / MY DEAL (lead 2026-09-25-051): research, 5 angles, 20 ads — image prompts + Hebrew copy.

An online store for professional hair-care brands (Olaplex, K18, Bolly Jon, Olie're Paris, Herbaliste, Mon Platin,
Indola, Jan Mor). The products are the real brands' products, so every prompt passes the store's photo of it.
Visual direction (far from Stav's green jewellery, B-scents' hotel dusk, Asta-In's botanics and JewelryFactory's
dark leather): bold fashion colour-block studio — one seamless saturated backdrop matched to each product's colour,
glossy hard light, hair in motion, magazine-beauty confidence.
Ads speak to the customer in feminine singular (their own ads do); the page addresses the business in plural.
Meta policy: no personal-attribute questions; results as "looks / feels", no medical claims.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-25-051"

# Higgsfield media ids of the store's product photos (itsmydeal.co.il)
REF = {
    "bolly": "bc8e6753-c25d-4d36-9cdf-49c82fe390d0",      # Bolly Jon Color Therapy set: pink shampoo, serum, mask
    "olaplex3": "13631493-499f-4821-bdff-0a80534759dc",   # Olaplex No.3 100 ml
    "janmor": "763f7a6e-2e12-49d3-b234-a72f7d07695d",     # Jan Mor La Lueur shampoo + mask set
    "k18": "a0b3d350-af03-4eca-bfa0-3e688c3ec214",        # K18 purple foam shampoo
    "oliere_beige": "7641228a-5835-4f5c-9284-adc42452ec47",
    "oliere_brown": "d4db0591-c259-4492-bafd-465848f79214",
    "seasoil_serum": "8c1db9e2-afcf-4735-8d7a-8ab66800735d",
    "seasoil_shampoo": "39c73847-438f-4414-9a94-f947effb707b",
    "seasoil_mask": "5a265759-796f-4000-922b-075e8431fd97",
    "hyloren": "d9b3eade-d4f4-41f9-9ba6-0a6120afc65e",    # Mon Platin Hyloren premium set with case
    "olaplex3plus": "e8c11f8b-ba61-463a-8190-443dd3f90a1c",
    "dryshampoo": "6ea8bd1b-9ea2-40de-a5ca-19b36ab57828",  # Olie're dry shampoo
    "indola_serum": "c97f8991-9f7f-4ac7-b1aa-db2a242c9f32",
}

STYLE = ("Premium fashion-beauty advertising photograph, bold colour-block studio: one seamless saturated backdrop, "
         "glossy directional light with crisp shadows, luminous healthy hair, confident magazine-campaign energy, "
         "shot on medium format, photorealistic. ")
FIDELITY = ("The products must be exact matches of the reference photos: same bottle shapes, colours, caps, labels and "
            "logo layout — do not redesign them and do not add or change any text on them. No other text, signage, "
            "watermarks or logos anywhere in the image. ")

TOP = ("COMPOSITION: the subject sits in the lower 60% of the frame; above it the same seamless backdrop simply "
       "continues, evenly lit and empty — no objects, edges or lines. One continuous photograph — no borders, bands, "
       "panels or split frames.")
SIDE = ("COMPOSITION: the subject sits on one side; the other 40% of the width is the same seamless backdrop, evenly lit "
        "and empty. One continuous photograph — no borders, bands, panels or split frames.")


def P(scene: str, air: str) -> str:
    return STYLE + scene + " " + air + " " + FIDELITY


RESEARCH = {
    "one_liner": "חנות אונליין למותגי טיפוח שיער מקצועיים (Olaplex, K18, Bolly Jon, Olie're Paris, Mon Platin ועוד). "
                 "₪59–599, 20% הנחה קבועה בקוד OFF20, משלוח חינם מעל ₪249. מיצוב: המוצרים של המספרה, במחיר נגיש.",
    "hero_products": ["Olaplex No.3 — ₪159 / No.3 Plus 370 מ״ל — ₪599", "סדרת Color Therapy של Bolly Jon — ₪459",
                      "K18 שמפו סגול — ₪239", "בשמי שיער של Olie're Paris — ₪139", "Herbaliste Sea & Soil — ₪119–169"],
    "audience": [
        {"persona": "בעלת השיער הצבוע", "who": "נשים 25–50", "cares": "לשמור על הצבע והברק בין טיפול לטיפול במספרה"},
        {"persona": "מכורת הטיפוח", "who": "נשים 20–40", "cares": "מותגים מקצועיים שהיא רואה ברשתות, במחיר טוב ובמשלוח מהיר"},
        {"persona": "השיער היבש והפגום", "who": "נשים 30–55", "cares": "שיקום אחרי החלקות, צבע ופן — רך, בריא, מבריק"},
    ],
    "pains": ["\"הצבע דוהה אחרי שבועיים\"", "\"השיער יבש ושבור מהחלקות\"", "\"במספרה זה עולה פי שניים\"",
              "\"אני לא יודעת מה מתאים לשיער שלי\""],
    "desires": ["שיער של אחרי מספרה, כל יום", "צבע שנשאר", "ריח טוב שנשאר בשיער", "לקנות מותג מקצועי בלי לשלם כפול"],
    "objections": ["\"זה מקורי?\"", "\"למה פה זול יותר?\"", "זמני משלוח", "\"מה מתאים לי?\""],
    "current_ads_audit": "9 מודעות פעילות: סרטוני UGC של בנות שמחזיקות מוצר מול המצלמה ותמונות מוצר על רקע לבן. "
                         "חלקן רצות כמעט 100 יום — סימן שהקהל קונה. אבל כל מודעה נשענת על הקוד OFF20, "
                         "ואין שום דבר שמבדל את החנות ממאה חנויות אחרות שמוכרות את אותם מותגים.",
    "gaps": ["אין ויזואל פרימיום אחד", "החנות עצמה לא מקבלת זהות — רק מבצע", "בשמי השיער והמותגים הפחות מוכרים "
             "כמעט לא מופיעים", "אין מודעה שעונה על 'זה מקורי?'", "אין קמפיין לפי סוג שיער"],
    "angles": [
        {"id": "A1", "name": "המספרה, אצלך במקלחת", "idea": "המותגים שהספרים עובדים איתם, לשימוש ביתי.", "persona": "מכורת הטיפוח", "hook": "הסוד של הספרים. אצלך במקלחת.", "why": "המסר שכבר עובד להם בסרטונים, בוויזואל ברמה של המותגים."},
        {"id": "A2", "name": "צבע שנשאר", "idea": "שמירה על שיער צבוע ובלונד בין טיפולים.", "persona": "בעלת השיער הצבוע", "hook": "הצבע מהמספרה. לשבועות.", "why": "כאב חוזר וקהל עם רכישות חוזרות."},
        {"id": "A3", "name": "בושם לשיער", "idea": "בשמי שיער ושמפו יבש של Olie're Paris: פינוק ויוקרה.", "persona": "מכורת הטיפוח", "hook": "הריח שנשאר בשיער.", "why": "מוצר רגשי ומתנתי, בלי תחרות מחירים."},
        {"id": "A4", "name": "שיקום לשיער יבש", "idea": "Sea & Soil, Olaplex ו-Jan Mor לשיער אחרי החלקות, צבע ופן.", "persona": "השיער היבש והפגום", "hook": "מיבש ושבור לרך ומבריק.", "why": "הצורך הכי רחב בקטגוריה."},
        {"id": "A5", "name": "המותגים הכי טובים. מחיר של חנות.", "idea": "החנות עצמה: מותגים מקצועיים מקוריים, 20% הנחה קבועה, משלוח חינם מעל 249.", "persona": "מכורת הטיפוח", "hook": "כל המותגים של המספרה. במקום אחד.", "why": "בונה זהות לחנות ומעלה את סל הקנייה."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now",
       people=False, note=None, verify=None):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=note, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=verify or [], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 המספרה, אצלך במקלחת ----------
ad(1, "A1", "4:5", ["olaplex3"],
   P("The Olaplex No.3 bottle from the reference standing on a glossy white acrylic block against a seamless pale "
     "sky-blue backdrop, a single long glossy strand of chestnut hair curving around the base, crisp studio light.", TOP),
   "הסוד של הספרים.<br>אצלך במקלחת.", "אולפלקס מספר 3 · 159 ש״ח",
   "יש סיבה שכל ספר שני עובד עם Olaplex.\n\nמספר 3 הוא הטיפול הביתי שמחזק את השיער מבפנים, בין טיפול לטיפול במספרה.\n\n159 ש״ח, ועם הקוד OFF20 עוד 20% הנחה.",
   "הסוד של הספרים, אצלך במקלחת. Olaplex No.3.",
   "הטיפול שהספרים ממליצים", "Olaplex No.3 · 159 ש״ח")
ad(2, "A1", "1:1", ["olaplex3plus"],
   P("The tall Olaplex No.3 Plus bottle from the reference on a glossy white plinth against a seamless soft-lavender "
     "backdrop, one hard light creating a crisp shadow, a few clear water droplets on the bottle.", TOP),
   "הגדול.<br>החדש.", "אולפלקס 3 פלוס · 370 מ״ל",
   "Olaplex No.3 Plus החדש, בגודל 370 מ״ל.\n\nהשדרוג של הטיפול הכי מפורסם בעולם השיער, לשיקום מלא יותר.\n\nהמחיר של החנות, והמשלוח חינם.",
   "Olaplex No.3 Plus החדש, 370 מ״ל.",
   "Olaplex No.3 Plus החדש", "משלוח חינם")
ad(3, "A1", "9:16", ["olaplex3"],
   P("Back view of a woman with long, glossy, freshly-blown-out chestnut hair flowing down her back, against a seamless "
     "warm-sand backdrop, the Olaplex No.3 bottle from the reference held low in her hand at her side, hair catching the "
     "light. No face visible.", TOP),
   "שיער של אחרי מספרה.<br>כל יום.", "טיפוח מקצועי לבית",
   "את מכירה את התחושה של יציאה מהמספרה? שיער רך, מבריק, מלא חיים.\n\nעם המוצרים שהספרים עצמם עובדים איתם, אפשר להרגיש ככה גם ביום רביעי רגיל.\n\nכל המותגים המקצועיים, במקום אחד.",
   "שיער של אחרי מספרה, כל יום.",
   "תחושה של אחרי מספרה", "מותגים מקצועיים", people=True)
ad(4, "A1", "4:5", ["k18"],
   P("The K18 purple shampoo bottle from the reference standing in a shallow pool of glossy lilac foam on a seamless "
     "vivid lilac backdrop, crisp studio light, playful and clean.", TOP),
   "בלונד בלי צהוב.", "שמפו סגול · 239 ש״ח",
   "הבלונד יצא מושלם מהמספרה, ואחרי שבוע הוא מתחיל להצהיב?\n\nהשמפו הסגול של K18 מנטרל גוונים צהובים ושומר על בלונד קריר ובהיר, במרקם קצף נעים.\n\n239 ש״ח, 20% הנחה עם OFF20.",
   "K18 שמפו סגול: בלונד בלי צהוב.",
   "בלונד בלי צהוב", "K18 · 239 ש״ח")

# ---------- A2 צבע שנשאר ----------
ad(5, "A2", "4:5", ["bolly"],
   P("The three Bolly Jon Color Therapy products from the reference (pink shampoo, serum and mask jar) arranged on stepped "
     "glossy coral blocks against a seamless coral-pink backdrop, bold crisp light and shadow.", TOP),
   "הצבע מהמספרה.<br>לשבועות.", "מארז 3 מוצרים לשיער צבוע",
   "השיער צבוע? ככה שומרים עליו זוהר ורך.\n\nסדרת Color Therapy של Bolly Jon: שמפו, סרום ומסכה שנבנו לשיער צבוע ויבש, ושומרים על הגוון.\n\nהמארז המלא ב-459 ש״ח.",
   "הצבע מהמספרה, לשבועות. Color Therapy.",
   "צבע שנשאר", "מארז Color Therapy")
ad(6, "A2", "1:1", ["bolly"],
   P("Close crop of glossy copper-red coloured hair in a smooth wave filling the lower half of the frame, the Bolly Jon "
     "pink serum bottle from the reference resting on the hair, seamless coral backdrop above, crisp light.", TOP),
   "הגוון נשאר.<br>הברק נשאר.", "לשיער צבוע",
   "כל חפיפה עם שמפו רגיל לוקחת איתה קצת מהצבע.\n\nמוצרים לשיער צבוע שומרים על הגוון ועל הברק, ומאריכים את הזמן עד הצבע הבא.\n\nכל הסדרות לשיער צבוע באתר.",
   "הגוון נשאר, הברק נשאר.",
   "מוצרים לשיער צבוע", "20% עם OFF20")
ad(7, "A2", "9:16", ["hyloren"],
   P("The Mon Platin Hyloren premium set from the reference: its pink-and-white travel case open, bottles and jar "
     "standing in front of it, on a glossy blush-pink floor against a seamless blush-pink backdrop, soft glossy light.", TOP),
   "מהדורה מוגבלת.<br>לשיער מוחלק.", "סט פרימיום · 479 ש״ח",
   "סט הפרימיום של Mon Platin לשיער מוחלק, במהדורה מוגבלת עם תיק נשיאה.\n\nכל מה שצריך כדי לשמור על החלקה רכה ומבריקה לאורך זמן.\n\n479 ש״ח.",
   "מהדורה מוגבלת לשיער מוחלק. Hyloren.",
   "סט Hyloren במהדורה מוגבלת", "479 ש״ח")
ad(8, "A2", "4:5", ["k18"],
   P("Back view of a woman with long icy-platinum blonde hair in a sleek low ponytail against a seamless lilac backdrop, "
     "holding the K18 purple shampoo bottle from the reference at shoulder height, crisp light. No face visible.", TOP),
   "הבלונד שלך.<br>כמו ביום הראשון.", "שמפו סגול לבלונד",
   "הבלונד הכי יפה ביום שיוצאים מהמספרה. אז למה לא לשמור עליו ככה?\n\nK18 Purple מנטרל צהוב ומחזק את השיער בכל חפיפה.\n\n239 ש״ח, משלוח חינם מעל 249.",
   "הבלונד שלך, כמו ביום הראשון.",
   "בלונד של יום ראשון", "K18 · 239 ש״ח", people=True)

# ---------- A3 בושם לשיער ----------
ad(9, "A3", "4:5", ["oliere_beige", "oliere_brown"],
   P("The two Olie're Paris hair perfume bottles from the references (cream and chocolate brown) standing side by side on "
     "a glossy travertine-beige block against a seamless warm camel backdrop, a soft cloud of fine mist in the air.", TOP),
   "הריח שנשאר<br>בשיער.", "בושם לשיער · 139 ש״ח",
   "בושם על העור נעלם עד הצהריים. בשיער הוא נשאר.\n\nבשמי השיער של Olie're Paris מעניקים ריח עדין וברק, בלי לייבש.\n\n139 ש״ח לבקבוק.",
   "הריח שנשאר בשיער. Olie're Paris.",
   "בושם שנשאר בשיער", "139 ש״ח")
ad(10, "A3", "1:1", ["oliere_brown"],
   P("A woman's hand spraying the chocolate-brown Olie're Paris hair perfume bottle from the reference toward long glossy "
     "dark hair, a fine mist catching the light, seamless chocolate-brown backdrop. Only hand and hair in frame.", TOP),
   "ריסוס אחד.<br>כל היום.", "שלושה ניחוחות לבחירה",
   "ריסוס אחד בבוקר, וכל מי שמתקרב שם לב.\n\nבושם לשיער בבקבוק מעוצב, שמתאים גם למתנה.\n\nשלושה ניחוחות לבחירה באתר.",
   "ריסוס אחד, כל היום. בושם לשיער.",
   "ריסוס אחד, כל היום", "שלושה ניחוחות", people=True)
ad(11, "A3", "9:16", ["dryshampoo"],
   P("The Olie're Paris dry shampoo can from the reference standing on a glossy mocha block against a seamless mocha "
     "backdrop, a fine white powder mist drifting softly beside it, crisp light.", TOP),
   "יום שני של שיער.<br>בלי שאף אחד יידע.", "שמפו יבש שקוף",
   "אין זמן לחפוף? לא צריך.\n\nהשמפו היבש השקוף של Olie're Paris סופג שומניות, מוסיף נפח ולא משאיר שאריות לבנות.\n\n79 ש״ח.",
   "יום שני של שיער, בלי שאף אחד יידע.",
   "שמפו יבש שקוף", "79 ש״ח")
ad(12, "A3", "4:5", ["oliere_beige"],
   P("The cream Olie're Paris hair perfume bottle from the reference in an open cream gift box with tissue paper, on a "
     "seamless soft-champagne backdrop, a satin ribbon beside it, soft glossy light.", TOP),
   "המתנה שהיא<br>לא קנתה לעצמה.", "בושם לשיער · 139 ש״ח",
   "מחפשת מתנה שלא נראית כמו עוד מתנה?\n\nבושם לשיער של Olie're Paris, בבקבוק שנראה טוב על כל שידה.\n\n139 ש״ח, משלוח מהיר.",
   "המתנה שהיא לא קנתה לעצמה.",
   "מתנה עם ריח", "139 ש״ח")

# ---------- A4 שיקום לשיער יבש ----------
ad(13, "A4", "4:5", ["seasoil_serum", "seasoil_shampoo", "seasoil_mask"],
   P("The three Herbaliste Sea & Soil products from the references (serum, shampoo bottle and mask tube) standing on "
     "glossy aqua blocks against a seamless ocean-teal backdrop, rippling water caustics of light across the backdrop.", TOP),
   "מים ואדמה.<br>לשיער יבש.", "סדרת סי אנד סויל",
   "סדרת Sea & Soil של Herbaliste משלבת מינרלים מהים ומהאדמה לשיקום אינטנסיבי של שיער יבש, פגום או צבוע.\n\nשמפו, מרכך, מסכה וסרום.\n\nמ-119 ש״ח.",
   "Sea & Soil: שיקום לשיער יבש ופגום.",
   "שיקום אינטנסיבי", "מ-119 ש״ח")
ad(14, "A4", "1:1", ["seasoil_mask"],
   P("A thick glossy swirl of rich mask cream on a teal glass slab, the Herbaliste Sea & Soil mask tube from the reference "
     "lying beside it, seamless deep-teal backdrop, crisp macro light.", TOP),
   "5 דקות מסכה.<br>שבוע של רכות.", "מסכה לשיער יבש",
   "פעם בשבוע, חמש דקות, והשיער מרגיש אחרת.\n\nמסכת Sea & Soil לשיקום אינטנסיבי של שיער יבש ופגום.\n\n169 ש״ח.",
   "5 דקות מסכה, שבוע של רכות.",
   "מסכה לשיער יבש", "169 ש״ח")
ad(15, "A4", "9:16", ["janmor"],
   P("The Jan Mor La Lueur shampoo and mask from the reference standing on a glossy sage block against a seamless "
     "sage-green backdrop, soft crisp light, calm and luxurious.", TOP),
   "שמפו ומסכה.<br>ברמה של סלון.", "ז׳אן מור · 500 מ״ל",
   "המארז שסוגר את הפינה: שמפו 500 מ״ל ומסכה 500 מ״ל מסדרת La Lueur של ז׳אן מור.\n\nלשיער רך, מבריק ומלא חיים, בגודל שמחזיק חודשים.\n\n369 ש״ח.",
   "שמפו ומסכה ברמה של סלון. Jan Mor.",
   "מארז La Lueur", "369 ש״ח")
ad(16, "A4", "4:5", ["indola_serum"],
   P("Close crop of a woman's long glossy dark-brown hair in a smooth sheet across the lower part of the frame, the Indola "
     "finishing serum bottle from the reference resting on it, seamless warm-grey backdrop above, crisp glossy light.", TOP),
   "בלי פריז.<br>רק ברק.", "סרום גימור · 119 ש״ח",
   "יום לח, שיער מתנפח. מכירה?\n\nסרום הגימור של Indola מרסן פריז ומעניק ברק בריא, בכמה טיפות.\n\n119 ש״ח.",
   "בלי פריז, רק ברק. סרום Indola.",
   "סרום נגד פריז", "119 ש״ח", people=True)

# ---------- A5 המותגים הכי טובים. מחיר של חנות. ----------
ad(17, "A5", "4:5", ["olaplex3", "k18", "oliere_beige"],
   P("Editorial still life of the Olaplex No.3, K18 purple shampoo and cream Olie're Paris bottles from the references "
     "on three glossy blocks of different heights against a seamless butter-yellow backdrop, bold crisp shadows.", TOP),
   "כל המותגים של המספרה.<br>במקום אחד.", "כל המותגים המקצועיים",
   "Olaplex, K18, Bolly Jon, Olie're Paris, Mon Platin ועוד.\n\nכל המותגים המקצועיים שהספרים עובדים איתם, מקוריים, במקום אחד.\n\nמשלוח חינם בקנייה מעל 249 ש״ח.",
   "כל המותגים של המספרה, במקום אחד.",
   "המותגים המקצועיים", "משלוח חינם מעל 249")
ad(18, "A5", "1:1", ["bolly", "olaplex3"],
   P("A glossy cobalt-blue shopping box with its lid off, the Olaplex No.3 bottle and the Bolly Jon pink shampoo from the "
     "references peeking out of white tissue paper, on a seamless cobalt-blue backdrop, crisp light.", TOP),
   "מקורי.<br>ומגיע עד הבית.", "1–5 ימי עסקים",
   "כל המוצרים באתר מקוריים, ישירות מהיבואנים.\n\nמזמינים היום, ותוך 1–5 ימי עסקים הם אצלך. מעל 249 ש״ח המשלוח עלינו.",
   "מקורי, ומגיע עד הבית.",
   "מוצרים מקוריים", "משלוח חינם מעל 249")
ad(19, "A5", "4:5", ["olaplex3plus", "hyloren"],
   P("A confident woman with voluminous glossy auburn blow-out hair standing against a seamless tangerine backdrop, "
     "turned three-quarters away, holding the Olaplex No.3 Plus bottle from the first reference; the Mon Platin Hyloren "
     "case from the second reference at her feet. Face in soft profile at the right edge.", SIDE),
   "20% הנחה.<br>על הכול. תמיד.", "קוד OFF20",
   "בלי לחכות למבצע ובלי לרדוף אחרי קופונים.\n\n20% הנחה על כל האתר עם הקוד OFF20, כל יום.\n\nמשלוח חינם מעל 249 ש״ח.",
   "20% הנחה על הכול, תמיד. OFF20.",
   "20% הנחה קבועה", "קוד OFF20", people=True)
ad(20, "A5", "9:16", ["seasoil_serum", "oliere_brown", "k18"],
   P("A tall editorial stack: the Herbaliste Sea & Soil serum, the brown Olie're Paris bottle and the K18 purple shampoo "
     "from the references balanced on staggered glossy blocks against a seamless fuchsia backdrop, bold crisp shadows.", TOP),
   "לכל סוג שיער.<br>המוצר שלו.", "יבש · צבוע · מתולתל · מוחלק",
   "שיער יבש, צבוע, מתולתל או מוחלק: לכל אחד יש את המוצרים שלו.\n\nבאתר הכול מסודר לפי סוג שיער, כדי שתמצאי בדיוק מה שמתאים לך.\n\n20% הנחה עם OFF20.",
   "לכל סוג שיער, המוצר שלו.",
   "מוצרים לפי סוג שיער", "20% עם OFF20")

HERO_PROMPT = P("Hero campaign photograph for a professional hair-care store: back three-quarter view of a woman with long, "
                "glossy, flowing chestnut hair caught in motion, against a seamless warm coral backdrop, holding the "
                "Olaplex No.3 bottle from the first reference at her side, crisp glossy light. Face turned away, not visible.",
                "Tall vertical frame. The subject sits in the lower 55%; the upper 45% is the same seamless coral "
                "backdrop, evenly lit and empty. One continuous photograph — no borders, bands or panels.")

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "ref": REF}, sys.stdout, ensure_ascii=False, indent=1)
