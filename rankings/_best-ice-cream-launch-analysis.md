# Best Ice Cream launch - analysis working file

Analysis-only working file for the `best-ice-cream` Top-3 launch. Author: Claude
session 2026-08-25, branch `best-ice-cream-launch`, off `main` @ `704fcf5`.
Nothing here has been applied to the tree.

Location per `_strategy/WORKFLOW.md`: underscore-prefixed, in the directory of
the work it supports (`rankings/`), not `_strategy/`. Same as
`_best-wings-launch-analysis.md`.

Recipe followed: **DECISIONS #23, "Top-N launch recipe (formalized)"**, read from
the tree rather than from the prompt. Section 9 below lists every place the
prompt and the recipe disagree.

---

## 1. Roster verification - the two gates, run independently

Per #23 the two gates are: **identity** (own site authoritative, third parties
corroborating) and **liveness** (own site INADMISSIBLE, dated third-party
signals REQUIRED). Both were run against the supplied data rather than adopting
it.

| Candidate | Liveness evidence | Verdict |
|---|---|---|
| Off Track Ice Cream | Yelp updated **June 2026**, 435 reviews / 625 photos, no closure marker; Tripadvisor active | **PASS** |
| Turbo Cone | Yelp updated **August 2026**, 89 reviews / 124 photos, no closure marker | **PASS** |
| Gustard's Custard | Yelp updated **June 2026**, 15 reviews, no closure marker | **PASS** (thin review count, but a real dated signal with no closure marker) |

All three clear both gates. **Zero exclusions** - the first launch in this
project's history where the whole proposed roster survives. That is worth
noting precisely because it is not the norm: best-wings lost three of five.

Category claim verified per #23 rule 5, not assumed: all three are listed under
Yelp's "Ice Cream & Frozen Yogurt" category, Turbo Cone is described by the Post
and Courier as *"Charleston's only soft-serve ice cream shop"*, and Gustard's own
site sells frozen custard. Frozen custard on an ice-cream list is an editorial
adjacency rather than a mismatch - flagging it, not blocking on it.

---

## 2. Per-restaurant findings, with provenance

### 2a. Off Track Ice Cream - `off-track-ice-cream`

Own site (`offtrackicecream.com`) confirms, and **agrees with the supplied data**
on every field it states:

| Field | Value | Source |
|---|---|---|
| `name` | `Off Track Ice Cream` | own site (styled all-caps in headers) |
| `cuisine` | `Ice Cream` | own site: *"make all of our ice cream from scratch"* |
| `neighborhood` | `Harleston Village` | supplied; 6 Beaufain St is in Harleston Village |
| `schemaType` | `IceCreamShop` | see section 3 |
| `streetAddress` | `6 Beaufain St` | own site |
| `addressLocality` / `Region` / `postalCode` / `Country` | `Charleston` / `SC` / `29401` / `US` | own site |
| `hours` | `Su-Th 12:00-22:00, Fr-Sa 12:00-23:00` | own site states Sun-Thu 12pm-10pm, Fri-Sat 12pm-11pm |
| `hoursHumanReadable` | `Sun[EN]Thu: 12pm[EN]10pm\nFri[EN]Sat: 12pm[EN]11pm` | en-dash U+2013 per tree convention |
| `websiteURL` | `https://offtrackicecream.com/` | - |
| `priceRange` | **null** | not sourced |

**`phone` is a gap.** The supplied data gives `(843) 203-6997`. **Their own site
does not state a phone number at all.** Since the own site is the authoritative
identity source and it is silent, this needs either third-party corroboration or
`phone: null`. Do not ship the supplied number unverified.

**Evidence-tier note on hours.** The hours come from the own site, which #23
marks inadmissible for liveness. Liveness itself is solidly established
independently (Yelp June 2026, 435 reviews). No third-party source contradicts
the hours. Shipping them is defensible, but it is a weaker evidence tier than
Hannibal's got on best-wings, where three independent listings agreed. Flagging
rather than silently treating it as equivalent.

### 2b. Turbo Cone - `turbo-cone`

**The supplied data is wrong in two places.** Both corrected below.

