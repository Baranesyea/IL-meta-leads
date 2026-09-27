"""Kalahari Rose Israel (lead 2026-09-25-002): research, 5 angles, 20 ads — image prompts + Hebrew copy.

Israeli store of a US natural-skincare brand (WooCommerce, 13 products): face creams by skin type (Revitalise for
oily/combination, Hydrate for dry/sensitive, Luxury for mature, ₪119), serums (Whisper, Royal, ₪127), Renewal eye
cream (₪79), Luscious body cream (₪280), kits (₪192–743). 100% natural ingredients, Ministry of Health licensed,
free shipping over ₪300. Black glass jars with a gold star mark.
Their ads: three versions of one new Sukkot video campaign (20% off the whole site until 4.10), two UGC talking-head
videos and one packshot — all to the home page. Two days old: the account had no running ads before it.
Visual direction (new in the set): warm desert botanical — Kalahari dunes and sandstone at golden hour, dried desert
flowers and rose petals, blush and terracotta, the black-and-gold jars glowing against warm sand.
Ad copy in feminine singular (their site speaks to "את"). Meta policy: no medical or "anti-aging results" promises,
no "do you have wrinkles?" — talk about the product and the ritual.
"""
import json
import sys

sys.path.insert(0, ".")

LID = "2026-09-25-002"

REF = {
    "whisper": "5be2e7e0-7da8-4fef-a645-9cff2e48f532",     # Whisper face serum, black dropper bottle, ₪127
    "royal": "2b7695af-de62-4946-850c-abb688c6895d",       # Royal face serum, black dropper bottle, ₪127
    "revitalise": "a733286b-8eee-48c6-9692-b897e29b1c13",  # Revitalise face cream (oily/combination), black jar, ₪119
    "hydrate": "e93ba8f7-2c3e-4c6e-afba-c2cba2da7527",     # Hydrate face cream (dry/sensitive), black jar, ₪119
    "luxury": "a5a28163-2783-4f50-8c42-a4d6e3046068",      # Luxury face cream (mature skin), black jar, ₪119
    "renewal": "5a815f17-ef12-4c72-bf74-d9a4718fc48b",     # Renewal eye cream, small black jar, ₪79
    "luscious": "72af0433-e184-4dbd-83d2-8949c4ca106c",    # Luscious body cream, large black jar, ₪280
    "glow_kit": "248e10a1-df8b-4c00-92ad-7497555d4836",    # Glow Essentials: face cream + serum set, ₪559
}

STYLE = ("Premium natural-skincare advertising photograph, warm desert botanical: golden-hour sunlight over soft sand "
         "and sandstone, dried desert flowers, pale rose petals, blush and terracotta tones, the black glass jars and "
         "bottles glowing against warm sand, creamy product textures, shallow depth of field, shot on medium format, "
         "photorealistic, magazine quality. ")
FIDELITY = ("Products must be exact matches of the reference photos: black glass jars and dropper bottles with the same "
            "gold label layout and star mark — do not redesign them and do not add or change any text on them. No other "
            "text, signage, watermarks or logos anywhere. People look natural, real skin texture, anatomically correct "
            "hands. ")
TOP = ("COMPOSITION: the subject sits in the lower 60% of the frame; above it the same soft background simply continues, "
       "calm and empty — no objects, edges or lines. One continuous photograph — no borders, bands, panels or split "
       "frames.")


def P(scene: str, air: str = TOP) -> str:
    return STYLE + scene + " " + air + " " + FIDELITY


