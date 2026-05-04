#!/usr/bin/env python3
"""Render Open Graph share-preview images via Playwright + headless Chromium.

Usage:
    python scripts/generate_og_images.py --slug best-pizza
    python scripts/generate_og_images.py --rankings              # all 8
    python scripts/generate_og_images.py --details               # all 33
    python scripts/generate_og_images.py --default               # site default
    python scripts/generate_og_images.py --all                   # everything

Inputs:
    og-templates/ranking.html  + data/og_rankings.json   → 8 ranking PNGs
    og-templates/detail.html   + data/restaurants.json   → 33 detail PNGs
    og-templates/default.html                            → 1 default PNG

Output:
    assets/images/og-{slug}.png              (rankings + featured-winner)
    assets/images/og-restaurant-{slug}.png   (details — note prefix)
    assets/images/og-default.png             (site default)

Brand colors are read from tailwind.config.js at run-time so this script
shares the single-source-of-truth invariant the rest of the project does.
"""

import argparse
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT / 'og-templates'
DATA_DIR = ROOT / 'data'
OUTPUT_DIR = ROOT / 'assets' / 'images'
TAILWIND_CONFIG = ROOT / 'tailwind.config.js'

VIEWPORT_WIDTH = 1200
VIEWPORT_HEIGHT = 630


