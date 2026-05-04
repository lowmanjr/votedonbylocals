# Next session — first prompt seed

When you're ready to resume, paste this into Claude (the chat layer) to
bootstrap context:

> Resuming votedonbylocals work. Read `_strategy/HANDOFF.md` and
> `_strategy/TRACKED.md` to get current state. Last session
> (May 4 afternoon) closed with 3 PRs merged: #12 (best-new-coffee-shop
> per-page meta + JSON-LD — closed master plan steps 2 + 3 to 100%),
> #13 (PLAN.md / HANDOFF.md doc reconciliation — HANDOFF is now source
> of truth for per-step status), and #14 (hero dot-pattern tokenization).
> The unambiguous next major workstream is master plan step 5: OG
> image generation. Lead with it.

Why this works: HANDOFF gives you the end-of-last-session snapshot,
TRACKED gives the open items. Together they're enough to propose
next-workstream options without re-reading old chat transcripts.

## Lead workstream: master plan step 5 — OG image generation

**Pre-work to expect:**

- Visual design decision FIRST, before any code:
  - What does an OG image for a ranking page ("Best Pizza in Charleston") look like?
  - What does one for a detail page ("FIG") look like?
  - Should ranking-page images and detail-page images share a template, or be visually distinct categories?
  - Brand-orange / cream / dark colors carry over from chrome.
  - Typography: Poppins for display, DM Sans for body — same as site chrome. Reinforces brand recognition in shared previews.
- Build approach decision:
  - Recommended: HTML/CSS template rendered via headless browser (Playwright). Python script that takes a slug, populates the template, screenshots at 1200×630, writes PNG to `assets/images/og-{slug}.png`.
  - Alternatives: Figma batch export (one-off, harder to update when restaurants change), hand-designed-per-image (highest quality ceiling, doesn't scale).
- Scope: ~42 images.
  - 8 ranking pages: og-best-pizza.png, og-best-burger.png, og-best-coffee-shops.png, og-best-tex-mex.png, og-best-nice-restaurants.png, og-best-casual-spots.png, og-best-new-restaurants.png, og-best-new-coffee-shop.png
  - 33 detail pages: og-{restaurant-slug}.png each
  - 1 site default: og-default.png (for index, about, etc.)
- Estimated scope: 1–2 days. Half visual design, half pipeline build, some time for export + verification.

**Why this is the lead:**

- The og:image URL is ALREADY DECLARED in every page's chrome via `<meta property="og:image" content="...og-{slug}.png">`. Today every one of those URLs 404s. Shipping step 5 fulfills the existing promise. The longer this is deferred, the more time passes with broken share previews.
- URL-stable (adds asset files only, no URL changes) — safe during the May 7–20 GSC quiet window.

## Other workstreams ready in TRACKED (not the lead)

Surface only if the operator explicitly redirects:

- **BreadcrumbList schema** — eligible as of May 4 (bulk port done; step 2 + step 3 at 100%). ~2 hours.
- **Detail-page Locations module** — 11 multi-location restaurants queued. 1–2 day design-first workstream.
- **Netlify pretty-URL canonical asymmetry** — discrete config-only PR. DO NOT START during May 7–20 GSC window. Either pre-window with full preview-isolation, or post-May-20.
- **Title verbosity for cuisine-name overlap** — ~30 min. Trigger when bulk port reveals more cases.

## What NOT to start without thinking

- Active-nav highlighting: would need per-page injection logic in the inliner — bigger than it looks.
- Pre-commit hook for `--check`: setup-friction tax for solo dev.
- `dateModified` maintenance discipline: process question, not code.