RESEARCH = {
    "one_liner": "הזרוע הישראלית של מותג טיפוח טבעי אמריקאי: קרמי פנים לפי סוג עור, סרומים, קרם עיניים וקרם גוף, "
                 "100% רכיבים טבעיים וברישיון משרד הבריאות. ₪79–743, משלוח חינם מעל ₪300. מיצוב: טיפוח טבעי-יוקרתי "
                 "שמותאם לסוג העור.",
    "hero_products": ["קרמי פנים Revitalise / Hydrate / Luxury — ₪119", "סרומים Whisper ו-Royal — ₪127",
                      "קרם עיניים Renewal — ₪79", "קרם גוף Luscious — ₪280", "ערכות — ₪192–743"],
    "audience": [
        {"persona": "הטבעית", "who": "נשים 28–50", "cares": "טיפוח בלי רכיבים שהיא לא מכירה"},
        {"persona": "העור הבוגר", "who": "נשים 40–60", "cares": "עור רך ומלא, שגרה פשוטה שעובדת"},
        {"persona": "מחפשת המתנה", "who": "25–55", "cares": "מתנת טיפוח יפה שנראית יוקרתית"},
    ],
    "pains": ["\"אני לא יודעת איזה קרם מתאים לעור שלי\"", "\"הקרמים בפארם מלאים ברכיבים שאני לא מבינה\"",
              "\"העור שלי יבש ורגיש\"", "\"טבעי זה בדרך כלל לא מרגיש יוקרתי\""],
    "desires": ["עור רך וזוהר", "שגרה פשוטה", "טבעי שמרגיש יוקרתי", "מתנה שעושה רושם"],
    "objections": ["\"לא מכירה את המותג\"", "\"זה באמת טבעי?\"", "מחיר", "\"איזה מוצר לבחור\""],
    "current_ads_audit": "שלוש מודעות, כולן גרסאות של קמפיין סוכות חדש (20% הנחה עד 4.10) שעלה לפני יומיים: שני סרטוני UGC של "
                         "נשים שמדברות למצלמה ומודעת מוצר אחת. לפני זה לא רצו מודעות בכלל, אז אין עדיין נתונים על מה עובד. "
                         "כל השלוש מובילות לדף הבית, והמבחן הכי חשוב של המותג, קרם לפי סוג עור, לא מופיע באף אחת.",
    "gaps": ["המותג לא מוכר, ואין מודעה שמציגה אותו", "ההתאמה לסוג העור, היתרון הכי ברור, לא מופיעה",
             "אין ויזואל פרימיום אחד, למרות אריזות שחור-זהב יפות", "הסיפור של קלהרי, המדבר והרכיבים הטבעיים, לא מסופר",
             "כל המודעות מובילות לדף הבית"],
    "angles": [
        {"id": "A1", "name": "הקרם של העור שלך", "idea": "שלושה קרמים לשלושה סוגי עור: שומני ומעורב, יבש ורגיש, בוגר. בוחרים את שלך.", "persona": "הטבעית", "hook": "יש לך עור יבש? זה הקרם שלך.", "why": "עונה ישירות על ההתלבטות הכי גדולה, ומוביל לעמוד מוצר."},
        {"id": "A2", "name": "טיפות של זהב", "idea": "הסרומים Whisper ו-Royal: כמה טיפות בבוקר ובערב, שמן טבעי שנספג מהר.", "persona": "העור הבוגר", "hook": "שלוש טיפות. זה כל הטקס.", "why": "מוצר ויזואלי מאוד וקל להבנה."},
        {"id": "A3", "name": "העיניים", "idea": "Renewal, קרם עיניים טבעי ב-79 ש״ח: הכניסה הכי קלה למותג.", "persona": "הטבעית", "hook": "המקום הכי עדין בפנים. מגיע לו הכי טבעי.", "why": "מחיר כניסה נמוך למותג לא מוכר."},
        {"id": "A4", "name": "הגוף", "idea": "Luscious, קרם גוף עשיר ליובש חריף: טיפוח פנים, לכל הגוף.", "persona": "העור הבוגר", "hook": "העור שלך צמא? הנה המים.", "why": "סל גבוה ומוצר עם כאב ברור."},
        {"id": "A5", "name": "מהמדבר, בטבעיות", "idea": "המותג עצמו: מותג אמריקאי עם 100% רכיבים טבעיים, ברישיון משרד הבריאות, עכשיו בישראל. ערכות ומתנות.", "persona": "מחפשת המתנה", "hook": "טבעי. אמיתי. סוף סוף בישראל.", "why": "בונה אמון במותג לא מוכר."},
    ],
}

A = []


def ad(n, angle, fmt, refs, prompt, overlay, sub, primary, short, headline, desc, cta="Shop Now", people=False):
    A.append(dict(ad_no=n, angle_id=angle, format=fmt, refs=refs, prompt=prompt, overlay=overlay, overlay_sub=sub,
                  note=None, primary_text=primary, alt_texts=[short], headline=headline, description=desc,
                  cta=cta, has_people=people, to_verify=[], layout={},
                  image=f"ads/ad_{n:02d}.png", image_raw=f"ads_raw/ad_{n:02d}.png"))


# ---------- A1 הקרם של העור שלך ----------
ad(1, "A1", "4:5", ["revitalise", "hydrate", "luxury"],
   P("The three black face-cream jars from the references (Revitalise, Hydrate, Luxury) standing in a row on a warm "
     "sandstone ledge at golden hour, soft sand around them, a few dried desert flowers, long warm shadows."),
   "שלושה סוגי עור.<br>שלושה קרמים.", "קרמי פנים טבעיים · 119 ש״ח",
   "עור שומני ומעורב, יבש ורגיש, או בוגר? לכל אחד יש קרם משלו.\n\nקרמי פנים עם 100% רכיבים טבעיים, 119 ש״ח לקרם.",
   "שלושה סוגי עור. שלושה קרמים.", "קרמי פנים לפי סוג עור", "119 ש״ח")
