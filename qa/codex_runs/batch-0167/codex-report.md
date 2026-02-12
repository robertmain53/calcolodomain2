CHANGELOG
- sito_modificato/blackjack-strategy.html
  - Rebuilt the page to match the canonical CalcDomain hero layout, preserving the requested IDs and class structure while reusing all original explanatory content.
  - Consolidated the introductory, methodology, glossary, and FAQ material into the How to Use section and moved the audit/citation/changelog data into the meta section with matching verification badges.
  - Implemented the required parse/validate/compute/format/render/update functions with debounced inputs, reset support, and deterministic formatting so the UI never renders NaN/Infinity.

TEST REPORT
- Input vector (player total, dealer card) → Recommended action (matches previous Hit/Stand rule):
  1. (16, 10) → Hit
  2. (17, 10) → Stand
  3. (12, 5) → Hit
  4. (18, 2) → Stand
  5. (4, 11) → Hit
  6. (21, 3) → Stand
  7. (7, 7) → Hit
  8. (19, 9) → Stand
  9. (10, 6) → Hit
  10. (20, 11) → Stand
- Parity statement: The calculator still outputs “Hit” for player totals below 17 and “Stand” once the total reaches 17 or higher, matching the behavior of the legacy script for every valid vector.
- Console error check: Not run (browser-only), but the new DOM-based script uses standard APIs and should not emit errors.
- Deviations: Added validation/range messaging for the inputs so invalid totals do not propagate to the results, which the legacy version did not guard against; the nominal decision logic otherwise remains unchanged.
