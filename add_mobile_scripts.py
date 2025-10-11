#!/usr/bin/env python3
"""
Add mobile menu scripts to pages that have the button but missing script
"""

import re
from pathlib import Path

def needs_script(content):
    """Check if page has mobile toggle but missing script"""
    has_toggle = 'id="mobile-menu-toggle"' in content
    has_script = 'mobileToggle' in content and 'addEventListener' in content
    return has_toggle and not has_script

def add_mobile_script(file_path):
    """Add mobile menu script if needed"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not needs_script(content):
        return False

    script = '''
    <script>
        // Mobile menu toggle
        (function() {
            const mobileToggle = document.getElementById('mobile-menu-toggle');
            const mobileMenu = document.getElementById('mobile-menu');
            if (mobileToggle && mobileMenu) {
                mobileToggle.addEventListener('click', () => {
                    mobileMenu.classList.toggle('hidden');
                });
            }
        })();
    </script>'''

    # Add before </body>
    if '</body>' in content:
        content = content.replace('</body>', script + '\n</body>')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def main():
    base_path = Path("/home/uc/Projects/calcdomain2")
    files = sorted(base_path.glob('*.html'))

    fixed = 0

    for file_path in files:
        if file_path.name.startswith('template-'):
            continue

        try:
            if add_mobile_script(file_path):
                print(f"✅ {file_path.name}")
                fixed += 1
        except Exception as e:
            print(f"❌ {file_path.name}: {str(e)}")

    print(f"\n✅ Added mobile script to {fixed} files")

if __name__ == "__main__":
    main()