| Field | Value | Source |
|---|---|---|
| `name` | `Turbo Cone` | own site |
| `cuisine` | `Soft Serve` | own site + Post and Courier |
| `neighborhood` | `West Ashley` | supplied; 828 St Andrews Blvd is West Ashley |
| `schemaType` | `IceCreamShop` | see section 3 |
| `streetAddress` | `828 St Andrews Blvd` | own site (prints it lowercase, "828 saint andrews blvd") |
| `addressLocality` / `Region` / `postalCode` / `Country` | `Charleston` / `SC` / `29407` / `US` | own site |
| `phone` | `+1-843-900-4242` | own site |
| `websiteURL` | **`https://www.turbocone.com/`** | **CORRECTION - see below** |
| `hours` | **null** | **CONFLICT - see below** |
| `hoursHumanReadable` | DECISIONS #13.10 fallback | see below |
| `priceRange` | **null** | not sourced |

**CORRECTION 1 - the website exists.** The supplied data says *"website NOT FOUND
- search for one before shipping null"*. It was found: **`turbocone.com`**, live,
with address, phone, hours and menu. Ship the URL, not null.

**CORRECTION 2 - the hours are not "Daily 12:00-22:00".** Sources disagree:

- **Own site**: Mon-Thu 12:00-21:00, Fri-Sat 12:00-22:00, Sun 12:00-21:00
- **Third-party listing**: *"Monday - closed, Tues-Thurs 12-9, Fri-Sat 12-10, Sun 12-9"*

Two disagreements at once: whether Monday is open at all, and the supplied
"22:00" applies only to Fri-Sat. Per #13.10 this is exactly the unresolvable
case: **`hours: null`** plus the visible fallback, copying the
`tonis-detroit-style-pizza` shape from the tree with a literal em-dash U+2014:

```
Hours vary [U+2014] see turbocone.com or call (843) 900-4242 for current hours.
```

**"HurriCone" - do NOT put it in copy.** The supplied data flags it for
verification, correctly. Result: **not verified against a primary source.** The
own site names no signature item at all - it lists only *"Classic and seasonal
flavors of soft serve ice cream"* plus cones, cups, shakes and floats. The name
appears only in a TikTok caption and an aggregator blurb, and the Post and
Courier article that would settle it returned HTTP 429. Note also the spelling in
those secondary sources is **"HurriCone"** with a capital C, not "Hurricone" as
supplied - which is itself a reason to be wary of a half-sourced proper noun.
None of the proposed copy uses it, so nothing is blocked.

### 2c. Gustard's Custard - `gustards-custard`

| Field | Value | Source |
|---|---|---|
| `name` | `Gustard's Custard` | own site |
| `cuisine` | `Frozen Custard` | own site |
| `neighborhood` | **needs operator input** | see gap below |
| `schemaType` | `IceCreamShop` | see section 3 |
| `streetAddress` | `2200 Heriot St` | own site |
| `addressLocality` / `Region` / `Country` | `Charleston` / `SC` / `US` | own site |
| `postalCode` | **`29403`** | **own site is WRONG - see below** |
| `phone` | **null** | own site states none; none found |
| `websiteURL` | `https://gustards.com/` | - |
| `hours` | **null** | **three-way conflict - see below** |
| `hoursHumanReadable` | DECISIONS #13.10 fallback | see below |
| `priceRange` | **null** | not sourced |

**The ZIP claim is CONFIRMED, and this is the interesting one.** The supplied data
asserts USPS gives 29403 and that the 29412 printed on their own site is wrong.
That contradicts #23's "own site is authoritative for identity", so it was
checked rather than accepted: **Over The Horizon Brewing occupies the same street
address - 2200 Heriot St - and independent listings give it `Charleston, SC
29403`.** Two businesses at one address cannot have different ZIPs. 29412 is
James Island; Heriot St is upper-peninsula. **Ship 29403.**

Worth recording as a refinement to #23: *own site authoritative for identity*
does not mean *own site infallible on every field*. A typo'd ZIP contradicted by
an independent business at the identical street address is a factual error, not
an identity choice. The rule holds for what a business calls itself; it does not
override arithmetic or geography.

**Hours are a genuine three-way conflict.** Confirmed, as the supplied data
warned:

- **Own site**: Tue-Sun 12:00-22:00, Mon closed
- **Third-party listing**: Tue-Thu 16:00-22:00, Fri-Sun 11:00-22:00
- Supplied data reports Yelp and Google giving further variants

