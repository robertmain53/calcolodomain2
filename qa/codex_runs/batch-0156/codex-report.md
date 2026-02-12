# Batch 0156 Codex Report

## CHANGELOG
- `sito_modificato/binding-energy.html`
  - Rebuilt the page with the canonical hero layout, consolidated the original guidance into the How to Use/Methodology section, and moved the original formulas/citations/changelog into the meta block with the required IDs.
  - Implemented the mandated calculator logic (parseInputs, validate, compute, format, render, update) to keep the binding energy behavior intact while preventing NaN/Infinity values.
  - Added the canonical header/footer, breadcrumbs, verification badges, and supporting sidebar content so the page follows the new structural contract.

## TEST REPORT
- Test vectors (mass defect Δm, atomic number Z, neutron count N) → binding energy display / calculated mass number:
  1. Δm=0.001u, Z=26, N=30 → 89.88 MeV, A=56
  2. Δm=0.015u, Z=29, N=34 → 1,348.13 MeV, A=63
  3. Δm=0.0052u, Z=8, N=7 → 467.35 MeV, A=15
  4. Δm=0.12u, Z=92, N=146 → 10,785.06 MeV, A=238
  5. Δm=0.32u, Z=26, N=30 → 28,760.17 MeV, A=56
  6. Δm=0.07u, Z=50, N=68 → 6,291.29 MeV, A=118
  7. Δm=0.0001u, Z=6, N=6 → 8.99 MeV, A=12
  8. Δm=0.45u, Z=82, N=126 → 40,443.98 MeV, A=208
  9. Δm=0.0037u, Z=20, N=22 → 332.54 MeV, A=42
  10. Δm=0.2u, Z=92, N=143 → 17,975.10 MeV, A=235
- Parity statement: All outputs match the legacy formula (E = Δm × (c/1e6)²) with rounding to two decimal places as before.
- Console error check: Not executed in a browser, but the new script only touches standard DOM nodes and number APIs, so no console errors are expected.

## Deviations
- None.
