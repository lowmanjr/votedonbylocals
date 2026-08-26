# Best Ramen launch - analysis working file

Analysis-only working file for the `best-ramen` Top-2 launch. Author: Claude
session 2026-08-26, branch `best-ramen-launch`, off `main` @ `51d8de9`
(verified clean and level with `origin/main`, 0 ahead / 0 behind).

**Status: applied, across two PRs.** Section 11 records the operator resolutions
and the split.

- **PR 1** - `bar-weems-data-correction`, **merged as #46** (`9ed4149`). Bar Weems
  neighborhood, cuisine, stale hours and the prose cascade.
- **PR 2** - `best-ramen-launch`, this launch, branched off `9ed4149` so the
  regen could not re-bake the corrected fields.

Where a drafted section was superseded by what actually shipped, the section
says so inline rather than being rewritten - the draft is the record of the
reasoning, section 11 is the record of the decision.

Location per `_strategy/WORKFLOW.md`: underscore-prefixed, in the directory of
the work it supports (`rankings/`), not `_strategy/`. Same as
`_best-wings-launch-analysis.md` and `_best-ice-cream-launch-analysis.md`.

Recipe followed: **DECISIONS #23, "Top-N launch recipe (formalized)"**, read from
the tree rather than from the prompt. Section 10 lists every place the prompt
and the recipe/tree disagree.

---

## 0. The finding that reframes this launch

**`bar-weems` is already in the tree.** The prompt presents both restaurants as
output of an external sourcing pass. Half of it is not:

| Artifact | State |
|---|---|
| `data/restaurants.json` -> `bar-weems` | **exists**, added 2026-05-03 (workstream H bulk port) |
| `restaurants/bar-weems.html` | **exists**, live, `dateModified` 2026-05-03T19:03:39-04:00 |
| `rankings/best-new-restaurants.html` | **row 2**, with ItemList entry and body row |
| `assets/images/og-restaurant-bar-weems.png` | exists |

Consequences that change the shape of the whole launch:

1. Bar Weems is an **`appearsOn` append + regen + `dateModified` hand-bump**,
   not a new entry. That is the exact trap #23 step 5 warns about and the one
   that forced PR #36 after PR #34.
2. **#23 rule 4 applies**: "the gate applies to pre-existing entries too ... the
   bump is an assertion of freshness." Both gates were therefore run against
   Bar Weems as rigorously as against the net-new candidate.
3. Three fields the prompt treats as open questions are in fact **populated
   values already shipped on a live page** - `neighborhood`, `addressLocality`,
   and `hours`. Two of the three turn out to be wrong. See sections 2a and 10.
4. Only **one** net-new restaurant (`hachiya-ramen`) and **one** net-new detail
   page result from this launch.

---

## 1. Roster verification - the two gates, run independently

Per #23 the gates are **identity** (own site authoritative, third parties
corroborating) and **liveness** (own site INADMISSIBLE, dated third-party
signals REQUIRED). Both were run against the supplied data rather than adopting
it.

| Candidate | Liveness evidence (third-party, dated) | Verdict |
|---|---|---|
| Bar Weems | Yelp **updated Aug 2026**, 82 photos / 22 reviews, no closure marker; Charleston Magazine feature **July 2026**; Apple Maps listing active with full hours | **PASS** |
| Hachiya Ramen | Yelp **updated Aug 2026**, 109 photos / 99 reviews, no closure marker; P&C Charleston's Choice **Best Ramen 2025** winner listing | **PASS** |

**Zero exclusions from the supplied roster.** Second launch running to make that
claim (best-ice-cream was the first) - still not the norm; best-wings lost three
of five.

**Category claim verified per #23 rule 5, not assumed.** Both are ramen shops by
primary categorisation, not adjacencies:

- Bar Weems - Yelp's sole category is **"Ramen"**. Own site's descriptor line is
  "house made noodles". P&C ran it as "Bar Weems ramen opens in North Charleston".
- Hachiya Ramen - Yelp category **"Ramen"**; won **Post and Courier Charleston's
  Choice "Best Ramen" 2025**; own site menu lists Tonkotsu Ramen, Tonkotsu
  Tantamen and a vegetarian bowl.

This is the cleanest category fit the project has had. Contrast best-ice-cream,
where frozen custard had to be flagged as an editorial adjacency.

**One editorial observation, offered not as a reorder request.** The strongest
external "best ramen" credential in Charleston - P&C's Charleston's Choice Best
Ramen 2025 - belongs to **rank 2**, not rank 1. Rank order is operator-confirmed
and is not touched here. Flagging only because a reviewer who knows the P&C award
will notice, and the PR body is a better place to pre-empt that than the comments.

---

## 2. Per-restaurant findings, with provenance

### 2a. Bar Weems - `bar-weems` (PRE-EXISTING, cross-listing)

Own site (`barweems.com`, fetched 2026-08-26) confirms identity. Table shows
**current tree value -> verified value**:

| Field | Tree today | Verified | Source |
|---|---|---|---|
| `name` | `Bar Weems` | unchanged | own site |
| `schemaType` | `Restaurant` | unchanged - see section 3 | - |
| `streetAddress` | `1921 Reynolds Ave` | unchanged | own site: "1921 REYNOLDS AVENUE" |
| `addressLocality` | `North Charleston` | **unchanged - CONFIRMED** | own site, Yelp, Apple Maps, Charleston Mag, P&C |
| `addressRegion` / `postalCode` / `Country` | `SC` / `29405` / `US` | unchanged | own site |
| `phone` | `+1-854-202-1175` | unchanged | own site: "854-202-1175" |
| `websiteURL` | `https://barweems.com` | unchanged | tree convention drops `www` + trailing slash |
| `hours` | `We-Sa 17:00-01:00` | **`Tu-Sa 17:00-01:00` - CORRECTION** | see below |
| `hoursHumanReadable` | `Wed[EN]Sat: 5pm[EN]1am\nSun[EN]Tue: Closed` | **`Tue[EN]Sat: 5pm[EN]1am\nSun[EN]Mon: Closed`** | see below |
| `neighborhood` | `Park Circle` | **WRONG - see below** | P&C |
| `cuisine` | `Japanese` | **open TRACKED item fires - see below** | - |
| `monthYear` | `May 2026` | **`August 2026`** | launch convention (6 entries already carry it) |
| `priceRange` | `$$` | unchanged | not re-sourced; no contradicting signal |

