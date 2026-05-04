# Next session — first prompt seed

When you're ready to resume, paste this into Claude (the chat layer) to
bootstrap context:

> Resuming votedonbylocals work. Read `_strategy/HANDOFF.md` and
> `_strategy/TRACKED.md` to get current state. Last session (May 4) closed
> with 6 PRs merged: sitemap+robots, Tailwind CDN kill, header/footer
> inlining, dateModified plumbing, and inliner --check / --refresh tooling.
> Next workstreams confirmed: (1) master plan step 5 — OG image generation,
> and (2) best-new-coffee-shop per-page meta. We can take them in either
> order. My slight preference is to start with best-new-coffee-shop since
> it's smaller and closes steps 2 and 3 to 100%, but happy to lead with
> OG images if you think the visual design pass should come first.

Why this works: HANDOFF gives you the end-of-last-session snapshot,
TRACKED gives the open items. Together they're enough to propose
next-workstream options without re-reading old chat transcripts.

## Workstream A: best-new-coffee-shop per-page meta

**Pre-work to expect:**
- Investigation pass: read current state of
  `rankings/best-new-coffee-shop.html` head, identify what meta is
  present vs missing.
- Design decisions to surface BEFORE any code:
  1. JSON-LD schema type — `LocalBusiness` vs `CafeOrCoffeeShop`?
     The latter is more specific but requires more fields. Pick one
     and document the reasoning in DECISIONS.md.
  2. Required JSON-LD fields — address, hours, geo coordinates,
     priceRange, openingHoursSpecification, etc. Operator must
     confirm which fields have real data vs which would require
     fabrication. Anti-fabrication ethos: only ship fields where
     data is truthful.
  3. OG block — full Twitter Card + Open Graph. Site convention is
     in canonical chrome; check for asymmetries.
  4. Canonical URL form — `.html` per project convention (DECISIONS).
  5. Inclusion in dateModified backfill — does this page get
     datePublished + dateModified after JSON-LD lands? Probably
     yes; trigger PR #8's mechanism on this page.
- Estimated scope: ~1 day. Half schema design, half page edits.

**Why start here (slight preference):**
- Smaller scope than OG images.
- Closes step 2 + step 3 to 100%.
- Unblocks BreadcrumbList workstream (deferred per DECISIONS #15).
- Doesn't touch URLs — safe during the May 7–20 GSC quiet window if
  it slips into that period.

## Workstream B: master plan step 5 — OG image generation

**Pre-work to expect:**
- Visual design decision FIRST, before any code:
  - What does an OG image for "Best Pizza in Charleston" look like?
  - What does one for "FIG" (a single restaurant) look like?
  - Should ranking-page images and detail-page images share a
    template, or be visually distinct categories?
  - Brand-orange / cream / dark colors carry over from chrome.
  - Typography: Poppins for display, DM Sans for body — same as
    site chrome. Reinforces brand recognition in shared previews.
- Build approach decision:
  - Recommended: HTML/CSS template rendered via headless browser
    (Playwright). Python script that takes a slug, populates the
    template, screenshots at 1200×630, writes PNG to
    `assets/images/og-{slug}.png`.
  - Alternatives: Figma batch export (one-off, harder to update
    when restaurants change), hand-designed-per-image (highest
    quality ceiling, doesn't scale).
- Scope: ~42 images.
  - 8 ranking pages: og-best-pizza.png, og-best-burger.png,
    og-best-coffee-shops.png, og-best-tex-mex.png,
    og-best-nice-restaurants.png, og-best-casual-spots.png,
    og-best-new-restaurants.png, og-best-new-coffee-shop.png
  - 33 detail pages: og-{restaurant-slug}.png each
  - 1 site default: og-default.png (for index, about, etc.)
- Estimated scope: 1–2 days. Half visual design, half pipeline build,
  some time for export + verification.

**Why this might lead instead:**
- The og:image URL is ALREADY DECLARED in every page's chrome via
  `<meta property="og:image" content="...og-{slug}.png">`. Today
  every one of those URLs 404s. Shipping step 5 fulfills the
  existing promise. The longer this is deferred, the more time
  passes with broken share previews.
- Visual design takes longer than meta workstream — getting it
  started sooner means iteration cycles can begin.

## What NOT to start without thinking

The four surfaced follow-ups in TRACKED are all valid candidates for
quick wins, but each has a real reason it's not at the top:
- Pre-commit hook for --check: setup-friction tax for solo dev
- dateModified maintenance discipline: process question, not code
- Hero dot-pattern brand-color duplication: 30 min, not blocking
- Active-nav highlighting: would need per-page injection logic in
  the inliner — bigger than it looks
