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

### Post-May-20 chrome follow-ups (1 item)

- **Add `id="rankings"` to the cards-grid section on `index.html`.** The BreadcrumbList JSON-LD on all 8 ranking pages declares `https://votedonbylocals.com/#rankings` as the intermediate breadcrumb URL. Schema works without the anchor today (fragment falls back to top of document on a homepage that IS the rankings index). Adding the `id` turns the fragment into a real on-page anchor that scrolls to the cards section. Single edit to one `<div>` near `index.html` line 158-160. Held until post-May-20 because it's a chrome edit during the GSC quiet window. No schema changes needed when shipped — the existing JSON-LD already references `/#rankings`. Filed by PR #18 (BreadcrumbList rollout).

### Netlify pretty-URL canonical asymmetry (1 item)

- **Configure redirect rule for no-`.html` → `.html`.** Netlify currently 200-dual-serves both forms (identical Etag, no redirect). Internal anchors get `.html` stripped by Netlify pretty-URL post-processing; canonical/og:url/JSON-LD all declare the `.html` form. Google honors the canonical, so functionally fine — this is a structural cleanup, not a bug fix. **Attempted in workstream H bulk port (reverted):** `/restaurants/:slug /restaurants/:slug.html 301!` creates an infinite loop because Netlify's `:slug` placeholder matches segments containing `.html` and the `!` flag forces the rule on already-redirected paths (foo.html → foo.html.html → foo.html.html.html…). A working fix likely needs either (a) a two-rule pattern with an explicit `/restaurants/*.html /restaurants/:splat.html 200` passthrough rewrite preceding the 301, or (b) `pretty_urls = false` in netlify.toml to disable Netlify's anchor rewriting at the source. Either approach must be preview-tested in an isolated PR before merge. Discovered during workstream H bulk port PHASE 8 verification.

### Locations workstream follow-ups (3 items)

Each is a single data update to a multi-location restaurant's `locations[]` array, triggered by an external event. Design + schema is locked (DECISIONS #17, schemaVersion 1.1); these are content adds when their triggers fire.

