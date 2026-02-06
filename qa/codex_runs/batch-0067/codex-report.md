CHANGELOG
- sito_modificato/fcfe.html: Rebuilt the calculator page using the mortgage-payment canonical layout, preserved the original explanatory guide, glossary, FAQ, formulas, citations, changelog, and verification badges, and re-implemented the FCFE computation inside the mandated parse/validate/compute/format/render/update structure with debounced inputs.
- sito_modificato/fcff.html: Not yet refactored; pending canonical layout conversion.
- sito_modificato/fdi-roi.html: Pending work to mirror canonical structure.
- sito_modificato/fea-truss.html: Pending work to mirror canonical structure.
- sito_modificato/federal-income-tax-head-of-household.html: Pending canonical refactor.
- sito_modificato/federal-income-tax-married-filing-jointly.html: Pending canonical refactor.
- sito_modificato/federal-income-tax-single.html: Pending canonical refactor.
- sito_modificato/feet-and-inches-to-cm.html: Pending canonical refactor.
- sito_modificato/feet-of-water-to-psi.html: Pending canonical refactor.
- sito_modificato/feet-per-second-to-mph.html: Pending canonical refactor.

TEST REPORT
- sito_modificato/fcfe.html test vectors (FCFE output, USD rounding):
  1. inputs = (Net Income $100,000, Depreciation $5,000, CapEx $20,000, ΔWC $3,000, Net Borrowing $10,000) → FCFE $92,000.00
  2. inputs = (0, 0, 0, 0, 0) → FCFE $0.00
  3. inputs = (−50,000, 4,000, 1,000, −2,000, 5,000) → FCFE −$40,000.00
  4. inputs = (200,000, 0, 0, 0, 0) → FCFE $200,000.00
  5. inputs = (50,000, 10,000, 50,000, 10,000, 0) → FCFE $0.00
  6. inputs = (120,000, 20,000, 50,000, −5,000, −10,000) → FCFE $85,000.00
  7. inputs = (1,000, 200, 500, 100, 50) → FCFE $650.00
  8. inputs = (750,000, 120,000, 200,000, 50,000, 30,000) → FCFE $650,000.00
  9. inputs = (30,000, 0, 15,000, 5,000, 10,000) → FCFE $20,000.00
 10. inputs = (85.50, 0.50, 20.10, −5.60, 3.25) → FCFE $74.75
- Remaining pages: no canonical refactor yet, so no diagnostic vectors executed.
- Parity: The new page reuses the original FCFE formula and rounding strategy, so outputs should match the legacy calculator to the cent when provided identical inputs.
- Console error check: not run (page not yet redeployed for interactive QA).

DEVIATIONS
- Only the FCFE calculator has been refactored so far; the other nine pages remain untouched because the full canonical migration scope could not be completed within this run. Each will require a similar rebuild in a follow-up batch.
