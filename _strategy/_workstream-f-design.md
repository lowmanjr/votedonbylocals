# Workstream F design — 5 top-level pages chrome upgrade

Working file. Will live at the repo root or under `_strategy/` per your call (it spans 5 files plus style.css; no single subdirectory naturally owns it). Author: Claude session 2026-05-03 picking up F per `_strategy/TRACKED.md`.

## Premise

Bring `about.html`, `vote.html`, `suggest-category.html`, `ambassadors.html`, `thank-you.html` onto the canonical chrome pattern established in step 1. After the upgrade, all 16 non-template HTML files on the site share an identical `<head>` chrome shape (Tailwind config inline, font preconnect+stylesheet link, body classes), and the dependency-aware `style.css` prune from DECISIONS #11 is no longer blocked.

This unblocks PLAN.md step 4 (kill Tailwind CDN) directly: a future build step needs uniform `<head>` shape across all pages so it can rewrite `<script src="cdn.tailwindcss.com">` and the inline config in one pattern. The current asymmetry — 16 pages with inline config, 5 without — would force the build to emit two different replacement patterns.

## Evidence: what's actually on the 5 pages today

Read the dump line-by-line. The 5 top-level pages have a **strict subset** of the canonical chrome:

| canonical chrome element                                  | top-level pages today |
| --------------------------------------------------------- | --------------------- |
| Google Analytics                                          | ✅ present (verbatim) |
| `<meta charset>` + `<meta viewport>`                      | ✅ present (verbatim) |
| `<title>` + `<meta description>`                          | ✅ present            |
| favicon link (`assets/images/favicon.png`, no `../`)      | ✅ present            |
| **font preconnect (googleapis + gstatic)**                | ❌ absent             |
| **font stylesheet link**                                  | ❌ absent             |
| Tailwind CDN script                                       | ✅ present            |
| **inline `tailwind.config = { ... }`**                    | ❌ absent             |
| `<link rel="stylesheet" href="assets/css/style.css">`     | ✅ present            |
| `<script src="assets/js/main.js" defer></script>`         | ✅ present            |
| `<body>` classes                                          | only `antialiased`    |

The bolded gaps are exactly what the upgrade adds. Everything else is already canonical.

## Class vocabulary the 5 pages actually use

Greps against the dump:

- **Tailwind utilities resolving via inline config** (need brand-orange / brand-cream / brand-dark / brand-gray defined): `bg-brand-orange` (vote/ambassadors/about), `border-brand-orange` (about), `font-poppins` (all 5)
- **Tailwind variants that need brand-orange in the inline config to function**: `focus:border-brand-orange`, `focus:ring-brand-orange` (vote × 8, suggest-category × 3, ambassadors × 4)
- **Standard Tailwind utilities** (no brand vocabulary): the rest — `bg-white/50`, `rounded-xl`, `space-y-*`, `text-gray-700`, etc.

### Surfacing a finding: focus-state styling is silently broken today

`focus:border-brand-orange` and `focus:ring-brand-orange` are **Tailwind utility variants**, not plain CSS classes. They resolve only via Tailwind's compiler against a config that defines `brand-orange`. The 5 top-level pages have no inline Tailwind config, so on those pages these variants resolve to undefined and the classes are no-ops.

`style.css` defines plain `.border-brand-orange` and `.bg-brand-orange` rules — those cover the bare classes (e.g. `border-brand-orange` alone), but they do **not** cover the variant-prefixed forms (`focus:border-brand-orange`). Tailwind's variants are JIT-generated; you can't simulate them with hand-rolled CSS without writing `:focus { border-color: #E67E22 }` rules per-class.

So today, on vote / suggest-category / ambassadors, focused form inputs do not render the brand-orange focus border or ring. They probably fall back to the browser default focus ring (visible but generic) or to whatever Tailwind's fallback resolution is.

This isn't a regression introduced by F — it's pre-existing. F **fixes it as a side effect** by adding the inline Tailwind config that makes `brand-orange` a defined color value, at which point the focus variants compile correctly. Worth noting in the commit message but doesn't change the upgrade plan.

## The exact diff per page (canonical chrome insertion)

Same insertion on all 5 pages. Drop the new lines into the `<head>` after the favicon link, before the `style.css` link. Verbatim, copy-paste from canonical:

