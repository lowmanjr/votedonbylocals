import React from 'react';
import { DESIGN } from './design.js';
import type {
  Featured1RankingData,
  RankingData,
  TopNRankingData,
} from './data.js';

export interface RowState {
  opacity: number;
  yOffset: number;
}

export interface Featured1State {
  bodyOpacity: number;
  bodyOffset: number;
}

export interface CompositionProps {
  data: RankingData;
  mode: 'card' | 'reel';
  rowStates?: RowState[];
  featured1State?: Featured1State;
}

export function Composition({
  data,
  mode,
  rowStates,
  featured1State,
}: CompositionProps): React.ReactElement {
  if (data.layout === 'featured-1') {
    return <Featured1Layout data={data} mode={mode} state={featured1State} />;
  }
  return <TopNLayout data={data} mode={mode} rowStates={rowStates} />;
}

// ---------------------------------------------------------------------------
// Top-N layout (existing composition, refactored — no behavior change)
// ---------------------------------------------------------------------------

function TopNLayout({
  data,
  mode,
  rowStates,
}: {
  data: TopNRankingData;
  mode: 'card' | 'reel';
  rowStates?: RowState[];
}): React.ReactElement {
  const { colors, fonts, card, reel, zones, row } = DESIGN;
  const isReel = mode === 'reel';

  // Reel mode pulls horizontal margins in to the universal cross-platform
  // safe zone (900-wide content band centered in the 1080-wide canvas, x∈
  // [90, 990]). Card mode keeps the original 40px IG-feed margins. Same
  // discriminator pattern Featured1Layout uses below.
  const sidePad = isReel ? REEL_SAFE_SIDE_PAD : 40;

  const effectiveRowStates: RowState[] = data.rows.map((_, i) => {
    if (isReel && rowStates && rowStates[i]) return rowStates[i];
    return { opacity: 1, yOffset: 0 };
  });

  const cardEl = (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        width: card.width,
        height: card.height,
        backgroundColor: colors.cream,
      }}
    >
      <div
        style={{
          display: 'flex',
          height: zones.headerH,
          alignItems: 'center',
          justifyContent: 'space-between',
          paddingLeft: sidePad,
          paddingRight: sidePad,
        }}
      >
        <div
          style={{
            fontFamily: fonts.display,
            fontWeight: 600,
            fontSize: 16,
            color: colors.dark,
            letterSpacing: '0.1em',
          }}
        >
          VOTED ON BY LOCALS
        </div>
        <div
          style={{
            fontFamily: fonts.display,
            fontWeight: 600,
            fontSize: 16,
            color: colors.dark,
            letterSpacing: '0.1em',
          }}
        >
          CHARLESTON
        </div>
      </div>

      {/*
        CONTENT GROUP: hero + rows composed as one unit and centred together
        between the pinned header and footer. Previously hero and rows were
        siblings with fixed heights, so at low row counts the rows centred
        inside a tall rows zone while the hero stayed pinned directly under
        the header — stranding it above a floating row block. Grouping them
        moves the slack OUTSIDE the content instead of between its two halves.

        Height is heroH + rowsH so the group still spans exactly the space the
        two zones used to occupy; header and footer pinning is unchanged.
      */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          height: zones.heroH + zones.rowsH,
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: zones.heroH,
          }}
        >
          <div
            style={{
              display: 'flex',
              fontFamily: fonts.display,
              fontWeight: 800,
              fontSize: 80,
              lineHeight: 1.0,
            }}
          >
            <span style={{ color: colors.dark }}>Best&nbsp;</span>
            <span style={{ color: colors.orange }}>{data.category}</span>
          </div>
          <div
            style={{
              fontFamily: fonts.body,
              fontWeight: 500,
              fontSize: 22,
              color: colors.gray,
              marginTop: 12,
            }}
          >
            {data.subtitle}
          </div>
        </div>

        {/*
          Rows are now CONTENT-SIZED, not zone-sized. The former
          `height: zones.rowsH` plus `justifyContent: 'center'` (added by PR #37
          for small-N centring) is superseded: with the group centring the hero
          and rows together, centring rows inside their own box would have
          nothing left to centre. HERO_ROWS_GAP replaces the slack that used to
          separate them by accident.
        */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            marginTop: HERO_ROWS_GAP,
          }}
        >
          {data.rows.map((r, i) => {
            const state = effectiveRowStates[i];
            return (
              <div
                key={i}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  height: row.height,
                  opacity: state.opacity,
                  transform: `translateY(${state.yOffset}px)`,
                  borderTop: i === 0 ? '1px solid transparent' : `1px solid ${hexAlpha(colors.gray, 0.15)}`,
                  paddingLeft: sidePad,
                  paddingRight: sidePad,
                }}
              >
                <div
                  style={{
                    display: 'flex',
                    width: row.badgeSize,
                    height: row.badgeSize,
                    borderRadius: row.badgeSize / 2,
                    backgroundColor: colors.orange,
                    color: colors.white,
                    fontFamily: fonts.display,
                    fontWeight: 700,
                    fontSize: 36,
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                  }}
                >
                  {r.rank}
                </div>
                <div style={{ width: 30, flexShrink: 0 }} />
                <div
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    flex: 1,
                  }}
                >
                  <div
                    style={{
                      fontFamily: fonts.display,
                      fontWeight: 700,
                      fontSize: row.namePx,
                      color: colors.dark,
                      lineHeight: 1.1,
                    }}
                  >
                    {r.name}
                  </div>
                  <div
                    style={{
                      fontFamily: fonts.body,
                      fontWeight: 400,
                      fontSize: row.taglinePx,
                      color: colors.gray,
                      marginTop: 4,
                      lineHeight: 1.2,
                    }}
                  >
                    {r.tagline}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div
        style={{
          display: 'flex',
          height: zones.footerH,
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <div
          style={{
            fontFamily: fonts.display,
            fontWeight: 600,
            fontSize: 18,
            color: colors.orange,
          }}
        >
          votedonbylocals.com
        </div>
      </div>
    </div>
  );

  if (!isReel) return cardEl;

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        width: reel.width,
        height: reel.height,
        backgroundColor: colors.cream,
      }}
    >
      <div style={{ display: 'flex', height: reel.padTop }} />
      {cardEl}
      <div style={{ display: 'flex', height: reel.padBottom }} />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Featured-1 layout
