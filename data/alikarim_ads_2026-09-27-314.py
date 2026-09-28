"""Ali Karim / עלי כריים (lead 2026-09-27-314): research, 5 angles, 20 ads — image prompts + Hebrew copy.

Physiotherapist, osteopath and chiropractic treatment (Neuroflex clinic). Clinics in Majd al-Krum and Be'er Sheva.
Phone / WhatsApp Business 050-228-0590 (the WhatsApp Business profile was checked by Eran on 2026-09-28).
Their ads: 17 active, all phone videos of him treating real patients (good: authentic), in Hebrew and Arabic, but only
about five different texts, every button opens Messenger (the number is only in the text), no ad about one specific
pain, and the two strongest facts (first consultation at no cost, partial refund for Clalit members) sit at the very end
of a long text. Several lines are the kind Meta pushes back on in health ads ("כואב לך?", "אם אתם סובלים מ...",
"תוצאות מובטחות").
Clinic ads, so: no product fidelity. References are his own treatment room (cream bed, white shelves, plants, oak
herringbone floor) so the set feels like his place. The therapist is never shown with a face (hands, forearms, from
behind): we don't put a fake Ali in his ads. Patients look natural, no exaggerated pain faces.
Copy: plural, never asserts the reader's condition ("כואב לכם?" / "אתם סובלים"); talks about the situation instead.
No promises of results, no Latin letters, no dashes.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-27-314"

REF = {"room": "2d9f9a09-0249-422c-a72c-ef6e815b86cd",   # his shelves with plants and lantern (frame of ad 1615049366703092)
       "bed": "649c931d-a5b2-4e31-bd89-88a9f72b63eb"}    # cream table and oak herringbone floor (frame of ad 1723871258623038)

STYLE = ("Premium healthcare advertising photograph, warm and calm: soft natural light, clean uncluttered spaces, warm "
         "neutral tones with touches of green, honest real people with real skin texture, shot on a full frame camera, "
         "shallow depth of field, photorealistic, editorial quality, not stock-looking. ")
RULES = ("No text, letters, logos, signs or watermarks anywhere. Anatomically correct hands and fingers. Nobody looks "
         "in pain in an exaggerated way; expressions are natural. The therapist is never shown with a face: only hands "
         "and forearms, or from behind. ")
ONE = ("COMPOSITION: one real photograph taken in one place, in one shot. The subject sits low in the frame; the top "
       "third is simply more of the same wall or background, plain and softly lit. No collage, no inset photo, no "
       "pasted rectangle, no seams, no bands, no borders.")
ROOM = ("The room matches the reference photos of the clinic: cream padded treatment table, white wall shelves with a "
        "small plant and a lantern, warm oak herringbone floor. ")


def P(scene: str, air: str = ONE, room: bool = False) -> str:
    return STYLE + (ROOM if room else "") + scene + " " + air + " " + RULES


RESEARCH = {
    "one_liner": "פיזיותרפיסט, אוסטאופת וטיפולי כירופרקטיקה, עם קליניקות במג'ד אל כרום ובבאר שבע. טיפול ידני אישי "
                 "לכאבי גב, פריצות דיסק, צוואר, כתפיים ומפרקים. ייעוץ ראשון בלי עלות והחזר חלקי לחברי כללית.",
    "hero_products": ["טיפול בכאבי גב ופריצת דיסק", "סיאטיקה", "צוואר וכתפיים", "שיקום וחזרה לתנועה"],
    "audience": [
        {"persona": "העובד עם הגב", "who": "גברים ונשים 30–60, עבודה פיזית או ישיבה ארוכה", "cares": "לחזור לתפקד בלי כדורים"},
        {"persona": "מול המסך", "who": "25–45, משרד ונהיגה", "cares": "צוואר וכתפיים תפוסים, שינה טובה"},
        {"persona": "רוצים לזוז", "who": "50–70", "cares": "מדרגות, הליכה, נכדים, בלי לפחד מכאב"},
    ],
    "pains": ["\"כל בוקר מתחיל בכאב גב\"", "\"הכאב יורד לי לרגל\"", "\"הצוואר תפוס מהמחשב\"",
              "\"כבר ניסיתי כדורים ומשככים\"", "\"אני לא יודע למי לפנות\""],
    "desires": ["לקום בבוקר בלי כאב", "לישון לילה שלם", "לחזור ללכת, לרוץ ולשחק עם הילדים", "מטפל אחד שמכיר אותי"],
    "objections": ["\"זה יעלה לי הון\"", "\"עוד טיפול שלא יעזור\"", "\"זה רחוק ממני\"", "\"מי בכלל מטפל בי\""],
    "current_ads_audit": "17 מודעות פעילות, כולן סרטונים אמיתיים של עלי מטפל במטופלים, בעברית ובערבית. זה הדבר הכי "
                         "חזק שיש להן. אבל יש רק כחמישה טקסטים, רובם בכמה עותקים, כל הכפתורים פותחים הודעה בפייסבוק "
                         "והמספר מופיע רק בתוך הטקסט, ואין אף מודעה שמדברת על כאב מסוים. ייעוץ ראשון בלי עלות והחזר "
                         "חלקי לחברי כללית מופיעים רק בסוף טקסט ארוך. חלק מהמשפטים הם מהסוג שמטא נוטה לעצור במודעות "
                         "בריאות.",
    "gaps": ["כל הכפתורים למסנג'ר, והוואטסאפ רק בטקסט", "אין מודעה לכאב מסוים: דיסק, סיאטיקה, צוואר, כתף, ברכיים",
             "ייעוץ ראשון בלי עלות והחזר מכללית קבורים בסוף", "אותם טקסטים בכמה עותקים",
             "משפטים שמטא מגבילה במודעות בריאות"],
    "angles": [
        {"id": "A1", "name": "גב תחתון ודיסק", "idea": "הכאב שמתחיל כבר ביציאה מהמיטה, ומה עושים איתו: אבחון, טיפול ידני ותרגילים.", "persona": "העובד עם הגב", "hook": "כשכל בוקר מתחיל בכאב גב.", "why": "הכאב הכי נפוץ, ומי שיש לו מחפש פתרון עכשיו."},
        {"id": "A2", "name": "סיאטיקה", "idea": "הכאב שיורד לרגל, בנהיגה, בעמידה ובלילה.", "persona": "העובד עם הגב", "hook": "כשהכאב יורד לרגל.", "why": "כאב חד ומפחיד, שמוביל לפנייה מהירה."},
        {"id": "A3", "name": "צוואר וכתפיים", "idea": "יום מול המסך, צוואר תפוס וכתף שלא עולה עד הסוף.", "persona": "מול המסך", "hook": "יום מול המסך. והצוואר מרגיש הכול.", "why": "קהל צעיר יותר, שעוד לא מכיר את הקליניקה."},
        {"id": "A4", "name": "חזרה לתנועה", "idea": "מה חוזרים לעשות: מדרגות, הליכה, ריצה, משחק עם הנכדים.", "persona": "רוצים לזוז", "hook": "מדרגות, בלי לעצור באמצע.", "why": "מדבר על התוצאה ולא על הכאב, וזה מה שמטא מעדיפה."},
        {"id": "A5", "name": "מטפל אחד, ישר לוואטסאפ", "idea": "עלי עצמו, ייעוץ ראשון בלי עלות, החזר חלקי מכללית, ושאלה שנשלחת ישר אליו.", "persona": "כולם", "hook": "שאלה על הכאב? כתבו לעלי.", "why": "מוריד את החשש מהפנייה הראשונה, ומוביל ישר לשיחה."},
    ],
}

A = []
WA = "WhatsApp"


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta=WA, people=False):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=None, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=[], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


END = "\n\nכתבו לנו בוואטסאפ ונקבע ייעוץ ראשון, בלי עלות."

# ---------- A1 גב תחתון ודיסק ----------
ad(1, "A1", "4:5", [],
   P("Early morning in a bright simple bedroom: a man in his forties in a grey t-shirt sits on the edge of the bed, "
     "feet on the floor, one hand pressed on his lower back, about to stand up slowly. Soft window light, white "
     "sheets. Seen from the side, his face calm and tired."),
   "כשכל בוקר<br>מתחיל בכאב גב.", "פיזיותרפיה · אוסטאופתיה · כירופרקטיקה",
   "יש כאב גב שמתחיל עוד לפני שיוצאים מהמיטה, ומלווה את כל היום.\n\nבקליניקה של עלי כריים מתחילים באבחון, וממשיכים "
   "בטיפול ידני ובתרגילים שמתאימים לגב של כל אחד." + END,
   "כאב גב שמתחיל כבר בבוקר? מתחילים באבחון.", "טיפול בכאבי גב", "ייעוץ ראשון בלי עלות", people=True)
ad(2, "A1", "1:1", ["room", "bed"],
   P("Close-up of a therapist's two hands placed on the lower back of a patient lying face down on the cream "
     "treatment table, patient in a plain dark t-shirt, calm focused touch, soft daylight. Only hands, forearms and "
     "the patient's back are visible.", room=True),
   "פריצת דיסק.<br>מתחילים באבחון נכון.", "טיפול ידני ותרגילים מותאמים",
   "פריצת דיסק היא לא משפט אחד לכולם. אצל כל אחד היא מרגישה אחרת, ולכן גם הטיפול.\n\nעלי כריים, פיזיותרפיסט "
   "ואוסטאופת, בודק קודם מה בדיוק קורה בגב, ורק אז בונה טיפול." + END,
   "פריצת דיסק? מתחילים באבחון.", "טיפול בפריצת דיסק", "אבחון וטיפול ידני", people=True)
ad(3, "A1", "4:5", [],
   P("A father in his thirties in a sunny living room lifting his laughing four year old son up in the air, both "
     "happy, natural movement, bright window behind them, warm light. Faces natural."),
   "להרים את הילד<br>בלי לחשוב פעמיים.", "טיפול בכאבי גב · מג'ד אל כרום · באר שבע",
   "יש רגעים שהגב לא אמור להיות חלק מהם. להרים את הילד, לסחוב קניות, לשחק על הרצפה.\n\nבקליניקה של עלי כריים "
   "עובדים על הגב, כדי שתוכלו לחזור לרגעים האלה." + END,
   "להרים את הילד בלי לחשוב פעמיים.", "טיפול בכאבי גב", "מג'ד אל כרום · באר שבע", people=True)
ad(4, "A1", "9:16", ["room"],
   P("A realistic anatomical spine model standing on a white wall shelf in the clinic next to a small green plant and "
     "a lantern, soft morning light, shallow depth of field. No people.", room=True),
   "הגב לא אמור<br>לנהל לכם את היום.", "פיזיותרפיה · אוסטאופתיה · כירופרקטיקה",
   "עבודה, נהיגה, ישיבה ארוכה. ובסוף היום הגב מרגיש את הכול.\n\nעלי כריים, פיזיותרפיסט ואוסטאופת עם יותר מעשר "
   "שנות ניסיון, מטפל בכאבי גב בטיפול ידני אישי." + END,
   "הגב לא אמור לנהל לכם את היום.", "טיפול בכאבי גב", "יותר מעשר שנות ניסיון")

# ---------- A2 סיאטיקה ----------
ad(5, "A2", "4:5", [],
   P("A woman in her fifties standing at a bright home kitchen counter, one hand resting on the back of her hip and "
     "upper thigh, pausing mid task, soft daylight, calm tired expression, seen from the side."),
   "כשהכאב<br>יורד לרגל.", "טיפול בסיאטיקה",
   "כאב שמתחיל בגב התחתון ויורד לאורך הרגל יכול להפוך עמידה במטבח למשימה.\n\nבקליניקה של עלי כריים בודקים מאיפה "
   "הכאב מגיע, ומטפלים במקור שלו." + END,
   "כשהכאב יורד לרגל.", "טיפול בסיאטיקה", "אבחון וטיפול ידני", people=True)
ad(6, "A2", "1:1", ["room", "bed"],
   P("A therapist's hands gently lifting a patient's straight leg by the heel and knee, the patient lying on his back "
     "on the cream treatment table in grey sweatpants, a careful examination, soft daylight. Only the therapist's "
     "hands and forearms are visible, no therapist face.", room=True),
   "סיאטיקה.<br>יש מה לעשות.", "אבחון · טיפול ידני · תרגילים",
   "סיאטיקה לא חייבת להיות משהו שלומדים לחיות איתו.\n\nמתחילים באבחון מסודר, ממשיכים בטיפול ידני, ומקבלים תרגילים "
   "שאפשר לעשות גם בבית." + END,
   "סיאטיקה? יש מה לעשות.", "טיפול בסיאטיקה", "ייעוץ ראשון בלי עלות", people=True)
ad(7, "A2", "4:5", [],
   P("Inside a car, a man in his forties driving on a sunny highway, one hand on the wheel and the other pressing the "
     "side of his lower back, shot from the passenger seat, natural light, calm focused face."),
   "שעה בנהיגה.<br>והרגל כבר כואבת.", "טיפול בסיאטיקה ובכאבי גב",
   "מי שנוהג הרבה מכיר את זה: אחרי שעה, הכאב כבר יורד לרגל.\n\nעלי כריים מטפל בסיאטיקה ובכאבי גב בקליניקות במג'ד "
   "אל כרום ובבאר שבע." + END,
   "שעה בנהיגה, והרגל כבר כואבת.", "טיפול בסיאטיקה", "מג'ד אל כרום · באר שבע", people=True)
ad(8, "A2", "9:16", [],
   P("A man in his fifties walking easily along a dirt path through a Galilee olive grove in soft morning light, "
     "relaxed posture, seen from behind and slightly to the side, hills in the background."),
   "לחזור ללכת<br>בלי לספור צעדים.", "טיפול בסיאטיקה · מג'ד אל כרום",
   "הליכה של בוקר, בלי לחשוב כמה צעדים נשארו עד שהכאב חוזר.\n\nזו המטרה של הטיפול: לחזור לזוז בחופשיות." + END,
   "לחזור ללכת בלי לספור צעדים.", "טיפול בסיאטיקה", "ייעוץ ראשון בלי עלות", people=True)

# ---------- A3 צוואר וכתפיים ----------
ad(9, "A3", "4:5", [],
   P("Evening at a home desk: a woman in her thirties at a laptop rubbing the back of her neck with one hand, warm "
     "desk lamp light, plants in the background, calm tired expression, seen from the side."),
   "יום מול המסך.<br>והצוואר מרגיש הכול.", "טיפול בצוואר ובכתפיים",
   "שמונה שעות מול מחשב, ועוד שעה בטלפון. הצוואר והכתפיים סוחבים את כל זה.\n\nעלי כריים מטפל בצוואר ובכתפיים "
   "תפוסים, עם טיפול ידני ותרגילים קצרים ליום העבודה." + END,
   "יום מול המסך, והצוואר מרגיש הכול.", "טיפול בצוואר ובכתפיים", "טיפול ידני ותרגילים", people=True)
ad(10, "A3", "1:1", ["room"],
   P("A patient sitting on the cream treatment table seen from behind, a therapist's hands working on the muscles "
     "between the neck and the shoulders, soft daylight. Only the therapist's hands and forearms are visible.",
     room=True),
   "צוואר תפוס<br>לא עובר מעצמו.", "טיפול בצוואר ובכתפיים",
   "צוואר תפוס שחוזר כל כמה ימים הוא סימן שכדאי לבדוק מה עומד מאחוריו.\n\nבקליניקה של עלי כריים מתחילים "
   "באבחון, וממשיכים בטיפול ידני." + END,
   "צוואר תפוס לא עובר מעצמו.", "טיפול בצוואר", "ייעוץ ראשון בלי עלות", people=True)
ad(11, "A3", "4:5", [],
   P("A man in his fifties in a bright kitchen reaching up to a high cabinet with one arm, his other hand on his "
     "shoulder, the reaching arm stopping halfway, natural expression, soft daylight, seen from the side."),
   "כתף שלא עולה<br>עד הסוף.", "טיפול בכאבי כתף",
   "להוריד משהו מהמדף העליון, ללבוש מעיל, להסתרק. כשהכתף לא עולה עד הסוף, כל דבר קטן נהיה מסובך.\n\nעלי כריים "
   "מטפל בכתף כואבת ובהגבלה בתנועה." + END,
   "כתף שלא עולה עד הסוף.", "טיפול בכאבי כתף", "אבחון וטיפול ידני", people=True)
ad(12, "A3", "9:16", [],
   P("A woman sleeping peacefully on her side in a bright calm bedroom in the early morning, white sheets, soft light "
     "from the window, relaxed face."),
   "לישון לילה שלם<br>בלי להתהפך.", "טיפול בצוואר, בגב ובכתפיים",
   "כשהצוואר או הגב כואבים, גם הלילה נהיה קשה.\n\nהטיפול של עלי כריים מתחיל בשאלה פשוטה: מה מפריע לכם לישון, "
   "ומאיפה זה מגיע." + END,
   "לישון לילה שלם בלי להתהפך.", "טיפול בצוואר ובגב", "ייעוץ ראשון בלי עלות", people=True)

# ---------- A4 חזרה לתנועה ----------
ad(13, "A4", "4:5", [],
   P("A man in his sixties climbing old stone steps in a Galilee village street, one hand lightly on the rail, "
     "smiling slightly, warm afternoon light, bougainvillea on the wall."),
   "מדרגות.<br>בלי לעצור באמצע.", "טיפול בכאבי ברכיים ומפרקים",
   "מדרגות, עלייה לבית של הילדים, סיבוב בשכונה. דברים פשוטים שכאב בברכיים יכול לקחת.\n\nבקליניקה של עלי כריים "
   "עובדים על תנועה, כוח ויציבות, בקצב שלכם." + END,
   "מדרגות, בלי לעצור באמצע.", "טיפול בכאבי ברכיים", "מג'ד אל כרום · באר שבע", people=True)
ad(14, "A4", "1:1", [],
   P("A grandfather in his sixties kicking a ball with his six year old grandson in a sunny village yard with an olive "
     "tree, both laughing, natural movement, warm light."),
   "לשחק עם הנכדים.<br>ולא לשלם על זה אחר כך.", "טיפול בגב, בברכיים ובמפרקים",
   "משחק בחצר עם הנכדים שווה הכול. גם בלי כאב למחרת.\n\nעלי כריים, פיזיותרפיה ואוסטאופתיה, עם טיפול אישי שמתאים "
   "לגיל ולגוף." + END,
   "לשחק עם הנכדים, בלי כאב למחרת.", "טיפול בכאבי מפרקים", "ייעוץ ראשון בלי עלות", people=True)
ad(15, "A4", "4:5", [],
   P("A woman in her thirties stretching her leg on a park bench before a run, early morning, athletic clothes, "
     "focused calm face, soft golden light, trees in the background."),
   "לחזור לרוץ<br>אחרי פציעה.", "שיקום אחרי פציעת ספורט",
   "פציעה בברך, בקרסול או בגב לא חייבת לסיים את העונה.\n\nעלי כריים מלווה חזרה הדרגתית לספורט: טיפול, תרגילים "
   "ובדיקה שהגוף מוכן." + END,
   "לחזור לרוץ אחרי פציעה.", "שיקום ספורט", "טיפול ותרגילים", people=True)
ad(16, "A4", "9:16", ["room"],
   P("In the clinic, a woman in her forties doing a guided exercise with a green elastic resistance band while "
     "sitting on the cream treatment table, a therapist's hand lightly guiding her elbow. Only the therapist's hand "
     "and forearm are visible.", room=True),
   "טיפול שממשיך<br>גם בבית.", "תרגילים מותאמים אישית",
   "הטיפול לא נגמר כשיוצאים מהקליניקה. כל מטופל מקבל תרגילים קצרים, שמתאימים בדיוק לו, להמשך בבית.\n\nככה "
   "השיפור נשאר." + END,
   "טיפול שממשיך גם בבית.", "תרגילים מותאמים אישית", "פיזיותרפיה ואוסטאופתיה", people=True)

# ---------- A5 מטפל אחד, ישר לוואטסאפ ----------
ad(17, "A5", "4:5", ["room", "bed"],
   P("The clinic treatment room itself, empty and ready: the cream padded treatment table with a fresh white sheet, "
     "white wall shelves with a small plant and a lantern, warm oak herringbone floor, soft morning light through the "
     "window. No people.", room=True),
   "קליניקה אחת.<br>מטפל אחד שמכיר אתכם.", "עלי כריים · מג'ד אל כרום · באר שבע",
   "בקליניקה של עלי כריים אין פס ייצור. מי שמאבחן הוא גם מי שמטפל, מהפגישה הראשונה ועד שהכאב מאחוריכם.\n\n"
   "יותר מעשר שנות ניסיון בפיזיותרפיה, אוסטאופתיה וטיפולי כירופרקטיקה." + END,
   "מטפל אחד שמכיר אתכם.", "עלי כריים, פיזיותרפיה ואוסטאופתיה", "מג'ד אל כרום · באר שבע")
ad(18, "A5", "1:1", ["room"],
   P("Close-up of a therapist's two hands resting calmly on a patient's upper back between the shoulder blades, the "
     "patient lying face down on the cream treatment table, soft daylight, gentle and focused. Only hands and "
     "forearms visible.", room=True),
   "טיפול ידני.<br>אישי, לא פס ייצור.", "פיזיותרפיה · אוסטאופתיה",
   "כל טיפול מתחיל בהקשבה: מה כואב, ממתי, ומה כבר ניסיתם.\n\nאחר כך טיפול ידני שמתאים בדיוק לכם." + END,
   "טיפול ידני, אישי.", "טיפול ידני אישי", "ייעוץ ראשון בלי עלות", people=True)
ad(19, "A5", "4:5", [],
   P("A man's hand holding a smartphone over a wooden kitchen table with a cup of coffee, the phone screen shows a "
     "blurred generic chat app with green bubbles and no readable text, soft morning light."),
   "שאלה על הכאב?<br>כתבו לעלי בוואטסאפ.", "תשובה ישירות מהמטפל",
   "לא בטוחים אם זה בשבילכם? פשוט כתבו לעלי בוואטסאפ מה כואב וממתי.\n\nתקבלו תשובה ישירות מהמטפל, בלי מזכירות "
   "ובלי התחייבות.",
   "שאלה על הכאב? כתבו לעלי.", "כתבו לנו בוואטסאפ", "תשובה ישירות מהמטפל", people=True)
ad(20, "A5", "9:16", ["room", "bed"],
   P("After a session: a man in his forties sitting up on the edge of the cream treatment table, stretching his arms "
     "up with a relieved small smile, soft daylight in the clinic room.", room=True),
   "ייעוץ ראשון<br>בלי עלות.", "החזר חלקי לחברי כללית",
   "הפגישה הראשונה היא שיחה ובדיקה, בלי עלות ובלי התחייבות. ולחברי כללית יש גם החזר חלקי על הטיפולים.\n\nכתבו "
   "לנו בוואטסאפ ונקבע.",
   "ייעוץ ראשון בלי עלות.", "ייעוץ ראשון בלי עלות", "החזר חלקי לחברי כללית", people=True)

HERO_PROMPT = P("Hero photograph for a physiotherapy clinic: the calm treatment room in soft morning light, the cream "
                "padded treatment table with a fresh white sheet on the left third of the frame, white shelves with a "
                "plant and a lantern, warm oak herringbone floor. The right two thirds are the same calm white wall "
                "and window light, empty. No people.",
                "One continuous photograph, no borders, bands or panels.", room=True)
HERO_M_PROMPT = P("Vertical hero photograph for a physiotherapy clinic: the calm treatment room seen from the door, the "
                  "cream treatment table and herringbone floor in the lower half, above it the same white wall with a "
                  "small plant on a shelf and soft window light. No people.", room=True)

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "hero_m": HERO_M_PROMPT, "ref": REF}, sys.stdout,
              ensure_ascii=False, indent=1)
