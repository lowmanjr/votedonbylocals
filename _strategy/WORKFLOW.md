# Workflow norms

How Claude and operator collaborate on Voted On By Locals. The norms below have emerged across sessions; capturing them so any new session can land in the same workflow without the operator re-explaining each one.

## Analyze-then-execute cadence

For any non-trivial change — refactor, content port, new feature scaffolding, schema design — the first response is analysis written to a file (prefixed with underscore to mark as a working artifact), not code. The operator reviews the analysis, gives feedback or changes, and a second prompt executes the change.

Skip the analysis step ONLY for genuinely mechanical single-file edits where the diff is obvious and the consequences are bounded (typo fix, single-line content update, removing a single line of dead code).

The cost of writing an analysis is real but smaller than the cost of one "shipped a bug, now reverting" cycle. See `DECISIONS.md` #12 for worked examples where this pattern caught real issues before they shipped.

## Working files convention

Files prefixed with underscore (`_template-analysis.md`, `_port-content-sheet.md`, etc.) are intermediate artifacts created during a workstream. They live in the directory of the work they support — not in `_strategy/`. The `_strategy/` docs are durable; underscore working files in other directories are intentionally ephemeral.

A working file can be deleted once its workstream is fully done AND the decisions/learnings have been migrated to a durable strategy doc. Until then, leave it. A future contributor (or future Claude session) might want to see the analysis that led to the current state.

## Handoff structure

Six durable strategy docs, each with one purpose. `PLAN.md` lives at the repo root because it's the project's top-level entry point; the other five live in `_strategy/`. Don't bundle. If a piece of information could go in two places, pick one and link from the other.

- `PLAN.md` — what (the master plan, what's complete, what's next)
- `DECISIONS.md` — why (non-obvious calls and their reasoning)
- `CONTEXT.md` — where we're going (brand, vision, monetization analysis, two-forks framing)
- `TRACKED.md` — what's loose (open one-offs, workstreams, deferred items)
- `HANDOFF.md` — how to start (read order, current state, workflow norms condensed)
- `WORKFLOW.md` — how we work (this file)

## Session bootstrap pattern

Every new session begins with the operator pasting a bootstrap message that asks Claude to:

1. Read the docs `HANDOFF.md` lists, in that order.
2. Read the canonical template and any active working files (e.g., `rankings/_template-canonical.html`, any `_*.md` files relevant to the current workstream).
3. Summarize back: what the project is, what's complete, what's next, any open questions.
4. Wait for explicit operator confirmation before proceeding.

This catches handoff drift — if Claude's summary is wrong, the operator catches it before any code gets written. The summary doubles as a stress test of the docs themselves: anything Claude can't reconstruct from the docs is a doc gap to fix.

## Self-correction norm

When the operator's instruction contains an obvious, unambiguous typo or incorrect reference, Claude should silently fix it and surface the correction in the response. Examples of fixes Claude should make without asking:

- Filename typo with one obvious target (operator says `best-coffe-shops` when they clearly mean `best-coffee-shops`; or `style.cs` when they clearly mean `style.css`)
- Misspelled tool/library name where the correct spelling is unambiguous
- Off-by-one in a section number when the section title disambiguates the intent

Claude should NOT silently fix anything ambiguous or substantive. Those go back to the operator as questions. Specifically, do NOT silently change:

- Editorial decisions (cuisine values, tone, copy)
- Architectural decisions (URL patterns, schema choice, naming)
- Anything where two interpretations are equally plausible

## Pushback norm

When an operator instruction will cause a problem if executed literally (e.g., deleting CSS rules that other pages still depend on), Claude should:

1. Audit the dependency before making the change.
2. Execute what's safe (the parts that don't break things).
3. Block what isn't (refuse to ship the breakage).
4. Report the breakdown with concrete evidence (which files, which lines, which dependency).

Don't execute literally if literal execution will ship breakage. The operator wants the goal, not the literal command. The `style.css` cleanup (`DECISIONS.md` #11) is the worked example: operator asked for 6 deletions, audit showed 5 would break top-level pages, Claude executed 1 and reported the other 5 as blocked with reasons. Operator accepted that resolution.

## Verification norm

Every workstream should end with concrete mechanical verification:

- HTTP 200 checks via local server
- Regex sweeps for unfilled placeholders, deleted strings, etc.
- Structural diffs against canonical templates
- File-existence and line-count sanity checks

Visual review (does it look right?) is the operator's responsibility — Claude can't see the rendered page. Mechanical verification (does it parse, does it serve, does it match the spec?) is Claude's responsibility.

The bar: at end of session, the operator should be able to confirm the state in <2 minutes by spot-checking what Claude verified, rather than re-running the verification themselves.
