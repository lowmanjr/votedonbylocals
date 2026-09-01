#!/usr/bin/env python3
"""
Generate sitemap.xml and _redirects from the filesystem.

Discovers indexable HTML pages in the project root, rankings/, and restaurants/.
Excludes underscore-prefixed working files and thank-you.html (noindexed; also
deliberately kept out of _redirects -- see build_redirects).

Both artifacts come from the same page enumeration so a new page cannot ship
in the sitemap without its redirect rule (or vice versa):

    sitemap.xml   <loc> entries are the extension-less URLs the pages'
                  canonicals declare.
    _redirects    one forced 301 per page from the physical .html path to
                  the extension-less URL, then the hand-maintained rules in
                  data/manual_redirects.txt (retired URLs) under a
                  "# manual" header -- see load_manual_redirects.

Run from project root:
    python scripts/generate_sitemap.py
"""

import json
import re
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent

SITE_URL = "https://votedonbylocals.com"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Directories to scan, mapped to their URL prefix.
SCAN_DIRS = {
    "": "/",
    "rankings": "/rankings/",
    "restaurants": "/restaurants/",
}

EXCLUDE_FILES = {"thank-you.html"}

# Hand-maintained redirect rules for retired URLs, merged into _redirects.
MANUAL_REDIRECTS_PATH = PROJECT_ROOT / "data" / "manual_redirects.txt"


def extract_dateModified_from_html(filepath):
    """Parse the JSON-LD <script> block; return dateModified value or None.

    Handles both page shapes: a single-location page's flat node, and a
    multi-location page's `@graph`, where the dates live on the brand
    Organization node. Without the @graph branch every multi-location page
    would silently lose its <lastmod>.
    """
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.search(
        r'<script type="application/ld\+json">(.+?)</script>',
        text, re.DOTALL,
    )
    if not m:
        return None
    try:
        data = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    if "dateModified" in data:
        return data["dateModified"]
    for node in data.get("@graph") or []:
        if isinstance(node, dict) and "dateModified" in node:
            return node["dateModified"]
    return None


def discover_pages():
    """Return list of (html_path, clean_path, lastmod_or_None) tuples.

    html_path is the site-relative path of the physical file, e.g.
    "/rankings/best-pizza.html". clean_path is the extension-less URL the
    site serves and the page's canonical declares ("/" for the homepage).
    """
    entries = []
    for subdir, url_prefix in SCAN_DIRS.items():
        scan_path = PROJECT_ROOT / subdir if subdir else PROJECT_ROOT
        for html in sorted(scan_path.glob("*.html")):
            name = html.name
            if name.startswith("_") or name in EXCLUDE_FILES:
                continue
            html_path = f"{url_prefix}{name}"
            if subdir == "" and name == "index.html":
                clean_path = "/"
            else:
                clean_path = f"{url_prefix}{name.removesuffix('.html')}"
            lastmod = extract_dateModified_from_html(html)
            entries.append((html_path, clean_path, lastmod))
    return entries


def build_sitemap(entries):
    NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
    root = Element("urlset", xmlns=NS)
    for _, clean_path, lastmod in entries:
        url_el = SubElement(root, "url")
        SubElement(url_el, "loc").text = f"{SITE_URL}{clean_path}"
        if lastmod is not None:
            SubElement(url_el, "lastmod").text = lastmod
    tree = ElementTree(root)
    indent(tree, space="  ")
    return tree


