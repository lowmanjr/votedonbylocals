# Tracked items — centralized

The single source of truth for outstanding follow-ups across the project. Three categories:

1. **Open one-off items** — single-edit fixes that don't depend on other work. An operator with 10 minutes can pick any of these off.
2. **Tracked workstreams** — multi-step efforts that need a coherent block of focused work but aren't yet on the master plan.
3. **Deferred for later master-plan steps** — explicitly held items that will be addressed when the master plan reaches the right step. Not blocked on judgment; blocked on sequencing.

When an item resolves, move it to the bottom under "## Resolved" with a brief note on the resolution. When a new item arises, add it to the right category.

---

## Open one-off items

Single-line edits, mostly to JSON-LD `servesCuisine` values or content fields. Each can be resolved independently.

### Editorial promotion items (1 item)

- **`best-new-restaurants` Top 4 → Top 5 promotion.** Page currently has 4 entries; subtitle reads "Four standouts — with more to come." Promote to Top 5 on the next refresh **only when a real 5th candidate exists**. Do NOT fabricate a 5th from training data — the whole reason this is a tracked item is that the project explicitly opposes the kind of fabricated content this would be. The Top-4 framing was made intentional, not a gap, so the page is fine as-is until a real 5th lands.

### Netlify pretty-URL canonical asymmetry (1 item)

- **Configure redirect rule for no-`.html` → `.html`.** Netlify currently 200-dual-serves both forms (identical Etag, no redirect). Internal anchors get `.html` stripped by Netlify pretty-URL post-processing; canonical/og:url/JSON-LD all declare the `.html` form. Google honors the canonical, so functionally fine — this is a structural cleanup, not a bug fix. **Attempted in workstream H bulk port (reverted):** `/restaurants/:slug /restaurants/:slug.html 301!` creates an infinite loop because Netlify's `:slug` placeholder matches segments containing `.html` and the `!` flag forces the rule on already-redirected paths (foo.html → foo.html.html → foo.html.html.html…). A working fix likely needs either (a) a two-rule pattern with an explicit `/restaurants/*.html /restaurants/:splat.html 200` passthrough rewrite preceding the 301, or (b) `pretty_urls = false` in netlify.toml to disable Netlify's anchor rewriting at the source. Either approach must be preview-tested in an isolated PR before merge. Discovered during workstream H bulk port PHASE 8 verification.

### Hero dot-pattern brand-color duplication (1 item)

- **`index.html` inline `<style>` hardcodes `#E67E22`.** The `.bg-dot-pattern` rule at index.html:51-57 (hero pattern background, only used on the homepage) hardcodes the brand-orange hex rather than referencing the `brand.orange` token from `tailwind.config.js`. Functionally fine today, but if the brand-orange value ever changes, the hero pattern will silently retain the old color. Resolution options: (a) move the rule into `src/input.css` as a `@layer components` block using `theme('colors.brand.orange')` so it tracks the config; (b) leave inline and add a comment cross-referencing `tailwind.config.js` so future-maintainer-self gets a heads-up. Decided not to bundle into the step-4 migration to keep that PR's scope tight. Surfaced during step-4 PHASE 0 investigation.

---

## Tracked workstreams

Multi-step efforts. Each has a description, prerequisite, and rough scope estimate.

### `best-new-coffee-shop.html` per-page meta harmonization

**Current state:** During step 1, the chrome of `best-new-coffee-shop` was harmonized to canonical KEEP blocks (GA, fonts, Tailwind config, body classes, header/footer pattern), but the per-page meta (title, description, OG tags, JSON-LD) was deliberately not touched. The page currently has:
- A `<title>` and `<meta description>` in single-winner style (kept).
- No canonical URL, no Open Graph tags (`og:url`, `og:image`, `og:site_name`, `og:description`), and no Twitter card.
- No JSON-LD at all.

**Why it's tracked, not done now:** This page would need a `LocalBusiness` (or `CafeOrCoffeeShop` if matching the coffee-shops convention) JSON-LD schema, not the `ItemList` of items the canonical uses. That's a different schema profile with different required fields (address, hours, geo coordinates if available, price range, openingHours, etc.). It deserves its own design pass rather than being shoehorned into the canonical's ranking-list shape.

**Why it matters:** This is the only featured-winner page on the site today. If the project adds more (e.g., `best-new-bar`, `best-new-bakery`) the schema decision and the meta-conventions decided here become the template for all future single-winner pages. Worth getting right rather than rushing.

**Estimated scope:** ~1 day. Half of it is schema design (which `LocalBusiness` fields to populate, which to omit, how to handle hours-data accuracy); half is page edits (canonical URL, full OG block, Twitter card, JSON-LD).

