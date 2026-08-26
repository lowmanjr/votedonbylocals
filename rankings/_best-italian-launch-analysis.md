# Best Italian launch - analysis working file

Analysis-only working file for the `best-italian` Top-5 launch. Author: Claude
session 2026-08-26, branch `best-italian-launch`, cut from `main` @ `8c697db`
(verified clean, `git status --short` empty, before the branch was created).

**Status: applied.** Analysis pass 2026-08-26, build pass the same day.
Section 13 records the operator resolutions and the two records this file
originally got wrong.

Where a drafted section was superseded by what actually shipped, the section
says so inline rather than being rewritten - the draft is the record of the
reasoning, section 13 is the record of the decision. Same convention as
`_best-ramen-launch-analysis.md` section 11.

Location per `_strategy/WORKFLOW.md`: underscore-prefixed, in the directory of
the work it supports (`rankings/`), not `_strategy/`. Same as
`_best-wings-launch-analysis.md`, `_best-ice-cream-launch-analysis.md` and
`_best-ramen-launch-analysis.md`.

Recipe followed: DECISIONS #23 "Top-N launch recipe (formalized)", as amended
by PR #50 (`8c697db`). Anchors read in full: #4, #17, #18, #19, #20, #23, and
`rankings/_detail-page-template.html` intentional decision #4.

---

## 0. The finding that reframes this launch

**All five candidates are net-new, and the roster has zero bench.**

The prompt hypothesised that Sorelle and Le Farfalle were "plausibly already on
best-nice-restaurants" and Mondo's on best-casual-spots. Verified: **none of the
three is anywhere in the tree.** Neither are Wild Olive or Coda del Pesce.

That makes this the launch the recipe explicitly warns about:

> "Never zero bench, whatever the provenance. best-ice-cream supplied exactly 3
> for a Top-3 and best-ramen exactly 2 for a Top-2. Both happened to survive."

Five supplied for a Top-5, all net-new, is the third consecutive zero-bench
roster and the largest one yet. Two things soften it and one sharpens it:

- **Softening 1 - provenance.** The roster is operator-supplied
  ("operator-confirmed order"), and operator-supplied rosters are 0-for-10 on
  attrition across best-ice-cream and best-ramen. All five cleared both gates
  here too (section 2), so the bench was not needed.
