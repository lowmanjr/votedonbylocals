# Handoff — read this first

You're picking up the Voted On By Locals project in a fresh session. This page gets you oriented in under five minutes.

## Read these files in order before doing anything

1. `PLAN.md` (repo root) — the 7-step master plan and current state.
2. `_strategy/DECISIONS.md` — the non-obvious calls already made (15 entries). Don't re-relitigate these without explicit reason.
3. `_strategy/CONTEXT.md` — brand positioning, monetization analysis, the "two forks ahead" framing. Read before making strategic suggestions.
4. `_strategy/TRACKED.md` — outstanding one-off items, tracked workstreams, deferred items, and the running Resolved log.
5. `_strategy/WORKFLOW.md` — meta-process: analyze-first cadence, working-files convention, session bootstrap, self-correction norm, pushback norm, verification norm. How we work.
6. `rankings/_template-canonical.html` — canonical Top-5 ranking template. Chrome conventions from here apply across the site.
7. `rankings/_detail-page-template.html` — canonical detail-page template. Per-restaurant pages are generated from this via `scripts/generate_detail_page.py` + `data/restaurants.json`.

That's about 30 minutes of reading. Don't skip it.

## Last session summary (May 4, 2026)

**Shipped:**
- **PR #2** — workstream F: 5 top-level pages chrome upgrade + style.css prune (silent fix: form focus rings now resolve correctly).
- **PR #3** — best-coffee-shops detail pages + step-3 cross-link.
- **PR #4** — bulk port: 24 restaurant detail pages across 5 rankings, Azul Mexicano cuisine flip (Tex-Mex → Mexican), 4 locality reconciliations (San Miguel → Mt Pleasant, Chico Feo → Folly Beach, Edmund's Oast → North Charleston, Bar Weems → North Charleston), Home Team BBQ multi-entry AppearsOn shipped (first restaurant on >1 ranking). Generator patched for multi-entry AppearsOn. _redirects 301 attempt reverted within the same PR (created infinite loop; tracked for next attempt).

**Detail-page coverage:** 34 of ~37 restaurants. Only `best-new-coffee-shop` remains, by design (separate workstream).

**Master plan position:**
- Step 1 (template harmonization) ✅
- Step 2 (detail pages) ✅ except `best-new-coffee-shop`
- Step 3 (cross-linking) ✅ except `best-new-coffee-shop`
- Step 4 (kill Tailwind CDN) — next major workstream
- Steps 5–7 (OG images, sitemap/robots, final polish) — pending

**Calendar pin:** GSC re-audit window May 7–20. Avoid URL-structure changes during that window. Step 4 (Tailwind kill) is fine — it changes how CSS loads, not URLs.

## Workflow norms — confirmed this session

- **Claude Code drives PR lifecycle end-to-end:** branch, commits, push, PR, deploy poll, mechanical preview verify, rebase-merge, branch delete, local main reset. User intervenes only for visual judgment, substantive design questions, or halts.
- **Netlify-tolerant anchor regex memoized:**
  ```
  href=[\x22\x27]/restaurants/([a-z-]+)(?:\.html)?[\x22\x27]
  ```
  Silent default in preview-verification scripts; not surfaced as a finding.
- **Investigation-first:** before any branch/commit, dump current state (data counts, generator handling, TRACKED.md content, ranking-page JSON-LD) so edits are surgical and halts surface early.
- **Tight scope per PR:** opportunistic SEO/infra adds get pulled if they cost more than nothing. PR #4 _redirects revert is the precedent — when an infra change broke the preview, it got reverted same-PR rather than letting the rest of the work wait.
- **Unicode/HTML-entity normalization:** future verification scripts comparing rendered titles to source strings should NFC-normalize and decode HTML entities on both sides. Señor Tequila's caught this — the page was correct, the verification script's prefix check wasn't Unicode-aware.

## What's next

**Recommended:** master plan step 4 (kill Tailwind CDN). Prerequisites are now satisfied — top-level pages are on the canonical chrome (PR #2), detail pages exist (PR #3 + #4), so the Tailwind class set is stable across the whole site. Step 4 needs a design pass before any code: which build approach (Tailwind CLI / PostCSS / hand-roll), where the build runs (Netlify build / local / GitHub Action), how it integrates with the project's minimal-tooling ethos.

**Alternative:** `best-new-coffee-shop` per-page meta workstream. Smaller scope; completes step 2/3 detail-page coverage to 100%. Would unblock BreadcrumbList (currently deferred per DECISIONS #15 Q3=A).

See `_strategy/_session-resume.md` for the bootstrap prompt to start the next session.

## Workflow norm (operator preference, established)

**Analyze first. Propose. Wait for approval. Then execute.** Don't skip the analysis step even when the task seems mechanically simple. See DECISIONS #12 + WORKFLOW.md for the worked rationale.

The cost of analyze-first is real but smaller than the cost of one "shipped a bug, now reverting" cycle. PR #4's _redirects loop is a recent example where investigation caught the bug in PHASE 8 verification before the bad config reached production.

## Tone and style

The operator prefers concise, specific responses. Match the request:
- Quick question gets a direct answer.
- Multi-step task gets a structured breakdown with checkboxes/status.
- Strategy question gets recommendation + tradeoffs in 2–3 sentences, framed as something the operator can redirect.
- Don't narrate internal deliberation. State decisions and results.
- End-of-turn summaries: one or two sentences. What changed and what's next. Not a re-statement of the whole session.

## What NOT to do

- Don't start step 4 work without first proposing the design choices listed above.
- Don't modify any of the existing pages without explicit reason — they're considered stable as of this session's close.
- Don't introduce conventions that conflict with `_strategy/DECISIONS.md` without first surfacing the conflict and getting explicit override.
- Don't fabricate restaurant data, vote counts, or hours. The brand wedge is anti-fabrication; this is the project's most important integrity line.
- Don't bundle the `best-new-coffee-shop` per-page meta workstream into step 4 — it's a separate tracked workstream and stays tracked until the operator surfaces it.
- Don't retry the `/restaurants/:slug /restaurants/:slug.html 301!` _redirects rule from PR #4 without one of the candidate fixes documented in TRACKED.md (two-rule passthrough OR `pretty_urls = false` in netlify.toml). The naive rule infinite-loops.
