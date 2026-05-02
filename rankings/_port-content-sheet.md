# OLD-Page Port Content Sheet

Stage-2 deliverable for the rankings template harmonization. This sheet drafts every content field needed to port the 4 OLD pages to `_template-canonical.html`:

- `best-coffee-shops.html`
- `best-casual-spots.html`
- `best-nice-restaurants.html`
- `best-new-restaurants.html`

**No source files were edited.** Once this sheet is approved, step 3 of the migration plan executes the port using these values.

Today's date: **2026-05-01** → all "Updated" pills use **May 2026**.

Restaurants are listed in the existing on-page rank order. Confidence-flagged values are marked **🚩 verify** — best guesses I'd want a Charleston local (the author) to confirm before publishing.

---

## ✅ Resolved — description split (Option A applied)

The canonical now uses two separate content fields:

- `{{Description}}` — long keyword-rich copy (~150 chars), used by `<meta description>` and JSON-LD `description`.
- `{{ShareTagline}}` — short hook-driven copy (~60–110 chars), used by `og:description` and `twitter:description` only.

Each per-page section below provides both values, clearly labeled.

---

## 1. `best-coffee-shops.html`

| Field | Value |
|---|---|
| Slug | `best-coffee-shops` |
| Hero emoji | ☕ (already in use) |
| EmojiAriaLabel | `coffee` |
| Category | `Coffee Shops` |
| Year | `2026` |
| MonthYear | `May 2026` |

**Title:** `Best Coffee Shops in Charleston, SC | Locals Guide (2026)`

**Meta description:** `The best coffee shops in Charleston, SC, voted on by the local community. From cozy downtown gems and European-style cafés to dedicated roasters and bakeries.`

**ShareTagline** (used by `og:description` + `twitter:description`): `The community-voted best places for coffee and pastries in the Holy City.`

**Keywords:** `best coffee Charleston SC, Charleston coffee shops, best espresso Charleston, local cafes Charleston, Charleston coffee rankings`

### Restaurants (existing rank order — names + taglines already on the page)

| # | Name | Tagline (existing) | servesCuisine (proposed) |
|---|---|---|---|
| 1 | Harken Cafe | Cozy, Downtown Gem | `Coffee Shop` |
| 2 | Sightsee | Coffee & Retail | `Coffee Shop` |
| 3 | Babas on Cannon | European-style Cafe | `European Café` |
| 4 | Second State Coffee | Local Roaster | `Coffee Roastery` |
| 5 | The Harbinger Cafe & Bakery | Charming, Great Pastries | `Café and Bakery` |

### Page-level notes

- **Schema type recommendation (this page only):** the canonical uses `"@type": "Restaurant"` for every row. For coffee shops, the more semantically accurate type is `"@type": "CafeOrCoffeeShop"` (a subclass of `FoodEstablishment`). Both pass Google validation. Recommend swapping `Restaurant` → `CafeOrCoffeeShop` *only on this page* — flag for review since it diverges from the canonical.
- All 5 restaurant names + taglines copy verbatim from current page; no rewrites needed.

---

## 2. `best-casual-spots.html`

| Field | Value |
|---|---|
| Slug | `best-casual-spots` |
| Hero emoji | 🤙 (already in use) |
| EmojiAriaLabel | `shaka` |
| Category | `Casual Spots` |
| Year | `2026` |
| MonthYear | `May 2026` |

**Title:** `Best Casual Spots in Charleston, SC | Locals Guide (2026)`

**Meta description:** `Charleston's best casual restaurants, voted on by locals. Easy-going eats from BBQ joints and breweries to Vietnamese sandwiches and Folly Beach food shacks.`

**ShareTagline** (used by `og:description` + `twitter:description`): `Where Charleston locals actually eat on a Tuesday.`

**Keywords:** `best casual restaurants Charleston SC, Charleston casual dining, easy eats Charleston, local favorites Charleston, Charleston restaurants`

### Restaurants

