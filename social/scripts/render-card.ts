import { mkdirSync, statSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';
import React from 'react';
import satori from 'satori';
import { Composition } from '../src/composition.js';
import { loadRankingData } from '../src/data.js';
import { DESIGN } from '../src/design.js';
import { loadAdditionalAsset } from '../src/emoji.js';
import { loadFonts } from '../src/fonts.js';

function parseSlug(): string {
  const args = process.argv.slice(2);
  const idx = args.indexOf('--slug');
  if (idx === -1 || idx === args.length - 1) {
    throw new Error('Missing required argument: --slug <ranking-slug>');
  }
  return args[idx + 1];
}

function readPngDims(buf: Uint8Array): { width: number; height: number } {
  const view = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  return {
    width: view.getUint32(16),
    height: view.getUint32(20),
  };
}

async function main(): Promise<void> {
  const slug = parseSlug();
  const data = loadRankingData(slug);
  const fonts = await loadFonts();

  const __dirname = fileURLToPath(new URL('.', import.meta.url));
  const SOCIAL_ROOT = resolve(__dirname, '..');
  const REPO_ROOT = resolve(SOCIAL_ROOT, '..');
  const outDir = resolve(REPO_ROOT, 'social-assets', slug);
  const outPath = resolve(outDir, 'card.png');

  const element = React.createElement(Composition, { data, mode: 'card' as const });
  const svg = await satori(element, {
    width: DESIGN.card.width,
    height: DESIGN.card.height,
    fonts,
    loadAdditionalAsset,
  });

  const png = new Resvg(svg, {
    fitTo: { mode: 'width', value: DESIGN.card.width },
  })
    .render()
    .asPng();

  mkdirSync(outDir, { recursive: true });
  writeFileSync(outPath, png);

  const size = statSync(outPath).size;
  if (size < 30_000 || size > 5_000_000) {
    throw new Error(
      `Output size ${size} bytes outside expected band 30,000–5,000,000`,
    );
  }

  const dims = readPngDims(png);
  if (dims.width !== DESIGN.card.width || dims.height !== DESIGN.card.height) {
    throw new Error(
      `Output dimensions ${dims.width}×${dims.height} != expected ${DESIGN.card.width}×${DESIGN.card.height}`,
    );
  }

  console.log(
    `wrote ${outPath} (${(size / 1024).toFixed(1)}KB, ${dims.width}×${dims.height})`,
  );
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
