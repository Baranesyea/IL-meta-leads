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

## 2026-09-25 — Overlay v2 (typography variety + don't cover the product)

- Eran: typography identical on every ad and sometimes covers important details; he'll upload fonts
  to `assets/fonts/`.
- `src/overlay.py`: 6 layouts (editorial / corner / bigtype / column / band / frame). Per angle the 4 ads
  get 4 different layouts. `find_zone()` scores candidate zones by edge density + luminance variance on
  the actual image and places text in the emptiest one; full-width layouts only where the band is empty
  (score ≤ BUSY), else a small corner/column. Text + brand colour follow local brightness.

## 2026-09-25 — Eran's fonts + design directions

- Fonts in `assets/fonts/`: FbOptimum Light/Regular/Black (all ad typography, weight contrast),
  FbIdealist (handwriting — designer signature / short personal note only). Set in `config.yaml → overlay.fonts`.
  Fonts are Hebrew-only; Latin (14K) falls back — fine for now.
- Eran: "several directions per delivery, not one template with different photos". `src/overlay.py` now has
  7 directions: contrast, quiet (+signature), stack, note (handwritten), cover (frame+masthead),
  panel (bottom colour panel, never touches the product), label (museum label).
  Each angle gets 4 different directions; panels capped at 4–5 per lead; `has_people` on an ad enables a
  skin-tone penalty so text avoids faces/necks/hands; `layout.direction` forces a direction per ad.
- Idealist must be ≥100px to read. Keep handwritten notes short (≤ 5 words).

## 2026-09-25 — Legibility pass + web fonts

- Eran: tiny text, white text on busy photos, text on the model's lips = unacceptable.
- Min sizes raised (details ≥30px on a 1080 canvas, headlines 60–170px). Busy background under text →
  translucent plate. Text zones are now cut to the free space above/below each ad's `protect` boxes
  (product, faces, hands — set per ad; Haar face detection as a backup) and text shrinks to fit.
- Web fonts: `assets/fonts/web/*.woff2` + `fonts.css` (family "Optimum" 300/400/900, "Idealist").
  Fb fonts are commercial — confirm the web licence covers public pages.

## 2026-09-25 — Base44 app "IL Meta" (client report pages)

- App id `6ab69996dac5efca4ece2296` (editor: https://app.base44.com/apps/6ab69996dac5efca4ece2296/editor/preview).
  Home = "כאן יהיה תוכן" (builder-made, sidebar). Client pitch pages: `/p/<slug>` standalone
  (`src/pages/ClientPitch.jsx` + `src/reports/data.js` in the Base44 app; copies in `web/base44/`).
  Stav: `/p/stav-56f5e275`. Hero = full-bleed creative with parallax + floating ad cards, Optimum web font.
- BLOCKED: images (ads webp) and woff2 fonts are not yet in the app's `public/` — uploading the asset
  bundle to external storage was refused by the environment's policy. Needs Eran's decision.
- Missing: Eran's WhatsApp link for the CTA (`contact_url`).

## 2026-09-25 — IL Meta site v2 (live)

- Live: https://il-meta.base44.app  (home = "כאן יהיה תוכן", no menus, no client lists)
  Stav: https://il-meta.base44.app/p/stav-56f5e275
- Each client only sees their own page (standalone route, unguessable slug, noindex). Sidebar/Layout,
  /report route and the builder's sample entity pages were removed from routing.
- Whole app uses Eran's fonts (Optimum 300/400/900 + Idealist) from /public/fonts (pulled from this repo).
- Client page = brand showcase: full-screen hero campaign (Ken Burns + parallax), campaign marquee,
  editorial split (lab diamond), handwritten quote band, then the pitch (insights, 5 angles × 4 ads, CTA).
- Ads on the site are drawn live: raw Higgsfield photos (webp, /public/reports/<client>/raw_NN.webp) +
  `src/components/AdCanvas.jsx`, a React port of templates/overlay.html.j2 driven by the per-ad `spec`
  exported by `src/overlay.py` (layout.render). Keep the two in sync when the overlay changes.
- Source of truth for site files: `web/base44/` in this repo → synced into the Base44 sandbox with
  curl from raw.githubusercontent (repo is public). AdCanvas.jsx currently lives only in the Base44 app.
- Still missing: Eran's WhatsApp link for the CTA (`contact_url` in data.js).

## 2026-09-25 (evening) — client page fixes
- Editor pages: Base44 lists a page per *component file* + literal route, and only re-scans routes when a file is
  saved through the builder path (`POST /api/apps/{id}/coding/write-batch`), not via sandbox `run_command`.
  So each client gets `src/pages/<Name>.jsx` (thin wrapper around ClientPitch with a fixed slug) + a literal
  `/p/<slug>` route between the CLIENT-ROUTES markers in App.jsx, saved via write-batch. Stav → `Stav.jsx`.
- Contrast: `overlay.legibility()` measures the pixels under each text box (5th/95th luminance percentile) and
  picks ink + the minimum scrim for 4.5:1 (big Black type) / 7:1 (thin, script, small type); busy boxes or
  scrim > .62 → plate. `brand_line()` drops the brand line on busy strips. Sub lines no longer faded,
  small type sizes raised, Idealist stroke thickened. Specs (scrim, plate_bg, brand_color) exported to data.js.
- Client page: lightbox close button fixed on top (was covered by the ad box on mobile), opaque backdrop,
  scroll lock; campaign strip = one height; angle rows chunked by viewport (4/2/1) and justified to one height.
- CTA WhatsApp: https://wa.me/972545471522 (Eran).

## 2026-09-25 (night) — full-bleed only
- Eran: plates behind text and photo+colour-strip panels read as a compromise, not premium. Both removed
  (MAX_PANELS=0, no plates). Zones now slide over the whole frame incl. beside the subject (mid_left/right)
  clear of `protect`; scrim = band feathered around the text only, strength from legibility().
- Hand-picked look per ad: `layout.direction` wins even in a tight frame (e.g. ad 12 → contrast above the head).
- Baked-in black bands: ad 6 cropped; ad 10 cropped + outpainted upward (Higgsfield outpaint 2 cr, low-res
  768px → only the new sky is used, original sharp pixels composited back). Originals kept as *_v1_*.png.
- Page-style leak: `.bp .card` (white card) also hit the ad's label `.card` → renamed `.lcard` in AdCanvas.
- Client page: ads without caption strips, edge to edge on phones; campaign strip = JS drift + native swipe
  (pauses on touch, resumes after 2.2s); headlines type in on scroll (`Type`, layout-stable, reduced-motion safe);
  phone split section = photo melting into dark ground under the text.
- Base44 quirk: create_checkpoint can snapshot a stale commit right after a sandbox commit — re-run until
  git_commit_hash matches `git log -1` before deploying.

## 2026-09-26 — legibility verified on the rendered ad
- Eran (screenshots): text too small / too close to the jewel on phones. Rule now: never trust the layout
  math alone. After rendering, MEASURE_JS reads the main line's px and the letters' real box; an ad fails if
  main < 78px (script < 92) on the 1080 canvas or the letters touch a padded protect box → retried with another look.
- Review at phone size (390px wide), never on a small contact sheet. Hand-drawn `protect` boxes are
  authoritative and must be tight (face and hand as separate boxes); Haar only when none exist.
- Headlines use text-wrap:balance (no lone last word).
- Page (phones): hero words in the photo's dark top so the pendant is clear; lab-diamond photo above its
  text; quote band text in the photo's dark top, ring below.