**Path forward:** Either roll into step 7 (final polish) or split off as its own micro-workstream when the operator wants to add a second featured-winner page.

### Detail-page Locations module (multi-location restaurants)

**Files affected:** `rankings/_detail-page-template.html`, `scripts/generate_detail_page.py`, `data/restaurants.json` (schema extension), affected detail pages.

**Current state:** Per DECISIONS #14.4, multi-location restaurants ship with primary-location only in the pilot. Toni's Detroit Style Pizza has a second location (Wando/Daniel Island, 1171 Clements Ferry Rd, 29492) currently absent from its detail page. D'Allesandro's Pizza has two additional locations (Nexton Square Summerville, Greenville) currently absent. Pages are correct as-shipped — they just don't yet show the additional locations.

**Why it's tracked, not done now:** Designing the Locations module against a single multi-location restaurant in the pilot would over-fit. Better to design once a second multi-location restaurant lands in a different ranking page and we have two independent test cases. The design needs to handle: per-location `Place` microdata in JSON-LD, visual presentation of multiple locations in the sidebar, and how to handle locations across cities (when the editorial scope from #14.1 expands beyond greater Charleston).

**Trigger to activate:** ACTIVATED 2026-05-03 by Babas on Cannon (3 locations: Cannon, Meeting, Wentworth) during best-coffee-shops port. Workstream H bulk port surfaced 7 additional multi-location restaurants. Full in-scope set as of 2026-05-04: **8 from workstream H** (babas-on-cannon, heavys-barburger, home-team-bbq, santis, senor-tequilas, azul-mexicano, agaves-cantina, bon-banh-mi-southeast-asian-kitchen) plus **3 from prior PRs** (tonis-detroit-style-pizza, dallesandros-pizza, second-state-coffee) — 11 total, all shipping primary-location-only. Design pass is the next gated workstream — not folded into bulk port.

**Estimated scope:** 1–2 days. Half template + script work; half per-location data collection for the affected restaurants.

### Title verbosity for cuisine-name overlap

**Files affected:** detail-page `<title>` rendering in the generator script; possibly the JSON schema (new optional `titleCuisine` override field).

**Current state:** Toni's Detroit Style Pizza ships with `<title>Toni's Detroit Style Pizza — Detroit Style Pizza in Charleston | Voted On By Locals</title>`. Correct given the data; verbose because `name` and `cuisine` overlap. Affects any restaurant whose name contains its cuisine.

**Why it's tracked, not done now:** Pilot is small enough that the verbosity is manageable. The fix (an optional `titleCuisine` override in JSON that the script uses in the title only when present) is one line of script + one optional field, but designing it against just Toni's risks overfitting.

**Trigger to activate:** at the editorial flesh stage for affected restaurants, OR when bulk port reveals more cuisine-name-overlap cases.

**Estimated scope:** ~30 min — add `titleCuisine` to the JSON schema (null by default, optional override), update step 12 in the script to fall back to `cuisine` when `titleCuisine` is null.

### BreadcrumbList schema across rankings + details

**Files affected:** all 8 ranking pages, the detail-page template, all detail pages.

**Current state:** No `BreadcrumbList` JSON-LD anywhere on the site. Considered and deferred during step 3. Ranking-only (`Home → Best Pizza`) is mechanical but low-value as a 2-node breadcrumb. The high-value case (`Home → Best Pizza → {Restaurant}`) requires touching the detail-page template, which was out of step 3 scope.

**Why it's tracked, not done now:** The high-value version requires the detail-page template work; doing only the ranking-side version locks in a 2-node-only convention that gets retrofitted later anyway. Cleaner to add ranking + detail breadcrumbs in one pass once detail-page coverage is global.

**Trigger to activate:** after the bulk-port workstream completes (or as a stage of it, on a per-ranking basis as detail pages ship per ranking).

**Estimated scope:** ~2 hours — one schema block in the ranking template + one in the detail-page template, plus per-page rendering for the 8 rankings and ~37 detail pages.

### dateModified maintenance discipline

**Files affected:** detail pages and ranking pages going forward.

**Current state:** 40 pages now carry `datePublished` + `dateModified` JSON-LD fields, both seeded from git-creation-date. `dateModified` is intended to update only when editorial content changes — not on chrome edits.

**Why it's tracked:** No process today guarantees that operator remembers to bump `dateModified` on editorial edits. Risk: stale `dateModified` silently mismeasures content freshness for crawlers. Discipline-only solution today; a pre-commit hook or generator enhancement could automate.

**Estimated scope:** depends on chosen approach. Pre-commit hook = ~30min. Generator-flag-driven update = ~1hr. Pure documentation discipline = no code, just a note in HANDOFF.md or PR template.

**Trigger to activate:** when a discrepancy surfaces (e.g., a sitemap audit shows stale `dateModified` vs actual editorial activity), or when a build pipeline / CI is introduced that could host the hook.

---

## Deferred for later master-plan steps

These are explicitly held until the master plan reaches the right step. They aren't blocked on operator judgment — they're blocked on sequencing.

- **OG image generation** — Master plan **step 5**. Canonical references `og:image` URLs at `https://votedonbylocals.com/assets/images/og-{slug}.png` for all 7 ranking pages; none exist yet. Detail pages from step 2 will multiply the need (~37 more). Build all in one Figma file, export in batch.

