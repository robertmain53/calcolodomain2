# CHANGELOG
- sito_modificato/bohr-model.html
  - Rebuilt the page to follow the mortgage-payment canonical layout (hero grid, how-to/methodology, meta) while keeping the same navigation/footer structure.
  - Migrated every original guide/FAQ paragraph into the new "Full original guide (expanded)" panel and preserved the cited sources, formulas, and changelog entries under the required meta section (Formulas / Citations / Changelog).
  - Replaced the legacy script with modular `parseInputs`, `validate`, `compute`, `format`, `render`, and `update` logic, added debounced input handling, and enforced consistent formatting (4 decimals) for energy and radius outputs.

# TEST REPORT
- Parity: Energy and radius values continue to follow the Bohr model formulas (`E = -13.6 × Z² / n²`, `r = 0.529 × n² / Z`), so the new layout shows the same numeric behavior as the legacy engine (same rounding to four decimals).
- Test vectors (inputs -> Energy / Radius):
  1. n=1, Z=1 -> -13.6000 eV / 0.5290 Å
  2. n=2, Z=1 -> -3.4000 eV / 2.1160 Å
  3. n=3, Z=1 -> -1.5111 eV / 4.7610 Å
  4. n=1, Z=2 -> -54.4000 eV / 0.2645 Å
  5. n=2, Z=2 -> -13.6000 eV / 1.0580 Å
  6. n=5, Z=1 -> -0.5440 eV / 13.2250 Å
  7. n=4, Z=3 -> -7.6500 eV / 2.8213 Å
  8. n=1, Z=10 -> -1360.0000 eV / 0.0529 Å
  9. n=2, Z=5 -> -85.0000 eV / 0.4232 Å
 10. n=3, Z=5 -> -37.7778 eV / 0.9522 Å
- Console error check: Not run (browser console not available in this environment).

# DEVIATIONS
- None.
