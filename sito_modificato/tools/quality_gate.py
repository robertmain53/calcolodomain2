#!/usr/bin/env python3
"""
Quality gate for HTML pages in sito_modificato.
Fails the build on malformed metadata, canonical issues, JSON-LD errors,
missing/forbidden H1 patterns, and excessive duplicate titles/descriptions.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://calcdomain.com"

# Duplicate thresholds (tune as needed).
MAX_DUP_TITLE = 5
MAX_DUP_DESCRIPTION = 8

# Forbidden H1 patterns (case-insensitive).
FORBIDDEN_H1_PATTERNS = [
    r"calculator guide",
    r"calculator overview",
    r"tools & calculators",
    r"tools & guides",
]


HEAD_RE = re.compile(r"<head[^>]*>", re.IGNORECASE)
HEAD_BLOCK_RE = re.compile(r"<head[^>]*>.*?</head>", re.IGNORECASE | re.DOTALL)
CANONICAL_RE = re.compile(r"<link[^>]+rel=[\"']canonical[\"'][^>]*>", re.IGNORECASE)
CANONICAL_HREF_RE = re.compile(
    r"<link[^>]+rel=[\"']canonical[\"'][^>]*href=[\"']([^\"']+)[\"'][^>]*>",
    re.IGNORECASE,
)
META_CONTENT_RE = re.compile(r"content=[\"']([^\"']*)[\"']", re.IGNORECASE)
META_DESC_RE = re.compile(
    r"<meta[^>]+name=[\"']description[\"'][^>]*>", re.IGNORECASE
)
OG_DESC_RE = re.compile(
    r"<meta[^>]+property=[\"']og:description[\"'][^>]*>", re.IGNORECASE
)
TW_DESC_RE = re.compile(
    r"<meta[^>]+name=[\"']twitter:description[\"'][^>]*>", re.IGNORECASE
)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
JSONLD_RE = re.compile(
    r"<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>",
    re.IGNORECASE | re.DOTALL,
)


def slug_to_canonical(rel_path: Path) -> str:
    rel = rel_path.as_posix()
    if rel == "index.html":
        rel_url = ""
    elif rel.endswith("/index.html"):
        rel_url = "/" + rel[: -len("/index.html")]
    else:
        rel_url = "/" + rel[: -len(".html")]
    return f"{BASE_URL}{rel_url}"


def clean_text(html_fragment: str) -> str:
    text = TAG_RE.sub(" ", html_fragment)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_meta_content(tag_html: str) -> str:
    m = META_CONTENT_RE.search(tag_html)
    return m.group(1) if m else ""


def is_malformed_meta(content: str) -> bool:
    if "/> />" in content:
        return True
    if "<" in content or ">" in content:
        return True
    if re.search(r"<[^>]+>", content):
        return True
    return False


def jsonld_truncated(raw: str) -> bool:
    if "..." in raw:
        return True
    if raw.rstrip().endswith((",", ":")):
        return True
    if raw.count("{") != raw.count("}"):
        return True
    if raw.count("[") != raw.count("]"):
        return True
    return False


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT
    html_files = sorted(root.rglob("*.html"))

    errors: List[str] = []
    titles: Dict[str, List[str]] = {}
    descriptions: Dict[str, List[str]] = {}
    h1s: Dict[str, List[str]] = {}

    forbidden_h1_re = re.compile("|".join(FORBIDDEN_H1_PATTERNS), re.IGNORECASE)

    for path in html_files:
        rel = path.relative_to(root)
        html = path.read_text(encoding="utf-8")

        head_block = HEAD_BLOCK_RE.search(html)
        if not head_block:
            errors.append(f"{rel}: missing </head> or head block")
            continue

        head_html = head_block.group(0)
        outside_html = html[: head_block.start()] + html[head_block.end() :]

        canon_tags = CANONICAL_RE.findall(html)
        if not canon_tags:
            errors.append(f"{rel}: canonical missing")
        elif len(canon_tags) > 1:
            errors.append(f"{rel}: multiple canonical tags ({len(canon_tags)})")
        if CANONICAL_RE.search(outside_html):
            errors.append(f"{rel}: canonical outside <head>")

        canon_href = ""
        canon_match = CANONICAL_HREF_RE.search(head_html)
        if canon_match:
            canon_href = canon_match.group(1).strip()
        expected = slug_to_canonical(rel)
        if canon_href and canon_href != expected:
            errors.append(f"{rel}: canonical mismatch ({canon_href} != {expected})")

        # Meta description validation
        for label, regex in [
            ("meta description", META_DESC_RE),
            ("og:description", OG_DESC_RE),
            ("twitter:description", TW_DESC_RE),
        ]:
            m = regex.search(head_html)
            if not m:
                continue
            content = extract_meta_content(m.group(0))
            if is_malformed_meta(content):
                errors.append(f"{rel}: malformed {label} content")

        # JSON-LD validation
        for raw in JSONLD_RE.findall(head_html):
            raw = raw.strip()
            if not raw:
                errors.append(f"{rel}: empty JSON-LD block")
                continue
            if jsonld_truncated(raw):
                errors.append(f"{rel}: JSON-LD appears truncated")
                continue
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: JSON-LD invalid ({exc.msg})")

        # Title/description tracking
        title_match = TITLE_RE.search(head_html)
        if title_match:
            title = clean_text(title_match.group(1))
            titles.setdefault(title, []).append(str(rel))

        desc_match = META_DESC_RE.search(head_html)
        if desc_match:
            desc = extract_meta_content(desc_match.group(0)).strip()
            if desc:
                descriptions.setdefault(desc, []).append(str(rel))

        # H1 validation
        h1_match = H1_RE.search(html)
        if not h1_match:
            errors.append(f"{rel}: missing H1")
        else:
            h1_text = clean_text(h1_match.group(1))
            if forbidden_h1_re.search(h1_text):
                errors.append(f"{rel}: forbidden H1 pattern ({h1_text})")
            h1s.setdefault(h1_text, []).append(str(rel))

    # Duplicate thresholds
    for title, paths in titles.items():
        if len(paths) > MAX_DUP_TITLE:
            errors.append(
                f"title duplicated {len(paths)}x: '{title}' (e.g., {paths[:3]})"
            )
    for desc, paths in descriptions.items():
        if len(paths) > MAX_DUP_DESCRIPTION:
            errors.append(
                f"description duplicated {len(paths)}x: '{desc[:60]}...' (e.g., {paths[:3]})"
            )

    if errors:
        print("QUALITY GATE FAILED")
        print(f"Total errors: {len(errors)}")
        for err in errors:
            print(f"- {err}")
        return 1

    print("QUALITY GATE PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
