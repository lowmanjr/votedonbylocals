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

## Last session summary (August 24–25, 2026)

`best-wings` launched as a **Top-3** — the second Top-N launch, and the one that closed the recipe deferral in DECISIONS #23.

- **PR #39** — `best-wings` Top-3: Home Team BBQ, Hannibal's Kitchen, Moe's Crosstown Tavern. 64 files. One net-new restaurant entry (`hannibals-kitchen`), two `appearsOn` appends, full registry pass (nav, homepage grid, vote form, `og_rankings.json`), 2 new OG PNGs, sitemap regen. Merged as `cb61c37`.
- **The roster shrank from 5 to 3 during sourcing.** Three of the five proposed restaurants were excluded and all three net-new candidates failed: Dashi (confirmed permanently closed 2026-06-14), Tru Blues House of Wings (contested status), Nigel's Good Food (location set contested). Hannibal's Kitchen was sourced as a replacement and passed. All filed in TRACKED with the conflict-vs-closure distinction: the first two carry re-verification triggers, Dashi carries a no-trigger record so a future session does not re-propose it.
- **Two rules were discovered and are now documented in DECISIONS #23.** (a) The identity-vs-liveness gate: an own website is authoritative for name, address and menu, and *inadmissible* as evidence the doors are open — liveness needs dated third-party signals, and a conflict between sources disqualifies exactly like a closure. (b) `servesCuisine` on ranking ItemLists is list-scoped and hand-authored, not copied from `restaurants.json`; it governs 12 of 40 pre-launch entries and had never been written down.
- **Top-3 is a new ranking-length precedent**, alongside Top-2 from PR #34. Both arrived as what survived honest sourcing rather than as a target — N is an output, never an input.
- **PR #40** (open) — reword Hannibal's tagline; the shipped "Soul Food Landmark" duplicated row 1's "BBQ Institution".
- **PR #41** (open) — this documentation pass: formalize the Top-N recipe, correct the merge norm, refresh this summary, fix the stale page count in `inline_chrome.py`.

Ordering gotcha worth remembering: `generate_sitemap.py` reads `dateModified` to build `<lastmod>`, so it must run **after** any `dateModified` bumps or the sitemap ships stale dates silently.

## Master plan position

Current truth (per-step status of record; PLAN.md intentionally omits this):

- **Step 1** (template harmonization) ✅
- **Step 2** (detail pages) ✅ — closed by PR #12
- **Step 3** (schema cross-linking) ✅ — closed by PR #12
- **Step 4** (kill Tailwind CDN) ✅ — PR #6
- **Step 5** (OG image generation) ✅ — closed by PR #16; backplate polish in PR #17
- **Step 6** (sitemap.xml + robots.txt) ✅ — PR #5 (sitemap), PR #5 (robots), PR #8 (`<lastmod>`)
- **Step 7** (final polish) ⏳ partial — header/footer inlining done (PR #7); inliner tooling shipped (PR #9 + #10); other final-polish items TBD when surfaced

Steps 1–6 are now done; step 7 is the only formal master plan item remaining. Future workstreams source from `_strategy/TRACKED.md`, not PLAN.

## Calendar pin

~~GSC re-audit window **May 7–20**~~ — **this window closed 2026-05-20 and is no longer binding** (noted 2026-08-25). URL-structure work is unblocked, including the Netlify pretty-URL canonical asymmetry in TRACKED. The reasoning below is retained because it applies to the *next* sitemap resubmission, not because a window is currently open.

Why it matters: Google takes ~2 weeks to crawl a freshly submitted sitemap. URL changes mid-crawl confuse re-indexing — pages can lose ranking signal that took weeks to establish.

URL-stable workstreams that are safe in-window:
- OG image generation (adds asset files, no URL changes)
- Per-page meta / JSON-LD edits (PR #12 is the worked example)
- Tooling work that doesn't touch production HTML

The most recent `--refresh` PR (#10) is a worked example: tooling-only changes that don't touch production HTML are fine during the window.

## Workflow norms — confirmed and reinforced this session

- **Claude Code drives PR lifecycle end-to-end:** branch, commits, push, PR, deploy poll, mechanical preview verify, squash-merge, branch delete, local main reset. **Squash, not rebase** — corrected 2026-08-25 against the evidence: `main` is linear, merge commits have a single parent, and each carries a `(#N)` suffix, which is squash behaviour. Pass `--subject` explicitly at merge time, because GitHub defaults the squash subject to the PR title and that will land without a conventional type prefix (see DECISIONS #23, "Merge"). User intervenes only for visual judgment, substantive design questions, or halts.
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

Master plan steps 1–6 are done. Future workstreams source from `_strategy/TRACKED.md`. Step 7 (final polish) remains open as a catch-bucket but isn't a discrete next target.

**Lead: Detail-page Locations module.** 11 multi-location restaurants queued (8 from workstream H bulk port + 3 from prior PRs). 1–2 day design-first workstream — data shape, URL decision, and JSON-LD shape (Place children vs branchOf parent) all need design pass before code. URL decision determines GSC-window safety: one-canonical-URL is window-safe; sub-URLs per location are not.

### Other workstreams in TRACKED, in rough priority order

Not the lead — surface when the operator redirects:

- **Top-level pages OG coverage** — 5 pages still bare (about, vote, suggest-category, ambassadors, thank-you). ~2 hours, design-first per-page. Adjacent to PR #16's OG pipeline; tooling still warm. Window-safe.
- **OG meta-line dedup when restaurant name contains cuisine descriptor** — sweep-and-fix. Pairs naturally with title-verbosity workstream. Polish-tier; no urgency.
- **Title verbosity for cuisine-name overlap** — ~30 min. Trigger when bulk port reveals more cases.
- **Post-May-20 chrome follow-ups** — TRACKED entry for "Add `id='rankings'` to index.html cards section" tied to PR #18's `/#rankings` fragment. Trigger: post-May-20.
- **Netlify pretty-URL canonical asymmetry** — discrete config-only PR. **DO NOT START during May 7–20 GSC window**; earliest safe restart is May 21.

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
