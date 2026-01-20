#!/usr/bin/env python3
import argparse
import csv
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


def extract_meta_description(html: str) -> str:
    match = re.search(
        r'(?is)<meta[^>]+name=["\']description["\'][^>]*>',
        html,
    )
    if match:
        tag = match.group(0)
        content = re.search(r'content=["\'](.*?)["\']', tag, re.I | re.S)
        if content:
            return re.sub(r"\s+", " ", content.group(1)).strip()
    match = re.search(r"(?is)<p[^>]*>(.*?)</p>", html)
    if match:
        return re.sub(r"(?is)<[^>]+>", " ", match.group(1)).strip()
    return ""


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


def category_label(slug: str) -> str:
    overrides = {
        "construction-diy": "Construction & DIY",
        "health-fitness": "Health & Fitness",
        "lifestyle-everyday": "Lifestyle & Everyday",
        "math-conversions": "Math & Conversions",
    }
    return overrides.get(slug, slug.replace("-", " ").title())


def read_categories_from_csv() -> List[str]:
    path = ROOT / "cat.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row["category"].strip() for row in reader if row.get("category")]


def update_footer_template(categories: List[str]) -> None:
    if not categories:
        return
    footer_path = ROOT / "template_perfetti" / "footer_perfetto.html"
    text = footer_path.read_text(encoding="utf-8")
    list_items = ["        <ul class=\"space-y-2\">"]
    for slug in categories:
        label = category_label(slug)
        list_items.append(
            f'          <li><a href="https://calcdomain.com/categories/{slug}" class="text-gray-400 hover:text-white">{label}</a></li>'
        )
    list_items.append("        </ul>")
    new_list = "\n".join(list_items)
    pattern = re.compile(r'(?is)(<h4[^>]*>\s*Categories\s*</h4>\s*)<ul[^>]*>.*?</ul>')
    new_text = pattern.sub(r"\1" + new_list, text, count=1)
    footer_path.write_text(new_text, encoding="utf-8")


def update_site_footers() -> None:
    footer = (ROOT / "template_perfetti" / "footer_perfetto.html").read_text(encoding="utf-8")
    for p in SITE_ROOT.rglob("*.html"):
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r"<footer\b[^>]*>", text, flags=re.I)
        if not match:
            continue
        start = match.start()
        end = text.find("</footer>", match.end())
        if end == -1:
            continue
        end += len("</footer>")
        new_text = text[:start] + footer + text[end:]
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")


def build_homepage_cards(categories: List[str]) -> str:
    cards = []
    for slug in categories:
        label = category_label(slug)
        cards.append(
            f'''                <a href="https://calcdomain.com/categories/{slug}" class="card-hover bg-white rounded-lg shadow-md overflow-hidden">
                    <div class="bg-gradient-to-r from-slate-700 to-slate-800 p-6 text-white">
                        <div class="flex items-center justify-between">
                            <div>
                                <h3 class="text-xl font-bold mb-2">{label}</h3>
                            </div>
                            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                        </div>
                    </div>
                    <div class="p-6">
                        <p class="text-gray-600 mb-4">Browse calculators in {label}.</p>
                    </div>
                </a>'''
        )
    return "\n\n".join(cards)


