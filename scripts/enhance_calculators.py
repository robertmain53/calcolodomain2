#!/usr/bin/env python3
"""
Enhance specific calculator pages by applying the modern CalcDomain layout,
injecting breadcrumbs, header/footer, and a Related Tools sidebar, and ensure
each tool appears on its category and subcategory listing pages.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "calculators-data.json"

CATEGORY_INFO = {
    "science": {"name": "Science", "path": "science.html"},
    "math": {"name": "Math & Conversions", "path": "math-conversions.html"},
    "finance": {"name": "Finance", "path": "finance.html"},
    "health": {"name": "Health & Fitness", "path": "health-fitness.html"},
    "lifestyle": {"name": "Lifestyle & Everyday", "path": "lifestyle-everyday.html"},
    "engineering": {"name": "Engineering", "path": "engineering.html"},
    "construction": {"name": "Construction & DIY", "path": "construction-diy.html"},
}

SUBCATEGORY_INFO = {
    "chemistry": {
        "name": "Chemistry",
        "path": "subcategories/chemistry.html",
        "category": "science",
        "category_marker": '<section id="chemistry">',
    },
    "physics": {
        "name": "Physics",
        "path": "subcategories/physics.html",
        "category": "science",
        "category_marker": '<section id="physics">',
    },
    "biology": {
        "name": "Biology & Genetics",
        "path": "subcategories/biology.html",
        "category": "science",
        "category_marker": '<section id="biology">',
    },
    "geometry": {
        "name": "Geometry",
        "path": "subcategories/geometry.html",
        "category": "math",
        "category_marker": "<!-- Sub-Category: Geometry -->",
    },
    "measurement-unit-conversions": {
        "name": "Measurement Unit Conversions",
        "path": "subcategories/measurement-unit-conversions.html",
        "category": "math",
        "category_marker": "<!-- Sub-Category: Measurement Unit Conversions -->",
    },
    "core-math-algebra": {
        "name": "Core Math & Algebra",
        "path": "subcategories/core-math-algebra.html",
        "category": "math",
        "category_marker": "<!-- Sub-Category: Core Math & Algebra -->",
    },
    "finance-investment": {
        "name": "Investment",
        "path": "subcategories/finance-investment.html",
        "category": "finance",
        "category_marker": "<!-- Sub-Category: Investment -->",
    },
    "finance-loans-debt": {
        "name": "Loans & Debt",
        "path": "subcategories/finance-loans-debt.html",
        "category": "finance",
        "category_marker": "<!-- Sub-Category: Loans & Debt -->",
    },
    "finance-mortgage-real-estate": {
        "name": "Mortgage & Real Estate",
        "path": "subcategories/finance-mortgage-real-estate.html",
        "category": "finance",
        "category_marker": "<!-- Sub-Category: Mortgage & Real Estate -->",
    },
    "finance-taxes": {
        "name": "Taxes",
        "path": "subcategories/taxes.html",
        "category": "finance",
        "category_marker": "<!-- Sub-Category: Taxes -->",
    },
    "business-small-biz": {
        "name": "Business & Small Biz",
        "path": "subcategories/business-small-biz.html",
        "category": "finance",
        "category_marker": "<!-- Sub-Category: Business & Small Biz -->",
    },
    "fitness": {
        "name": "Fitness",
        "path": "subcategories/fitness.html",
        "category": "health",
        "category_marker": "<!-- Sub-Category: Fitness -->",
    },
    "health-metrics": {
        "name": "Health Metrics",
        "path": "subcategories/health-metrics.html",
        "category": "health",
        "category_marker": "<!-- Sub-Category: Health Metrics -->",
    },
    "automotive": {
        "name": "Automotive",
        "path": "subcategories/automotive.html",
        "category": "lifestyle",
        "category_marker": "<!-- Sub-Category: Automotive -->",
    },
    "hobbies": {
        "name": "Hobbies",
        "path": "subcategories/hobbies.html",
        "category": "lifestyle",
        "category_marker": "<!-- Sub-Category: Hobbies -->",
    },
    "miscellaneous": {
        "name": "Miscellaneous",
        "path": "subcategories/miscellaneous.html",
        "category": "lifestyle",
        "category_marker": "<!-- Sub-Category: Miscellaneous -->",
    },
    "time-date": {
        "name": "Time & Date",
        "path": "subcategories/time-date.html",
        "category": "lifestyle",
        "category_marker": "<!-- Sub-Category: Time & Date -->",
    },
    "mechanical-engineering": {
        "name": "Mechanical Engineering",
        "path": "subcategories/mechanical-engineering.html",
        "category": "engineering",
        "category_marker": "<!-- Mechanical Engineering Section -->",
    },
    "structural-engineering": {
        "name": "Structural Engineering",
        "path": "subcategories/structural-engineering.html",
        "category": "engineering",
        "category_marker": "<!-- Structural Engineering Section -->",
    },
    "electrical": {
        "name": "Electrical",
        "path": "subcategories/electrical.html",
        "category": "engineering",
        "category_marker": "<!-- Electrical Engineering Section -->",
    },
    "construction-diy-materials-estimation": {
        "name": "Materials Estimation",
        "path": "subcategories/construction-diy-materials-estimation.html",
        "category": "construction",
        "category_marker": "<!-- Sub-Category: Materials Estimation -->",
    },
}

PAGE_SUBCATEGORY = {
    "beer-lambert-law": "chemistry",
    "henderson-hasselbalch": "chemistry",
    "inscribed-angle-calculator": "geometry",
    "kite-calculator": "geometry",
    "volume-converter": "measurement-unit-conversions",
    "equilateral-triangle-calculator": "geometry",
    "reactance": "electrical",
    "cycling-speed": "fitness",
    "isosceles-triangle-calculator": "geometry",
    "pmi": "finance-mortgage-real-estate",
    "target-heart-rate": "health-metrics",
    "nonagon-calculator": "geometry",
    "forward-kinematics": "mechanical-engineering",
    "speed-converter": "measurement-unit-conversions",
    "weight-converter": "measurement-unit-conversions",
    "rhombus-calculator": "geometry",
    "cube-calculator": "geometry",
    "scalene-triangle-calculator": "geometry",
    "thin-lens-equation": "physics",
    "running-pace": "fitness",
    "dividend-yield": "finance-investment",
    "welded-connection": "structural-engineering",
    "student-loan-payoff": "finance-loans-debt",
    "bearing-life": "mechanical-engineering",
    "q-value": "physics",
    "balloon-loan": "finance-loans-debt",
    "golden-ratio": "geometry",
    "masonry-column-design": "structural-engineering",
    "car-depreciation": "automotive",
    "natural-frequency": "mechanical-engineering",
    "relativistic-mass": "physics",
    "hazen-williams": "mechanical-engineering",
    "darcy-weisbach": "mechanical-engineering",
    "yarn": "hobbies",
    "one-rep-max": "fitness",
    "arm": "finance-mortgage-real-estate",
    "heat-loss": "mechanical-engineering",
    "electronegativity-difference": "chemistry",
    "lmtd": "mechanical-engineering",
    "tire-size": "automotive",
    "oil-change": "automotive",
    "born-haber-cycle": "chemistry",
    "integral": "core-math-algebra",
    "interest-only-loan": "finance-loans-debt",
    "titration-curve": "chemistry",
    "duct-sizing": "mechanical-engineering",
    "chiller-load": "mechanical-engineering",
    "masonry-shear-wall-design": "structural-engineering",
    "isotope-abundance": "chemistry",
    "welding-cost": "structural-engineering",
    "empirical-formula": "chemistry",
    "unit-converter": "measurement-unit-conversions",
    "arrhenius-equation": "chemistry",
    "birthday": "time-date",
    "fin-heat-transfer": "mechanical-engineering",
    "portfolio-standard-deviation": "finance-investment",
    "stoichiometry": "chemistry",
    "vat": "finance-taxes",
    "derivative": "core-math-algebra",
    "probability": "core-math-algebra",
    "ficks-law": "chemistry",
    "mpg": "automotive",
    "vo2-max": "fitness",
    "journal-bearing-design": "mechanical-engineering",
    "final-grade": "miscellaneous",
    "limit": "core-math-algebra",
    "gibbs-free-energy": "chemistry",
    "crane-runway-beam-design": "structural-engineering",
    "uncertainty-principle": "physics",
    "island-biogeography": "biology",
    "photoelectric-effect": "physics",
    "nernst-equation": "chemistry",
    "life-table": "health-metrics",
    "chemical-equation-balancer": "chemistry",
    "beta": "finance-investment",
    "fuel-cost": "automotive",
    "speeds-and-feeds": "mechanical-engineering",
    "centripetal-force": "physics",
    "niche-breadth": "biology",
    "hydrostatic-pressure": "physics",
    "sharpe-ratio": "finance-investment",
    "psychrometric-chart": "mechanical-engineering",
    "frustum-volume": "geometry",
    "rectangular-prism-volume": "geometry",
    "knitting-gauge": "hobbies",
    "rot13": "miscellaneous",
    "cell-doubling-time": "biology",
    "thermal-stress": "mechanical-engineering",
    "pressure-vessel-design": "mechanical-engineering",
    "chain-drive-design": "mechanical-engineering",
    "ctr": "business-small-biz",
    "roas": "business-small-biz",
    "canadian-mortgage": "finance-mortgage-real-estate",
    "regex-tester": "miscellaneous",
    "regular-polygon-area": "geometry",
    "dscr": "finance-mortgage-real-estate",
    "iban-validator": "finance-loans-debt",
    "quartile": "core-math-algebra",
    "mortgage-points": "finance-mortgage-real-estate",
    "profitability-index": "finance-investment",
    "poker-odds": "hobbies",
    "candle-making": "hobbies",
    "sewing-yardage": "hobbies",
    "darts-checkout": "hobbies",
    "epoxy-resin": "construction-diy-materials-estimation",
}

RELATED_BY_SUBCATEGORY = {
    "chemistry": [
        "molarity",
        "dilution",
        "stoichiometry",
        "titration-curve",
        "nernst-equation",
        "arrhenius-equation",
        "electronegativity-difference",
        "gibbs-free-energy",
    ],
    "physics": [
        "centripetal-force",
        "thin-lens-equation",
        "photoelectric-effect",
        "relativistic-mass",
        "uncertainty-principle",
        "hydrostatic-pressure",
        "q-value",
    ],
    "biology": [
        "cell-doubling-time",
        "niche-breadth",
        "island-biogeography",
        "life-table",
        "bacterial-growth-curve",
    ],
    "geometry": [
        "triangle-calculator",
        "circle-calculator",
        "area-calculator",
        "volume-calculator",
        "surface-area-calculator",
        "regular-polygon-area",
    ],
    "measurement-unit-conversions": [
        "length-converter",
        "conversions-temperature",
        "weight-converter",
        "speed-converter",
        "unit-converter",
        "volume-converter",
    ],
    "core-math-algebra": [
        "derivative",
        "integral",
        "limit",
        "probability",
        "quadratic-formula",
        "polynomial",
    ],
    "finance-investment": [
        "roi",
        "irr",
        "npv",
        "beta",
        "sharpe-ratio",
        "dividend-yield",
        "profitability-index",
        "portfolio-standard-deviation",
    ],
    "finance-loans-debt": [
        "loan-payoff",
        "loan-comparison",
        "interest-only-loan",
        "balloon-loan",
        "student-loan-payoff",
        "apr",
        "iban-validator",
    ],
    "finance-mortgage-real-estate": [
        "mortgage-payment",
        "mortgage-points",
        "refinance-calculator",
        "canadian-mortgage",
        "arm",
        "pmi",
        "dscr",
    ],
    "finance-taxes": [
        "tax-bracket-calculator",
        "sales-tax-calculator",
        "vat",
        "income-tax-calculator",
        "capital-gains-tax",
    ],
    "business-small-biz": [
        "roi",
        "break-even-calculator",
        "contribution-margin-calculator",
        "ctr",
        "roas",
        "profit-margin-calculator",
    ],
    "fitness": [
        "running-pace",
        "vo2-max",
        "one-rep-max",
        "cycling-speed",
        "calorie",
        "tdee",
    ],
    "health-metrics": [
        "bmi-calculator",
        "body-fat",
        "target-heart-rate",
        "waist-to-hip-ratio-calculator",
        "vo2-max",
        "life-table",
    ],
    "automotive": [
        "mpg",
        "fuel-cost",
        "tire-size",
        "car-depreciation",
        "oil-change",
    ],
    "hobbies": [
        "candle-making",
        "knitting-gauge",
        "sewing-yardage",
        "poker-odds",
        "darts-checkout",
        "yarn",
    ],
    "miscellaneous": [
        "unit-converter",
        "final-grade",
        "rot13",
        "regex-tester",
        "word-counter",
    ],
    "time-date": [
        "age-calculator",
        "day-of-week-calculator",
        "time-difference-calculator",
        "date-duration",
        "birthday",
    ],
    "mechanical-engineering": [
        "duct-sizing",
        "chiller-load",
        "psychrometric-chart",
        "fin-heat-transfer",
        "chain-drive-design",
        "pressure-vessel-design",
        "thermal-stress",
        "speeds-and-feeds",
        "bearing-life",
        "natural-frequency",
    ],
    "structural-engineering": [
        "wood-beam-design",
        "welded-connection",
        "masonry-column-design",
        "masonry-shear-wall-design",
        "crane-runway-beam-design",
        "welding-cost",
    ],
    "electrical": [
        "ohm-s-law-calculator",
        "voltage-divider",
        "amps-to-watts",
        "reactance",
        "watts-to-amps",
    ],
    "construction-diy-materials-estimation": [
        "concrete-calculator",
        "tile-calculator",
        "epoxy-resin",
        "drywall-calculator",
        "mulch-calculator",
    ],
}

TARGET_SLUGS = sorted(PAGE_SUBCATEGORY.keys())


def load_calculator_meta() -> Dict[str, Dict[str, str]]:
    with DATA_PATH.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    return {item["slug"]: item for item in data}


# --- Helpers replicated (and trimmed) from tools/normalize_site.py ---

def extract_tag(pattern: str, text: str, flags: int = re.I | re.S) -> Tuple[str, str]:
    match = re.search(pattern, text, flags)
    if not match:
        return "", text
    new_text = text[:match.start()] + text[match.end():]
    return match.group(0).strip(), new_text


def clean_head(head_html: str) -> Tuple[str, str, str, str, str]:
    title_tag, rest = extract_tag(r"<title>.*?</title>", head_html)
    desc_tag, rest = extract_tag(r'<meta[^>]+name=["\']description["\'][^>]*>', rest)
    canon_tag, rest = extract_tag(r'<link[^>]+rel=["\']canonical["\'][^>]*>', rest)

    rest = re.sub(r'<meta[^>]+charset[^>]*>', "", rest, flags=re.I)
    rest = re.sub(r'<meta[^>]+viewport[^>]*>', "", rest, flags=re.I)
    rest = re.sub(r'<script[^>]+cdn\.tailwindcss\.com[^>]*>\s*</script>', "", rest, flags=re.I)
    rest = re.sub(r'<link[^>]+fonts\.googleapis\.com[^>]*>', "", rest, flags=re.I)
    rest = re.sub(r'<script[^>]+search\.js[^>]*>\s*</script>', "", rest, flags=re.I)
    rest = re.sub(r'<script[^>]+MathJax[^>]*>\s*</script>', "", rest, flags=re.I)
    rest = re.sub(r'<script>\s*window\.MathJax[\s\S]*?</script>', "", rest, flags=re.I)
    rest = re.sub(r'<link[^>]+rel=["\'](?:shortcut icon|icon|apple-touch-icon|manifest)["\'][^>]*>', "", rest, flags=re.I)

    style_blocks = re.findall(r"<style[\s\S]*?</style>", rest, flags=re.I)
    rest = re.sub(r"<style[\s\S]*?</style>", "", rest, flags=re.I)

    head_extra = rest.strip()
    style_extra = "\n".join(style_blocks)
    return title_tag, desc_tag, canon_tag, style_extra, head_extra


def strip_header_footer(body_html: str) -> Tuple[str, str, List[str]]:
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
    body = re.sub(r'<aside[\s\S]*?class="[^"]*w-full[^>]*>\s*[\s\S]*?</aside>', "", body, flags=re.I)
    body = body.strip()

    trailing_scripts: List[str] = []
    pattern = re.compile(r"(?:<script[\s\S]*?</script>\s*)$", re.I)
    while True:
        match = pattern.search(body)
        if not match:
            break
        trailing_scripts.insert(0, match.group().strip())
        body = body[:match.start()].rstrip()

    return body, breadcrumb_html, trailing_scripts


def extract_intro(content: str) -> Tuple[str, str, str]:
    h1_tag, remaining = extract_tag(r"<h1[\s\S]*?</h1>", content)
    p_tag, remaining = extract_tag(r"<p[\s\S]*?</p>", remaining)
    return h1_tag, p_tag, remaining.strip()


def ensure_heading(title_tag: str, h1_tag: str) -> Tuple[str, str]:
    title_text = ""
    if title_tag:
        title_text = re.sub(r"</?title>", "", title_tag, flags=re.I).strip()
    if not h1_tag and title_text:
        h1_tag = f'<h1 class="text-3xl font-extrabold text-gray-900 mb-2">{title_text}</h1>'
    elif h1_tag:
        if 'class="' in h1_tag:
            h1_tag = re.sub(
                r'class="([^"]*)"',
                lambda m: m.group(0)[:-1] + " text-3xl font-extrabold text-gray-900 mb-2\"",
                h1_tag,
                count=1,
            )
        else:
            h1_tag = h1_tag.replace("<h1", '<h1 class="text-3xl font-extrabold text-gray-900 mb-2"', 1)
    return title_text, h1_tag


def build_default_intro(meta_desc: str) -> str:
    if meta_desc:
        match = re.search(r'content=["\']([^"\']+)["\']', meta_desc)
        if match:
            return f'<p class="text-gray-600 mb-6">{match.group(1)}</p>'
    return '<p class="text-gray-600 mb-6">Use this calculator to run quick scenarios and explore the detailed explanation below.</p>'


def indent_html(html: str, spaces: int) -> str:
    if not html.strip():
        return ""
    indent = " " * spaces
    lines = [line.rstrip() for line in html.splitlines()]
    return "\n".join(f"{indent}{line}" if line else "" for line in lines)


HEAD_SNIPPET = """<head>
<link rel="icon" type="image/png" href="https://calcdomain.com/favicon-96x96.png" sizes="96x96" />
<link rel="icon" type="image/svg+xml" href="https://calcdomain.com/favicon.svg" />
<link rel="shortcut icon" href="https://calcdomain.com/favicon.ico" />
<link rel="apple-touch-icon" sizes="180x180" href="https://calcdomain.com/apple-touch-icon.png" />
<link rel="manifest" href="https://calcdomain.com/site.webmanifest" />
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
    <link rel="preload" href="https://calcdomain.com/assets/js/mobile-menu.js" as="script">
    <link rel="preload" href="https://calcdomain.com/assets/js/page-enhancements.js" as="script">
    <script src="https://calcdomain.com/search.js" defer></script>
