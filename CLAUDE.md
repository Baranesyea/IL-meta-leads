# Project: Ad Lead Engine (Israel)

> Implementation status, findings and decisions live in `NOTES.md` — read it first.
> Eran's binding design rules for ads and client pages: `DESIGN_RULES.md` — check every item before showing work.

## Mission
Every day, find **10 qualified leads**: small/medium Israeli businesses that sell **physical products** and are **currently running ads on Meta**. For each lead, research their ads, write a strategic mini report, generate **20 new premium product ads** (image + Hebrew copy), and produce two HTML pages:
1. **Internal lead page** (for Eran): contact details, research, angles, new ads, outreach message.
2. **Client pitch page** (for the business owner): a polished page showing what we found and the 20 new ads.

Eran approves each lead before the expensive step (image generation). Nothing is sent to the business automatically. Eran does all outreach himself.

---

## Pipeline overview

```
1. DISCOVER    -> find Israeli advertisers in Meta Ad Library
2. FILTER      -> keep only product businesses, small/medium, active ads
3. QUALIFY     -> find FB page, IG page, owner's IG, WhatsApp number  (HARD GATE)
4. COLLECT     -> pull their current ads (creatives, copy, dates, landing pages)
5. RESEARCH    -> product, audience, pains, current angles, gaps -> 5 new angles
6. APPROVE     -> Eran reviews lead + angles on the dashboard (HUMAN GATE)
7. GENERATE    -> 20 premium product ad images
8. COPY        -> Hebrew primary text, headline, description, CTA per ad
9. PUBLISH     -> internal lead page + client pitch page + daily dashboard
```

Run stages 1–5 until 10 leads reach the APPROVE stage for the day. Stages 7–9 run only on approved leads.

---

## Stage 1 — DISCOVER

**Important constraint:** the official Meta Ad Library API (`ads_archive`) only returns non-political ads for ads delivered in the EU/UK. Israeli commercial ads are **not** available through it. Use one of these, in order of preference:

1. **Apify actor** for Facebook Ads Library scraping (e.g. "Facebook Ads Library Scraper"). Input: search URL with `country=IL`, `ad_type=all`, `active_status=active`, `media_type=all`.
2. **Playwright scraper** of `https://www.facebook.com/ads/library/` as a fallback. Slow, rate-limit carefully (random delays, 1 browser, no parallel hammering).
3. If Eran connects the **Meta Ads MCP** (`ads_library_search`) to Claude Code, test whether it returns IL commercial ads. If it does, prefer it. *(Tested 2026-09-25: it does — see NOTES.md.)*

**Search strategy:** rotate daily through Hebrew product keywords and categories so we don't hit the same advertisers:
- קוסמטיקה, טיפוח, סרום, בישום, תכשיטים, אופנה, בגדי ים, נעליים, תיקים, מוצרי תינוקות, מוצרי בית, עיצוב הבית, מטבח, תוספי תזונה, חיות מחמד, ספורט, גאדג'טים, מתנות, קפה, שוקולד
- Also search English terms + `country=IL` (many Israeli brands advertise in English).

Store the keyword used and date, so tomorrow's run continues from the next keyword.

Output per advertiser: `page_id`, `page_name`, `page_url`, list of ad IDs, ad count.

---

## Stage 2 — FILTER

Keep the advertiser only if ALL are true:
- **Sells a physical product.** Signals: CTA like "Shop now / לרכישה / להזמנה", landing page is a store (Shopify, WooCommerce, Wix Stores, Konimbo, Tranzila checkout, product page with price + add to cart). Reject: services, courses, coaches, real estate, clinics, events, apps, lead-gen forms for services.
- **Is Israeli.** Hebrew ad copy, `.co.il` domain, ₪ prices, or Israeli phone numbers.
- **Is small/medium, owner-reachable.** Reject big chains and known brands (e.g. Super-Pharm, Castro, Fox, Golf, Shufersal, international brands). Heuristics: FB page followers under ~200k, not a public company, has a founder face in content, IG bio mentions a person.
- **Has at least 2 active ads.**
- **Not already in the database** (dedupe by page_id AND domain across all past days).

