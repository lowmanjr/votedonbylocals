# Best Wings launch - analysis working file

Working file for the `best-wings` Top-5 ranking launch. Author: Claude session
2026-08-24, branch `best-wings-launch`. Analysis only - nothing in this file has
been applied to the tree.

**Location rationale:** `_strategy/WORKFLOW.md` specifies this. Verbatim: *"Files
prefixed with underscore ... are intermediate artifacts created during a
workstream. They live in the directory of the work they support - not in
`_strategy/`."* A ranking-page launch is owned by `rankings/`, matching the
existing precedents `rankings/_template-analysis.md`,
`rankings/_port-content-sheet.md`, `rankings/_step-3-design.md`,
`rankings/_detail-page-design.md`. So the location was **specified, not chosen**.

The one in-tree counter-example, `_strategy/_workstream-f-design.md`, is
self-documenting about why it is an exception - its own line 3 reads *"Will live
at the repo root or under `_strategy/` per your call (it spans 5 files plus
style.css; no single subdirectory naturally owns it)."* That reasoning does not
apply here.

Working files are **tracked, not scratch** - `git ls-files` returns all six
underscore working files. `.gitignore` has no underscore rule. Bonus: files under
`rankings/_*` are excluded from `sitemap.xml` (generator skips `_`-prefixed) and
from crawl (`robots.txt` has `Disallow: /rankings/_`).

---

## 0. State at time of writing

```
branch:   best-wings-launch  (created from main @ 5d45683, checkout confirmed)
status:   clean
chrome:   python scripts/inline_chrome.py --check  ->  "[OK] 54 files in sync", exit 0
tooling:  Python 3.11.3, playwright importable, node v22.13.0, npm 10.9.2
```

---

## 1. Roster resolution against `data/restaurants.json`

Matched on normalized slug and normalized name (lowercase, NFD-strip-diacritics,
punctuation to space, collapse whitespace). Near misses reported, not guessed.

| # | Roster entry | Result | Slug |
|---|---|---|---|
| 1 | Home Team BBQ | **EXISTS** - exact name match | `home-team-bbq` |
| 2 | Tru Blues House of Wings (Mount Pleasant) | **ABSENT** - no exact match, zero token-overlap near misses | proposed `tru-blues-house-of-wings` |
| 3 | Moe's Crosstown Tavern | **EXISTS** - exact name match | `moes-crosstown-tavern` |
| 4 | Nigel's Good Food | **ABSENT** - no exact match. Token-overlap hits are all apostrophe-name artifacts (`verns`, `santis`, `teds-butcherblock`, etc.) matching only on the tokenized `s`; none is a real near miss | proposed `nigels-good-food` |
| 5 | Dashi | **ABSENT** - no exact match, zero token-overlap near misses | proposed `dashi` |

Proposed slugs follow the in-tree convention, verified against all 36 entries:
apostrophes **dropped, not hyphenated** (`moes-crosstown-tavern`,
`little-jacks-tavern`, `heavys-barburger`, `dallesandros-pizza`, `verns`,
`santis`); accents stripped (`senor-tequilas` for "Senor Tequila's", with acute
e); `&` dropped entirely (`the-harbinger-cafe-bakery`); articles and prepositions
kept (`babas-on-cannon`, `the-wedge`, `the-harbinger-cafe-bakery`).

### 1a. Existing entries - current state

**`home-team-bbq`**

- `appearsOn`: `/rankings/best-burger.html`, `/rankings/best-casual-spots.html` (2 entries)
- `locations[]`: **YES**, 3 secondaries - Downtown, Sullivan's Island, Mt Pleasant
- `schemaType`: `Restaurant`; `cuisine`: `Barbecue`; `neighborhood`: `West Ashley`
- Fields currently null: `geoLat`, `geoLng`, `imageURL`, `editorialBody`, `areaServed`
- Field absent entirely (not null): `displayCuisine`
- Nulls inside `locations[]`: Downtown `websiteURL`; Sullivan's Island
  `websiteURL`; all three secondaries `geoLat` + `geoLng`
- Already wings-aware in its own data: `tagline` is literally `"BBQ, Wings, Good
  Times"`, `description` says *"famous for its smoked meats, wings, and
  burgers"*, `keywords` contains `"Charleston wings"`. Adding it to a wings list
  requires **no schema edit beyond `appearsOn`**.

**`moes-crosstown-tavern`**

- `appearsOn`: `/rankings/best-burger.html` (1 entry)
- `locations[]`: **NO** - single-location
- `schemaType`: `Restaurant`; `cuisine`: `American`; `neighborhood`: `Hampton Park`
- Fields currently null: `geoLat`, `geoLng`, `imageURL`, `editorialBody`, `areaServed`
- Field absent entirely (not null): `displayCuisine`
- **Editorial flag:** every prose field is burger-framed with no wings mention -
  `tagline` `"Legendary Dive Bar Burger"`, `shareTagline` *"The legendary
  dive-bar burger, voted best by Charleston locals."*, `description` *"known for
  its legendary burger"*, `keywords` `"dive bar burger Charleston"`. Its detail
  page hero will still read "Legendary Dive Bar Burger" while the page lists
  "Appears on: Best Wings in Charleston". Not a bug and not blocking - the
  per-list tagline lives on the ranking page, not in `restaurants.json` - but it
  is a visible mismatch the operator may want to resolve. **Not resolving it
  silently.** Options: leave as-is; broaden `tagline`; or file a TRACKED
  editorial item. Operator call.

### 1b. Absent entries - required-field gap table

**No values are supplied below. This step identifies gaps; it does not fill
them.** No web search was performed. Per `_strategy/HANDOFF.md` "What NOT to do":
*"Don't fabricate restaurant data, hours, OG image content, or meta
descriptions."*

