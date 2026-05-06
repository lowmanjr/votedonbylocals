import React from 'react';
import { DESIGN } from './design.js';
import type { RankingData } from './data.js';

export interface RowState {
  opacity: number;
  yOffset: number;
}

export interface CompositionProps {
  data: RankingData;
  mode: 'static' | 'reel';
  rowStates?: RowState[];
}

export function Composition({ data, mode, rowStates }: CompositionProps): React.ReactElement {
  // Featured-1 layout support arrives in the next commit (Featured1Layout).
  // For now, narrow to top-n so the data.ts discriminated-union refactor
  // typechecks without duplicating composition logic prematurely.
  if (data.layout !== 'top-n') {
    throw new Error(
      `Composition layout '${data.layout}' not yet supported — Featured1Layout lands in the next commit`,
    );
  }

  const { colors, fonts, card, reel, zones, row } = DESIGN;
  const isReel = mode === 'reel';

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
          paddingLeft: 40,
          paddingRight: 40,
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

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          height: zones.rowsH,
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
                paddingLeft: 40,
                paddingRight: 40,
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

function hexAlpha(hex: string, alpha: number): string {
  const m = hex.match(/^#([0-9a-fA-F]{6})$/);
  if (!m) return hex;
  const n = parseInt(m[1], 16);
  const r = (n >> 16) & 0xff;
  const g = (n >> 8) & 0xff;
  const b = n & 0xff;
  return `rgba(${r},${g},${b},${alpha})`;
}
