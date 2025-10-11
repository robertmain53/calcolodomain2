#!/usr/bin/env python3
"""
Batch Page Fixer - Process multiple pages with quality checks
"""

import re
from pathlib import Path
import json

class BatchPageFixer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.reference_file = self.base_path / "mortgage-payment.html"
        self.load_components()

    def load_components(self):
        """Load standard components from reference"""
        with open(self.reference_file, 'r', encoding='utf-8') as f:
            ref_content = f.read()

        # Mobile menu button
        self.mobile_button = '''<button id="mobile-menu-toggle" class="md:hidden p-2">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                </button>'''

        # Mobile menu div
        self.mobile_menu = '''
            <div id="mobile-menu" class="md:hidden mt-4 hidden">
                <div class="space-y-2">
                    <a href="search.html" class="block py-2 text-gray-700 hover:text-blue-600">Advanced Search</a>
                    <a href="index.html#categories" class="block py-2 text-gray-700 hover:text-blue-600">Categories</a>
                </div>
            </div>'''

        # Mobile menu script
        self.mobile_script = '''
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

        # Footer
        footer_match = re.search(r'<!-- Footer -->.*?</footer>', ref_content, re.DOTALL)
        self.footer = footer_match.group(0) if footer_match else None

        print("✓ Components loaded\n")

    def fix_page(self, file_path):
        """Apply all fixes to a page"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        fixes = []

        # Fix 1: Add mobile menu button if missing
        if 'id="mobile-menu-toggle"' not in content:
            # Find insertion point - before closing of header div, after desktop nav
            pattern = r'(<div class="hidden md:flex[^>]*>.*?</div>)\s*\n\s*</div>\s*\n\s*</nav>'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(
                    pattern,
                    r'\1\n                \n                ' + self.mobile_button + r'\n            </div>\n        </nav>',
                    content,
                    flags=re.DOTALL
                )
                fixes.append('mobile_button')

        # Fix 2: Add mobile menu div if missing
        if 'id="mobile-menu"' not in content:
            # Insert before closing nav tag
            pattern = r'(</div>\s*\n\s*)(</nav>)'
            if re.search(pattern, content):
                content = re.sub(pattern, r'\1            ' + self.mobile_menu + r'\n        \2', content, count=1)
                fixes.append('mobile_menu')

        # Fix 3: Add search input ID if missing
        if 'id="search-input"' not in content:
            content = re.sub(
                r'(<input\s+type="search"(?![^>]*id=)[^>]*)(>)',
                r'\1 id="search-input"\2',
                content
            )
            if 'id="search-input"' in content:
                fixes.append('search_id')

        # Fix 4: Fix footer
        if self.footer:
            footer_pattern = r'<footer.*?</footer>'
            if re.search(footer_pattern, content, re.DOTALL):
                content = re.sub(footer_pattern, self.footer, content, flags=re.DOTALL)
                fixes.append('footer')
            elif '</body>' in content:
                content = content.replace('</body>', '\n    ' + self.footer + '\n\n</body>')
                fixes.append('footer')

        # Fix 5: Add mobile menu script if missing
        if 'mobile-menu-toggle' not in content or 'addEventListener' not in content:
            if '</body>' in content:
                content = content.replace('</body>', self.mobile_script + '\n</body>')
                fixes.append('mobile_script')

        # Only save if changes were made
        if content != original:
            # Backup
            backup = file_path.with_suffix('.html.bak')
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(original)

            # Save fixed
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True, fixes
        else:
            return False, []

    def process_batch(self, file_list):
        """Process a batch of files"""
        results = {'fixed': 0, 'skipped': 0, 'errors': 0, 'details': []}

        for file_path in file_list:
            try:
                fixed, fixes = self.fix_page(file_path)
                if fixed:
                    print(f"✅ {file_path.name:<40} Fixed: {', '.join(fixes)}")
                    results['fixed'] += 1
                    results['details'].append({
                        'file': file_path.name,
                        'status': 'fixed',
                        'fixes': fixes
                    })
                else:
                    print(f"✓  {file_path.name:<40} Already compliant")
                    results['skipped'] += 1
            except Exception as e:
                print(f"❌ {file_path.name:<40} Error: {str(e)}")
                results['errors'] += 1
                results['details'].append({
                    'file': file_path.name,
                    'status': 'error',
                    'error': str(e)
                })

        return results


def main():
    base_path = Path("/home/uc/Projects/calcdomain2")
    fixer = BatchPageFixer(base_path)

    print("=" * 80)
    print("BATCH PAGE FIXER - COMPREHENSIVE FIXES")
    print("=" * 80)
    print()

    # Get all HTML files that need fixing (exclude templates, already perfect ones)
    all_files = sorted(base_path.glob('*.html'))

    # Exclude files
    exclude = [
        'index.html', 'search.html', 'seach.html', 'test-search.html',
        'template-calc.html', 'template-cat.html', 'template-home.html',
        'mortgage-payment.html',  # Reference file
        '1031-exchange.html', '15-vs-30-year-mortgage.html',
        '2d-frame-analysis.html', 'event-budget.html',
        'house-affordability.html', 'percentage-calculator.html'
    ]

    files_to_fix = [f for f in all_files if f.name not in exclude]

    print(f"Found {len(files_to_fix)} files to process")
    print()

    # Process in batches of 50 for progress tracking
    batch_size = 50
    total_results = {'fixed': 0, 'skipped': 0, 'errors': 0, 'details': []}

    for i in range(0, len(files_to_fix), batch_size):
        batch = files_to_fix[i:i+batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (len(files_to_fix) + batch_size - 1) // batch_size

        print(f"Batch {batch_num}/{total_batches} ({len(batch)} files)")
        print("-" * 80)

        results = fixer.process_batch(batch)

        total_results['fixed'] += results['fixed']
        total_results['skipped'] += results['skipped']
        total_results['errors'] += results['errors']
        total_results['details'].extend(results['details'])

        print()
        print(f"Batch {batch_num} Summary: Fixed: {results['fixed']}, Skipped: {results['skipped']}, Errors: {results['errors']}")
        print()

    # Final summary
    print("=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print(f"Total files processed: {len(files_to_fix)}")
    print(f"✅ Fixed: {total_results['fixed']}")
    print(f"✓  Already compliant: {total_results['skipped']}")
    print(f"❌ Errors: {total_results['errors']}")
    print()

    # Save results
    with open(base_path / 'fix_results_comprehensive.json', 'w') as f:
        json.dump(total_results, f, indent=2)

    print("Results saved to: fix_results_comprehensive.json")


if __name__ == "__main__":
    main()
