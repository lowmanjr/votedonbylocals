# Handoff — read this first

You're picking up the Voted On By Locals project in a fresh session. This page gets you oriented in under five minutes.

## Read these files in order before doing anything

1. `PLAN.md` (repo root) — the 7-step master plan and current state.
2. `_strategy/DECISIONS.md` — the 12 non-obvious calls already made. Don't re-relitigate these without explicit reason.
3. `_strategy/CONTEXT.md` — brand positioning, monetization analysis, the "two forks ahead" framing. Read before making strategic suggestions.
4. `_strategy/TRACKED.md` — outstanding one-off items, tracked workstreams, and deferred items.
5. `_strategy/WORKFLOW.md` — meta-process: analyze-first cadence, working-files convention, session bootstrap, self-correction norm, pushback norm, verification norm. How we work.
6. `rankings/_template-canonical.html` — the canonical Top-5 ranking template. The chrome conventions established here apply to all future page templates including detail pages.
7. `rankings/_template-analysis.md` — analysis of the two design generations + the harmonization plan + the active tracked-items list.
8. `rankings/_port-content-sheet.md` — content fields per page + step-3/step-4 port summary.

That's about 30 minutes of reading. Don't skip it. The session that produced these files burned several rounds of analysis to land on the conventions; reading the conclusions is much cheaper than re-deriving them.

## Where things stand

Step 1 of the master plan (template harmonization across all 8 ranking pages) is **structurally complete** as of the previous session. All 7 Top-5 ranking pages conform to the canonical template. `best-new-coffee-shop.html` has its chrome harmonized but body content kept distinct (single-winner feature layout). `style.css` was audited and minimally pruned — 5 of 6 originally-proposed deletions are blocked on a tracked workstream (top-level page chrome upgrade) and documented inline in `style.css`. Open editorial follow-ups (cuisine-flag verifications, Top-4 → Top-5 promotion) live in `_strategy/TRACKED.md` and don't block step 2.

The site has 8 ranking pages: 7 Top-5 pages on the canonical template, plus `best-new-coffee-shop.html` on its own single-winner layout. "Ranking pages" elsewhere means all 8 unless otherwise scoped.

## What's next

**Step 2 of the master plan: restaurant detail pages.**

There are ~37 restaurants listed across the 8 ranking pages today; each is currently shown as just a name + tagline. Step 2 builds a per-restaurant detail page for each one. This is the highest-leverage content step in the entire master plan — it unlocks long-tail SEO, the restaurant-claimable winner badges flywheel (see `_strategy/CONTEXT.md`), richer schema, and the editorial surface area for the brand voice.

**Open design questions for the start of step 2** (don't pick answers in isolation — surface them and propose, per the workflow norm below):
- URL pattern: `/restaurants/{slug}.html`, `/r/{slug}.html`, `/charleston/{slug}.html` (anticipates multi-city), or flat `/{slug}.html`?
- Page template: mirror `best-new-coffee-shop`'s single-winner feature layout, or design a new richer-schema layout?
- Schema: `Restaurant` (matching ranking-page convention), `LocalBusiness` (richer — full address, hours, geo, price), or `CafeOrCoffeeShop`/`BarOrPub` etc. per the per-page-configurable pattern established in step 1?
- Editorial scope: hand-written editorial per restaurant, or stub-then-flesh, or auto-generate-from-tagline?
- Content fields: what new placeholder set does the detail-page template need? How does it overlap with the canonical's existing field set?

## Workflow norm (operator preference, established this session)

**Analyze first. Propose. Wait for approval. Then execute. Do not skip the analysis step even when the task seems mechanically simple.**

The operator (John) prefers:
- **Investigation-first before coding.** Read the relevant source files, grep for patterns, understand current state. Then propose. Don't start writing files until the proposal is approved.
- **Read-only verification before any writes.** When uncertain about file content, *re-read the source file* — don't trust narration of what it contains, including your own narration from earlier in the session. Files change; context drifts.
- **Audits before destructive operations.** When deleting, modifying, or restructuring something that touches multiple files, audit dependencies first. The `style.css` cleanup in this session is a worked example — would have visually broken 5 pages if executed without the dependency audit.
- **Tight scope per task.** Each PR / cleanup batch should be tightly scoped and individually revertable. Don't bundle independent changes into one large edit.
- **Surface decisions, don't make them silently.** When you encounter a design question that wasn't explicitly resolved (e.g., "should the schema type for this new page be Restaurant or LocalBusiness?"), surface it as a question with options and a recommendation. Don't pick an answer and move on without explicit confirmation.

This pattern is captured in `_strategy/DECISIONS.md` #12 and expanded in `_strategy/WORKFLOW.md`. The cost of analyze-first is real but smaller than the cost of one "shipped a bug, now reverting" cycle.

## Tone and style

The operator prefers concise, specific responses. Match the request:
- Quick question gets a direct answer.
- Multi-step task gets a structured breakdown with checkboxes/status.
- Strategy question gets recommendation + tradeoffs in 2–3 sentences, framed as something the operator can redirect.
- Don't narrate internal deliberation. State decisions and results.
- End-of-turn summaries: one or two sentences. What changed and what's next. Not a re-statement of the whole session.

When in doubt: less prose, more concrete.

## What NOT to do

- Don't start step 2 work without first proposing the design choices listed above.
- Don't modify any of the existing ported pages (the 8 ranking pages, the 5 top-level pages, the homepage) without explicit reason — they're considered done as of this session's close.
- Don't introduce new conventions that conflict with `_strategy/DECISIONS.md` without first surfacing the conflict and getting explicit override.
- Don't fabricate restaurant data or vote counts. The brand wedge is anti-fabrication; this is the project's most important integrity line.
- Don't bundle the 5-top-level-pages chrome upgrade or the `best-new-coffee-shop` per-page meta workstream into step 2. Those are tracked workstreams and stay tracked until the operator surfaces them.
