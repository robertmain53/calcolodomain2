# CHANGELOG
- sito_modificato/bar-to-psi.html
  - Rebuilt the page to match the mortgage-payment canonical layout (header, hero grid, how-to, meta, footer) while preserving every original informational section under “Full original guide (expanded)”.
  - Added a structured calculator hero that keeps the four pressure inputs and a sticky results card, plus related-calculator sidebar content.
  - Replaced the inline conversion script with the mandated parse/validate/compute/format/render/update workflow, added input-reset behavior, and ensured rounding/validation parity with the legacy engine.

# TEST REPORT
- Test vectors (format: source unit/value → {bar, psi, kPa, atm}):
  1. Bar 1 → {bar: 1, psi: 14.50377, kPa: 100, atm: 0.9869233}
  2. Bar 2.2 → {bar: 2.2, psi: 31.9083, kPa: 220, atm: 2.171231}
  3. Bar 5.5 → {bar: 5.5, psi: 79.77076, kPa: 550, atm: 5.428078}
  4. PSI 14.50377 → {bar: 0.9999997, psi: 14.50377, kPa: 99.99997, atm: 0.986923}
  5. PSI 31.9 → {bar: 2.199428, psi: 31.9, kPa: 219.9428, atm: 2.170666}
  6. PSI 80 → {bar: 5.515806, psi: 80, kPa: 551.5806, atm: 5.443677}
  7. kPa 100 → {bar: 1, psi: 14.50377, kPa: 100, atm: 0.9869233}
  8. kPa 220 → {bar: 2.2, psi: 31.9083, kPa: 220, atm: 2.171231}
  9. atm 1 → {bar: 1.01325, psi: 14.69595, kPa: 101.325, atm: 1}
 10. atm 2.47 → {bar: 2.502728, psi: 36.29899, kPa: 250.2728, atm: 2.47}
- Parity statement: The conversion results use the same Pascal-based factors and seven-digit rounding that the legacy widget produced, so outputs match the original behavior.
- Console error check: Node execution of the conversion helper script completed with no runtime errors (browser console not available).

# DEVIATIONS
- None.
