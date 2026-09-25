# Implementation notes (decisions & findings)

## 2026-09-25 — Steps 1–2 (scaffold + discover + filter)

- **Discovery source:** the Meta Ads MCP `ads_library_search` (country=IL, ACTIVE) **does return
  Israeli commercial ads** (currency ILS). It is the preferred source (per CLAUDE.md Stage 1, option 3).
  - Returns: ad id, page_id, page_name, link title, creation/delivery times, snapshot URL, currency.
  - Does NOT return: ad body text, landing URL, media. Those come in stages 3–4.
  - Max 50 ads per call, newest first. Querying with `page_ids=[...]`, `limit=1` gives the page's
    exact active-ad count via `estimated_total_count` (used for the ≥2 active ads rule).
  - The MCP can only be called by Claude Code, so the pipeline ingests JSON dumps from
    `data/raw/discover/` (`discovery.backend: mcp_import`).
- **Network:** this cloud environment blocks facebook.com, api.apify.com and google.com. The Apify
  backend is written but untested; the Playwright fallback can't run here.
- **Filter:** without a landing URL, "sells a physical product" is only a probable verdict from page
  name + ad titles. New status `filtered` sits between `discovered` and `qualified`; stage 3 confirms
  on the real website and can still reject.
- **Images (stage 7):** provider deliberately left `undecided` in config.yaml — decide with Eran
  what we generate and on which model before building stage 7.

## 2026-09-25 — Step 3 (qualify)

- Network opened by Eran. Chromium needed the proxy CA in `~/.pki/nssdb` (added with certutil) and
  `proxy=HTTPS_PROXY` in Playwright launch.
- **Works:** Ad Library ad pages via Playwright without login → landing URL, full ad text, dates.
  Business websites via httpx (Playwright fallback on 403/503). Link-in-bio pages are followed.
- **Doesn't work:** Facebook page "About" (login wall). Instagram profiles/bios — scraping them is
  off-limits in this environment. Some stores (goluggage, lavender) block bots even in Chromium.
- First run on the 7 filtered leads: website 6/7, IG page 3/7, owner IG 0/7, WhatsApp 3/7.
  Owner IG is the bottleneck: sites almost never name the owner's personal IG, and web search
  didn't surface it either (tested on 2 leads). Decision pending with Eran.

## 2026-09-25 — Discovery v2, stage 4–5 first pass

- **Discovery now uses the Ad Library search page in Chromium (no login)** — `backend: playwright`.
  Gives full ad data (body, landing URL, CTA, media, start date, page likes, categories).
  Logged-out pagination is rate-limited → ~30 ads per keyword, so the keyword list is long.
- `python run.py find` loops keywords until `daily_target` leads are `qualified`.
- **Owner IG is best-effort, not a gate** (Eran: "we said 10 clear leads"). Qualified =
  website + business IG + WhatsApp. Owner name often found via website About / web search.
- Manually rejected after review: beauty academy (courses), car dealer, Danon (established chain).
- Collect: Woo Store API / Shopify products.json via httpx, Chromium fallback for protected stores.
- Research for 2026-09-25-076 (Stav Fine Jewelry) written by Claude Code in-session;
  `python run.py internal <id>` renders a self-contained internal page (images inlined).

## 2026-09-25 — Fix: multi-version ads + first image test

- Ads with several versions (dynamic creative / catalog) come back from Ad Library search with
  `{{product.brand}}` / `{{product.name}}` placeholders. Eran caught it. `collect.resolve_rendered`
  now opens the ad's own library page and takes the real text; `multiple_versions` is recorded.
  Stav's audit + WhatsApp message corrected (her 550-day winners are founder/education videos).
- Image model decision (with Eran): **Higgsfield `nano_banana_pro`**, 4:5, 2k, 2 credits/image,
  2 product reference photos per ad (one colour variant only — Shopify images come in Y/W/R gold).
  Test: 3/3 kept the real product (flower pendant, lab-diamond ring, sapphire threaders).
  `soul_2` failed (no model on-body, redesigned the pendant) — not used.
- Hebrew text: `src/overlay.py` + `templates/overlay.html.j2` (Frank Ruhl Libre + Heebo, Chromium).

## 2026-09-25 — 20 ads for Stav (076), round 1

- Eran: direction good; font wrong (he'll send one → `config.yaml: overlay.*_font`, supports a file
  in `assets/fonts/`); wants some on-model shots; stronger messages; diverse angles/looks for testing.
- 5 angles × 4, each with a different look (dark studio / bright / on-model / flat lay / typographic)
  and mixed formats (4:5, 1:1, 9:16). 6 on-model shots via nano_banana_pro with a worn reference photo.
- Copy per ad in `data/leads/2026-09-25-076.json → new_ads[]` (overlay, primary, short alt, headline,
  description, CTA, `to_verify` for claims to confirm with the business). Script kept in
  `data/stav_ads_2026-09-25-076.py`.
- QA: 1 retry (ad 14: pendant petals came out hollow). ~43 Higgsfield credits total for this lead.
- Overlay: RTL + ₪ + maqaf breaks bidi ("מ־₪1,500") → write prices as "1,500 ש״ח" on images.
