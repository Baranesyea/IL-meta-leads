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

## 2026-09-26 — second client from the template: B-scents (lead 2026-09-25-066)
- Scent diffusers / perfume oils / laundry perfume — deliberately far from Stav (jewellery). Page:
  https://il-meta.base44.app/p/bscents-97198747 (plural address). Built end to end from `data/bscents_*.py`
  + `src/site_export.py` into the shared `ClientPitch.jsx` template (`REPORTS` in data.js).
- Product refs must be the brand's own labels: store photos of oils named after designer perfumes
  (BLUE CHANEL, CREED) were swapped for the MUSK VANILLA bottle. "note" look only for ads that have a note;
  subs Hebrew-only (mixed Latin/Hebrew scrambles in RTL).
- Higgsfield: ~58 credits (21 initial + 5 regen + 2 face fixes + 1 outpaint, nano_banana_pro 2k).
- Verification (live, Playwright 390×844 / 1280×700 / 1440×900) found the quote band parallax used a
  hard-coded page offset (`y - 2200`), leaving a grey stripe on tall phone pages. Now `bandShift()` is
  relative to the band's own position and clamped inside its 12% bleed.
- Base44 sandbox: app code is in `/app` (a fresh shell starts in `/workspace`).

## 2026-09-26 — Eran on B-scents: text on wall lines, slang, before/after
- Text over wall corners / soffit / window frames reads broken (ad 9 screenshot). Regenerated ads 1,3,6,9,10,12,20
  with prompts that demand one seamless wall/backdrop where the text goes, and protect boxes that fence off the
  remaining lines (14 credits; old images kept as `ads_raw/ad_XX_v_lines.png`). The other 13 keep their looks
  (`layout.direction` pinned from the previous render).
- overlay: MEASURE_JS now measures every text run (headlines split by `<br>` were missed, so the protect-overlap
  check ignored them). `crossing_lines()` is advisory only: soft wall shadows score high, diagonal soffits low.
- "אשכרה" (their own tagline) removed from ad 15, angle A4 hook and the split title.
- New page section `compare` (after the insights): "היום" = 4 of their running ads (Ad Library media, videos as
  thumbnails with a play mark) above "איתנו" = 4 of ours for the same products, in matching order.
  B-scents: `data/bscents_site.py`; Stav: `data/stav_compare.py`.

- (later) Eran on Stav: the hero button sat on the model's face on a short phone (375×667: the photo was pinned
  at 36% from the top, the words overflowed onto it). Hero is now a flex column below 7:5 — words, then the photo
  in its own box. The before/after rows became review pairs right under "הקמפיין שלך עובד" (their ad | ours),
  followed by "מה היינו משנים" + the insights.
- (later) Eran: a hero split into words + photo "is not a hero"; and the before/after should be their 4 ads
  small, ours big — not pairs. Phone hero now uses `hero_bg_m` (tall outpainted photo) full-bleed with a soft
  top shade; Stav's dark top was extended locally (plain background), B-scents' button sits at the bottom.
  Higgsfield: 3 outpaints (6 credits).
- (later) Eran: a "why work with me" section on every page, one before the end, with a nav link. Built as the
  shared `OFFER` in ClientPitch.jsx (not per-client data): intro on one side, 6 numbered things you get on the
  other, then "מחיר חודשי קבוע. הכל כלול." Grammar per client via `address` ("f" Stav, "pl" B-scents).

## 2026-09-26 — two more clients: Asta-In (016) and JewelryFactory (087)
- Picked from leads with a WhatsApp number, a physical product, ≥4 collected ads and store photos:
  Asta-In (natural astaxanthin skincare, bright botanical-biotech look, light hero) and JewelryFactory
  (personalised jewellery/gifts, warm masculine look). Kalahari Rose skipped: one ad only (no "today" row).
  Pages: /p/astain-3f8c21d7, /p/jewelryfactory-8d2e61b4 (plural address, shared OFFER section).
- Higgsfield: 320 → 186 credits (~134): 42 initial + ~22 regenerations + heroes/phone heroes.
- Lesson: "upper third is one calm surface" makes nano_banana bake in flat bands / split panels. Ask for the
  same scene continuing as soft out-of-focus background, "one continuous photograph — no borders, bands,
  panels, split frames". For people, ask for a plain wall filling the side/top the text goes on.
- Outpaint of a dark hero can come back as a pasted rectangle — check it; a native 9:16 generation worked better.
- Template: `hero_theme: "light"` (dark ink/nav on bright photos), `band.theme: "light"`, and a short-phone
  rule (max-height 700px) that tightens hero type so the button stays above the product.
- Workflow helpers: data/fetch_generated.py, grid_sheet.py (10% grid for protect boxes), render_lead.py,
  phone_sheet.py (390px review).
- (later) JewelryFactory ad 13 regenerated: a laser can't spark from nowhere — the bracelet now lies on a laser
  bed, beam from the laser head onto the engraving plate, no hands. Rule: every physical process in an image
  must be physically plausible (tool present, acting on the right part).
