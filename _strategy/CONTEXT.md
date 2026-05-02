# Strategic context

This document captures the strategic frame around Voted On By Locals: brand positioning, vision, monetization paths and their trade-offs, deferred infrastructure that matters, and the "two forks ahead" framing for upcoming decisions.

The intent is to give a fresh reader (or a future Claude session) enough context to make decisions that are *consistent with the brand*, not just locally optimal for a given task. Local optimality without strategic context is how an editorial site gets ad units bolted on.

---

## Brand positioning

The site's About page positions the project explicitly: *"a simple, transparent list for us, free from ads and algorithms."* That sentence is the brand wedge. Yelp's reputation problem (paid placement, gamed reviews, manipulative ranking algorithms) plus Google's enshittification (AI-summarized travel content, sponsored results, scrambled local search) has created an obvious space for an antidote. "By locals for locals" is the trust premise; "voted on" is the methodology premise; "free from ads and algorithms" is the integrity premise.

**Tension:** That positioning makes ads, sponsored placements, and pay-to-play directly off-limits. Anything that smells like advertising erodes the brand wedge. The About page has explicitly committed the project to *not* doing this. So monetization, when it comes, has to come through paths that don't compromise the editorial position — which restricts the option set significantly. See "Three monetization paths" below.

**Implication for design decisions:** When a feature could be read as either editorial or commercial, defer to the editorial framing. Examples already enforced in this session:
- The bottom CTA reads "Disagree with this list? Cast your vote!" — community-energy framing, not subscription-driver framing.
- `aggregateRating` is intentionally absent from JSON-LD because fabricated rating numbers would be a form of credibility-purchase.
- Hardcoded vote totals were removed from the canonical because they implied a precision the data didn't have.

---

## Vision: multi-city expansion via ambassadors

The Ambassadors page exists today, but it's a contact form — not a system. The vision is a network of locally-led guides, each ambassador running their own city's rankings under the Voted On By Locals brand and getting some economic share of whatever monetization eventually lands.

**Current state:** Charleston-only. Every page has Charleston-specific copy ("Holy City"), Charleston in JSON-LD `addressLocality`, Charleston in page titles, Charleston in meta descriptions. Forms collect Charleston-area zip codes for verification. The brand voice is regionally specific (references to neighborhoods like Folly Beach, Park Circle, Harleston Village).

**What multi-city actually requires** (none of which exists yet):
- A content-templating decision: per-city subdomain (`charleston.votedonbylocals.com`)? path prefix (`votedonbylocals.com/charleston/best-pizza`)? region routing? CMS-style data layer feeding a single template? This is a fork-in-the-road decision that locks in a lot of downstream work.
- Per-city ambassador economics: revenue share, content rights, brand parity standards, exit terms, what happens if an ambassador goes silent.
- Per-city content quality control: when a Charleston ranking is edited by John, that's clearly editorial. When an Austin ambassador edits an Austin ranking, who validates it? What's the brand's quality standard?
- Operationally: a way to onboard, train, and offboard ambassadors. None of this is a problem to solve in step 2.

**Defer to:** post-step-7 strategic workstream, or split off as its own track once the Charleston foundation is solid.

---

## The flywheel hypothesis: restaurant-claimable winner badges → physical decals → free distribution

This is the single biggest unrealized growth lever the project has, and it's not built yet.

**The hypothesis:** When a restaurant wins a category (or just makes a Top-5), they want to show it off. Restaurants are deeply incentivized to broadcast third-party validation — "voted #1 by Charleston locals" is a credibility signal worth real money to them. If the project gives them an easy way to share that validation, they will, because it's in their direct self-interest.

**The artifacts:**
1. **Digital badge.** A small image (PNG or SVG) the restaurant can put on their own website, Instagram bio link, takeout menus, outgoing newsletters. Clicks through to the restaurant's detail page on the Voted On By Locals site.
2. **Physical decal/sticker.** A printed version the restaurant puts on their door, takeout window, business cards. Drives organic discovery — people walking past see the sticker, get curious about who Voted On By Locals is, look it up.
3. **Verified-claim status.** When a restaurant claims their listing, they get the badge, the sticker, and a verified mark on their detail page. (See monetization path B below — claim flow could be the verification subscription.)

