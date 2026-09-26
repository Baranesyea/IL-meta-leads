"""B-scents (lead 2026-09-25-066): research, 5 angles, 20 ads — image prompts + Hebrew copy.

Visual direction (deliberately far from Stav's jewellery campaign): architectural quiet luxury —
hotel-lobby calm, travertine, oak, linen, brass, long window light; products shot like design objects.
Copy addresses the business in the plural (no owner name on the site).
No third-party brand / hotel names in ads (their scent names reference them — IP + Meta policy risk).
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-25-066"

# Higgsfield media ids of the store's real product photos (imported from b-scents.co.il)
REF = {
    "b150w": "5a17741f-472b-4bca-8b10-194a4fa47081",   # B-150 white
    "b150b": "71cbf24d-9aff-4e23-8895-9e0084c69e66",   # B-150 black
    "b25": "c3db5fed-5291-49cc-a662-0a29d1678b66",     # B-25 white
    "b420": "503dd503-7297-4c27-ae1f-471cd8e73079",    # B-420 white horizontal
    "oil": "533d11a8-d590-4bec-901a-7eb44983e1de",     # 500 ml perfume oil, MUSK VANILLA label (the first
                                                       # reference carried a third-party brand name - not usable)
    "laundry": "3e9dcc60-3a98-413f-a906-8976488db796",  # 200 ml laundry perfume (pink)
    "car": "3e8d48b1-a9f2-4e13-8502-104a947b0210",     # TO-CAR black
    "cargold": "1818ca53-6aed-4ff0-b7b9-2f46f4c3987a",  # TO-CAR gold
    "leo": "3dcf9d25-9671-47a9-bc34-4c715cc0f8ff",     # LEO parfum
    "liya": "270604c1-c34b-44c7-9af1-41e29cd7ca15",    # LIYA parfum
}

STYLE = ("Premium editorial advertising photograph, quiet-luxury architectural interior style, "
         "soft natural light, refined muted palette, shot on medium format, shallow depth of field, "
         "photorealistic, magazine campaign quality. ")
FIDELITY = ("The product must be an exact match of the reference photo: same shape, proportions, color, "
            "materials, buttons and logo placement — do not redesign it, do not add or change any text or "
            "label on it. No other text, signage, watermarks or logos anywhere in the image. ")


def P(scene: str, air: str) -> str:
    return STYLE + scene + " " + air + " " + FIDELITY


TOP = "Leave the upper third of the frame calm and uncluttered (plain wall, ceiling or soft background) for typography."
SIDE = "Keep one side of the frame calm and uncluttered for typography."

RESEARCH = {
    "one_liner": "יבואן ומשווק מערכות ריח חכמות (מפיצי ריח חשמליים ללא מים), שמני בושם, בישום לכביסה ובשמים — לבית, לרכב ולעסקים. ₪44–799. מיצוב: יוקרה נגישה, 'ריח של מלון בבית'.",
    "hero_products": ["מפיץ ריח חשמלי B-150 — עד 150 מ״ר, שליטה מהנייד — ₪599",
                      "תמצית שמן בושם לכביסה 200 מ״ל — ₪44 (מארז 11 ניחוחות ₪395)",
                      "שמני בושם למפיץ 500 מ״ל בהשראת ריחות מלונות וחנויות — ₪179",
                      "B-420 לעסקים עד 420 מ״ר — ₪799; מפיץ לרכב TO-CAR — ₪299"],
    "audience": [
        {"persona": "הבית כמלון", "who": "נשים וגברים 30–55, בעלי בית/דירה מעוצבת", "cares": "חוויה של מלון בוטיק בבית, ריח קבוע בלי להתעסק, מוצר שנראה טוב על הקיר"},
        {"persona": "מנהלת הבית", "who": "נשים 25–50, משפחות", "cares": "כביסה שמריחה אחרי ייבוש ובארון, תמורה למחיר, מוצר שעובד באמת"},
        {"persona": "בעלי עסקים", "who": "חנויות, קליניקות, משרדים, לובים", "cares": "חוויית לקוח, ריח מותג שזוכרים, מכשיר שעובד לבד בלי תחזוקה"},
    ],
    "pains": ["\"מפיצי הריח שקניתי לא מורגשים בכלל\"", "\"הריח של המרכך נעלם אחרי הייבוש\"",
              "\"מפיצים עם מים משאירים לחות ואדים\"", "\"הלקוחות נכנסים לחנות ולא מרגישים כלום\"",
              "\"נרות ומקלות נגמרים מהר ולא ממלאים חלל גדול\""],
    "desires": ["להיכנס הביתה ולהרגיש בחופשה", "ריח שנשאר גם כשהמכשיר כבוי", "כביסה שמריחה כמו בושם ימים",
                "מקום שלקוחות זוכרים", "שליטה מהנייד — לכוון פעם אחת ולשכוח"],
    "objections": ["מחיר המכשיר (₪329–799)", "\"זה באמת מורגש?\"", "עלות מילוי שוטפת", "\"זה בטוח לנשימה/לילדים?\" (IFRA/SDS)"],
    "current_ads_audit": "כל 15 המודעות הפעילות הן סרטוני UGC בסגנון טיקטוק: אנשים מחזיקים את המוצר, צילומי מסך מוואטסאפ, טקסט על המסך. הן רצות 111–211 יום — סימן שהקהל מגיב לפנים אמיתיות. אבל 11 מתוך 15 הן על בישום לכביסה (₪44), והמוצר היקר והמבדל — מפיץ הריח החשמלי — מקבל 2 מודעות בלבד, בלי ויזואל אחד שמראה אותו כאובייקט עיצובי בבית יפה. אין שום פנייה לעסקים, אין רכב, אין את הבשמים LEO/LIYA.",
    "gaps": ["אין ויזואל פרימיום אחד בכל החשבון", "המכשיר (₪599) כמעט לא מפורסם", "אין קמפיין לעסקים (B-420, בישום בהתאמה אישית)",
             "ההבטחה 'ריח של מלון בבית' לא מקבלת תמונה", "רכב ובשמים אישיים לא קיימים במודעות"],
    "angles": [
        {"id": "A1", "name": "ריח של מלון, בבית", "idea": "המפיץ כאובייקט עיצובי בבית שנראה ומרגיש כמו לובי של מלון בוטיק.", "persona": "הבית כמלון", "hook": "חמישה כוכבים. בלי צ׳ק אאוט.", "why": "זו ההבטחה שהם כבר מוכרים (ריחות בהשראת מלונות) — עכשיו עם תמונה שמוכיחה אותה."},
        {"id": "A2", "name": "הכביסה שמריחה כמו בושם", "idea": "תמצית שמן בושם במקום מרכך: הריח נשאר אחרי הייבוש ובארון.", "persona": "מנהלת הבית", "hook": "ריח שנשאר גם בארון.", "why": "המוצר שכבר עובד להם במודעות — בשפה ויזואלית שמצדיקה מחיר ויוצרת מותג."},
        {"id": "A3", "name": "ריח שלקוחות זוכרים", "idea": "בישום מקצועי לעסקים: חנות, קליניקה, קבלה של מלון.", "persona": "בעלי עסקים", "hook": "לקוחות זוכרים איך המקום הריח.", "why": "קהל עם תקציב גבוה ורכישות חוזרות של מילוי, שהיום לא מקבל אף מודעה."},
        {"id": "A4", "name": "בלי מים. בלי אדים. רק ריח.", "idea": "הטכנולוגיה כיתרון: אידוי שמן בושם טהור, שליטה מהנייד, תזמון לפי ימים ושעות.", "persona": "הבית כמלון", "hook": "מפיץ ריח שאשכרה מפיץ.", "why": "עונה על ההתנגדות הכי גדולה ('זה בכלל מורגש?') וממצב מול מפיצי אדים זולים."},
        {"id": "A5", "name": "הריח שלכם, לאן שתלכו", "idea": "הרכב והבושם האישי: TO-CAR ו-LEO / LIYA.", "persona": "הבית כמלון", "hook": "הריח שלכם נוסע איתכם.", "why": "מרחיב את סל הקנייה ומוסיף מתנות — מוצרים שקיימים באתר ולא מקבלים חשיפה."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now",
       people=False, note=None, verify=None):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=note, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=verify or [], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 ריח של מלון, בבית ----------
ad(1, "A1", "4:5", ["b150w"],
   P("The white wall-mounted electric scent diffuser from the reference, mounted at eye level on a warm travertine wall "
     "in a serene luxury home entryway, a low oak console below with a ceramic vase of dried olive branches, soft late-afternoon "
     "window light raking across the stone.", TOP),
   "ריח של לובי מלון.<br>בכניסה שלכם.", "מפיץ ריח חשמלי · עד 150 מ״ר",
   "יש רגע כזה כשנכנסים ללובי של מלון טוב. הריח עוטף אתכם עוד לפני שמישהו אמר שלום.\n\nעכשיו הרגע הזה מחכה לכם בכניסה הביתה.\n\nמפיץ הריח החשמלי B-150 של בי סנטס מאדה תמצית שמן בושם טהורה, בלי מים ובלי אלכוהול, וממלא חללים עד 150 מ״ר.\n\nבוחרים ריח, מכוונים שעות מהנייד, ושוכחים ממנו.",
   "הריח של לובי מלון, בכניסה הביתה. מפיץ B-150 עד 150 מ״ר.",
   "ריח של מלון בוטיק בבית", "מפיץ ריח חשמלי עם שליטה מהנייד")
ad(2, "A1", "4:5", ["b150w"],   # generated 1:1, outpainted upward to 4:5 for room above her head
  
   P("A woman in her late thirties in a cream linen shirt stepping into her bright minimalist living room after a long day, eyes "
     "closed, a small relaxed smile, taking a slow breath; the white wall-mounted diffuser from the reference is visible on the "
     "wall behind her, in soft focus. Warm natural light, calm and cinematic.", SIDE),
   "נכנסים הביתה.<br>ומרגישים בחופשה.", "ריח שנשאר בחלל גם כשהמכשיר כבוי",
   "אתם מכירים את התחושה הזאת בחדר של מלון טוב? הכול שקט, נקי, והריח עושה חצי מהעבודה.\n\nאפשר להרגיש ככה גם בבית, כל יום.\n\nמפיצי הריח של בי סנטס עובדים על אידוי שמן בושם טהור, והריח נשאר בחלל גם אחרי שהמכשיר כבוי.\n\nמגוון ניחוחות בהשראת מלונות וחנויות יוקרה, באתר.",
   "להיכנס הביתה ולהרגיש בחופשה. מפיצי ריח עם שמן בושם טהור.",
   "הבית שלכם, בגרסת המלון", "ניחוחות בהשראת מלונות יוקרה", people=True)
ad(3, "A1", "9:16", ["b150b", "oil"],
   P("The black wall-mounted diffuser from the first reference on a dark walnut-panelled wall of a moody boutique-hotel style "
     "living room at dusk, a brass floor lamp casting a warm pool of light, the perfume-oil bottle from the second reference on a "
     "low marble side table beneath it. Deep shadows, rich warm tones.", TOP),
   "חמישה כוכבים.<br>בלי צ׳ק אאוט.", "שמן בושם 100% · בלי מים",
   "לא צריך להזמין חדר כדי להרגיש כמו במלון חמישה כוכבים.\n\nמספיק מכשיר אחד על הקיר ושמן בושם שנבחר בקפידה.\n\nה-B-150 בשחור של בי סנטס משתלב בכל עיצוב, ומפזר ריח עשיר ומורגש בחללים עד 150 מ״ר.\n\nבואו לבחור את הניחוח של הבית שלכם.",
   "חמישה כוכבים בבית, בלי צ׳ק אאוט. B-150 בשחור.",
   "מלון חמישה כוכבים. בסלון.", "B-150 בשחור, עד 150 מ״ר")
ad(4, "A1", "4:5", ["oil"],
   P("Close still life of the perfume-oil bottle from the reference standing on a honed travertine block, a soft beam of window "
     "light passing through the golden oil and casting an amber glow on the stone, a sprig of white jasmine lying beside it.", TOP),
   "ריח שנשאר<br>גם כשהמכשיר כבוי.", "100% תמצית שמן בושם · 500 מ״ל",
   "רוב מפיצי הריח מפזרים בעיקר אדים. אנחנו מפזרים בושם.\n\nשמני הבושם של בי סנטס הם 100% תמצית, בלי מים ובלי אלכוהול, ועומדים בתקני IFRA ו-SDS.\n\nלכן הריח לא נעלם כשהמכשיר נכבה. הוא נשאר בחלל.\n\nעשרות ניחוחות לבחירה, 500 מ״ל ב-179 ש״ח.",
   "100% תמצית שמן בושם. ריח שנשאר גם כשהמכשיר כבוי.",
   "ריח שנשאר בחלל", "500 מ״ל · 179 ש״ח")

# ---------- A2 הכביסה שמריחה כמו בושם ----------
ad(5, "A2", "4:5", ["laundry"],
   P("The laundry perfume bottle from the reference standing on top of a neat stack of crisp folded white cotton towels on an "
     "oak shelf in a sunlit linen closet, soft morning light, airy and fresh, pale neutral tones.", TOP),
   "הכביסה<br>שמריחה כמו בושם.", "תמצית שמן בושם לכביסה · 200 מ״ל",
   "נכון שתמיד חלמתם שהריח יישאר על הכביסה? גם אחרי המייבש, גם אחרי שבוע בארון.\n\nתמצית שמן הבושם לכביסה של בי סנטס נכנסת לתא המרכך במקום המרכך, ומבשמת ומרככת בבת אחת.\n\n100% תמצית בושם, בלי כתמים.\n\n200 מ״ל ב-44 ש״ח, במגוון ניחוחות.",
   "הכביסה שמריחה כמו בושם. 200 מ״ל ב-44 ש״ח.",
   "כביסה שמריחה כמו בושם", "במקום המרכך · 44 ש״ח")
ad(6, "A2", "1:1", ["laundry"],
   P("A smiling woman in her early thirties in a soft grey knit, pressing a freshly folded white towel to her face and breathing "
     "in, in a bright Scandinavian laundry room with white cabinets; the laundry perfume bottle from the reference stands on the "
     "counter beside her. Natural daylight, joyful and clean.", SIDE),
   "ריח שנשאר<br>גם בארון.", "גם אחרי המייבש",
   "הכביסה יוצאת מהמכונה ומריחה נהדר. יום אחרי, כבר לא.\n\nעם תמצית שמן הבושם לכביסה של בי סנטס זה נגמר: הריח נאחז בבד ונשאר גם אחרי הייבוש וגם בארון.\n\nשופכים 10 עד 20 מ״ל לתא המרכך, וזהו.\n\nמגוון ניחוחות באתר.",
   "ריח שנשאר על הכביסה גם אחרי הייבוש וגם בארון.",
   "הריח לא נעלם אחרי הייבוש", "תמצית שמן בושם לכביסה", people=True)
ad(7, "A2", "9:16", ["laundry"],
   P("Overhead flat lay on white linen: eleven bottles of the exact same design as the reference arranged in a gentle arc, each "
     "with a different soft liquid and label colour (green, pink, orange, black, gold, lilac, white, sky blue and more), a few "
     "sprigs of lavender and cotton flowers between them, soft even daylight.", TOP),
   "11 ניחוחות.<br>לכל מצב רוח.", "מארז כל הריחות · 11 × 200 מ״ל",
   "לא יודעים איזה ריח לבחור? לא צריך.\n\nבמארז כל הריחות של בי סנטס מקבלים את כל 11 הניחוחות לכביסה: מפרחוני ועד רענן, מבושם יוקרתי ועד ריח של כביסה של פעם.\n\n11 בקבוקים של 200 מ״ל ב-395 ש״ח.\n\nכל כביסה, ריח אחר.",
   "כל 11 הניחוחות לכביסה במארז אחד, 395 ש״ח.",
   "מארז כל הריחות לכביסה", "11 בקבוקים · 395 ש״ח")
ad(8, "A2", "4:5", ["laundry"],
   P("Macro detail: a hand pouring a thin golden stream of perfume from the laundry perfume bottle from the reference into a "
     "small clear measuring cup resting on a white washing machine's open detergent drawer, soft daylight, clean white tones.", TOP),
   "10 מ״ל במקום המרכך.<br>זה כל הסוד.", "מגיע עם כוס מדידה",
   "מרכך כביסה רגיל מכיל 5% עד 10% תמצית בושם. השאר זה מים וחומרים.\n\nאצלנו זה 100% תמצית שמן בושם.\n\nלכן מספיקים 10 עד 20 מ״ל בתא המרכך כדי שכל הכביסה תריח ימים.\n\nנסו בקבוק אחד ב-44 ש״ח ותרגישו את ההבדל.",
   "100% תמצית בושם במקום מרכך. 10 מ״ל לכביסה.",
   "10 מ״ל. כל הכביסה מריחה.", "100% תמצית שמן בושם")

# ---------- A3 ריח שלקוחות זוכרים ----------
ad(9, "A3", "4:5", ["b420"],
   P("Minimal high-end fashion boutique interior with pale plaster walls, a few neutral garments on a brushed brass rail, a "
     "travertine plinth, and the white horizontal scent machine from the reference mounted discreetly on the wall; warm gallery "
     "spotlights, calm and expensive.", TOP),
   "לקוחות זוכרים<br>איך המקום הריח.", "לעסקים · עד 420 מ״ר",
   "לקוחות לא תמיד זוכרים מה קנו. הם זוכרים איך הרגישו.\n\nוחוש הריח הוא הקיצור הכי מהיר לזיכרון.\n\nה-B-420 של בי סנטס ממלא חללים עד 420 מ״ר, נשלט מהנייד ב-Wi-Fi, ואפשר גם לפזר דרכו ריח דרך המיזוג.\n\nרוצים ריח מותג משלכם? דברו איתנו.",
   "הריח שהלקוחות שלכם יזכרו. B-420 עד 420 מ״ר.",
   "ריח מותג לעסק שלכם", "B-420 · שליטה ב-Wi-Fi", cta="Learn More")
ad(10, "A3", "1:1", ["b150b"],
   P("Boutique hotel reception: a curved travertine desk, a large arrangement of white flowers, soft linen-shaded lamps, and the "
     "black wall-mounted diffuser from the reference on the wall behind the desk. No people. Warm, welcoming, quiet luxury.", TOP),
   "הריח הוא<br>קבלת הפנים.", "בישום מקצועי לעסקים",
   "לפני שמישהו אמר שלום, הלקוח כבר קיבל רושם ראשון.\n\nבי סנטס מספקת מערכות ריח ושמני בושם לבתי מלון, לחנויות, לקליניקות ולמשרדים, בהתאמה לחלל ולאופי המקום.\n\nמכשירים חסכוניים, שליטה מהנייד, וריח שנשאר.\n\nלהזמנות בסיטונאות ולריח בהתאמה אישית, השאירו פרטים.",
   "הריח הוא קבלת הפנים של העסק שלכם.",
   "בישום מקצועי לעסקים", "בתי מלון · חנויות · קליניקות", cta="Learn More")
ad(11, "A3", "9:16", ["b420"],
   P("Serene upscale spa or aesthetic clinic waiting lounge: curved bouclé armchairs, a low stone table with a glass of water, "
     "sheer curtains filtering soft light, and the white horizontal scent machine from the reference mounted on the wall.", TOP),
   "עד 420 מ״ר<br>של ריח אחד מדויק.", "שליטה מלאה מהנייד",
   "חלל גדול צריך מכשיר רציני.\n\nה-B-420 של בי סנטס מפזר ריח אחיד בחללים עד 420 מ״ר, עם מאוורר פנימי וחיצוני ושליטה מהנייד ב-Wi-Fi או ב-Bluetooth.\n\nמכוונים עוצמה, ימים ושעות, והמכשיר עובד לבד.\n\nלקליניקות, ללובים, לחנויות ולמשרדים.",
   "B-420: ריח אחיד בחללים עד 420 מ״ר, שליטה מהנייד.",
   "ריח אחיד לחללים גדולים", "B-420 · 799 ש״ח", cta="Learn More")
ad(12, "A3", "4:5", ["b150w"],
   P("A stylish woman in her early forties, owner of an elegant concept store, standing behind her oak counter checking her phone "
     "with a calm confident expression; the white wall-mounted diffuser from the reference is on the plaster wall behind her. "
     "Warm afternoon light, shallow depth of field.", SIDE),
   "מכוונים פעם אחת.<br>הריח עובד לבד.", "תזמון ימים ושעות מהנייד",
   "יש לכם מספיק דברים לנהל בעסק. הריח לא צריך להיות אחד מהם.\n\nבמפיצי הריח של בי סנטס מכוונים מראש עוצמה ושעות פעילות, אפשר להגדיר כל יום אחרת, והכול מהנייד.\n\nואם תרצו, אנחנו נכוון בשבילכם עוד לפני שהמכשיר יוצא אליכם.\n\nבואו לדבר על הריח של העסק.",
   "מכוונים פעם אחת, והריח עובד לבד. שליטה מהנייד.",
   "הריח שמנהל את עצמו", "תזמון מלא מהנייד", people=True, cta="Learn More")

# ---------- A4 בלי מים. בלי אדים. רק ריח. ----------
ad(13, "A4", "4:5", ["b25"],
   P("The compact white scent diffuser from the reference standing on a light oak sideboard beside a hand-thrown ceramic vase and "
     "a linen napkin, Scandinavian minimal living room, clean morning light, pale warm neutrals.", TOP),
   "בלי מים.<br>בלי אדים. רק ריח.", "טכנולוגיית אידוי שמן בושם",
   "מפיץ אדים מפזר בעיקר מים. אתם מקבלים לחות, ומעט מאוד ריח.\n\nמפיצי הריח של בי סנטס עובדים על אידוי תמצית שמן בושם טהורה, בלי מים, בלי גז ובלי אלכוהול.\n\nהתוצאה: ריח מורגש באמת, בלי אדים ובלי כתמים.\n\nה-B-25 הקומפקטי, לחללים עד 25 מ״ר, ב-329 ש״ח.",
   "בלי מים, בלי אדים. אידוי שמן בושם טהור.",
   "ריח אמיתי, בלי אדים", "329 ש״ח · עד 25 מ״ר")
ad(14, "A4", "1:1", ["b25"],
   P("The compact white scent diffuser from the reference (the device only - no bottle anywhere in the scene) on a walnut "
     "bedside table next to a linen-shaded lamp glowing warm, crisp white bedding softly out of focus, calm evening mood.", TOP),
   "ריח לפי לוח זמנים.<br>שלכם.", "שליטה מהנייד",
   "רוצים שהבית יריח טוב כשאתם חוזרים, ושקט בלילה?\n\nעם מפיצי הריח של בי סנטס מתזמנים ימים, שעות ועוצמה ישר מהנייד, וכל יום יכול להיראות אחרת.\n\nה-B-25 עובד על חשמל או על סוללות, ונתלה בלי קידוח.\n\nכל הדגמים באתר.",
   "מתזמנים את הריח של הבית מהנייד.",
   "הריח בזמן שלכם", "B-25 · חשמל או סוללות")
ad(15, "A4", "9:16", ["b150w"],
   P("Sculptural studio product shot: the white diffuser from the reference standing on a pale stone plinth against a warm beige "
     "seamless backdrop, a single soft key light with a long gentle shadow, like a luxury design-object campaign.", TOP),
   "מפיץ ריח<br>שאשכרה מפיץ.", "עד 150 מ״ר · 599 ש״ח",
   "קניתם פעם מפיץ ריח ואחרי יומיים כבר לא הרגשתם כלום?\n\nה-B-150 של בי סנטס בנוי אחרת: מאוורר פנימי, משאבה מחוזקת ואידוי שמן בושם טהור, לחללים עד 150 מ״ר.\n\nהוא חסכוני בשמן ובחשמל, ומגיע עם 100 מ״ל שמן בושם.\n\n599 ש״ח, באתר.",
   "מפיץ ריח שאשכרה מפיץ. B-150 עם 100 מ״ל שמן.",
   "המפיץ שאשכרה מפיץ", "B-150 · 599 ש״ח")
ad(16, "A4", "4:5", ["b150b", "oil"],
   P("Dramatic perfume-campaign still life: the black diffuser from the first reference and the perfume-oil bottle from the second "
     "reference on polished black marble, low-key lighting with a crisp rim light outlining their edges, a faint wisp of fine mist "
     "drifting upward, deep black background.", TOP),
   "טכנולוגיית אידוי<br>של שמן בושם טהור.", "עומד בתקני בטיחות בינלאומיים",
   "הסוד הוא לא רק בריח. הוא באיך שהוא מתפזר.\n\nהמכשירים של בי סנטס מאדים תמצית שמן בושם לחלקיקים זעירים שממלאים את החלל, בלי מים ובלי אלכוהול.\n\nהשמנים שלנו עומדים בתקנים המחמירים של IFRA ו-SDS.\n\nריח עשיר, מורגש, ובטוח.",
   "אידוי שמן בושם טהור. ריח עשיר ובטוח.",
   "איך נשמע ריח יוקרתי", "תקני IFRA ו-SDS")

# ---------- A5 הריח שלכם, לאן שתלכו ----------
ad(17, "A5", "4:5", ["car"],
   P("The black car scent diffuser from the reference sitting in the cup holder of a luxury car's leather centre console at night, "
     "its soft LED glow, city lights blurred into warm bokeh through the windshield, cinematic moody tones.", TOP),
   "הריח שלכם<br>נוסע איתכם.", "מפיץ ריח נטען לרכב",
   "הרכב הוא החדר שאתם מבלים בו הכי הרבה זמן בלי לשים לב.\n\nה-TO-CAR של בי סנטס נכנס למחזיק הכוסות, נטען ב-USB, ומפזר שמן בושם אמיתי בשלוש עוצמות.\n\nמגיע עם שני בקבוקוני שמן בושם של 15 מ״ל.\n\n299 ש״ח, באתר.",
   "מפיץ ריח נטען לרכב עם שמן בושם אמיתי. 299 ש״ח.",
   "ריח של מלון, בנסיעה", "TO-CAR · 299 ש״ח")
ad(18, "A5", "1:1", ["leo"],
   P("A well-dressed man in a dark tailored suit spraying the perfume bottle from the reference onto his wrist, dark charcoal "
     "background, a single warm spotlight catching the faceted black cap and the golden liquid, elegant and masculine.", SIDE),
   "ליאו.<br>בושם לגבר. מיוצר בישראל.", "100 מ״ל · 289 ש״ח",
   "בושם שנשאר איתכם כל היום, ולא נעלם עד הצהריים.\n\nליאו של בי סנטס מיוצר בישראל, מחומרי גלם שנבחרו בקפידה, בבקבוק שנראה טוב על כל שיש.\n\n100 מ״ל ב-289 ש״ח, ומגיעה איתו דוגמית במתנה.\n\nלגבר שיודע מה הוא לובש.",
   "ליאו, בושם לגבר מיוצר בישראל. 100 מ״ל.",
   "ליאו. בושם לגבר.", "100 מ״ל · 289 ש״ח", people=True)
ad(19, "A5", "9:16", ["liya"],
   P("The women's perfume bottle from the reference resting on flowing deep-red silk with luxurious folds, soft directional light "
     "making the gold liquid and the faceted gold cap glow, rich and sensual perfume-campaign mood.", TOP),
   "לייה.<br>נשיות עם חתימה.", "100 מ״ל · מיוצר בישראל",
   "יש בשמים שמריחים. ויש בשמים שזוכרים.\n\nלייה של בי סנטס: פרחוני, מתקתק ורענן, עם תווי מנדרינה, פריחת תפוז, וניל ודבש.\n\nמיוצר בישראל, 100 מ״ל ב-289 ש״ח, עם דוגמית במתנה.\n\nפינוק לעצמך, או מתנה למישהי שאוהבים.",
   "לייה, בושם לאישה מיוצר בישראל. 100 מ״ל.",
   "לייה. בושם לאישה.", "100 מ״ל · 289 ש״ח")
ad(20, "A5", "4:5", ["cargold"],
   P("Sunny daytime inside a luxury car, shot from the back seat between the front seats: the gold car scent diffuser from the "
     "reference sits sharp in the centre cup holder in the lower third; a woman in a cream blazer is at the wheel on the left, "
     "seen from behind and softly out of focus (no face visible); through the windshield a bright, soft, empty sky fills the "
     "upper half of the frame.", "The upper 40% of the frame must be bright, calm sky with nothing in it."),
   "5 דקות בלי תזוזה?<br>הוא נכבה לבד.", "חיישן תנועה מובנה",
   "מפיץ ריח לרכב שחושב בשבילכם.\n\nל-TO-CAR של בי סנטס יש חיישן תזוזה: כשהרכב זז הוא עובד, ואחרי 5 דקות בלי תנועה הוא נכבה לבד.\n\nשלוש עוצמות ריח, תאורת לד עדינה, וסוללה נטענת.\n\nבשחור או בזהב, ב-299 ש״ח.",
   "מפיץ לרכב עם חיישן תזוזה שנכבה לבד. 299 ש״ח.",
   "המפיץ שנכבה לבד", "TO-CAR · שחור או זהב", people=True)

HERO_PROMPT = P("Hero campaign photograph for a luxury home-fragrance brand: the black wall-mounted diffuser from the first reference on "
                "a deep charcoal plaster wall of a dim, elegant boutique-hotel lounge, a single warm beam of light grazing the wall and the "
                "device, the perfume-oil bottle from the second reference on a travertine shelf just below it, the upper half of the frame "
                "in deep soft shadow (dark and empty), rich warm tones, cinematic.",
                "The upper 45% of the frame must be dark and empty. Portrait 4:5.")

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "ref": REF}, sys.stdout, ensure_ascii=False, indent=1)
