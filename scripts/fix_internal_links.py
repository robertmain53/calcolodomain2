#!/usr/bin/env python3
"""
Utility to clean up internal links, canonical tags, and breadcrumb metadata
across CalcDomain static HTML files.

Steps performed for each HTML file:
  * Normalize canonical link to https://calcdomain.com/<relative-path>
  * Replace known-bad URLs with current slugs
  * Repair breadcrumb JSON-LD items (category + subcategory mapping) and remove
    entries that still point to missing pages
  * Update visible anchor tags:
        - fix common typos (missing .html, bad slugs)
        - map legacy slugs to the new structure when a deterministic match exists
        - drop hyperlinks that would lead to 404s while preserving link text
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent

HTML_EXT = ".html"
DOMAIN = "https://calcdomain.com/"


def gather_existing_paths() -> set[str]:
    paths: set[str] = set()
    for file_path in ROOT.rglob(f"*{HTML_EXT}"):
        rel = file_path.relative_to(ROOT).as_posix()
        paths.add(rel)
    return paths


EXISTING_HTML = gather_existing_paths()


def rel_exists(path: str) -> bool:
    return path in EXISTING_HTML


# Direct replacements for legacy paths (relative without leading slash)
DIRECT_PATH_MAP: Dict[str, Optional[str]] = {
    "everyday-life.html": "lifestyle-everyday.html",
    "lifestyle.html": "lifestyle-everyday.html",
    "everyday/.html": "lifestyle-everyday.html",
    "everyday/miscellaneous.html": "subcategories/miscellaneous.html",
    "everyday/character-counter.html": "character-counter.html",
    "construction.html": "construction-diy.html",
    "health-and-fitness.html": "health-fitness.html",
    "geometry.html": "math-conversions.html",
    "analytic-geometry.html": "subcategories/geometry.html",
    "conic-classifier.html": "conic-classifier.html",
    "construction-diy/project-layout-design.html": "subcategories/construction-diy-project-layout-design.html",
    "engineering/electrical.html": "subcategories/electrical.html",
    "engineering/electrical/amps-to-watts-calculator.html": "amps-to-watts.html",
    "finance/loans-debt.html": "subcategories/finance-loans-debt.html",
    "math/calculus.html": "calculus.html",
    "math/geometry/polygons.html": "polygon-calculator.html",
    "math/geometry/volume-calculator.html": "volume-calculator.html",
    "science/chemistry.html": "subcategories/chemistry.html",
    "science/chemistry/calibration-curve.html": "calibration-curve.html",
    "science.html#biology.html": "science.html",
    "taxation/florida-income-tax-calculator.html": "florida-income-tax.html",
    "subcategories/construction-materials-estimation.html": "subcategories/construction-diy-materials-estimation.html",
    "subcategories/construction-materials.html": "subcategories/construction-diy-materials-estimation.html",
    "subcategories/construction-project-layout-design.html": "subcategories/construction-diy-project-layout-design.html",
    "subcategories/materials-estimation.html": "subcategories/construction-diy-materials-estimation.html",
    "subcategories/engineering-electrical.html": "subcategories/electrical.html",
    "subcategories/finance-business-small-biz.html": "subcategories/business-small-biz.html",
    "subcategories/finance-taxes.html": "subcategories/taxes.html",
    "subcategories/health-diet-nutrition.html": "subcategories/diet-nutrition.html",
    "subcategories/lifestyle-automotive.html": "subcategories/automotive.html",
    "subcategories/lifestyle-everyday-hobbies.html": "subcategories/hobbies.html",
    "subcategories/lifestyle-everyday.html": "lifestyle-everyday.html",
    "subcategories/lifestyle-misc.html": "subcategories/miscellaneous.html",
    "subcategories/lifestyle-miscellaneous.html": "subcategories/miscellaneous.html",
    "subcategories/lmiscellaneous.html": "subcategories/miscellaneous.html",
    "subcategories/geometry-2d.html": "subcategories/geometry.html",
    "subcategories/math-analytic-geometry.html": "subcategories/geometry.html",
    "subcategories/math-polygons.html": "subcategories/geometry.html",
    "subcategories/it-cctv.html": "subcategories/miscellaneous.html",
    "subcategories/workshop-layout-calculator.html": "subcategories/construction-diy-project-layout-design.html",
    "subcategories/index.html": "index.html",
    "subcategories/about.html": "about.html",
    "subcategories/contact.html": "contact.html",
    "subcategories/privacy.html": "privacy.html",
    "subcategories/terms.html": "terms.html",
    "subcategories/search.html": "search.html",
    "subcategories/template-subcat.html": None,
    "subcategories/timezone-converter.html": "subcategories/time-date.html",
    "subcategories/time-converter.html": "subcategories/time-date.html",
    "subcategories/time-converter/index.html": "subcategories/time-date.html",
    "subcategories/mph-to-mach.html": "subcategories/measurement-unit-conversions.html",
    "subcategories/mach-to-mph.html": "subcategories/measurement-unit-conversions.html",
    "subcategories/technology-networking.html": "subcategories/miscellaneous.html",
    "priming-sugar-calculator-5-gallons": "priming-sugar-5-gallons.html",
    "priming-sugar-calculator-5-gallons.html": "priming-sugar-5-gallons.html",
}


def converter_category_fallback(path: str) -> Optional[str]:
    """Collapse legacy converter subcategory pages into the new measurement unit hub."""
    if not path.startswith("subcategories/"):
        return None
    name = path.split("/", 1)[1]
    if "converter" in name or "conversions" in name or name.endswith("-converter.html"):
        return "subcategories/measurement-unit-conversions.html"
    if name in {
        "angle-converter.html",
        "area-converter.html",
        "calendar-converter.html",
        "capacitance-converter.html",
        "charge-converter.html",
        "clothing-size-converter.html",
        "color-converter.html",
        "conductivity-converter.html",
        "coordinate-converter.html",
        "coordinate-conversions.html",
        "coordinate-converters.html",
        "currency-converter.html",
        "current-converter.html",
        "data-storage-converter.html",
        "data-transfer-converter.html",
        "density-converter.html",
        "drill-bit-converter.html",
        "electric-field-converter.html",
        "energy-converter.html",
        "energy-conversions.html",
        "flow-rate-converter.html",
        "font-size-converter.html",
        "force-converter.html",
        "frequency-converter.html",
        "fuel-consumption-converter.html",
        "illuminance-converter.html",
        "inductance-converter.html",
        "length-converter.html",
        "luminosity-converter.html",
        "magnetic-field-converter.html",
        "number-base-converter.html",
        "paper-size-converter.html",
        "pipe-size-converter.html",
        "power-converter.html",
        "pressure-converter.html",
        "radiation-converter.html",
        "radioactivity-converter.html",
        "resistance-converter.html",
        "ring-size-converter.html",
        "screen-resolution-converter.html",
        "screw-size-converter.html",
        "shoe-size-converter.html",
        "speed-converter.html",
        "speed-conversions.html",
        "temperature-converter.html",
        "tire-size-converter.html",
        "torque-converter.html",
        "viscosity-converter.html",
        "voltage-converter.html",
        "volume-converter.html",
        "weight-converter.html",
        "wire-gauge-converter.html",
        "workshop-layout-calculator.html",
    }:
        return "subcategories/measurement-unit-conversions.html"
    return None


CATEGORY_MAP: Dict[str, Tuple[str, str]] = {
    "Construction": ("Construction & DIY", "construction-diy.html"),
    "Construction & DIY": ("Construction & DIY", "construction-diy.html"),
    "Construction DIY": ("Construction & DIY", "construction-diy.html"),
    "Engineering": ("Engineering", "engineering.html"),
    "Everyday Life": ("Lifestyle & Everyday", "lifestyle-everyday.html"),
    "Everyday life": ("Lifestyle & Everyday", "lifestyle-everyday.html"),
    "Lifestyle": ("Lifestyle & Everyday", "lifestyle-everyday.html"),
    "Lifestyle & Everyday": ("Lifestyle & Everyday", "lifestyle-everyday.html"),
    "Lifestyle Everyday": ("Lifestyle & Everyday", "lifestyle-everyday.html"),
    "Finance": ("Finance", "finance.html"),
    "Geometry": ("Math & Conversions", "math-conversions.html"),
    "Math": ("Math & Conversions", "math-conversions.html"),
    "Health & Fitness": ("Health & Fitness", "health-fitness.html"),
    "IT & Networking": ("Science & Technology", "science.html"),
    "Technology": ("Science & Technology", "science.html"),
    "Science": ("Science", "science.html"),
    "Taxation": ("Finance", "finance.html"),
}


SUBCATEGORY_MAP: Dict[str, Optional[str]] = {
    "Algebra": "subcategories/core-math-algebra.html",
    "Analytic Geometry": "subcategories/geometry.html",
    "Automotive": "subcategories/automotive.html",
    "Biology & Genetics": "subcategories/biology.html",
    "Business & Small Biz": "subcategories/business-small-biz.html",
    "Business Small Biz": "subcategories/business-small-biz.html",
    "CCTV & Surveillance": None,
    "Calculus": "subcategories/core-math-algebra.html",
    "Chemistry": "subcategories/chemistry.html",
    "Concrete Slab Calculator": "subcategories/construction-diy-materials-estimation.html",
    "Diet & Nutrition": "subcategories/diet-nutrition.html",
    "Electrical": "subcategories/electrical.html",
    "Electrical (General)": "subcategories/electrical.html",
    "Everyday": "subcategories/miscellaneous.html",
    "Fitness": "subcategories/fitness.html",
    "Flooring Calculator": "subcategories/construction-diy-materials-estimation.html",
    "Florida State Income Tax Calculator": "subcategories/taxes.html",
    "Geometry": "subcategories/geometry.html",
    "Health Metrics": "subcategories/health-metrics.html",
    "Hobbies": "subcategories/hobbies.html",
    "Investment": "subcategories/finance-investment.html",
    "Loans & Debt": "subcategories/finance-loans-debt.html",
    "Materials": "subcategories/construction-diy-materials-estimation.html",
    "Materials Estimation": "subcategories/construction-diy-materials-estimation.html",
    "Miscellaneous": "subcategories/miscellaneous.html",
    "Mortgage & Real Estate": "subcategories/finance-mortgage-real-estate.html",
    "Networking": None,
    "Nutrition": "subcategories/diet-nutrition.html",
    "Perimeter Calculator": "subcategories/geometry.html",
    "Personal Loans": "subcategories/finance-personal-loans.html",
    "Polygon Geometry": "subcategories/geometry.html",
    "Project Layout & Design": "subcategories/construction-diy-project-layout-design.html",
    "Project Layout Design": "subcategories/construction-diy-project-layout-design.html",
    "Retirement": "subcategories/finance-retirement.html",
    "Taxes": "subcategories/taxes.html",
    "Time & Date": "subcategories/time-date.html",
    "Time Date": "subcategories/time-date.html",
    "Time and Date": "subcategories/time-date.html",
    "polygon calculator": "subcategories/geometry.html",
}


TEXT_REPLACEMENTS: Tuple[Tuple[str, str], ...] = (
    ("httpsa://", "https://"),
    ("http://calcdomain.com/", DOMAIN),
    ("https://www.calcdomain.com/", DOMAIN),
    ("http://www.calcdomain.com/", DOMAIN),
    ("https://calcdomain.com/construction.html", f"{DOMAIN}construction-diy.html"),
    ("https://calcdomain.com/health-and-fitness.html", f"{DOMAIN}health-fitness.html"),
    ("https://calcdomain.com/everyday-life.html", f"{DOMAIN}lifestyle-everyday.html"),
    ("https://calcdomain.com/geometry.html", f"{DOMAIN}math-conversions.html"),
)


MD_LINK_PATTERN = re.compile(
    r"\[(https://calcdomain\.com/[^\]]+)\]\(https://calcdomain\.com/[^\)]+\)"
)


ANCHOR_PATTERN = re.compile(
    r"<a\s+(?P<prefix>[^>]*?)href=\"(?P<href>[^\"]+)\"(?P<suffix>[^>]*)>(?P<body>.*?)</a>",
    re.IGNORECASE | re.DOTALL,
)


CANONICAL_PATTERN = re.compile(
    r"<link\s+[^>]*rel=\"canonical\"[^>]*>",
    re.IGNORECASE,
)

ASSET_SUFFIX_FIXES: Tuple[Tuple[str, str], ...] = (
    (".png.html", ".png"),
    (".svg.html", ".svg"),
    (".ico.html", ".ico"),
    (".webmanifest.html", ".webmanifest"),
)


def clean_markdown_links(html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        return match.group(1)

    return MD_LINK_PATTERN.sub(repl, html)


def map_relative_path(path: str) -> Optional[str]:
    if not path:
        return path

    path = path.replace("\\", "/")

    if path in DIRECT_PATH_MAP:
        direct = DIRECT_PATH_MAP[path]
        if direct is None:
            return None
        if direct:
            path = direct

    fallback = converter_category_fallback(path)
    if fallback:
        path = fallback

    # Ensure .html extension
    if not path.endswith(HTML_EXT):
        candidate = f"{path}{HTML_EXT}"
        if rel_exists(candidate):
            path = candidate

    # Try trimming legacy suffixes (-calculator, -calculators, -calc)
    if not rel_exists(path):
        dirname, filename = os.path.split(path)
        basename = filename[:-5] if filename.endswith(HTML_EXT) else filename
        for suffix in ("-calculator", "-calculators", "-calc"):
            if basename.endswith(suffix):
                trimmed = basename[: -len(suffix)]
                if trimmed:
                    candidate = "/".join(filter(None, [dirname, f"{trimmed}{HTML_EXT}"]))
                    if rel_exists(candidate):
                        path = candidate
                        break

    return path if rel_exists(path) else None


def normalize_internal_path(path: str) -> Optional[str]:
    mapped = map_relative_path(path)
    if mapped and rel_exists(mapped):
        return mapped
    if mapped:
        # Already mapped but still missing -> final attempt with .html appended
        if not mapped.endswith(HTML_EXT):
            candidate = f"{mapped}{HTML_EXT}"
            if rel_exists(candidate):
                return candidate
    return mapped if mapped and rel_exists(mapped) else None


def to_relative(from_file: Path, target: str) -> str:
    target_path = Path(target)
    start = from_file.parent
    rel = os.path.relpath(target_path, start).replace("\\", "/")
    return rel


@dataclass
class HrefResolution:
    href: Optional[str]
    drop: bool = False


def resolve_href(href: str, source_file: Path) -> HrefResolution:
    href = href.strip()
    if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
        return HrefResolution(href=href)

    if href.startswith("javascript:"):
        return HrefResolution(href=href)

    is_absolute = False
    scheme = "https"
    rel_path = ""

    if href.startswith("http://") or href.startswith("https://"):
        is_absolute = True
        if href.startswith(DOMAIN):
            rel_path = href[len(DOMAIN) :]
        elif href.startswith(DOMAIN.replace("https://", "http://")):
            rel_path = href[len(DOMAIN) :]
        else:
            # external domain
            return HrefResolution(href=href)
    else:
        rel_path = href

    rel_path = rel_path.lstrip("/")
    if rel_path.endswith("/") and rel_path != "":
        rel_path = f"{rel_path}index.html"

    if not rel_path.endswith(HTML_EXT):
        potential = f"{rel_path}{HTML_EXT}"
        if rel_exists(potential):
            rel_path = potential

    mapped = normalize_internal_path(rel_path)
    if not mapped:
        return HrefResolution(href=None, drop=True)

    if is_absolute:
        return HrefResolution(href=f"{DOMAIN}{mapped}")

    new_href = to_relative(source_file, mapped)
    return HrefResolution(href=new_href)


def replace_anchors(html: str, file_path: Path) -> str:
    def repl(match: re.Match[str]) -> str:
        href = match.group("href")
        resolution = resolve_href(href, file_path)
        if resolution.drop or not resolution.href:
            return match.group("body")
        if resolution.href == href:
            return match.group(0)
        return f"<a {match.group('prefix')}href=\"{resolution.href}\"{match.group('suffix')}>{match.group('body')}</a>"

    return ANCHOR_PATTERN.sub(repl, html)


def update_canonical(html: str, rel_path: str) -> str:
    expected = f'<link rel="canonical" href="{DOMAIN}{rel_path}">'
    html = CANONICAL_PATTERN.sub("", html)
    html = html.replace("<head>", f"<head>\n{expected}", 1)
    return html


def build_breadcrumb_items(raw_items, file_path: Path) -> list:
    items: list[dict] = []
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        position = item.get("position")
        name = item.get("name", "")
        url = item.get("item", "")

        if position == 1:
            items.append(
                {"@type": "ListItem", "position": len(items) + 1, "name": "Home", "item": DOMAIN}
            )
            continue

        if isinstance(name, str):
            name = name.strip()

        if isinstance(url, str):
            url = url.strip()

        if position == 2 and name in CATEGORY_MAP:
            mapped_name, mapped_path = CATEGORY_MAP[name]
            items.append(
                {
                    "@type": "ListItem",
                    "position": len(items) + 1,
                    "name": mapped_name,
                    "item": f"{DOMAIN}{mapped_path}",
                }
            )
            continue

        if position == 3 and name in SUBCATEGORY_MAP:
            mapped_path = SUBCATEGORY_MAP[name]
            if mapped_path:
                items.append(
                    {
                        "@type": "ListItem",
                        "position": len(items) + 1,
                        "name": name,
                        "item": f"{DOMAIN}{mapped_path}",
                    }
                )
            continue

        if url.startswith("[") and "](" in url:
            url = re.sub(r"^\[([^\]]+)\]\(([^\)]+)\)$", r"\2", url)

        if url.startswith(DOMAIN):
            rel_path = url[len(DOMAIN) :]
        else:
            rel_path = url.lstrip("/")

        mapped = normalize_internal_path(rel_path)
        if not mapped:
            continue

        items.append(
            {
                "@type": "ListItem",
                "position": len(items) + 1,
                "name": name,
                "item": f"{DOMAIN}{mapped}",
            }
        )

    if not items:
        items = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN},
            {
                "@type": "ListItem",
                "position": 2,
                "name": Path(file_path).stem.replace("-", " ").title(),
                "item": f"{DOMAIN}{file_path.relative_to(ROOT).as_posix()}",
            },
        ]

    for idx, entry in enumerate(items, start=1):
        entry["position"] = idx
    return items


def process_breadcrumb_container(container, file_path: Path) -> bool:
    changed = False
    if isinstance(container, dict) and container.get("@type") == "BreadcrumbList":
        new_items = build_breadcrumb_items(container.get("itemListElement", []), file_path)
        if new_items != container.get("itemListElement"):
            container["itemListElement"] = new_items
            changed = True
    elif isinstance(container, list):
        for entry in container:
            if isinstance(entry, dict) and entry.get("@type") == "BreadcrumbList":
                new_items = build_breadcrumb_items(entry.get("itemListElement", []), file_path)
                if new_items != entry.get("itemListElement"):
                    entry["itemListElement"] = new_items
                    changed = True
    return changed


def adjust_breadcrumbs(html: str, file_path: Path) -> str:
    pattern = re.compile(
        r"(<script type=\"application/ld\+json\">)(.*?)(</script>)",
        re.DOTALL,
    )

    def repl(match: re.Match[str]) -> str:
        prefix, json_body, suffix = match.groups()
        try:
            data = json.loads(json_body)
        except json.JSONDecodeError:
            return match.group(0)

        page_rel = file_path.relative_to(ROOT).as_posix()
        page_url = f"{DOMAIN}{page_rel}"

        def fix_url(value: object) -> Tuple[object, bool]:
            if not isinstance(value, str):
                return value, False
            if value.startswith(DOMAIN):
                base, frag = (value[len(DOMAIN) :].split("#", 1) + [""])[:2]
                mapped = normalize_internal_path(base) or page_rel
                new_url = f"{DOMAIN}{mapped}"
                if frag:
                    new_url = f"{new_url}#{frag}"
                if new_url != value:
                    return new_url, True
            return value, False

        def fix_url_fields(obj: dict) -> bool:
            changed = False
            if not isinstance(obj, dict):
                return False
            for key in ("url", "@id"):
                if key in obj:
                    new_val, updated_val = fix_url(obj[key])
                    if updated_val:
                        obj[key] = new_val
                        changed = True
            return changed

        updated = False
        if isinstance(data, dict):
            if fix_url_fields(data):
                updated = True
            if fix_url_fields(data.get("mainEntityOfPage", {})):
                updated = True
            if data.get("@type") == "BreadcrumbList":
                new_items = build_breadcrumb_items(data.get("itemListElement", []), file_path)
                if new_items != data.get("itemListElement"):
                    data["itemListElement"] = new_items
                    updated = True
            else:
                if "breadcrumb" in data:
                    if process_breadcrumb_container(data["breadcrumb"], file_path):
                        updated = True
            if "@graph" in data and isinstance(data["@graph"], list):
                for node in data["@graph"]:
                    if not isinstance(node, dict):
                        continue
                    if fix_url_fields(node):
                        updated = True
                    if fix_url_fields(node.get("mainEntityOfPage", {})):
                        updated = True
                    if "breadcrumb" in node:
                        if process_breadcrumb_container(node["breadcrumb"], file_path):
                            updated = True
                    if node.get("@type") == "BreadcrumbList":
                        new_items = build_breadcrumb_items(node.get("itemListElement", []), file_path)
                        if new_items != node.get("itemListElement"):
                            node["itemListElement"] = new_items
                            updated = True
        if not updated:
            return match.group(0)

        new_body = json.dumps(data, indent=2)
        return f"{prefix}{new_body}{suffix}"

    return pattern.sub(repl, html)


def process_html_file(file_path: Path) -> None:
    rel_path = file_path.relative_to(ROOT).as_posix()
    html = file_path.read_text(encoding="utf-8")

    original_html = html

    for old, new in TEXT_REPLACEMENTS:
        html = html.replace(old, new)

    html = clean_markdown_links(html)
    html = update_canonical(html, rel_path)
    html = adjust_breadcrumbs(html, file_path)
    html = replace_anchors(html, file_path)

    for bad, good in ASSET_SUFFIX_FIXES:
        html = html.replace(bad, good)

    if html != original_html:
        file_path.write_text(html, encoding="utf-8")


def main() -> None:
    for file_path in ROOT.rglob(f"*{HTML_EXT}"):
        process_html_file(file_path)


if __name__ == "__main__":
    main()
