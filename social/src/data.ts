import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const REPO_ROOT = resolve(__dirname, '..', '..');

export interface RankingRow {
  rank: number;
  name: string;
  tagline: string;
}

export interface Featured1Spot {
  name: string;
  neighborhood: string;
  emojis: string[];
  tagline: string;
  address: string;
  hours: string;
}

export interface TopNRankingData {
  layout: 'top-n';
  title: string;
  category: string;
  subtitle: string;
  rows: RankingRow[];
}

export interface Featured1RankingData {
  layout: 'featured-1';
  title: string;
  coloredWord: string;
  subtitle: string;
  emoji: string;
  featured: Featured1Spot;
}

export type RankingData = TopNRankingData | Featured1RankingData;

interface Restaurant {
  slug: string;
  name: string;
  tagline: string;
  neighborhood: string | null;
  hoursHumanReadable: string | null;
  address: {
    streetAddress: string | null;
    addressLocality: string | null;
    addressRegion: string | null;
    postalCode: string | null;
  };
  appearsOn?: { url: string; title: string }[];
}

interface OgRankingEntry {
  slug: string;
  category: string;
  spots: number;
}

interface ItemListEntry {
  position: number;
  item: { url: string };
}

interface JsonLdAny {
  '@context'?: string;
  '@type'?: string;
  name?: string;
  url?: string;
  itemListElement?: ItemListEntry[];
}

export function loadRankingData(slug: string): RankingData {
  const ogEntry = loadOgRankingEntry(slug);
  if (ogEntry.spots === 1) return loadFeatured1(slug, ogEntry);
  return loadTopN(slug, ogEntry);
}

function loadOgRankingEntry(slug: string): OgRankingEntry {
  const path = resolve(REPO_ROOT, 'data', 'og_rankings.json');
  const parsed = JSON.parse(readFileSync(path, 'utf-8')) as { rankings: OgRankingEntry[] };
  const entry = parsed.rankings.find((r) => r.slug === slug);
  if (!entry) {
    throw new Error(`Unknown ranking slug: ${slug} (no entry in data/og_rankings.json)`);
  }
  return entry;
}

function loadRankingHtml(slug: string): string {
  const rankingPath = resolve(REPO_ROOT, 'rankings', `${slug}.html`);
  try {
    return readFileSync(rankingPath, 'utf-8');
  } catch {
    throw new Error(`Ranking page not found: ${rankingPath}`);
  }
}

function loadRestaurants(): Restaurant[] {
  const path = resolve(REPO_ROOT, 'data', 'restaurants.json');
  return (JSON.parse(readFileSync(path, 'utf-8')) as { restaurants: Restaurant[] }).restaurants;
}

// ---------------------------------------------------------------------------
// Top-N path (existing behavior)
// ---------------------------------------------------------------------------

function loadTopN(slug: string, _ogEntry: OgRankingEntry): TopNRankingData {
  const html = loadRankingHtml(slug);
  const itemList = extractItemList(html);
  const urls: string[] = itemList.itemListElement.map((it: ItemListEntry) => it.item.url);

  const restaurants = loadRestaurants();
  const bySlug = new Map<string, Restaurant>(restaurants.map((r) => [r.slug, r]));

  // Per-ranking taglines come from the page's body rows, not restaurants.json.
  // For cross-listed restaurants (e.g. Home Team BBQ on best-burger AND
  // best-casual-spots), each ranking can carry its own descriptor.
  const taglinesBySlug = extractRowTaglines(html);

  const rows: RankingRow[] = urls.map((url, idx) => {
    const m = url.match(/\/restaurants\/([^/]+)\.html$/);
    if (!m) throw new Error(`Could not parse restaurant slug from URL: ${url}`);
    const restaurantSlug = m[1];
    const r = bySlug.get(restaurantSlug);
    if (!r) {
      throw new Error(
        `Restaurant '${restaurantSlug}' referenced from ranking ItemList is missing from data/restaurants.json`,
      );
    }
    const tagline = taglinesBySlug.get(restaurantSlug);
    if (tagline === undefined) {
      throw new Error(
        `Slug '${restaurantSlug}' appears in JSON-LD ItemList but no matching body row tagline was found in the ranking page (mismatch between ItemList and body rows)`,
      );
    }
    return { rank: idx + 1, name: r.name, tagline };
  });

  if (!slug.startsWith('best-')) {
    throw new Error(`Slug does not start with 'best-': ${slug}`);
  }
  const category = slug
    .slice('best-'.length)
    .split('-')
    .map(titleCase)
    .join(' ');

  const monthYearMatch = html.match(/Updated\s+([A-Z][a-z]+\s+\d{4})/);
  if (!monthYearMatch) {
    throw new Error('Could not extract "Updated {Month Year}" pill text from ranking page');
  }
  const monthYear = monthYearMatch[1];

  return {
    layout: 'top-n',
    title: `Best ${category}`,
    category,
    subtitle: `As voted by Charleston locals · ${monthYear}`,
    rows,
  };
}

