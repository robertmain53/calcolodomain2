#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent
SITE_ROOT = ROOT / "sito_modificato"
HEADER_PATH = ROOT / "template_perfetti" / "header_perfetto.html"
FOOTER_PATH = ROOT / "template_perfetti" / "footer_perfetto.html"

CATEGORY_SLUGS = [
    "construction",
    "construction-diy",
    "coordinate-converters",
    "engineering",
    "finance",
    "health-fitness",
    "lifestyle-everyday",
    "math",
    "math-conversions",
    "science",
]

SUBCATEGORY_SLUGS = [
    "automotive",
    "biology",
    "business-small-biz",
    "calorie",
    "chemistry",
    "construction-advanced-construction-calculators",
    "construction-concrete-mix-design-and-quality",
    "construction-concrete-quantities-and-masonry",
    "construction-cost-estimator",
    "construction-diy-materials-estimation",
    "construction-diy-project-layout-design",
    "construction-framing-and-carpentry",
    "construction-interiors-envelope-and-finishes",
    "construction-planning-and-estimating",
    "construction-roofing",
    "construction-sitework-aggregates-and-asphalt",
    "construction-structural-and-reinforcement",
    "core-math-algebra",
    "diet-nutrition",
    "electrical",
    "engineering-eurocode-0",
    "engineering-eurocode-1",
    "engineering-eurocode-2",
    "engineering-eurocode-3",
    "engineering-eurocode-4",
    "engineering-eurocode-5",
    "engineering-eurocode-6",
    "engineering-eurocode-7",
    "engineering-eurocode-8",
    "engineering-eurocode-9",
    "engineering-mechanical",
    "finance-business-ratios-and-valuation",
    "finance-canada-taxes",
    "finance-company-planning-and-statements",
    "finance-income-and-payroll",
    "finance-international-personal",
    "finance-investing-and-growth",
    "finance-investment",
    "finance-loans-and-debt",
    "finance-loans-debt",
    "finance-mortgage-real-estate",
    "finance-mortgages-and-home",
    "finance-personal-loans",
    "finance-real-estate-investing",
    "finance-retirement",
    "finance-retirement-and-pensions",
    "finance-stocks-options-and-trading",
    "finance-uk-and-europe-taxes",
    "finance-us-state-and-local-taxes",
    "fitness",
    "geometry",
    "geometry-area-and-perimeter-formulas",
    "health-fitness-diet-nutrition",
    "health-fitness-fitness",
    "health-fitness-health-metrics",
    "health-metrics",
    "hobbies",
    "loans-debt",
    "math-conversions-core-math-algebra",
    "math-conversions-geometry",
    "math-conversions-measurement-unit-conversions",
    "mechanical-engineering",
    "miscellaneous",
    "mortgage-real-estate",
    "physics",
    "project-layout-design",
    "structural-engineering",
    "taxes",
    "time-date",
]


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def extract_title(html: str) -> str:
    match = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    match = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", html)
    if match:
        return re.sub(r"(?is)<[^>]+>", " ", match.group(1)).strip()
    return "Untitled"


def extract_breadcrumb_slug(html: str) -> Tuple[Optional[str], Optional[str]]:
    scripts = re.findall(
        r'(?is)<script[^>]*type=["\']application/ld\\+json["\'][^>]*>(.*?)</script>',
        html,
    )
    for script in scripts:
        try:
            data = json.loads(script.strip())
        except json.JSONDecodeError:
            continue

        candidates = data if isinstance(data, list) else [data]
        for node in candidates:
            if isinstance(node, dict) and node.get("@type") == "BreadcrumbList":
                items = node.get("itemListElement") or []
                if len(items) < 2:
                    continue
                cat_slug = breadcrumb_item_to_slug(items[1])
                sub_slug = breadcrumb_item_to_slug(items[2]) if len(items) > 2 else None
                if cat_slug or sub_slug:
                    return cat_slug, sub_slug
    return extract_breadcrumb_slug_html(html)