</head>"""

TAILWIND_STYLE = """
        body { font-family: 'Inter', sans-serif; }
        .legacy-content h2 { font-size: 1.5rem; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem; }
        .legacy-content h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; }
        .legacy-content p { margin-bottom: 1rem; line-height: 1.65; }
        .legacy-content ul, .legacy-content ol { margin-left: 1.5rem; margin-bottom: 1rem; }
        .legacy-content li { margin-bottom: 0.5rem; }
""".strip("\n")

HEADER_TEMPLATE = """    <header class="bg-white shadow-sm sticky top-0 z-50">
        <nav class="container mx-auto px-4 lg:px-6 py-4">
            <div class="flex justify-between items-center">
                <a href="https://calcdomain.com/index.html" class="text-2xl font-bold text-blue-600">CalcDomain</a>
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
                    <a href="https://calcdomain.com/search.html" class="text-gray-700 hover:text-blue-600">Advanced Search</a>
                    <a href="https://calcdomain.com/index.html#categories" class="text-gray-700 hover:text-blue-600">Categories</a>
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
                    <a href="https://calcdomain.com/search.html" class="block py-2 text-gray-700 hover:text-blue-600">Advanced Search</a>
                    <a href="https://calcdomain.com/index.html#categories" class="block py-2 text-gray-700 hover:text-blue-600">Categories</a>
                </div>
            </div>
        </nav>
    </header>"""

FOOTER_TEMPLATE = """    <footer class="bg-white border-t mt-12">
        <div class="container mx-auto px-6 py-8 text-center text-gray-600 text-sm">
            <p>&copy; 2025 CalcDomain. All Rights Reserved.</p>
            <div class="mt-4 space-x-4">
                <a href="https://calcdomain.com/about.html" class="hover:text-blue-600">About</a>
                <a href="https://calcdomain.com/contact.html" class="hover:text-blue-600">Contact</a>
                <a href="https://calcdomain.com/privacy.html" class="hover:text-blue-600">Privacy</a>
                <a href="https://calcdomain.com/terms.html" class="hover:text-blue-600">Terms</a>
            </div>
        </div>
    </footer>"""

SHARED_SCRIPTS = """    <script>
        document.getElementById('mobile-menu-toggle')?.addEventListener('click', () => {
            const menu = document.getElementById('mobile-menu');
            menu?.classList.toggle('hidden');
        });
    </script>
    <script defer src="https://calcdomain.com/assets/js/mobile-menu.js"></script>
    <script defer src="https://calcdomain.com/assets/js/page-enhancements.js"></script>"""

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


def build_breadcrumb(category: Dict[str, str], subcategory: Dict[str, str], title: str) -> str:
    return (
        '                <nav class="text-sm text-gray-600 mb-4" aria-label="Breadcrumb">\n'
        '                    <a href="https://calcdomain.com/index.html" class="hover:text-blue-600">Home</a> &raquo;\n'
        f'                    <a href="https://calcdomain.com/{category["path"]}" class="hover:text-blue-600">{category["name"]}</a> &raquo;\n'
        f'                    <a href="https://calcdomain.com/{subcategory["path"]}" class="hover:text-blue-600">{subcategory["name"]}</a> &raquo;\n'
        f'                    <span class="text-gray-900">{title}</span>\n'
        "                </nav>"
    )


def build_related_card(slug: str, related_slugs: List[str], meta_lookup: Dict[str, Dict[str, str]]) -> str:
    items = []
    for rel in related_slugs:
        if rel == slug:
            continue
        meta = meta_lookup.get(rel, {})
        rel_title = meta.get("title") or rel.replace("-", " ").title()
        items.append(
            f'                        <li><a href="https://calcdomain.com/{rel}.html" class="text-blue-600 hover:underline">{rel_title}</a></li>'
        )
        if len(items) >= 5:
            break
    if not items:
        items.append('                        <li><a href="https://calcdomain.com/search.html" class="text-blue-600 hover:underline">Explore all calculators</a></li>')
    return (
        "                    <div class=\"bg-white p-6 rounded-lg shadow-md\">\n"
        "                        <h2 class=\"text-lg font-semibold text-gray-900 mb-3\">Related Tools</h2>\n"
        "                        <ul class=\"space-y-2 text-sm text-gray-700\">\n"
        + "\n".join(items)
        + "\n                        </ul>\n"
        "                    </div>"
    )


def normalize_links(html: str, page_path: Path) -> str:
    def replacement(match: re.Match[str]) -> str:
        href = match.group(1)
        if not href or href.startswith(("#", "mailto:", "javascript:")):
            return match.group(0)
        if "://" in href:
            return match.group(0)
        full = (page_path.parent / href).resolve()
        if full.suffix == "":
            tentative = full.with_suffix(".html")
            if tentative.exists():
                href_new = os.path.relpath(tentative, page_path.parent).replace(os.sep, "/")
                return match.group(0).replace(href, href_new)
        return match.group(0)

    return re.sub(r'href="([^"]+)"', replacement, html)


def enhance_page(slug: str, subcat_key: str, meta_lookup: Dict[str, Dict[str, str]]) -> None:
    path = ROOT / f"{slug}.html"
    if not path.exists():
        print(f"[skip] {slug}.html not found")
        return

    subcat = SUBCATEGORY_INFO[subcat_key]
    category = CATEGORY_INFO[subcat["category"]]
    meta = meta_lookup.get(slug, {})

    text = path.read_text(encoding="utf-8", errors="ignore")
    head_match = re.search(r"<head[\s\S]*?</head>", text, flags=re.I)
    body_match = re.search(r"<body[\s\S]*?</body>", text, flags=re.I)
    if not head_match or not body_match:
        print(f"[warn] unable to parse {slug}")
        return

    head_inner = re.sub(r"^<head[^>]*>", "", head_match.group(0), flags=re.I)
    head_inner = re.sub(r"</head>\s*$", "", head_inner, flags=re.I).strip()

    body_inner = re.sub(r"^<body[^>]*>", "", body_match.group(0), flags=re.I)
    body_inner = re.sub(r"</body>\s*$", "", body_inner, flags=re.I).strip()

    title_tag, desc_tag, canon_tag, style_extra, head_extra = clean_head(head_inner)
    body_content, _, trailing_scripts = strip_header_footer(body_inner)
    h1_tag, intro_tag, remaining = extract_intro(body_content)
    title_text, h1_tag = ensure_heading(title_tag, h1_tag)
    intro = None
    if intro_tag:
        intro = re.sub(r'<p[^>]*>', '<p class="text-gray-600 mb-6">', intro_tag, count=1, flags=re.I)
    if not intro:
        intro = build_default_intro(desc_tag)
    if not title_text:
        title_text = meta.get("title") or slug.replace("-", " ").title()

    legacy_block = "\n".join(
        [
            f"                    {h1_tag}",
            f"                    {intro}",
            "                    <div class=\"legacy-content space-y-6\">",
            indent_html(remaining, 20),
            "                    </div>",
        ]
    )

    related_candidates = RELATED_BY_SUBCATEGORY.get(subcat_key, [])
    aside_card = build_related_card(slug, related_candidates, meta_lookup)

    breadcrumb_block = build_breadcrumb(category, subcat, title_text)

    page_scripts = "\n".join(trailing_scripts)

    new_head = HEAD_SNIPPET.format(
        title_tag=title_tag or f"<title>{title_text}</title>",
        description_tag=desc_tag or (meta.get("description") and f'<meta name="description" content="{meta["description"]}">') or "",
        canonical_tag=canon_tag or f'<link rel="canonical" href="https://calcdomain.com/{slug}.html">',
        meta_extra=head_extra,
        tailwind_style="\n        ".join(TAILWIND_STYLE.splitlines()),
        style_extra=style_extra,
    )

    new_body = BODY_TEMPLATE.format(
        header=HEADER_TEMPLATE,
        breadcrumb_block=breadcrumb_block,
        content_block=legacy_block,
        aside_block=aside_card,
        footer=FOOTER_TEMPLATE,
        shared_scripts=SHARED_SCRIPTS,
        page_scripts=indent_html(page_scripts, 4) if page_scripts else "",
    )

    new_html = "<!DOCTYPE html>\n<html lang=\"en\">\n" + new_head + "\n" + new_body + "\n</html>\n"
    new_html = normalize_links(new_html, path)
    new_html = re.sub(
        r'(    <link rel="preload" href="https://calcdomain.com/assets/js/mobile-menu.js" as="script">\n)+',
        '    <link rel="preload" href="https://calcdomain.com/assets/js/mobile-menu.js" as="script">\n',
        new_html,
    )
    new_html = re.sub(
        r'(    <link rel="preload" href="https://calcdomain.com/assets/js/page-enhancements.js" as="script">\n)+',
        '    <link rel="preload" href="https://calcdomain.com/assets/js/page-enhancements.js" as="script">\n',
        new_html,
    )
    new_html = re.sub(
        r'(    <script defer src="https://calcdomain.com/assets/js/mobile-menu.js"></script>\n)+',
        '    <script defer src="https://calcdomain.com/assets/js/mobile-menu.js"></script>\n',
        new_html,
    )
    new_html = re.sub(
        r'(    <script defer src="https://calcdomain.com/assets/js/page-enhancements.js"></script>\n)+',
        '    <script defer src="https://calcdomain.com/assets/js/page-enhancements.js"></script>\n',
        new_html,
    )

    lines: List[str] = []
    seen_once = set()
    targets = {
        '<link rel="preload" href="https://calcdomain.com/assets/js/mobile-menu.js" as="script">',
        '<link rel="preload" href="https://calcdomain.com/assets/js/page-enhancements.js" as="script">',
        '<script defer src="https://calcdomain.com/assets/js/mobile-menu.js"></script>',
        '<script defer src="https://calcdomain.com/assets/js/page-enhancements.js"></script>',
    }
    for line in new_html.splitlines():
        stripped = line.strip()
        if 'href="/assets/js/mobile-menu.js"' in stripped or 'href="/assets/js/page-enhancements.js"' in stripped:
            continue
        if stripped in targets:
            if stripped in seen_once:
                continue
            seen_once.add(stripped)
        lines.append(line)
    new_html = "\n".join(lines) + "\n"

    path.write_text(new_html, encoding="utf-8")


def build_card_html(slug: str, meta: Dict[str, str], indent: str, absolute: bool = False) -> str:
    title = meta.get("title") or slug.replace("-", " ").title()
    description = meta.get("description") or "Explore this calculator to run scenarios and understand the underlying formulas."
    href = f"https://calcdomain.com/{slug}.html" if absolute else f"{slug}.html"
    block = [
        '<a href="{href}" class="card-hover bg-white p-5 rounded-lg shadow-sm border flex items-start gap-4">'.format(href=href),
        '    <div class="bg-blue-100 p-3 rounded-full">',
        '        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path></svg>',
        "    </div>",
        "    <div>",
        f'        <h3 class="font-semibold text-gray-800">{title}</h3>',
        f'        <p class="text-sm text-gray-600 mt-1">{description}</p>',
        "    </div>",
        "</a>",
    ]
    return "\n".join(indent + line if line else "" for line in block)


def find_matching_div(text: str, start_index: int) -> int:
    depth = 0
    idx = start_index
    while idx < len(text):
        if text.startswith("<div", idx):
            depth += 1
            close = text.find(">", idx)
            if close == -1:
                return -1
            idx = close + 1
            continue
        if text.startswith("</div>", idx):
            depth -= 1
            idx += len("</div>")
            if depth == 0:
                return idx
            continue
        idx += 1
    return -1


def ensure_in_listing(
    file_path: Path, marker: str, slug: str, card_html: str, grid_keyword: str
) -> None:
    text = file_path.read_text(encoding="utf-8")
    if f"{slug}.html" in text:
        return

    marker_idx = text.find(marker)
    if marker_idx == -1:
        return

    grid_idx = text.find(grid_keyword, marker_idx)
    if grid_idx == -1:
        return

    div_start = text.rfind("<div", marker_idx, grid_idx + len(grid_keyword))
    if div_start == -1 or div_start < grid_idx:
        div_start = grid_idx

    closing_idx = find_matching_div(text, div_start)
    if closing_idx == -1:
        return

    insert_pos = closing_idx - len("</div>")
    text = text[:insert_pos] + "\n" + card_html + "\n" + text[insert_pos:]
    file_path.write_text(text, encoding="utf-8")


def ensure_subcategory_listing(slug: str, subcat_key: str, meta_lookup: Dict[str, Dict[str, str]]) -> None:
    info = SUBCATEGORY_INFO[subcat_key]
    subcat_path = ROOT / info["path"]
    if not subcat_path.exists():
        return
    text = subcat_path.read_text(encoding="utf-8")
    if f"{slug}.html" in text:
        return
    meta = meta_lookup.get(slug, {})
    card = build_card_html(slug, meta, " " * 12, absolute=True)
    marker = "<!-- Calculators Grid -->"
    marker_idx = text.find(marker)
    if marker_idx == -1:
        return
    grid_idx = text.find('<div class="grid', marker_idx)
    if grid_idx == -1:
        return
    closing_idx = find_matching_div(text, grid_idx)
    if closing_idx == -1:
        return
    insert_pos = closing_idx - len("</div>")
    text = text[:insert_pos] + "\n" + card + "\n" + text[insert_pos:]
    subcat_path.write_text(text, encoding="utf-8")


def ensure_category_listing(slug: str, subcat_key: str, meta_lookup: Dict[str, Dict[str, str]]) -> None:
    info = SUBCATEGORY_INFO[subcat_key]
    category_key = info["category"]
    cat_info = CATEGORY_INFO[category_key]
    cat_path = ROOT / cat_info["path"]
    if not cat_path.exists():
        return

    text = cat_path.read_text(encoding="utf-8")
    if f"{slug}.html" in text:
        return

    meta = meta_lookup.get(slug, {})
    card = build_card_html(slug, meta, " " * 28, absolute=False)

    marker = info.get("category_marker")
    if category_key == "engineering":
        ensure_engineering_section(slug, subcat_key, meta_lookup)
        return

    if not marker or marker not in text:
        return

    grid_keyword = '<div class="grid'
    if category_key == "science":
        grid_keyword = '<div class="card-grid'

    ensure_in_listing(cat_path, marker, slug, card, grid_keyword)


def ensure_engineering_section(slug: str, subcat_key: str, meta_lookup: Dict[str, Dict[str, str]]) -> None:
    path = ROOT / CATEGORY_INFO["engineering"]["path"]
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if f"{slug}.html" in text:
        return
    meta = meta_lookup.get(slug, {})
    title = meta.get("title") or slug.replace("-", " ").title()
    description = meta.get("description") or "Run mechanical and structural engineering calculations with instant feedback."
    if subcat_key == "mechanical-engineering":
        section_heading = "Mechanical Engineering Calculators"
        section_id = "mechanical-engineering-calculators"
    elif subcat_key == "structural-engineering":
        section_heading = "Structural Engineering Calculators"
        section_id = "structural-engineering-calculators"
    else:
        section_heading = "Electrical Engineering Calculators"
        section_id = "electrical-engineering-calculators"

    section_marker = f'id="{section_id}"'
    if section_marker not in text:
        section_template = (
            f'    <section class="mb-10" id="{section_id}">\n'
            f'      <h2 class="text-2xl font-semibold text-gray-800 mb-4">{section_heading}</h2>\n'
            '      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">\n'
            '      </div>\n'
            '    </section>\n'
        )
        quick_start = text.find('<section class="mb-10">')
        if quick_start != -1:
            quick_end = text.find("</section>", quick_start)
            if quick_end != -1:
                insert_pos = quick_end + len("</section>")
            else:
                insert_pos = quick_start + len('<section class="mb-10">')
        else:
            insert_pos = text.find("</main>")
            if insert_pos == -1:
                insert_pos = len(text)
        text = text[:insert_pos] + "\n" + section_template + text[insert_pos:]

    section_idx = text.find(section_marker)
    if section_idx == -1:
        return
    grid_idx = text.find('<div class="grid', section_idx)
    if grid_idx == -1:
        return
    closing_idx = find_matching_div(text, grid_idx)
    if closing_idx == -1:
        return
    insert_pos = closing_idx - len("</div>")
    card = (
        '        <a href="{slug}.html" class="bg-white p-4 rounded-lg border shadow-sm hover:shadow-lg transition flex flex-col gap-2">\n'
        '          <h3 class="font-semibold text-gray-800">{title}</h3>\n'
        '          <p class="text-sm text-gray-600">{description}</p>\n'
        "        </a>"
    ).format(slug=slug, title=title, description=description)
    text = text[:insert_pos] + "\n" + card + "\n" + text[insert_pos:]
    path.write_text(text, encoding="utf-8")


def main() -> None:
    meta_lookup = load_calculator_meta()
    for slug in TARGET_SLUGS:
        subcat_key = PAGE_SUBCATEGORY[slug]
        enhance_page(slug, subcat_key, meta_lookup)
        ensure_subcategory_listing(slug, subcat_key, meta_lookup)
        ensure_category_listing(slug, subcat_key, meta_lookup)


if __name__ == "__main__":
    main()
