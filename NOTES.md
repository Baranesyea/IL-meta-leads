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