ad(2, "A1", "4:5", ["hydrate"],
   P("The black Hydrate face-cream jar from the reference, lid off, on soft pale sand at golden hour, a generous swirl "
     "of rich cream on a smooth stone beside it, pale rose petals, warm light."),
   "עור יבש ורגיש?<br>זה הקרם שלך.", "הידרייט · 119 ש״ח",
   "קרם עשיר ועוטף לעור יבש ורגיש, מרכיבים טבעיים בלבד.\n\nנספג בנעימות ומשאיר תחושה רכה. 119 ש״ח.",
   "עור יבש ורגיש? זה הקרם שלך.", "קרם Hydrate", "119 ש״ח")
ad(3, "A1", "1:1", ["revitalise"],
   P("The black Revitalise face-cream jar from the reference on a pale sandstone slab in crisp golden light, a light "
     "whipped swirl of cream beside it, a sprig of dried desert grass."),
   "קליל. טבעי.<br>לעור שומני.", "ריווייטלייז · 119 ש״ח",
   "קרם קליל לעור שומני ומעורב, שנספג מהר.\n\n100% רכיבים טבעיים, 119 ש״ח.",
   "קליל וטבעי, לעור שומני.", "קרם Revitalise", "119 ש״ח")
ad(4, "A1", "4:5", ["luxury"],
   P("A woman in her fifties with natural glowing skin and soft silver-streaked hair, seen in profile in warm golden "
     "light, gently touching her cheek; the black Luxury face-cream jar from the reference on a sandstone ledge in the "
     "foreground. She fills the right half; the left half is warm plain wall."),
   "העור שלך השתנה.<br>גם הקרם צריך.", "לאקשרי לעור בוגר · 119 ש״ח",
   "קרם עשיר במיוחד לעור בוגר, מרכיבים טבעיים שהעור מכיר.\n\nחלק מהשגרה של הבוקר והערב. 119 ש״ח.",
   "העור שלך השתנה. גם הקרם צריך.", "קרם Luxury", "119 ש״ח", people=True)

# ---------- A2 טיפות של זהב ----------
ad(5, "A2", "4:5", ["whisper"],
   P("The black Whisper serum dropper bottle from the reference standing on warm sandstone at golden hour, a single "
     "golden drop falling from its glass dropper held just above, warm backlight glowing through the oil."),
   "שלוש טיפות.<br>זה כל הטקס.", "סרום ויספר · 127 ש״ח",
   "שלוש טיפות בבוקר, שלוש בערב. שמן טבעי קליל שנספג מהר.\n\nסרום Whisper, 127 ש״ח.",
   "שלוש טיפות. זה כל הטקס.", "סרום Whisper", "127 ש״ח")
ad(6, "A2", "1:1", ["royal"],
   P("The black Royal serum dropper bottle from the reference lying on its side on pale sand, a small pool of golden "
     "serum glowing beside the dropper, dried rose petals, warm golden light."),
   "זהב נוזלי.<br>לעור שלך.", "סרום רויאל · 127 ש״ח",
   "סרום Royal עשיר ומזין, לעור שצריך עוד קצת.\n\n127 ש״ח, 100% רכיבים טבעיים.",
   "זהב נוזלי, לעור שלך.", "סרום Royal", "127 ש״ח")
ad(7, "A2", "4:5", ["whisper"],
   P("Close-up of a woman's open palm with three golden serum drops on it, soft natural skin, golden-hour light; the "
     "black Whisper serum bottle from the reference stands on a sandstone ledge beside her hand. Only the hand visible."),
   "טבעי שמרגישים<br>מהטיפה הראשונה.", "סרומים · 127 ש״ח",
   "שמן טבעי, קליל ונספג, שהעור מרגיש מהרגע הראשון.\n\nסרום Whisper או Royal, 127 ש״ח.",
   "טבעי שמרגישים מהטיפה הראשונה.", "סרומים טבעיים", "127 ש״ח", people=True)
ad(8, "A2", "9:16", ["whisper", "royal"],
   P("The two black serum dropper bottles from the references (Whisper and Royal) standing on a sculpted sand dune "
     "ridge at golden hour, long soft shadows, warm glowing sky behind, a few dried desert flowers."),
   "שני סרומים.<br>שני עולמות.", "ויספר · רויאל",
   "Whisper הקליל ליום, Royal העשיר ללילה.\n\nכל סרום 127 ש״ח, משלוח חינם מעל 300.",
   "שני סרומים, שני עולמות.", "סרומים טבעיים", "127 ש״ח")

