# Best Bar launch - analysis working file

**Status:** ANALYSIS ONLY. Nothing applied, nothing committed.
**Branch:** `best-bar-launch`, cut from `main` at `a8d9bb5`.
**Date:** 2026-08-28.
**Recipe:** DECISIONS #23, Top-N launch recipe (formalized), as amended 2026-08-26.

This file is the pre-build record for a proposed 16th ranking category,
`best-bar`, at Top-5. It follows the #23 step sequence. Every place this
prompt and the recipe/tree disagree is collected in section 11 rather than
resolved silently.

---

## 0. Roster and scope

Operator-confirmed order, five entries, Top-5:

| # | Name (as proposed) | Tree status |
|---|---|---|
| 1 | Last Saint | net-new |
| 2 | Moe's Crosstown Tavern | **pre-existing** - third listing |
| 3 | Graft | net-new (name determination open, see 4b) |
| 4 | The Royal American | net-new |
| 5 | Burns Alley Tavern | net-new |

### 0a. Zero bench - accepted, and this is the fifth consecutive time

DECISIONS #23 says, flatly: *"Never zero bench, whatever the provenance."*
This roster supplies exactly five operator-confirmed candidates for a Top-5
with no spare. The prompt states this was accepted rather than overlooked,
and that is recorded here as such.

The run is now **five consecutive**: `best-ice-cream` (3 for 3),
`best-ramen` (2 for 2), `best-italian` (5 for 5), `best-seafood` (4 for 4),
and now `best-bar` (5 proposed, 5 cleared). The TRACKED item already filed
from best-seafood says the rule "is being routinely overridden by practice"
and asks for either an amendment or a spare. **This launch is the fifth data
point and should be appended to that item rather than filed as a new one.**

Exposure at N=5 is **editorial, not structural** - a late failure drops the
page to Top-4, a documented length with its own count framing (#4, #20). It
is not the N=1 case, where a failure changes template, renderer path and
page shape.

### 0b. The two operator exclusions - recorded so a future session does not read them as oversights

Both were considered and dropped by the operator. Neither is a sourcing
failure; both are editorial scope calls. To be filed per #23 step 11 / #22.

- **Salty Mike's** - excluded over an ownership change that locals describe
  as having turned it touristy. This is a **consensus/taste** exclusion, not
  a liveness or identity failure. Same class as the best-seafood
  "setting-driven tier" exclusion (Bowen's Island, The Wreck, Crosby's,
  Hyman's), which was likewise never sourced and filed as a no-trigger
  record. **Recommend: no-trigger record.** Re-proposing it would require a
  new consensus signal, not a re-verification, so a trigger would be
  meaningless.
- **Little Palm** - excluded because it is a hotel pool restaurant rather
  than a bar. This is a **category** exclusion and the cleanest kind: it
  fails #23 rule 5 (verify the category claim, not just existence) on its
  face. **Recommend: no-trigger record.**

Neither was sourced in this pass, deliberately - the operator's reasons are
scope decisions, and researching them would not change them.

---

## 1. STEP 0 - branch

`main` verified at `a8d9bb519c41f3268dd28f4d1feddee6b8fa6a6f`, matching
`origin/main` exactly (0 ahead, 0 behind). Working tree clean. **No SHA in
the prompt was trusted; both were re-derived.**

HEAD was already `main`, so the prompt's "if HEAD is not main, branch from
main explicitly" conditional did not fire. The explicit form was used
anyway, since it is strictly safer and self-documenting:

    git checkout -b best-bar-launch main

Confirmed after the fact: branch `best-bar-launch`, HEAD `a8d9bb5`,
merge-base with `main` `a8d9bb5`, `git status --short` empty.

---

## 2. STEP 1 - tree first

Per #23 section 0a ("Check the tree before you source anything", amended
2026-08-26). Run before any sourcing.

> **Citation note.** The prompt cites this as "amended #23 rule 1". The
> tree-first requirement is #23 recipe **section 0a**; the numbered "rule 1"
> in #23 is *"An own-site page is never sufficient evidence of liveness"*.
> The best-seafood analysis file used the same shorthand, so it is house
> usage rather than a fresh error. No substantive disagreement - noted for
> accuracy only.

### 2a. Moe's Crosstown Tavern - confirmed, and this is the THIRD listing

Present as `moes-crosstown-tavern`. `appearsOn` currently carries two
entries; `best-bar` at position 2 would be the third.

**Current prose fields, verbatim from `data/restaurants.json`:**

    tagline:       "Legendary Dive Bar Burger"

    description:   "Moe's Crosstown Tavern is a Hampton Park dive bar in
                    Charleston, SC, known for its legendary burger. Voted
                    by Charleston locals as one of the city's best burgers."

    shareTagline:  "The legendary dive-bar burger, voted best by Charleston
                    locals."

    keywords:      "Moe's Crosstown Tavern Charleston, dive bar burger
                    Charleston, Hampton Park bar, best burger Charleston SC"

    appearsOn:     [ { "url":   "/rankings/best-burger.html",
                       "title": "Best Burger in Charleston" },
                     { "url":   "/rankings/best-wings.html",
                       "title": "Best Wings in Charleston" } ]

Other stored fields, for the record: `cuisine: "American"`,
`neighborhood: "Hampton Park"`, `schemaType: "Restaurant"`,
`monthYear: "August 2026"`, `priceRange: "$$"`,
`hours: "Mo-Su 11:00-02:00"`, `phone: "+1-843-641-0469"`,
`websiteURL: "https://moescrosstowntavern.com"`. No `displayCuisine`.

Per-list taglines already shipped, verbatim from the ranking pages:

| Page | Tagline |
|---|---|
| `best-burger` | `Legendary Dive Bar Burger` |
| `best-wings` | `Dive Bar Wings, Open Till 2am` |

`dateModified` on the rendered detail page is `2026-08-24T12:00:00-04:00`
(set by the best-wings launch). A best-bar listing bumps it to
`2026-08-28T12:00:00-04:00`. Per the tree's convention, `dateModified` lives
in the rendered HTML JSON-LD, not in `restaurants.json`, and the generator
preserves it on regen - so this is a hand edit after regeneration.

### 2b. The open TRACKED item on Moe's - CRITICAL, and this launch is its stated trigger

**The item exists and is open.** `_strategy/TRACKED.md:109`, filed under
"Roster exclusions from the best-wings launch":

> **Moe's Crosstown Tavern prose is single-category-framed but now
> cross-listed.** Every prose field (`tagline`, `description`,
> `shareTagline`, `keywords`) frames Moe's solely as a burger destination,
> written when `best-burger` was its only listing. It now also appears on
> `best-wings`. [...] Home Team BBQ is the pattern to follow [...]
> Tutti-class editorial cascade, deliberately kept out of the launch PR to
> keep that diff reviewable. **Trigger: next edit to this entry.**

**The trigger fires.** A `best-bar` listing is an edit to this entry - an
`appearsOn` append plus a hand-bumped `dateModified`. There is no reading
under which that is not "the next edit to this entry".

**And the mismatch is worse here than the item anticipated.** The item was
written about a wings listing and says the mismatch "is only visible on the
shared detail-page hero". On a **bar** list the problem is categorical
rather than cosmetic. The detail page for a restaurant listed among
Charleston's best *bars* would carry a `tagline` naming a burger, a
`description` whose only claim is "known for its legendary burger", and a
`shareTagline` that is entirely about the burger. Three of four prose fields
assert a food specialism on a page whose new inbound link is a bar ranking.
Only `keywords` contains a bar token at all, and "Hampton Park bar" is there
as a locator, not a claim.

**Recommendation: split it out. Cascade PR lands FIRST, launch PR second.**

This follows the **Bar Weems precedent** exactly. From #23's own account of
best-ramen:

> Discovering that mid-launch forced the work into two PRs so the
> corrections could land before the launch regen stamped a fresh
> `dateModified` over them.

The failure mode #23 names is *a launch stamping a fresh `dateModified` over
known-wrong fields*. That is precisely what a single combined PR would do
here: regenerate `moes-crosstown-tavern.html`, stamp
`2026-08-28T12:00:00-04:00`, and thereby assert freshness over prose that a
filed TRACKED item already says is wrong for its **current** listings, never
mind the third one this PR adds.

The counter-argument is weak. The item itself says the cascade was
"deliberately kept out of the launch PR to keep that diff reviewable" -
which is an argument for keeping it out of *this* launch PR too, and that is
exactly what splitting does. Both readings agree.

Cost of splitting: one extra PR, one extra regen of a single detail page.
Cost of not splitting: the specific documented failure the recipe was
amended to prevent.

**Sourced material now exists to do the cascade well.** Moe's own site
(verified this pass, section 5e) supplies bar-forward framing that does not
have to be invented:

- browser title / masthead: `Moe's Crosstown Tavern - Sports Bar and Grill
  Charleston, SC`
- self-description: "vintage pub", "sports bar and grill"
- "a local watering hole in the Charleston area for **25+ years**"
- claimed awards: **"Best Neighborhood Bar" 25+ consecutive years**, "Best
  Pub Food" 9 years running
- menu breadth: burgers prominently, **wings**, a Reuben, "some of the best
  appetizers"

That last set is the Home Team BBQ pattern the TRACKED item asks for -
`tagline` "BBQ, Wings, Good Times", `description` naming several things -
and Moe's own site already names burgers, wings and pub food together, so
the broadened prose would be sourced rather than composed.

**One caution before that material ships:** the award claims are
**self-reported on the own site**. Per #23's identity/liveness split, an own
site is authoritative for what a business calls itself but is not an
independent record, and an award is a claim about a third party's decision.
"Best Neighborhood Bar, 25+ consecutive years" reads like a Charleston City
Paper reader poll; **corroborate it against the awarding publication before
putting a number in shipped prose.** If it does not corroborate, the
non-numeric own-site language ("vintage pub", "local watering hole") is
still fully usable and needs no external support.

**Reported, not decided**, per the prompt.

### 2c. Graft and tutti-pizza share 700 King St - confirmed, with a real implication

`tutti-pizza` is stored at **`700 King St Suite A`**, Charleston, **29403**.
Graft's own site prints **"700 King Street, Suite B, Charleston, South
Carolina, 29403"**. Same building, adjacent suites. Confirmed.

The prompt adds that they are "under common ownership." **That claim was not
corroborated in this pass.** Graft's own About page names its owners as Femi
Oyediran and Miles White (both sommeliers), with Kirsten Bhattacharyya as
Director of Operations, and makes no mention of a pizza concept; nothing
found connects either owner to Tutti Pizza. **Recorded as unverified.** It
changes no recommendation below - see why immediately.

**Implication 1 - no `locations[]` relationship, whatever the ownership.**
Even if common ownership is confirmed, two differently-branded businesses in
two suites are **sibling concepts**, not locations of one another. The tree
has settled precedent: Volpe (Coda del Pesce), Seahorse (Chubby Fish), and
Johnny's Garage / The Bounty Bar (The Royal American - section 4c). #17's
`locations[]` is for one brand in several places. Neither entry gains one.

**Implication 2, load-bearing: the tree contradicts itself about what
neighborhood 700 King St is in.**

| Address | ZIP | Stored `neighborhood` | Entry |
|---|---|---|---|
| 684 King St | 29403 | **Upper King** | `weltons-tiny-bakeshop` |
| **700 King St Suite A** | **29403** | **Westside** | **`tutti-pizza`** |
| 710 King St | 29403 | **Upper King** | `little-jacks-tavern` |

`tutti-pizza` is the tree's **only** `Westside` entry, and it sits
numerically between two `Upper King` entries, on the same block, in the same
ZIP. Graft is in the same building.

This is the **`gustards-custard` situation restated one field over.** #23
records that "two businesses at one address cannot have different ZIPs" and
overrode an own-site value on that basis. The same logic gives: **two
businesses at one address cannot be in different neighborhoods.**

Independent evidence resolves it. The Post and Courier's 2018 opening piece
on Graft carries "Eastside" in its **section slug** but its **body text says
"Upper King Street"** for this exact address. Body prose beats a section
tag, and the best-seafood amendment to the surface hierarchy is directly on
point: rank surfaces by *how deliberately each was authored for the thing
being asserted*. A CMS section tag is not authored about this address at all.

The ZIP band corroborates independently. Every `29403` King Street entry in
the tree is Upper King / North Central / Westside (upper peninsula); the one
`29401` King Street entry, 193 King St, is `Lower King`.

**Recommendation: Graft ships `neighborhood: "Upper King"`.** It matches both
flanking entries, the ZIP band, and the one piece of dated editorial prose
that names a neighborhood for this address.

**`tutti-pizza`'s `Westside` is the outlier and should be re-derived - but
NOT in this PR.** Tutti is not on `best-bar`, gets no `appearsOn` append and
no `dateModified` bump, so nothing here stamps freshness over it. Filing it
is correct; fixing it is a separate, cheap follow-up. See section 10.

Graft's own About page says "uptown Charleston". That is marketing register,
not a neighborhood a surveyor would name, and it fails #23's "would a local
surveyor agree?" test. Not used.

**A second, weaker instance of the same class**, recorded and not acted on:
`the-harbinger-cafe-bakery` at **1107 King St** ships `North Central` while
`ok-donna` at **1117 King St** ships `Upper King` - ten street numbers
apart. Unlike the 700 King case this one is genuinely fuzzy: North Central
and the Upper King corridor legitimately overlap up there, and no source
contradicts either value. **No-trigger observation only.**

### 2d. The other four are net-new on slug AND name - confirmed

Checked against `data/restaurants.json` (49 entries), `restaurants/` (49
files), and a case-insensitive grep across every `*.html`, `*.json`, `*.md`,
`*.ts`, `*.py` and `*.xml` in the tree excluding `node_modules` and `.git`:

| Candidate | Name anywhere in tree? | Slug file exists? |
|---|---|---|
| Last Saint | no | `restaurants/last-saint.html` - clear |
| Graft (any form) | no | `graft.html` / `graft-wine-shop.html` - clear |
| The Royal American | no | `the-royal-american.html` - clear |
| Burns Alley Tavern | no | `burns-alley-tavern.html` - clear |

Also confirmed absent from the whole tree: **Salty Mike's**, **Little
Palm**, **Bounty**. Zero hits each - no prior session considered and
recorded any of them, so the section 0b filings are genuinely new.

Nearby-address false-positive check, run because three of the five sit on
streets the tree already occupies: `little-jacks-tavern` is at 710 King St
(not 354 or 700), `heavys-barburger` is at 1137 Morrison Dr (not 970),
`babas-on-cannon`'s secondary is at 804 Meeting St (not 472). No collisions.

### 2e. Other open TRACKED items this launch touches

| Item | Status this launch |
|---|---|
| Moe's burger-only prose | **fires** - see 2b |
| Sorelle Mercato / #17 same-address sub-venue | **fires** - second instance, see 4a |
| Zero bench at N>=3 | **fires** - fifth consecutive, see 0a |
| `servesCuisine` generic-override no-op | **fires** - third instance, see 7c |
| `priceRange` re-derivation sweep | **fires**, should not be serviced here - see 7d |
| `IceCreamShop` schemaType docblocks | **stale, already done** - close it, see 6a |
| `social/src/data.ts` slug-derived category | **does NOT fire** - see 9c |
| Generator seeds dates in UTC | **fires** - four new pages to hand-normalize, see 9b |

---

## 3. STEP 2 - what the supplied data got right, and what it did not

The prompt's data was treated as a hypothesis, not adopted. Summary first;
per-candidate detail follows.

| Field | Supplied | Verified outcome |
|---|---|---|
| Last Saint address | `472 Meeting St B` | **`472 Meeting St`** - the suite letter is unsourced |
| Last Saint hours | Daily 17:00-02:00 | **confirmed**, own site: "5pm-2am Daily" |
| Last Saint phone | none given | **none exists** - confirmed, see 4a |
| Graft name | `Graft Wine Shop & Wine Bar` | **`Graft Wine Shop`** per own masthead - see 4b |
| Graft address | `700B King St` | **`700 King St Suite B`** - own site form, matches suite-mate |
| Graft phone | `+1-843-718-3359` | **confirmed** |
| Graft hours | daily 12:00-22:00 | **incomplete** - that is the *retail* half only, see 4b |
| Royal American address | `970 Morrison Dr` | **confirmed** |
| Royal American phone | `+1-843-817-6925` | **confirmed** |
| Royal American hours | daily 11:00-02:00 | **confirmed**, own site: "Open Daily 11 am - 2 am" |
| Burns Alley address | `354B King St` `29401` | **confirmed** - three independent sources |
| Burns Alley phone | `+1-843-723-6735` | **confirmed** |
| Burns Alley hours | daily 12:00-02:00 | **confirmed** |
| Burns Alley two floors | asserted | **weakly sourced** - see 4d |
| Burns Alley price level 1 | asserted | **unsourced**, and the framing is wrong - see 7d |
| Burns Alley CofC hangout | asserted | **confirmed**, multiply - see 4d |

---

## 4. STEP 2 (cont.) - the four determinations the prompt asked for

### 4a. Last Saint's ANNEX - it is an in-venue room, and it fires the Sorelle Mercato trigger

**What the Annex actually is.** Post and Courier (**2025-06-27**): *"A yellow
door at the back of Last Saint will take you into a tucked-away little
speakeasy"*, "equipped with six barstools and three booths", *"only open
Thursday through Saturday nights starting at 5:30 p.m."* Entry is by ringing
a bell at the door or by advance online reservation. There is no menu; the
bartender builds to request. It has its own Resy venue listing under the
name **"Annex @ Last Saint"**, and Last Saint's own homepage links to that
Resy page.

**Determination: an in-venue room with no data implication.** Taking the
prompt's three options in turn:

- **Not a `locations[]` secondary.** Same street address as the parent. This
  is the exact reasoning the Sorelle Mercato TRACKED item records: *"a
  `subOrganization` whose address is byte-identical to the parent's asserts
  a location that does not exist."* Adding it would put a false location in
  the entity graph.
- **Not a separate business.** The name is *Annex **at** Last Saint* -
  grammatically subordinate. Same premises, same door, same ownership; P&C
  presents it as a space within Last Saint rather than an independent
  venue. It has no address, phone or site of its own.
- **Yes, an in-venue room.** `last-saint` ships single-location, with no
  `locations[]` and no `subOrganization`. The Annex earns a mention in the
  editorial `tagline` (it is the most distinctive thing about the venue) and
  nothing structural.

**This is the same class as Sorelle Mercato, and that matters procedurally.**
The best-italian TRACKED item reads:

> **DECISIONS #17 has no language for a same-address sub-venue.** [...]
> **Deliberately not amended in this PR** - #23's own Top-N recipe was
> deferred until a second launch confirmed the pattern, and the consistent
> move is to wait for a second same-address instance rather than generalise
> from one. **Trigger: the next time a candidate has a sub-venue sharing its
> address.**

**That trigger fires now.** The Annex is the second instance, and it is the
confirming case the item was waiting for. The two together define the
pattern cleanly:

| | Sorelle Mercato | Annex @ Last Saint |
|---|---|---|
| Address | identical to parent (88 Broad St) | identical to parent (472 Meeting St) |
| Separation | different floor, same building | room behind a door, same unit |
| Hours | 08:00-16:00 vs parent 17:00-22:00 | Thu-Sat from 17:30 vs parent daily 17:00-02:00 |
| Own booking listing | no | **yes - its own Resy venue** |
| Resolution | single-location | single-location |

The Annex is the **harder** of the two on exactly one axis - it has a
distinct bookable listing, which Mercato did not. That is worth stating in
the amendment, because a future session will hit a case where a separate
reservation listing is the only evidence of separateness, and the answer
should be that **a booking listing is a reservations-platform artifact, not
a business identity**. Distinct hours and distinct booking are both normal
for a room inside one venue.

**Recommended #17 amendment language** (to be drafted in a docs PR, not
here): a same-address sub-venue is neither a `locations[]` secondary nor a
distinct entry. The parent ships single-location. Distinct hours, a distinct
name, and a distinct reservation listing do **not** individually or
collectively make it a location; only a **distinct address** does.