**HOURS - RESOLVED, and the prompt's premise does not survive contact.**

The prompt describes "four sets" and pre-authorises `null` + the #13.10 fallback.
There are **two** distinct claims, and they resolve 4-to-1:

| Source | Claim | Tier |
|---|---|---|
| **Own site**, fetched 2026-08-26 | "SUNDAY & MONDAY CLOSED", "TUESDAY - SATURDAY 5PM - 1AM" | identity-authoritative, liveness-inadmissible |
| **Yelp**, updated Aug 2026 | Tue 5:00pm-1:00am, Wed 5:00pm-1:00am | dated third-party |
| **Apple Maps** | "Sun - Mon: Closed", "Tue - Sat: 5:00PM - 1:00AM" | third-party |
| Aggregated day-grid | Mon closed, Tue-Sat 5:00pm-1:00am, Sun closed | third-party |
| **Charleston Magazine**, July 2026 | "Wednesday-Saturday, 5 p.m.-1 a.m." | dated third-party, **outlier** |

The disagreement is **exactly one day - whether Tuesday is open** - and everything
except one monthly print title says it is. Charleston Magazine is the outlier and
carries the longest editorial lead time of the five.

**#13.10 does not fire.** Its trigger is *unresolvable* conflict; this is a
resolved one with a single stale dissenter. Writing `null` here would discard
four converging sources in deference to the weakest one, and would *remove* live
data from a shipped page. The prompt's instruction was explicitly conditional
("If unresolvable, null + the #13.10 fallback") - the condition fails, so the
fallback and its phone clause are moot.

Note the tree's current `We-Sa` matches Charleston Magazine, i.e. **the tree is
one day stale**, not merely un-updated. Correcting it is the honest bump.

**NEIGHBORHOOD - the tree ships a factual error.**

The prompt calls this "unresolved". It is worse: `neighborhood: "Park Circle"` is
populated, live, and **wrong**, and the error has cascaded into three prose
fields.

Post and Courier, twice and unambiguously:

> "Reynolds Avenue is in the **Chicora Cherokee neighborhood**"

> "A left turn leads toward bustling **Park Circle** ... Heading **right** will
> take you to the **Reynolds Avenue restaurant corridor**."

Reynolds Ave is never described as part of Park Circle in any source read; it is
consistently presented as the *adjacent* corridor, with Park Circle's commercial
core on East Montague Ave. The prompt's own framing ("Park Circle spillover but
is not Park Circle proper") matches the sources - it just did not know the tree
had already committed to the wrong side of that line.

Contaminated fields, all currently asserting Park Circle:

```
neighborhood  : "Park Circle"
description   : "Bar Weems is a Park Circle Japanese restaurant in North Charleston, SC, ..."
shareTagline  : "Handmade ramen and cocktails in Park Circle, voted best by Charleston locals."
keywords      : "Bar Weems Charleston, Park Circle ramen, North Charleston Japanese, ..."
```

Three options, **operator call**:

- **(A) Correct to `Chicora-Cherokee` + cascade.** Sourced. Follows the **Tutti
  precedent** (DECISIONS #18): prose fields that "explicitly contradicted the
  factual correction" were rewritten *in the same PR* because that is "hard
  inconsistency rather than benign redundancy." A wrong neighborhood is hard
  inconsistency. **Recommended.** Note P&C renders it unhyphenated ("Chicora
  Cherokee"); the City of North Charleston's own name for the district is
  hyphenated. No precedent in `restaurants.json` either way.
- **(B) `null` + cascade.** The `tonis-detroit-style-pizza` precedent - a
  fixed-address `Restaurant` with null `neighborhood` and no `areaServed`,
  verified live in the tree. Renderer handles it: `compose_detail_meta` branches
  on falsy neighborhood, and `generate_detail_page.py` drops the subtitle `<p>`
  entirely when cuisine and neighborhood both resolve empty. Safe, but discards
  a sourced fact.
- **(C) Leave it.** Not viable. It is now known-wrong, and this PR bumps
  `dateModified` on that page - #23 rule 4's "asserting freshness about
  [something false] is worse than saying nothing."

Either (A) or (B) requires the same prose cascade, so the cascade is not a
tiebreaker. **(A)** is recommended.

**CUISINE - this launch fires an open TRACKED trigger.**

`_strategy/TRACKED.md`, "Cuisine specificity editorial review (3 borderline
cases)":

> "Bar Weems (cuisine "Japanese" -> could refine to "Ramen" per their own "noodle
> house" framing + Yelp's "Ramen" categorization). **Trigger: editorial review
> pass when next editing these entries.**"

A best-**ramen** launch editing this entry is that trigger, as directly as it
gets. Refining `cuisine` to `Ramen`:

- Detail `<title>` moves from "Bar Weems [EM] Japanese in Charleston" to
  "Bar Weems [EM] Ramen in Charleston" (not suppressed - see section 4).
- OG meta-line and hero subtitle follow.
- `servesCuisine` on the **detail** page follows raw `cuisine` per #18.5.
- `servesCuisine` on **best-new-restaurants**' ItemList does **not** have to
  follow: #23 makes ranking-page `servesCuisine` hand-authored and list-scoped,
  explicitly "NOT a copy of `restaurants.json.cuisine`", and says of the two
  rules "Do not unify them." Leaving `Japanese` there is legitimate.
- `description` / `keywords` say "Japanese restaurant" / "North Charleston
  Japanese" - same cascade as the neighborhood fix, so they merge into one edit.

Recommended, and it retires a TRACKED item. **Operator call** - it is an
editorial-specificity change, and the TRACKED entry itself frames it that way.

**Grounded editorial facts available.** Opened **December 2025** at 1921 Reynolds
Ave (Charleston Mag: "landed there in early December"). Owner **Weems Pennington**,
self-taught, ~5 years of pop-ups including Estadio and Sweatman's Garden. Noodles
"made by hand each day"; What Now Charleston calls it one of the few ramen
operations making noodles in house. Craft cocktail program with named drinks
(Everynight Fireworks, You'd Prefer an Astronaut). Late-nite menu 10pm-12:30am.

### 2b. Hachiya Ramen - `hachiya-ramen` (NET-NEW)

Own site (`hachiya-ramen.com`, fetched 2026-08-26) **agrees with the supplied
data on every field it states**. This is the cleanest sourcing input the project
has received.

| Field | Value | Source |
|---|---|---|
| `name` | `Hachiya Ramen` | own site - **and the prompt's disambiguation is correct**, see below |
| `cuisine` | `Ramen` | own site + Yelp category + P&C award category |
| `neighborhood` | **null** | not stated; see below |
| `schemaType` | `Restaurant` | see section 3 |
| `streetAddress` | `996 Johnnie Dodds Blvd, Ste 101` | own site: "996 Johnnie Dodds Boulevard, Suite #101" |
| `addressLocality` | `Mount Pleasant` | own site, P&C, Yelp - literal municipality per #14.2 / #15 Q5 |
| `addressRegion` / `postalCode` / `Country` | `SC` / `29464` / `US` | own site |
| `phone` | `+1-843-708-0774` | own site: "(843) 708-0774" |
| `websiteURL` | `https://hachiya-ramen.com/` | own site |
| `hours` | `Tu-Su 11:30-20:30` | own site: "Sun, Tue, Wed, Thur, Fri, Sat: 11:30 AM - 8:30 PM"; Monday absent |
| `hoursHumanReadable` | `Tue[EN]Sun: 11:30am[EN]8:30pm\nMon: Closed` | derived; en-dash U+2013 per tree convention |
| `priceRange` | **null** | not sourced |
| `locations[]` | **single-location** | see Clements Ferry determination |

**Hours confirmed on all three sources the prompt cites** - own site, Yelp and
the P&C listing all give 11:30-20:30 with Monday closed. No conflict. Ship them.

**NAME - the prompt's instruction is right, and here is the proof.** "Hachiya"
alone collides with **Hachiya Kyoto Steakhouse and Sushi Bar, 688 Citadel Haven
Dr, Charleston, SC 29414** (West Ashley Town Center) - a hibachi/sushi house,
formerly Miyabi Kyoto, phone (843) 571-6025. Genuinely a different restaurant,
though not an unrelated one: Hachiya Ramen's co-owner **Yuichiro "Junior"
Takebata** was "the chef at West Ashley's Hachiya Kyoto Steakhouse and Sushi Bar"
(P&C), and What Now Charleston framed the ramen shop as Hachiya Kyoto expanding.
Sister restaurants, distinct entities, distinct entries. **Use "Hachiya Ramen".**

**Co-owners confirmed: Richard Milana and Yuichiro "Junior" Takebata** (P&C,
2024-09-23). The prompt's "Yuichiro Takebata" is correct; "Junior" is the
by-name he is quoted under.

**Opened confirmed: Tuesday, September 17, 2024.** P&C's "Now Open" piece ran
2024-09-23.

**`neighborhood` is a gap - recommend `null`.** 996 Johnnie Dodds Blvd is the
main commercial artery through Mount Pleasant; the own site uses only "Mt
Pleasant". No sub-neighborhood label is stated anywhere. This is precisely the
`tonis-detroit-style-pizza` case as resolved on 2026-05-05: *"commercial-corridor
addresses lacking a clear sub-neighborhood identity are valid null cases - the
renderer no longer produces empty `<p>` artifacts."* Toni's is itself on Hwy 17
in Mount Pleasant. Same street, same resolution. **`null`, on precedent, not as
a shrug.**

**Service model, recorded because it bears on section 3.** P&C: "Tall touch
screens are perched where a host stand would normally be" - kiosk ordering, food
run to the table. P&C's headline framing is "Speed and quality take center stage."
Fast-casual, not fast food.

**Broth.** Own site: "slow-cooked broths, fresh noodles, and balanced flavors."
P&C on the tonkotsu: "a meaty liquid", "cloudy", "filled with intensity but void
of excess fat." **Three ramen types, one vegetarian.** No source ranks them or
names a signature - this matters for the tagline, section 6c.

---

## 3. schemaType - reported as reasoning, not defaulted

The prompt asks for "the most-specific applicable FoodEstablishment subclass."
**That phrasing does not adjudicate the Bar Weems question, and it is worth
saying why before answering it.**

`Restaurant` and `BarOrPub` are **sibling** direct subclasses of
`FoodEstablishment`. Neither is more specific than the other. The operative rule
- detail-template intentional decision #4, "override to the most-specific
applicable subclass of FoodEstablishment **when accurate**" - resolves ties on
*accuracy*, and specificity only orders a chain (e.g. `IceCreamShop` over
`FoodEstablishment`, as best-ice-cream established). So the real question is
which type is true, not which is deeper.

### Bar Weems -> `Restaurant` (no change)

| For `BarOrPub` | For `Restaurant` |
|---|---|
| The name begins with "Bar" | Own site's own descriptor line is "house made noodles" |
| 5pm-1am hours, late-nite menu 10pm-12:30am | Yelp's **sole** category is "Ramen" - not Bars, not Cocktail Bars |
| Named craft-cocktail program; applied for beer/wine/liquor permit | P&C ran it under food / "Now Open" as a ramen restaurant |
| | What Now Charleston "emphasizes ... housemade noodles as defining features **rather than positioning it as a bar-focused venue**" |
| | It is being listed on a **ramen** ranking; `BarOrPub` on that ItemList would misdescribe the claim being made |
| | The tree already ships `Restaurant` on a live detail page and a live ItemList |

**Verdict: keep `Restaurant`.** `BarOrPub` is defensible but weaker on every
source that is not the signage. A restaurant with a serious bar program is still
a restaurant; the name is branding, not a schema classification. Changing it
would also churn structured data on two live pages for no accuracy gain.

Worth recording: `BarOrPub` remains **unused** in this dataset - it was also the
type held back when Tru Blues was excluded from best-wings. It is not being
avoided; it just has not been accurate yet.

### Hachiya Ramen -> `Restaurant`

`FastFoodRestaurant` was considered on the strength of the kiosk ordering and
P&C's "speed" framing, and **rejected**: kiosk-ordered, table-delivered ramen is
fast-*casual*, and no source calls it fast food. No ramen-specific schema.org
type exists. `Restaurant` is both accurate and the dataset norm.

Current spread for reference: 28 `Restaurant`, 5 `CafeOrCoffeeShop`, 3
`IceCreamShop`, 2 `FoodEstablishment`, 1 `Bakery`, 0 `BarOrPub`. This launch
adds one `Restaurant`.

---

## 4. Slug, dedup and social-card checks - all run, none predicted

| Check | Result |
|---|---|
| `best-ramen` in `data/og_rankings.json` | **no** - free |
| `rankings/best-ramen.html` exists | **no** - free |
| `assets/images/og-best-ramen.png` exists | **no** - free |
| `hachiya-ramen` slug collision | **none** - free |
| `bar-weems` slug | **EXISTS - and that is correct.** Not a collision: it is the same restaurant being cross-listed, which is an `appearsOn` append. The recipe's step 4 covers exactly this. |
| Social card title derivation | `best-ramen` -> **"Best Ramen"** |

**Social card derivation traced through `social/src/data.ts`, not guessed.**
`slug.slice('best-'.length).split('-').map(titleCase).join(' ')` with
`titleCase(s) = s[0].toUpperCase() + s.slice(1).toLowerCase()`. Single token
`ramen` -> `Ramen`; `title` = `Best Ramen`. **Clean** - no hyphen loss, unlike
`best-tex-mex` -> "Best Tex Mex". The pipeline also requires an
`Updated {Month Year}` pill (regex `/Updated\s+([A-Z][a-z]+\s+\d{4})/`) and each
row name wrapped in the `/restaurants/{slug}.html` anchor; both are in the drafted
markup.

**Cuisine-dedup - run through `scripts/_cuisine_dedup.py`, not eyeballed:**

| name | cuisine | normalized | `_resolve_display_cuisine` |
|---|---|---|---|
| Hachiya Ramen | `Ramen` | `hachiya ramen` / `ramen` | **SUPPRESSED** |
| Bar Weems | `Japanese` | `bar weems` / `japanese` | `'Japanese'` |
| Bar Weems | `Ramen` (if refined) | `bar weems` / `ramen` | `'Ramen'` - renders |

**The prompt's prediction is confirmed by execution.** Hachiya Ramen
auto-suppresses per #18. **Do not add a `displayCuisine` override** - the prompt
is right and the tree agrees. Its detail `<title>` becomes "Hachiya Ramen in
Charleston | Voted On By Locals" and its hero subtitle collapses; with
`neighborhood` also null, `generate_detail_page.py`'s null-handling drops the
subtitle `<p>` entirely - the Toni's path, already live.

Bar Weems does **not** suppress under either cuisine value, so the section-2a
refinement is display-visible.

`servesCuisine` keeps the raw `cuisine` on detail pages regardless (#18.5).

---

## 5. STEP 4 - the registry grid at 13 categories

`best-ramen` is the **13th** ranking. Confirmed against the tree: 12 entries in
`og_rankings.json`, 12 cards in `index.html`, 12 links in each of the two
`components/header.html` menus.

`index.html:168` is
`<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">`, inside a
`container mx-auto max-w-4xl` (896px).

| Cards | base (1 col) | md (2 cols) | lg (4 cols) |
|---|---|---|---|
| 12 (today) | 12 rows, clean | 6 rows of 2 - clean | 3 rows of 4 - clean |
| **13 (after this launch)** | 13 rows, clean | 7 rows, **last row 1 - ORPHAN** | 4 rows, **last row 1 - ORPHAN** |

**The standing ruling's conclusion holds. Its stated reasoning does not.**

The best-wings Q7 ruling reads:

> "Do NOT change `grid-cols`. Reasoning: at `lg:grid-cols-4` eleven cards render
> 4/4/3, which is clean, and that is the primary desktop view."

That premise **expires at 13**. lg now renders 4/4/4/1 - the orphan lands on the
primary desktop view for the first time, and md orphans simultaneously. This is
the worst grid state since the class was set, and strictly worse than the 11-card
case the ruling was written for.

The conclusion survives anyway, for a reason the ruling never had to state:
**13 is prime.** No column count divides it but 1 and 13. `md:grid-cols-3` gives
5 rows of 3 + 1 and re-opens the ~277px-card objection that sent the 10-card
change to `md:grid-cols-2`; `lg:grid-cols-3` gives 4 rows of 3 + 1. **Every
option orphans.** So the orphan is unavoidable rather than chosen, and changing
`grid-cols` buys nothing while costing readability.

**Ruling still applies - but re-derive it at 14**, where `md:2` and `lg:4`
both return to clean (7x2, 4/4/4/2) and the question closes itself.

**One ambiguity in the prompt worth naming.** "Do not touch index.html" is the
wings ruling's shorthand for *do not change the `grid-cols` class*. Recipe step 7
still requires the new homepage **card**, and skipping it would drop a required
registry edit and leave the 13th ranking undiscoverable from the homepage. The
card is in; the class is not.

---

## 6. Drafted page content - DRAFT ONLY

### 6a. Head meta

```
<title>Best Ramen in Charleston, SC | Locals Guide (2026)</title>

<meta name="description" content="Discover the best ramen in Charleston, SC.
From house-made noodles to slow-cooked tonkotsu broth, explore the top bowls
voted on by the local community.">

<meta name="keywords" content="best ramen Charleston SC, Charleston ramen
rankings, tonkotsu Charleston, house-made noodles Charleston, local favorites
Charleston">

<link rel="canonical" href="https://votedonbylocals.com/rankings/best-ramen.html">

<meta property="og:title"       content="Best Ramen in Charleston | Voted On By Locals">
<meta property="og:description" content="Charleston's best ramen, voted by the local community.">
<meta property="og:type"        content="website">
<meta property="og:url"         content="https://votedonbylocals.com/rankings/best-ramen.html">
<meta property="og:image"       content="https://votedonbylocals.com/assets/images/og-best-ramen.png">
<meta property="og:site_name"   content="Voted On By Locals">

<meta name="twitter:card"        content="summary_large_image">
<meta name="twitter:title"       content="Best Ramen in Charleston | Voted On By Locals">
<meta name="twitter:description" content="Charleston's best ramen, voted by the local community.">
<meta name="twitter:image"       content="https://votedonbylocals.com/assets/images/og-best-ramen.png">
```

Both description descriptors are anchored to a specific entry - house-made
noodles = Bar Weems' own descriptor line; slow-cooked tonkotsu = Hachiya's own
site plus P&C - so the sentence survives either entry changing without becoming
false. `{{Description}}` / `{{ShareTagline}}` split per DECISIONS #3.

### 6b. Hero, subtitle, pill

```html
<h1 class="text-4xl sm:text-6xl font-extrabold font-poppins text-brand-dark leading-tight">
    Best <span class="text-brand-orange">Ramen</span> [U+1F35C]
</h1>

<p class="text-brand-gray mt-4 text-lg font-medium">As voted by Charleston locals. Two standouts [U+2014] with more to come.</p>

<div class="inline-block bg-white px-3 py-1 rounded-full text-xs text-gray-400 border border-gray-100 mt-2 shadow-sm">
    Updated August 2026
</div>
```

**Emoji: U+1F35C STEAMING BOWL**, `aria-label="steaming bowl"`. It is the
Unicode-designated ramen glyph (the reference glyph is a ramen bowl with
chopsticks) and is unambiguous at card size. aria-label uses the Unicode name per
tree convention - verified against `poultry leg` (U+1F357) on best-wings and
`soft ice cream` (U+1F366) on best-ice-cream. Alternate considered: U+1F372 POT
OF FOOD, rejected as generic stew.

**Subtitle is the exact Top-2 string** #23 prescribes, byte-matched against the
live `rankings/best-frozen-margarita.html:271`:
`As voted by Charleston locals. Two standouts [EM] with more to come.`

**No NEW pill** - #23 is explicit that the pill is featured-1 ceremony only, and
the 60-day decay rule has nothing to decay on a Top-N. Verified in the tree:
`components/header.html` carries exactly one NEW-pill artifact set, all
`best-bakery`.

### 6c. Taglines - one grounded, one flagged

| Rank | Restaurant | Proposed | Assessment |
|---|---|---|---|
| 1 | Bar Weems | `House-Made Noodles, Late-Night Bowls` | **GROUNDED** - shipped as-is |
| 2 | Hachiya Ramen | `Slow-Cooked Broth, Tonkotsu First` | **PARTLY GROUNDED - flagged, NOT shipped** |

> **Superseded.** Rank 2 shipped as **`Slow-Cooked Broth, Kiosk Fast`** - see
> section 11 for the two-step path that got there. The analysis below is the
> record of why the originally proposed "Tonkotsu First" was rejected; it stands,
> and the same objection ultimately retired "Four-Minute Bowl" as well.
>
> Note that `Slow-Cooked Broth, Kiosk Fast` appears in this section's own
> alternatives list, proposed there and passed over. It came back.

**Rank 1 clears cleanly.** "House-Made Noodles" is the own site's literal
descriptor line ("house made noodles"), corroborated by Charleston Magazine
("noodles made by hand each day"). "Late-Night Bowls" is grounded in the 1am
close plus the own site's "LATE NITE MENU 10PM-12:30AM". No duplication risk
against Bar Weems' existing best-new-restaurants row tagline ("Handmade Ramen &
Cocktails") - different words, different page, and the PR #40 precedent was about
duplication *within* a page.

**Flag on rank 2: "Tonkotsu First" is not grounded.** "Slow-Cooked Broth" is -
the own site says "slow-cooked broths" verbatim. But no source ranks the bowls or
names a signature. P&C reports **three ramen types, one vegetarian**, and
describes the tonkotsu without calling it the flagship. "First" asserts a menu
hierarchy nothing supports. Same class of defect as best-ice-cream's "Piled High".

Grounded alternatives, all from the own site or P&C:

- `Slow-Cooked Tonkotsu, Kyoto Roots` - minimal change; keeps tonkotsu (it is on
  the menu and is the bowl P&C described) and drops the ranking claim. Takebata
  was born and raised in Kyoto. **Recommended.**
- `Slow-Cooked Broth, Cloudy Tonkotsu` - P&C: "cloudy", "void of excess fat".
- `Slow-Cooked Broth, Kiosk Fast` - P&C's speed framing; accurate but unflattering.
- `Charleston's Choice Best Ramen 2025` - impeccably sourced, but it borrows
  another outlet's verdict on a page whose whole premise is the local vote, and
  it sits under a restaurant ranked 2nd here. **Flagging the tension, not
  recommending it.**

Operator call. Not blocking - per WORKFLOW.md, tone and copy are operator
territory.

### 6d. ItemList JSON-LD

Field order copied from the production shape (`@context, @type, name,
description, datePublished, dateModified, url, itemListElement`).
**ItemList MUST precede BreadcrumbList** - per #23, `generate_sitemap.py` parses
only the first `ld+json` block and `<lastmod>` vanishes silently otherwise.

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Best Ramen in Charleston, SC",
  "description": "<same string as meta description>",
  "datePublished": "2026-08-26T12:00:00-04:00",
  "dateModified": "2026-08-26T12:00:00-04:00",
  "url": "https://votedonbylocals.com/rankings/best-ramen.html",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "item": {
        "@type": "Restaurant", "name": "Bar Weems",
        "url": "https://votedonbylocals.com/restaurants/bar-weems.html",
        "servesCuisine": "Ramen",
        "address": { "@type": "PostalAddress", "addressLocality": "North Charleston", "addressRegion": "SC" } } },
    { "@type": "ListItem", "position": 2, "item": {
        "@type": "Restaurant", "name": "Hachiya Ramen",
        "url": "https://votedonbylocals.com/restaurants/hachiya-ramen.html",
        "servesCuisine": "Ramen",
        "address": { "@type": "PostalAddress", "addressLocality": "Mount Pleasant", "addressRegion": "SC" } } }
  ]
}
```

**`addressLocality` per #15 Q5** - literal municipality, reconciled to the value
on the corresponding detail page. `North Charleston` and `Mount Pleasant`, not
the editorial "Charleston" rollup. Bar Weems' was already reconciled in the
2026-05-03 bulk port; Hachiya's is set correctly at birth.

**`servesCuisine` proposals, flagged not decided** per #23's "flag them in the PR
body rather than deciding silently":

| Entry | `restaurants.json.cuisine` | ItemList `servesCuisine` | Rule applied |
|---|---|---|---|
| Bar Weems | `Japanese` (or `Ramen` if refined) | `Ramen` | **override the generic** - "Japanese" is the `American`-class offender on a ramen list |
| Hachiya Ramen | `Ramen` | `Ramen` | preserve the specific |

Both land on `Ramen` by different halves of the same rule. Note this is
list-scoped and does **not** propagate to best-new-restaurants' ItemList, where
`Japanese` remains a legitimate hand-authored value (#23: "Two different
documents, two different rules. Do not unify them.").

### 6e. BreadcrumbList, rows, CTA

BreadcrumbList **second**: Home / Rankings (`/#rankings`) / Best Ramen.