# ---------- A3 העיניים ----------
ad(9, "A3", "4:5", ["renewal"],
   P("The small black Renewal eye-cream jar from the reference, lid off, on a smooth pale stone in soft golden light, "
     "a tiny dab of cream on the stone beside it, dried rose petals."),
   "המקום הכי עדין.<br>מגיע לו הכי טבעי.", "רניואל · 79 ש״ח",
   "העור סביב העיניים הוא הכי דק בפנים. מגיע לו קרם עדין וטבעי.\n\nקרם עיניים Renewal, 79 ש״ח.",
   "המקום הכי עדין. מגיע לו הכי טבעי.", "קרם עיניים Renewal", "79 ש״ח")
ad(10, "A3", "1:1", ["renewal"],
   P("A woman's ring finger gently dabbing a tiny amount of cream under her eye, soft natural skin with real texture, "
     "eyes closed, warm golden light; the small black Renewal jar from the reference in the lower foreground. Close "
     "crop of one eye and cheek."),
   "טפיחה אחת<br>בבוקר.", "קרם עיניים · 79 ש״ח",
   "טופחים בעדינות באצבע הקמיצה, בבוקר ובערב.\n\nRenewal, קרם עיניים טבעי, 79 ש״ח.",
   "טפיחה אחת בבוקר.", "קרם עיניים", "79 ש״ח", people=True)
ad(11, "A3", "4:5", ["renewal", "whisper"],
   P("The small black Renewal eye-cream jar and the black Whisper serum bottle from the references side by side on a "
     "warm sandstone ledge at golden hour, soft sand, a dried desert flower."),
   "הכרות עם<br>קלהרי רוז.", "מתחילות מ-79 ש״ח",
   "רוצה להכיר את המותג? קרם העיניים הוא ההתחלה הכי קלה.\n\n79 ש״ח, ומשלוח חינם בהזמנה מעל 300.",
   "הכרות עם קלהרי רוז.", "להתחיל מקרם העיניים", "79 ש״ח")
ad(12, "A3", "9:16", ["renewal"],
   P("The small black Renewal eye-cream jar from the reference resting on a sculpted sand ripple at golden hour, long "
     "shadow, warm glowing sky above, pale rose petals scattered on the sand."),
   "קטן בגודל.<br>גדול בטיפוח.", "רניואל · 79 ש״ח",
   "צנצנת קטנה של קרם עיניים טבעי, לבוקר ולערב.\n\n79 ש״ח.",
   "קטן בגודל, גדול בטיפוח.", "קרם עיניים", "79 ש״ח")

# ---------- A4 הגוף ----------
ad(13, "A4", "4:5", ["luscious"],
   P("The large black Luscious body-cream jar from the reference, lid off, on warm sandstone at golden hour, a thick "
     "luxurious swirl of body cream beside it, dried desert flowers, warm light."),
   "העור שלך צמא?<br>הנה המים.", "לושס · 280 ש״ח",
   "קרם גוף עשיר לעור יבש מאוד, מרכיבים טבעיים בלבד.\n\nמורחים אחרי המקלחת, והעור מרגיש רך ועטוף. 280 ש״ח.",
   "העור שלך צמא? הנה המים.", "קרם גוף Luscious", "280 ש״ח")
ad(14, "A4", "1:1", ["luscious"],
   P("A woman's sun-kissed shoulder and arm in soft golden light, a smooth sheen of body cream on her skin, wrapped "
     "in a blush linen towel; the large black Luscious jar from the reference on a stone ledge beside her. Face out of "
     "frame."),
   "טיפוח פנים.<br>לכל הגוף.", "קרם גוף · 280 ש״ח",
   "הגוף מגיע לאותו טיפוח כמו הפנים.\n\nLuscious, קרם גוף טיפולי טבעי, 280 ש״ח.",
   "טיפוח פנים, לכל הגוף.", "קרם גוף", "280 ש״ח", people=True)
ad(15, "A4", "4:5", ["luscious", "hydrate"],
   P("The large black Luscious body-cream jar and the black Hydrate face-cream jar from the references on a blush "
     "linen towel over warm sandstone, golden-hour light, dried rose petals."),
   "מהפנים<br>ועד הרגליים.", "הידרייט · לושס",
   "קרם פנים לעור יבש וקרם גוף עשיר. כל מה שעור יבש צריך.\n\nמשלוח חינם מעל 300 ש״ח.",
   "מהפנים ועד הרגליים.", "פנים וגוף", "משלוח חינם מעל 300")