Unresolvable. **`hours: null`** plus the #13.10 fallback. Note the shape must
drop the phone clause, since there is no phone to point at:

```
Hours vary [U+2014] see gustards.com for current hours.
```

**`neighborhood` is a gap.** Not supplied and not stated on the own site. 2200
Heriot St sits in the upper-peninsula industrial strip near Over The Horizon
Brewing; plausible labels are "Charleston Neck" or "Upper Peninsula", but neither
has precedent in `restaurants.json` and neither is sourced. **Operator call, or
ship `null`** - it is nullable, and the OG meta-line and hero subtitle both
degrade cleanly (`compose_detail_meta` handles a null neighborhood).

Grounded editorial facts available: opened **August 2024** (Charleston City
Paper, 2024-08-27), owner Nelson Burch, named after his dog Gus, dog-friendly
with "pooch scoops".

---

## 3. schemaType: `IceCreamShop` is sanctioned

**Verified against the tree, and the answer is yes - but not for the reason the
prompt implies.**

Both docblocks carry an *enumerated* list that does not include `IceCreamShop`:

- `rankings/_template-canonical.html`: `CafeOrCoffeeShop` / `BarOrPub` /
  `NightClub` / `Bakery`
- `rankings/_detail-page-template.html` `{{SchemaType}}`: the same four

But those lists are **illustrative, not closed** - the canonical's entries read
"(future bar page)", "(future club page)", "(future bakery page)", i.e. they are
forward-looking examples rather than an allowlist. The operative rule is the
detail template's intentional decision #4:

> "Default is `Restaurant`; **override to the most-specific applicable subclass of
> FoodEstablishment when accurate.**"

`IceCreamShop` is a real schema.org type and a direct subclass of
`FoodEstablishment`, so it satisfies the rule. **Sanctioned. It would be a first
use in this dataset** (current spread: 28 `Restaurant`, 5 `CafeOrCoffeeShop`, 2
`FoodEstablishment`, 1 `Bakery`, and `BarOrPub` still unused after Tru Blues was
held).

Follow-up worth filing: both docblocks' enumerated lists should gain
`IceCreamShop` when this ships, so the next reader does not have to re-derive
that the list is open. Same class of doc-accuracy fix as the `49 -> 56` page
count in PR #41.

---

## 4. Slug and social-card checks

All verified against the tree:

| Check | Result |
|---|---|
| `off-track-ice-cream` slug/name collision | none |
| `turbo-cone` slug/name collision | none |
| `gustards-custard` slug/name collision | none (apostrophe dropped per `dallesandros-pizza` convention) |
| `best-ice-cream` already in `og_rankings.json` | no |
| `rankings/best-ice-cream.html` exists | no |
| Social card title derivation | `best-ice-cream` -> **"Best Ice Cream"** - clean, no hyphen loss (contrast `best-tex-mex` -> "Best Tex Mex") |

**Cuisine-dedup auto-detect**, run through `scripts/_cuisine_dedup.py` rather
than predicted by eye:

| Entry | cuisine | Auto-detect |
|---|---|---|
| Off Track Ice Cream | `Ice Cream` | **SUPPRESSED** in display surfaces - "ice cream" is a substring of the name |
| Turbo Cone | `Soft Serve` | rendered |
| Gustard's Custard | `Frozen Custard` | rendered |

Off Track's suppression is DECISIONS #18 working as designed: its detail title
becomes "Off Track Ice Cream in Charleston | Voted On By Locals" and its hero
subtitle drops to the neighborhood alone. **Do not add a `displayCuisine`
override to defeat it.** `servesCuisine` keeps the raw value.

---

## 5. Drafted page content - DRAFT ONLY

### 5a. Head meta