Log rejected advertisers with a `reject_reason` so we never re-check them.

---

## Stage 3 — QUALIFY (hard gate)

A lead is **qualified** only when we have ALL FOUR:

| Field | Where to look |
|---|---|
| Facebook page URL | From the Ad Library result |
| Instagram business page | FB page "About"/linked account, website header/footer, Linktree |
| Owner's personal Instagram | IG bio ("Founded by @x", "by @x"), website About/Our Story page, IG highlights/tagged posts, FB page posts signed by the owner, press articles |
| WhatsApp number | `wa.me/` or `api.whatsapp.com` links on website, FB page WhatsApp button, IG bio link, Linktree, website contact page |

Rules:
- WhatsApp must be an Israeli mobile: normalize to `+9725XXXXXXXX`. Accept `05X-XXXXXXX`, `+972-5X...`, `972 5X...`. Reject landlines (02/03/04/08/09) unless explicitly a WhatsApp link.
- Record **source URL for every field** and a `confidence` (high = explicit link, medium = inferred from text, low = guess). Owner IG with low confidence does NOT count; the lead stays unqualified.
- Do not message anyone and do not use any unofficial "is this number on WhatsApp" checkers.
- If any field is missing: status `unqualified`, list what's missing, move on.

Also capture: business name (Hebrew + English if available), website, city if visible, owner's name if visible, email if visible.

---

## Stage 4 — COLLECT current ads

For each qualified lead, save up to 15 active ads:
- Ad ID, start date, days running, platforms (FB/IG), number of variations
- Primary text, headline, CTA, landing URL
- Media: download images; for videos save the thumbnail + video URL
- Flag **"likely winners"**: ads running 30+ days or with many variations

Also fetch the main landing page / store: product names, prices, hero product, current offer (discount, free shipping, bundle), and **download 3–6 clean product photos** (needed as references in Stage 7).

---

## Stage 5 — RESEARCH (mini report)

Write in **Hebrew**, concise, sharp. Structure:

1. **The business in one line** — what they sell, price range, positioning (premium / mid / discount).
2. **Hero product(s)** — what they push most in ads.
3. **Audience** — primary and secondary personas: gender, age range, life situation, what they care about. Base this on the ad copy, visuals, and site, not guesses.
4. **Pains the product solves** — 3–5, in the customer's own language.
5. **Desires / outcomes** — what the customer really wants.
6. **Objections** — price, trust, "does it work", shipping, etc.
7. **Current ads audit** — what angles/formats they use now, what's working (long-running ads), what's weak (generic visuals, no hook, weak offer, bad text overlay, not mobile-first).
8. **Gaps and opportunities** — what they are NOT doing.
9. **5 new angles** — each with: name, core idea, target persona, hook line (Hebrew), why it should work.

Save as structured JSON (see schema) plus rendered into the HTML pages.

---

## Stage 6 — APPROVE (human gate)

Generate/refresh `output/dashboard.html` listing today's leads with status. For each lead show: name, links, WhatsApp, current ads thumbnails, the 5 angles.

Eran approves by editing `data/approvals.json` (or via a simple CLI: `python run.py approve <lead_id>` / `reject <lead_id> "reason"`). He may also edit angles before approving.

Only `approved` leads go to Stage 7.

---

## Stage 7 — GENERATE 20 ads

> **Open decision:** before building this stage, agree with Eran on exactly what we generate and which image model. Do not start generating before that.

**Structure:** 5 angles × 4 creatives = 20. Mix of formats per angle:
- 1:1 (1080×1080) and 4:5 (1080×1350) as main; produce 9:16 (1080×1920) for 1 of each 4 if easy.

