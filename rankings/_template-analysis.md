# Ranking Pages Template Analysis

A read-and-compare pass over all 8 files in `rankings/` to surface the structural delta between the two design generations and propose a single canonical template.

No source files were modified for this analysis.

---

## 1. Page inventory at a glance

| File | Generation | Format | GA | OG | JSON-LD | Updated date | Vote count |
|---|---|---|---|---|---|---|---|
| `best-pizza.html` | NEW | Top 5 list | ✓ | partial (no `og:image`, no `og:url`-for-page) | ✓ `ItemList` | "Updated February 2026" pill | empty placeholder `<p>` |
| `best-burger.html` | NEW | Top 5 list | ✓ | ✗ | ✗ | inline " • Updated January 2026" in subtitle | "Based on 1,769 local votes collected in 2025." |
| `best-tex-mex.html` | NEW | Top 5 list | ✓ | ✗ | ✗ | inline " • Updated January 2026" in subtitle | "Based on 1,420 local votes collected in 2025." |
| `best-new-coffee-shop.html` | NEW | **Single winner** (different layout) | ✓ | ✗ | ✗ | none ("The freshest brew in town." subtitle only) | n/a |
| `best-new-restaurants.html` | TRANSITIONAL | Top 4 list (only 4 entries) | ✓ | ✗ | ✗ | "January 2026" small uppercase line | none |
| `best-coffee-shops.html` | OLD | Top 5, numeric ranks | ✗ | ✗ | ✗ | "Last updated: September 1, 2025" | none |
| `best-casual-spots.html` | OLD | Top 5, numeric ranks | ✗ | ✗ | ✗ | "Last updated: September 1, 2025" | none |
| `best-nice-restaurants.html` | OLD | Top 5, numeric ranks | ✗ | ✗ | ✗ | "Last updated: September 1, 2025" | none |

A few important observations from this table alone:

- **Three pages have no Google Analytics at all** (`best-coffee-shops`, `best-casual-spots`, `best-nice-restaurants`). Any traffic to those pages is invisible.
- **Only one page has structured data** (`best-pizza`). Lists of local restaurants are the textbook use case for `ItemList` + `Restaurant` schema — this is the single highest-value SEO miss.
- **Updated dates use four different formats** across the 8 pages, and three pages are 8+ months stale.
- **Vote counts are inconsistent and not derived** — only 2 pages have them, and the two numbers (1,769 vs 1,420) appear to be hardcoded marketing copy.

---

## 2. Structural differences — NEW vs OLD

### 2.1 `<head>` scaffolding

NEW pages (`best-pizza`, `best-burger`, `best-tex-mex`, `best-new-coffee-shop`):

- Inline GA snippet
- `<link rel="preconnect">` for `fonts.googleapis.com` + `fonts.gstatic.com`
- Google Fonts stylesheet load (DM Sans + Poppins)
- Tailwind CDN script **plus** an inline `tailwind.config` block defining the `brand` color palette and font families
- Body classes: `antialiased bg-brand-cream text-brand-dark min-h-screen flex flex-col`

OLD pages (`best-coffee-shops`, `best-casual-spots`, `best-nice-restaurants`):

