"""Pet Best / פט בסט (lead 2026-09-26-012): research, 5 angles, 20 ads — image prompts + Hebrew copy.

A pet supermarket in the Ramat Yishai area with a web store: dry and wet food (Merrick grain-free, Belcando vet-line
cans, Nature's Protection, Advance), Trixie cat furniture, natural chews (buffalo horn, Petex duck donut), litter,
pads. Free shipping from 199, phone orders on *3647. Ads run for 100–400 days (proven), incl. Russian-language ads,
but they are packshots on white or flat promo flyers.
Visual direction (new in the set): bright, warm home lifestyle — sunlit modern Israeli homes (white walls, light oak,
plants), real dogs and cats living with the product, candid and joyful; still-lifes on light oak with soft shadows.
Ads speak to the customer in plural (their own ads do). Meta policy: vet-line food described as its own label says
("support for…"), no medical promises, no "is your dog sick?" questions.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-26-012"

REF = {
    "donut": "051b4bd1-c402-4777-af86-cf4186cff555",          # Petex dental donut with duck coating, clear bag
    "renal": "8248a80c-56cc-484a-a19b-708e38ba1c59",          # Belcando Vetline Renal can 400 g, ₪18
    "gastro": "9af3035b-9d7d-4ba1-a1c5-03fdbd1dac5d",         # Belcando Vetline Gastro can 400 g, ₪18
    "weight": "472142c8-6d33-44ab-8588-dc3ba581df4b",         # Belcando Vetline Weight Control can 400 g, ₪18
    "merrick_small": "7db6c131-23f2-4162-8d5a-8a73e8e9f661",  # Merrick Lil' Plates salmon & sweet potato 5.4 kg, ₪269
    "merrick_salmon": "ecf70a74-e738-4d3d-b880-6f293084ef21", # Merrick salmon & sweet potato 10 kg, ₪359
    "merrick_beef": "49022dc6-1baa-46d1-91d3-d9aeb8f12238",   # Merrick beef & sweet potato 10 kg, ₪359
    "tower": "29b5017e-1918-49e1-9fc1-9a92936ac22f",          # Trixie scratching tower 82 cm, beige, ₪339
    "ball": "7aa125b8-cb5f-41bf-92b3-755ee863729c",           # Trixie scratching ball 29×31 cm, ₪279
    "vittoria": "19e7d633-f75d-42fb-a031-34402cf1d99b",       # Trixie Vittoria scratcher 43 cm, ₪169
    "mat": "5d47f3a9-23ff-4b85-a16f-68190b3ad369",            # Trixie scratching mat with toy, brown, ₪129
    "horn": "f09872d1-e6e5-4d2d-8f96-a4e49188c6d9",           # natural buffalo horn chew, ₪75
}

STYLE = ("Premium pet-lifestyle advertising photograph, bright warm home editorial: a sunlit modern home with white "
         "walls, light oak floors and green plants, soft natural window light, real healthy dogs and cats living "
         "happily with the product, candid and joyful, shot on medium format, photorealistic. ")
FIDELITY = ("Products must be exact matches of the reference photos: same bag, can and furniture shapes, colours, labels "
            "and logo layout — do not redesign them and do not add or change any text on them. No other text, signage, "
            "watermarks or logos anywhere in the image. Animals look natural and healthy, anatomically correct. ")
TOP = ("COMPOSITION: the subject sits in the lower 60% of the frame; above it the same bright wall simply continues, "
       "calm and empty — no objects, frames, windows edges or lines. One continuous photograph — no borders, bands, "
       "panels or split frames.")


def P(scene: str, air: str = TOP) -> str:
    return STYLE + scene + " " + air + " " + FIDELITY


RESEARCH = {
    "one_liner": "סופרמרקט לחיות מחמד באזור רמת ישי, עם אתר ומשלוחים: מזון יבש ורטוב, מזון רפואי, ריהוט גירוד לחתולים, "
                 "חטיפי לעיסה, חול ופדים. ₪15–359, משלוח חינם מ-199, הזמנות גם ב-3647*.",
    "hero_products": ["מריק ללא דגנים — ₪269–359", "שימורי בלקנדו וטליין (כליות, עיכול, משקל) — ₪18",
                      "מתקני גירוד טריקסי — ₪109–339", "קרן בופאלו טבעית — ₪75", "מבצעי זוגות וחול (5+1)"],
    "audience": [
        {"persona": "בעלי הכלב שבוחרים מזון", "who": "25–55", "cares": "מזון איכותי ונקי, במחיר הוגן, שמגיע עד הבית"},
        {"persona": "אחרי הווטרינר", "who": "30–65", "cares": "מזון ייעודי שהווטרינר המליץ עליו, זמין ומיד"},
        {"persona": "בעלי חתולים בדירה", "who": "22–45", "cares": "חתול רגוע, רהיטים שלמים ובית שנראה טוב"},
        {"persona": "דוברי רוסית באזור", "who": "30–65", "cares": "שירות ותוכן בשפה שלהם (כבר רץ אצלם)"},
    ],
    "pains": ["\"הכלב מגרד / הבטן רגישה ואני לא יודע מה להאכיל\"", "\"הווטרינר אמר מזון רפואי, איפה משיגים?\"",
              "\"החתול הורס את הספה\"", "\"שק של 10 ק״ג — לסחוב מהחנות?\""],
    "desires": ["כלב עם אנרגיה ופרווה יפה", "חתול מרוצה ורהיטים שלמים", "מזון שמגיע לבד", "מחיר הוגן"],
    "objections": ["\"באינטרנט יותר זול\"", "\"זה באמת ללא דגנים?\"", "זמני משלוח", "\"איזה מזון מתאים לכלב שלי?\""],
    "current_ads_audit": "15 מודעות פעילות, חלקן רצות יותר משנה (411 ו-398 יום) — סימן חזק שהן מוכרות. יש גם מודעות ברוסית, "
                         "וזה מצוין. אבל כמעט כולן שקית מזון על רקע לבן או פלאייר מבצע, ואין אף תמונה של כלב או חתול "
                         "אמיתי שנהנה מהמוצר. כל חנות אחרת יכולה להריץ את אותן מודעות.",
    "gaps": ["אין חיות אמיתיות במודעות", "המזון הרפואי (בלקנדו) בלי סיפור", "ריהוט החתולים, מוצר ויזואלי, בלי במה",
             "הסופרמרקט עצמו (שירות, משלוח, 3647*) לא מקבל זהות", "אין זווית 'ללא דגנים' למזון הפרימיום"],
    "angles": [
        {"id": "A1", "name": "ללא דגנים", "idea": "מריק: סלמון או בקר ובטטה, ללא דגנים. מזון פרימיום שנראה ומרגיש אחרת.", "persona": "בעלי הכלב שבוחרים מזון", "hook": "סלמון ובטטה. בלי דגנים.", "why": "מוצר פרימיום עם רווח גבוה ומסר ברור."},
        {"id": "A2", "name": "כשהווטרינר אמר דיאטה", "idea": "שימורי בלקנדו וטליין: כליות, עיכול ומשקל. זמין, במלאי ועד הבית.", "persona": "אחרי הווטרינר", "hook": "הווטרינר אמר דיאטה? יש לנו.", "why": "קנייה חוזרת לאורך זמן, קהל שמחפש בדיוק את זה."},
        {"id": "A3", "name": "החתול צריך איפה", "idea": "מתקני גירוד טריקסי: החתול מקבל מקום משלו, הספה נשארת שלכם.", "persona": "בעלי חתולים בדירה", "hook": "החתול צריך איפה לגרד. תנו לו.", "why": "מוצר ויזואלי ומחיר סל גבוה."},
        {"id": "A4", "name": "לעיסה טבעית", "idea": "קרן בופאלו ודונאט ברווז: חטיפי לעיסה ארוכים ששומרים על שיניים ומעסיקים.", "persona": "בעלי הכלב שבוחרים מזון", "hook": "לועס. רגוע. שמח.", "why": "מוצר זול יחסית שמוסיף לכל הזמנה."},
        {"id": "A5", "name": "הסופרמרקט של החיות", "idea": "פט בסט עצמה: הכול במקום אחד, משלוח חינם מ-199, הזמנה ב-3647*.", "persona": "כולם", "hook": "כל מה שהם צריכים. עד הדלת.", "why": "בונה זהות לחנות מול האתרים הגדולים."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now", people=False):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=None, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=[], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 ללא דגנים ----------
ad(1, "A1", "4:5", ["merrick_salmon"],
   P("The Merrick salmon & sweet potato 10 kg bag from the reference standing on a light oak kitchen floor in a sunlit "
     "white kitchen, a ceramic bowl of kibble in front of it, a happy border collie sitting beside the bag looking at "
     "the bowl."),
   "סלמון ובטטה.<br>בלי דגנים.", "מריק · 10 ק״ג · 359 ש״ח",
   "מזון יבש מלא לכלב בוגר, עם סלמון אמיתי כרכיב ראשון ובטטה, ובלי דגנים.\n\nמריק, 10 ק״ג, 359 ש״ח. משלוח חינם עד הבית.",
   "סלמון ובטטה. בלי דגנים.", "מריק ללא דגנים", "359 ש״ח", people=True)
ad(2, "A1", "1:1", ["merrick_beef"],
   P("The Merrick beef & sweet potato bag from the reference on light oak boards, a raw sweet potato and a ceramic bowl "
     "of kibble beside it, soft window light, white wall."),
   "בקר אמיתי.<br>רכיב ראשון.", "מריק בקר · 359 ש״ח",
   "כשהרכיב הראשון בשק הוא בקר אמיתי, רואים את זה בקערה.\n\nמריק בקר ובטטה, ללא דגנים, 10 ק״ג ב-359 ש״ח.",
   "בקר אמיתי, רכיב ראשון.", "מריק בקר ובטטה", "359 ש״ח")
ad(3, "A1", "4:5", ["merrick_small"],
   P("A small white maltese sitting on a light linen sofa in a bright living room, next to the pink Merrick Lil' Plates "
     "small-breed bag from the reference standing on the floor, soft window light, green plant."),
   "כלב קטן.<br>ארוחה בגודל שלו.", "מריק לגזע קטן · 269 ש״ח",
   "לכלב קטן צריך כופתיות קטנות ומזון עשיר.\n\nמריק לגזע קטן: סלמון ובטטה, ללא דגנים, 5.4 ק״ג ב-269 ש״ח.",
   "כלב קטן, ארוחה בגודל שלו.", "מריק לגזע קטן", "269 ש״ח", people=True)
ad(4, "A1", "9:16", ["merrick_salmon", "merrick_beef", "merrick_small"],
   P("The three Merrick bags from the references standing in a row on a light oak floor against a bright white wall, "
     "a small ceramic bowl of kibble in front, soft window light, a green plant at the side."),
   "שלושה טעמים.<br>אפס דגנים.", "מריק בפט בסט",
   "סלמון, בקר, ומתכון מיוחד לגזעים קטנים.\n\nכל סדרת מריק ללא דגנים, במלאי ועם משלוח חינם מ-199 ש״ח.",
   "שלושה טעמים, אפס דגנים.", "סדרת מריק", "משלוח חינם מ-199")

# ---------- A2 כשהווטרינר אמר דיאטה ----------
ad(5, "A2", "4:5", ["renal", "gastro", "weight"],
   P("The three Belcando Vetline cans from the references (Renal, Gastro, Weight Control) standing in a neat row on a "
     "light oak kitchen counter, a white ceramic bowl in front, soft morning window light, bright white wall."),
   "הווטרינר אמר דיאטה?<br>יש לנו.", "בלקנדו וטליין · 18 ש״ח",
   "הווטרינר המליץ על מזון ייעודי, ועכשיו צריך למצוא אותו.\n\nשימורי בלקנדו וטליין: כליות, מערכת עיכול ומשקל. במלאי, 18 ש״ח לפחית, עד הבית.",
   "הווטרינר אמר דיאטה? יש לנו.", "מזון ייעודי לכלבים", "18 ש״ח")
ad(6, "A2", "1:1", ["weight"],
   P("A slightly chubby happy beagle sitting on a light oak floor beside the green Belcando Weight Control can from the "
     "reference, looking up hopefully, bright kitchen, soft window light."),
   "קצת פחות.<br>אותה הנאה.", "וויט קונטרול · 18 ש״ח",
   "דיאטה לא חייבת להיות עונש.\n\nבלקנדו ווייט קונטרול: מזון ייעודי לתמיכה במשקל, שהכלב עדיין מחכה לו. 18 ש״ח.",
   "קצת פחות, אותה הנאה.", "תמיכה במשקל", "18 ש״ח", people=True)
ad(7, "A2", "4:5", ["gastro"],
   P("A calm golden retriever lying on a soft rug in a sunlit living room, resting its head beside the orange Belcando "
     "Gastro can from the reference, peaceful mood, soft light."),
   "בטן רגועה.<br>כלב רגוע.", "בלקנדו גסטרו · 18 ש״ח",
   "לכלבים עם בטן רגישה.\n\nבלקנדו גסטרו: מזון ייעודי לתמיכה במערכת העיכול. 18 ש״ח לפחית, במלאי.",
   "בטן רגועה, כלב רגוע.", "תמיכה בעיכול", "18 ש״ח", people=True)
ad(8, "A2", "4:5", ["renal"],
   P("The blue Belcando Renal can from the reference standing on a light oak counter next to a white ceramic bowl and a "
     "small glass of water, soft window light, bright white wall, calm and clean."),
   "מזון ייעודי.<br>בלי לחפש.", "כליות · עיכול · משקל",
   "כל סדרת בלקנדו וטליין במלאי קבוע.\n\nמזמינים מהבית, ומקבלים עד הדלת. משלוח חינם מ-199 ש״ח.",
   "מזון ייעודי, בלי לחפש.", "בלקנדו וטליין", "משלוח חינם מ-199")

# ---------- A3 החתול צריך איפה ----------
ad(9, "A3", "4:5", ["tower"],
   P("A fluffy ginger cat stretched out on the top platform of the beige Trixie scratching tower from the reference, in "
     "a bright living room by a window, soft light, green plant."),
   "החתול צריך איפה לגרד.<br>תנו לו.", "מתקן טריקסי · 339 ש״ח",
   "חתול שמגרד את הספה פשוט לא קיבל מקום משלו.\n\nמתקן גירוד טריקסי, 82 ס״מ, עם שתי קומות ומקום לנמנם. 339 ש״ח.",
   "החתול צריך איפה לגרד. תנו לו.", "מתקן גירוד לחתול", "339 ש״ח", people=True)
ad(10, "A3", "1:1", ["ball"],
   P("A curious grey tabby kitten peeking and pawing at the Trixie sisal scratching ball from the reference on a light oak "
     "floor, bright room, soft window light."),
   "הצעצוע.<br>והמגרד.", "כדור גירוד · 279 ש״ח",
   "כדור גירוד מסיסל שחתולים מטפסים עליו, מגרדים ומשחקים.\n\nטריקסי, 29×31 ס״מ, 279 ש״ח.",
   "הצעצוע והמגרד.", "כדור גירוד טריקסי", "279 ש״ח", people=True)
ad(11, "A3", "4:5", ["vittoria", "mat"],
   P("A white-and-grey cat scratching the Trixie Vittoria scratcher from the reference, with the brown Trixie scratching "
     "mat from the second reference on the floor beside it, next to an intact light linen sofa, bright room."),
   "הספה שלכם.<br>נשארת שלכם.", "טריקסי · מ-129 ש״ח",
   "חתולים צריכים לגרד. זה טבעי. השאלה רק איפה.\n\nמגרדים ושטיחי גירוד של טריקסי מ-129 ש״ח, והספה נשארת שלמה.",
   "הספה שלכם נשארת שלכם.", "מגרדים לחתול", "מ-129 ש״ח", people=True)
ad(12, "A3", "9:16", ["tower"],
   P("The beige Trixie scratching tower from the reference standing in a bright minimalist living room corner by a "
     "window, a black cat sitting calmly on its middle platform, light oak floor, plant, soft light."),
   "יפה לחתול.<br>יפה לסלון.", "טריקסי בגוון בז׳",
   "מתקן גירוד בגוון בז׳ שנראה טוב גם בסלון מעוצב.\n\nטריקסי, 82 ס״מ, 339 ש״ח. משלוח חינם מ-199 ש״ח.",
   "יפה לחתול, יפה לסלון.", "מתקן גירוד מעוצב", "339 ש״ח", people=True)

# ---------- A4 לעיסה טבעית ----------
ad(13, "A4", "4:5", ["horn"],
   P("A german shepherd lying on a sunlit wooden balcony deck, chewing a natural buffalo horn from the reference held "
     "between its paws, potted plants behind, warm soft light."),
   "לועס.<br>רגוע. שמח.", "קרן בופאלו · 75 ש״ח",
   "קרן בופאלו טבעית: לעיסה ארוכה שמעסיקה, מרגיעה ושומרת על השיניים.\n\n100% טבעי, 75 ש״ח.",
   "לועס. רגוע. שמח.", "קרן בופאלו טבעית", "75 ש״ח", people=True)
ad(14, "A4", "1:1", ["donut"],
   P("The Petex duck-coated dental donut from the reference, taken out of its bag, lying on a light oak board next to "
     "its clear bag, soft window light, bright white background."),
   "דונאט<br>שמותר לו.", "דונאט ברווז · פטקס",
   "חטיף דנטלי בצורת דונאט עם ציפוי ברווז.\n\nלועסים, נהנים, ושומרים על שיניים נקיות. במלאי בפט בסט.",
   "דונאט שמותר לכלב.", "דונאט דנטלי", "פטקס")
ad(15, "A4", "4:5", ["horn", "donut"],
   P("Two happy dogs, a boxer and a labrador, lying side by side on a sunny lawn, one chewing the natural buffalo horn "
     "and one the Petex duck donut from the references, warm soft light."),
   "אחד לכל אחד.<br>ושקט לכולם.", "חטיפי לעיסה טבעיים",
   "שני כלבים בבית? שני חטיפי לעיסה, ושעה של שקט.\n\nקרן בופאלו ודונאט ברווז, טבעיים ועמידים.",
   "אחד לכל אחד, ושקט לכולם.", "חטיפי לעיסה", "משלוח חינם מ-199", people=True)
ad(16, "A4", "4:5", ["horn"],
   P("Still life: two natural buffalo horns from the reference lying on a light oak board with soft window shadows, "
     "bright white wall, clean and minimal."),
   "100% טבעי.<br>100% עסוק.", "קרן בופאלו · 75 ש״ח",
   "חטיף לעיסה אחד שמחזיק ימים.\n\nקרן בופאלו טבעית לגמרי, לכלבים בינוניים וגדולים. 75 ש״ח.",
   "100% טבעי, 100% עסוק.", "קרן בופאלו", "75 ש״ח")

# ---------- A5 הסופרמרקט של החיות ----------
ad(17, "A5", "4:5", ["merrick_salmon", "mat", "horn"],
   P("A bright home entrance: an open delivery box on the light oak floor with the Merrick salmon bag, the natural "
     "buffalo horn and the rolled brown Trixie scratching mat from the references, a happy dog and a cat inspecting "
     "the box together, soft window light."),
   "כל מה שהם צריכים.<br>עד הדלת.", "משלוח חינם מ-199 ש״ח",
   "מזון, חטיפים, חול, מגרדים ומזון ייעודי: הכול בחנות אחת.\n\nפט בסט, הסופרמרקט לחיות מחמד. משלוח חינם מ-199 ש״ח.",
   "כל מה שהם צריכים, עד הדלת.", "הסופרמרקט לחיות", "משלוח חינם מ-199", people=True)
ad(18, "A5", "1:1", ["merrick_salmon"],
   P("A smiling border collie sitting at a bright home front door beside the Merrick salmon 10 kg bag from the "
     "reference, as if it just arrived, soft daylight."),
   "10 ק״ג.<br>בלי לסחוב.", "משלוח עד הבית",
   "שק של 10 ק״ג לא צריך לעלות איתכם במדרגות.\n\nמזמינים מפט בסט, ומקבלים עד הדלת. חינם מ-199 ש״ח.",
   "10 ק״ג, בלי לסחוב.", "משלוח עד הבית", "חינם מ-199", people=True)
ad(19, "A5", "4:5", ["ball", "merrick_small"],
   P("A cosy bright living room: a cat napping on the Trixie scratching ball from the reference while a small maltese "
     "sits next to the pink Merrick small-breed bag from the second reference, soft window light, plants."),
   "לכלב. לחתול.<br>לכולם בבית.", "הכל במקום אחד",
   "יש בבית גם כלב וגם חתול? אצלנו יש את מה ששניהם צריכים.\n\nמזון, חטיפים, מגרדים וצעצועים, עם משלוח חינם מ-199 ש״ח.",
   "לכלב, לחתול, לכולם בבית.", "הכל במקום אחד", "משלוח חינם מ-199", people=True)
ad(20, "A5", "4:5", ["renal", "merrick_beef", "horn"],
   P("Still life on a light oak shelf against a bright white wall: the Merrick beef bag, the Belcando Renal can and a "
     "natural buffalo horn from the references, a small plant, soft window light."),
   "מזמינים באתר.<br>או בטלפון.", "פט בסט",
   "מעדיפים לדבר עם מישהו? התקשרו ל־3647* ונעזור לכם לבחור.\n\nאו הזמינו באתר, עם משלוח חינם מ-199 ש״ח.",
   "מזמינים באתר או ב־3647*.", "הזמנה בטלפון", "3647*")

HERO_PROMPT = P("Hero campaign photograph for a pet supermarket: a joyful golden retriever and a ginger cat lying "
                "together on a light linen rug in a sunlit bright living room, the Merrick salmon bag from the reference "
                "standing on the oak floor beside them, soft window light, green plants. The animals sit in the lower "
                "60% of the frame; above them the same bright white wall continues, calm and empty.",
                "One continuous photograph — no borders, bands or panels.")
HERO_M_PROMPT = HERO_PROMPT

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "hero_m": HERO_M_PROMPT, "ref": REF}, sys.stdout,
              ensure_ascii=False, indent=1)
