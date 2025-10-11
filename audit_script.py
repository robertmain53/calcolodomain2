#!/usr/bin/env python3
"""
Comprehensive HTML Page Audit Script
Systematically checks each HTML calculator page for consistency with reference standards
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import json

class PageAuditor:
    def __init__(self, base_path, reference_file="mortgage-payment.html"):
        self.base_path = Path(base_path)
        self.reference_file = reference_file
        self.reference_patterns = {}
        self.audit_results = []

    def extract_reference_patterns(self):
        """Extract key patterns from reference page"""
        ref_path = self.base_path / self.reference_file
        if not ref_path.exists():
            print(f"Reference file not found: {ref_path}")
            return False

        with open(ref_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Define patterns to check
        self.reference_patterns = {
            'mobile_menu_toggle': r'<button\s+id="mobile-menu-toggle"',
            'mobile_menu_div': r'<div\s+id="mobile-menu"',
            'mobile_menu_script': r'mobile-menu-toggle.*addEventListener',
            'breadcrumbs_nav': r'<nav\s+class="text-sm mb-4 text-gray-600">',
            'breadcrumbs_home_link': r'<a\s+href="index\.html"[^>]*>Home</a>\s*&raquo;',
            'related_section': r'<h3[^>]*>Related.*?Tools</h3>|<h3[^>]*>Related.*?Calculators</h3>',
            'sidebar_aside': r'<aside\s+class="w-full lg:w-1/3">',
            'sticky_ad': r'Sticky Ad Unit',
            'footer': r'<footer\s+class="bg-white',
            'footer_copyright': r'&copy;\s*\d{4}\s*CalcDomain',
            'footer_links': r'<a\s+href="about\.html".*?>About</a>',
            'main_nav_container': r'<nav\s+class="container mx-auto',
            'search_input': r'<input[^>]*id="search-input"',
            'logo_link': r'<a\s+href="index\.html"\s+class="[^"]*font-bold[^"]*text-blue-600[^"]*">CalcDomain</a>',
            'layout_two_column': r'<div\s+class="flex flex-col lg:flex-row gap-8">',
            'main_content': r'<main\s+class="w-full lg:w-2/3">',
        }

        return True

    def audit_single_page(self, file_path):
        """Audit a single HTML page"""
        rel_path = file_path.relative_to(self.base_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                'file': str(rel_path),
                'error': f"Could not read file: {str(e)}",
                'checks': {}
            }

        checks = {}
        issues = []

        # Check each pattern
        for pattern_name, pattern_regex in self.reference_patterns.items():
            match = re.search(pattern_regex, content, re.IGNORECASE | re.DOTALL)
            checks[pattern_name] = bool(match)
            if not match:
                issues.append(pattern_name)

        # Additional checks
        # Check if mobile menu has both toggle button and menu div
        has_toggle = checks.get('mobile_menu_toggle', False)
        has_menu = checks.get('mobile_menu_div', False)
        mobile_menu_complete = has_toggle and has_menu and checks.get('mobile_menu_script', False)

        # Check breadcrumbs completeness
        breadcrumbs_complete = checks.get('breadcrumbs_nav', False) and checks.get('breadcrumbs_home_link', False)

        # Check footer completeness
        footer_complete = checks.get('footer', False) and checks.get('footer_copyright', False)

        # Check if it has proper 2-column layout
        has_layout = checks.get('layout_two_column', False) and checks.get('main_content', False)

        return {
            'file': str(rel_path),
            'checks': checks,
            'issues': issues,
            'summary': {
                'mobile_menu_complete': mobile_menu_complete,
                'breadcrumbs_complete': breadcrumbs_complete,
                'footer_complete': footer_complete,
                'has_layout': has_layout,
                'has_related_section': checks.get('related_section', False),
                'has_sidebar': checks.get('sidebar_aside', False),
                'has_ads': checks.get('sticky_ad', False),
                'total_issues': len(issues)
            }
        }

    def audit_all_pages(self, exclude_patterns=None):
        """Audit all HTML pages"""
        if exclude_patterns is None:
            exclude_patterns = ['template-', 'index.html']

        html_files = list(self.base_path.glob('*.html'))

        # Filter out excluded files
        html_files = [
            f for f in html_files
            if not any(pattern in f.name for pattern in exclude_patterns)
        ]

        print(f"Found {len(html_files)} HTML files to audit")

        for html_file in sorted(html_files):
            result = self.audit_single_page(html_file)
            self.audit_results.append(result)

        return self.audit_results

    def generate_summary_report(self):
        """Generate a summary report"""
        total_files = len(self.audit_results)

        # Count issues
        issue_counts = defaultdict(int)
        files_with_issues = []

        for result in self.audit_results:
            if 'error' in result:
                continue

            summary = result['summary']

            if not summary['mobile_menu_complete']:
                issue_counts['missing_mobile_menu'] += 1
            if not summary['breadcrumbs_complete']:
                issue_counts['missing_breadcrumbs'] += 1
            if not summary['footer_complete']:
                issue_counts['missing_footer'] += 1
            if not summary['has_layout']:
                issue_counts['missing_layout'] += 1
            if not summary['has_related_section']:
                issue_counts['missing_related_section'] += 1
            if not summary['has_sidebar']:
                issue_counts['missing_sidebar'] += 1
            if not summary['has_ads']:
                issue_counts['missing_ads'] += 1

            if summary['total_issues'] > 0:
                files_with_issues.append({
                    'file': result['file'],
                    'issues': result['issues'],
                    'issue_count': summary['total_issues']
                })

        return {
            'total_files_audited': total_files,
            'files_with_issues': len(files_with_issues),
            'issue_breakdown': dict(issue_counts),
            'top_problematic_files': sorted(files_with_issues, key=lambda x: x['issue_count'], reverse=True)[:20]
        }

    def save_detailed_report(self, output_file='audit_detailed_report.json'):
        """Save detailed audit report to JSON"""
        output_path = self.base_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.audit_results, f, indent=2)
        print(f"Detailed report saved to: {output_path}")

    def save_summary_report(self, output_file='audit_summary_report.json'):
        """Save summary report to JSON"""
        summary = self.generate_summary_report()
        output_path = self.base_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        print(f"Summary report saved to: {output_path}")
        return summary


def main():
    base_path = "/home/uc/Projects/calcdomain2"

    auditor = PageAuditor(base_path)

    print("=" * 80)
    print("CALCDOMAIN HTML PAGE AUDIT")
    print("=" * 80)
    print()

    # Extract patterns from reference
    print("Step 1: Extracting patterns from reference page (mortgage-payment.html)...")
    if not auditor.extract_reference_patterns():
        print("Error: Could not extract reference patterns")
        return
    print(f"✓ Extracted {len(auditor.reference_patterns)} patterns to check")
    print()

    # Audit all pages
    print("Step 2: Auditing all HTML calculator pages...")
    auditor.audit_all_pages()
    print("✓ Audit complete")
    print()

    # Generate and display summary
    print("Step 3: Generating summary report...")
    summary = auditor.generate_summary_report()
    print()

    print("=" * 80)
    print("AUDIT SUMMARY")
    print("=" * 80)
    print(f"Total files audited: {summary['total_files_audited']}")
    print(f"Files with issues: {summary['files_with_issues']}")
    print()

    print("Issue Breakdown:")
    print("-" * 80)
    for issue, count in sorted(summary['issue_breakdown'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / summary['total_files_audited']) * 100
        print(f"  {issue.replace('_', ' ').title():<40} {count:>4} files ({percentage:>5.1f}%)")
    print()

    print("Top 20 Most Problematic Files:")
    print("-" * 80)
    for i, file_info in enumerate(summary['top_problematic_files'][:20], 1):
        print(f"{i:2}. {file_info['file']:<50} ({file_info['issue_count']} issues)")
    print()

    # Save reports
    print("Step 4: Saving detailed reports...")
    auditor.save_detailed_report()
    auditor.save_summary_report()
    print()
    print("=" * 80)
    print("AUDIT COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