```html
    <!-- KEEP: Fonts ---------------------------------------------------- -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Poppins:wght@400;600;700;800&display=swap" rel="stylesheet">

    <!-- KEEP: Tailwind + brand config ---------------------------------- -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['DM Sans', 'sans-serif'],
                        poppins: ['Poppins', 'sans-serif'],
                    },
                    colors: {
                        brand: {
                            orange: '#E67E22',
                            cream: '#FFF8F0',
                            dark: '#2D3748',
                            gray: '#4A4A4A'
                        }
                    }
                }
            }
        }
    </script>
```

Replacing the existing bare `<script src="https://cdn.tailwindcss.com"></script>` line.

**Body class change:** all 5 pages today have `<body class="antialiased">`. Canonical is `<body class="antialiased bg-brand-cream text-brand-dark min-h-screen flex flex-col">`. Drop-in replacement, identical on all 5.

## Two open design questions before execution

### Q1 — Poppins font weights: 400;600;700;800 (canonical) or 600;700 (current style.css `@import`)?

The 5 top-level pages currently load fonts via `style.css`'s `@import`, which requests `Poppins:wght@600;700`. The canonical chrome's font-stylesheet `<link>` requests `Poppins:wght@400;600;700;800` — two extra weights.

Once F lands, both the canonical-chrome `<link>` and `style.css`'s `@import` will fire on every top-level page, requesting overlapping but non-identical weight sets. Browsers will fetch and cache both, with the broader set winning where they overlap. Net behavior: page renders correctly, slight redundancy on initial load.

After step 4 (kill Tailwind CDN), the build step almost certainly inlines fonts at compile time and the `@import` in style.css gets dropped or rewritten. Until then:

- **A. Don't touch style.css.** Accept the redundant request. F stays purely additive on top-level pages; style.css `@import` cleanup defers to step 4 / step 7.
- **B. Update style.css `@import` to match canonical (`Poppins:wght@400;600;700;800`).** Brings the two requests into alignment. Cosmetic — both browsers and DNS caches handle it fine. One-line edit.
- **C. Delete style.css `@import` entirely.** All 16 (post-F: all 21) pages will load fonts via the canonical-chrome `<link>` instead. **But:** the rankings/restaurants/index already load fonts via the canonical `<link>` AND inherit the `@import` from style.css today, so this is a deletion that affects all 21 pages, not just the 5 being upgraded. Broader scope than F — needs its own dependency audit.

**Recommendation: A.** Keep F purely additive. Step 4 / 7 handles the `@import` deletion as part of the build-step migration, where the right pattern is a single source of font-loading truth (the build output), not "edit style.css now then again later." Cost of A is one redundant network request per top-level page until step 4 lands. Acceptable.

### Q2 — style.css prune: which 5 rules can be deleted, exactly?

Per the comment block in `style.css` (lines 378–393 in the dump), this prune was blocked on F. Now F unblocks it. Cataloguing what's actually deletable:

```css
body {
    background-color: #FFF8F0;     /* DELETE — canonical body uses bg-brand-cream class */
    color: #4A4A4A;                /* DELETE — canonical body uses text-brand-dark class */
    font-family: 'DM Sans', sans-serif;  /* KEEP — site-wide default; inline config sets sans family but doesn't apply to <body> directly without a class */
}

.font-poppins {                    /* KEEP — used by all 5 top-level pages even after upgrade; inline config defines poppins as a font family but font-poppins class still needs to map */
    font-family: 'Poppins', sans-serif;
}

.bg-brand-orange {                 /* DELETE — replaced by Tailwind utility from inline config */
    background-color: #E67E22;
}
.border-brand-orange {             /* DELETE — replaced by Tailwind utility from inline config */
    border-color: #E67E22;
}
```

Four deletions: 2 body declarations + 2 full rules. **The `body` rule itself stays** (its `font-family` declaration is still load-bearing); only its `background-color` and `color` declarations get removed. That matches the TRACKED entry's note ("one of which is the body rule's `background-color`/`color` declarations rather than a whole-rule deletion").

**Open question on `.font-poppins`:** the inline Tailwind config declares `poppins: ['Poppins', 'sans-serif']` under `fontFamily`. This makes the Tailwind utility class `font-poppins` resolve to the right family on pages that have the inline config. So once F lands and all 5 pages have the inline config, `.font-poppins` (the plain-CSS class in style.css) is redundant — Tailwind's utility takes over.

So actually 5 deletions, not 4: drop `.font-poppins` from style.css too.

**Caveat I want to flag:** I haven't independently verified that Tailwind's CDN-mode JIT actually emits a `.font-poppins { font-family: Poppins, sans-serif }` rule when `font-poppins` appears in markup. It should — that's the documented behavior — but the verification step needs to confirm visual fidelity post-upgrade before the `.font-poppins` rule deletes. Two-stage prune: delete the obviously-redundant rules first, leave `.font-poppins` for a follow-up if visual review surfaces any regression.