// ---------------------------------------------------------------------------
// Featured-1 path
// ---------------------------------------------------------------------------

function loadFeatured1(slug: string, _ogEntry: OgRankingEntry): Featured1RankingData {
  const html = loadRankingHtml(slug);

  const featuredJsonLd = extractSingleEntityJsonLd(html);
  const restaurantName = featuredJsonLd.name;
  if (!restaurantName) {
    throw new Error(
      `Featured-1 page rankings/${slug}.html has a single-entity JSON-LD block but no name field`,
    );
  }

  // Resolve the featured restaurant from restaurants.json by appearsOn url.
  // The JSON-LD `url` on featured-1 pages points at the page itself
  // (DECISIONS #16), so we can't derive the restaurant slug from it.
  // appearsOn is the durable cross-link from data/restaurants.json back to
  // the ranking page; matching on it is robust to brand renames and
  // location-specific naming.
  const restaurants = loadRestaurants();
  const rankingRefUrl = `/rankings/${slug}.html`;
  const featuredRestaurant = restaurants.find((r) =>
    (r.appearsOn ?? []).some((a) => a.url === rankingRefUrl),
  );
  if (!featuredRestaurant) {
    throw new Error(
      `Featured-1 ranking ${slug} has no matching restaurant in data/restaurants.json (no entry with appearsOn url '${rankingRefUrl}')`,
    );
  }

  // Hero parts — extract from page body.
  const coloredWord = extractHeroColoredWord(html);
  const emoji = extractHeroEmoji(html);
  const subtitle = extractHeroSubtitle(html);

  // Per-restaurant emoji icon group — extract the bg-gray-100 spans inside
  // the featured card. Pattern stable across both featured-1 pages
  // (best-new-coffee-shop uses title=, best-bakery uses role=img + aria-label).
  const emojis = extractFeaturedEmojis(html);
  if (emojis.length === 0) {
    throw new Error(
      `Featured-1 page rankings/${slug}.html has no per-restaurant emoji icons (expected <span class="bg-gray-100 p-2 rounded-lg text-2xl">...)`,
    );
  }

  // Validate fields needed for the social card.
  if (!featuredRestaurant.neighborhood) {
    throw new Error(
      `Featured restaurant '${featuredRestaurant.slug}' has null neighborhood in data/restaurants.json — required for featured-1 social card`,
    );
  }
  if (!featuredRestaurant.address.streetAddress) {
    throw new Error(
      `Featured restaurant '${featuredRestaurant.slug}' has null address.streetAddress — required for featured-1 social card`,
    );
  }
  if (!featuredRestaurant.hoursHumanReadable) {
    throw new Error(
      `Featured restaurant '${featuredRestaurant.slug}' has null hoursHumanReadable — required for featured-1 social card`,
    );
  }

  return {
    layout: 'featured-1',
    title: `Best ${coloredWord}`,
    coloredWord,
    subtitle,
    emoji,
    featured: {
      name: featuredRestaurant.name,
      neighborhood: featuredRestaurant.neighborhood,
      emojis,
      tagline: featuredRestaurant.tagline,
      address: featuredRestaurant.address.streetAddress,
      hours: featuredRestaurant.hoursHumanReadable,
    },
  };
}

// ---------------------------------------------------------------------------
// HTML / JSON-LD extraction
// ---------------------------------------------------------------------------

function extractRowTaglines(html: string): Map<string, string> {
  // Each row in the ranking page body has the shape:
  //   <a href="/restaurants/{slug}.html" class="hover:text-brand-orange ...">{Name}</a></h2>
  //       <p class="text-brand-gray font-medium ...">{tagline}</p>
  // Non-greedy `[\s\S]*?` between the anchor and the first text-brand-gray <p>
  // catches the row's tagline without crossing into the next row.
  const re = /<a href="\/restaurants\/([^"]+)\.html"[^>]*>[^<]+<\/a>[\s\S]*?<p class="text-brand-gray[^"]*">([^<]+)<\/p>/g;
  const map = new Map<string, string>();
  for (const m of html.matchAll(re)) {
    map.set(m[1], m[2].trim());
  }
  return map;
}

