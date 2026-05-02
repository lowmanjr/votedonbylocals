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
