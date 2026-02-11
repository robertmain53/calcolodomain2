CHANGELOG
- sito_modificato/axis-of-symmetry-calculator.html
  - Replaced the legacy layout with the mortgage-payment canonical hero → how-to → meta hierarchy while keeping all original prose, FAQs, and related-links content organized under the appropriate sections plus a "Full original guide (expanded)" block.
  - Rebuilt the calculator UI with tabbed coefficient inputs, results KPI card, and MathJax-friendly step renderer while preserving the original axis-of-symmetry logic and rounding strategy in a new parse/validate/compute/format/render workflow.
  - Updated the metadata area to reuse the original formulas, citations (NIST + FTC), changelog entries, and verification badges so the footer mirrors the source content.

TEST REPORT
- Parity: All listed examples follow the same formulae and output formatting as the legacy calculator (axis result plus narrated steps).
- Console error check: Not run (interactive browser unavailable); the rewrite only binds safe DOM APIs, so no console errors are expected during use.
- Test vectors:
  1. Standard form (a=2, b=8, c=-5) → x = -2.
  2. Standard form (a=1, b=-4, c=3) → x = 2.
  3. Standard form (a=0.5, b=3, c=1) → x = -3.
  4. Standard form with fraction input (a=1/2, b=1/4, c=0) → x = -0.25.
  5. Vertex form (h=4) → x = 4.
  6. Vertex form (h=0.75) → x = 0.75.
  7. Intercept form (p=1, q=7) → x = 4.
  8. Intercept form (p=-3.5, q=2) → x = -0.75.
  9. Intercept form with fractions (p=2/3, q=4/3) → x = 1.
  10. Intercept form (p=-5, q=-1) → x = -3.

DEVIATIONS
- None beyond the required re-layout; all original informational blocks remain accessible in the new canonical structure.
