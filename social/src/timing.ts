import { DESIGN } from './design.js';

export const TOTAL_FRAMES = Math.round(
  DESIGN.anim.totalDurationS * DESIGN.anim.fps,
);

function clamp01(t: number): number {
  return Math.max(0, Math.min(1, t));
}

export function easeOutCubic(t: number): number {
  return 1 - Math.pow(1 - clamp01(t), 3);
}

function rowProgress(frame: number, rowIndex: number): number {
  const startS = DESIGN.anim.firstRevealS + rowIndex * DESIGN.anim.staggerS;
  const durS = DESIGN.anim.rowDurationS;
  const t = (frame / DESIGN.anim.fps - startS) / durS;
  return clamp01(t);
}

export function rowOpacityAtFrame(frame: number, rowIndex: number): number {
  return easeOutCubic(rowProgress(frame, rowIndex));
}

export function rowOffsetAtFrame(frame: number, rowIndex: number): number {
  const eased = easeOutCubic(rowProgress(frame, rowIndex));
  return DESIGN.anim.yOffsetPx * (1 - eased);
}