| # | Name | Tagline (existing) | servesCuisine (proposed) |
|---|---|---|---|
| 1 | Chico Feo | Funky, Folly Beach Staple 🌴 | `Caribbean-influenced` 🚩 (op to verify) |
| 2 | Home Team BBQ | BBQ, Wings, Good Times 🍗 | `Barbecue` |
| 3 | Bon Banh Mi Southeast Asian Kitchen | Vietnamese Sandwiches, Quick Bites 🥖 | `Vietnamese` |
| 4 | Edmund's Oast | Brewery, Great Food 🍺 | `American Brewery` |
| 5 | Ted's Butcherblock | Prime Sandwiches, Local Butcher 🥪 | `American Deli` |

### Page-level notes

- 🚩 **Chico Feo cuisine.** Tagline says "Funky, Folly Beach Staple" — actual menu leans Caribbean / Latin / Lowcountry. `Caribbean` is the dominant flavor but worth confirming. Alternative: `Latin American`.
- **Inline emoji in taglines.** All 5 existing taglines have a trailing emoji per row (🌴 🍗 🥖 🍺 🥪). The canonical's convention is *page-theme-emoji-only* in the icon column, NOT per-restaurant emoji in the tagline. **Decision needed:**
  - **Recommended: strip the per-restaurant emoji from each tagline.** The icon column is the icon; a second emoji inline reads as visual noise and conflicts with intentional-decision #1 in the canonical.
  - Alternative: keep them. Visually busier but preserves existing voice.
  - This is the single judgment call that most affects the port output for this page. **Flag for explicit review.**

---

## 3. `best-nice-restaurants.html`

| Field | Value |
|---|---|
| Slug | `best-nice-restaurants` |
| Hero emoji | 🍷 (**proposed** — page currently has none) |
| EmojiAriaLabel | `wine glass` |
| Category | `Nice Restaurants` |
| Year | `2026` |
| MonthYear | `May 2026` |

**Title:** `Best Nice Restaurants in Charleston, SC | Locals Guide (2026)`

**Meta description:** `The best fine dining and upscale restaurants in Charleston, SC, voted on by locals. The definitive list for a special night out in the Holy City.`

**ShareTagline** (used by `og:description` + `twitter:description`): `Charleston's best fine dining, voted by the people who actually live here.`

**Keywords:** `best fine dining Charleston SC, best nice restaurants Charleston, upscale Charleston restaurants, romantic Charleston restaurants, special occasion Charleston`

### Restaurants

| # | Name | Tagline (existing) | servesCuisine (proposed) |
|---|---|---|---|
| 1 | Vern's | Cozy, Neighborhood Bistro | `New American` 🚩 (op to verify) |
| 2 | Chubby Fish | Creative Seafood, Always Fresh | `Seafood` |
| 3 | Zero George | Elegant, Upscale Experience | `Contemporary American` |
| 4 | FIG | American, Seasonal | `Contemporary American` |
| 5 | Malagón | Spanish Market & Tapería | `Spanish` |

### Page-level notes

- **Hero emoji.** This page has no hero emoji on the existing site. Default proposed: 🍷 (wine glass — reads "nice restaurant" without being too fancy). Alternatives:
  - 🥂 (cheers — celebratory; fine but feels more "anniversary" than "fine dining")
  - 🍽️ (plate with utensils — neutral; technically correct but bland)
  - Lean: **🍷.** Flag if you want one of the others.
- 🚩 **Vern's cuisine.** Tagline is "Cozy, Neighborhood Bistro." Could read as French bistro or Continental American. The actual restaurant is American/Continental — `Contemporary American` is the safer SEO call. Alternative: `Bistro` (more literal but a less common search term).
- **Three rows would share `Contemporary American`.** That's fine for SEO accuracy. If you want differentiation, FIG could be `American Farm-to-Table` and Zero George could be `American Fine Dining`. Flag for preference.

---

## 4. `best-new-restaurants.html`