Row markup is the standard block, twice, page emoji reused, each name wrapped in
the anchor the social pipeline's regex requires:

```html
<h2 class="font-poppins font-bold text-xl sm:text-2xl text-brand-dark mb-1 leading-snug"><a href="/restaurants/{slug}.html" class="hover:text-brand-orange transition-colors">{Name}</a></h2>
<p class="text-brand-gray font-medium text-sm sm:text-base">{Tagline}</p>
```

CTA canonical per DECISIONS #7: "Disagree with this list? Cast your vote!" with
the button reading `Vote for Best Ramen`.

---

## 7. The five registry edits

| # | File | Edit |
|---|---|---|
| 1 | `components/header.html` | desktop dropdown, appended after `Best Ice Cream` (L45), end of the Top-N cluster below the divider |
| 2 | `components/header.html` | mobile menu, appended after `Best Ice Cream` (L80) |
| 3 | `index.html` | homepage grid card, appended after the ice-cream card (L229-232); **`grid-cols` untouched** per section 5 |
| 4 | `vote.html` | `<option>Best Ramen</option>` inserted after L180, before `</select>` at L181, 32-space indent |
| 5 | `data/og_rankings.json` | `{"slug": "best-ramen", "category": "Ramen", "spots": 2}` + bump `_meta.lastUpdated` |