**Recommendation: 4 deletions in F's PR (2 body declarations + `.bg-brand-orange` + `.border-brand-orange`), `.font-poppins` deferred to a separate one-off.** Reduces the F PR's risk surface (any visual regression on heading typography is harder to attribute when bundled). The standalone `.font-poppins` deletion can land in a 5-line follow-up after John spot-checks one page in preview.

## Verification recipe

After edits, before commit:

```bash
# All 5 top-level pages have canonical-chrome elements:
for f in about.html vote.html suggest-category.html ambassadors.html thank-you.html; do
  echo "--- $f ---"
  grep -c "tailwind.config = {" "$f"          # expect 1
  grep -c "fonts.googleapis.com" "$f"         # expect 2 (preconnect + stylesheet link)
  grep -c "bg-brand-cream" "$f"               # expect 1 (body class)
  grep -c "min-h-screen flex flex-col" "$f"   # expect 1 (body class)
done
```

Each line should print `1`, `2`, `1`, `1` — total 4 successes per file × 5 files = 20 `1` or `2` lines.

```bash
# style.css deletions verified:
grep -c "background-color: #FFF8F0" assets/css/style.css   # expect 0
grep -c "color: #4A4A4A" assets/css/style.css              # expect 0
grep -c "^\.bg-brand-orange" assets/css/style.css          # expect 0
grep -c "^\.border-brand-orange" assets/css/style.css      # expect 0
grep -c "^body {" assets/css/style.css                     # expect 1 (rule stays, declarations gone)
grep -c "font-family: 'DM Sans'" assets/css/style.css      # expect 1 (the body rule's remaining declaration)
grep -c "^\.font-poppins" assets/css/style.css             # expect 1 (deferred deletion)
```

```bash
# All 21 pages still serve and parse (via local dev or curl-equivalent):
# John runs Netlify dev; spot-checks all 5 upgraded pages render with brand-orange focus
# rings on form inputs (vote, suggest-category, ambassadors), brand-cream background,
# and DM-Sans-on-cream typography. Visual fidelity = John's call at preview time.
```

## Commit grouping

Recommend 3 commits:

1. **`feat: upgrade 5 top-level pages to canonical chrome`** — adds font preconnect+link + inline Tailwind config + body class expansion to about/vote/suggest-category/ambassadors/thank-you. Side effect: brand-orange focus rings on form inputs now render correctly (pre-existing silent bug, fixed incidentally).
2. **`chore: prune now-redundant style.css rules`** — deletes the 2 body declarations + `.bg-brand-orange` + `.border-brand-orange`. Keeps `.font-poppins` (separate follow-up) and the body rule's font-family (still load-bearing). Updates the comment block in style.css to reflect the new state.
3. **`docs: resolve 5-top-level-pages workstream in TRACKED, log DECISIONS #16 if substantive calls were made`** — TRACKED scope-correction + Resolved migration; DECISIONS entry only if Q1=B or Q2-deferred-decision was non-obvious enough. (My recs above land Q1=A and Q2=4-deletions-now-1-deferred. Q1=A is "stay additive, defer to step 4" which is the obvious call given step 4's existence; Q2 is mechanical execution of DECISIONS #11. Probably no #16 needed unless John picks something other than the recommendations.)

Per the prior turn's lesson: **branch first.** `git checkout -b workstream-f-top-level-chrome-upgrade` before the first commit.

## Out of scope (do not bundle)

- step 4 (kill Tailwind CDN) itself
- header/footer build-time inlining
- `style.css` `@import` deletion (Q1=A)
- `.font-poppins` deletion (deferred to one-off)
- best-new-coffee-shop per-page meta workstream (different schema design pass)
- updating any of the 16 already-canonical pages (they're done)

## What waits for John's approval

- Q1 pick (A/B/C). My rec: A.
- Q2 pick (4 deletions vs 5 deletions in this PR). My rec: 4 now, defer `.font-poppins`.
- Commit grouping pick (3 separate vs single PR-with-3-commits vs different shape). My rec: single PR, 3 individually-revertable commits.
- Where this design doc lives. Recommend `_strategy/_workstream-f-design.md` (doesn't fit any single subdirectory; lives near other workstream-level strategy artifacts).

Once approved, the next turn produces the Claude Code prompt that executes commits 1–3 with verification gates between each.
