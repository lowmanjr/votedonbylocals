"""Shared helpers for cuisine-name redundancy dedup.

Used by both `generate_detail_page.py` (mechanical display surfaces in the
HTML body) and `generate_og_images.py` (OG image rendered meta-line).

Resolution order at render time (per DECISIONS #18 and the 2026-05-05
design pass):
  1. If `displayCuisine` field is non-null, use that.
  2. Else if normalized cuisine is a substring of normalized name → suppress
     cuisine in mechanical display surfaces (return None).
  3. Else use `cuisine` as-is.

Mechanical surfaces only — JSON-LD `servesCuisine` always uses raw `cuisine`
to keep the entity-resolution signal intact.
"""

import re
import unicodedata


def _normalize_for_match(text):
    """Lowercase, NFD-strip-diacritics, & → and, strip punctuation,
    collapse whitespace. Used to detect cuisine-name redundancy.
    """
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.replace('&', ' and ')
    text = re.sub(r"['’]", '', text)  # straight + curly apostrophes
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _should_suppress_cuisine(name, cuisine):
    """True when normalized cuisine is a substring of normalized name."""
    return _normalize_for_match(cuisine) in _normalize_for_match(name)


def _resolve_display_cuisine(restaurant):
    """Return the cuisine string for display surfaces, or None to suppress.

    None means the rendering layer should drop the cuisine slot entirely
    (collapsing " — Cuisine in Charleston" to " in Charleston" in titles
    and "Cuisine · Neighborhood" to "Neighborhood" in subtitle/meta-line
    surfaces).
    """
    override = restaurant.get('displayCuisine')
    if override is not None:
        return override
    if _should_suppress_cuisine(restaurant['name'], restaurant['cuisine']):
        return None
    return restaurant['cuisine']