`spots: 2` - not 1, so the social pipeline stays on the Top-N path rather than
routing into the featured-1 renderer.

Homepage card hook is editorial - operator supplies. Existing hooks run 5-8 words
with a trailing page emoji. Proposal: `House-made noodles and slow-cooked broth.
[U+1F35C]` - category-level, asserts nothing about either restaurant specifically,
so it survives a roster change.

**Note on the count.** #23's recipe steps 3, 4, 6, 7 and 8 are five *files*
(`og_rankings.json`, `restaurants.json`, `header.html`, `index.html`,
`vote.html`); the best-ice-cream file counted five *edits* by splitting
`header.html` in two and omitting `restaurants.json`. Same work either way. This
table uses the ice-cream framing to match the prompt's phrasing;
`data/restaurants.json` is covered in section 8.

---

## 8. Blast radius

One net-new restaurant, one cross-listing. Lighter than best-ice-cream (three
net-new), heavier than best-wings in one respect: the cross-listing re-opens the
`dateModified` trap.

| Step | Files |
|---|---|
| `rankings/best-ramen.html` | 1 new |
| `data/restaurants.json` | 1 modified - 1 new entry (`hachiya-ramen`), 1 `appearsOn` append + field corrections (`bar-weems`) |
| `data/og_rankings.json` | 1 modified |
| `restaurants/hachiya-ramen.html` | 1 new, generated |
| `restaurants/bar-weems.html` | 1 **regenerated** + hand-bumped `dateModified` |
| `components/header.html` | 1 modified |
| `index.html`, `vote.html` | 2 modified |
| `_strategy/TRACKED.md` | 1 modified - see section 9 |
| `_strategy/DECISIONS.md` | 1 modified if the #23 footnote in section 10 is adopted |
| `sitemap.xml` | 1 regenerated |
| `assets/images/og-best-ramen.png` | 1 new |
| `assets/images/og-restaurant-hachiya-ramen.png` | 1 new |
| `assets/images/og-restaurant-bar-weems.png` | **shipped in PR 1** - the OG meta-line is `cuisine [MID] neighborhood`, verified against `og-templates/detail.html:17,188`, and both fields changed |
| `inline_chrome.py --refresh` | **62 files** (60 in sync today, verified via `--check`; + 1 ranking + 1 detail) |

