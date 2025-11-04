#!/usr/bin/env python3
"""
Fix calculator HTML pages - applies consistent MathJax configuration fixes.

This script:
1. Fixes MathJax configuration (properly escapes backslashes)
2. Preserves all existing structure and styling
3. Only modifies the MathJax configuration block
"""

import re
import sys
from pathlib import Path


def fix_mathjax_config(content):
    """Fix MathJax configuration by properly escaping backslashes."""

    # Pattern to match the MathJax configuration block with improperly escaped backslashes
    pattern = r"(window\.MathJax\s*=\s*\{[\s\S]*?tex:\s*\{[\s\S]*?inlineMath:\s*\[\[)'\\?\(',\s*'\\?\)'\]\s*,\s*\['?\$'?\s*,\s*'?\$'?\]"

    # Check if we need to fix it
    if re.search(pattern, content):
        # Replace single backslashes with double backslashes for proper escaping
        content = re.sub(
            r"inlineMath:\s*\[\['\\?\(',\s*'\\?\)'\]\s*,\s*\['?\$'?\s*,\s*'?\$'?\]\]",
            "inlineMath: [['\\\\(','\\\\)'], ['$', '$']]",
            content
        )

        # Fix displayMath if it exists and needs fixing
        content = re.sub(
            r"displayMath:\s*\[\['\\?\[',\s*'\\?\]'\]\]",
            "displayMath: [['$','$'], ['\\\\[','\\\\]']]",
            content
        )

    return content


def process_file(filepath):
    """Process a single HTML file."""
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if file has MathJax configuration
        if 'window.MathJax' not in content:
            return False, "No MathJax config found"

        # Check if already fixed (has properly escaped backslashes)
        if re.search(r"inlineMath:\s*\[\['\\\\?\(',\s*'\\\\?\)'\]", content):
            # Check if it's the correct format
            if re.search(r"inlineMath:\s*\[\['\\\\\\(',\s*'\\\\\\)'\]", content):
                return False, "Already fixed"

        # Apply fixes
        fixed_content = fix_mathjax_config(content)

        # Check if anything changed
        if content == fixed_content:
            return False, "No changes needed"

        # Write the fixed content back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

        return True, "Fixed"

    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    # Get the project root (parent of tools directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Find all HTML files (excluding specific files)
    exclude_files = {
        'index.html', 'finance.html', 'math.html', 'science.html',
        'engineering.html', 'construction.html', 'conversions.html',
        'lifestyle-everyday.html', 'about.html', 'contact.html',
        'privacy.html', 'terms.html'
    }

    exclude_patterns = {'template-', 'search.html'}

    html_files = []
    for html_file in project_root.glob('*.html'):
        # Skip if in exclude list
        if html_file.name in exclude_files:
            continue

        # Skip if matches exclude pattern
        if any(pattern in html_file.name for pattern in exclude_patterns):
            continue

        html_files.append(html_file)

    print(f"Found {len(html_files)} calculator HTML files to process")

    # Process files
    fixed_count = 0
    skipped_count = 0
    error_count = 0

    for i, filepath in enumerate(html_files, 1):
        success, message = process_file(filepath)

        if success:
            fixed_count += 1
            print(f"[{i}/{len(html_files)}] ✓ {filepath.name}: {message}")
        else:
            if "Error" in message:
                error_count += 1
                print(f"[{i}/{len(html_files)}] ✗ {filepath.name}: {message}")
            else:
                skipped_count += 1
                if i % 100 == 0:  # Only print every 100th skip to reduce noise
                    print(f"[{i}/{len(html_files)}] - {filepath.name}: {message}")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total files processed: {len(html_files)}")
    print(f"Fixed: {fixed_count}")
    print(f"Skipped (no changes): {skipped_count}")
    print(f"Errors: {error_count}")
    print("="*60)


if __name__ == '__main__':
    main()
