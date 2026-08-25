function envNum(key: string, fallback: number): number {
  const raw = process.env[key];
  if (raw === undefined || raw === '') return fallback;
  const n = Number(raw);
  if (Number.isNaN(n)) {
    throw new Error(`env ${key} is not a number: ${JSON.stringify(raw)}`);
  }
  return n;
}

function envStr(key: string, fallback: string): string {
  const raw = process.env[key];
  return raw === undefined || raw === '' ? fallback : raw;
}

export const DESIGN = {
  colors: {
    cream: envStr('DESIGN_COLORS_CREAM', '#FFF8F0'),
    orange: envStr('DESIGN_COLORS_ORANGE', '#E67E22'),
    dark: envStr('DESIGN_COLORS_DARK', '#2D3748'),
    gray: envStr('DESIGN_COLORS_GRAY', '#4A4A4A'),
    white: envStr('DESIGN_COLORS_WHITE', '#FFFFFF'),
  },
  fonts: {
    display: envStr('DESIGN_FONTS_DISPLAY', 'Poppins'),
    body: envStr('DESIGN_FONTS_BODY', 'DM Sans'),
  },
  card: {
    width: envNum('DESIGN_CARD_WIDTH', 1080),
    height: envNum('DESIGN_CARD_HEIGHT', 1350),
  },
  // Reels were retired 2026-08-25 (DECISIONS #24). This block is RETAINED and
  // INERT: composition.tsx destructures `reel` from DESIGN and its isReel
  // branches still reference these values, so removing it breaks typecheck.
  // Nothing reads it at runtime any more — render-card.ts never passes
  // mode: 'reel'. Do not 'clean this up' without also editing composition.tsx.
  reel: {
    width: envNum('DESIGN_REEL_WIDTH', 1080),
    height: envNum('DESIGN_REEL_HEIGHT', 1920),
    padTop: envNum('DESIGN_REEL_PADTOP', 285),
    padBottom: envNum('DESIGN_REEL_PADBOTTOM', 285),
  },
  zones: {
    headerH: envNum('DESIGN_ZONES_HEADERH', 100),
    heroH: envNum('DESIGN_ZONES_HEROH', 180),
    rowsH: envNum('DESIGN_ZONES_ROWSH', 980),
    footerH: envNum('DESIGN_ZONES_FOOTERH', 90),
  },
  row: {
    height: envNum('DESIGN_ROW_HEIGHT', 140),
    badgeSize: envNum('DESIGN_ROW_BADGESIZE', 80),
    namePx: envNum('DESIGN_ROW_NAMEPX', 36),
    taglinePx: envNum('DESIGN_ROW_TAGLINEPX', 20),
  },
};

export type Design = typeof DESIGN;
