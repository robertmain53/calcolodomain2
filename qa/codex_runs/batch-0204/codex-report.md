CHANGELOG
- sito_modificato/bs-7671-cable-sizing.html — Replaced the legacy layout with the canonical hero+meta template from the mortgage sample, reorganized the narrative content into the how-to and metadata sections, and rewrote the calculator UI/logic with parse/validate/compute/format/render functions plus the required event workflow.

TEST REPORT
- Parity: The new calculator keeps the same BS 7671 formulas/rounding rules as the original page so the numeric outputs match the legacy behavior.
- Console error check: Not run (browser console not available in this environment).
- Test vectors (Node.js reproduction of the embedded compute logic, showing key outputs for each input set):
  1. mode=sizing, Ib=32, single-phase, Ca×Cg×Ci×Cf=0.800 → Iz_min=40.00 A, ΔV=17.28 V (7.51 %), max length≈19.97 m.
  2. mode=verify, Ib=40, single-phase, factors=1.000 → Iz_min=40.00 A, ΔV=15.20 V (6.61 %), max length≈11.35 m.
  3. mode=full, Ib=65, three-phase, factors≈0.769 → Iz_min=84.47 A, ΔV=21.61 V (5.40 %), max length≈32.39 m, S_min≈44.23 mm².
  4. mode=verify, Ib=55, three-phase, factors=0.900 → Iz_min=61.11 A, ΔV=23.76 V (5.94 %), max length≈26.94 m.
  5. mode=full, Ib=25, single-phase, factors=1.000 → Iz_min=25.00 A, ΔV=10.45 V (4.54 %), max length≈13.21 m, S_min≈19.44 mm².
  6. mode=sizing, Ib=20, three-phase, factors=1.000 → Iz_min=20.00 A, ΔV/max length not computed (voltage inputs omitted).
  7. mode=verify, Ib=80, single-phase, factors=0.680 → Iz_min≈117.65 A, ΔV=31.43 V (13.66 %), max length≈16.47 m.
  8. mode=full, Ib=120, three-phase, factors≈0.689 → Iz_min≈174.29 A, ΔV=42.34 V (10.58 %), max length≈28.34 m, S_min≈98.90 mm².
  9. mode=sizing, Ib=15, single-phase, factors=1.000 → Iz_min=15.00 A, ΔV=3.60 V (1.57 %), max length≈47.92 m.
 10. mode=verify, Ib=90, single-phase, factors=0.855 → Iz_min≈105.26 A, ΔV=42.52 V (18.49 %), max length≈20.28 m.
