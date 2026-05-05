# Next session — first prompt seed

When you're ready to resume, paste this into Claude (the chat layer) to
bootstrap context:

> Resuming votedonbylocals work. Read `_strategy/HANDOFF.md` and
> `_strategy/TRACKED.md` to get current state. Last session
> (May 4 evening) closed with 3 PRs merged: #16 (master plan step 5 —
> OG image generation; 42 PNGs + tooling + index.html chrome edits for
> og:image, og:site_name, and twitter:card), #17 (OG backplate fix via
> color-mix on brand.orange at 14%; 42 PNGs re-rendered), and #18
> (BreadcrumbList JSON-LD across 8 rankings + 33 details, with
> /#rankings as the schema-only intermediate URL on rankings and a
> 2-level Home → {Restaurant} structure on details).
> Master plan steps 1–6 are now done; step 7 (final polish) is the only
> formal item remaining. Future workstreams source from TRACKED, not
> PLAN. Lead: detail-page Locations module (11 multi-location
> restaurants queued, design-first, 1–2 days).

Why this works: HANDOFF gives the end-of-last-session snapshot, TRACKED
gives the open items. Together they're enough to propose next-workstream
options without re-reading old chat transcripts. The master plan is now
effectively complete — TRACKED is the working backlog.

## Lead workstream: detail-page Locations module

**Pre-work to expect:**

- Design decision FIRST, before any code. How does a multi-location
  detail page render?
  - Stacked locations within existing detail-page chrome (one H1, an
    in-body Locations section listing each address)?
  - Tab/toggle UI to switch between locations?
  - Separate sub-pages per location at `/restaurants/{slug}/{loc-slug}`
    sharing one canonical detail page?
  - Inline list of addresses as a single section?
- Data shape question. `restaurants.json` currently has single
  address/neighborhood fields per restaurant. Multi-location needs
  either an in-place `locations: [...]` array or a separate
  `locations.json` keyed by slug. The choice affects every consumer
  (detail-page generator, valuation pipeline if any, OG renderer).
- Identify the 11 affected restaurants (noted in workstream H bulk
  port) and inventory their actual address counts before designing.
- URL decision: one canonical detail URL with multi-location body, or
  separate sub-URLs per location? Affects URL-stability classification.
  One-canonical-URL is URL-stable; sub-URLs are URL-additive with
  redirect/canonical implications.
- SEO consideration: schema.org allows multiple `Place` entities under
  one `Organization`/`Restaurant`, OR separate `Restaurant` entities
  with shared `branchOf` parent. Decide before writing JSON-LD.
- Generator coupling: `_detail-page-template.html` +
  `generate_detail_page.py` produce all 33 details today. Multi-
  location support either needs template branches (single-loc vs
  multi-loc) or a unified template that handles both via array
  iteration where single-loc is just `len(locations) == 1`.

**Why this is the lead:**

- Biggest unblocked piece on TRACKED. Has been queued since the
  workstream H bulk port surfaced the second multi-location case.
- Design-first matches investigation-first session norms.
- Improves user-facing capability for restaurants with multiple
  Charleston locations — the gap is real, not cosmetic.
- URL-stability depends on the URL decision above. If the answer is
  one-canonical-URL (most likely), the workstream is fully window-safe.

## Other workstreams ready in TRACKED (not the lead)

Surface only if the operator explicitly redirects:

- **Top-level pages OG coverage** — 5 pages still have no OG block
  (about, vote, suggest-category, ambassadors, thank-you). ~2 hours,
  design-first per-page (decide unique `og-{slug}.png` or share
  `og-default.png`; author title/description per page). Adjacent to
  step-5 work, pipeline still warm. Window-safe (additive metadata).
- **OG meta-line dedup when restaurant name contains cuisine
  descriptor** — sweep-and-fix. Low priority. Filed when Harbinger
  showed "Cafe & Bakery" in name + "Café and Bakery" in cuisine.
- **Title verbosity for cuisine-name overlap** — ~30 min, trigger-based.
  Pairs naturally with the OG meta-line dedup work; could ship together.
- **GSC re-audit** — eligible May 21+ (post-quiet-window). Two weeks
  of indexing data from April SEO work plus the May schema additions.

## What NOT to start without thinking

- **Netlify pretty-URL canonical asymmetry** — discrete config-only PR.
  DO NOT START during May 7–20 GSC quiet window. Earliest safe
  restart: May 21. Pre-window window (May 5–6) was considered and
  declined this session — wrong risk profile to ship canonical handling
  3 days before a 16-day freeze.
- **Post-May-20 chrome follow-ups** — TRACKED entry includes "Add
  id='rankings' to index.html cards section" tied to PR #18's
  `/#rankings` fragment URL. Trigger: post-May-20. Schema works
  without the anchor today; the follow-up turns the fragment into a
  real on-page scroll target.
- **dateModified maintenance discipline** — trigger-based, no current
  discrepancy known. Defer until one surfaces.
- **Active-nav highlighting** — would need per-page injection logic in
  the inliner. Bigger than it looks.

## Quiet window posture

- **Today**: May 4
- **GSC quiet window**: May 7–20 (no URL changes, no canonical work,
  no risky-to-indexing edits)
- **If resuming May 5–6**: pre-window. Schema-additive + asset work
  fine. Avoid canonical/URL changes — not worth the timing risk this
  close to the freeze.
- **If resuming May 7–20**: quiet window. Schema-only and asset-only.
  Lead workstream (Locations module) is design-first which fits — the
  design pass and data-shape work can land in-window; URL/canonical
  decisions wait until after.
- **If resuming May 21+**: full menu open. Netlify pretty-URL,
  post-May-20 chrome follow-ups, GSC re-audit, Locations module
  implementation all available.