- Collected 039/051/054 via `src.collect.run` (all three are resellers of international hair brands).
  Built It's My Deal (051) → /p/mydeal-5b7e19c2: bold colour-block studio look; overlay subs Hebrew-only
  (brand names moved to the primary text). ~60 Higgsfield credits.
- `hero_bg_color` (per client): the desktop hero's side fill colour, so a warm photo doesn't fade into the
  default green-black.
- 2026-09-26 — two more WhatsApp leads, both live:
  - Zaban (088) REJECTED on inspection: 26 branches, 150+ employees, since 1975 (zaban.co.il/about) — a chain.
    Check an "About"/branches page before building a jewellery lead.
  - Hair Cosmetics (039) → /p/haircosmetics-8b8eb022: tone-on-tone plaster studio (one soft colour per ad,
    arches, product texture as the hero detail), curls/straight hair from behind.
  - Jackson Jewelry (086, family business since 2005, factory store Ramat Gan) → /p/jackson-18bceed3:
    sun-drenched Mediterranean skin editorial (golden hard light, leaf shadows, linen, limestone).
    The product data from collect had wrong images for Nili/Sania — re-fetched og:image per product page.
  - ~110 Higgsfield credits for both (1148 → 1038), incl. ~10 regenerations.
- Lessons: at 9:16 with people the model often bakes a flat colour band above the subject (or a hard seam) even
  with the no-bands wording — move that ad to 4:5 rather than retry. Arches/niches put vertical edges exactly
  where centred text goes; ask for "one flat seamless wall, no arches" when the text needs the top. The model
  invented a label ("BIOTOP") on a jar once — name the exact label words in the prompt and forbid others.
  Never "14K" (or any Latin) in overlay lines — it scrambles RTL; write "14 קראט". Band quotes (handwriting)
  must stay short (≤ ~18 chars) or they clip on a 375px phone.
- 2026-09-26 (later) — Home page (`/`) is now Eran's about page (web/base44/src/pages/Home.jsx): hero with his
  Higgsfield Soul "Eran" photo (bald, glasses; files in public/home/), story, 17 years, 6 things you get, how it
  starts (look → free campaign page → work), fixed monthly price, WhatsApp CTA. Phone hero: photo pinned to the
  bottom at full width so the words never reach his face.
- Pet discovery: `discover.run(browser, keyword=...)` with pet keywords (חיות מחמד, מזון לחתולים …) → 34 advertisers.
  Built Kelev Teva (026-024, "health store for dogs", Moshav Beit HaLevi) → /p/kelevteva-369078b4 (warm natural
  golden-light editorial) and Pet Best (026-012, pet supermarket, Ramat Yishai) → /p/petbest-20bd483a (bright home
  lifestyle). Other qualified pet leads with WhatsApp: Mega Pet (021), Kolbo (029), Pet Sale (018), Pets-online (034),
  Dr Food (026, also a vet clinic), Kef Lahayot (002) and Crazy Pet (006, no IG).
- Lessons: the model invents packaging for loose products (Wiggle buffalo ears) — say "loose chews, no bag, no
  label". With a pasted-looking room band on top, re-prompt as "one real photograph taken in one room, the top
  third is the plain wall, no collage / inset / seams" — that fixed all five. Animals' faces get protect boxes too.

## 2026-09-26 (evening) — CRM, lightbox fix, new home photos
- **Lightbox X fix** (all client pages): the X now renders outside `.lb` as a fixed `.lbx` button (z-index max, safe-area aware), plus a second "סגירה" button under the copy. Verified live on mobile tap + desktop click, 3 pages.
- **CRM** at `/crm` (`src/pages/Crm.jsx`): Base44 login + `role === 'admin'`, and the `LeadCRM` entity has admin-only RLS on every operation (anonymous API read returns `[]`).
  Per lead: page link, website/FB/IG links, WhatsApp number, editable first message (autosaves on blur), wa.me link with the message prefilled, copy button, status select (חדש / נשלח / נענה / נקבעה פגישה / נסגר / לא מעוניין / לא רלוונטי) that stamps `last_contact_date`, notes. Filter tabs with counts.
  Seed: `data/crm/seed.py` → `seed.json` (9 published leads, messages in Eran's voice). New leads: add a row with `create_entities` (entity `LeadCRM`).
- Leads 076 (Stav) and 066 (B-scents) set to `published` with `client_page`.
- **Home photos** replaced with the cinematic dark set from Higgsfield history (nano_banana_flash, 928×1152): hero 4b737cbb, story 6360cdd0, end c6dbc1bc. More in the same series: 753a4f8a, b16c1144, a5148b6f, 0c8c9086, 0b894934, d0893915, 4204d371, a0d1e0cc, d07635b7.
  Hero photo edges are masked into the page colour; short phones (≤720px tall) get an 84% photo so the buttons never cover the face.