```
<title>Best Ice Cream in Charleston, SC | Locals Guide (2026)</title>

<meta name="description" content="Discover the best ice cream in Charleston, SC.
From scratch-made scoops to soft serve and frozen custard, explore the top spots
voted on by the local community.">

<meta name="keywords" content="best ice cream Charleston SC, Charleston ice cream
rankings, soft serve Charleston, frozen custard Charleston, local favorites
Charleston">

<link rel="canonical" href="https://votedonbylocals.com/rankings/best-ice-cream.html">

<meta property="og:title"       content="Best Ice Cream in Charleston | Voted On By Locals">
<meta property="og:description" content="Charleston's best ice cream, voted by the local community.">
<meta property="og:type"        content="website">
<meta property="og:url"         content="https://votedonbylocals.com/rankings/best-ice-cream.html">
<meta property="og:image"       content="https://votedonbylocals.com/assets/images/og-best-ice-cream.png">
<meta property="og:site_name"   content="Voted On By Locals">

<meta name="twitter:card"        content="summary_large_image">
<meta name="twitter:title"       content="Best Ice Cream in Charleston | Voted On By Locals">
<meta name="twitter:description" content="Charleston's best ice cream, voted by the local community.">
<meta name="twitter:image"       content="https://votedonbylocals.com/assets/images/og-best-ice-cream.png">
```

The description's three descriptors are each grounded in a specific roster entry
(scratch-made = Off Track's own copy; soft serve = Turbo Cone; frozen custard =
Gustard's), so it survives any single-entry change without becoming false.

### 5b. Hero, subtitle, pill

```html
<h1 class="text-4xl sm:text-6xl font-extrabold font-poppins text-brand-dark leading-tight">
    Best <span class="text-brand-orange">Ice Cream</span> [U+1F366]
</h1>

<p class="text-brand-gray mt-4 text-lg font-medium">As voted by Charleston locals. Three standouts [U+2014] with more to come.</p>

<div class="inline-block bg-white px-3 py-1 rounded-full text-xs text-gray-400 border border-gray-100 mt-2 shadow-sm">
    Updated August 2026
</div>
```

**Emoji: U+1F366 SOFT ICE CREAM**, `aria-label="soft ice cream"`. The cone form is
the iconic "ice cream" glyph and covers all three shapes on this list (scoops,
soft serve, custard). Alternate considered: U+1F368 ICE CREAM (bowl with spoon),
rejected as less recognisable at card size. aria-label uses the Unicode name,
matching the tree's convention (`poultry leg`, `tropical drink`).

**Subtitle carries Top-3 count framing** per #23's ranking-length section - the
exact string that section prescribes.

### 5c. Taglines - two grounded, one flagged

| Rank | Restaurant | Proposed | Assessment |
|---|---|---|---|
| 1 | Off Track Ice Cream | `Scratch-Made Scoops, Vegan Too` | **GROUNDED** - own site: *"make all of our ice cream from scratch"* and a described vegan base (raw cashews, coconut cream) |
| 2 | Turbo Cone | `West Ashley Soft Serve, Piled High` | **PARTLY GROUNDED - flagged** |
| 3 | Gustard's Custard | `Frozen Custard, Dogs Welcome` | **GROUNDED** - own site: *"Dogs welcome"*, *"The dog gets a scoop too"* |

**Flag on rank 2.** "West Ashley" and "Soft Serve" are both solid - the address is
West Ashley and the Post and Courier calls it Charleston's only soft-serve shop.
**"Piled High" is not sourced.** Nothing on the own site or in any source
describes portion size or presentation. It is a plausible flourish, but it
asserts a visual characteristic no source supports. Grounded alternatives, all
from the own site or P&C:

- `West Ashley Soft Serve, Nothing Else` (P&C: the *only* soft-serve shop)
- `Charleston's Only Soft-Serve Shop`
- `West Ashley Soft Serve, Cones and Shakes` (own site menu)

Operator call. Not blocking - it is editorial voice, and per WORKFLOW.md's
self-correction norm tone and copy are operator territory.

### 5d. ItemList JSON-LD

Field order copied from the production shape (`@context, @type, name,
description, datePublished, dateModified, url, itemListElement`).
**ItemList block MUST precede BreadcrumbList** - per #23, `generate_sitemap.py`
parses only the first `ld+json` block and `<lastmod>` vanishes silently
otherwise.

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Best Ice Cream in Charleston, SC",
  "description": "<same string as meta description>",
  "datePublished": "2026-08-25T12:00:00-04:00",
  "dateModified": "2026-08-25T12:00:00-04:00",
  "url": "https://votedonbylocals.com/rankings/best-ice-cream.html",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "item": {
        "@type": "IceCreamShop", "name": "Off Track Ice Cream",
        "url": "https://votedonbylocals.com/restaurants/off-track-ice-cream.html",
        "servesCuisine": "Ice Cream",
        "address": { "@type": "PostalAddress", "addressLocality": "Charleston", "addressRegion": "SC" } } },
    { "@type": "ListItem", "position": 2, "item": {
        "@type": "IceCreamShop", "name": "Turbo Cone",
        "url": "https://votedonbylocals.com/restaurants/turbo-cone.html",
        "servesCuisine": "Soft Serve",
        "address": { "@type": "PostalAddress", "addressLocality": "Charleston", "addressRegion": "SC" } } },
    { "@type": "ListItem", "position": 3, "item": {
        "@type": "IceCreamShop", "name": "Gustard's Custard",
        "url": "https://votedonbylocals.com/restaurants/gustards-custard.html",
        "servesCuisine": "Frozen Custard",
        "address": { "@type": "PostalAddress", "addressLocality": "Charleston", "addressRegion": "SC" } } }
  ]
}
```

All three `addressLocality` values are the literal municipality **Charleston**
per #15 Q5 - Harleston Village, West Ashley and the upper peninsula are all
within the City of Charleston, so no rollup is involved.

**`servesCuisine` proposals, flagged not decided** per #23:

| Entry | `restaurants.json.cuisine` | ItemList `servesCuisine` | Rule applied |
|---|---|---|---|
| Off Track Ice Cream | `Ice Cream` | `Ice Cream` | preserve the specific |
| Turbo Cone | `Soft Serve` | `Soft Serve` | preserve the specific |
| Gustard's Custard | `Frozen Custard` | `Frozen Custard` | preserve the specific |

Note this list has **no generic-override case at all** - unlike best-wings, where
Moe's `American` had to become `Wings`. All three cuisines here are already
specific, so #23's "override the generic, preserve the specific" resolves to
preserve across the board. That makes it the least contentious `servesCuisine`
set the project has had, and it is worth saying so in the PR body rather than
leaving reviewers to wonder why nothing was overridden.

### 5e. BreadcrumbList, rows, CTA

BreadcrumbList second: Home / Rankings (`/#rankings`) / Best Ice Cream.

