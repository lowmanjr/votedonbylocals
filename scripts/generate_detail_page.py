#!/usr/bin/env python3
"""Generate restaurants/{slug}.html from the template + restaurants.json data.

Usage:
    python scripts/generate_detail_page.py <slug>
    python scripts/generate_detail_page.py <slug> --output PATH
    python scripts/generate_detail_page.py --all

Reference target: restaurants/park-pizza-co.html. The script must
produce a byte-identical file when run for slug 'park-pizza-co'.

Architecture: template-as-source-of-truth. The template carries all
structural HTML; this script applies a 14-step transformation
pipeline to fill in per-restaurant data and resolve the
optional-block conventions documented in the template's intentional
decisions block.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

from _cuisine_dedup import _resolve_display_cuisine

ROOT = Path(__file__).parent.parent
TEMPLATE_PATH = ROOT / 'rankings' / '_detail-page-template.html'
DATA_PATH = ROOT / 'data' / 'restaurants.json'


def get_git_creation_date(filepath):
    """Return the ISO-8601 date+tz of the file's first-add commit, or None
    if git is unavailable or the file has no history.

    Used to seed datePublished + dateModified for new pages.
    """
    try:
        result = subprocess.run(
            ['git', 'log', '--diff-filter=A', '--format=%aI', '--', str(filepath)],
            capture_output=True, text=True, check=True, cwd=ROOT,
        )
        lines = [l for l in result.stdout.strip().split('\n') if l]
        # Earliest add wins (in case of delete-then-re-add history).
        return lines[-1] if lines else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def read_existing_dates(filepath):
    """Read the existing page's JSON-LD and return any datePublished /
    dateModified it carries. Returns {} if the file doesn't exist or the
    JSON-LD can't be parsed.

    Used so that regeneration preserves operator-maintained dateModified
    rather than re-seeding from git on every run.

    Handles both page shapes: a single-location page's flat node, and a
    multi-location page's `@graph` (where the dates live on the brand
    Organization node). Without the @graph branch, regenerating a
    multi-location page would silently re-seed its dates from git.
    """
    if not filepath.exists():
        return {}
    try:
        text = filepath.read_text(encoding='utf-8')
        m = re.search(
            r'<script type="application/ld\+json">(.+?)</script>',
            text, re.DOTALL,
        )
        if not m:
            return {}
        data = json.loads(m.group(1))
        for node in jsonld_nodes(data):
            found = {
                k: node[k] for k in ('datePublished', 'dateModified') if k in node
            }
            if found:
                return found
        return {}
    except (json.JSONDecodeError, OSError):
        return {}


def jsonld_nodes(data):
    """Yield the parsed JSON-LD object itself, then any `@graph` members.

    One helper for both page shapes so date lookups do not have to know
    which shape they are reading. Mirrored in scripts/generate_sitemap.py
    (which reads the same two shapes for <lastmod>).
    """
    if not isinstance(data, dict):
        return
    yield data
    for node in data.get('@graph') or []:
        if isinstance(node, dict):
            yield node


def _slugify(label):
    """Produce a URL-fragment-safe slug from a location label.

    Lowercase; collapse runs of non-alphanumerics into a single hyphen;
    strip leading/trailing hyphens. Used for `subOrganization` `@id`
    fragments per DECISIONS #17.
    """
    return re.sub(r'[^a-z0-9]+', '-', label.lower()).strip('-')


# ---------------------------------------------------------------------------
# Multi-location resolution (per DECISIONS #13.11, 2026-09-01 revision)
# ---------------------------------------------------------------------------

DAY_CODES = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
DAY_NAMES = {
    'Mo': 'Monday', 'Tu': 'Tuesday', 'We': 'Wednesday', 'Th': 'Thursday',
    'Fr': 'Friday', 'Sa': 'Saturday', 'Su': 'Sunday',
}
_HOURS_CHUNK = re.compile(
    r'(Mo|Tu|We|Th|Fr|Sa|Su)(?:-(Mo|Tu|We|Th|Fr|Sa|Su))?'
    r'\s+([0-2]\d:[0-5]\d)-([0-2]\d:[0-5]\d)$'
)


def parse_opening_hours(hours, context):
    """Parse a schema.org openingHours string into openingHoursSpecification.

    The `hours` field stays the single source of truth for machine-readable
    hours; this expands it rather than duplicating it in the data. Accepts
    the comma-separated form the data already uses, with or without a space
    after the comma ("Mo-Fr 07:00-17:00, Sa-Su 08:00-17:00").

    A string this cannot fully express raises — never a silent omission,
    which would publish a location as having no hours at all.
    """
    specs = []
    for chunk in hours.split(','):
        chunk = chunk.strip()
        if not chunk:
            continue
        m = _HOURS_CHUNK.fullmatch(chunk)
        if not m:
            raise ValueError(
                f"{context}: cannot parse openingHours segment {chunk!r} "
                f"from {hours!r}"
            )
        start, end, opens, closes = m.groups()
        for stamp in (opens, closes):
            hh, mm = (int(p) for p in stamp.split(':'))
            if hh > 24 or (hh == 24 and mm):
                raise ValueError(f"{context}: invalid time {stamp!r} in {hours!r}")
        first = DAY_CODES.index(start)
        last = DAY_CODES.index(end) if end else first
        if last < first:
            raise ValueError(
                f"{context}: day range {chunk!r} runs backwards through the week"
            )
        specs.append({
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": [DAY_NAMES[d] for d in DAY_CODES[first:last + 1]],
            "opens": opens,
            "closes": closes,
        })
    if not specs:
        raise ValueError(f"{context}: openingHours {hours!r} yielded no segments")
    return specs


def maps_url_for(address):
    """Derive a Google Maps search URL from a PostalAddress-shaped dict.

    Derived rather than stored: a maps link is a deterministic function of
    an address we already have, so storing one per location would be data
    to keep in sync for no added information. A per-location `maps_url`
    field overrides this when a canonical place link is worth pinning.
    """
    parts = [
        address.get('streetAddress'),
        address.get('addressLocality'),
        f"{address.get('addressRegion', '')} {address.get('postalCode', '')}".strip(),
    ]
    query = ', '.join(p for p in parts if p)
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}"


def resolve_locations(restaurant):
    """Return every location of a multi-location restaurant, primary first,
    normalized to one shape. Empty list for single-location restaurants.

    The primary location lives in the record's top-level address / phone /
    hours fields; `primaryLocation` is the optional overlay that gives it
    the display name, slug, neighborhood and own URL that entries in
    `locations[]` carry natively.
    """
    secondaries = restaurant.get('locations') or []
    if not secondaries:
        return []

    resolved = [_resolve_primary(restaurant)]
    resolved.extend(_resolve_secondary(restaurant, loc) for loc in secondaries)

    seen = {}
    for loc in resolved:
        if loc['slug'] in seen:
            raise ValueError(
                f"{restaurant['slug']}: duplicate location slug {loc['slug']!r} "
                f"({seen[loc['slug']]} and {loc['name']}) — section ids and "
                f"JSON-LD @ids must be unique within a page"
            )
        seen[loc['slug']] = loc['name']
    return resolved


def _resolve_primary(restaurant):
    overlay = restaurant.get('primaryLocation') or {}
    if restaurant.get('primaryLocation') is not None and not overlay.get('slug'):
        raise ValueError(
            f"{restaurant['slug']}: primaryLocation requires an explicit slug"
        )
    label = overlay.get('label') or restaurant.get('neighborhood')
    slug = overlay.get('slug') or (_slugify(label) if label else 'main')
    address = restaurant.get('address') or {}
    return {
        'slug': slug,
        'name': overlay.get('name') or _location_name(restaurant, label),
        'address': address,
        'neighborhood': (
            overlay.get('neighborhood')
            or restaurant.get('neighborhood')
            or address.get('addressLocality')
        ),
        'phone': restaurant.get('phone'),
        'hours': restaurant.get('hours'),
        'hoursHumanReadable': restaurant.get('hoursHumanReadable'),
        'url': overlay.get('url'),
        'mapsURL': overlay.get('maps_url') or maps_url_for(address),
    }


def _resolve_secondary(restaurant, loc):
    address = loc.get('address') or {}
    label = loc.get('label')
    return {
        'slug': loc.get('slug') or _slugify(label),
        'name': loc.get('name') or _location_name(restaurant, label),
        'address': address,
        'neighborhood': loc.get('neighborhood') or address.get('addressLocality'),
        'phone': loc.get('phone'),
        'hours': loc.get('hours'),
        'hoursHumanReadable': loc.get('hoursHumanReadable'),
        'url': loc.get('websiteURL'),
        'mapsURL': loc.get('maps_url') or maps_url_for(address),
    }


def _location_name(restaurant, label):
    """Compose "<Brand> — <Label>", the name convention already in the
    shipped subOrganization nodes. An explicit per-location `name` wins.
    """
    if not label:
        return restaurant['name']
    return f"{restaurant['name']} — {label}"


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------

def generate(template, restaurant):
    """Apply the 14-step transformation pipeline to produce final HTML."""
    text = template
    text = step_1_strip_top_docblock(text)
    text = step_2_replace_jsonld_docblock(text, restaurant)
    text = step_3_substitute_jsonld_script(text, restaurant)
    text = step_4_strip_future_proof_blocks(text)
    text = step_5_strip_editorial_body(text, restaurant)
    text = step_6_simplify_info_sidebar_comment(text)
    text = step_7_handle_address_section(text, restaurant)
    text = step_8_handle_optional_sidebar_blocks(text, restaurant)
    text = step_9_handle_locations_section(text, restaurant)
    text = step_10_strip_appears_on_repeating_comment(text)
    text = step_11_transform_section_replace_comments(text)
    text = step_12_transform_inline_replace_comments(text)
    text = step_13_substitute_remaining_placeholders(text, restaurant)
    text = step_14_apply_multilocation_title(text, restaurant)
    return text


# ---------------------------------------------------------------------------
# Step 1: top docblock
# ---------------------------------------------------------------------------

def step_1_strip_top_docblock(text):
    """Remove the template's top documentation comment (the giant <!-- ... -->
    that starts the file with field docs and intentional-decisions).
    """
    return re.sub(r'^<!--.*?-->\n', '', text, count=1, flags=re.DOTALL)


# ---------------------------------------------------------------------------
# Step 2: JSON-LD docblock → single-line section header
# ---------------------------------------------------------------------------

def step_2_replace_jsonld_docblock(text, restaurant):
    """Replace the JSON-LD HTML comment block (containing optional-snippet
    guidance) with a single-line section header
    `    <!-- JSON-LD: <SchemaType> ----...---- -->`.

    The dash padding is computed to match the standard KEEP-comment width
    derived from the template (which keeps section headers visually aligned).
    """
    schema_type = restaurant['schemaType']
    width = _derive_comment_width(text)
    header_inner = f'JSON-LD: {schema_type}'
    # `<!-- TEXT --DASHES-- -->` = 5 + len(TEXT) + 1 + N + 1 + 3 = 10 + len(TEXT) + N
    dash_count = width - 10 - len(header_inner)
    new_header = f'    <!-- {header_inner} {"-" * dash_count} -->'

    return re.sub(
        r'    <!--\n\s+REPLACE: JSON-LD.*?-->\n',
        new_header + '\n',
        text,
        count=1,
        flags=re.DOTALL,
    )


def _derive_comment_width(template):
    """Measure the standard `<!-- KEEP: ... -->` line width (without leading
    indent) so we can generate matching-width section headers.
    """
    for line in template.split('\n'):
        s = line.strip()
        if s.startswith('<!-- KEEP:') and s.endswith('-->') and '---' in s:
            return len(s)
    return 73  # safe fallback


# ---------------------------------------------------------------------------
# Step 3: JSON-LD <script> contents
# ---------------------------------------------------------------------------

def step_3_substitute_jsonld_script(text, restaurant):
    """Replace the JSON-LD `<script>` block contents with serialized JSON
    built from the restaurant data via build_jsonld_dict().

    Field policy:
      - REQUIRED: @context, @type, name, description, url, address (or
        areaServed for mobile vendors), servesCuisine.
      - OPTIONAL added only if non-null in data: telephone, openingHours,
        priceRange, sameAs, image, geo.

    The serialized JSON is indented with 2-space JSON indent and prefixed
    with 4 spaces to match the surrounding script-tag indent.
    """
    obj = build_jsonld_dict(restaurant)
    json_text = json.dumps(obj, indent=2, ensure_ascii=False)
    indented_json = '\n'.join('    ' + line for line in json_text.split('\n'))

    new_script = (
        '    <script type="application/ld+json">\n'
        + indented_json + '\n'
        + '    </script>'
    )

    return re.sub(
        r'    <script type="application/ld\+json">\n.*?\n    </script>',
        new_script,
        text,
        count=1,
        flags=re.DOTALL,
    )


def build_jsonld_dict(restaurant):
    """Build the ordered JSON-LD dict from restaurant data. Field order
    matches what the template + reference page produces.

    datePublished + dateModified are seeded from the file's git first-add
    commit timestamp on first generation. Subsequent regenerations preserve
    whatever values are in the existing HTML, so operator-maintained
    dateModified is not overwritten on re-run.
    """
    slug = restaurant['slug']
    detail_path = ROOT / 'restaurants' / f'{slug}.html'

    existing = read_existing_dates(detail_path)
    seed_date = (
        get_git_creation_date(detail_path)
        or datetime.now(timezone.utc).isoformat(timespec='seconds')
    )
    date_published = existing.get('datePublished') or seed_date
    date_modified = existing.get('dateModified') or seed_date

    canonical = f"https://votedonbylocals.com/restaurants/{slug}"

    if restaurant.get('locations'):
        return build_multilocation_graph(
            restaurant, canonical, date_published, date_modified
        )

    obj = {
        "@context": "https://schema.org",
        "@type": restaurant['schemaType'],
        "name": restaurant['name'],
        "description": restaurant['description'],
        "datePublished": date_published,
        "dateModified": date_modified,
        "url": canonical,
    }

    is_mobile_vendor = (
        restaurant['schemaType'] == 'FoodEstablishment'
        and restaurant.get('areaServed')
    )

    if is_mobile_vendor:
        obj['areaServed'] = restaurant['areaServed']
    else:
        addr = restaurant['address']
        obj['address'] = {
            "@type": "PostalAddress",
            "streetAddress": addr['streetAddress'],
            "addressLocality": addr['addressLocality'],
            "addressRegion": addr['addressRegion'],
            "postalCode": addr['postalCode'],
            "addressCountry": addr.get('addressCountry', 'US'),
        }

    obj['servesCuisine'] = restaurant['cuisine']

    # Optional fields, in template-snippet order
    if restaurant.get('phone'):
        obj['telephone'] = restaurant['phone']
    if restaurant.get('hours'):
        obj['openingHours'] = restaurant['hours']
    if restaurant.get('priceRange'):
        obj['priceRange'] = restaurant['priceRange']
    if restaurant.get('websiteURL'):
        obj['sameAs'] = restaurant['websiteURL']
    if restaurant.get('imageURL'):
        obj['image'] = restaurant['imageURL']
    if restaurant.get('geoLat') is not None and restaurant.get('geoLng') is not None:
        obj['geo'] = {
            "@type": "GeoCoordinates",
            "latitude": restaurant['geoLat'],
            "longitude": restaurant['geoLng'],
        }

    return obj


def build_multilocation_graph(restaurant, canonical, date_published, date_modified):
    """Build the @graph JSON-LD for a multi-location restaurant.

    A brand with five cafes is not one FoodEstablishment with an address;
    it is an Organization and five places. The flat shape had to pick one
    location's address for the top-level node, which made the other four
    addressless satellites hanging off `subOrganization`. Here every
    location — the primary included — is a first-class node with its own
    @id, address and hours, and the Organization holds only what is true
    of the brand.

    Each node's @id fragment is also the id of its section in the rendered
    HTML, so the structured data and the page point at the same anchors.
    """
    brand_url = restaurant.get('websiteURL')
    locations = resolve_locations(restaurant)

    brand = {
        "@type": "Organization",
        "@id": f"{canonical}#brand",
        "name": restaurant['name'],
        "description": restaurant['description'],
        "datePublished": date_published,
        "dateModified": date_modified,
        "mainEntityOfPage": canonical,
    }
    if brand_url:
        brand['url'] = brand_url
    same_as = restaurant.get('sameAs') or ([brand_url] if brand_url else None)
    if same_as:
        brand['sameAs'] = same_as
    brand['subOrganization'] = [
        {"@id": f"{canonical}#{loc['slug']}"} for loc in locations
    ]

    graph = [brand]
    for loc in locations:
        addr = loc['address']
        node = {
            "@type": restaurant['schemaType'],
            "@id": f"{canonical}#{loc['slug']}",
            "name": loc['name'],
            "parentOrganization": {"@id": f"{canonical}#brand"},
            "address": {
                "@type": "PostalAddress",
                "streetAddress": addr['streetAddress'],
                "addressLocality": addr['addressLocality'],
                "addressRegion": addr['addressRegion'],
                "postalCode": addr['postalCode'],
                "addressCountry": addr.get('addressCountry', 'US'),
            },
            "servesCuisine": restaurant['cuisine'],
        }
        if loc['phone']:
            node['telephone'] = loc['phone']
        if loc['hours']:
            node['openingHours'] = loc['hours']
            node['openingHoursSpecification'] = parse_opening_hours(
                loc['hours'], f"{restaurant['slug']}#{loc['slug']}"
            )
        node['hasMap'] = loc['mapsURL']
        url = loc['url'] or brand_url
        if url:
            node['url'] = url
        if restaurant.get('priceRange'):
            node['priceRange'] = restaurant['priceRange']
        graph.append(node)

    return {"@context": "https://schema.org", "@graph": graph}


# ---------------------------------------------------------------------------
# Step 4: future-proof slot comment blocks
# ---------------------------------------------------------------------------

def step_4_strip_future_proof_blocks(text):
    """Strip the badge-image and claim-CTA future-proof slot comments
    (template intentional decision #5). Each is a multi-line HTML comment
    plus a trailing blank line. Removed entirely until the corresponding
    workstream activates.
    """
    text = re.sub(
        r'                <!--\n\s+FUTURE-PROOF SLOT: badge image.*?                -->\n\n',
        '',
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = re.sub(
        r'            <!--\n\s+FUTURE-PROOF SLOT: claim CTA.*?            -->\n\n',
        '',
        text,
        count=1,
        flags=re.DOTALL,
    )
    return text


# ---------------------------------------------------------------------------
# Step 5: editorial body
# ---------------------------------------------------------------------------

def step_5_strip_editorial_body(text, restaurant):
    """Strip the EDITORIAL BODY commented-out block. If editorialBody is
    null (stub-then-flesh, page is in stub stage), also remove the
    `border-t border-gray-100 pt-6` styling from the INFO SIDEBAR outer
    div — the divider exists only to separate editorial copy from the
    sidebar, so it's redundant when there's no editorial copy.
    """
    text = re.sub(
        r'                    <!--\n\s+EDITORIAL BODY.*?                    -->\n\n',
        '',
        text,
        count=1,
        flags=re.DOTALL,
    )
    if restaurant.get('editorialBody') is None:
        text = text.replace(
            '<div class="border-t border-gray-100 pt-6">',
            '<div>',
            1,
        )
    return text


# ---------------------------------------------------------------------------
# Step 6: INFO SIDEBAR comment
# ---------------------------------------------------------------------------

def step_6_simplify_info_sidebar_comment(text):
    """Shorten the verbose INFO SIDEBAR comment to the simple form."""
    return text.replace(
        '<!-- INFO SIDEBAR (address always present; other fields conditional) -->',
        '<!-- INFO SIDEBAR -->',
        1,
    )


# ---------------------------------------------------------------------------
# Step 7: address vs area-served (fixed-location vs mobile-vendor)
# ---------------------------------------------------------------------------

def step_7_handle_address_section(text, restaurant):
    """Resolve the address-block conventions per intentional decision #9.

    Fixed-location:
      - Collapse the 2-line "REPLACE: address" + "For MOBILE VENDORS"
        instruction into a simple `<!-- Address -->`.
      - Strip the MOBILE VENDOR ALTERNATIVE comment block + leading blank.

    Multi-location (`locations` non-empty):
      - Drop the address block entirely; the Locations section carries
        every address, this one included.
      - Retitle the sidebar h2 "Good to know" so the heading still
        describes what remains under it (website, price).

    Mobile vendor (schemaType == FoodEstablishment AND areaServed populated):
      - Strip the address div + REPLACE/instruction comments.
      - Replace the MOBILE VENDOR ALTERNATIVE comment block with the
        active area-served HTML.
      - Change the h2 from "Where to find it" to "Area served".
    """
    is_mobile_vendor = (
        restaurant['schemaType'] == 'FoodEstablishment'
        and restaurant.get('areaServed')
    )

    if is_mobile_vendor:
        # Strip the fixed-address comment + instruction + address div
        text = re.sub(
            r'                        <!-- REPLACE: address \(always required for fixed-location restaurants\) -->\n'
            r'                        <!-- For MOBILE VENDORS:.*?intentional decision #9\. -->\n'
            r'                        <div class="mb-4">\n'
            r'                            <p class="text-brand-dark font-medium">\{\{StreetAddress\}\}</p>\n'
            r'                            <p class="text-brand-gray text-sm">\{\{AddressLocality\}\}, \{\{AddressRegion\}\} \{\{PostalCode\}\}</p>\n'
            r'                        </div>\n\n',
            '',
            text,
            count=1,
            flags=re.DOTALL,
        )
        # Change h2
        text = text.replace(
            '<h2 class="font-poppins font-bold text-lg text-brand-dark mb-4">Where to find it</h2>',
            '<h2 class="font-poppins font-bold text-lg text-brand-dark mb-4">Area served</h2>',
            1,
        )
        # Replace the MOBILE VENDOR ALTERNATIVE comment block with active HTML
        text = re.sub(
            r'                        <!--\n\s+MOBILE VENDOR ALTERNATIVE.*?                        -->\n',
            '                        <!-- Area served -->\n'
            '                        <div class="mb-4">\n'
            '                            <p class="text-brand-dark font-medium">{{AreaServed}}</p>\n'
            '                        </div>\n',
            text,
            count=1,
            flags=re.DOTALL,
        )
    elif restaurant.get('locations'):
        # Multi-location: every address, including this one, is rendered in
        # the Locations section below. Showing one of them here under
        # "Where to find it" would state a fact twice and imply the brand
        # has a single home. The heading becomes "Good to know" for what
        # is left: website and price, both brand-level facts.
        text = re.sub(
            r'                        <!-- REPLACE: address \(always required for fixed-location restaurants\) -->\n'
            r'                        <!-- For MOBILE VENDORS:.*?intentional decision #9\. -->\n'
            r'                        <div class="mb-4">\n'
            r'                            <p class="text-brand-dark font-medium">\{\{StreetAddress\}\}</p>\n'
            r'                            <p class="text-brand-gray text-sm">\{\{AddressLocality\}\}, \{\{AddressRegion\}\} \{\{PostalCode\}\}</p>\n'
            r'                        </div>\n\n',
            '',
            text,
            count=1,
            flags=re.DOTALL,
        )
        text = text.replace(
            '<h2 class="font-poppins font-bold text-lg text-brand-dark mb-4">Where to find it</h2>',
            '<h2 class="font-poppins font-bold text-lg text-brand-dark mb-4">Good to know</h2>',
            1,
        )
        text = _strip_mobile_vendor_block(text)

    else:
        # Fixed-location: simplify the address comment header
        text = re.sub(
            r'                        <!-- REPLACE: address \(always required for fixed-location restaurants\) -->\n'
            r'                        <!-- For MOBILE VENDORS:.*?intentional decision #9\. -->\n',
            '                        <!-- Address -->\n',
            text,
            count=1,
            flags=re.DOTALL,
        )
        text = _strip_mobile_vendor_block(text)

    return text


def _strip_mobile_vendor_block(text):
    """Remove the MOBILE VENDOR ALTERNATIVE comment block + its leading
    blank line, so siblings stay single-blank-spaced.
    """
    return re.sub(
        r'\n                        <!--\n\s+MOBILE VENDOR ALTERNATIVE.*?                        -->\n',
        '',
        text,
        count=1,
        flags=re.DOTALL,
    )


# ---------------------------------------------------------------------------
# Step 8: optional sidebar blocks (hours, phone, website, price range)
# ---------------------------------------------------------------------------

def step_8_handle_optional_sidebar_blocks(text, restaurant):
    """For each optional sidebar block:
      - If data has the field, replace the comment block with rendered HTML.
      - If data lacks the field, remove the comment block + a leading blank
        line so we don't end up with double blanks between siblings.

    Order: hours, phone, website, price range (matches template order).

    Multi-location pages suppress the hours and phone blocks for the same
    reason they suppress the address: those are facts about one location,
    and each location states its own in the Locations section. Website and
    price describe the brand, so they stay here — visible exactly once.
    """
    is_multi = bool(restaurant.get('locations'))

    text = _handle_one_block(
        text,
        comment_marker='OPTIONAL: hours block',
        rendered=(
            build_hours_block(restaurant['hoursHumanReadable'])
            if restaurant.get('hoursHumanReadable') and not is_multi else None
        ),
    )
    text = _handle_one_block(
        text,
        comment_marker='OPTIONAL: phone block',
        rendered=(
            build_phone_block(restaurant['phone'])
            if restaurant.get('phone') and not is_multi else None
        ),
    )
    text = _handle_one_block(
        text,
        comment_marker='OPTIONAL: website block',
        rendered=build_website_block(restaurant['websiteURL']) if restaurant.get('websiteURL') else None,
    )
    text = _handle_one_block(
        text,
        comment_marker='OPTIONAL: price range block',
        rendered=build_price_block(restaurant['priceRange']) if restaurant.get('priceRange') else None,
    )

    if is_multi and not restaurant.get('websiteURL') and not restaurant.get('priceRange'):
        # Nothing brand-level left to show: drop the card rather than ship a
        # heading over an empty box.
        text = _strip_empty_info_card(text)

    return text


def _strip_empty_info_card(text):
    """Remove the whole MAIN CONTENT CARD when its sidebar rendered empty."""
    return re.sub(
        r'            <!-- MAIN CONTENT CARD -+ -->\n'
        r'            <div class="bg-white.*?\n            </div>\n\n',
        '',
        text,
        count=1,
        flags=re.DOTALL,
    )


def _handle_one_block(text, *, comment_marker, rendered):
    """Replace one optional-block comment region with `rendered` HTML, or
    strip it (plus a leading blank line) if rendered is None.
    """
    pattern = (
        r'                        <!--\n\s+' + re.escape(comment_marker) +
        r'.*?                        -->\n'
    )
    if rendered is not None:
        return re.sub(pattern, rendered, text, count=1, flags=re.DOTALL)
    # Strip the block + the leading blank line (so siblings stay single-blank-spaced)
    return re.sub(r'\n' + pattern, '', text, count=1, flags=re.DOTALL)


def build_hours_block(hours_human_readable):
    """Render the hours sidebar block. Converts `\\n` separators to
    `<br>\\n` + 32-space continuation indent (the indent inside the <p>).
    Note: the template's commented version uses class `whitespace-pre-line`;
    the rendered version uses explicit <br> tags instead, so that class is
    intentionally NOT included in the output.
    """
    lines = hours_human_readable.split('\n')
    indented_content = '<br>\n                                '.join(lines)
    return (
        '                        <!-- Hours -->\n'
        '                        <div class="mb-4">\n'
        '                            <p class="text-brand-gray text-xs uppercase tracking-wide mb-1">Hours</p>\n'
        '                            <p class="text-brand-dark text-sm">\n'
        f'                                {indented_content}\n'
        '                            </p>\n'
        '                        </div>\n'
    )


def build_phone_block(phone_e164):
    """Render the phone sidebar block. The tel: href uses E.164 format
    directly (per RFC 3966); the visible link text uses formatted display
    `(AAA) PPP-NNNN`.
    """
    phone_display = format_phone_display(phone_e164)
    return (
        '                        <!-- Phone -->\n'
        '                        <div class="mb-4">\n'
        '                            <p class="text-brand-gray text-xs uppercase tracking-wide mb-1">Phone</p>\n'
        '                            <p class="text-brand-dark text-sm">\n'
        f'                                <a href="tel:{phone_e164}" class="hover:text-brand-orange transition-colors">{phone_display}</a>\n'
        '                            </p>\n'
        '                        </div>\n'
    )


def format_phone_display(phone_e164):
    """Convert E.164 `+1-AAA-PPP-NNNN` to display `(AAA) PPP-NNNN`."""
    if phone_e164.startswith('+1-'):
        rest = phone_e164[3:]
        parts = rest.split('-')
        if len(parts) == 3:
            return f'({parts[0]}) {parts[1]}-{parts[2]}'
    return phone_e164


def _format_website_display(website_url):
    """Strip scheme (`https://` or `http://`) and trailing slash for cleaner
    display. Shared by the brand-level sidebar block and the per-location
    card website row.
    """
    display = website_url
    if display.startswith('https://'):
        display = display[len('https://'):]
    elif display.startswith('http://'):
        display = display[len('http://'):]
    if display.endswith('/'):
        display = display[:-1]
    return display


def build_website_block(website_url):
    """Render the website sidebar block. The href uses the full URL as-is;
    the visible link text strips the scheme (`https://` or `http://`) and
    any trailing slash for cleaner display.
    """
    display = _format_website_display(website_url)
    return (
        '                        <!-- Website -->\n'
        '                        <div class="mb-4">\n'
        '                            <p class="text-brand-gray text-xs uppercase tracking-wide mb-1">Website</p>\n'
        '                            <p class="text-brand-dark text-sm break-all">\n'
        f'                                <a href="{website_url}" rel="noopener" target="_blank" class="text-brand-orange hover:underline">{display}</a>\n'
        '                            </p>\n'
        '                        </div>\n'
    )


def build_price_block(price_range):
    """Render the price-range sidebar block."""
    return (
        '                        <!-- Price range -->\n'
        '                        <div class="mb-4">\n'
        '                            <p class="text-brand-gray text-xs uppercase tracking-wide mb-1">Price</p>\n'
        f'                            <p class="text-brand-dark text-sm">{price_range}</p>\n'
        '                        </div>\n'
    )


# ---------------------------------------------------------------------------
# Step 9: OTHER LOCATIONS placeholder (multi-loc only)
# ---------------------------------------------------------------------------

def step_9_handle_locations_section(text, restaurant):
    """Resolve the LOCATIONS placeholder block per DECISIONS #17.

    Single-loc (no `locations` field, or empty array): strip the entire
    commented placeholder block + leading blank line. Output is byte-equal
    to the pre-template-edit state — single-loc rendering is unchanged.

    Multi-loc: replace the placeholder with the active "Locations"
    section, one card per location in data order, the primary first. Each
    card carries id="{slug}", which is the fragment its JSON-LD node uses
    as @id, so a link to a location's structured-data identity lands on
    that location's card. Neighborhood, phone, hours and own-URL rows are
    conditional — dropped when the field is absent, per the
    "empty-or-omitted, NOT placeholder" convention from template
    intentional decision #2.
    """
    locations = resolve_locations(restaurant)
    if not locations:
        return re.sub(
            r'\n            <!--\n\s+LOCATIONS BLOCK.*?            -->\n',
            '',
            text,
            count=1,
            flags=re.DOTALL,
        )

    cards = '\n'.join(_render_location_card(loc) for loc in locations)
    section = (
        '            <section class="border-t border-gray-100 pt-8">\n'
        '                <h2 class="font-poppins font-bold text-2xl text-brand-dark mb-6">Locations</h2>\n'
        '                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">\n'
        f'{cards}\n'
        '                </div>\n'
        '            </section>\n'
    )
    return re.sub(
        r'            <!--\n\s+LOCATIONS BLOCK.*?            -->\n',
        section,
        text,
        count=1,
        flags=re.DOTALL,
    )


def _render_location_card(loc):
    """Render one LOCATION_CARD <div> for a location resolved by
    resolve_locations(). Optional rows are dropped when absent.

    scroll-mt-24 keeps a card clear of the sticky header when reached by
    its #fragment.
    """
    addr = loc['address']
    heading_margin = 'mb-1' if loc['neighborhood'] else 'mb-3'
    lines = [
        f'                    <div id="{loc["slug"]}" class="border border-gray-100 rounded-lg p-5 scroll-mt-24">',
        f'                        <h3 class="font-poppins font-semibold text-lg text-brand-dark {heading_margin}">{loc["name"]}</h3>',
    ]
    if loc['neighborhood']:
        lines.append(
            f'                        <p class="text-brand-gray text-xs uppercase tracking-wide mb-3">{loc["neighborhood"]}</p>'
        )
    lines.extend([
        '                        <address class="not-italic mb-3">',
        f'                            <p class="text-brand-dark font-medium">{addr["streetAddress"]}</p>',
        f'                            <p class="text-brand-gray text-sm">{addr["addressLocality"]}, {addr["addressRegion"]} {addr["postalCode"]}</p>',
        '                        </address>',
    ])
    if loc['phone']:
        phone_tel = loc['phone'].replace('-', '')
        phone_display = format_phone_display(loc['phone'])
        lines.append(
            f'                        <p class="text-brand-gray text-sm mb-2"><a href="tel:{phone_tel}" class="hover:text-brand-orange">{phone_display}</a></p>'
        )
    if loc['hoursHumanReadable']:
        lines.append(
            f'                        <p class="text-brand-gray text-sm whitespace-pre-line mb-2">{loc["hoursHumanReadable"]}</p>'
        )
    lines.append(
        f'                        <p class="text-brand-gray text-sm mb-2"><a href="{loc["mapsURL"]}" rel="noopener" target="_blank" class="text-brand-orange hover:underline">Directions</a></p>'
    )
    if loc['url']:
        lines.append(
            f'                        <p class="text-brand-gray text-sm break-all"><a href="{loc["url"]}" rel="noopener" target="_blank" class="hover:text-brand-orange">{_format_website_display(loc["url"])}</a></p>'
        )
    lines.append('                    </div>')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Step 10: APPEARS ON repeating-row comment
# ---------------------------------------------------------------------------

def step_10_strip_appears_on_repeating_comment(text):
    """Strip the REPEATING ROW guidance comment from the APPEARS ON section.
    The placeholder substitution for the actual entries happens in step 13.
    """
    return re.sub(
        r'                    <!--\n\s+REPEATING ROW.*?                    -->\n',
        '',
        text,
        count=1,
        flags=re.DOTALL,
    )


# ---------------------------------------------------------------------------
# Step 11: section-level REPLACE comments (with separator dashes)
# ---------------------------------------------------------------------------

def step_11_transform_section_replace_comments(text):
    """For section-level REPLACE comments (`<!-- REPLACE: <text> ---- -->`),
    strip the "REPLACE: " prefix and add 9 dashes (the prefix length) so
    the comment line keeps the same total width as the surrounding KEEP
    comments.
    """
    def repl(m):
        prefix = m.group(1)  # "<!-- "
        body = m.group(2)    # text content (no dashes), with trailing space
        dashes = m.group(3)  # existing dashes
        suffix = m.group(4)  # " -->"
        return f'{prefix}{body}{dashes}---------{suffix}'
    return re.sub(r'(<!-- )REPLACE: ([^-]+)(-+)( -->)', repl, text)


# ---------------------------------------------------------------------------
# Step 12: inline REPLACE comments (no separator dashes)
# ---------------------------------------------------------------------------

def step_12_transform_inline_replace_comments(text):
    """For inline REPLACE comments (`<!-- REPLACE: <text> -->`, no dashes),
    strip the "REPLACE: " prefix and capitalize the first letter of the
    content. Other casing is preserved (e.g., "REPLACE: Updated [Month
    Year] pill" stays "Updated [Month Year] pill").
    """
    def repl(m):
        content = m.group(1)
        if content:
            content = content[0].upper() + content[1:]
        return f'<!-- {content} -->'
    return re.sub(r'<!-- REPLACE: ([^>]+?) -->', repl, text)


# ---------------------------------------------------------------------------
# Step 13: substitute remaining placeholders
# ---------------------------------------------------------------------------

def step_13_substitute_remaining_placeholders(text, restaurant):
    """Replace all simple `{{Placeholder}}` occurrences in the visible HTML
    with values from the restaurant data. Also handles the AppearsOn
    placeholders (one or more entries; the template's single-entry <li> is
    cloned per entry).
    """
    # AppearsOn entries (one or more)
    appears_on = restaurant.get('appearsOn', [])
    if appears_on:
        text = _render_appears_on_entries(text, appears_on)

    # Required scalar fields
    text = text.replace('{{slug}}', restaurant['slug'])
    text = text.replace('{{RestaurantName}}', restaurant['name'])

    # Cuisine — surface-aware resolution per DECISIONS #18.
    #   None → suppression (drop the cuisine slot from titles + hero subtitle)
    #   string → substitute (the displayCuisine override or raw cuisine)
    # JSON-LD `servesCuisine` is built in step_3 from raw `cuisine` and is
    # NOT affected by this resolution.
    display_cuisine = _resolve_display_cuisine(restaurant)

    # When both cuisine (display) and neighborhood are absent, drop the
    # subtitle <p> block entirely. Without this, the cuisine-suppression
    # and null-neighborhood passes below leave an empty <p> in the hero.
    # Live case: Toni's Detroit Style Pizza — name-contains-cuisine
    # auto-suppresses cuisine (DECISIONS #18), and neighborhood is
    # deliberately null for commercial-corridor addresses without a
    # clear sub-neighborhood label.
    if display_cuisine is None and not restaurant.get('neighborhood'):
        # Note: comment matches the post-step-12 form (REPLACE: prefix
        # stripped, first letter capitalized), since step_13 runs after
        # step_12 in the pipeline.
        text = re.sub(
            r'\n                <!-- Cuisine \+ neighborhood subtitle -->\n'
            r'                <p class="text-brand-gray mt-4 text-lg font-medium">\n'
            r'                    \{\{Cuisine\}\} · \{\{Neighborhood\}\}\n'
            r'                </p>\n',
            '',
            text,
            count=1,
        )

    if display_cuisine is None:
        text = text.replace(' — {{Cuisine}}', '')
        text = text.replace('{{Cuisine}} · {{Neighborhood}}', '{{Neighborhood}}')
        text = text.replace('{{Cuisine}}', '')
    else:
        text = text.replace('{{Cuisine}}', display_cuisine)

    text = text.replace('{{Tagline}}', restaurant['tagline'])
    text = text.replace('{{MonthYear}}', restaurant['monthYear'])
    text = text.replace('{{Description}}', restaurant['description'])
    text = text.replace('{{ShareTagline}}', restaurant['shareTagline'])
    text = text.replace('{{Keywords}}', restaurant['keywords'])

    if restaurant.get('neighborhood'):
        text = text.replace('{{Neighborhood}}', restaurant['neighborhood'])
    else:
        # Drop the " · {{Neighborhood}}" segment from the hero subtitle
        # so the cuisine line stands alone (no dangling separator).
        text = text.replace(' · {{Neighborhood}}', '')
        # Also drop any standalone {{Neighborhood}} that the cuisine-suppression
        # path may have left when both cuisine and neighborhood are absent
        # (Toni's Detroit Style Pizza is the live case — cuisine auto-suppressed
        # because name contains it, and neighborhood is null because the Mt Pleasant
        # primary location doesn't have one in the dataset). The line above only
        # catches " · {{Neighborhood}}"; this catches the leading-separator-gone form.
        text = text.replace('{{Neighborhood}}', '')

    addr = restaurant.get('address') or {}
    if addr.get('streetAddress'):
        text = text.replace('{{StreetAddress}}', addr['streetAddress'])
    if addr.get('addressLocality'):
        text = text.replace('{{AddressLocality}}', addr['addressLocality'])
    if addr.get('addressRegion'):
        text = text.replace('{{AddressRegion}}', addr['addressRegion'])
    if addr.get('postalCode'):
        text = text.replace('{{PostalCode}}', addr['postalCode'])

    if restaurant.get('areaServed'):
        text = text.replace('{{AreaServed}}', restaurant['areaServed'])

    return text


def _render_appears_on_entries(text, appears_on):
    """Clone the template's single-entry <li> block per appearsOn entry.
    Preserves byte-equality with the prior single-entry implementation when
    len(appears_on) == 1.
    """
    li_pattern = re.compile(
        r'                    <li>\n                        <a href="\{\{AppearsOn1\.RankingURL\}\}".*?                    </li>',
        re.DOTALL,
    )
    li_template = (
        '                    <li>\n'
        '                        <a href="{url}" class="inline-flex items-center text-brand-orange hover:underline font-medium">\n'
        '                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">\n'
        '                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />\n'
        '                            </svg>\n'
        '                            {title}\n'
        '                        </a>\n'
        '                    </li>'
    )
    rendered = '\n'.join(li_template.format(url=e['url'], title=e['title']) for e in appears_on)
    return li_pattern.sub(rendered, text, count=1)


# ---------------------------------------------------------------------------
# Step 14: multi-location <title>
# ---------------------------------------------------------------------------

def step_14_apply_multilocation_title(text, restaurant):
    """Retitle multi-location pages.

    Nobody searches a five-cafe brand as "<Name> — <Cuisine> in
    Charleston"; they search it for where the cafes are and when they are
    open. Multi-location pages default to "<Name> Locations & Hours |
    Voted On By Locals"; `titleOverride` replaces that outright when a
    record needs different wording.

    Only <title> changes. og:title, twitter:title and the meta
    description keep the conventions they already have.

    Runs last, after step 13 has resolved the placeholders inside the
    original <title>, so this replaces a fully rendered line.
    """
    if not restaurant.get('locations'):
        return text
    title = restaurant.get('titleOverride') or (
        f"{restaurant['name']} Locations & Hours | Voted On By Locals"
    )
    return re.sub(
        r'<title>.*?</title>',
        lambda _m: f'<title>{title}</title>',
        text,
        count=1,
        flags=re.DOTALL,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Generate a restaurant detail page from the template + data.'
    )
    parser.add_argument('slug', nargs='?', help='Restaurant slug (e.g., park-pizza-co)')
    parser.add_argument('--all', action='store_true', help='Generate every restaurant in restaurants.json')
    parser.add_argument('--output', help='Output path (default: restaurants/{slug}.html)')
    args = parser.parse_args()

    if not args.all and not args.slug:
        parser.error('Provide a slug or use --all')
    if args.all and args.output:
        parser.error('--output is not allowed with --all')

    template = TEMPLATE_PATH.read_text(encoding='utf-8')
    with DATA_PATH.open(encoding='utf-8') as f:
        data = json.load(f)

    restaurants = data['restaurants']

    if args.all:
        for r in restaurants:
            out_path = ROOT / 'restaurants' / f"{r['slug']}.html"
            _write_lf(out_path, generate(template, r))
            print(f'Wrote {out_path}')
    else:
        r = next((x for x in restaurants if x['slug'] == args.slug), None)
        if r is None:
            sys.exit(f"Slug '{args.slug}' not found in {DATA_PATH}")
        out_path = Path(args.output) if args.output else ROOT / 'restaurants' / f"{args.slug}.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        _write_lf(out_path, generate(template, r))
        print(f'Wrote {out_path}')


def _write_lf(path, content):
    """Write content with LF line endings (override Windows CRLF default).
    The reference page is LF; emitting CRLF would break byte-for-byte parity.
    """
    with path.open('w', encoding='utf-8', newline='\n') as f:
        f.write(content)


if __name__ == '__main__':
    main()