**Image model:** use an API Eran has credits for (configurable in `.env`):
- Option A: Higgsfield (Eran has an account; connect its MCP to Claude Code or use its API)
- Option B: Nano Banana / Gemini image model via OpenRouter
The model must support **image reference / image-to-image**, because:

**The product must look exactly like their real product.** Always pass the downloaded product photos as references. Never invent packaging, labels, or logos. If the model distorts the product, composite the real product cutout (background removed) onto a generated scene instead.

**Premium style requirements:**
- Studio-quality lighting, editorial/luxury feel, clean composition, lots of negative space
- Styles to rotate: studio hero shot, lifestyle-in-use, macro texture/detail, flat lay, before/after or problem/solution, UGC-style premium, bold typographic ad
- Consistent with the brand's colors (extract palette from their site/logo)
- No cheesy stock look, no cluttered layouts, no fake reviews or fake badges

**Hebrew text on images:** image models render Hebrew badly. Generate images **without text**, then add the headline/overlay in a second step using HTML+CSS rendered with Playwright (or Pillow with a proper RTL Hebrew font like Heebo/Assistant/Rubik). Keep overlay short (max ~6 words), mobile-readable.

Save to `output/<lead_id>/ads/ad_01.png ... ad_20.png`. Add a subtle "Preview" watermark version for the client page (`ads_preview/`).

Budget guard: max retries per ad = 2; log cost per lead.

---

## Stage 8 — COPY

For each of the 20 ads, write in Hebrew:
- **Primary text** (3 variations of length: short 1–2 lines; medium ~4 lines; the ad gets one of them, the others stored as alternates)
- **Headline** (up to ~40 chars)
- **Description** (optional, short)
- **CTA button** (Shop Now / Learn More / Order Now)

Voice: natural Israeli Hebrew, not translated-sounding. Hook in the first line. Follow Meta policy (no personal-attribute claims like "Are you overweight?", no exaggerated medical claims, no fake urgency).

---

## Stage 9 — PUBLISH

### A. Internal lead page `output/<lead_id>/internal.html` (Hebrew, RTL)
- Business header: name, logo, website, city
- Contact block: FB page, IG page, owner IG, **WhatsApp click-to-chat** link (`https://wa.me/972...`) — each with source link + confidence
- Their current ads (gallery, days running, winner flags)
- Mini report (all sections from Stage 5)
- The 20 new ads with copy under each, grouped by angle
- **Suggested first WhatsApp message** from Eran (short, personal, non-spammy, references something specific from their ads, offers to send the page)
- Status + notes

### B. Client pitch page `output/<lead_id>/client.html` (Hebrew, RTL, premium design)
- Personal opening addressed to the business/owner by name
- "What we noticed in your current ads" (3–4 respectful, sharp insights — never insulting)
- The new angles (short version)
- Gallery of the 20 new ads (watermarked previews) with copy
- Clear CTA: WhatsApp to Eran
- Must be mobile-first, fast, single self-contained HTML file (images inlined or in a sibling folder), no internal notes, no scraped personal data beyond what's public on their business pages

### C. Daily dashboard `output/dashboard.html`
Table of all leads by date with status, links to both pages.

Deploy client pages to a static host (Netlify/Vercel/Cloudflare Pages) with an unguessable URL per lead, e.g. `/p/<random-slug>/`. Deployment step is optional in v1, local files first.

---

## Data model

`data/leads.db` (SQLite index, rebuilt automatically from the JSONs) with table `leads`, plus one JSON per lead at `data/leads/<lead_id>.json` (source of truth):

