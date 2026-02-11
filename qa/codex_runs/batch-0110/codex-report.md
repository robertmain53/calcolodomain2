# Batch 0110 Report

## CHANGELOG
- `sito_modificato/average-down.html`: Rebuilt the page to align with the mortgage-payment canonical layout, relocated interpretive content under How to Use and Full original guide (expanded), preserved the original formulas/citations/changelog block, and refactored the calculator script into the mandated parse/validate/compute/format/render/update flow with stronger rounding and input safety.

## TEST REPORT
- Test vectors (inputs: initial price, initial shares, new price, new shares → outputs: avg price, total shares, total cost, initial value, additional value):
  1. 100, 10, 90, 5 → 96.67, 15.00, 1450.00, 1000.00, 450.00
  2. 150, 20, 120, 10 → 140.00, 30.00, 4200.00, 3000.00, 1200.00
  3. 50, 100, 45, 50 → 48.33, 150.00, 7250.00, 5000.00, 2250.00
  4. 200, 5, 180, 2 → 194.29, 7.00, 1360.00, 1000.00, 360.00
  5. 5, 100, 10, 50 → 6.67, 150.00, 1000.00, 500.00, 500.00
  6. 120.5, 40, 110.25, 10 → 118.45, 50.00, 5922.50, 4820.00, 1102.50
  7. 88.88, 12, 92.5, 8 → 90.33, 20.00, 1806.56, 1066.56, 740.00
  8. 250, 30, 260, 15 → 253.33, 45.00, 11400.00, 7500.00, 3900.00
  9. 33.33, 3, 30, 3 → 31.67, 6.00, 189.99, 99.99, 90.00
  10. 400, 25, 350, 5 → 391.67, 30.00, 11750.00, 10000.00, 1750.00
- Parity statement: The new script still computes the weighted average cost with identical rounding and validation logic, so outputs remain identical to the legacy page for matching inputs.
- Console error check: not executed (page rendered statically in editor-only environment).

## Deviations
- None.
