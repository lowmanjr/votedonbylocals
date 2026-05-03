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

**Trigger to activate:** when the bulk port hits a third multi-location restaurant. (Two known: Toni's, D'Allesandro's. Third triggers the design.)

**Estimated scope:** 1–2 days. Half template + script work; half per-location data collection for the affected restaurants.

### Multi-entry AppearsOn handling in generator script

**Files affected:** `scripts/generate_detail_page.py`.

**Current state:** Script handles single-entry AppearsOn (one ranking page per restaurant). All 5 pilot restaurants are single-entry. Multi-entry support is a known future extension flagged in the script's docstring.

**Why it's tracked, not done now:** Designing without a real test case risks shipping the wrong abstraction. When the first restaurant appearing on >1 ranking page lands (likely as the bulk port progresses across rankings), we'll have a concrete case to design against.

**Trigger to activate:** when the bulk port hits the first restaurant appearing on >1 ranking page.

**Estimated scope:** ~2 hours — duplicate the AppearsOn `<li>` block per entry in the script's step 12. Mostly mechanical.

### Title verbosity for cuisine-name overlap

**Files affected:** detail-page `<title>` rendering in the generator script; possibly the JSON schema (new optional `titleCuisine` override field).

**Current state:** Toni's Detroit Style Pizza ships with `<title>Toni's Detroit Style Pizza — Detroit Style Pizza in Charleston | Voted On By Locals</title>`. Correct given the data; verbose because `name` and `cuisine` overlap. Affects any restaurant whose name contains its cuisine.

**Why it's tracked, not done now:** Pilot is small enough that the verbosity is manageable. The fix (an optional `titleCuisine` override in JSON that the script uses in the title only when present) is one line of script + one optional field, but designing it against just Toni's risks overfitting.

**Trigger to activate:** at the editorial flesh stage for affected restaurants, OR when bulk port reveals more cuisine-name-overlap cases.

**Estimated scope:** ~30 min — add `titleCuisine` to the JSON schema (null by default, optional override), update step 12 in the script to fall back to `cuisine` when `titleCuisine` is null.

### Bulk port of remaining ~32 detail pages

**Files affected:** `data/restaurants.json` (32 new entries), `restaurants/*.html` (32 new pages), generated by existing `scripts/generate_detail_page.py`.

**Current state:** 5 of ~37 detail pages live (the best-pizza pilot). The remaining ~32 restaurants across the other 7 ranking pages have no detail pages yet — they appear on rankings as name + tagline only, the pre-step-2 state.

**Why it's tracked, not done now:** Each of the other 7 ranking pages is its own data-collection pass (~5 restaurants × ~7 fields = ~35 cells per ranking). The pattern is now mechanical (web research → JSON → `python scripts/generate_detail_page.py --all`), but the data collection itself is the gating activity.

**Order of operations:** Recommended one ranking page at a time, mirroring the pilot's tight scope. After each ranking's restaurants land, also do the master plan step 3 work (schema cross-linking) for that ranking page only, so the ranking page → detail page wiring stays current as detail pages ship.

**Estimated scope:** ~3–4 hours per ranking page (data collection + JSON entry + generation + visual review). 7 rankings remaining = 21–28 hours total for full bulk port.

### BreadcrumbList schema across rankings + details

**Files affected:** all 8 ranking pages, the detail-page template, all detail pages.

**Current state:** No `BreadcrumbList` JSON-LD anywhere on the site. Considered and deferred during step 3. Ranking-only (`Home → Best Pizza`) is mechanical but low-value as a 2-node breadcrumb. The high-value case (`Home → Best Pizza → {Restaurant}`) requires touching the detail-page template, which was out of step 3 scope.

**Why it's tracked, not done now:** The high-value version requires the detail-page template work; doing only the ranking-side version locks in a 2-node-only convention that gets retrofitted later anyway. Cleaner to add ranking + detail breadcrumbs in one pass once detail-page coverage is global.

**Trigger to activate:** after the bulk-port workstream completes (or as a stage of it, on a per-ranking basis as detail pages ship per ranking).

**Estimated scope:** ~2 hours — one schema block in the ranking template + one in the detail-page template, plus per-page rendering for the 8 rankings and ~37 detail pages.

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

- **2026-05-03 — Doc consistency: 5-top-level-pages workstream placement.** Resolved via three small edits anchoring the workstream to step 4 as an explicit prerequisite. See commit f66cd17 and DECISIONS log entry context. (Workstream itself remains tracked above — only the placement-fuzziness was resolved.)

- **2026-05-03 — Step 2 pilot port (best-pizza, 5 of ~37 detail pages).** Pilot ships 5 detail pages at /restaurants/{slug}.html with full chrome, JSON-LD, address/hours/phone/price/website where data exists. Generator script (commit 9c6b3f7) is reusable for the bulk port. Strategic decisions captured in DECISIONS #14. Bulk port for the remaining ~32 pages tracked above as a separate workstream.

- **2026-05-03 — canonical-template boilerplate removed from 7 ranking pages.** Initially scoped as a single-file cleanup on `best-pizza.html`. Pre-flight grep found the boilerplate was actually propagated to all 7 ranking pages during step 1 harmonization, plus an extended page-deviation note on `best-new-restaurants.html`. Resolved per D2: full delete from 6 pages, surgical rewrite preserving the page-specific deviation note on the 7th. Convention-level notes (emoji reuse, vote-count absence, favicon-vs-OG asymmetry) verified durable in DECISIONS #1 / #2 / #10 before delete. See commit 902c584.

- **2026-05-03 — 5 top-level pages chrome upgrade.** about.html, vote.html, suggest-category.html, ambassadors.html, and thank-you.html now share the canonical chrome (inline Tailwind config + font preconnect/stylesheet + canonical body classes). Side effect: focus:border-brand-orange / focus:ring-brand-orange Tailwind variants on form inputs now resolve correctly (were silent no-ops before — variants need brand-orange in Tailwind's config, which only the inline config provides). Sibling commit pruned 2 redundant style.css declarations + 2 redundant rules (DECISIONS #11). .font-poppins retained pending step 4. Unblocks PLAN.md step 4. See commits 689d3d2 (chrome upgrade) and f60c5e5 (style.css prune).