**Last Saint phone: none exists - confirmed, not assumed.** The prompt asked
to source one or confirm none. Checked: the own site's dedicated `/contact`
page lists an address, hours and `info@lastsaintchs.com` and **no phone**;
the homepage lists no phone; Difford's Guide, a bar-specific directory,
explicitly carries no phone for the venue. The venue routes contact through
email and Resy. **Ship `phone: null`** per the `_meta.fieldPolicy` rule that
null means absent. Note this is a *positive* finding rather than a gap: the
detail template's sidebar drops the Phone row when the field is null, which
is the correct rendering.

**Address - drop the suite letter.** The prompt supplies `472 Meeting St B`.
The own site prints "472 Meeting Street, Charleston, SC" with no unit;
Difford's gives "472 Meeting Street, Charleston, South Carolina, 29403" with
no unit; the venue's own Toast ordering page is slugged
`last-saint-472-meeting-st`. The building **does** have lettered units - a
real-estate listing for "472 Meeting Street Unit D" exists - so "B" is
*plausible*, but **no source states it is Last Saint's**. Per the field
policy, ship **`472 Meeting St`**.

Note the contrast, which is the useful part: of the three lettered addresses
in this roster, **two are sourced and one is not**. Graft's Suite B is
printed on Graft's own site; Burns Alley's Unit B appears in three
independent records; Last Saint's B appears nowhere.

**Second location: none.** Own site silent (the strongest negative signal per
#23 rule 6). Owner Joey Goetz has other *concepts* - he is bar director at
`ok-donna`, which is **already in the tree**, and press describes further
projects on King Street and an "Italian-ish" collaboration. All are separate
brands at separate addresses: the Volpe / Seahorse pattern. **No
`locations[]`.** The `ok-donna` overlap is worth a no-trigger record, since
a future session may otherwise re-derive it.

### 4b. Graft - the own site does not call it "Graft Wine Shop & Wine Bar"

**Resolved against the own site using the #23 surface hierarchy** (logo /
masthead > headings > body prose > title and footer):

| Surface | Text | Rank |
|---|---|---|
| Own site logo / masthead | **"Graft Wine Shop"** | 1 - highest |
| Own site h2 heading | **"graft wine shop"** | 2 |
| Own site About body prose | "**Graft** is a wine shop and wine bar in uptown Charleston, South Carolina." | 3 |
| Own site footer | "Graft Newsletter" | 4 |
| Own site domain | `graftchs.com` | - |

Off-site forms, for completeness: Instagram display name and one Facebook
page read "Graft Wine Shop & Wine Bar"; a second Facebook page reads "Graft
Wine Shop"; Yelp reads "Graft Wine Shop"; Tripadvisor reads "Graft Wine
Bar"; En Primeur Club and Afar read "Graft Wine Shop & Wine Bar".

**Recommendation: `name: "Graft Wine Shop"`, `slug: graft-wine-shop`.**

The top two surfaces agree, and the body prose treats "Graft" as the name
with "a wine shop and wine bar" as *description*. The "& Wine Bar" long form
lives only on social profiles and aggregators. Social display names are
authored for discovery - the same keyword-bearing register as the `keywords`
field - not as identity, which is exactly the distinction #23's hierarchy
exists to make.

**This dissolves the ampersand question rather than answering it.** The
prompt asks whether the ampersand needs handling in the slug, JSON-LD or
social-card derivation. Under the recommended name there is no ampersand.
Recorded anyway, because the operator may prefer the long form and because
the answer is useful either way:

