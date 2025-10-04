#!/usr/bin/env python3
"""
Batch HTML fixer for CalcDomain pages.

What it does per HTML file:
  - Removes nested <html>...</html> fragments accidentally injected in <body>
  - Ensures MathJax v3 config + script are present exactly once in <head>
  - Ensures Tailwind + Inter + search.js present (without duplicating)
  - Ensures bottom includes once: /assets/js/mobile-menu.js and /assets/js/page-enhancements.js
  - Removes duplicate/trailing repeated includes (Tailwind/Inter/search.js/assets js)
  - Optional: writes minimal assets if missing (--write-assets)

Usage:
  python3 batch_fix_html.py --root /path/to/site [--pattern '**/*.html'] [--exclude index.html --exclude template-*.html] [--dry-run] [--write-assets]

Report:
  - Prints a summary table and saves a JSON log at out/fix_report.json (relative to root)

Note:
  - Idempotent: safe to run multiple times.
"""
import argparse, re, sys, json
from pathlib import Path
from datetime import datetime

HEAD_TAILWIND = '<script src="https://cdn.tailwindcss.com"></script>'
HEAD_INTER = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
HEAD_SEARCH = '<script src="search.js" defer></script>'

HEAD_MATHJAX = '''<!-- MathJax for LaTeX formulas -->
<script>
  window.MathJax = {
    tex: {
      inlineMath: [['\\(','\\)'], ['$', '$']],
      displayMath: [['\\[','\\]']]
    },
    svg: { fontCache: 'global' }
  };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<link rel="preload" href="/assets/js/mobile-menu.js" as="script">
<link rel="preload" href="/assets/js/page-enhancements.js" as="script">
'''

BOTTOM_INCLUDES = '''<script defer src="/assets/js/mobile-menu.js"></script>
<script defer src="/assets/js/page-enhancements.js"></script>
'''

MOBILE_MENU_JS = """// /assets/js/mobile-menu.js (minimal)
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('mobile-menu-toggle');
  const menu = document.getElementById('mobile-menu');
  if (!btn || !menu) return;
  btn.addEventListener('click', () => {
    const isOpen = !menu.classList.contains('hidden');
    menu.classList.toggle('hidden', isOpen);
    btn.setAttribute('aria-expanded', String(!isOpen));
  });
});
"""

PAGE_ENHANCEMENTS_JS = """// /assets/js/page-enhancements.js
document.addEventListener('DOMContentLoaded', () => {
  // Upgrade FAQ H3 blocks to <details>
  const faq = document.querySelector('#faq');
  const wrap = faq ? faq.nextElementSibling : null;
  if (faq && wrap) {
    let n = wrap.firstElementChild;
    while (n) {
      if (n.tagName === 'H3') {
        const q = n.textContent.trim();
        const parts = [];
        let cur = n.nextElementSibling;
        while (cur && cur.tagName !== 'H3') {
          parts.push(cur.outerHTML);
          const rm = cur;
          cur = cur.nextElementSibling;
          wrap.removeChild(rm);
        }
        const details = document.createElement('details');
        details.className = 'bg-white rounded-lg border p-4 mb-2';
        const summary = document.createElement('summary');
        summary.className = 'cursor-pointer font-semibold select-none';
        summary.textContent = q;
        const ans = document.createElement('div');
        ans.className = 'pt-2 text-gray-700';
        ans.innerHTML = parts.join('');
        details.appendChild(summary);
        details.appendChild(ans);
        wrap.removeChild(n);
        wrap.insertBefore(details, cur || null);
        n = cur;
      } else {
        n = n.nextElementSibling;
      }
    }
  }
});
"""

def strip_nested_html_blocks(html: str) -> str:
  # remove nested <html>...</html> chunks inside body
  html = re.sub(r"<html>\s*<head>.*?</head>\s*</html>", "", html, flags=re.I|re.S)
  html = re.sub(r"<html>\s*<body>.*?</body>\s*</html>", "", html, flags=re.I|re.S)
  html = re.sub(r"\s*<html>.*?</html>\s*", "", html, flags=re.I|re.S)
  return html

def ensure_head_requirements(html: str) -> (str, dict):
  changed = {}
  # Tailwind, Inter, search.js
  for snippet, key, detect in [
    (HEAD_INTER, "inter", "fonts.googleapis.com/css2?family=Inter"),
    (HEAD_TAILWIND, "tailwind", "cdn.tailwindcss.com"),
    (HEAD_SEARCH, "search", 'script src="search.js"')
  ]:
    if detect.lower() not in html.lower():
      html = re.sub(r"</head>", snippet + "\n</head>", html, count=1, flags=re.I)
      changed[key] = True
    else:
      changed[key] = False

  # MathJax + preloads
  if "MathJax-script" not in html:
    html = re.sub(r"</head>", HEAD_MATHJAX + "\n</head>", html, count=1, flags=re.I)
    changed["mathjax"] = True
  else:
    changed["mathjax"] = False
  return html, changed

