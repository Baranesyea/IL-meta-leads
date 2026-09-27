"""Seed rows for the Base44 LeadCRM entity (Eran's private CRM at /crm).
Messages follow Eran's voice rules: plural, no emojis, no dashes, one observation first.
No link in the first message (Eran, 2026-09-27): the problem, "I prepared a few things, OK if I send them?",
free with no signup, and the intro line last, because the work matters more than who he is."""
import json, glob

BASE = "https://il-meta.base44.app/p/"
END = ("הכנתי לכם כמה דברים שפותרים את זה, כולל 20 מודעות חדשות עם המוצרים שלכם.\n"
       "זה בסדר אם אשלח לכם?\n"
       "זה בחינם לחלוטין, ולא צריך להשאיר מייל או להירשם.\n\n"
       "אני ערן, איש מוצר, חוויית לקוח ומומחה בקריאייטיב מדוייק. אני עושה את זה כבר 17 שנים.")

# second message, after a yes: the page link and an ask for a 30 minute call (Eran, 2026-09-27)
END2 = ("מעולה, הנה זה:\n{url}\n\n"
        "אם אהבתם את זה, אשמח שנקבע שיחה של 30 דקות, כדי שאוכל להראות לכם איך אני יכול לעזור לכם "
        "לשפר את התוצאות, עם אותו התקציב שאתם גם ככה מוציאים היום.")

LEADS = [
 ("2026-09-25-054", "redstar-02f7aee4",
  "לחצתי על המודעות שלכם, וארבע מהן מובילות לעמוד שגיאה. כל לחיצה עליהן היא כסף שהולך לפח."),
 ("2026-09-26-021", "megapet-beb32c3c",
  "לחצתי על המודעות שלכם. שמונה מודעות על נושאים שונים, וכולן מובילות לדף הבית, אז הרבה מהלוחצים פשוט עוזבים."),
 ("2026-09-26-024", "kelevteva-369078b4",
  "רוב המודעות שלכם הן אותו באנר של משלוח חינם. מה שמיוחד אצלכם, חנות בריאות לכלבים, כמעט לא מופיע שם."),
 ("2026-09-26-012", "petbest-20bd483a",
  "יש לכם מודעות שרצות כבר יותר משנה, אבל כמעט בכולן רואים שקית על רקע לבן ולא כלב או חתול אמיתי."),
 ("2026-09-25-086", "jackson-18bceed3",
  "עסק משפחתי עם מפעל ברמת גן מאז 2005, והסיפור הזה לא מופיע באף מודעה שלכם. גם יהלומי המעבדה לא מוסברים שם."),
 ("2026-09-25-039", "haircosmetics-8b8eb022",
  "המודעות שלכם רצות כבר חצי שנה, אבל כולן מראות בקבוק, מחיר וכפתור. תלתלים אמיתיים אין שם."),
 ("2026-09-25-076", "stav-56f5e275",
  "הסרטונים שלכם על יהלומים שחורים רצים כבר שנה וחצי, אבל המודעות הסטטיות הן עדיין תמונות מהאתר על רקע לבן."),
 ("2026-09-25-066", "bscents-97198747",
  "רוב המודעות שלכם הן על הבישום לכביסה, ומפיץ הריח, המוצר הכי מיוחד שלכם, כמעט לא מקבל במה."),
 ("2026-09-25-016", "astain-3f8c21d7",
  "המשפט שלא צריך להתאפר עובד אצלכם, אבל הסיפור של החווה ושל האצה האדומה לא מופיע באף מודעה."),
 ("2026-09-25-087", "jewelryfactory-8d2e61b4",
  "המודעות שלכם רצות כבר חצי שנה, אבל בכולן רואים מוצר על רקע לבן ולא את הרגע שבו פותחים את המתנה."),
 ("2026-09-25-051", "mydeal-5b7e19c2",
  "כל המודעות שלכם נשענות על קוד הנחה של 20 אחוז, וכל חנות עם אותם מותגים יכולה להגיד את אותו הדבר."),
 ("2026-09-25-071", "billy-264ffd4c",
  "לחצתי על המודעות שלכם. 12 מודעות עם אותו מבצע, כולן מובילות לדף הבית, והכי חדשה עלתה לפני חמישה חודשים."),
 ("2026-09-25-002", "kalahari-7c3e91d5",
  "האריזות השחורות עם הזהב שלכם נראות ממש יוקרה. מה שחסר במודעות זה הדבר הכי מיוחד אצלכם, קרם לכל סוג עור."),
]

def rows():
    out = []
    for i, (lid, slug, opening) in enumerate(LEADS):
        d = json.load(open(f"data/leads/{lid}.json"))
        b, c = d["business"], d["contact"]
        url = BASE + slug
        msg = opening + "\n\n" + END   # no link: Eran asks first, sends the page (url) after a yes
        assert "—" not in msg and "-" not in msg.replace(url, ""), lid
        out.append({
            "lead_id": lid, "slug": slug, "sort_order": i + 1,
            "business_name": b.get("name_he") or b.get("name_en"),
            "category": b.get("category") or "", "city": b.get("city") or "",
            "owner_name": b.get("owner_name") or "", "website": b.get("website") or "",
            "facebook": (c.get("facebook_page") or {}).get("url") or "",
            "instagram": (c.get("instagram_page") or {}).get("url") or "",
            "owner_instagram": (c.get("owner_instagram") or {}).get("url") or "",
            "whatsapp": (c.get("whatsapp") or {}).get("number_e164") or "",
            "message": msg, "message2": END2.format(url=url), "status": "new", "notes": "",
        })
    return out

if __name__ == "__main__":
    r = rows()
    json.dump(r, open("data/crm/seed.json", "w"), ensure_ascii=False, indent=1)
    print(r[0]["message"]); print(len(r))
