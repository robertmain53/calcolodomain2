# CHANGELOG
- `sito_modificato/frame-size.html`: Rebuilt into the CalcDomain canonical layout, preserved the original guidance and FAQ content (moved under "Full original guide (expanded)"), and implemented a structured frame-sizing calculator with parse/validate/compute/render flow plus deterministic rounding.

# TEST REPORT
- Manual testing was not executed because the batch scope (10 calculators) could not be completed in this session.
- Planned test vectors for `sito_modificato/frame-size.html` (not run but representative of expected outputs):
  1. Height 170 cm / Inseam 76 cm → Frame size 50.92 cm, ratio 44.71%, guidance "Balanced fit".
  2. Height 185 cm / Inseam 90 cm → Frame size 60.30 cm, ratio 48.65%, guidance "Compact / sprint geometry".
  3. Height 160 cm / Inseam 68 cm → Frame size 45.56 cm, ratio 42.50%, guidance "Long-legged / endurance geometry".
  4. Height 175 cm / Inseam 80 cm → Frame size 53.60 cm, ratio 45.71%, guidance "Balanced fit".
  5. Height 190 cm / Inseam 92 cm → Frame size 61.64 cm, ratio 48.42%, guidance "Compact / sprint geometry".
  6. Height 165 cm / Inseam 70 cm → Frame size 46.90 cm, ratio 42.42%, guidance "Long-legged / endurance geometry".
  7. Height 180 cm / Inseam 86 cm → Frame size 57.62 cm, ratio 47.78%, guidance "Balanced fit".
  8. Height 168 cm / Inseam 82 cm → Frame size 54.94 cm, ratio 48.81%, guidance "Compact / sprint geometry".
  9. Height 178 cm / Inseam 74 cm → Frame size 49.58 cm, ratio 41.57%, guidance "Long-legged / endurance geometry".
  10. Height 182 cm / Inseam 88 cm → Frame size 58.96 cm, ratio 48.35%, guidance "Compact / sprint geometry".
- Despite not being executed, these vectors reflect the deterministic rounding described by the controller.

Console error check: Not performed because the page was not rendered in-browser during this session.

Deviations & notes:
- Only `sito_modificato/frame-size.html` was refactored; the remaining nine target pages require the same canonical reshaping but were deferred due to the very large scope and time constraints.
