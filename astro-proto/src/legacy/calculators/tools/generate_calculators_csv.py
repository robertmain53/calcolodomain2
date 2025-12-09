#!/usr/bin/env python3
"""
Generate a CSV file with metadata for CalcDomain calculators.

The CSV includes slug, title, category (from breadcrumbs),
subcategory description (short card copy when available, otherwise the meta
description), and any keywords found in meta tags or JSON-LD blocks.
"""

from __future__ import annotations

import csv
import json
import posixpath
import re
from html import unescape
from pathlib import Path
from typing import Dict, Iterable, Optional

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {".git", "out", "tools", "tools_bundle_v4", "tools_bundle_v5", "tmp_src"}
CSV_HEADERS = ["slug", "title", "category", "subcategory_description", "keywords"]


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def strip_tags(raw: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?</\\1>", " ", raw)
    text = re.sub(r"(?is)<!--.*?-->", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    return collapse_ws(unescape(text))


def read_html(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def is_html_candidate(path: Path) -> bool:
    if path.suffix != ".html":
        return False
    if any(seg in SKIP_DIRS for seg in path.parts):
        return False
    return True


def get_title(html_text: str) -> str:
    match = re.search(r"(?is)<title[^>]*>(.*?)</title>", html_text)
    if match:
        return collapse_ws(unescape(match.group(1)))
    match = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", html_text)
    if match:
        return strip_tags(match.group(1))
    return ""


def get_meta_description(html_text: str) -> str:
    match = re.search(r'(?is)<meta[^>]+name=["\']description["\'][^>]*>', html_text)
    if match:
        tag = match.group(0)
        content = re.search(r'content=["\'](.*?)["\']', tag, re.I | re.S)
        if content:
            return collapse_ws(unescape(content.group(1)))
    match = re.search(r"(?is)<p[^>]*>(.*?)</p>", html_text)
    if match:
        return strip_tags(match.group(1))
    return ""


def infer_category_subcategory(html_text: str) -> tuple[str, str]:
    cat = sub = ""
    breadcrumb_match = re.search(
        r'(?is)<nav[^>]*(?:breadcrumb|aria-label=["\']breadcrumb["\'])[^>]*>.*?</nav>',
        html_text,
    )
    if not breadcrumb_match:
        breadcrumb_match = re.search(
            r'(?is)<div[^>]*class=["\'][^"\']*(?:breadcrumb|breadcrumbs)[^"\']*["\'][^>]*>.*?</div>',
            html_text,
        )
    if breadcrumb_match:
        snip = breadcrumb_match.group(0)
        anchors = re.findall(r'(?is)<a[^>]*>(.*?)</a>', snip)
        texts = [strip_tags(a) for a in anchors if strip_tags(a)]
        texts = [t for t in texts if collapse_ws(t).lower() != "home"]
        if len(texts) >= 1:
            cat = texts[0]
        if len(texts) >= 2:
            sub = texts[1]
    if not cat:
        match = re.search(r'(?is)>(Finance|Health|Math|Lifestyle|Construction)[^<]*<', html_text)
        if match:
            cat = strip_tags(match.group(0))
    return collapse_ws(cat), collapse_ws(sub)


def slug_from_href(base_path: Path, href: str) -> Optional[str]:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "javascript:", "http://", "https://")):
        return None
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href.endswith(".html"):
        return None
    base_rel = base_path.relative_to(ROOT).as_posix()
    base_dir = posixpath.dirname(base_rel)
    if href.startswith("https://calcdomain.com/"):
        norm = posixpath.normpath(href.lstrip("https://calcdomain.com/"))
    else:
        norm = posixpath.normpath(posixpath.join(base_dir, href))
    if norm.startswith("https://calcdomain.com/"):
        return None
    return posixpath.splitext(posixpath.basename(norm))[0]


def build_card_descriptions(html_files: Iterable[Path]) -> Dict[str, str]:
    card_desc: Dict[str, str] = {}
    card_pattern = re.compile(r'<a[^>]+href=["\']([^"\']+?)["\'][^>]*>(.*?)</a>', re.I | re.S)
    for path in html_files:
        html_text = read_html(path)
        for match in card_pattern.finditer(html_text):
            href, inner = match.groups()
            if "<h3" not in inner.lower():
                continue
            p_match = re.search(r"(?is)<p[^>]*>(.*?)</p>", inner)
            if not p_match:
                continue
            desc = strip_tags(p_match.group(1))
            if not desc:
                continue
            slug = slug_from_href(path, href)
            if not slug:
                continue
            # Prefer longer descriptions if multiple cards mention the same slug
            if slug not in card_desc or len(desc) > len(card_desc[slug]):
                card_desc[slug] = desc
    return card_desc


def extract_keywords(html_text: str) -> str:
    keywords: list[str] = []
    for meta in re.finditer(r'(?is)<meta[^>]+name=["\']keywords["\'][^>]*>', html_text):
        tag = meta.group(0)
        content_match = re.search(r'content=["\'](.*?)["\']', tag, re.I | re.S)
        if content_match:
            content = content_match.group(1)
            parts = [collapse_ws(part) for part in content.split(",")]
            keywords.extend([part for part in parts if part])
    if not keywords:
        for block in re.finditer(
            r'(?is)<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            html_text,
        ):
            raw_json = block.group(1).strip()
            try:
                data = json.loads(raw_json)
            except Exception:
                continue
            def collect(obj):
                if isinstance(obj, dict):
                    if "keywords" in obj:
                        val = obj["keywords"]
                        if isinstance(val, str):
                            parts = [collapse_ws(part) for part in val.split(",")]
                            keywords.extend([part for part in parts if part])
                        elif isinstance(val, list):
                            keywords.extend(
                                [collapse_ws(str(item)) for item in val if collapse_ws(str(item))]
                            )
                    for value in obj.values():
                        collect(value)
                elif isinstance(obj, list):
                    for item in obj:
                        collect(item)
            collect(data)
            if keywords:
                break
    seen: list[str] = []
    for kw in keywords:
        if kw not in seen:
            seen.append(kw)
    return ", ".join(seen)


def main() -> None:
    html_files = [p for p in ROOT.rglob("*.html") if is_html_candidate(p)]
    card_descriptions = build_card_descriptions(html_files)

    rows = []
    for path in sorted(html_files):
        # Skip subcategory index pages (not calculators)
        try:
            rel_parent = path.parent.relative_to(ROOT)
        except ValueError:
            rel_parent = Path(".")
        if rel_parent.parts and rel_parent.parts[0] == "subcategories":
            continue

        html_text = read_html(path)
        slug = path.stem
        title = get_title(html_text)
        category, _ = infer_category_subcategory(html_text)
        meta_desc = get_meta_description(html_text)
        subcat_desc = card_descriptions.get(slug, meta_desc)
        keywords = extract_keywords(html_text)

        rows.append({
            "slug": slug,
            "title": title,
            "category": category,
            "subcategory_description": subcat_desc,
            "keywords": keywords,
        })

    rows.sort(key=lambda r: r["slug"])

    output_path = ROOT / "calculators.csv"
    with output_path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()
