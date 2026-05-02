# Tracked items — centralized

The single source of truth for outstanding follow-ups across the project. Three categories:

1. **Open one-off items** — single-edit fixes that don't depend on other work. An operator with 10 minutes can pick any of these off.
2. **Tracked workstreams** — multi-step efforts that need a coherent block of focused work but aren't yet on the master plan.
3. **Deferred for later master-plan steps** — explicitly held items that will be addressed when the master plan reaches the right step. Not blocked on judgment; blocked on sequencing.

When an item resolves, move it to the bottom under "## Resolved" with a brief note on the resolution. When a new item arises, add it to the right category.

---

## Open one-off items

Single-line edits, mostly to JSON-LD `servesCuisine` values or content fields. Each can be resolved independently.

### Cuisine-flag verifications (4 items)

These were authored during the migration with the "if uncertain" rule (use a defensible value, flag for operator verification, don't block on it).

- **`best-casual-spots.html` / Chico Feo.** Shipped: `servesCuisine: "Caribbean-influenced"`. Operator (John) to verify and finalize. Alternatives if menu-actual differs: `Caribbean`, `Latin American`, `Lowcountry`. Single-line JSON-LD edit when finalized.

- **`best-nice-restaurants.html` / Vern's.** Shipped: `servesCuisine: "New American"`. Operator to verify. Bistro-leaning — could read as `French Bistro`, `Continental`, or `Contemporary American` depending on framing. Single-line JSON-LD edit.

- **`best-burger.html` / cuisine values.** Shipped: 4 × `Burgers` + 1 × `Barbecue` (the `Barbecue` is on Home Team BBQ, which is unambiguously a BBQ joint listed for its burger — disambiguated correctly). Operator may want to refine the others: Moe's Crosstown Tavern → `American Tavern`, Lowland → `American`. Up to operator preference; current values are defensible.

- **`best-tex-mex.html` / cuisine values.** Shipped: 5 × `Tex-Mex`. Azul Mexicano in particular ("Modern Aesthetic" tagline) may read better as `Mexican` rather than `Tex-Mex`. Operator to refine if desired.

### Editorial promotion items (1 item)

- **`best-new-restaurants` Top 4 → Top 5 promotion.** Page currently has 4 entries; subtitle reads "Four standouts — with more to come." Promote to Top 5 on the next refresh **only when a real 5th candidate exists**. Do NOT fabricate a 5th from training data — the whole reason this is a tracked item is that the project explicitly opposes the kind of fabricated content this would be. The Top-4 framing was made intentional, not a gap, so the page is fine as-is until a real 5th lands.

---

## Tracked workstreams

Multi-step efforts. Each has a description, prerequisite, and rough scope estimate.

### Upgrade 5 top-level pages to canonical chrome

**Files:** `about.html`, `vote.html`, `suggest-category.html`, `ambassadors.html`, `thank-you.html`.

**Current state:** These 5 pages are still on the pre-canonical chrome pattern: no inline Tailwind config, no font preconnect+link, body uses bare `antialiased` instead of the full canonical body classes (`antialiased bg-brand-cream text-brand-dark min-h-screen flex flex-col`). They depend on `style.css`'s plain-CSS class duplications (`.bg-brand-orange`, `.border-brand-orange`, `.font-poppins`, the `@import` for Google Fonts, and hardcoded body background/color) to render correctly.

**Why it's tracked, not done now:** Doing the upgrade is mechanically simple but touches 5 pages and changes how visual styles cascade. Wanted the ranking-page migration to land cleanly first.

**Why it matters:**
- Prerequisite for completing `style.css` pruning (5 of 6 deletions are blocked on this; see also `_strategy/DECISIONS.md` #11)
- Prerequisite for site-wide visual consistency
- Prerequisite for the future "kill Tailwind CDN" workstream (master plan step 4) — that step needs to apply uniformly across all pages, not just rankings

**Estimated scope:** Each page needs ~20 lines added to `<head>` (inline Tailwind config, font preconnect, fonts link) and ~5 classes added to `<body>`. No body content changes required.

**Order of operations when ready:** (1) upgrade the 5 pages → (2) verify all 14 routes still render → (3) delete the 5 blocked `style.css` rules (one of which is the body rule's `background-color`/`color` declarations rather than a whole-rule deletion) → (4) verify again. Same dependency-audit-then-execute pattern used in CLEANUP 1.

### `best-new-coffee-shop.html` per-page meta harmonization

**Current state:** During step 1, the chrome of `best-new-coffee-shop` was harmonized to canonical KEEP blocks (GA, fonts, Tailwind config, body classes, header/footer pattern), but the per-page meta (title, description, OG tags, JSON-LD) was deliberately not touched. The page currently has:
- A `<title>` and `<meta description>` in single-winner style (kept).
- No canonical URL, no Open Graph tags (`og:url`, `og:image`, `og:site_name`, `og:description`), and no Twitter card.
- No JSON-LD at all.

**Why it's tracked, not done now:** This page would need a `LocalBusiness` (or `CafeOrCoffeeShop` if matching the coffee-shops convention) JSON-LD schema, not the `ItemList` of items the canonical uses. That's a different schema profile with different required fields (address, hours, geo coordinates if available, price range, openingHours, etc.). It deserves its own design pass rather than being shoehorned into the canonical's ranking-list shape.

**Why it matters:** This is the only featured-winner page on the site today. If the project adds more (e.g., `best-new-bar`, `best-new-bakery`) the schema decision and the meta-conventions decided here become the template for all future single-winner pages. Worth getting right rather than rushing.

**Estimated scope:** ~1 day. Half of it is schema design (which `LocalBusiness` fields to populate, which to omit, how to handle hours-data accuracy); half is page edits (canonical URL, full OG block, Twitter card, JSON-LD).

**Path forward:** Either roll into step 7 (final polish) or split off as its own micro-workstream when the operator wants to add a second featured-winner page.

---

## Deferred for later master-plan steps

These are explicitly held until the master plan reaches the right step. They aren't blocked on operator judgment — they're blocked on sequencing.

- **Replacing Tailwind CDN with built CSS** — Master plan **step 4**. The CDN is a real Core Web Vitals concern (~3MB JS at runtime, JIT-compiles in browser, FOUC risk). Currently in use on all 14 pages. Replacing requires either a tiny build step (Tailwind CLI) or a hosted built CSS. Prerequisites: step 2 (detail pages) so the Tailwind class set is stable, and the 5-top-level-pages chrome upgrade workstream so the migration applies uniformly.

- **Replacing client-side header/footer fetch with build-time inlining** — Master plan **step 7** (final polish). `assets/js/main.js` injects `components/header.html` and `components/footer.html` at runtime via `fetch()`. Causes mild FOUC, no nav for JS-disabled clients, slight crawl-pipeline complication. Cleaner with build-time inlining or server-side include. Defer until a build step is introduced (likely as part of step 4).

- **`sitemap.xml`** — Master plan **step 6**. Currently absent. Build after the URL set stabilizes (post-step-2 detail pages, post-step-3 schema cross-links).

- **`robots.txt`** — Master plan **step 6**. Currently absent. Trivial once `sitemap.xml` exists; the file just declares the crawl policy and points at the sitemap.

- **OG image generation** — Master plan **step 5**. Canonical references `og:image` URLs at `https://votedonbylocals.com/assets/images/og-{slug}.png` for all 7 ranking pages; none exist yet. Detail pages from step 2 will multiply the need (~37 more). Build all in one Figma file, export in batch.

- **Vote aggregation pipeline** — Not on the master plan; **strategic deferred**. See `_strategy/CONTEXT.md` → "Things deferred but important." Currently votes go to Netlify Forms; rankings are hand-curated. Building a real aggregation backend (Google Sheets / Airtable / a small JSON file) is a prerequisite for `aggregateRating` JSON-LD, for any visible "live vote totals," and for the flywheel-hypothesis claim flow.

- **Fraud prevention** — Not on the master plan; **strategic deferred**. Tied to vote aggregation. Self-reported zip is the only check today; gameability gets worse with any visible vote count.

- **Restaurant claim flow** — Not on the master plan; **strategic deferred**. Pairs with monetization path B. Prerequisite: detail pages exist (step 2).

- **Multi-city templating** — Not on the master plan; **strategic deferred**. The single biggest "unblocking" decision the project has but explicitly held until Charleston is a stronger foundation. See `_strategy/CONTEXT.md` for the full framing.

---

## Resolved

(Move items here as they complete. Include the resolution date and a brief note. Empty for now — the migration itself is documented in `rankings/_template-analysis.md` and `rankings/_port-content-sheet.md`.)
