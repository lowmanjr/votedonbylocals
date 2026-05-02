# Detail-page design analysis

Working file for step 2 of the master plan. Surfaces the open design questions, proposes options with tradeoffs and a recommendation per question, and asks for explicit operator confirmation before any execution.

This is an analysis, not a decision. Per the workflow norm (`_strategy/WORKFLOW.md`, `_strategy/DECISIONS.md` #12), nothing in this document ships until John confirms the recommendations or redirects on specific items.

The questions below echo the original list in `_strategy/HANDOFF.md` plus a seventh that the bootstrap brief surfaced (scope of first deliverable). An additional unsolicited eighth concern is added at the end — not a design question, but an operational one I'd want a decision on before pages start shipping.

---

## Q1 — URL pattern

The choice is structurally coupled with the multi-city architecture (`_strategy/CONTEXT.md` line 29), which is itself deferred. The right framing is therefore: which URL pattern has the lowest retrofit cost across the multi-city architectures we might later pick?

**Options.**

A) `/restaurants/{slug}.html` — mirrors the existing `/rankings/{slug}.html` convention. Semantic, short, stable.

B) `/charleston/{slug}.html` — anticipates the path-prefix multi-city architecture by including the city today.

C) `/r/{slug}.html` — short alias. Worse for SEO (search engines benefit from semantic paths) and reads as engineer-y rather than editorial.

D) `/{slug}.html` (flat at root) — unworkable. Slug collisions with existing top-level pages (`about`, `vote`, etc.) and category pages.

**Recommendation: A — `/restaurants/{slug}.html`.**

Under the subdomain multi-city architecture (`charleston.votedonbylocals.com`), pattern A needs zero retrofit — the city is in the subdomain. Under the path-prefix architecture, pattern A requires a bulk find-replace + 301 redirects (mechanical, ~1 day) — the same retrofit pattern B would need under the subdomain architecture. Pattern A is the option that reads correctly under either future and matches the existing `/rankings/` convention; pattern B prematurely commits to one of two equally-likely multi-city architectures.

**Tradeoffs.** If the project ever picks the path-prefix multi-city architecture, every detail-page URL has to migrate. This couples to Q6 (badge anchor) — once badges with these URLs are on restaurant websites, the migration also costs a redirect-stability commitment. Cost is real but bounded.

---

## Q2 — Page template

The detail-page template needs to handle: restaurant name + cuisine + neighborhood, structured address + hours + phone (when available), editorial body (variable length per Q4), the inverse cross-link to ranking pages this restaurant appears on, and future-proof slots for the badge image and claim CTA per the flywheel hypothesis (`_strategy/CONTEXT.md` lines 38–56).

**Options.**

A) **Mirror `best-new-coffee-shop`'s single-winner layout exactly.** It already has the right body shape (large card, badge, neighborhood label, multi-paragraph editorial, pull quote, address+hours sidebar) and chrome harmonized to canonical KEEP blocks per `_strategy/DECISIONS.md` #8.

B) **Design a wholly new richer-schema layout.** Maximum design freedom; throws away the existing single-winner work; requires a new visual design pass.

C) **Hybrid — borrow the `best-new-coffee-shop` body shape and add detail-page-specific modules.** Keep the chrome, keep the card+sidebar structure, but replace single-winner-specific elements (the "Suggest a different winner" CTA reads wrong on a detail page) and add the rankings-cross-link section + the future-proof badge/claim slots.

**Recommendation: C — Hybrid.**

Pure mirror (A) ships pages with copy that doesn't fit (the "Suggest a different winner" CTA assumes single-winner framing) and is missing the rankings cross-link that Step 3 of the master plan depends on. Pure new design (B) discards ~80% of structurally appropriate existing work for ~20% of fit-to-purpose changes.

**Tradeoffs.** The hybrid choice forces an early resolution of the `best-new-coffee-shop` per-page meta workstream (currently tracked-and-deferred per `_strategy/TRACKED.md`). If detail pages adopt LocalBusiness-derived schema (Q3), the same schema profile becomes the obvious answer for the single-winner page, and the workstream collapses into step 2 as a side effect. Worth flagging as a scope creep that's actually convergent.

---

## Q3 — Schema type

