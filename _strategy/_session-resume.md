# Next session — first prompt seed

When you're ready to resume, paste this into Claude (the chat layer, not Claude Code) to bootstrap context:

> Resuming votedonbylocals work. Read `_strategy/HANDOFF.md` and `_strategy/TRACKED.md` to get current state, then propose options for the next workstream. My instinct is step 4 (kill Tailwind CDN) but happy to hear if something else has higher leverage given the GSC re-audit window May 7–20.

Why this works: HANDOFF gives you the end-of-last-session snapshot, TRACKED gives the open items. Together they're enough to propose next-workstream options without re-reading old chat transcripts.

## Recommended first workstream: step 4 (kill Tailwind CDN)

Pre-work to expect:
- **Investigation pass first** (analyze-first cadence): which files reference `cdn.tailwindcss.com`, what's the current Tailwind config (inline `tailwind.config`), what build tooling exists (npm? esbuild? just static?), and what the migration target should be.
- **Likely options:**
  - (a) Tailwind CLI build step producing a static `style.css`
  - (b) PostCSS pipeline
  - (c) hand-roll the ~30 utility classes actually used and drop Tailwind entirely
- **Decisions to surface before code:** which option, where the build runs (Netlify build? local? GitHub Action?), how it integrates with the existing minimal-tooling ethos.

## Alternative: best-new-coffee-shop workstream

Smaller scope, completes step 2/step 3 detail-page coverage to 100%. Would unblock BreadcrumbList (currently deferred per DECISIONS #15 Q3=A).
