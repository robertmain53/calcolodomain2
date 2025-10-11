#!/usr/bin/env python3
"""
Add mobile menu toggle buttons to pages that are missing them
"""

import re
from pathlib import Path

def fix_mobile_button(file_path):
    """Add mobile menu toggle button if missing"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if button already exists
    if 'id="mobile-menu-toggle"' in content:
        return False

    mobile_button = '''<button id="mobile-menu-toggle" class="md:hidden p-2">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>'''

    # Pattern 1: After closing </div> before mobile menu div
    pattern1 = r'(<div class="hidden md:block"></div>)\s*\n\s*(<div id="mobile-menu")'
    if re.search(pattern1, content):
        replacement = r'\1\n                \n                ' + mobile_button + r'\n            \2'
        content = re.sub(pattern1, replacement, content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    # Pattern 2: After hidden md:flex div (for pages with desktop nav)
    pattern2 = r'(<div class="hidden md:flex[^>]*>.*?</div>)\s*\n\s*(</div>\s*\n\s*<div id="mobile-menu")'
    if re.search(pattern2, content, re.DOTALL):
        replacement = r'\1\n                \n                ' + mobile_button + r'\n            \2'
        content = re.sub(pattern2, replacement, content, flags=re.DOTALL)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    # Pattern 3: Before mobile menu div with simpler structure
    pattern3 = r'(</div>)\s*\n\s*(<div id="mobile-menu")'
    if re.search(pattern3, content):
        # Make sure we're in header/nav section
        if '<div id="mobile-menu"' in content:
            replacement = r'\1\n                \n                ' + mobile_button + r'\n            \2'
            content = re.sub(pattern3, replacement, content, count=1)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

    return False

def main():
    base_path = Path("/home/uc/Projects/calcdomain2")
    files = sorted(base_path.glob('*.html'))

    fixed = 0
    skipped = 0

    for file_path in files:
        if file_path.name.startswith('template-'):
            continue

        try:
            if fix_mobile_button(file_path):
                print(f"✅ {file_path.name}")
                fixed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"❌ {file_path.name}: {str(e)}")

    print(f"\n✅ Fixed: {fixed}")
    print(f"✓  Skipped (already had button): {skipped}")

if __name__ == "__main__":
    main()
