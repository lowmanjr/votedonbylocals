# Decisions log

Non-obvious calls made during the template-harmonization session. One entry per decision. Each captures: what was decided, what was considered, why this choice prevailed.

The point of this log is to prevent the next session (or a future contributor) from re-relitigating these. If a decision needs revisiting later, do it as a new entry that references the prior one — don't silently change behavior.

---

## 1. Emoji-per-row over dot-bullets, page-theme emoji over per-restaurant emoji

**What was decided:** Each restaurant row in a Top-5 ranking uses the *same* emoji as the page hero (e.g., 🍕 on `best-pizza`, 🍔 on `best-burger`) as its leading icon. Per-restaurant emoji are intentionally not a content field.

**Alternatives considered:**
- Orange-dot bullet (`<div class="h-3 w-3 rounded-full bg-brand-orange/40">`) used in `best-burger`/`best-tex-mex` pre-migration
- Numeric ranks (1, 2, 3, 4, 5) used in the older ranking pages
- Per-restaurant emoji where each restaurant gets its own (e.g., on a coffee shop page: ☕ for one place, 🥐 for a bakery, 🍵 for a tea-leaning spot)
- No icon at all

**Why this choice:** Emoji-per-row is more visually distinctive at small sizes than dot bullets, signals the page topic at a glance, and reads as more "by locals" than institutional/numbered. Page-theme emoji (vs per-restaurant) creates a visual rhythm that anchors each page to its category and avoids implying a richer per-restaurant content model the project hasn't committed to. Also — important — emoji rendering is platform-consistent enough that it doesn't degrade across iOS/Android/Chrome/Firefox.

---

## 2. Hardcoded vote totals removed from canonical

**What was decided:** The "Based on N local votes collected in YEAR" footer is intentionally absent from the canonical template. Pre-migration, two pages (`best-burger`: 1,769; `best-tex-mex`: 1,420) had hardcoded numbers in their HTML.

**Alternatives considered:**
- Keep as an optional content field with placeholder syntax (`{{VoteCount}}` / `{{VoteYear}}`)
- Replace with rounded hand-wavy copy ("based on hundreds of votes")
- Leave the existing two pages with their numbers, never add to others

**Why this choice:** The pre-migration numbers were marketing copy, not derived from any real vote-aggregation pipeline. Keeping a placeholder field invites future fabrication — the next maintainer plugs in a plausible-looking number. The intentional absence is documented in the canonical (`Intentional design decisions` block) so a future contributor can't reintroduce it without an explicit conversation. When real aggregate vote data exists (see `_strategy/TRACKED.md` → vote aggregation pipeline), add it back as a real component with structured-data backing — not a string placeholder.

---

## 3. {{Description}} vs {{ShareTagline}} split

**What was decided:** Two separate content fields per page. `{{Description}}` is long (~150 chars), keyword-rich, used by `<meta description>` and JSON-LD `description`. `{{ShareTagline}}` is short (~60–110 chars), hook-driven, used only by `og:description` and `twitter:description`.