Schema.org's hierarchy: `LocalBusiness` ⊃ `FoodEstablishment` ⊃ {`Restaurant`, `CafeOrCoffeeShop`, `BarOrPub`, `Bakery`, `NightClub`}. Google's structured-data validator accepts the most-specific applicable type as best practice. The per-page-configurable pattern from `_strategy/DECISIONS.md` #5 already covers this — the question is just how to extend it from rankings to details.

**Options.**

A) **Restaurant only** — matches the per-item type used in ranking-page `ItemList`. Simple, consistent. Loses semantic accuracy for coffee shops, bars, etc.

B) **LocalBusiness only** — uniform parent type across all detail pages. Loses the more-specific subclass info (a coffee shop is more accurately `CafeOrCoffeeShop` than `LocalBusiness`).

C) **Per-restaurant most-specific applicable type, defaulting to Restaurant.** Same pattern as DECISIONS #5 (`Restaurant` default, override to `CafeOrCoffeeShop` etc.). Each detail page declares the most accurate type for that establishment.

**Recommendation: C — extends the established pattern.**

Detail pages aren't fundamentally a different schema problem from rankings — they're the per-entity richer-data version of the same problem. The pattern that already works for rankings should carry forward.

**Field policy** (separate decision needed under C):

*Required* (page does not ship without): `@type`, `name`, `address` (street, locality, region, postalCode, country).

*Strongly recommended where data exists*: `telephone`, `url` (restaurant's own website), `openingHours`, `priceRange`, `geo` (lat/lng), `servesCuisine`, `image`.

*Out of scope until adjacent workstreams activate*: `aggregateRating` (deferred per DECISIONS #9 until vote aggregation pipeline exists), `acceptsReservations` (entangled with monetization path C, currently the least brand-safe path per CONTEXT).

The anti-fabrication line (HANDOFF) applies hard here. If we don't have real hours, we omit `openingHours` entirely — we do not put placeholder values, "call ahead," or fabricated approximations. Same rule for every nice-to-have field.

**Tradeoffs.** Real cost: a per-restaurant data-collection pass to source addresses (and ideally hours, phone, geo) before pages can ship. 37 restaurants × ~5 minutes per restaurant = ~3 hours of data entry. Sources: Google Places, restaurant's own site, Apple Maps. Open: should we use a structured data store for this (small JSON file the template reads) or hand-author per page? Recommend the JSON file — single source of truth, easier to maintain, anticipates the multi-city / vote-aggregation infrastructure CONTEXT calls out as deferred-but-important.

---

## Q4 — Editorial scope per restaurant

The most strategically loaded question. Per HANDOFF "What NOT to do": *"Don't fabricate restaurant data. The brand wedge is anti-fabrication; this is the project's most important integrity line."*

**Options.**

A) **Hand-written editorial per restaurant.** 200–400 words of original copy from John per page. Best brand quality, slowest. ~30 min per page × 37 = ~18 hours of writing time gates step 2 completion.

B) **Stub-then-flesh.** Pages ship with real-but-minimal content (name, address, cuisine, hours-if-available, hero tagline carried from ranking page, 1-sentence "appears on the [Best Pizza](...) ranking" cross-link). No fabricated body copy. Editorial body added later, one tight commit per restaurant.

C) **Auto-generate body copy from existing tagline + cuisine + neighborhood data.** Templated sentences ("Located in Park Circle, this Caribbean-influenced spot...") produced programmatically.

**Recommendation: B — Stub-then-flesh.**

Option C directly violates the anti-fabrication wedge. Even when the inputs are real, auto-generated editorial-shaped content reads as editorial-shaped content that wasn't editorially written. The brand premise is "by locals" — auto-gen is by neither locals nor anyone. Hard no.

Option A is the brand-best option but blocks step 2 from shipping behind ~18 hours of writing time, which converts step 2 from a plan step into an editorial backlog.

Option B is the only choice that respects the wedge AND lets step 2 ship in a measurable timeframe. The minimum stub still contains real, editorially defensible content — it just doesn't pretend to be richer than it is. Pages exist for SEO accrual, schema, and the flywheel anchor immediately. Editorial growth is monotonic.

**Tradeoffs.** The failure mode is real: stub-then-flesh sites are everywhere, and many never get fleshed. Mitigation: define the minimum stub explicitly and refuse to ship anything thinner. Proposed minimum:

