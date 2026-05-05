import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

type SatoriWeight = 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900;

interface SatoriFont {
  name: string;
  data: Buffer;
  weight: SatoriWeight;
  style: 'normal' | 'italic';
}

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const SOCIAL_ROOT = resolve(__dirname, '..');

interface FontSpec {
  name: string;
  weight: SatoriWeight;
  packagePath: string;
}

const FONT_SPECS: FontSpec[] = [
  { name: 'Poppins', weight: 400, packagePath: '@fontsource/poppins/files/poppins-latin-400-normal.woff' },
  { name: 'Poppins', weight: 600, packagePath: '@fontsource/poppins/files/poppins-latin-600-normal.woff' },
  { name: 'Poppins', weight: 700, packagePath: '@fontsource/poppins/files/poppins-latin-700-normal.woff' },
  { name: 'Poppins', weight: 800, packagePath: '@fontsource/poppins/files/poppins-latin-800-normal.woff' },
  { name: 'DM Sans', weight: 400, packagePath: '@fontsource/dm-sans/files/dm-sans-latin-400-normal.woff' },
  { name: 'DM Sans', weight: 500, packagePath: '@fontsource/dm-sans/files/dm-sans-latin-500-normal.woff' },
  { name: 'DM Sans', weight: 700, packagePath: '@fontsource/dm-sans/files/dm-sans-latin-700-normal.woff' },
];

export async function loadFonts(): Promise<SatoriFont[]> {
  return FONT_SPECS.map((spec) => {
    const filePath = resolve(SOCIAL_ROOT, 'node_modules', spec.packagePath);
    return {
      name: spec.name,
      data: readFileSync(filePath),
      weight: spec.weight,
      style: 'normal' as const,
    };
  });
}
