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

---

## #19 — Featured-winner ranking launch recipe

**Date:** 2026-05-06
**Status:** Decided
**Anchor:** DECISIONS #4 (anti-fab — don't pad to fixed Top-N), #5 (per-page schemaType subclass), #8 (best-new-coffee-shop kept on its own template), #16 (featured-winner JSON-LD `url` points at the page itself).

### What was decided

The recipe for launching a new top-level ranking as a featured-1 (single-winner format), now established across two launches: `best-new-coffee-shop` (Jan/Feb 2026) and `best-bakery` (May 2026). Captures both the file-set inventory and the conventions that should propagate forward.

### Template

Copy `rankings/best-new-coffee-shop.html` as the starting point — NOT `_template-canonical.html`, which is Top-N only per #8. Adapt: head meta block, JSON-LD (single Restaurant entity with the per-category subclass), BreadcrumbList, hero h1 + emoji, restaurant name + neighborhood, per-restaurant emoji icons (the featured-1 layout deliberately does carry per-restaurant emoji in the icon group, scoped to this layout — DECISIONS #1's "page-theme only" rule applies to Top-N rows, not the featured-1 icon group), 3-paragraph editorial blurb, italic pull quote, address+hours+phone+website sidebar, "Suggest a different winner" CTA (kept from precedent).

### Subtitle voice

Canonical voice + count framing: **"As voted by Charleston locals. One standout — with more to come."** Mirrors the Top-4 pattern from #4 (`best-new-restaurants` uses "Four standouts — with more to come.") — establishes a unified subtitle pattern for ranking pages with intentional sub-canonical entry counts.

`best-new-coffee-shop` currently uses "The freshest brew in town." (its launch-time poetic register). TRACKED entry filed for retrofit to bring it in line.

### schemaType

Per-page subclass of `FoodEstablishment` per #5: `Bakery`, `CafeOrCoffeeShop`, `BarOrPub`, `NightClub`. Do NOT default to `Restaurant` for non-restaurant categories — the more-specific subclass strengthens the entity-resolution graph and matches what Google's structured-data validator prefers.

### File set

For each new featured-1 launch:

- `data/og_rankings.json` — append `{slug, category, spots: 1}`; bump `_meta.lastUpdated`
- `data/restaurants.json` — append the restaurant entry (full schema)
- `rankings/{slug}.html` — NEW, adapted from best-new-coffee-shop precedent
- `restaurants/{restaurant-slug}.html` — generated via `python scripts/generate_detail_page.py {restaurant-slug}`
- `components/header.html` — add ranking row to dropdown (desktop + mobile) with NEW pill / mobile (New!) styling, positioned above the Top-N divider
- `index.html` — add card to homepage rankings grid (resize grid as needed; 9 cards now use `md:grid-cols-3` after the best-bakery launch)
- `assets/images/og-{slug}.png` — generated via `python scripts/generate_og_images.py --slug {slug}`
- `assets/images/og-restaurant-{restaurant-slug}.png` — same script with the restaurant slug
- `sitemap.xml` — regenerated via `python scripts/generate_sitemap.py` (filesystem scan auto-includes new pages)
- 49+ inlined production pages — refreshed via `python scripts/inline_chrome.py --refresh` (header changes propagate automatically)

Estimated commit shape: 4 commits (data + ranking + detail; nav + grid + inline; OG + sitemap; doc consolidation if needed).

### NEW pill decay rule

60 days from launch. Persistent pill is fine for the first 60 days; after that the pill comes off via manual edit to `components/header.html`:
- desktop: remove the trailing `<span ...>NEW</span>` and the `relative` class on the parent `<a>`
- mobile: replace the `text-brand-orange bg-orange-50 font-bold` classes + "(New!)" suffix with the standard `text-gray-700 hover:bg-orange-50 hover:text-brand-orange font-medium` + plain title
- `index.html` homepage card: remove the `border-brand-orange/20` border highlight + corner NEW ribbon, switch to plain `border-transparent hover:border-brand-orange/20`

Then `python scripts/inline_chrome.py --refresh` to propagate. TRACKED items file each removal at launch+60d.

The 60-day window is editorial — a featured-1 launch is news for ~2 months in our cadence; after that the page is just another ranking and the NEW pill becomes visual noise. Discoverability via the dropdown ordering (featured-1 entries stay above the Top-N divider) is sufficient long-term.

### Social-card pipeline (deferred)