- **The tree already has the precedent.** `the-harbinger-cafe-bakery` is
  `name: "The Harbinger Cafe & Bakery"` with slug `the-harbinger-cafe-bakery`
  - the `&` is **dropped from the slug entirely**, not rendered as "and".
- **JSON-LD: no handling needed, and none should be added.** The generator
  emits a raw `&` inside the `<script type="application/ld+json">` body,
  which is correct - entity-escaping inside a script element would corrupt
  the JSON.
- **`<title>` / `og:title` / `twitter:title`: the generator emits a raw `&`
  there too.** Harbinger has shipped that way since launch. Strictly, a bare
  `&` in HTML text should be `&amp;`; in practice `& ` is not a valid entity
  reference so every parser recovers, and it renders correctly. **Not a
  defect to fix inside a launch PR** - if it is ever worth fixing it is a
  generator change affecting one existing page.
- **`_cuisine_dedup.py` normalizes `&` to " and "**, which is the trigger
  case #18 was written for (Harbinger: name "Cafe & Bakery" + cuisine "Café
  and Bakery"). This is where the ampersand actually bites - see 7b.

**Hours: the prompt's "daily 12:00-22:00" is the retail half only.** The own
site's contact page gives **two** schedules, confirmed identically on a
second source:

    Retail:  12PM - 10PM daily
    Bar:     Mon-Thu  4PM - 10PM
             Fri      2PM - 10PM
             Sat-Sun 12PM - 10PM

For a **bar** list this distinction is not cosmetic: Monday through Friday
the bar opens two to four hours after the shop does. This is not an hours
*conflict* in the #23 sense - no source disagrees with another, and #13.10
does not fire - it is one venue with two service windows, and the prompt
collapsed them.

**Recommendation.** `openingHours` describes when the establishment is open,
and the shop and bar are one room, so:

    hours:               "Mo-Su 12:00-22:00"
    hoursHumanReadable:  "Mon-Sun: 12pm-10pm\nBar service from 4pm Mon-Thu,
                          2pm Fri"

**Flagged for operator decision** - the alternative is to store the bar
window as the hours, which is arguably more useful on a bar page but
understates when you can walk in. Recommending the establishment hours with
the bar window carried in the human-readable field.

**Address: `700 King St Suite B`.** The own site prints "700 King Street,
Suite B"; P&C printed "700 King St., Suite B" in 2018. Storing it in that
form also matches its suite-mate `tutti-pizza` (`700 King St Suite A`)
exactly, which keeps the same-building relationship legible in the data.
The prompt's `700B King St` is the aggregator form.

**Phone `+1-843-718-3359`: confirmed** on the own site ("(843) 718-3359").

**Second location: none.** Own site silent on the About and Contact pages
(strongest negative signal). Graft has been at 700 King St Suite B since it
opened in **March 2018** - there is no relocation and no prior address. The
P&C "Eastside" section slug is a CMS tag, not a second site; the same
article's body says Upper King Street.

### 4c. The Royal American - definite article confirmed, Bounty Bar is a separate business

**Definite article: keep it, in both `name` and `slug`.** The own site's
masthead reads **"The Royal American"** and its heading banner reads
"* THE ROYAL AMERICAN *". Facebook, Yelp and every ticketing listing carry
"The". The tree's precedent is unanimous and three-fold:

| Entry | `name` | `slug` |
|---|---|---|
| `the-ordinary` | The Ordinary | `the-ordinary` |
| `the-wedge` | The Wedge | `the-wedge` |
| `the-harbinger-cafe-bakery` | The Harbinger Cafe & Bakery | `the-harbinger-cafe-bakery` |

All three keep "The" in **both** fields. So: `name: "The Royal American"`,
`slug: the-royal-american`.

**Bounty Bar: separate business, confirmed.** The Royal American's own site
names "our sister properties **The Bounty Bar & Grill + Johnny's Garage**".
Post and Courier headlined it "**The Bounty Bar, sister concept to The Royal
American**, now open on Folly Beach" (April 2022). It has a different brand
name, a different address (15 Center St, Folly Beach), its own website
(`thebountybar.com`) and its own Facebook page.

**Not a `locations[]` secondary.** This is the Volpe / Seahorse / Wild Olive
sibling-concept pattern, and it is the strongest instance the tree has seen:
the ownership group (All Good Industries, Karalee Nielsen Fallert) operates
**six distinct brands** - Taco Boy, The Royal American, Park & Grove, The
Bounty Bar, Johnny's Garage and The Green Hearth Project. A shared owner is
not a shared brand.

**The prompt missed one.** There is a **third** sibling in the same sentence
on the own site - **Johnny's Garage**, in Hanahan, "from the team behind The
Royal American and The Bounty Bar". Same treatment: separate business, no
`locations[]`. Worth recording in the same no-trigger entry so a future
session does not re-derive either.

Note in passing: Johnny's Garage is in **Hanahan**, which now has tree
precedent via `cane-pazzo`. Not relevant to this launch; noted because the
Cane Pazzo TRACKED item asked for municipality precedent to be tracked.

### 4d. Burns Alley Tavern

**Name: `Burns Alley Tavern`, no apostrophe.** Own-site masthead reads
"**Burns Alley Tavern** Local Dive Bar". Tripadvisor and MenuPix carry
"Burn's Alley Neighborhood Bar" with an apostrophe. This is the **Tru Blues
case** exactly - the own site is authoritative for its own spelling, and the
aggregators are wrong. Note the venue was genuinely *named* "Burns Alley
Neighborhood Bar" in 2013 (Charleston Living, 2013-01-30) and has since been
renamed, so the aggregator entries are stale rather than merely misspelled.

**Address `354B King St`, `29401`: confirmed** by three independent records -
Yelp ("354 B King St"), restaurant.com (slug `354-king-st-b`), and
Charleston Living (2013, "354-B King St."). Store as **`354B King St`** per
the prompt; note the tree's existing suite forms use "Suite A"/"Unit"
spellings, so `354 King St Unit B` is the more house-consistent form.
**Flagged as a trivial formatting choice, not a fact.**

**Phone `+1-843-723-6735`: confirmed.**
**Hours daily 12:00-02:00: confirmed** - "open 7 days a week starting at
noon", Mon-Sun 12:00-02:00.

**College of Charleston characterization: CONFIRMED, multiply.** Recorded per
the prompt's request:
- "The place is a **huge College of Charleston hangout**, and it's full of
  students."
- A Tripadvisor review is titled "**Busy student bar with karaoke**".
- Charleston Living (2013): the College of Charleston arena sits "**smack dab
  in their back alley**", driving game-day traffic; the piece describes
  "Fans, alumni, exceptionally tall former players, regulars".

**Tagline consequence, stated plainly:** this characterization is well
sourced but it comes from **reviews and press, not the venue**, and on a
list whose entire editorial wedge is "voted by locals" a tagline that leads
with "college bar" reads as a caveat rather than a recommendation. See 8b -
recommendation is to carry it in `keywords` and the analysis, not the
tagline, with the alternative drafted in case the operator disagrees.

**Two floors: WEAKLY sourced - do not assert flatly.** The only support
found is a review reading *"There are two 'floors' to the place as well,
with a good amount of seats each"* - **with the scare quotes in the
original**, which hedge whether they are proper floors or a mezzanine. Per
#23's inverted-claim rule, publishing "Two Floors" as a flat assertion
slightly overstates a hedged source. The tree has a **"Three Floors"**
tagline precedent (`sorelle` on `best-italian`), so the *form* is
established and the claim would be usable **if corroborated by one
unhedged source**. Until then it should not lead the tagline. See 8b.

Also confirmed and usable: two entrances, one down Burns Lane off King and
one **through the back of the neighbouring La Hacienda**; opened **May
2006**; live music most nights across a wide genre range; karaoke.

**Second location: none.** Own site is near-contentless (copyright 2024, no
address, no hours) and mentions none; no press or directory signal of an
expansion. Single-location.

### 4e. Moe's Crosstown Tavern - re-verified, per #23 rule 4

> *"The gate applies to pre-existing entries too, not just new ones. Any
> restaurant about to receive a new listing and a `dateModified` bump must
> clear it first - the bump is an assertion of freshness."*

Run, not assumed. **Passes.**

- **Liveness:** Yelp updated **July 2026** with 254 reviews; Tripadvisor
  carries a 2026 listing; charlestonranked lists it as "#41 Bar in
  Charleston". Multiple dated third-party signals, all positive, none
  contradicting.
- **Identity:** own site live, masthead "Moe's Crosstown Tavern - Sports Bar
  and Grill Charleston, SC".
- **Stored data re-checked against source:** address `714 Rutledge Ave` -
  confirmed; phone `(843) 641-0469` - confirmed; hours daily 11:00-02:00 -
  confirmed. **No stored field is stale.** (Contrast Bar Weems, where the
  same check found two of three wrong.)
