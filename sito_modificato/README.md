# CalcDomain Static Site

This repository contains the static HTML output for CalcDomain and the tooling to rebuild
category/subcategory index pages plus the search and sitemap files.

## Build / Regenerate Output

From the repo root:

```bash
python3 run.py
```

`run.py` does the following:
- Scans all HTML in `sito_modificato/` and reads JSON-LD breadcrumbs.
- Regenerates category pages in `sito_modificato/categories/`.
- Regenerates subcategory pages in `sito_modificato/subcategories/`.
- Creates `sito_modificato/categories/general.html` for pages with no recognized category.
- Generates `sito_modificato/search.json`, `sito_modificato/calculators-data.json`, and `sito_modificato/sitemap.xml`.
- Runs `git add .`, `git commit -m "YYYY-MM-DD"`, and `git push -u origin main`.

To skip git operations:

```bash
python3 run.py --no-git
```

## How This Site Was Built

- Individual calculator pages are static HTML in `sito_modificato/`.
- Category and subcategory indexes are generated from JSON-LD breadcrumb data.
- Search and sitemap data are generated from the HTML files.

## Deploy

The deploy root is `sito_modificato/`.