ad(16, "A4", "4:5", ["luscious"],
   P("The large black Luscious body-cream jar from the reference standing on a sand dune crest at golden hour, soft "
     "wind ripples in the sand, warm glowing sky, the jar catching the last light."),
   "יובש של מדבר?<br>יש לזה תשובה.", "לושס · 280 ש״ח",
   "קרם גוף עשיר, לעור שצמא לחות.\n\n280 ש״ח, 100% רכיבים טבעיים.",
   "יובש של מדבר? יש לזה תשובה.", "קרם גוף Luscious", "280 ש״ח")

# ---------- A5 מהמדבר, בטבעיות ----------
ad(17, "A5", "4:5", ["glow_kit"],
   P("The Glow Essentials set from the reference (black face-cream jar and serum bottle) arranged on a warm sandstone "
     "plinth at golden hour, soft sand, dried desert flowers and pale rose petals, long warm shadows."),
   "טבעי. אמיתי.<br>סוף סוף בישראל.", "קלהרי רוז",
   "מותג טיפוח אמריקאי עם 100% רכיבים טבעיים, ברישיון משרד הבריאות, עכשיו גם בישראל.\n\nמשלוח חינם מעל 300 ש״ח.",
   "טבעי. אמיתי. סוף סוף בישראל.", "קלהרי רוז", "משלוח חינם מעל 300")
ad(18, "A5", "1:1", ["revitalise", "whisper", "renewal", "luscious"],
   P("Four black-and-gold products from the references (a face-cream jar, a serum dropper bottle, the small eye-cream "
     "jar and the large body-cream jar) arranged on a warm sandstone slab at golden hour, soft sand, dried flowers."),
   "רק מה<br>שהטבע נותן.", "100% רכיבים טבעיים",
   "בלי רכיבים שאי אפשר לבטא. רק רכיבים מהטבע.\n\nקלהרי רוז, מ-79 ש״ח.",
   "רק מה שהטבע נותן.", "קוסמטיקה טבעית", "מ-79 ש״ח")
ad(19, "A5", "4:5", ["glow_kit"],
   P("Hands tying a blush silk ribbon around a sand-coloured gift box on a sunlit linen table, the black face-cream "
     "jar and serum bottle of the Glow Essentials set from the reference inside, dried rose petals. Only hands visible."),
   "מתנה שמרגישה<br>יוקרה.", "ערכות מתנה · מ-192 ש״ח",
   "ערכות טיפוח טבעיות באריזה שחור-זהב, מוכנות למתנה.\n\nמ-192 ש״ח, משלוח חינם מעל 300.",
   "מתנה שמרגישה יוקרה.", "ערכות מתנה", "מ-192 ש״ח", people=True)
ad(20, "A5", "9:16", ["glow_kit", "luscious"],
   P("The Glow Essentials set and the large Luscious body-cream jar from the references standing on sculpted sandstone "
     "in a warm desert canyon at golden hour, soft light glowing on the black-and-gold labels, dried desert flowers."),
   "השגרה שלך.<br>מהטבע.", "משלוח חינם מעל 300 ש״ח",
   "פנים, עיניים וגוף. שגרה שלמה מרכיבים טבעיים בלבד.\n\nמשלוח חינם מעל 300 ש״ח.",
   "השגרה שלך, מהטבע.", "קלהרי רוז", "משלוח חינם מעל 300")

HERO_PROMPT = P("Hero campaign photograph for a natural skincare brand: the black Glow Essentials cream jar and serum "
                "bottle and the large Luscious body-cream jar from the references standing on a sculpted sandstone "
                "ledge in the Kalahari desert at golden hour, soft dunes behind, dried desert flowers and pale rose "
                "petals, warm glowing light. The products sit in the lower 55% of the frame on the left half; above "
                "and to the right the warm sand and sky continue, calm and empty.",
                "One continuous photograph — no borders, bands or panels.")
HERO_M_PROMPT = P("Hero campaign photograph for a natural skincare brand: the black Glow Essentials cream jar and serum "
                  "bottle from the reference standing on a sculpted sandstone ledge in the desert at golden hour, soft "
                  "dunes behind, dried desert flowers. The products sit in the lower 45% of the frame, centred; the top "
                  "half is warm glowing sky over the dunes, calm and empty.",
                  "One continuous photograph — no borders, bands or panels.")

if __name__ == "__main__":
    json.dump({"research": RESEARCH, "ads": A, "hero": HERO_PROMPT, "hero_m": HERO_M_PROMPT, "ref": REF}, sys.stdout,
              ensure_ascii=False, indent=1)