**Alternatives considered:** A single `{{Description}}` field used in all four places (the canonical's initial draft).

**Why this choice:** Search snippets and share previews have different optimal lengths and tones. Search snippets reward keyword density and complete sentences (~150 chars before truncation). Share previews reward punchy hooks (~60–110 chars before truncation on most platforms). A single description either ends up too long for share or too short for snippets. Existing `best-pizza.html` already authored them differently before migration ("Discover the best pizza in Charleston, SC. From authentic Neapolitan to crispy Detroit style…" vs "The definitive guide to the best slices in the Holy City.") — so the canonical now matches that practice rather than fights it.

---

## 4. Top-4 framing for `best-new-restaurants`

**What was decided:** Keep `best-new-restaurants` as a Top-4 list (not Top-5). Subtitle reads "As voted by Charleston locals. Four standouts — with more to come." The canonical otherwise specifies 5 rows per ranking page.

**Alternatives considered:**
- Pad to Top-5 with a 5th entry from training-data memory of older Charleston openings
- Rename the page to "Top 4 New Restaurants"
- Collapse into the general `best-restaurants` style with mixed entry counts

**Why this choice:** "Best New" is naturally a smaller-pool category — opening counts vary year over year. There may legitimately not be 5 worthy new openings every quarter. Padding to a fixed 5 invites fabrication, which is exactly the editorial quality this site exists to be the antidote to. The "with more to come" framing makes the count intentional rather than an awkward gap. The canonical supports 4 entries trivially (delete the row 5 markup block in the `<main>` body and the position-5 entry in the JSON-LD `ItemList`). Promotion to Top-5 happens later when a real 5th candidate exists — see `_strategy/TRACKED.md`.

---

## 5. CafeOrCoffeeShop schema for coffee page; per-page @type configurability

**What was decided:** `best-coffee-shops` uses `"@type": "CafeOrCoffeeShop"` for all 5 JSON-LD items, overriding the canonical default of `"Restaurant"`. The canonical template documents this as an extensible per-page override pattern: `Restaurant` (default) → `CafeOrCoffeeShop` (coffee), `BarOrPub` (future bar pages), `NightClub`, `Bakery`, etc.

**Alternatives considered:**
- Use `"Restaurant"` for everything — simplest, technically valid (Google accepts it)
- Force a single type across the whole site for consistency
- Pick one custom super-type and use it everywhere

**Why this choice:** schema.org provides `CafeOrCoffeeShop` as a more semantically accurate subclass of `FoodEstablishment`. Using it on the coffee page is more correct without diverging from the canonical's structure (the per-page override is one line of edit). Documenting the override pattern in the canonical's JSON-LD comment block means future pages (a bar page, a club page, a bakery page) can use the right type without re-deciding the convention. All listed types subclass `FoodEstablishment` and pass Google's structured-data validator.

---

## 6. 🍷 hero emoji for `best-nice-restaurants`

**What was decided:** 🍷 (wine glass) is the page-theme emoji for `best-nice-restaurants`. Pre-migration this page had no hero emoji at all.

**Alternatives considered:**
- 🥂 (cheers — celebratory, more anniversary/wedding-feel)
- 🍽️ (plate with utensils — neutral, slightly bland)
- ✨ (already used by `best-new-restaurants`, so unavailable)

**Why this choice:** 🍷 signals upscale dining without veering into special-occasion or anniversary territory. Reads as "nice meal out" rather than "celebration" — which matches the page's spec (best NICE restaurants — for a special night out, but not exclusively for milestone events).

---

## 7. "Disagree with this list?" CTA copy as canonical

**What was decided:** "Disagree with this list? Cast your vote!" is the canonical bottom-CTA copy on all ranking pages. Pre-migration, `best-pizza` used "Have a different favorite?"; `best-burger`/`best-tex-mex` used the "Disagree" version; older pages had no copy line.

**Alternatives considered:**
- "Have a different favorite?" (best-pizza's existing, friendlier tone)
- "Vote now" alone with no copy line (older pages' pattern)
- "Tell us your pick" or other neutral variants

**Why this choice:** "Disagree" triggers active response — it invites the reader to challenge the consensus, which is the actual conversion driver. The site's product *is* local consensus; the CTA should make people want to argue with the consensus. "Have a different favorite?" is more polite but reads as optional ("nice if you do, fine if you don't"). A/B testing wasn't run, but the copy decision is reversible — if conversion data later suggests otherwise, swap the canonical and re-port.

---

## 8. `best-new-coffee-shop` kept on its own template (chrome harmonized, body distinct)

**What was decided:** `best-new-coffee-shop.html` remains a single-winner feature page with a body layout fundamentally different from the Top-5 canonical (one big card with badge, neighborhood label, multi-paragraph editorial, pull quote, address+hours sidebar, "Suggest a different winner" CTA). Only the chrome (head, GA, fonts, Tailwind config, body classes, header/footer pattern) was harmonized to match the canonical's KEEP blocks.

**Alternatives considered:**
- Fold it into the Top-5 canonical template by truncating the editorial richness
- Leave the entire page untouched (lose chrome consistency)
- Build a separate "featured-winner" template variant

**Why this choice:** There's a real product reason for the format difference — "Best New {category}" rankings often have a single clear winner that warrants depth. Folding into Top-5 would lose meaningful information (address, hours, the editorial blurb, the pull quote). But chrome (everything in `<head>`, body class set, header/footer pattern) should be uniform across the site for maintainability. Resolution: harmonize chrome only, leave body distinct. Same template family — different body type. A future "featured-winner" template variant is a tracked workstream when a second single-winner page is added.

---

## 9. `aggregateRating` intentionally absent from JSON-LD until real vote data exists

**What was decided:** None of the JSON-LD `Restaurant`/`CafeOrCoffeeShop` items include an `aggregateRating` field. The canonical's JSON-LD section has a comment block explicitly documenting this absence and how to add it cleanly when real data exists.

**Alternatives considered:**
- Include `aggregateRating` with derived numbers (e.g., from the pre-migration "1,769 votes" copy)
- Include with placeholder values like `ratingValue: 5, ratingCount: 100`
- Add per-restaurant ratings hand-curated by the editor

**Why this choice:** Fabricated structured data is treated as deceptive markup by Google and can trigger manual penalties (and a credibility hit if anyone notices the numbers don't reconcile). The site doesn't yet have a real vote-aggregation pipeline (vote submissions go to Netlify Forms; rankings are hand-curated, not derived from counts). Better to have NO `aggregateRating` than a fake one. The canonical documents the schema.org reference and exactly where to add the field when real data lands. Vote aggregation is on the deferred list — see `_strategy/TRACKED.md`.

---

## 10. Relative favicon path vs absolute OG image URL (deliberate asymmetry)

**What was decided:** `<link rel="icon" href="../assets/images/favicon.png">` uses a relative path. `og:image`, `twitter:image`, `og:url`, `canonical` all use absolute URLs (`https://votedonbylocals.com/...`). The canonical documents this asymmetry as intentional.

**Alternatives considered:**
- Make all paths absolute (consistent but verbose)
- Make all paths relative (would silently break previews on every social platform)

**Why this choice:** Favicons are loaded by the browser with the document as the base URL — relative paths resolve. OG/Twitter images are fetched out-of-context by social platforms (Facebook, X, iMessage, Slack, LinkedIn, Discord) which have no document base — they REQUIRE absolute URLs. Relative `og:image` paths silently break previews on every platform: the platform sees `../assets/images/og-best-pizza.png`, has no base to resolve against, and either drops the image or renders the literal string. This is a known and well-documented gotcha. Documented in the canonical's intentional-decisions block so a future maintainer doesn't "fix" the asymmetry into a regression.

---

## 11. style.css: 5 rules retained (blocked on top-level pages upgrade) rather than deleted

**What was decided:** Of the 6 cleanup deletions originally proposed for `style.css`, only `.brand-orange` (bare class, color: #E67E22) was deleted. Five rules retained: `.bg-brand-orange`, `.border-brand-orange`, `.font-poppins`, `@import url()` for Google Fonts, and the `body` rule's `background-color`/`color` declarations.

**Alternatives considered:**
- Delete all 6 per the original cleanup plan
- Delete all 6, accept temporary visual breakage on 5 top-level pages, fix forward
- Manually upgrade the 5 top-level pages so the full prune becomes safe

**Why this choice:** 5 top-level pages (`about`, `vote`, `suggest-category`, `ambassadors`, `thank-you`) have not yet been migrated to canonical chrome. They use `<body class="antialiased">` only — no `bg-brand-cream text-brand-dark`, no inline Tailwind config, no font preconnect+link. They depend on style.css's plain-CSS class duplications and the body rule for visual rendering. Deleting those 5 rules visually breaks those 5 pages (browser-default white background, black text, no fonts loaded, orange buttons go transparent, "Golden Rule" box loses dashed border on `about.html`). The full prune is blocked on a separate workstream — upgrading those pages — which is now tracked in `_strategy/TRACKED.md` ("Upgrade 5 top-level pages to canonical chrome"). Documented inside style.css itself with a 13-line comment so the rules can't be silently re-deleted.

---

## 12. Analyze-then-execute workflow cadence (catches errors before they ship)

**What was decided:** For each step in the migration, write a structured analysis BEFORE making changes. Get explicit user approval. Then execute. The workflow pattern across this session was: (a) analyze and propose in markdown, (b) wait for approval, (c) execute with verification, (d) summarize what changed. Even when the task seemed mechanically simple.

**Alternatives considered:** Just execute each task and iterate — faster on the happy path, more rework on the unhappy path.

**Why this choice:** The analyze-first cadence caught real issues in this session before they shipped. Specific examples:

- **Description-vs-ShareTagline split (#3 above):** Without the analysis pass, the canonical would have used a single `{{Description}}` field for both meta and OG/Twitter. Lower-quality share previews everywhere. The analysis surfaced the pre-existing different-strings authoring on `best-pizza` and led to the two-field split.
- **style.css prune (#11 above):** Without the dependency audit, the full prune would have shipped. 5 top-level pages would have visually broken. Operator would have had to revert under pressure rather than discover the constraint cleanly.
- **Top-4 vs Top-5 for `best-new-restaurants` (#4 above):** Without the analysis pass, would have padded with a fabricated 5th entry from training data — the exact failure mode this site is positioned against.

The cost of writing an analysis (one document, 5–15 minutes of model time) is much less than the cost of one "we shipped a bug, now reverting" cycle. The pattern is now a workflow norm — see `_strategy/HANDOFF.md` and `_strategy/WORKFLOW.md` for how it carries forward to the next session.

---

## 13. Detail-page design decisions (Step 2 of master plan)

**What was decided:** Eight design choices for the per-restaurant detail pages introduced in step 2 of the master plan. Captured here as a single entry rather than eight separate ones because the choices form a self-consistent system — they were proposed and approved together, and several are paired (Q5/Q8, Q1/Q6).

The full analysis lives at `rankings/_detail-page-design.md`. The decisions:

1. **URL pattern:** `/restaurants/{slug}.html`. Mirrors the existing `/rankings/{slug}.html` convention. Compatible with both plausible multi-city architectures (subdomain → zero retrofit; path-prefix → mechanical bulk migration).

2. **Template approach:** Hybrid — extend `best-new-coffee-shop`'s body shape and chrome, replace single-winner-specific elements (the "Suggest a different winner" CTA reads wrong on a detail page), add detail-page-specific modules (rankings cross-link section, future-proof slots for badge + claim CTA).

3. **Schema type:** Per-restaurant most-specific applicable @type, defaulting to `Restaurant`. Extends the per-page-configurable pattern from #5 above. Field policy split into required (won't ship without), strongly-recommended-where-data-exists, and out-of-scope-pending-other-workstreams (the latter excludes `aggregateRating` per #9 and `acceptsReservations` to avoid implying monetization path C).

4. **Editorial scope:** Stub-then-flesh. Pages ship with a defined minimum stub (name, hero tagline, real address, cuisine + neighborhood sentence, "Appears on" cross-link, optional structured data where available). Body editorial is added later, one tight commit per restaurant. Fabrication and auto-generation explicitly rejected as violations of the brand wedge documented in `_strategy/CONTEXT.md`.

5. **Content fields:** Drafted set in the analysis file. Roughly doubles canonical's count. Future-proof slots for badge image (flywheel) and claim CTA (monetization path B) declared in template but empty until adjacent workstreams activate.

6. **Badge anchor + slug stability:** URL pattern from #1 confirmed badge-friendly. Slugs are stable through rebrands — a renamed restaurant keeps its original slug, with the new name in the page title. Rationale: badges placed on restaurant websites and storefront stickers keep working without coordinating a redirect cascade.

7. **First deliverable scope:** Pilot with `best-pizza`'s 5 detail pages, then bulk-port the rest. Mirrors the proven step-1 pattern (build canonical → port via 1 page → bulk-port). Catches template/schema/data-collection issues on 5 pages instead of 37.

8. **Per-restaurant data store:** Single JSON file at `data/restaurants.json` rather than inline-per-page. Compatible with both forks per `_strategy/CONTEXT.md` line 149; inline forecloses Fork B affordances (vote aggregation, claim flow, multi-city). Read-time strategy: build-step substitution, paired with master plan step 4 (kill Tailwind CDN) which introduces a build step anyway.

**Convergent side effects** (noted explicitly so they're not surprises later):
- The `best-new-coffee-shop` per-page meta workstream (currently in `_strategy/TRACKED.md`) resolves as a natural side effect of #2 + #3 — the same schema profile applies. Move that workstream into the step-2 execution scope.
- The `data/restaurants.json` store is also infrastructure for vote aggregation, claim flow, and multi-city — currently all deferred. Step 2 builds the foundation ahead of need.
- The build step master plan step 4 requires gets pre-justified by step 2's data store — no longer a step-4-specific concern.

**Alternatives considered for each decision:** documented in detail in `rankings/_detail-page-design.md`. Most notable rejections: auto-generated editorial body (#4, brand-wedge violation), inline per-restaurant data (#8, forecloses Fork B), all-37-at-once big-bang ship (#7, risk concentration), URL pattern with city prefix today (#1, prematurely commits to one of two equally-likely multi-city architectures).

---

## 14. Detail-page pilot strategic decisions (Step 2 of master plan)

**What was decided:** Four strategic choices that emerged during the data-collection pass for the step 2 pilot port. Captured here as a single entry rather than four separate ones because the choices are tightly coupled — they together define how detail pages handle real-world restaurant complexity that the design analysis (#13) didn't anticipate.

The choices became necessary when actual restaurant data revealed three structural cases the design analysis hadn't covered: a Mt Pleasant restaurant on a "Charleston" ranking page (Toni's), a mobile food vendor with no fixed address (Dough Boyz), and multi-location restaurants (Toni's, D'Allesandro's). The decisions:

1. **Editorial scope: greater Charleston / Lowcountry, not Charleston peninsula.** Mount Pleasant, North Charleston, Daniel Island, James Island, West Ashley, Folly Beach, Sullivan's Island, and Isle of Palms are all editorially "Charleston" for the purposes of Voted On By Locals rankings. The brand wedge is greater Charleston as locals experience it, not the literal city limits.

2. **Structured data uses literal municipality, not the editorial umbrella.** A Mount Pleasant restaurant gets `addressLocality: "Mount Pleasant"` in JSON-LD, NOT `"Charleston"`. The editorial framing ("Charleston") lives in page prose, `<title>`, and meta description; the structured data tells the truth about which municipality the building is in. Same pattern as Disney World listed in Bay Lake, FL while marketed as "Orlando." This preserves both the editorial brand identity and Google's local-search accuracy.

3. **Mobile food vendors use the `FoodEstablishment` schema with `areaServed`, not `Restaurant` with `address`.** Dough Boyz (a mobile pizza pop-up) gets `@type: "FoodEstablishment"`, all address sub-fields except locality/region set to null, and a new `areaServed` field carrying descriptive operating-area text. Visible "Where to find it" sidebar block is replaced with "Area served" pointing customers to the vendor's social channels for current location/schedule. Pattern is reusable for future food trucks, pop-ups, and mobile vendors.

4. **Multi-location restaurants get one detail page per brand, not per location.** A restaurant with multiple locations (Toni's: Mt Pleasant + Wando; D'Allesandro's: Charleston + Summerville + Greenville) gets a single detail page at the brand-level slug (`tonis-detroit-style-pizza`, `dallesandros-pizza`) with the primary location prominently featured. A "Locations" section inside the page will hold additional locations with their own addresses and hours via per-location `Place` microdata, preserving most per-location SEO value without slug proliferation. The pilot ships primary-location-only per multi-location restaurant; the Locations module is a tracked workstream for activation when a second multi-location restaurant ships.

**Alternatives considered:**
- For #1: scope strictly to Charleston peninsula (rejected — would exclude well-loved local restaurants Charleston locals consider part of their food scene)
- For #2: flatten all addresses to "Charleston" for editorial consistency (rejected — misrepresents the structured data, hurts local SEO, and Google treats fabricated location data as deceptive markup)
- For #3: skip mobile vendors entirely from rankings (rejected — Dough Boyz is a real, voted-on Charleston restaurant; excluding it because of an address-shape limitation would distort the rankings); use `Restaurant` with a fake address (rejected — fabrication, violates the brand wedge)
- For #4: one detail page per location with disambiguating slugs like `dallesandros-pizza-charleston` / `dallesandros-pizza-summerville` (rejected — operator framing emphasized highlighting the restaurant brand identity over per-location SEO; slug proliferation also weakens the badge anchor model from #13.6)

**Convergent side effects:**
- DECISIONS #13.4 (stub-then-flesh editorial) handled cleanly by the pilot — minimum-stub pages shipped without fabricated body copy, all REQUIRED fields present.
- The new `areaServed` field is now part of the JSON schema for ALL restaurants (4 of 5 with null, 1 set). Future mobile vendors land cleanly without schema migration.
- The generator script (`scripts/generate_detail_page.py`, commit 9c6b3f7) encodes all 4 decisions in code. The decisions and their implementation are now coupled — changing the decisions requires updating the script + regenerating affected pages.

**Where the resolution shows up in the codebase:**
- Decision #1: editorial scope is implicit in the rankings (Toni's appearing on `best-pizza` validates Mt Pleasant inclusion) and in the step-2 commit messages
- Decision #2: literal municipality values in `data/restaurants.json` for tonis-detroit-style-pizza ("Mount Pleasant") and park-pizza-co ("North Charleston")
- Decision #3: dough-boyz entry in `data/restaurants.json` (schemaType="FoodEstablishment", null address fields, areaServed populated) + the template's intentional decision #9 + the script's mobile-vendor branch
- Decision #4: pilot-shipped pages for tonis-detroit-style-pizza and dallesandros-pizza both use brand-level slugs with primary locations only; the Locations module tracked in `_strategy/TRACKED.md`

**Earlier-session details that are now part of this resolution:**
- The data-collection workflow (Claude chat for web research, Claude Code for repo writes) — see `_strategy/WORKFLOW.md` extension implicitly approved this session
- Anti-fabrication wedge applied at the field level: Toni's hours stay null because no reliable source could be found; Dough Boyz priceRange stays null because mobile-vendor pricing varies too much. Visible HTML uses honest fallback copy ("Hours vary — see [website]") rather than fabricated values. Per template intentional decision #10.

---

## #15 — Step 3 cross-linking: defer breadcrumbs entirely; extend #14.2 locality logic back to ranking ItemList

**Date:** 2026-05-03
**Context:** Step 3 (schema cross-linking on rankings) for `best-pizza.html` — pilot scope. Two of the five design questions in `rankings/_step-3-design.md` were non-obvious enough to log here; the other three (visible HTML cross-links, per-item @type mirror, verification recipe) are mechanical follow-ons of established conventions.

### Q3 — defer BreadcrumbList schema entirely (A over B/C/D)

The mechanical option (B: ranking-only `Home → Best Pizza`) is tempting because it costs ~5 minutes per page and Google sometimes renders 2-node breadcrumbs in SERPs. We declined it.

**Why:** the high-value version is the 3-node detail-page case (`Home → Best Pizza → {Restaurant}`), which requires touching the detail-page template — out of step 3's bootstrap-defined scope. Shipping the ranking-only version locks in a 2-node convention that gets retrofitted when the 3-node version lands later, and the cleanest path is to add ranking + detail breadcrumbs in one pass once detail-page coverage is global. Tracked as a workstream in `_strategy/TRACKED.md`, gated on bulk-port completion (or layered into bulk port on a per-ranking basis).

**Trade-off accepted:** small near-term SEO opportunity cost on the 8 ranking pages until the workstream activates. Acceptable given the bulk port is the gating activity for everything in this neighborhood.

### Q5 — reconcile ranking-page addressLocality to literal municipality (B over A/C)

Detail pages ship with literal municipalities per #14.2 — Toni's = "Mount Pleasant", Park Pizza Co = "North Charleston". The current ranking-page ItemList sets `addressLocality: "Charleston"` for all 5 entries, an editorial-rollup convention that predates #14.2.

The moment step 3 wires `url` cross-links between the two documents, the same restaurant carries two different `addressLocality` values across the structured-data graph on the same site. A search-engine entity resolver could legitimately flag the inconsistency.

**Why B (reconcile in the same PR):** the change is two locality strings; the same JSON-LD block is being touched anyway for the `url` fields; deferring leaves a contradiction the bulk port will inherit on every ranking page with a non-Charleston-municipality entry. Fixing the pattern at best-pizza now sets the right convention for the bulk port — as detail pages ship per ranking, the ranking-page locality reconciles in the same PR.

**Why not A (keep separated):** treating ItemList as "editorial rollup" and detail-page schema as "literal entity" is defensible in the abstract, but the cross-link mechanic of step 3 binds the two documents into one structured-data graph in Google's eyes. The "different scopes" framing dissolves once the url field exists.

**Why not C (defer as tracked workstream):** trivial enough to ship now; deferring just multiplies the same 2-line edit across 7 future ranking-page PRs.

**Trade-off accepted:** broadens step 3's strict "cross-linking only" scope by 2 lines. Surfaced explicitly in the design doc; not silent.

**Convention going forward:** when a ranking page's detail pages ship, the ranking-page ItemList's `addressLocality` per item reconciles to the literal municipality used on the corresponding detail page in the same PR. This makes #14.2 a property of the structured-data graph as a whole rather than detail-pages-only.

---

## #16 — Featured-winner JSON-LD `url` points at the page itself

**Date:** 2026-05-04
**Context:** PR #12 — adding JSON-LD to `best-new-coffee-shop.html`. The page features a single winner (Babas on Wentworth) — the location that won "best new coffee shop." Babas-the-brand has 3 locations (Cannon, Meeting, Wentworth); the existing detail page at `/restaurants/babas-on-cannon.html` describes Cannon specifically per DECISIONS #14.4 (multi-location restaurants ship primary-location-only until the Locations module workstream activates). No `/restaurants/babas-on-wentworth.html` exists. The featured-winner page is therefore functionally the detail context for the Wentworth location.

### What was decided

The JSON-LD `url` field on a featured-winner page (a single-winner ranking page like `best-new-coffee-shop.html`) points at the **featured-winner page itself**, not at any detail-page slug.

### Alternatives considered

- **U2 — point at the brand's existing detail page** (`/restaurants/babas-on-cannon.html`). Rejected: misroutes — that page describes Cannon specifically, not Wentworth. The crawler-graph claim becomes "Wentworth's address is at Cannon's URL," which is wrong.
- **U3 — stand up a new detail page at `/restaurants/babas-on-wentworth.html`** in the same PR. Rejected: scope creep, and sets a dubious precedent for future single-winner pages (would multiply detail-page slugs for every featured-winner location whether or not the editorial scope warrants it).

### Why U1

The featured-winner page IS the detail context for the featured location. Pointing JSON-LD `url` at the page itself is the honest claim — "this page is about this entity, here." The asymmetry with detail-page convention (where `url` points at `/restaurants/{slug}.html`) is intentional: featured-winner pages are a different content shape with no separate detail page, and the schema follows that.

### Convention going forward

When a future single-winner page exists (e.g., `best-new-bar`, `best-new-bakery`):
1. JSON-LD describes the specific featured location.
2. JSON-LD `url` is the featured-winner page's own URL (`/rankings/{slug}.html`).
3. If the featured location is also a multi-location brand, no detail-page-slug retrofit is required — the brand-level detail page (if one exists from the bulk port) describes its primary location independently.
4. When the Locations module workstream activates, the cross-reference between brand and Wentworth-location may surface via `branchOf` / `parentOrganization` from the brand's detail page side, not from the featured-winner page side.

### Trade-off accepted

Featured-winner JSON-LD doesn't cross-link to the brand's detail page in the structured-data graph. This is acceptable because (a) the editorial cross-link still exists in HTML (the detail page for the brand will mention or link to the featured location once Locations module ships), and (b) over-engineering the JSON-LD graph for a single page when the cross-reference will be established from the other direction is YAGNI.

---

## #17 — Multi-location restaurant rendering pattern (Locations module)

**Date:** 2026-05-05
**Status:** Decided
**Anchor:** DECISIONS #14.4 (one brand-anchored detail page per multi-location restaurant), DECISIONS #14.1 (editorial scope: greater Charleston), DECISIONS #16 (brand-side cross-link convention).

### Decision

1. **Data shape.** Additive `locations[]` array on `restaurants.json` entries. Single-location entries are unchanged (array absent or `null`); multi-location entries gain the array. A `primaryLocationLabel` field was considered and rejected — the primary presents anonymously in the existing sidebar, so no label field is needed.

2. **JSON-LD pattern.** Top-level Restaurant (or subclass) JSON-LD is unchanged for the primary. Multi-location entries additionally gain an `@id` of form `<canonical>#brand` and a `subOrganization` array with one entry per secondary. Each `subOrganization` entry has `@type` matching the parent, `@id` of form `<canonical>#<location-slug>`, `name` formatted `"<Brand> — <Label>"`, a full PostalAddress `address`, `telephone`, `openingHours`, and a `parentOrganization` back-reference to the top-level `@id`. Rationale: Google's preferred pattern is one page per location, which we deviate from per DECISIONS #14.4 to preserve brand identity and avoid slug proliferation. The "intentional and clearly separated" multi-entity pattern with unique `@id`s is the supported single-page alternative; `subOrganization` with `parentOrganization` back-references establishes the brand→branch relationship cleanly without requiring a separate top-level `Organization` node.

3. **UI pattern.** The sidebar is unchanged for all restaurants — the primary location's address/hours/phone/website/price block stays where it is on every page. Multi-location pages add a full-width "Other locations" section below the editorial body and above the "Appears on" cross-link, with one card per secondary (label heading + address + condensed hours + phone). One pattern scales N=2 through N=5 without per-page branching.

4. **Editorial scope.** Only in-scope locations (currently greater Charleston per DECISIONS #14.1) appear in `locations[]` and the corresponding JSON-LD `subOrganization`. Out-of-scope locations (e.g., Home Team BBQ Aspen CO / Columbia SC / Greenville SC Upstate; D'Allesandro's Greenville SC Upstate) are excluded entirely from both the data and the rendered page. TRACKED carries follow-ups for re-inclusion when editorial scope expands.

### Implementation status

- Schema documented this PR (schemaVersion 1.1, template docblock decision #11, this entry).
- Template + generator + Babas pilot follows in the next PR.
- Data populate for the remaining 9 multi-location restaurants in a subsequent PR.

---

## #18 — Cuisine-name redundancy dedup

**Date:** 2026-05-05
**Status:** Decided
**Anchor:** TRACKED workstreams "Title verbosity for cuisine-name overlap" and "OG meta-line dedup when restaurant name contains cuisine descriptor" — both shipping in this PR. The two TRACKED entries originally proposed surface-named override fields (`titleCuisine`, `ogMetaCuisine`); the design pass collapsed those into a single display-side override (`displayCuisine`) since the same redundancy class affects four mechanical surfaces and a per-surface override would multiply the override-field count without adding expressive power.

### Decision

1. **Data shape.** Single optional `displayCuisine` field (string, nullable) on `restaurants.json` entries. Drives all mechanical display surfaces; no per-surface variant. Single-source-of-truth: when present, used uniformly across `<title>`, `og:title`, `twitter:title`, hero subtitle, and OG image meta-line.

2. **Auto-detect rule.** When `displayCuisine` is null, the generator suppresses cuisine in mechanical display surfaces if normalized cuisine is a substring of normalized name. Normalization: lowercase, NFD-strip-diacritics (`Café` → `cafe`), `&` → `and`, strip apostrophes and other punctuation, collapse whitespace. The `&`/`and` and diacritic folds catch the trigger case (Harbinger: name "Cafe & Bakery" + cuisine "Café and Bakery"). Apostrophe stripping catches names like Toni's, D'Allesandro's, Ted's.

3. **Resolution order at render time.** `displayCuisine` (if non-null) → auto-detect suppression (if cuisine in name) → `cuisine` as-is. Override beats auto-detect because the override is the expression of editorial intent ("we explicitly want this short form"), while auto-detect is the heuristic fallback for the common case.

4. **Mechanical-surfaces-only scope.** Affected surfaces: detail `<title>`, og:title, twitter:title, hero subtitle "Cuisine · Neighborhood", OG image rendered meta-line. NOT affected: detail `<meta description>`, og:description, twitter:description. The hand-authored `description` and `shareTagline` fields may legitimately mention cuisine words as part of natural prose (e.g., Harbinger's shareTagline "Charming King Street cafe and bakery, voted best by Charleston locals." — cuisine words present, but as prose, not a separate slot). Mechanical suppression on prose would mangle editorial. Editorial review of those fields is a separate filed follow-up.

5. **JSON-LD `servesCuisine` preservation.** Always uses the raw `cuisine` field — independent of display resolution. Reasoning: `servesCuisine` is read by Google's entity-resolution graph, not by humans. The redundancy concern is human readability; entity resolution wants the most specific true cuisine label. Keeping `servesCuisine` raw preserves entity-resolution accuracy regardless of what the display renders.

### Cuisine-field corrections shipped in the same PR

- **Tutti Pizza factual correction.** `cuisine` field was "Neapolitan Pizza"; corrected to "New York-Style Pizza" based on Post & Courier coverage and Tutti's own Tock listing. Discovery context: surveying name+cuisine pairs for the dedup workstream surfaced the misclassification — Tutti's name doesn't contain "Neapolitan" so auto-detect wouldn't catch it; verification of the field exposed the editorial drift. `displayCuisine` set to "New York-Style" (drops the redundant "Pizza" word, since name already contains it). Editorial fields (tagline, description, shareTagline, keywords) still reference "Neapolitan" — flagged as part of the editorial-review follow-up.
- **Second State editorial precision.** `cuisine` field was "Coffee Roastery"; refined to "Specialty Coffee Roaster" — matches Second State's own positioning more precisely. `displayCuisine` set to "Specialty Roaster" (drops "Coffee" which name already contains).

### Trade-offs accepted

- **Auto-detect heuristic may produce false positives or negatives** as the dataset grows. False positive: a future restaurant whose name coincidentally contains its cuisine word but where the editorial intent is to keep cuisine displayed (e.g., a name-twin coincidence). False negative: a future restaurant with a synonym match that the substring rule misses (e.g., name "Espresso Bar X" + cuisine "Coffee Shop"). The `displayCuisine` override path handles both cases — override is the escape hatch for any auto-detect mistake.
- **Two paths instead of one** (override + auto-detect) is more complex than a single approach (e.g., always require operator-curated `displayCuisine`). Accepted because: (a) the auto-detect rule catches the common case mechanically without per-restaurant editorial work; (b) the override path is needed anyway for the rename cases like Tutti / Second State where the cuisine field was edited for accuracy and the display form happens to differ.

### Follow-ups filed

1. **Editorial review of `description` + `shareTagline` cuisine redundancy** across the 9 dedup-affected restaurants. Mechanical display surfaces handled by `displayCuisine` + auto-detect (this PR); hand-authored prose fields may still contain redundant cuisine words by editorial choice. Pass through when next editing those fields, or never if redundancy reads as natural prose.
2. **Cuisine-field accuracy audit** across all 33 restaurants. Tutti's "Neapolitan Pizza" misclassification was discovered incidentally during this workstream; other entries may have similar drift. Trigger: when next touching `restaurants.json` data significantly, or proactively if entity-resolution issues surface in GSC.

### Implementation status

- Schema documented this PR (schemaVersion 1.2, template docblock decision #12, this entry).
- Generator + OG-image pipeline updated this PR (`scripts/_cuisine_dedup.py` shared module + step_13 + `compose_detail_meta`).
- 9 detail pages + 9 OG PNGs regenerated this PR.
