import { spawn } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';
import React from 'react';
import satori from 'satori';
import { Composition } from '../src/composition.js';
import type { Featured1State, RowState } from '../src/composition.js';
import { loadRankingData } from '../src/data.js';
import { DESIGN } from '../src/design.js';
import { loadAdditionalAsset } from '../src/emoji.js';
import { loadFonts } from '../src/fonts.js';
import {
  TOTAL_FRAMES,
  featured1OffsetAtFrame,
  featured1OpacityAtFrame,
  rowOffsetAtFrame,
  rowOpacityAtFrame,
} from '../src/timing.js';

interface ProcessResult {
  exitCode: number;
  stdout: string;
  stderr: string;
}

function parseSlug(): string {
  const args = process.argv.slice(2);
  const idx = args.indexOf('--slug');
  if (idx === -1 || idx === args.length - 1) {
    throw new Error('Missing required argument: --slug <ranking-slug>');
  }
  return args[idx + 1];
}

function runProcess(cmd: string, args: string[]): Promise<ProcessResult> {
  return new Promise((resolveFn, rejectFn) => {
    const child = spawn(cmd, args);
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (chunk: Buffer) => {
      stdout += chunk.toString();
    });
    child.stderr.on('data', (chunk: Buffer) => {
      stderr += chunk.toString();
    });
    child.on('error', rejectFn);
    child.on('close', (code) => {
      resolveFn({ exitCode: code ?? -1, stdout, stderr });
    });
  });
}

interface FfprobeStream {
  codec_type: string;
  codec_name?: string;
  width?: number;
  height?: number;
  pix_fmt?: string;
  nb_frames?: string;
}

interface FfprobeFormat {
  duration?: string;
}

interface FfprobeOutput {
  streams: FfprobeStream[];
  format: FfprobeFormat;
}