- No GA
- No font preconnect or `<link>` to Google Fonts (relies on `style.css`'s `@import url()` — slower)
- Tailwind CDN script with **no** inline config
- Body class: just `antialiased`

The OLD pages render OK only because the `bg-brand-orange`/`brand-orange`/`border-brand-orange` classes happen to also exist as plain CSS classes in `style.css`. If `style.css` were ever cleaned up, those pages would visually break — silent fragility.

`best-new-restaurants` sits in the middle: it has GA, but no font preconnect and no inline Tailwind config. Body class is just `antialiased`.

### 2.2 Hero block

NEW order: link → h1 → subtitle → optional date pill.

```
[‹ Back to All Rankings]
Best <orange>{Category}</orange> {Emoji}      ← text-4xl sm:text-6xl font-extrabold
"As voted by Charleston locals"
[Updated {Month Year}]                        ← optional pill or inline
```

OLD order: h1 → date → link.

```
Best {Category} {Emoji}                       ← text-4xl sm:text-5xl font-bold (no orange highlight)
"Last updated: September 1, 2025"
‹ Back to All Rankings                        ← small inline link
```

The orange-highlight on the category word (NEW) is the most important visual cue — it's the brand stamp on every page and is missing from all OLD pages.

### 2.3 List card

NEW:

- Container: `bg-white rounded-[2rem] shadow-xl border border-brand-orange/10 overflow-hidden relative`
- 2px orange accent bar at top: `<div class="h-2 w-full bg-brand-orange"></div>`
- Inner padding: `p-2 sm:p-4`
- Row separators: `<div class="divide-y divide-gray-100">` wrapping each row
- Row class: `group p-5 sm:p-6 hover:bg-orange-50/40 transition-colors rounded-xl flex items-start gap-4 sm:items-center`
- Restaurant name: `<h2 class="font-poppins font-bold text-xl sm:text-2xl text-brand-dark mb-1 leading-snug">`
- Tagline: `<p class="text-brand-gray font-medium text-sm sm:text-base">`

OLD:

- Container: `bg-white p-6 sm:p-8 rounded-xl shadow-lg` (no accent bar, smaller corner radius, no border)
- Row separators: explicit `<hr>` between rows
- Row class: `flex items-center gap-4` (no hover state)
- Restaurant name: `<h3 class="font-bold text-lg text-gray-800">` (less prominent — tagline is `text-sm` rather than `text-base`)
- **Has a numeric rank column** (`<div class="text-4xl font-bold brand-orange opacity-70 w-10 text-center">1</div>`) — this is the most visible visual difference

### 2.4 Row icon/marker style — two NEW variants

The newer generation has not actually settled on one row treatment:

- **Emoji-per-row** (`best-pizza`): every row has a small `<span class="text-2xl">🍕</span>` matching the page theme. Reads warmer, more on-brand, more visually distinctive.
- **Orange-dot bullet** (`best-burger`, `best-tex-mex`): each row has `<div class="h-3 w-3 rounded-full bg-brand-orange/40"></div>`. Reads cleaner, more institutional, less playful.

**Recommendation: standardize on emoji-per-row.** It's the harder pattern to fake (the dot bullets are nearly invisible at small sizes), it carries the page theme into the rhythm of the list, and it gives every page a unique visual signature. The dot variant doesn't add information.

### 2.5 Bottom CTA

NEW:

- Framing block: `bg-orange-50 p-6 sm:p-8 text-center border-t border-brand-orange/10`
- Copy line above the button: "Have a different favorite?" (best-pizza) / "Disagree with this list? Cast your vote!" (best-burger, best-tex-mex)
- Button: pill-shaped (`rounded-full`), `font-poppins font-bold text-lg py-3 px-8` (best-burger/tex-mex) or `py-4 px-10` (best-pizza), with arrow icon, hover lift, `active:scale-95`
- Button label varies: "Vote Now" / "Vote for Best Pizza"

OLD:

- No framing block — button just sits inside the white card
- No copy line above
- Button: full-width block (`block text-center w-full`), `rounded-lg`, label "Vote Now"

The "Disagree with this list?" copy is the strongest CTA on the site — it triggers actual response. Default the canonical to that wording.

### 2.6 Restaurant heading semantics

This is a small but real bug. NEW pages mix `<h2>` (best-pizza) and `<h3>` (best-burger, best-tex-mex) for restaurant names. OLD pages use `<h3>`. None of the pages use a consistent semantic h-level. The canonical should pin restaurant names to `<h2>` (page already has one h1).

---

## 3. Per-restaurant content fields

### What the canonical (NEW) template requires per row

| Field | Required? | Source on existing OLD pages? |
|---|---|---|
| Restaurant name | yes | ✓ already present |
| Tagline (≈2–6 words) | yes | ✓ already present |
| Page-theme emoji | yes (if emoji-per-row variant chosen) | n/a — comes from the page, not the row |
| `servesCuisine` for JSON-LD | yes | ✗ needs to be authored — the existing taglines are descriptive ("Cozy, Neighborhood Bistro") not cuisine ("Contemporary American Bistro") |

### What the canonical (NEW) template requires per page

| Field | Required? | Source on existing OLD pages? |
|---|---|---|
| Page slug (for canonical/og:url) | yes | ✓ filename |
| Hero emoji | yes | partial — `best-coffee-shops` has ☕, `best-casual-spots` has 🤙, `best-nice-restaurants` has none and needs one (e.g. 🍷 or 🥂) |
| Category title | yes | ✓ |
| `<title>` and `<meta description>` | yes | ✓ |
| `<meta keywords>` | optional | ✗ — not yet written for OLD pages |
| Canonical URL | yes | ✗ none |
| OG title / description / image / url | yes | ✗ — would need OG description + an OG image asset (none currently exists for any page) |
| Twitter card meta | yes | ✗ none |
| JSON-LD `ItemList` | yes | ✗ — needs `servesCuisine` per restaurant, authored |
| "Updated [Month Year]" | yes | partial — current "September 1, 2025" dates are stale |
| Vote count footer | optional — only when an accurate number exists | n/a (currently arbitrary) |
| "Best New Restaurants" 5th entry | yes if standardizing to Top 5 | ✗ — currently 4 entries |

The actual structural lift to port an OLD page to the NEW template is small (copy/paste the canonical and fill in name + tagline). The **content** lift is non-trivial: every page needs OG description, OG image (design asset), JSON-LD cuisine values, and a fresh date.

---

## 4. `best-new-coffee-shop.html` — keep distinct, harmonize the chrome

This page is structurally different from the Top 5 pages. It's a single-winner feature page:

- Big card with one restaurant (Babas on Wentworth)
- "#1 Voted by Locals" badge
- Neighborhood label ("Harleston Village")
- Multi-paragraph editorial blurb
- Pull quote
- "The Details" sidebar with **address** and **hours**
- CTA at bottom: "Suggest a different winner" → `/suggest-category.html` (not "Vote Now")
- Container is `max-w-3xl` (everything else is `max-w-2xl`)

**Recommendation: keep this as a separate template variant.** Folding it into a Top 5 layout would lose meaningful information (address, hours, prose). There's a real product reason for the difference — "Best New {category}" type rankings often have one clear winner that warrants depth.

What *should* be unified, even though the layouts differ:

- `<head>` scaffolding (GA, fonts, Tailwind config, meta, OG, JSON-LD — using `LocalBusiness` instead of `ItemList`)
- Body classes
- Header/footer pattern
- Hero block (back link → h1 → subtitle → date pill)
- Brand colors and typography

Going forward, treat this as **two templates sharing one chrome**:

1. `_template-canonical.html` — Top 5 list (this analysis proposes it)
2. *future* `_template-featured-winner.html` — single-winner deep-dive (modeled on `best-new-coffee-shop` but with the canonical head/scaffolding pulled in). Out of scope for this round; flag for a follow-up.

---

## 5. Cross-cutting inconsistencies

| Concern | Issue |
|---|---|
| GA tracking | 3 of 8 pages have no GA snippet (`best-coffee-shops`, `best-casual-spots`, `best-nice-restaurants`) |
| OG tags | 7 of 8 pages have no OG tags; even `best-pizza` is missing `og:image` and a per-page `og:url` |
| Twitter cards | 0 of 8 |
| JSON-LD | 1 of 8 (`best-pizza` — `ItemList`) |
| Canonical URLs | 0 of 8 |
| `<title>` pattern | `best-pizza` uses `"Best Pizza in Charleston, SC \| Locals Guide (2026)"`. Others use varying shorter forms. No fixed pattern. |
| Updated-date format | 4 distinct formats: pill (`best-pizza`), inline-after-bullet (`best-burger`, `best-tex-mex`), small uppercase line (`best-new-restaurants`), prose "Last updated: …" (3 OLD pages) |
| Date staleness | 3 pages still say "Last updated: September 1, 2025" — 8+ months stale |
| Vote count | Only 2 pages show one. Numbers (1,769 / 1,420) are hardcoded copy, not derived. Implies precision the data doesn't have. |
| Brand colors | NEW pages define `brand` colors inline via Tailwind config; OLD pages don't — they accidentally work because `style.css` exposes the same names as plain CSS classes |
| Hero ordering | NEW: link → h1 → subtitle → date. OLD: h1 → date → link |
| Container width | 7 pages `max-w-2xl`; `best-new-coffee-shop` is `max-w-3xl` |
| Restaurant heading element | `best-pizza` uses `<h2>`; `best-burger`/`best-tex-mex`/OLD pages use `<h3>` — broken h-level hygiene |
| Emoji-per-row vs dot-bullet | Two coexisting NEW variants — not yet standardized |
| Tailwind CDN at runtime | All 8 pages use it. Real performance/CLS concern. Out of scope here, flag for later. |

---

## 6. Recommended canonical template

See `_template-canonical.html` in this directory for the full HTML skeleton with `<!-- REPLACE: ... -->` markers.

The canonical merges the strongest elements:

- **From `best-pizza`:** richer head scaffolding (font preconnect, inline Tailwind config, full body classes), JSON-LD `ItemList` of `Restaurant`, hero-link-above-h1 ordering, separate "Updated" pill, emoji-per-row.
- **From `best-burger`/`best-tex-mex`:** the "Disagree with this list? Cast your vote!" CTA copy — the strongest call-to-action wording on the site.
- **Newly added (none of the 8 pages have them):** canonical URL, Twitter card meta, `og:image`, per-page `og:url`, semantic `<h2>` for restaurant names, JSON-LD applied uniformly.

Each conforming page only needs to fill in roughly these 18–22 placeholders:

- Page slug (used in `og:url`, `og:image`, canonical)
- Hero emoji
- Category title (e.g. "Pizza")
- One paragraph of description copy (re-used in `<title>`, `<meta description>`, `og:description`, `twitter:description`, JSON-LD `description`)
- Keyword string
- Updated date string (e.g. "February 2026")
- 5 × `(name, tagline, servesCuisine-for-JSON-LD)`
- (optional) vote count + year

That's the whole content surface to maintain per page.

### Migration plan (revised — current step in **bold**)

1. Approve `_template-canonical.html` as the spec. **Done** ✅. Three required edits applied: vote-count footer removed; intentional-decisions section added to top header (emoji-per-row convention, relative favicon vs absolute OG image, vote counts deliberately not a placeholder field); aggregateRating documented as intentionally absent in JSON-LD.
2. **[CURRENT STEP] Author missing per-page content fields for the 4 OLD pages** — OG description, JSON-LD `servesCuisine` values, fresh dates, 5th-entry decision for `best-new-restaurants`. Stage in `_port-content-sheet.md` for review. **Do not start editing pages yet.**
3. Port the 4 OLD pages (`best-coffee-shops`, `best-casual-spots`, `best-nice-restaurants`, `best-new-restaurants`) to the canonical, using the approved content sheet.
4. Backport the canonical's missing meta (canonical URL, Twitter card, `og:image` URL, per-page `og:url`, JSON-LD) onto the 3 already-NEW pages (`best-pizza`, `best-burger`, `best-tex-mex`) so all 7 Top 5 pages truly match.
5. Verify every page renders correctly **and break the latent `style.css` color-class dependency**. Confirm no page relies on `style.css` exposing `bg-brand-orange` / `brand-orange` / `border-brand-orange` as plain CSS classes — the inline Tailwind config in the canonical should be the only source of brand-color tokens. Then prune those plain CSS classes out of `style.css`.
6. Featured-winner template harmonization (`best-new-coffee-shop`) — flag, defer to a later workstream.

### Out of scope for this migration (deferred — separate workstreams)

- **OG image generation.** Moved out of this migration entirely. The canonical references `og-{{slug}}.png` URLs that don't yet exist; missing image previews are acceptable until the image workstream completes (most platforms gracefully omit the preview rather than failing the share).
- Replacing Tailwind CDN with a built/precompiled stylesheet
- Replacing client-side `fetch()` of `header.html`/`footer.html` with build-time inlining or SSI
- Adding `sitemap.xml` and `robots.txt`
- A featured-winner template harmonization pass (`best-new-coffee-shop`)

---

## Tracked items

Open follow-ups that don't block the migration but should be revisited.

- **`best-casual-spots` / Chico Feo cuisine.** Shipped with `servesCuisine: "Caribbean-influenced"` (resolved from `"Caribbean"` per the "if uncertain" rule). Operator (John) to verify and finalize. The actual menu also has Latin and Lowcountry influences; alternatives include `"Latin American"` or `"Caribbean"`. Single-line JSON-LD edit when finalized.
- **`best-nice-restaurants` / Vern's cuisine.** Shipped with `servesCuisine: "New American"` (resolved from `"Contemporary American"` per the "if uncertain" rule). Operator (John) to verify and finalize. Bistro-leaning — could read as French bistro, Continental, or American depending on framing. Single-line JSON-LD edit when finalized.
- **`best-new-restaurants` is currently Top 4.** Promote to Top 5 on the next refresh when a real 5th candidate exists. Do NOT fabricate. The page subtitle has been updated to "Four standouts — with more to come" so the format is intentional, not an awkward gap. Revisit at the next ranking refresh.

---

## Tracked workstream: Upgrade 5 top-level pages to canonical chrome

Migrated to `_strategy/TRACKED.md` as the canonical home for tracked workstreams — see "Upgrade 5 top-level pages to canonical chrome" there for current state, scope, and order of operations. This section is preserved as a pointer; the original analysis it captured has been folded into `_strategy/TRACKED.md` and `_strategy/DECISIONS.md` #11.