def remove_duplicate_bottom(html: str) -> str:
  # drop repeated tailwind/fonts/search at bottom
  html = re.sub(r"(\s*<script src=\"https://cdn\.tailwindcss\.com\"></script>\s*)+$", "", html, flags=re.I)
  html = re.sub(r"(\s*<link[^>]+fonts\.googleapis\.com[^>]+>\s*)+$", "", html, flags=re.I)
  html = re.sub(r"(\s*<script[^>]*src=\"search\.js\"[^>]*></script>\s*)+$", "", html, flags=re.I)
  # remove duplicated site js
  html = re.sub(r"(\s*<script\s+defer\s+src=\"/assets/js/mobile-menu\.js\"></script>\s*){2,}", "\n<script defer src=\"/assets/js/mobile-menu.js\"></script>\n", html, flags=re.I)
  html = re.sub(r"(\s*<script\s+defer\s+src=\"/assets/js/page-enhancements\.js\"></script>\s*){2,}", "\n<script defer src=\"/assets/js/page-enhancements.js\"></script>\n", html, flags=re.I)
  return html

def ensure_bottom_includes(html: str) -> (str, dict):
  changed = {"bottom_mobile": False, "bottom_enh": False}
  if "/assets/js/mobile-menu.js" not in html:
    html = re.sub(r"</body>", '<script defer src="/assets/js/mobile-menu.js"></script>\n</body>', html, count=1, flags=re.I)
    changed["bottom_mobile"] = True
  if "/assets/js/page-enhancements.js" not in html:
    html = re.sub(r"</body>", '<script defer src="/assets/js/page-enhancements.js"></script>\n</body>', html, count=1, flags=re.I)
    changed["bottom_enh"] = True
  return html, changed

def strip_nested_and_process(html: str) -> (str, dict):
  report = {"stripped_nested": False}
  new = strip_nested_html_blocks(html)
  if new != html:
    report["stripped_nested"] = True
  html = new
  html, head_changes = ensure_head_requirements(html)
  html = remove_duplicate_bottom(html)
  html, bottom_changes = ensure_bottom_includes(html)
  report.update(head_changes)
  report.update(bottom_changes)
  return html, report

def write_assets_if_missing(root: Path):
  assets = root / "assets" / "js"
  assets.mkdir(parents=True, exist_ok=True)
  mm = assets / "mobile-menu.js"
  pe = assets / "page-enhancements.js"
  if not mm.exists():
    mm.write_text(MOBILE_MENU_JS, encoding="utf-8")
  if not pe.exists():
    pe.write_text(PAGE_ENHANCEMENTS_JS, encoding="utf-8")

def main():
  import fnmatch
  ap = argparse.ArgumentParser()
  ap.add_argument("--root", required=True, help="Site root (e.g., /home/yeahupsrl/calcdomain2)")
  ap.add_argument("--pattern", default="**/*.html", help="Glob pattern relative to root (default: **/*.html)")
  ap.add_argument("--exclude", action="append", default=[], help="Glob(s) to exclude (repeatable)")
  ap.add_argument("--dry-run", action="store_true", help="Analyze only; do not write files")
  ap.add_argument("--write-assets", action="store_true", help="Create minimal assets js if missing")
  args = ap.parse_args()

  root = Path(args.root).resolve()
  if not root.exists():
    print(f"Root not found: {root}", file=sys.stderr)
    sys.exit(2)

  if args.write_assets:
    write_assets_if_missing(root)

  # Collect files
  if args.pattern == "**/*.html":
    files = list(root.rglob("*.html"))
  else:
    files = list(root.glob(args.pattern))

  # Apply excludes
  targets = []
  import fnmatch as _fnm
  for f in files:
    rel = f.relative_to(root).as_posix()
    if any(_fnm.fnmatch(rel, ex) for ex in args.exclude):
      continue
    if f.is_file():
      targets.append(f)

  out_dir = root / "out"
  out_dir.mkdir(parents=True, exist_ok=True)
  report_path = out_dir / "fix_report.json"
  report = {
    "root": str(root),
    "pattern": args.pattern,
    "exclude": args.exclude,
    "ts": datetime.utcnow().isoformat() + "Z",
    "processed": [],
    "summary": {}
  }

  changed = 0
  for fp in targets:
    try:
      html = fp.read_text(encoding="utf-8", errors="ignore")
      new_html, rep = strip_nested_and_process(html)
      rep["file"] = fp.relative_to(root).as_posix()
      rep["changed"] = (new_html != html)
      if rep["changed"] and not args.dry_run:
        fp.write_text(new_html, encoding="utf-8")
      report["processed"].append(rep)
      if rep["changed"]:
        changed += 1
      print(f"[{'CHANGED' if rep['changed'] else 'OK'}] {rep['file']}  "
            f"(nested={rep['stripped_nested']} mathjax={rep['mathjax']} "
            f"tailwind={rep['tailwind']} inter={rep['inter']} search={rep['search']} "
            f"bottomMobile={rep['bottom_mobile']} bottomEnh={rep['bottom_enh']})")
    except Exception as e:
      print(f"[ERROR] {fp}: {e}", file=sys.stderr)

  report["summary"] = {
    "files_total": len(targets),
    "files_changed": changed
  }
  report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
  print(f"== Summary: {changed}/{len(targets)} files changed. Report -> {report_path}")

if __name__ == "__main__":
  main()
