#!/usr/bin/env python3
"""
Fix breadcrumbs and related links with proper filename matching
"""

import csv
import re
from pathlib import Path
from collections import defaultdict
import json

class SmartCSVFixer:
    def __init__(self, base_path, csv_path):
        self.base_path = Path(base_path)
        self.csv_path = Path(csv_path)
        self.calculators = {}
        self.slug_to_filename = {}  # Map CSV slug to actual filename
        self.by_category = defaultdict(list)
        self.by_subcategory = defaultdict(lambda: defaultdict(list))

    def load_csv_and_match_files(self):
        """Load CSV and match to actual files"""
        # First, get all actual files
        actual_files = {f.name: f for f in self.base_path.glob('*.html')
                       if not f.name.startswith('template-')}

        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row['slug'].strip()
                title = row['Title'].strip()
                category = row['Category (Main)'].strip()
                subcategory = row['Subcategory'].strip() if row['Subcategory'] else ''

                # Try to find actual file
                possible_names = [
                    f"{slug}.html",
                    f"{slug.replace('-calculator', '')}.html",
                    f"{slug}-calculator.html" if not slug.endswith('-calculator') else f"{slug}.html",
                ]

                actual_filename = None
                for name in possible_names:
                    if name in actual_files:
                        actual_filename = name
                        break

                # Store calculator info
                self.calculators[slug] = {
                    'title': title,
                    'category': category,
                    'subcategory': subcategory,
                    'slug': slug,
                    'filename': actual_filename
                }

                if actual_filename:
                    self.slug_to_filename[slug] = actual_filename

                    # Index by category
                    self.by_category[category].append(slug)

                    # Index by subcategory
                    if subcategory:
                        self.by_subcategory[category][subcategory].append(slug)

        matched = len(self.slug_to_filename)
        total = len(self.calculators)

        print(f"✓ Loaded {total} calculators from CSV")
        print(f"✓ Matched {matched} to actual files ({matched/total*100:.1f}%)")
        print(f"✓ Found {len(self.by_category)} main categories")
        print()

    def get_filename_from_slug(self, slug):
        """Get actual filename for a slug"""
        return self.slug_to_filename.get(slug)

    def find_slug_for_file(self, filename):
        """Find CSV slug for a filename"""
        # Try exact match
        for slug, fname in self.slug_to_filename.items():
            if fname == filename:
                return slug

        # Try without -calculator suffix
        base = filename.replace('.html', '').replace('-calculator', '')
        for slug, info in self.calculators.items():
            if slug == base or slug.replace('-calculator', '') == base:
                return slug

        return None

    def generate_breadcrumbs(self, slug):
        """Generate breadcrumbs HTML"""
        if slug not in self.calculators:
            return None

        calc = self.calculators[slug]
        category = calc['category']
        subcategory = calc['subcategory']

        cat_slug = category.lower().replace(' & ', '-').replace(' ', '-')
        breadcrumb = f'''<nav class="text-sm mb-4 text-gray-600">
            <a href="index.html" class="hover:text-blue-600">Home</a> &raquo;
            <a href="{cat_slug}.html" class="hover:text-blue-600">{category}</a> &raquo;'''

        if subcategory:
            sub_slug = f"{cat_slug}-{subcategory.lower().replace(' & ', '-').replace(' ', '-')}"
            breadcrumb += f'''
            <a href="/subcategories/{sub_slug}.html" class="hover:text-blue-600">{subcategory}</a> &raquo;'''

        breadcrumb += f'''
            <span>{calc['title']}</span>
        </nav>'''

        return breadcrumb

    def get_related_calculators(self, slug, limit=6):
        """Get related calculators with actual filenames"""
        if slug not in self.calculators:
            return []

        calc = self.calculators[slug]
        category = calc['category']
        subcategory = calc['subcategory']
        related = []

        # Get from same subcategory
        if subcategory and subcategory in self.by_subcategory[category]:
            for s in self.by_subcategory[category][subcategory]:
                if s != slug and s in self.slug_to_filename:
                    related.append({
                        'slug': s,
                        'title': self.calculators[s]['title'],
                        'filename': self.slug_to_filename[s]
                    })
                    if len(related) >= limit:
                        break

        # Get from same category
        if len(related) < limit:
            for s in self.by_category[category]:
                if s != slug and s not in [r['slug'] for r in related]:
                    if s in self.slug_to_filename:
                        related.append({
                            'slug': s,
                            'title': self.calculators[s]['title'],
                            'filename': self.slug_to_filename[s]
                        })
                        if len(related) >= limit:
                            break

        return related[:limit]

    def generate_related_section(self, slug):
        """Generate related section with correct filenames"""
        related = self.get_related_calculators(slug)
        if not related:
            return None

        calc = self.calculators.get(slug)
        category_name = calc['category'] if calc else 'Related'

        section = f'''<div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="font-bold text-lg mb-4">Related {category_name} Tools</h3>
                        <ul class="space-y-3">'''

        for rel in related:
            section += f'''
                            <li><a href="{rel['filename']}" class="text-blue-600 hover:underline">{rel['title']}</a></li>'''

        section += '''
                        </ul>
                    </div>'''

        return section

    def fix_page(self, file_path):
        """Fix a page with proper slug matching"""
        filename = file_path.name

        # Find slug for this file
        slug = self.find_slug_for_file(filename)

        if not slug:
            return False, f"No CSV entry found for {filename}"

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        fixes = []

        # Fix breadcrumbs
        breadcrumbs = self.generate_breadcrumbs(slug)
        if breadcrumbs:
            pattern = r'<nav class="text-sm mb-4 text-gray-600"[^>]*>.*?</nav>'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, breadcrumbs, content, flags=re.DOTALL)
                fixes.append('breadcrumbs')
            else:
                pattern2 = r'(<main[^>]*>\s*)'
                if re.search(pattern2, content):
                    content = re.sub(pattern2, r'\1\n                ' + breadcrumbs + '\n\n                ', content)
                    fixes.append('breadcrumbs_added')

        # Fix related section
        related_section = self.generate_related_section(slug)
        if related_section:
            if '<aside' in content and 'lg:w-1/3' in content:
                pattern = r'<div class="bg-white p-6 rounded-lg shadow-md">\s*<h3[^>]*>Related.*?</div>\s*</div>'
                if re.search(pattern, content, re.DOTALL):
                    content = re.sub(pattern, related_section, content, flags=re.DOTALL)
                    fixes.append('related_replaced')
                else:
                    # Add after ads
                    if 'Sticky Ad' in content:
                        content = re.sub(
                            r'(Sticky Ad Unit.*?</div>)\s*\n',
                            r'\1\n\n                    ' + related_section + '\n',
                            content,
                            flags=re.DOTALL
                        )
                        fixes.append('related_added')

        # Update canonical URL
        canonical_url = f"https://calcdomain.com/{filename}"
        if '<link rel="canonical"' in content:
            content = re.sub(
                r'<link rel="canonical" href="[^"]*"',
                f'<link rel="canonical" href="{canonical_url}"',
                content
            )
            fixes.append('canonical')

        if content != original:
            backup = file_path.with_suffix('.html.smartfix')
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(original)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True, fixes

        return False, []

    def process_all(self):
        """Process all files"""
        results = {'fixed': 0, 'skipped': 0, 'errors': 0, 'details': []}

        exclude = ['template-', 'index.html', 'search.html', 'test-search.html', 'seach.html']
        html_files = [f for f in sorted(self.base_path.glob('*.html'))
                      if not any(ex in f.name for ex in exclude)]

        print(f"Processing {len(html_files)} files...")
        print()

        for file_path in html_files:
            try:
                fixed, fixes = self.fix_page(file_path)

                if fixed:
                    if isinstance(fixes, list):
                        print(f"✅ {file_path.name:<50} {', '.join(fixes)}")
                        results['fixed'] += 1
                    else:
                        print(f"⚠️  {file_path.name:<50} {fixes}")
                        results['skipped'] += 1
                else:
                    results['skipped'] += 1

            except Exception as e:
                print(f"❌ {file_path.name:<50} Error: {str(e)}")
                results['errors'] += 1

        return results


def main():
    base_path = Path("/home/uc/Projects/calcdomain2")
    csv_path = base_path / "paths.csv"

    print("="*80)
    print("SMART CSV FIXER - PROPER FILENAME MATCHING")
    print("="*80)
    print()

    fixer = SmartCSVFixer(base_path, csv_path)
    fixer.load_csv_and_match_files()

    results = fixer.process_all()

    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Fixed: {results['fixed']}")
    print(f"Skipped: {results['skipped']}")
    print(f"Errors: {results['errors']}")

    with open(base_path / 'smart_fix_results.json', 'w') as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
