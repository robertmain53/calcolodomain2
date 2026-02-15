# CHANGELOG
- `sito_modificato/bsa-calculator.html`: Rebuilt the BSA calculator into the canonical mortgage-payment layout, preserved all original narrative content via the How to Use card and Full original guide block, and reimplemented the interactive BSA formulas with a new parse/validate/compute/render pipeline, Chart.js bar chart, and deterministic rounding.

# TEST REPORT
- *Test vectors (inputs → Mosteller / Du Bois / Haycock / Gehan–George in m², rounded to three decimals):*
  1. Metric 170 cm / 70 kg → 1.818 / 1.810 / 1.826 / 1.831
  2. Metric 152.4 cm / 60 kg → 1.594 / 1.566 / 1.609 / 1.615
  3. Metric 190 cm / 95 kg → 2.239 / 2.234 / 2.249 / 2.246
  4. Metric 130 cm / 35 kg → 1.124 / 1.110 / 1.131 / 1.145
  5. Metric 210 cm / 120 kg → 2.646 / 2.652 / 2.653 / 2.642
  6. US 68 in / 165 lb → 1.895 / 1.883 / 1.904 / 1.908
  7. US 60 in / 130 lb → 1.580 / 1.554 / 1.594 / 1.601
  8. US 72 in / 185 lb → 2.065 / 2.061 / 2.072 / 2.073
  9. US 58 in / 110 lb → 1.429 / 1.413 / 1.438 / 1.448
  10. US 80 in / 240 lb → 2.479 / 2.485 / 2.485 / 2.478
- Parity: Each vector mirrors the outputs of the original calculator formulas (Mosteller, Du Bois, Haycock, Gehan–George) with three-decimal rounding; no behavioral drift observed when recomputing the same formulas.
- Console error check: not run (not available in this CLI-only environment).

No additional deviations were required beyond reorganizing the content to the canonical layout and updating the calculator script.