The `social/` pipeline (PR #28) supports Top-N rankings only. The data loader (`social/src/data.ts:32-95`) expects `ItemList` JSON-LD + body row anchors with `<a href="/restaurants/{slug}.html">` — featured-1 has neither (single Restaurant entity per #16, single editorial card body). Featured-1 launches skip social cards until the loader supports the featured-winner shape. TRACKED workstream filed.

### Trade-off accepted

The featured-1 layout duplicates content fields between `rankings/{slug}.html` (hero, blurb, sidebar) and `restaurants/{restaurant-slug}.html` (name, address, hours, etc.). When the restaurant's data changes (e.g., hours shift), both files need updating. Acceptable for the launch cadence (a handful of featured-1 pages over the year); if duplication becomes painful, a generator pass for the ranking page (analogous to `generate_detail_page.py`) becomes the obvious next move.

---

## #20 — Ranking length is per-page editorial

**Date:** 2026-05-06
**Status:** Decided
**Anchor:** DECISIONS #4 (Top-4 framing for `best-new-restaurants`), #8 (best-new-coffee-shop kept on its own template), #19 (featured-winner ranking launch recipe).

### What was decided

The canonical Top-5 (per `_template-canonical.html`) is the default ranking length for pages launching with a full slate, but **ranking length is editorial per page**. Documented exceptions:

- **Featured-1** (single-winner, separate template per #8): `best-new-coffee-shop`, `best-bakery`. Used when one strong local-consensus pick exists and the slate isn't full. Subtitle frames the count: "One standout — with more to come."
- **Top-4**: `best-new-restaurants` (per #4). Used when 4 confident picks exist but a 5th would require fabrication. Subtitle: "Four standouts — with more to come."
- **Top-5** (canonical default): `best-pizza`, `best-tex-mex`, `best-coffee-shops`, `best-casual-spots`, `best-nice-restaurants`. Subtitle: "As voted by Charleston locals."
- **Top-7**: `best-burger` (PR #27). Used when real local consensus pushes past the canonical — Charleston has a deeper burger scene than 5 spots can hold honestly. No "more to come" framing — the slate is full as-is. Subtitle: "As voted by Charleston locals."

### Why this matters

DECISIONS #4 already established the principle (don't pad to fixed N with fabrication) but framed it as a single-page exception. The practice has now generalized: ranking length depends on the depth of real local consensus + editorial judgment about when "more to come" framing is appropriate vs. when the slate is naturally full. This entry promotes the practice from per-page exception to documented convention.

### When promoting / demoting ranking length

- **Top-N → featured-1**: only if the slate genuinely shrinks (rare; most natural growth is the other direction). Demoting an established Top-N to featured-1 should be documented per-page.
- **featured-1 → Top-N**: natural growth path. Replace the featured-1 template body with the canonical Top-N body, populate the new slate, drop the "more to come" framing if the slate is now full. Keep the featured-1 winner at position 1 unless local consensus shifts.
- **Top-5 → Top-7+**: editorial expansion when consensus depth justifies it. Cautious move — ranking-length inflation is a slippery slope. Trigger should be specific local-consensus signal, not "we want more content."
- **Top-7 → Top-5**: rare. If consensus thins, demote. Don't pad.

### Trade-off accepted

Per-page ranking length means the site doesn't have a uniform "Top 5" brand promise. Acceptable because the editorial wedge (real local consensus) is the actual brand promise; ranking length is a consequence of consensus depth, not a target.

---

## #21 — Sidebar icon convention on featured-1 ranking pages

**Date:** 2026-05-06
**Status:** Decided
**Anchor:** DECISIONS #19 (featured-winner ranking launch recipe).

### What was decided

The sidebar icon convention as currently used on the two featured-1 ranking pages (`rankings/best-bakery.html` and `rankings/best-new-coffee-shop.html`):

- **Library:** Heroicons v1 solid (https://github.com/tailwindlabs/heroicons/tree/v1.0.6).
- **viewBox:** `0 0 20 20` for every sidebar icon. NOT the 24×24 v2 / Lucide grid — keeping a single icon-grid convention across the sidebar set.
- **Size class:** `h-5 w-5`.
- **Color:** `text-brand-orange` on the SVG element + `fill="currentColor"` on the SVG root + no per-path fill (so the orange propagates via currentColor inheritance).

Current sidebar icon set in use: `location-marker` (Address row), `clock` (Hours row), `phone` (Phone row), `external-link` (Website row). Pin / clock / phone are heroicons-v1 solid name-matched; the Website row uses `external-link` (NOT `globe` or `globe-alt`) — see "Website icon choice" below.

### Scope: how icons render, not which rows exist

The two featured-1 pages currently have different sidebar **field sets**: best-bakery shows Address + Hours + Phone + Website (4 rows), best-new-coffee-shop shows Address + Hours only (2 rows). This convention is about HOW icons render in a row, not WHICH rows are present.

Whether to expand best-new-coffee-shop's sidebar to match best-bakery's is a separate editorial question — filed as a TRACKED follow-up ("Featured-1 sidebar parity").

### Website icon choice

Heroicons v1 has a `globe-alt` variant whose busy interior (continents-blob pattern) renders as ambiguous orb shapes at h-5 w-5 (20px) — easy to mis-read as pin-adjacent next to the actual address pin. Initial best-bakery shipped with globe-alt; user feedback flagged it as visually weak.

Replaced with `external-link` (square + diagonal-arrow). Cleaner at 20px, and arguably a stronger UX signal for a Website link — communicates "this opens externally" more directly than a globe metaphor.

### Don't reach for other libraries

Don't introduce Lucide, Heroicons v2, or other icon libraries for the sidebar without widening the entire sidebar icon set in one pass. Mixing libraries within the same sidebar set creates visual inconsistency (different stroke weights, different grids, different filled-vs-outlined treatment). If a future redesign wants to migrate, do all four icons in one PR + update this entry.

### Trade-off accepted

The sidebar icon set is locked into Heroicons v1, which is no longer actively maintained (Heroicons moved to v2 in late 2022). Acceptable because the v1 icons in use are functional, the visual style is internally consistent, and migration to v2 (or Lucide) is a deliberate widening exercise rather than ad-hoc drift.

---

## #22 — TRACKED filing requires same-PR file edit, not just PR-description prose

**Date:** 2026-05-06
**Status:** Decided
**Anchor:** Pattern observed across PRs #29, #30, and the TopNLayout safe-zone retrofit.

### Pattern observed

Three recent PRs included PR-description prose claiming a follow-up was "filed as TRACKED" without the corresponding `_strategy/TRACKED.md` edit landing in the same PR's diff. Each surfaced as a gap when the next PR tried to "close" the entry that didn't exist:

- **PR #29** (best-bakery launch) — areaServed-omission follow-up was implicit in the PR description's "deviations" section, but the `_strategy/TRACKED.md` entry didn't land until a separate one-off commit (`f2f97ff`) after the user flagged the gap.
- **PR #29** (same PR) — original "TRACKED #9" Website-icon issue was referenced informally in conversation but never filed in `TRACKED.md`. The closure commit (PR #31) had to add a Resolved entry without a matching Open entry to close.
- **PR #30** (social pipeline featured-1 support) — description said "Filed as follow-up TRACKED entry to regenerate [the burger reel]." The TRACKED.md edit didn't land. The retrofit PR (this one) had to add a Resolved entry acknowledging the never-filed open entry.

### Discipline

When a PR description includes any of the following language about future work:
- "Filed as TRACKED [entry/follow-up/workstream]"
- "Added to TRACKED"
- "Queued in TRACKED"
- Equivalent phrasing implying a TRACKED edit

…the same PR's diff MUST include a matching `_strategy/TRACKED.md` change. PR-description prose alone is insufficient — the file is the source of truth, the prose is documentation that points at the file.

If the work doesn't warrant a TRACKED entry (small enough to defer informally, or genuinely already covered elsewhere), the PR description should not use "filed as TRACKED" language. Use "worth filing if it recurs" or "consider as a follow-up" — language that doesn't claim a file edit exists.

### Verification at PR review time

When reviewing a PR whose description uses any of the trigger language above:
- `git diff main..HEAD --stat | grep TRACKED` should show a `_strategy/TRACKED.md` change.
- If absent, the PR description language is wrong — either the TRACKED edit needs to land before merge, or the PR description needs softer phrasing.

### Future enhancement (deferred)

A pre-merge CI check could automate this: parse the PR body, regex for the trigger language, then assert `_strategy/TRACKED.md` appears in the diff. Not implemented today — current discipline + manual verification at review is sufficient for the cadence we ship at.

### Trade-off accepted

The discipline costs ~15 seconds per PR (run grep, edit TRACKED.md inline if needed). The trade-off vs. drift cost: every gap discovered later requires (a) investigation to confirm the entry doesn't exist, (b) a Resolved entry that has to acknowledge the gap, (c) some friction surfacing the gap to the user. Cumulatively much more expensive than the same-PR file edit.

---

## #23 — Top-2 ranking precedent + NEW pill is featured-1 only

**Date:** 2026-05-07
**Status:** Decided
**Anchor:** DECISIONS #4 (Top-4 framing), #19 (featured-winner ranking launch recipe), #20 (ranking length is per-page editorial).

### What was decided

Two related conventions captured together because the second falls out of the first as soon as a Top-N launch happens.

**1. Top-2 joins the documented ranking-length precedents.**

DECISIONS #20 enumerates featured-1, Top-4, Top-5, Top-7. **Top-2** is now a fifth precedent. First Top-2 launch ships in this PR (`best-frozen-margarita`). Subtitle voice for sub-canonical Top-N follows the pattern from #4 + #19's "more to come" framing:

> "As voted by Charleston locals. Two standouts — with more to come."

The unified pattern across all sub-canonical entry counts:
- featured-1: "One standout — with more to come." (#19)
- Top-2: "Two standouts — with more to come." (this entry)
- Top-4: "Four standouts — with more to come." (#4)
- Top-5 and Top-7: no count-framing, slate is full as-is (#20)

Promotion path is implicit: if real local consensus expands the slate, drop the "more to come" qualifier and bump the entry count. Don't pad with fabrication to reach a target N (#4 anti-fab principle).

**2. NEW pill is featured-1 launch ceremony only.**

DECISIONS #19's launch recipe specifies the NEW pill / mobile-(New!) styling for featured-1 launches (`best-new-coffee-shop`, `best-bakery`). The recipe doesn't address Top-N launches because at the time of #19 there had been no Top-N launch. This entry clarifies the implicit scope: **Top-N launches do NOT get the NEW pill**, regardless of being newly added.

Reasoning: discoverability for Top-N launches is sufficient via dropdown ordering (the new entry sits at the end of the Top-N cluster, naturally drawing the eye on first visit). The NEW pill is doing a different job for featured-1 — signaling that a single-winner page exists at all (smaller cluster, easier to miss without ceremony). Top-N pages are dropdown-ordinary by design.

The 60-day decay rule from #19 therefore does not apply to Top-N launches — there is nothing to decay.

### Top-N launch recipe — deferral closed

This section previously said: *"one launch isn't enough to confirm a pattern ... defer recipe documentation until a second Top-N launch shows what the recipe genuinely shares vs. what was specific to this PR."*

**That second launch happened: `best-wings` (Top-3, PR #39, 2026-08-24).** It was the confirming case the deferral was waiting for, and a good one — unlike best-frozen-margarita, where both restaurants already existed on another ranking, best-wings required net-new restaurant entries and therefore exercised the sourcing, schema-creation and OG-generation paths that PR #34 never touched.

The recipe below is now formalized. The provisional list it replaces was correct as far as it went; what follows adds the parts only a from-scratch launch could reveal.

### Top-N launch recipe (formalized)

#### 0. Candidate sourcing — do this before anything else

**Start with roughly twice your target N.** Expect heavy attrition on status checks. On best-wings, of the five restaurants originally proposed, **three were excluded** — and, more starkly, **all three net-new candidates failed**:

| Candidate | Status | Outcome |
|---|---|---|
| Home Team BBQ | pre-existing entry | passed liveness |
| Moe's Crosstown Tavern | pre-existing entry | passed liveness |
| Tru Blues House of Wings | net-new | **excluded** — contested status |
| Nigel's Good Food | net-new | **excluded** — location set contested |
| Dashi | net-new | **excluded** — permanently closed 2026-06-14 |
| Hannibal's Kitchen | net-new, substituted in | passed |

A fourth net-new candidate had to be found to land a Top-3. Scale that: a fresh Top-5 with no pre-existing entries should start from ~10 candidates. Budget the sourcing pass as real work, not a formality — it is where the launch actually gets decided.

#### The two-gate sourcing rule

Every candidate must clear **two independent gates**, and the admissible evidence differs:

| Question | Own website | Dated third-party signals |
|---|---|---|
| **Identity** — brand name and spelling, address, phone, menu, what it serves | **AUTHORITATIVE** | corroborating only |
| **Liveness** — is it currently operating, current hours | **INADMISSIBLE** | **REQUIRED** |

Restaurant websites are near-universally maintained for identity and near-universally stale on status. All three failures on best-wings turned on exactly that split:

- **Tru Blues** — its own site is the *best* source for the brand spelling (own header reads "Tru Blues House of Wings", no apostrophe, contra Instagram/Facebook "Tru Blue's" and Tripadvisor "True Blue's") and simultaneously *worthless* as evidence the doors are open.
- **Nigel's** — the own site advertised a Hanahan location with full hours that Yelp had marked closed that same month, while silently dropping the 2011 original that Yelp had marked closed two months earlier.
- **Hannibal's** (which passed) — its own About page still carries a COVID-era line about being closed for in-house dining with patio service only, years stale. Identity came from the own site; hours from three independent listings.

Rules that fall out of this:

1. An own-site page is **never** sufficient evidence of liveness, however current it looks.
2. A **conflict** between sources is disqualifying, exactly like a confirmed closure. Only converging evidence of "open" clears the gate.
3. Distinguish the two failure modes when filing TRACKED: a **conflict** gets a re-verification trigger (Tru Blues, Nigel's); a **confirmed permanent closure** gets a no-trigger record whose purpose is to stop a future session re-proposing it (Dashi).
4. The gate applies to **pre-existing entries too**, not just new ones. Any restaurant about to receive a new listing and a `dateModified` bump must clear it first — the bump is an assertion of freshness, and asserting freshness about a closed restaurant is worse than saying nothing.
5. Verify the **category claim**, not just existence. Hannibal's went on a wings list, so its wings were confirmed on the menu (drumettes in the house batter, per a Post and Courier review) before it shipped. Note that restaurantji's listing surfaces no wings at all — a single-source check would have produced a false negative.

#### `servesCuisine` is list-scoped

**Ranking-page ItemList `servesCuisine` is hand-authored per list. It is NOT a copy of `restaurants.json.cuisine`.** This was undocumented anywhere until now, and it governs **12 of the 40 pre-best-wings ItemList entries**.

The rule: **override the generic, preserve the specific.**

- Where `restaurants.json.cuisine` is a *specific* genre, keep it. Home Team BBQ carries `Barbecue` on best-burger, best-casual-spots *and* best-wings — consistent across the graph even though two of those are not barbecue lists.
- Where it is *generic* (`American` is the usual offender), use the list's category. Moe's Crosstown Tavern is `American` in the data, `Burgers` on best-burger, `Wings` on best-wings.
- Refinements are also legitimate: `Mexican` → `Tex-Mex` on best-tex-mex; `American` → `Contemporary American` on best-nice-restaurants.

This is separate from DECISIONS #18, whose "`servesCuisine` always uses the raw `cuisine` field" rule governs the **detail-page generator** only. Two different documents, two different rules. Do not unify them.

Because these are hand-picked editorial calls, **flag them in the PR body rather than deciding silently.**

#### Ranking length

**Top-3** joins the documented precedents. The full set is now featured-1 / **Top-2** / **Top-3** / Top-4 / Top-5 / Top-7. Sub-canonical counts take count framing per #4 and #19:

> "As voted by Charleston locals. Three standouts — with more to come."

Top-2 and Top-3 both arrived the same way: not as a target, but as what survived honest sourcing. That is the #4 anti-fabrication principle working as designed — **N is an output of consensus depth and verification, never an input.** If sourcing leaves you with three, ship three.

#### The step sequence

1. **Sourcing pass** (section 0 above). Nothing else starts until the roster is settled.
2. **New ranking page** authored from `rankings/_template-canonical.html`, adopting the production JSON-LD pattern (per-item `url` cross-links + `datePublished`/`dateModified` per #15 Q3), NOT the canonical's bare ItemList shape. Trim rows and ItemList positions to N. Note the canonical's row `<h2>` has no anchor — production rows wrap the name in `<a href="/restaurants/{slug}.html" class="hover:text-brand-orange transition-colors">`, which the social pipeline's regex requires.
3. **`data/og_rankings.json`** append `{slug, category, spots: N}`; bump `_meta.lastUpdated`. `spots` is not cosmetic — `spots === 1` routes the social pipeline into the featured-1 renderer.
4. **`data/restaurants.json`** — new entries for net-new restaurants, `appearsOn` append for cross-listed ones. Sweep stale `priceRange`/`hours` opportunistically while the entry is open.
5. **Detail-page regen** via `python scripts/generate_detail_page.py {slug}` — never `--all`, which rewrites every page and destroys the diff. Then **hand-bump `dateModified`** on any page whose `appearsOn` changed; the generator preserves prior dates by design, so regeneration alone leaves them stale.
6. **`components/header.html`** nav entry, Top-N cluster below the divider, **no NEW pill**. Then `python scripts/inline_chrome.py --refresh`.
7. **`index.html`** homepage grid card. Adjust `grid-cols` only if the count genuinely breaks the layout.
8. **`vote.html`** `<option>` appended at end. Top-N only — featured-1 routes discovery through `/suggest-category`.
9. **OG images**: `python scripts/generate_og_images.py --slug {slug}` for the ranking and for each net-new restaurant.
10. **Sitemap**: `python scripts/generate_sitemap.py`.
11. **TRACKED filing** for every exclusion, as a same-PR file edit per #22.
12. **Social assets** — separate follow-up PR cadence, not part of the launch PR.

#### Ordering constraints that will bite

- **`generate_sitemap.py` must run AFTER the `dateModified` bumps.** It reads `dateModified` to build `<lastmod>`. Run it before the bumps and the sitemap ships stale dates, silently. On best-wings this meant deviating from the written step order.
- **The ItemList JSON-LD block must precede BreadcrumbList.** `generate_sitemap.py` parses only the *first* `ld+json` block. Put BreadcrumbList first and `<lastmod>` vanishes with no error and no warning.
- **New ranking and detail pages must exist before `inline_chrome.py --refresh`**, or they ship with stale chrome and `--check` exits 2.
- **`npm run build:css` only if new utility classes appear.** Copying an existing page introduces none; verify with a class-set diff rather than running it reflexively.

#### Environment

**Playwright's Chromium must be installed before `generate_og_images.py` will run**: `python -m playwright install chromium` (~87 MB). `requirements.txt` declares `playwright>=1.40`, but that is the Python package only — the browser binary is a separate download and a fresh machine will not have it. The failure mode is a wall of box-drawing characters telling you to run `playwright install`.

#### Merge

**Set the squash subject explicitly.** This repo squash-merges (linear history, single-parent commits, `(#N)` appended). GitHub defaults the squash subject to the **PR title**, which is prose and will land on `main` without a conventional type prefix. Pass it:

```
gh pr merge {N} --squash --subject "feat: ... (#{N})" --body-file {commit-body} --delete-branch
```

Type must have precedent in this repo: `feat` / `docs` / `fix` / `chore`. Ranking launches are `feat`. Do not invent a type.

#### Traps that look like bugs but are not

- **`{{Emoji}}` in `og-templates/ranking.html`** is declared in the docblock but never substituted by `render_ranking`. It looks like an unfilled-placeholder bug. It is not — the occurrence is inside an HTML comment, and per that template's intentional decision #6 emoji were deliberately removed in schemaVersion 1.1. **Leave it alone.**
- **`{{Emoji}}`, `{{Restaurant#}}` and `{{Tagline#}}` surviving in a shipped ranking page** are likewise inside the REPEATING ROW documentation comment. Every production Top-N page carries them. A placeholder sweep must exclude HTML comments or it will produce false positives.
- **`inline_chrome.py` writing LF while the working copy is CRLF.** `core.autocrlf=true` plus the generator's deliberate `_write_lf` means git stores LF and converts on checkout. The "LF will be replaced by CRLF" warnings are cosmetic; diffs stay minimal.

### Trade-off accepted

The "no NEW pill on Top-N" convention reads as inconsistent at first glance ("a launch is a launch"). Acceptable because the editorial role of the pill is announcement-of-existence (featured-1 has higher risk of being missed), not announcement-of-novelty (Top-N inherits dropdown discoverability for free). The visual asymmetry is functional, not arbitrary.

---

## #24 — Reel rendering retired; card-only social pipeline

**Date:** 2026-08-25
**Status:** Decided
**Anchor:** #19 (featured-winner launch recipe, social-card deferral), #23 (Top-N launch recipe, step 12 "Social assets").

### What was decided

**Reel (`.mp4`) rendering is retired.** The social pipeline is card-only from 2026-08-25. Three reels were ever produced — best-bakery, best-burger, best-frozen-margarita, all in May 2026 — and none since. `best-wings` never got one.

### Removed

| Path | Why it was reel-only |
|---|---|
| `social/scripts/render-reel.ts` | reel entry point; frame loop plus `ffmpeg` stitching |
| `social/src/timing.ts` | imported by `render-reel.ts` and nothing else; every export is frame-based |
| `DESIGN.anim` in `social/src/design.ts` | consumed only by `timing.ts` and `render-reel.ts` |
| `DESIGN.featured1Anim` in `social/src/design.ts` | same |
| `render:reel` npm script | reel entry point |

This also drops the external **`ffmpeg`** binary dependency, which was never declared anywhere — `render-reel.ts` shelled out to it and failed at runtime if absent.

### Deliberately NOT removed

**`social/src/composition.tsx` is untouched.** Its `isReel` branches are now unreachable, but cutting them is surgery inside the file the card renders from, and the risk is not worth the tidiness. What is now dead but retained:

- `const isReel = mode === 'reel'` in both `TopNLayout` and `Featured1Layout` — permanently `false`, because `render-card.ts` is the only remaining entry point and it hardcodes `mode: 'card' as const`.
- Everything after `if (!isReel) return cardEl;` (`TopNLayout`) and `if (!isReel) return composedBody;` (`Featured1Layout`) — the reel canvas wrappers.
- `REEL_SAFE_TOP_PAD` (260) and `REEL_SAFE_SIDE_PAD` (90), and the `sidePad` ternaries that select them. `sidePad` now constant-folds to 40.
- `RowState` / `Featured1State` types and the `rowStates` / `featured1State` props. `effectiveRowStates` still computes, but its `isReel && rowStates` branch is never taken, so every row resolves to `{opacity: 1, yOffset: 0}`.
- `FEATURED1_REEL_ZONES`.

**`DESIGN.reel` is retained on purpose.** `composition.tsx` destructures `reel` from `DESIGN` and its unreachable branches still reference `reel.width` / `.height` / `.padTop` / `.padBottom`. Removing the block while leaving `composition.tsx` alone breaks `npm run typecheck`. The block is annotated in place so it is not later deleted as apparent dead code. It is inert: nothing reads it at runtime.

### Looks broken, is not

Same class as the `{{Emoji}}` trap in #23.

The reel canvas was sized so that its padding wrapped the card body exactly:

```
reel.height 1920 - padTop 285 - padBottom 285 = 1350 = card.height
```

That arithmetic was load-bearing while reels shipped — the reel literally wrapped the same 1350-tall composition in symmetric padding. **It no longer constrains anything.** `card.height` is now free to change without reference to the reel numbers.

**REALIZED 2026-08-25 (#25).** This was written as a prediction; the resize has since happened. `card.height` is now **1440**, so the identity no longer reconciles: `1920 - 570 = 1350 != 1440`. **This is expected, not a bug** — it is the outcome this entry anticipated, and it confirms the reel constants are now fully decoupled from the card. Do not "fix" `DESIGN.reel` to restore the arithmetic, and do not treat the mismatch as evidence of a broken resize. The reel constants are frozen at their retirement values and describe a renderer that no longer runs.

### Card geometry note, recorded while it was verified

The card is a fixed-height flex column with **no `flexGrow` and no absolute positioning anywhere**. Its four zones sum exactly to the card height:

```
headerH 100 + heroH 180 + rowsH 980 + footerH 90 = 1350 = card.height
```

So changing `card.height` alone did **not** reflow — it left unallocated space at the bottom of the column (1440 would have left 90px of dead cream). **Fixed in #25**, which makes `rowsH` derived so the zones always sum to `card.height`. `rowsH` is the natural sink, and it already carries `justifyContent: 'center'` from the PR #37 small-N change, so rows would stay optically centred.

### Verification

The best-burger card was rendered immediately before the removal and again immediately after. **Byte-identical**, 96,531 bytes, sha256 `ea6f5e090524d895aa3b17e012116174ca52b176ee00b17da49a3d53a3604d87`. That is the proof the card path was untouched. `npm run typecheck` exits 0.

### Trade-off accepted

Leaving unreachable reel branches in `composition.tsx` means the file reads as if it still supports two modes. Accepted because the alternative — editing the only file the card renders from, purely for tidiness — risks the one output that still matters, and the byte-identical regression check above only holds because that file was not touched. If reels are ever revived, the branches are still there; if the file is refactored for another reason, strip them then, under a test that re-runs the same byte comparison.

### Existing reel artifacts

The three rendered `reel.mp4` files under `social-assets/` are left in place. That directory is gitignored, so they are local-only and nothing in the repo references them.

---

## #25 — Card height is layout-agnostic; default moved to 1440 (3:4)

**Date:** 2026-08-25
**Status:** Decided
**Anchor:** #24 (reel retirement; recorded the zone-sum coupling this entry resolves).

### The coupling that was removed

`DESIGN.zones.rowsH` was the literal `980`. That happened to equal `1350 - 100 - 180 - 90`, so the four zones summed to exactly `card.height` — by coincidence, not by construction. Nothing enforced it, and nothing flagged it: the card tree has **no `flexGrow` and no absolute positioning**, so a taller canvas would simply have stranded unpainted space at the bottom of the column.

`rowsH` is now **derived**:

```
rowsH = card.height - headerH - heroH - footerH
```

`headerH` / `heroH` / `footerH` stay literal because they are **content-sized** — a fixed lockup, a fixed hero block, a fixed footer line. They do not scale with canvas height. `rowsH` is the **sink** that absorbs the remainder. `DESIGN_ZONES_ROWSH` still overrides if a caller wants to break the identity deliberately.

### Featured-1 had the same bug, independently

`FEATURED1_CARD_ZONES` in `composition.tsx` is a **second, separate height model**: featured-1's root height is the *sum of its own four zones*, not `DESIGN.card.height`. Its `body` was the literal `960`, which happened to equal `1350 - 100 - 200 - 90`. Same coincidence, same latent bug, in a different file.

This was missed by an earlier investigation that only traced `TopNLayout`. It surfaced here by probing rather than reasoning — rendering `best-bakery` with `DESIGN_CARD_HEIGHT=1440` forced, with no code change, produced a 1080x1440 PNG whose cream stopped at 1350 with a **white band across the bottom 90px**. The dimension assertion in `render-card.ts` did *not* catch it, because satori sizes the canvas from `DESIGN.card` regardless of what the React tree asks for. So the failure mode was visual, not a crash.

`FEATURED1_CARD_ZONES.body` is now derived the same way. `FEATURED1_REEL_ZONES` is untouched — that path is dead per #24.

### Why 1440

1080x1440 is **3:4**, which is what Instagram's 2026 grid previews at. A 4:5 card (1080x1350) is trimmed roughly **7 percent top and bottom** on the profile grid, which crops into the hero and the footer wordmark. 1350 remains available at any time via `DESIGN_CARD_HEIGHT=1350`, and the derivation keeps the zone sum correct at that height too.

### What the extra 90px does to the layout

`rowsH` goes 980 -> 1070. At `row.height` 140 that is 7.64 rows of capacity, up from exactly 7.00.

| Ranking | Rows | Used | Slack in rowsH | Reads as |
|---|---|---|---|---|
| best-burger | 7 | 980 | 90 (45 above / 45 below) | comfortable — a clear improvement on 1350, where 7 rows filled `rowsH` with **zero** slack |
| best-wings | 3 | 420 | 650 (325 above / 325 below) | **sparse** — the row block is centred but adrift in the middle of the card |

The sparseness at low N is **not** caused by this change — 3 rows in the old 980 already left 560px of slack. 1440 widens it by 90px. Rows stay optically centred either way because the rows zone carries `justifyContent: 'center'` from PR #37.

If low-N cards should read tighter, the lever is **not** card height. Options, none taken here: scale `row.height` with row count, cap `rowsH` at `rows * row.height` plus a margin and let the hero absorb the rest, or give low-N cards a distinct layout. Left open deliberately — it is an editorial call about how a Top-3 should look, not a geometry bug.

### Verification

Each derivation was proven **behavior-preserving before** the default moved, by rendering at the old height and byte-comparing:

| Check | Result |
|---|---|
| best-burger at `DESIGN_CARD_HEIGHT=1350`, before vs after deriving `rowsH` | **byte-identical**, 96,531 b, sha256 `ea6f5e09...3604d87` |
| best-bakery at `DESIGN_CARD_HEIGHT=1350`, before vs after deriving featured-1 `body` | **byte-identical**, 71,340 b, sha256 `cf41980e...cb87c577` |
| `npm run typecheck` | exits 0 |
| best-wings / best-burger at the new default | both 1080x1440, verified from the PNG headers |

Byte-identity at the old height is the whole point: it proves the derivation computes exactly what the literal did, so the only behavioural change is the one the default flip makes deliberately.

### Trade-off accepted

Two zone models still exist — `DESIGN.zones` for Top-N, `FEATURED1_CARD_ZONES` for featured-1 — and both must now be kept in sync with `card.height` by hand if a fifth zone is ever added. Unifying them was out of scope here; the byte-identical guarantees above only hold because the change to each was minimal. If a third layout appears, unify first.

---

## #26 — Hero and rows compose as one centred content group

**Date:** 2026-08-25
**Status:** Decided
**Anchor:** #25 (derived `rowsH`, 1440 default), PR #37 (small-N row centring — **superseded by this entry**).

### The defect

Hero and rows were **siblings** in the root flex column, each with a fixed zone height:

```
root (column, height = card.height)
  header  height 100                          pinned top
  hero    height 180, justifyContent center
  rows    height 1070, justifyContent center
  footer  height  90                          pinned bottom
```

At low row counts the rows centred *inside their own tall zone* while the hero stayed pinned directly under the header. The slack landed **between the two halves of the content**, stranding the hero at the top and leaving the row block floating in the middle. On a 3-row card that was a **325px gap** between hero and row 1.

### The fix

Hero and rows are now wrapped in a single **content group** of height `heroH + rowsH`, centred as a unit between the pinned header and footer. The rows box becomes content-sized rather than zone-sized, and an explicit `HERO_ROWS_GAP = 40` separates hero from row 1 at every row count.

```
root (column, height = card.height)
  header       height 100                     pinned top, unchanged
  contentGroup height heroH + rowsH, justifyContent center
    hero       height 180                     unchanged internally
    rows       content-sized, marginTop 40
  footer       height  90                     pinned bottom, unchanged
```

Slack now collects **outside** the content — above the hero and below the last row, symmetrically — instead of inside it.

### Measured effect

Zone-level, at the 1440 default:

| | 3 rows (best-wings) | 7 rows (best-burger) |
|---|---|---|
| hero bottom -> row 1, **before** | 325 | 45 |
| hero bottom -> row 1, **after** | **40** | **40** |
| last row -> footer, before | 325 | 45 |
| last row -> footer, after | 305 | 25 |
| hero top shift | +305 | +25 |
| row 1 top shift | +20 | +20 |

The hero-to-row-1 gap is now **constant at 40 regardless of row count**, which is the whole point. Previously it was whatever the rows zone happened to leave over: 0 at 7 rows / 1350, 45 at 7 rows / 1440, 325 at 3 rows / 1440.

7 rows shifts down 20-25px and is otherwise unaffected — nothing clips, nothing collides.

### PR #37 is superseded, not contradicted

PR #37 (`bdb7da2`) added exactly one line — `justifyContent: 'center'` on the rows zone — under the subject *"TopNLayout small-N row centring"*. It was solving **this same problem** at 1350, for the Top-2 case: without it, a short row list top-aligned inside a tall zone and looked dropped.

That was the right fix for the tools available then, but it could only centre the rows *within their own zone*, which is precisely what stranded the hero. Grouping hero and rows addresses the same complaint one level up, so the rows-zone centring is now redundant: with the rows box content-sized, there is no leftover space inside it to centre against. It has been removed as part of this change.

**This supersedes #37, it does not conflict with it.** Anyone reading #37's commit and wondering where its line went should find the answer here.

### Featured-1 deliberately untouched

`Featured1Layout` was inspected and **left alone**, and the reason matters for anyone tempted to "finish the job".

It does **not** have the hero/body separation this entry fixes. Its body carries `paddingTop: 100` and **no `justifyContent`**, so it defaults to `flex-start`: content begins immediately below the hero and flows downward as one continuous run — badge, icons, name, neighbourhood, tagline, address. There is no interior gap to collapse, because there are not two separately-positioned halves.

What featured-1 *does* have is **trailing slack** below the last line, which #25 widened by 90px. That is a different question with a different answer — bottom-weighted whitespace under a top-anchored block, not a stranded element — and it was out of scope here. Recorded so the distinction is not lost.

Verified: `best-bakery` renders **byte-identical** before and after this change.

### Layout is now row-count agnostic

This pairs with #25. Together the two entries make the Top-N card independent of both variables that were previously baked in:

- **#25** made it **height**-agnostic — `rowsH` derives from `card.height`, so the zones always sum correctly at any canvas height.
- **#26** makes it **row-count**-agnostic — the hero-to-rows relationship is fixed, so 2 rows and 7 rows produce the same internal composition with different outer margins.

Neither entry attempts to make the card *look* equally full at every row count. A 3-row card still carries ~305px of margin above and below. That is honest — the list is short — and it is now expressed as symmetric outer whitespace rather than as a hole in the middle of the layout.

### Verification

Byte-identity deliberately does **not** hold for Top-N here — this is an intentional visual change, so it was proven by eye and by measurement instead.

| Check | Result |
|---|---|
| `best-wings` (3 rows) | changed as intended; hero now sits directly above row 1 |
| `best-burger` (7 rows) | shifted 20-25px, no clipping or collision |
| `best-bakery` (featured-1) | **byte-identical**, confirming featured-1 untouched |
| `npm run typecheck` | exits 0 |

### Trade-off accepted

`HERO_ROWS_GAP` is a hand-picked constant (40) rather than a derived value. It sits inside the range the old accidental gap spanned (0 to 45 at 7 rows) so 7-row cards barely move, but it is a design choice, not arithmetic. If the hero block is ever resized, revisit it.
