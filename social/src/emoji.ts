import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const SOCIAL_ROOT = resolve(__dirname, '..');
const CACHE_DIR = resolve(SOCIAL_ROOT, '.emoji-cache');

const TWEMOJI_BASE =
  'https://cdn.jsdelivr.net/gh/twitter/twemoji@latest/assets/svg';

/**
 * Convert an emoji segment (one or more code points) to the Twemoji
 * filename convention: hyphen-joined hex code points with no leading
 * zeros. Variation selectors (U+FE0F) are stripped — Twemoji's bare
 * filenames omit them (e.g., ✈️ → "2708", not "2708-fe0f"). Surrogate
 * pairs are handled by `[...segment]` which iterates code points, not
 * code units. Regional-indicator sequences (flags) come through as
 * multiple code points joined with '-' (e.g., 🇺🇸 → "1f1fa-1f1f8").
 */
function toTwemojiCodepoint(segment: string): string {
  return [...segment]
    .map((c) => c.codePointAt(0))
    .filter((cp): cp is number => cp !== undefined && cp !== 0xfe0f)
    .map((cp) => cp.toString(16))
    .join('-');
}

async function fetchAndCache(codepoint: string, cachePath: string): Promise<string> {
  const url = `${TWEMOJI_BASE}/${codepoint}.svg`;
  const resp = await fetch(url);
  if (!resp.ok) {
    throw new Error(
      `Twemoji fetch failed for ${codepoint} (status ${resp.status}): ${url}`,
    );
  }
  const text = await resp.text();
  mkdirSync(CACHE_DIR, { recursive: true });
  writeFileSync(cachePath, text, 'utf-8');
  return text;
}

/**
 * Satori `loadAdditionalAsset` callback. Resolves emoji segments to
 * Twemoji SVG data URIs, served from a local cache that self-populates
 * on first miss via the jsdelivr CDN.
 *
 * For non-emoji codes (custom asset paths satori may emit in the
 * future), returns an empty string so satori falls through to its
 * default handling.
 */
export async function loadAdditionalAsset(
  code: string,
  segment: string,
): Promise<string> {
  if (code !== 'emoji') return '';

  const codepoint = toTwemojiCodepoint(segment);
  if (!codepoint) return '';

  const cachePath = resolve(CACHE_DIR, `${codepoint}.svg`);
  let svg: string;
  if (existsSync(cachePath)) {
    svg = readFileSync(cachePath, 'utf-8');
  } else {
    svg = await fetchAndCache(codepoint, cachePath);
  }

  const base64 = Buffer.from(svg, 'utf-8').toString('base64');
  return `data:image/svg+xml;base64,${base64}`;
}
