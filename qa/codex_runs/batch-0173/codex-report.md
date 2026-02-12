# CHANGELOG
- sito_modificato/bmi-prime.html
  - Rebuilt the BMI Prime page to match the mortgage-payment canonical layout, including the required header, hero, methodology, meta, and footer sections.
  - Reorganized all interpretive content (data source, glossary, FAQ) into the How to Use / Methodology card and preserved formulas, citations, and changelog details inside the meta section.
  - Implemented the BMI/BMI Prime calculator logic with the mandated parse/validate/compute/format/render/update workflow, defensive rounding, and event handling mirroring the canonical behavior.

# TEST REPORT
- Test vectors (weight kg, height cm → BMI, BMI Prime):
  1. (70, 170) → BMI=24.22, BMI Prime=0.97
  2. (50, 160) → BMI=19.53, BMI Prime=0.78
  3. (90, 180) → BMI=27.78, BMI Prime=1.11
  4. (120, 165) → BMI=44.08, BMI Prime=1.76
  5. (55.5, 168.3) → BMI=19.59, BMI Prime=0.78
  6. (80, 175) → BMI=26.12, BMI Prime=1.04
  7. (66, 175) → BMI=21.55, BMI Prime=0.86
  8. (102, 185) → BMI=29.80, BMI Prime=1.19
  9. (45, 150) → BMI=20.00, BMI Prime=0.80
 10. (78.9, 172.4) → BMI=26.55, BMI Prime=1.06
- Parity: Results match the legacy BMI Prime calculations (same formulas and two-decimal rounding strategy).
- Console error check: Not run (UI inspection requires a browser, but the embedded script is isolated and uses standard DOM APIs only).

# DEVIATIONS
- None.
