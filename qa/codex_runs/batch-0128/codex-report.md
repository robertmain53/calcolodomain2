# Codex Run 0128 Report

## CHANGELOG
- `sito_modificato/bathroom-layout-calculator.html`
  - Rebuilt the entire page atop the canonical mortgage layout (header, hero cards, meta section, footer) while preserving the original title, description, citations, changelog, and verification badges.
  - Added structured inputs/results hero, robust validation, debounced updates, per-field inline errors, and sticky results card with pass/fail messaging derived from the legacy rule set.
  - Reorganized interpretive copy into the How to Use / Full original guide sections and preserved audit notes under the new meta layout.

## TEST REPORT
- Parity note: The legacy page lacked a working calculator shell, so we validated outputs against the derived rule logic instead of a prior UI.
- Vector 1 (all values above min): All standards met (5 passes).
- Vector 2 (every rule below the minimum): 5 failure(s) reported, one for each clearance.
- Vector 3 (only toilet front below): 1 failure (toilet front) with the rest passing.
- Vector 4 (only doorway below): 1 failure (doorway width) while other clearances pass.
- Vector 5 (only shower entry provided): All standards met for the single measurement.
- Vector 6 (decimal inputs around thresholds): Toilet Side fails by 0.2"; others pass, showing rounding.
- Vector 7 (exact minimums): All standards met with zero differences.
- Vector 8 (toilet front set to 0): Toilet front fails; other clearances pass.
- Vector 9 (negative toilet front): Validation stops calculation and surfaces "Toilet Front Clearance cannot be negative."
- Vector 10 (vanity pass, doorway fail): Vanity passes; doorway fails by 1".
- Console errors: Node-based test harness executed without uncaught exceptions; browser console not run in this environment.

## DEVIATIONS
- None; all content from the legacy page was relocated to the canonical sections (hero, how-to, meta) and the audit notes were referenced in the new "Full original guide (expanded)" block.
