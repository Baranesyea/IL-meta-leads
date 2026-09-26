"""Seed rows for the Base44 LeadCRM entity (Eran's private CRM at /crm).
Messages follow Eran's voice rules: plural, no emojis, no dashes, one observation first."""
import json, glob

BASE = "https://il-meta.base44.app/p/"
END = ("אני ערן, ואני בונה קריאייטיב למודעות בפייסבוק ובאינסטגרם.\n"
       "ישבתי והכנתי לכם 20 מודעות חדשות, עם המוצרים האמיתיים שלכם.\n"
       "הכול מחכה לכם כאן:\n{url}\n\n"
       "זה בחינם ובלי שום התחייבות. אם משהו שם מדבר אליכם, אשמח לדבר.\n"
       "ערן")

LEADS = [
 ("2026-09-26-024", "kelevteva-369078b4",
  "ראיתי שרוב המודעות שלכם הן אותו באנר עם משלוח חינם מעל 299.\n"
  "אבל מה שמיוחד אצלכם זה שאתם חנות בריאות לכלבים, ואת זה כמעט לא רואים שם."),
 ("2026-09-26-012", "petbest-20bd483a",
  "יש לכם מודעות שרצות כבר יותר משנה, וזה סימן שהן מוכרות. ראיתי שאתם מפרסמים גם ברוסית, ממש אהבתי.\n"
  "מה שלא מצאתי זה כלב או חתול אמיתי שנהנה מהמוצר. כמעט הכול שקית על רקע לבן."),
 ("2026-09-25-086", "jackson-18bceed3",
  "עסק משפחתי עם מפעל ברמת גן מאז 2005. זה סיפור שהרבה מתחרים היו שמחים שיהיה להם, ולא מצאתי אותו באף מודעה שלכם.\n"
  "גם יהלומי המעבדה, היתרון הכי חזק שלכם במחיר, לא מוסברים שם."),
 ("2026-09-25-039", "haircosmetics-8b8eb022",
  "ראיתי שהמודעות שלכם רצות כבר חצי שנה, והביצוע מסודר ונקי.\n"
  "מה שחסר לי שם זה תלתלים אמיתיים. כל המודעות מראות בקבוק, מחיר וכפתור."),
 ("2026-09-25-076", "stav-56f5e275",
  "ראיתי את הסרטונים שלכם על יהלומים שחורים. הם רצים כבר יותר משנה וחצי, וזה אומר שהם עובדים.\n"
  "מה שתפס לי את העין זה שהמודעות הסטטיות הן עדיין תמונות מהאתר על רקע לבן, והתכשיטים שלכם שווים הרבה יותר מזה."),
 ("2026-09-25-066", "bscents-97198747",
  "ראיתי שרוב המודעות שלכם הן על הבישום לכביסה, והן רצות כבר חודשים. כנראה שהקהל אוהב אתכם.\n"
  "אבל מפיץ הריח, המוצר הכי מיוחד שלכם, כמעט לא מופיע ולא מקבל את הבמה שמגיעה לו."),
 ("2026-09-25-016", "astain-3f8c21d7",
  "המשפט שאומר שלא צריך להתאפר רץ אצלכם בכמה גרסאות, ובצדק. הוא חזק.\n"
  "מה שלא מצאתי באף מודעה זה את הסיפור של החווה ושל האצה האדומה. זה הסיפור הכי חזק שיש לכם."),
 ("2026-09-25-087", "jewelryfactory-8d2e61b4",
  "המודעות שלכם רצות כבר חצי שנה ויותר, אז ברור שהמוצרים נמכרים.\n"
  "אבל בכל המודעות רואים מוצר על רקע לבן, ולא את הרגע שבו מישהו פותח את המתנה."),
 ("2026-09-25-051", "mydeal-5b7e19c2",
  "ראיתי שכל המודעות שלכם נשענות על קוד ההנחה של 20 אחוז. זה עובד, אבל כל חנות עם אותם מותגים יכולה להגיד את אותו הדבר.\n"
  "מה שחסר זו סיבה לקנות דווקא אצלכם."),
]

def rows():
    out = []
    for i, (lid, slug, opening) in enumerate(LEADS):
        d = json.load(open(f"data/leads/{lid}.json"))
        b, c = d["business"], d["contact"]
        url = BASE + slug
        msg = opening + "\n\n" + END.format(url=url)
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
            "message": msg, "status": "new", "notes": "",
        })
    return out

if __name__ == "__main__":
    r = rows()
    json.dump(r, open("data/crm/seed.json", "w"), ensure_ascii=False, indent=1)
    print(r[0]["message"]); print(len(r))