Row markup is the standard block, three times, with the page emoji reused and
each name wrapped in the anchor the social pipeline's regex requires:

```html
<h2 class="font-poppins font-bold text-xl sm:text-2xl text-brand-dark mb-1 leading-snug"><a href="/restaurants/{slug}.html" class="hover:text-brand-orange transition-colors">{Name}</a></h2>
<p class="text-brand-gray font-medium text-sm sm:text-base">{Tagline}</p>
```

CTA copy canonical per #7: "Disagree with this list? Cast your vote!" with the
button reading `Vote for Best Ice Cream`.

---

## 6. The five registry edits

| # | File | Edit |
|---|---|---|
| 1 | `components/header.html` | desktop dropdown, appended to the end of the Top-N cluster below the divider |
| 2 | `components/header.html` | mobile menu, same position |
| 3 | `index.html` | homepage grid card - see section 7 |
| 4 | `vote.html` | `<option>Best Ice Cream</option>` appended at end |
| 5 | `data/og_rankings.json` | `{slug: "best-ice-cream", category: "Ice Cream", spots: 3}` + bump `_meta.lastUpdated` |

**No NEW pill** - #23 is explicit that the pill is featured-1 launch ceremony
only, and Top-N launches inherit dropdown discoverability. Verified in the tree:
`components/header.html` still contains exactly one NEW-pill artifact set, all
belonging to `best-bakery`.

`spots: 3` - not 1, so the social pipeline stays on the Top-N path.

---

## 7. STEP 4: 12 cards resolves the orphan at both breakpoints

**Verified against the current file, and the answer is yes.** `index.html`
currently holds **11** cards; the grid is unchanged from best-wings.

| Cards | base (1 col) | md (2 cols) | lg (4 cols) |
|---|---|---|---|
| 11 (today) | 11 rows, clean | 6 rows, **last row 1 - ORPHAN** | 3 rows, last row 3 of 4 |
| **12 (after this launch)** | 12 rows, clean | **6 rows of 2 - clean** | **3 rows of 4 - clean** |

Adding the 12th card **resolves the md orphan flagged in the best-wings
analysis, and simultaneously fills the lg row.** 12 is the first count since 8
that divides evenly by both 2 and 4.

**`index.html` needs no `grid-cols` change.** Leave the class exactly as it is.