```json
{
  "lead_id": "2026-09-25-001",
  "status": "discovered|rejected|filtered|unqualified|qualified|researched|approved|generated|published|contacted",
  "reject_reason": null,
  "business": {
    "name_he": "", "name_en": "", "website": "", "city": "", "category": "",
    "owner_name": "", "email": ""
  },
  "contact": {
    "facebook_page": {"url": "", "source": "", "confidence": "high"},
    "instagram_page": {"url": "", "source": "", "confidence": ""},
    "owner_instagram": {"url": "", "source": "", "confidence": ""},
    "whatsapp": {"number_e164": "+9725...", "source": "", "confidence": ""}
  },
  "meta": {"page_id": "", "active_ads_count": 0, "search_keyword": ""},
  "current_ads": [
    {"ad_id": "", "start_date": "", "days_running": 0, "platforms": [], "primary_text": "",
     "headline": "", "cta": "", "landing_url": "", "media": [], "likely_winner": false}
  ],
  "products": [{"name": "", "price": "", "url": "", "images": []}],
  "research": {
    "one_liner": "", "hero_products": [], "audience": [], "pains": [], "desires": [],
    "objections": [], "current_ads_audit": "", "gaps": [],
    "angles": [{"id": "A1", "name": "", "idea": "", "persona": "", "hook": "", "why": ""}]
  },
  "new_ads": [
    {"ad_no": 1, "angle_id": "A1", "format": "4:5", "image": "", "image_preview": "",
     "primary_text": "", "alt_texts": [], "headline": "", "description": "", "cta": ""}
  ],
  "outreach": {"suggested_whatsapp_message": ""},
  "cost": {"image_gen_usd": 0},
  "timestamps": {}
}
```

---

## Folder structure

```
/  (repo root)
  CLAUDE.md  NOTES.md
  .env                 # API keys (Apify, image model, OpenRouter, etc.) — see .env.example
  config.yaml          # daily target, keywords, filters, style settings
  run.py               # CLI entry
  /src
    common.py  db.py  discover.py  filter.py  qualify.py  collect.py
    research.py  generate.py  copy.py  publish.py
  /templates           # Jinja2 HTML templates: internal, client, dashboard
  /assets/fonts        # Heebo / Assistant / Rubik
  /data                # leads.db, leads/*.json, raw/discover/*.json, approvals.json, keyword_state.json
  /output              # dashboard.html, <lead_id>/internal.html, client.html, ads/
  /logs
```

## CLI

```
python run.py discover        # stage 1 (ingests MCP dumps from data/raw/discover/)
python run.py filter          # stage 2
python run.py find            # stages 1-5 until 10 leads reach "researched" today
python run.py status [date]   # list leads + status
python run.py approve <id>    # mark approved
python run.py reject <id> "reason"
python run.py build           # stages 7-9 for all approved leads
python run.py build <id>      # single lead
python run.py dashboard       # rebuild dashboard
```

## Tech stack
- Python 3.11+, Playwright, httpx, BeautifulSoup, Jinja2, Pillow, SQLite
- Apify client (discovery), image model client (configurable), rembg for product cutouts
- Use Claude (via Claude Code itself or the Anthropic API) for research, angles, and copy

## Rules
- Respect rate limits, add random delays, cache every fetched page.
- Only collect publicly available business contact info. Never store personal data beyond the four required fields + public business info.
- Never contact anyone automatically. All outreach is manual by Eran. (Israeli law restricts unsolicited commercial messages; first contact should be a personal, one-to-one message.)
- Every step must be resumable: if a run crashes, rerunning continues from each lead's current status.
- Log everything to `/logs/<date>.log`.

## Build order (for Claude Code)
1. Scaffold project, config, DB, CLI skeleton. ✅
2. Stage 1–2 (discover + filter). Test with one keyword, show Eran 10 raw advertisers. ✅
3. Stage 3 (qualify). Test on those 10, report hit rate per field. ✅ (owner IG = best-effort)
4. Stage 4–5 (collect + research). Produce one full JSON + internal.html for review. ✅ (waiting for Eran)
5. Stage 6 (approval flow + dashboard).
6. Stage 7–8 (generation + copy). Test on ONE approved lead first, 4 ads only, get Eran's feedback on quality before running all 20.
7. Stage 9 (client page), then optional deploy.

Stop and ask Eran after steps 2, 3, 4 and 6 before continuing.