**Ordering constraints that will bite** (#23):

1. `python scripts/generate_detail_page.py bar-weems` and
   `... hachiya-ramen` - **never `--all`**, which rewrites every page and destroys
   the diff.
2. **Hand-bump `bar-weems`' `dateModified`** after regen. The generator preserves
   prior dates by design (2026-05-03T19:03:39-04:00 today), so regeneration alone
   leaves it stale. Per the tree's `dateModified` mechanism, the value lives in
   the rendered detail page's JSON-LD, not in `restaurants.json`.
3. New ranking + detail pages must exist **before** `inline_chrome.py --refresh`,
   or they ship stale chrome and `--check` exits 2.
4. **`generate_sitemap.py` runs LAST**, after the `dateModified` bump - it reads
   `dateModified` to build `<lastmod>`, and running it early ships stale dates
   silently.
5. `npm run build:css` **only** if a class-set diff shows new utilities. Copying
   an existing page introduces none.
6. Playwright Chromium must be installed before `generate_og_images.py`
   (`python -m playwright install chromium`, ~87 MB).

---

## 9. TRACKED entries this launch generates

To file in the launch PR per #22 (same-PR file edit, not PR prose).

> **Hachiya Ramen Clements Ferry second location - opening undetermined,
> secondary excluded from `locations[]`.** A second location at 654 Hopewell Dr,
> Ste 102/103, Charleston, SC 29492 (Point Hope, Clements Ferry corridor) has
> been announced by co-owner Yuichiro "Junior" Takebata. As of **2026-08-26 no
> source confirms it has opened**: The Daniel Island News (2026-02-11) reported it
> "is currently navigating permitting and is **expected to open** around September
> or October"; the restaurant's own Facebook page was still writing in future
> tense on **2026-07-15** ("all of your favorites **are coming to** Hachiya Ramen
> Clements Ferry"); **the own website does not mention a second location at all**,
> which is itself a signal; and the Google listing carries no ratings, hours or
> phone. The stated target window has not yet arrived. Per DECISIONS #17 a
> multi-location entry needs `locations[]`; per #23's conflict rule an
> undetermined status is excluded rather than guessed. `hachiya-ramen` therefore
> ships single-location. Trigger: a dated confirmation that the Point Hope shop
> is open - a "now open" announcement, a dated review, or a directory listing with
> hours. On confirmation, add the secondary to `locations[]` and regenerate the
> detail page. Filed by the best-ramen launch.

> **Bar Weems neighborhood was "Park Circle"; corrected.** [File only if option
> (A) or (B) in section 2a ships - this is a resolution record, not an open item.]
> The entry carried `neighborhood: "Park Circle"` from the 2026-05-03 workstream H
> bulk port, with the same claim cascaded into `description`, `shareTagline` and
> `keywords`. Post and Courier places 1921 Reynolds Ave in the **Chicora-Cherokee**
> neighborhood and explicitly contrasts the two ("A left turn leads toward
> bustling Park Circle ... Heading right will take you to the Reynolds Avenue
> restaurant corridor"). Corrected in the best-ramen launch under the Tutti
> precedent (DECISIONS #18): prose contradicting a factual correction is hard
> inconsistency and is fixed in the same PR.

**One existing TRACKED item to RETIRE, not file** - if the cuisine refinement in
section 2a ships: the Bar Weems clause of *"Cuisine specificity editorial review
(3 borderline cases)"*. Its trigger ("when next editing these entries") fires
here. FIG and Edmund's Oast remain open, so the entry is edited down rather than
deleted.

---

## 10. Where this prompt and the recipe/tree disagree

Reported per the instruction, in descending order of consequence.

1. **The prompt does not know Bar Weems is already in the tree.** It supplies
   Bar Weems as external sourcing output. `data/restaurants.json`,
   `restaurants/bar-weems.html` and row 2 of `best-new-restaurants` have carried
   it since 2026-05-03. This converts "new entry" into "`appearsOn` append +
   regen + `dateModified` hand-bump", pulls in #23 rule 4, and means three fields
   the prompt frames as open questions are live shipped values. **Highest-
   consequence divergence; everything below flows from it.**

2. **Bar Weems' own site says Tue-Sat, not Wed-Sun.** Fetched 2026-08-26:
   "SUNDAY & MONDAY CLOSED / TUESDAY - SATURDAY 5PM - 1AM". The prompt attributes
   Wed-Sun to the own site and Wed-Sat to Charleston Magazine; the magazine's
   Wed-Sat is right, the own site's Wed-Sun is not a claim any source makes.

3. **"Four sets" of hours is two, and they resolve 4-to-1.** Own site + Yelp
   (Aug 2026) + Apple Maps + an aggregated day-grid all give Tue-Sat; only
   Charleston Magazine (July 2026) says Wed-Sat. **The prompt's `null` +
   #13.10 instruction was conditional on unresolvability and the condition
   fails.** Nulling here would delete live data in deference to the single
   stalest source. The phone-clause question is therefore moot.

4. **The tree's existing hours are stale by one day** (`We-Sa` -> `Tu-Sa`). Not
   contemplated by the prompt, and it is a correction rather than an addition.

5. **Bar Weems' neighborhood is not "unresolved" - it is populated and wrong.**
   `Park Circle` is live, and cascaded into three prose fields. P&C puts Reynolds
   Ave in Chicora-Cherokee and explicitly distinguishes the two areas. The prompt
   offers "propose, or null with the tonis precedent"; there is a third and better
   option (correct it to the sourced name), and a fourth that must be ruled out
   (leave it).

6. **The locality question was closed on 2026-05-03, not open.** The prompt asks
   to "verify and apply DECISIONS #15 Q5" as if undecided; TRACKED's workstream-H
   record already lists "Bar Weems locality -> North Charleston" as shipped.
   Re-derived from scratch anyway per the instruction, and it holds - own site,
   Yelp, Apple Maps, Charleston Magazine and P&C all say North Charleston, and
   29405 is a North Charleston ZIP. Google's "Charleston" is postal-city
   rendering; #14.2 wants the literal municipality. **No change.**

7. **"Most-specific applicable subclass" does not decide Bar Weems.**
   `Restaurant` and `BarOrPub` are siblings under `FoodEstablishment`, not
   nested. Intentional decision #4's operative word for this case is *accurate*,
   not *specific*. Stating it precisely so the next reader does not think
   specificity settled it. (Same class of precision note as best-ice-cream's
   finding that the docblock type lists are illustrative, not an allowlist.)

8. **The prompt omits that this launch fires an open TRACKED trigger** - Bar
   Weems `cuisine` "Japanese" -> "Ramen", trigger "when next editing these
   entries". A best-ramen launch is that edit.

9. **Roster size undershoots the recipe, again.** #23 section 0: "start with
   roughly twice your target N", and it calls sourcing "where the launch actually
   gets decided". This prompt supplies **exactly 2 candidates for a Top-2 - 1x N,
   zero bench**. It worked because both passed, but a single failure would have
   silently reduced this to a featured-1, which is a different page shape, a
   different renderer path (`spots: 1`), and gets a NEW pill. **This is the second
   consecutive launch to make the same omission** (best-ice-cream: 3 for a Top-3),
   which makes it a pattern in the prompting rather than a one-off.

10. **STEP 4's standing ruling needs re-derivation, not re-application.** The
    wings Q7 reasoning ("lg 4/4/3 is clean, and that is the primary desktop
    view") is false at 13 cards - lg renders 4/4/4/1. The conclusion survives
    only because 13 is prime and no column count fixes it. Reported in full in
    section 5.

11. **"Do not touch index.html" is ambiguous and one reading is wrong.** It means
    do not change `grid-cols`; recipe step 7 still requires the homepage card.

12. **"Tonkotsu First" is not grounded** (section 6c). Also: the prompt's
    "Slow-Cooked Broth" is grounded verbatim, so only half the tagline is at issue.

13. **`websiteURL` form.** Prompt gives `https://www.barweems.com/`; the tree
    stores `https://barweems.com` (no `www`, no trailing slash), consistent with
    the field's convention across other entries. Keep the tree form.

14. **A footnote #23 should probably gain** (offered, not applied). #23's gate
    table marks the own site "INADMISSIBLE" for liveness *and current hours*.
    That is right for liveness and slightly too strong for hours: here the own
    site is one of four converging sources on hours and agrees with two dated
    third-party listings. The rule should be read as *own-site hours are never
    **sufficient** on their own*, not *own-site hours are evidence of nothing*.
    Compare best-ice-cream's parallel footnote on "own site authoritative for
    identity" not meaning "own site infallible on every field".

---

## 11. Resolutions (operator, 2026-08-26)

All eight open questions are closed. Recorded here rather than only in the PRs,
so this file stays the durable record of the launch.

| # | Question | Resolution |
|---|---|---|
| 1 | Bar Weems `neighborhood` | **(A) `Chicora-Cherokee`** + prose cascade |
| 2 | Hyphenation | **hyphenated** - `Chicora-Cherokee` |
| 3 | Bar Weems `cuisine` | **refine** `Japanese` -> `Ramen` |
| 4 | Hachiya tagline | **`Slow-Cooked Broth, Kiosk Fast`** - superseded `Four-Minute Bowl`, see below |
| 5 | Hero emoji | **confirmed** - U+1F35C, `aria-label="steaming bowl"` |
| 6 | Homepage card hook | **confirmed** - `House-made noodles and slow-cooked broth. [U+1F35C]` |
| 7 | best-new-restaurants ItemList `servesCuisine` | **leave** `Japanese` - list-scoped per #23 |
| 8 | #23 footnote from 10.14 | **adopt, in a later docs PR** - not in either launch PR |

### The launch splits into two PRs

**Q1 and Q3 ship in PR 1, not the launch PR.** The Bar Weems data correction
was pulled forward into its own PR (`bar-weems-data-correction`) and must merge
**before** the launch PR, so that the launch's `appearsOn` regen does not bake
the wrong neighborhood into a freshly-touched page and stamp a `dateModified`
on top of it. That ordering is the whole point of the split: #23 rule 4 says the
bump asserts freshness, and asserting freshness over a known-wrong field is the
failure mode being avoided.

| PR | Scope |
|---|---|
| **PR 1** - `bar-weems-data-correction` | Q1 + Q2 + Q3, the prose cascade, the stale-hours fix, `bar-weems` regen + `dateModified` bump, OG re-render, TRACKED clause retirement. **No `appearsOn` edit.** |
| **PR 2** - `best-ramen-launch` | Everything else in this file: the new ranking page, `hachiya-ramen`, the five registry edits, Q4/Q5/Q6 copy, `appearsOn` append, the Clements Ferry TRACKED filing. |
| later docs PR | Q8 |

### Note on the Hachiya tagline - resolved in two steps, 2026-08-26

**Shipped: `Slow-Cooked Broth, Kiosk Fast`.** It got there via a rejected
intermediate, and both steps are worth keeping because they turn on different
tests.

**Step 1 - `Tonkotsu First` rejected: not sourced.** No source ranks the bowls
or names a signature; P&C reports three ramen types, one vegetarian. Detail in
section 6c.

**Step 2 - `Four-Minute Bowl` rejected: sourced, but the framing inverts the
source.** The number is real. Post and Courier's "Now Open" piece:

> "The bowl arrives about four minutes later. The chef apologizes for the wait."

But P&C presents four minutes as **a wait that warranted an apology**, measured
against the owners' stated target of three ("their goal is to have food out in
three minutes once you order it"). Publishing it as a selling point inverts what
the source actually says. That is a subtler failure than fabrication - every word
is defensible in isolation and the citation would survive a spot-check - which is
exactly why it is worth naming. **A sourced fact can still be misused by
reframing.** Sourcing is necessary, not sufficient; the claim also has to mean
what the source meant.

**Why `Kiosk Fast` clears both tests.** Multiply sourced and directionally
faithful:

- P&C's own framing: *"Speed and quality take center stage"*; the pair "said
  their focus is speed and quality - hence the self-service kiosks."
- The kiosks are literal and observed: *"Tall touch screens are perched where a
  host stand would normally be."*
- It asserts speed as an intent and a mechanism, which is what the article
  asserts, rather than a specific measured time the article treats as a miss.
- It also matches the shipped `description`, which already reads "ordered from
  self-service kiosks" - so page and data now say the same thing.

"Slow-Cooked Broth" was never in question - own site verbatim ("slow-cooked
broths, fresh noodles, and balanced flavors"). The two halves now sit in useful
tension: slow broth, fast service, which is the actual proposition.

**Research note worth keeping.** The first pass wrongly flagged "Four-Minute
Bowl" as unsourced. The article had been fetched successfully - it was the **Bar
Weems** P&C piece that returned HTTP 429, not this one. The miss was in the
question, not the fetch: the earlier prompt asked about *broth cooking time*, and
the answer ("does not specify cooking time") was true of the broth and silent on
serve time. **A negative answer is scoped to the question asked, not to the
document.**

Settled without needing operator input, on evidence:

- **Bar Weems `hours`** = `Tu-Sa 17:00-01:00`; #13.10 does not fire.
- **Bar Weems `addressLocality`** = `North Charleston`, unchanged, re-confirmed.
- **Bar Weems `schemaType`** = `Restaurant`, unchanged. `BarOrPub` considered and
  rejected on the evidence, not by default.
- **Hachiya `hours`** = `Tu-Su 11:30-20:30`, Mon closed - three sources agree.
- **Hachiya `neighborhood`** = `null` on the `tonis-detroit-style-pizza` precedent.
- **Hachiya `schemaType`** = `Restaurant`; `FastFoodRestaurant` rejected.
- **Hachiya name** = `Hachiya Ramen`; the West Ashley collision is real.
- **Clements Ferry** excluded; `hachiya-ramen` ships single-location with a
  re-verification trigger.
- **No `displayCuisine` override** for Hachiya - #18 auto-detect fires, verified
  by running `scripts/_cuisine_dedup.py`.
- **No NEW pill** - Top-N per #23.
- **`index.html` `grid-cols`** unchanged; card added.

---

## Encoding note

Non-ASCII intentionally referenced by codepoint rather than glyph in this file,
to survive console round-tripping:

- **U+1F35C** STEAMING BOWL - proposed hero/row emoji.
- **U+2014** EM DASH, marked `[EM]` - required in the subtitle count framing.
- **U+2013** EN DASH, marked `[EN]` - `hoursHumanReadable` day and time ranges.
  Shape precedent: `park-pizza-co`. Copy the shape from the tree, not from here.
- **U+00B7** MIDDLE DOT, marked `[MID]` - the OG meta-line separator.
