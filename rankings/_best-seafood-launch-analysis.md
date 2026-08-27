# Best Seafood launch - analysis working file

Analysis-only working file for the `best-seafood` Top-4 launch. Author: Claude
session 2026-08-27, branch `best-seafood-launch`, cut from `main` @ `d111f60`
(verified clean, `git status --short` empty, before the branch was created).

**Status: analysis complete; prep pass complete; launch NOT built.** Every
field in sections 0-12 is a proposal. Section 11 lists the points where the
analysis prompt and the tree/recipe disagree; section 12 lists what needed an
operator decision.

**Sections 13-15 were added by the prep pass on 2026-08-27** and supersede
parts of what precedes them: section 13 scopes the new CI gate, section 14 is
the call script for the one unresolved field, and **section 15 records the
operator's resolutions**. Where a drafted section was superseded, it says so
inline rather than being rewritten - the draft is the record of the reasoning,
section 15 is the record of the decision. Same convention as
`_best-ramen-launch-analysis.md` section 11 and
`_best-italian-launch-analysis.md` section 13.

Location per `_strategy/WORKFLOW.md`: underscore-prefixed, in the directory of
the work it supports (`rankings/`), not `_strategy/`. Same as
`_best-wings-launch-analysis.md`, `_best-ice-cream-launch-analysis.md`,
`_best-ramen-launch-analysis.md` and `_best-italian-launch-analysis.md`.

---

## 0. Roster and scope

Operator-confirmed order, Top-4:

| # | Name (proposed) | Tree status |
|---|---|---|
| 1 | Chubby Fish | **pre-existing** - `appearsOn` append + `dateModified` bump |
| 2 | 167 Raw Oyster Bar | **net-new** - full entry, detail page, OG image |
| 3 | The Ordinary | **net-new** - full entry, detail page, OG image |
| 4 | Coda del Pesce | **pre-existing** - `appearsOn` append + `dateModified` bump |