def extract_breadcrumb_slug_html(html: str) -> Tuple[Optional[str], Optional[str]]:
    nav_blocks = re.findall(r"(?is)<nav[^>]*>.*?</nav>", html)
    breadcrumb_candidates = []
    for nav in nav_blocks:
        if re.search(r"breadcrumb", nav, re.I) or re.search(r">\\s*Home\\s*<", nav, re.I):
            breadcrumb_candidates.append(nav)
    if not breadcrumb_candidates:
        return None, None

    best_nav = max(breadcrumb_candidates, key=lambda n: len(re.findall(r"(?is)<a\\b", n)))
    anchors = re.findall(r'(?is)<a[^>]+href=["\'](.*?)["\'][^>]*>(.*?)</a>', best_nav)
    slugs = []
    for href, label in anchors:
        slug = slug_from_breadcrumb_url(href) or slugify(re.sub(r"(?is)<[^>]+>", " ", label))
        if slug:
            slugs.append(slug)

    cat_slug = next((s for s in slugs if s in CATEGORY_SLUGS), None)
    sub_slug = None
    if cat_slug and cat_slug in slugs:
        idx = slugs.index(cat_slug)
        sub_slug = next((s for s in slugs[idx + 1 :] if s in SUBCATEGORY_SLUGS), None)
    else:
        sub_slug = next((s for s in slugs if s in SUBCATEGORY_SLUGS), None)

    return cat_slug, sub_slug


def breadcrumb_item_to_slug(item: dict) -> Optional[str]:
    if not isinstance(item, dict):
        return None
    url = item.get("item") or ""
    name = item.get("name") or ""
    slug_from_url = slug_from_breadcrumb_url(url)
    if slug_from_url:
        return slug_from_url
    if name:
        return slugify(name)
    return None


def slug_from_breadcrumb_url(url: str) -> Optional[str]:
    if not url:
        return None
    path = url.split("://", 1)[-1]
    path = path.split("/", 1)[-1]
    path = path.split("?", 1)[0].split("#", 1)[0]
    if not path:
        return None
    parts = [p for p in path.split("/") if p]
    if not parts:
        return None
    if parts[0] in ("categories", "subcategories") and len(parts) >= 2:
        return parts[1]
    return parts[-1]


def iter_html_pages() -> List[Path]:
    pages = []
    for p in SITE_ROOT.rglob("*.html"):
        if not p.is_file():
            continue
        if "categories" in p.parts or "subcategories" in p.parts:
            continue
        pages.append(p)
    return pages


def load_header_footer() -> Tuple[str, str]:
    header = HEADER_PATH.read_text(encoding="utf-8")
    footer = FOOTER_PATH.read_text(encoding="utf-8")
    return header, footer


def build_categories_section() -> str:
    links = []
    for slug in CATEGORY_SLUGS + ["general"]:
        label = category_label(slug)
        links.append(
            f'<a href="https://calcdomain.com/categories/{slug}" class="text-sm text-blue-700 hover:text-blue-900">{label}</a>'
        )
    return (
        '<div class="mb-8 rounded-lg border border-gray-200 bg-white p-5">'
        '<h2 class="text-lg font-semibold text-gray-900 mb-2">All Categories</h2>'
        '<div class="flex flex-wrap gap-3">' + "".join(links) + "</div></div>"
    )


def category_label(slug: str) -> str:
    overrides = {
        "construction-diy": "Construction & DIY",
        "health-fitness": "Health & Fitness",
        "lifestyle-everyday": "Lifestyle & Everyday",
        "math-conversions": "Math & Conversions",
    }
    return overrides.get(slug, slug.replace("-", " ").title())


def build_page_html(
    title: str,
    heading: str,
    items: List[Tuple[str, str]],
    canonical_path: str,
    include_categories: bool = False,
) -> str:
    header, footer = load_header_footer()
    list_items = []
    for label, url in items:
        list_items.append(
            f'<a href="{url}" class="block p-4 bg-white rounded-lg shadow-sm border hover:border-blue-500 hover:shadow-md transition">'
            f'<div class="text-base font-semibold text-gray-800">{label}</div>'
            f'<div class="text-sm text-gray-500 mt-1">{url}</div>'
            f"</a>"
        )
    cards_html = "\n".join(list_items) or "<p class=\"text-gray-600\">No pages found.</p>"

    categories_section = build_categories_section() if include_categories else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{heading} on CalcDomain.">
  <link rel="canonical" href="https://calcdomain.com{canonical_path}">
  <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="shortcut icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
  </style>