REQUIRED fields per `rankings/_detail-page-template.html` docblock + the
`data/restaurants.json` `_meta.fieldPolicy` (*"Empty string ('') is NOT a valid
placeholder - null means 'absent'; '' means 'present and empty', which is a
fabrication."*).

| REQUIRED field | tru-blues-house-of-wings | nigels-good-food | dashi |
|---|---|---|---|
| `slug` | proposed above | proposed above | proposed above |
| `name` | **CONFIRM** - see note 1 | MISSING | MISSING |
| `tagline` | MISSING | MISSING | MISSING |
| `cuisine` | MISSING | MISSING | MISSING |
| `neighborhood` | MISSING | MISSING | MISSING |
| `schemaType` | MISSING - see note 2 | MISSING | MISSING |
| `monthYear` | MISSING - see s.3 | MISSING | MISSING |
| `address.streetAddress` | MISSING | MISSING | MISSING |
| `address.addressLocality` | operator gave "Mount Pleasant" - see note 3 | MISSING | MISSING |
| `address.addressRegion` | `"SC"` (default) | `"SC"` (default) | `"SC"` (default) |
| `address.postalCode` | MISSING | MISSING | MISSING |
| `address.addressCountry` | `"US"` (default) | `"US"` (default) | `"US"` (default) |
| `description` | MISSING | MISSING | MISSING |
| `shareTagline` | MISSING | MISSING | MISSING |
| `keywords` | MISSING | MISSING | MISSING |
| `appearsOn` | 1 entry, known - see s.3 | 1 entry, known | 1 entry, known |

Optional fields (`phone`, `hours`, `hoursHumanReadable`, `priceRange`,
`websiteURL`, `displayCuisine`, `areaServed`) ship as `null` where uncollected.
`geoLat` / `geoLng` / `imageURL` / `editorialBody` are `null` on all 36 existing
entries - match that.

`locations[]`: **cannot be determined from the tree for any of the three.** If
any is multi-location within greater Charleston (editorial scope per DECISIONS
#14.1), it needs a `locations[]` array per DECISIONS #17. The operator's
parenthetical "(Mount Pleasant)" on Tru Blues reads as a disambiguator, which is
weak evidence of more than one location - flagging, not concluding.

Notes:

1. **Tru Blues display name needs confirmation.** The roster line is `Tru Blues
   House of Wings (Mount Pleasant)`. Whether the `name` field is `"Tru Blues
   House of Wings"` with the parenthetical as a location hint, or whether the
   parenthetical is part of the brand, changes both `name` and `slug`. Slug is
   immutable through rebrands per template intentional decision #3, so this must
   be right at creation.
2. **`schemaType` is not automatically `Restaurant`.** Per DECISIONS #5 pick the
   most specific `FoodEstablishment` subclass. If any of these is a truck or
   pop-up, it is `FoodEstablishment` + `areaServed` + null address sub-fields per
   template intentional decision #9 (the `dough-boyz` pattern on `best-pizza`).
3. **"Mount Pleasant" vs "Mt Pleasant" is inconsistent in the tree today.**
   `restaurants.json` has `tonis-detroit-style-pizza`
   `addressLocality: "Mount Pleasant"` but `san-miguel-mexican-grill`
   `addressLocality: "Mt Pleasant"`, and both spellings propagate into their
   ranking-page ItemLists. `home-team-bbq`'s `locations[]` uses
   `label: "Mt Pleasant"` with `addressLocality: "Mount Pleasant"`.
   **Recommendation: use `"Mount Pleasant"`** (full form, matches the
   `addressLocality`-vs-`label` split Home Team already models). File the
   existing `san-miguel` divergence as a TRACKED one-off rather than fixing it in
   this PR - out of scope, and it is a live cross-linked-graph inconsistency of
   exactly the class DECISIONS #15 Q5 addressed for the rollup-vs-literal case.

---

## 2. Drafted page content - DRAFT ONLY, NOT APPLIED

### 2a. Head meta

Voice calibrated against the four existing Top-N pages (char counts measured in
the tree: titles 50-61, descriptions 113-157, og:descriptions 50-70, keywords
132-142).

```
<title>Best Wings in Charleston, SC | Locals Guide (2026)</title>            (49)

<meta name="description" content="Discover the best wings in Charleston, SC.
From dive-bar plates to dedicated wing houses, explore the top spots voted on
by the local community.">                                                   (145)

<meta name="keywords" content="best wings Charleston SC, Charleston wings
rankings, chicken wings Charleston, wing spots Charleston, local favorites
Charleston">                                                                (137)

<link rel="canonical" href="https://votedonbylocals.com/rankings/best-wings.html">

<meta property="og:title"       content="Best Wings in Charleston | Voted On By Locals">   (44)
<meta property="og:description" content="Charleston's best wings, voted by the local community."> (54)
<meta property="og:type"        content="website">
<meta property="og:url"         content="https://votedonbylocals.com/rankings/best-wings.html">
<meta property="og:image"       content="https://votedonbylocals.com/assets/images/og-best-wings.png">
<meta property="og:site_name"   content="Voted On By Locals">

<meta name="twitter:card"        content="summary_large_image">
<meta name="twitter:title"       content="Best Wings in Charleston | Voted On By Locals">
<meta name="twitter:description" content="Charleston's best wings, voted by the local community.">
<meta name="twitter:image"       content="https://votedonbylocals.com/assets/images/og-best-wings.png">
```

**Flag on `description`:** the clause "From dive-bar plates to dedicated wing
houses" leans on two things - Moe's own in-tree `description` ("Hampton Park dive
bar") and the operator-supplied name "House of Wings". It asserts nothing I could
not source. If the operator would rather assert nothing at all about the roster
until entries are populated, the neutral fallback is:

```
Discover the best wings in Charleston, SC. Explore the top wing spots across the
Lowcountry, voted on by the local community.                                (124)
```

`og:image` is an **absolute** URL while the favicon stays relative. Deliberate
asymmetry per DECISIONS #10 - do not "fix".

### 2b. Hero, subtitle, pill

```html
<!-- REPLACE: hero h1 (Category + Emoji) -->
<h1 class="text-4xl sm:text-6xl font-extrabold font-poppins text-brand-dark leading-tight">
    Best <span class="text-brand-orange">Wings</span> 🍗
</h1>

<p class="text-brand-gray mt-4 text-lg font-medium">As voted by Charleston locals</p>

<!-- REPLACE: Updated [Month Year] pill -->
<div class="inline-block bg-white px-3 py-1 rounded-full text-xs text-gray-400 border border-gray-100 mt-2 shadow-sm">
    Updated August 2026
</div>
```

**Emoji:** U+1F357 POULTRY LEG. `aria-label="poultry leg"` - matches the in-tree
aria-label convention of plain lowercase Unicode-ish names (`pizza slice`,
`hamburger`, `taco`, `coffee`, `wine glass`, `sparkles`, `shaka`, `tropical
drink`). Alternative considered: U+1F414 CHICKEN, rejected because the site's
emoji all depict the food as served, not the animal. One emoji for the whole page
and reused on every row - `_template-canonical.html` intentional decision #1
forbids per-restaurant emoji on Top-N.

**Subtitle:** no count framing. DECISIONS #20 - Top-5 is the canonical default and
its slate is full as-is; "more to come" framing is only for sub-canonical counts
(featured-1 / Top-2 / Top-4). Verified against the tree: all three Top-5 pages and
Top-7 `best-burger` use the bare `"As voted by Charleston locals"`.

**Pill month:** `Updated August 2026` (today is 2026-08-24). Note every existing
page reads "Updated May 2026", so this will be the only page with a later month.
That is correct, not drift.

### 2c. Per-row taglines

The tagline lives on the **ranking page body row**, not in `restaurants.json`.
This is deliberate so a cross-listed restaurant carries a different descriptor
per list. Verified in the tree - `home-team-bbq` is "Smoky, Underrated Gem" on
`best-burger` and "BBQ, Wings, Good Times" on `best-casual-spots`.

Voice reference measured from the tree: Title Case, 2-6 words, often two
comma-separated attributes. e.g. "Thick, Cheesy, Crispy Edges", "Brisket-Chuck
Blend, Sunchoke Relish", "Generous Pours, Reliable Slush", "Park Circle
Neighborhood Spot".

| Rank | Restaurant | Tagline |
|---|---|---|
| 1 | Home Team BBQ | **PROPOSAL, needs sign-off** - see below |
| 2 | Tru Blues House of Wings | **BLOCKED** |
| 3 | Moe's Crosstown Tavern | **PROPOSAL, needs sign-off** - see below |
| 4 | Nigel's Good Food | **BLOCKED** |
| 5 | Dashi | **BLOCKED** |

**Home Team BBQ** - candidates, each grounded only in its own in-tree data
(`cuisine: Barbecue`, `neighborhood: West Ashley`, 4 total locations, downtown
open to midnight, wings named in its own tagline/description/keywords):

- `Barbecue Joint, Wings on Every Table`
- `Smokehouse Wings, Four Locations`
- `BBQ Staple, Wings Included`

**Moe's Crosstown Tavern** - candidates, grounded in `neighborhood: Hampton
Park`, its own "dive bar" self-description, and `hours: Mo-Su 11:00-02:00`:

- `Dive Bar Wings, Open Till 2am`
- `Hampton Park Dive, Late-Night Wings`

Both sets **differ from the same restaurant's taglines on other lists**, which is
the intended behavior, and both are flagged for operator sign-off rather than
chosen. `_strategy/WORKFLOW.md` self-correction norm lists *"Editorial decisions
(cuisine values, tone, copy)"* among the things not to decide unilaterally.

**Why rows 2, 4, 5 are blocked:** there is no data anywhere in the tree for Tru
Blues House of Wings, Nigel's Good Food, or Dashi, and web search was
out-of-scope for this pass. Any tagline I wrote for them would be invented
descriptive copy about a real business - the exact thing the brand wedge exists
to oppose. Operator supplies these, or authorizes a sourcing pass, before the
execute step. Everything else on the page can be built without them.

### 2d. ItemList JSON-LD

Field order copied verbatim from `best-burger`'s block, which is the production
shape: `@context, @type, name, description, datePublished, dateModified, url,
itemListElement`. HANDOFF records that field *order* is itself a semantic surface
- mirror it, do not re-order.

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Best Wings in Charleston, SC",
  "description": "<same string as meta description>",
  "datePublished": "2026-08-24T12:00:00-04:00",
  "dateModified": "2026-08-24T12:00:00-04:00",
  "url": "https://votedonbylocals.com/rankings/best-wings.html",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "item": {
        "@type": "Restaurant", "name": "Home Team BBQ",
        "url": "https://votedonbylocals.com/restaurants/home-team-bbq.html",
        "servesCuisine": "Barbecue",
        "address": { "@type": "PostalAddress",
                     "addressLocality": "Charleston", "addressRegion": "SC" } } },

    { "@type": "ListItem", "position": 2, "item": {
        "@type": "<< BLOCKED >>", "name": "<< BLOCKED >>",
        "url": "https://votedonbylocals.com/restaurants/tru-blues-house-of-wings.html",
        "servesCuisine": "<< BLOCKED >>",
        "address": { "@type": "PostalAddress",
                     "addressLocality": "Mount Pleasant", "addressRegion": "SC" } } },

    { "@type": "ListItem", "position": 3, "item": {
        "@type": "Restaurant", "name": "Moe's Crosstown Tavern",
        "url": "https://votedonbylocals.com/restaurants/moes-crosstown-tavern.html",
        "servesCuisine": "Wings",
        "address": { "@type": "PostalAddress",
                     "addressLocality": "Charleston", "addressRegion": "SC" } } },

    { "@type": "ListItem", "position": 4, "item": {
        "@type": "<< BLOCKED >>", "name": "<< BLOCKED >>",
        "url": "https://votedonbylocals.com/restaurants/nigels-good-food.html",
        "servesCuisine": "<< BLOCKED >>",
        "address": { "@type": "PostalAddress",
                     "addressLocality": "<< BLOCKED >>", "addressRegion": "SC" } } },

    { "@type": "ListItem", "position": 5, "item": {
        "@type": "<< BLOCKED >>", "name": "<< BLOCKED >>",
        "url": "https://votedonbylocals.com/restaurants/dashi.html",
        "servesCuisine": "<< BLOCKED >>",
        "address": { "@type": "PostalAddress",
                     "addressLocality": "<< BLOCKED >>", "addressRegion": "SC" } } }
  ]
}
```

**`addressLocality` is the literal municipality, not "Charleston" rollup** -
DECISIONS #15 Q5, and its stated convention going forward: *"when a ranking
page's detail pages ship, the ranking-page ItemList's `addressLocality` per item
reconciles to the literal municipality used on the corresponding detail page in
the same PR."* Home Team BBQ's **primary** address is 1205 Ashley River Rd, West
Ashley, which is literally in the City of Charleston - so `"Charleston"` is
correct for it, not a rollup. Same for Moe's (714 Rutledge Ave, 29403). Tru Blues
is `"Mount Pleasant"` per note 3 above. Rows 4 and 5 are blocked on address data.

**`servesCuisine` on a ranking ItemList is list-scoped and hand-authored - it is
NOT a copy of `restaurants.json.cuisine`.** This is undocumented anywhere in
`_strategy/` and I only found it by comparing all 40 ItemList entries against the
data file: **12 of 40 diverge.** The pattern is clear from `best-burger`, which
uses `"Burgers"` for six entries whose `cuisine` fields say `American`/`Burgers`,
but keeps `"Barbecue"` for Home Team BBQ. And `best-tex-mex` uses `"Tex-Mex"` for
four entries whose `cuisine` is `Mexican`. So:

- Home Team BBQ gets `"Barbecue"` on this page, matching what it already carries
  on both of its existing ItemList appearances.
- Moe's gets `"Wings"` (its `cuisine` is the generic `American`; the list is the
  right anchor, per HANDOFF's PR #12 note *"`servesCuisine` value choice is
  brand-consistency-bound - the page's own copy is the right anchor, not a
  generic genre label"*).

**Date format:** `best-frozen-margarita` set the precedent of a hand-picked
noon-local stamp. It used `-05:00` for a May date; detail pages generated in May
used `-04:00`. August in Charleston is EDT, so `-04:00` is the correct offset. The
in-tree inconsistency is noted, not propagated.

### 2e. BreadcrumbList JSON-LD

Emitted as the **second** `ld+json` block, after ItemList. Shape is identical
across all 8 Top-N pages: `Home` -> `Rankings` (`https://votedonbylocals.com/#rankings`)
-> `Best Wings` (`https://votedonbylocals.com/rankings/best-wings.html`).

### 2f. Rows and CTA

Row block, duplicated 5x, class strings byte-identical to `best-pizza` /
`best-burger` / `best-frozen-margarita` (verified identical across all three):

```html
<!-- REPLACE: row N -->
<div class="group p-5 sm:p-6 hover:bg-orange-50/40 transition-colors rounded-xl flex items-start gap-4 sm:items-center">
    <div class="flex-shrink-0 mt-1 sm:mt-0 opacity-80 group-hover:opacity-100 transition-opacity transform group-hover:scale-110 duration-200">
        <span class="text-2xl" role="img" aria-label="poultry leg">🍗</span>
    </div>
    <div class="flex-1">
        <h2 class="font-poppins font-bold text-xl sm:text-2xl text-brand-dark mb-1 leading-snug"><a href="/restaurants/{slug}.html" class="hover:text-brand-orange transition-colors">{Name}</a></h2>
        <p class="text-brand-gray font-medium text-sm sm:text-base">{Tagline}</p>
    </div>
</div>
```

Bottom CTA copy is canonical per DECISIONS #7 - keep `Disagree with this list?
Cast your vote!` and set the button label to `Vote for Best Wings`.

---

## 3. Exact registry edits with anchors

All line numbers are against the tree as of `5d45683`.

### 3a. `components/header.html` - desktop dropdown

Top-N cluster sits **below** the divider on L38. Current tail:

```
L42 |                             <a href="/rankings/best-casual-spots.html" class="block px-4 py-2.5 text-gray-600 hover:text-brand-orange hover:bg-orange-50/50 transition-colors">Best Casual Spots</a>
L43 |                             <a href="/rankings/best-frozen-margarita.html" class="block px-4 py-2.5 text-gray-600 hover:text-brand-orange hover:bg-orange-50/50 transition-colors">Best Frozen Margarita</a>
L44 |                         </div>
```

**Insert after L43, before L44** (28-space indent):

```html
                            <a href="/rankings/best-wings.html" class="block px-4 py-2.5 text-gray-600 hover:text-brand-orange hover:bg-orange-50/50 transition-colors">Best Wings</a>
```

### 3b. `components/header.html` - mobile menu

```
L75 |                 <a href="/rankings/best-casual-spots.html" class="block py-2 px-4 text-gray-700 hover:bg-orange-50 hover:text-brand-orange font-medium">Best Casual Spots</a>
L76 |                 <a href="/rankings/best-frozen-margarita.html" class="block py-2 px-4 text-gray-700 hover:bg-orange-50 hover:text-brand-orange font-medium">Best Frozen Margarita</a>
L77 |  (blank)
L78 |                 <div class="border-t border-gray-100 my-2"></div>
```

**Insert after L76, before the blank L77** (16-space indent):

```html
                <a href="/rankings/best-wings.html" class="block py-2 px-4 text-gray-700 hover:bg-orange-50 hover:text-brand-orange font-medium">Best Wings</a>
```

### 3c. NEW pill - confirmed from the tree: **NO**

DECISIONS #23 part 2: *"Top-N launches do NOT get the NEW pill, regardless of
being newly added."* Verified mechanically - `components/header.html` contains
exactly three NEW-pill artifacts (L34 `relative` class, L36 the `NEW` span, L70
the mobile `(New!)` variant) and **all three belong to `best-bakery`**, a
featured-1 page. No Top-N entry carries one. The 60-day decay rule from
DECISIONS #19 therefore does not apply to this launch - there is nothing to
decay, and no TRACKED item to file.

### 3d. `index.html` - homepage grid card

```
L215 |                 <a href="/rankings/best-frozen-margarita.html" class="group block bg-white p-8 rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-transparent hover:border-brand-orange/20">
L216 |                     <h2 class="text-2xl font-bold font-poppins text-brand-dark group-hover:text-brand-orange transition-colors">Best Frozen Margarita</h2>
L217 |                     <p class="text-gray-600 mt-1">Charleston's coldest, most-poured margaritas. [tropical drink emoji]</p>
L218 |                 </a>
L219 |  (blank)
L220 |             </div>
```

**Insert after L218 and its trailing blank L219, before L220** (16-space indent).
Plain-card variant - no `border-brand-orange/20` highlight, no corner ribbon,
those are featured-1 launch ceremony:

```html
                <a href="/rankings/best-wings.html" class="group block bg-white p-8 rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-transparent hover:border-brand-orange/20">
                    <h2 class="text-2xl font-bold font-poppins text-brand-dark group-hover:text-brand-orange transition-colors">Best Wings</h2>
                    <p class="text-gray-600 mt-1">{one-line hook}. 🍗</p>
                </a>
```

The hook line is editorial - operator supplies. Existing hooks are 5-8 words with
a trailing emoji ("From wood-fired to classic slices.", "From dive bars to smash
hits.", "Easy eats for any day of the week.").

**Grid-cols: no change required.** L164 is
`<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">`. With 11
cards: `lg` gives 4/4/3, `md` gives 5 rows of 2 plus a single-card row, base gives
one column. Nothing breaks. **But** the `md` breakpoint leaves one orphaned card,
and this project has twice adjusted `grid-cols` at count boundaries for exactly
that reason (9 cards -> `md:grid-cols-3`; 10 cards -> `md:grid-cols-2
lg:grid-cols-4`). Whether the `md` orphan is acceptable is a visual judgment,
which is operator territory per `_strategy/WORKFLOW.md`'s verification norm. My
read: leave it, since `lg:grid-cols-4` is the primary desktop view and 4/4/3 is
clean. Flagging so it is a decision, not an oversight.

### 3e. `vote.html` - `<option>` appended at end

```
L173 |                                 <option>Best Burger</option>
L174 |                                 <option>Best Frozen Margarita</option>
L175 |                             </select>
```

**Insert after L174, before L175** (32-space indent):

```html
                                <option>Best Wings</option>
```

Governed by the in-file comment at L161-165: *"Top-N rankings only ... Append new
entries at end on launch (chronological by launch date)."* This is a Top-N launch,
so it **does** take an option - unlike the two featured-1 pages, which are
correctly absent (8 options for 8 Top-N pages today). This is the step PR #34
missed; DECISIONS #23 step 9 exists specifically to stop it happening again.

### 3f. `data/og_rankings.json`

```
L55 |     {
L56 |       "slug": "best-frozen-margarita",
L57 |       "category": "Frozen Margarita",
L58 |       "spots": 2
L59 |     }
L60 |   ]
```

**Append after L59** - add a comma to L59 so it reads `    },` then insert:

```json
    {
      "slug": "best-wings",
      "category": "Wings",
      "spots": 5
    }
```

**And bump L4** from `"lastUpdated": "2026-05-07"` to `"lastUpdated": "2026-08-24"`.

`spots: 5` must equal the real row count. It is not cosmetic: it drives the OG
image's "5 spots" label **and** the social pipeline's layout branch
(`social/src/data.ts` routes `spots === 1` to the featured-1 renderer).

---

## 4. Command sequence and blast radius

Execute in this order. File counts are what each step is expected to touch.

| # | Command / action | Files touched |
|---|---|---|
| 1 | Author `rankings/best-wings.html` (copy `best-pizza.html`, adapt; or start from `_template-canonical.html` and adopt the production JSON-LD shape per DECISIONS #23 step 1) | 1 new |
| 2 | Edit `data/restaurants.json`: append `appearsOn` entry to `home-team-bbq` + `moes-crosstown-tavern`; append 3 new restaurant objects; bump `_meta.lastUpdated` | 1 |
| 3 | Edit `data/og_rankings.json` per 3f | 1 |
| 4 | `python scripts/generate_detail_page.py home-team-bbq` | 1 rewritten |
| 5 | `python scripts/generate_detail_page.py moes-crosstown-tavern` | 1 rewritten |
| 6 | `python scripts/generate_detail_page.py tru-blues-house-of-wings` | 1 new |
| 7 | `python scripts/generate_detail_page.py nigels-good-food` | 1 new |
| 8 | `python scripts/generate_detail_page.py dashi` | 1 new |
| 9 | Manual `dateModified` bump in 2 regenerated detail pages - see below | 2 |
| 10 | Edit `components/header.html` per 3a + 3b | 1 |
| 11 | Edit `index.html` per 3d | 1 |
| 12 | Edit `vote.html` per 3e | 1 |
| 13 | `python scripts/inline_chrome.py --refresh` | **58 rewritten** |
| 14 | `python scripts/generate_og_images.py --slug best-wings` | 1 new PNG |
| 15 | `--slug tru-blues-house-of-wings` / `nigels-good-food` / `dashi` | 3 new PNGs |
| 16 | `python scripts/generate_sitemap.py` | 1 rewritten, +4 URLs |
| 17 | `python scripts/inline_chrome.py --check` | 0 (expect exit 0, "58 files in sync") |

**Do NOT run `generate_detail_page.py --all`** - it would rewrite all 39 detail
pages and blow the diff out for no reason.

**The 58 in step 13:** 54 files carry chrome markers today (confirmed by
`--check` output, not inferred). Steps 1 and 6-8 add 4 more marker-bearing files,
so `--refresh` writes 58. Every one of them will actually differ, because
`header.html` changed. Steps 1 and 6-8 must precede step 13 or the new pages get
stale chrome and `--check` fails with exit 2.

**Note:** `inline_chrome.py`'s own docstring and `--help` still say "49 production
HTML pages". Stale by 5 today, by 9 after this launch. Cosmetic; not fixing it in
the launch PR.

**No OG regeneration needed for `home-team-bbq` or `moes-crosstown-tavern`.**
Confirmed by reading `render_detail` in `scripts/generate_og_images.py:171-183` -
it substitutes only `name`, an adaptive font size derived from `name`, and a
meta-line from `cuisine` + `neighborhood`. None of those changed. `appearsOn` is
not an input.

**No `npm run build:css` needed** provided the new page introduces zero new
utility classes. Copying an existing Top-N page guarantees that. Verify before
skipping.

### `dateModified` bumps

| Detail page | Current `dateModified` | Bump? |
|---|---|---|
| `restaurants/home-team-bbq.html` | `2026-05-03T19:03:39-04:00` | **YES** |
| `restaurants/moes-crosstown-tavern.html` | `2026-05-03T19:03:39-04:00` | **YES** |
| the 3 new pages | none yet | No - seeded at generation |

Both existing pages gain a visitor-facing "Appears on" row, which is real
editorial freshness. The generator **preserves** prior dates by design
(`read_existing_dates`, `generate_detail_page.py:52-72`), so regeneration alone
leaves them stale. This is the exact failure PR #34 shipped and PR #36 had to fix;
see TRACKED's Resolved entry dated 2026-05-07 and the `dateModified maintenance
discipline` workstream. **The source of truth is the rendered HTML's JSON-LD, not
`data/restaurants.json`** - that schema carries no such field.

Bump both to the same stamp used for the ranking page: `2026-08-24T12:00:00-04:00`.
Then re-run the generator for each to confirm the new value survives regen.

**Watch the timezone on the 3 new pages.** `build_jsonld_dict` seeds from
`get_git_creation_date`, which returns `None` for a file with no git history, and
falls back to `datetime.now(timezone.utc).isoformat(timespec='seconds')` - i.e.
`+00:00`. Every existing page uses `-04:00` or `-05:00`. Either accept the
mismatch or hand-normalize the three new stamps to `-04:00` after first
generation. Recommend hand-normalizing for graph consistency.

---

## 5. Pre-flight checklist for the execute pass

Class strings below were verified by **running the actual social-pipeline regexes
from `social/src/data.ts` against `best-pizza.html`, `best-burger.html`, and
`best-frozen-margarita.html`** - not read off the prior report. All three pages
matched cleanly (5, 7, and 2 rows respectively; pill matched on all three).

- [ ] **ItemList block emitted BEFORE BreadcrumbList.** Verified as invariant
      across all 8 Top-N pages. `scripts/generate_sitemap.py`'s
      `extract_dateModified_from_html` matches only the **first** `ld+json` block;
      put BreadcrumbList first and `<lastmod>` silently vanishes - no error.
      `social/src/data.ts:extractItemList` iterates all blocks so it is tolerant,
      but the sitemap is not.
- [ ] **Row anchor class string exact:**
      `<a href="/restaurants/{slug}.html" class="hover:text-brand-orange transition-colors">`
      The social regex is
      `/<a href="\/restaurants\/([^"]+)\.html"[^>]*>[^<]+<\/a>[\s\S]*?<p class="text-brand-gray[^"]*">([^<]+)<\/p>/g`
      - the `class` attribute must start with `hover:text-brand-orange` only
      insofar as `[^>]*` tolerates it, but the tagline `<p>` **must** start its
      class with literally `text-brand-gray`.
- [ ] **Tagline paragraph class exact:**
      `<p class="text-brand-gray font-medium text-sm sm:text-base">`
- [ ] **Updated pill text matches `/Updated\s+([A-Z][a-z]+\s+\d{4})/`** - i.e.
      `Updated August 2026`, capital month, four-digit year. Confirmed matching on
      all three sampled pages.
- [ ] **`spots` in `og_rankings.json` equals the real body-row count (5), and is
      not 1.** `spots === 1` reroutes the social pipeline into `loadFeatured1`,
      which expects a single-entity JSON-LD block and no ItemList, and will throw.
- [ ] **Every ItemList `item.url` slug resolves to a `restaurants.json` entry AND
      to a body row with a tagline.** `loadTopN` throws on either miss, with
      distinct messages. Body-row order must equal ItemList `position` order -
      the social card derives `rank` from ItemList index, not from `position`.
- [ ] **Social card title check:** `best-wings` -> slice `best-`, split `-`,
      titleCase -> **"Best Wings"**. Correct. (Recorded for future reference:
      this derivation loses hyphens and lowercases acronyms - `best-tex-mex`
      renders "Best Tex Mex" and a hypothetical `best-bbq` would render "Best
      Bbq". Not a problem for this slug.)
- [ ] **`python scripts/inline_chrome.py --check` returns exit 0** after
      `--refresh`, printing "58 files in sync". Exit 1 = divergence, exit 2 =
      missing markers on a new page.
- [ ] **No literal `{{Placeholder}}` left anywhere** in the new page or the 3 new
      detail pages. Regex sweep for `\{\{[A-Za-z]` across `rankings/` and
      `restaurants/`.
- [ ] **No `""` empty-string values** introduced into `restaurants.json`. Absent
      data is `null`. `_meta.fieldPolicy` calls `""` a fabrication.
- [ ] **`aggregateRating` absent** from all new JSON-LD (DECISIONS #9).
- [ ] **`og:image` absolute, favicon relative** (DECISIONS #10).
- [ ] **Chrome not hand-edited** in any of the 58 pages - only
      `components/header.html` plus `--refresh`.
- [ ] ~~**First render of the U+1F357 emoji needs network.** `social/src/emoji.ts`
      fetches Twemoji `1f357.svg` from `cdn.jsdelivr.net` on cache miss and writes
      to `social/.emoji-cache/`, which is gitignored and currently holds only
      `1f950` and `2615`. Applies to the social PR, not the launch PR.~~

      **CORRECTION (2026-08-25): this checklist item was wrong and is void.** A
      Top-N card never requests an emoji at all, so no fetch happens and the empty
      cache is irrelevant. `TopNLayout` renders the rank as a number inside an
      orange circular badge (`{r.rank}`, `composition.tsx` row-badge block), and
      `RankingRow` in `social/src/data.ts` carries only `{rank, name, tagline}` —
      there is no emoji field on the Top-N path. The only two emoji references in
      `composition.tsx` (lines 420 and 496) are both inside `Featured1Layout`.

      The cache contents corroborate this exactly: `.emoji-cache/` holds `1f950`
      (croissant) and `2615` (hot beverage), which are precisely best-bakery's
      featured-1 icon group. Neither best-burger nor best-frozen-margarita — both
      Top-N, both rendered — contributed a single file.

      The original claim is kept struck through rather than deleted because the
      underlying mechanism it describes is real and still applies: `emoji.ts` does
      fetch from jsdelivr on cache miss, and that *would* bite a **featured-1**
      launch introducing a new icon. The error was scoping it to a Top-N launch,
      where the emoji path is never exercised.
- [ ] **`_strategy/` docs updated in the same PR as the file edits** they describe
      - DECISIONS #22 requires the file edit, not just PR-description prose.

Discrepancies found between the tree and the prior investigation report: see
section 7.

---

## 6. PR decomposition

Separate PRs per concern, matching the cadence the repo already uses.

### PR 1 - `best-wings` Top-5 launch

Steps 1-17 above. Suggested commit shape, mirroring DECISIONS #19's 4-commit
estimate:

1. `feat: add best-wings ranking page + restaurant data` (steps 1-9)
2. `feat: register best-wings in nav, homepage grid, vote form` (steps 10-13)
3. `feat: best-wings OG images + sitemap` (steps 14-16)

Files: 1 ranking page + 3 new detail pages + 2 regenerated detail pages + 4 PNGs
+ `restaurants.json` + `og_rankings.json` + `header.html` + `sitemap.xml`, and the
58-file chrome refresh (of which `index.html` and `vote.html` also carry their own
content edits).

### PR 2 - social card + reel

`npm run render:card -- --slug best-wings` and
`npm run render:reel -- --slug best-wings`, from `social/`. Outputs land in
`social-assets/best-wings/`, which is **gitignored** - so this PR carries code
changes only if the Top-5 layout needs adjustment, and otherwise carries nothing
committable. Separate per the established pattern (PRs #28, #30, #33, #37 were all
standalone social PRs). Top-5 is the layout the pipeline was originally built for,
so no `justifyContent` small-N work is expected here.

### Explicitly OUT of scope for the launch PR

- **`best-bakery` NEW pill removal.** Out. It is a different concern (featured-1
  decay ceremony under DECISIONS #19) that happens to touch the same two files.
  Bundling it makes the launch diff ambiguous and couples an editorial-calendar
  item to a content launch. It is also **overdue** - the TRACKED item schedules it
  for 2026-07-05, roughly seven weeks ago - so it deserves its own PR and its own
  visual check, not a ride-along. Worth doing soon; not here.
- **`index.html` `id="rankings"`.** Out. It was gated on "post-May-20" (the GSC
  quiet window), which has long passed, so it is unblocked - but it is a
  BreadcrumbList-fragment concern from PR #18, unrelated to this launch. Its own
  one-line PR.
- **Social card and reel.** Out, per PR 2 above and the explicit note in DECISIONS
  #23 step 10 that social is *"separate follow-up PR cadence per the existing
  pattern, not strictly part of the launch PR."*
- **Formalizing the Top-N recipe in DECISIONS #23.** Out of the launch PR, but it
  becomes **due right after**. #23 deferred formalization *"until a second Top-N
  launch shows what the recipe genuinely shares vs. what was specific to this
  PR"* - and this is that second launch. The recipe can only be written from what
  actually happened, so it must follow the launch, not precede it. Propose a third
  PR: `docs: formalize Top-N launch recipe in DECISIONS #23` once PR 1 merges. New
  material this launch contributes that PR #34 could not: three net-new
  restaurants (#34 had zero), a first-time `servesCuisine` list-scoping decision,
  and the new-page `dateModified` timezone seam.

---

## 7. Prior-report claims that did not hold up, and new findings

Checked against the tree, not carried forward.

**Held up:** the 54-file chrome count (now confirmed by `--check`'s own output,
not inferred); ItemList-before-BreadcrumbList on every Top-N page; the sitemap's
first-block-only `dateModified` parse; all social-pipeline class strings; the
`index.html` grid class at L164; NEW-pill-is-featured-1-only; the `vote.html`
Top-N-only rule; `spots` as a layout switch; `dateModified` living only in
rendered HTML.

**Needed correction:**

1. **`cuisine` is not "always used for JSON-LD `servesCuisine`".** The prior
   report's field table said so. That is true only for the **detail-page**
   generator, where DECISIONS #18 point 5 mandates it. On **hand-authored
   ranking-page ItemLists** it is list-scoped and hand-picked: **12 of 40 entries
   diverge from `restaurants.json.cuisine`** (`best-tex-mex` uses "Tex-Mex" for
   four `Mexican` entries; `best-burger` uses "Burgers" for three `American`
   entries; `best-nice-restaurants` uses "Contemporary American" for two
   `American` entries; and more). Directly relevant here - it is why Moe's gets
   "Wings" and not "American".

**New findings, neither in the prior report nor in `_strategy/`:**

2. **Live `servesCuisine` drift on `best-pizza` / Tutti Pizza.** The ranking page
   ItemList says `"Neapolitan Pizza"`; the cross-linked detail page
   `restaurants/tutti-pizza.html` says `"New York-Style Pizza"`. DECISIONS #18
   records the `restaurants.json` correction from "Neapolitan Pizza" to "New
   York-Style Pizza" and flags the *editorial* fields as an open follow-up, but
   never mentions the ranking-page ItemList. So the same entity carries two
   different `servesCuisine` values across a `url`-linked structured-data graph -
   the same inconsistency class DECISIONS #15 Q5 fixed for `addressLocality`.
   Pre-existing, unrelated to this launch. **Recommend filing as a TRACKED
   one-off; do not fix in the launch PR.** Also note DECISIONS #18's own
   follow-up 2 ("Cuisine-field accuracy audit") triggers on *"when next touching
   `restaurants.json` data significantly"* - which this launch does.

3. **"Mount Pleasant" vs "Mt Pleasant" split in `restaurants.json`.**
   `tonis-detroit-style-pizza` uses the full form, `san-miguel-mexican-grill` the
   abbreviation, and both propagate into ranking ItemLists. Blocks nothing, but it
   forces a choice for Tru Blues. See section 1b note 3.

4. **New detail pages will get a `+00:00` timestamp.** `build_jsonld_dict` falls
   back to `datetime.now(timezone.utc)` when git has no first-add commit for the
   file, while all 36 existing pages carry `-04:00` / `-05:00`. First time this
   path matters, because PR #34 added no net-new restaurants.

5. **`inline_chrome.py` docstring says "49 production HTML pages"** in three
   places (module docstring, `--check` exit-code note, `argparse` description).
   Actual is 54, going to 58. Cosmetic.

---

## 8. Question resolutions

Resolved 2026-08-24. Q4 (partial), Q5-Q10 are decided below and need no further
input. Q1, Q2, Q3 and three of the five taglines cannot be resolved from the
repository and are **not** resolvable by me - see "Still open" at the end.

### RESOLVED

**Q4a - Home Team BBQ tagline: `BBQ Institution, Wings to Match`**

Differs from both of its existing per-list taglines ("Smoky, Underrated Gem" on
best-burger, "BBQ, Wings, Good Times" on best-casual-spots), which is the intended
behavior. "Institution" and "to match" are editorial judgment in the register the
site already uses ("Legendary Dive Bar Burger"); neither asserts an unverifiable
fact about ingredients or preparation. Deliberately avoided "Smokehouse Wings" -
that would imply the wings are smoked, which nothing in the tree establishes.

**Q4b - Moe's Crosstown Tavern tagline: `Dive Bar Wings, Open Till 2am`**

Both halves are grounded in the entry's own data: "dive bar" from its
`description`, and 2am from `hours: "Mo-Su 11:00-02:00"` /
`hoursHumanReadable: "Mon-Sun: 11am-2am"`. Matches the register of its
best-burger tagline without repeating it.

**Q5 - Hero emoji: U+1F357 POULTRY LEG, `aria-label="poultry leg"`. Confirmed.**

Every page emoji on the site depicts food as served, never the animal, which
rules out U+1F414 CHICKEN. `aria-label` follows the in-tree convention of plain
lowercase names ("pizza slice", "wine glass", "tropical drink"). One emoji for the
page, reused on all five rows per `_template-canonical.html` intentional decision
#1. Twemoji coverage (`1f357.svg`) is a PR-2 concern, already on the checklist.

**Q6 - Homepage card hook: `Crispy, saucy, and worth the napkins.` + emoji**

Category-level editorial that asserts nothing about any specific restaurant, so
it survives any roster change. Length and shape match the existing hooks (5-8
words, trailing page emoji).

Alternate, **only if the five-name roster holds**: `From dive bars to wing
houses.` - mirrors best-burger's "From dive bars to smash hits." but leans on Tru
Blues' name, so it breaks if the roster trims. Primary is the safer default.

**Q7 - `md`-breakpoint orphan: accept it. Leave `index.html` L164 unchanged.**

Do NOT change `grid-cols`. Reasoning: at `lg:grid-cols-4` eleven cards render
4/4/3, which is clean, and that is the primary desktop view. Switching `md` from
2 to 3 columns would put three `p-8` cards with `text-2xl` headings inside a
`max-w-4xl` (896px) container - roughly 277px per card - which is almost
certainly why the 10-card change went to `md:grid-cols-2` rather than keeping
`md:grid-cols-3`. Trading a readable `md` layout for one orphaned card is a bad
swap. A future 12th card makes `md:2` even again.

**Q8 - Moe's burger-framed prose: leave it, file a TRACKED one-off.**

Out of scope for the launch PR. The per-list tagline lives on the ranking page,
so the wings list itself reads correctly; the mismatch is only visible on the
shared detail-page hero. Fixing it properly is a Tutti-class editorial cascade
(`tagline`, `description`, `shareTagline`, `keywords`) - an editorial-voice
change that would balloon the launch diff and warrants its own review.

TRACKED entry to file, under "Brand identity follow-ups":

> **Moe's Crosstown Tavern prose is single-category-framed but now cross-listed.**
> Every prose field (`tagline`, `description`, `shareTagline`, `keywords`) frames
> Moe's solely as a burger destination, written when best-burger was its only
> listing. It now also appears on best-wings. Home Team BBQ is the pattern to
> follow - its `tagline` "BBQ, Wings, Good Times" and `description` naming smoked
> meats, wings, and burgers read correctly across all of its lists. Broaden Moe's
> shared prose on the same model. Detail-page-only surface; ranking pages carry
> their own per-list taglines and are unaffected. Trigger: next edit to this
> entry. Filed by the best-wings launch.

**Q9 - `"Mount Pleasant"` for Tru Blues' `address.addressLocality`. Confirmed.**

It is the legal municipality, and `tonis-detroit-style-pizza` already uses it.
The tree's apparent inconsistency is narrower than section 1b note 3 suggested -
corrected here after a full sweep:

- `"Mt Pleasant"` as a `locations[].label` is **intentional display copy** and is
  correct as-is. Three entries use it that way (`home-team-bbq`, `santis`,
  `bon-banh-mi-southeast-asian-kitchen`).
- The only **schema-field** offender is `san-miguel-mexican-grill`, which carries
  `"Mt Pleasant"` in `address.addressLocality` - and that propagates to its
  detail page's visible postal address ("Mt Pleasant, SC 29464") and to the
  ItemLists on `best-tex-mex` and `best-frozen-margarita`.
- Its `neighborhood: "Mt Pleasant"` is a **display** field (hero subtitle, OG
  meta-line) and should be **left alone**. Only `address.addressLocality` is
  wrong.

TRACKED entry to file, under "Schema completeness follow-ups":

> **`san-miguel-mexican-grill` `address.addressLocality` is `"Mt Pleasant"`;
> should be `"Mount Pleasant"`.** A postal address field should carry the legal
> municipality, as `tonis-detroit-style-pizza` does. Scope: one field in
> `data/restaurants.json`, regenerate `restaurants/san-miguel-mexican-grill.html`,
> and reconcile the ItemList `addressLocality` on `rankings/best-tex-mex.html` and
> `rankings/best-frozen-margarita.html` in the same PR per DECISIONS #15 Q5. Do
> NOT touch the `neighborhood` field - "Mt Pleasant" is correct there as display
> copy, matching the `locations[].label` convention. Filed by the best-wings
> launch.

**Q10 - Both `dateModified` bumps confirmed; offset `-04:00`.**

`restaurants/home-team-bbq.html` and `restaurants/moes-crosstown-tavern.html` both
move from `2026-05-03T19:03:39-04:00` to the launch stamp. An `appearsOn` addition
puts a new visitor-facing "Appears on" row on the page, which is real editorial
freshness - the PR #34 / PR #36 precedent is this exact case. Charleston is on EDT
in August, so `-04:00` is correct. Use the actual launch date at noon local; if
executed today that is `2026-08-24T12:00:00-04:00`, matching the ranking page's
own `datePublished` / `dateModified`.

Also normalize the three new detail pages' seeded `+00:00` stamps to `-04:00`
after first generation, so the whole graph is on one offset.

---

## 9. Sourcing pass results (2026-08-24)

Operator authorized a sourcing pass for Q1 / Q2 / Q3. Method: each restaurant's
own website treated as the anchor, cross-checked against independent listings.
Per-field provenance recorded below. Anything not stated by a source ships
`null` - nothing was inferred or filled from model knowledge.

**Outcome: the five-name roster does not survive contact with the sources. One of
the three is fully verified, one is partially blocked, one is closed.**

### 9a. Tru Blues House of Wings - EXCLUDED, contested operating status

> **STATUS CHANGED 2026-08-24, after this section was first written.** An
> unconfirmed report gives a final service date of **2026-07-03** following
> renovations, while the restaurant's own site, Yelp, Tripadvisor and
> restaurantji all carry no closure marker. That is a live conflict, and
> contested status is disqualifying under the same exclude-and-re-verify
> precedent applied to Nigel's Good Food in 9b and, before that, to Toni's
> Clements Ferry and Señor Tequila's Mt Pleasant.
>
> **This is NOT the Dashi case.** Dashi is a confirmed permanent closure with
> three converging sources and gets no re-verification trigger (9c). Tru Blues
> is a conflict between sources, and gets one (9e).
>
> Everything below is **retained deliberately** - the identity research is
> correct and independently verified, and it is the expensive part to redo. If
> the status resolves to "open", this section is ready to use as-is.

Q1 resolved. **Own site header and logo spell it `Tru Blues House of Wings`, no
apostrophe.** Third-party listings disagree with each other and with the
restaurant - Instagram `@trublueshouseofwings` and Facebook use "Tru Blue's",
Tripadvisor uses "True Blue's". The site's own copy is the anchor per the PR #12
convention recorded in HANDOFF. Use the no-apostrophe form.

The "(Mount Pleasant)" in the roster line is a **disambiguator, not part of the
brand** - the own site advertises a single location and no other Tru Blues exists
in the listings. Q3 for this entry: **single-location, no `locations[]` needed.**

Slug `tru-blues-house-of-wings` stands.

| Field | Value | Source |
|---|---|---|
| `name` | `Tru Blues House of Wings` | own site header/logo, trublueswings.com |
| `cuisine` | `Wings` | own copy: *"the best chicken wings in town"* |
| `neighborhood` | `Mt Pleasant` | display form, matching `san-miguel-mexican-grill` |
| `schemaType` | `BarOrPub` | own copy: *"One of Mount Pleasant's oldest bars"*, self-describes as a sports bar |
| `streetAddress` | `1039 Johnnie Dodds Blvd` | own contact page |
| `addressLocality` | `Mount Pleasant` | legal municipality per Q9; own site writes "Mt Pleasant" |
| `addressRegion` / `postalCode` / `addressCountry` | `SC` / `29464` / `US` | own contact page |
| `phone` | `+1-843-881-1858` | own contact page |
| `websiteURL` | `https://trublueswings.com/` | - |
| `hours` | **`null`** | own site does not state hours; aggregator values were partial and unconfirmed |
| `hoursHumanReadable` | `Hours vary [em-dash] see trublueswings.com or call (843) 881-1858 for current hours.` | DECISIONS #13.10 fallback, copying the `tonis-detroit-style-pizza` string shape exactly |
| `priceRange`, `geoLat`, `geoLng`, `imageURL`, `editorialBody`, `areaServed`, `displayCuisine` | `null` | not sourced |

Two notes held for a future execute pass, **if the status question resolves to
"open"**:

- **`BarOrPub` would be its first use in this dataset** (current spread: 28
  `Restaurant`, 5 `CafeOrCoffeeShop`, 2 `FoodEstablishment`, 1 `Bakery`). It is
  explicitly sanctioned in both template docblocks and by DECISIONS #5. No code
  change needed - `schemaType` is passed straight through.
- **The cuisine-dedup auto-detect would fire on this entry, correctly.**
  Normalized `"wings"` is a substring of normalized `"tru blues house of wings"`,
  so `_should_suppress_cuisine` returns true and the generator drops the cuisine
  slot from `<title>`, `og:title`, `twitter:title`, the hero subtitle, and the OG
  meta-line. Title becomes "Tru Blues House of Wings in Charleston | Voted On By
  Locals"; hero subtitle becomes "Mt Pleasant" alone. This is DECISIONS #18
  working as designed - **do not add a `displayCuisine` override to defeat it.**
  `servesCuisine` in the JSON-LD keeps the raw `Wings`.

### 9a-bis. Identity gate vs liveness gate - a rule this launch established

Tru Blues is the case that forced the distinction. Its own website is the **best**
source for how the brand spells its own name, and simultaneously **worthless** as
evidence that the doors are open. Restaurant websites are near-universally
maintained for identity and near-universally stale on status - Nigel's own site
still advertises a location Yelp marked closed this month (9b), and Hannibal's own
About page still carries a COVID-era line about being closed for in-house dining
years after the fact (9f).

**The rule, for this and every future launch:**

| Question | Own site | Dated third-party signals |
|---|---|---|
| What is the brand called? Address, phone, menu, what it serves | **AUTHORITATIVE** | corroborating only |
| Is it currently operating? Current hours? | **INADMISSIBLE** | **REQUIRED** |

An own-site page is never sufficient evidence of liveness, no matter how current
it looks. Liveness requires dated third-party signals: recent reviews, directory
closure markers, news coverage, dated social posts. A **conflict** between
sources is disqualifying, exactly like a closure - the entry gets excluded and a
re-verification trigger filed. Only converging evidence of "open" clears the gate.

This applies to **existing** entries too, not just new ones. Any restaurant about
to receive a new listing and a `dateModified` bump should clear the liveness gate
first - the bump is an assertion of freshness, and asserting freshness about a
closed restaurant is worse than saying nothing. Both existing entries on this
launch were gated before proceeding; see 9g.

### 9b. Nigel's Good Food - PARTIALLY BLOCKED, location set is contested

Q3 resolved: **multi-location, so it needs `locations[]` per DECISIONS #17** - but
which locations is exactly the unresolved part.

| Location | Own site `/location/` | Yelp | Verdict |
|---|---|---|---|
| 3760 Ashley Phosphate Rd, North Charleston 29418 (the 2011 original) | **absent** | marked CLOSED, updated June 2026 | **Converging closure signal - exclude** |
| 9616 Hwy 78, Ladson 29456 ("Nigel's Good Food II") | listed, no hours, no phone | no closure marker found | **Only clean location** |
| 7000 Bowen Pier Dr Unit 2, Hanahan 29410 | listed, `Mon. - Sat. 11am-8pm` | marked CLOSED, updated **August 2026** | **Live conflict - exclude pending verification** |

The own site advertises Hanahan with full hours while Yelp marks it closed this
month. The site has also silently dropped the Ashley Phosphate original, which
suggests the site is maintained but lags. That is the exact pattern behind the
existing TRACKED entries for Toni's Clements Ferry (*"Yelp marked closed June
2025; official site lists only Mt Pleasant"*) and Señor Tequila's Mt Pleasant -
both of which resolved to **exclude and file a re-verification trigger**, not to
guess.

Wings relevance is real but indirect: "Geechie Wings" is a signature dish, and
turkey wings appear on the soul-food menu. It is a soul-food restaurant, not a
wing specialist. Home Team BBQ sets the precedent that a non-specialist can carry
a wings listing, so this is an editorial call, not a disqualifier.

What is missing regardless of the location question: **no phone number appears on
any page of the own site**, and hours exist only for the contested Hanahan
location. So even the clean Ladson entry ships `phone: null`, `hours: null`,
`hoursHumanReadable: null` - and unlike Tru Blues, the DECISIONS #13.10 fallback
copy cannot be used, because that string requires either a website or a phone to
point the reader at, and the brand-level site does not carry per-location contact
detail.

Also unresolved: **is Ladson inside editorial scope?** DECISIONS #14.1 scopes to
greater Charleston. The dataset already includes Summerville (29486), Mount
Pleasant, North Charleston, Folly Beach and Sullivan's Island, so Ladson is
plausibly in - but it has no precedent in the tree. Operator call.

**Recommendation: hold Nigel's out of the launch PR.** Its primary location is
genuinely undetermined right now, and a detail page's `address` is not a field
that can ship provisionally - it drives JSON-LD, the visible sidebar, and the
ItemList `addressLocality`. Add it in a follow-up once the operator confirms which
door is open.

### 9c. Dashi - BLOCKED, permanently closed

**The Dashi restaurant at 1262 Remount Rd, North Charleston closed permanently on
June 14, 2026.** Three independent sources agree:

- Post and Courier, published 2026-06-15: *"Dashi's last day of service was June
  14, co-owner Oscar Hines confirmed to The Post and Courier."*
- Live 5 News, 2026-06-15: "Lowcountry Asian, Latin fusion restaurant permanently
  closing its doors."
- Yelp, updated August 2026: both the Food Trucks listing and the Wine Bars
  listing at 1262 Remount Rd are marked CLOSED.

The food-truck route does not rescue it - Dashi ran as a truck for five years
before the 2019 brick-and-mortar, but the truck listing is itself marked closed,
so the `dough-boyz` mobile-vendor pattern (`FoodEstablishment` + `areaServed`) has
nothing to attach to.

The only surviving Dashi-branded business is **Dashi Wine Bar and Emporium on
Rivers Avenue**, per the same Post and Courier piece: *"He said the Dashi Wine Bar
and Emporium, located down the road on Rivers Avenue, will remain open."* That is
a different name at a different address, and no source connects it to the Thai
wings the restaurant was known for. It is not a substitute entry.

**Dashi is out. Not deferred - out.** Ranking a restaurant that closed ten weeks
ago is the single most damaging content error this site could publish, given the
brand wedge.

### 9d. Revised roster and knock-on changes

**FINAL roster.** Three of the five names originally proposed did not survive
sourcing; a fourth restaurant was substituted in.

| Rank | Restaurant | Status |
|---|---|---|
| 1 | Home Team BBQ | READY - existing entry, `appearsOn` append only. Liveness gate passed (9g) |
| 2 | Hannibal's Kitchen | READY - new entry, fully sourced and gated (9f) |
| 3 | Moe's Crosstown Tavern | READY - existing entry, `appearsOn` append only. Liveness gate passed (9g) |
| - | Tru Blues House of Wings | EXCLUDED - contested status, re-verification filed (9a, 9e) |
| - | Nigel's Good Food | HELD - location set contested (9b, 9e) |
| - | Dashi | REMOVED - confirmed closed 2026-06-14, no trigger (9c, 9e) |

Attrition rate on the originally proposed roster: **three of five excluded**, for
three different reasons - one confirmed closure, two unresolved conflicts. That is
the sourcing pass earning its cost.

**`best-wings` is a Top-3, not a Top-5.** Consequences, all of which supersede the
Top-5 assumptions earlier in this file:

- `data/og_rankings.json` -> `"spots": 3`, not 5. Still not 1, so the social
  pipeline stays on the Top-N path.
- Subtitle takes count framing per DECISIONS #4 / #20 / #23:
  **"As voted by Charleston locals. Three standouts - with more to come."**
  Top-3 is a **new ranking-length precedent** - the documented set is
  featured-1 / Top-2 / Top-4 / Top-5 / Top-7. It slots into the existing pattern
  without inventing anything, and DECISIONS #23 should record it alongside Top-2
  when the recipe is formalized.
- ItemList carries 3 entries, positions 1-3. Body carries 3 rows.
- Rank order within the surviving three is preserved from the operator's roster:
  Home Team BBQ, Tru Blues, Moe's.
- Only **one** new restaurant entry, detail page, and OG PNG instead of three.
  Revised blast radius: `--refresh` touches **56** files, not 58.
- `vote.html`, `components/header.html`, `index.html` edits are unchanged - none
  of them depends on N.
- Still only two `dateModified` bumps (Home Team BBQ, Moe's), unchanged from Q10.
- Final taglines, all three settled:

  | Rank | Restaurant | Tagline |
  |---|---|---|
  | 1 | Home Team BBQ | `BBQ Institution, Wings to Match` |
  | 2 | Hannibal's Kitchen | `Gullah Soul Food, Fried Drumettes` (superseded `Soul Food Landmark, Fried Drumettes` post-launch - see note below) |
  | 3 | Moe's Crosstown Tavern | `Dive Bar Wings, Open Till 2am` |

  All three differ from the same restaurant's taglines on any other list, which is
  the intended per-list behavior. Hannibal's is grounded in sourced fact - it has
  operated since 1985 (landmark) and its wings are fried drumettes in the house
  batter (9f), not a generic descriptor.

### 9e. TRACKED entries this pass generates

To file in the launch PR per DECISIONS #22 (same-PR file edit, not PR prose):

> **Nigel's Good Food - location set unresolved, held from `best-wings`.** Own
> site `/location/` advertises Ladson (9616 Hwy 78, 29456) and Hanahan (7000
> Bowen Pier Dr Unit 2, 29410); Yelp marks Hanahan CLOSED as of August 2026 and
> the 2011 Ashley Phosphate original (3760 Ashley Phosphate Rd) CLOSED as of June
> 2026, and the own site no longer lists Ashley Phosphate at all. No phone number
> appears anywhere on the own site; per-location hours exist only for the
> contested Hanahan location. Primary-location choice therefore cannot be made
> without operator verification. Also unresolved: whether Ladson falls inside the
> DECISIONS #14.1 greater-Charleston editorial scope (no Ladson precedent in the
> dataset; Summerville is the nearest analogue). Trigger: operator confirms which
> locations are open, or a research pass reaches the restaurant directly. Same
> exclude-and-re-verify pattern as the Toni's Clements Ferry and Señor Tequila's
> Mt Pleasant entries. Filed by the best-wings launch.

> **Tru Blues House of Wings - operating status contested, held from
> `best-wings`.** An unconfirmed report gives a final service date of 2026-07-03
> following renovations. Against that: the restaurant's own site
> (trublueswings.com) is live with no closure notice, and Yelp, Tripadvisor and
> restaurantji carry no closure marker. Per the identity-vs-liveness rule
> (analysis file section 9a-bis), an own site is inadmissible as liveness
> evidence, and the third-party sources here are absence-of-a-marker rather than
> a positive dated signal of operation - so the conflict is unresolved in both
> directions. Identity research is complete and verified and is preserved in the
> analysis file section 9a: own-site spelling is "Tru Blues House of Wings" (no
> apostrophe, contra Instagram/Facebook "Tru Blue's" and Tripadvisor "True
> Blue's"); 1039 Johnnie Dodds Blvd, Mount Pleasant, SC 29464;
> +1-843-881-1858; single-location; `schemaType` `BarOrPub`. If it reopens or the
> closure report is disproved, the entry is ready to ship as-is and slots in at
> rank 2. Trigger: a dated third-party signal either way - a recent review, a
> reopening announcement, or a directory closure marker. Same pattern as Toni's
> Clements Ferry and Señor Tequila's Mt Pleasant. **Distinct from the Dashi entry
> below, which is a confirmed permanent closure and carries no trigger.** Filed by
> the best-wings launch.

> **Dashi removed from `best-wings` consideration - permanently closed
> 2026-06-14.** The Remount Rd restaurant closed per Post and Courier
> (2026-06-15, co-owner confirmed) and Live 5 News; Yelp marks both the food-truck
> and wine-bar listings at 1262 Remount Rd closed as of August 2026. Dashi Wine
> Bar and Emporium on Rivers Avenue remains open but is a distinct business at a
> distinct address with no sourced wings connection. No re-verification trigger -
> this is a permanent closure, not a conflicting signal. Recorded so a future
> session does not re-propose it. Filed by the best-wings launch.

### 9f. Hannibal's Kitchen - VERIFIED, ships at rank 2

Substituted into the roster after Tru Blues was excluded. Cleared both gates:
identity confirmed against the own site, liveness confirmed against dated
third-party signals.

**Liveness:** Yelp updated July 2026 with 453 reviews and 642 photos, no closure
marker; restaurantji listing carries no closed / temporarily closed marker;
Tripadvisor active. PASS.

**Slug:** `hannibals-kitchen`. Apostrophe dropped, not hyphenated - verified
against the tree's convention across all 36 entries (`dallesandros-pizza` for
"D'Allesandro's", plus `moes-crosstown-tavern`, `little-jacks-tavern`,
`heavys-barburger`, `santis`, `verns`, `teds-butcherblock`, `weltons-tiny-bakeshop`,
`tonis-detroit-style-pizza`, `edmunds-oast`).

**Single location** - no `locations[]` needed. No second address surfaced in any
source.

| Field | Value | Source |
|---|---|---|
| `name` | `Hannibal's Kitchen` | own site, all listings agree |
| `cuisine` | `Soul Food` | own site "Feeding The Soul Of the City"; listings categorize as Soul Food |
| `neighborhood` | `Eastside` | Tripadvisor files it under "East Side"; 16 Blake St is in the Eastside neighborhood |
| `schemaType` | `Restaurant` | default per DECISIONS #5; no more specific subclass applies |
| `streetAddress` | `16 Blake St` | own site, restaurantji, Yelp, EatOkra all agree |
| `addressLocality` / `Region` / `postalCode` / `Country` | `Charleston` / `SC` / `29403` / `US` | same |
| `phone` | `+1-843-722-2256` | restaurantji, Yelp, own site agree |
| `websiteURL` | `https://hannibalkitchen.com/` | - |
| `priceRange` | `$` | operator-supplied; consistent with listings |
| `hours` | `Mo-Sa 11:00-20:00` | **CONFIRMED** - restaurantji lists it per-day (Mon-Sat 11AM-8PM, Sunday Closed); two further independent listings agree |
| `hoursHumanReadable` | `Mon[U+2013]Sat: 11am[U+2013]8pm\nSun: Closed` | en-dash U+2013 per the tree's convention; shape copied from `park-pizza-co`, the exact Mon-Sat + Sun-closed precedent |
| `displayCuisine`, `geoLat`, `geoLng`, `imageURL`, `editorialBody`, `areaServed` | `null` | not sourced |

**Hours were confirmed, so the DECISIONS #13.10 fallback is NOT used.** The
operator's instruction to avoid the own About page was correct and independently
necessary: that page still carries a line about being closed for in-house dining
with patio service only, which is COVID-era residue years stale. It was not used
for hours or for dine-in status. This is the concrete case that motivated the
identity-vs-liveness rule in 9a-bis.

**Wings are genuinely on the menu** - verified before putting a soul-food
restaurant on a wings list. Chicken wing drumettes at $16 as a plate and 6-piece
drumettes at $5.50 as a side, fried in the same powdery house batter as their
fried shrimp and whole flounder, per the Post and Courier restaurant review.
Turkey wings appear as a daily special. Note that restaurantji's page does not
surface wings at all, so a single-source check would have produced a false
negative here.

**Copy constraint honored: the word "buffalo" appears in no field.** Their wings
are fried drumettes in the house batter with sauce options, which is a materially
different thing, and the sourced description supports the distinction.

Editorial fields drafted to the site's register, asserting only sourced facts
(operating since 1985, Huger family, soul food, Eastside, fried drumettes):

- `tagline`: ~~`Soul Food Landmark, Fried Drumettes`~~ -> **`Gullah Soul Food, Fried Drumettes`**
  (superseded post-launch. "Landmark" duplicated the claim already made by row 1's
  "BBQ Institution"; the replacement is grounded in their own About page, which leads
  on Gullah culture and the Eastside. Single-listed, so `restaurants.json.tagline` and
  the ranking-page row string move together.)
- `description`: `Hannibal's Kitchen is an Eastside soul food landmark in Charleston, SC, serving Gullah classics and fried wing drumettes since 1985. Voted by Charleston locals as one of the city's best wings.`
- `shareTagline`: `Eastside soul food since 1985, voted best wings by Charleston locals.`
- `keywords`: `Hannibal's Kitchen Charleston, best wings Charleston SC, soul food Charleston, Eastside Charleston restaurants, Gullah food Charleston`

### 9g. Liveness gate on the two existing entries

Run before either entry took a new listing and a `dateModified` bump, per the rule
in 9a-bis. Own sites were treated as inadmissible for this purpose.

| Entry | Dated third-party signals | Verdict |
|---|---|---|
| `home-team-bbq` (1205 Ashley River Rd, West Ashley) | Yelp updated **August 2026**, 634 reviews / 570 photos, no closure marker. Tripadvisor 481 reviews, 4.5/5, ranked #66 of 807 Charleston restaurants. Charleston Area CVB listing active. | **PASS** |
| `moes-crosstown-tavern` (714 Rutledge Ave) | Yelp updated **July 2026**, 254 reviews / 245 photos, no closure marker. Tripadvisor 2026 review page active. Charleston Magazine dining guide listing. Restaurant Guru 4.6/5 across 2,455 reviews. | **PASS** |

Neither shows a closure or conflict signal. Both cleared to receive the
`best-wings` listing and the `dateModified` bump to `2026-08-24T12:00:00-04:00`.

---

## Encoding note

Non-ASCII characters intentionally present in this file, so the execute pass can
verify they survived the round trip:

- U+1F357 POULTRY LEG - the proposed hero/row emoji, appears in sections 2b, 2f, 3d.
  Also referenced by codepoint throughout, so a mangled glyph is recoverable.
- U+00F1 LATIN SMALL LETTER N WITH TILDE - in "Señor Tequila's", sections 9b and 9e.

**One deliberate ASCII substitution to repair at execute time.** Section 9a's
`hoursHumanReadable` value is written as `Hours vary [em-dash] see ...`. The real
value must use a literal em-dash U+2014, byte-identical to the existing
`tonis-detroit-style-pizza` string:

```
Hours vary [U+2014] see tonisdetroitpizza.com or call (843) 416-8232 for current hours.
```

Copy that string's shape from `data/restaurants.json`, not from this file.

No arrows or box glyphs were used. Other existing site copy quoted here has been
rendered with ASCII hyphens where the original uses an em-dash; the originals are
unchanged in the tree and should be copied from the tree, not from this file.
