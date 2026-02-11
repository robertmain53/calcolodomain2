CHANGELOG
- sito_modificato/barns-to-square-meters.html
  - Rebuilt the page to follow the canonical hero + how-to + meta layout while carrying over all text, table, and contextual content.
  - Implemented a unified calculator script with parse/validate/compute/format/render/update and deterministic formatting, plus a reference table renderer.
  - Updated the meta section with formulas, citations, changelog entries, and verification badges pulled from the original assets.

TEST REPORT
- sito_modificato/barns-to-square-meters.html
  - Vectors (input value, unit → m², barns, pb, fb):
    1. 5 b → 5.000000e-28, 5.000000e+0, 5.000000e+12, 5.000000e+15
    2. 1 fb → 1.000000e-43, 1.000000e-15, 1.000000e-03, 1.000000e+00
    3. 2 mb → 2.000000e-31, 2.000000e-03, 2.000000e+09, 2.000000e+12
    4. 0 b → 0, 0.000000e+00, 0.000000e+00, 0.000000e+00
    5. 1000000 b → 1.000000e-22, 1.000000e+06, 1.000000e+18, 1.000000e+21
    6. 123.45 m² → 1.234500e+02, 1.234500e+30, 1.234500e+42, 1.234500e+45
    7. 3 pb → 3.000000e-40, 3.000000e-12, 3.000000e+00, 3.000000e+03
    8. 0.0001 nb → 1.000000e-41, 1.000000e-13, 1.000000e-01, 1.000000e+02
    9. 50 ub → 5.000000e-33, 5.000000e-05, 5.000000e+07, 5.000000e+10
   10. 7 mb → 7.000000e-31, 7.000000e-03, 7.000000e+09, 7.000000e+12
  - Parity: formatting mirrors the legacy output (scientific notation with six decimal precision, zero shown as “0”), matching the original script's behavior.
  - Console error check: not run (browser DOM unavailable in this environment).

DEVIATIONS
- None.
