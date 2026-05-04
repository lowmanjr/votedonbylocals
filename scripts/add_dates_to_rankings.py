#!/usr/bin/env python3
"""
One-shot: backfill datePublished + dateModified on the 7 ItemList ranking
pages.

For each in-scope page:
  - Parse the JSON-LD <script> block.
  - Verify @type is ItemList.
  - Verify neither datePublished nor dateModified is already present
    (idempotent if both present; halt if mixed state).
  - Inject both fields seeded from `git log --diff-filter=A` on the file.
  - Re-serialize the <script> block, preserving the existing 4-space block
    indent and 2-space JSON indent.

Excludes:
  - rankings/_*.html (working files)
  - rankings/best-new-coffee-shop.html (no JSON-LD; separate workstream)

Two-pass (validate-then-apply) — halts loudly on per-file divergence. Same
shape as scripts/migrate_chrome.py and scripts/inline_chrome.py.

Run from project root:
    python scripts/add_dates_to_rankings.py
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RANKINGS_DIR = PROJECT_ROOT / 'rankings'
EXCLUDE = {'best-new-coffee-shop.html'}

JSONLD_RE = re.compile(
    r'(    <script type="application/ld\+json">\n)(.+?)(\n    </script>)',
    re.DOTALL,
)


def discover_files():
    files = []
    for f in sorted(RANKINGS_DIR.glob('*.html')):
        if f.name.startswith('_') or f.name in EXCLUDE:
            continue
        files.append(f)
    return files


def get_git_creation_date(filepath):
    try:
        result = subprocess.run(
            ['git', 'log', '--diff-filter=A', '--format=%aI', '--', str(filepath)],
            capture_output=True, text=True, check=True, cwd=PROJECT_ROOT,
        )
        lines = [l for l in result.stdout.strip().split('\n') if l]
        return lines[-1] if lines else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def categorize(filepath):
    """Return ('inline'|'skip'|'fail', reason)."""
    text = filepath.read_text(encoding='utf-8')
    m = JSONLD_RE.search(text)
    if not m:
        return ('fail', 'no JSON-LD <script> block found')
    try:
        data = json.loads(m.group(2))
    except json.JSONDecodeError as e:
        return ('fail', f'JSON parse error: {e}')
    if data.get('@type') != 'ItemList':
        return ('fail', f"@type is {data.get('@type')!r}, expected 'ItemList'")
    has_pub = 'datePublished' in data
    has_mod = 'dateModified' in data
    if has_pub and has_mod:
        return ('skip', 'already has datePublished + dateModified')
    if has_pub or has_mod:
        return ('fail', f'mixed state: datePublished={has_pub}, dateModified={has_mod}')
    return ('inline', 'OK')


def apply_edits(filepath):
    text = filepath.read_text(encoding='utf-8')
    m = JSONLD_RE.search(text)
    open_tag, body, close_tag = m.group(1), m.group(2), m.group(3)
    data = json.loads(body)

    seed_date = (
        get_git_creation_date(filepath)
        or datetime.now(timezone.utc).isoformat(timespec='seconds')
    )

    # Rebuild dict with datePublished + dateModified inserted between
    # description and url. Other fields preserve their existing order.
    rebuilt = {}
    for key in ('@context', '@type', 'name', 'description'):
        if key in data:
            rebuilt[key] = data[key]
    rebuilt['datePublished'] = seed_date
    rebuilt['dateModified'] = seed_date
    for key, value in data.items():
        if key not in rebuilt:
            rebuilt[key] = value

    new_body = json.dumps(rebuilt, indent=2, ensure_ascii=False)
    new_body_indented = '\n'.join('    ' + line for line in new_body.split('\n'))
    new_text = text[:m.start()] + open_tag + new_body_indented + close_tag + text[m.end():]
    filepath.write_text(new_text, encoding='utf-8')


def main():
    files = discover_files()
    print(f"Discovered {len(files)} ranking pages.")

    inline_targets = []
    skip_targets = []
    failures = {}

    for f in files:
        status, reason = categorize(f)
        if status == 'inline':
            inline_targets.append(f)
        elif status == 'skip':
            skip_targets.append(f)
        else:
            failures[f] = reason

    if failures:
        print(f"\nHALT: {len(failures)} file(s) failed validation. No files modified.")
        for f, reason in failures.items():
            print(f"  {f.relative_to(PROJECT_ROOT)}: {reason}")
        sys.exit(1)

    if skip_targets:
        print(f"Skipping {len(skip_targets)} already-backfilled file(s).")

    if not inline_targets:
        print("Nothing to backfill.")
        return

    for f in inline_targets:
        apply_edits(f)
        print(f"  backfilled: {f.relative_to(PROJECT_ROOT)}")

    print(f"\nBackfilled {len(inline_targets)} files.")


if __name__ == "__main__":
    main()