// ---------------------------------------------------------------------------

// Featured-1 carries its own zone model, independent of DESIGN.zones, and its
// root height is the SUM of these four rather than DESIGN.card.height. `body` is
// now DERIVED so that sum always equals card.height for any card.height.
//
// It was a literal 960, which happened to equal 1350 - 100 - 200 - 90. That
// coincidence hid the coupling: raising card.height left featured-1 content at
// 1350 inside a taller canvas, showing a band of un-painted background below the
// footer. header / hero / footer are content-sized and do not scale.
const FEATURED1_CARD_HEADER = 100;
const FEATURED1_CARD_HERO = 200;
const FEATURED1_CARD_FOOTER = 90;
const FEATURED1_CARD_ZONES = {
  header: FEATURED1_CARD_HEADER,
  hero: FEATURED1_CARD_HERO,
  body:
    DESIGN.card.height -
    FEATURED1_CARD_HEADER -
    FEATURED1_CARD_HERO -
    FEATURED1_CARD_FOOTER,
  footer: FEATURED1_CARD_FOOTER,
};
const FEATURED1_REEL_ZONES = { header: 90, hero: 180, body: 1050, footer: 80 };
// Universal cross-platform safe zone for 1080×1920 reels: 900×1400 centered.
// Top pad 260 + content 1400 + bottom pad 260 = 1920.
// Gap between the hero block and the first row inside the content group.
// Before grouping, this space was whatever slack the rows zone happened to
// leave: 0 at 7 rows / 1350, 45 at 7 rows / 1440, 325 at 3 rows / 1440. It is
// now an explicit margin, constant at every row count.
const HERO_ROWS_GAP = 40;

const REEL_SAFE_TOP_PAD = 260;
const REEL_SAFE_BOTTOM_PAD = 260;
const REEL_SAFE_SIDE_PAD = 90; // 1080 - 900 = 180, /2 = 90

function Featured1Layout({
  data,
  mode,
  state,
}: {
  data: Featured1RankingData;
  mode: 'card' | 'reel';
  state: Featured1State | undefined;
}): React.ReactElement {
  const { colors } = DESIGN;
  const isReel = mode === 'reel';
  const zones = isReel ? FEATURED1_REEL_ZONES : FEATURED1_CARD_ZONES;

  // Reel-mode body opacity / offset come from the timing module via state.
  // Card mode is always fully revealed.
  const bodyOpacity = isReel && state ? state.bodyOpacity : 1;
  const bodyOffset = isReel && state ? state.bodyOffset : 0;

  // The composition's "card body" (the four zones) is identical in shape
  // between card and reel — only zone heights and side padding differ.
  // Reel mode wraps it in cream pad above + below to land in the universal
  // cross-platform safe zone.
  const sidePad = isReel ? REEL_SAFE_SIDE_PAD : 40;

  const composedBody = (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        width: isReel ? 1080 : 1080,
        height: zones.header + zones.hero + zones.body + zones.footer,
        backgroundColor: colors.cream,
      }}
    >
      <Featured1Header sidePad={sidePad} height={zones.header} />
      <Featured1Hero data={data} height={zones.hero} sidePad={sidePad} />
      <Featured1Body
        data={data}
        height={zones.body}
        sidePad={sidePad}
        opacity={bodyOpacity}
        offset={bodyOffset}
      />
      <Featured1Footer height={zones.footer} />
    </div>
  );

  if (!isReel) return composedBody;

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        width: 1080,
        height: 1920,
        backgroundColor: colors.cream,
      }}
    >
      <div style={{ display: 'flex', height: REEL_SAFE_TOP_PAD }} />
      {composedBody}
      <div style={{ display: 'flex', height: REEL_SAFE_BOTTOM_PAD }} />
    </div>
  );
}

