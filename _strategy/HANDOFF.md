# Handoff — read this first

You're picking up the Voted On By Locals project in a fresh session. This page gets you oriented in under five minutes.

## Read these files in order before doing anything

1. `PLAN.md` (repo root) — the 7-step master plan: structural/strategic content (the *why* of each step). Per-step status lives in this HANDOFF (see "Master plan position" below), not in PLAN.md.
2. `_strategy/DECISIONS.md` — the non-obvious calls already made. Don't re-relitigate these without explicit reason.
3. `_strategy/CONTEXT.md` — brand positioning, monetization analysis, the "two forks ahead" framing. Read before making strategic suggestions.
4. `_strategy/TRACKED.md` — outstanding one-off items, tracked workstreams, deferred items, and the running Resolved log.
5. `_strategy/WORKFLOW.md` — meta-process: analyze-first cadence, working-files convention, session bootstrap, self-correction norm, pushback norm, verification norm. How we work.
6. `rankings/_template-canonical.html` — canonical Top-5 ranking template. Chrome conventions from here apply across the site.
7. `rankings/_detail-page-template.html` — canonical detail-page template. Per-restaurant pages are generated from this via `scripts/generate_detail_page.py` + `data/restaurants.json`.

That's about 30 minutes of reading. Don't skip it.

## Last session summary (May 4, 2026 — afternoon)