function extractItemList(html: string): { itemListElement: ItemListEntry[] } {
  for (const block of iterateJsonLdBlocks(html)) {
    if (block['@type'] === 'ItemList' && Array.isArray(block.itemListElement)) {
      return { itemListElement: block.itemListElement };
    }
  }
  throw new Error('No ItemList JSON-LD block found in ranking page');
}

function extractSingleEntityJsonLd(html: string): JsonLdAny {
  // Featured-1 ranking pages carry a single Restaurant-class entity
  // (Bakery, CafeOrCoffeeShop, BarOrPub, NightClub, FoodEstablishment,
  // Restaurant). Anything that's not BreadcrumbList AND has a name field
  // qualifies — keeps this resilient to future per-page @type additions
  // (per DECISIONS #5's per-page schemaType convention).
  const candidates: JsonLdAny[] = [];
  for (const block of iterateJsonLdBlocks(html)) {
    if (block['@type'] === 'BreadcrumbList') continue;
    if (block['@type'] === 'ItemList') continue;
    if (typeof block.name !== 'string') continue;
    candidates.push(block);
  }
  if (candidates.length === 0) {
    throw new Error(
      'No single Restaurant-class JSON-LD entity found in featured-1 ranking page (expected one with @type Bakery / CafeOrCoffeeShop / etc. and a name field)',
    );
  }
  if (candidates.length > 1) {
    throw new Error(
      `Expected exactly one single-entity JSON-LD block on featured-1 ranking page, found ${candidates.length}`,
    );
  }
  return candidates[0];
}

function* iterateJsonLdBlocks(html: string): Generator<JsonLdAny> {
  const re = /<script type="application\/ld\+json">([\s\S]*?)<\/script>/g;
  for (const match of html.matchAll(re)) {
    try {
      yield JSON.parse(match[1]) as JsonLdAny;
    } catch {
      // skip non-JSON or malformed blocks
    }
  }
}

function extractHeroColoredWord(html: string): string {
  // Featured-1 hero h1 shape:
  //   <h1 ...>Best <span class="text-brand-orange">Bakery</span> 🥐</h1>
  //   <h1 ...>Best New <span class="text-brand-orange">Coffee Shop</span> ☕</h1>
  // Capture the orange-span content.
  const m = html.match(/<h1[^>]*>[\s\S]*?<span class="text-brand-orange">([^<]+)<\/span>[\s\S]*?<\/h1>/);
  if (!m) {
    throw new Error('Featured-1 hero h1 colored word not found (expected <span class="text-brand-orange">...)');
  }
  return m[1].trim();
}

function extractHeroEmoji(html: string): string {
  // Capture the trailing token after the colored span and before </h1>.
  const m = html.match(/<h1[^>]*>[\s\S]*?<\/span>\s*(\S+)\s*<\/h1>/);
  if (!m) {
    throw new Error('Featured-1 hero emoji not found (expected emoji after </span> and before </h1>)');
  }
  return m[1].trim();
}

function extractHeroSubtitle(html: string): string {
  // Featured-1 hero subtitle is the first <p class="text-brand-gray ...">
  // after the h1 close.
  const heroIdx = html.search(/<\/h1>/);
  if (heroIdx === -1) {
    throw new Error('Featured-1 hero h1 closing tag not found');
  }
  const tail = html.slice(heroIdx);
  const m = tail.match(/<p class="text-brand-gray[^"]*">([^<]+)<\/p>/);
  if (!m) {
    throw new Error('Featured-1 hero subtitle <p> not found after h1');
  }
  return m[1].trim();
}

function extractFeaturedEmojis(html: string): string[] {
  // Per-restaurant icon group:
  //   <span class="bg-gray-100 p-2 rounded-lg text-2xl" ...>🥐</span>
  // Both featured-1 page variants (title= or role/aria-label) use the same
  // class string for the icon spans.
  const re = /<span class="bg-gray-100 p-2 rounded-lg text-2xl"[^>]*>([^<]+)<\/span>/g;
  const out: string[] = [];
  for (const m of html.matchAll(re)) {
    out.push(m[1].trim());
  }
  return out;
}

function titleCase(s: string): string {
  if (s.length === 0) return s;
  return s[0].toUpperCase() + s.slice(1).toLowerCase();
}