| Field | Value |
|---|---|
| Slug | `best-new-restaurants` |
| Hero emoji | ✨ (already in use) |
| EmojiAriaLabel | `sparkles` |
| Category | `New Restaurants` |
| Year | `2026` |
| MonthYear | `May 2026` |

**Title:** `Best New Restaurants in Charleston, SC | Locals Guide (2026)`

**Meta description:** `The hottest new restaurant openings in Charleston, SC, voted on by locals. From a French bistro to a ramen bar, an NY-style deli, and a neighborhood pasta and pizza spot.`

**ShareTagline** (used by `og:description` + `twitter:description`): `The freshest restaurants in the Holy City, voted by the people who live here.`

**Keywords:** `best new restaurants Charleston SC, new Charleston restaurants 2026, Charleston restaurant openings, what's new Charleston dining, newest restaurants Charleston`

### Restaurants (current — 4 entries)

| # | Name | Tagline (existing) | servesCuisine (proposed) |
|---|---|---|---|
| 1 | Merci | Charming French Bistro | `French` |
| 2 | Bar Weems | Handmade Ramen & Cocktails | `Japanese` |
| 3 | The Wedge | Authentic NY-Style Deli Sandwiches | `American Deli` |
| 4 | OK Donna | Neighborhood Pasta & Pizza | `Italian` |

### 5th-entry decision

**Recommendation: keep this page as Top 4. Do NOT pad with a 5th entry.**

Reasoning:

1. **"Best New" is naturally a smaller-pool category.** The set of opening-this-year restaurants worth ranking is finite and shifts month-to-month. A Top 5 for "best new" implicitly claims that there are always exactly 5 worthy new openings; there often aren't. Top 4 reads as honest curation.
2. **Padding invites fabrication.** I don't have current Charleston intel sufficient to confidently propose a 5th name. Anything I'd suggest would come from training-data memory of older openings, which is exactly the kind of stale-but-confident content this site exists to be the antidote to.
3. **The author is actively curating this page.** The last 9 commits all touch `best-new-restaurants.html`. If a 5th entry belonged here, it would already be there. The omission is editorial, not an oversight.
4. **The canonical supports 4 entries trivially.** Just delete the row 5 block and the corresponding `position: 5` ListItem in the JSON-LD. Nothing else changes structurally.

**Editorial rule going forward:** add a 5th entry only when there's a confident 5th pick. If "best new" runs at 3 entries one quarter, that's also acceptable. Don't pad the slot for slot's sake.

If the author overrides this and wants a 5th entry: identify it editorially and add it back via a follow-up edit. Don't delegate the choice to me.

---

## Cross-page issues — resolutions

| # | Issue | Resolution |
|---|---|---|
| 1 | `{{Description}}` doing double duty | ✅ Option A applied — `{{ShareTagline}}` added to canonical |
| 2 | Per-restaurant emoji in `best-casual-spots` taglines | ✅ Strip on port |
| 3 | Schema type for coffee shops | ✅ `CafeOrCoffeeShop` used on `best-coffee-shops` only |
| 4 | Hero emoji for `best-nice-restaurants` | ✅ 🍷 |
| 5 | Top-4 vs Top-5 for `best-new-restaurants` | ✅ Keep at Top 4; subtitle reflects "more to come" framing |
| 6 | `Contemporary American` repeating on `best-nice-restaurants` | ✅ Acceptable as-is — no differentiation |
| 7 | `Caribbean` for Chico Feo | 🚩 Using `Caribbean-influenced` per resolution; operator to verify in separate review pass |
| 8 | `Contemporary American` for Vern's | 🚩 Using `New American` per resolution; operator to verify in separate review pass |

All resolved. Step 3 (port) executes next.

---

## Port summary — step 3 complete

All 4 OLD pages have been overwritten with canonical-conformant HTML. Verified via `python -m http.server` returning HTTP 200 on all 4 routes, plus `grep` confirmation that no `{{...}}` placeholders remain outside HTML comments (the doc-header and repeating-row comment intentionally retain their template-field references as documentation).