def update_homepage(categories: List[str], today: str) -> None:
    if not categories:
        return
    index_path = SITE_ROOT / "index.html"
    if not index_path.exists():
        return
    text = index_path.read_text(encoding="utf-8", errors="ignore")
    start = text.find("<!-- Categories Section -->")
    end = text.find("<!-- Features Section -->", start)
    if start == -1 or end == -1:
        return
    section = f'''<!-- Categories Section -->
    <section id="categories" class="py-16 bg-gray-50">
        <div class="container mx-auto px-4">
            <div class="text-center mb-12 mt-5">
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Calculator Categories</h2>
                <p class="text-lg text-gray-600">Updated from `cat.csv` to match live category pages.</p>
                <p class="text-sm text-gray-500 mt-2">Latest update: {today}</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
{build_homepage_cards(categories)}
            </div>
        </div>
    </section>
'''
    updated = text[:start] + section + "\n    <!-- Features Section -->" + text[end:]
    # Update or insert WebPage JSON-LD with dateModified
    web_page_pattern = re.compile(
        r'(?is)<script[^>]*type=["\']application/ld\+json["\'][^>]*>\s*\{\s*"@context"\s*:\s*"https://schema\.org"\s*,\s*"@type"\s*:\s*"WebPage".*?\}\s*</script>'
    )
    if web_page_pattern.search(updated):
        updated = re.sub(
            r'(?is)("dateModified"\s*:\s*")[^"]+(")',
            r"\1" + today + r"\2",
            updated,
        )
    else:
        insert_after = re.search(
            r'(?is)<script[^>]*type=["\']application/ld\+json["\'][^>]*>.*?"@type"\s*:\s*"WebSite".*?</script>',
            updated,
        )
        if insert_after:
            web_page = (
                f'\n<script type="application/ld+json">\n{{\n'
                f'  "@context": "https://schema.org",\n'
                f'  "@type": "WebPage",\n'
                f'  "name": "CalcDomain",\n'
                f'  "url": "https://calcdomain.com",\n'
                f'  "dateModified": "{today}"\n'
                f'}}\n</script>'
            )
            updated = updated[: insert_after.end()] + web_page + updated[insert_after.end() :]
    index_path.write_text(updated, encoding="utf-8")


def parent_category_for_subcategory(sub_slug: str) -> Optional[str]:
    prefixes = [
        ("finance-", "finance"),
        ("construction-diy-", "construction-diy"),
        ("construction-", "construction"),
        ("health-fitness-", "health-fitness"),
        ("math-conversions-", "math-conversions"),
        ("engineering-", "engineering"),
    ]
    for prefix, cat in prefixes:
        if sub_slug.startswith(prefix):
            return cat
    direct_map = {
        "automotive": "lifestyle-everyday",
        "biology": "science",
        "calorie": "health-fitness",
        "chemistry": "science",
        "core-math-algebra": "math",
        "diet-nutrition": "health-fitness",
        "electrical": "engineering",
        "fitness": "health-fitness",
        "geometry": "math",
        "geometry-area-and-perimeter-formulas": "math",
        "health-metrics": "health-fitness",
        "hobbies": "lifestyle-everyday",
        "loans-debt": "finance",
        "mechanical-engineering": "engineering",
        "miscellaneous": "lifestyle-everyday",
        "mortgage-real-estate": "finance",
        "physics": "science",
        "project-layout-design": "construction-diy",
        "structural-engineering": "engineering",
        "taxes": "finance",
        "time-date": "lifestyle-everyday",
    }
    return direct_map.get(sub_slug)


def build_breadcrumbs(
    label: str,
    section_slug: str,
    parent_label: Optional[str] = None,
    parent_slug: Optional[str] = None,
) -> Tuple[str, List[Dict[str, str]]]:
    crumbs = [{"name": "Home", "url": "https://calcdomain.com"}]
    if parent_label and parent_slug:
        crumbs.append(
            {
                "name": parent_label,
                "url": f"https://calcdomain.com/categories/{parent_slug}",
            }
        )
    crumbs.append(
        {
            "name": label,
            "url": f"https://calcdomain.com/{section_slug}/{slugify(label)}",
        }
    )
    html = (
        '<nav class="text-sm text-gray-600 mb-6" aria-label="Breadcrumbs">'
        f'<a href="{crumbs[0]["url"]}" class="hover:text-blue-600">Home</a>'
    )
    for crumb in crumbs[1:]:
        html += f' &raquo; <a href="{crumb["url"]}" class="hover:text-blue-600">{crumb["name"]}</a>'
    html += "</nav>"
    return html, crumbs


def build_json_ld(
    title: str,
    canonical_path: str,
    breadcrumb_items: List[Dict[str, str]],
    items: List[Tuple[str, str, str]],
    last_updated: str,
) -> str:
    breadcrumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "name": crumb["name"],
                "item": crumb["url"],
            }
            for idx, crumb in enumerate(breadcrumb_items)
        ],
    }

    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": title,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "url": f"https://calcdomain.com{url}",
                "name": label,
            }
            for idx, (label, url, _desc) in enumerate(items)
        ],
    }

    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "CalcDomain",
        "url": "https://calcdomain.com",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://calcdomain.com/search?q={search_term_string}",
            "query-input": "required name=search_term_string",
        },
    }

    organization = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "CalcDomain",
        "url": "https://calcdomain.com",
        "logo": "https://calcdomain.com/apple-touch-icon.png",
    }

    webpage = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": f"https://calcdomain.com{canonical_path}",
        "dateModified": last_updated,
    }

    return json.dumps(
        [breadcrumbs, item_list, website, organization, webpage],
        ensure_ascii=False,
        indent=2,
    )