- Restaurant name (h1)
- Hero tagline (carried verbatim from ranking page)
- Real, structured address
- Cuisine + neighborhood (1 sentence)
- "Appears on: [Best Pizza]({...})" cross-link
- (Optional, where data exists) hours, phone, website link
- The "Disagree with this list?" CTA pattern from the canonical, adapted

That's a real page, not a placeholder. ~80–120 words of structural content + structured data, none of it fabricated.

---

## Q5 — Content fields

The detail-page template's placeholder set, drafted to match the canonical's pattern. Roughly doubles the field count from rankings — expected, since detail pages carry more per-entity data.

**Carried directly from canonical** (semantics intact): `{{slug}}`, `{{Year}}`, `{{MonthYear}}`, `{{Description}}`, `{{ShareTagline}}`, `{{Keywords}}`.

**New required fields**: `{{RestaurantName}}`, `{{Tagline}}`, `{{Cuisine}}`, `{{Neighborhood}}`, `{{StreetAddress}}`, `{{AddressLocality}}` (defaults "Charleston"), `{{AddressRegion}}` (defaults "SC"), `{{PostalCode}}`, `{{SchemaType}}` (defaults "Restaurant"), `{{AppearsOn}}` (the rankings cross-link list — array of {RankingURL, RankingTitle}).

**New optional fields** (template renders the section conditionally, page only fills if real data exists): `{{Phone}}`, `{{Hours}}`, `{{PriceRange}}`, `{{WebsiteURL}}`, `{{GeoLat}}`, `{{GeoLng}}`, `{{ImageURL}}`, `{{EditorialBody}}` (per Q4's flesh stage).

**Future-proof slots** (declared in template, empty until adjacent workstreams activate): badge image slot (flywheel), claim CTA slot (monetization path B). These exist as commented-out HTML blocks the template can light up later without restructuring.

**Recommendation: ship template with the above field set.** Open question worth surfacing: do we want to maintain the per-restaurant data as a structured JSON file the build references, or as inline values per page? The JSON file is the answer if any of (multi-city, vote aggregation, claim flow) is foreseeable. Inline is the answer if Fork A (editorial hobby) is the committed direction. Per CONTEXT line 149 — *"make step 2 decisions in a way that's compatible with both forks"* — JSON file wins because it's compatible with both, while inline forecloses the data-driven options.

---

## Q6 — Badge anchor

The flywheel hypothesis (`_strategy/CONTEXT.md` lines 38–56) requires each detail page to have a stable anchor URL the badge can link to. Confirming Q1 plays cleanly with badge generation, plus surfacing the slug-stability policy that step 2 implicitly commits to.

**Confirmation.** Q1's recommended pattern `/restaurants/{slug}.html` works as the badge anchor. Badge-image URL would be `https://votedonbylocals.com/assets/images/badge-{category}-{slug}.png`. Badge → detail-page link is stable except under the path-prefix multi-city retrofit case noted in Q1.

**Slug-stability policy worth deciding now** (because it's load-bearing on every badge ever placed): when a restaurant rebrands or changes ownership, does the slug change? Recommended policy: **slugs are stable; rebrands keep the original slug, with the new name in the page title and the old name aliased internally.** Rationale: badges placed on restaurant websites, takeout menus, and storefront stickers keep working without the project needing to coordinate a redirect cascade. Cost: occasional cosmetic mismatch between slug and current name (e.g., a slug `chico-feo` for a restaurant later renamed). Acceptable.

The badge artifact itself is out of scope for step 2 — Q6 is just confirming that step 2 doesn't lock out the badge work. It doesn't.

---

## Q7 — Scope of first deliverable

The bootstrap brief surfaced this as not on the original list but worth raising. Weak prior toward pilot, same logic as analyze-first.

**Options.**

A) **All 37 detail pages at once.** Big bang. Full SEO surface, full flywheel anchor coverage from day 1.

B) **Pilot — one ranking page's worth (5 restaurants), then bulk-port.** Recommend `best-pizza`'s 5 since it's the canonical seed page from step 1.

C) **Tiered rollout by editorial readiness.** Ship the restaurants John has best editorial intuition for first.

**Recommendation: B — pilot with `best-pizza`'s 5.**