def load_manual_redirects(entries):
    """Read the hand-maintained rules in data/manual_redirects.txt: retired
    URLs whose page no longer exists in the deploy. Returns the validated
    rule lines, or [] when the file is absent.

    Netlify syntax, one `from to status` per line; `#` comments and blank
    lines are ignored. Every rule is checked against the page enumeration
    so a typo cannot ship:
      - from-path starts with "/" and is not a path the generated block
        owns (a live page's .html path or clean URL), and no from-path
        repeats -- Netlify takes the first match
      - target is a discovered clean URL or an absolute http(s) URL, so a
        retired URL always lands on a page that exists
      - status is a 3-digit code, optionally forced with "!"
    The rules are meant to be unforced: with no file at a retired path
    there is nothing to shadow, and if a file ever reappears there the
    collision check fails the run instead of the file silently winning.
    """
    if not MANUAL_REDIRECTS_PATH.exists():
        return []
    html_paths = {html_path for html_path, _, _ in entries}
    clean_paths = {clean_path for _, clean_path, _ in entries}
    seen = set()
    rules = []
    lines = MANUAL_REDIRECTS_PATH.read_text(encoding="utf-8").splitlines()
    for lineno, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        where = f"{MANUAL_REDIRECTS_PATH.name}:{lineno}"
        parts = line.split()
        if len(parts) != 3:
            raise SystemExit(f"{where}: expected 'from to status', got {raw!r}")
        src, dst, status = parts
        if not src.startswith("/"):
            raise SystemExit(f"{where}: from-path must start with '/': {src}")
        if src in html_paths or src in clean_paths:
            raise SystemExit(
                f"{where}: {src} is a live page path; the generated block "
                f"already owns it"
            )
        if src in seen:
            raise SystemExit(f"{where}: duplicate from-path {src}")
        if dst not in clean_paths and not re.match(r"https?://", dst):
            raise SystemExit(
                f"{where}: target {dst} is not a discovered clean URL; a "
                f"retired URL must land on a page that exists"
            )
        if not re.fullmatch(r"\d{3}!?", status):
            raise SystemExit(f"{where}: bad status {status!r}")
        seen.add(src)
        rules.append(f"{src} {dst} {status}")
    return rules


def build_redirects(entries, manual_rules=()):
    """Build the Netlify _redirects file: one forced 301 per page, .html
    path -> extension-less path. Forced (301!) because the .html files
    exist in the deploy and Netlify only shadows existing paths with
    forced rules.

    thank-you.html is deliberately absent (via EXCLUDE_FILES): the vote
    form posts to /thank-you.html, and a forced redirect on a Netlify
    form action path risks breaking submissions.

    manual_rules (from load_manual_redirects) follow the generated block
    under a "# manual" header, so the file stays fully generated: the
    source of those lines is data/manual_redirects.txt, never this file.
    """
    lines = [
        "# Generated by scripts/generate_sitemap.py -- do not edit by hand.",
        "# One forced 301 per page: the physical .html path redirects to the",
        "# extension-less URL the page's canonical declares. thank-you.html is",
        "# deliberately absent: the vote form posts to /thank-you.html, and a",
        "# forced redirect on a Netlify form action path risks breaking",
        "# submissions.",
    ]
    for html_path, clean_path, _ in entries:
        lines.append(f"{html_path} {clean_path} 301!")
    if manual_rules:
        lines.append("")
        lines.append(
            "# manual -- hand-maintained rules from data/manual_redirects.txt "
            "(retired URLs; unforced because no file exists at those paths)."
        )
        lines.extend(manual_rules)
    return "\n".join(lines) + "\n"


def main():
    entries = discover_pages()

    tree = build_sitemap(entries)
    sitemap_out = PROJECT_ROOT / "sitemap.xml"
    tree.write(sitemap_out, encoding="utf-8", xml_declaration=True)

    manual_rules = load_manual_redirects(entries)
    redirects_out = PROJECT_ROOT / "_redirects"
    with redirects_out.open("w", encoding="utf-8", newline="\n") as f:
        f.write(build_redirects(entries, manual_rules))

    n_lastmod = sum(1 for _, _, lm in entries if lm is not None)
    print(f"Wrote {sitemap_out} with {len(entries)} URLs ({n_lastmod} with <lastmod>).")
    print(
        f"Wrote {redirects_out} with {len(entries)} redirect rules "
        f"({len(manual_rules)} manual)."
    )
    for _, clean_path, lastmod in entries:
        suffix = f"  [lastmod: {lastmod}]" if lastmod else ""
        print(f"  {SITE_URL}{clean_path}{suffix}")


if __name__ == "__main__":
    main()