- **Category claim (#23 rule 5):** it is a bar. Own site self-describes as
  "sports bar and grill" and "vintage pub", claims "Best Neighborhood Bar"
  awards, and calls itself "a local watering hole"; the tree's own
  `description` already calls it "a Hampton Park dive bar". Cleared.
- **Second location (#23 rule 6):** none. Own site mentions one location;
  no press or directory signal. Single-location.

### 4f. Second-location check - all five, per the standing rule

| Candidate | Own site says | Other signals | Outcome |
|---|---|---|---|
| Last Saint | silent | owner has separate concepts (`ok-donna`, King St project) - different brands | single-location |
| Moe's Crosstown Tavern | one location | none | single-location |
| Graft Wine Shop | silent, About + Contact | none; same address since March 2018 | single-location |
| The Royal American | names **sister properties**, explicitly not locations | Bounty Bar (Folly Beach), Johnny's Garage (Hanahan) - separate brands, separate sites | single-location |
| Burns Alley Tavern | silent | none | single-location |

**No `locations[]` array on any of the five.** Three of the five have sibling
concepts under shared ownership, which is the pattern #23 rule 6 exists to
distinguish from a genuine pending second location - and none of the six
sibling brands is even future-tense. This is a cleaner sweep than the three
consecutive launches that each hit a pending second location.

---

## 5. STEP 2 (cont.) - the two gates, run independently

Per #23, identity and liveness take different evidence and were sourced
separately.

### 5a. Liveness gate - dated third-party REQUIRED, own site INADMISSIBLE

| Candidate | Dated third-party signals | Verdict |
|---|---|---|
| Last Saint | Yelp updated **July 2026** (103 photos, 65 reviews); Tripadvisor 2026 listing; active Resy booking for the Annex; live Toast ordering page | **OPEN** |
| Moe's Crosstown Tavern | Yelp updated **July 2026**, 254 reviews; Tripadvisor 2026 | **OPEN** |
| Graft Wine Shop | Yelp updated **March 2026** (94 photos, 66 reviews); Tripadvisor active; restaurantguru rating 4.8 | **OPEN** (weakest of the five - see note) |
| The Royal American | **booked 2026-2027 concert calendar** across Bandsintown, Songkick and JamBase; Yelp updated **July 2026** (198 reviews) | **OPEN** - strongest |
| Burns Alley Tavern | Yelp updated **August 2026** (146 photos, 173 reviews); wheree updated June 2026; Untappd active | **OPEN** - freshest |

**Note on Graft.** Its freshest dated third-party marker is March 2026,
about five months stale at time of writing, where the other four carry
July or August 2026. There is **no negative signal** - no closure marker
anywhere, own site current with 2026 hours, and it is a small retail shop
that simply attracts fewer new reviews than a music venue or a student bar.
Per #23 the gate wants *converging evidence of open*, and it converges; but
this is the one entry where a single fresher confirmation would be cheap
insurance. **Recommend one dated check before the build pass.**

A booked forward calendar (The Royal American) is worth naming as a
first-class liveness signal - it is a positive dated assertion about future
operation, which is stronger than absence-of-a-closure-marker. That is
exactly what the Tru Blues exclusion lacked.

### 5b. Identity gate - own site AUTHORITATIVE

| Candidate | Own site | Name as shipped |
|---|---|---|
| Last Saint | `lastsaintchs.com` - masthead "Last Saint" | **Last Saint** |
| Moe's Crosstown Tavern | `moescrosstowntavern.com` | **unchanged** |
| Graft | `graftchs.com` - masthead "Graft Wine Shop" | **Graft Wine Shop** (see 4b) |
| The Royal American | `theroyalamerican.com` - masthead "The Royal American" | **The Royal American** |
| Burns Alley Tavern | `burnsalley.com` - masthead "Burns Alley Tavern Local Dive Bar" | **Burns Alley Tavern** |

Two name determinations turned on this gate and both went **against** an
aggregator: Graft (own site short-form beats social long-form) and Burns
Alley (own site no-apostrophe beats Tripadvisor's apostrophe).

### 5c. Category gate - #23 rule 5, verify the claim not just existence

This is a **bar** list, so each entry's bar-ness was confirmed rather than
assumed from the name:

| Candidate | Evidence it is a bar |
|---|---|
| Last Saint | own site: "an eastside cocktail bar"; Yelp category **Bars**; Difford's Guide (a bar directory) categorises it as a cocktail bar |
| Moe's Crosstown Tavern | own site: "sports bar and grill", "vintage pub", "local watering hole"; claimed "Best Neighborhood Bar" awards |
| Graft Wine Shop | own About: "Graft is a wine shop **and wine bar**"; posted bar-service hours distinct from retail hours |
| The Royal American | own site heading: "**Neighborhood Bar** - Restaurant - Live Music Venue" |
| Burns Alley Tavern | own masthead: "**Local Dive Bar**"; Yelp category **Dive Bars** |

All five cleared. Graft is the only one where the category is *half* the
business, and its own site states both halves explicitly.

### 5d. Hours - own site corroborates, dated third-party decides

No #13.10 fallback fired. No candidate had an unresolvable hours conflict.

| Candidate | Own site | Third-party | Shipped |
|---|---|---|---|
| Last Saint | "5pm-2am Daily" | agrees | `Mo-Su 17:00-02:00` |
| Moe's | daily 11:00-02:00 | agrees; matches stored | unchanged |
| Graft Wine Shop | retail 12-10 daily; bar M-Th 4-10, F 2-10, Sa-Su 12-10 | second source reproduces both | `Mo-Su 12:00-22:00` + split in human-readable (see 4b) |
| The Royal American | "Open Daily 11 am - 2 am"; "Kitchen open 'til 1am" | agrees | `Mo-Su 11:00-02:00` |
| Burns Alley | own site states none | multiple agree: daily 12:00-02:00 | `Mo-Su 12:00-02:00` |

Burns Alley is the clean textbook case: the own site is silent on hours, so
dated third-party decides outright, exactly as the amended rule prescribes.

### 5e. Verifiable facts - independent record checked against own site

One deviation, one non-deviation, both recorded:

- **Last Saint suite letter** - the prompt supplies "B"; own site prints no
  unit; no independent record supplies one. **Not shipped.** This is the
  field-policy call (null/absent beats fabricated), not an override.
- **Graft ZIP `29403`** - own site prints it, `tutti-pizza` at the same
  street address stores the same value. Consistent. No `gustards-custard`
  situation here.
- **Burns Alley ZIP `29401`** - differs from every other King Street entry
  except `167-raw-oyster-bar` (193 King St, also 29401). Consistent with a
  lower-peninsula address; used as corroboration for the neighborhood call
  in 8f.

---

## 6. STEP 3 - schemaType

### 6a. `BarOrPub` is still sanctioned, and the docblock lists do NOT need amending

**Sanctioned by intentional decision #4 - verified verbatim** from
`rankings/_detail-page-template.html`:

> **4. SchemaType is per-page configurable.**
> Mirrors the per-page override pattern from DECISIONS #5. Default is
> "Restaurant"; override to the most-specific applicable subclass of
> FoodEstablishment when accurate.

**And the lists already carry it. All three of them.** This is the direct
answer to the prompt's question, and it differs from the IceCreamShop case:

| Location | Current text |
|---|---|
| `_template-canonical.html:114` | `- (future bar page)    -> "BarOrPub"` |
| `_detail-page-template.html:27-28` | `{{SchemaType}} "Restaurant" (default), or CafeOrCoffeeShop / IceCreamShop / BarOrPub / Bakery / NightClub` |
| `_detail-page-template.html:316` | `- bar -> "BarOrPub"` |

Both docblocks additionally now carry **"LIST IS ILLUSTRATIVE, NOT AN
ALLOWLIST"** and both reproduce the #19 sibling-tie and service-model
cautions.

**So the IceCreamShop-style amendment is not needed - because it already
happened.** The work landed in **PR #50** (`8c697db`, "docs: amend #19 and
#23 from the wings, ice-cream and ramen launches"), confirmed by
`git log -S`.

**But the TRACKED item that asked for it is still filed as OPEN**
(`_strategy/TRACKED.md:117`, in the Open section - the Resolved section
starts at line 248). Its stated ask - add `IceCreamShop` to both lists,
"ideally with a one-line note that the list is open" - is satisfied in full.
**Recommend closing it in this launch's TRACKED edit**, moving it to
Resolved with a note pointing at `8c697db`. Zero-cost, and it removes a
stale open item that a future session would otherwise re-investigate exactly
as this one did.

**One cosmetic residue.** `_template-canonical.html:114` reads "(future bar
page)". The moment `best-bar` ships, that placeholder is stale. It should
become `- best-bar -> "BarOrPub"`, matching the form already used for
`best-coffee-shops` and `best-ice-cream` two lines above. One line, belongs
in the launch PR.

**Generator support verified, not assumed.** `scripts/generate_detail_page.py`
reads `restaurant['schemaType']` verbatim at lines 134, 222 and 255 with no
allowlist validation; the only special case is `FoodEstablishment` (the
mobile-vendor path). `BarOrPub` passes through with **no code change**.

### 6b. Per-entry reasoning - not one type across the board

The prompt is right to ask for this per entry, and the tree backs that up.
**The ranking-page ItemList `@type` mirrors each entry's stored
`schemaType`, per entry - it is not a page-level constant.** `best-burger`
proves it: Pubfare ships `FoodEstablishment` in the ItemList while the other
six rows ship `Restaurant`. `best-coffee-shops` and `best-ice-cream` look
uniform only because their entries happen to be uniform.

The controlling test for these five is #19's sibling caution: `Restaurant`
and `BarOrPub` are **both direct subclasses of FoodEstablishment**, so
"most-specific" cannot break the tie. **Pick on accuracy, and remember a
name is branding, not a classification.**

| Entry | Proposed | Reasoning |
|---|---|---|
| **Last Saint** | **`BarOrPub`** | Not a close call. Cocktail bar with no food programme found; own site says "an eastside cocktail bar"; Yelp's category is Bars; a bar-specific directory lists it. `Restaurant` would be inaccurate, not merely less specific. **This is the dataset's first `BarOrPub`.** |
| **Moe's Crosstown Tavern** | **`Restaurant` - unchanged** | Real kitchen, appears on two *food* lists (`best-burger`, `best-wings`), Yelp's category is "American". Bar Weems reasoning applies in mirror image: the name says Tavern but a name is branding. Changing it would also ripple the ItemList `@type` on two other ranking pages - **out of scope for a launch.** |
| **Graft Wine Shop** | **`BarOrPub`** | Genuinely both a bar and a retail shop; the two halves cannot both be the `@type`. `Winery` is wrong (it does not make wine). The hospitality half wins, following `malagon` - "Spanish Market & Tapería", market plus restaurant, ships `Restaurant`. **The retail half is unmodelled; recorded as a known limitation, not a defect.** |
| **The Royal American** | **`BarOrPub`** | **The closest call of the five.** Both are accurate: full kitchen open till 1am, famous burgers and patty melts, and Yelp's category is "American" (which is what decided Bar Weems the other way). What tips it is the higher-authority surface: the own site's own heading orders itself **"Neighborhood Bar - Restaurant - Live Music Venue"**, bar first. `NightClub` is explicitly ruled out - "Live Music Venue" invites it, but it is a neighbourhood bar with a stage, not a club. |
| **Burns Alley Tavern** | **`BarOrPub`** | Own masthead "Local Dive Bar", Yelp category "Dive Bars", no kitchen surfaced. Clear. |

**Net: four `BarOrPub`, one `Restaurant` unchanged.** The mixed ItemList is
fine and has precedent (`best-burger`).

Two entries are music venues (`The Royal American`, `Burns Alley Tavern`)
and neither takes a music-specific type: schema.org's `MusicVenue` is not a
`FoodEstablishment` subclass, so it is unavailable under intentional
decision #4 without a broader schema change. `BarOrPub` is the accurate
`FoodEstablishment` answer for both; the music identity lives in the
editorial fields.

---

## 7. STEP 3 (cont.) - cuisine

### 7a. What the tree does for bar-like entries

`cuisine` is required, and the prompt is right that it is awkward here. The
tree's existing practice, surveyed:

| Entry | `cuisine` | `schemaType` |
|---|---|---|
| `moes-crosstown-tavern` | American | Restaurant |
| `little-jacks-tavern` | American | Restaurant |
| `edmunds-oast` (a brewery) | American | Restaurant |
| `bar-weems` | Ramen | Restaurant |
| `chico-feo` | Caribbean | Restaurant |

**Every bar-like entry in the tree carries a food cuisine.** There is no
drinks-only precedent, because there has never been a drinks-only entry.
Last Saint and (largely) Graft are the first.

The tree also shows the escape hatch: the **ranking-page** `servesCuisine`
is list-scoped and can refine toward venue type where the stored value is
generic. `edmunds-oast` is stored `American` and carries **`American
Brewery`** on `best-casual-spots`. That is the model for this list.

### 7b. `_cuisine_dedup.py` - RUN, not predicted

Run against `scripts/_cuisine_dedup.py` directly. The prompt's suspicion was
correct **and there is a second hit it did not anticipate.**

| Name | Candidate `cuisine` | Result |
|---|---|---|
| Last Saint | `Cocktail Bar` | displays `Cocktail Bar` |
| Moe's Crosstown Tavern | `American` (current) | displays `American` - **unaffected** |
| Moe's Crosstown Tavern | `Tavern` | **SUPPRESSED** |
| Graft Wine Shop | `Wine Bar` | displays `Wine Bar` |
| Graft Wine Shop | `Wine Shop` | **SUPPRESSED** |
| Graft Wine Shop & Wine Bar | `Wine Bar` | **SUPPRESSED** |
| **The Royal American** | **`American`** | **SUPPRESSED** |
| The Royal American | `Bar Food` | displays `Bar Food` |
| The Royal American | `Pub Food` | displays `Pub Food` |
| **Burns Alley Tavern** | **`Tavern`** | **SUPPRESSED** |
| Burns Alley Tavern | `Dive Bar` | displays `Dive Bar` |

Three findings:

1. **The prompt's prediction is confirmed.** `Burns Alley Tavern` + `Tavern`
   suppresses - "tavern" is a substring of "burns alley tavern".

2. **`The Royal American` + `American` also suppresses**, which the prompt
   did not anticipate. This matters more than the Burns Alley case, because
   `American` is the tree's single most common cuisine value (6 entries) and
   the obvious default for a neighbourhood bar. The most natural choice
   would have silently dropped the cuisine slot from the title, the hero
   subtitle and the OG meta-line.

3. **The Graft name determination and the dedup outcome are coupled.** Under
   the recommended `Graft Wine Shop`, cuisine `Wine Bar` displays normally.
   Under the prompt's `Graft Wine Shop & Wine Bar`, the same cuisine
   **suppresses** - because the module normalizes `&` to " and ", making
   "wine bar" a substring. Deciding the name decides this too.

**Suppression is not a bug** - it is #18's designed behaviour, and
"The Royal American - American in Charleston" is genuinely worse than
"The Royal American in Charleston". But it should be **chosen**, not
stumbled into, and it also removes the cuisine from the OG image meta-line,
which is a visual change nobody would predict from the data.

### 7c. Proposed `cuisine` per entry

| Entry | `cuisine` | `displayCuisine` | Reasoning |
|---|---|---|---|
| Last Saint | `Cocktail Bar` | null | Own site's own words. **First non-food cuisine value in the dataset** - flagged as a precedent, not slipped in. Dedup clean. |
| Moe's Crosstown Tavern | `American` - **unchanged** | null | Do not touch. Any change here belongs in the 2b cascade PR, and `Tavern` in particular would suppress. |
| Graft Wine Shop | `Wine Bar` | null | Own About names both halves; `Wine Bar` is the half that matches the list and the `schemaType`. `Wine Shop` would suppress. |
| The Royal American | `Bar Food` | null | Avoids the `American` suppression, and is accurate - own site is a bar with a kitchen; press describes "pub comfort food", burgers and patty melts. |
| Burns Alley Tavern | `Dive Bar` | null | Own masthead "Local Dive Bar"; Yelp category "Dive Bars". `Tavern` would suppress. |

No `displayCuisine` overrides are needed - the values were chosen so
auto-detect does not fire, which is cleaner than overriding it after the
fact.

**Alternative worth putting to the operator:** accept suppression for The
Royal American with `cuisine: "American"`, since the suppressed title reads
well. Rejected here because it would also blank the cuisine slot on the OG
image meta-line, and because `Bar Food` is more informative on a bar list.

### 7d. `servesCuisine` on the ranking ItemList - list-scoped, proposed not decided

Per #23 these are **hand-authored per list**, not copies of
`restaurants.json.cuisine`, and must be **flagged rather than decided
silently**. Flagged:

| # | Entry | Stored `cuisine` | Proposed list `servesCuisine` | Rule applied |
|---|---|---|---|---|
| 1 | Last Saint | Cocktail Bar | `Cocktail Bar` | preserve the specific |
| 2 | Moe's Crosstown Tavern | American | **`Pub Food`** | override the generic |
| 3 | Graft Wine Shop | Wine Bar | `Wine Bar` | preserve the specific |
| 4 | The Royal American | Bar Food | `Bar Food` | preserve the specific |
| 5 | Burns Alley Tavern | Dive Bar | `Dive Bar` | preserve the specific |

Moe's is the only override, and it is the pattern #23 describes exactly:
`American` in the data, list-specific on the page - `Burgers` on
best-burger, `Wings` on best-wings, and now **`Pub Food`** on best-bar.
`Pub Food` is sourced to the own site ("Best Pub Food" 9 years running) and
keeps all three of Moe's rows distinct from one another.

**The generic-override no-op fires a THIRD time.** The existing TRACKED item
(filed from best-italian, recurring on best-seafood) notes that #23's
"override the generic with the list category" rule no-ops when the list
category *is* the generic term. Here the list category is **"Bar"**, and
"Bar" is not usable as a `servesCuisine` value at all - `servesCuisine`
names a cuisine, not a venue type. So on this list the override clause does
not merely no-op, it is **inapplicable**, and four of five rows are decided
entirely by the "preserve the specific" clause with the fifth overridden to
a term (`Pub Food`) that is **not** the list category.

That is a genuinely new wrinkle worth adding to the existing item: for
venue-type categories rather than cuisine categories, the list category is
never the right `servesCuisine` value.

### 7e. `priceRange` - the prompt's premise is wrong twice

The prompt says Burns Alley is "Price level 1 - the cheapest entry."

**First problem: it would not be the cheapest.** Four entries already ship
`$`: `park-pizza-co`, `smash-city-burgers`, `the-wedge`, `hannibals-kitchen`.
Burns Alley at `$` would be the **fifth**, tying rather than setting a floor.
It would be the cheapest **on this list**, which is presumably the intent.

**Second problem: no price tier was sourceable for any of the five.** Yelp
returns HTTP 403 to automated fetching, and no other source consulted
carried a tier for these venues.

**Recommendation: ship `priceRange: null` on all four net-new entries**, per
the `_meta.fieldPolicy` rule that empty-and-honest beats filled-and-
fabricated. This matches `hachiya-ramen`, all six `best-italian` entries and
two of four `best-seafood` entries. `moes-crosstown-tavern` keeps its
existing `$$` untouched. Fourteen of 49 entries already ship null, so this
is the tree's normal state, not a gap.

**The existing `priceRange` sweep TRACKED item fires again and should again
not be serviced here.** It asks for a re-derivation "from one source" across
the affected entries; that is a sweep, not something to do one entry at a
time inside a launch PR. Best-seafood made the same call. The trigger has
now fired **twice** without being serviced, which is worth noting on the
item - a trigger that never gets serviced is the #19 NEW-pill failure mode
in miniature.

---

## 8. STEP 4 - drafted content. DRAFT ONLY, nothing applied

### 8a. Ranking length and subtitle - verified against the tree, not the prompt

Top-5 is canonical, so the subtitle takes the **bare** form with **no count
framing and no trailing period**:

    <p class="text-brand-gray mt-4 text-lg font-medium">As voted by Charleston locals</p>

**Verified by re-deriving every ranking page's subtitle and row count:**

| Rows | Pages | Subtitle |
|---|---|---|
| 1 | best-bakery, best-new-coffee-shop | "...locals. One standout - with more to come." |
| 2 | best-frozen-margarita, best-ramen | "...locals. Two standouts - with more to come." |
| 3 | best-ice-cream, best-wings | "...locals. Three standouts - with more to come." |
| 4 | best-new-restaurants, best-seafood | "...locals. Four standouts - with more to come." |
| **5** | **best-casual-spots, best-coffee-shops, best-nice-restaurants, best-pizza, best-tex-mex** | **"As voted by Charleston locals"** |
| 6 | best-italian | "As voted by Charleston locals" |
| 7 | best-burger | "As voted by Charleston locals" |

The rule is exactly as #20/#23 state: counts **below** canonical five take
count framing; five and above take the bare form.

> **Citation drift in the prompt.** It cites "best-italian shipped Top-5
> bare". The **conclusion is right**; the **exemplar has moved**.
> `best-italian` is now **Top-6** - it was promoted with Cane Pazzo on
> 2026-08-27 (six rows, `spots: 6`). It did ship Top-5 bare, but a session
> checking that citation today finds a Top-6 page. The five live Top-5
> precedents are the ones listed above.

### 8b. Taglines - proposed, with grounding stated per entry

House register, derived from the shipped pages: **two short Title-Case noun
phrases separated by a comma, no verbs, roughly three to six words.**
Examples: "Three Floors, Southern Italian"; "No Reservations, Daily Catch";
"Generous Pours, Reliable Slush"; "Brewery, Great Food".

Constraint from the prompt, applied: **two entries are live-music rooms, so
they must not both lead on music.** Resolved by giving the music lead to
**The Royal American**, where a booked touring calendar is the defining
identity, and giving **Burns Alley** its hidden-alley hook instead, where
music is one amenity among several.

| # | Entry | Proposed tagline | Grounding |
|---|---|---|---|
| 1 | Last Saint | **`Cocktails Till 2am, Speakeasy Behind`** | *(prompt's proposal, accepted)* "cocktail bar" - own site; "5pm-2am Daily" - own site; speakeasy at the back - P&C 2025-06-27, "a yellow door at the back of Last Saint will take you into a tucked-away little speakeasy". **All three clauses sourced.** |
| 2 | Moe's Crosstown Tavern | **`Neighborhood Bar, Twenty-Five Years`** | Own site: "Best Neighborhood Bar" 25+ consecutive years; "a local watering hole in the Charleston area for 25+ years". Avoids "Dive Bar" (used on both other rows) and avoids the 2am hook (used on best-wings). **Flag: the award is self-reported - corroborate before shipping the number.** |
| 3 | Graft Wine Shop | **`Wine Shop and Bar, Same Room`** | *(prompt's proposal, accepted with a note)* "a wine shop and wine bar" is verbatim own-site About prose. **"Same Room" is an inference** - supported by the shelf-price-plus-corkage model and "surrounded by shelves of incredible wines", but not stated by any source. Under the recommended name `Graft Wine Shop` this tagline does necessary work: it is the only surface that tells a reader the place is a bar. |
| 4 | The Royal American | **`Original Live Music, Kitchen Till 1am`** | Own site: "original live music from the best local, regional, and national artists"; "Kitchen open 'til 1am every damn day". **Both clauses near-verbatim from the own site.** Takes the music lead. |
| 5 | Burns Alley Tavern | **`Down an Alley, Off Lower King`** | "tucked away in an alley off lower King Street" - multiply sourced; two entrances, one via Burns Lane; ZIP 29401 corroborates lower peninsula. **Does not lead on music** (per the constraint), does not repeat "Dive Bar" a third time across the site, and keeps the college framing out of the shop window. |

**Nothing above is ungrounded**, with two flags stated rather than buried:
Moe's award number needs corroboration, and Graft's "Same Room" is an
inference from a sourced mechanism rather than a sourced phrase.

**Alternatives, drafted so the operator has a real choice:**

- Moe's, if the award does not corroborate: **`Vintage Pub, Hampton Park`** -
  "vintage pub" is the own site's own words and needs no external support;
  "Hampton Park" is the stored neighborhood.
- Burns Alley, **only if the two-floors claim gets one unhedged source**:
  **`Two Floors, Down an Alley`**. The form has direct precedent (`sorelle`
  ships "Three Floors, Southern Italian"). Not recommended as-is because the
  sole source hedges with scare quotes - see 4d.
- Burns Alley, if the operator wants the college angle surfaced:
  **`College Town Staple, Down an Alley`**. **Register risk flagged:** the
  characterization comes from reviews, not the venue, and on a
  voted-by-locals list "college bar" can read as a caveat rather than a
  recommendation.
- Graft, if "Same Room" is judged too inferential:
  **`Buy Off the Shelf, Drink It Here`** - describes the sourced
  retail-plus-corkage mechanism directly. Slightly outside the noun-phrase
  register.

### 8c. Hero emoji - the binding constraint is not the one the prompt names

**Proposal: U+1F37B CLINKING BEER MUGS.** `aria-label: "clinking beer mugs"`.

**The rule first, correctly stated.** Per the best-seafood finding, the site's
actual rule is **never a LIVE animal**; a served preparation is admissible,
*including an animal presented as food* (U+1F357 POULTRY LEG on best-wings
is the precedent that establishes it). **For a bar category this rule does
not bind at all** - every candidate glyph is drinkware. So the constraint
that actually decides this is collision, and the prompt identifies only half
of it.

**Full census of hero emoji in use, re-derived from the pages:**

| Page | Codepoint | Name |
|---|---|---|
| best-bakery | U+1F950 | CROISSANT |
| best-burger | U+1F354 | HAMBURGER |
| best-casual-spots | U+1F919 | CALL ME HAND |
| best-coffee-shops | U+2615 | HOT BEVERAGE |
| best-frozen-margarita | **U+1F379** | **TROPICAL DRINK** |
| best-ice-cream | U+1F366 | SOFT ICE CREAM |
| best-italian | U+1F35D | SPAGHETTI |
| best-new-coffee-shop | U+2615 | HOT BEVERAGE *(reused)* |
| best-new-restaurants | U+2728 | SPARKLES |
| best-nice-restaurants | **U+1F377** | **WINE GLASS** |
| best-pizza | U+1F355 | SLICE OF PIZZA |
| best-ramen | U+1F35C | STEAMING BOWL |
| best-seafood | U+1F9AA | OYSTER |
| best-tex-mex | U+1F32E | TACO |
| best-wings | U+1F357 | POULTRY LEG |

**The prompt names TROPICAL DRINK as the collision to avoid. It misses
U+1F377 WINE GLASS**, already on `best-nice-restaurants` - which is the more
awkward of the two, because it is the single most obvious "bar" glyph *and*
because Graft is a wine bar, so it would read as a category label rather
than a page theme.

So **two stemmed-drinkware glyphs are already taken**, and that rules out
the obvious remaining ones on visual grounds:

- **U+1F378 COCKTAIL GLASS** - a third stemmed glass. At the row-icon size
  it is easily confused with TROPICAL DRINK, which is literally a stemmed
  glass with garnish. It also privileges Last Saint over the dive bars.
  **Rejected.**
- **U+1F942 CLINKING GLASSES** - two stemmed flutes. Collides with WINE
  GLASS and reads celebratory/wine rather than "bar". **Rejected.**
- **U+1F943 TUMBLER GLASS** - a squat rocks glass. Genuinely distinct
  silhouette and admirably drink-neutral. **Viable fallback**, but it is a
  small low-contrast amber shape that reads poorly at 20px.
- **U+1F37B CLINKING BEER MUGS** - **recommended.** Two tilted mugs with
  foam: the only candidate whose silhouette is not a single glass, so it is
  unmistakable next to both taken glyphs at small size. It reads "bar as a
  place" rather than "one specific drink", which suits a roster spanning a
  cocktail bar, a wine bar, a sports tavern and two dive bars. Its
  beer-leaning is the honest cost, and it under-serves Graft slightly.

This matters because per `_template-canonical.html` intentional decision #1
the hero emoji is **reused as the leading icon on every row**: at Top-5 that
is **1 hero (no `aria-label`) + 5 rows (each `aria-label`ed) = 6
occurrences**. Small-size legibility is the dominant criterion.

**`aria-label` convention**, verified across the shipped pages: plain
lowercase names - `pizza slice`, `hamburger`, `taco`, `coffee`, `wine
glass`, `sparkles`, `shaka`, `tropical drink`, `poultry leg`, `oyster`.
So: **`clinking beer mugs`**.

**No Twemoji implication.** Verified: `social/.emoji-cache/` contains exactly
two files, `1f950.svg` and `2615.svg` - the hero emoji of the two
**featured-1** pages. `extractHeroEmoji()` is called only from
`loadFeatured1()`; `loadTopN()` never calls it and its rows carry
`{rank, name, tagline}` only. **A Top-5 launch triggers no Twemoji fetch and
adds no cache entry.**

### 8d. Proposed `data/restaurants.json` entries - DRAFT

Four net-new entries plus one append. Field order follows the tree's
convention. `geoLat`, `geoLng`, `imageURL`, `editorialBody`, `areaServed`
are `null` throughout, matching every recent launch.

**1. `last-saint`**

    slug:               "last-saint"
    name:               "Last Saint"
    tagline:            "Cocktails Till 2am, Speakeasy Behind"
    cuisine:            "Cocktail Bar"
    neighborhood:       "Eastside"
    schemaType:         "BarOrPub"
    monthYear:          "August 2026"
    address:            472 Meeting St, Charleston, SC 29403, US
    phone:              null            <- confirmed none exists, see 4a
    hours:              "Mo-Su 17:00-02:00"
    hoursHumanReadable: "Mon-Sun: 5pm-2am"
    priceRange:         null
    websiteURL:         "https://www.lastsaintchs.com"
    appearsOn:          [ best-bar ]

**2. `graft-wine-shop`**

    slug:               "graft-wine-shop"
    name:               "Graft Wine Shop"
    tagline:            "Wine Shop and Bar, Same Room"
    cuisine:            "Wine Bar"
    neighborhood:       "Upper King"
    schemaType:         "BarOrPub"
    monthYear:          "August 2026"
    address:            700 King St Suite B, Charleston, SC 29403, US
    phone:              "+1-843-718-3359"
    hours:              "Mo-Su 12:00-22:00"
    hoursHumanReadable: "Mon-Sun: 12pm-10pm\nBar service from 4pm Mon-Thu, 2pm Fri"
    priceRange:         null
    websiteURL:         "https://www.graftchs.com"
    appearsOn:          [ best-bar ]

**3. `the-royal-american`**

    slug:               "the-royal-american"
    name:               "The Royal American"
    tagline:            "Original Live Music, Kitchen Till 1am"
    cuisine:            "Bar Food"
    neighborhood:       "NoMo"
    schemaType:         "BarOrPub"
    monthYear:          "August 2026"
    address:            970 Morrison Dr, Charleston, SC 29403, US
    phone:              "+1-843-817-6925"
    hours:              "Mo-Su 11:00-02:00"
    hoursHumanReadable: "Mon-Sun: 11am-2am"
    priceRange:         null
    websiteURL:         "https://www.theroyalamerican.com"
    appearsOn:          [ best-bar ]

**4. `burns-alley-tavern`**

    slug:               "burns-alley-tavern"
    name:               "Burns Alley Tavern"
    tagline:            "Down an Alley, Off Lower King"
    cuisine:            "Dive Bar"
    neighborhood:       "Lower King"
    schemaType:         "BarOrPub"
    monthYear:          "August 2026"
    address:            354B King St, Charleston, SC 29401, US
    phone:              "+1-843-723-6735"
    hours:              "Mo-Su 12:00-02:00"
    hoursHumanReadable: "Mon-Sun: 12pm-2am"
    priceRange:         null
    websiteURL:         "https://burnsalley.com"
    appearsOn:          [ best-bar ]

**5. `moes-crosstown-tavern` - append only**

    appearsOn += { "url":   "/rankings/best-bar.html",
                   "title": "Best Bar in Charleston" }

    dateModified (in the rendered HTML, by hand after regen):
                   2026-08-24T12:00:00-04:00  ->  2026-08-28T12:00:00-04:00

**No other field on Moe's is touched in the launch PR.** All prose changes
belong to the 2b cascade PR, which lands first.

**`description` and `shareTagline`** for the four net-new entries are not
drafted here - they are hand-authored prose and want an editorial pass with
the operator rather than a draft that gets rubber-stamped. All the sourced
material needed is in sections 4 and 5.

### 8e. Neighborhood determinations - all four have direct tree precedent

| Entry | Value | Grounding |
|---|---|---|
| Last Saint | `Eastside` | Own site: "an eastside cocktail bar". Tree precedent: `hannibals-kitchen` (16 Blake St), `smash-city-burgers` (47 Cooper St). **Caveat:** 472 Meeting St sits on the western edge of the Eastside - Meeting Street is conventionally its boundary - where the two precedent addresses sit deeper in. The venue's own characterization is being taken as decisive, and it is the kind of claim a business is well placed to make about itself. Recorded so it is reviewable. |
| Graft Wine Shop | `Upper King` | See 2c. Flanked by 684 and 710 King St, both `Upper King`, same ZIP; P&C body text says "Upper King Street" for this address. Conflicts with suite-mate `tutti-pizza`'s `Westside`, which is the outlier. |
| The Royal American | `NoMo` | Direct precedent: `heavys-barburger` (1137 Morrison Dr) and `santis` (1302 Meeting Street Rd) both ship `NoMo`. Third-party prose independently calls it "the North Morrison corridor locals call NoMo". Strongest of the four. |
| Burns Alley Tavern | `Lower King` | Third-party: "an alley off **lower** King Street". Tree precedent: `167-raw-oyster-bar` (193 King St) is `Lower King`. **ZIP corroborates independently** - Burns Alley is 29401, as is 193 King St, while every `Upper King` / `North Central` / `Westside` King Street entry is 29403. |

Per #23, `keywords` are **not** propagated from `neighborhood` - they are
re-asked for search intent. For Burns Alley in particular, "College of
Charleston bar" belongs in `keywords`, where it is a term people actually
type, rather than in the tagline.

---

## 9. STEP 5 - registry check at 16 categories

### 9a. Count

**15 ranking pages today; `best-bar` makes 16.** Verified three ways, all
agreeing: `rankings/best-*.html` = 15 files; `data/og_rankings.json.rankings`
= 15 entries; `index.html` page-owned grid cards = 15 (counted **after
stripping the two `AUTOGENERATED` chrome blocks**, per #23's verification
guidance - the raw grep returns 45 because the inlined desktop and mobile
nav each link every ranking).

### 9b. Grid, re-derived at both breakpoints from the current `index.html`

The grid container, read fresh at `index.html:171`:

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

Three column counts, but `grid-cols-1` cannot orphan, so two can:

| Cards | `md:grid-cols-2` | `lg:grid-cols-4` |
|---|---|---|
| 15 (today) | 7 rows + **1 orphan** | 3 rows + **3 in the last row** |
| **16 (after)** | **8 rows, CLEAN** | **4 rows, CLEAN** |

**16 is clean at both.**

### 9c. But 16 is NOT the first count clean at both - the prompt's hypothesis is refuted

The prompt says "16 may be the first count clean at both - verify rather than
assume." Verified, and it is not.

Clean at both requires divisibility by 4 (divisible by 4 implies divisible
by 2), so the clean counts are 4, 8, 12, 16. The question is only which of
those the site has actually passed through **under the current grid class**.

Reconstructed from git, reading `index.html` at each grid-class change and
at each ranking launch:

| Commit | Event | Grid class | Cards | md:2 | lg:4 |
|---|---|---|---|---|---|
| `be1d0b7` | - | `md:grid-cols-2` | 7 | - | - |
| `65c9c2d` | best-bakery | `md:grid-cols-3` | 9 | - | - |
| `1d00538` | best-frozen-margarita | **`md:grid-cols-2 lg:grid-cols-4`** | 10 | clean | orphan 2 |
| `cb61c37` | best-wings | same | 11 | orphan 1 | last row 3/4 |
| **`51d8de9`** | **best-ice-cream** | same | **12** | **CLEAN** | **CLEAN** |
| `a8899f7` | best-ramen | same | 13 | orphan 1 | last row 1/4 |
| `7e368e6` | best-italian | same | 14 | clean | last row 2/4 |
| `395587f` | best-seafood | same | 15 | orphan 1 | last row 3/4 |
| *(proposed)* | **best-bar** | same | **16** | **CLEAN** | **CLEAN** |

**The `best-ice-cream` launch already shipped 12 cards clean at both
breakpoints under the identical grid class.** 16 is the **second** such
count, not the first.

### 9d. Does the accept-the-orphan ruling still apply to anything?

**No - nothing on the homepage grid.** At 16 there is no orphan at any
breakpoint, so the ruling has nothing to govern this launch. It remains live
for future counts: 17, 18 and 19 all orphan somewhere, and 17 and 19 are
prime, which is the case #19's reasoning was written about.

**Two documentation findings fall out of checking this:**

1. **#19's grid bullet is stale again.** It says "The grid is
   `grid-cols-1 md:grid-cols-2 lg:grid-cols-4` and stands at **13 cards**."
   The class is right; the count is **15**, and has been since best-seafood.
   This is the third time this one bullet has gone stale (it previously said
   9 cards / `md:grid-cols-3`). **Recommend removing the count from the
   prose entirely** and replacing it with an instruction to re-derive it -
   the same fix #19 already applied to the inlined-page count, where it now
   says "Do not hardcode the number in a plan - run `inline_chrome.py
   --check` first". A number that has gone stale three times should not be a
   number.

2. **#19's cross-reference is dangling.** That same bullet ends "(see #23's
   grid discussion)". **#23 has no grid discussion.** Its only grid mention
   is recipe step 7: *"`index.html` homepage grid card. Adjust `grid-cols`
   only if the count genuinely breaks the layout."* The orphan reasoning -
   "no column count divides a prime" - lives **only in #19 itself**. This is
   the same class as the emoji-rule finding from best-seafood: a convention
   pointing at a home it does not have. Cheap to fix in the next docs pass.

### 9e. The other registry surfaces

| Surface | Current | Change |
|---|---|---|
| `data/og_rankings.json` | 15 entries | append `{"slug": "best-bar", "category": "Bar", "spots": 5}`; bump `_meta.lastUpdated` to `2026-08-28` |
| `components/header.html` desktop | entries at lines 31-45 | append after `best-seafood` (line 45), **below** the Top-N divider, plain classes, **no NEW pill** |
| `components/header.html` mobile | entries at lines 69-83 | append after `best-seafood` (line 83) |
| `index.html` | 15 cards, grid at line 171 | append 16th card, `border-transparent hover:border-brand-orange/20`; **do not touch `grid-cols`** |
| `vote.html` | 13 `<option>` entries, lines 163-175 | append `<option value="Best Bar">Best Bar</option>` |

**A header asymmetry worth knowing before editing.** The **desktop** dropdown
has a divider (`<div class="h-px bg-gray-100 my-1 mx-4"></div>`) between the
general/new cluster (Nice Restaurants, New Restaurants, New Coffee Shop,
Bakery) and the dish-category cluster (Pizza through Seafood). The **mobile**
menu has **no such divider** - it is a flat list, and its only divider (line
85) separates the whole rankings list from About/Vote. So "below the
divider" per #23 step 6 is meaningful on desktop and vacuous on mobile; on
both, `best-bar` simply appends after `best-seafood`.

`vote.html` carries 13 options, not 15, because the two **featured-1** pages
(`best-bakery`, `best-new-coffee-shop`) are excluded - they route discovery
through `/suggest-category` per #23 step 8. `best-bar` is Top-N, so it is
included, making 14.

**The `social/src/data.ts` divergence does NOT fire.** That TRACKED item's
trigger is "before the next **hyphenated or multi-word** ranking slug ships".
`best-bar` is a single token after the `best-` prefix: the social loader
computes `"bar".split("-").map(titleCase).join(" ")` = **"Bar"**, and
`og_rankings.json` would carry **"Bar"**. The two paths agree. **A near
miss, not a hit** - worth noting on the item that the trigger survived
another launch untested, so the divergence is still silent and still
unfixed.

---

## 10. Files this PR (or PRs) would touch

**Recommended shape: two PRs**, per the 2b recommendation and the Bar Weems
precedent.

### PR 1 - Moe's editorial cascade (lands FIRST)

| File | Change |
|---|---|
| `data/restaurants.json` | `moes-crosstown-tavern`: broaden `tagline`, `description`, `shareTagline`, `keywords` off the burger-only framing |
| `restaurants/moes-crosstown-tavern.html` | regen via `python scripts/generate_detail_page.py moes-crosstown-tavern`, then hand-bump `dateModified` |
| `assets/images/og-restaurant-moes-crosstown-tavern.png` | regen - the OG meta-line reads from the prose fields |
| `sitemap.xml` | regen **after** the bump |
| `_strategy/TRACKED.md` | move the Moe's item to Resolved |

Small, reviewable, and self-contained - which is what the TRACKED item asked
for when it said the cascade was kept out of the launch diff.

### PR 2 - the `best-bar` launch

| File | Change |
|---|---|
| `rankings/best-bar.html` | **NEW**, from `_template-canonical.html`; production JSON-LD (per-item `url` + `datePublished`/`dateModified`), 5 rows, **ItemList block BEFORE BreadcrumbList** |
| `data/og_rankings.json` | append `{best-bar, Bar, 5}`; bump `_meta.lastUpdated` |
| `data/restaurants.json` | 4 new entries; `appearsOn` append on Moe's; bump `_meta.lastUpdated` |
| `restaurants/last-saint.html` | **NEW** - `generate_detail_page.py last-saint` |
| `restaurants/graft-wine-shop.html` | **NEW** |
| `restaurants/the-royal-american.html` | **NEW** |
| `restaurants/burns-alley-tavern.html` | **NEW** |
| `restaurants/moes-crosstown-tavern.html` | regen + hand-bump `dateModified` to `2026-08-28T12:00:00-04:00` |
| `components/header.html` | nav entry x2 (desktop + mobile), no NEW pill |
| `index.html` | 16th grid card; **no `grid-cols` change** |
| `vote.html` | `<option>` appended |
| `assets/images/og-best-bar.png` | **NEW** |
| `assets/images/og-restaurant-{4 slugs}.png` | **NEW** x4 |
| `assets/images/og-restaurant-moes-crosstown-tavern.png` | regen |
| `sitemap.xml` | regen, **last** |
| all inlined pages | `python scripts/inline_chrome.py --refresh` |
| `rankings/_template-canonical.html` | one line: `(future bar page)` -> `best-bar` |
| `_strategy/TRACKED.md` | see section 11 |
| `rankings/_best-bar-launch-analysis.md` | this file |

**Social assets are a separate follow-up PR**, per #23 step 12.

### 10a. Baselines measured now, so the build pass has real numbers

- `python scripts/inline_chrome.py --check` -> **`[OK] 72 files in sync`**.
  After the launch: 72 + 1 ranking + 4 detail = **77 expected**. Per #19,
  re-run `--check` and use *that* as the baseline rather than trusting this
  number.
- `restaurants/*.html` = **49**; after: 53.
- `assets/images/og-restaurant-*.png` = **49**; after: 53.
- `assets/images/og-*.png` total = **65**; after: 70.
- `sitemap.xml` `<url>` entries = **69**; after: 74.

### 10b. Ordering constraints that will bite this launch specifically

- **`generate_sitemap.py` runs LAST**, after every `dateModified` bump. It
  reads `dateModified` to build `<lastmod>`; run it early and the sitemap
  ships stale dates **silently**.
- **ItemList JSON-LD must precede BreadcrumbList** in `best-bar.html`.
  `generate_sitemap.py` parses only the *first* `ld+json` block; reverse
  them and `<lastmod>` vanishes with no error. Verified that all three
  recent launches put ItemList first.
- **All new pages must exist before `inline_chrome.py --refresh`**, or they
  ship with stale chrome and `--check` exits 2.
- **`generate_detail_page.py` seeds dates in UTC.** Four new pages means
  **eight** stamps to hand-normalize from `+00:00` to
  `2026-08-28T12:00:00-04:00`. The best-italian launch did ten in one pass
  and the TRACKED item notes the workaround scales linearly while the
  generator fix is constant. **This launch is another data point for fixing
  the generator instead.**
- **`npm run build:css` only if new utility classes appear.** Copying an
  existing page introduces none - verify with a class-set diff rather than
  running it reflexively.
- **Playwright Chromium must be installed** before `generate_og_images.py`
  will run: `python -m playwright install chromium`.

### 10c. Traps that are not bugs

- `{{Emoji}}` in `og-templates/ranking.html` - inside an HTML comment,
  deliberately unsubstituted since schemaVersion 1.1. Leave it.
- `{{Emoji}}`, `{{Restaurant#}}`, `{{Tagline#}}` surviving in the shipped
  ranking page - inside the REPEATING ROW documentation comment. Every
  production Top-N page carries them. A placeholder sweep must exclude HTML
  comments.
- `inline_chrome.py` writing LF against a CRLF working copy - cosmetic, per
  `core.autocrlf`.
- Any live-verification regex must tolerate **single or double quotes, any
  attribute order, and an optional `.html`** - Netlify rewrites all three -
  and must strip the `AUTOGENERATED` blocks before asserting on page-owned
  content.

### 10d. Merge

Squash subject must be set explicitly - GitHub defaults it to the PR title,
which lands on `main` without a type prefix. Ranking launches are `feat`;
the cascade PR is `fix` or `chore`.

    gh pr merge {N} --squash --subject "feat: ... (#{N})" --body-file {body} --delete-branch

---

## 11. TRACKED entries this launch would generate

Per #22, these must land as a **same-PR file edit**, not PR-description
prose.

**New - roster exclusions (no trigger, both):**

1. **Salty Mike's - excluded by the operator over a post-ownership-change
   shift locals describe as touristy.** Not sourced; a consensus call, not a
   liveness or identity failure. No-trigger record; re-proposal would need a
   new consensus signal.
2. **Little Palm - excluded by the operator as a hotel pool restaurant
   rather than a bar.** Fails the #23 rule 5 category test on its face.
   No-trigger record.

**New - findings:**

3. **`tutti-pizza` ships `neighborhood: "Westside"` at 700 King St, between
   two `Upper King` entries in the same ZIP.** The tree's only Westside
   entry. Graft ships `Upper King` at the same street address on independent
   evidence (P&C body text). Two businesses at one address cannot be in two
   neighborhoods - the `gustards-custard` ZIP logic, one field over. Trigger:
   next edit to `tutti-pizza`. Cheap; deliberately not fixed in the launch PR
   because Tutti receives no `dateModified` bump here.
4. **`the-harbinger-cafe-bakery` (1107 King St, `North Central`) and
   `ok-donna` (1117 King St, `Upper King`)** - same class, ten street
   numbers apart, but genuinely fuzzy since the two districts overlap.
   **No-trigger observation.**
5. **The Royal American's ownership group runs six distinct brands** - Taco
   Boy, The Royal American, Park & Grove, The Bounty Bar (Folly Beach),
   Johnny's Garage (Hanahan), The Green Hearth Project. **None is a
   `locations[]` secondary.** No-trigger record, so a future session does not
   re-derive it. Same treatment as Volpe and Seahorse.
6. **Last Saint's owner Joey Goetz is bar director at `ok-donna`, already in
   the tree**, plus further King Street and "Italian-ish" projects. Separate
   brands, not locations. No-trigger record.
7. **`last-saint` ships `phone: null` - confirmed absent, not uncollected.**
   Own `/contact` page, homepage and a bar-specific directory all carry no
   phone; contact routes through email and Resy. Recorded so a future
   session does not "fix" it by inventing one.
8. **`last-saint` ships `472 Meeting St` with no unit letter.** The prompt
   supplied "B"; the building does have lettered units, but no source
   assigns one to Last Saint. Trigger: if a sourced unit letter surfaces.
9. **Burns Alley Tavern's "two floors" is sourced only to a review that
   hedges it with scare quotes.** Not shipped in the tagline. Trigger: one
   unhedged source, at which point `Two Floors, Down an Alley` becomes
   available (the `sorelle` "Three Floors" precedent).
10. **Graft Wine Shop's freshest dated liveness signal is March 2026**, five
    months older than the other four entries. No negative signal anywhere.
    Trigger: recheck at the next edit to this entry.
11. **`Cocktail Bar` is the dataset's first non-food `cuisine` value.**
    Every prior bar-like entry (Moe's, Little Jack's, Edmund's Oast, Bar
    Weems) carries a food cuisine. Recorded as a deliberate precedent.
12. **`BarOrPub` is the dataset's first use**, sanctioned since #5 and named
    in both docblocks since PR #50 but never shipped - the `best-wings`
    candidate that would have used it (Tru Blues) was excluded. Recorded as
    the precedent-setting instance, like `IceCreamShop` before it.
13. **Graft Wine Shop's retail half is unmodelled in JSON-LD.** `BarOrPub`
    captures the bar; there is no `FoodEstablishment` subclass for a wine
    shop, and the two halves cannot both be the `@type`. Follows `malagon`
    (market + restaurant ships `Restaurant`). No-trigger record.
14. **`priceRange` ships `null` on all four net-new entries** - no tier was
    sourceable (Yelp 403s). Folds into the existing sweep item.

**Amendments to existing items:**

15. **Sorelle Mercato / #17 same-address sub-venue - THE TRIGGER FIRED.**
    Annex @ Last Saint is the second instance the item was explicitly
    waiting for. Recommend amending #17 with the language in 4a, including
    the new wrinkle: a **distinct reservation listing** does not make a
    sub-venue a location; only a distinct address does.
16. **Zero bench - fifth consecutive launch.** Append to the best-seafood
    item rather than filing anew.
17. **`servesCuisine` generic-override no-op - third instance, with a new
    wrinkle.** On a **venue-type** category rather than a cuisine category,
    the list category ("Bar") is not a usable `servesCuisine` value at all,
    so the override clause is not merely a no-op but inapplicable.
18. **`priceRange` sweep - trigger fired a second time without being
    serviced.** Worth noting on the item.
19. **UTC date seeding - four new pages, eight stamps** to hand-normalize.
    Another data point for fixing the generator.
20. **`social/src/data.ts` - trigger did NOT fire.** `best-bar` is a single
    token and agrees on both paths. Note the near-miss on the item.

**To close:**

21. **`IceCreamShop` missing from the schemaType docblocks - RESOLVED.** The
    work landed in PR #50 (`8c697db`); both lists carry `IceCreamShop`,
    `BarOrPub` and the "ILLUSTRATIVE, NOT AN ALLOWLIST" note. Move to
    Resolved.

**Documentation follow-ups (next docs PR, not this launch):**

22. **#19's homepage-grid bullet says "13 cards"; it is 15.** Third time
    stale. Replace the number with an instruction to re-derive it.
23. **#19 points at "#23's grid discussion", which does not exist.** The
    orphan reasoning lives only in #19.

---

## 12. Where this prompt and the recipe/tree disagree

Collected rather than resolved silently, per the prompt.

| # | Prompt says | Actual | Severity |
|---|---|---|---|
| 1 | Graft is "Graft Wine Shop & Wine Bar" | Own site masthead and heading both say **"Graft Wine Shop"**; the long form is social/aggregator only | **Material** - changes name, slug, and the dedup outcome |
| 2 | Graft "daily 12:00-22:00" | That is the **retail** half; the **bar** opens 16:00 Mon-Thu and 14:00 Fri | **Material** on a bar list |
| 3 | Last Saint at "472 Meeting St B" | No source assigns Last Saint a unit letter; own site prints none | **Material** - a fabricated address component |
| 4 | Burns Alley is "price level 1 - the cheapest entry" | Four entries already ship `$`; and no price tier was sourceable for any of the five | **Material** - both the tier and the superlative |
| 5 | Burns Alley has "two floors" | Sourced only to a review that hedges it with scare quotes | **Moderate** - not shippable as a flat claim |
| 6 | Ampersand handling needed for Graft | Dissolves under the correct name; and the tree already has the precedent (`the-harbinger-cafe-bakery` drops `&` from the slug) | Moderate |
| 7 | Emoji: avoid TROPICAL DRINK | Also **U+1F377 WINE GLASS**, already on `best-nice-restaurants` - the more awkward collision, since Graft is a wine bar | **Moderate** - the prompt names half the constraint |
| 8 | Emoji rule is "never a LIVE animal" | Correct, and correctly stated - but it **does not bind here**, since every candidate is drinkware. The real constraint is collision | Minor framing |
| 9 | "16 may be the first count clean at both" | **12 already was**, at the best-ice-cream launch, under the identical grid class | **Moderate** - hypothesis refuted |
| 10 | "best-italian shipped Top-5 bare" | True historically, but it is **Top-6 now** (Cane Pazzo, 2026-08-27). Conclusion holds; exemplar has moved | Minor citation drift |
| 11 | Bounty Bar is "sister bar on Folly" | Correct - **and there is a third sibling, Johnny's Garage**, named in the same own-site sentence | Minor omission |
| 12 | Graft and Tutti are "under common ownership" | **Not corroborated.** Graft's own site names two sommelier owners and no pizza concept | Minor - changes no recommendation |
| 13 | "per amended #23 rule 1" | The tree-first rule is #23 **section 0a**; "rule 1" is the own-site-liveness rule. House shorthand, used the same way in the best-seafood file | Cosmetic |
| 14 | "Re-derive the grid at both breakpoints" | There are **three** column counts (1 / 2 / 4); two can orphan, so "both" is right if it means those two | Cosmetic |

**Where the prompt was right and worth crediting:** Moe's is the third
listing at position 2; the TRACKED item exists and this launch is its stated
trigger; Graft and Tutti do share 700 King St; all four others are net-new on
slug and name; `BarOrPub` would be the first use and is still sanctioned;
`cuisine` really is awkward for bars; `Burns Alley Tavern` + `Tavern` really
does trip suppression; Top-5 really does take the bare subtitle; the
definite article really does belong in name and slug; Bounty really is a
separate business; the Annex really is the Sorelle Mercato class; and 16
really is clean at both breakpoints. The prompt's instinct to have the dedup
module **run rather than predicted** is what surfaced the Royal American
suppression, which nobody predicted.

---

## 13. Open questions requiring an operator decision before a build pass

> **All eight resolved 2026-08-28. See section 15.** The questions are kept
> as written so the record shows what was open, not only what was chosen.

1. **Moe's cascade: split into a PR that lands first?** Recommended, per 2b
   and the Bar Weems precedent. **Reported, not decided.**
2. **Graft's name: `Graft Wine Shop` (recommended, own-site masthead),
   `Graft` (own-site body prose), or `Graft Wine Shop & Wine Bar` (prompt,
   social/aggregator)?** Decides the slug and the dedup outcome.
3. **Graft's stored `hours`: establishment hours (recommended) or bar-service
   hours?**
4. **Moe's tagline: `Neighborhood Bar, Twenty-Five Years` (needs award
   corroboration) or `Vintage Pub, Hampton Park` (needs nothing)?**
5. **Burns Alley: keep the college framing out of the tagline
   (recommended), or surface it?**
6. **Hero emoji: U+1F37B CLINKING BEER MUGS (recommended) or U+1F943
   TUMBLER GLASS?**
7. **`priceRange`: null on all four (recommended), or attempt a sourced
   sweep across the list first?**
8. **`description` and `shareTagline` for the four net-new entries** - not
   drafted; want an editorial pass.

---

## 14. Verification summary

| Check | Result |
|---|---|
| `main` SHA re-derived, not trusted | `a8d9bb5`, == `origin/main` |
| Branch cut from `main` explicitly | `best-bar-launch` @ `a8d9bb5` |
| Tree-first check run before sourcing | yes - 1 pre-existing, 4 net-new |
| Both #23 gates, run independently | 5 of 5 cleared |
| Category gate (#23 rule 5) | 5 of 5 cleared |
| Pre-existing entry re-verified (#23 rule 4) | Moe's - passed, no stale fields |
| Second-location check (#23 rule 6) | 5 of 5 - all single-location |
| `_cuisine_dedup.py` run, not predicted | yes - found an unanticipated hit |
| Generator `schemaType` support | verified by reading the source, no allowlist |
| Grid re-derived at both breakpoints | yes, and across git history |
| Subtitle convention verified against tree | yes - all 15 pages |
| Emoji census re-derived from pages | yes - 15 pages |
| Twemoji implication | none - cache is featured-1 only |
| Chrome baseline measured | `[OK] 72 files in sync` |

**Nothing in this file has been applied. No files outside this one were
modified. No commit was made.**

---

## 15. Operator resolutions - 2026-08-28

All eight section 13 questions resolved. Recorded here rather than edited
into section 13, so the file shows what was open as well as what was chosen.

### Q1 - Moe's cascade: SPLIT. Yes.

Section 10 stands as written: **two PRs, cascade first.** This file's PR
shape needs no revision.

### Q2 - Graft: `Graft Wine Shop`

**Masthead over body prose**, per the #23 surface hierarchy. The own site's
logo and h2 both read "Graft Wine Shop"; the About page's "Graft is a wine
shop and wine bar" is a *description* of the business, not a rendering of
its name, and it sits one rank lower in the hierarchy besides.

Slug: **`graft-wine-shop`**.

**Recorded consequence, from the section 7b run:** the rejected long form
would have **suppressed the cuisine**. `_cuisine_dedup.py` folds `&` to
" and ", so `Graft Wine Shop & Wine Bar` normalizes to
`graft wine shop and wine bar`, which contains `wine bar` - and cuisine
`Wine Bar` would have been dropped from the `<title>`, `og:title`,
`twitter:title`, hero subtitle and OG image meta-line. Under the chosen
name, `wine bar` is **not** a substring of `graft wine shop`, so the cuisine
displays normally. The name call and the display outcome were coupled, and
the coupling only surfaced because the module was run rather than predicted.

### Q3 - Graft hours: establishment hours

`hours: "Mo-Su 12:00-22:00"`, with the bar window carried in
`hoursHumanReadable`.

**Reasoning given: `openingHours` means open to the public.** The shop and
the bar are one room; a customer can walk in at noon any day. Storing the
narrower bar-service window would assert the venue is shut at times it is
demonstrably open, which is a worse error than under-describing when the
bar is pouring. The bar window is real information and keeps its place in
the human-readable field.

### Q4 - Moe's tagline: `Vintage Pub, Hampton Park`

Both reasons recorded, because the second is reusable:

1. **The award is uncorroborated.** "Best Neighborhood Bar, 25+ consecutive
   years" is self-reported on the own site and traceable to no named poll.
   Treated as marketing, the same as Hank's "voted best seafood."
2. **A year count decays in a permanent tagline.** "Twenty-Five Years" is
   correct on the day it ships and wrong every year after, with nothing in
   the repo to notice. This is the **#19 NEW-pill failure mode in miniature**
   - a value with an expiry date, written in prose, in a file nobody is
   obliged to re-read. #19 retired a convention over exactly this, on the
   evidence that the decay step is never executed as written. A tagline
   should not need maintenance to stay true.

`Vintage Pub, Hampton Park` needs neither corroboration nor maintenance:
"vintage pub" is the own site's own words, and `Hampton Park` is the stored
`neighborhood`.

### Q5 - Burns Alley: college framing stays OUT of the tagline

Tagline remains **`Down an Alley, Off Lower King`**.

The characterization is well sourced and **is recorded** - in section 4d
(the three sources), in section 8b (the rejected alternative
`College Town Staple, Down an Alley`, with its register risk stated), and it
belongs in `keywords`, where "College of Charleston bar" is a term people
actually type. It stays out of the tagline because it comes from reviews
rather than the venue, and on a voted-by-locals list it reads as a caveat
rather than a recommendation.

### Q6 - Hero emoji: U+1F37B CLINKING BEER MUGS

`aria-label: "clinking beer mugs"`. Confirmed as recommended in 8c. Avoids
both taken drink glyphs - U+1F379 TROPICAL DRINK and U+1F377 WINE GLASS -
on silhouette rather than on hue, which is what matters at the row-icon size
where it repeats five times.

### Q7 - `priceRange`: null on all

All four net-new entries ship `priceRange: null`. No tier was sourceable
(Yelp 403s to automated fetching), and per `_meta.fieldPolicy`
empty-and-honest beats filled-and-fabricated. `moes-crosstown-tavern` keeps
its existing `$$` untouched. Fourteen of 49 entries already ship null.

The existing `priceRange` sweep item stays open and stays unserviced here;
it asks for a re-derivation "from one source", which is a sweep, not launch
work.

### Q8 - `description` and `shareTagline`: drafted in PR 2

Not drafted in this pass. To be written in the launch PR, grounded in the
sourced material already collected in sections 4 and 5. Deferred
deliberately: these are the two hand-authored prose fields, and drafting
them here would invite a rubber stamp rather than an editorial read.

### What this changes in the launch PR

Nothing structural. Sections 8d and 10 were drafted against the
recommendations, and all seven recommendations were accepted; Q4 is the only
question resolved **against** the file's first choice, and it swaps one
already-drafted tagline for the already-drafted alternative. The entry for
`graft-wine-shop` in 8d already carries the chosen name, slug, cuisine and
hours.