def build_page_html(
    title: str,
    heading: str,
    items: List[Tuple[str, str, str]],
    canonical_path: str,
    section_slug: str = "categories",
    parent_label: Optional[str] = None,
    parent_slug: Optional[str] = None,
    description: Optional[str] = None,
    subcategory_items: Optional[List[Tuple[str, str, str]]] = None,
    last_updated: Optional[str] = None,
) -> str:
    header, footer = load_header_footer()
    list_items = []
    for label, url, desc in items:
        description = desc or "No description available."
        list_items.append(
            f'<a href="{url}" class="block p-4 bg-white rounded-lg shadow-sm border hover:border-blue-500 hover:shadow-md transition">'
            f'<div class="text-base font-semibold text-gray-800">{label}</div>'
            f'<div class="text-sm text-gray-500 mt-1">{description}</div>'
            f"</a>"
        )
    cards_html = "\n".join(list_items) or "<p class=\"text-gray-600\">No pages found.</p>"

    subcat_html = ""
    if subcategory_items:
        sub_items = []
        for label, url, desc in subcategory_items:
            description = desc or "Subcategory overview."
            sub_items.append(
                f'<a href="{url}" class="block p-4 bg-white rounded-lg shadow-sm border hover:border-blue-500 hover:shadow-md transition">'
                f'<div class="text-base font-semibold text-gray-800">{label}</div>'
                f'<div class="text-sm text-gray-500 mt-1">{description}</div>'
                f"</a>"
            )
        subcat_html = (
            '<section class="mb-10">'
            '<h2 class="text-2xl font-semibold text-gray-900 mb-4">Subcategories</h2>'
            f'<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{"".join(sub_items)}</div>'
            "</section>"
        )
    breadcrumbs_html, breadcrumb_items = build_breadcrumbs(
        heading,
        section_slug,
        parent_label=parent_label,
        parent_slug=parent_slug,
    )
    json_ld = build_json_ld(
        title,
        canonical_path,
        breadcrumb_items,
        items,
        last_updated or date.today().isoformat(),
    )
    meta_description = description or f"{heading} calculators and guides on CalcDomain."

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{meta_description}">
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
  <script type="application/ld+json">
{json_ld}
  </script>
</head>
<body class="bg-gray-50 text-gray-800">
{header}
  <main class="container mx-auto px-4 py-10 max-w-5xl">
    {breadcrumbs_html}
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">{heading}</h1>
      <p class="text-gray-600 mt-2">Browse calculators and resources in this section.</p>
      <p class="text-sm text-gray-500 mt-2">Latest update: {last_updated or date.today().isoformat()}</p>
    </div>
    {subcat_html}
    <section>
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">Calculators</h2>
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {cards_html}
      </div>
    </section>
  </main>
{footer}
  <script src="/assets/js/mobile-menu.js" defer></script>
  <script src="/search.js" defer></script>
