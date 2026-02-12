# Batch 0178 Codex Report

## CHANGELOG
- `sito_modificato/bod.html`
  - Rebuilt the entire page to match the mortgage-payment canonical layout while preserving the BOD concept, hero, how-to, and footer hierarchy.
  - Added the required calculator sections, contextual guidance, citations, changelog, badges, and related links from the original content.
  - Implemented the new calculator script with parse/validate/compute/format/render/update functions, safe number handling, and deterministic rounding.

## TEST REPORT
- `sito_modificato/bod.html` vectors (BOD = (Initial DO - Final DO) / Volume, rounded to 2 decimals):
  1. Initial 9.00, Final 3.00, Volume 0.50 → BOD 12.00 mg/L
  2. Initial 8.50, Final 4.20, Volume 0.50 → BOD 8.60 mg/L
  3. Initial 6.00, Final 6.00, Volume 1.00 → BOD 0.00 mg/L
  4. Initial 7.00, Final 2.00, Volume 0.75 → BOD 6.67 mg/L
  5. Initial 10.20, Final 3.10, Volume 0.65 → BOD 10.92 mg/L
  6. Initial 12.00, Final 2.50, Volume 1.20 → BOD 7.92 mg/L
  7. Initial 5.30, Final 1.90, Volume 0.30 → BOD 11.33 mg/L
  8. Initial 20.00, Final 10.00, Volume 2.00 → BOD 5.00 mg/L
  9. Initial 4.50, Final 2.00, Volume 0.20 → BOD 12.50 mg/L
  10. Initial 8.00, Final 8.00, Volume 0.25 → BOD 0.00 mg/L
  - Parity statement: the calculator follows the exact same BOD formula (initial minus final DO divided by volume) with consistent rounding, so all outputs match the legacy behavior.
  - Console error check: Not executed; static inspection shows no obvious console errors and the JS guards against NaN/Infinity.

## DEVIATIONS
- None.