- **Vote aggregation pipeline** — Not on the master plan; **strategic deferred**. See `_strategy/CONTEXT.md` → "Things deferred but important." Currently votes go to Netlify Forms; rankings are hand-curated. Building a real aggregation backend (Google Sheets / Airtable / a small JSON file) is a prerequisite for `aggregateRating` JSON-LD, for any visible "live vote totals," and for the flywheel-hypothesis claim flow.

- **Fraud prevention** — Not on the master plan; **strategic deferred**. Tied to vote aggregation. Self-reported zip is the only check today; gameability gets worse with any visible vote count.

- **Restaurant claim flow** — Not on the master plan; **strategic deferred**. Pairs with monetization path B. Prerequisite: detail pages exist (step 2).

- **Multi-city templating** — Not on the master plan; **strategic deferred**. The single biggest "unblocking" decision the project has but explicitly held until Charleston is a stronger foundation. See `_strategy/CONTEXT.md` for the full framing.

---

## Resolved

- **2026-05-04 — Inliner detection-check (`--check` flag) + marker retrofit.** `scripts/inline_chrome.py` now wraps inlined chrome in `<!-- AUTOGENERATED FROM components/* -->` markers; new `--check` mode detects divergence between inlined chrome and `components/` source-of-truth. Exit 0 if synced, 1 if divergent, 2 if markers missing. `--verbose` appends per-file unified diff. All 49 production HTML pages retrofitted with markers in the same PR. Hardens the source-of-truth pattern from PR #7 — divergence from `components/` is now detectable rather than silent. Pre-commit hook deferred: `--check` is invoked on-demand today; hooking can wire it into the git lifecycle later if divergence becomes a real problem in practice. No setup-friction tax until that's needed.

- **2026-05-04 — `dateModified` plumbing + sitemap `<lastmod>`.** 33 detail pages + 7 ranking pages = 40 pages now carry `datePublished` and `dateModified` in their JSON-LD, seeded from git-creation-date via `git log --diff-filter=A --format=%aI`. Sitemap emits `<lastmod>` for those 40 pages; the 5 root pages and `best-new-coffee-shop.html` omit it (URL count unchanged at 46). `scripts/add_dates_to_rankings.py` retained as one-shot reference; the detail-page generator now preserves existing dates on regeneration so operator-maintained `dateModified` survives re-runs. Maintenance workflow (operator updates `dateModified` on editorial edits) is tracked separately above.

- **2026-05-04 — Build-time header/footer inlining (master plan step 7, partial).** `components/header.html` and `components/footer.html` now inlined at build time across all 49 pages via `scripts/inline_chrome.py`. `components/` retained as editable source-of-truth (operator edits there, re-runs inliner, commits). Eliminates runtime fetch + FOUC + JS-disabled-empty-nav. `main.js` reduced from 44 to 11 lines. Step 7 (final polish) is broader than this one workstream; the inlining piece is now resolved.

