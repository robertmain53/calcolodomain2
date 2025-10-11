#!/usr/bin/env python3
"""
Clean up duplicate footer comments
"""

import re
from pathlib import Path

def clean_duplicate_footer_comments(file_path):
    """Remove duplicate <!-- Footer --> comments"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find multiple consecutive <!-- Footer --> comments
    pattern = r'(<!-- Footer -->\s*){2,}'

    if re.search(pattern, content):
        # Replace with single comment
        content = re.sub(pattern, '<!-- Footer -->\n    ', content)

        # Save
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_path = Path("/home/uc/Projects/calcdomain2")
    files = sorted(base_path.glob('*.html'))

    cleaned = 0
    for file_path in files:
        if file_path.name.startswith('template-'):
            continue

        try:
            if clean_duplicate_footer_comments(file_path):
                print(f"✅ {file_path.name}")
                cleaned += 1
        except Exception as e:
            print(f"❌ {file_path.name}: {str(e)}")

    print(f"\n✓ Cleaned {cleaned} files")

if __name__ == "__main__":
    main()