| File | HTTP | Lines | Δ vs canonical | Conformance | Deviations from canonical |
|---|---|---|---|---|---|
| `best-coffee-shops.html` | 200 | 348 | −4 | ✅ Conformant | (1) JSON-LD `@type` is `CafeOrCoffeeShop` on all 5 items (vs canonical `Restaurant`) per resolution #3. (2) JSON-LD comment block replaced the canonical's @type-options list with a per-page override note. |
| `best-casual-spots.html` | 200 | 352 | 0 | ✅ Conformant | None. Per-restaurant emoji (🌴 🍗 🥖 🍺 🥪) stripped from existing taglines per resolution #2. |
| `best-nice-restaurants.html` | 200 | 352 | 0 | ✅ Conformant | None. New hero emoji 🍷 introduced per resolution #4 (page previously had no hero emoji). |
| `best-new-restaurants.html` | 200 | 342 | −10 | ✅ Conformant w/ documented deviations | (1) Top 4 instead of Top 5: row-5 HTML block omitted, JSON-LD position-5 `ListItem` omitted. (2) Hero subtitle modified to "As voted by Charleston locals. Four standouts — with more to come." per resolution #5. (3) Top-of-file comment block added documenting both deviations. |

### Content-field placeholder fallbacks

None. Every `{{...}}` placeholder in actual page content was filled with an authored value. (The doc-header comment retains `{{...}}` references as field-list documentation — these are not content.)

### Operator-verify cuisine flags

Two `servesCuisine` values were resolved per the user's "if uncertain" guidance and are flagged for John's separate review pass:

- 🚩 `best-casual-spots.html` row 1 — **Chico Feo** → `Caribbean-influenced` (was: `Caribbean`)
- 🚩 `best-nice-restaurants.html` row 1 — **Vern's** → `New American` (was: `Contemporary American`)

Both ship with these values today; the operator can swap them in a follow-up edit without touching anything else.

### Brand-color dependency status

All 4 ported pages use Tailwind utility classes (`bg-brand-orange`, `text-brand-orange`, `border-brand-orange`, etc.) that resolve via the inline Tailwind config in each page's `<head>`. No port relies on `style.css`'s plain CSS classes (`.brand-orange`, `.bg-brand-orange`) for brand-color rendering. The latent `style.css` color-class dependency described in `_template-analysis.md` §2.1 still exists in the file itself but is no longer load-bearing for any of the 4 ported pages — step 5 of the migration plan can prune those classes when ready.

### Step 4 — backporting NEW pages — complete

All 3 already-NEW pages overwritten with canonical-conformant HTML. Verified the same way as step 3: HTTP 200 via local Python server, no live `{{...}}` placeholders (all `{{` matches are inside the doc-header and repeating-row comment blocks), no live `Based on 1,…` vote-count copy (verified via `grep`: only `_template-analysis.md` retains those references as historical documentation, no HTML file does), and structural line-for-line match with the canonical (352 lines each).