- **Out-of-scope re-inclusion when editorial scope expands.** Once editorial scope expands beyond greater Charleston (per DECISIONS #14.1), re-include the following multi-location secondaries currently excluded from `data/restaurants.json` `locations[]`: Home Team BBQ Aspen CO; Home Team BBQ Columbia SC; Home Team BBQ Greenville SC (Upstate); D'Allesandro's Pizza Greenville SC (Upstate). Add to the brand's `locations[]` and regenerate the affected detail pages.

- **Heavy's Barburger Isle of Palms — third location opens Spring 2026.** A third Heavy's Barburger location opens Spring 2026 on Ocean Boulevard, Isle of Palms. Add as the third entry to Heavy's `locations[]` once open. Trigger: opening confirmation.

- **Toni's Detroit Style Pizza — re-verification.** Toni's exited the Locations workstream 2026-05-05 because the Clements Ferry (Wando/Daniel Island) second location closed (Yelp marked closed June 2025; official site lists only Mt Pleasant). Trigger to re-add Toni's to the workstream and populate `locations[]`: reopening announcement, OR operator-confirmed verification that the closure signal was wrong.

---

## Tracked workstreams

Multi-step efforts. Each has a description, prerequisite, and rough scope estimate.

### Detail-page Locations module (multi-location restaurants)

**Files affected:** `rankings/_detail-page-template.html`, `scripts/generate_detail_page.py`, `data/restaurants.json` (schema extension), affected detail pages.

**Status (2026-05-05):**
- Design pass completed 2026-05-05 — data shape, JSON-LD pattern, UI pattern locked (see DECISIONS #17).
- Schema v1.1 shipped in PR #19. Template + generator + Babas pilot shipped in this PR; pilot validates the multi-location rendering pattern with 2 secondaries (Meeting Street + Wentworth) and the conditional null-phone drop. Data populate for the remaining 9 multi-location restaurants follows in a subsequent PR.
- Toni's Detroit Style Pizza removed from workstream — Clements Ferry second location closed (Yelp marked closed June 2025; official site lists only Mt Pleasant). Restaurant now single-location, exits workstream. Re-verification trigger: reopening announcement or operator-confirmed status change.

**Current state:** Per DECISIONS #14.4, multi-location restaurants ship with primary-location only in the pilot. D'Allesandro's Pizza has additional locations (Nexton Square Summerville is in-scope; Greenville SC Upstate is out-of-scope per DECISIONS #14.1) currently absent. Pages are correct as-shipped — they just don't yet show the additional locations.

**Why it's tracked, not done now:** Designing the Locations module against a single multi-location restaurant in the pilot would over-fit. Better to design once a second multi-location restaurant lands in a different ranking page and we have two independent test cases. The design needs to handle: per-location `Place` microdata in JSON-LD, visual presentation of multiple locations in the sidebar, and how to handle locations across cities (when the editorial scope from #14.1 expands beyond greater Charleston).

**Trigger to activate:** ACTIVATED 2026-05-03 by Babas on Cannon (3 locations: Cannon, Meeting, Wentworth) during best-coffee-shops port. Workstream H bulk port surfaced 7 additional multi-location restaurants. Full in-scope set as of 2026-05-05: **8 from workstream H** (babas-on-cannon, heavys-barburger, home-team-bbq, santis, senor-tequilas, azul-mexicano, agaves-cantina, bon-banh-mi-southeast-asian-kitchen) plus **2 from prior PRs** (dallesandros-pizza, second-state-coffee) — 10 total, all shipping primary-location-only. Design pass is the next gated workstream — not folded into bulk port.

**Estimated scope:** 1–2 days. Half template + script work; half per-location data collection for the affected restaurants.

### Title verbosity for cuisine-name overlap

**Files affected:** detail-page `<title>` rendering in the generator script; possibly the JSON schema (new optional `titleCuisine` override field).

**Current state:** Toni's Detroit Style Pizza ships with `<title>Toni's Detroit Style Pizza — Detroit Style Pizza in Charleston | Voted On By Locals</title>`. Correct given the data; verbose because `name` and `cuisine` overlap. Affects any restaurant whose name contains its cuisine.

**Why it's tracked, not done now:** Pilot is small enough that the verbosity is manageable. The fix (an optional `titleCuisine` override in JSON that the script uses in the title only when present) is one line of script + one optional field, but designing it against just Toni's risks overfitting.

**Trigger to activate:** at the editorial flesh stage for affected restaurants, OR when bulk port reveals more cuisine-name-overlap cases.

**Estimated scope:** ~30 min — add `titleCuisine` to the JSON schema (null by default, optional override), update step 12 in the script to fall back to `cuisine` when `titleCuisine` is null.

### dateModified maintenance discipline

**Files affected:** detail pages and ranking pages going forward.

**Current state:** 40 pages now carry `datePublished` + `dateModified` JSON-LD fields, both seeded from git-creation-date. `dateModified` is intended to update only when editorial content changes — not on chrome edits.

**Why it's tracked:** No process today guarantees that operator remembers to bump `dateModified` on editorial edits. Risk: stale `dateModified` silently mismeasures content freshness for crawlers. Discipline-only solution today; a pre-commit hook or generator enhancement could automate.

**Estimated scope:** depends on chosen approach. Pre-commit hook = ~30min. Generator-flag-driven update = ~1hr. Pure documentation discipline = no code, just a note in HANDOFF.md or PR template.

**Trigger to activate:** when a discrepancy surfaces (e.g., a sitemap audit shows stale `dateModified` vs actual editorial activity), or when a build pipeline / CI is introduced that could host the hook.

### Top-level pages OG coverage

**Files affected:** `about.html`, `vote.html`, `suggest-category.html`, `ambassadors.html`, `thank-you.html`. Possibly new `og-{slug}.png` assets if per-page images chosen over shared default.

**Current state:** 5 top-level pages have no Open Graph block at all — no `og:image`, no `og:title`, no `og:description`, no `og:url`, no `og:site_name`, no Twitter card. PR #16 (master plan step 5) patched `index.html` to add `og:image`, `og:site_name`, and `twitter:card` (closing the twitter-large-image-card-rendering loop with the new `og-default.png`). The other 5 pages remain bare.

**Why it's tracked, not done now:** Each page needs design decisions before the OG block can ship: unique `og-{slug}.png` per page (extending the step-5 pipeline) or shared `og-default.png`? Per-page `og:title` and `og:description` strings? Pulling these into PR #16 would have meant making those design calls under PR pressure rather than deliberately.

**Estimated scope:** ~2 hours, design-first. Decide per-page asset strategy + draft per-page meta strings + extend the OG pipeline if unique images are chosen. Then ~5 small HTML edits + 0-5 new PNG renders.

**Trigger to activate:** when ready to lead with it. Lower-priority than rankings + detail surfaces (these pages get less inbound traffic); not blocking on anything.

### OG meta-line dedup when restaurant name contains cuisine descriptor

**Files affected:** `og-templates/detail.html` (rendered meta line), `scripts/generate_og_images.py` (`compose_detail_meta` logic) OR `data/restaurants.json` (per-affected-entry hand-curated override field).

**Current state:** OG detail images render the meta line as `{Cuisine} · {Neighborhood}`. When the restaurant name already contains a cuisine descriptor — e.g., "The Harbinger Cafe & Bakery" with cuisine "Café and Bakery" — the share preview reads the descriptor twice. Data-faithful; not a defect, just a redundancy. Spotted on the Harbinger render during step 5 review (PR #16).

**Why it's tracked, not done now:** Two reasonable fix paths and the choice depends on how many entries in `restaurants.json` have this overlap (single-digit edge case → hand-curate; broader pattern → generic suppression rule in the script). The sweep + decision belongs to a separate session, not bundled into step 5. **Conceptually related** to the existing "Title verbosity for cuisine-name overlap" workstream above — same redundancy class, different surface (`<title>` on-site vs. OG meta line). Could be designed and shipped together.

**Estimated scope:** ~30 min — sweep `restaurants.json` for name-contains-cuisine cases, propose either (a) suppress-cuisine-when-redundant rule in `compose_detail_meta` OR (b) optional `ogMetaCuisine` override field per affected entry. Then re-render affected detail PNGs.

**Trigger to activate:** next time we touch detail OG content. Polish-tier; no urgency. Pair with title-verbosity workstream activation.

---

## Deferred for later master-plan steps

These are explicitly held until the master plan reaches the right step. They aren't blocked on operator judgment — they're blocked on sequencing.

- **Vote aggregation pipeline** — Not on the master plan; **strategic deferred**. See `_strategy/CONTEXT.md` → "Things deferred but important." Currently votes go to Netlify Forms; rankings are hand-curated. Building a real aggregation backend (Google Sheets / Airtable / a small JSON file) is a prerequisite for `aggregateRating` JSON-LD, for any visible "live vote totals," and for the flywheel-hypothesis claim flow.

- **Fraud prevention** — Not on the master plan; **strategic deferred**. Tied to vote aggregation. Self-reported zip is the only check today; gameability gets worse with any visible vote count.

- **Restaurant claim flow** — Not on the master plan; **strategic deferred**. Pairs with monetization path B. Prerequisite: detail pages exist (step 2).

- **Multi-city templating** — Not on the master plan; **strategic deferred**. The single biggest "unblocking" decision the project has but explicitly held until Charleston is a stronger foundation. See `_strategy/CONTEXT.md` for the full framing.

---

## Resolved

- **2026-05-04 — OG backplate fix (color-mix on brand.orange at 14%).** All three OG templates (`ranking.html`, `detail.html`, `default.html`) had a brand-mark backplate using Tailwind's `orange-50` (`#FFF7ED`) — fine on the live header's white nav bar but invisible on the OG cream canvas (`#FFF8F0`, one hex-digit difference). Replaced with `color-mix(in srgb, var(--brand-orange) 14%, transparent)` so the backplate derives from the brand-orange token (single source of truth preserved — brand color edits in `tailwind.config.js` propagate on the next render batch). All 42 OG PNGs re-rendered; spot-checked across composition variants (short detail FIG, wrapped ranking Best Nice Restaurants, default). Schema-additive PR; GSC quiet-window safe (asset refresh only, no chrome edits). See merged PR #17.

- **2026-05-04 — Master plan step 5: Open Graph image generation.** All 42 OG share-preview PNGs shipped: 8 ranking pages, 33 detail pages, 1 site default. Pipeline: HTML/CSS templates in `og-templates/` (ranking, detail, default), Python script `scripts/generate_og_images.py` renders via Playwright + headless Chromium at 1200×630 (deviceScaleFactor=2). Brand colors substituted at render time from `tailwind.config.js` so the single-source-of-truth invariant holds. Three intentional design decisions per template (no emoji, no URL stamp, no date — all docblocked). Detail template uses three-tier adaptive font sizing (132/108/84px) with worst-case validator (Bon Banh Mi at 35 chars). Same-PR `index.html` chrome edits added `og:image`, `og:site_name`, and `twitter:card` (closing the twitter-large-image-card-rendering loop). Two follow-ups filed: top-level pages OG coverage (5 pages: about, vote, suggest-category, ambassadors, thank-you) and OG meta-line dedup when restaurant name contains cuisine descriptor (Harbinger). New dependency: `playwright>=1.40` in `requirements.txt`. See merged PR #16.

- **2026-05-04 — BreadcrumbList schema across rankings + details.** All 8 ranking pages and 33 detail pages now carry `BreadcrumbList` JSON-LD. Ranking shape: Home → Rankings (`/#rankings`) → Best {Category}. Detail shape: Home → {RestaurantName} (no intermediate "Restaurants" node — site has no /restaurants index or nav category, and detail pages are cross-listed across rankings so a parent ranking would be ambiguous). `/#rankings` fragment resolves to the homepage today; small post-May-20 follow-up filed above to add `id="rankings"` to the cards section. Detail-page generator regenerated all 33 pages from `_detail-page-template.html`; ranking pages hand-edited (no ranking-page generator). Schema-only PR — no chrome edits, GSC quiet-window safe. See merged PR #18.

- **2026-05-04 — Hero dot-pattern brand-color duplication.** Moved `.bg-dot-pattern` from `index.html` inline `<style>` into `src/input.css` as `@layer components`, using `theme('colors.brand.orange')` instead of hardcoded `#E67E22`. Brand-color changes in `tailwind.config.js` now propagate automatically. Visual unchanged. See merged PR #14.

- **2026-05-04 — Doc reconciliation: PLAN.md status retired, HANDOFF as source of truth.** Per-step status markers (✅/⏳) and stale per-step text removed from `PLAN.md`; `HANDOFF.md` becomes the single source of truth for current per-step status. PLAN.md retains the structural/strategic *why* of each step (content stable across sessions). Edit also removed Step 1's stale "Tracked items remaining" sub-section, Step 2's "Open design questions" sub-section, the entire `## What's next` section in PLAN.md, and HANDOFF's "PLAN.md reconciliation" sub-section under What's next. Net change: PLAN.md ~25% shorter, HANDOFF.md ~10 lines shorter. See merged PR #13.

- **2026-05-04 — `best-new-coffee-shop.html` per-page meta + JSON-LD.** Added canonical URL, full Open Graph block, Twitter card, keywords meta, and `CafeOrCoffeeShop` JSON-LD describing Babas on Wentworth (the featured winner) at 115 Wentworth St, Charleston SC 29401. JSON-LD shape mirrors `babas-on-cannon.html` field-by-field. Triggered PR #8's date-seed mechanism on this page; sitemap `<lastmod>` coverage 40 → 41 pages (URL count unchanged at 46). Master plan step 2 + step 3 now at 100%. Anti-fab: omitted telephone (Cannon's number, location-specific), geo (null in data), image (null in data); shipped from real data: address, openingHours, priceRange, sameAs. JSON-LD `url` points at the featured-winner page itself per new DECISIONS #16. See merged PR #12.

- **2026-05-04 — Inliner `--refresh` flag.** `scripts/inline_chrome.py` now supports `--refresh` to strip existing marker-wrapped chrome and re-inline from `components/*.html`. Closes the friction introduced by PR #9: editing `components/` no longer requires manual placeholder restoration across 49 files. Mutually exclusive with `--check`. Default inline path (skip-if-marker) unchanged — refresh is opt-in.

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
