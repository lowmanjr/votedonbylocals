#!/usr/bin/env python3
"""
Generate sitemap.xml from the filesystem.

Discovers indexable HTML pages in the project root, rankings/, and restaurants/.
Excludes underscore-prefixed working files and thank-you.html (noindexed).

Run from project root:
    python scripts/generate_sitemap.py
"""

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


def discover_urls():
    urls = []
    for subdir, url_prefix in SCAN_DIRS.items():
        scan_path = PROJECT_ROOT / subdir if subdir else PROJECT_ROOT
        for html in sorted(scan_path.glob("*.html")):
            name = html.name
            if name.startswith("_") or name in EXCLUDE_FILES:
                continue
            if subdir == "" and name == "index.html":
                urls.append(f"{SITE_URL}/")
            else:
                urls.append(f"{SITE_URL}{url_prefix}{name}")
    return urls


def build_sitemap(urls):
    NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
    root = Element("urlset", xmlns=NS)
    for u in urls:
        url_el = SubElement(root, "url")
        SubElement(url_el, "loc").text = u
    tree = ElementTree(root)
    indent(tree, space="  ")
    return tree


def main():
    urls = discover_urls()
    tree = build_sitemap(urls)
    out = PROJECT_ROOT / "sitemap.xml"
    tree.write(out, encoding="utf-8", xml_declaration=True)
    print(f"Wrote {out} with {len(urls)} URLs.")
    for u in urls:
        print(f"  {u}")


if __name__ == "__main__":
    main()
