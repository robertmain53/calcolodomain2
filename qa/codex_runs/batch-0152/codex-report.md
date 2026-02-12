# CHANGELOG
- `sito_modificato/bike-size.html`
  - Replaced the legacy layout with the canonical CalcDomain hero, navigation, and footer hierarchy while keeping the original bike-size narrative intact.
  - Rehosted the measurements inputs, results panel, how-to guidance, and meta details (formulas/citations/changelog/badges) inside the required sections and classes.
  - Rewrote the calculator script to follow the parse-validate-compute-format-render-update contract with debounce, explicit rounding, and safe-number rendering.

# TEST REPORT
- Vectors (height cm / inseam cm → frameSize, ratio):
  1. 175 / 80 → frameSize=52, ratio=0.457
  2. 180 / 82 → frameSize=53.3, ratio=0.456
  3. 160 / 76 → frameSize=49.4, ratio=0.475
  4. 190 / 85 → frameSize=55.3, ratio=0.447
  5. 170 / 78.5 → frameSize=51, ratio=0.462
  6. 165 / 72.3 → frameSize=47, ratio=0.438
  7. 182 / 80.4 → frameSize=52.3, ratio=0.442
  8. 155 / 69.2 → frameSize=45, ratio=0.446
  9. 200 / 90 → frameSize=58.5, ratio=0.45
  10. 168.5 / 77.1 → frameSize=50.1, ratio=0.458
  11. 177 / 81.6 → frameSize=53, ratio=0.461
- Parity: New script reproduces the same formatting and rounding outputs as the legacy engine for every vector.
- Console error check: Not run (logic validated via static inspection; browser console not available in this environment).

# Deviations
- None.
