#!/usr/bin/env python3
"""
Build-time inliner for header/footer chrome.

Replaces these placeholders across all production HTML pages:
  <header id="main-header"></header>  → contents of components/header.html
  <footer id="main-footer"></footer>  → contents of components/footer.html

Indentation of the placeholder line is preserved on every line of the
inlined component, so the resulting markup stays readable.

components/ remains the editable source-of-truth. Operator workflow:
  1. Edit components/header.html or components/footer.html.
  2. Run `python scripts/inline_chrome.py`.
  3. Commit.

Two-pass (validate-then-apply) — halts loudly if any file's placeholder state
is inconsistent. Same shape as scripts/migrate_chrome.py.

Idempotent: a file with 0 placeholders (already inlined) is skipped without
error. A file with mixed state (e.g., header inlined but footer placeholder
still present) halts with a diagnostic — this should never happen in normal
operation but catches manual editing mistakes.

Run from project root:
    python scripts/inline_chrome.py
"""

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["", "rankings", "restaurants"]

HEADER_PLACEHOLDER = '<header id="main-header"></header>'
FOOTER_PLACEHOLDER = '<footer id="main-footer"></footer>'


def discover_files():
    files = []
    for subdir in SCAN_DIRS:
        scan_path = PROJECT_ROOT / subdir if subdir else PROJECT_ROOT
        for html in sorted(scan_path.glob("*.html")):
            files.append(html)
    return files


def load_components():
    header_path = PROJECT_ROOT / "components" / "header.html"
    footer_path = PROJECT_ROOT / "components" / "footer.html"
    return (
        header_path.read_text(encoding="utf-8"),
        footer_path.read_text(encoding="utf-8"),
    )


def replace_placeholder(html, placeholder, component_text):
    """Replace `placeholder` with `component_text`, prepending the placeholder
    line's leading whitespace to every line of the component (preserving
    visual indent in the resulting HTML).

    Returns (new_html, count_replaced).
    """
    # Capture (start-anchor, leading whitespace) before the literal placeholder.
    pattern = re.compile(
        r'(^|\n)([ \t]*)' + re.escape(placeholder),
        re.MULTILINE,
    )
    matches = list(pattern.finditer(html))
    if not matches:
        return html, 0

    component = component_text.rstrip("\n")
    out_parts = []
    last = 0
    for m in matches:
        prefix, indent = m.group(1), m.group(2)
        out_parts.append(html[last:m.start()])
        # Prepend `indent` to every line of the component.
        if indent:
            indented = "\n".join(
                (indent + line if line else line)
                for line in component.split("\n")
            )
        else:
            indented = component
        out_parts.append(prefix + indented)
        last = m.end()
    out_parts.append(html[last:])
    return "".join(out_parts), len(matches)


def categorize(filepath):
    """Return (text, header_count, footer_count)."""
    text = filepath.read_text(encoding="utf-8")
    h = text.count(HEADER_PLACEHOLDER)
    f = text.count(FOOTER_PLACEHOLDER)
    return text, h, f


def main():
    files = discover_files()
    print(f"Discovered {len(files)} HTML pages.")

    header_text, footer_text = load_components()

    inline_targets = []
    skip_targets = []
    failures = {}

    for f in files:
        _, h_count, f_count = categorize(f)
        if h_count == 1 and f_count == 1:
            inline_targets.append(f)
        elif h_count == 0 and f_count == 0:
            skip_targets.append(f)
        else:
            failures[f] = f"header_count={h_count}, footer_count={f_count} (want both=1 or both=0)"

    if failures:
        print(f"\nHALT: {len(failures)} file(s) have mismatched placeholder state. No files modified.")
        for f, msg in failures.items():
            print(f"  {f.relative_to(PROJECT_ROOT)}: {msg}")
        sys.exit(1)

    if skip_targets:
        print(f"Skipping {len(skip_targets)} already-inlined file(s).")

    if not inline_targets:
        print("Nothing to inline.")
        return

    for f in inline_targets:
        text = f.read_text(encoding="utf-8")
        text, _ = replace_placeholder(text, HEADER_PLACEHOLDER, header_text)
        text, _ = replace_placeholder(text, FOOTER_PLACEHOLDER, footer_text)
        f.write_text(text, encoding="utf-8")
        print(f"  inlined: {f.relative_to(PROJECT_ROOT)}")

    print(f"\nInlined {len(inline_targets)} files.")


if __name__ == "__main__":
    main()
