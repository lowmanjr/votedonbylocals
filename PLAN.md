# Voted On By Locals — Master Plan

## Project summary

Voted On By Locals (votedonbylocals.com) is a static HTML site that publishes community-voted Top-5 restaurant rankings for Charleston, SC. It's a single-author project — no framework, no database, no backend. Pages are hand-written HTML deployed to Netlify; vote submissions flow into Netlify Forms and rankings are hand-curated from those submissions. The brand wedge is "anti-algorithm, ad-free, by locals" — explicitly positioned against Yelp/Google reviews. Current scale: 8 ranking pages (7 Top-5 lists + 1 single-winner feature for `best-new-coffee-shop`), ~37 restaurants total, 5 top-level support pages (`about`, `vote`, `suggest-category`, `ambassadors`, `thank-you`), one homepage. Multi-city expansion via "ambassadors" is the stated long-term vision but currently exists only as a contact form.

## How to read this document

This is the master plan for everything that needs to happen on the site after the initial template-harmonization migration. Each step has a `why this order` justification — the sequencing is load-bearing, not arbitrary. Earlier steps create the foundation later steps depend on. Don't reorder steps without thinking through what gets retrofitted.

For why each individual decision was made, see `_strategy/DECISIONS.md`. For the broader strategic context (brand positioning, monetization analysis, the multi-city vision), see `_strategy/CONTEXT.md`. For the running list of one-off and workstream items, see `_strategy/TRACKED.md`. For the meta-process (how Claude and operator collaborate, analyze-first cadence, etc.), see `_strategy/WORKFLOW.md`. For next-session onboarding, start with `_strategy/HANDOFF.md`.

---

## The 7-step master plan

### Step 1: Template harmonization (rankings) — ✅ COMPLETE

Unified all 8 ranking pages onto a single canonical template (`rankings/_template-canonical.html`). Standardized: `<head>` chrome (GA, font preconnect, inline Tailwind config), body classes, hero block, list card, bottom CTA, JSON-LD `ItemList` of `Restaurant` items with full address per item, canonical URL, full Open Graph + Twitter card meta, semantic `<h2>` for restaurant headings, emoji-per-row icons, "Updated [Month Year]" pill, "Disagree with this list? Cast your vote!" CTA copy. Two content fields split: `{{Description}}` (long, keyword-rich) for `<meta description>` + JSON-LD; `{{ShareTagline}}` (short, hook-driven) for OG/Twitter. Per-page deviations documented in canonical: `CafeOrCoffeeShop` schema type override on `best-coffee-shops`; Top-4 with "more to come" subtitle on `best-new-restaurants`. `best-new-coffee-shop` chrome harmonized to canonical KEEP blocks while body content (single-winner feature with editorial blurb + address/hours sidebar) preserved.

**Why first:** The 8 ranking pages are the most visible content on the site. Two design generations coexisted (newer/canonical seed in `best-pizza`, older numbered-list pattern in `best-nice-restaurants` etc.) and metadata was inconsistent (only 1 of 8 pages had structured data, only 1 had OG tags, 4 different "Updated" date formats). Without a single source of truth, every subsequent step would multiply the inconsistency — schema would need authoring 8 different ways, OG images 8 different sizes, sitemap entries 8 different URL conventions. The template is the chassis everything that follows depends on.

**Tracked items remaining from this step** (full list in `_strategy/TRACKED.md`):
- 4 cuisine-flag verifications (Chico Feo, Vern's, Azul Mexicano, Home Team BBQ disambiguation)
- 5-top-level-pages chrome upgrade workstream (`about`, `vote`, `suggest-category`, `ambassadors`, `thank-you`)
- `best-new-coffee-shop` per-page meta workstream (deferred until LocalBusiness vs CafeOrCoffeeShop schema decision is made)

---

### Step 2: Restaurant detail pages — ⏳ NEXT

Build a per-restaurant detail page for each ranked establishment. The ranking pages currently list ~37 restaurants total; each is shown as a name + tagline only. Detail pages turn each restaurant into a crawlable entity with its own URL, schema, content, and badge target.

Open design questions for the start of step 2:
- **URL pattern.** Options: `/restaurants/{slug}.html`, `/r/{slug}.html`, `/charleston/{slug}.html` (city prefix anticipates multi-city), `/{slug}.html` (flat). Each has trade-offs.
- **Page template.** Could mirror `best-new-coffee-shop`'s single-winner feature layout (address, hours, editorial blurb, pull quote) or use a different richer-schema layout (`LocalBusiness` with full geo + hours + price range + cuisine).
- **Editorial scope.** Hand-written editorial per restaurant? Stub initially with auto-generated copy from existing rankings? Both?
- **Cross-linking.** Each ranking page's JSON-LD `item.url` should point to the detail page (this is also Step 3's main mechanic).

