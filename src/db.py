"""SQLite index + one JSON file per lead (the JSON is the source of truth)."""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from urllib.parse import urlparse

from .common import DATA, now_iso, today

DB_PATH = DATA / "leads.db"
LEADS_DIR = DATA / "leads"

STATUSES = [
    "discovered", "rejected", "filtered", "unqualified", "qualified",
    "researched", "approved", "generated", "published", "contacted",
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    lead_id     TEXT PRIMARY KEY,
    page_id     TEXT UNIQUE NOT NULL,
    page_name   TEXT,
    domain      TEXT,
    status      TEXT NOT NULL,
    reject_reason TEXT,
    search_keyword TEXT,
    run_date    TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_leads_domain ON leads(domain);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
"""


@contextmanager
def connect():
    DATA.mkdir(parents=True, exist_ok=True)
    fresh = not DB_PATH.exists()
    conn = sqlite3.connect(DB_PATH)
    if fresh:
        conn.executescript(SCHEMA)
        conn.commit()
        conn.close()
        reindex()  # leads.db is a rebuildable index; lead JSONs are the source of truth
        conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def normalize_domain(url: str | None) -> str | None:
    if not url:
        return None
    host = urlparse(url if "://" in url else f"https://{url}").hostname or ""
    host = host.lower().removeprefix("www.")
    return host or None


def empty_lead(lead_id: str, page_id: str, page_name: str, keyword: str) -> dict:
    return {
        "lead_id": lead_id,
        "status": "discovered",
        "reject_reason": None,
        "business": {"name_he": "", "name_en": "", "website": "", "city": "",
                     "category": "", "owner_name": "", "email": ""},
        "contact": {
            "facebook_page": {"url": f"https://www.facebook.com/{page_id}",
                              "source": "meta_ad_library", "confidence": "high"},
            "instagram_page": {"url": "", "source": "", "confidence": ""},
            "owner_instagram": {"url": "", "source": "", "confidence": ""},
            "whatsapp": {"number_e164": "", "source": "", "confidence": ""},
        },
        "meta": {"page_id": page_id, "page_name": page_name,
                 "active_ads_count": 0, "search_keyword": keyword,
                 "sample_ads": [], "filter": {}},
        "current_ads": [],
        "products": [],
        "research": {},
        "new_ads": [],
        "outreach": {"suggested_whatsapp_message": ""},
        "cost": {"image_gen_usd": 0},
        "timestamps": {"discovered": now_iso()},
    }


def reindex() -> None:
    """Rebuild the SQLite index from data/leads/*.json."""
    for path in sorted(LEADS_DIR.glob("*.json")):
        save_lead(json.loads(path.read_text(encoding="utf-8")))


def load_lead(lead_id: str) -> dict:
    with open(LEADS_DIR / f"{lead_id}.json", encoding="utf-8") as f:
        return json.load(f)


def save_lead(lead: dict) -> None:
    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    path = LEADS_DIR / f"{lead['lead_id']}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(lead, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)
    domain = normalize_domain(lead["business"].get("website"))
    with connect() as conn:
        conn.execute(
            """INSERT INTO leads (lead_id, page_id, page_name, domain, status, reject_reason,
                                  search_keyword, run_date, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?)
               ON CONFLICT(lead_id) DO UPDATE SET
                 page_name=excluded.page_name, domain=excluded.domain, status=excluded.status,
                 reject_reason=excluded.reject_reason, updated_at=excluded.updated_at""",
            (lead["lead_id"], lead["meta"]["page_id"], lead["meta"].get("page_name"), domain,
             lead["status"], lead.get("reject_reason"), lead["meta"].get("search_keyword"),
             lead["lead_id"][:10], now_iso()),
        )


def set_status(lead: dict, status: str, reject_reason: str | None = None) -> None:
    assert status in STATUSES, status
    lead["status"] = status
    lead["reject_reason"] = reject_reason
    lead["timestamps"][status] = now_iso()
    save_lead(lead)


def page_known(page_id: str) -> bool:
    with connect() as conn:
        return conn.execute("SELECT 1 FROM leads WHERE page_id=?", (str(page_id),)).fetchone() is not None


def domain_known(domain: str | None, exclude_lead: str | None = None) -> bool:
    if not domain:
        return False
    with connect() as conn:
        row = conn.execute("SELECT 1 FROM leads WHERE domain=? AND lead_id != ?",
                           (domain, exclude_lead or "")).fetchone()
        return row is not None


def next_lead_id(date: str | None = None) -> str:
    date = date or today()
    with connect() as conn:
        n = conn.execute("SELECT COUNT(*) FROM leads WHERE run_date=?", (date,)).fetchone()[0]
    return f"{date}-{n + 1:03d}"


def leads_by_status(*statuses: str, date: str | None = None) -> list[dict]:
    q = "SELECT lead_id FROM leads"
    conds, args = [], []
    if statuses:
        conds.append(f"status IN ({','.join('?' * len(statuses))})")
        args += statuses
    if date:
        conds.append("run_date=?")
        args.append(date)
    if conds:
        q += " WHERE " + " AND ".join(conds)
    q += " ORDER BY lead_id"
    with connect() as conn:
        ids = [r[0] for r in conn.execute(q, args)]
    return [load_lead(i) for i in ids]
