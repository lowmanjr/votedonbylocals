#!/usr/bin/env python3
"""
Drift gate for the generated stylesheet.

assets/css/built.css is a Tailwind build artifact that is committed to the
repo. It is produced by `npm run build:css` from src/input.css plus the content
globs in tailwind.config.js. Nothing regenerates it automatically, so it goes
stale silently whenever HTML starts using a utility class that was not already
emitted -- which is exactly how the homepage desktop grid shipped rendering two
columns instead of four for four months (see PR #55).

This script regenerates the stylesheet to a TEMPORARY path and compares it
byte-for-byte against the committed file. It never writes the tracked file.

Output style matches scripts/inline_chrome.py --check so both CI gates read the
same way.

Run from anywhere:
    python scripts/check_built_css.py

Exit codes:
    0 - committed built.css matches a fresh build
    1 - drift detected; run `npm run build:css` and commit the result
    2 - toolchain problem (tailwindcss binary missing, or the build failed)
"""

import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_CSS = PROJECT_ROOT / "src" / "input.css"
BUILT_CSS = PROJECT_ROOT / "assets" / "css" / "built.css"
REL_BUILT = "assets/css/built.css"

# npm installs a .cmd shim on Windows and a shebang script everywhere else.
BIN_NAME = "tailwindcss.cmd" if os.name == "nt" else "tailwindcss"
TAILWIND_BIN = PROJECT_ROOT / "node_modules" / ".bin" / BIN_NAME


def sha16(data):
    return hashlib.sha256(data).hexdigest()[:16]


def main():
    if not TAILWIND_BIN.exists():
        print("[FAIL] tailwindcss binary not found at node_modules/.bin/" + BIN_NAME)
        print("       Run `npm ci` first.")
        return 2

    if not BUILT_CSS.exists():
        print("[FAIL] " + REL_BUILT + " is missing from the repo.")
        print("       Fix: run `npm run build:css` and commit the result.")
        return 1

    with tempfile.TemporaryDirectory() as tmpdir:
        fresh = Path(tmpdir) / "built.css"
        proc = subprocess.run(
            [str(TAILWIND_BIN), "-i", str(INPUT_CSS), "-o", str(fresh), "--minify"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0 or not fresh.exists():
            print("[FAIL] tailwindcss build failed (exit " + str(proc.returncode) + "):")
            detail = (proc.stderr or proc.stdout or "").strip()
            for line in detail.split("\n")[-10:]:
                print("       " + line)
            return 2

        committed = BUILT_CSS.read_bytes()
        rebuilt = fresh.read_bytes()

    if committed == rebuilt:
        print("[OK] " + REL_BUILT + " in sync with src/input.css ("
              + str(len(committed)) + " bytes)")
        return 0

    print("[FAIL] " + REL_BUILT + " is stale - a fresh build produces different bytes.")
    print("       committed   : " + str(len(committed)) + " bytes, sha256 " + sha16(committed))
    print("       fresh build : " + str(len(rebuilt)) + " bytes, sha256 " + sha16(rebuilt))
    print("       Fix: run `npm run build:css` and commit " + REL_BUILT + ".")
    return 1


if __name__ == "__main__":
    sys.exit(main())