- **2026-05-04 — Tailwind CDN → local built.css (master plan step 4).** All 49 pages migrated from `<script src="cdn.tailwindcss.com">` + the 19-line inline `tailwind.config` block to `<link rel="stylesheet" href=".../assets/css/built.css">`. New tooling: Tailwind v3.4.19 as devDependency, `npm run build:css` produces ~20KB minified output, `scripts/migrate_chrome.py` retained as reference for future mass chrome edits. Eliminates ~3MB of blocking JS at runtime plus the JIT FOUC cycle. `assets/css/style.css` reduced to 4 lines (Tailwind now emits `.font-poppins`). Bonus fix: `index.html` `rel="canonical"` added (was `og:url`-only — surfaced during PR #5 investigation). One new Open one-off surfaced: hero dot-pattern hardcoded brand color (see above).

- **2026-05-04 — `sitemap.xml` (master plan step 6).** 46-URL sitemap live at `https://votedonbylocals.com/sitemap.xml`. Filesystem-scan generator at `scripts/generate_sitemap.py` excludes `_*` working files and `thank-you.html` (the latter also gets `<meta name="robots" content="noindex">`). No `lastmod` — `dateModified` plumbing deferred to a follow-up workstream. See merged PR #5.

- **2026-05-04 — `robots.txt` (master plan step 6).** Allow-all crawl with explicit `Disallow: /rankings/_` for the working-file templates that ship to production but should not be indexed. Sitemap directive points at the production sitemap URL. See merged PR #5.

- **2026-05-03 — Doc consistency: 5-top-level-pages workstream placement.** Resolved via three small edits anchoring the workstream to step 4 as an explicit prerequisite. See commit f66cd17 and DECISIONS log entry context. (Workstream itself remains tracked above — only the placement-fuzziness was resolved.)

- **2026-05-03 — Step 2 pilot port (best-pizza, 5 of ~37 detail pages).** Pilot ships 5 detail pages at /restaurants/{slug}.html with full chrome, JSON-LD, address/hours/phone/price/website where data exists. Generator script (commit 9c6b3f7) is reusable for the bulk port. Strategic decisions captured in DECISIONS #14. Bulk port for the remaining ~32 pages tracked above as a separate workstream.

- **2026-05-03 — canonical-template boilerplate removed from 7 ranking pages.** Initially scoped as a single-file cleanup on `best-pizza.html`. Pre-flight grep found the boilerplate was actually propagated to all 7 ranking pages during step 1 harmonization, plus an extended page-deviation note on `best-new-restaurants.html`. Resolved per D2: full delete from 6 pages, surgical rewrite preserving the page-specific deviation note on the 7th. Convention-level notes (emoji reuse, vote-count absence, favicon-vs-OG asymmetry) verified durable in DECISIONS #1 / #2 / #10 before delete. See commit 902c584.

- **2026-05-03 — 5 top-level pages chrome upgrade.** about.html, vote.html, suggest-category.html, ambassadors.html, and thank-you.html now share the canonical chrome (inline Tailwind config + font preconnect/stylesheet + canonical body classes). Side effect: focus:border-brand-orange / focus:ring-brand-orange Tailwind variants on form inputs now resolve correctly (were silent no-ops before — variants need brand-orange in Tailwind's config, which only the inline config provides). Sibling commit pruned 2 redundant style.css declarations + 2 redundant rules (DECISIONS #11). .font-poppins retained pending step 4. Unblocks PLAN.md step 4. See commits 689d3d2 (chrome upgrade) and f60c5e5 (style.css prune).

- **2026-05-03 — Best-coffee-shops detail-page port (5 of ~37, workstream H 1/7).** First ranking-page bulk port. 5 detail pages shipped (Harken Cafe, Sightsee, Babas on Cannon, Second State Coffee, The Harbinger Cafe & Bakery), all schemaType=CafeOrCoffeeShop. Step-3 cross-linking applied in same PR. Multi-location restaurants (Babas, Second State) ship primary-location only per #14.4 — Babas tripped the Locations module trigger. See merged PR #3 commits.

- **2026-05-03 — Workstream H bulk port (24 detail pages across 5 rankings).** 23 unique restaurants (Home Team BBQ shared between best-burger and best-casual-spots) covering 24 ranking-row entries. Closes the bulk-port workstream for all 7 multi-entry rankings (best-pizza pilot + best-coffee-shops + workstream H's 5 rankings = 7 of 7). The featured-winner page best-new-coffee-shop remains separate per its own tracked workstream. Step-3 cross-linking applied in same PR (5 commits, one per ranking). Reconciliations: San Miguel locality → Mt Pleasant, Chico Feo locality → Folly Beach, Edmund's Oast locality → North Charleston, Bar Weems locality → North Charleston, Azul Mexicano cuisine → Mexican. See workstream-h-bulk-port branch commits (bd958c1 data, 0ff23d3 detail pages, b0bb27e/e54137b/c916543/4d6da5a/051e5b9 step-3 cross-link).

- **2026-05-03 — Multi-entry AppearsOn handling in generator script.** Triggered by Home Team BBQ (best-burger + best-casual-spots) during workstream H bulk port. Script's step 12 now clones the template's single-entry `<li>` block per appearsOn entry. Byte-equality preserved for single-entry case (verified against park-pizza-co regeneration → no diff). See commit 776b374.

- **2026-05-03 — Cuisine-flag verifications (4 items).** Resolved during workstream H bulk port. Chico Feo confirmed `Caribbean-influenced` on the ranking page, with `Caribbean` used as the detail-page schema value. Vern's confirmed `New American`. Home Team BBQ on best-burger row confirmed `Barbecue` (no change). Azul Mexicano flipped from `Tex-Mex` to `Mexican` per the "Modern Aesthetic" tagline reading. Other defensible values (Moe's `Burgers`, Lowland `Burgers`, other Tex-Mex `Tex-Mex`) retained as-is. See commits b0bb27e (best-burger) and e54137b (best-tex-mex Azul flip).
