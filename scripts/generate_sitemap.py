#!/usr/bin/env python3
"""
Generate sitemap.xml from the filesystem.

Discovers indexable HTML pages in the project root, rankings/, and restaurants/.
Excludes underscore-prefixed working files and thank-you.html (noindexed).

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


def extract_dateModified_from_html(filepath):
    """Parse the JSON-LD <script> block; return dateModified value or None."""
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
    return data.get("dateModified")


def discover_urls():
    """Return list of (url, lastmod_or_None) tuples."""
    entries = []
    for subdir, url_prefix in SCAN_DIRS.items():
        scan_path = PROJECT_ROOT / subdir if subdir else PROJECT_ROOT
        for html in sorted(scan_path.glob("*.html")):
            name = html.name
            if name.startswith("_") or name in EXCLUDE_FILES:
                continue
            if subdir == "" and name == "index.html":
                url = f"{SITE_URL}/"
            else:
                url = f"{SITE_URL}{url_prefix}{name}"
            lastmod = extract_dateModified_from_html(html)
            entries.append((url, lastmod))
    return entries


def build_sitemap(entries):
    NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
    root = Element("urlset", xmlns=NS)
    for url, lastmod in entries:
        url_el = SubElement(root, "url")
        SubElement(url_el, "loc").text = url
        if lastmod is not None:
            SubElement(url_el, "lastmod").text = lastmod
    tree = ElementTree(root)
    indent(tree, space="  ")
    return tree


def main():
    entries = discover_urls()
    tree = build_sitemap(entries)
    out = PROJECT_ROOT / "sitemap.xml"
    tree.write(out, encoding="utf-8", xml_declaration=True)
    n_lastmod = sum(1 for _, lm in entries if lm is not None)
    print(f"Wrote {out} with {len(entries)} URLs ({n_lastmod} with <lastmod>).")
    for url, lastmod in entries:
        suffix = f"  [lastmod: {lastmod}]" if lastmod else ""
        print(f"  {url}{suffix}")


if __name__ == "__main__":
    main()
