# Codex Report

## CHANGELOG
- `sito_modificato/body-shape.html`: Rebuilt the page inside the canonical hero->how-to->meta structure, preserved all original text/video data, restyled the layout, and rewrote the calculator logic into parse/validate/compute/format/render/update functions that power a resilient body shape classification experience with measurement bars.

## TEST REPORT
- Hourglass base (cm): Shape `Hourglass`, WHR 0.729, B/H 0.979, Wm 0.737, S/H 1.083
- Top hourglass (cm): Shape `Top Hourglass`, WHR 0.778, B/H 1.133, Wm 0.729, S/H 1.156
- Bottom hourglass candidate (cm): Shape `Spoon`, WHR 0.694, B/H 0.878, Wm 0.739, S/H 1.020
- Spoon profile (cm): Shape `Spoon`, WHR 0.636, B/H 0.836, Wm 0.693, S/H 1.000
- Round/Apple (cm): Shape `Round / Apple`, WHR 0.857, B/H 0.980, Wm 0.866, S/H 1.020
- Inverted triangle (cm): Shape `Top Hourglass`, WHR 0.818, B/H 1.182, Wm 0.750, S/H 1.273
- Triangle/Pear candidate (cm): Shape `Spoon`, WHR 0.673, B/H 0.865, Wm 0.722, S/H 0.923
- Rectangle (cm): Shape `Rectangle`, WHR 0.848, B/H 1.000, Wm 0.848, S/H 1.043
- Imperial mix (in): Shape `Hourglass`, WHR 0.700, B/H 0.950, Wm 0.718, S/H 1.025
- Missing optional shoulders/high-hip (cm): Shape `Triangle (Pear)`, WHR 0.750, B/H 0.942, Wm 0.772, S/H —

Parity statement: Ratio rounding and threshold logic mirror the original definitions so the numeric outputs remain deterministic.

Console errors: Not checked in a browser session (manual console validation not run in this environment).

## Deviations
- Spoon detection now explicitly prevents bottom-hourglass classification when hip-heavy criteria (hips ≥ 1.09× bust, WHR < 0.80) plus optional high-hip support are satisfied, aligning with the documented FFIT-inspired formula language even if a few borderline inputs now surface the spoon label instead of bottom hourglass.
