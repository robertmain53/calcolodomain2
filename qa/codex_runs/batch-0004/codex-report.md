# Batch 0004 Report

## CHANGELOG
- `sito_modificato/air-force-pft.html`: Rebuilt page around the canonical layout, preserved all original guidance (how-to, methodology, guide sections, citations, changelog, verification badges), and replaced the legacy script with the new parse/validate/compute/format/render/update pipeline so the calculator retains its scoring behavior while matching the required structure and hooks.
- Remaining target files (`airbnb`, `aircraft-performance`, `aircraft-range`, `airfoil`, `aisc-bolted-connection`, `aisc-steel-beam-design`, `aisc-steel-column-design`, `aisc-welded-connection`, `alabama-income-tax`) still require refactor; paused after one page due to time.

## TEST REPORT
- **Test vectors (Air Force PFT):**
  1. Inputs {runTime: 570, pushUps: 50, sitUps: 50} → total 63.33, run 90, push 50, sit 50, rating Marginal
  2. {540, 60, 60} → 73.33, run 100, push 60, sit 60, rating Good
  3. {660, 70, 40} → 56.67, run 60, push 70, sit 40, rating Needs Improvement
  4. {720, 30, 30} → 33.33, run 40, push 30, sit 30, rating Needs Improvement
  5. {510, 90, 90} → 93.33, run 100, push 90, sit 90, rating Excellent
  6. {600, 25, 25} → 43.33, run 80, push 25, sit 25, rating Needs Improvement
  7. {750, 100, 100} → 76.67, run 30, push 100, sit 100, rating Good
  8. {480, 40, 80} → 73.33, run 100, push 40, sit 80, rating Good
  9. {590, 55, 55} → 64.44, run 83.33, push 55, sit 55, rating Marginal
  10. {650, 20, 65} → 49.44, run 63.33, push 20, sit 65, rating Needs Improvement
- **Parity statement:** Node-based computation using the same rounding logic as the page outputs produces the same 2-decimal totals and rating buckets, so the refactored JS should honor legacy behavior.
- **Console error check:** Not run (no browser environment available in this batch run).

## NOTES
- Only the Air Force PFT page was refactored so far; the other targets await the same canonical treatment.
