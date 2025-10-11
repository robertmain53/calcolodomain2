#!/usr/bin/env python3
"""
Page Fix Script - Human-like systematic repairs
Applies fixes to HTML calculator pages with quality checks
"""

import os
import re
from pathlib import Path
import json

class PageFixer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.reference_file = self.base_path / "mortgage-payment.html"
        self.fixes_applied = []

        # Load reference components
        self.load_reference_components()

    def load_reference_components(self):
        """Extract reusable components from reference page"""
        with open(self.reference_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract mobile menu button
        mobile_button_match = re.search(
            r'<button id="mobile-menu-toggle"[^>]*>.*?</button>',
            content, re.DOTALL
        )
        self.mobile_menu_button = mobile_button_match.group(0) if mobile_button_match else None

        # Extract mobile menu div
        mobile_menu_match = re.search(
            r'<div id="mobile-menu"[^>]*>.*?</div>\s*</nav>',
            content, re.DOTALL
        )
        self.mobile_menu_div = mobile_menu_match.group(0).replace('</nav>', '').strip() if mobile_menu_match else None

        # Extract mobile menu script
        mobile_script_match = re.search(
            r'// Mobile menu toggle.*?}\s*}\s*\)\(\);',
            content, re.DOTALL
        )
        if not mobile_script_match:
            # Alternative pattern
            mobile_script_match = re.search(
                r'const mobileToggle = document\.getElementById.*?\}\s*\}',
                content, re.DOTALL
            )
        self.mobile_menu_script = mobile_script_match.group(0) if mobile_script_match else None

        # Extract footer
        footer_match = re.search(
            r'<!-- Footer -->.*?</footer>',
            content, re.DOTALL
        )
        self.footer = footer_match.group(0) if footer_match else None

        # Extract search input pattern
        self.search_input_pattern = r'<input[^>]*type="search"[^>]*>'

        print("✓ Loaded reference components from mortgage-payment.html")

    def analyze_page(self, file_path):
        """Analyze what fixes a page needs"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        needs_fixes = []

        # Check mobile menu
        if not re.search(r'id="mobile-menu-toggle"', content):
            needs_fixes.append('mobile_menu_button')
        if not re.search(r'id="mobile-menu"', content):
            needs_fixes.append('mobile_menu_div')
        if not re.search(r'mobile-menu-toggle.*addEventListener|mobileToggle.*addEventListener', content, re.DOTALL):
            needs_fixes.append('mobile_menu_script')

        # Check search input
        if not re.search(r'id="search-input"', content):
            needs_fixes.append('search_input_id')

        # Check footer
        if not re.search(r'<footer.*?bg-white.*?border-t', content, re.DOTALL):
            needs_fixes.append('footer')
        elif not re.search(r'href="about\.html"', content):
            needs_fixes.append('footer_links')

        # Check layout
        if not re.search(r'class="flex flex-col lg:flex-row gap-8"', content):
            needs_fixes.append('layout')

        # Check sidebar
        if not re.search(r'<aside.*?class="w-full lg:w-1/3"', content):
            needs_fixes.append('sidebar')

        # Check breadcrumbs
        if not re.search(r'<nav class="text-sm mb-4 text-gray-600">', content):
            needs_fixes.append('breadcrumbs')

        return needs_fixes

    def fix_mobile_menu_button(self, content):
        """Add mobile menu toggle button"""
        # Find the header navigation section where desktop links are
        pattern = r'(<div class="hidden md:flex items-center[^>]*>.*?</div>)\s*\n\s*(</div>)'

        if re.search(pattern, content, re.DOTALL):
            # Insert mobile menu button after desktop nav
            replacement = r'\1\n                \n                ' + self.mobile_menu_button + r'\n            \2'
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            print("  ✓ Added mobile menu toggle button")
        else:
            # Try alternative insertion point - before closing nav div
            pattern2 = r'(</div>\s*</nav>)'
            if '</nav>' in content:
                # Insert before first </nav>
                nav_pos = content.find('</nav>')
                if nav_pos > 0:
                    # Find the div before nav close
                    insert_pos = content.rfind('</div>', 0, nav_pos)
                    if insert_pos > 0:
                        content = content[:insert_pos] + '\n                \n                ' + self.mobile_menu_button + content[insert_pos:]
                        print("  ✓ Added mobile menu toggle button (alternative position)")

        return content

    def fix_mobile_menu_div(self, content):
        """Add mobile menu dropdown"""
        # Find where to insert - after the main header div, before closing nav
        pattern = r'(</div>\s*\n\s*)(</nav>)'

        if re.search(pattern, content):
            replacement = r'\1            \n            ' + self.mobile_menu_div + r'\n        \2'
            content = re.sub(pattern, replacement, content, count=1)
            print("  ✓ Added mobile menu dropdown div")

        return content

    def fix_mobile_menu_script(self, content):
        """Add mobile menu JavaScript"""
        # Check if there's already a script tag before </body>
        if not re.search(r'mobile.*menu.*toggle', content, re.IGNORECASE):
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

            # Insert before </body>
            content = content.replace('</body>', script + '\n</body>')
            print("  ✓ Added mobile menu JavaScript")

        return content

    def fix_search_input_id(self, content):
        """Add id="search-input" to search field"""
        # Find search input without id
        pattern = r'<input\s+type="search"(?![^>]*id=)[^>]*>'

        def add_id(match):
            input_tag = match.group(0)
            # Insert id after type="search"
            return input_tag.replace('type="search"', 'type="search" id="search-input"')

        if re.search(pattern, content):
            content = re.sub(pattern, add_id, content)
            print("  ✓ Added id='search-input' to search field")

        return content

    def fix_footer(self, content):
        """Replace or add proper footer"""
        # Try to find existing footer
        footer_pattern = r'<footer.*?</footer>'

        if re.search(footer_pattern, content, re.DOTALL):
            # Replace existing footer
            content = re.sub(footer_pattern, self.footer, content, flags=re.DOTALL)
            print("  ✓ Replaced footer with standard version")
        else:
            # Add footer before </body>
            content = content.replace('</body>', '\n    ' + self.footer + '\n\n</body>')
            print("  ✓ Added standard footer")

        return content

    def fix_page(self, file_path, dry_run=False):
        """Fix a single page"""
        rel_path = file_path.relative_to(self.base_path)
        print(f"\n📄 Processing: {rel_path}")

        # Analyze what needs fixing
        needs_fixes = self.analyze_page(file_path)

        if not needs_fixes:
            print("  ✓ Page is already compliant!")
            return {'file': str(rel_path), 'status': 'already_compliant', 'fixes': []}

        print(f"  Found {len(needs_fixes)} issues: {', '.join(needs_fixes)}")

        # Load content
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        content = original_content
        fixes_applied = []

        # Apply fixes in order
        if 'mobile_menu_button' in needs_fixes and self.mobile_menu_button:
            content = self.fix_mobile_menu_button(content)
            fixes_applied.append('mobile_menu_button')

        if 'mobile_menu_div' in needs_fixes and self.mobile_menu_div:
            content = self.fix_mobile_menu_div(content)
            fixes_applied.append('mobile_menu_div')

        if 'search_input_id' in needs_fixes:
            content = self.fix_search_input_id(content)
            fixes_applied.append('search_input_id')

        if 'footer' in needs_fixes or 'footer_links' in needs_fixes:
            if self.footer:
                content = self.fix_footer(content)
                fixes_applied.append('footer')

        if 'mobile_menu_script' in needs_fixes and self.mobile_menu_script:
            content = self.fix_mobile_menu_script(content)
            fixes_applied.append('mobile_menu_script')

        # Save if not dry run
        if not dry_run and content != original_content:
            # Create backup
            backup_path = file_path.with_suffix('.html.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)

            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  💾 Saved changes (backup: {backup_path.name})")
        elif dry_run:
            print("  🔍 DRY RUN - No changes written")

        return {
            'file': str(rel_path),
            'status': 'fixed',
            'fixes': fixes_applied,
            'issues_remaining': [f for f in needs_fixes if f not in fixes_applied]
        }

    def fix_batch(self, file_list, dry_run=False):
        """Fix a batch of files"""
        results = []

        for file_path in file_list:
            try:
                result = self.fix_page(file_path, dry_run=dry_run)
                results.append(result)
            except Exception as e:
                print(f"  ❌ Error fixing {file_path.name}: {str(e)}")
                results.append({
                    'file': str(file_path.relative_to(self.base_path)),
                    'status': 'error',
                    'error': str(e)
                })

        return results


def main():
    base_path = "/home/uc/Projects/calcdomain2"
    fixer = PageFixer(base_path)

    print("=" * 80)
    print("CALCDOMAIN PAGE FIXER - PHASE 1")
    print("Systematic fixes with quality assurance")
    print("=" * 80)
    print()

    # Start with high-priority mortgage/loan calculators that need fixes
    priority_files = [
        'loan-amortization.html',
        'mortgage-refinance.html',
        'heloc.html',
        'auto-loan-calculator.html',
        'student-loan-calculator.html',
        'personal-loan-calculator.html',
        'simple-loan-calculator.html',
    ]

    print("Phase 1: High-Priority Mortgage/Loan Calculators")
    print("-" * 80)

    files_to_fix = []
    for filename in priority_files:
        file_path = Path(base_path) / filename
        if file_path.exists():
            files_to_fix.append(file_path)
        else:
            print(f"⚠️  File not found: {filename}")

    print(f"\nProcessing {len(files_to_fix)} files...")
    print()

    # Fix files
    results = fixer.fix_batch(files_to_fix, dry_run=False)

    # Summary
    print()
    print("=" * 80)
    print("PHASE 1 SUMMARY")
    print("=" * 80)

    fixed_count = sum(1 for r in results if r['status'] == 'fixed')
    already_compliant = sum(1 for r in results if r['status'] == 'already_compliant')
    errors = sum(1 for r in results if r['status'] == 'error')

    print(f"✅ Fixed: {fixed_count}")
    print(f"✓  Already compliant: {already_compliant}")
    print(f"❌ Errors: {errors}")
    print()

    # Save results
    with open(Path(base_path) / 'fix_results_phase1.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Results saved to: fix_results_phase1.json")


if __name__ == "__main__":
    main()