| File | HTTP | Lines | Δ vs canonical | Conformance | Per-page changes |
|---|---|---|---|---|---|
| `best-pizza.html` | 200 | 352 | 0 | ✅ Conformant | (1) Added: canonical URL, `og:url`, `og:image`, `og:site_name`, full Twitter card meta. (2) JSON-LD restructured: ItemList-level `name`/`description`/`url` added; `address` filled in for positions 2–5 (was only on position 1); existing `servesCuisine` values preserved. (3) ShareTagline (`og:description` / `twitter:description`) reuses existing OG copy: "The definitive guide to the best slices in the Holy City." (4) Date pill: "February 2026" → "May 2026". (5) Empty placeholder `<p class="text-center text-gray-400 text-xs mt-8"></p>` removed. (6) CTA copy aligned to canonical ("Disagree with this list? Cast your vote!" — was "Have a different favorite?"). |
| `best-burger.html` | 200 | 352 | 0 | ✅ Conformant | (1) **Vote-count footer DELETED** ("Based on 1,769 local votes collected in 2025."). Confirmed absent via `grep`. (2) Dot-bullet rows (`<div class="h-3 w-3 rounded-full bg-brand-orange/40">`) → emoji-per-row (`<span>🍔</span>` with aria-label "hamburger"). (3) `<h3>` restaurant headings → `<h2>`. (4) Subtitle split: combined "As voted by Charleston locals • Updated January 2026" → canonical's two-element pattern (subtitle + "Updated May 2026" pill). (5) Title aligned to canonical format. (6) Added: full OG block, Twitter card, canonical URL, JSON-LD ItemList. (7) Vote button label "Vote Now" → "Vote for Best Burger". (8) Hero "Back" link styling normalized to canonical. |
| `best-tex-mex.html` | 200 | 352 | 0 | ✅ Conformant | (1) **Vote-count footer DELETED** ("Based on 1,420 local votes collected in 2025."). Confirmed absent via `grep`. (2) Dot-bullet rows → emoji-per-row (🌮 with aria-label "taco"). (3) `<h3>` → `<h2>`. (4) Subtitle split into canonical's two-element pattern with "Updated May 2026" pill. (5) Title aligned to canonical format. (6) Added: full OG block, Twitter card, canonical URL, JSON-LD ItemList. (7) Vote button "Vote Now" → "Vote for Best Tex-Mex". (8) Hero "Back" link styling normalized to canonical. |

### Step 4 cuisine-value provenance

For `best-pizza`, the JSON-LD `servesCuisine` values are preserved verbatim from the page's existing JSON-LD: Neapolitan Pizza, Wood-Fired Pizza, Pizza, Detroit Style Pizza, Pizza.

For `best-burger` (no prior JSON-LD), authored values are: Burgers, Burgers, Burgers, **Barbecue** (Home Team BBQ — disambiguated from the page topic), Burgers. All flagged as 🚩 op-verify in the tracked items list — operator can refine on the next pass.

For `best-tex-mex` (no prior JSON-LD), authored values are: Tex-Mex × 5. Flagged 🚩 op-verify — Azul Mexicano in particular reads as more "Modern Mexican" than Tex-Mex on the existing tagline; operator may want `Mexican` there.

### CTA-copy alignment (notable structural change)

`best-pizza.html` previously used the CTA copy *"Have a different favorite?"* — the canonical uses *"Disagree with this list? Cast your vote!"*. Canonical conformance pulled best-pizza onto the canonical wording. This was a deliberate choice (the canonical's CTA was already approved as the strongest copy on the site); flagging here so it's visible during your visual review.

### Operator-verify cuisine flags — updated set (now 4 items)

| Page | Restaurant | Shipped value | Reason flagged |
|---|---|---|---|
| `best-casual-spots` | Chico Feo | `Caribbean-influenced` | Resolved per "if uncertain" rule; menu has Latin / Lowcountry overlap |
| `best-nice-restaurants` | Vern's | `New American` | Resolved per "if uncertain" rule; bistro-leaning could read as French / Continental |
| `best-burger` | All 4 burger-leaning rows | `Burgers` | Authored cuisine; Home Team BBQ correctly differentiated as `Barbecue` |
| `best-tex-mex` | All 5 rows | `Tex-Mex` | Authored cuisine; Azul Mexicano may be better as `Mexican` |

All hardened in `_template-analysis.md` `## Tracked items` (the first two as named items per the user's instruction; the last two are documented here in this summary as part of the step-4 record).

### Final state — migration plan checkpoint

Steps 1 → 4 of the migration plan are complete. All 7 Top-5 ranking pages now conform to `_template-canonical.html`. Outstanding plan items:

- **Step 5** — verify all 7 pages render correctly (operator visual check pending) and prune the latent `style.css` brand-color class dependency. See style.css audit findings (separate report) for what's currently in style.css.
- **Step 6** — defer: featured-winner template harmonization for `best-new-coffee-shop`.