Correction to the prompt: the grid line is at **`index.html:166`**, not L164. The
prompt's L164 is carried over from the best-wings analysis and is now stale.

---

## 8. Blast radius

Three net-new restaurants, so this is a heavier launch than best-wings (one).

| Step | Files |
|---|---|
| `rankings/best-ice-cream.html` | 1 new |
| `data/restaurants.json` | 1 modified (3 new entries, no `appearsOn` appends - none are cross-listed) |
| `data/og_rankings.json` | 1 modified |
| `restaurants/{3 slugs}.html` | 3 new, generated |
| `components/header.html` | 1 modified |
| `index.html`, `vote.html` | 2 modified |
| `_strategy/TRACKED.md` | 1 modified - Park Circle trigger, see section 10 |
| `sitemap.xml` | 1 regenerated |
| `assets/images/og-best-ice-cream.png` + 3 detail PNGs | 4 new |
| `inline_chrome.py --refresh` | **60 files** (56 today + 1 ranking + 3 detail) |

**No `dateModified` hand-bumps needed** - none of the three is an existing entry,
so nothing gains an `appearsOn` row. That removes the trap that bit PR #34 and
required PR #36.

**Ordering still matters**: the new pages must exist before `--refresh`, and
`generate_sitemap.py` runs last. `npm run build:css` only if a class-set diff
shows new utilities - copying an existing page introduces none.

---

## 9. Where this prompt and the recipe disagree

Reported per the instruction, in descending order of consequence.

1. **Roster size undershoots the recipe.** #23 section 0 says **"start with
   roughly twice your target N"** and calls the sourcing pass "where the launch
   actually gets decided". This prompt supplies exactly **3 candidates for a
   Top-3 - 1x N, zero bench.** It happened to work because all three passed, but
   that was luck, not method: best-wings lost three of five and needed a
   substitute. Had one failed here, the launch would have silently become a
   Top-2. Not a blocker this time; worth correcting next time.

2. **Turbo Cone's website exists.** Prompt says NOT FOUND; `turbocone.com` is
   live. Ship the URL.

3. **Turbo Cone's hours are wrong as supplied.** "Daily 12:00-22:00" matches no
   source. Own site gives Mon-Thu and Sun to 21:00 with only Fri-Sat to 22:00; a
   third party says Monday is closed entirely. Resolves to `null` + #13.10
   fallback.

4. **Off Track's phone is unsourced.** Supplied as `(843) 203-6997`; the own
   site - the authoritative identity source - states no phone at all.

5. **"Hurricone" is both unverified and misspelled in the prompt.** Secondary
   sources spell it "HurriCone"; no primary source reachable. Keep it out of
   copy.

6. **`index.html` grid line is 166, not 164.**

7. **The prompt asserts `IceCreamShop` "is a valid schema.org FoodEstablishment
   subtype"** as a premise. True, and it does check out - but the thing that
   actually sanctions it is intentional decision #4's *rule*, not the enumerated
   lists, which do not contain it. Worth stating precisely so the next reader
   does not conclude the lists are an allowlist.

8. **Gustard's ZIP: the prompt is right and #23 needs a footnote.** The prompt
   overrides the own site, which #23 calls authoritative for identity.
   Independently confirmed via a co-located business. The recipe's rule should be
   read as *authoritative for what a business calls itself*, not *infallible on
   every field*.

---

## 10. TRACKED entries this launch generates

To file in the launch PR per #22 (same-PR file edit, not PR prose).

> **Off Track Ice Cream Park Circle second location - opening undetermined,
> secondary excluded from `locations[]`.** A second location at 1054 E Montague
> Ave, Park Circle (North Charleston), in the former Pink Crocodile space, was
> announced in November 2025 by owners Marc and Alissa Zera, targeting a summer
> 2026 opening. As of 2026-08-25 **no source confirms it has opened** - Post and
> Courier, What Now Charleston, Holy City Sinner and chshappenings all describe
> it in future tense, and **the restaurant's own site does not mention a second
> location at all**, which is itself a signal. Per DECISIONS #17 a multi-location
> entry needs `locations[]`; per #23's conflict rule an undetermined status is
> excluded rather than guessed. `off-track-ice-cream` therefore ships
> single-location. Trigger: a dated confirmation that the Park Circle shop is
> open - a "now open" announcement, a dated review, or a directory listing. On
> confirmation, add the secondary to `locations[]` and regenerate the detail
> page. Filed by the best-ice-cream launch.

