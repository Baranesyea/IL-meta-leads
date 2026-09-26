# Design rules — ads + client page (Eran's feedback, binding)

Every rule here came from Eran reviewing real output. Check each one before showing anything.
The Stav page (`/p/stav-56f5e275`) is the reference implementation: one template for every client.

## Process
- **Review at phone size, never on a contact sheet.** Render each ad at 390px wide and look at it. The page:
  scroll the whole live URL at 390×844 and at desktop (1280×700 laptop, 1440×900) before reporting done.
- Verify on the real deployed link, not the Base44 editor preview (its dim "state" is the editor's, not ours).
- Don't stop to ask when the direction is clear — push to a finished result, then report.
- Hebrew replies to Eran; never mix Hebrew and English on one line.

## Ads (images)
- Premium, magazine-campaign feel (Vogue / perfume / watch ad). Real product must look exactly like the real
  product — pass the store's product photos as references; never invent packaging, labels or logos.
- Some creatives on a model; diverse angles **and** diverse looks (for testing) — never one template with
  different photos. Typography directions rotate: contrast, quiet, stack, note, cover, label.
- Fonts: Optimum (Light/Regular/Black) for all type; Idealist handwriting only for a signature or a short
  personal note, stroke-thickened.
- **Full bleed only.** No colour strip / panel cutting the photo, no plate/box behind text ("a compromise").
  Legibility comes from placing text in the photo's own calm space; if needed a soft band scrim feathered
  around the text (measured strength), never a box.
- **Text never touches the product, a face, lips or hands.** Hand-drawn `protect` boxes per ad, tight and
  separate (face and hand are two boxes). Keep clear air around the jewel/product.
- **Big and legible on a phone:** main line ≥ 78px on the 1080 canvas (script ≥ 92px); sub lines not faded;
  balanced wrapping (no lone last word). The pipeline measures the rendered ad and retries another look.
- Contrast: measured per ad (4.5:1 big type, 7:1 thin/script/small). Brand line hidden on busy strips.
- Baked-in black bands in generated images: crop, or outpaint the missing space (keep the original pixels).
- Hebrew text is rendered after generation (HTML/CSS), never by the image model.
- Copy: natural Israeli Hebrew, strong hooks, Meta policy (no personal-attribute claims, no fake urgency).

## Client page (one per client, `/p/<unguessable-slug>`)
- Standalone brand showcase: no menus to other clients, no internal notes. The client must say "wow".
- Same template for everyone: colours, fonts (Optimum web font), structure. Content comes from `data.js`.
- Structure: fixed bar (wordmark, nav: מה היינו משנים / הקמפיין / 20 המודעות) → HERO (full screen, the
  product visible — on phones the words sit in the photo's dark space and the product is never under text or
  shade; on desktop the whole photo, words on the other side) with a CTA button "מה היינו משנים בקמפיין שלך"
  → the review right after the hero ("עברנו על הקמפיין שלך", 4 insights, button to the campaign) → campaign
  strip → editorial split (photo above text on phones) → quote band (text in the photo's dark area, product
  clear) → 5 angle sections → closing: "<name>, את כל זה הכנו בשבילך. בחינם, בלי התחייבות." + what working
  together adds + WhatsApp button (Eran: https://wa.me/972545471522).
- Rows of ads: every image in a row has the same height (justified by aspect ratio); edge to edge on phones;
  no white caption strip under an ad.
- Campaign strip: swipe on touch, drag + arrows with a mouse, auto-drift that pauses only while interacting
  or while an ad is open — never on hover (it got stuck).
- Lightbox: close button always on top (fixed), opaque backdrop, scroll lock, closes on backdrop / Esc.
- Headlines type in on scroll (layout-stable). Hero headline sized by width **and** height so it never
  climbs into the bar on short laptop screens.
- Address the owner in the right grammatical gender (Stav: feminine).
