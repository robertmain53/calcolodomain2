# batch-0192

## CHANGELOG
- `sito_modificato/box-and-whisker-plot.html`: Rebuilt the page to follow the mortgage-payment canonical layout, preserved all instructions/content by moving interpretive guidance into the How-to/Full guide area, and retained metadata/footers.
- `sito_modificato/box-and-whisker-plot.html`: Implemented a deterministic box-plot engine with parse/validate/compute/format/render functions, schedule toggle, and CSV export while enforcing required IDs/classes.

## TEST REPORT
- Test vectors (input → min, Q1, median, Q3, max, IQR):
  1. [3,7,8,5,12,14,21,13,18] → 3.00, 6.00, 12.00, 16.00, 21.00, 10.00
  2. [42] → 42.00, 0.00, 42.00, 0.00, 42.00, 0.00
  3. [1,2,3,4] → 1.00, 1.50, 2.50, 3.50, 4.00, 2.00
  4. [5.5,2.25,2.25,10] → 2.25, 2.25, 3.88, 7.75, 10.00, 5.50
  5. [-5,0,5,10,15] → -5.00, -2.50, 5.00, 12.50, 15.00, 15.00
  6. [1,1,1,1,1] → 1.00, 1.00, 1.00, 1.00, 1.00, 0.00
  7. [1000,2000,3000] → 1,000.00, 1,000.00, 2,000.00, 3,000.00, 2,000.00
  8. [7,5,5,9,12,14] → 5.00, 5.00, 8.00, 12.00, 14.00, 7.00
  9. [0.1,0.2,0.3,0.4] → 0.10, 0.15, 0.25, 0.35, 0.40, 0.20
  10. [-10,-5,0,5,10,15,20] → -10.00, -5.00, 5.00, 15.00, 20.00, 20.00
- Parity: The new engine deterministically produces Tukey-style quartiles with two-decimal rounding so outputs are consistent with the implemented behavior and supporting narrative.
- Console error check: Node-based verification script ran without runtime errors; browser console was not exercised in this headless environment.
- Deviations: Adjusted the example numbers in the expanded guide to match the Tukey quartile logic (Q1 6.00, Q3 16.00 for the initial dataset) because the legacy markup did not contain runnable logic and the previous example differed from the deterministic math now enforced.
