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

export interface RankingData {
  title: string;
  category: string;
  subtitle: string;
  rows: RankingRow[];
}

interface Restaurant {
  slug: string;
  name: string;
  tagline: string;
}

interface ItemListEntry {
  position: number;
  item: { url: string };
}

export function loadRankingData(slug: string): RankingData {
  const rankingPath = resolve(REPO_ROOT, 'rankings', `${slug}.html`);
  let html: string;
  try {
    html = readFileSync(rankingPath, 'utf-8');
  } catch {
    throw new Error(`Ranking page not found: ${rankingPath}`);
  }

  const itemList = extractItemList(html);
  const urls: string[] = itemList.itemListElement.map((it: ItemListEntry) => it.item.url);

  const restaurantsPath = resolve(REPO_ROOT, 'data', 'restaurants.json');
  const restaurants: Restaurant[] = JSON.parse(
    readFileSync(restaurantsPath, 'utf-8'),
  ).restaurants;
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
    title: `Best ${category}`,
    category,
    subtitle: `As voted by Charleston locals · ${monthYear}`,
    rows,
  };
}

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
  const re = /<script type="application\/ld\+json">([\s\S]*?)<\/script>/g;
  for (const match of html.matchAll(re)) {
    try {
      const parsed = JSON.parse(match[1]);
      if (parsed && parsed['@type'] === 'ItemList') return parsed;
    } catch {
      // skip non-JSON or non-matching blocks
    }
  }
  throw new Error('No ItemList JSON-LD block found in ranking page');
}

function titleCase(s: string): string {
  if (s.length === 0) return s;
  return s[0].toUpperCase() + s.slice(1).toLowerCase();
}