This mirrors the proven step-1 pattern (build canonical → port via 1 page → bulk-port the rest). Shipping 5 detail pages tells us: does the template render correctly across the variants we'll see? does the schema validate in Google Search Console? does the data-collection pass reveal blockers (a restaurant whose address Google doesn't list, hours that vary too much to schema-encode, etc.)? does the editorial scope per page (Q4 stub) feel right when read end-to-end?

If anything's wrong, we caught it on 5 pages, not 37. After pilot validation, the bulk port is mechanical — roughly 6× the pilot work, no design decisions.

Option C introduces an editorial-readiness ordering that gets in the way of the structural validation a pilot is for. Editorial readiness matters for the flesh stage, not the stub stage.

**Tradeoffs.** B takes one extra round-trip versus A — a ~1-day delay in full-coverage shipping. Acceptable cost.

---

## Q8 (added) — Per-restaurant data store

Not on the original question list but functionally load-bearing on Q3, Q5, and Q7. Surfacing it for an explicit decision.

Each detail page will need: structured address, optional hours/phone/website/geo, the cuisine + neighborhood values, the "appears on" cross-link list. That data lives somewhere.

**Options.**

A) **Inline per HTML file.** Each detail page hardcodes its own fields. Simple, no build step. Hard to update at scale (a chain restaurant changing hours = N file edits).

B) **Single JSON file at `data/restaurants.json`.** Source of truth for per-restaurant data; template reads from it at build or via a tiny client-side fetch. Easy to update; enables future "restaurant changed hours" updates as a one-line JSON edit; structurally compatible with the eventual claim flow (claim writes update the JSON).

C) **Per-restaurant Markdown files** with frontmatter. Splits the difference; closer to a CMS pattern.

**Recommendation: B — `data/restaurants.json`.**

Compatible with both forks per CONTEXT line 149: under Fork A it's a slight overhead with no immediate payoff; under Fork B it's the foundation for vote aggregation, claim flow, and multi-city templating. Inline (A) actively forecloses Fork B affordances.

Open: read-time strategy — build-step substitution (introduces a build step, prerequisite for step 4) or runtime `fetch()` in the page (zero build dependency, slight FOUC). Probably build-step substitution since step 4 is going to introduce one anyway, but worth deciding deliberately rather than by default.

---

## What needs explicit operator confirmation before execution

For each of the following, John picks the option (or redirects with a different one). Some are paired and resolve together.

| Q | Decision needed | Recommendation |
|---|---|---|
| 1 | URL pattern | `/restaurants/{slug}.html` |
| 2 | Page template approach | Hybrid (extend `best-new-coffee-shop`) |
| 3 | Schema type | Per-restaurant most-specific (extends DECISIONS #5) |
| 3 | Field policy | Required vs strongly-recommended-where-data-exists vs out-of-scope per the table above |
| 4 | Editorial scope | Stub-then-flesh, with the minimum-stub definition above |
| 5 | Content fields | The drafted set above (or amendments) |
| 5 | Data store form | (paired with Q8) |
| 6 | Slug-stability policy | Slugs stable through rebrands |
| 7 | First-deliverable scope | Pilot with `best-pizza`'s 5 |
| 8 | Per-restaurant data store | `data/restaurants.json` |
| 8 | Read-time strategy | Build-step substitution (paired with master plan step 4) |

## What this analysis explicitly does NOT decide

- The exact HTML structure of the detail-page template (that's a follow-up working file once Q1–Q8 are confirmed — would live at `rankings/_detail-page-template.html` or similar).
- The badge artifact design (out of scope per Q6 confirmation).
- The claim flow (deferred per CONTEXT, not in step 2).
- Whether to backfill the `best-new-coffee-shop` per-page meta workstream as a side effect of Q2/Q3 resolution. Implicitly likely; explicitly worth a separate decision.
- The OG image generation for ~37 new images (master plan step 5).

## Convergent side effects of these decisions

If the recommendations land as proposed, three pieces of currently-deferred work collapse together as step 2 ships:

1. The `best-new-coffee-shop` per-page meta workstream resolves (gets the same schema profile as detail pages).
2. The infrastructure for vote aggregation, claim flow, and multi-city all gets one foundational piece (the `data/restaurants.json` store) ahead of need.
3. The build step that master plan step 4 (kill Tailwind CDN) requires gets justified by step 2 needs as well — no longer a step-4-specific concern.

None of those is a deliberate scope expansion; they're load-bearing convergences worth noting so John can decide whether to ride them or split them out.