async function main(): Promise<void> {
  const slug = parseSlug();
  console.log(`Loading ranking data: ${slug}`);
  const data = loadRankingData(slug);
  console.log(`Layout: ${data.layout}`);

  console.log(`Loading fonts...`);
  const fonts = await loadFonts();

  const __dirname = fileURLToPath(new URL('.', import.meta.url));
  const SOCIAL_ROOT = resolve(__dirname, '..');
  const REPO_ROOT = resolve(SOCIAL_ROOT, '..');
  const outDir = resolve(REPO_ROOT, 'social-assets', slug);
  const outPath = resolve(outDir, 'reel.mp4');
  mkdirSync(outDir, { recursive: true });

  const tmpDir = mkdtempSync(join(tmpdir(), 'reel-'));
  console.log(`Temp dir: ${tmpDir}`);

  const overallStart = Date.now();

  try {
    console.log(`Rendering ${TOTAL_FRAMES} frames at ${DESIGN.reel.width}x${DESIGN.reel.height}...`);
    const renderStart = Date.now();

    for (let frame = 0; frame < TOTAL_FRAMES; frame++) {
      // Per-layout state composition. Top-n uses one RowState per body
      // row (existing per-row stagger animation); featured-1 uses one
      // Featured1State for the whole featured-spot zone (single coordinated
      // reveal — see DESIGN.featured1Anim).
      let element: React.ReactElement;
      if (data.layout === 'top-n') {
        const rowStates: RowState[] = data.rows.map((_, i) => ({
          opacity: rowOpacityAtFrame(frame, i),
          yOffset: rowOffsetAtFrame(frame, i),
        }));
        element = React.createElement(Composition, {
          data,
          mode: 'reel' as const,
          rowStates,
        });
      } else {
        const featured1State: Featured1State = {
          bodyOpacity: featured1OpacityAtFrame(frame),
          bodyOffset: featured1OffsetAtFrame(frame),
        };
        element = React.createElement(Composition, {
          data,
          mode: 'reel' as const,
          featured1State,
        });
      }

      const svg = await satori(element, {
        width: DESIGN.reel.width,
        height: DESIGN.reel.height,
        fonts,
        loadAdditionalAsset,
      });

      const png = new Resvg(svg, {
        fitTo: { mode: 'width', value: DESIGN.reel.width },
      })
        .render()
        .asPng();

      const framePath = join(
        tmpDir,
        `frame-${String(frame).padStart(4, '0')}.png`,
      );
      writeFileSync(framePath, png);

      if ((frame + 1) % 30 === 0 || frame === TOTAL_FRAMES - 1) {
        const elapsed = (Date.now() - renderStart) / 1000;
        const perFrame = elapsed / (frame + 1);
        const remaining = perFrame * (TOTAL_FRAMES - 1 - frame);
        console.log(
          `  frame ${frame + 1}/${TOTAL_FRAMES} (${elapsed.toFixed(1)}s elapsed, ${perFrame.toFixed(2)}s/frame, ~${remaining.toFixed(0)}s remaining)`,
        );
      }
    }

    const renderS = (Date.now() - renderStart) / 1000;
    const perFrameS = renderS / TOTAL_FRAMES;
    console.log(`Frame render complete: ${renderS.toFixed(1)}s (${perFrameS.toFixed(2)}s/frame avg)`);

    console.log('ffmpeg stitching...');
    const ffmpegStart = Date.now();
    const ffmpegArgs = [
      '-y',
      '-framerate', String(DESIGN.anim.fps),
      '-i', join(tmpDir, 'frame-%04d.png'),
      '-c:v', 'libx264',
      '-pix_fmt', 'yuv420p',
      '-movflags', '+faststart',
      '-crf', '18',
      outPath,
    ];
    const ffmpegResult = await runProcess('ffmpeg', ffmpegArgs);
    if (ffmpegResult.exitCode !== 0) {
      throw new Error(
        `ffmpeg exited with code ${ffmpegResult.exitCode}\nstderr:\n${ffmpegResult.stderr}`,
      );
    }
    const ffmpegS = (Date.now() - ffmpegStart) / 1000;
    console.log(`ffmpeg complete: ${ffmpegS.toFixed(1)}s`);

    console.log('ffprobe verifying...');
    const ffprobeStart = Date.now();
    const ffprobeArgs = [
      '-v', 'error',
      '-show_streams',
      '-show_format',
      '-of', 'json',
      outPath,
    ];
    const ffprobeResult = await runProcess('ffprobe', ffprobeArgs);
    if (ffprobeResult.exitCode !== 0) {
      throw new Error(
        `ffprobe exited with code ${ffprobeResult.exitCode}\nstderr:\n${ffprobeResult.stderr}`,
      );
    }

    const probe: FfprobeOutput = JSON.parse(ffprobeResult.stdout);
    const stream = probe.streams.find((s) => s.codec_type === 'video');
    if (!stream) throw new Error('No video stream in output');

    const fileSize = statSync(outPath).size;
    const duration = parseFloat(probe.format.duration ?? '0');
    const nbFrames = parseInt(stream.nb_frames ?? '0', 10);

    const checks: Array<[string, boolean]> = [
      [`width === 1080 (got ${stream.width})`, stream.width === 1080],
      [`height === 1920 (got ${stream.height})`, stream.height === 1920],
      [`codec_name === 'h264' (got ${stream.codec_name})`, stream.codec_name === 'h264'],
      [`pix_fmt === 'yuv420p' (got ${stream.pix_fmt})`, stream.pix_fmt === 'yuv420p'],
      [`nb_frames === ${TOTAL_FRAMES} (got ${nbFrames})`, nbFrames === TOTAL_FRAMES],
      [`duration in [9.4, 9.6] (got ${duration.toFixed(3)})`, duration >= 9.4 && duration <= 9.6],
      [`size in [50KB, 50MB] (got ${fileSize} bytes)`, fileSize >= 50_000 && fileSize <= 50_000_000],
    ];

    const failed = checks.filter(([, ok]) => !ok);
    if (failed.length > 0) {
      throw new Error(
        `ffprobe assertions failed:\n${failed.map(([msg]) => '  - ' + msg).join('\n')}`,
      );
    }
    const ffprobeS = (Date.now() - ffprobeStart) / 1000;

    const overallS = (Date.now() - overallStart) / 1000;
    console.log('PASS: all ffprobe assertions');
    console.log(`Output:    ${outPath}`);
    console.log(`Size:      ${(fileSize / 1024).toFixed(1)} KB`);
    console.log(`Stream:    ${stream.width}x${stream.height} ${stream.codec_name} ${stream.pix_fmt}`);
    console.log(`Frames:    ${nbFrames}`);
    console.log(`Duration:  ${duration.toFixed(3)} s`);
    console.log(`Wall-clock breakdown:`);
    console.log(`  render:  ${renderS.toFixed(1)}s (${perFrameS.toFixed(2)}s/frame)`);
    console.log(`  ffmpeg:  ${ffmpegS.toFixed(1)}s`);
    console.log(`  ffprobe: ${ffprobeS.toFixed(1)}s`);
    console.log(`  total:   ${overallS.toFixed(1)}s`);
  } finally {
    console.log(`Cleaning up temp dir: ${tmpDir}`);
    rmSync(tmpDir, { recursive: true, force: true });
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
