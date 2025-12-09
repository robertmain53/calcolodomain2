#!/usr/bin/env python3
"""
Find all 404 errors (broken internal links) in HTML files.

This script:
1. Scans all HTML files for internal links
2. Checks if linked files exist
3. Reports all broken links by category
"""

import re
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse, unquote


def extract_links(content, filepath):
    """Extract all internal links from HTML content."""
    links = set()

    # Find href links
    href_pattern = r'href=["\']([^"\']+)["\']'
    for match in re.finditer(href_pattern, content):
        link = match.group(1)
        # Skip external links, anchors, javascript, mailto, etc.
        if link.startswith(('#', 'javascript:', 'mailto:', 'tel:', 'http://', 'https://')):
            continue
        links.add(link)

    # Find src links (images, scripts)
    src_pattern = r'src=["\']([^"\']+)["\']'
    for match in re.finditer(src_pattern, content):
        link = match.group(1)
        if link.startswith(('http://', 'https://', 'data:', '//')):
            continue
        links.add(link)

    return links


def resolve_link(source_file, link):
    """Resolve a link relative to the source file."""
    source_dir = source_file.parent

    # Remove query strings and anchors
    link = link.split('?')[0].split('#')[0]

    if not link:
        return None

    # Handle absolute paths (starting with /)
    if link.startswith('/'):
        # Relative to project root
        target = source_file.parents[0] / link.lstrip('/')
    else:
        # Relative to source file directory
        target = source_dir / link

    # Resolve to absolute path
    try:
        target = target.resolve()
    except:
        return None

    return target


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    print("Scanning for 404 errors...")
    print("="*60)

    # Find all HTML files
    html_files = list(project_root.glob('*.html'))
    html_files.extend(project_root.glob('subcategories/*.html'))

    # Track broken links
    broken_links = defaultdict(list)  # {source_file: [(link, reason)]}
    missing_files = set()
    total_links_checked = 0

    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            links = extract_links(content, html_file)

            for link in links:
                total_links_checked += 1
                target = resolve_link(html_file, link)

                if target is None:
                    broken_links[html_file].append((link, "Invalid path"))
                    continue

                if not target.exists():
                    broken_links[html_file].append((link, "File not found"))
                    missing_files.add(link)

        except Exception as e:
            print(f"Error processing {html_file.name}: {e}")

    # Report results
    print(f"\nTotal HTML files scanned: {len(html_files)}")
    print(f"Total links checked: {total_links_checked}")
    print(f"Files with broken links: {len(broken_links)}")
    print(f"Unique missing files: {len(missing_files)}")
    print("="*60)

    if broken_links:
        print("\n404 ERRORS BY FILE:")
        print("="*60)

        # Sort by number of broken links
        sorted_files = sorted(broken_links.items(), key=lambda x: len(x[1]), reverse=True)

        for source_file, links in sorted_files[:20]:  # Show top 20
            print(f"\n{source_file.name} ({len(links)} broken links):")
            for link, reason in links[:10]:  # Show first 10 per file
                print(f"  ✗ {link} - {reason}")
            if len(links) > 10:
                print(f"  ... and {len(links) - 10} more")

    # Most common missing files
    if missing_files:
        print("\n\nMOST COMMON MISSING FILES:")
        print("="*60)

        # Count occurrences
        missing_count = defaultdict(int)
        for source_file, links in broken_links.items():
            for link, reason in links:
                if reason == "File not found":
                    missing_count[link] += 1

        # Sort by frequency
        sorted_missing = sorted(missing_count.items(), key=lambda x: x[1], reverse=True)

        for link, count in sorted_missing[:30]:  # Top 30
            print(f"  {count:3d}x  {link}")

    # Save full report
    report_file = project_root / "tools" / "404_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("404 ERRORS REPORT\n")
        f.write("="*60 + "\n\n")
        f.write(f"Total HTML files scanned: {len(html_files)}\n")
        f.write(f"Total links checked: {total_links_checked}\n")
        f.write(f"Files with broken links: {len(broken_links)}\n")
        f.write(f"Unique missing files: {len(missing_files)}\n")
        f.write("="*60 + "\n\n")

        for source_file, links in sorted(broken_links.items()):
            f.write(f"\n{source_file.name} ({len(links)} broken links):\n")
            for link, reason in links:
                f.write(f"  ✗ {link} - {reason}\n")

    print(f"\n\nFull report saved to: {report_file}")


if __name__ == '__main__':
    main()
