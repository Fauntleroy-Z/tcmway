#!/usr/bin/env python3
"""Add shared mobile accessibility structure to TCM Way pages.

This migration is intentionally idempotent. It:
1. wraps page content in a single <main id="main-content"> landmark;
2. loads /css/mobile-accessibility.css after inline page styles;
3. sets listen.js cache keys for the accessibility and Hub CTA releases.

Usage:
  python3 scripts/mobile-a11y-migrate.py --check
  python3 scripts/mobile-a11y-migrate.py --write
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS_LINK = '<link rel="stylesheet" href="/css/mobile-accessibility.css?v=20261118-a11y">'
LISTEN_VERSION = "20261118-a11y"
HUB_LISTEN_VERSION = "20261128-hub-cta"

BODY_RE = re.compile(r"<body\b[^>]*>", re.IGNORECASE)
BODY_END_RE = re.compile(r"</body\s*>", re.IGNORECASE)
HEAD_END_RE = re.compile(r"</head\s*>", re.IGNORECASE)
HEADER_END_RE = re.compile(r"</header\s*>", re.IGNORECASE)
FOOTER_RE = re.compile(r"<footer\b", re.IGNORECASE)
MAIN_RE = re.compile(r"<main\b", re.IGNORECASE)
MAIN_OPEN_RE = re.compile(r"<main\b([^>]*)>", re.IGNORECASE)
CSS_RE = re.compile(r'href=["\']/css/mobile-accessibility\.css(?:\?[^"\']*)?["\']', re.IGNORECASE)
LISTEN_RE = re.compile(r'(/js/listen\.js\?v=)([^"\']+)', re.IGNORECASE)
BAIDU_RE = re.compile(
    r"\n?<script>\s*var _hmt = _hmt \|\| \[\];.*?hm\.baidu\.com.*?</script>\s*",
    re.IGNORECASE | re.DOTALL,
)
FIRST_COMIC_RE = re.compile(
    r'<img\b[^>]*class="[^"]*\bcomic-break\b[^"]*"[^>]*>',
    re.IGNORECASE,
)


def migrate_html(path: Path, text: str) -> tuple[str, list[str]]:
    changes: list[str] = []

    body = BODY_RE.search(text)
    body_end = BODY_END_RE.search(text)
    existing_main = MAIN_RE.search(text)
    if body and body_end and not existing_main:
        header_end = HEADER_END_RE.search(text, body.end(), body_end.start())
        footer = FOOTER_RE.search(text, body.end(), body_end.start())
        start = header_end.end() if header_end else body.end()
        end = footer.start() if footer else body_end.start()
        if start >= end:
            raise ValueError(f"{path}: cannot determine main content bounds")
        text = text[:start] + '\n<main id="main-content">\n' + text[start:end] + "\n</main>\n" + text[end:]
        changes.append("main")

    main_open = MAIN_OPEN_RE.search(text)
    if main_open and "id=" not in main_open.group(1):
        replacement = f'<main id="main-content"{main_open.group(1)}>'
        text = text[:main_open.start()] + replacement + text[main_open.end():]
        changes.append("main-id")

    head_end = HEAD_END_RE.search(text)
    if head_end and not CSS_RE.search(text):
        text = text[:head_end.start()] + CSS_LINK + "\n" + text[head_end.start():]
        changes.append("css")

    listen_version = HUB_LISTEN_VERSION if ' data-hub-cta="' in text else LISTEN_VERSION

    def replace_listen(match: re.Match[str]) -> str:
        if match.group(2) == listen_version:
            return match.group(0)
        return match.group(1) + listen_version

    bumped, _ = LISTEN_RE.subn(replace_listen, text)
    count = sum(
        1
        for match in LISTEN_RE.finditer(text)
        if match.group(2) != listen_version
    )
    if count:
        text = bumped
        changes.append(f"listen-version:{count}")

    text, baidu_count = BAIDU_RE.subn("\n", text)
    if baidu_count:
        changes.append(f"remove-baidu-analytics:{baidu_count}")

    comic = FIRST_COMIC_RE.search(text)
    if comic:
        tag = comic.group(0)
        if 'fetchpriority="high"' not in tag or 'loading="lazy"' in tag:
            tag = re.sub(r'\sloading="lazy"', ' loading="eager"', tag, flags=re.IGNORECASE)
            if 'fetchpriority="high"' not in tag:
                tag = tag[:-1] + ' fetchpriority="high">'
            text = text[:comic.start()] + tag + text[comic.end():]
            changes.append("first-comic-priority")

    return text, changes


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    pending: list[tuple[Path, list[str]]] = []
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts or ".hermes" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        migrated, changes = migrate_html(path, text)
        if changes:
            pending.append((path, changes))
            if args.write:
                path.write_text(migrated, encoding="utf-8")

    for path, changes in pending:
        print(f"{path.relative_to(ROOT)}: {', '.join(changes)}")
    print(f"{'pending' if args.check else 'migrated'}: {len(pending)} files")

    if args.check and pending:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