**Why this is high-leverage:**
- Each badge a restaurant displays is free, durable distribution.
- Each click-through is a high-intent visitor (they already know about a specific restaurant; now they're learning about the platform).
- Each new visitor potentially becomes a voter.
- Each new voter feeds the next ranking refresh.
- The flywheel: votes → rankings → badges → distribution → new visitors → new voters.

**Why it isn't built yet:** Step 2 (restaurant detail pages) is a prerequisite. Each badge needs a "this restaurant" anchor URL, and detail pages don't exist yet. Once they do, the badge artifact is a small follow-up — a Figma design, an export pipeline, and a tiny "claim this listing" form. The strategic upside is large; the execution lift is small. **High priority for step 2's adjacent workstream.**

---

## Three monetization paths (and which compromise the brand)

> **This section is analysis, not a committed plan.** The three paths and their relative ordering are output from a strategic conversation, not decisions. The actual monetization decision moment is after step 2 of the master plan — once the restaurant detail pages exist and the badge/claim flow becomes designable, then the trade-offs below have concrete shapes to evaluate against. Until then, treat this as one frame for thinking, not the frame.

The site is explicitly ad-free per its positioning. Monetization has to come through paths that don't read as advertising. Three paths identified, ranked by brand-safety:

### (a) Newsletter / paid reader tier — *most brand-safe, smallest revenue ceiling*

**What it is:** Free tier gets the rankings as they're published. Paid tier gets early access to drafts, behind-the-scenes editorial notes, deeper context per restaurant, "the John list" of personal picks not on the official rankings, ambassador stories from other cities once those exist.

**Why it's brand-safe:** Pure editorial product. The reader is paying for *more editorial*, not for any change to the rankings or for rank order. The free tier remains a complete product (all rankings are free); the paid tier is additive.

**Compromise risk:** Almost none. The only failure mode is the paid tier ending up empty / not-worth-it, which damages the paid product but doesn't damage the brand.

**Implementation:** Existing platforms (Substack, Beehiiv, Ghost) handle this entirely. ~1 day of setup, ongoing editorial cadence is the ongoing cost.

### (b) Restaurant verification subscription — *medium brand-safe, medium revenue ceiling*

**What it is:** Restaurants pay a monthly fee to claim their listing on the site. Claiming gives them: ability to edit their tagline (within editorial guidelines), upload a photo, see analytics on their detail page (visits, click-throughs, share metrics), receive the digital badge + physical sticker (the flywheel from above).

**Why it's brand-safe-ish:** Editorial integrity (the ranking) is downstream of public votes, not subscriber money. Claiming the listing is metadata — which restaurant gets which photo, which URL the badge points to — and explicitly does NOT change rank order. The subscriber cannot pay to be #1.

**Compromise risk:** *Real but manageable.* Two failure modes:
1. **Perceived pay-to-play.** Even if the rankings stay editorial, the optics of restaurants paying anything to the site can erode trust if the relationship isn't communicated cleanly. Mitigation: explicit, prominent communication that ranks aren't affected by subscription status; visible "subscribed" markers that read as verification, not advertising; never adjust ranking algorithms in a way correlated with subscription.
2. **Editorial drift.** Over time, subscribed restaurants are more visible (their detail pages are richer, more photos, more verified data); unsubscribed ones look thinner. That's not pay-to-play in rank order, but it's pay-to-look-good. Probably acceptable; flag it.

**Implementation:** This is what the Step-2 detail pages enable. Pairs with the flywheel hypothesis above. Estimated ~3–6 weeks of work to build the claim flow, payment integration (Stripe), and the verification tooling.

### (c) Reservation affiliates (OpenTable / Resy / Yelp Reservations) — *least brand-safe, highest revenue ceiling*

**What it is:** When a user clicks through from a ranking or detail page to make a reservation at a featured restaurant, the site earns a referral fee from the reservation platform.

**Why it's brand-safe-ish:** Framed correctly, this is a service to readers — "book directly from this page" — not a paid placement decision. The link is downstream of editorial choice (the restaurant is on the list because it earned the votes; the reservation link is a convenience).

**Compromise risk:** *High.* Two specific concerns:
1. **Coverage bias.** Reservation platforms only cover restaurants on their network. If the site adds reservation CTAs only to restaurants that happen to be on OpenTable/Resy, those restaurants get richer detail pages, more visible CTAs, higher click-through. That subtly biases reader experience toward restaurants on those platforms — even if rankings stay editorial.
2. **Money-flow visibility.** Reservation affiliate links are a more visible commercial relationship than a verification subscription. Readers who notice "this site makes money when I click through to OpenTable" can mentally categorize the project as "a Yelp competitor monetizing the same way Yelp does." That's very close to the wedge that the brand exists to oppose.

**Implementation:** Mechanically simple — a few link-out CTAs on detail pages. Strategically the trickiest of the three.

### Suggested ordering

If/when monetization becomes a real workstream:
1. **Newsletter first.** Smallest revenue ceiling but also smallest brand risk and shortest time to first dollar. Tests whether readers will pay for editorial.
2. **Restaurant verification second.** Larger revenue ceiling, requires step 2 (detail pages) and the flywheel infrastructure. Use the newsletter learnings to inform pricing/positioning.
3. **Reservation affiliates last (or never).** Highest brand risk. Add only if newsletter + verification haven't met financial needs and only with strict editorial controls.

**What COMPROMISES the brand outright:** Display ads, sponsored rankings, pay-to-play visibility, "premium listing" tiers that affect rank order, sponsored "best of" categories, takeover units, "powered by [advertiser]" branding, AI-generated content. The About page positioning makes any of these reputationally expensive — adding them would be a strategic pivot, not an iteration.

---

## Things deferred but important

These are infrastructure-level concerns that the migration intentionally postponed but will need to be addressed before the project can operate at any meaningful scale.

- **Vote aggregation pipeline.** Currently votes go to Netlify Forms; rankings are hand-curated by the editor reading those submissions. There's no aggregate count, no per-restaurant "votes received" number, no "trending up this month" signal. The whole `aggregateRating` JSON-LD field is deferred on this. Any meaningful growth — more cities, more categories, more readers — will overwhelm hand-curation. Off the master plan; **strategic deferred** (see `_strategy/TRACKED.md`) — held until vote-driven features become active workstreams (claim flow, `aggregateRating`, visible vote totals). Building a real aggregation backend (Google Sheets / Airtable / a small JSON file the site reads via fetch) is probably ~1 week of work.

- **Fraud prevention.** Self-reported zip code is the only check on whether a voter is local. With any visible vote count, gameability gets significantly worse — a competing restaurant could easily ballot-stuff. Need at minimum: rate limiting, IP de-duplication, magic-link email verification for repeat voters, possibly a "social proof of locality" check (e.g., must verify with a Charleston-area phone number). Ties to the vote aggregation pipeline above.

- **Restaurant claim flow.** The flywheel hypothesis requires a way for restaurants to "claim this listing." Currently no plumbing — restaurants can email the project but there's no system. Pairs with monetization path (b) — claim flow is probably the verification subscription. ~2 weeks of work, contingent on step 2 detail pages.

- **Multi-city templating.** The site is hardcoded for Charleston everywhere — copy ("Holy City"), `addressLocality` in JSON-LD, page titles, neighborhood references in editorial. Adding a second city requires a content-templating decision that doesn't yet exist. Per-city subdomain vs path prefix vs CMS data layer is a fork-in-the-road that affects every subsequent piece of content. **This is the single biggest "unblocking" decision the project has — but it's also the easiest to defer until Charleston is a stronger foundation.**

- **OG image generation pipeline.** Step 5 of the master plan. Detail pages from step 2 will multiply the count significantly (~37 restaurant images on top of ~10 ranking images). Manual export from Figma is fine for the current scale; a pipeline matters at multi-city scale.

---

## "Two forks ahead" framing

After step 2 (restaurant detail pages), the project sits at a strategic fork. The fork doesn't need to be decided right now — step 2 itself is compatible with both directions — but recognizing the fork in advance helps make step-2 decisions that don't accidentally lock one direction in.

### Fork A: Editorial hobby

The site stays at hand-curated quality. Ranking refreshes happen when John feels like it. Detail pages are written editorially, one or a few at a time, when the editor has the energy. Monetization stays minimal (newsletter, maybe). No vote aggregation pipeline because hand-curation is fine at one-city scale. No claim flow because the flywheel isn't being chased. No multi-city because that's a different product.

This fork has a low operating cost, a high editorial ceiling (the writing can be excellent), a small audience ceiling, and a vanishing revenue ceiling. It's a good blog. It's the fork the brand currently most-resembles.

### Fork B: Business

The site builds the vote aggregation pipeline, the claim flow, the badge/sticker system, the multi-city templating. Adds monetization paths (b) and (a). Begins recruiting ambassadors. Treats the project as a startup rather than a hobby.

This fork has a much higher operating cost, requires either John or hired help to maintain, has a moderate editorial ceiling (the writing has to scale), a much larger audience ceiling, and a meaningful revenue ceiling.

### When the fork becomes real

**Step 2 itself is compatible with both forks.** Detail pages add value either way — they improve the editorial product (Fork A) AND they unlock the flywheel infrastructure (Fork B).

**Within the master plan, some steps have a fork-leaning character — but the leans are weak.** Killing the Tailwind CDN suggests scale-up infrastructure; sitemap/robots matter most when SEO is doing real work; schema cross-linking and OG images are fork-neutral and pay back under either fork. Every master-plan step has value regardless of fork. The actual fork-commitment moment isn't reached by executing the plan — it's reached when you start pulling strategically-deferred items (vote aggregation, claim flow, multi-city) into active work. That's the decision to make consciously, not "around step 5–6."

**For now:** make step 2 decisions in a way that's compatible with both forks. Use URL patterns that work whether or not multi-city happens. Use schema that's standard regardless of monetization. Write detail pages well enough to be hobby-quality and structured enough to be business-ready.
