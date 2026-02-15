CHANGELOG
- `sito_modificato/break-even-analysis.html`
  - Rebuilt the page using the mortgage-payment canonical layout (hero inputs/results, metadata, canonical nav/footer) while keeping header/title structure intact.
  - Consolidated original guide content into a How-to/Methodology card that now covers usage guidance, data sources, formulas, glossary, example, and FAQ text.
  - Added the new vanilla JS contract (parseInputs, validate, compute, format, render, update) with debounced interactions, deterministic rounding, and safe-number handling.

TEST REPORT
- Parity: Calculated outputs rely on the original break-even formulas and the same rounding/ceil rules described on the legacy page, so rounding/behavior matches expected legacy values.
- Vector 1 (Default USD example): Break-even units = 2,778; BE sales = $111,111.11; Contribution margin ratio = 45.00%; Target units = 3,334; Margin of safety = 20.63%.
- Vector 2 (Decimal units permitted): Break-even units = 1,904.76; BE sales = $87,142.86; Contribution margin ratio = 34.43%; Projected profit = $1,500.00; Margin of safety = 4.76%.
- Vector 3 (High fixed cost, EUR): Break-even units = 3,479; BE sales = €208,695.65; Contribution margin ratio = 57.50%; Target sales = €252,173.91; Margin of safety = 30.43%.
- Vector 4 (Low margin, round up): Break-even units = 15,000; BE sales = $300,000.00; Margin of safety = -1400.00%; Projected profit = -$14,000.00; target metrics suppressed because targetProfit input is zero.
- Vector 5 (Zero target profit &GBP): Break-even units = 457.14; BE sales = £22,857.14; CM ratio = 35.00%; Projected profit = £750.00; Margin of safety = 8.57%.
- Vector 6 (No expected units): Break-even units = 1,715; BE sales = $128,571.43; Target units = 2,143; Projections and margin of safety display “—” because expected units = 0.
- Vector 7 (Large forecast): Break-even units = 4,616; BE sales = $103,846.15; Target units = 5,129; Projected profit = $52,500.00; Margin of safety = 53.85%.
- Vector 8 (JPY formatting): Break-even units = 2,000; BE sales = ¥2,400,000.00; Target profit units = 2,667; Projected profit = -¥630,000.00; Margin of safety = -233.33%.
- Vector 9 (High expected units, no target profit): Break-even units = 3,125.00; BE sales = $46,875.00; Projected profit = $7,000.00; Margin of safety = 21.88%.
- Vector 10 (Low price/Canadian): Break-even units = 2,667; BE sales = CA$26,666.67; Target units = 3,734; Margin of safety = -6.67%.
- Console error check: Not run (browser console unavailable in this environment), but the Node-based compute script executed without runtime errors.

Any deviations
- None beyond the required migration to the canonical hero layout and the inclusion of the legacy content and metadata that the brief mandated.
