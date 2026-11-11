#!/usr/bin/env python3
"""Insert the TCM Way Kitchen Pharmacy CTA into article HTML.

The operation is idempotent: files containing the marker are skipped.
"""

from __future__ import annotations

import argparse
import html
from pathlib import Path
from urllib.parse import urlencode


MARKER = "data-tcmway-newsletter-cta"
BASE_URL = "https://tcmway.net/kitchen-pharmacy/"


def cta_block(slug: str) -> str:
    query = urlencode(
        {
            "utm_source": "tcmway",
            "utm_medium": "article_cta",
            "utm_campaign": "kitchen_pharmacy",
            "utm_content": slug,
        }
    ).replace("&", "&amp;")
    target = f"{BASE_URL}?{query}"
    safe_slug = html.escape(slug, quote=True)
    return f"""
<aside {MARKER}="article" data-article-slug="{safe_slug}"
       style="margin:2.5rem 0;padding:1.45rem 1.55rem;border:1px solid #e4cfb8;border-left:5px solid #b83a2a;border-radius:4px 18px 4px 18px;background:#fffaf3;color:#3b2a1a;">
  <p style="margin:0 0 .45rem;color:#b83a2a;font-family:-apple-system,'Helvetica Neue',sans-serif;font-size:.72rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;">Free practical guide</p>
  <h2 style="margin:0 0 .55rem;font-size:1.35rem;font-weight:normal;line-height:1.25;">The 7-Day Kitchen Pharmacy</h2>
  <p style="margin:0 0 1rem;color:#7a5c45;font-size:.94rem;line-height:1.65;">Seven familiar ingredients, seven five-minute rituals, and an honest note on what tradition and evidence each actually support.</p>
  <p style="margin:0;"><a href="{target}" data-cta="kitchen_pharmacy" data-article-slug="{safe_slug}" style="display:inline-block;padding:.72rem 1.15rem;border-radius:6px;background:#b83a2a;color:#fff;font-family:-apple-system,'Helvetica Neue',sans-serif;font-size:.9rem;font-weight:600;text-decoration:none;">Get the free guide →</a></p>
  <p style="margin:.75rem 0 0;color:#7a5c45;font-size:.78rem;">No supplement purchase required. Unsubscribe anytime.</p>
</aside>
"""


def insert_block(text: str, block: str) -> tuple[str, bool]:
    if MARKER in text:
        return text, False

    anchors = [
        '<div class="medical-disclaimer"',
        "<!-- RELATED POSTS -->",
        "</article>",
    ]
    for anchor in anchors:
        position = text.find(anchor)
        if position >= 0:
            return text[:position] + block + "\n" + text[position:], True
    raise ValueError("no supported insertion anchor found")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--slugs", nargs="+", required=True)
    args = parser.parse_args()

    changed: list[str] = []
    skipped: list[str] = []
    for slug in args.slugs:
        path = args.root / "posts" / f"{slug}.html"
        if not path.is_file():
            raise SystemExit(f"missing post: {path}")
        original = path.read_text(encoding="utf-8")
        updated, did_change = insert_block(original, cta_block(slug))
        if not did_change:
            skipped.append(slug)
            continue
        changed.append(slug)
        if not args.dry_run:
            path.write_text(updated, encoding="utf-8")

    print(f"mode={'dry-run' if args.dry_run else 'write'}")
    print(f"changed={len(changed)}")
    for slug in changed:
        print(f"CHANGED {slug}")
    print(f"skipped={len(skipped)}")
    for slug in skipped:
        print(f"SKIPPED {slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
