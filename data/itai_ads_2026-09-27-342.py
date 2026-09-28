"""Itai Elbaz / איתי אלבז (lead 2026-09-27-342): research, 5 angles, 20 ads — image prompts + Hebrew copy.

Chinese medicine: acupuncture, cupping, nutrition. One clinic in Karmiel. WhatsApp 053-462-3129 (his WhatsApp profile
"איתי אלבז ~ רפואה סינית", bio: pain of all kinds, back, migraines, stomach; nutrition and balance; checked by Eran
2026-09-28).
Their ads: 5 active, only two texts. The migraine story about "חנה" (3 copies) is strong and specific; the other text
is a generic list of claims ("תוצאות כבר מהטיפול הראשון", "מאות מטופלים", "להיפטר מזה"), the kind Meta restricts in
health ads. Headlines: "לחצו לפרטים", one typo "לחצו לפטים", one in Russian on Hebrew text. Four of five ads run since
April (155 days) in a small area (Karmiel), newest from 6 Sep. All buttons already open WhatsApp (good).
Clinic ads, so no product fidelity. References are frames of his own treatment room (rice paper folding screen, white
treatment table with a white cover, navy bolster, salt lamp, warm wood, light walls). The therapist is never shown with
a face (hands, forearms, from behind): we don't put a fake Itai in his ads.
Copy: plural, never asserts the reader's condition, no promised results, no Latin letters, no dashes.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-27-342"

REF = {"room": "6af35d3c-1b63-4b5a-a42f-715260f29040",   # rice paper screen, white table, bolster (ad 1511015147207008)
       "bed": "c76af457-f68f-406d-8ea6-8c86d71c45ce"}    # white table, navy bolster, salt lamp (ad 2330259721052318)

STYLE = ("Premium healthcare advertising photograph, warm and calm: soft natural light, clean uncluttered spaces, warm "
         "neutral tones with touches of green and soft amber, honest real people with real skin texture, shot on a "
         "full frame camera, shallow depth of field, photorealistic, editorial quality, not stock-looking. ")
RULES = ("No text, letters, logos, signs or watermarks anywhere. Anatomically correct hands and fingers. Nobody looks "
         "in pain in an exaggerated way; expressions are natural. The therapist is never shown with a face: only hands "
         "and forearms, or from behind. Acupuncture needles, when shown, are very thin, few and discreet. ")
ONE = ("COMPOSITION: wide natural framing with open space above the subject. One single continuous photograph, no "
       "borders, no panels, no inset images, no split frame.")
ROOM = ("The room matches the reference photos of the clinic: a light wooden rice paper folding screen, a treatment "
        "table with a white cover, a navy blue bolster, a softly glowing salt lamp, warm wood and light walls. ")


def P(scene: str, air: str = ONE, room: bool = False) -> str:
    return STYLE + (ROOM if room else "") + scene + " " + air + " " + RULES


RESEARCH = {
    "one_liner": "מטפל ברפואה סינית בכרמיאל: דיקור, כוסות רוח וייעוץ תזונה. מטפל בכאבי גב, כתפיים, ברכיים ומפרקים, "
                 "במיגרנות ובכאבי ראש, ובבעיות בטן ושינה. קליניקה אחת, מטפל אחד.",
    "hero_products": ["דיקור סיני למיגרנות וכאבי ראש", "טיפול בכאבי גב וכתפיים", "ברכיים ומפרקים", "תזונה ואיזון"],
    "audience": [
        {"persona": "כאב ראש שחוזר", "who": "נשים 30–55, עבודה ובית", "cares": "יום בלי התקף, פחות כדורים, לתכנן בלי לחשוש"},
        {"persona": "הגב והכתפיים", "who": "גברים ונשים 35–60, עבודה פיזית או ישיבה", "cares": "לחזור לתפקד, לנסות משהו אחר"},
        {"persona": "רוצים לזוז", "who": "55–75, כרמיאל והגליל", "cares": "הליכה, גינה, נכדים, בלי ניתוח"},
    ],
    "pains": ["\"כאב הראש מבטל לי את היום\"", "\"יש לי תיק שלם של כדורים\"", "\"הגב תפוס כל השבוע\"",
              "\"הברכיים לא נותנות לי ללכת\"", "\"כבר ניסיתי הכול\""],
    "desires": ["יום שלם בלי כאב ראש", "לישון טוב ולקום עם כוח", "לחזור ללכת ולעבוד בגינה", "מטפל אחד שמקשיב"],
    "objections": ["\"דיקור זה בשבילי?\"", "\"זה כואב, המחטים?\"", "\"עוד טיפול שלא יעזור\"", "\"כמה טיפולים צריך\""],
    "current_ads_audit": "5 מודעות פעילות עם שני טקסטים בלבד. הסיפור על חנה והמיגרנות הוא המודעה הכי חזקה: ספציפי, "
                         "אנושי, עם פרט שנזכרים בו (התיק עם הכדורים). הטקסט השני הוא רשימת הבטחות כלליות. הכותרות לא "
                         "אומרות כלום (\"לחצו לפרטים\"), באחת יש שגיאת כתיב ואחת ברוסית. ארבע מהמודעות רצות מאפריל, "
                         "באזור קטן. כל הכפתורים כבר פותחים וואטסאפ, וזה נכון.",
    "gaps": ["רק שני טקסטים, ארבעה מהם מאפריל", "כותרות ריקות, אחת עם שגיאה ואחת ברוסית",
             "אין מודעה לברכיים, לכתפיים, לבטן או לשינה, למרות שזה מה שהוא מטפל בו",
             "משפטים שמטא מגבילה במודעות בריאות", "אין מודעה שמסבירה מה קורה בטיפול הראשון"],
    "angles": [
        {"id": "A1", "name": "מיגרנות וכאבי ראש", "idea": "עוד סיפורים כמו של חנה: היום שנעלם, ארוחת שישי, התיק עם הכדורים.", "persona": "כאב ראש שחוזר", "hook": "כשכאב ראש מבטל לכם את היום.", "why": "זו המודעה שכבר עובדת אצלו. מרחיבים אותה לעוד רגעים."},
        {"id": "A2", "name": "גב, צוואר וכתפיים", "idea": "דיקור, כוסות רוח וטיפול ידני לגב ולכתפיים תפוסים.", "persona": "הגב והכתפיים", "hook": "הגב סוחב את כל השבוע.", "why": "הכאב הכי נפוץ, ועוד אין לו מודעה משלו."},
        {"id": "A3", "name": "ברכיים ומפרקים", "idea": "מדברים על מה שחוזרים לעשות: טיילת, גינה, רכיבה בשבת.", "persona": "רוצים לזוז", "hook": "ללכת לטיילת, ולחזור ברגל.", "why": "קהל מבוגר יותר בגליל, שמחפש דרך בלי ניתוח."},
        {"id": "A4", "name": "איזון: שינה, בטן ותזונה", "idea": "הצד השני של הקליניקה: תזונה, שינה ואנרגיה, כמו שכתוב בפרופיל שלו.", "persona": "כולם", "hook": "לישון לילה שלם, ולקום עם כוח.", "why": "פותח קהל חדש שלא מחפש טיפול בכאב."},
        {"id": "A5", "name": "איתי, כרמיאל, ישר לוואטסאפ", "idea": "מטפל אחד, קליניקה קטנה, מה קורה בטיפול הראשון, ושאלה שנשלחת ישר אליו.", "persona": "כולם", "hook": "שאלה על הכאב? כתבו לאיתי.", "why": "מוריד את החשש מדיקור ומהפנייה הראשונה."},
    ],
}

A = []
WA = "WhatsApp"


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta=WA, people=False):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=None, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=[], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


END = "\n\nכתבו לאיתי בוואטסאפ ונקבע טיפול בקליניקה בכרמיאל."

# ---------- A1 מיגרנות וכאבי ראש ----------
ad(1, "A1", "4:5", [],
   P("Late morning in a quiet living room with the curtains half closed: a woman in her late thirties sits on the "
     "sofa, eyes closed, fingertips resting on her temple, a glass of water on the side table. Soft filtered light, "
     "calm tired expression, seen from the side."),
   "כשכאב ראש<br>מבטל לכם את היום.", "רפואה סינית ודיקור · כרמיאל",
   "יש כאבי ראש שלא נשארים בראש. הם מבטלים פגישות, מוציאים מהעבודה מוקדם, ומשאירים את היום באמצע.\n\nאיתי אלבז "
   "מטפל במיגרנות ובכאבי ראש בדיקור סיני, בקליניקה שלו בכרמיאל." + END,
   "כשכאב ראש מבטל לכם את היום.", "טיפול במיגרנות וכאבי ראש", "דיקור סיני בכרמיאל", people=True)
ad(2, "A1", "1:1", ["room", "bed"],
   P("A patient lying face down on the treatment table with the white cover, a therapist's two hands gently pressing "
     "the muscles at the base of the skull and the top of the neck, two or three very thin acupuncture needles on the "
     "upper shoulders, salt lamp glowing softly in the background. Only hands and forearms of the therapist.",
     room=True),
   "מיגרנה.<br>יש עוד דרך לבדוק.", "דיקור סיני לכאבי ראש",
   "דיקור עובד על נקודות בצוואר ובבסיס הגולגולת, שם מצטבר הרבה מהמתח שמלווה כאבי ראש.\n\nבקליניקה של איתי "
   "מתחילים בשיחה: מתי זה מגיע, כמה זמן זה נמשך, ומה כבר ניסיתם." + END,
   "מיגרנה? יש עוד דרך לבדוק.", "דיקור סיני למיגרנות", "טיפול אישי בכרמיאל", people=True)
ad(3, "A1", "4:5", [],
   P("On a light wooden kitchen table in soft morning light: a small open fabric pouch with little compartments "
     "holding a few blister packs of pills, next to a cup of tea and a pair of reading glasses. Calm, still, no "
     "people. Unbranded packs with no readable text."),
   "תיק קטן.<br>לכל כאב כדור אחר.", "הסיפור של חנה",
   "חנה הגיעה לאיתי עם תיק קטן, עם מחיצות. לכל סוג כאב כדור אחר. עשר שנים של מיגרנות, ויום שאחרי שאי אפשר לתכנן.\n\n"
   "היא לא חיפשה נס. היא חיפשה מישהו שיקשיב. עבדו יחד כמה שבועות בדיקור, והיום היא מגיעה פעם בחודש.\n\nכל גוף "
   "מגיב אחרת, ולכן כל טיפול מתחיל בשיחה." + END,
   "תיק קטן. לכל כאב כדור אחר.", "הסיפור של חנה", "דיקור סיני למיגרנות", people=False)
ad(4, "A1", "9:16", [],
   P("A warm Friday night dinner table at home, candles lit, challah and salads, family members' hands and shoulders "
     "around the table, one chair slightly pulled back and empty. Warm golden light, cozy, no faces in focus."),
   "ארוחת שישי.<br>מתחילה ועד הסוף.", "טיפול במיגרנות · כרמיאל",
   "ארוחת שישי שלמה, בלי לקום באמצע לחדר חשוך.\n\nזה בדיוק מה שחנה רצתה, ולשם מכוון הטיפול: לחזור לרגעים "
   "הקטנים שכאב ראש לוקח." + END,
   "ארוחת שישי, מתחילה ועד הסוף.", "טיפול במיגרנות", "דיקור סיני בכרמיאל", people=True)

# ---------- A2 גב, צוואר וכתפיים ----------
ad(5, "A2", "4:5", [],
   P("A man in his forties in a small carpentry workshop at the end of the day, standing by the workbench, one hand "
     "on his lower back, stretching slightly backwards, warm late light through the window, sawdust, calm tired "
     "face, seen from the side."),
   "הגב סוחב<br>את כל השבוע.", "רפואה סינית לכאבי גב",
   "עבודה פיזית, נהיגה, ישיבה ארוכה. ובסוף השבוע הגב מרגיש את הכול.\n\nאיתי אלבז מטפל בכאבי גב בדיקור, בכוסות "
   "רוח ובמגע ידני, בקליניקה בכרמיאל." + END,
   "הגב סוחב את כל השבוע.", "טיפול בכאבי גב", "דיקור וכוסות רוח", people=True)
ad(6, "A2", "1:1", ["room", "bed"],
   P("A patient lying face down on the treatment table with the white cover, four round clear glass cupping cups "
     "placed on the upper back and shoulders, soft daylight, salt lamp glowing in the background. No therapist "
     "visible.", room=True),
   "כוסות רוח<br>לגב ולכתפיים.", "רפואה סינית · כרמיאל",
   "כוסות רוח הן אחד הטיפולים הוותיקים ברפואה הסינית, ובקליניקה של איתי הן חלק מהטיפול בגב ובכתפיים, יחד עם דיקור "
   "ומגע ידני.\n\nכל טיפול מותאם למה שמצאנו בשיחה ובבדיקה." + END,
   "כוסות רוח לגב ולכתפיים.", "כוסות רוח ודיקור", "קליניקה בכרמיאל", people=True)
ad(7, "A2", "4:5", [],
   P("A woman in her thirties at a home office desk with a laptop, turning her head slowly to the side with one hand "
     "on her neck and shoulder, plants and a window behind her, soft afternoon light, calm expression."),
   "צוואר תפוס<br>מהמחשב ומהטלפון.", "טיפול בצוואר ובכתפיים",
   "שמונה שעות מול מסך, ועוד כמה בטלפון. הצוואר והכתפיים סוחבים את זה כל יום.\n\nבקליניקה של איתי משחררים את "
   "האזור בדיקור ובמגע, ומקבלים כמה הרגלים קטנים ליום העבודה." + END,
   "צוואר תפוס מהמחשב ומהטלפון.", "טיפול בצוואר ובכתפיים", "דיקור ומגע ידני", people=True)
ad(8, "A2", "9:16", ["room", "bed"],
   P("Close view in the clinic: a therapist's two hands resting on a patient's upper back between the shoulder "
     "blades, the patient lying face down on the white covered table, a navy bolster, soft light and the rice paper "
     "screen blurred behind. Only hands and forearms visible.", room=True),
   "דיקור, כוסות רוח<br>ומגע ידני.", "טיפול אישי בגב ובכתפיים",
   "לא כל כאב גב דומה, ולא כל טיפול מתאים לכולם.\n\nאיתי משלב דיקור, כוסות רוח ומגע ידני, לפי מה שהגוף שלכם "
   "צריך באותו שבוע." + END,
   "דיקור, כוסות רוח ומגע ידני.", "טיפול אישי בגב", "רפואה סינית בכרמיאל", people=True)

# ---------- A3 ברכיים ומפרקים ----------
ad(9, "A3", "4:5", [],
   P("Two women in their sixties walking and chatting on a wide paved park promenade with trees and green hills in "
     "the Galilee, early morning soft light, sport shoes, relaxed easy steps, seen from the front at a distance."),
   "ללכת לטיילת.<br>ולחזור ברגל.", "טיפול בכאבי ברכיים · כרמיאל",
   "הליכת בוקר עם חברה, בלי לחשוב איך חוזרים.\n\nאיתי אלבז מטפל בכאבי ברכיים ומפרקים בדיקור ובמגע, ומלווה "
   "חזרה לתנועה בקצב שלכם." + END,
   "ללכת לטיילת, ולחזור ברגל.", "טיפול בכאבי ברכיים", "רפואה סינית בכרמיאל", people=True)
ad(10, "A3", "1:1", ["room", "bed"],
   P("A patient lying on her back on the white covered treatment table in loose light trousers rolled above the "
     "knee, a therapist's hands gently holding the knee, three very thin acupuncture needles around the kneecap, soft "
     "daylight, salt lamp glowing behind. Only hands and forearms of the therapist.", room=True),
   "ברכיים ומפרקים.<br>בקצב שלכם.", "דיקור סיני · כרמיאל",
   "המחטים בדיקור דקות מאוד, ורוב המטופלים מופתעים כמה זה רגוע.\n\nבקליניקה של איתי מטפלים בכאבי ברכיים "
   "ומפרקים, ומסבירים כל שלב לפני שמתחילים." + END,
   "כאבי ברכיים? דיקור סיני בכרמיאל.", "דיקור לברכיים ומפרקים", "מסבירים כל שלב", people=True)
ad(11, "A3", "4:5", [],
   P("A woman in her sixties kneeling on a garden kneeling pad in a sunny home garden with herbs and vegetables, "
     "planting, smiling slightly, straw hat, warm morning light, seen from the side."),
   "לעבוד בגינה.<br>ולא לשלם על זה בערב.", "טיפול בברכיים ובגב",
   "שעתיים בגינה שוות הכול. גם בלי כאב בערב.\n\nאיתי אלבז, רפואה סינית ודיקור, מטפל בברכיים, בגב ובמפרקים "
   "בקליניקה בכרמיאל." + END,
   "לעבוד בגינה, בלי כאב בערב.", "טיפול בברכיים ובגב", "דיקור סיני בכרמיאל", people=True)
ad(12, "A3", "9:16", [],
   P("A man in his sixties riding a bicycle on a quiet country road between fields and hills in the Galilee on a "
     "Saturday morning, helmet, relaxed posture, golden light, seen from behind and slightly to the side."),
   "לחזור לרכוב<br>בשבת בבוקר.", "טיפול במפרקים · כרמיאל",
   "רכיבה של שבת בבוקר, כמו פעם.\n\nהטיפול של איתי מתחיל במה שחשוב לכם לחזור לעשות, וממשיך משם." + END,
   "לחזור לרכוב בשבת בבוקר.", "טיפול במפרקים", "רפואה סינית בכרמיאל", people=True)

# ---------- A4 איזון: שינה, בטן ותזונה ----------
ad(13, "A4", "4:5", [],
   P("Early morning in a bright calm bedroom: a woman in her forties sitting up in bed stretching her arms, rested "
     "and calm, white linen, soft sunlight through the window, a plant on the windowsill."),
   "לישון לילה שלם.<br>ולקום עם כוח.", "רפואה סינית ואיזון",
   "שינה, אנרגיה ומצב רוח קשורים זה לזה, והרפואה הסינית מסתכלת עליהם יחד.\n\nאיתי אלבז משלב דיקור וייעוץ "
   "תזונה, לפי מה שהגוף שלכם צריך." + END,
   "לישון לילה שלם, ולקום עם כוח.", "רפואה סינית ואיזון", "דיקור ותזונה", people=True)
ad(14, "A4", "1:1", [],
   P("On a warm wooden table: a clear glass cup of herbal tea with slices of fresh ginger, a small bowl of dried "
     "herbs, goji berries and a few dates, soft side light, a softly glowing salt lamp far in the background. No "
     "people."),
   "בטן רגועה<br>מתחילה בצלחת.", "ייעוץ תזונה ברפואה סינית",
   "נפיחות, כבדות אחרי ארוחה, בטן שלא נרגעת. הרבה פעמים זה מתחיל במה שאוכלים ומתי.\n\nאיתי אלבז נותן ייעוץ "
   "תזונה ברוח הרפואה הסינית, פשוט ומתאים ליום יום." + END,
   "בטן רגועה מתחילה בצלחת.", "ייעוץ תזונה", "רפואה סינית בכרמיאל")
ad(15, "A4", "4:5", [],
   P("A warm bowl of vegetable soup with rice, greens and a soft boiled egg on a light wooden table, steam rising, a "
     "linen napkin and a spoon, soft morning window light. No people."),
   "תזונה שמתאימה<br>לגוף שלכם.", "ייעוץ תזונה ואיזון",
   "אין תפריט אחד שמתאים לכולם. ברפואה הסינית מתחילים מהגוף: מה מרגיש כבד, מה חסר, ומה עושה טוב.\n\nבקליניקה "
   "של איתי זה חלק מהטיפול." + END,
   "תזונה שמתאימה לגוף שלכם.", "ייעוץ תזונה", "חלק מהטיפול")
ad(16, "A4", "9:16", ["room", "bed"],
   P("In the clinic: a man in his forties lying on his back on the white covered treatment table, eyes closed, "
     "breathing calmly, a light blanket over his legs, the salt lamp glowing warm, the rice paper screen behind. "
     "No therapist visible.", room=True),
   "שעה אחת<br>רק בשבילכם.", "רפואה סינית ודיקור · כרמיאל",
   "שעה בלי טלפון, בלי רעש, רק עם הגוף.\n\nככה נראה טיפול אצל איתי: שקט, איטי, ומותאם בדיוק לכם." + END,
   "שעה אחת רק בשבילכם.", "טיפול ברפואה סינית", "קליניקה בכרמיאל", people=True)

# ---------- A5 איתי, כרמיאל, ישר לוואטסאפ ----------
ad(17, "A5", "4:5", ["room", "bed"],
   P("The clinic treatment room itself, empty and ready: the treatment table with a fresh white cover and a navy "
     "bolster, the light wooden rice paper folding screen, the softly glowing salt lamp on a wooden side table, warm "
     "wood and light walls, soft morning light. No people.", room=True),
   "קליניקה קטנה.<br>מטפל אחד שמכיר אתכם.", "איתי אלבז · רפואה סינית ודיקור",
   "בקליניקה של איתי אין תור ארוך ואין מטפל מתחלף. מי שמקשיב בפגישה הראשונה הוא גם מי שמטפל עד הסוף.\n\n"
   "דיקור, כוסות רוח וייעוץ תזונה, בכרמיאל." + END,
   "מטפל אחד שמכיר אתכם.", "איתי אלבז, רפואה סינית", "קליניקה בכרמיאל")
ad(18, "A5", "1:1", ["room"],
   P("Close-up on a wooden side tray in the clinic: sealed sterile acupuncture needle packs, a few round glass "
     "cupping cups and a small folded white towel, the salt lamp glowing softly behind, shallow depth of field. No "
     "people, no readable text on the packs.", room=True),
   "מה קורה<br>בטיפול הראשון?", "שיחה, בדיקה, ורק אחר כך טיפול",
   "הטיפול הראשון מתחיל בשיחה: מה מפריע, ממתי, ומה כבר ניסיתם. רק אחרי זה מחליטים יחד איך מטפלים.\n\nמחטים "
   "סטריליות לשימוש אחד, והסבר על כל שלב." + END,
   "מה קורה בטיפול הראשון?", "הטיפול הראשון אצל איתי", "שיחה, בדיקה וטיפול")
ad(19, "A5", "4:5", [],
   P("Close-up of a woman's hand holding a smartphone above a wooden table next to a cup of herbal tea, the phone "
     "screen shows a blurred generic chat app with green bubbles and no readable text, soft morning window light, a "
     "plant in the soft background."),
   "שאלה על הכאב?<br>כתבו לאיתי בוואטסאפ.", "תשובה ישירות מהמטפל",
   "לא בטוחים אם דיקור מתאים לכם? פשוט כתבו לאיתי בוואטסאפ מה מפריע וממתי.\n\nתקבלו תשובה ישירות ממנו, בלי "
   "מזכירות ובלי התחייבות.",
   "שאלה על הכאב? כתבו לאיתי.", "כתבו לאיתי בוואטסאפ", "תשובה ישירות מהמטפל", people=True)
ad(20, "A5", "9:16", ["room", "bed"],
   P("After a session: a woman in her forties sitting up on the edge of the white covered treatment table, putting "
     "on her shoes, a small relaxed smile, the salt lamp and the rice paper screen behind, soft daylight.",
     room=True),
   "רפואה סינית<br>בכרמיאל.", "דיקור · כוסות רוח · תזונה",
   "איתי אלבז מטפל בכרמיאל בדיקור, בכוסות רוח ובייעוץ תזונה: כאבי גב וכתפיים, ברכיים, כאבי ראש ומיגרנות, בטן "
   "ושינה." + END,
   "רפואה סינית בכרמיאל.", "איתי אלבז, רפואה סינית", "דיקור · כוסות רוח · תזונה", people=True)

HERO_PROMPT = P("Hero photograph for a Chinese medicine clinic: the calm treatment room in soft morning light, the "
                "treatment table with a white cover and navy bolster and the rice paper folding screen on the left "
                "third of the frame, the salt lamp glowing warm. The right two thirds are the same calm light wall "
                "and soft window light, empty. No people.",
                "One continuous photograph, no borders, bands or panels.", room=True)
HERO_M_PROMPT = P("Vertical hero photograph for a Chinese medicine clinic: the calm treatment room, the white covered "
                  "table, navy bolster and the salt lamp in the lower half, above it the rice paper screen and the "
                  "same light wall with soft window light. No people.", room=True)

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "hero_m": HERO_M_PROMPT, "ref": REF}, sys.stdout,
              ensure_ascii=False, indent=1)
