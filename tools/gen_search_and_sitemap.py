#!/usr/bin/env python3
# tools/gen_search_and_sitemap.py
import sys, json, re, html
from pathlib import Path
from datetime import datetime, timezone
from html import unescape

try:
    from bs4 import BeautifulSoup  # type: ignore
except ImportError:  # fallback when bs4 isn't available
    BeautifulSoup = None

ROOT = Path(__file__).resolve().parents[1] if (Path(__file__).name == "gen_search_and_sitemap.py") else Path.cwd()
# If you move this file, set ROOT = Path("https://calcdomain.com/home/yeahupsrl/calcdomain2")

OUT_SEARCH = ROOT / "search.json"
OUT_CALCS  = ROOT / "calculators-data.json"
OUT_SITEMAP = ROOT / "sitemap.xml"

def is_html_candidate(p: Path) -> bool:
    # include only top-level content pages in the repo tree
    if not p.name.endswith(".html"):
        return False
    # ignore obvious non-pages
    if any(seg in {"out", ".git", "tools", "tools_bundle_v4", "tools_bundle_v5", "tmp_src"} for seg in p.parts):
        return False
    return True

def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def strip_tags(raw: str) -> str:
    text = re.sub(r"(?is)<(script|style).*?</\\1>", " ", raw)
    text = re.sub(r"(?is)<!--.*?-->", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    return collapse_ws(unescape(text))

def text_or_none(x):
    if BeautifulSoup:
        return (x.get_text(" ", strip=True) if x else "").strip() or None
    return collapse_ws(x) if x else None

def get_title(doc):
    if BeautifulSoup:
        t = text_or_none(doc.title)
        if t:
            return collapse_ws(t)
        h1 = doc.find("h1")
        if h1:
            return collapse_ws(h1.get_text(" ", strip=True))
        return None
    match = re.search(r"(?is)<title[^>]*>(.*?)</title>", doc)
    if match:
        return strip_tags(match.group(1))
    h1 = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", doc)
    if h1:
        return strip_tags(h1.group(1))
    return None

def get_meta_description(doc):
    if BeautifulSoup:
        m = doc.find("meta", attrs={"name":"description"})
        if m and m.get("content"):
            return m["content"].strip()
        p = doc.find("p")
        if p:
            txt = collapse_ws(p.get_text(" ", strip=True))
            return txt[:300]
        return None
    match = re.search(r'(?is)<meta[^>]+name=["\']description["\'][^>]*>', doc)
    if match:
        tag = match.group(0)
        content = re.search(r'content=["\'](.*?)["\']', tag, re.I | re.S)
        if content:
            return collapse_ws(unescape(content.group(1)))
    p = re.search(r"(?is)<p[^>]*>(.*?)</p>", doc)
    if p:
        return strip_tags(p.group(1))[:300]
    return None

def infer_category_subcategory(doc):
    cat = sub = None
    if BeautifulSoup:
        bc = doc.find(lambda tag: tag.name in ("nav","ol","ul","div") and ("breadcrumb" in " ".join(tag.get("class", [])) or "breadcrumbs" in " ".join(tag.get("class", []))))
        if not bc:
            bc = doc.find(lambda tag: tag.name == "nav" and (tag.get("aria-label", "") or "").lower().startswith("breadcrumb"))
        if bc:
            links = [a.get_text(" ", strip=True) for a in bc.find_all("a")]
            items = [x for x in links if x]
            if len(items) >= 1:
                cat = items[0]
            if len(items) >= 2:
                sub = items[1]
        if not cat:
            tag = doc.find(lambda t: t.name in ("a","span","div") and re.search(r"(Finance|Health|Math|Lifestyle|Construction)", t.get_text(" ", strip=True), re.I))
            if tag:
                cat = tag.get_text(" ", strip=True)
        return (cat or ""), (sub or "")

    breadcrumb_match = re.search(r'(?is)<nav[^>]*(?:breadcrumb|aria-label=["\']breadcrumb["\'])[^>]*>.*?</nav>', doc)
    if not breadcrumb_match:
        breadcrumb_match = re.search(r'(?is)<div[^>]*class=["\'][^"\']*(?:breadcrumb|breadcrumbs)[^"\']*["\'][^>]*>.*?</div>', doc)
    if breadcrumb_match:
        snip = breadcrumb_match.group(0)
        anchors = re.findall(r'(?is)<a[^>]*>(.*?)</a>', snip)
        texts = [strip_tags(a) for a in anchors if strip_tags(a)]
        if len(texts) >= 1:
            cat = texts[0]
        if len(texts) >= 2:
            sub = texts[1]
    if not cat:
        match = re.search(r'(?is)>(Finance|Health|Math|Lifestyle|Construction)[^<]*<', doc)
        if match:
            cat = strip_tags(match.group(0))
    return (cat or ""), (sub or "")

def slug_from_path(p: Path):
    return p.stem

def collect_pages(root: Path):
    pages = []
    for p in root.rglob("*.html"):
        if not is_html_candidate(p):
            continue
        try:
            html_text = p.read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(html_text, "lxml") if BeautifulSoup else html_text
            title = get_title(soup) or slug_from_path(p).replace("-", " ").title()
            desc = get_meta_description(soup) or ""
            cat, sub = infer_category_subcategory(soup)
            slug = slug_from_path(p)
            url  = f"https://calcdomain.com/{p.relative_to(root).as_posix()}"
            pages.append({
                "slug": slug,
                "url": url,
                "title": title,
                "category": cat,
                "subcategory": sub,
                "description": desc,
            })
        except Exception as e:
            # non-fatal: skip broken file
            # print(f"[WARN] {p}: {e}", file=sys.stderr)
            pass
    return pages

def write_json_files(records):
    # search.json — same array structure, pretty-printed
    OUT_SEARCH.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    # calculators-data.json — same content so your search.js loads it seamlessly
    OUT_CALCS.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

def write_sitemap(root: Path, pages):
    # Build a minimal sitemap.xml
    # Host isn’t strictly required in local generation; search engines accept relative, but we’ll allow DOMAIN env in hook.
    domain = (root / ".sitemap_domain").read_text(encoding="utf-8").strip() if (root / ".sitemap_domain").exists() else ""
    def full(u):
        if domain and u.startswith("https://calcdomain.com/"):
            return f"{domain.rstrip('/')}{u}"
        return u

    now = datetime.now(timezone.utc)
    def iso(mtime):
        return datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    urls = []
    # include index.html at root if exists
    idx = root / "index.html"
    if idx.exists():
        urls.append({
            "loc": full("https://calcdomain.com/index.html"),
            "lastmod": iso(idx.stat().st_mtime),
            "changefreq": "weekly",
            "priority": "1.0"
        })
    # include all pages
    for r in pages:
        rel = r["url"]
        fp = root / rel.lstrip("https://calcdomain.com/")
        if not fp.exists():
            continue
        urls.append({
            "loc": full(rel),
            "lastmod": iso(fp.stat().st_mtime),
            "changefreq": "weekly",
            "priority": "0.8" if "category" in rel or "subcategories" in rel else "0.5"
        })

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    for u in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{html.escape(u['loc'])}</loc>")
        xml.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        xml.append(f"    <changefreq>{u['changefreq']}</changefreq>")
        xml.append(f"    <priority>{u['priority']}</priority>")
        xml.append("  </url>")
    xml.append("</urlset>\n")
    OUT_SITEMAP.write_text("\n".join(xml), encoding="utf-8")

def main():
    root = ROOT
    pages = collect_pages(root)
    write_json_files(pages)
    write_sitemap(root, pages)
    print(f"Generated {OUT_SEARCH.name}, {OUT_CALCS.name}, and {OUT_SITEMAP.name}.")

if __name__ == "__main__":
    main()