def read_brand_colors():
    """Parse tailwind.config.js for the brand.* color values.

    Returns {'brandOrange': '#E67E22', ...}. Single source of truth for
    brand colors lives in tailwind.config.js — this regex extraction keeps
    that invariant rather than duplicating values into Python.
    """
    text = TAILWIND_CONFIG.read_text(encoding='utf-8')
    pattern = re.compile(
        r"brand:\s*\{([^}]*)\}", re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        sys.exit('Could not locate brand color block in tailwind.config.js')

    inner = m.group(1)
    colors = {}
    for name, value in re.findall(r"(\w+):\s*'(#[0-9A-Fa-f]+)'", inner):
        colors[f'brand{name.capitalize()}'] = value

    required = {'brandOrange', 'brandCream', 'brandDark', 'brandGray'}
    missing = required - colors.keys()
    if missing:
        sys.exit(f'Missing brand colors in tailwind.config.js: {missing}')
    return colors


def substitute(template_html, **fields):
    """Replace {{Field}} placeholders with their values."""
    out = template_html
    for key, value in fields.items():
        out = out.replace('{{' + key + '}}', str(value))
    return out


def pluralize_spots(n):
    """'5 spots' / '1 spot' / '0 spots' — generic, not hand-curated.

    Triggered by best-new-coffee-shop (n=1) but applies to any future
    featured-winner-shaped page.
    """
    return f"{n} spot{'s' if n != 1 else ''}"


def compose_detail_meta(cuisine, neighborhood):
    """'{Cuisine} · {Neighborhood}', or just '{Cuisine}' when neighborhood is null.

    Mobile vendors (per DECISIONS #14.3) ship with null neighborhood —
    the on-page hero handles them; OG must too. Falling back to cuisine
    alone is honest (the data we have) and avoids a trailing separator.
    """
    if neighborhood:
        return f"{cuisine} · {neighborhood}"
    return cuisine


def compute_name_font_size(name):
    """Three-tier adaptive sizing for restaurant names. See detail.html
    intentional decision #3 for cutoff rationale.

    ≤14 chars  → 132px   (matches ranking's hero)
    15-22      → 108px
    ≥23        → 84px
    """
    n = len(name)
    if n <= 14:
        return '132px'
    if n <= 22:
        return '108px'
    return '84px'


def render(html, output_path):
    """Screenshot the rendered HTML to a PNG at 1200×630."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={'width': VIEWPORT_WIDTH, 'height': VIEWPORT_HEIGHT},
            device_scale_factor=2,
        )
        page = context.new_page()
        page.set_content(html, wait_until='networkidle')
        # Wait for Google Fonts to finish loading — without this we can
        # screenshot before Poppins/DM Sans land and get a serif fallback.
        page.evaluate('document.fonts.ready')
        page.screenshot(path=str(output_path), full_page=False)
        browser.close()
    print(f'  wrote {output_path.relative_to(ROOT)}')


def render_ranking(slug, brand_colors):
    """Render one ranking-page OG image."""
    data_path = DATA_DIR / 'og_rankings.json'
    rankings = json.loads(data_path.read_text(encoding='utf-8'))['rankings']
    entry = next((r for r in rankings if r['slug'] == slug), None)
    if entry is None:
        sys.exit(f'Slug not found in og_rankings.json: {slug}')

    template = (TEMPLATES_DIR / 'ranking.html').read_text(encoding='utf-8')
    html = substitute(
        template,
        Category=entry['category'],
        SpotsLabel=pluralize_spots(entry['spots']),
        **brand_colors,
    )
    output = OUTPUT_DIR / f'og-{slug}.png'
    print(f'rendering ranking: {slug}')
    render(html, output)


def render_detail(slug, brand_colors):
    """Render one detail-page OG image."""
    data_path = DATA_DIR / 'restaurants.json'
    restaurants = json.loads(data_path.read_text(encoding='utf-8'))['restaurants']
    entry = next((r for r in restaurants if r['slug'] == slug), None)
    if entry is None:
        sys.exit(f'Slug not found in restaurants.json: {slug}')

    template = (TEMPLATES_DIR / 'detail.html').read_text(encoding='utf-8')
    html = substitute(
        template,
        RestaurantName=entry['name'],
        NameFontSize=compute_name_font_size(entry['name']),
        MetaLine=compose_detail_meta(entry['cuisine'], entry.get('neighborhood')),
        **brand_colors,
    )
    output = OUTPUT_DIR / f'og-restaurant-{slug}.png'
    print(f'rendering detail: {slug}')
    render(html, output)


def render_default(brand_colors):
    """Render the site-default OG image. Static template — no per-instance
    data, only brand colors substituted."""
    template = (TEMPLATES_DIR / 'default.html').read_text(encoding='utf-8')
    html = substitute(template, **brand_colors)
    output = OUTPUT_DIR / 'og-default.png'
    print('rendering default')
    render(html, output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--slug', help='Single slug to render')
    group.add_argument('--rankings', action='store_true', help='All 8 rankings')
    group.add_argument('--details', action='store_true', help='All 33 details')
    group.add_argument('--default', action='store_true', help='Site default')
    group.add_argument('--all', action='store_true', help='Everything')
    args = parser.parse_args()

    brand_colors = read_brand_colors()
    print(f'brand colors from tailwind.config.js: {brand_colors}')

    if args.slug:
        # Determine type from data files. Ranking slugs live in og_rankings.json;
        # detail slugs in restaurants.json. Slug 'default' renders the site default.
        rankings = json.loads(
            (DATA_DIR / 'og_rankings.json').read_text(encoding='utf-8')
        )['rankings']
        restaurants = json.loads(
            (DATA_DIR / 'restaurants.json').read_text(encoding='utf-8')
        )['restaurants']
        if any(r['slug'] == args.slug for r in rankings):
            render_ranking(args.slug, brand_colors)
        elif any(r['slug'] == args.slug for r in restaurants):
            render_detail(args.slug, brand_colors)
        else:
            sys.exit(
                f'Slug {args.slug!r} not found in og_rankings.json or '
                f'restaurants.json.'
            )
    elif args.rankings:
        rankings = json.loads(
            (DATA_DIR / 'og_rankings.json').read_text(encoding='utf-8')
        )['rankings']
        for r in rankings:
            render_ranking(r['slug'], brand_colors)
    elif args.details:
        restaurants = json.loads(
            (DATA_DIR / 'restaurants.json').read_text(encoding='utf-8')
        )['restaurants']
        for r in restaurants:
            render_detail(r['slug'], brand_colors)
    elif args.default:
        render_default(brand_colors)
    elif args.all:
        rankings = json.loads(
            (DATA_DIR / 'og_rankings.json').read_text(encoding='utf-8')
        )['rankings']
        restaurants = json.loads(
            (DATA_DIR / 'restaurants.json').read_text(encoding='utf-8')
        )['restaurants']
        for r in rankings:
            render_ranking(r['slug'], brand_colors)
        for r in restaurants:
            render_detail(r['slug'], brand_colors)
        render_default(brand_colors)


if __name__ == '__main__':
    main()
