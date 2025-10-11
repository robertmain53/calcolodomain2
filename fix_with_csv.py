#!/usr/bin/env python3
"""
Fix breadcrumbs, related links, and URLs using CSV data
"""

import csv
import re
from pathlib import Path
from collections import defaultdict
import json

class CSVBasedFixer:
    def __init__(self, base_path, csv_path):
        self.base_path = Path(base_path)
        self.csv_path = Path(csv_path)
        self.calculators = {}
        self.by_category = defaultdict(list)
        self.by_subcategory = defaultdict(lambda: defaultdict(list))
        self.load_csv()

    def load_csv(self):
        """Load and parse CSV file"""
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row['slug'].strip()
                title = row['Title'].strip()
                category = row['Category (Main)'].strip()
                subcategory = row['Subcategory'].strip() if row['Subcategory'] else ''

                # Store calculator info
                self.calculators[slug] = {
                    'title': title,
                    'category': category,
                    'subcategory': subcategory,
                    'slug': slug
                }

                # Index by category
                self.by_category[category].append(slug)

                # Index by subcategory
                if subcategory:
                    self.by_subcategory[category][subcategory].append(slug)

        print(f"✓ Loaded {len(self.calculators)} calculators from CSV")
        print(f"✓ Found {len(self.by_category)} main categories")
        print(f"✓ Found {sum(len(subs) for subs in self.by_subcategory.values())} subcategories")
        print()

    def get_category_slug(self, category):
        """Convert category name to slug"""
        return category.lower().replace(' & ', '-').replace(' ', '-').replace('&', 'and')

    def get_subcategory_slug(self, category, subcategory):
        """Convert subcategory to slug"""
        cat_slug = self.get_category_slug(category)
        sub_slug = subcategory.lower().replace(' & ', '-').replace(' ', '-').replace('&', 'and')
        return f"{cat_slug}-{sub_slug}"

    def generate_breadcrumbs(self, slug):
        """Generate breadcrumbs HTML for a calculator"""
        if slug not in self.calculators:
            return None

        calc = self.calculators[slug]
        category = calc['category']
        subcategory = calc['subcategory']
        title = calc['title']

        cat_slug = self.get_category_slug(category)

        breadcrumb = f'''<nav class="text-sm mb-4 text-gray-600">
            <a href="index.html" class="hover:text-blue-600">Home</a> &raquo;
            <a href="{cat_slug}.html" class="hover:text-blue-600">{category}</a> &raquo;'''

        if subcategory:
            sub_slug = self.get_subcategory_slug(category, subcategory)
            breadcrumb += f'''
            <a href="/subcategories/{sub_slug}.html" class="hover:text-blue-600">{subcategory}</a> &raquo;'''

        breadcrumb += f'''
            <span>{title}</span>
        </nav>'''

        return breadcrumb

    def get_related_calculators(self, slug, limit=6):
        """Get related calculators from same subcategory/category"""
        if slug not in self.calculators:
            return []

        calc = self.calculators[slug]
        category = calc['category']
        subcategory = calc['subcategory']
        related = []

        # First, get from same subcategory
        if subcategory and subcategory in self.by_subcategory[category]:
            for s in self.by_subcategory[category][subcategory]:
                if s != slug and s in self.calculators:
                    related.append(self.calculators[s])
                    if len(related) >= limit:
                        break

        # If not enough, get from same category
        if len(related) < limit:
            for s in self.by_category[category]:
                if s != slug and s not in [r['slug'] for r in related]:
                    if s in self.calculators:
                        related.append(self.calculators[s])
                        if len(related) >= limit:
                            break

        return related[:limit]

    def generate_related_section(self, slug):
        """Generate related calculators HTML section"""
        related = self.get_related_calculators(slug)
        if not related:
            return None

        calc = self.calculators.get(slug)
        category_name = calc['category'] if calc else 'Related'

        section = f'''<div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="font-bold text-lg mb-4">Related {category_name} Tools</h3>
                        <ul class="space-y-3">'''

        for rel in related:
            rel_slug = rel['slug']
            rel_title = rel['title']
            # Try to find the actual file
            file_path = self.base_path / f"{rel_slug}.html"
            if not file_path.exists():
                # Try with -calculator suffix
                file_path = self.base_path / f"{rel_slug}-calculator.html"

            filename = file_path.name if file_path.exists() else f"{rel_slug}.html"

            section += f'''
                            <li><a href="{filename}" class="text-blue-600 hover:underline">{rel_title}</a></li>'''

        section += '''
                        </ul>
                    </div>'''

        return section

    def fix_page(self, file_path):
        """Fix a single page with CSV data"""
        # Extract slug from filename
        filename = file_path.stem
        slug = filename.replace('-calculator', '')

        # Check if slug exists in CSV
        if slug not in self.calculators:
            # Try exact match
            if filename in self.calculators:
                slug = filename
            else:
                return False, f"Slug '{slug}' not found in CSV"

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        fixes = []

        # Fix 1: Update breadcrumbs
        breadcrumbs = self.generate_breadcrumbs(slug)
        if breadcrumbs:
            # Find and replace existing breadcrumbs
            pattern = r'<nav class="text-sm mb-4 text-gray-600"[^>]*>.*?</nav>'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, breadcrumbs, content, flags=re.DOTALL)
                fixes.append('breadcrumbs')
            else:
                # Try to insert breadcrumbs after <main> tag
                pattern2 = r'(<main[^>]*>\s*)'
                if re.search(pattern2, content):
                    content = re.sub(pattern2, r'\1\n                ' + breadcrumbs + '\n\n                ', content)
                    fixes.append('breadcrumbs_inserted')

        # Fix 2: Update/add related section in sidebar
        related_section = self.generate_related_section(slug)
        if related_section:
            # Check if sidebar exists
            if '<aside' in content and 'lg:w-1/3' in content:
                # Find sidebar sticky div
                pattern = r'(<div class="sticky top-24">)(.*?)(</aside>)'
                match = re.search(pattern, content, re.DOTALL)

                if match:
                    sidebar_content = match.group(2)

                    # Check if related section already exists
                    if 'Related' in sidebar_content and 'Tools' in sidebar_content:
                        # Replace existing related section
                        related_pattern = r'<div class="bg-white p-6 rounded-lg shadow-md">\s*<h3[^>]*>Related.*?</div>\s*</div>'
                        if re.search(related_pattern, sidebar_content, re.DOTALL):
                            new_sidebar = re.sub(related_pattern, related_section, sidebar_content, flags=re.DOTALL)
                            content = content.replace(sidebar_content, new_sidebar)
                            fixes.append('related_replaced')
                    else:
                        # Add related section after ads
                        content = re.sub(
                            r'(Sticky Ad Unit.*?</div>)\s*\n',
                            r'\1\n\n                    ' + related_section + '\n',
                            content,
                            flags=re.DOTALL
                        )
                        fixes.append('related_added')

        # Fix 3: Update canonical URL
        calc_info = self.calculators[slug]
        canonical_url = f"https://calcdomain.com/{file_path.name}"

        canonical_pattern = r'<link rel="canonical" href="[^"]*"'
        if re.search(canonical_pattern, content):
            content = re.sub(
                canonical_pattern,
                f'<link rel="canonical" href="{canonical_url}"',
                content
            )
            fixes.append('canonical')

        # Save if changed
        if content != original:
            # Backup
            backup = file_path.with_suffix('.html.csvfix')
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(original)

            # Save
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True, fixes

        return False, []

    def process_all(self):
        """Process all HTML files"""
        results = {'fixed': 0, 'skipped': 0, 'errors': 0, 'details': []}

        # Get all HTML files
        html_files = sorted(self.base_path.glob('*.html'))

        # Exclude templates and special files
        exclude = ['template-', 'index.html', 'search.html', 'seach.html', 'test-search.html']
        html_files = [f for f in html_files if not any(ex in f.name for ex in exclude)]

        print(f"Processing {len(html_files)} files...")
        print()

        for file_path in html_files:
            try:
                fixed, fixes = self.fix_page(file_path)

                if fixed:
                    if isinstance(fixes, list):
                        print(f"✅ {file_path.name:<45} {', '.join(fixes)}")
                        results['fixed'] += 1
                        results['details'].append({
                            'file': file_path.name,
                            'status': 'fixed',
                            'fixes': fixes
                        })
                    else:
                        print(f"⚠️  {file_path.name:<45} {fixes}")
                        results['errors'] += 1
                else:
                    results['skipped'] += 1

            except Exception as e:
                print(f"❌ {file_path.name:<45} Error: {str(e)}")
                results['errors'] += 1
                results['details'].append({
                    'file': file_path.name,
                    'status': 'error',
                    'error': str(e)
                })

        return results


def main():
    base_path = Path("/home/uc/Projects/calcdomain2")
    csv_path = base_path / "paths.csv"

    print("=" * 80)
    print("CSV-BASED BREADCRUMBS & RELATED LINKS FIXER")
    print("=" * 80)
    print()

    fixer = CSVBasedFixer(base_path, csv_path)
    results = fixer.process_all()

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Fixed: {results['fixed']}")
    print(f"Skipped: {results['skipped']}")
    print(f"Errors: {results['errors']}")
    print()

    # Save results
    with open(base_path / 'csv_fix_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("Results saved to: csv_fix_results.json")


if __name__ == "__main__":
    main()
