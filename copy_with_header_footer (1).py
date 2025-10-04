#!/usr/bin/env python3
import argparse, re, sys
from pathlib import Path
from bs4 import BeautifulSoup

def read_html(path: Path):
    return path.read_text(encoding="utf-8", errors="ignore")

def write_html(path: Path, html: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")

def extract_from_reference(ref_path: Path, nav_regex: str):
    soup = BeautifulSoup(read_html(ref_path), "lxml")
    header = soup.find("header")
    footer = soup.find("footer")
    header_html = str(header) if header else ""
    footer_html = str(footer) if footer else ""
    rx = re.compile(nav_regex, re.I)
    nav_scripts = []
    if soup.body:
        for s in soup.body.find_all("script"):
            src = s.get("src", "") or ""
            text = s.get_text() or ""
            if rx.search(src) or rx.search(text):
                nav_scripts.append(str(s))
    nav_scripts_html = "\n".join(nav_scripts)
    return header_html, footer_html, nav_scripts_html

def replace_blocks(html: str, header_html: str, footer_html: str, nav_scripts_html: str, nav_regex: str):
    soup = BeautifulSoup(html, "lxml")
    existing_header = soup.find("header")
    if header_html:
        if existing_header:
            existing_header.replace_with(BeautifulSoup(header_html, "lxml"))
        elif soup.body:
            soup.body.insert(0, BeautifulSoup(header_html, "lxml"))
    existing_footer = soup.find("footer")
    if footer_html:
        if existing_footer:
            existing_footer.replace_with(BeautifulSoup(footer_html, "lxml"))
        elif soup.body:
            soup.body.append(BeautifulSoup(footer_html, "lxml"))
    rx = re.compile(nav_regex, re.I)
    if soup.body and nav_scripts_html:
        for s in list(soup.body.find_all("script")):
            src = s.get("src", "") or ""
            text = s.get_text() or ""
            if rx.search(src) or rx.search(text):
                s.decompose()
        body_html = str(soup.body)
        if nav_scripts_html not in body_html:
            soup.body.append(BeautifulSoup(nav_scripts_html, "lxml"))
    return str(soup)

def main():
    ap = argparse.ArgumentParser(description="Copy *.html replacing header/footer/nav-scripts based on a reference HTML.")
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--skip-existing", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--nav-pattern", default=r"(nav|menu)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src_root = Path(args.src).resolve()
    dst_root = Path(args.dst).resolve()
    ref_path = Path(args.ref).resolve()

    if not src_root.exists():
        print(f"ERROR: src not found: {src_root}", file=sys.stderr); sys.exit(1)
    if not dst_root.exists():
        print(f"ERROR: dst not found: {dst_root}", file=sys.stderr); sys.exit(1)
    if not ref_path.exists():
        print(f"ERROR: ref not found: {ref_path}", file=sys.stderr); sys.exit(1)

    header_html, footer_html, nav_scripts_html = extract_from_reference(ref_path, args.nav_pattern)

    log_lines = []
    html_files = [p for p in src_root.rglob("*.html")]
    copied = 0; skipped = 0

    for src_file in html_files:
        rel = src_file.relative_to(src_root)
        dst_file = dst_root / rel
        if dst_file.exists() and not args.force:
            if args.skip_existing or not args.force:
                skipped += 1
                log_lines.append(f"SKIP (exists): {rel}")
                continue

        src_html = read_html(src_file)
        merged_html = replace_blocks(src_html, header_html, footer_html, nav_scripts_html, args.nav_pattern)

        if args.dry_run:
            log_lines.append(f"DRYRUN COPY: {rel}")
        else:
            write_html(dst_file, merged_html)
            copied += 1
            log_lines.append(f"COPIED: {rel}")

    out_dir = dst_root / "out"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "merge_log.txt").write_text("\n".join(log_lines) + f"\n\nSummary: copied={copied} skipped={skipped}\n", encoding="utf-8")
    print(f"Done. Copied={copied}, Skipped={skipped}. See {out_dir/'merge_log.txt'}")

if __name__ == "__main__":
    main()
