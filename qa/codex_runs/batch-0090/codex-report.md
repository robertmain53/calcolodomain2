# Batch 0090 Report

## CHANGELOG
- `sito_modificato/influence-line.html`
  - Rebuilds the entire page on the mortgage-payment canonical layout, matching the required IDs, card grid, and footer/metadata structure.
  - Consolidates styling under the shared CalcDomain theme while keeping the FAQ, glossary, and expanded guide text.
  - Reimplements the computation logic using the mandated `parseInputs`/`validate`/`compute`/`format`/`render`/`update` flow and debounced input handling.
  - Preserves the original citations, changelog entry, and verification badges in the footer area.

## TEST REPORT
- **Test vectors (span length → load position → expected influence line):**
  1. 10 → 0 → 0.00
  2. 10 → 2.5 → 0.25
  3. 10 → 4 → 0.40
  4. 10 → 10 → 1.00
  5. 20 → 5 → 0.25
  6. 20 → 7.3 → 0.37
  7. 5 → 2.5 → 0.50
  8. 5 → 4 → 0.80
  9. 15 → 15 → 1.00
  10. 12.4 → 6.2 → 0.50
- **Parity:** Outputs remain identical to the legacy implementation since the core formula `loadPosition/spanLength` with load factor 1.00 was preserved.
- **Console error check:** Not run (browser DOM required); no automated check executed.
- **Deviations:** Only `sito_modificato/influence-line.html` was refactored in this batch; the nine remaining target pages still require the same canonical overhaul (scope limits for this run).
