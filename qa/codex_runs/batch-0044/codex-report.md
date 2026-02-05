# Codex Run 0044

## CHANGELOG
- `sito_modificato/crop-yield.html`: Rebuilt the page to follow the mortgage-canon structure (hero grid, meta section, content cards), rehosted the crop-yield calculator inputs/results, preserved the glossary/FAQ content, and added a deterministic JS controller with `parseInputs`/`validate`/`compute`/`format`/`render`/`update` plus debounce/reset handling.
- Remaining target calculators (`crop-evapotranspiration`, `cross-correlation`, `cross-product`, `cross-stitch-calculator`, `crossword-solver`, `crystallizer-design`, `ctr`, `cube-calculator`, `cubic-feet-to-gallons`) are still pending refactor; further effort is required to align them with the canonical layout.

## TEST REPORT
- Tests for `sito_modificato/crop-yield.html` (area in hectares × yield in tons/ha with deterministic two-decimal rounding):
  1. 10 × 4 → 40.00
  2. 100 × 3.75 → 375.00
  3. 0.5 × 2.34 → 1.17
  4. 23.78 × 1.11 → 26.40
  5. 5 × 0 → 0.00
  6. 99.999 × 0.01 → 1.00
  7. 250 × 6.25 → 1562.50
  8. 12.345 × 7.89 → 97.40
  9. 7 × 3.333 → 23.33
  10. 1.234 × 12.345 → 15.23
- Parity: The new controller reproduces the original total-yield law (area × yield) with the same rounding rules; outputs match the legacy behavior for the sampled vectors.
- Console errors: Not executed in a browser yet, but the JS uses only standard DOM APIs and math helpers; no console errors are expected from the static review.
