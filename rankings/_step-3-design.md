# Step 3 design analysis — `best-pizza` schema cross-linking

Working file. Lives at `rankings/_step-3-design.md` per the working-files convention. Author: Claude session of 2026-05-03 picking up step 3 from `_strategy/CONTEXT.md` bootstrap.

## Premise

Step 3 wires the ranking page's JSON-LD `ItemList` to the 5 detail pages shipped in step 2 pilot. The literal mechanic from PLAN.md is one `"url"` field per item. The bootstrap surfaces 4 design questions; reading the live `best-pizza.html` against the 5 detail pages surfaces a 5th. Each question below gets options + a recommendation + tradeoffs. Nothing executes until you approve them per question.

If all 5 recommendations are approved as written: ~10-line diff inside `<script type="application/ld+json">` + 5 `<a>` wrappers in the body of `rankings/best-pizza.html`. One PR, individually revertable.

---

## Q1 — JSON-LD `url` field only, or also visible HTML cross-links?

Currently the 5 restaurant rows render as `<h2>` + tagline plain text — no anchor. The "Appears on" block on each detail page already links *back* to `/rankings/best-pizza.html`, so detail → ranking is already a clickable path. Step 3 is the inverse direction.

**A. JSON-LD `url` only.** Add `"url": "..."` to each item. No HTML changes. Crawlers follow the link; users can't.

**B. JSON-LD `url` + clickable `<h2>`.** Wrap each restaurant `<h2>` in an `<a href="/restaurants/{slug}.html">` with a brand-orange hover (matching the existing "Appears on" link styling on detail pages). Users + crawlers both benefit. Symmetrically completes the navigation loop.

**C. JSON-LD `url` + separate "View details →" link** under each tagline. Adds visible affordance without changing the typography of the name. Slight visual weight bump per row.

**Recommendation: B.** The ranking → detail navigation is the user-visible payoff of step 2. Gating it behind structured-data-only links leaves most of the value off the user-facing surface. Visual change is color/hover only — no layout shift, no per-row reflow. Bootstrap's framing of step 3 as "mechanical, fast, schema-only" is technically violated by B, so flagging explicitly. Strict-bootstrap-literal: A.

---

## Q2 — Per-item `@type` upgrade?

The bootstrap mentions `Restaurant` → `LocalBusiness` as a possible upgrade. Reading the data, the actually-interesting case for best-pizza is different: detail pages use mixed `@type` per DECISION #14.3. Dough Boyz is `FoodEstablishment` because it's a mobile vendor. The current ranking-page ItemList still calls Dough Boyz `Restaurant` — a *subclass* of FoodEstablishment — which overspecifies (implies fixed location it doesn't have). Same logical issue DECISION #14.3 was solving on the detail-page side.

**A. Keep all items as `Restaurant`.** Status quo. Semantic mismatch on Dough Boyz; Google's validator won't complain.

**B. Mirror the detail-page `@type` per item.** Tutti / D'Allesandro's / Toni's / Park Pizza stay `Restaurant`; Dough Boyz becomes `FoodEstablishment`. 1-line change. Sets the precedent for bulk port (where the same reasoning applies on coffee pages with `CafeOrCoffeeShop`, future bar pages with `BarOrPub`, etc.).

**C. Upgrade all items to `LocalBusiness`.** Sideways move — `LocalBusiness` is a *parent* of `Restaurant`, so this makes the data *less* specific. Don't recommend.

**Recommendation: B.** Same reasoning as DECISION #14.3 applied consistently. Cost is 1 line. Important precedent for the bulk port.

---

## Q3 — BreadcrumbList schema?

**A. None added.** Defer all breadcrumbs.

**B. Ranking page only.** `Home → Best Pizza`. 2-node breadcrumb, mechanical add to the ranking page's `<head>`. Real-but-small SEO value (Google sometimes renders breadcrumbs in SERPs).

**C. Detail pages too.** `Home → Best Pizza → {Restaurant}`. Higher SEO value (deeper hierarchy = higher SERP-render likelihood). Requires touching the detail-page template — explicitly out of step 3 scope per bootstrap.

**D. Both B and C.**

**Recommendation: A — defer.** The 2-node case alone is low-value. The high-value case (C) requires detail-page template work which is out of bootstrap scope. Cleaner to defer the entire breadcrumb workstream until bulk port lands and detail-page coverage is global, then add B+C in one pass. New tracked workstream entry would land in `_strategy/TRACKED.md` if approved.

---

## Q4 — Cross-link verification mechanism

The 5 url fields point at file paths trivially derivable from the URLs (`https://votedonbylocals.com/restaurants/{slug}.html` → `restaurants/{slug}.html`). Verification confirms: (a) JSON parses; (b) each url is well-formed; (c) the implied local file exists; (d) the slug in the url has a corresponding entry in `data/restaurants.json`.

