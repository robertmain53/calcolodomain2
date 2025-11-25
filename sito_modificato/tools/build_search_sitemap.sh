#!/usr/bin/env bash
# tools/build_search_sitemap.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Prefer an activated venv, otherwise use VENV override, otherwise fallback to python3.
if [ -n "${VIRTUAL_ENV:-}" ]; then
  PY="$VIRTUAL_ENV/bin/python"
elif [ -n "${VENV:-}" ]; then
  PY="$VENV/bin/python"
else
  PY="$(command -v python3 || true)"
fi

if [ -z "$PY" ] || [ ! -x "$PY" ]; then
  echo "ERROR: Python not found. Activate your venv or set VENV to its path." >&2
  exit 1
fi

echo "[build] Generating search.json, calculators-data.json, sitemap.xml..."
"$PY" "$ROOT/tools/gen_search_and_sitemap.py"

# normalize newlines & ensure stable ordering (jq optional)
if command -v jq >/dev/null 2>&1; then
  tmp="$ROOT/search.json.tmp"
  jq '.' "$ROOT/search.json" > "$tmp" && mv "$tmp" "$ROOT/search.json"
  tmp2="$ROOT/calculators-data.json.tmp"
  jq '.' "$ROOT/calculators-data.json" > "$tmp2" && mv "$tmp2" "$ROOT/calculators-data.json"
fi

echo "[build] Done."
