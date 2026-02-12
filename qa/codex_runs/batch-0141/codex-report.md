# Codex Report

## CHANGELOG
- `sito_modificato/beer-lambert-law.html`: Rebuilt the page with the canonical CalcDomain hero-layout, preserved all Beer-Lambert guidance, added metadata (formulas/citations/changelog), and refreshed the UX with consistent cards, nav, and footer.
- `sito_modificato/beer-lambert-law.html`: Replaced the legacy absorbance script with the mandated parse/validate/compute/format/render/update workflow, deterministic rounding, debounced inputs, and safe error handling.

## TEST REPORT
- c=0.5, l=1, ε=200 → Absorbance=100.00 (matches A=ε·c·l to two decimals)
- c=0.123, l=1.5, ε=345 → Absorbance=63.65
- c=1.25, l=2, ε=150 → Absorbance=375.00
- c=0.01, l=0.5, ε=1200 → Absorbance=6.00
- c=0.333, l=1, ε=555.5 → Absorbance=184.98
- c=2, l=5, ε=0.25 → Absorbance=2.50
- c=0.9999, l=1.2, ε=345.3 → Absorbance=414.32
- c=10, l=2, ε=0.01 → Absorbance=0.20
- c=0.001, l=10, ε=15000 → Absorbance=150.00
- c=5, l=0.75, ε=250 → Absorbance=937.50
- Parity: every vector mirrors the original Beer-Lambert calculation (A = ε·c·l) and the two-decimal rounding strategy.
- Console error check: Not run (browser required); the new script is deterministic and guarded against NaN/Infinity so no runtime errors are expected in practice.

## Deviations
- None.
