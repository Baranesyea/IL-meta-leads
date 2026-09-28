"""Gali Ripui / גלי ריפוי (lead 2026-09-27-344): research, 5 angles, 20 ads — image prompts + Hebrew copy.

Private clinic in Ashkelon (בית פרנק, רחוב החלוץ 1), run by Dr. Michal Katzin (PhD, 20 years). Shockwave therapy
combined with electromagnetic pulses, for shoulder (calcification, limited movement), tennis elbow, knees, back and heel
spur. Recognised by insurance companies; discount for Leumit and Meuhedet members. WhatsApp 054-211-9121 (checked by
Eran 2026-09-28; she said she'd be glad to get the report).
Their ads: 3 active, all videos, only 2 texts: the same text runs since May 2025 (500+ days) and again since June 2026;
newest ad from 22 June. All buttons open Messenger, the headline has a typo ("לציאט"). One text lists five pains in one
line. Strongest facts (a doctor with 20 years, insurance coverage, HMO discount) sit at the end. Several lines are the
kind Meta restricts in health ads ("אין צורך לסבול", "ממוססים את הדלקת").
Clinic ads, so no product fidelity. The applicator of her shockwave device (reference frame from her video) appears
in the treatment shots. Dr. Michal is never faked: no face of a practitioner, only hands and forearms.
Copy: plural, never asserts the reader's condition, no promised results, no Latin letters, no dashes.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-27-344"

REF = {"device": "7fa69417-2bf7-4ced-9a31-522b00ef9892"}   # shockwave applicator on a shoulder (ad 1687756718851369)

STYLE = ("Premium healthcare advertising photograph, calm and bright: soft natural light, clean uncluttered spaces, "
         "white and soft sky blue tones with a small warm yellow accent, honest real people with real skin texture, "
         "shot on a full frame camera, shallow depth of field, photorealistic, editorial quality, not stock-looking. ")
RULES = ("No text, letters, logos, signs or watermarks anywhere. Anatomically correct hands and fingers. Nobody looks "
         "in pain in an exaggerated way; expressions are natural. The practitioner is never shown with a face: only "
         "hands and forearms, or from behind. ")
ONE = ("COMPOSITION: wide natural framing with open space above the subject. One single continuous photograph, no "
       "borders, no panels, no inset images, no split frame.")
ROOM = ("A bright modern private clinic room: white walls, one soft blue accent wall, a white treatment chair or "
        "table, and a compact medical shockwave device with a handheld applicator like in the reference photo. ")


def P(scene: str, air: str = ONE, room: bool = False) -> str:
    return STYLE + (ROOM if room else "") + scene + " " + air + " " + RULES


RESEARCH = {
    "one_liner": "מרפאה פרטית באשקלון לטיפול בכאבים אורתופדיים בגלי הלם ובפולסים אלקטרומגנטיים, בלי ניתוח ובלי "
                 "זריקות. בניהול ד\"ר מיכל קצין, עם 20 שנות ניסיון. מוכר בחברות הביטוח, והנחה לחברי לאומית ומאוחדת.",
    "hero_products": ["כתף: הסתיידות ומגבלת תנועה", "דורבן בעקב", "מרפק טניס", "ברכיים וגב"],
    "audience": [
        {"persona": "הכתף שלא עולה", "who": "45–70, נשים וגברים", "cares": "להרים יד, להתלבש, לישון על הצד, בלי ניתוח"},
        {"persona": "הצעד הראשון בבוקר", "who": "35–65, עומדים והולכים הרבה", "cares": "ללכת בלי לחשוב על העקב"},
        {"persona": "המרפק של העבודה", "who": "30–60, עבודה ידנית, מחשב, ספורט", "cares": "לאחוז, להרים, לעבוד"},
    ],
    "pains": ["\"הצעד הראשון בבוקר הוא הכי קשה\"", "\"אני לא מצליחה להרים את היד\"", "\"כואב לי להרים כוס\"",
              "\"אמרו לי שרק ניתוח\"", "\"לא רוצה עוד זריקה\""],
    "desires": ["לחזור לתנועה מלאה", "בלי ניתוח ובלי זריקות", "טיפול קצר וברור", "שהביטוח ישתתף"],
    "objections": ["\"זה כואב?\"", "\"כמה טיפולים צריך?\"", "\"כמה זה עולה?\"", "\"זה באמת בלי ניתוח?\""],
    "current_ads_audit": "3 מודעות פעילות, כולן סרטונים, ורק שני טקסטים. אותו טקסט רץ ממאי 2025 ושוב מיוני 2026, "
                         "והמודעה הכי חדשה עלתה ביוני. כל הכפתורים פותחים הודעה בפייסבוק, ובכותרת יש שגיאת כתיב. "
                         "הטקסט מונה חמישה כאבים במשפט אחד, והעובדות הכי חזקות (רופאה עם 20 שנות ניסיון, כיסוי "
                         "ביטוחי, הנחה לחברי קופה) מופיעות רק בסוף.",
    "gaps": ["אין מודעה נפרדת לכל כאב", "הכפתור למסנג'ר ולא לוואטסאפ", "שגיאת כתיב בכותרת",
             "ד\"ר מיכל, הביטוח וההנחה קבורים בסוף", "אותו טקסט רץ יותר משנה", "משפטים שמטא מגבילה במודעות בריאות"],
    "angles": [
        {"id": "A1", "name": "כתף", "idea": "הכתף שלא עולה עד הסוף: להתלבש, להסתרק, לישון על הצד.", "persona": "הכתף שלא עולה", "hook": "כשהיד לא עולה עד הסוף.", "why": "הסרטון על הכתף הוא הכי ממוקד שיש להם. מרחיבים אותו."},
        {"id": "A2", "name": "דורבן בעקב", "idea": "הצעד הראשון בבוקר, עמידה ארוכה, הליכה.", "persona": "הצעד הראשון בבוקר", "hook": "הצעד הראשון בבוקר.", "why": "כאב מאוד מוכר, שמי שיש לו מחפש פתרון בלי זריקה."},
        {"id": "A3", "name": "מרפק טניס", "idea": "לאחוז כוס, להרים שקית, לעבוד עם העכבר.", "persona": "המרפק של העבודה", "hook": "כשגם כוס קפה מרגישה כבדה.", "why": "קהל עובד וצעיר יותר, שעוד לא מכיר את הקליניקה."},
        {"id": "A4", "name": "ברכיים וגב", "idea": "הליכה, מדרגות, ים באשקלון.", "persona": "הכתף שלא עולה", "hook": "לרדת לים. ולעלות בחזרה.", "why": "מדבר על מה שחוזרים לעשות, בשפה של אשקלון."},
        {"id": "A5", "name": "ד\"ר מיכל, ביטוח, וואטסאפ", "idea": "רופאה עם 20 שנות ניסיון, מוכר בביטוח, הנחה לחברי קופה, ושאלה שנשלחת בוואטסאפ.", "persona": "כולם", "hook": "שאלה על הטיפול? כתבו לד\"ר מיכל.", "why": "מוריד את החשש מהמחיר ומהפנייה הראשונה."},
    ],
}

A = []
WA = "WhatsApp"


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta=WA, people=False):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=None, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=[], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


END = "\n\nכתבו לנו בוואטסאפ, וד\"ר מיכל קצין תחזור אליכם עם כל הפרטים."

# ---------- A1 כתף ----------
ad(1, "A1", "4:5", [],
   P("Morning in a bright bedroom: a woman in her fifties putting on a light cardigan, one arm going into the sleeve "
     "and stopping at shoulder height, her other hand holding the shoulder, calm thoughtful expression, soft window "
     "light, seen from the side."),
   "כשהיד לא עולה<br>עד הסוף.", "טיפול בכתף בגלי הלם · אשקלון",
   "ללבוש מעיל, להסתרק, להוריד משהו מהמדף. כשהכתף לא עולה עד הסוף, כל דבר קטן נהיה מסובך.\n\nבמרפאת גלי ריפוי "
   "באשקלון מטפלים בכתף בגלי הלם ובפולסים אלקטרומגנטיים, בלי ניתוח ובלי זריקות." + END,
   "כשהיד לא עולה עד הסוף.", "טיפול בכתף בלי ניתוח", "גלי הלם · אשקלון", people=True)
ad(2, "A1", "1:1", ["device"],
   P("Close-up in the clinic: a practitioner's hand holding the handheld shockwave applicator from the reference "
     "photo against the front of a patient's bare shoulder, the patient in a light blue top pulled aside, calm, soft "
     "daylight, white and soft blue background. Only the practitioner's hand and forearm are visible.", room=True),
   "הסתיידות בכתף.<br>בלי ניתוח ובלי זריקות.", "גלי הלם ופולסים אלקטרומגנטיים",
   "הסתיידות בכתף יכולה להגביל את התנועה ולהפריע לשינה.\n\nבמרפאת גלי ריפוי מטפלים בה בגלי הלם בשילוב פולסים "
   "אלקטרומגנטיים. טיפול קצר, בלי ניתוח, בלי זריקות ובלי תרופות." + END,
   "הסתיידות בכתף? בלי ניתוח ובלי זריקות.", "טיפול בהסתיידות בכתף", "גלי הלם באשקלון", people=True)
ad(3, "A1", "4:5", [],
   P("A man in his sixties reaching up to place a jar on a high kitchen shelf with an easy full arm movement, "
     "relaxed, bright kitchen with morning light, seen from the side."),
   "להגיע למדף העליון.<br>בלי לחשוב פעמיים.", "טיפול בכאבי כתף · אשקלון",
   "יש תנועות שעושים בלי לחשוב. עד שהכתף מתחילה להגביל.\n\nבמרפאת גלי ריפוי עובדים על החזרה לתנועה, בטיפול "
   "בגלי הלם שמוכר בחברות הביטוח." + END,
   "להגיע למדף העליון, בלי לחשוב פעמיים.", "טיפול בכאבי כתף", "מוכר בחברות הביטוח", people=True)
ad(4, "A1", "9:16", [],
   P("Night in a calm bedroom with soft bedside lamp light: a woman in her fifties asleep peacefully on her side, "
     "white linen, relaxed face, warm and quiet."),
   "לישון על הצד.<br>כל הלילה.", "טיפול בכתף בגלי הלם",
   "כשהכתף כואבת, גם הלילה נהיה קצר.\n\nד\"ר מיכל קצין, עם 20 שנות ניסיון, מטפלת בכאבי כתף במרפאת גלי ריפוי "
   "באשקלון." + END,
   "לישון על הצד, כל הלילה.", "טיפול בכאבי כתף", "ד\"ר מיכל קצין · אשקלון", people=True)

# ---------- A2 דורבן בעקב ----------
ad(5, "A2", "4:5", [],
   P("Early morning: bare feet stepping down from a bed onto a light wooden floor, soft sunlight across the floor, "
     "white linen hanging from the bed, close and calm, only feet and lower legs visible."),
   "הצעד הראשון<br>בבוקר.", "טיפול בדורבן בעקב · אשקלון",
   "מי שיש לו דורבן מכיר את הרגע הזה: הצעד הראשון מהמיטה.\n\nבמרפאת גלי ריפוי מטפלים בדורבן בעקב בגלי הלם, בלי "
   "זריקות ובלי ניתוח, בסדרת טיפולים קצרה." + END,
   "הצעד הראשון בבוקר.", "טיפול בדורבן בעקב", "בלי זריקות ובלי ניתוח", people=True)
ad(6, "A2", "1:1", ["device"],
   P("Close-up in the clinic: a patient's bare foot resting on a white padded support, a practitioner's hand holding "
     "the handheld shockwave applicator from the reference photo against the heel, soft daylight, white and soft blue "
     "tones. Only the practitioner's hand and forearm are visible.", room=True),
   "דורבן בעקב.<br>טיפול בלי זריקה.", "גלי הלם · מרפאת גלי ריפוי",
   "גלי הלם הם אחד הטיפולים המוכרים לדורבן בעקב, בלי זריקה ובלי ניתוח.\n\n"
   "המרפאה באשקלון, בבית פרנק." + END,
   "דורבן בעקב? טיפול בלי זריקה.", "טיפול בדורבן בגלי הלם", "מרפאת גלי ריפוי · אשקלון", people=True)
ad(7, "A2", "4:5", [],
   P("A woman in her forties walking barefoot on the wet sand at the edge of the sea at sunrise, easy relaxed steps, "
     "soft golden light, seen from the side at a distance, Mediterranean beach."),
   "ללכת על החוף.<br>בלי לספור צעדים.", "טיפול בדורבן · אשקלון",
   "הליכה של בוקר על החוף באשקלון, בלי לחשוב על העקב.\n\nלשם מכוון הטיפול בגלי ריפוי: סדרה קצרה של טיפולים "
   "בגלי הלם, בלי זריקות." + END,
   "ללכת על החוף, בלי לספור צעדים.", "טיפול בדורבן בעקב", "גלי הלם באשקלון", people=True)
ad(8, "A2", "9:16", [],
   P("A woman in her fifties, a nurse or shop worker, standing at the end of a long shift, leaning lightly on a "
     "counter and shifting her weight off one foot, calm tired expression, soft warm light, seen from the side."),
   "עומדים כל היום.<br>והעקב מרגיש הכול.", "טיפול בדורבן בעקב",
   "עבודה בעמידה, משמרת ארוכה, ובסוף היום העקב מרגיש כל צעד.\n\nבמרפאת גלי ריפוי מטפלים בדורבן בגלי הלם, "
   "והטיפול מוכר בחברות הביטוח." + END,
   "עומדים כל היום, והעקב מרגיש הכול.", "טיפול בדורבן", "מוכר בחברות הביטוח", people=True)

# ---------- A3 מרפק טניס ----------
ad(9, "A3", "4:5", [],
   P("A man in his forties at a kitchen counter lifting a mug of coffee with one hand, the other hand holding his "
     "forearm just below the elbow, calm expression, bright morning light, seen from the side."),
   "כשגם כוס קפה<br>מרגישה כבדה.", "טיפול במרפק טניס · אשקלון",
   "מרפק טניס לא שייך רק לטניס. הוא מגיע מעבודה עם הידיים, ממחשב, מכלים ומהרמות.\n\nבמרפאת גלי ריפוי מטפלים "
   "בו בגלי הלם, בלי ניתוח ובלי זריקות." + END,
   "כשגם כוס קפה מרגישה כבדה.", "טיפול במרפק טניס", "גלי הלם · אשקלון", people=True)
ad(10, "A3", "1:1", ["device"],
   P("Close-up in the clinic: a patient's forearm resting on a white padded armrest, a practitioner's hand holding "
     "the handheld shockwave applicator from the reference photo against the outer side of the elbow, soft daylight, "
     "white and soft blue tones. Only the practitioner's hand and forearm are visible.", room=True),
   "מרפק טניס.<br>טיפול קצר, בלי ניתוח.", "גלי הלם ופולסים אלקטרומגנטיים",
   "במרפאת גלי ריפוי מטפלים במרפק טניס בגלי הלם ובפולסים אלקטרומגנטיים, בלי ניתוח ובלי זריקות.\n\nד\"ר מיכל "
   "קצין מסבירה כל שלב לפני שמתחילים." + END,
   "מרפק טניס? טיפול קצר, בלי ניתוח.", "טיפול במרפק טניס", "ד\"ר מיכל קצין", people=True)
ad(11, "A3", "4:5", [],
   P("A man in his thirties, a craftsman, working with a hand tool at a wooden workbench, strong forearms, focused "
     "calm face, warm workshop light, seen from the side."),
   "הידיים הן העבודה.<br>והמרפק צריך להחזיק.", "טיפול במרפק טניס",
   "נגרים, טכנאים, ספרים, מי שעובד עם הידיים כל יום. המרפק סוחב את כל העבודה.\n\nבמרפאת גלי ריפוי באשקלון מטפלים "
   "במרפק טניס בגלי הלם." + END,
   "הידיים הן העבודה.", "טיפול במרפק טניס", "גלי הלם באשקלון", people=True)
ad(12, "A3", "9:16", [],
   P("A woman in her fifties playing padel on an outdoor court on a sunny morning, mid swing, relaxed and smiling, "
     "blue court and sky, seen from the side at a distance."),
   "לחזור למגרש.<br>בלי לוותר על המכה.", "טיפול במרפק טניס · אשקלון",
   "טניס, פאדל, או סתם משחק עם הילדים. מרפק טניס לא צריך לעצור את זה.\n\nבמרפאת גלי ריפוי מטפלים בו בגלי הלם, "
   "בסדרת טיפולים קצרה." + END,
   "לחזור למגרש, בלי לוותר על המכה.", "טיפול במרפק טניס", "סדרת טיפולים קצרה", people=True)

# ---------- A4 ברכיים וגב ----------
ad(13, "A4", "4:5", [],
   P("A couple in their sixties walking down a wide promenade toward the sea in Ashkelon at golden hour, relaxed easy "
     "steps, seen from behind at a distance, palm trees and the Mediterranean ahead."),
   "לרדת לים.<br>ולעלות בחזרה.", "טיפול בברכיים ובגב · אשקלון",
   "הטיילת, המדרגות לחוף, והדרך חזרה.\n\nבמרפאת גלי ריפוי מטפלים בכאבי ברכיים וגב בגלי הלם ובפולסים "
   "אלקטרומגנטיים, בלי ניתוח ובלי זריקות." + END,
   "לרדת לים, ולעלות בחזרה.", "טיפול בכאבי ברכיים", "גלי הלם באשקלון", people=True)
ad(14, "A4", "1:1", ["device"],
   P("Close-up in the clinic: a patient sitting on a white treatment table in rolled up light trousers, a "
     "practitioner's hand holding the handheld shockwave applicator from the reference photo against the side of the "
     "knee, soft daylight, white and soft blue tones. Only the practitioner's hand and forearm are visible.",
     room=True),
   "כאבי ברכיים.<br>בלי ניתוח ובלי זריקות.", "גלי הלם · אשקלון",
   "כשהברך מתחילה להגביל, הרבה אנשים שומעים שהפתרון הוא זריקה או ניתוח.\n\nבמרפאת גלי ריפוי יש עוד דרך לבדוק: "
   "טיפול בגלי הלם, שמוכר בחברות הביטוח." + END,
   "כאבי ברכיים? בלי ניתוח ובלי זריקות.", "טיפול בכאבי ברכיים", "מוכר בחברות הביטוח", people=True)
ad(15, "A4", "4:5", [],
   P("A grandmother in her sixties climbing a few outdoor stone steps holding the hand of her five year old "
     "granddaughter, both smiling, warm afternoon light, a garden path, seen from the side."),
   "מדרגות עם הנכדה.<br>בקצב שלה.", "טיפול בכאבי ברכיים",
   "מדרגות, גן שעשועים, טיול קצר. דברים פשוטים שברך כואבת יכולה לקחת.\n\nבמרפאת גלי ריפוי מטפלים בכאבי ברכיים, "
   "בניהול ד\"ר מיכל קצין." + END,
   "מדרגות עם הנכדה, בקצב שלה.", "טיפול בכאבי ברכיים", "ד\"ר מיכל קצין · אשקלון", people=True)
ad(16, "A4", "9:16", [],
   P("A man in his fifties gardening, bending down easily to pick a basket of tomatoes in a sunny home garden, "
     "relaxed posture, warm morning light, seen from the side."),
   "להתכופף בגינה.<br>ולהזדקף בלי לחשוב.", "טיפול בכאבי גב · אשקלון",
   "להתכופף, להרים, להזדקף. תנועות של כל יום שגב כואב הופך לפרויקט.\n\nבמרפאת גלי ריפוי מטפלים בכאבי גב בגלי "
   "הלם ובפולסים אלקטרומגנטיים." + END,
   "להתכופף בגינה, ולהזדקף בלי לחשוב.", "טיפול בכאבי גב", "גלי הלם באשקלון", people=True)

# ---------- A5 ד"ר מיכל, ביטוח, וואטסאפ ----------
ad(17, "A5", "4:5", ["device"],
   P("The clinic treatment room itself, empty and ready: a white padded treatment table, the compact shockwave device "
     "with its handheld applicator from the reference photo on a small cart, white walls and one soft blue accent "
     "wall, a plant, soft morning light through a window. No people.", room=True),
   "מרפאה פרטית<br>באשקלון.", "ד\"ר מיכל קצין · 20 שנות ניסיון",
   "גלי ריפוי היא מרפאה פרטית לטיפול בכאבים אורתופדיים, בבית פרנק באשקלון. ד\"ר מיכל קצין מנהלת אותה, עם 20 "
   "שנות ניסיון.\n\nכתף, דורבן, מרפק טניס, ברכיים וגב, בגלי הלם ובפולסים אלקטרומגנטיים." + END,
   "מרפאה פרטית באשקלון.", "גלי ריפוי, ד\"ר מיכל קצין", "20 שנות ניסיון")
ad(18, "A5", "1:1", [],
   P("On a clean white desk in a bright clinic: a folded insurance form, a pen and a pair of glasses next to a small "
     "plant, soft daylight, calm and orderly, shallow depth of field. No people, no readable text."),
   "מוכר בחברות<br>הביטוח.", "הנחה לחברי לאומית ומאוחדת",
   "הטיפול בגלי ריפוי פרטי, אבל מוכר בחברות הביטוח ומכוסה לפי תנאי הפוליסה. ולחברי לאומית ומאוחדת יש הנחה.\n\n"
   "כתבו לנו ונבדוק יחד מה מגיע לכם." + END,
   "מוכר בחברות הביטוח.", "כיסוי ביטוחי והנחה לחברי קופה", "לאומית ומאוחדת")
ad(19, "A5", "4:5", [],
   P("Close-up of a woman's hand holding a smartphone above a white table next to a cup of tea, the phone screen "
     "shows a blurred generic chat app with green bubbles and no readable text, soft morning window light, a plant in "
     "the soft background."),
   "שאלה על הטיפול?<br>כתבו לד\"ר מיכל.", "תשובה בוואטסאפ",
   "לא בטוחים אם גלי הלם מתאימים לכם? כתבו לנו בוואטסאפ מה כואב וממתי.\n\nד\"ר מיכל קצין תחזור אליכם עם תשובה, "
   "בלי התחייבות.",
   "שאלה על הטיפול? כתבו לד\"ר מיכל.", "כתבו לנו בוואטסאפ", "תשובה ישירות מהמרפאה", people=True)
ad(20, "A5", "9:16", ["device"],
   P("After a session in the bright clinic: a woman in her fifties sitting on the edge of the white treatment table, "
     "raising her arm fully above her head with a small relieved smile, the shockwave device from the reference photo "
     "in the soft background, white and soft blue tones, soft daylight.", room=True),
   "בלי ניתוח.<br>בלי זריקות.<br>בלי כדורים.", "גלי ריפוי · אשקלון",
   "גלי הלם בשילוב פולסים אלקטרומגנטיים, בסדרת טיפולים קצרה, במרפאה פרטית באשקלון.\n\nכתף, דורבן, מרפק טניס, "
   "ברכיים וגב." + END,
   "בלי ניתוח, בלי זריקות, בלי כדורים.", "גלי ריפוי, אשקלון", "גלי הלם ופולסים אלקטרומגנטיים", people=True)

# Desktop hero sits in a tall frame (about 4:5): generate at 4:5 with the subject filling it (NOTES, 2026-09-28).
HERO_PROMPT = P("Hero photograph for a private shockwave therapy clinic, close framing: a woman in her fifties sitting on "
                "a white treatment table in a light top, a practitioner's hand holding the handheld shockwave "
                "applicator from the reference photo against her shoulder, the device beside them, white walls and a "
                "soft blue accent wall, bright soft daylight. The treatment fills the frame, subject in the middle and "
                "lower part. Only the practitioner's hand and forearm are visible.",
                "One continuous photograph, no borders, bands or panels.", room=True)
HERO_M_PROMPT = P("Vertical hero photograph for a private shockwave therapy clinic: a woman in her fifties sitting on a "
                  "white treatment table, a practitioner's hand holding the handheld shockwave applicator from the "
                  "reference photo against her shoulder, the device beside them, in the lower 60 percent of the frame; "
                  "above them the calm white and soft blue wall. Only the practitioner's hand and forearm are visible.",
                  room=True)

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "hero_m": HERO_M_PROMPT, "ref": REF}, sys.stdout,
              ensure_ascii=False, indent=1)
