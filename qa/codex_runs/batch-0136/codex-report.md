CHANGELOG
- sito_modificato/bearing-capacity.html
  - Rebuilt the page to follow the mortgage-payment canonical layout (header, calc hero grid, methodology, meta, and footer) while preserving all original guidance.
  - Replaced the old form/results markup with canonical cards plus the required schedule/download controls, and reorganized text into How to Use/Methodology plus the mandated meta sections (formulas, citations, changelog, verification badges).
  - Implemented a new calculation engine (parse/validate/compute/format/render/update) that preserves the previous Terzaghi factors for backward-compatible outputs and adds a robust schedule breakdown table and CSV export.

TEST REPORT
- sito_modificato/bearing-capacity.html
  - Parity statement: Retains the legacy Terzaghi factors (Nc=5.14, Nq=1, Nγ=0.5) to ensure the same numeric behavior as the previous implementation while tightening validation and rounding to two decimals.
  - Test vectors (width m, depth m, unit weight kN/m³, cohesion kPa, friction angle ° → ultimate kN/m² with components):
    1. (2, 1, 18, 25, 30) → 155.50 (128.50, 18.00, 9.00)
    2. (3, 1.5, 20, 30, 35) → 199.20 (154.20, 30.00, 15.00)
    3. (1.5, 2, 17, 15, 28) → 117.48 (77.10, 34.00, 6.38)
    4. (2.5, 1.2, 19, 40, 33) → 240.28 (205.60, 22.80, 11.88)
    5. (2, 0.8, 16, 10, 25) → 72.20 (51.40, 12.80, 8.00)
    6. (4, 1.8, 21, 50, 37) → 315.80 (257.00, 37.80, 21.00)
    7. (1.2, 1, 14, 5, 20) → 43.90 (25.70, 14.00, 4.20)
    8. (3.5, 2.5, 22, 60, 38) → 382.65 (308.40, 55.00, 19.25)
    9. (2.2, 1.6, 18.5, 35, 32) → 219.68 (179.90, 29.60, 10.18)
    10. (1.8, 0.9, 15, 12, 27) → 81.93 (61.68, 13.50, 6.75)
  - Console error check: Not run in the CLI; please verify in a browser to confirm there are no runtime console errors.

DEVIATIONS
- None.
