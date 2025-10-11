#!/usr/bin/env python3
"""
Check for 404 errors - filename mismatches and broken links
"""

import csv
import re
from pathlib import Path
from collections import defaultdict

class Error404Checker:
    def __init__(self, base_path, csv_path):
        self.base_path = Path(base_path)
        self.csv_path = Path(csv_path)
        self.csv_slugs = {}
        self.actual_files = set()
        self.issues = defaultdict(list)

    def load_csv(self):
        """Load slugs from CSV"""
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row['slug'].strip()
                self.csv_slugs[slug] = {
                    'title': row['Title'].strip(),
                    'category': row['Category (Main)'].strip(),
                    'subcategory': row['Subcategory'].strip()
                }
        print(f"✓ Loaded {len(self.csv_slugs)} slugs from CSV")

    def scan_actual_files(self):
        """Scan actual HTML files"""
        for file in self.base_path.glob('*.html'):
            if not file.name.startswith('template-'):
                self.actual_files.add(file.name)
        print(f"✓ Found {len(self.actual_files)} HTML files")

    def check_filename_mismatches(self):
        """Check if CSV slugs match actual files"""
        print("\n" + "="*80)
        print("CHECKING FILENAME MISMATCHES")
        print("="*80)

        missing_files = []

        for slug, info in self.csv_slugs.items():
            # Try different filename patterns
            possible_names = [
                f"{slug}.html",
                f"{slug}-calculator.html",
            ]

            found = False
            actual_name = None

            for name in possible_names:
                if name in self.actual_files:
                    found = True
                    actual_name = name
                    break

            if not found:
                missing_files.append({
                    'slug': slug,
                    'title': info['title'],
                    'expected': possible_names[0]
                })

        if missing_files:
            print(f"\n⚠️  Found {len(missing_files)} CSV entries without matching files:\n")
            for item in missing_files[:20]:  # Show first 20
                print(f"   ❌ {item['slug']:<40} → Expected: {item['expected']}")
            if len(missing_files) > 20:
                print(f"   ... and {len(missing_files) - 20} more")
        else:
            print("\n✅ All CSV slugs have matching files!")

        return missing_files

    def check_orphan_files(self):
        """Check for HTML files not in CSV"""
        print("\n" + "="*80)
        print("CHECKING ORPHAN FILES (not in CSV)")
        print("="*80)

        exclude = ['index.html', 'search.html', 'seach.html', 'test-search.html',
                   'template-calc.html', 'template-cat.html', 'template-home.html',
                   'about.html', 'contact.html', 'privacy.html', 'terms.html',
                   'author.html', 'blog.html']

        # Category pages
        category_pages = ['finance.html', 'health-fitness.html', 'math-conversions.html',
                         'construction-diy.html', 'lifestyle-everyday.html']
        exclude.extend(category_pages)

        orphans = []

        for filename in sorted(self.actual_files):
            if filename in exclude:
                continue

            # Remove .html and -calculator suffix to get slug
            slug = filename.replace('.html', '').replace('-calculator', '')

            # Check if slug exists in CSV
            if slug not in self.csv_slugs and filename.replace('.html', '') not in self.csv_slugs:
                orphans.append(filename)

        if orphans:
            print(f"\n⚠️  Found {len(orphans)} orphan files (not in CSV):\n")
            for filename in orphans[:30]:  # Show first 30
                print(f"   ⚠️  {filename}")
            if len(orphans) > 30:
                print(f"   ... and {len(orphans) - 30} more")
        else:
            print("\n✅ No orphan files found!")

        return orphans

    def check_internal_links(self, sample_size=50):
        """Check for broken internal links in HTML files"""
        print("\n" + "="*80)
        print(f"CHECKING INTERNAL LINKS (sample of {sample_size} files)")
        print("="*80)

        broken_links = []
        files_to_check = sorted(self.actual_files)[:sample_size]

        for filename in files_to_check:
            file_path = self.base_path / filename

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find all href links to .html files
                links = re.findall(r'href="([^"]*\.html)"', content)

                for link in links:
                    # Skip external links and anchors
                    if link.startswith('http') or link.startswith('#'):
                        continue

                    # Remove leading slash and path
                    link_file = link.split('/')[-1]

                    # Check if file exists
                    if link_file not in self.actual_files:
                        # Skip subcategories and special paths
                        if '/subcategories/' not in link and link_file not in ['index.html']:
                            broken_links.append({
                                'in_file': filename,
                                'broken_link': link,
                                'target': link_file
                            })

            except Exception as e:
                print(f"   Error reading {filename}: {e}")

        if broken_links:
            print(f"\n⚠️  Found {len(broken_links)} potentially broken links:\n")
            # Group by broken link
            by_link = defaultdict(list)
            for item in broken_links:
                by_link[item['target']].append(item['in_file'])

            for target, sources in list(by_link.items())[:20]:
                print(f"   ❌ {target} - linked from {len(sources)} files")
                for source in sources[:3]:
                    print(f"      → {source}")
                if len(sources) > 3:
                    print(f"      → ... and {len(sources) - 3} more")
        else:
            print("\n✅ No broken links found in sample!")

        return broken_links

    def generate_report(self):
        """Generate comprehensive 404 report"""
        self.load_csv()
        self.scan_actual_files()

        missing_files = self.check_filename_mismatches()
        orphans = self.check_orphan_files()
        broken_links = self.check_internal_links(sample_size=100)

        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"CSV entries: {len(self.csv_slugs)}")
        print(f"Actual files: {len(self.actual_files)}")
        print(f"Missing files: {len(missing_files)}")
        print(f"Orphan files: {len(orphans)}")
        print(f"Broken links (in sample): {len(broken_links)}")

        # Save detailed report
        report = {
            'summary': {
                'csv_entries': len(self.csv_slugs),
                'actual_files': len(self.actual_files),
                'missing_files': len(missing_files),
                'orphan_files': len(orphans),
                'broken_links': len(broken_links)
            },
            'missing_files': missing_files,
            'orphan_files': orphans,
            'broken_links': broken_links[:100]  # Limit to 100
        }

        import json
        with open(self.base_path / '404_errors_report.json', 'w') as f:
            json.dump(report, f, indent=2)

        print("\nDetailed report saved to: 404_errors_report.json")

        return report


def main():
    base_path = Path("/home/uc/Projects/calcdomain2")
    csv_path = base_path / "paths.csv"

    print("="*80)
    print("404 ERRORS CHECKER")
    print("Checking for filename mismatches and broken links")
    print("="*80)

    checker = Error404Checker(base_path, csv_path)
    checker.generate_report()


if __name__ == "__main__":
    main()