</body>
</html>
"""


def main() -> None:
    today = date.today().isoformat()
    category_set = set(CATEGORY_SLUGS)
    subcategory_set = set(SUBCATEGORY_SLUGS)
    category_pages: Dict[str, List[Tuple[str, str, str]]] = {c: [] for c in CATEGORY_SLUGS}
    subcategory_pages: Dict[str, List[Tuple[str, str, str]]] = {s: [] for s in SUBCATEGORY_SLUGS}
    general_pages: List[Tuple[str, str, str]] = []

    for page in iter_html_pages():
        html = page.read_text(encoding="utf-8", errors="ignore")
        title = extract_title(html)
        description = extract_meta_description(html)
        cat_slug, sub_slug = extract_breadcrumb_slug(html)

        rel_url = f"/{page.relative_to(SITE_ROOT).as_posix()}"

        if cat_slug in category_set:
            category_pages[cat_slug].append((title, rel_url, description))
            if sub_slug in subcategory_set:
                subcategory_pages[sub_slug].append((title, rel_url, description))
        else:
            general_pages.append((title, rel_url, description))

    categories_dir = SITE_ROOT / "categories"
    subcategories_dir = SITE_ROOT / "subcategories"
    categories_dir.mkdir(parents=True, exist_ok=True)
    subcategories_dir.mkdir(parents=True, exist_ok=True)

    subcategories_by_category: Dict[str, List[str]] = {c: [] for c in CATEGORY_SLUGS}
    for sub_slug in SUBCATEGORY_SLUGS:
        parent_slug = parent_category_for_subcategory(sub_slug)
        if parent_slug:
            subcategories_by_category[parent_slug].append(sub_slug)

    for cat_slug in CATEGORY_SLUGS:
        posts = category_pages[cat_slug]
        sub_slugs = subcategories_by_category.get(cat_slug, [])
        sub_items = []
        for sub_slug in sub_slugs:
            if not subcategory_pages[sub_slug]:
                continue
            label = sub_slug.replace("-", " ").title()
            sub_items.append((label, f"/subcategories/{sub_slug}", f"{label} calculators"))

        if not posts and not sub_items:
            cat_path = categories_dir / f"{cat_slug}.html"
            if cat_path.exists():
                cat_path.unlink()
            continue

        heading = category_label(cat_slug)
        desc_bits = []
        if sub_items:
            desc_bits.append(f"{len(sub_items)} subcategories")
        if posts:
            desc_bits.append(f"{len(posts)} calculators")
        example = ", ".join([p[0] for p in posts[:3]])
        description = f"{heading} includes {', '.join(desc_bits)}."
        if example:
            description += f" Examples: {example}."
        html = build_page_html(
            f"{heading} | CalcDomain",
            heading,
            posts,
            f"/categories/{cat_slug}",
            section_slug="categories",
            description=description,
            subcategory_items=sub_items,
            last_updated=today,
        )
        (categories_dir / f"{cat_slug}.html").write_text(html, encoding="utf-8")

    for sub_slug in SUBCATEGORY_SLUGS:
        posts = subcategory_pages[sub_slug]
        if not posts:
            sub_path = subcategories_dir / f"{sub_slug}.html"
            if sub_path.exists():
                sub_path.unlink()
            continue
        heading = sub_slug.replace("-", " ").title()
        parent_slug = parent_category_for_subcategory(sub_slug)
        parent_label = category_label(parent_slug) if parent_slug else None
        example = ", ".join([p[0] for p in posts[:3]])
        description = f"{heading} includes {len(posts)} calculators."
        if example:
            description += f" Examples: {example}."
        html = build_page_html(
            f"{heading} | CalcDomain",
            heading,
            posts,
            f"/subcategories/{sub_slug}",
            section_slug="subcategories",
            parent_label=parent_label,
            parent_slug=parent_slug,
            description=description,
            last_updated=today,
        )
        (subcategories_dir / f"{sub_slug}.html").write_text(html, encoding="utf-8")

    general_heading = "General"
    if general_pages:
        example = ", ".join([p[0] for p in general_pages[:3]])
        description = f"General includes {len(general_pages)} calculators."
        if example:
            description += f" Examples: {example}."
        general_html = build_page_html(
            "General | CalcDomain",
            general_heading,
            general_pages,
            "/categories/general",
            section_slug="categories",
            description=description,
            last_updated=today,
        )
        (categories_dir / "general.html").write_text(general_html, encoding="utf-8")
    else:
        general_path = categories_dir / "general.html"
        if general_path.exists():
            general_path.unlink()

    print(
        f"Wrote {len(CATEGORY_SLUGS)} category pages, "
        f"{len(SUBCATEGORY_SLUGS)} subcategory pages, and general category."
    )
    categories_from_csv = read_categories_from_csv()
    if not categories_from_csv:
        categories_from_csv = CATEGORY_SLUGS + (["general"] if general_pages else [])
    update_footer_template(categories_from_csv)
    update_site_footers()
    update_homepage(categories_from_csv, today)
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
