#!/usr/bin/env python3
"""
One-shot migration: switch chrome from Tailwind CDN to local built.css
across all production HTML pages.

Per-file edits:
  EDIT A — delete <script src="https://cdn.tailwindcss.com"></script>
  EDIT B — delete the inline <script> ... tailwind.config = { ... } </script> block
  EDIT C — insert <link rel="stylesheet" href="...assets/css/built.css">
           immediately before the existing style.css link, matching its indent

EDIT B matches by content boundaries (a <script> with no attributes whose body
contains `tailwind.config = {`), not by exact whitespace. This keeps the script
robust against minor inter-page indentation drift.

Two-pass: validate all files first, then apply only if every file's pattern
counts are exactly (1, 1, 1). If any file diverges, the script halts WITHOUT
modifying anything and prints the divergent files.

Not idempotent — designed to run exactly once during the step-4 migration.
Kept in scripts/ as a reference for future similar mass chrome edits.

Run from project root:
    python scripts/migrate_chrome.py
"""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["", "rankings", "restaurants"]

CDN_RE = re.compile(
    r'[ \t]*<script src="https://cdn\.tailwindcss\.com"></script>\r?\n?'
)
INLINE_CONFIG_RE = re.compile(
    r'[ \t]*<script>\s*tailwind\.config\s*=\s*\{.*?\}\s*</script>\r?\n?',
    re.DOTALL,
)
STYLE_CSS_RE = re.compile(
    r'^([ \t]*)<link rel="stylesheet" href="[^"]*style\.css">',
    re.MULTILINE,
)


def discover_files():
    files = []
    for subdir in SCAN_DIRS:
        scan_path = PROJECT_ROOT / subdir if subdir else PROJECT_ROOT
        for html in sorted(scan_path.glob("*.html")):
            files.append(html)
    return files


def get_built_prefix(filepath):
    """Subdir pages get '../', root pages get ''."""
    rel = filepath.relative_to(PROJECT_ROOT)
    return "../" if len(rel.parts) > 1 else ""


def validate(filepath):
    """Returns list of issues (empty if OK)."""
    text = filepath.read_text(encoding="utf-8")
    issues = []
    cdn_count = len(CDN_RE.findall(text))
    config_count = len(INLINE_CONFIG_RE.findall(text))
    style_count = len(STYLE_CSS_RE.findall(text))
    if cdn_count != 1:
        issues.append(f"CDN script count={cdn_count} (want 1)")
    if config_count != 1:
        issues.append(f"inline tailwind.config block count={config_count} (want 1)")
    if style_count != 1:
        issues.append(f"style.css link count={style_count} (want 1)")
    return issues


def apply_edits(filepath):
    text = filepath.read_text(encoding="utf-8")
    text = CDN_RE.sub("", text, count=1)
    text = INLINE_CONFIG_RE.sub("", text, count=1)
    m = STYLE_CSS_RE.search(text)
    indent = m.group(1)
    prefix = get_built_prefix(filepath)
    new_line = f'{indent}<link rel="stylesheet" href="{prefix}assets/css/built.css">\n'
    text = text[: m.start()] + new_line + text[m.start():]
    filepath.write_text(text, encoding="utf-8")


def main():
    files = discover_files()
    print(f"Discovered {len(files)} HTML pages.")

    failures = {}
    for f in files:
        issues = validate(f)
        if issues:
            failures[f] = issues

    if failures:
        print(f"\nHALT: {len(failures)} file(s) diverge. No files modified.")
        for f, issues in failures.items():
            print(f"  {f.relative_to(PROJECT_ROOT)}: {', '.join(issues)}")
        sys.exit(1)

    for f in files:
        apply_edits(f)
        print(f"  migrated: {f.relative_to(PROJECT_ROOT)}")

    print(f"\nMigrated {len(files)} files.")


if __name__ == "__main__":
    main()