**Recommended recipe** (run from repo root):

```bash
python -c "
import re, json, pathlib
html = pathlib.Path('rankings/best-pizza.html').read_text()
m = re.search(r'<script type=\"application/ld\+json\">\s*(\{.*?\})\s*</script>', html, re.DOTALL)
data = json.loads(m.group(1))
roster = json.loads(pathlib.Path('data/restaurants.json').read_text())['restaurants']
roster_slugs = {r['slug'] for r in roster}
for item in data['itemListElement']:
    url = item['item'].get('url', '')
    slug = url.rsplit('/', 1)[-1].replace('.html', '') if url else ''
    file_exists = pathlib.Path(f'restaurants/{slug}.html').exists() if slug else False
    in_json = slug in roster_slugs
    print(f'{slug:35s} url={bool(url):d} file={file_exists:d} json={in_json:d}')
"
```

Pass criteria: all 5 lines print `url=1 file=1 json=1`.

If Q1=B (visible HTML links added), supplement with one manual click of each link in the local Netlify dev preview.

**Recommendation: the script above as primary; manual click as supplement only if Q1=B.**

---

## Q5 — addressLocality divergence between ranking and detail pages

*(Newly visible at step 3; not in the bootstrap's Q1–Q4 list.)*

The current `ItemList` on `best-pizza.html` sets `addressLocality: "Charleston"` for all 5 restaurants. The detail pages ship the literal municipality per DECISION #14.2: Toni's = `"Mount Pleasant"`, Park Pizza Co = `"North Charleston"`. Once step 3 wires url cross-links between the two documents, the same restaurant carries two different `addressLocality` values across the structured-data graph on the same site. A search-engine entity resolver could legitimately flag this as inconsistent metadata.

**A. Keep separated.** Ranking JSON-LD stays editorial-frame ("Charleston" for all 5). Detail JSON-LD stays literal. Treat as different scopes (ItemList describes the ranking editorially; detail describes the entity precisely). Cross-document inconsistency accepted.

**B. Reconcile on the ranking page in this same PR.** Update items 4 (Toni's = "Mount Pleasant") and 5 (Park Pizza Co = "North Charleston"). 2-line change. Honors DECISION #14.2 uniformly.

**C. Defer as a new tracked workstream.** Don't touch in step 3.

**Recommendation: B.** The change is trivial (2 locality strings) and the same JSON-LD block is being touched anyway for the `url` field. The alternative (A or C) leaves a contradiction the bulk port will inherit — every future ranking page with a non-Charleston-municipality entry repeats the divergence. Fixing the pattern at best-pizza now sets the right convention for the bulk port: as detail pages ship per ranking, the ranking-page locality reconciles in the same PR. Caveat: technically broadens step 3's scope beyond strict cross-linking. Flagging explicitly.

---

## Summary table

| Q | Topic | Recommendation | Net change to `best-pizza.html` |
|---|---|---|---|
| Q1 | Visible HTML cross-links | B (clickable `<h2>`) | 5 `<a>` wrappers in body |
| Q2 | Per-item `@type` | B (mirror detail page) | 1 line in JSON-LD (Dough Boyz) |
| Q3 | BreadcrumbList | A (defer) | 0 |
| Q4 | Verification | Script + manual spot-check | 0 (verification only) |
| Q5 | addressLocality divergence | B (reconcile) | 2 lines in JSON-LD (items 4, 5) |

If all 5 recommendations are approved: ~10-line diff inside `<script type="application/ld+json">` + 5 `<a>` wrappers in the body. One PR. Individually revertable.

If any are rejected, the corresponding work narrows or moves to a new TRACKED entry as specified per question.

---

## What waits for your approval

Pick A/B/C/etc. per question. Once approved, execution is one tightly-scoped change to `rankings/best-pizza.html` followed by the Q4 verification script. End-of-turn summary will note what changed plus any tracked items spawned (Q3 generates a "BreadcrumbList workstream" entry for `_strategy/TRACKED.md` if A is selected; Q5 is a one-shot if B is selected, no tracking needed).

## Inconsistencies noted during read but out of step-3 scope

- **`best-pizza.html` still carries the canonical-template instructional comment block at the top** (lines 1–51 — "CANONICAL TOP-5 RANKING TEMPLATE", REPLACE/KEEP marker docs, intentional-decisions notes). Reads as though the file *is* the template. Likely a leftover from when best-pizza seeded the canonical. Not addressed by step 3. Worth a separate one-line tracked item — recommend logging in `_strategy/TRACKED.md` open one-offs.
- **`rankings/_detail-page-template.html` was not in the upload set this session**, though the bootstrap references it. The 5 rendered detail pages plus `_detail-page-design.md` provided enough context for step 3, but flagging.
