## CHANGELOG
- sito_modificato/big-o.html
  - Rebuilt the page around the canonical layout hierarchy (hero grid, how-to, meta section, footer) while keeping the original informational content.
  - Added the mandated calculator JS contract (parse/validate/compute/format/render/update) with debounced inputs, reset behavior, and deterministic rounding.
  - Preserved legacy supplemental material inside the "Full original guide (expanded)" section and relocated formulas, citations, and changelog into the meta area.

## TEST REPORT
- Test 1: O(1) @ n=1 → 1
- Test 2: O(log n) @ n=8 → 3
- Test 3: O(n) @ n=100 → 100
- Test 4: O(n log n) @ n=500 → 4,483
- Test 5: O(n²) @ n=100 → 10,000
- Test 6: O(2ⁿ) @ n=10 → 1,024
- Test 7: O(n!) @ n=10 → 3,628,800
- Test 8: O(n log n) @ n=1000 → 9,966
- Test 9: O(2ⁿ) @ n=20 → 1,048,576
- Test 10: O(n!) @ n=12 → 479,001,600
- Parity: Outputs match the original Big-O calculator’s behavior because the same estimate and formatting logic (factorial approximation, step rounding/exponential formatting, friendly growth text) was retained verbatim.
- Console error check: Node-based verification produced no errors; browser console was not available in this environment (script confirmed to be syntactically valid).

## Deviations
- None.