- **Softening 2 - failure at N=5 is editorial, not structural.** The recipe's
  zero-bench alarm is loudest at N=1, where a failure changes the page *shape*
  (different template, `spots: 1` renderer, NEW pill). At N=5 a failure drops to
  Top-4, which is a documented precedent with its own count framing (#4, #20).
  The blast radius of a late failure here is a subtitle edit, not a rebuild.
- **Sharpening - this is the most expensive roster to re-source.** Five net-new
  entries means five full schema records, five generated detail pages and five
  new OG images. best-wings, the only prior all-researched roster, lost 3 of 5.
  If a candidate had failed here, the replacement cost is a full net-new entry,
  not an `appearsOn` append.

**There is a free bench candidate already in the tree.** See section 1b.

---

## 1. STEP 1 - tree first, per amended #23 rule 1

Run before any sourcing, per the rule the best-ramen launch produced.

Method: `grep -ril` for `wild`, `olive`, `coda`, `pesce`, `farfalle`, `sorelle`,
`mondo` across `data/`, `restaurants/` and `rankings/`; plus a full dump of all
41 `slug`/`name` pairs from `data/restaurants.json` read directly, so the answer
does not depend on the greps alone.

### 1a. Result - five absences, both hypotheses false

| Candidate | In `restaurants.json`? | Detail page? | On any ranking? | Verdict |
|---|---|---|---|---|
| Wild Olive | no | no | no | **net-new** |
| Coda del Pesce | no | no | no | **net-new** |
| Le Farfalle | no | no | no | **net-new** |
| Sorelle | no | no | no | **net-new** |
| Mondo's | no | no | no | **net-new** |

Zero matches, zero near misses. Every grep pattern returned empty across all
three directories.

The two rosters the prompt named, read from `appearsOn`:

- **best-nice-restaurants** = `verns`, `chubby-fish`, `zero-george`, `fig`,
  `malagon`. No Sorelle, no Le Farfalle.
- **best-casual-spots** = `home-team-bbq`, `chico-feo`,
  `bon-banh-mi-southeast-asian-kitchen`, `edmunds-oast`, `teds-butcherblock`.
  No Mondo's.

**Consequence: no `appearsOn` appends, no `dateModified` hand-bumps on existing
pages, and #23 rule 4 (the gate applies to pre-existing entries) does not fire
for any of the five.** Every candidate takes the full net-new path. This is the
opposite of best-ramen's finding, and it is worth recording that the check is
cheap enough to be worth running even when it comes back empty - the cost was
one grep, and it retired two live hypotheses that would otherwise have shaped
the sourcing pass.

Tree integrity confirmed while I was in there: 41 entries in
`data/restaurants.json`, 41 files in `restaurants/`, symmetric difference empty.
13 ranking slugs in `data/og_rankings.json`, 13 non-underscore files in
`rankings/`, symmetric difference empty.

### 1b. What the tree check DID surface - `ok-donna`

The five greps came back empty, but the tree contains an Italian restaurant the
roster does not mention:

```
slug:      ok-donna
name:      OK Donna
cuisine:   Italian
tagline:   Neighborhood Pasta & Pizza
address:   1117 King St, Charleston, SC 29403
hours:     Mo 17:00-23:00,We-Su 17:00-23:00
appearsOn: best-new-restaurants only
```

`best-new-restaurants.html` already carries `"servesCuisine": "Italian"` for it -
the only `Italian` servesCuisine string anywhere in `rankings/`.

**This is the zero-cost bench candidate.** Adding it would be an `appearsOn`
append + regen + `dateModified` hand-bump, not a net-new entry - roughly a tenth
of the work of sourcing a sixth restaurant from scratch.

**Not proposed as a roster change.** The order is operator-confirmed, N is an
output of consensus and not mine to pad (#4 anti-fabrication), and a Top-6 is
not a documented ranking length. Raised because the recipe asks for a bench and
this is the cheapest one available. **Operator decision.**

If it is taken up, it flips to the pre-existing-entry path and #23 rule 4 fires:
re-run both gates before the `dateModified` bump. Two fields would want checking
first - `phone` is `null`, and `monthYear` still reads "May 2026".

Two further names surfaced incidentally from a P&C piece ("50 Italian
restaurants have opened in SC since 2022") - **Indaco** and **Costa**. Neither
is in the tree; both are unverified; recorded only so a future session does not
think the category was surveyed exhaustively.

---

## 2. STEP 2 - both gates, run independently

The supplied data was treated as a hypothesis, not a source. Every field below
was re-derived. Results: **the supplied data is unusually good - but it is wrong
in four places and incomplete in one, and one of the wrong ones is the tagline
premise for Mondo's.**

### 2a. Liveness gate - dated third-party, REQUIRED

| Candidate | Signal 1 | Signal 2 | Signal 3 | Verdict |
|---|---|---|---|---|
| Wild Olive | Yelp, updated **Aug 2026**, 945 reviews | Resy active booking page | Wheree, updated May 2026 | **PASS** |
| Coda del Pesce | Yelp, updated **Jul 2026**, 248 reviews | Resy active booking page | Tripadvisor listing live | **PASS** |
| Le Farfalle | Yelp, updated **Jul 2026**, 782 reviews | Resy active booking page | Charleston Mag dining guide | **PASS** |
| Sorelle | Yelp, updated **Aug 2026**, 449 reviews | Michelin Guide listing | Tripadvisor / Corner listings | **PASS** |
| Mondo's | Yelp, updated **May 2026**, 350 reviews | Restaurantji, status **Open**, 309 reviews | Restaurant Guru, 2175 reviews | **PASS** |

No conflicts, no closure signals, no contested-status findings. Nothing on this
roster resembles best-wings' Tru Blues / Nigel's / Dashi failures.

Seasonality was checked specifically for Coda del Pesce, as an oceanfront Isle
of Palms restaurant where a seasonal closure would be unremarkable. No source
describes one; high-season/off-season language in the listings refers to
reservation difficulty, not to closing. **PASS.**

### 2b. Category gate - #23 rule 5, verify the claim not just existence

All five must be verifiably Italian to sit on a best-italian list.

| Candidate | Own site self-description | Third-party category |
|---|---|---|
| Wild Olive | "Wild Olive Cucina Italiana" (copyright) | Yelp: Italian |
| Coda del Pesce | "his all Italian seafood restaurant" | Yelp: Italian |
| Le Farfalle | "A regional Italian restaurant" | Yelp: Italian |
| Sorelle | Southern Italian (site + MINA Group) | Michelin: Southern Italian |
| Mondo's | "Mondo's Italian Restaurant" | Yelp: Italian |

**All five PASS.** No single-source dependencies.

### 2c. Hours - own site corroborates, dated third-party decides

| Candidate | Prompt supplied | Verified | Match? |
|---|---|---|---|
| Wild Olive | Mo-Th 17:00-22:00, Fr-Sa 16:00-23:00, Su 16:00-22:00 | own site "Mon-Thurs 5-10 pm, Fri-Sat 4-11 pm, Sun 4-10 pm"; Yelp Aug 2026 agrees | **exact** |
| Coda del Pesce | Tu-Sa 17:30-21:00, Mo/Su closed | own site "Tuesday - Saturday 5:30 PM - close"; Yelp Jul 2026 gives the 21:00 close | **exact** |
| Le Farfalle | Mo-We 17:00-21:30, Th-Sa 17:00-22:00, Su 17:00-21:30 | own site x2 "Sunday - Wednesday 5:00 - 9:30 / Thursday - Saturday 5:00 - 10:00" | **exact, restated** |
| Sorelle | Tu-Su 17:00-22:00, Mo closed | own site "Tuesday - Sunday, 5:00PM - 10:00PM" | **exact** |
| Mondo's | Mo-Sa 16:00-21:00, Su closed | Restaurantji "Monday-Saturday 4-9 PM; Sunday Closed"; P&C "dinner Monday through Saturday" | **exact** |

**Five for five.** No hours conflict anywhere on this roster, so #13.10's
null-plus-fallback path does not come near firing.

**Le Farfalle needed three reads to land, and the detour is worth recording.**
The first fetch of `/location/le-farfalle/` returned "Sunday - Tuesday
5:00 - 9:30", leaving Wednesday unaccounted; a search summary then asserted
"Monday is the only day the restaurant is closed", which contradicts both the
prompt and the first read. Two further own-site reads - `/contact/` and the
homepage - **both** returned "Dinner Only / Sunday - Wednesday 5:00 - 9:30 /
Thursday - Saturday 5:00 - 10:00". The Sun-Tue read was a summariser
transcription error, not a site inconsistency, and the "closed Monday" claim is
unsupported by any primary source.

This is #23's "negative answers are scoped to the question you asked" in a new
guise: **a bad read of a good source looks exactly like a source conflict.**
Re-reading the same source a different way resolved it. Practical guard for the
next session: when a single fetch produces a day-range that leaves a gap in the
week, re-read before recording a conflict.

Note the prompt expressed Le Farfalle's hours as `Mo-We` + `Su` and the own site
groups them as `Su-We`. **Identical sets.** The own-site grouping is proposed
below because it is one clause shorter and matches how the operator publishes it.

**Le Farfalle serves no brunch or lunch.** A search summary claimed "brunch is
served Saturdays and Sundays"; both own-site pages say "Dinner Only" and the
menus page shows no brunch service. The brunch claim is stale or wrong and is
**not** carried into the draft.

### 2d. Verifiable facts - independent record wins on contradiction

Addresses, ZIPs and phones cross-checked against own site plus at least one
independent listing. **No Gustard's-class contradiction found.** All five ZIPs
are consistent with their municipality: 29455 Johns Island, 29451 Isle of Palms,
29401 peninsular Charleston (x2), 29412 James Island.

One address nuance: Coda del Pesce's own site gives **"1130 Ocean Blvd, 2nd
Floor, Isle of Palms, SC 29451"**. The prompt omits the floor. Flagged in
section 9e - a unit designator is a real part of the address but no existing
`streetAddress` in the tree carries one.

### 2e. Pending second locations - the standing per-candidate check

Fourth consecutive launch to be checked; **first to come back clean on every
candidate.** All five ship single-location and none needs a `locations[]` array
per #17.

| Candidate | What exists | Determination |
|---|---|---|
| Wild Olive | Own site lists "OUR OTHER CONCEPTS": The Obstinate Daughter, The Douglas, Lester's (Savannah), Beardcat Sweet Shop | **Sibling brands, not Wild Olive branches.** Distinct names and concepts. Lester's is Savannah - out of editorial scope per #17.4 / #14.1 regardless. |
| Coda del Pesce | **Volpe**, 161 Rutledge Ave, Vedrinski's newer concept. Also **Trattoria Lucca**, his former restaurant | **Volpe is a separate brand**, not a Coda location. **Trattoria Lucca closed in 2020** (P&C). |
| Le Farfalle | **Da Toscano** (New York) and a porchetta shop, both Toscano projects | **Separate brands.** Da Toscano is out of scope by geography. |
| Sorelle | **Sorelle Mercato** - see section 3, the launch's one real determination | **Same building, same address, same phone. Not a second location.** |
| Mondo's | Owner Chris Orlando's family runs **Orlando's Pizza** on Daniel Island and Mount Pleasant | **Different brand.** Not Mondo's locations. |

**Coda del Pesce's own About page is six years stale**, and it is worth pinning
because it is the cleanest example of #23's identity/status split this launch
produced. The page still refers to Trattoria Lucca in the present tense as "his
charming downtown Charleston restaurant". It closed in 2020. The same page is
simultaneously the **best** source for the restaurant's own name spelling
(section 4) and **worthless** as evidence of what is currently operating -
exactly the Tru Blues pattern. The current sister concept, Volpe, appears on the
homepage but not on the About page, so the site is internally inconsistent about
its own portfolio.

---

## 3. The Sorelle Mercato determination

**Asked: `locations[]` secondary per #17, or a distinct concept? Answer: neither.
It is a service area inside the same venue, and it gets no representation in the
data at all.**

Evidence, own site first:

- **Same street address.** `sorellecharleston.com` publishes exactly one address,
  **88 Broad St**, and one phone, **(843) 974-1575**, for the whole operation.
  Yelp's separate `sorelle-mercato-charleston` listing also gives **88 Broad St**
  - not 90.
- **The Mercato is a room.** The site describes Sorelle as a venue that
  "features a mercato, central bar, wine room, and a grand dining room". Design
  press places it precisely: **the mercato is on the first floor**, the main
  dining room and chef's table on the second, private dining on the third.
- **It is a menu section, not a site.** The own site's navigation lists "Dinner"
  and "Mercato" as sibling menu pages under one restaurant, at `/menu/...` and
  `/location/mercato/` - inside the Sorelle site, not a site of its own.
- **It is a daypart.** Mercato 08:00-16:00 daily; Sorelle dinner 17:00-22:00
  Tu-Su. They do not overlap. One address, two service windows.

**Why not `locations[]`:** #17's data shape exists for "multi-location
restaurants" - the same brand at *different physical locations*, each with its
own `PostalAddress`, `telephone` and `openingHours`, rendered as an "Other
locations" card. A `subOrganization` entry whose address is byte-identical to
the parent's asserts a second location that does not exist. It would also render
a card duplicating the sidebar.

**Why not a distinct concept:** it shares the brand name, the building, the
phone, the website and the ownership. Nothing about it is separately addressable.

**Proposed treatment:** Sorelle ships as a single-location entry. No
`locations[]`, no `subOrganization` JSON-LD, no separate `restaurants.json`
entry, no `sorelle-mercato` slug.

**Two consequences to flag, both operator calls:**

1. **`hours` understates the building.** Proposed `Tu-Su 17:00-22:00` is the
   dinner restaurant - the entity actually being ranked on a best-italian list.
   Someone reading the detail page will not learn the Mercato is open from 8am.
   The alternative is a combined string, which would misrepresent dinner
   availability. **Recommend dinner-only, and let the Mercato surface in
   editorial body copy if and when that page gets fleshed.**
2. **The prompt's "90 Broad St" is not corroborated.** Own site and Yelp both say
   88. The three-townhome footprint may well span 88-90 on the deed, but no
   source I read publishes 90 as the Mercato's address. Not carried forward.

**Precedent note:** this is a *third* category alongside #17's existing two
(in-scope secondary / out-of-scope secondary) - a same-address sub-venue. If a
second one ever appears, #17 should probably name it explicitly. Filed in
section 11.

---

## 4. The name conflicts - there are three, not two

The prompt flagged Coda del Pesce and Mondo's. **Wild Olive is a third**, and it
is the one with a mechanical consequence.

### 4a. Wild Olive -> `Wild Olive`

Four forms in circulation:

| Form | Where |
|---|---|
| **Wild Olive** | **own site logo and page headers** |
| Wild Olive Cucina Italiana | own site copyright line ("(c) 2026 Wild Olive Cucina Italiana"); Resy venue name |
| Wild Olive Restaurant | own site `<title>`; Google; Cvent; Nextdoor |
| WILD OLIVE | Yelp, Tripadvisor (all-caps listing chrome) |

**Proposed: `Wild Olive`.** The prompt's instinct on "Wild Olive Restaurant" is
confirmed - it appears only in `<title>` tags and directory listings, which is
listing decoration exactly as suspected. "Cucina Italiana" is the legal/entity
form, correctly in the copyright line and on the booking platform, but it is not
what the restaurant calls itself in its own masthead.

**This choice is load-bearing** - see 7b. `Wild Olive Cucina Italiana` +
`cuisine: "Italian"` trips the #18 auto-detect and silently suppresses the
cuisine slot across four display surfaces. `Wild Olive` does not.

### 4b. Coda del Pesce -> `Coda del Pesce` (lowercase `del`)

**The prompt's stated tiebreak - "Own site decides" - does not resolve this,
because the own site contradicts itself.** Reported per the instruction to flag
disagreements.

| Own-site surface | Form |
|---|---|
| About page body prose, multiple occurrences | **Coda del Pesce** |
| Homepage main heading: "Coda del Pesce (Italian for 'tail of the fish')" | **Coda del Pesce** |
| Homepage `<title>` tag | Coda Del Pesce |
| Footer | Coda Del Pesce |

Resolved by adding a sub-rule the recipe implies but does not state: **within a
single site, running prose outranks `<title>` and footer chrome.** Title tags
are SEO-cased and footers are template furniture; neither is anyone writing the
name. The gloss "Italian for 'tail of the fish'" also settles the grammar -
`del` is an Italian preposition and lowercases.

Press corroborates 8-to-2 for lowercase:

- **Coda del Pesce**: Moultrie News, Charleston City Paper, Food Network, Only
  In Your State, Garden and Gun, 10Best, Travel and Leisure, Southern Living
- **Coda Del Pesce**: Eater, Post and Courier

**Proposed: `Coda del Pesce`.** Own-site prose plus an 8-of-10 press majority.
Note this lands on the prompt's "editorial" form - but by a different route than
the prompt specified, and the route matters for the next session.

Slug is unaffected: `coda-del-pesce` either way.

### 4c. Mondo's -> `Mondo's Italian Restaurant`, with a caveat about how I know

| Form | Where |
|---|---|
| **Mondo's Italian Restaurant** | own site `<title>` (via search index); Post and Courier, consistently; Yelp; Restaurantji |
| Mondo's Italian Cuisine | Facebook; Tripadvisor |
| Mondo's | the operator roster; conversational use |

**CAVEAT - the Identity gate for Mondo's is incomplete.** `eatatmondos.com`
returned **HTTP 403** to my fetcher on both `/` and `/new-menu/`. I could not
read the own site directly. The `<title>` above reaches me second-hand through
the search index, and I never saw the logo, header or copyright line - which is
precisely where 4a's answer came from for Wild Olive.

**Proposed: `Mondo's Italian Restaurant`, marked LOW CONFIDENCE**, on P&C's
consistent usage plus the indexed title. **The operator should open
eatatmondos.com and confirm the masthead before this ships.** If the masthead
says "Mondo's Italian Cuisine", that is the answer and P&C is wrong.

**This choice is also load-bearing** - see 7b. Both candidate long forms suppress
the cuisine slot; bare `Mondo's` does not.

---

## 5. Mondo's menu status - the prompt's premise is inverted

The prompt says: *"RECENTLY REOPENED after a major renovation with a SCALED-BACK
MENU per current reviews."* Both halves need correction, and the second is the
#23 "inverted" failure mode - a real thing, framed backwards.

**On "recently":** the reopening was **2025-10-30** (Post and Courier). That is
**just under ten months** before today. Recent in the life of a 27-year
restaurant; not recent in the sense a tagline implies.

**On "scaled-back":** every dated source describes an **expansion**.

- P&C, 2025-10-30: took over the vacant suite next door in the Shoppes of Folly
  Road, **increased dining capacity by about 30 percent**, expanded the kitchen
  with a hybrid wood-fired Neapolitan-style pizza oven, and **served pizza for
  the first time** in the restaurant's history.
- P&C, same piece, owner Chris Orlando: "new dishes, including the pizzas, will
  roll out gradually... We'll test things out and the things that stick, will
  end up on the menu."
- Current listing copy: "The menu is being revamped, adding new items and
  changing some favorites, but the dishes remain tasty."
- Current review digest: "the pizza has been phenomenal, though the pizza menu
  changes regularly."

Three independent searches for a reduced or limited Mondo's menu returned
nothing. **No source supports "scaled-back."**

**What is true, and what the prompt was probably reaching for:** the menu is
**in flux**. A deliberately gradual rollout, dishes being tested and dropped, a
pizza menu that "changes regularly" - a diner mid-rollout could easily describe
that as a smaller menu than they remembered. The direction is wrong but the
**operational conclusion is identical and stands**: no dish-level claim about
Mondo's is safe to publish, because the menu is not stable.

**And I could not do the check the prompt asked for.** "Verify anything that
goes into copy against the current menu" - `eatatmondos.com/new-menu/` is 403 to
me, as is the Sirved mirror. **The current menu was not read.** The draft
therefore carries no Mondo's dish reference of any kind, which is the safe
outcome either way, but the gate is open rather than passed.

---

## 6. STEP 3 - schemaType

Per `_detail-page-template.html` intentional decision #4 - "override to the
most-specific applicable subclass of FoodEstablishment when accurate" - as
amended by #19 on 2026-08-26.

**Proposed: `Restaurant` for all five.**

### Coda del Pesce - the one the prompt asked about

The question was whether Italian seafood argues for a seafood-specific subclass.
**It does not, and the reason is decisive rather than judgemental: schema.org has
no seafood subclass of `FoodEstablishment`.**

The complete set of direct subclasses is `Bakery`, `BarOrPub`, `Brewery`,
`CafeOrCoffeeShop`, `Distillery`, `FastFoodRestaurant`, `IceCreamShop`,
`Restaurant`, `Winery`. There is no `SeafoodRestaurant`. #19's amendment that
the docblock list is "illustrative, not an allowlist" widens the field to *any
real schema.org subclass* - but it cannot conjure a type that does not exist.

So "most-specific applicable" bottoms out at `Restaurant`. This is a different
failure from best-ramen's Bar Weems case: there, two **siblings** existed and
depth could not break the tie, so accuracy did. Here there is **no sibling to
consider at all** - the chain simply ends.

**In-repo precedent confirms it.** `chubby-fish` carries `cuisine: "Seafood"`
and `schemaType: "Restaurant"`. A seafood restaurant already ships `Restaurant`
in this tree.

The seafood signal is not lost - it lives in `cuisine` / `servesCuisine`
("Italian Seafood"), which is where an entity-resolution graph reads it. Putting
it in `@type` was never available.

### The other four, briefly

- **Wild Olive** - `Restaurant`. No competing subclass.
- **Le Farfalle** - `Restaurant`. "Osteria" is an editorial register, not a
  schema.org type.
- **Sorelle** - `Restaurant`. The in-venue mercato might invite a market/store
  type; the *ranked entity* is the dinner restaurant, and the mercato is a room
  inside it (section 3). Same reasoning that keeps it out of `locations[]`.
- **Mondo's** - `Restaurant`. The new wood-fired oven might invite a
  pizza-specific type; none exists, and all five of this tree's pizza
  restaurants already ship `Restaurant`.

Distribution after this launch: `Restaurant` 30 -> 35, others unchanged
(`CafeOrCoffeeShop` 5, `IceCreamShop` 3, `FoodEstablishment` 2, `Bakery` 1).

---

## 7. STEP 3 - slug, dedup, social card. All run, none predicted.

### 7a. Slug collisions - none

Checked programmatically against `data/restaurants.json`, `data/og_rankings.json`,
`restaurants/*.html` and `rankings/*.html`.

| Proposed slug | Collides? |
|---|---|
| `best-italian` | no - absent from og_rankings.json and rankings/ |
| `wild-olive` | no |
| `coda-del-pesce` | no |
| `le-farfalle` | no |
| `sorelle` | no |
| `mondos-italian-restaurant` | no |
| `mondos` (alternative) | no |
| `mondos-italian-cuisine` (alternative) | no |

All three Mondo's spellings are free, so 4c's naming question can be resolved on
the merits without slug pressure.

### 7b. Cuisine dedup - RUN, not predicted, and it fires twice

`scripts/_cuisine_dedup.py` has no `__main__` block - it is a shared module, not
a CLI. Imported and called `_resolve_display_cuisine()` /
`_should_suppress_cuisine()` directly against the proposed records, including the
rejected name variants.

```
NAME                             CUISINE            SUPPRESS  DISPLAY RESULT
--------------------------------------------------------------------------------
Wild Olive                       Italian            False     'Italian'
Wild Olive Cucina Italiana       Italian            True      None
Coda del Pesce                   Italian Seafood    False     'Italian Seafood'
Le Farfalle                      Italian            False     'Italian'
Sorelle                          Southern Italian   False     'Southern Italian'
Mondo's                          Italian            False     'Italian'
Mondo's Italian Restaurant       Italian            True      None
Mondo's Italian Cuisine          Italian            True      None
```

**All five proposed entries pass clean** - no suppression, no `displayCuisine`
override needed, cuisine renders on every display surface.

**But two rejected name forms suppress, and that is the finding.** The naming
decisions in section 4 are not cosmetic:

- **`Wild Olive Cucina Italiana`** suppresses. Normalisation lowercases and
  strips punctuation, and `"italian"` is a substring of `"italiana"`. Choosing
  the copyright-line form would silently drop the cuisine slot from the detail
  `<title>`, `og:title`, `twitter:title`, the hero subtitle and the OG image
  meta-line.
- **Both Mondo's long forms** suppress, for the obvious reason - the cuisine word
  is in the name.

**This is a live decision, not a defect.** For Mondo's the suppression is
arguably *correct*: "Mondo's Italian Restaurant - Italian in Charleston" is
exactly the redundancy #18 was written to kill, and the auto-detect handling it
without an override is the mechanism working. For Wild Olive it would be a
**false positive** of the kind #18's trade-off section anticipates - "Italiana"
is not the cuisine word, it is a coincidental substring - and `displayCuisine`
is the documented escape hatch.

**Recommendation:** take `Wild Olive` (no suppression, no override, nothing to
explain) and let Mondo's suppression stand if the long form is confirmed. **Flag
both to the operator rather than deciding silently**, since both follow from a
naming call that is still open in 4c.

### 7c. Social card - CORRECTED 2026-08-26, this section was wrong

> **This section originally concluded "there is no derivation." That is false,
> and the error is preserved below with the correction, because the shape of the
> mistake matters more than the conclusion.** Two category paths exist. I
> examined only the Python one, found no derivation there, and generalised to
> the whole pipeline. Worse, I cited `best-tex-mex` -> `"Tex-Mex"` as *proof* -
> but that is the `og_rankings.json` value feeding the **Python** path, so I used
> evidence from one pipeline to make a claim about the other. The 2026-08-24
> investigation's record was right; mine was wrong. Full correction in section
> 13b.

The prompt asks to "confirm `best-italian` titleCases cleanly through the social
card derivation."

**The OG-image path has no derivation.** `render_ranking()` in
`scripts/generate_og_images.py` reads:

```python
Category=entry['category'],
SpotsLabel=pluralize_spots(entry['spots']),
```

`category` is a **hand-authored string field** in `data/og_rankings.json`, not a
transform of the slug. `og-templates/ranking.html` documents it as
`{{Category}} display name, e.g. "Pizza"` and renders it verbatim. Precedent
confirms hand-authoring rather than derivation: `best-new-coffee-shop` ->
`"New Coffee Shop"`, `best-frozen-margarita` -> `"Frozen Margarita"`,
`best-tex-mex` -> `"Tex-Mex"` (a slug-derived titlecase would give "Tex Mex").

So on the **OG-image** path nothing is computed and nothing can go wrong. The
value to type is `"Italian"`, and the only mechanical step is
`pluralize_spots(5)` -> `"5 spots"`, correct for a Top-5.

Rendered card reads: **Italian** / "As voted by Charleston locals [MID] 5 spots".
Verified after rendering - the shipped `og-best-italian.png` reads exactly that.

**The social-card path is a different story - see section 13b.** `loadTopN()` in
`social/src/data.ts` *does* derive the category from the slug, and it drops
hyphens. `best-italian` is a single token so both paths agree here; `best-tex-mex`
already diverges in production.

### 7d. Chrome baseline - measured, not inherited

`python scripts/inline_chrome.py --check` -> `[OK] 62 files in sync`, exit 0.

Matches #19's documented 62. Recorded because the recipe says to measure rather
than hardcode. **Post-launch target is 68** (62 + 1 ranking + 5 detail pages),
and the refresh must be run *after* all six new files exist.

---

## 8. STEP 5 - the registry grid at 14 categories

**The prior claim is half right and should not be inherited.** The prompt is
correct to be suspicious.

Measured, not assumed: the homepage grid block contains exactly **13** cards, on
`index.html:167`, class `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4`. (The
other 26 `/rankings/` hrefs in the file are the desktop and mobile nav chrome
inside the AUTOGENERATED block - scoped out per #23's live-verification
corollary, which is the same trap that produced two false defect reports last
week.)

| N | base `grid-cols-1` | `md:grid-cols-2` | `lg:grid-cols-4` |
|---|---|---|---|
| 13 (today) | clean | 6 rows + **orphan of 1** | 3 rows + **orphan of 1** |
| **14 (this launch)** | clean | **7 rows, CLEAN** | 3 rows + **orphan of 2** |

**Verdict: 14 returns to clean at `md`, and does NOT at `lg`.** "Clean at both"
is wrong. 14 = 2 x 7 exactly, so the two-column breakpoint resolves; 14 mod 4 = 2,
so the four-column breakpoint leaves a trailing row half-filled.

The prompt's arithmetic instinct - "14 does not divide evenly by 4" - is the
correct one and is the half the prior analysis missed.

Worth noting the orphan gets *visually* worse at `lg` even as the total improves:
13 leaves one card alone on a row, 14 leaves two, which reads more like a gap
than a deliberate trailing item. That is an aesthetic judgement, not a break.

**Recommendation: change nothing.** #19's rule is "adjust only if a count
genuinely breaks the layout", and a partially-filled final row is the normal
resting state of any responsive grid whose item count is not a multiple of the
column count. The alternatives are all worse: `lg:grid-cols-7` is absurd at card
width, and dropping to `lg:grid-cols-3` would give 4 rows + orphan of 2 while
making every card wider and the section taller. **No `grid-cols` edit in this
PR.** Next clean-at-`lg` count is 16.

**Adjacent open TRACKED item, deliberately NOT folded in.** TRACKED line 23 asks
for `id="rankings"` on this exact `<div>` ("near `index.html` line 158-160"),
held "until post-May-20 because it's a chrome edit during the GSC quiet window".
That window has passed, and this PR touches the very element. It is still a
separate concern with its own rationale and should ship on its own merits, not
be smuggled in because a launch happened to open the file. **Raised, not
actioned.**

---

## 9. STEP 4 - drafted content. DRAFT ONLY, nothing applied.

### 9a. Ranking length and subtitle

Top-5. Per #23 / #20, **Top-5 takes no count framing** - "Top-5 and Top-7: no
count-framing, slate is full as-is". Verified against the tree rather than the
doc: `best-pizza.html:315` and `best-tex-mex.html:315` both read exactly:

```
As voted by Charleston locals
```

No trailing period, no count clause. `best-ramen.html:270`, a Top-2, carries the
count framing - confirming the split is real and not drift.

**Proposed subtitle: `As voted by Charleston locals`** - byte-identical to the
Top-5 precedent.

**No NEW pill** - retired entirely for all page shapes (#19, 2026-08-26), and it
was never available to Top-N anyway (#23).

### 9b. Taglines - three clean, one flagged, one needs replacing

Assessed against both #23 tests: **unsourced** ("can you cite it?") and
**inverted** ("does your framing match the source's?").

**1. Wild Olive - "Island Trattoria, Handmade Pasta" -> FLAGGED, half unsourced**

- *"Handmade Pasta"* - **GROUNDED**, multiply sourced. Chef bio: Brad Grozis's
  "specialty being signature house-made pasta and house-cured salumi". Review
  digest: "all handmade pasta and quality food"; "House made pasta is the heart
  and soul of the menu."
  **Caveat worth stating:** the own menu does *not* use this language. It lists
  the pasta dishes (Baked Penne, Bavette, Ravioli, Agnolotti) with no
  preparation claim. So the phrase is sourced to a chef bio and reviews, not to
  the restaurant's own menu. That is admissible - it is converging third-party
  evidence about the food - but it is a weaker footing than Le Farfalle's
  focaccia, which is on the menu verbatim.
- *"Island Trattoria"* - **UNSOURCED.** "Island" is fine (Johns Island). But
  **no source calls Wild Olive a trattoria.** The own site calls itself
  *Cucina Italiana*; Charleston Magazine calls it "sophisticated rustic
  Italian"; Yelp says Italian. *Trattoria* is a specific category claim -
  casual, family-run - and it is being applied to a restaurant that positions
  upmarket and takes Resy bookings. This is an editorial coinage, and it fails
  "can you cite it?"

  **Proposed replacements**, in order of preference:
  - `Island Cucina, Handmade Pasta` - "Cucina" is the restaurant's own word.
  - `Johns Island Italian, Handmade Pasta` - flatly factual, loses some music.

**2. Coda del Pesce - "Oceanfront Italian, Seafood Led" -> CLEAN, ship as-is**

Both halves multiply sourced.
- *Oceanfront*: Garden and Gun, "sourced from right outside the dining room's
  expansive beach-facing windows"; Only In Your State, "sweeping views of the
  Atlantic Ocean"; Southern Living, "floor-to-ceiling windows"; Travel and
  Leisure, "on the front beach of Isle of Palms"; own site, "stunning ocean
  views"; and the address is literally 1130 Ocean Blvd, 2nd floor.
- *Seafood Led*: own site, "his all Italian seafood restaurant" and "Most every
  dish... features fresh, locally or sustainably caught seafood."

Not inverted: every source frames the ocean and the seafood as the draw, which
is how the tagline uses them.

**3. Le Farfalle - "Downtown Osteria, Rosemary Focaccia" -> CLEAN, one note**

- *Rosemary Focaccia*: **GROUNDED on the own menu, verbatim.** The item is
  "**Warm Rosemary Focaccia**" - "Tomato Sugo, Whipped Ricotta & Olive Oil",
  $10. Charleston Magazine independently calls it "a delight". Strongest
  grounding of any dish reference on this roster.
- *Downtown*: own site, "nestled downtown in the beautiful and quaint Harleston
  Village".
- *Osteria*: **sourced, but not self-applied.** Charleston Magazine: "Michael
  Toscano's Italian osteria". A DINEvent piece titles it "Le Farfalle Osteria".
  The own site says "regional Italian restaurant" and does not use the word.
  Citable to named editorial, so it passes - but it is third-party register,
  not the restaurant's own. **Noted, not flagged.** If the operator wants
  own-site language throughout, `Regional Italian, Rosemary Focaccia` is the
  swap.

**4. Sorelle - "Three Floors, Southern Italian" -> CLEAN, and it survived a
scare**

- *Three Floors*: **GROUNDED.** I initially suspected this was an inversion of
  "three historic townhomes" - a horizontal fact rendered as a vertical one,
  which would have been a textbook #23 inverted claim. **It is not.** The
  building is both. Design press describes a "three-story concept" and places
  each level: **first floor** mercato, cafe, wine room and bar; **second floor**
  main dining room, marble pasta counter and chef's table; **third floor**
  private dining with a ten-person marble table. Three townhomes *and* three
  floors, independently attested.
- *Southern Italian*: **GROUNDED.** Michelin Guide, "modern approach to Southern
  Italian food"; Charleston Magazine, "Southern Italian fare"; chef Nick Dugan's
  own positioning via MINA Group / Beemok.

Recorded because "verify the thing that looks like an inversion" is what the
recipe asks for, and this time the answer was that the copy was right.

**5. Mondo's - "James Island Standby, Newly Renovated" -> NEEDS REPLACING**

- *"James Island Standby"* - **GROUNDED, near-verbatim.** A listing digest reads
  "Mondo's has been a **James Island standby** since the late '90s serving
  red-sauce classics and generous portions." P&C independently: "a James Island
  fixture for 27 years." Keep this half.
- *"Newly Renovated"* - **DECAYING, recommend against.** The reopening was
  2025-10-30, **ten months ago**, and the tagline is a permanent field on a page
  with no expiry mechanism. This is structurally the same objection that retired
  the NEW pill: #19 gave the pill a 60-day decay rule precisely because novelty
  claims go stale, then the whole convention was withdrawn because the decay had
  to be remembered by hand and **the evidence says launches forget**
  (`best-bakery`'s pill shipped 52 days late; PR #48/#49 cleaned up two of them).
  Writing "Newly" into a tagline re-introduces exactly that maintenance debt, in
  a field with no decay rule at all.

  Two independent reasons to drop it, not one: it decays, **and** section 5
  shows the renovation framing the prompt supplied is inverted.

  **Proposed replacements**, all sourced to P&C's reopening coverage:
  - `James Island Standby, Wood-Fired Pizza` - **preferred.** Durable, concrete,
    and the pizza oven is the single most-reported fact about the reopening.
  - `James Island Standby, Red-Sauce Classics` - safest of all; "red-sauce
    classics" is quoted verbatim from a current listing and is immune to the
    menu being in flux.
  - `James Island Standby, Since the Late '90s` - pure longevity, zero menu risk.

  **Caution on the pizza option**, given section 5: pizza is confirmed present
  and confirmed praised, but the *pizza menu* "changes regularly". "Wood-Fired
  Pizza" asserts a capability (there is a wood-fired oven and it makes pizza),
  not a dish, so it survives menu churn. **A specific pizza would not.** If the
  operator wants zero menu exposure, take the red-sauce or longevity option.

### 9c. `servesCuisine` - list-scoped, proposed not decided

Per #23: ranking-page ItemList `servesCuisine` is hand-authored per list, "not a
copy of `restaurants.json.cuisine`" - override the generic, preserve the
specific. Flagged rather than decided, as the recipe requires.

| Restaurant | `restaurants.json.cuisine` | Proposed ItemList `servesCuisine` | Rule applied |
|---|---|---|---|
| Wild Olive | Italian | **Italian** | no-op - see below |
| Coda del Pesce | Italian Seafood | **Italian Seafood** | preserve the specific |
| Le Farfalle | Italian | **Italian** | no-op - see below |
| Sorelle | Southern Italian | **Southern Italian** | preserve the specific |
| Mondo's | Italian | **Italian** | no-op - see below |

**This list exposes a case the rule does not anticipate, and it should be
recorded.** #23's mechanism assumes the *data* is generic and the *list* is
specific - `American` on a burger list becomes `Burgers`. Here the list category
**is** the generic term. "Italian" is simultaneously the honest cuisine value
for three of these restaurants and the name of the ranking they sit on, so the
"override the generic with the list's category" step is a no-op: the override
and the original are the same string.

That leaves the second half of the rule doing all the work - **preserve the
specific** - which cleanly keeps `Italian Seafood` and `Southern Italian` rather
than flattening both to `Italian` for list consistency. Flattening would be the
tempting move and would destroy real entity-resolution signal.

**Two open questions for the operator:**

1. **Le Farfalle: `Italian` or `Regional Italian`?** Its own site says "a
   regional Italian restaurant". `Regional Italian` is more specific and
   sourced. Against: it is a self-description rather than a recognised cuisine
   genre, and it reads oddly next to `Southern Italian` (which names an actual
   region) in the same ItemList.
2. **Consistency vs specificity across the list.** Three `Italian`, one
   `Italian Seafood`, one `Southern Italian` is heterogeneous by design. #23
   endorses that (Home Team BBQ keeps `Barbecue` on three lists), but it is a
   visible editorial choice on a page where all five rows are the same cuisine
   family.

### 9d. Proposed `restaurants.json` entries - DRAFT

Field policy: required fields filled, optional fields `null` where not
collected. **Empty string is never valid.** Values below carry a confidence
mark: **[V]** verified against own site plus at least one independent source;
**[S]** single-source or search-summary only, wants a firmer read before
shipping; **[?]** open operator decision.

Common to all five: `schemaType: "Restaurant"` [V], `monthYear: "August 2026"`,
`geoLat`/`geoLng`/`imageURL`/`editorialBody`/`areaServed`/`locations` all `null`
(matching every recent launch - stub-then-flesh per intentional decision #1),
`appearsOn` = the single `best-italian` entry, `displayCuisine` absent.

**1. `wild-olive`**
```
name           Wild Olive                                          [?] see 4a
tagline        Island Cucina, Handmade Pasta                       [?] see 9b
cuisine        Italian                                             [V]
neighborhood   Johns Island                                        [V]
streetAddress  2867 Maybank Hwy                                    [V]
locality       Johns Island        region SC    ZIP 29455          [V]
phone          +1-843-737-4177                                     [V]
hours          Mo-Th 17:00-22:00,Fr-Sa 16:00-23:00,Su 16:00-22:00  [V]
priceRange     null                                                [?] see 9e
websiteURL     https://www.wildolive.com                           [V]
```

**2. `coda-del-pesce`**
```
name           Coda del Pesce                                      [V] see 4b
tagline        Oceanfront Italian, Seafood Led                     [V]
cuisine        Italian Seafood                                     [V]
neighborhood   Isle of Palms                                       [S] see 9e
streetAddress  1130 Ocean Blvd                                     [?] floor, 9e
locality       Isle of Palms       region SC    ZIP 29451          [V]
phone          +1-843-242-8570                                     [V]
hours          Tu-Sa 17:30-21:00                                   [V]
priceRange     $$$                                                 [S]
websiteURL     https://codadelpesce.com                            [V]
```

**3. `le-farfalle`**
```
name           Le Farfalle                                         [V]
tagline        Downtown Osteria, Rosemary Focaccia                 [V]
cuisine        Italian                                             [?] see 9c
neighborhood   Harleston Village                                   [V] own site
streetAddress  15 Beaufain St                                      [V]
locality       Charleston          region SC    ZIP 29401          [V]
phone          +1-843-212-0920                                     [V]
hours          Su-We 17:00-21:30,Th-Sa 17:00-22:00                 [V]
priceRange     $$$                                                 [S]
websiteURL     https://www.lefarfallecharleston.com                [V]
```

**4. `sorelle`**
```
name           Sorelle                                             [V]
tagline        Three Floors, Southern Italian                      [V]
cuisine        Southern Italian                                    [V]
neighborhood   Downtown                                            [?] see 9e
streetAddress  88 Broad St                                         [V]
locality       Charleston          region SC    ZIP 29401          [V]
phone          +1-843-974-1575                                     [V]
hours          Tu-Su 17:00-22:00                                   [V] dinner only, see 3
priceRange     $$$                                                 [S]
websiteURL     https://www.sorellecharleston.com                   [V]
```

**5. `mondos-italian-restaurant`**
```
name           Mondo's Italian Restaurant                          [?] LOW CONF, 4c
tagline        James Island Standby, Wood-Fired Pizza              [?] see 9b
cuisine        Italian                                             [V]
neighborhood   James Island                                        [V]
streetAddress  915 Folly Rd                                        [V]
locality       Charleston          region SC    ZIP 29412          [V]
phone          +1-843-795-8400                                     [V]
hours          Mo-Sa 16:00-21:00                                   [V]
priceRange     null                                                [?] see 9e
websiteURL     https://eatatmondos.com                             [S] 403 to fetcher
```

`description`, `shareTagline`, `keywords` and `hoursHumanReadable` are
deliberately **not drafted here** - they follow the tagline and name
resolutions, and drafting prose on top of five open decisions would produce five
prose cascades to redo. They are mechanical once sections 4 and 9b close.

One thing to carry into them, per #23's `neighborhood`/`keywords` rule: **do not
propagate `neighborhood` into `keywords`.** "Harleston Village italian" and
"Johns Island italian" have thin search volume; "downtown Charleston italian"
and "Charleston italian restaurant" do the real work. Re-ask what someone would
type rather than find-and-replacing the factual string.

### 9e. Open field questions

1. **`priceRange` is soft on all five and mixed in provenance.** Sorelle `$$$`
   is explicit in a listing; Le Farfalle and Coda del Pesce come from a search
   summary describing them as "expensive"; Wild Olive and Mondo's returned
   nothing. Proposing `null` for the two unsourced ones per the field policy
   ("empty-and-honest > filled-and-fabricated") and `$$$` marked **[S]** for the
   three. **Recommend re-deriving all five from one consistent source** rather
   than shipping a mix of listing data and prose adjectives - a `$$$` derived
   from the word "expensive" is an inference, not a reading.
2. **Sorelle's `neighborhood`.** 88 Broad St. `South of Broad` would be **wrong**
   - that district is south of the street, and 88 Broad is on it. Sourced
   options: `Downtown` (the site's own Mercato copy says "88 Broad Street in
   Historic Downtown Charleston") or `Broad Street` (a corridor, not a
   neighborhood). **Proposing `Downtown`**, flagged, and letting `keywords` do
   the search work per the Bar Weems precedent.
3. **Coda del Pesce's `neighborhood`.** `Isle of Palms` duplicates
   `addressLocality`, which is a little redundant on the "Cuisine [MID]
   Neighborhood" meta-line. `Front Beach` is what Travel and Leisure's phrasing
   implies but no source states it as a neighborhood name. **Proposing
   `Isle of Palms`** and accepting the redundancy over inventing a district.
4. **Coda del Pesce's "2nd Floor".** The own site publishes "1130 Ocean Blvd,
   2nd Floor". No `streetAddress` in the tree carries a unit designator.
   **Proposing plain `1130 Ocean Blvd`** for consistency; the floor is real and
   could go in editorial body copy later.
5. **Sorelle's hours understate the building** - see section 3.

---

## 10. Files this PR would touch

Per #23's step sequence. **Not applied.** Estimated **21 files**, of which 12 are
new - the largest launch in the tree's history (best-ramen touched 1 net-new
detail page, best-ice-cream 3; this is 5).

**New (12):**

1. `rankings/best-italian.html` - from `_template-canonical.html`, with the
   production JSON-LD pattern (per-item `url` + `datePublished`/`dateModified`
   per #15 Q3), **not** the canonical's bare ItemList. Rows trimmed to 5. Row
   `<h2>` names must be wrapped in
   `<a href="/restaurants/{slug}.html" class="hover:text-brand-orange transition-colors">`
   - the social pipeline's regex requires it and the canonical omits it.
2. - 6. `restaurants/{wild-olive,coda-del-pesce,le-farfalle,sorelle,mondos-italian-restaurant}.html`
   - generated one at a time via `generate_detail_page.py {slug}`, **never
   `--all`**.
7. `assets/images/og-best-italian.png`
8. - 12. `assets/images/og-restaurant-{slug}.png` x5

**Modified (9):**

13. `data/og_rankings.json` - append `{"slug": "best-italian", "category":
    "Italian", "spots": 5}`; bump `_meta.lastUpdated`.
14. `data/restaurants.json` - five new entries; bump `_meta.lastUpdated`.
    41 -> 46 entries.
15. `components/header.html` - desktop dropdown, appended after Best Ramen
    (below the `<div class="h-px bg-gray-100 my-1 mx-4">` divider, inside the
    Top-N cluster); mobile menu, appended after Best Ramen. **No NEW pill.**
    Note the mobile menu has no cluster divider - it is a flat 13-item list, so
    the append point is simply the end.
16. `index.html` - 14th card, `border-transparent hover:border-brand-orange/20`
    like every other. **No `grid-cols` change** (section 8).
17. `vote.html` - `<option>Best Italian</option>` appended at end. Correct for a
    Top-N; the file carries 11 options for 13 rankings because the two featured-1
    pages route through `/suggest-category` per step 8.
18. `sitemap.xml` - regenerated.
19. `_strategy/TRACKED.md` - same-PR file edit per #22 (section 11).
20. `_strategy/DECISIONS.md` - only if the #17 amendment in section 11 is taken.
21. `rankings/_best-italian-launch-analysis.md` - this file.

Plus **62 -> 68 inlined pages** refreshed by `inline_chrome.py --refresh`.

### Ordering constraints that will bite this launch specifically

- **`generate_sitemap.py` runs LAST**, after the `dateModified` normalisation in
  the next bullet. It reads `dateModified` to build `<lastmod>`; run it early and
  the sitemap ships stale dates silently.
- **All five new detail pages will be seeded in UTC.** `generate_detail_page.py`
  writes `2026-08-26T..:..:..+00:00`; every launch page in the tree carries
  `T12:00:00-04:00`. **Five hand-normalisations this time, not one.** This is
  the launch where the open TRACKED item stops being a nuisance and becomes a
  five-fold repetition - see section 11.
- **ItemList JSON-LD must precede BreadcrumbList** in `best-italian.html`.
  `generate_sitemap.py` parses only the first `ld+json` block; invert them and
  `<lastmod>` vanishes with no error.
- **All six new pages must exist before `inline_chrome.py --refresh`**, or they
  ship with stale chrome and `--check` exits 2. Target 68.
- **`npm run build:css`: expected NOT needed.** Copying existing pages
  introduces no new utility classes. Verify with a class-set diff rather than
  running it reflexively.
- **Playwright Chromium must be installed** before `generate_og_images.py` -
  `python -m playwright install chromium`, ~87 MB. Not verified this session
  (no image generation attempted in an analysis pass).
- **Squash subject must be set explicitly**: `feat: ... (#N)`. GitHub defaults to
  the PR title, which is prose and would land on `main` without a type prefix.

### PR shape

Unlike best-ramen, **no split is needed.** That split existed because a
pre-existing entry carried wrong data that had to be corrected before the launch
regen stamped a fresh `dateModified` over it. Here all five are net-new, there
is nothing to correct, and #23 rule 4 does not fire. **Single PR.**

The one thing that could force a split is section 1b - if the operator adds
`ok-donna`, that is a pre-existing entry, rule 4 fires, and its `phone: null`
and stale `monthYear` want resolving before the bump.

---

## 11. TRACKED entries this launch would generate

Same-PR file edits per #22 - prose in a PR description does not count as filing.

**No exclusion records.** All five candidates cleared both gates; there is no
conflict, no closure and no contested location set to file. First launch since
best-frozen-margarita with a clean sheet.

To file:

1. **Mondo's own-site Identity gate incomplete.** `eatatmondos.com` returned
   HTTP 403 to automated fetching on both `/` and `/new-menu/`. The name form
   and the current menu were never read at source. Re-verification trigger: open
   the site in a browser and confirm the masthead brand form before the entry
   ships; re-check the menu before any dish-level copy is ever added to that
   page. **Blocks nothing in the current draft** (no Mondo's dish reference), but
   the gate is open, not passed.
2. **`priceRange` unsourced or weakly sourced across all five.** Two proposed
   `null`, three proposed `$$$` from prose adjectives rather than listing data.
   Trigger: next time these entries are edited, or before any price-based
   surface is added.
3. **`generate_detail_page.py` UTC seeding - five hand-normalisations.** The
   existing item (TRACKED line 127) proposes the generator fix as the better
   remedy. This launch is the strongest evidence yet: the workaround scales
   linearly with roster size, and a five-page launch is five chances to forget.
   **Recommend the generator fix land before or with this launch** rather than
   adding five more manual steps. If it does, the three legacy `+00:00` pages
   (`little-jacks-tavern`, `pubfare-burger`, `weltons-tiny-bakeshop`) can be
   normalised in the same pass and the item closed outright.
4. **Coda del Pesce's own site is stale on its own portfolio.** The About page
   presents Trattoria Lucca (closed 2020) in the present tense and omits Volpe.
   No action - the entry cites nothing from that page except the name spelling,
   which is exactly the field an own site *is* authoritative for. Filed as a
   no-trigger record so a future session does not re-derive the same finding, and
   as a clean citable example of the identity/status split for #23.
5. **Sorelle Mercato - the same-address sub-venue case.** #17 currently
   distinguishes in-scope from out-of-scope secondaries. It has no language for a
   sub-venue sharing the parent's street address, phone and website. Recommend a
   short amendment recording the determination and its test - *does it have its
   own address?* - so the next launch does not re-litigate it. Alternatively
   record it here only and amend #17 when a second instance appears; **the
   recipe's own precedent is to wait for the second case** (#23's Top-N recipe
   was deferred until a second Top-N launch), so **deferring is the more
   consistent choice** and is what I would recommend.
6. **`servesCuisine` when the list category is itself the generic term.** New
   case, section 9c. Worth a line in #23 whenever it is next amended, since the
   "override the generic" half of the rule no-ops and only "preserve the
   specific" does any work.

Adjacent, **not** filed by this launch and **not** actioned: TRACKED line 23's
`id="rankings"` anchor on the homepage grid `<div>` (section 8).

---

## 12. Where this prompt and the recipe/tree disagree

Reported per the instruction, in descending order of consequence.

1. **Mondo's "scaled-back menu" is inverted.** Every dated source describes an
   expansion - 30 percent more capacity, a new wood-fired oven, pizza for the
   first time in 27 years. Three searches for a reduced menu returned nothing.
   The real phenomenon is a **gradual rollout** ("we'll test things out and the
   things that stick, will end up on the menu"), which a diner could reasonably
   experience as a smaller menu. **The prompt's operational instruction survives
   intact and should be followed** - the menu is unstable, so no dish-level claim
   is safe - but the premise behind it is backwards, and a future session should
   not inherit "scaled back" as fact.

2. **The tree-first hypotheses are all false.** Sorelle and Le Farfalle are not
   on best-nice-restaurants; Mondo's is not on best-casual-spots; none of the
   five is anywhere in `data/restaurants.json` or `restaurants/`. **All five are
   net-new.** This is the mirror image of best-ramen - there the check found an
   entry the prompt thought was new; here it found nothing where the prompt
   expected three. The check earned its place both times.

3. **The roster has zero bench, which the recipe forbids outright.** "Never zero
   bench, whatever the provenance." Five supplied for a Top-5, all net-new. It
   held - all five passed - and at N=5 a failure would have been editorial
   (drop to Top-4, a documented length) rather than structural. But the recipe's
   rule is unconditional and this roster does not satisfy it. **`ok-donna` is
   already in the tree with `cuisine: "Italian"` and would have been a
   near-zero-cost bench** (section 1b).

4. **"Own site decides" does not resolve Coda del Pesce.** The site is
   internally inconsistent - prose says `Coda del Pesce`, `<title>` and footer
   say `Coda Del Pesce`. Resolved by a sub-rule the recipe implies but never
   states: **within one site, running prose outranks title-tag and footer
   chrome.** Press corroborates 8-to-2 for lowercase. The answer matches the
   prompt's expected form; **the stated method did not produce it**, and that is
   the part worth recording.

5. ~~**There is no social-card "derivation" to verify.**~~ **RETRACTED - this
   was my error, not the prompt's.** A derivation does exist, in
   `social/src/data.ts`. My claim was scoped to the Python OG-image path and
   wrongly generalised, and the `best-tex-mex` evidence I cited came from the
   *other* pipeline. `best-tex-mex` renders as "Tex Mex" through the social
   path - hyphen lost - while `og_rankings.json` correctly says "Tex-Mex".
   Corrected in 7c, diagnosed in 13b, filed in TRACKED. Moot for
   `best-italian`, which is a single token and comes out "Italian" either way.

6. **"14 returns to clean at both breakpoints" is half wrong** - and the prompt's
   suspicion is the correct half. 14 is clean at `md:grid-cols-2` (7 rows
   exactly) and orphaned at `lg:grid-cols-4` (3 rows + 2). Recommendation is
   still to change nothing; a half-filled final row is not a broken layout.

7. **Sorelle Mercato is at 88 Broad St, not 90.** Own site and Yelp agree on 88 -
   the same address as Sorelle, which is most of why it is not a second location.
   The prompt's 08:00-16:00 daily is correct.

8. **Wild Olive has a name conflict the prompt did not anticipate, and it is the
   one that matters mechanically.** The prompt flagged "Wild Olive Restaurant"
   as listing decoration - correct, confirmed. But the own site's copyright line
   and its Resy listing both say **"Wild Olive Cucina Italiana"**, a third form,
   and that form **trips the #18 cuisine-dedup auto-detect** ("italian" is a
   substring of "italiana"), silently suppressing the cuisine slot on four
   display surfaces. Verified by running `_cuisine_dedup.py`, not predicted.

9. **Wild Olive's chef attribution is imprecise.** The prompt says "Chef Jacques
   Larson". Larson is the **founder** - Charleston Magazine still frames it as
   "Chef Jacques Larson's Wild Olive" - but the current **Executive Chef is Brad
   Grozis**, per the own site and a 2026 bio. Both statements are defensible if
   worded carefully; "Chef Jacques Larson" presented as current is the inverted
   form. **No impact on the current draft** - no proposed tagline names a chef -
   but it would matter the moment editorial body copy is written, and the
   "handmade pasta" grounding traces partly to Grozis's bio.

10. **"Island Trattoria" is unsourced.** No source calls Wild Olive a trattoria;
    its own word is *Cucina*. Flagged with replacements in 9b.

11. **"Newly Renovated" decays and should not ship in a permanent field.** The
    reopening was 2025-10-30, ten months ago. This is the objection that retired
    the NEW pill (#19), reappearing in a field that has no decay rule at all.

12. **Le Farfalle's hours are correct as supplied**, but only after three reads -
    an early own-site fetch mis-transcribed the day range and a search summary
    asserted a Monday closure no primary source supports. Recording the shape
    because it is a new variant of a documented trap: **a bad read of a good
    source is indistinguishable from a source conflict** until you re-read.

13. **Le Farfalle serves no brunch**, contrary to a search summary. Both own-site
    pages say "Dinner Only". Not carried into the draft.

14. **Mondo's Identity gate could not be completed** - `eatatmondos.com` is 403
    to automated fetching. The name form is second-hand via the search index and
    the current menu was never read, so the prompt's "verify anything that goes
    into copy against the current menu" was **not satisfiable this session**.
    The draft carries no Mondo's dish reference, so nothing unsafe follows, but
    the gate is open rather than passed and the operator should close it by hand.

---

---

## 13. Resolutions and corrections (build pass, 2026-08-26)

### 13a. Operator resolutions

| Question | Resolution |
|---|---|
| Mondo's name | **`Mondo's Italian Restaurant`.** Own-site masthead logo and page heading both read "Italian Restaurant"; the "Italian Cuisine" form in body prose is casual drift. |
| Mondo's hours | **`Mo-Sa 16:00-21:00`**, Sunday closed - confirmed on the own site and matching Google. Shipped as drafted. |
| Coda del Pesce | **`Coda del Pesce`**, lowercase `del`, per 4b. |
| `ok-donna` | **Excluded.** Zero bench **accepted as a known risk**, not overlooked. Filed in TRACKED as a record rather than a task. |
| Wild Olive | **`Wild Olive`** - see 13c. Dedup does not fire; no `displayCuisine` override. |
| Taglines | Coda del Pesce, Le Farfalle, Sorelle unchanged. Wild Olive and Mondo's replaced - see 13d. |

**The surface-authority hierarchy, now stated explicitly.** The operator's Mondo's
ruling generalises the sub-rule 4b had to invent for Coda del Pesce, and the two
agree. Ordered by **how deliberate the surface is**:

> **logo / masthead > headings > body prose > title tag and footer chrome**

The reasoning is that each step down is less considered than the one above.
A logo is designed once and signed off; a heading is written deliberately; body
prose is written fluently and drifts; a `<title>` is written for search engines
and a footer is template furniture nobody re-reads. This **extends** 4b rather
than contradicting it - 4b only needed the bottom half of the ladder (prose beats
title tag and footer), and Mondo's needed the top half (masthead beats prose).
Both launches now resolve name conflicts with one rule.

### 13b. Correction: two category paths exist, and they disagree

**My section 7c was wrong.** The 2026-08-24 investigation's record is the correct
one. Both paths exist and they are genuinely independent:

| Surface | Code | Mechanism | `best-tex-mex` |
|---|---|---|---|
| OG image (PNG) | `scripts/generate_og_images.py` `render_ranking()` | reads `entry['category']` **verbatim** from `og_rankings.json` | **"Tex-Mex"** (correct) |
| Social card | `social/src/data.ts` `loadTopN()` | **derives from the slug** | **"Tex Mex"** (hyphen lost) |

The derivation:

```ts
const category = slug
  .slice('best-'.length)
  .split('-')
  .map(titleCase)
  .join(' ');
```

Two things make it worse than it first looks:

1. **`loadTopN` is handed the correct value and throws it away.** Its signature is
   `loadTopN(slug: string, _ogEntry: OgRankingEntry)` - the underscore marks the
   og entry as deliberately unused. `og_rankings.json.category` is hand-authored,
   already correct, and sitting right there.
2. **`titleCase` lowercases the tail**: `s[0].toUpperCase() + s.slice(1).toLowerCase()`.
   So it would also flatten any intentional internal capitalisation, not just
   hyphens.

**Verified live at build time**, not read off the source. Running the real loader:

```
--- best-italian ---   category: Italian    title: Best Italian
--- best-tex-mex ---   category: Tex Mex    title: Best Tex Mex
```

Simulated across all 14 slugs, `best-tex-mex` is the **only** current divergence.
`best-italian` is a single token and yields "Italian" on both paths, so this
launch is unaffected - exactly as the prompt predicted. Filed in TRACKED with the
fix (read `_ogEntry.category` instead of deriving) and a trigger: **before the
next hyphenated ranking slug ships**, because the failure is silent.

**The lesson worth keeping** is not "check the TypeScript too." It is that I
proved a negative about a pipeline I had not opened, and then cited evidence from
a *different* pipeline to support it. A negative finding is scoped to where you
looked - the same trap #23 already documents for sourcing questions ("negative
answers are scoped to the question you asked"), here applied to code.

### 13c. Wild Olive: the logo settles it

4a proposed `Wild Olive` but could not read the masthead - the logo is an image
(`WO_logo_lockup_round_color_1-edit.png`) with **no alt text, no `aria-label`, no
`title` attribute**, and the site publishes no `og:site_name` and no JSON-LD. The
page heading reads "CUCINA ITALIANA / JOHNS ISLAND, SOUTH CAROLINA", which on its
own could be read either way.

Resolved by fetching the logo PNG and looking at it. The lockup carries **four**
text elements at **three** type sizes:

| Element | Size | Role |
|---|---|---|
| **WILD OLIVE** | **largest, top arc** | the wordmark |
| CUCINA ITALIANA | small, bottom arc | descriptor |
| JOHNS / ISLAND | small, flanking the mark | locality |

**"CUCINA ITALIANA" is set at the same size as "JOHNS ISLAND".** That is the
decisive detail: if "Cucina Italiana" were part of the name, so would "Johns
Island" be, and nobody would argue the restaurant is called "Wild Olive Johns
Island". Both are descriptors orbiting the wordmark. "Wild Olive Cucina Italiana"
in the copyright line and on Resy is the legal/entity form, which is what those
surfaces are for.

**Shipped `Wild Olive`.** The #18 dedup therefore does **not** fire, and no
`displayCuisine` override was added - none would have been legitimate. Confirmed
in the rendered output: `<title>Wild Olive [EM] Italian in Charleston</title>`,
cuisine slot intact.

### 13d. Final taglines

| Restaurant | Shipped | Status |
|---|---|---|
| Wild Olive | **Island Cucina, House Made Pasta** | replaced |
| Coda del Pesce | Oceanfront Italian, Seafood Led | unchanged |
| Le Farfalle | Downtown Osteria, Rosemary Focaccia | unchanged |
| Sorelle | Three Floors, Southern Italian | unchanged |
| Mondo's Italian Restaurant | **James Island Mainstay, Gorgonzola Pasta** | replaced |

**Wild Olive - "Island Cucina, House Made Pasta".** Every word is the
restaurant's own. *Cucina* is on the logo and is the page heading; *Island* is on
the logo and in the heading's second line; *House made pasta* is quoted verbatim
from the own site's About copy - "House made pasta is the heart and soul of the
menu". This retires "Island Trattoria", which failed the "can you cite it?" test:
no source calls Wild Olive a trattoria, and *trattoria* is a category claim
(casual, family-run) applied to a restaurant that positions upmarket and takes
Resy bookings. **No count**, so nothing decays - the operator's constraint rules
out "Since 2009" and "Seventeen Years" alike, both of which were available and
both of which would rot.

**Mondo's - "James Island Mainstay, Gorgonzola Pasta". Pizza was considered and
rejected on three independent grounds**, and the operator's instinct to ask was
right:

1. **The verification the recipe demands could not be completed.** "Verify the
   oven and pizza are current on the menu, not just announced" - `eatatmondos.com`
   403s on both `/` and `/new-menu/`, as does the Sirved mirror. The own menu was
   never read. Pizza is *reported* present and praised, but on a page I could not
   open.
2. **It is the least settled part of the menu.** Post and Courier quotes the owner
   saying dishes "will roll out gradually - we'll test things out and the things
   that stick, will end up on the menu", and a current review digest says "the
   pizza menu changes regularly". A tagline is a permanent field.
3. **It would misrepresent the restaurant, and the data says so.** The
   customers'-favorites listing - the closest available proxy for what people
   actually order - contains **nine pasta and red-sauce items and zero pizza**:
   Gnocchi Gorgonzola, Italian Sausage Lasagna, Gemelli with Parmesan Cream
   Sauce, Pesto Penne, Rigatoni Bolognese, Spaghetti and Meatballs, Chicken
   Parmigiana, House Made Meatball, Arancini. Leading a 27-year pasta room on a
   ten-month-old oven inverts its own emphasis.

   There is a fourth, site-shaped reason: **the tree already has a `best-pizza`
   Top-5**. Tagging the Italian-list entry "Wood-Fired Pizza" invites the obvious
   question of why it is not on the pizza list.

*Gorgonzola Pasta* is grounded in two independent sources - a menu aggregator
("gorgonzola, cream, red onions, walnuts, tomatoes, and fresh rigatoni") and the
customers'-favorites listing ("Gnocchi Gorgonzola") - **but not in the own
menu**, which is why TRACKED carries a re-verification trigger. *Mainstay* is the
operator's word for what the source calls a "James Island standby since the late
'90s"; synonymous, and neither is a count.

### 13e. What the build confirmed that analysis could only predict

- **The dedup fired exactly as modelled.** `Mondo's Italian Restaurant` suppresses
  the cuisine slot - `<title>Mondo's Italian Restaurant in Charleston</title>`,
  and the OG card meta-line reads "James Island" rather than
  "Italian [MID] James Island". `Wild Olive` does not suppress. `servesCuisine`
  stays raw `"Italian"` in both JSON-LD blocks per #18 rule 5. The suppression
  reads *better* than the alternative, which is #18 working as designed rather
  than a cost.
- **Chrome landed on 68**, the predicted 62 + 6. `--check` exit 0.
- **All ten seeded stamps were UTC**, as the recipe warned - `T21:28:0N+00:00`,
  hand-normalised to `T12:00:00-04:00` before the sitemap ran.
- **No new utility classes**, confirmed by class-set diff against three existing
  ranking pages and an existing detail page. `npm run build:css` correctly not run.
- **The social loader parsed the new page end-to-end** - all five ItemList slugs
  resolved against `restaurants.json` and all five body-row taglines matched.
  Both are hard failures in `loadTopN`, so a silent mismatch was not possible.
- **The homepage grid stands at 14** with `grid-cols` untouched: clean at
  `md:grid-cols-2` (7 rows), orphan of 2 at `lg:grid-cols-4`, accepted per the
  standing ruling in section 8.

## Encoding note

Non-ASCII referenced by codepoint rather than glyph, to survive console
round-tripping. Copy the shapes from the tree, not from this file.

- **U+1F35D** SPAGHETTI - candidate homepage-card emoji, matching the trailing
  emoji every other card carries. Not proposed above; operator's call.
- **U+2014** EM DASH, marked `[EM]` - not required for a Top-5 (no count
  framing), but present in `_template-canonical.html` boilerplate.
- **U+2013** EN DASH, marked `[EN]` - `hoursHumanReadable` day and time ranges.
  Shape precedent: `park-pizza-co`.
- **U+00B7** MIDDLE DOT, marked `[MID]` - the OG meta-line and hero-subtitle
  separator, "Cuisine [MID] Neighborhood".
- **U+0027** APOSTROPHE - **corrected 2026-08-26.** This entry originally
  named U+2019 RIGHT SINGLE QUOTATION MARK. Checked at build time: U+2019 does
  **not** occur anywhere in `data/restaurants.json`, and `Santi's` stores a
  plain ASCII `0x27`. `Mondo's Italian Restaurant` shipped with the ASCII
  apostrophe, matching `Moe's Crosstown Tavern`, `Hannibal's Kitchen` and
  `D'Allesandro's Pizza`. (`_cuisine_dedup.py` normalises both forms
  identically, so dedup was never at risk either way - but the file should say
  what the tree actually contains.)
