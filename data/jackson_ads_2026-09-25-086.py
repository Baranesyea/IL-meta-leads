"""Jackson Jewelry / ג'קסון תכשיטים (lead 2026-09-25-086): research, 5 angles, 20 ads — image prompts + Hebrew copy.

A family jewellery business since 2005 with a factory store in Ramat Gan (HaYarkon 15) and a web store: 14K gold,
natural and lab-grown diamonds, engraved/name jewellery, men's Monaco bracelets, custom design. Free shipping and a
lifetime warranty. Their ads: a catalogue feed, a 5% club coupon flyer, a 12% holiday coupon flyer, one engraving
ad and a job posting — no brand story, no jewellery on skin in a premium way.
Visual direction (far from Stav's green, B-scents' hotel dusk, Asta-In's botanics, JewelryFactory's dark leather,
My Deal's colour-block and Hair Cosmetics' plaster studio): sun-drenched Mediterranean skin editorial — warm golden
hard sunlight with crisp leaf / window-shutter shadows, sun-kissed bare skin, white linen, warm limestone.
Ads speak to the customer in feminine singular except the men's angle (masculine / "for him").
Meta policy: no personal-attribute questions, no fake urgency.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-25-086"

# Higgsfield media ids of the store's product photos (jackson.co.il)
REF = {
    "nili": "c2124dcb-774a-45e5-984b-e5913dc4a31f",       # lab-diamond ring Nili: emerald-cut solitaire, yellow gold, ₪2,900
    "sania": "17413c9b-259f-45c7-bb38-75adb32b380a",      # lab-diamond ring Sania: four-stone flower, split shank, ₪3,200
    "monaco_white": "1d574636-ae25-4006-a962-bd91222ca0fd",  # Monaco figaro bracelet, full pavé, white gold, ₪3,980
    "monaco_onyx": "c73ab20d-e879-4e67-8fba-84dc68c30a67",   # Monaco tennis bracelet, black onyx, ₪3,415
    "cuban": "b26e1d87-79d6-4149-a79e-e7f96db4cf7a",      # Monaco classic polished cuban 6.5 mm, yellow gold, ₪3,697
    "cubes": "e13f2b7d-e7a7-4340-b35b-85bace5ab5b8",      # DANA letter-cube name necklace, ₪1,970
    "wings": "a09d0767-ab21-42fc-baad-9b73c4559180",      # letter + wings necklace, ₪2,650
    "rotem": "b32d4236-b13e-4681-adea-4938241bd2f3",      # ring Rotem: bezel diamonds in swirls, ₪2,280
    "mali": "34ce733d-e53b-478c-bf65-a58ff6dcdab5",       # ring Mali: graduated diamond curve, ₪1,890
    "nelly": "035e7404-855f-4808-803b-ed0e756bb62a",      # ring Nelly: twisted marquise band, ₪2,190
    "name_he": "03d232c6-f626-46d0-81f4-e92bfbd677a5",    # Hebrew name necklace "הודיה", ₪1,560
    "tahel": "dec8cbad-59c4-40bf-8ba0-61affe1588a0",      # engraved signet ring "Tahel" + diamond, ₪1,320
    "heart3": "80966068-fafa-4601-beac-592fba1238fc",     # heart pendant, 3 engraved names + diamonds, ₪2,691
    "tennis": "00664a71-7f76-44e7-b359-f313855ee908",     # lab-diamond tennis bracelet 2.01 ct, ₪4,420
}

STYLE = ("Premium fine-jewellery advertising photograph, sun-drenched Mediterranean editorial: warm golden late-afternoon "
         "hard sunlight, crisp soft-edged shadows of leaves or window shutters falling across the scene, sun-kissed "
         "natural skin, white linen and warm limestone, luminous and effortless, shot on medium format, photorealistic. ")
FIDELITY = ("The jewellery must be an exact match of the reference photos: same metal colour, links, setting, stone "
            "shapes, count and proportions, same engraved letters — do not redesign it. Real scale on the body. No text, "
            "signage, watermarks or logos anywhere in the image. ")

TOP = ("COMPOSITION: the subject sits in the lower 60% of the frame; above it the same background simply continues, "
       "evenly lit and empty — no objects, edges or lines. One continuous photograph — no borders, bands, panels or "
       "split frames.")
SIDE = ("COMPOSITION: the subject sits on one side; the other 40% of the width is the same background, evenly lit and "
        "empty. One continuous photograph — no borders, bands, panels or split frames.")


def P(scene: str, air: str) -> str:
    return STYLE + scene + " " + air + " " + FIDELITY


RESEARCH = {
    "one_liner": "עסק משפחתי לתכשיטים מאז 2005, עם חנות מפעל ברמת גן ואתר: זהב 14K, יהלומים טבעיים ויהלומי מעבדה, "
                 "תכשיטי חריטה וצמידי מונקו לגברים. ₪1,300–6,300, משלוח חינם ואחריות לכל החיים.",
    "hero_products": ["טבעות יהלומי מעבדה (נילי ₪2,900, סניה ₪3,200)", "צמיד טניס יהלומי מעבדה — ₪4,420",
                      "צמידי מונקו לגברים — ₪2,140–4,970", "שרשראות שם וחריטה — ₪1,320–2,691",
                      "טבעות יהלומים עדינות ליום־יום — ₪1,890–2,390"],
    "audience": [
        {"persona": "המתנה הגדולה", "who": "גברים ונשים 25–50", "cares": "מתנה לאירוסין, יום נישואין או לידה שתישאר לתמיד"},
        {"persona": "מפנקת את עצמה", "who": "נשים 25–45", "cares": "יהלום אמיתי ליום־יום, במחיר הגיוני"},
        {"persona": "הגבר עם הצמיד", "who": "גברים 20–45", "cares": "צמיד זהב נוכח ואיכותי, מקום שמבין בזה"},
        {"persona": "אמא/סבתא", "who": "נשים 30–65", "cares": "שמות הילדים והנכדים קרוב ללב"},
    ],
    "pains": ["\"בחנויות תכשיטים המחיר מנופח\"", "\"לא יודעת אם יהלום מעבדה זה 'אמיתי'\"",
              "\"קונים באינטרנט ולא יודעים מה מקבלים\"", "\"מתנה שתהיה אישית באמת\""],
    "desires": ["יהלום גדול ונוצץ במחיר סביר", "תכשיט שעונדים כל יום", "מתנה עם משמעות", "לקנות ממקום שסומכים עליו"],
    "objections": ["\"יהלום מעבדה זה כמו זירקון?\"", "\"מה אם צריך תיקון?\"", "זמני ייצור (עד 14 ימי עסקים)",
                   "\"לקנות תכשיט יקר באונליין?\""],
    "current_ads_audit": "7 מודעות פעילות: קטלוג אוטומטי (רץ 210 יום), פלאייר מועדון 5%, פלאייר קופון חג 12%, מודעת חריטה "
                         "אחת ומודעת דרושים. הקטלוג מוכיח שיש ביקוש, אבל אין אף תמונה של תכשיט על הגוף באור טוב, "
                         "אין סיפור של העסק המשפחתי והמפעל, ויהלומי המעבדה — היתרון הכי חזק במחיר — לא מוסברים.",
    "gaps": ["אין צילום פרימיום של תכשיט על עור", "הסיפור 'משפחה + מפעל מאז 2005' לא מסופר",
             "יהלומי מעבדה בלי הסבר ובלי ביטחון", "צמידי המונקו לגברים כמעט בלי במה", "אחריות לכל החיים לא מופיעה"],
    "angles": [
        {"id": "A1", "name": "יהלום אמיתי. מחיר אחר.", "idea": "יהלומי מעבדה: אותו יהלום בדיוק, כימית ואופטית, במחיר שמאפשר גדול יותר.", "persona": "מפנקת את עצמה", "hook": "יהלום אמיתי. מחיר אחר.", "why": "היתרון הכי חזק שלהם, ועונה על 'זה אמיתי?'."},
        {"id": "A2", "name": "מהמפעל שלנו", "idea": "עסק משפחתי מאז 2005, מפעל וחנות ברמת גן, אחריות לכל החיים.", "persona": "המתנה הגדולה", "hook": "ישר מהמפעל. מאז 2005.", "why": "אמון ומחיר בלי מתווכים — בדיוק מה שמרגיע קנייה יקרה באונליין."},
        {"id": "A3", "name": "השמות שלהם, קרוב ללב", "idea": "שרשראות שם, חריטה ותליוני שמות — מתנה עם משמעות.", "persona": "אמא/סבתא", "hook": "השמות שלהם. קרוב ללב.", "why": "רגש, מתנות ורכישה חוזרת לכל אירוע."},
        {"id": "A4", "name": "הצמיד שלו", "idea": "צמידי מונקו מזהב לגברים: קובני, פיגארו, שיבוץ ואוניקס.", "persona": "הגבר עם הצמיד", "hook": "צמיד שלא מורידים.", "why": "קטגוריה עם מחיר גבוה שכמעט לא מקבלת תקציב."},
        {"id": "A5", "name": "הטבעת של כל יום", "idea": "טבעות יהלומים עדינות מתחת ל-2,400 ש״ח: לענוד, לשלב, לא להוריד.", "persona": "מפנקת את עצמה", "hook": "יהלום קטן. כל יום.", "why": "מחיר כניסה נמוך יותר וקנייה אימפולסיבית לעצמה."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now",
       people=False, note=None, verify=None):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=note, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=verify or [], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 יהלום אמיתי. מחיר אחר. ----------
ad(1, "A1", "4:5", ["nili"],
   P("Close-up of a woman's sun-kissed hand resting on white linen, wearing the Nili emerald-cut solitaire ring from the "
     "reference on her ring finger, warm hard sunlight making the diamond flash, soft leaf shadows across the linen.", TOP),
   "יהלום אמיתי.<br>מחיר אחר.", "טבעת נילי · 2,900 ש״ח",
   "יהלום מעבדה הוא יהלום לכל דבר: אותו פחמן, אותה קשיות, אותו ניצוץ. ההבדל היחיד הוא איפה הוא נוצר.\n\nוזה מה שמאפשר טבעת כמו נילי, זהב 14K עם יהלום בחיתוך אמרלד, ב-2,900 ש״ח.",
   "יהלום אמיתי, מחיר אחר. טבעת נילי.",
   "טבעת יהלום מעבדה", "2,900 ש״ח", people=True)
ad(2, "A1", "1:1", ["sania"],
   P("The Sania four-stone flower ring from the reference standing on a small block of warm limestone, crisp golden "
     "sunlight throwing a long soft shadow and tiny rainbow sparkles on the stone, a few leaf shadows.", TOP),
   "ארבעה יהלומים.<br>פרח אחד.", "טבעת סניה · 3,200 ש״ח",
   "ארבעה יהלומי מעבדה בצורת פרח, על טבעת זהב 14K מפוצלת.\n\nטבעת שנראית כמו תכשיט של אירוע, ונענדת כל יום.\n\n3,200 ש״ח, משלוח חינם ואחריות לכל החיים.",
   "ארבעה יהלומים, פרח אחד. טבעת סניה.",
   "טבעת סניה", "3,200 ש״ח")
ad(3, "A1", "9:16", ["tennis"],
   P("A woman's sun-kissed wrist and hand resting on the edge of a white linen-covered table, wearing the yellow-gold "
     "lab-diamond tennis bracelet from the reference, hard golden sunlight making every stone sparkle, window-shutter "
     "shadows on the linen. Only the wrist and hand in frame.", TOP),
   "68 יהלומים.<br>על היד שלך.", "צמיד טניס · 2 קראט",
   "צמיד טניס של 2 קראט יהלומי מעבדה, 68 אבנים, בזהב 14K.\n\nתכשיט שפעם היה שמור לאירועים, והיום נענד עם ג'ינס.\n\n4,420 ש״ח.",
   "68 יהלומים, על היד שלך. צמיד טניס.",
   "צמיד טניס 2 קראט", "4,420 ש״ח", people=True)
ad(4, "A1", "4:5", ["nili", "sania"],
   P("The Nili and Sania rings from the references lying side by side on warm limestone in bright golden sunlight, "
     "crisp shadows, tiny rainbow refractions dancing on the stone around them.", TOP),
   "אותו יהלום.<br>רק נוצר אחרת.", "יהלומי מעבדה · זהב 14 קראט",
   "שואלים אותנו הרבה: יהלום מעבדה זה כמו זירקון? ממש לא.\n\nיהלום מעבדה הוא יהלום אמיתי, זהה כימית ואופטית ליהלום מהאדמה, בדיוק באותה קשיות. רק במחיר אחר.",
   "אותו יהלום, רק נוצר אחרת.",
   "מה זה יהלום מעבדה", "זהב 14K")

# ---------- A2 מהמפעל שלנו ----------
ad(5, "A2", "4:5", ["sania"],
   P("A jeweller's workbench by a sunny window: the Sania ring from the reference held upright in a small brass ring "
     "clamp, jeweller's tools softly out of focus, warm hard sunlight through the window, leaf shadows. No hands, no "
     "faces.", TOP),
   "ישר מהמפעל.<br>מאז 2005.", "עסק משפחתי · רמת גן",
   "מאז 2005 אנחנו עסק משפחתי שמייצר תכשיטים, עם מפעל וחנות ברמת גן.\n\nבלי מתווכים ובלי מחיר מנופח: מהשולחן של הצורף, ישר אלייך.",
   "ישר מהמפעל, מאז 2005.",
   "עסק משפחתי מאז 2005", "חנות מפעל ברמת גן")
ad(6, "A2", "1:1", ["tahel"],
   P("The engraved gold signet ring from the reference standing on a small linen-wrapped jewellery box on warm "
     "limestone, golden sunlight, soft leaf shadows, calm and warm.", TOP),
   "אחריות<br>לכל החיים.", "על כל תכשיט",
   "תכשיט טוב נשאר איתך שנים. ולכן כל תכשיט שיוצא מאיתנו מגיע עם אחריות לכל החיים.\n\nמשלוח חינם עד הבית, או איסוף מהחנות ברמת גן.",
   "אחריות לכל החיים, על כל תכשיט.",
   "אחריות לכל החיים", "משלוח חינם")
ad(7, "A2", "9:16", ["nili"],
   P("A small open cream jewellery box on white linen by a sunny window, the Nili ring from the reference nestled "
     "inside, hard golden sunlight and window-shutter shadows across the linen. No people.", TOP),
   "אתם בוחרים.<br>אנחנו מעצבים.", "עיצוב אישי בהזמנה",
   "יש לך תמונה של טבעת שחלמת עליה? רעיון לתכשיט שעוד לא קיים?\n\nבג'קסון מעצבים ומייצרים תכשיטים בהתאמה אישית, לפי הטעם, הסגנון והסיפור שלך.",
   "אתם בוחרים, אנחנו מעצבים.",
   "תכשיט בעיצוב אישי", "עסק משפחתי מאז 2005")
ad(8, "A2", "4:5", ["tennis", "cuban"],
   P("The yellow-gold tennis bracelet and the polished gold cuban bracelet from the references laid in gentle curves on "
     "warm limestone in hard golden sunlight, long crisp shadows, leaf shadows.", TOP),
   "זהב 14 קראט.<br>בלי מתווכים.", "משלוח חינם עד הבית",
   "כשהמפעל והחנות הם אותו מקום, המחיר נשאר הוגן.\n\nזהב 14K ויהלומים, עם משלוח חינם ואחריות לכל החיים.",
   "זהב 14K, בלי מתווכים.",
   "ישר מהמפעל", "משלוח חינם")

# ---------- A3 השמות שלהם, קרוב ללב ----------
ad(9, "A3", "4:5", ["heart3"],
   P("Close crop of a woman's sun-kissed collarbone and white linen shirt collar, wearing the gold heart pendant with "
     "three engraved names from the reference, warm hard sunlight and leaf shadows on the skin. Crop below the chin — "
     "no face.", TOP),
   "השמות שלהם.<br>קרוב ללב.", "תליון לב · 3 שמות",
   "שלושה שמות, לב אחד, והכי קרוב ללב.\n\nתליון זהב 14K עם חריטה של שמות הילדים ויהלומים קטנים.\n\n2,691 ש״ח, משלוח חינם.",
   "השמות שלהם, קרוב ללב.",
   "תליון לב עם שמות", "2,691 ש״ח", people=True)
ad(10, "A3", "1:1", ["name_he"],
   P("The gold Hebrew name necklace from the reference lying on white linen in warm golden sunlight, the chain curving "
     "softly, crisp leaf shadows. Keep the Hebrew letters exactly as in the reference.", TOP),
   "השם שלה.<br>בזהב.", "שרשרת שם · 1,560 ש״ח",
   "המתנה הכי אישית שיש: השם שלה, בכתב יד, בזהב 14K.\n\nשרשרת שם בעברית או באנגלית, בעבודת יד.\n\n1,560 ש״ח.",
   "השם שלה, בזהב.",
   "שרשרת שם", "1,560 ש״ח")
ad(11, "A3", "4:5", ["cubes"],
   P("Close crop of a woman's sun-kissed neck and shoulder in a white linen top, wearing the gold letter-cube name "
     "necklace from the reference, warm hard sunlight, leaf shadows across the skin. Crop below the lips — no face.", TOP),
   "כל קובייה.<br>אות שלך.", "שרשרת קוביות · 1,970 ש״ח",
   "קוביות זהב עם האותיות שבחרת: השם שלך, של הילדים, או מילה שרק שניכם מבינים.\n\n1,970 ש״ח, זהב 14K.",
   "כל קובייה, אות שלך.",
   "שרשרת קוביות עם שם", "1,970 ש״ח", people=True)
ad(12, "A3", "4:5", ["tahel"],
   P("A woman's sun-kissed hand resting on her white linen sleeve, wearing the engraved gold signet ring from the "
     "reference on her index finger, the engraved name visible, hard golden sunlight, leaf shadows.", TOP),
   "חריטה שנשארת<br>על היד.", "טבעת חריטה · 1,320 ש״ח",
   "טבעת חותם מזהב עם שם בחריטה ויהלום קטן.\n\nמתנה לאמא, לחברה הכי טובה, או לעצמך.\n\n1,320 ש״ח.",
   "חריטה שנשארת על היד.",
   "טבעת חריטה עם יהלום", "1,320 ש״ח", people=True)

# ---------- A4 הצמיד שלו ----------
ad(13, "A4", "4:5", ["cuban"],
   P("A man's tanned wrist and hand in the rolled-up sleeve of a white linen shirt, resting on a warm limestone ledge, "
     "wearing the polished yellow-gold cuban bracelet from the reference, hard golden sunlight, crisp shadows. Only the "
     "forearm and hand in frame.", TOP),
   "צמיד<br>שלא מורידים.", "מונקו קלאסי · 6.5 מ״מ",
   "צמיד מונקו קלאסי מזהב 14K, 6.5 מ״מ, מבריק ונוכח.\n\nצמיד שעונדים כל יום, לכל החיים, עם אחריות לכל החיים.\n\n3,697 ש״ח.",
   "צמיד שלא מורידים. מונקו קלאסי.",
   "צמיד מונקו לגבר", "3,697 ש״ח", people=True)
ad(14, "A4", "1:1", ["monaco_white"],
   P("The white-gold full pavé Monaco figaro bracelet from the reference coiled on dark warm stone in a single shaft of "
     "hard golden sunlight, every stone sparkling, deep soft shadows around.", TOP),
   "זהב לבן.<br>שיבוץ מלא.", "מונקו פיגארו · 3,980 ש״ח",
   "צמיד פיגארו מזהב לבן 14K בשיבוץ מלא: נוכח, נוצץ, ולא מתנצל.\n\n3,980 ש״ח, משלוח חינם.",
   "זהב לבן, שיבוץ מלא. מונקו פיגארו.",
   "מונקו פיגארו בשיבוץ", "3,980 ש״ח")
ad(15, "A4", "9:16", ["monaco_onyx"],
   P("A man's tanned wrist resting on the steering wheel of a classic car in golden late-afternoon sunlight, wearing the "
     "black onyx Monaco tennis bracelet from the reference, a white linen cuff, soft warm background. Only the forearm "
     "and hand in frame.", TOP),
   "שחור.<br>זהב. הוא.", "טניס אוניקס · 3,415 ש״ח",
   "צמיד טניס מזהב 14K בשיבוץ אוניקס שחור.\n\nהמתנה שהוא לא יקנה לעצמו, ולא יוריד.\n\n3,415 ש״ח.",
   "שחור, זהב, הוא. טניס אוניקס.",
   "צמיד אוניקס לגבר", "3,415 ש״ח", people=True)
ad(16, "A4", "4:5", ["cuban", "monaco_onyx"],
   P("The polished yellow-gold cuban bracelet and the black onyx tennis bracelet from the references side by side on a "
     "folded white linen shirt, hard golden sunlight, crisp leaf shadows.", TOP),
   "המתנה<br>שהוא לא יוריד.", "צמידי מונקו לגבר",
   "יום הולדת, יום נישואין, או סתם כי מגיע לו.\n\nצמידי מונקו מזהב 14K, מ-2,140 ש״ח, עם משלוח חינם ואחריות לכל החיים.",
   "המתנה שהוא לא יוריד.",
   "צמידי זהב לגבר", "מ-2,140 ש״ח")

# ---------- A5 הטבעת של כל יום ----------
ad(17, "A5", "4:5", ["rotem", "mali", "nelly"],
   P("A woman's sun-kissed hand resting on white linen, wearing the Rotem, Mali and Nelly diamond rings from the "
     "references stacked on two fingers, hard golden sunlight, leaf shadows across the hand.", TOP),
   "יהלום קטן.<br>כל יום.", "טבעות יהלומים מ-1,890 ש״ח",
   "לא כל טבעת צריכה אירוע.\n\nטבעות יהלומים עדינות בזהב 14K, לענוד לבד או לשלב, מ-1,890 ש״ח.",
   "יהלום קטן, כל יום.",
   "טבעות יהלומים עדינות", "מ-1,890 ש״ח", people=True)
ad(18, "A5", "1:1", ["mali"],
   P("The Mali graduated-diamond ring from the reference balanced on the rim of a small white ceramic cup on warm "
     "limestone, bright golden sunlight, crisp shadows, calm morning mood.", TOP),
   "הקפה של הבוקר.<br>והטבעת.", "טבעת מלי · 1,890 ש״ח",
   "הטבעת שנשארת גם כשמורידים את כל השאר.\n\nטבעת מלי: קשת של יהלומים קטנים בזהב 14K.\n\n1,890 ש״ח.",
   "הקפה של הבוקר, והטבעת. טבעת מלי.",
   "טבעת מלי", "1,890 ש״ח")
ad(19, "A5", "4:5", ["rotem"],
   P("A woman's sun-kissed hand lightly touching her white linen collar, wearing the Rotem swirl diamond ring from the "
     "reference, hard golden sunlight and window-shutter shadows. Crop at the collar — no face.", TOP),
   "מתנה.<br>לעצמך.", "טבעת רותם · 2,280 ש״ח",
   "מתי בפעם האחרונה קנית משהו רק בשבילך?\n\nטבעת רותם: יהלומים קטנים בשיבוץ עגול, בזהב 14K.\n\n2,280 ש״ח.",
   "מתנה לעצמך. טבעת רותם.",
   "טבעת רותם", "2,280 ש״ח", people=True)
ad(20, "A5", "4:5", ["nelly", "rotem"],
   P("The Nelly twisted marquise ring and the Rotem ring from the references lying on crumpled white linen in hard golden "
     "sunlight, crisp leaf shadows.", TOP),
   "שתיים<br>ביחד.", "משלבים טבעות · זהב 14 קראט",
   "אחת עדינה, אחת נוכחת, ושתיהן ביחד על אותה אצבע.\n\nטבעות יהלומים לשילוב, עם משלוח חינם ואחריות לכל החיים.",
   "שתיים ביחד. טבעות לשילוב.",
   "טבעות לשילוב", "משלוח חינם")

HERO_PROMPT = P("Hero campaign photograph for a family fine-jewellery house: close crop of a woman's sun-kissed hand "
                "resting on her white linen-covered shoulder, wearing the Nili emerald-cut solitaire ring from the first "
                "reference and the yellow-gold tennis bracelet from the second reference, hard golden sunlight, crisp "
                "leaf shadows across skin and linen. Crop below the chin — no face.",
                "The subject sits in the lower 65% of the frame; above it the same warm background continues, evenly "
                "lit and empty. One continuous photograph — no borders, bands or panels.")
HERO_M_PROMPT = P("Hero campaign photograph for a family fine-jewellery house: close crop of a woman's sun-kissed hand "
                  "resting on her white linen-covered shoulder, wearing the Nili emerald-cut solitaire ring from the "
                  "first reference and the yellow-gold tennis bracelet from the second reference, hard golden sunlight, "
                  "crisp leaf shadows across skin and linen. Crop below the chin — no face.",
                  "Tall vertical frame: the subject sits in the lower 55%; the upper 45% is the same warm background, "
                  "slightly deeper at the very top, evenly lit and completely empty. One continuous photograph — no "
                  "borders, bands or panels.")

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "hero_m": HERO_M_PROMPT, "ref": REF}, sys.stdout,
              ensure_ascii=False, indent=1)
