#!/usr/bin/env python3
"""
Normalize CalcDomain HTML pages to the new Tailwind layout.

What it does per HTML file (unless excluded):
  • Rebuilds <head> with the shared includes (Tailwind, Inter, MathJax, /search.js)
    while preserving page-specific meta tags, JSON-LD blocks, and custom styles.
  • Replaces the header/footer with the canonical layout that uses root-relative URLs.
  • Wraps legacy body content inside the new main scaffold so every calculator,
    category, and subcategory page shares the same flex-based layout.
  • Normalizes internal links to root-relative paths and fixes common 404s
    (e.g. foo-calculator.html → /foo.html if that page exists).
  • De-duplicates trailing script includes and re-appends them after the shared JS.

Usage:
    python3 tools/normalize_site.py [--dry-run] [--limit 20]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

HEADER_TEMPLATE = """    <header class="bg-white shadow-sm sticky top-0 z-50">
        <nav class="container mx-auto px-4 lg:px-6 py-4">
            <div class="flex justify-between items-center">
                <a href="/index.html" class="text-2xl font-bold text-blue-600">CalcDomain</a>

                <div class="w-full max-w-md hidden md:block mx-8">
                    <div class="relative">
                        <input type="search" id="search-input" placeholder="Search for a calculator..."
                               class="w-full py-2 px-4 pr-12 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                               autocomplete="off">
                        <svg class="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-gray-400"
                             fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                        </svg>
                        <div id="search-results" class="absolute top-full left-0 right-0 hidden bg-white border border-gray-200 rounded-lg shadow-lg mt-2 max-h-96 overflow-y-auto z-50"></div>
                    </div>
                </div>

                <div class="hidden md:flex items-center space-x-6 text-sm">
                    <a href="/search.html" class="text-gray-700 hover:text-blue-600">Advanced Search</a>
                    <a href="/index.html#categories" class="text-gray-700 hover:text-blue-600">Categories</a>
                </div>

                <button id="mobile-menu-toggle" class="md:hidden p-2" aria-label="Open menu">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>
            </div>

            <div id="mobile-menu" class="md:hidden mt-4 hidden">
                <div class="space-y-2">
                    <a href="/search.html" class="block py-2 text-gray-700 hover:text-blue-600">Advanced Search</a>
                    <a href="/index.html#categories" class="block py-2 text-gray-700 hover:text-blue-600">Categories</a>
                </div>
            </div>
        </nav>
    </header>"""

FOOTER_TEMPLATE = """    <footer class="bg-white border-t mt-12">
        <div class="container mx-auto px-6 py-8 text-center text-gray-600 text-sm">
            <p>&copy; 2025 CalcDomain. All Rights Reserved.</p>
            <div class="mt-4 space-x-4">
                <a href="/about.html" class="hover:text-blue-600">About</a>
                <a href="/contact.html" class="hover:text-blue-600">Contact</a>
                <a href="/privacy.html" class="hover:text-blue-600">Privacy</a>
                <a href="/terms.html" class="hover:text-blue-600">Terms</a>
            </div>
        </div>
    </footer>"""

TAILWIND_STYLE = """
        body { font-family: 'Inter', sans-serif; }
        .prose { max-width: 65ch; }
        .prose h2 { font-size: 1.5rem; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem; }
        .prose h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; }
        .prose p { margin-bottom: 1rem; line-height: 1.65; }
        .prose ul, .prose ol { margin-left: 1.5rem; margin-bottom: 1rem; }
        .prose li { margin-bottom: 0.5rem; }
        .formula-box {
            background: #f3f4f6;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 1rem;
            overflow-x: auto;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        }
        details > summary { cursor: pointer; font-weight: 600; padding: 0.5rem 0; }
        details[open] > summary { margin-bottom: 0.5rem; }
        .result-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1.25rem; text-align: center; }
        .result-card h4 { font-size: 0.95rem; color: #6b7280; margin-bottom: 0.25rem; }
        .result-card p { font-size: 1.75rem; font-weight: 700; color: #2563eb; }
        @media print {
            body * { visibility: hidden; }
            #print-section, #print-section * { visibility: visible; }
            #print-section { position: absolute; left: 0; top: 0; width: 100%; }
        }
""".strip("\n")

HEAD_SNIPPET = """<head>
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
<link rel="manifest" href="/site.webmanifest" />
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {title_tag}
    {description_tag}
    {canonical_tag}
    {meta_extra}
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
{tailwind_style}
    </style>
{style_extra}
    <script>
      window.MathJax = {{
        tex: {{
          inlineMath: [['\\(','\\)'], ['$', '$']],
          displayMath: [['\\[','\\]']]
        }},
        svg: {{ fontCache: 'global' }}
      }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
    <link rel="preload" href="/assets/js/mobile-menu.js" as="script">
    <link rel="preload" href="/assets/js/page-enhancements.js" as="script">
{head_scripts}
    <script src="/search.js" defer></script>
</head>"""

BODY_TEMPLATE = """<body class="bg-gray-50 text-gray-900">
{header}
    <main class="container mx-auto px-4 lg:px-6 py-10">
        <div class="flex flex-col lg:flex-row gap-8">
            <section class="w-full lg:w-2/3">
{breadcrumb_block}
                <div id="print-section" class="bg-white p-6 rounded-lg shadow-md">
{content_block}
                </div>
            </section>
            <aside class="w-full lg:w-1/3">
                <div class="sticky top-24 space-y-6">
{aside_block}
                </div>
            </aside>
        </div>
    </main>
{footer}
{shared_scripts}
{page_scripts}
</body>"""

SHARED_SCRIPTS = """    <script>
        document.getElementById('mobile-menu-toggle')?.addEventListener('click', () => {
            const menu = document.getElementById('mobile-menu');
            menu?.classList.toggle('hidden');
        });
    </script>
    <script defer src="/assets/js/mobile-menu.js"></script>
    <script defer src="/assets/js/page-enhancements.js"></script>"""

EXCLUDE_FILES = {
    # Templates should be edited manually.
    "template-calc.html",
    "template-cat.html",
    "template-home.html",
    "template-subcat.html",
}

def extract_tag(pattern: str, text: str, flags: int = re.I | re.S) -> Tuple[str, str]:
    match = re.search(pattern, text, flags)
    if not match:
        return "", text
    new_text = text[:match.start()] + text[match.end():]
    return match.group(0).strip(), new_text


def clean_head(head_html: str) -> Tuple[str, str, str, str, str]:
    """Return title tag, description meta, canonical link, style extra, head extra."""
    title_tag, rest = extract_tag(r"<title>.*?</title>", head_html)
    desc_tag, rest = extract_tag(r'<meta[^>]+name=["\']description["\'][^>]*>', rest)
    canon_tag, rest = extract_tag(r'<link[^>]+rel=["\']canonical["\'][^>]*>', rest)

    # Remove duplicates we are going to add ourselves
    rest = re.sub(r'<meta[^>]+charset[^>]*>', '', rest, flags=re.I)
    rest = re.sub(r'<meta[^>]+viewport[^>]*>', '', rest, flags=re.I)
    rest = re.sub(r'<script[^>]+cdn\.tailwindcss\.com[^>]*>\s*</script>', '', rest, flags=re.I)
    rest = re.sub(r'<link[^>]+fonts\.googleapis\.com[^>]*>', '', rest, flags=re.I)
    rest = re.sub(r'<script[^>]+search\.js[^>]*>\s*</script>', '', rest, flags=re.I)
    rest = re.sub(r'<link[^>]+mobile-menu\.js[^>]*>', '', rest, flags=re.I)
    rest = re.sub(r'<link[^>]+page-enhancements\.js[^>]*>', '', rest, flags=re.I)
    rest = re.sub(r'<script[^>]+MathJax[^>]*>\s*</script>', '', rest, flags=re.I)
    rest = re.sub(r'<script>\s*window\.MathJax[\s\S]*?</script>', '', rest, flags=re.I)
    rest = re.sub(r'<link[^>]+rel=["\'](?:shortcut icon|icon|apple-touch-icon|manifest)["\'][^>]*>', '', rest, flags=re.I)

    # Separate <style> blocks so we can append after our Tailwind helper styles
    style_blocks = re.findall(r"<style[\s\S]*?</style>", rest, flags=re.I)
    rest = re.sub(r"<style[\s\S]*?</style>", "", rest, flags=re.I)

    head_extra = rest.strip()
    style_extra = "\n".join(style_blocks)

    return title_tag, desc_tag, canon_tag, style_extra, head_extra


def strip_header_footer(body_html: str) -> Tuple[str, str, List[str]]:
    """Remove legacy header/footer and return cleaned html, breadcrumb, and trailing scripts."""
    body = re.sub(r"<header[\s\S]*?</header>", "", body_html, count=1, flags=re.I)

    breadcrumb_html = ""
    breadcrumb_match = re.search(
        r"<nav[^>]*(aria-label=\"[^\"]*breadcrumb[^\"]*\"|class=\"[^\"]*(breadcrumb|breadcrumbs)[^\"]*\")[^>]*>[\s\S]*?</nav>",
        body,
        flags=re.I,
    )
    if breadcrumb_match:
        breadcrumb_html = breadcrumb_match.group(0).strip()
        body = body[:breadcrumb_match.start()] + body[breadcrumb_match.end():]

    body = re.sub(r"<footer[\s\S]*?</footer>", "", body, flags=re.I)
    body = body.strip()

    trailing_scripts: List[str] = []
    script_pattern = re.compile(r"<script[\s\S]*?</script>\s*$", re.I)
    while True:
        match = script_pattern.search(body)
        if not match:
            break
        trailing_scripts.insert(0, match.group().strip())
        body = body[:match.start()].rstrip()

    return body, breadcrumb_html, trailing_scripts


def extract_intro(content: str) -> Tuple[str, str, str]:
    """Extract first <h1>, first <p>, and return remaining content."""
    h1_tag, remaining = extract_tag(r"<h1[\s\S]*?</h1>", content)
    p_tag, remaining = extract_tag(r"<p[\s\S]*?</p>", remaining)
    return h1_tag, p_tag, remaining.strip()


def ensure_heading(title_tag: str, h1_tag: str) -> Tuple[str, str]:
    """Provide fallback title/h1 when they are missing."""
    title_text = ""
    if title_tag:
        title_text = re.sub(r"<\/?title>", "", title_tag, flags=re.I).strip()
    if not h1_tag and title_text:
        h1_tag = f"<h1 class=\"text-3xl font-extrabold text-gray-900 mb-2\">{title_text}</h1>"
    elif h1_tag:
        # Inject Tailwind classes if missing
        if "class=" not in h1_tag:
            h1_tag = h1_tag.replace("<h1", '<h1 class="text-3xl font-extrabold text-gray-900 mb-2"', 1)
        else:
            h1_tag = re.sub(r'class="[^"]*"', lambda m: m.group(0).rstrip('"') + ' text-3xl font-extrabold text-gray-900 mb-2"', h1_tag, count=1)
    return title_text, h1_tag


def build_default_intro(meta_desc: str) -> str:
    desc_content = ""
    if meta_desc:
        desc_content = re.search(r'content=["\']([^"\']+)["\']', meta_desc)
    summary = desc_content.group(1) if desc_content else ""
    if summary:
        return f'<p class="text-gray-600 mb-6">{summary}</p>'
    return '<p class="text-gray-600 mb-6">Use this calculator to run quick scenarios and explore the detailed explanation below.</p>'


def make_aside(meta_desc: str, title_text: str) -> str:
    summary = ""
    if meta_desc:
        match = re.search(r'content=["\']([^"\']+)["\']', meta_desc)
        if match:
            summary = match.group(1)
    bullets = [
        "Snapshot the calculator’s primary use case.",
        "Highlight one actionable insight or rule of thumb.",
        "Link back to categories to continue exploring."
    ]
    bullet_html = "".join(f'<li>• {line}</li>' for line in bullets)
    heading = title_text or "Calculator overview"
    return f"""                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h2 class="text-lg font-semibold text-gray-900 mb-3">{heading}</h2>
                        <ul class="space-y-2 text-sm text-gray-600">
{bullet_html}
                        </ul>
                    </div>

                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h2 class="text-lg font-semibold text-gray-900 mb-3">Explore more</h2>
                        <ul class="space-y-2 text-sm text-blue-600">
                            <li><a href="/index.html#categories" class="hover:underline">Browse all categories</a></li>
                            <li><a href="/search.html" class="hover:underline">Launch advanced search</a></li>
                            <li><a href="/about.html" class="hover:underline">About CalcDomain</a></li>
                        </ul>
                    </div>"""


def normalize_links(html: str, page_path: Path) -> str:
    """Normalize internal link targets to prevent 404s."""
    def replacement(match: re.Match[str]) -> str:
        href = match.group(1)
        if not href or href.startswith(("#", "mailto:", "javascript:")):
            return match.group(0)
        if "://" in href:
            return match.group(0)

        raw = href
        clean = raw.split("#")[0].split("?")[0]

        target_path: Path
        if clean.startswith("/"):
            target_path = ROOT / clean.lstrip("/")
        else:
            target_path = (page_path.parent / clean).resolve()

        if not target_path.exists():
            # Try removing "-calculator" before .html
            if clean.endswith("-calculator.html"):
                alt = clean.replace("-calculator.html", ".html")
                candidate = (ROOT / alt.lstrip("/")) if alt.startswith("/") else (page_path.parent / alt).resolve()
                if candidate.exists():
                    new_href = "/" + candidate.relative_to(ROOT).as_posix()
                    return match.group(0).replace(href, new_href)
            # Try removing duplicated "-calc"
            if clean.endswith("-calc.html"):
                alt = clean.replace("-calc.html", ".html")
                candidate = (ROOT / alt.lstrip("/")) if alt.startswith("/") else (page_path.parent / alt).resolve()
                if candidate.exists():
                    new_href = "/" + candidate.relative_to(ROOT).as_posix()
                    return match.group(0).replace(href, new_href)
            # Try resolving by adding leading slash if file lives at root
            root_candidate = ROOT / clean.lstrip("/")
            if root_candidate.exists():
                new_href = "/" + root_candidate.relative_to(ROOT).as_posix()
                return match.group(0).replace(href, new_href)
            return match.group(0)

        # Found an existing file
        new_href = "/" + target_path.relative_to(ROOT).as_posix()
        return match.group(0).replace(href, new_href)

    return re.sub(r'href="([^"]+)"', replacement, html)


def normalize_file(path: Path, dry_run: bool = False) -> bool:
    if path.name in EXCLUDE_FILES:
        return False

    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text

    head_match = re.search(r"<head[\s\S]*?</head>", text, flags=re.I)
    body_match = re.search(r"<body[\s\S]*?</body>", text, flags=re.I)
    if not head_match or not body_match:
        return False

    head_inner = head_match.group(0)
    head_inner = re.sub(r"^<head[^>]*>", "", head_inner, flags=re.I)
    head_inner = re.sub(r"</head>\s*$", "", head_inner, flags=re.I).strip()

    body_inner = body_match.group(0)
    body_inner = re.sub(r"^<body[^>]*>", "", body_inner, flags=re.I)
    body_inner = re.sub(r"</body>\s*$", "", body_inner, flags=re.I).strip()

    title_tag, desc_tag, canon_tag, style_extra, head_extra = clean_head(head_inner)

    body_without_header, breadcrumb_html, trailing_scripts = strip_header_footer(body_inner)
    h1_tag, intro_tag, remaining = extract_intro(body_without_header)
    title_text, h1_tag = ensure_heading(title_tag, h1_tag)

    intro = ""
    if intro_tag:
        intro = re.sub(r'<p([^>]*)>', r'<p\1 class="text-gray-600 mb-6">', intro_tag, count=1, flags=re.I)
    else:
        intro = build_default_intro(desc_tag)

    if not h1_tag:
        h1_tag = '<h1 class="text-3xl font-extrabold text-gray-900 mb-2">Calculator</h1>'

    content_block = "\n".join([
        f"                    {h1_tag}",
        f"                    {intro}",
        "                    <div class=\"legacy-content space-y-6\">",
        f"{indent_html(remaining, 6)}",
        "                    </div>"
    ])

    breadcrumb_block = ""
    if breadcrumb_html:
        breadcrumb_block = indent_html(breadcrumb_html, 12)
    else:
        breadcrumb_block = '                <nav class="text-sm text-gray-600 mb-4" aria-label="Breadcrumb">\n                    <a href="/index.html" class="hover:text-blue-600">Home</a> &raquo;\n                    <span class="text-gray-900">{}</span>\n                </nav>'.format(title_text or "Calculator")

    aside_block = make_aside(desc_tag, title_text)

    page_scripts = "\n".join(trailing_scripts)

    new_head = HEAD_SNIPPET.format(
        title_tag=title_tag or "<title>CalcDomain Calculator</title>",
        description_tag=desc_tag or '<meta name="description" content="Professional calculator by CalcDomain.">',
        canonical_tag=canon_tag or "",
        meta_extra=head_extra,
        tailwind_style="\n        ".join(TAILWIND_STYLE.splitlines()),
        style_extra=style_extra,
        head_scripts=""
    )

    new_body = BODY_TEMPLATE.format(
        header=HEADER_TEMPLATE,
        breadcrumb_block=breadcrumb_block,
        content_block=content_block,
        aside_block=aside_block,
        footer=FOOTER_TEMPLATE,
        shared_scripts=SHARED_SCRIPTS,
        page_scripts=indent_html(page_scripts, 4) if page_scripts else ""
    )

    new_html = "<!DOCTYPE html>\n<html lang=\"en\">\n" + new_head + "\n" + new_body + "\n</html>\n"
    new_html = normalize_links(new_html, path)

    if new_html != original and not dry_run:
        path.write_text(new_html, encoding="utf-8")
        return True
    return new_html != original


def indent_html(html: str, spaces: int) -> str:
    if not html.strip():
        return ""
    indent = " " * spaces
    lines = [line.rstrip() for line in html.splitlines()]
    return "\n".join(f"{indent}{line}" if line else "" for line in lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Normalize CalcDomain HTML pages.")
    ap.add_argument("--dry-run", action="store_true", help="Report files that would change without writing.")
    ap.add_argument("--limit", type=int, default=0, help="Limit processing to N files (useful for testing).")
    args = ap.parse_args()

    changed: List[Path] = []
    processed = 0

    for html_path in ROOT.rglob("*.html"):
        processed += 1
        if args.limit and processed > args.limit:
            break
        try:
            updated = normalize_file(html_path, dry_run=args.dry_run)
        except Exception as exc:  # pragma: no cover - report issues
            print(f"[ERROR] {html_path}: {exc}", file=sys.stderr)
            continue
        if updated:
            changed.append(html_path)

    if args.dry_run:
        print(f"[dry-run] {len(changed)} files would be updated.")
        for path in changed[:20]:
            print("   ", path.relative_to(ROOT))
    else:
        print(f"Updated {len(changed)} HTML files.")


if __name__ == "__main__":
    main()