Roster provenance: **operator-supplied**. Per #23's "How much bench" table,
operator rosters have run 0% attrition across best-ice-cream, best-ramen and
best-italian. 2x bench is over-provisioning for this provenance; budget the
verification as real work instead. This roster ships **zero bench** - four
confirmed for a Top-4. That is the fourth consecutive zero-bench launch and
#23 says "Never zero bench, whatever the provenance". Exposure here is
editorial, not structural: a late failure drops the page to Top-3, itself a
documented length with its own count framing (#20, #23). Recorded, not
silently accepted - see section 10.

### 0a. Scope note - the excluded tier is a decision, not an oversight

**Recorded at operator request so a future session does not read the omissions
as gaps in sourcing.**

The roster deliberately excludes the tier of Charleston seafood where **the
setting or the institution is the product rather than the cooking**:

- Bowen's Island
- The Wreck (of the Richard and Charlene)
- Crosby's
- Hyman's Seafood
- the Shem Creek waterfront cluster generally

These were not sourced and failed; they were **not sourced at all**, by
operator decision. The list is about cooking, not about view, longevity or
tourist prominence. A future session proposing any of the above is
re-litigating a settled editorial call, not surfacing a missed candidate.

This is a **no-trigger record** in the sense of #23 rule 3 - its purpose is to
stop re-proposal, not to schedule a recheck.

---

## 1. STEP 0 - branch, and two things the prompt got wrong about the starting state

### 1a. `main` is not at `1a6a429`

The prompt states: *"main synced at 1a6a429, clean."* Verified, and it is
stale by two commits:

```
git rev-parse --short main          -> d111f60
git rev-parse --short origin/main   -> d111f60
git log --oneline main..origin/main -> (empty)
git log --oneline origin/main..main -> (empty)
```

`1a6a429` is `feat: add Cane Pazzo to best-italian at position 4, Top-5 to
Top-6 (#52)`. Two commits have landed on `main` since:

| Commit | PR | Subject |
|---|---|---|
| `bdcb0a4` | #53 | fix: compute footer copyright year instead of hardcoding |
| `d111f60` | #54 | chore: remove YouTube and TikTok links from site footer |

`main` **is** clean and **is** synced with `origin/main` - the "clean, synced"
half of the claim holds. Only the commit id is wrong. Branch was cut from
`d111f60`.

### 1b. The session did not start on `main`, and a bare `checkout -b` would have been wrong

The prompt's STEP 0 reads `git checkout -b best-seafood-launch` with no base,
which presumes the working branch is `main`. It was not:

```
git branch --show-current -> fix/regenerate-built-css  @ 7cb4f89
```

`7cb4f89` is **unmerged** - it is the head of open **PR #55**
(`fix: regenerate built.css to restore missing utility classes`, opened
2026-08-27T14:29:30Z). A bare `git checkout -b best-seafood-launch` would have
based this launch on top of an open, unmerged PR, silently pulling
`assets/css/built.css` into the seafood diff and coupling two unrelated PRs.

Ran instead, with the base named explicitly:

```
git checkout -b best-seafood-launch main
```

Confirmed: `git branch --show-current` -> `best-seafood-launch`,
`git rev-parse --short HEAD` -> `d111f60`, `git status --short` -> empty.

**Note for the build pass:** PR #55 touched `assets/css/built.css` only. Per
#23's "npm run build:css only if new utility classes appear", this launch
copies an existing ranking page and should introduce none - so the two PRs
should not conflict. Verify with a class-set diff at build time rather than
assuming.

### 1c. State changed mid-session - PR #55 merged, `main` moved

> **SUPERSEDED by section 1d.** `main` moved again before the prep pass ran -
> PR #56 has since merged and the rebase actually performed went to `47328e9`,
> not the `0822622` this section names. The reasoning below is retained as the
> record; 1d is the record of what was done.

**Recorded because it invalidates the branch point above, and a build pass must
handle it first.**

While this analysis pass was running, the working copy moved underneath it.
Reflog, read after the file was written:

```
HEAD@{3}  checkout: moving from fix/regenerate-built-css to best-seafood-launch
HEAD@{2}  checkout: moving from best-seafood-launch to main
HEAD@{1}  pull --ff-only: Fast-forward          d111f60 -> 0822622
HEAD@{0}  checkout: moving from main to chore/ci-generated-artifact-gate
```

So, after this branch was cut:

- **PR #55 merged.** `main` is now `0822622`
  (`fix: regenerate built.css to restore missing utility classes (#55)`).
- A new branch **`chore/ci-generated-artifact-gate`** was created from it and is
  the current HEAD, carrying in-progress work (`package.json` modified,
  `.github/` and `scripts/check_built_css.py` untracked).
- **`best-seafood-launch` still exists, intact, at `d111f60`** - now exactly one
  commit behind `main`.

Consequences for the build pass:

1. **Rebase `best-seafood-launch` onto `main` (`0822622`) before starting.**
   The one intervening commit touches `assets/css/built.css` only, so no
   conflict is expected with anything in section 9's file list.
2. **Section 1b's warning is now historical**, not live - the PR it warned about
   has landed. The reasoning is retained because the *rule* it illustrates
   still holds: never `checkout -b` without naming the base when HEAD is not
   `main`.
3. **This file is currently untracked and sitting in the working tree while HEAD
   is on `chore/ci-generated-artifact-gate`.** It belongs on
   `best-seafood-launch`. Move it there before committing, and do not let it
   land in the CI-gate PR.
4. `scripts/check_built_css.py` and the new `.github/` workflow on that branch
   look like a **CI gate for generated artifacts**. If it lands first, it may
   assert that `built.css` is in sync with the sources - worth checking whether
   it also gates the generated detail pages, OG images or sitemap, all of which
   this launch regenerates.

### 1d. Prep pass, 2026-08-27 - PR #56 merged; branch rebased to `47328e9`

The CI-gate work anticipated in 1c landed while the prep pass was starting.
State at the time the rebase ran:

| | |
|---|---|
| `main` | **`47328e9`** - `chore: add CI gate for drift in committed generated artifacts (#56)` |
| `origin/main` | `47328e9` - in sync |
| `chore/ci-generated-artifact-gate` | **deleted** (merged) |
| `best-seafood-launch` | `d111f60` - intact, zero own commits |
| HEAD at pass start | `main`, working tree clean apart from this untracked file |

So the working file was **never in danger of landing in the CI PR** - that PR
had already been committed and merged, and this file was untracked on `main`
rather than on the CI-gate branch. It would, however, have followed HEAD into
whatever branch was cut from `main` next.

**How it was moved.** The CI-gate branch no longer existed and its work was no
longer in the working tree, so no stash, worktree or plumbing was needed - the
simple path was safe by then:

```
git checkout best-seafood-launch     # untracked .md travels with HEAD
git rebase main                      # -> "Successfully rebased and updated"
```

**Rebase result: `best-seafood-launch` @ `47328e9`**, identical to `main`.

**No conflict, and none was possible.** `git merge-base --is-ancestor
best-seafood-launch main` returned true, i.e. the branch had **zero commits of
its own** - the analysis pass deliberately committed nothing. A rebase of an
empty branch is a fast-forward, so the "expect no conflict because PR #55
touched only `built.css`" reasoning, while true, was not what made it safe.

**Deviation from the prep instruction, deliberate:** it said rebase onto `main`
**at `0822622`**. `main` had moved to `47328e9` by then, and `0822622` predates
the CI gate. Rebasing onto the named commit would have left the branch one
commit behind and, more importantly, **without the gate the launch now has to
satisfy** (section 13). Rebased onto current `main` instead.

**Working tree left clean** - `git status --short` shows only this file,
untracked, on `best-seafood-launch`.

---

## 2. STEP 1 - tree first, per amended #23 rule 1

Ran before any sourcing, per section 0a of the recipe ("Cost of the check: one
grep. Cost of skipping it: a split launch").

### 2a. The two expected pre-existing entries - both confirmed, both as predicted

The prompt predicted chubby-fish on best-nice-restaurants and coda-del-pesce
on best-italian. **Both correct.** Current field values as shipped:

**`chubby-fish`** (`data/restaurants.json`, line 1365):

| Field | Current value |
|---|---|
| `name` | `Chubby Fish` |
| `tagline` | `Creative Seafood, Always Fresh` |
| `cuisine` | `Seafood` |
| `neighborhood` | `Cannonborough-Elliotborough` |
| `schemaType` | `Restaurant` |
| `monthYear` | `May 2026` |
| `address` | 252 Coming St #A, Charleston, SC 29403 |
| `phone` | `+1-854-222-3949` |
| `hours` | `Tu-Sa 17:00-22:00` |
| `priceRange` | `$$$` |
| `websiteURL` | `https://chubbyfishcharleston.com` |
| `appearsOn` | `[/rankings/best-nice-restaurants.html]` - **one entry** |
| `geoLat` / `geoLng` / `imageURL` / `editorialBody` / `areaServed` | all `null` |

**`coda-del-pesce`** (line 1893):

| Field | Current value |
|---|---|
| `name` | `Coda del Pesce` (lowercase `del` - **SETTLED**, not re-derived) |
| `tagline` | `Oceanfront Italian, Seafood Led` |
| `cuisine` | `Italian Seafood` |
| `neighborhood` | `Isle of Palms` |
| `schemaType` | `Restaurant` |
| `monthYear` | `August 2026` |
| `address` | 1130 Ocean Blvd, Isle of Palms, SC 29451 |
| `phone` | `+1-843-242-8570` |
| `hours` | `Tu-Sa 17:30-21:00` |
| `priceRange` | `null` |
| `websiteURL` | `https://codadelpesce.com` |
| `appearsOn` | `[/rankings/best-italian.html]` - **one entry** |

Per the prompt's instruction, `Coda del Pesce`'s lowercase `del` was taken as
settled from the best-italian launch and **not re-derived**. It is recorded in
`_best-italian-launch-analysis.md` section 4b.

### 2b. `dateModified` - the two bumps, read from source of truth

`dateModified` lives in the **rendered detail-page JSON-LD**, not in
`data/restaurants.json`. Read from the pages themselves:

| Page | `datePublished` | `dateModified` (current) |
|---|---|---|
| `restaurants/chubby-fish.html` | `2026-05-03T19:03:39-04:00` | `2026-05-03T19:03:39-04:00` |
| `restaurants/coda-del-pesce.html` | `2026-08-26T12:00:00-04:00` | `2026-08-26T12:00:00-04:00` |

Both need a **hand bump** at launch, per #23 rule 4 and step 5 of the step
sequence: the generator preserves prior dates by design, so regeneration alone
leaves them stale.

Note the two carry **different timestamp shapes**. `coda-del-pesce` is
launch-normalized Eastern noon (`T12:00:00-04:00`); `chubby-fish` carries a
real `19:03:39` wall-clock from the 2026-05-03 workstream H bulk port. Both
are Eastern, so neither is the `+00:00` defect #23 flags for
`little-jacks-tavern` / `pubfare-burger` / `weltons-tiny-bakeshop`. Propose
bumping both to `2026-08-27T12:00:00-04:00` (launch-date Eastern noon), which
normalizes `chubby-fish`'s shape as a side effect.

**The two net-new pages will be seeded in UTC by the generator** and must be
hand-normalized to Eastern before shipping - #23's standing workaround, which
"every launch has to remember, and the evidence says launches forget".

### 2c. Citation drift in the prompt - minor, recorded for accuracy

The prompt says the two appends are *"per #23 rule 4 (the PR #34/#36 trap)"*.
Rule 4 of the two-gate sourcing rule reads:

> The gate applies to **pre-existing entries too**, not just new ones. Any
> restaurant about to receive a new listing and a `dateModified` bump must
> clear it first - the bump is an assertion of freshness, and asserting
> freshness about a closed restaurant is worse than saying nothing.

So rule 4 governs **re-running the gates** on pre-existing entries; it
presupposes the append+bump rather than mandating it. The requirement itself
lives in **section 0a's table** ("already present -> an `appearsOn` append, a
regen, and a **hand-bumped `dateModified`**") and in **steps 4 and 5** of the
step sequence. The prompt's instruction is right; only the pointer is loose.

On `#34/#36`: PR **#34** is the documented case in #23 - best-frozen-margarita,
"where both restaurants already existed on another ranking". **#36 is not
referenced anywhere in `DECISIONS.md` or `TRACKED.md`** in connection with this
trap. Recorded rather than silently adopted.

### 2d. The two net-new - confirmed net-new on slug AND name

Per the prompt's instruction to match on both:

```
grep -n -i "chubby|coda|167|ordinary" data/restaurants.json
  -> hits ONLY on chubby-fish (1365-1397) and coda-del-pesce (1893-1925)
  -> zero hits for "167", zero for "ordinary"

grep -rn -i "167 raw|the ordinary|ordinary" --include=*.html --include=*.json
        --include=*.md   (excluding node_modules, .git)
  -> ONE hit, and it is prose:
     _strategy/DECISIONS.md:600  "Top-N pages are dropdown-ordinary by design."
```

Also checked `restaurants/` directly - 46 files, no `167-*`, no
`the-ordinary.html`. **Both are genuinely net-new.** No `bar-weems` situation
here (the best-ramen cautionary case where a "fresh sourcing find" turned out
to be a shipped entry with two wrong fields).

### 2e. Open TRACKED items this launch triggers

Swept `_strategy/TRACKED.md` for items whose trigger this launch fires.

**FIRES - `priceRange` re-derivation on the best-italian entries.**
`TRACKED.md:141`, filed by the best-italian launch:

> `priceRange` is `null` on all five new entries. ... Trigger: **next edit to
> these entries**, or before any price-based surface is added. **Re-derive all
> five from one source rather than mixing listing data with prose adjectives.**

Extended at `TRACKED.md:167` by the Cane Pazzo addition to cover all six.
**Coda del Pesce is one of those entries and this launch edits it**
(`appearsOn` append + `dateModified` bump). The trigger fires. See section 8c
for what this launch can and cannot do about it.

**DOES NOT FIRE - `social/src/data.ts` slug-derived category divergence.**
`TRACKED.md:149`:

> Trigger: **before the next hyphenated or multi-word ranking slug ships**,
> since the divergence is silent.

`best-seafood` is single-token after the `best-` prefix. Verified against the
real code rather than reasoned about - see section 4c. **Both derivation paths
return `Seafood`.** This launch does not fire the trigger and does not fix the
bug; it remains open for the next genuinely hyphenated slug.

**DOES NOT FIRE - DECISIONS #17 same-address sub-venue.** `TRACKED.md`
Sorelle Mercato item, trigger: *"the next time a candidate has a sub-venue
sharing its address."* 167 Raw Oyster Bar's sibling concepts are at **289 East
Bay St**, **5 Fulton St** and **Nantucket MA** - all distinct addresses. The
Ordinary's sibling (FIG) is at **232 Meeting St**. No same-address sub-venue in
this roster. See section 6.

**NOT TRIGGERED but relevant - `dateModified` maintenance discipline**
workstream (`TRACKED.md:192`). Trigger is "when a discrepancy surfaces". This
launch performs two manual bumps correctly; no discrepancy surfaced.

---

## 3. STEP 2 - the two name determinations

### 3a. 167 Raw -> `167 Raw Oyster Bar`

The prompt's preliminary sourcing was **correct**. Established using the
surface hierarchy the prompt specified (logo/masthead > headings > body prose >
title and footer):

`167raw.com` **301-redirects to `167hospitality.com`** - the group site, not
the venue site. The venue's own site is **`167rawoysterbar.com`**. Both were
read.

| Surface | Reads |
|---|---|
| **Logo/masthead** (`167rawoysterbar.com`) | **`167 Raw Oyster Bar`** |
| **Heading** (same) | `167 Raw Oyster Bar` |
| **Group site venue logo** (`167hospitality.com`) | `167 Raw Oyster Bar` |
| Body prose (own site) | `167Raw is a New England style Oyster Bar...` (compressed, no space) |
| Footer (own site) | `(c) 2024 167 Hospitality. All rights reserved.` (parent group) |
| Charleston Magazine dining guide | `167 Raw Oyster Bar` |

The hierarchy resolves cleanly and without conflict. Masthead and headings -
the two highest surfaces - both read **`167 Raw Oyster Bar`**, and an
independent editorial listing corroborates. The body prose `167Raw` is a
compressed inline styling of the same name, not a competing brand; the footer
names the **parent group**, not the venue, and is correctly outranked.

**Proposed `name`: `167 Raw Oyster Bar`.** Address confirmed **193 King St,
Charleston, SC 29401**.

**Proposed `slug`: `167-raw-oyster-bar`.** Follows the tree's full-name
slugification convention - `the-harbinger-cafe-bakery`
("The Harbinger Cafe & Bakery"), `mondos-italian-restaurant`,
`bon-banh-mi-southeast-asian-kitchen`, `tonis-detroit-style-pizza`.

**FLAGGED: this would be the tree's first slug beginning with a digit.** All
46 existing slugs start with a letter. Checked rather than assumed:

| Consumer | Pattern | Digit-safe? |
|---|---|---|
| `scripts/generate_detail_page.py:85` | `re.sub(r'[^a-z0-9]+', '-', ...)` | **yes** - digits explicitly allowed |
| `social/src/data.ts:125` | `/\/restaurants\/([^/]+)\.html$/` | **yes** - `[^/]+` |
| `scripts/generate_sitemap.py:54` | `scan_path.glob("*.html")` | **yes** |

No letters-only slug pattern exists anywhere in `scripts/` or `social/src/`.
The only visible effect is **sitemap ordering** - `sorted()` puts digits before
letters, so `167-raw-oyster-bar.html` sorts to the top of the `restaurants/`
block. Cosmetic, no correctness impact.

### 3b. The Ordinary -> `The Ordinary`, and the tree DOES have leading-"The" precedent

The prompt asked me to *"report whether the tree has any precedent for a
leading 'The' in either field; if none, propose and flag rather than deciding
silently."*

**There is precedent, in both fields, twice.** The prompt anticipated finding
none:

| slug | name |
|---|---|
| `the-wedge` | `The Wedge` |
| `the-harbinger-cafe-bakery` | `The Harbinger Cafe & Bakery` |

Both keep the definite article in the `name` **and** carry it through into the
`slug`. That is a direct, unambiguous precedent, so this is a **precedent
application, not a proposal needing a flag.**

Own-site confirmation: `eattheordinary.com` masthead reads **`The Ordinary`**;
the site describes itself as "Fancy Seafood in Charleston, SC | Est. 2012" with
subtitle **"Oyster Hall"**, and "From the people of FIG."

**Proposed `name`: `The Ordinary`. Proposed `slug`: `the-ordinary`.** No flag
required.

### 3c. Slug collision check

No collisions. `167-raw-oyster-bar` and `the-ordinary` are both absent from
`restaurants/` (46 files) and from `data/restaurants.json` (47 entries).

---

## 4. STEP 2 (cont.) - dedup RUN, and both title-case paths

### 4a. `_cuisine_dedup.py` - run, not predicted, for all four

Executed `scripts/_cuisine_dedup.py` directly against candidate values rather
than reasoning about the outcome, per the prompt's instruction:

| name | cuisine tested | `_should_suppress_cuisine` | `_resolve_display_cuisine` |
|---|---|---|---|
| Chubby Fish | `Seafood` | `False` | `Seafood` |
| Coda del Pesce | `Italian Seafood` | `False` | `Italian Seafood` |
| 167 Raw Oyster Bar | `Seafood` | `False` | `Seafood` |
| **167 Raw Oyster Bar** | **`Oyster Bar`** | **`True`** | **`None` (SUPPRESSED)** |
| 167 Raw Oyster Bar | `Raw Bar` | `False` | `Raw Bar` |
| The Ordinary | `Seafood` | `False` | `Seafood` |
| The Ordinary | `Oyster Bar` | `False` | `Oyster Bar` |

Normalized forms, for the record:

```
'167 Raw Oyster Bar' -> '167 raw oyster bar'
'The Ordinary'       -> 'the ordinary'
'Chubby Fish'        -> 'chubby fish'
'Coda del Pesce'     -> 'coda del pesce'
```

**The live finding: `167 Raw Oyster Bar` + `cuisine: "Oyster Bar"` suppresses.**
`'oyster bar'` is a literal substring of `'167 raw oyster bar'`, so
`_resolve_display_cuisine` returns `None` and the rendering layer drops the
cuisine slot entirely - collapsing the detail-page title to "... in Charleston"
and the OG meta-line to bare "Lower King". That is the DECISIONS #18 mechanism
working correctly, but it is only the **desired** outcome if we intend to
suppress.

**Proposal: `cuisine: "Seafood"` for both net-new entries.** This avoids the
suppression, matches `chubby-fish`'s existing `Seafood`, and keeps the
`servesCuisine` entity-resolution signal intact on the detail page (per #18,
JSON-LD always uses raw `cuisine` regardless of display suppression).

`Raw Bar` was also tested and does **not** suppress, so it remains available if
the operator prefers a more specific descriptor - but see section 8b, where
"Raw Bar" is proposed as tagline copy instead, which is where it does more work.

### 4b. Both existing entries are unaffected

Neither `chubby-fish` (`Seafood`) nor `coda-del-pesce` (`Italian Seafood`)
suppresses. Their display surfaces are unchanged by this launch.

### 4c. `best-seafood` title-cases cleanly through BOTH derivation paths - VERIFIED

The prompt asked for confirmation through both paths. Both were traced in the
actual code, not predicted:

**Path A - `data/og_rankings.json`, hand-authored.** Read verbatim by
`render_ranking()` in `scripts/generate_og_images.py`. Proposed value:
`"category": "Seafood"`.

**Path B - `social/src/data.ts:145-149`, slug-derived:**

```js
const category = slug
  .slice('best-'.length)   // 'best-seafood' -> 'seafood'
  .split('-')              //               -> ['seafood']
  .map(titleCase)          //               -> ['Seafood']
  .join(' ');              //               -> 'Seafood'
```

with `titleCase` (line 360):

```js
function titleCase(s) {
  if (s.length === 0) return s;
  return s[0].toUpperCase() + s.slice(1).toLowerCase();
}
```

**Both paths return `Seafood`.** Page title on both paths: `Best Seafood`.

This is clean **because `seafood` is a single token**. The `TRACKED.md:149`
divergence bites only hyphenated or multi-word slugs (`best-tex-mex` yields
`Tex Mex` on path B against `Tex-Mex` on path A), and `titleCase`'s
`.toLowerCase()` tail would flatten any intentional internal capitalisation -
neither applies here. Same reason `best-italian` was unaffected.

**The underlying bug is not fixed by this launch and should not be read as
fixed.** It remains open for the next hyphenated ranking slug.

---

## 5. STEP 3 - verification. Both gates, run independently

Per the prompt: *"External research has been wrong before."* Nothing supplied
was adopted without an independent check. Two supplied claims turned out to
need correction and one turned out to be going stale - sections 5b, 6b, 11.

### 5a. Liveness gate - dated third-party, REQUIRED

Own sites are **inadmissible** here per #23. Dated third-party signals only:

| Candidate | Dated signals | Verdict |
|---|---|---|
| **Chubby Fish** | Yelp listing "Updated July 2026"; **2026 James Beard Award semifinalist** (Outstanding Restaurant); North America's 50 Best 2026 list entry; SC governor's 2026 culinary-ambassador coverage naming the restaurant | **PASS** - multiple independent, 2026-dated |
| **167 Raw Oyster Bar** | Yelp listing "Updated August 2026", 3,275 reviews; Charleston Magazine dining guide active listing; Tripadvisor active | **PASS** |
| **The Ordinary** | Yelp listing "Updated August 2026", 916 reviews; OpenTable "Updated 2026"; Tripadvisor active | **PASS** |
| **Coda del Pesce** | Yelp listing "Updated July 2026", 248 reviews; Tripadvisor active; restaurantji active | **PASS** |

No closure signals, no conflicts, on any of the four. All four clear the
liveness gate.

Note `yelp.com` returned **HTTP 403** to direct automated fetching - the same
failure mode `TRACKED.md` records for Mondo's own site. Yelp's dated
"Updated {Month} 2026" strings were read from search-result metadata rather
than by fetching the page. Recorded so a future session does not treat the 403
as a novel finding.

### 5b. Identity gate - own site AUTHORITATIVE

**Chubby Fish.** Own site masthead reads **`Chubby Fish CHS`**. The tree
carries `Chubby Fish`. This is the brand-colloquial-not-legal-form convention
already applied to `Santi's` (whose full registered name is "Santi's
Restaurante Mexicano" - `TRACKED.md:240`) and `Tutti Pizza`. **No change
proposed**; recorded so the `CHS` suffix is not re-discovered as a defect.

**167 Raw Oyster Bar.** Section 3a - resolved, no conflict.

**The Ordinary.** Section 3b - resolved, no conflict.

**Coda del Pesce.** Name settled per prompt instruction; not re-derived.

### 5c. Category gate - #23 rule 5, verify the claim not just existence

Every candidate is on a **seafood** list, so seafood must be confirmed on the
menu, not merely inferred from the name.

| Candidate | Category evidence |
|---|---|
| Chubby Fish | Own site: "We proudly offer fresh, Lowcountry seafood"; "DOCK TO TABLE."; menu changes daily; Michelin Guide and 50 Best entries describe raw bar, triggerfish tempura, braised grouper |
| 167 Raw Oyster Bar | Own site: "a New England style Oyster Bar... Our menu highlights the outstanding seafood mecca that is the East Coast"; Charleston Magazine lists raw bar, lobster rolls, po' boys, ceviche |
| The Ordinary | Own site: "Fancy Seafood in Charleston, SC"; subtitle "Oyster Hall"; P&C describes a raw bar and oyster-forward menu |
| Coda del Pesce | Already carries `cuisine: "Italian Seafood"`; menu coverage confirms daily crudo di pesce, primi/secondi/piatti from local catch |

All four **PASS**. Not a single-source check on any of them.

### 5d. Hours - own site corroborates, dated third-party decides

| Candidate | Stored / proposed | Sources | Status |
|---|---|---|---|
| **Chubby Fish** | `Tu-Sa 17:00-22:00` (stored) | Own site: Tue-Sat 5-10pm, Sun-Mon closed ("Gone Fishin'"). Third-party aggregate: Tue-Sat 5:00pm-10:00pm, closed Sun/Mon | **CONFIRMED unchanged.** No edit needed |
| **167 Raw Oyster Bar** | propose `Mo-Sa 11:00-23:00` | Own site: Mon-Sat 11AM-11PM, closed Sundays. Charleston Magazine: "11 a.m. to 11 p.m., Monday through Saturday". Third-party aggregate agrees | **CONVERGING.** Three sources, no dissent |
| **Coda del Pesce** | `Tu-Sa 17:30-21:00` (stored) | Third-party: Tue-Thu 5:30-9:00pm, **Fri-Sat 5:30-9:30pm**, closed Sun/Mon | **MINOR DRIFT** - see below |
| **The Ordinary** | **UNRESOLVED** | see below | **BLOCKED** - operator decision needed |

**Coda del Pesce drift.** The stored single range `Tu-Sa 17:30-21:00` matches
Tue-Thu but is 30 minutes short on Fri-Sat. This matters because of the
best-ramen precedent: *"Discovering that mid-launch forced the work into two
PRs so the corrections could land before the launch regen stamped a fresh
`dateModified` over them."* This launch **will** stamp a fresh `dateModified`
on `coda-del-pesce.html`. Two options, operator's call:

1. **Fix in-PR** (recommended, cheap): the drift is a half-hour on two days,
   one field, already open for the `appearsOn` append.
2. **Accept and record**: the stored value is a defensible simplification of a
   split schedule and the `hours` field format may not express per-day ranges
   cleanly. If accepted, it must be recorded, not left silent - otherwise the
   bump asserts freshness over a value known to be imprecise.

Note this is *drift*, not a resolved-vs-stale conflict: nothing contradicts the
5:30pm open or the Tue-Sat pattern.

**The Ordinary - a genuine three-way conflict.** This is the one field in the
launch that cannot be settled from what is available:

| Claim | Dark day | Opens | Closes |
|---|---|---|---|
| Own site (`eattheordinary.com`, two pages) | **Tuesday** | **4:00pm** | not stated anywhere |
| Yelp-derived aggregate | **Tuesday** | **5:00pm** | 9pm Mon-Thu, 10pm Fri-Sat |
| OpenTable | **Monday** | 5:00pm | 10:30pm nightly |

Applying #23's "count the sources and weight them by recency":

- **Dark day resolves 2-to-1 to Tuesday** (own site + Yelp aggregate). OpenTable
  is the outlier. This half is decided.
- **Open time**: own site says 4:00pm on two separate pages; two third-party
  sources say 5:00pm. #23 says the own site "corroborates, never establishes"
  and the dated third-party majority wins - which gives **5:00pm**. But the own
  site itself supplies a reconciling explanation: *"Join us from 4-5pm for
  half-priced oyster sliders for the month of August!"* That reads as a
  **seasonal early open**, meaning both claims can be true and 4:00pm may be
  August-only. This is not resolvable from public sources.
- **Close time**: 9pm/10pm split vs 10:30pm nightly. Two sources, no majority,
  no own-site value at all. **Genuine deadlock.**

This is exactly the case #13.10 exists for - and #23 warns it is *only* for
genuine deadlock, "not for a resolved question with one stale dissenter". The
dark-day half is resolved; the close-time half is deadlocked.

**Recommendation:** a single phone call to 843.414.7060 settles all three parts
and is far cheaper than shipping `null`. Failing that, ship `hours: null` +
`hoursHumanReadable: null` and let the detail page fall back to the honest
"Hours vary - see [website]" copy per DECISIONS #13 / template intentional
decision #10 - the `tonis-detroit-style-pizza` precedent. **Do not synthesize a
range from the three claims** - that is the fabrication the field policy
forbids.

### 5e. Verifiable facts - independent record wins on contradiction

Checked for the `gustards-custard` failure mode (own site printing a ZIP that
an independent record contradicts). **No contradictions found.**

| Candidate | Address | ZIP cross-check |
|---|---|---|
| 167 Raw Oyster Bar | 193 King St | **29401** - consistent across own site, Charleston Mag, Yelp, Tripadvisor. 193 King is below Calhoun, in the 29401 lower-peninsula band. Consistent |
| The Ordinary | 544 King St | **29403** - consistent across own site, Yelp, Tripadvisor. 544 King is above Calhoun, 29403 band. Consistent |

One stale third-party value worth recording, since it will resurface:
**Tripadvisor files 167 Raw Oyster Bar under neighborhood "Ansonborough".**
That is the **old 289 East Bay St location**, vacated in 2020. It is wrong for
193 King St. A future session cross-checking neighborhood against Tripadvisor
will hit it. Own site and the address itself win.

---

## 6. Second locations - the standing per-candidate check (#23 rule 6)

Run on **all four**, including the two pre-existing ones. Three consecutive
launches hit a pending second location before this one; #23 calls it "a
standing check, not an occasional surprise".

### 6a. 167 Raw Oyster Bar - the prompt's finding is CORRECT, with one wrinkle

The prompt states 167 Sushi Bar and Bar167 are **separate concepts, not
`locations[]` secondaries**. **Verified, and correct.**

| Venue | Address | Own website | Concept |
|---|---|---|---|
| **167 Raw Oyster Bar** | 193 King St, Charleston | `167rawoysterbar.com` | oyster bar (**our entry**) |
| 167 Sushi Bar | 289 East Bay St, Charleston | `167sushibar.com` | sushi |
| BAR167 | 5 Fulton St, Charleston | `bar167charleston.com` | Mediterranean bar/bistro |
| 167 Raw Fish Market | Nantucket, MA | (group site) | retail fish market |

Evidence they are distinct brands rather than locations of one restaurant:

1. **Distinct names.** None is "167 Raw Oyster Bar at {address}". A
   `locations[]` secondary under DECISIONS #17 is the same brand at another
   address; these are four different brands under one parent.
2. **Separate dedicated websites** for each.
3. **The group site classifies them as separate concepts**, each with its own
   logo, under the `167 Hospitality` umbrella.
4. **Distinct cuisines** - sushi, Mediterranean, retail fish market.
5. **Bar167's own origin story confirms the split.** P&C: it began as an
   intended overflow bar for 167 Raw Oyster Bar on King Street, and once
   redevelopment began "Bar 167 quickly took on a life of its own." It started
   as an annex and deliberately became a separate concept.

Bar167 opening date **verified as the prompt states**: opened **Aug 16, 2022**
at 5 Fulton St, the former Fulton Five space (building dates to the 1850s).

**The wrinkle worth flagging:** 167 Raw Oyster Bar's own site groups these
three under a heading that reads **"Our Other Locations"**. Read literally,
that is `locations[]` language. It is the parent group speaking in the venue
site's chrome - the same footer that reads "(c) 2024 167 Hospitality". The
DECISIONS #17 test is *same brand at a different address*, which these fail on
name, website and cuisine. **Proposal: 167 Raw Oyster Bar ships
single-location, no `locations[]`.** Flagged rather than decided silently
because the own site's own wording superficially argues the other way.

### 6b. 167 Sushi Bar is itself relocating - the prompt's premise is going stale

The prompt states: *"167 Sushi Bar now occupies 289 East Bay St."* True today,
**but time-limited**. Post and Courier and What Now Charleston report 167 Sushi
Bar is **moving to a larger historic address** (reported as 5 Cumberland St,
the former Bumpa's space). 289 East Bay St - where Sandole launched the brand
in Charleston - **stays within the group and becomes a new, undetermined
concept.**

Timing is itself contested across sources: one reports "later this year"
(2026), another headlines "Set for Bigger Home in **2027**". Per #23's
tense-reading rule this is future-tense and the window has not clearly arrived.

**No impact on this launch** - 167 Sushi Bar is a separate concept and no field
in our entry references it. Recorded because (a) the prompt's supplied fact has
a shelf life, and (b) a **new undetermined concept at 289 East Bay St** is
exactly the kind of thing a future roster pass should check before treating
that address as vacant. Filed with a re-verification trigger - section 10.

Careful with the two "5" addresses: **BAR167 is at 5 Fulton St**; the sushi bar
is reportedly moving to **5 Cumberland St**. Different streets.

### 6c. The Nantucket question - related business, no treatment required

The prompt asks whether the Nantucket market is a related business requiring
treatment. **It is related, and it requires none.**

P&C: owner **Jesse Sandole opened 167 Raw in Charleston in 2014 as an extension
of his family's seafood market at 167 Hummock Pond Road, Nantucket, Mass.**

Two consequences:

1. **The brand name is an address.** "167" is 167 Hummock Pond Road. That is a
   genuinely useful grounding fact and it is what makes the proposed tagline's
   "New England Roots" a literal statement rather than a vibe - section 8b.
2. **No treatment required.** The Nantucket business is (a) a **retail fish
   market**, a different concept from an oyster bar; (b) branded **167 Raw Fish
   Market**, a different name; and (c) in **Massachusetts** - far outside the
   DECISIONS #14.1 greater-Charleston / Lowcountry editorial scope, which even
   at its most permissive reading covers Hanahan and Summerville, not New
   England. It is neither a `locations[]` secondary nor an `appearsOn`
   candidate.

Filed as a **no-trigger record**: its purpose is to stop a future session
re-deriving the relationship or proposing the Nantucket market as a location.

### 6d. The Ordinary - no second location; FIG is a sibling that is already in the tree

- **Own site mentions no second location** - #23's "strongest negative signal".
- No press coverage of a Mike Lata second Ordinary or expansion surfaced.
- The only other venue named is **FIG**, "from the people of FIG."

**FIG is already an entry in this tree**: `restaurants/fig.html`, 232 Meeting
St, Ansonborough, `priceRange: "$$$$"`, on `best-nice-restaurants`. So The
Ordinary's sibling concept is a **separate existing tree entry at a separate
address** - structurally the same as Coda del Pesce / Volpe and Cane Pazzo /
the Bolchoz concepts. Separate brands under shared ownership, not locations.

**Proposal: The Ordinary ships single-location, no `locations[]`.**

Worth noting the tree now has **three** same-owner pairs among its entries
(Lata: FIG + The Ordinary; London: Chubby Fish + Seahorse; Vedrinski: Coda del
Pesce + Volpe) and **no field expresses that relationship**. Not a defect and
not in scope here; recorded in section 10 as an observation.

### 6e. Chubby Fish - check run for the first time, and it is clean

**This check has never been run on Chubby Fish.** The entry shipped in the
2026-05-03 workstream H bulk port; #23's standing second-location rule was
added **2026-08-26**. So the entry predates the rule. Run now:

- **Own site mentions no second Chubby Fish** - strongest negative signal.
- No press coverage of a second location or expansion surfaced.
- Chef/owner **James London** also owns **Seahorse** in Charleston - a
  **separate concept under the same owner**, same pattern as 6d. Not a location.

**PASS. Ships single-location, no `locations[]`.** Recorded because the entry
had never been subject to the check and a future session should not have to
re-establish that.

Side finding: the tree records no chef/owner for `chubby-fish`. James London is
now sourced (own site, James Beard Foundation, 50 Best). There is no
chef/owner field in the schema, so this is informational only.

### 6f. Coda del Pesce - checked at best-italian launch, unchanged

The best-italian launch established that Ken Vedrinski's sister concept
**Volpe** (161 Rutledge Ave) is a separate brand, and filed the own-site
staleness finding (`TRACKED.md`: the About page still presents the 2020-closed
**Trattoria Lucca** in the present tense) as a **no-trigger record**. Nothing
in this pass changes that. **No new second-location signal.** Ships
single-location.

---

## 7. STEP 5 - registry check at 15 categories

Re-derived from the **current** `index.html`, not inherited from the
best-italian analysis file's claim about 14.

### 7a. Count

`best-seafood` would be the **15th** ranking. Verified three ways, all agreeing
at 14 today:

- `rankings/best-*.html` -> **14** files
- `data/og_rankings.json` `rankings[]` -> **14** entries
- `index.html` homepage grid cards -> **14** (counted inside the grid block
  only, at `index.html:169`; a naive repo-wide grep returns 42 because the nav
  chrome and footer also link every ranking on every page)

### 7b. Grid outcome, re-derived at both breakpoints

`index.html:169`:

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
```

Three breakpoints, not two:

| Breakpoint | Columns | At 14 (today) | At 15 (with best-seafood) |
|---|---|---|---|
| base (`<768px`) | 1 | 14 rows, all full | 15 rows, all full - **no change in kind** |
| `md` (768-1023px) | 2 | 7 full rows, **clean** | 7 full rows **+ 1 orphan** |
| `lg` (`>=1024px`) | 4 | 3 full rows **+ 2 orphans** | 3 full rows **+ 3 in last row** |

So adding the 15th card makes `md` slightly worse (a clean 7x2 becomes a lone
trailing card) and `lg` slightly **better** (a 2-card last row becomes 3, i.e.
closer to full). They move in opposite directions; no single change improves
both.

**Proposal: do not touch `grid-cols`.** Recipe step 7 says adjust "only if the
count genuinely breaks the layout". A trailing orphan at one breakpoint is not
breakage, and it has shipped before - at 13 categories, `md` was 6 full rows
plus an orphan and `lg` was 3 rows plus 1. Odd counts are the normal condition
of this grid; every odd-numbered launch produces one.

### 7c. The other registry surfaces

**`components/header.html`** - two lists, both needing an entry:

- Desktop dropdown, lines 31-44. A divider (`<div class="h-px bg-gray-100 my-1 mx-4">`) sits at line 35, before `best-pizza`. Above it: nice-restaurants, new-restaurants, new-coffee-shop, bakery. Below it: pizza -> italian. **`Best Seafood` appends after `Best Italian` (line 44), below the divider**, per recipe step 6.
- Mobile menu, lines 68-81, no internal divider. **Appends after `Best Italian` (line 81).**
- **No NEW pill** - #23 clause 2, and moot anyway since the pill convention was retired entirely on 2026-08-26.
- Then `python scripts/inline_chrome.py --refresh`, and only **after** the new ranking and both new detail pages exist, or they ship with stale chrome and `--check` exits 2.

**`vote.html`** - 12 `<option>` entries at lines 172-183. Confirmed they are
**Top-N only**: `Best Bakery` and `Best New Coffee Shop` (the two featured-1
pages) are correctly absent, since featured-1 routes discovery through
`/suggest-category` per recipe step 8. **`<option>Best Seafood</option>`
appends at the end, after `Best Italian`.**

**`data/og_rankings.json`** - append `{"slug": "best-seafood", "category":
"Seafood", "spots": 4}` and bump `_meta.lastUpdated`. `spots: 4` is not
cosmetic: `spots === 1` would route the social pipeline into the featured-1
renderer.

### 7d. Twemoji - the prompt's claim is correct, and here is the verification

The prompt notes: *"no Twemoji fetch is implicated - Top-N cards render rank
badges, not emoji."* **Verified, not assumed.**

- `social/src/emoji.ts` fetches Twemoji SVGs from jsDelivr into
  `social/.emoji-cache/`.
- That cache contains exactly **two** files: `1f950.svg` (U+1F950 CROISSANT)
  and `2615.svg` (U+2615 HOT BEVERAGE).
- Those are precisely the hero emoji of the **two featured-1 pages** -
  `best-bakery` and `best-new-coffee-shop`.
- `extractHeroEmoji(html)` is called at `social/src/data.ts:200`, inside
  `loadFeatured1()` (which begins at line 170). `loadTopN()` spans lines
  110-168 and **never calls it**; its rows carry `{rank, name, tagline}` only.

**A Top-4 launch triggers no Twemoji fetch.** The hero emoji chosen in section
8d affects the ranking **page** only, never the social card.

---

## 8. STEP 4 - drafted content. DRAFT ONLY, nothing applied

### 8a. Ranking length and subtitle

**Top-4.** Already a documented precedent (#4, #20) - the full set is
featured-1 / Top-2 / Top-3 / Top-4 / Top-5 / Top-6 / Top-7. No new ranking
length is introduced, so unlike the Cane Pazzo addition there is nothing to add
to #20's enumeration.

Sub-canonical counts take count framing. Verified against the shipped
`best-new-restaurants` page, which is the existing Top-4:

> `As voted by Charleston locals. Four standouts - with more to come.`

**Proposed subtitle: identical to the above.** (For contrast, the shipped
Top-6 `best-italian` correctly carries a bare "As voted by Charleston locals",
since six sits above canonical.)

### 8b. Taglines - all four grounded, one echo to resolve

**Critical convention, verified before drafting:** ranking-row taglines are
**per-page and hand-authored**; they are *not* copies of
`restaurants.json.tagline`. Proven two ways:

1. **Home Team BBQ carries three different taglines** across its three
   rankings: `Smoky, Underrated Gem` (best-burger), `BBQ, Wings, Good Times`
   (best-casual-spots), `BBQ Institution, Wings to Match` (best-wings) - while
   `restaurants.json.tagline` is `BBQ, Wings, Good Times`, matching only one.
2. **The code says so explicitly**, `social/src/data.ts:117-119`:

   > *"Per-ranking taglines come from the page's body rows, not
   > restaurants.json. For cross-listed restaurants (e.g. Home Team BBQ on
   > best-burger AND best-casual-spots), each ranking can carry its own
   > descriptor."*

`restaurants.json.tagline` feeds the **detail page** (`{{Tagline}}` at
`generate_detail_page.py:771`) and the OG image. **So neither existing entry's
stored `tagline` needs to change**, and the two new ranking rows are free to
say something different. This is the convention, not an exception.

| # | Restaurant | Proposed best-seafood row tagline | Grounding | Verdict |
|---|---|---|---|---|
| 1 | Chubby Fish | `No Reservations, Daily Catch` | Own site prints **"NO RESERVATIONS"** verbatim; **"Our menu changes daily"**; **"DOCK TO TABLE."**; "fresh catches straight from the Atlantic Ocean and local rivers". Third-party: "walk-in only", "a daily line at 4pm for walk-in spots" | **GROUNDED** - both halves on the own site verbatim |
| 2 | 167 Raw Oyster Bar | `Raw Bar, New England Roots` | Own site: **"a New England style Oyster Bar"**; menu headed by raw bar selections. "Roots" is literal, not atmospheric: P&C records the Charleston restaurant opened in 2014 **as an extension of the owner's family seafood market at 167 Hummock Pond Road, Nantucket** - the brand name *is* that address | **GROUNDED** - and stronger than it first looks |
| 3 | The Ordinary | `Oyster Hall, Old Bank Building` | **"Oyster Hall" is the own site's own subtitle.** Bank half: P&C, the 544 King lot was sold to a bank in April 1927, opened 1928, designed by Simons and Lapham; **the vault door survives in the dining room** as "one of several signs of the seafood restaurant's previous life as a bank" | **GROUNDED** - see the caution below |
| 4 | Coda del Pesce | `Daily Crudo, Sustainably Caught` (recommended) | **"a daily crudo di pesce on the menu, anointed with oil and preserved lemon, and spiked with Calabrian chiles"**; "primi, secondi and piatti selections that **change daily** based on what's fresh"; "**locally or sustainably caught** seafood" | **GROUNDED** |

**Caution on The Ordinary's bank, and why the tagline survives it.** The prompt
and much secondary coverage say "former Bank of America building built in
1927". Both halves are slightly off:

- The 1927 date is the **lot sale** (9 April 1927); the bank opened **1928**.
- The original occupant was **Peoples-First National Bank**, not Bank of
  America. Bank of America was a **later** occupant whose Upper King branch
  closed, after which The Ordinary took the space.

The proposed tagline says **"Old Bank Building"** - generic on both the bank
name and the date - so it is true under every source. Had it read "1927 Bank of
America Building" it would have been an **inverted claim** in the #23 sense:
every word traceable to a source, and still wrong about what the source says.
**Do not let a later edit sharpen it into a specific bank or year without
re-reading the P&C building history.**

**Coda del Pesce - the two taglines side by side, as requested:**

| Page | Tagline | Pitch |
|---|---|---|
| `best-italian` (shipped, unchanged) | `Oceanfront Italian, Seafood Led` | setting + the Italian frame, seafood as modifier |
| `best-seafood` (proposed) | `Daily Crudo, Sustainably Caught` | the raw preparation + the sourcing standard |

These are meaningfully different pitches - one sells the room and the cuisine,
the other sells a specific dish and how the fish is caught. Neither repeats the
other's claim.

**Two flags on the Coda del Pesce line:**

1. **"Whole local fish" was NOT confirmed and is not used.** The prompt
   suggested grounding in "crudo, whole local fish". Crudo is multiply sourced
   and daily. **Whole-fish preparations did not surface in any source read.**
   Per #23's "negative answers are scoped to the question you asked", the honest
   record is: *the question "does the menu feature whole local fish" returned
   nothing from menu coverage and the own-site press page* - not "the restaurant
   does not serve whole fish". A differently-framed query against the same
   sources may find it. **Do not ship "whole fish" without reading it at
   source.**
2. **An echo to resolve.** The obvious alternative, `Daily Crudo, Local Catch`,
   is equally well grounded but puts **"Catch"** in two of four rows alongside
   Chubby Fish's `No Reservations, Daily Catch`, and **"Daily"** in two rows as
   well. On a four-row page that is a visible repetition.
   `Daily Crudo, Sustainably Caught` keeps the sourcing claim, drops the echo,
   and is sourced to the same sentence. **Recommended.** Operator may prefer
   the alternative; flagged rather than decided silently.

### 8c. `priceRange` - the prompt's premise is out of date, and the two existing entries disagree

**The prompt says: *"all five best-italian entries ship null."* Two corrections:**

1. **There are six, not five.** Cane Pazzo was added at position 4 in PR #52
   (2026-08-27), taking `best-italian` from Top-5 to Top-6.
2. **The "all null" half is correct.** Verified - all six ship `null`:
   wild-olive, coda-del-pesce, le-farfalle, sorelle, mondos-italian-restaurant,
   cane-pazzo.

**What the two existing entries carry - and they do not agree with each other:**

| Entry | `priceRange` |
|---|---|
| `chubby-fish` | **`$$$`** |
| `coda-del-pesce` | **`null`** |

So "propose consistently" has no single target: the roster's two existing
members already differ. Full tree census for context (47 entries): `$$` x23,
`null` x13, `$` x4, `$$$` x4, `$$$$` x3. **Null is not the tree norm** - 34 of
47 carry a value. It is the norm on `best-italian` specifically, because that
list hit an open sourcing problem.

**Where it renders:** `priceRange` appears in **detail-page JSON-LD only**
(`"priceRange": "$$$"` in `chubby-fish.html`; the key is omitted entirely when
null, as in `coda-del-pesce.html`). It does **not** appear on ranking pages -
`grep -c priceRange rankings/best-italian.html` and
`rankings/best-nice-restaurants.html` both return **0**. So the inconsistency
is invisible on the launch page itself and is purely a data-layer question.

**Proposal:**

| Entry | Proposed | Reasoning |
|---|---|---|
| `chubby-fish` | **keep `$$$`** | Shipped value, out of scope. Changing it needs its own sourcing pass |
| `coda-del-pesce` | **keep `null`** | Under the open `TRACKED.md:141` re-derivation item; see below |
| `167-raw-oyster-bar` | **`$$$`** (flagged) | Tripadvisor and restaurantguru both read `$$$`; per-person reports of $40-70 sit in that band; matches its closest peer on the page. **Dissent:** Charleston Magazine tags it **both** `$$$ ($25-$35)` and `$$$$ ($35+)`, which is a dual-tag rather than a clean contradiction. Operator call |
| `the-ordinary` | **`null`** | Genuine split with no majority: Facebook reads `$$$`, review consensus reads `$$$$`, one listing quotes a "$100-per-person price point" (prose, not a listing read). This is the **Cane Pazzo case exactly** - "Sources disagree ... ships null" - and the field policy's empty-and-honest-beats-filled-and-fabricated rule applies |

**On the fired TRACKED trigger.** `TRACKED.md:141` asks that the six
best-italian entries be re-derived **"from one source rather than mixing listing
data with prose adjectives"** - and this launch fires that trigger by editing
Coda del Pesce. **This launch should not attempt that re-derivation.** It is a
six-entry sweep across a different ranking, it is the kind of scope creep that
split the best-ramen launch into two PRs, and doing it badly (one entry at a
time, from whichever source answers first) is precisely what the item warns
against. **Recommendation: note in the PR body that the trigger fired and was
deliberately deferred**, and extend the TRACKED item to record that
`best-seafood` now has the same split - section 10.

### 8d. Hero emoji - proposed U+1F9AA, and the tension is real but narrower than stated

**Proposal: U+1F9AA OYSTER.**

The prompt frames the site's rule as *"food as served, never the animal"* and
concludes that fish, crab and lobster glyphs are out. That conclusion is right.
The **rule as stated is slightly too strong**, and the difference decides this
question - so here is the actual census rather than the assertion:

| Page | Codepoint | Name | As-served? |
|---|---|---|---|
| best-burger | U+1F354 | HAMBURGER | yes |
| best-casual-spots | U+1F919 | CALL ME HAND | n/a - not food |
| best-coffee-shops | U+2615 | HOT BEVERAGE | yes |
| best-frozen-margarita | U+1F379 | TROPICAL DRINK | yes |
| best-ice-cream | U+1F366 | SOFT ICE CREAM | yes |
| best-italian | U+1F35D | SPAGHETTI | yes |
| best-new-restaurants | U+2728 | SPARKLES | n/a - not food |
| best-nice-restaurants | U+1F377 | WINE GLASS | yes |
| best-pizza | U+1F355 | SLICE OF PIZZA | yes |
| best-ramen | U+1F35C | STEAMING BOWL | yes |
| best-tex-mex | U+1F32E | TACO | yes |
| **best-wings** | **U+1F357** | **POULTRY LEG** | **yes - and it is an animal part** |

(`best-bakery` and `best-new-coffee-shop` use the featured-1 template, whose
hero emoji sits in different markup - U+1F950 CROISSANT and U+2615 per the
Twemoji cache.)

**U+1F357 POULTRY LEG is the precedent that decides this.** It depicts a
drumstick - unambiguously an animal part - and it shipped, because it depicts
that part **cooked and served**. So the operative rule the tree actually
follows is not "never the animal" but:

> **never a live animal; a served preparation is admissible, including an
> animal presented as food.**

Under that rule:

- U+1F41F FISH, U+1F420 TROPICAL FISH, U+1F99E LOBSTER, U+1F980 CRAB all depict
  **live animals in habitat** and remain correctly ruled out - the prompt's
  conclusion holds, on slightly different reasoning.
- U+1F9AA OYSTER depicts an **open shell with the meat exposed**. For a raw
  bar, that *is* the plated dish - an oyster on the half shell is not a
  preparation step, it is the service. It sits in the same place as POULTRY LEG:
  an animal, presented as food.
- U+1F364 FRIED SHRIMP is unambiguously as-served and **fails on register**.
  This roster is a James Beard semifinalist, a Charleston Magazine mainstay, a
  2012 James Beard Best New Restaurant nominee and a chef-driven oceanfront
  Italian room. A fried-shrimp glyph reads as a casual fry house and
  mis-describes all four. The prompt's objection is correct.
- U+1F363 SUSHI is as-served but names the wrong cuisine - and would actively
  collide with 167 Sushi Bar, a *different* restaurant in the same group.

**The oyster-forward claim - verified 3 of 4, not asserted:**

| Restaurant | Oyster evidence |
|---|---|
| 167 Raw Oyster Bar | **In the name.** "New England style Oyster Bar" on the own site |
| The Ordinary | **Own site subtitle is "Oyster Hall"**; running August half-price oyster-slider promotion |
| Chubby Fish | Third-party: "sets the benchmark for raw bar offerings: **oysters take pride of place**"; "super-fresh raw oysters"; "grilled oysters with curry" |
| Coda del Pesce | **Not oyster-forward** - crudo-forward. No oyster claim found |

So the prompt's "three of four are oyster-forward" is **confirmed**, and the
fourth is not contradicted, merely different.

**The residual tension, stated honestly:** an oyster on the half shell is
**raw**, and technically alive at service. Under the strictest literal reading
of "food as served, never the animal", U+1F9AA is arguable. It is admissible
under the rule the tree's own POULTRY LEG precedent demonstrates, and there is
no other glyph that is simultaneously as-served, correct in register, and
descriptive of three quarters of the roster. **Recommended, with the reasoning
recorded here so the call is reviewable rather than assumed.**

Reminder from 7d: this choice touches the **ranking page only**. No Twemoji
fetch, no social-card impact, no new cache entry.

**Where it appears on the page - five occurrences, not one.** Measured on the
shipped `best-wings.html` (comments stripped, so the REPEATING ROW
documentation block is excluded):

| Occurrence | Markup |
|---|---|
| 1 - hero | inline in the `<h1>`, **no `aria-label`** |
| 2-4 - one per row | `<span class="text-2xl" role="img" aria-label="poultry leg">EMOJI</span>` |

One emoji for the whole page, reused on every row - `_template-canonical.html`
intentional decision #1 forbids per-restaurant emoji on Top-N. At Top-4 that
means **1 hero + 4 rows = 5 occurrences.**

**`aria-label` for this launch: `oyster`.** The in-tree convention is plain
lowercase Unicode-ish names - `pizza slice`, `hamburger`, `taco`, `coffee`,
`wine glass`, `sparkles`, `shaka`, `tropical drink`, `poultry leg`.

### 8e. `servesCuisine` on the ranking ItemList - list-scoped, proposed not decided

Per #23, ItemList `servesCuisine` is **hand-authored per list** and is not a
copy of `restaurants.json.cuisine`. Rule: **override the generic, preserve the
specific.** Because these are editorial calls, they are flagged here rather
than decided silently.

| # | Restaurant | `restaurants.json.cuisine` | Proposed ItemList `servesCuisine` | Why |
|---|---|---|---|---|
| 1 | Chubby Fish | `Seafood` | `Seafood` | generic, but the list category **is** `Seafood` - override is a no-op |
| 2 | 167 Raw Oyster Bar | `Seafood` (proposed) | `Seafood` | same no-op |
| 3 | The Ordinary | `Seafood` (proposed) | `Seafood` | same no-op |
| 4 | Coda del Pesce | `Italian Seafood` | **`Italian Seafood`** | **specific -> preserve.** Matches what it already carries on `best-italian`, keeping the graph consistent - the Home Team BBQ / `Barbecue` pattern |

**This is the second instance of the no-op case `TRACKED.md:149` flagged**,
filed by the best-italian launch:

> `servesCuisine`'s "override the generic" rule no-ops when the list category is
> itself the generic term. ... Worth a clarifying line in #23 whenever it is
> next amended.

On `best-italian` the collision was `Italian`; here it is `Seafood`, and it hits
**three of four rows** rather than three of six. One instance was a curiosity;
two consecutive launches make it a pattern, and it strengthens the case for the
clarifying amendment. Section 10.

### 8f. Proposed `data/restaurants.json` entries - DRAFT

Field order follows the existing entries exactly. `null` is used per
`_meta.fieldPolicy` - empty string is never a valid placeholder.

**New entry - 167 Raw Oyster Bar:**

```json
{
  "slug": "167-raw-oyster-bar",
  "name": "167 Raw Oyster Bar",
  "tagline": "Raw Bar, New England Roots",
  "cuisine": "Seafood",
  "neighborhood": "Lower King",
  "schemaType": "Restaurant",
  "monthYear": "August 2026",
  "geoLat": null,
  "geoLng": null,
  "imageURL": null,
  "editorialBody": null,
  "areaServed": null,
  "address": {
    "streetAddress": "193 King St",
    "addressLocality": "Charleston",
    "addressRegion": "SC",
    "postalCode": "29401",
    "addressCountry": "US"
  },
  "description": "167 Raw Oyster Bar is a Lower King seafood restaurant in Charleston, SC serving New England style raw bar, lobster rolls and daily catch. Voted by Charleston locals as one of the city's best seafood restaurants.",
  "shareTagline": "New England style raw bar on King Street, voted best by Charleston locals.",
  "keywords": "167 Raw Charleston, Charleston oyster bar, King Street seafood, raw bar Charleston SC, best seafood Charleston SC",
  "appearsOn": [
    {
      "url": "/rankings/best-seafood.html",
      "title": "Best Seafood in Charleston"
    }
  ],
  "phone": "+1-843-579-4997",
  "hours": "Mo-Sa 11:00-23:00",
  "hoursHumanReadable": "Mon-Sat: 11am-11pm\nSun: Closed",
  "priceRange": "$$$",
  "websiteURL": "https://www.167rawoysterbar.com"
}
```

**New entry - The Ordinary:**

```json
{
  "slug": "the-ordinary",
  "name": "The Ordinary",
  "tagline": "Oyster Hall, Old Bank Building",
  "cuisine": "Seafood",
  "neighborhood": "Upper King",
  "schemaType": "Restaurant",
  "monthYear": "August 2026",
  "geoLat": null,
  "geoLng": null,
  "imageURL": null,
  "editorialBody": null,
  "areaServed": null,
  "address": {
    "streetAddress": "544 King St",
    "addressLocality": "Charleston",
    "addressRegion": "SC",
    "postalCode": "29403",
    "addressCountry": "US"
  },
  "description": "The Ordinary is an Upper King seafood restaurant in Charleston, SC serving an oyster hall menu in a restored 1920s bank building. Voted by Charleston locals as one of the city's best seafood restaurants.",
  "shareTagline": "An oyster hall in a restored bank building on Upper King, voted best by Charleston locals.",
  "keywords": "The Ordinary Charleston, Charleston oyster hall, Upper King seafood, King Street oyster bar, best seafood Charleston SC",
  "appearsOn": [
    {
      "url": "/rankings/best-seafood.html",
      "title": "Best Seafood in Charleston"
    }
  ],
  "phone": "+1-843-414-7060",
  "hours": null,
  "hoursHumanReadable": null,
  "priceRange": null,
  "websiteURL": "https://eattheordinary.com"
}
```

`hours` shown as `null` **pending the section 5d resolution** - if the operator
confirms by phone, fill both hours fields and drop the fallback.

**`appearsOn` appends (existing entries, everything else unchanged):**

```json
// chubby-fish -> appearsOn becomes:
[
  { "url": "/rankings/best-nice-restaurants.html", "title": "Best Nice Restaurants in Charleston" },
  { "url": "/rankings/best-seafood.html",          "title": "Best Seafood in Charleston" }
]

// coda-del-pesce -> appearsOn becomes:
[
  { "url": "/rankings/best-italian.html",  "title": "Best Italian in Charleston" },
  { "url": "/rankings/best-seafood.html",  "title": "Best Seafood in Charleston" }
]
```

Neither entry's `tagline`, `cuisine`, `priceRange` or any other field changes -
per section 8b, the differentiated copy lives in the ranking row, not here.

### 8g. Neighborhood determinations - both have direct tree precedent

Both proposed values already exist in the tree, so neither is a new coinage.

**167 Raw Oyster Bar -> `Lower King`.** Precedent: `lowland` (36 George St)
carries `Lower King`. Sourcing: the King Street Historic District, also called
Lower King Street, runs from Calhoun to Broad; 193 King sits inside it. The
building is the c.1840 William Bell Building.

**The Ordinary -> `Upper King`.** Precedent, three entries:
`little-jacks-tavern` (710 King St), `ok-donna` (1117 King St),
`weltons-tiny-bakeshop` (684 King St) all carry `Upper King`. Sourcing: 544 King
is above Calhoun; coverage places The Ordinary in "Charleston's Upper King
Street District".

The tree's pattern is consistent and worth stating, since Tripadvisor files
**both** 167 Raw and The Ordinary under other names: **King Street addresses
take the King-corridor name; addresses off King in the same district take
`Cannonborough-Elliotborough`** (Cannon St, Spring St, Coming St, Bogard St,
St Philip St entries all do). 544 King is a King Street address, so `Upper King`
rather than `Cannonborough-Elliotborough`, even though the
Cannonborough-Elliotborough neighborhood association's boundary encompasses much
of Upper King.

Per #23's neighborhood/keywords divergence rule, the proposed `keywords` in 8f
do **not** simply propagate these strings - they carry "King Street seafood" and
"Upper King seafood" alongside the searched municipal terms, because both
corridor names are things people actually type.

---

## 9. Files this PR would touch

Following #23's step sequence, with its ordering constraints applied.

| # | File | Change |
|---|---|---|
| 1 | `rankings/best-seafood.html` | **NEW.** From `_template-canonical.html`, adopting the production JSON-LD pattern (per-item `url` cross-links + `datePublished`/`dateModified` per #15 Q3), NOT the canonical's bare ItemList. Trim to 4 rows / 4 ItemList positions |
| 2 | `data/og_rankings.json` | Append `{slug: best-seafood, category: Seafood, spots: 4}`; bump `_meta.lastUpdated` |
| 3 | `data/restaurants.json` | 2 new entries; 2 `appearsOn` appends; bump `_meta.lastUpdated` |
| 4 | `restaurants/167-raw-oyster-bar.html` | **NEW** (generated) |
| 5 | `restaurants/the-ordinary.html` | **NEW** (generated) |
| 6 | `restaurants/chubby-fish.html` | Regen + **hand-bump `dateModified`** |
| 7 | `restaurants/coda-del-pesce.html` | Regen + **hand-bump `dateModified`** |
| 8 | `components/header.html` | 2 nav entries (desktop + mobile), below the divider, no NEW pill |
| 9 | all pages carrying inlined chrome | `inline_chrome.py --refresh` output |
| 10 | `index.html` | 15th grid card. **No `grid-cols` change** (section 7b) |
| 11 | `vote.html` | `<option>Best Seafood</option>` at end |
| 12 | `assets/images/og/best-seafood.png` | **NEW** (generated) |
| 13 | `assets/images/og/167-raw-oyster-bar.png` | **NEW** (generated) |
| 14 | `assets/images/og/the-ordinary.png` | **NEW** (generated) |
| 15 | `sitemap.xml` | Regenerated - **after** the bumps |
| 16 | `_strategy/TRACKED.md` | Section 10 items - same-PR file edit per #22 |
| 17 | `rankings/_best-seafood-launch-analysis.md` | This file |

Confirm the OG output path at build time - listed above from convention, not
verified against `generate_og_images.py` in this pass.

### 9a. Ordering constraints that will bite this launch specifically

1. **`generate_sitemap.py` must run AFTER both `dateModified` bumps.** It reads
   `dateModified` to build `<lastmod>`; run it first and the sitemap ships stale
   dates silently. This launch has **two** bumps plus two new pages, so the
   window for getting it wrong is wider than usual.
2. **The ItemList JSON-LD block must precede BreadcrumbList** on the new ranking
   page. `generate_sitemap.py` parses only the *first* `ld+json` block; put
   BreadcrumbList first and `<lastmod>` vanishes with no error and no warning.
3. **All three new pages must exist before `inline_chrome.py --refresh`**, or
   they ship with stale chrome and `--check` exits 2.
4. **Hand-normalize the two new pages' seeded dates from UTC to Eastern**
   (`T12:00:00-04:00`). The generator seeds `+00:00`; three pages in the tree
   already carry the un-normalized form.
5. **Use `generate_detail_page.py {slug}`, never `--all`** - `--all` rewrites
   every page and destroys the diff.
6. **`npm run build:css` only if new utility classes appear.** Copying an
   existing ranking page should introduce none; verify with a class-set diff.
   **PR #55 has since merged** (`main` @ `0822622`), so rebase first and expect
   `built.css` to already be current - section 1c.
7. **Playwright's Chromium must be installed** before `generate_og_images.py`
   will run: `python -m playwright install chromium` (~87 MB).

### 9b. Traps that are not bugs

- `{{Emoji}}` in `og-templates/ranking.html` is declared but never substituted -
  it sits inside an HTML comment, deliberate per decision #6. Leave it.
- `{{Emoji}}`, `{{Restaurant#}}`, `{{Tagline#}}` surviving in the shipped
  ranking page are inside the REPEATING ROW documentation comment. Every
  production Top-N page carries them. A placeholder sweep must exclude HTML
  comments.
- `inline_chrome.py` writing LF against a CRLF working copy - cosmetic.
- **Verification must be Netlify-tolerant**: single OR double quotes, any
  attribute order, optional `.html`. Scope assertions to page-owned content by
  stripping `<!-- AUTOGENERATED ... -->` blocks first, or the shared nav chrome
  will fire them. When a live check fails, confirm whether the page or the
  pattern is wrong before reporting a defect.

### 9c. PR shape and merge

Single PR. Social assets are a **separate follow-up PR** per #23 step 12.

Squash subject must be set explicitly - GitHub defaults it to the PR title,
which lands on `main` without a conventional prefix:

```
gh pr merge {N} --squash --subject "feat: add best-seafood Top-4 with Chubby Fish, 167 Raw Oyster Bar, The Ordinary, Coda del Pesce (#{N})" --body-file {commit-body} --delete-branch
```

`feat` is correct for a ranking launch and has precedent in this repo.

---

## 10. TRACKED entries this launch would generate

Same-PR file edits per #22 - prose in the PR description does not count as
filing.

**No roster exclusions.** All four candidates cleared both gates. This is the
second fully clean sheet in a row after best-italian.

1. **Scope note: the setting-driven seafood tier was excluded by operator
   decision.** Section 0a. Bowen's Island, The Wreck, Crosby's, Hyman's and the
   Shem Creek cluster were never sourced - the list is about cooking, not
   setting or institution. **No-trigger record**; purpose is to stop
   re-proposal.

2. **Fourth consecutive zero-bench launch.** best-ice-cream, best-ramen,
   best-italian and now best-seafood have all supplied exactly N candidates
   against #23's "never zero bench" rule, and all have held. The run is now long
   enough that the rule is being routinely overridden by operator practice.
   Either the rule should be amended to distinguish operator rosters at N>=3
   (where a failure is editorial) from N=1 (where it is structural), or the
   bench should start being supplied. **No trigger; flag at the next #23
   amendment.**

3. **167 Sushi Bar is relocating; 289 East Bay St becomes an undetermined new
   concept.** Section 6b. No impact on this entry - separate concept - but the
   supplied fact "167 Sushi Bar now occupies 289 East Bay St" has a shelf life,
   and sources split on the timing ("later this year" 2026 vs a 2027 headline).
   **Trigger: recheck in 2027**, to confirm the move completed and to identify
   what opened at 289 East Bay St.

4. **The Nantucket business is the brand's origin, not a location.** Section 6c.
   167 Raw Fish Market, 167 Hummock Pond Road, Nantucket MA - a retail fish
   market under a different name, far outside #14.1 scope, and the source of the
   "167" in the brand name. **No-trigger record**; purpose is to stop a future
   session re-deriving it or proposing it as a `locations[]` secondary.

5. **Chubby Fish had never had the #23 rule 6 second-location check run.** The
   entry shipped 2026-05-03; the standing check was added 2026-08-26. Run in
   this pass: clean, ships single-location. Owner James London's other
   restaurant, **Seahorse**, is a separate concept. **Worth asking whether other
   pre-rule-6 entries should get a sweep** - most of the tree predates
   2026-08-26. No trigger on this entry.

6. **`servesCuisine`'s generic-override no-op has now happened twice.**
   Section 8e. `TRACKED.md:149` filed it from `best-italian` (`Italian`); it
   recurs here (`Seafood`) across three of four rows. **Fold into the existing
   item** and note the second instance strengthens the case for the #23
   clarifying line.

7. **`priceRange` trigger fired and was deliberately deferred.** Section 8c.
   Editing `coda-del-pesce` fires `TRACKED.md:141`'s "next edit to these
   entries" trigger. The six-entry re-derivation was **not** attempted here -
   wrong PR, and doing it one entry at a time is what the item warns against.
   **Extend the existing item** to record that `best-seafood` now carries the
   same split (`chubby-fish` `$$$`, `the-ordinary` proposed `null`,
   `167-raw-oyster-bar` proposed `$$$` over a dual-tag dissent) and that the
   trigger has now fired once without being serviced.

8. **The Ordinary's `hours` are unresolved across three sources.** Section 5d.
   Dark day resolves 2-to-1 to Tuesday; open time (4pm vs 5pm) is confounded by
   an August-only promotion; close time (9/10pm vs 10:30pm) is a genuine
   deadlock with no own-site value at all. **Trigger: resolve by phone
   (843.414.7060) before ship**, or ship `null` + the #13.10 fallback and
   recheck after August, when the seasonal promotion ends and the 4pm/5pm
   question may resolve itself.

9. **Coda del Pesce's stored `hours` are 30 minutes short on Fri-Sat.**
   Section 5d. Stored `Tu-Sa 17:30-21:00`; sources give Fri-Sat to 21:30. This
   launch stamps a fresh `dateModified` over it either way. **Trigger:
   this PR** - fix it in-PR or record the acceptance explicitly.

10. **The tree has three same-owner restaurant pairs and no field expresses
    the relationship.** Lata (FIG + The Ordinary), London (Chubby Fish +
    Seahorse), Vedrinski (Coda del Pesce + Volpe). All are separate brands at
    separate addresses, correctly *not* `locations[]` secondaries under
    DECISIONS #17. Observation only - #17 covers location sets, not ownership
    graphs, and nothing in the current surfaces needs it. **No trigger.**

11. **`167-raw-oyster-bar` would be the tree's first digit-leading slug.**
    Section 3a. All three consumers verified digit-safe
    (`generate_detail_page.py:85` uses `[^a-z0-9]+`; `social/src/data.ts:125`
    uses `[^/]+`; `generate_sitemap.py:54` uses `glob`). Only visible effect is
    sitemap ordering - digits sort before letters. **No-trigger record**, so a
    future session does not treat the sort position as a defect.

12. **Tripadvisor files 167 Raw Oyster Bar under "Ansonborough"** - the
    vacated-in-2020 East Bay address. Section 5e. Wrong for 193 King St.
    **No-trigger record**, to stop a future neighborhood cross-check adopting it.

13. **The Ordinary's bank provenance is more specific than common coverage
    says.** Section 8b. The 1927 date is the lot sale; the building opened 1928;
    the original occupant was Peoples-First National Bank, with Bank of America a
    later occupant. The shipped tagline says "Old Bank Building" and is true
    under every source. **No-trigger record**, so a future copy edit does not
    "sharpen" it into a wrong specific.

---

## 11. Where this prompt and the recipe/tree disagree

Reported per the prompt's instruction. Ordered by consequence.

1. **`main` is at `d111f60`, not `1a6a429`.** Section 1a. Stale by two commits
   (#53, #54). The "clean and synced" half of the claim was correct.

2. **The session did not start on `main`, so the prompt's bare `checkout -b`
   would have based this launch on an unmerged PR.** Section 1b. HEAD was
   `fix/regenerate-built-css` @ `7cb4f89`, the head of **open PR #55**. Branched
   from `main` explicitly instead. This is the one disagreement that would have
   caused real damage if followed literally.

3. **The tree DOES have leading-"The" precedent, in both fields.** Section 3b.
   The prompt anticipated none and asked me to "propose and flag rather than
   deciding silently". `the-wedge` / `The Wedge` and `the-harbinger-cafe-bakery`
   / `The Harbinger Cafe & Bakery` both carry the article in `name` **and**
   `slug`. So `The Ordinary` / `the-ordinary` is precedent application, not a
   flagged proposal.

4. **`best-italian` has six entries, not five.** Section 8c. Cane Pazzo landed
   at position 4 in PR #52, taking the list Top-5 -> Top-6. The prompt's
   substantive claim - that they all ship `null` - is correct; only the count is
   stale.

5. **"Report what the two existing entries carry and propose consistently" has
   no consistent target.** Section 8c. `chubby-fish` carries `$$$` and
   `coda-del-pesce` carries `null`. They already disagree, and null is not the
   tree norm (34 of 47 entries carry a value). Proposed per-entry on evidence
   instead, with the divergence recorded.

6. **The emoji rule as stated - "food as served, never the animal" - is
   contradicted by a shipped page.** Section 8d. `best-wings` carries U+1F357
   POULTRY LEG, which is an animal part. The operative rule is "never a *live*
   animal; a served preparation is admissible". The prompt's *conclusions* all
   survive (fish/crab/lobster out, fried shrimp wrong register) - and the
   corrected rule is what makes U+1F9AA OYSTER defensible rather than a
   borderline call.

7. **"Whole local fish" for Coda del Pesce could not be grounded.** Section 8b.
   Crudo is multiply sourced and daily; whole-fish preparations did not surface.
   Recorded as a scoped negative per #23 rather than as a fact about the menu.
   Not used in the proposed tagline.

8. **Minor citation drift: "#23 rule 4 (the PR #34/#36 trap)".** Section 2c.
   Rule 4 governs re-running the *gates* on pre-existing entries; the
   append+bump requirement lives in section 0a's table and steps 4-5. **PR #36
   is not referenced anywhere** in `DECISIONS.md` or `TRACKED.md` in connection
   with this trap; #34 is.

9. **The prompt says "both breakpoints"; the grid has three.** Section 7b.
   `grid-cols-1` / `md:grid-cols-2` / `lg:grid-cols-4`. Re-derived at all three.
   Base is unaffected, so the substance of the instruction was right.

10. **167 Sushi Bar's location is a moving target.** Section 6b. "167 Sushi Bar
    now occupies 289 East Bay St" is true today but the concept is relocating,
    with sources split on 2026 vs 2027. No effect on this launch.

**Where the prompt was right and worth saying so:** the "167 Raw Oyster Bar"
name; both second-location determinations (separate concepts, not
`locations[]`); the Bar167 Aug-2022 opening; the Nantucket relationship
existing at all; the Jason Stanhope correction (he was FIG's chef, not The
Ordinary's - nothing in this file carries him); the no-Twemoji claim; and the
"three of four are oyster-forward" claim, all four of which were verified rather
than assumed.

---

## 12. Open questions requiring an operator decision before a build pass

1. **The Ordinary's `hours`** (section 5d) - phone-confirm, or ship `null` +
   #13.10 fallback? **This is the only genuine blocker in the launch.**
2. **Coda del Pesce's Fri-Sat close** (section 5d) - fix the 30-minute drift
   in-PR, or accept and record?
3. **`167-raw-oyster-bar` `priceRange`** (section 8c) - `$$$` on the listing
   majority, or `null` given Charleston Magazine's dual `$$$`/`$$$$` tag?
4. **Coda del Pesce's best-seafood tagline** (section 8b) -
   `Daily Crudo, Sustainably Caught` (recommended, no echo) or
   `Daily Crudo, Local Catch` (repeats "Catch" and "Daily" against row 1)?
5. **Hero emoji** (section 8d) - confirm U+1F9AA OYSTER against the corrected
   rule.
6. **`servesCuisine` values** (section 8e) - editorial calls, flagged per #23.

> **All six are answered in section 15**, except #1 (The Ordinary's hours),
> which is held pending the call scripted in section 14.

---

## 13. The CI gate - scoped before it can surprise the launch PR

Read on `main` @ `47328e9`, where PR #56 landed it. **Nothing was modified.**
The files are now tracked on `main` rather than sitting untracked on a feature
branch, so the prep instruction's "do not modify that branch or its files" is
moot - the branch is gone and the files are ordinary tracked sources.

### 13a. What it actually asserts on

`.github/workflows/generated-artifacts.yml` runs **two** checks, and only two:

| Step | Command | Asserts |
|---|---|---|
| `built.css matches src/input.css` | `npm run check:css` -> `python scripts/check_built_css.py` | `assets/css/built.css` is byte-identical to a fresh `tailwindcss --minify` build |
| `Inlined chrome matches components/` | `python scripts/inline_chrome.py --check` | every production page's marker-wrapped header/footer matches `components/*.html` |

**It does NOT assert on:**

- **generated detail pages** (`restaurants/*.html`) - no check of any kind
- **OG images** (`assets/images/og/*.png`) - no check (CI installs no Playwright
  or Chromium, so it could not run `generate_og_images.py` even if asked)
- **`sitemap.xml`** - no check
- `data/restaurants.json` / `data/og_rankings.json` - no schema or consistency check

So it does **not** generalize to every generated artifact despite the workflow's
name. It covers exactly the two artifacts that have shipped stale before -
`built.css` (the four-month two-column homepage bug, PR #55) and inlined chrome.

**Answering the prep question directly: the launch PR would NOT fail on
regenerated detail pages or on OG PNGs.** Neither is gated. The two ordering
constraints most likely to bite this launch - "run `generate_sitemap.py` AFTER
the `dateModified` bumps" and "ItemList JSON-LD must precede BreadcrumbList" -
are **still discipline-only and still silent on failure.** The gate does not
help with either.

### 13b. When it runs

```yaml
on:
  pull_request:
    branches: [main]
```

**Pull requests targeting `main` only.** It does not run on push to `main`, and
there is no `workflow_dispatch`. So the launch PR **will** be gated before
merge, and a green `main` is not evidence the gate passed on anything merged
before #56.

Environment: `actions/checkout@v4`, Node **22** (pinned to match the developer
environment that produced the committed `built.css`), Python **3.11**, `npm ci`.
Both check scripts are stdlib-only, so `requirements.txt` is not installed - and
therefore **Playwright is not available in CI**, confirming OG images cannot be
gated there without a workflow change.

The second step carries `if: always()`, so a PR that drifts both ways reports
both failures in one run instead of one-then-the-other.

### 13c. What the launch PR has to satisfy

**Baseline measured on `47328e9` before any launch work - both gates green:**

```
python scripts/inline_chrome.py --check   -> [OK] 69 files in sync            (exit 0)
python scripts/check_built_css.py         -> [OK] assets/css/built.css in sync
                                             with src/input.css (20444 bytes) (exit 0)
```

**1. The chrome gate is the one that will bite.** `inline_chrome.py`
`SCAN_DIRS = ["", "rankings", "restaurants"]`, globbing `*.html` in each. The
69 files break down as **6 root + 16 rankings + 47 restaurants**.

This launch adds **three** files inside that scope -
`rankings/best-seafood.html`, `restaurants/167-raw-oyster-bar.html`,
`restaurants/the-ordinary.html` - taking the count to **72**. And because the
launch edits `components/header.html` (two nav entries), **every one of the 72
pages diverges until `inline_chrome.py --refresh` runs.**

Two distinct failure modes, with different exit codes:

| Mistake | `--check` result |
|---|---|
| Edit `components/header.html`, forget `--refresh` | **exit 1** - divergence in up to 144 regions (72 files x header+footer) |
| Ship a new page without marker-wrapped chrome | **exit 2** - "region(s) missing markers" |

This makes #23's ordering constraint - *"New ranking and detail pages must exist
before `inline_chrome.py --refresh`"* - a **hard, enforced requirement** rather
than a discipline note. That is a genuine improvement for this launch, which has
both a `components/` edit and three new pages.

**Gotcha worth recording: the two working templates in `rankings/` are inside
the gate.** `discover_files()` does not skip underscore-prefixed files, so
`rankings/_detail-page-template.html` and `rankings/_template-canonical.html`
both carry chrome markers and are both checked. This **diverges from
`generate_sitemap.py`, which explicitly excludes underscore-prefixed working
files.** Two generators, two conventions, same directory. Consequence for this
launch: copying `_template-canonical.html` to create the new ranking page is
fine, but **do not "tidy" chrome out of the templates** - it would turn the gate
red.

(This file, `_best-seafood-launch-analysis.md`, is `.md` and is globbed by
neither.)

**2. The `built.css` gate is a real risk, and #23's advice is now insufficient.**
`tailwind.config.js` content globs are:

```js
content: ["./*.html", "./rankings/*.html", "./restaurants/*.html", "./components/*.html"]
```

**All three new pages are scanned by Tailwind.** `check_built_css.py`
regenerates to a temp path and compares **byte-for-byte** - it never writes the
tracked file, so it is safe to run locally at any time.

#23 says *"`npm run build:css` only if new utility classes appear... verify with
a class-set diff rather than running it reflexively."* That is still the right
diagnosis, but the consequence has changed: **a missed new class is now a red
check, not a silent stale stylesheet.** If any of the three new pages introduces
even one utility class not already emitted, the fresh build differs and the PR
fails until `npm run build:css` is run and `built.css` committed.

Expected outcome: the new ranking page is a copy of an existing one and the two
detail pages come from the same generator and template as the existing 47, so
the class set should be a **subset** of what is already emitted, and `built.css`
should not need rebuilding. **Verify by running `python scripts/check_built_css.py`
locally after the three pages exist** - it is the same assertion CI makes, so a
local green is a reliable predictor. Do not assume.

**3. Run both gates locally before opening the PR.** Both are read-only, both
are fast, and both are the exact commands CI runs.

---

## 14. The Ordinary's hours - call script for 843.414.7060

Held per the prep instruction. **No hours value is proposed or shipped.** The
conflict is restated from section 5d:

| Source | Dark day | Opens | Closes |
|---|---|---|---|
| Own site (`eattheordinary.com`, two pages) | Tuesday | **4:00pm** | not stated anywhere |
| Yelp-derived aggregate | Tuesday | 5:00pm | 9pm Mon-Thu, 10pm Fri-Sat |
| OpenTable | **Monday** | 5:00pm | 10:30pm nightly |

Three questions, in the order that makes them easiest to answer. Each is phrased
so a host can answer it without interpreting our problem.

### Q1 - service start, separated from the August promotion

> *"What time do your doors open for dinner on a normal night - say a Thursday in
> October? And the 4pm opening on your site for the oyster-slider special, is
> that an August-only thing or is 4pm when you open year-round?"*

The second half is the part that matters. The own site advertises *"Join us from
4-5pm for half-priced oyster sliders for the month of August"*, which is a
plausible explanation for the entire 4pm-vs-5pm split.

| Answer | Implication |
|---|---|
| 4pm year-round | Own site is right; the two third-party 5pm readings are describing *dinner service*, not door-open. Ship open **16:00** - schema.org `openingHours` means open to the public, not kitchen-service start |
| 4pm is August-only, normally 5pm | Third-party majority is right and the own site is *seasonally* right. Ship **17:00** and file a re-verification trigger for next August |
| 4pm bar, 5pm dining room, year-round | Both true, different rooms. Ship **16:00** per the schema.org reading, and record the distinction so a future session does not "correct" it to 17:00 |

### Q2 - kitchen close versus bar close

> *"When does the kitchen stop taking orders, and what time does the bar actually
> close? Are those different - and do they change on Friday and Saturday?"*

This is the most likely explanation for the 9/10 vs 10:30 split, and it is the
half that is a **genuine deadlock** on public sources - two claims, no majority,
and no own-site value at all.

| Answer | Implication |
|---|---|
| Kitchen 9pm Mon-Thu / 10pm Fri-Sat, bar 10:30pm nightly | **Both sources are correct and measuring different things.** Deadlock dissolves. Ship the bar close (**22:30**) per schema.org, and record why the kitchen times were not used |
| One close time, varies Fri-Sat | Split-range format, exactly like sibling `fig` (section 15a) |
| One close time, same every night | Simple single range; whichever source disagrees is stale |

### Q3 - the dark day

> *"Which day are you closed? I've seen both Monday and Tuesday listed and I want
> to get it right."*

| Answer | Implication |
|---|---|
| **Tuesday** | Confirms the 2-to-1 majority (own site + Yelp). OpenTable is stale. Expected outcome |
| Monday | Own site **and** Yelp are both wrong - surprising enough that everything else taken from those two sources for this entry should be re-checked, not just hours |
| Neither / open seven days | New information; re-derive the whole field |

### Worth asking while on the phone, since it is free

> *"Does the schedule change seasonally - different hours in winter or high
> season?"*

If yes, a single stored `hours` value is a standing maintenance liability rather
than a one-time fix, and the honest options are a re-verification trigger each
season or `null` + the #13.10 fallback. Recording the answer either way is
cheaper than rediscovering it.

### If the call does not happen

Fall back to **`hours: null` + `hoursHumanReadable: null`**, letting the detail
page render the honest "Hours vary - see [website]" copy per DECISIONS #13 /
template intentional decision #10, the `tonis-detroit-style-pizza` precedent.
**Do not synthesize a range from the three claims** - a value assembled from
sources that contradict each other is the fabrication `_meta.fieldPolicy`
forbids, and it would ship under a fresh `dateModified` asserting it was
verified.

---

## 15. Operator resolutions - prep pass, 2026-08-27

These are decisions, not proposals. Where they supersede a drafted section, the
draft above is left intact as the record of the reasoning.

### 15a. Coda del Pesce hours - FIX IN THIS PR

**Decision: correct the Fri-Sat shortfall in the launch PR.** Rationale
accepted: the launch stamps a fresh `dateModified` over this entry either way,
and asserting freshness over a field known to be wrong is the Bar Weems failure
that split best-ramen into two PRs.

**Current values, read from `data/restaurants.json` before anything was
changed:**

```json
"hours": "Tu-Sa 17:30-21:00",
"hoursHumanReadable": "Tue–Sat: 5:30pm–9pm\nSun–Mon: Closed"
```

**Sourced schedule:** Tue-Thu 5:30pm-9:00pm; **Fri-Sat 5:30pm-9:30pm**; closed
Sun/Mon. The stored single range is correct Tue-Thu and **30 minutes short on
Fri and Sat.**

**Sourcing, re-confirmed during the prep pass rather than carried from the
analysis pass** - a single aggregated reading is too thin a basis for a
correction:

- **The own site does not establish a close time at all.** `codadelpesce.com`
  reads, verbatim: *"Tuesday - Saturday 5:30 PM - close"*. No closing time for
  any day. Under #23 the own site could not decide this field anyway, but it is
  worth recording that it does not even contradict the correction.
- **Dated third-party listings decide it, and they converge**: multiple
  independent listings give **Fri 5:30-9:30pm and Sat 5:30-9:30pm**, with
  Tue-Thu at 5:30-9:00pm. Yelp's listing carries an "Updated July 2026" stamp.
- **No dissenting source** proposes a 9:00pm Fri-Sat close. This is convergence,
  not a 2-to-1 majority - materially stronger than The Ordinary's situation in
  section 14.

Note the correction **only extends Fri-Sat**; the Tue-Thu 21:00 close that
shipped with the best-italian launch is confirmed correct and is unchanged.

**Corrected values to apply during the build pass:**

```json
"hours": "Tu-Th 17:30-21:00,Fr-Sa 17:30-21:30",
"hoursHumanReadable": "Tue–Thu: 5:30pm–9pm\nFri–Sat: 5:30pm–9:30pm\nSun–Mon: Closed"
```

(The day/time separators above are literal **U+2013 EN DASH**, quoted exactly as
`data/restaurants.json` stores them - these two lines are the only non-ASCII
content in this file, and deliberately so. Match the existing entries; do not
substitute ASCII hyphens. Note the `hours` field on the line above uses ASCII
hyphens - the two fields genuinely differ, and that is not a typo.)

**Format verified against the tree, not invented.** Multi-range `hours` is
well-established - **20 of 47 entries** use it. The closest precedents are an
exact structural match:

| Entry | `hours` |
|---|---|
| `fig` | `Tu-Th 17:30-22:30,Fr-Sa 17:30-23:00` |
| `le-farfalle` | `Su-We 17:00-21:30,Th-Sa 17:00-22:00` |
| `wild-olive` | `Mo-Th 17:00-22:00,Fr-Sa 16:00-23:00,Su 16:00-22:00` |

`fig` is the same shape, same 17:30 start, same Fri-Sa split - and is the
sibling concept of The Ordinary. Note the tree is **inconsistent on the
separator**: some entries use `, ` (comma-space), others `,` (no space). The
best-italian cluster (`le-farfalle`, `wild-olive`) and `fig` all use **no
space**, so the corrected value follows that.

**Nothing has been changed yet** - this is the prep pass. Apply during the
build.

### 15b. Coda del Pesce best-seafood tagline - `Daily Crudo, Sustainably Caught`

**Accepted** over `Daily Crudo, Local Catch`, on the repetition reasoning in
section 8b: the alternative would put **"Catch"** in two of four rows against
Chubby Fish's `No Reservations, Daily Catch`, and **"Daily"** in two of four.
Both are equally sourced; the accepted one carries no echo.

Side by side, final:

| Page | Tagline |
|---|---|
| `best-italian` (shipped, unchanged) | `Oceanfront Italian, Seafood Led` |
| `best-seafood` (this launch) | `Daily Crudo, Sustainably Caught` |

`restaurants.json.tagline` stays `Oceanfront Italian, Seafood Led` - per section
8b, ranking-row taglines are per-page and the stored field feeds the detail page
and OG image, not the row.

### 15c. `priceRange` - do not unify

**Decision: ship what is sourceable, null what is not. No unification pass.**

| Entry | Value | Basis |
|---|---|---|
| `chubby-fish` | **`$$$`** - unchanged | shipped value, out of scope |
| `coda-del-pesce` | **`null`** - unchanged | under the deferred TRACKED sweep |
| `167-raw-oyster-bar` | **`$$$`** | sourceable: Tripadvisor and restaurantguru both read `$$$`; per-person reports of $40-70 sit in that band. Charleston Magazine dual-tags `$$$`/`$$$$`, which is a dual-tag rather than a contradiction |
| `the-ordinary` | **`null`** | not sourceable: Facebook `$$$` vs review consensus `$$$$` vs a "$100-per-person" prose figure. No majority. The Cane Pazzo case exactly |

The resulting page carries two values and two nulls. That is **intentional and
invisible** - `priceRange` renders in detail-page JSON-LD only and is omitted
entirely when null; it does not appear on ranking pages at all (verified,
section 8c).

**The TRACKED six-entry sweep stays deferred to its own PR.** The trigger fired
(editing Coda del Pesce), and the launch PR will say so rather than servicing it
badly - `TRACKED.md:141` asks for a re-derivation "from one source", which is
not something to do one entry at a time inside a launch.

### 15d. The emoji rule - the correct formulation, and where the wrong one lives

**Recorded as a correction for the next docs PR.** The rule is:

> **Never a LIVE animal.** A served preparation is admissible, **including an
> animal presented as food.**

Not "never an animal". The tree's own `best-wings` page ships **U+1F357 POULTRY
LEG**, which is an animal part - admissible because it depicts that part cooked
and plated.

**Where the wrong formulation appears - two places, both in the same file:**

| Location | Text |
|---|---|
| `rankings/_best-wings-launch-analysis.md:229` | *"the site's emoji all depict the food as served, not the animal"* |
| `rankings/_best-wings-launch-analysis.md:822` | *"Every page emoji on the site depicts food as served, never the animal"* |

Both were written to justify choosing U+1F357 POULTRY LEG over U+1F414 CHICKEN.
**The outcome was right and the rule as stated was too broad** - the distinction
that actually did the work is live-animal vs served-preparation, not
animal vs not-animal. The file that states the rule most explicitly is the file
for the launch that contradicts its literal reading.

**The rule is in neither `DECISIONS.md` nor `TRACKED.md`** - `grep -c -i "as
served"` returns **0** for both. DECISIONS #6 covers only the
`best-nice-restaurants` wine glass and states no general rule. So this is an
undocumented convention that governs every launch, living only in one working
analysis file, and stated wrongly there twice.

**Recommendation for the docs PR: promote the corrected rule into
`DECISIONS.md`** rather than only fixing the two lines. Fixing them in place
leaves the convention undiscoverable in the strategy docs, which is how it came
to be restated incorrectly in the first place. Amending #6 - or a new entry
alongside it - is the durable fix.

### 15e. Hero emoji - U+1F9AA OYSTER confirmed

**Confirmed on the section 8d reasoning**, i.e. on the corrected 15d rule: an
oyster on the half shell is a plated dish, in the same position as POULTRY LEG.

Build detail per section 8d: **five occurrences** - one in the hero `<h1>` with
no `aria-label`, plus one per row (four rows), each as
`<span class="text-2xl" role="img" aria-label="oyster">`. Label follows the
in-tree plain-lowercase convention.

No Twemoji fetch, no social-card impact, no new `.emoji-cache` entry - Top-N
social cards render rank badges (section 7d).

### 15f. Still open

**Only The Ordinary's `hours`** - held pending the call scripted in section 14.
Everything else in section 12 is now resolved.
