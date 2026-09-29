"""Rephael Center / מרכז רפאל (lead 2026-09-27-313): research, 5 angles, 20 ads — image prompts + Hebrew copy.

Complementary medicine clinic, ברזאני 4, רמת אביב ג', תל אביב. "שיטת רפאל" (developed by Dr. Rafi Perter): diagnosis
first, then a personal multi-discipline plan (chiropractic, osteopathy, Chinese medicine and more). Known for herniated
discs, back, neck, headaches and migraines. Site: first diagnostic meeting at a special price, consultation without
commitment. WhatsApp 054-619-7522 (checked by Eran 2026-09-29).
Their ads: 15 collected (about 23 active), every one a talking-head video of a practitioner in a white coat in the
same office, so the feed sees one ad again and again; most texts run in two copies. The four newest (15 Sep) are the
best written (questions, no promises) and include a strong testimonial (Kobi Sidi), but their button no longer opens
WhatsApp like the older ones. Years of experience differ between ads and site (30, 35, 40). Older texts use lines Meta
restricts in health ads ("סובלים מפריצת דיסק?", "אם גם אתם סובלים") and mix singular and plural.
Clinic ads, so no product fidelity. No face of a practitioner is generated (only hands and forearms, or from behind):
the real practitioners are in their own videos, we don't fake them.
Copy: plural, never asserts the reader's condition, no promised results, no Latin letters, no dashes.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-27-313"
REF = {}

STYLE = ("Premium healthcare advertising photograph, calm and warm: soft natural light, clean uncluttered spaces, warm "
         "neutral tones with deep navy accents, honest real people with real skin texture, shot on a full frame camera, "
         "shallow depth of field, photorealistic, editorial quality, not stock-looking. ")
RULES = ("No text, letters, logos, signs or watermarks anywhere. Anatomically correct hands and fingers. Nobody looks "
         "in pain in an exaggerated way; expressions are natural. A practitioner is never shown with a face: only "
         "hands and forearms, or from behind. Only the people described are in the frame; no extra hands or arms. ")
ONE = ("COMPOSITION: wide natural framing with open space above the subject. One single continuous photograph, no "
       "borders, no panels, no inset images, no split frame.")
ROOM = ("A calm, classic private clinic in Tel Aviv: warm wooden bookshelves with medical books, a few framed diplomas "
        "on a light wall, white window blinds with soft daylight, a padded treatment table with a white sheet, an "
        "anatomical spine model on a shelf. ")


def P(scene: str, air: str = ONE, room: bool = False) -> str:
    return STYLE + (ROOM if room else "") + scene + " " + air + " " + RULES


RESEARCH = {
    "one_liner": "מרכז לרפואה משלימה ברמת אביב ג', תל אביב. שיטת רפאל: קודם אבחון מקור הכאב, ואז תוכנית אישית שמשלבת "
                 "כירופרקטיקה, אוסטאופתיה, רפואה סינית ועוד. מוכרים בעיקר בפריצות דיסק, גב, צוואר וכאבי ראש.",
    "hero_products": ["פריצת דיסק", "כאב שמקרין לרגל", "כאבי ראש ומיגרנות", "אבחון מקור הכאב"],
    "audience": [
        {"persona": "אמרו לי פריצת דיסק", "who": "35–65, תל אביב והמרכז", "cares": "לא למהר לניתוח, להבין מה באמת קורה"},
        {"persona": "ניסיתי הכול", "who": "40–70", "cares": "מישהו שיבדוק לעומק אחרי שכל הבדיקות יצאו תקינות"},
        {"persona": "הראש והצוואר", "who": "25–50, עבודה מול מסך", "cares": "פחות התקפים, פחות כדורים"},
    ],
    "pains": ["\"אמרו לי שהשלב הבא הוא ניתוח\"", "\"הכאב יורד לי לרגל\"", "\"כל הבדיקות תקינות והכאב נשאר\"",
              "\"כבר ניסיתי פיזיותרפיה, דיקור וכדורים\"", "\"כאבי הראש חוזרים כל שבוע\""],
    "desires": ["להבין מאיפה הכאב מגיע", "לא להגיע לניתוח אם לא חייבים", "טיפול אחד מסודר במקום עשרה מטפלים", "לחזור לשגרה"],
    "objections": ["\"עוד מטפל שלא יעזור\"", "\"רפואה משלימה, זה רציני?\"", "\"כמה זה יעלה\"", "\"זה רחוק ממני\""],
    "current_ads_audit": "כ־23 מודעות פעילות, וכולן אותו פורמט: מטפל בחלוק לבן מדבר למצלמה באותו חדר. רוב הטקסטים "
                         "רצים בשני עותקים. ארבע המודעות החדשות מספטמבר הן הכי טובות: שאלות במקום הבטחות, והמלצה חזקה "
                         "של קובי סידי. אבל בהן הכפתור כבר לא פותח וואטסאפ כמו בישנות. שנות הניסיון שונות בין המודעות "
                         "לאתר (30, 35 ו־40), והטקסטים הישנים משתמשים במשפטים שמטא מגבילה במודעות בריאות.",
    "gaps": ["אין אף מודעה שאינה סרטון מדבר", "המודעות החדשות לא מובילות לוואטסאפ", "מספר שנות ניסיון לא אחיד",
             "פגישת האבחון במחיר מיוחד לא מופיעה במודעות", "משפטים שמטא מגבילה במודעות בריאות"],
    "angles": [
        {"id": "A1", "name": "פריצת דיסק, בלי למהר לניתוח", "idea": "המשפט \"יש לך פריצת דיסק\" מבהיל. קודם מבינים מה קורה בגוף בפועל.", "persona": "אמרו לי פריצת דיסק", "hook": "פריצת דיסק לא אומרת בהכרח ניתוח.", "why": "הזווית שהם כבר התחילו בספטמבר, והכי ממוקדת."},
        {"id": "A2", "name": "הכאב שיורד לרגל", "idea": "סיאטיקה ועצב לחוץ: נהיגה, ישיבה, לילה.", "persona": "אמרו לי פריצת דיסק", "hook": "כשהכאב מהגב יורד לרגל.", "why": "כאב חד ומפחיד, שמוביל לפנייה מהירה."},
        {"id": "A3", "name": "כאבי ראש שחוזרים", "idea": "להסתכל גם על הצוואר, היציבה והנשימה, לא רק על הראש.", "persona": "הראש והצוואר", "hook": "כאבי ראש חוזרים? מסתכלים גם מעבר לראש.", "why": "קהל צעיר יותר, ומודעה שכבר עובדת אצלם."},
        {"id": "A4", "name": "הבדיקות תקינות, הכאב נשאר", "idea": "סוד האבחון: מחפשים את מקור הכאב, לא רק את מה שרואים בהדמיה.", "persona": "ניסיתי הכול", "hook": "כל הבדיקות תקינות. אז למה עדיין כואב?", "why": "מדבר ישר למי שכבר ניסה הכול, הקהל הכי חם שלהם."},
        {"id": "A5", "name": "שיטה אחת, מרכז אחד", "idea": "צוות רב תחומי תחת קורת גג אחת ברמת אביב, פגישת אבחון במחיר מיוחד, ושאלה בוואטסאפ.", "persona": "כולם", "hook": "עשרה מטפלים? או תוכנית אחת.", "why": "מוריד את החשש מהפנייה הראשונה ומהמחיר."},
    ],
}

A = []
WA = "WhatsApp"


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta=WA, people=False):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=None, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=[], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


END = "\n\nכתבו לנו בוואטסאפ ונקבע פגישת אבחון במרכז רפאל, רמת אביב."

# ---------- A1 פריצת דיסק ----------
ad(1, "A1", "4:5", [],
   P("A man in his late forties sitting at a kitchen table in the evening, holding an MRI report envelope, looking at "
     "it thoughtfully, a cup of tea beside him, warm lamp light, calm serious expression, seen from the side."),
   "פריצת דיסק<br>לא אומרת בהכרח ניתוח.", "מרכז רפאל · רמת אביב",
   "המילים \"פריצת דיסק\" מבהילות, במיוחד כשהכאב מקרין לרגל.\n\nלפני שמחליטים מה הלאה, כדאי לחבר בין מה שרואים "
   "בהדמיה לבין מה שקורה בגוף בפועל: איך אתם זזים, מה מחמיר ומה מקל. במרכז רפאל זה השלב הראשון." + END,
   "פריצת דיסק לא אומרת בהכרח ניתוח.", "טיפול בפריצת דיסק", "אבחון לפני החלטה", people=True)
ad(2, "A1", "1:1", [],
   P("A practitioner's two hands resting on the lower back of a patient lying face down on a padded treatment table "
     "with a white sheet, calm focused touch, soft daylight through white blinds. Only the practitioner's hands and "
     "forearms are visible.", room=True),
   "פריצת דיסק.<br>קודם מבינים, אחר כך מטפלים.", "שיטת רפאל · אבחון ותוכנית אישית",
   "לא כל פריצת דיסק זהה, ולכן גם לא כל טיפול.\n\nבשיטת רפאל מתחילים בבדיקה ידנית מעמיקה, ורק אחריה בונים תוכנית "
   "שמשלבת את הטיפולים שמתאימים לכם." + END,
   "פריצת דיסק? קודם מבינים.", "שיטת רפאל לפריצת דיסק", "בדיקה ידנית מעמיקה", people=True)
ad(3, "A1", "4:5", [],
   P("A woman in her fifties tying her sneakers on the steps of a quiet Tel Aviv apartment building entrance in the "
     "morning, ready for a walk, calm content expression, soft sunlight, seen from the side."),
   "לחזור ללכת.<br>בלי לחשוב על הגב.", "טיפול בפריצת דיסק · תל אביב",
   "הליכה של בוקר, סידורים, עלייה במדרגות. דברים שגב כואב לוקח בלי לשאול.\n\nבמרכז רפאל עובדים על החזרה אליהם, "
   "בתוכנית שנבנית אחרי אבחון." + END,
   "לחזור ללכת, בלי לחשוב על הגב.", "טיפול בפריצת דיסק", "מרכז רפאל · רמת אביב", people=True)
ad(4, "A1", "9:16", ["room"],
   P("A realistic anatomical spine model standing on a warm wooden bookshelf next to medical books and a small plant, "
     "soft window light through white blinds, shallow depth of field. No people.", room=True),
   "הדיסק הוא רק<br>חלק מהתמונה.", "מרכז רפאל · שיטת רפאל",
   "ההדמיה מראה דיסק. אבל הכאב מושפע גם מהיציבה, מהשרירים, מהתנועה ומהעומסים של היום יום.\n\nבמרכז רפאל מסתכלים "
   "על כל התמונה, ולא רק על הצילום." + END,
   "הדיסק הוא רק חלק מהתמונה.", "אבחון מקור הכאב", "שיטת רפאל")

# ---------- A2 הכאב שיורד לרגל ----------
ad(5, "A2", "4:5", [],
   P("Inside a car in Tel Aviv traffic, a man in his forties driving, one hand on the wheel and the other resting on "
     "his thigh, shifting in the seat, soft afternoon light, calm tired expression, shot from the passenger seat."),
   "כשהכאב מהגב<br>יורד לרגל.", "טיפול בסיאטיקה · רמת אביב",
   "ישיבה ארוכה, נהיגה, והכאב מתחיל בגב וממשיך לאורך הרגל.\n\nבמרכז רפאל בודקים מאיפה הכאב מגיע ומה לוחץ, ובונים "
   "טיפול שמתאים בדיוק לזה." + END,
   "כשהכאב מהגב יורד לרגל.", "טיפול בסיאטיקה", "מרכז רפאל · תל אביב", people=True)
ad(6, "A2", "1:1", [],
   P("In the clinic, a practitioner's hands gently lifting a patient's straight leg by the heel and knee, the patient "
     "lying on his back on the padded table in grey trousers, a careful examination, soft daylight. Only the "
     "practitioner's hands and forearms are visible.", room=True),
   "סיאטיקה.<br>מתחילים בבדיקה.", "בדיקה ידנית מעמיקה",
   "כאב שמקרין לרגל יכול להגיע מכמה מקומות, ולכן הבדיקה היא החלק הכי חשוב.\n\nבפגישה הראשונה במרכז רפאל עוברים "
   "על התנועה, על הגב ועל מה שמחמיר את הכאב." + END,
   "סיאטיקה? מתחילים בבדיקה.", "טיפול בסיאטיקה", "פגישת אבחון", people=True)
ad(7, "A2", "4:5", [],
   P("Night in a calm bedroom: a woman in her fifties asleep peacefully on her side with a pillow between her knees, "
     "soft bedside lamp light, white linen, relaxed face. She is alone in the frame."),
   "לישון לילה שלם.<br>בלי לחפש תנוחה.", "טיפול בכאבי גב ורגליים",
   "כשהכאב יורד לרגל, גם הלילה נהיה ארוך.\n\nבמרכז רפאל מחפשים את מקור הכאב, כדי שהטיפול יתאים לגוף שלכם ולא רק "
   "לכאב של היום." + END,
   "לישון לילה שלם, בלי לחפש תנוחה.", "טיפול בכאבי גב", "מרכז רפאל", people=True)
ad(8, "A2", "9:16", [],
   P("A man in his sixties walking easily along the Tel Aviv promenade by the sea in the early morning, relaxed "
     "posture, seen from behind and slightly to the side at a distance, soft golden light."),
   "לחזור לטיילת.<br>בקצב שלכם.", "מרכז רפאל · רמת אביב",
   "הליכה של בוקר לאורך הים, בלי לספור צעדים.\n\nזה מה שהטיפול במרכז רפאל מכוון אליו: לחזור לזוז, בקצב שמתאים לכם." + END,
   "לחזור לטיילת, בקצב שלכם.", "טיפול בכאבי גב", "מרכז רפאל · תל אביב", people=True)

# ---------- A3 כאבי ראש ----------
ad(9, "A3", "4:5", [],
   P("A woman in her thirties at a home office desk in the evening, eyes closed, rubbing the back of her neck with one "
     "hand, laptop open, warm desk lamp, plants in the background, calm tired expression, seen from the side."),
   "כאבי ראש חוזרים?<br>מסתכלים גם על הצוואר.", "טיפול בכאבי ראש ומיגרנות",
   "יש כאבי ראש שמתחילים בכלל בצוואר, ביציבה או בעומס של יום מול המסך.\n\nבמרכז רפאל לא מניחים מראש שכל כאב ראש "
   "הוא אותו דבר. בודקים, ואז מטפלים." + END,
   "כאבי ראש חוזרים? מסתכלים גם על הצוואר.", "טיפול בכאבי ראש", "מרכז רפאל · תל אביב", people=True)
ad(10, "A3", "1:1", [],
   P("In the clinic, a patient lying on her back on the padded table, a practitioner's two hands gently cradling the "
     "back of her neck and head, calm, soft daylight through white blinds. Only the practitioner's hands and forearms "
     "are visible.", room=True),
   "צוואר, יציבה ונשימה.<br>לא רק הראש.", "טיפול במיגרנות · שיטת רפאל",
   "כשכאבי הראש חוזרים, כדאי לבדוק גם את הצוואר, את התנועה ואת היציבה.\n\nבשיטת רפאל הטיפול משלב כמה תחומים, לפי "
   "מה שמצאנו בבדיקה." + END,
   "צוואר, יציבה ונשימה. לא רק הראש.", "טיפול במיגרנות", "שיטת רפאל", people=True)
ad(11, "A3", "4:5", [],
   P("On a wooden kitchen table in the morning: a small plastic pill organizer with a few days filled, a glass of water "
     "and a pair of glasses, soft window light, calm and still. No people, no readable text."),
   "עוד כדור.<br>ועוד התקף.", "טיפול בכאבי ראש ומיגרנות",
   "מי שחי שנים עם מיגרנות כבר מכיר את הכדורים, ויודע לזהות מתי התקף מתקרב.\n\nבמרכז רפאל בודקים מה עוד יכול להיות "
   "חלק מהתמונה, מעבר לראש." + END,
   "עוד כדור, ועוד התקף.", "טיפול במיגרנות", "מרכז רפאל · רמת אביב")
ad(12, "A3", "9:16", [],
   P("A woman in her thirties laughing at an outdoor Tel Aviv cafe table with a friend in soft afternoon light, relaxed "
     "and present, seen from the side, the friend only partly visible from behind."),
   "יום שלם.<br>בלי לחכות להתקף.", "טיפול בכאבי ראש · תל אביב",
   "לתכנן ערב, יום עבודה, טיול. בלי לחשוב כל הזמן מתי זה יגיע.\n\nלשם מכוון הטיפול במרכז רפאל." + END,
   "יום שלם, בלי לחכות להתקף.", "טיפול בכאבי ראש", "מרכז רפאל", people=True)

# ---------- A4 הבדיקות תקינות ----------
ad(13, "A4", "4:5", [],
   P("A woman in her fifties sitting on a sofa at home with a folder of medical test results open on her lap, looking "
     "out of the window thoughtfully, soft afternoon light, calm expression, seen from the side."),
   "כל הבדיקות תקינות.<br>אז למה עדיין כואב?", "סוד האבחון · מרכז רפאל",
   "צילומים, בדיקות דם, בירורים. כולם אומרים שהכול תקין, והכאב נשאר.\n\nבמרכז רפאל מתחילים בבדיקה ידנית מעמיקה, "
   "שמחפשת את מה שמפעיל את הכאב ולא רק את מה שרואים בצילום." + END,
   "כל הבדיקות תקינות. אז למה עדיין כואב?", "אבחון מקור הכאב", "מרכז רפאל · תל אביב", people=True)
ad(14, "A4", "1:1", [],
   P("On a clean wooden desk in the clinic: an open folder of test results and imaging reports, a pair of glasses and a "
     "pen, a practitioner's hand resting on the pages as if reviewing them, soft window light. Only the hand and "
     "forearm are visible, no readable text.", room=True),
   "פגישה ראשונה.<br>קודם מקשיבים.", "אבחון לפני טיפול",
   "בפגישה הראשונה עוברים על כל מה שכבר עשיתם: בדיקות, טיפולים, מה עזר ומה לא.\n\nרק אחרי זה נבנית תוכנית." + END,
   "פגישה ראשונה, קודם מקשיבים.", "פגישת אבחון", "מרכז רפאל", people=True)
ad(15, "A4", "4:5", [],
   P("A man in his sixties in a bright living room slowly bending to pick up a small grandchild's toy from the floor, "
     "easy movement, warm afternoon light, calm face, seen from the side."),
   "ניסיתם כבר הכול?<br>אולי חיפשו במקום הלא נכון.", "שיטת רפאל · רמת אביב",
   "פיזיותרפיה, דיקור, כדורים. כשהכאב חוזר, אולי הוא מגיע ממקום אחר ממה שחשבו.\n\nזה בדיוק מה שהאבחון בשיטת רפאל "
   "מחפש." + END,
   "ניסיתם כבר הכול?", "אבחון מקור הכאב", "שיטת רפאל", people=True)
ad(16, "A4", "9:16", ["room"],
   P("The classic clinic office itself, calm and empty: warm wooden bookshelves with medical books, framed diplomas on "
     "a light wall, a padded treatment table with a white sheet, white blinds with soft morning light. No people.",
     room=True),
   "מקום אחד<br>שמחבר את כל התמונה.", "מרכז רפאל · ברזאני 4, רמת אביב",
   "במקום לעבור ממטפל למטפל, במרכז רפאל יש צוות רב תחומי תחת קורת גג אחת, ותוכנית אחת שמחברת ביניהם." + END,
   "מקום אחד שמחבר את כל התמונה.", "מרכז רפאל", "רמת אביב ג'")

# ---------- A5 שיטה אחת, מרכז אחד ----------
ad(17, "A5", "4:5", ["room"],
   P("The clinic treatment room, calm and ready: a padded treatment table with a fresh white sheet, a warm wooden "
     "bookshelf with an anatomical spine model, framed diplomas, white blinds with soft daylight, a plant. No people.",
     room=True),
   "עשרה מטפלים?<br>או תוכנית אחת.", "שיטת רפאל · רמת אביב ג'",
   "כירופרקטיקה, אוסטאופתיה, רפואה סינית ועוד. במרכז רפאל כולם עובדים לפי תוכנית אחת, שנבנית אחרי אבחון.\n\n"
   "כך לא צריך להתחיל מההתחלה אצל כל מטפל חדש." + END,
   "עשרה מטפלים? או תוכנית אחת.", "שיטת רפאל", "צוות רב תחומי")
ad(18, "A5", "1:1", [],
   P("Close-up of a practitioner's hands writing a personal treatment plan in a notebook on a wooden desk, a spine "
     "model softly blurred behind, warm window light. Only hands and forearms, no readable text."),
   "פגישת אבחון<br>במחיר מיוחד.", "מרכז רפאל · רמת אביב",
   "הפגישה הראשונה היא אבחון: בדיקה, שיחה, ותוכנית. והיא במחיר מיוחד, כדי שיהיה קל להתחיל." + END,
   "פגישת אבחון במחיר מיוחד.", "פגישת אבחון", "מרכז רפאל")
ad(19, "A5", "4:5", [],
   P("Close-up of a woman's hand holding a smartphone above a wooden table next to a cup of coffee, the phone screen "
     "shows a blurred generic chat app with green bubbles and no readable text, soft morning window light, a plant in "
     "the soft background. Only one hand in the frame."),
   "שאלה על הכאב?<br>כתבו לנו בוואטסאפ.", "תשובה ישירות מהמרכז",
   "לא בטוחים אם זה מתאים לכם? כתבו לנו בוואטסאפ מה כואב וממתי, ונחזור אליכם עם תשובה, בלי התחייבות.",
   "שאלה על הכאב? כתבו לנו.", "כתבו לנו בוואטסאפ", "בלי התחייבות", people=True)
ad(20, "A5", "9:16", [],
   P("After a session: a man in his fifties standing up from the padded treatment table and stretching his back with a "
     "small relieved smile, calm clinic with bookshelves and white blinds behind, soft daylight. He is alone in the "
     "frame.", room=True),
   "מרכז רפאל.<br>רמת אביב ג'.", "פריצת דיסק · גב · צוואר · כאבי ראש",
   "מרכז רפאל, ברזאני 4 ברמת אביב ג'. פריצות דיסק, כאבי גב וצוואר וכאבי ראש, בשיטה שמתחילה באבחון." + END,
   "מרכז רפאל, רמת אביב ג'.", "מרכז רפאל", "שיטת רפאל")

# Desktop hero sits in a tall frame (about 4:5): the subject fills it (NOTES, 2026-09-28).
HERO_PROMPT = P("Hero photograph for a private back pain clinic, close framing: a man in his fifties lying face down on a "
                "padded treatment table with a white sheet, a practitioner's two hands resting on his lower back, "
                "warm wooden bookshelves and an anatomical spine model softly behind, white blinds with warm daylight. "
                "The treatment fills the frame, subject in the middle and lower part. Only the practitioner's hands "
                "and forearms are visible.", "One continuous photograph, no borders, bands or panels.", room=True)
HERO_M_PROMPT = P("Vertical hero photograph for a private back pain clinic: a man lying face down on a padded treatment "
                  "table, a practitioner's two hands on his lower back, in the lower 60 percent of the frame; above "
                  "them the calm wall with framed diplomas and a wooden bookshelf with a spine model. Only the "
                  "practitioner's hands and forearms are visible.", room=True)

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "hero_m": HERO_M_PROMPT, "ref": REF}, sys.stdout,
              ensure_ascii=False, indent=1)