**Why second:** Detail pages are the highest-value content step on the plan. They unlock: (a) long-tail SEO — "{restaurant name} Charleston" search queries currently land on Yelp/Google because no Voted On By Locals page exists for the restaurant; (b) restaurant-claimable winner badges (each badge needs a "this restaurant" anchor URL — see `_strategy/CONTEXT.md`'s flywheel hypothesis); (c) richer schema possible (per-restaurant `LocalBusiness` with full geo, hours, price); (d) editorial surface area for the brand voice. Doing this before step 3 (schema cross-linking) is necessary because step 3's whole mechanic is `ranking.item.url → detail.page` — there's no `detail.page` to link to until step 2.

---

### Step 3: Schema cross-linking on rankings — ⏳ not started

Update the ranking pages' JSON-LD `ItemList` so each item's `url` field points to the detail page from step 2. Possibly also: add `BreadcrumbList` schema, `mainEntityOfPage` references, and consider upgrading per-item `@type` from `Restaurant` to the full `LocalBusiness` profile that detail pages will host.

**Why third:** Schema cross-linking is what makes the structured data graph useful for Google's entity resolution. A standalone `ItemList` is fine; an `ItemList` whose items each link to canonical entity pages is much stronger. Doing this before detail pages exist would mean writing URLs to nowhere; doing it after is a single-pass content edit. Keep step 3 separate from step 2 because step 2 is page creation (high editorial scope) while step 3 is metadata weaving (mechanical, fast).

---

### Step 4: Kill Tailwind CDN — ⏳ not started

Replace `<script src="https://cdn.tailwindcss.com">` (~3MB JS, JIT-compiles in browser, real Core Web Vitals concern, causes FOUC) with a precompiled CSS file. Probably means introducing a tiny build step (Tailwind CLI, single command) or using a hosted built CSS. The inline `tailwind.config` blocks in each page's `<head>` get consolidated into a single source.

**Why fourth:** This is a performance/infrastructure change that touches every page in the site. Doing it before step 2 means re-doing the migration after step 2 adds detail pages. Doing it after detail pages means the page set is stable. **Prerequisite:** the 5-top-level-pages chrome upgrade tracked workstream (see `_strategy/TRACKED.md`). Step 4 cannot start until that workstream completes — those pages need to be on the Tailwind path so the build covers them uniformly.

---

### Step 5: OG image generation — ⏳ not started

The canonical template references `og:image` URLs at `https://votedonbylocals.com/assets/images/og-{slug}.png` that don't exist yet. Detail pages from step 2 will add their own OG image needs. Generate both batches together — likely one Figma file with overlay text per page, exporting ~10 ranking images + ~37 detail images.

**Why fifth:** By step 5 the URL set is stable (steps 1–4 done) and we know every page that needs an image. Generating images before that means redoing them when more URLs land. Also: every social share between now and step 5 fails to render an image preview — that's not catastrophic (most platforms gracefully omit the preview), but it does suppress click-through rates while we wait.

---

### Step 6: SEO hygiene (sitemap.xml + robots.txt) — ⏳ not started

Currently absent. `sitemap.xml` enumerates all crawlable URLs for search engines. `robots.txt` declares the crawl policy and points to the sitemap.

**Why sixth:** Building a sitemap before the URL set is stable wastes effort. By step 6 every URL has full structured data, canonical tags, OG images, and stable pretty paths. The sitemap acts on a clean slate. Could be done earlier in principle, but the value is greater after the page set is stable.

---

### Step 7: Final polish — ⏳ not started

Catch-all for cross-cutting items that surface during the migration but don't fit any single step. Expected contents:
- Replace client-side `fetch()` of `header.html`/`footer.html` with build-time inlining (currently `assets/js/main.js` injects header/footer at runtime — small FOUC risk, no nav for JS-disabled clients)
- Performance audit (Lighthouse, Core Web Vitals)
- Accessibility audit
- Broken-link sweep
- Whatever editorial cleanup the migration surfaced

**Why last:** Polish is naturally last — it's the things you notice once everything else is settled. Don't optimize prematurely.

---

## What's next

**Step 2: restaurant detail pages.** This is the next workstream and the highest-leverage content step in the entire plan. The first half of step 2 is a design pass (URL pattern, page template, editorial scope, schema choice). The second half is page generation across all ~37 restaurants.

Before starting step 2, the next-session reader should:
1. Read `_strategy/HANDOFF.md` for the workflow norms.
2. Read `_strategy/CONTEXT.md` to understand why detail pages matter strategically (the flywheel hypothesis around restaurant-claimable badges).
3. Read `rankings/_template-canonical.html` so the detail-page template can echo the chrome of the ranking template.
4. Read `_strategy/DECISIONS.md` to understand the established design conventions (emoji-per-row, ShareTagline split, aggregateRating absent, etc.) before introducing new ones for detail pages.

---

## Where to find session artifacts

- `rankings/_template-canonical.html` — the canonical Top-5 ranking template (single source of truth for chrome)
- `rankings/_template-analysis.md` — analysis of the two design generations + harmonization plan + tracked items
- `rankings/_port-content-sheet.md` — content fields per page + step-3/step-4 port summary
- `_strategy/DECISIONS.md` — decisions log (12 non-obvious calls made during the harmonization)
- `_strategy/CONTEXT.md` — strategic context (brand positioning, monetization analysis, multi-city vision, deferred infrastructure)
- `_strategy/TRACKED.md` — centralized tracked items (one-offs, workstreams, deferred-to-later-steps)
- `_strategy/WORKFLOW.md` — meta-process: how Claude and operator collaborate (analyze-first cadence, working-files convention, session bootstrap, pushback norm, verification norm)
- `_strategy/HANDOFF.md` — one-page brief for the next session (read first)