Three PRs merged in a focused doc/meta session. Earlier-May-4 session (6 PRs: #5–10) fully captured in `_strategy/TRACKED.md` Resolved.

- **PR #12** — `best-new-coffee-shop.html` per-page meta + JSON-LD. Closed master plan steps 2 + 3 to 100%. Sitemap `<lastmod>` coverage 40 → 41 pages (URL count unchanged at 46). Subtle: PHASE 0 investigation caught two corrections before code touched the page — JSON-LD field order needed to mirror `babas-on-cannon.html`'s shape verbatim, and `servesCuisine` flipped from spec's "Coffee" to "European Café" for brand consistency. Same shape as PR #8's field-semantics catch — the precedent keeps earning. JSON-LD `url` points at the featured-winner page itself per new DECISIONS #16 (Wentworth has no detail-page slug; the ranking page is its detail context).
- **PR #13** — PLAN.md / HANDOFF.md doc-hygiene reconciliation. PLAN.md is now structural/strategic (the *why* of each step); per-step status text fully retired. HANDOFF.md is the single source of truth for current per-step status. Subtle: PHASE 2 grep verification originally targeted the L7 stale-callout literal phrasing, missed L32's parallel "stale and pending reconciliation" phrasing — caught at spot-read. Workflow lesson: when retiring a callout, grep for the concept across phrasings, not the literal form.
- **PR #14** — Hero dot-pattern brand-color tokenization. Moved `.bg-dot-pattern` from `index.html` inline `<style>` into `src/input.css` as `@layer components` using `theme('colors.brand.orange')`. Visual unchanged. Subtle: PHASE 2 hex-sweep returned 1 hit in `assets/css/built.css` (compiler output), not 0 as spec expected. Hand-written `@layer components` rules compile to the raw config hex; Tailwind-auto-generated utilities serialize as decimal-rgb for opacity-modifier support. The single-source-of-truth invariant still holds (edit `tailwind.config.js` + rebuild → `built.css` updates). Future hex sweeps exclude `built.css` alongside `tailwind.config.js` as compiler output.

## Master plan position

Current truth (per-step status of record; PLAN.md intentionally omits this):

- **Step 1** (template harmonization) ✅
- **Step 2** (detail pages) ✅ — closed by PR #12
- **Step 3** (schema cross-linking) ✅ — closed by PR #12
- **Step 4** (kill Tailwind CDN) ✅ — PR #6
- **Step 5** (OG image generation) ⏳ — **NEXT major workstream**
- **Step 6** (sitemap.xml + robots.txt) ✅ — PR #5 (sitemap), PR #5 (robots), PR #8 (`<lastmod>`)
- **Step 7** (final polish) ⏳ partial — header/footer inlining done (PR #7); inliner tooling shipped (PR #9 + #10); other final-polish items TBD when surfaced

## Calendar pin

GSC re-audit window **May 7–20**. Avoid URL-structure changes during that window — Google's recrawl should land cleanly on the URL set as-of merge.

Why it matters: Google takes ~2 weeks to crawl a freshly submitted sitemap. URL changes mid-crawl confuse re-indexing — pages can lose ranking signal that took weeks to establish. Wait until post-window for any redirect/routing work (e.g., the Netlify pretty-URL canonical asymmetry in TRACKED).

URL-stable workstreams that are safe in-window:
- OG image generation (adds asset files, no URL changes)
- Per-page meta / JSON-LD edits (PR #12 is the worked example)
- Tooling work that doesn't touch production HTML

The most recent `--refresh` PR (#10) is a worked example: tooling-only changes that don't touch production HTML are fine during the window.

## Workflow norms — confirmed and reinforced this session

- **Claude Code drives PR lifecycle end-to-end:** branch, commits, push, PR, deploy poll, mechanical preview verify, rebase-merge, branch delete, local main reset. User intervenes only for visual judgment, substantive design questions, or halts.
- **Netlify-tolerant anchor regex memoized:** preview-verification regex must allow single OR double quotes, alphabetized attr order, and optional `.html` (Netlify pretty-URLs). Silent default in verification scripts; not surfaced as a finding.
- **Investigation-first:** before any branch/commit, dump current state (data counts, generator handling, TRACKED.md content, JSON-LD, marker presence, etc.) so edits are surgical and halts surface early. Six PRs landed today using this cadence with zero rollbacks.
- **Tight scope per PR:** opportunistic SEO/infra adds get pulled if they cost more than nothing. PR #4's `_redirects` revert (May 3) remains the worked example.
- **Unicode/HTML-entity normalization:** future verification scripts comparing rendered titles to source strings should NFC-normalize and decode HTML entities on both sides.
- **Halt-for-approval gates.** Used at PR #6 PHASE 3 (built.css verification) and at PR #6/#7 visual verify. They caught nothing critical, but the discipline is the point — they're the cheap-when-not-needed insurance against the expensive case.
- **Retrofit-via-rerun pattern.** PR #9's marker retrofit ran the inliner from a known-clean state rather than pattern-matching existing files for retrofit. When introducing a new marker / wrapper / convention, "re-run the generator" is safer than "find existing instances and surgically wrap them." Apply this if a similar situation surfaces.
- **Field-semantics correction precedent.** PR #8 caught a real ambiguity in the design pre-work — `dateModified` literally means "last modified" but the proposed git-first-add seed is semantically `datePublished`. Final solution: ship both fields. When designing new schema, watch for this kind of ambiguity in field names. Other surfaces with similar potential confusion: `aggregateRating` vs `reviewRating`, `address` vs `areaServed`, `LocalBusiness` vs `CafeOrCoffeeShop`. Flag explicitly during design pre-work. PR #12 reinforced this with two more catches: JSON-LD field *order* is also a semantic surface (`datePublished`/`dateModified` came before `url` in the prior precedent; mirror established structures verbatim rather than re-ordering), and `servesCuisine` value choice is brand-consistency-bound (the page's own copy is the right anchor, not a generic genre label).
- **PHASE 0 investigation pays off across PR types.** The discipline isn't only for code-heavy PRs. Three catches in the May 4 afternoon session: PR #12 (field-order + servesCuisine before any edit), PR #13 (L32 stale-callout caught via spot-read after the spec's grep missed it), PR #14 (built.css hex-sweep edge case caught at PHASE 2). The cost of investigation-first scales sublinearly with PR complexity; the savings from each catch scale linearly with how late it would have been caught otherwise.
- **Grep for the concept, not the literal phrase.** When retiring a callout, convention, or stale claim across multiple docs, the verification regex must match conceptual variations, not just one literal form. PR #13's verify pass missed L32's "stale and pending reconciliation" phrasing because the regex targeted L7's "stale relative to actual progress." Always sanity-check by spot-reading affected files end-to-end, not just by grep alone.
- **Compiler output ≠ source duplication.** Future repo-wide hex sweeps (`#E67E22`, etc.) should exclude `assets/css/built.css` alongside `tailwind.config.js`. Tailwind compiles `@layer components` rules with `theme()` calls to raw hex in the output, while auto-generated utilities serialize as `rgb(...)` for opacity-modifier support — so the same source-of-truth color appears in both forms in `built.css` legitimately. The single-source-of-truth invariant lives at the source layer (`tailwind.config.js`), not the output layer. PR #14 surfaced this.

## What's next

**Master plan step 5 — OG image generation** is the unambiguous next major workstream.

Design-first. Visual concept goes before code. Recommended build approach: HTML/CSS template rendered via headless browser (Playwright) — Python script populates a template per slug, screenshots at 1200×630, writes PNG to `assets/images/og-{slug}.png`. Alternatives are Figma batch export and hand-designed-per-image; both have higher quality ceilings but don't scale to ~42 images.

Scope: ~42 images total (8 ranking pages, 33 detail pages, 1 site default at `og-default.png`).

Why it matters: every page's chrome already declares `<meta property="og:image" content="...og-{slug}.png">`. Today every one of those URLs 404s. Step 5 fulfills the existing promise; longer deferral = more time with broken share previews.

Estimated scope: 1–2 days. Half visual design, half pipeline build, time for export + verification. URL-stable (asset-only additions), so safe in the May 7–20 GSC window.

### Other workstreams in TRACKED, in rough priority order

Not the lead — surface when ready to make any of these the next focus:

- **BreadcrumbList schema** — eligible as of May 4 (bulk port done; step 2 + step 3 at 100%). ~2 hours.
- **Detail-page Locations module** — 11 multi-location restaurants queued. 1–2 day design-first workstream.
- **Netlify pretty-URL canonical asymmetry** — discrete config-only PR. **DO NOT START during May 7–20 GSC window**; either ship pre-window (May 4–6 with full preview-isolation) or post-May-20.
- **Title verbosity for cuisine-name overlap** — ~30 min. Trigger when bulk port reveals more cases.

## Workflow norm (operator preference, reinforced)

**Analyze first. Propose. Wait for approval. Then execute.** Don't skip the analysis step even when the task seems mechanically simple. See DECISIONS #12 + WORKFLOW.md for the worked rationale.

The cost of analyze-first is real but smaller than the cost of one "shipped a bug, now reverting" cycle. PR #4's `_redirects` loop (May 3) and PR #9's `dedent` whitespace bug (caught in integration testing, fixed in the same PR) are recent examples of investigation-or-integration-test catching the bug before it reached production.

## Tone and style

The operator prefers concise, specific responses. Match the request:
- Quick question gets a direct answer.
- Multi-step task gets a structured breakdown with checkboxes/status.
- Strategy question gets recommendation + tradeoffs in 2–3 sentences, framed as something the operator can redirect.
- Don't narrate internal deliberation. State decisions and results.
- End-of-turn summaries: one or two sentences. What changed and what's next. Not a re-statement of the whole session.

## What NOT to do

- Don't introduce a Node-side build pipeline (Vite, Next.js, Astro, etc.) when the existing Python + npm-Tailwind setup is sufficient. Project ethos is minimal-tooling.
- Don't fabricate restaurant data, vote counts, hours, OG image content, or meta descriptions. The brand wedge is anti-fabrication; this is the project's most important integrity line.
- Don't unilaterally pull deferred items into a PR. The deferred items in `_strategy/TRACKED.md` are deliberate scoping, not failures — surface the conflict before pulling them in.
- Don't modify any of the 49 production HTML pages without explicit reason — they're considered stable as of this session's close.
- Don't introduce conventions that conflict with `_strategy/DECISIONS.md` without first surfacing the conflict and getting explicit override.
- Don't retry the `/restaurants/:slug /restaurants/:slug.html 301!` `_redirects` rule without one of the candidate fixes documented in TRACKED.md (two-rule passthrough OR `pretty_urls = false` in netlify.toml). The naive rule infinite-loops.
- Don't edit the inlined chrome directly in any of the 49 pages. Edit `components/header.html` or `components/footer.html`, then run `python scripts/inline_chrome.py --refresh`. Inline edits get overwritten on next refresh and are silently flagged by `--check` as divergence.