function Featured1Header({
  sidePad,
  height,
}: {
  sidePad: number;
  height: number;
}): React.ReactElement {
  const { colors, fonts } = DESIGN;
  return (
    <div
      style={{
        display: 'flex',
        height,
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: sidePad,
        paddingRight: sidePad,
      }}
    >
      <div
        style={{
          fontFamily: fonts.display,
          fontWeight: 600,
          fontSize: 16,
          color: colors.dark,
          letterSpacing: '0.1em',
        }}
      >
        VOTED ON BY LOCALS
      </div>
      <div
        style={{
          fontFamily: fonts.display,
          fontWeight: 600,
          fontSize: 16,
          color: colors.dark,
          letterSpacing: '0.1em',
        }}
      >
        CHARLESTON
      </div>
    </div>
  );
}

function Featured1Hero({
  data,
  height,
  sidePad,
}: {
  data: Featured1RankingData;
  height: number;
  sidePad: number;
}): React.ReactElement {
  const { colors, fonts } = DESIGN;
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height,
        paddingLeft: sidePad,
        paddingRight: sidePad,
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          fontFamily: fonts.display,
          fontWeight: 800,
          fontSize: 80,
          lineHeight: 1.0,
        }}
      >
        <span style={{ color: colors.dark }}>Best&nbsp;</span>
        <span style={{ color: colors.orange }}>{data.coloredWord}</span>
        <span style={{ marginLeft: 18 }}>{data.emoji}</span>
      </div>
      <div
        style={{
          fontFamily: fonts.body,
          fontWeight: 500,
          fontSize: 22,
          color: colors.gray,
          marginTop: 14,
          textAlign: 'center',
        }}
      >
        {data.subtitle}
      </div>
    </div>
  );
}

function Featured1Body({
  data,
  height,
  sidePad,
  opacity,
  offset,
}: {
  data: Featured1RankingData;
  height: number;
  sidePad: number;
  opacity: number;
  offset: number;
}): React.ReactElement {
  const { colors, fonts } = DESIGN;
  const { featured } = data;

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        height,
        paddingTop: 100,
        paddingLeft: sidePad,
        paddingRight: sidePad,
        opacity,
        transform: `translateY(${offset}px)`,
      }}
    >
      <div
        style={{
          display: 'flex',
          backgroundColor: colors.orange,
          color: colors.white,
          fontFamily: fonts.display,
          fontWeight: 700,
          fontSize: 18,
          paddingTop: 12,
          paddingBottom: 12,
          paddingLeft: 28,
          paddingRight: 28,
          borderRadius: 9999,
          letterSpacing: '0.05em',
        }}
      >
        #1 Voted by Locals
      </div>

      <div style={{ display: 'flex', height: 90 }} />

      <div
        style={{
          display: 'flex',
          fontSize: 96,
          lineHeight: 1.0,
        }}
      >
        {featured.emojis.join(' ')}
      </div>

      <div style={{ display: 'flex', height: 50 }} />

      <div
        style={{
          display: 'flex',
          fontFamily: fonts.display,
          fontWeight: 800,
          fontSize: 72,
          color: colors.dark,
          lineHeight: 1.0,
          textAlign: 'center',
        }}
      >
        {featured.name}
      </div>

      <div
        style={{
          display: 'flex',
          fontFamily: fonts.body,
          fontWeight: 500,
          fontSize: 28,
          color: colors.gray,
          marginTop: 8,
        }}
      >
        {featured.neighborhood}
      </div>

      <div style={{ display: 'flex', height: 80 }} />

      <div
        style={{
          display: 'flex',
          fontFamily: fonts.body,
          fontWeight: 600,
          fontSize: 32,
          color: colors.dark,
          textAlign: 'center',
        }}
      >
        {featured.tagline}
      </div>

      <div style={{ display: 'flex', height: 40 }} />

      <div
        style={{
          display: 'flex',
          fontFamily: fonts.body,
          fontWeight: 400,
          fontSize: 22,
          color: colors.gray,
          textAlign: 'center',
        }}
      >
        {featured.address} · {featured.hours}
      </div>
    </div>
  );
}

function Featured1Footer({ height }: { height: number }): React.ReactElement {
  const { colors, fonts } = DESIGN;
  return (
    <div
      style={{
        display: 'flex',
        height,
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div
        style={{
          fontFamily: fonts.display,
          fontWeight: 600,
          fontSize: 18,
          color: colors.orange,
        }}
      >
        votedonbylocals.com
      </div>
    </div>
  );
}

function hexAlpha(hex: string, alpha: number): string {
  const m = hex.match(/^#([0-9a-fA-F]{6})$/);
  if (!m) return hex;
  const n = parseInt(m[1], 16);
  const r = (n >> 16) & 0xff;
  const g = (n >> 8) & 0xff;
  const b = n & 0xff;
  return `rgba(${r},${g},${b},${alpha})`;
}
