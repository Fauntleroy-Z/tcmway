#!/usr/bin/env python3
"""Verify article share widgets without changing published content.

Checks:
- Twitter and Reddit share targets equal the page canonical URL.
- Optional Email sharing has a subject and a body equal to canonical.
- mailto URLs are ASCII and have no raw spaces/non-ASCII characters.
- The same Email subject is never reused across different articles.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse


SHARE_BLOCK_RE = re.compile(
    r"<p\b[^>]*>(?:(?!</p>).)*?Share on\s*<a\b(?:(?!</p>).)*?</p>",
    re.IGNORECASE | re.DOTALL,
)
ANCHOR_RE = re.compile(
    r'<a\b[^>]*\bhref=(["\'])(.*?)\1[^>]*>(.*?)</a>',
    re.IGNORECASE | re.DOTALL,
)
CANONICAL_TAG_RE = re.compile(
    r'<link\b[^>]*\brel=["\']canonical["\'][^>]*>',
    re.IGNORECASE,
)
CANONICAL_HREF_RE = re.compile(r'\bhref=["\']([^"\']+)["\']', re.IGNORECASE)
PLATFORM_MARKERS = {
    "twitter": "twitter.com/intent/tweet",
    "reddit": "reddit.com/submit",
}


def _query_value(url: str, key: str) -> str:
    values = parse_qs(urlparse(url).query, keep_blank_values=True).get(key)
    return values[0] if values else ""


def _uri_encoding_error(value: str) -> str | None:
    if any(ord(ch) > 127 for ch in value):
        return "contains non-ASCII characters"
    if any(ch.isspace() for ch in value):
        return "contains raw whitespace"
    for match in re.finditer("%", value):
        if not re.fullmatch(r"[0-9A-Fa-f]{2}", value[match.start() + 1 : match.start() + 3]):
            return "contains an invalid percent escape"
    return None


def validate_fragment(name: str, source: str) -> tuple[list[str], tuple[str, str] | None]:
    """Return issues and optional (canonical, email_subject)."""
    canonical_tag = CANONICAL_TAG_RE.search(source)
    canonical_href = CANONICAL_HREF_RE.search(canonical_tag.group(0)) if canonical_tag else None
    if not canonical_href:
        return [f"{name}: missing canonical URL"], None

    canonical = html.unescape(canonical_href.group(1)).strip()
    share_match = SHARE_BLOCK_RE.search(source)
    if not share_match:
        return [], None

    issues: list[str] = []
    anchors = []
    for quote, raw_href, _label in ANCHOR_RE.findall(share_match.group(0)):
        del quote
        anchors.append((raw_href, html.unescape(raw_href)))

    for platform, marker in PLATFORM_MARKERS.items():
        candidates = [(raw, decoded) for raw, decoded in anchors if marker in decoded]
        if not candidates:
            issues.append(f"{name}: {platform} share link missing")
            continue
        _raw, decoded = candidates[0]
        target = _query_value(decoded, "url")
        if target != canonical:
            issues.append(f"{name}: {platform} target {target or '<empty>'} != {canonical}")

    email_links = [(raw, decoded) for raw, decoded in anchors if decoded.lower().startswith("mailto:")]
    if not email_links:
        return issues, None

    raw_email, email_url = email_links[0]
    encoding_error = _uri_encoding_error(raw_email)
    if encoding_error:
        issues.append(f"{name}: Email share URI {encoding_error}")

    subject = _query_value(email_url, "subject").strip()
    body = _query_value(email_url, "body").strip()
    if not subject:
        issues.append(f"{name}: Email subject missing")
    if body != canonical:
        issues.append(f"{name}: Email body {body or '<empty>'} != {canonical}")
    return issues, ((canonical, subject) if subject else None)


def _self_test() -> None:
    good = """
    <link rel="canonical" href="https://tcmway.net/posts/good.html">
    <p>Share on
      <a href="https://twitter.com/intent/tweet?url=https://tcmway.net/posts/good.html">Twitter</a>
      <a href="https://reddit.com/submit?url=https://tcmway.net/posts/good.html">Reddit</a>
      <a href="mailto:?subject=Good%20Article&body=https://tcmway.net/posts/good.html">Email</a>
    </p>
    """
    bad = """
    <link rel="canonical" href="https://tcmway.net/posts/good.html">
    <p>Share on
      <a href="https://twitter.com/intent/tweet?url=https://tcmway.net/posts/wrong.html">Twitter</a>
      <a href="https://reddit.com/submit?url=https://tcmway.net/posts/good.html">Reddit</a>
      <a href="mailto:?subject=Raw Subject&body=">Email</a>
    </p>
    """
    good_issues, good_info = validate_fragment("good.html", good)
    bad_issues, _ = validate_fragment("bad.html", bad)
    if good_issues or not good_info:
        raise AssertionError(f"valid fixture failed: {good_issues}")
    expected = ("twitter target", "raw whitespace", "Email body")
    if not all(any(fragment in issue for issue in bad_issues) for fragment in expected):
        raise AssertionError(f"invalid fixture was not caught: {bad_issues}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        _self_test()
        print("✅ share widget validator self-test PASS")
        return 0

    posts_dir = Path(__file__).resolve().parent.parent / "posts"
    files = sorted(posts_dir.glob("*.html"))
    if not files:
        print(f"🔴 no HTML posts found under {posts_dir}", file=sys.stderr)
        return 1

    errors: list[str] = []
    subjects: dict[str, str] = {}
    share_widget_count = 0
    email_widget_count = 0
    for path in files:
        source = path.read_text(encoding="utf-8", errors="replace")
        if SHARE_BLOCK_RE.search(source):
            share_widget_count += 1
        issues, info = validate_fragment(path.name, source)
        if issues:
            errors.extend(issues)
        if info:
            email_widget_count += 1
            canonical, subject = info
            previous = subjects.get(subject)
            if previous and previous != canonical:
                errors.append(
                    f"{path.name}: Email subject reused across articles: "
                    f"{previous} and {canonical}"
                )
            else:
                subjects[subject] = canonical

    if errors:
        print(f"🔴 article share widget verification failed ({len(errors)} issue(s))")
        for issue in errors:
            print(f"  - {issue}")
        return 1

    print(
        f"✅ article share widgets PASS "
        f"({share_widget_count} share widgets, {email_widget_count} Email widgets, "
        f"{len(files)} post files, 0 duplicate subjects)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