> **`IceCreamShop` missing from the schemaType lists in both template
> docblocks.** `rankings/_template-canonical.html` and
> `rankings/_detail-page-template.html` both enumerate `CafeOrCoffeeShop` /
> `BarOrPub` / `NightClub` / `Bakery` as the subclass options. Those lists are
> illustrative rather than exhaustive - the operative rule is detail-template
> intentional decision #4, "the most-specific applicable subclass of
> FoodEstablishment when accurate" - but a reader can easily mistake them for an
> allowlist. `IceCreamShop` ships with best-ice-cream and should be added to
> both, ideally alongside a note that the list is open. Documentation-accuracy
> only, no behaviour change. Same class as the `49 -> 56` page-count fix in PR
> #41. Filed by the best-ice-cream launch.

---

## 11. Resolutions (operator, 2026-08-25)

All five open questions are closed. Recorded here rather than only in the PR,
so the file stays the durable record of the launch.

| # | Question | Resolution |
|---|---|---|
| 1 | Off Track phone | **`null`** - not on the own site, and Apple/Yelp are not the identity anchor |
| 2 | Gustard's neighborhood | **`null`** - no settled name for the upper-peninsula strip |
| 3 | Turbo Cone tagline | **`Retro Soft Serve, West Ashley`** |
| 4 | Hero emoji | **U+1F366**, `aria-label="soft ice cream"` |
| 5 | Homepage card hook | **`Scoops, soft serve, and frozen custard.`** + page emoji |

Plus the three carried from section 2, unchanged:

- **Turbo Cone `websiteURL`** = `https://www.turbocone.com/` - the supplied "NOT FOUND" was wrong.
- **Turbo Cone `hours`** = `null` + #13.10 fallback, **phone clause retained** (they have a phone).
- **Gustard's `hours`** = `null` + #13.10 fallback, **phone clause dropped** (no phone to point at).
- **Gustard's `postalCode`** = `29403`, overriding the own site's 29412.
- **Park Circle** excluded; `off-track-ice-cream` ships single-location with a re-verification trigger.

### Null-neighborhood precedent, verified before relying on it

Three entries already carry `neighborhood: null`. Checked rather than assumed,
because two of the three are a different case:

| Entry | schemaType | areaServed | Case |
|---|---|---|---|
| `dough-boyz` | FoodEstablishment | "Greater Charleston (mobile/pop-up)" | mobile vendor |
| `pubfare-burger` | FoodEstablishment | "Greater Charleston, SC" | mobile vendor |
| **`tonis-detroit-style-pizza`** | **Restaurant** | **null** | **fixed address, simply no neighborhood label** |

`tonis` is the precedent that matters: a fixed-address `Restaurant` with a null
neighborhood and no `areaServed`. Gustard's is exactly that shape, so this is a
precedented state rather than a novel one.

Render path verified in `scripts/generate_og_images.py`:
`compose_detail_meta(display_cuisine, neighborhood)` branches on a falsy
neighborhood and returns `display_cuisine` alone. Gustard's cuisine is not
suppressed by the dedup, so its OG meta-line reads **"Frozen Custard"** with no
trailing separator. `tonis` demonstrates the same path live today.

### Note on the Turbo Cone tagline

`Retro Soft Serve, West Ashley` is an **operator editorial decision**. "Soft
Serve" and "West Ashley" are both sourced (own site menu; the address). "Retro"
is a voice choice not present in any source I read - recording that plainly, not
as an objection. Per WORKFLOW.md's self-correction norm, tone and copy are
operator territory. It notably avoids the unverified "HurriCone", which was the
actual risk in this entry.

## Encoding note

Non-ASCII intentionally referenced by codepoint rather than glyph in this file,
to survive console round-tripping:

- **U+1F366** SOFT ICE CREAM - proposed hero/row emoji
- **U+2014** EM DASH - required in the subtitle count framing and in the #13.10
  hours fallback strings. Copy the fallback shape from
  `tonis-detroit-style-pizza` in `data/restaurants.json`, not from this file.
- **U+2013** EN DASH - `hoursHumanReadable` day and time ranges, marked `[EN]`
  above. Shape precedent: `park-pizza-co`.
