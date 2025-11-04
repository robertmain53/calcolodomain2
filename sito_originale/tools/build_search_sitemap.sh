#!/usr/bin/env bash
# tools/build_search_sitemap.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

VENV="${VENV:-/home/yeahupsrl/.venv}"
PY="$VENV/bin/python"

if [ ! -x "$PY" ]; then
  echo "ERROR: Python venv not found at $PY"
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
