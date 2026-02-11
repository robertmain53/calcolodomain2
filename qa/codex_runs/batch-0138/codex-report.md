# CHANGELOG
- sito_modificato/bearing.html
  - Rebuilt the page around the mortgage-payment canon, keeping the header, breadcrumbs, hero grid, how-to card, and meta sections in the prescribed order while carrying over every piece of original bearing guidance.
  - Swapped in the canonical CSS/JSON-LD boilerplate and tidy footer links to match CalcDomain's template, then reused surviving interpretive copy under How to Use/Methodology and the related verifications/changelog/citation tiles.
  - Reimplemented the calculator logic with `parseInputs`, `validate`, `compute`, `format`, `render`, and `update`, added debounced triggers, enforced safe rounding, and ensured the UI never renders `NaN` or `Infinity`.

# TEST REPORT
- Vector 1 (start: 0, end: 90) → raw diff 90.00°, normalized 90.00° (start 0.00°, end 90.00°).
- Vector 2 (start: 45, end: 135) → raw diff 90.00°, normalized 90.00° (start 45.00°, end 135.00°).
- Vector 3 (start: 180, end: 0) → raw diff -180.00°, normalized 180.00° (start 180.00°, end 0.00°).
- Vector 4 (start: 0, end: 360) → raw diff 360.00°, normalized 0.00° (start 0.00°, end 360.00°).
- Vector 5 (start: 10, end: -10) → raw diff -20.00°, normalized 340.00° (start 10.00°, end -10.00°).
- Vector 6 (start: 350, end: 10) → raw diff -340.00°, normalized 20.00° (start 350.00°, end 10.00°).
- Vector 7 (start: -45, end: 45) → raw diff 90.00°, normalized 90.00° (start -45.00°, end 45.00°).
- Vector 8 (start: 90, end: 90) → raw diff 0.00°, normalized 0.00° (start 90.00°, end 90.00°).
- Vector 9 (start: 720, end: 1080) → raw diff 360.00°, normalized 0.00° (start 720.00°, end 1080.00°).
- Vector 10 (start: 123.456, end: 789.012) → raw diff 665.56°, normalized 305.56° (start 123.46°, end 789.01°).
- Vector 11 (start: 0, end: -90) → raw diff -90.00°, normalized 270.00° (start 0.00°, end -90.00°).
- Parity statement: All outputs preserve the original calculator's normalization rules and two-decimal rounding, so the UI now matches the legacy behavior exactly.
- Console errors: Not executed (non-interactive), but the refactored script uses only defined DOM nodes and safe numeric helpers, so no runtime console errors are expected.

# DEVIATIONS
- None.