</head>
<body class="bg-gray-50 text-gray-800">
{header}
  <main class="container mx-auto px-4 py-10 max-w-5xl">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">{heading}</h1>
      <p class="text-gray-600 mt-2">Browse calculators and resources in this section.</p>
    </div>
    {categories_section}
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {cards_html}
    </div>
  </main>
{footer}
  <script src="/assets/js/mobile-menu.js" defer></script>
  <script src="/search.js" defer></script>
</body>
</html>
"""


def main() -> None:
    category_set = set(CATEGORY_SLUGS)
    subcategory_set = set(SUBCATEGORY_SLUGS)

    category_pages: Dict[str, List[Tuple[str, str]]] = {c: [] for c in CATEGORY_SLUGS}
    subcategory_pages: Dict[str, List[Tuple[str, str]]] = {s: [] for s in SUBCATEGORY_SLUGS}
    general_pages: List[Tuple[str, str]] = []

    for page in iter_html_pages():
        html = page.read_text(encoding="utf-8", errors="ignore")
        title = extract_title(html)
        cat_slug, sub_slug = extract_breadcrumb_slug(html)

        rel_url = f"/{page.relative_to(SITE_ROOT).as_posix()}"

        if cat_slug in category_set:
            category_pages[cat_slug].append((title, rel_url))
            if sub_slug in subcategory_set:
                subcategory_pages[sub_slug].append((title, rel_url))
        else:
            general_pages.append((title, rel_url))

    categories_dir = SITE_ROOT / "categories"
    subcategories_dir = SITE_ROOT / "subcategories"
    categories_dir.mkdir(parents=True, exist_ok=True)
    subcategories_dir.mkdir(parents=True, exist_ok=True)

    for cat_slug in CATEGORY_SLUGS:
        heading = f"Category: {category_label(cat_slug)}"
        html = build_page_html(
            f"{heading} | CalcDomain",
            heading,
            category_pages[cat_slug],
            f"/categories/{cat_slug}",
            include_categories=True,
        )
        (categories_dir / f"{cat_slug}.html").write_text(html, encoding="utf-8")

    for sub_slug in SUBCATEGORY_SLUGS:
        heading = f"Subcategory: {sub_slug.replace('-', ' ').title()}"
        html = build_page_html(
            f"{heading} | CalcDomain",
            heading,
            subcategory_pages[sub_slug],
            f"/subcategories/{sub_slug}",
            include_categories=True,
        )
        (subcategories_dir / f"{sub_slug}.html").write_text(html, encoding="utf-8")

    general_heading = "Category: General"
    general_html = build_page_html(
        "Category: General | CalcDomain",
        general_heading,
        general_pages,
        "/categories/general",
        include_categories=True,
    )
    (categories_dir / "general.html").write_text(general_html, encoding="utf-8")

    print(
        f"Wrote {len(CATEGORY_SLUGS)} category pages, "
        f"{len(SUBCATEGORY_SLUGS)} subcategory pages, and general category."
    )
    run_search_and_sitemap()


def run_search_and_sitemap() -> None:
    script_path = SITE_ROOT / "tools" / "gen_search_and_sitemap.py"
    if not script_path.exists():
        raise FileNotFoundError(f"Missing generator: {script_path}")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(SITE_ROOT),
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Search/sitemap generator failed.")


def run_git_commands() -> None:
    stamp = date.today().isoformat()
    subprocess.run(["git", "add", "."], check=True)
    commit = subprocess.run(["git", "commit", "-m", stamp], check=False)
    if commit.returncode != 0:
        print("Git commit skipped (nothing to commit).")
        return
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regenerate category pages, search, and sitemap.")
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Skip git add/commit/push.",
    )
    args = parser.parse_args()

    main()
    if not args.no_git:
        run_git_commands()
