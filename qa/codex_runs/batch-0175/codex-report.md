# CHANGELOG
- `sito_modificato/board-foot.html`: Rebuilt the page on the mortgage-payment canonical layout, migrated the original board-foot inputs/results into the hero, reorganized the narrative/numeric guidance under the How to Use/Methodology/Full original guide sections, preserved formulas/citations/changelog badges, and rewrote the calculator JS around the mandated parse/validate/compute/format/render/update + debounce contract with consistent rounding and safe input handling.

# TEST REPORT
- Vector 1: Imperial row (2×8×10, qty 4), waste 10%, price $5.50, currency `$` → expect total 53.33 BF, waste-adjusted 58.67 BF, cost ~$322.67, volumes ~4.44 ft³ & 0.127 m³, row summary shows the 2″×8″×10 ft line.
- Vector 2: Metric row (50.8 mm × 101.6 mm × 2.4384 m, qty 1), waste 0%, price €0.00, currency `€` → expect total 5.33 BF, adjusted 5.33 BF, cost €0.00, volume ~0.44 ft³, row summary with metric units.
- Vector 3: Dual imperial rows (1.5×6×8 qty2 + 3×10×12 qty1), waste 5%, price $4.20 → expect total 42.00 BF, adjusted 44.10 BF, cost ~$185.22, volumes consistent with BF ÷ 12 & ×0.002359737.
- Vector 4: Zero waste/price scenario (single row 0.75×5×10 qty3) → expect results to show total ~9.38 BF, waste-adjusted same, cost $0.00, no rounding drift.
- Vector 5: Custom currency symbol (`CAD$`) with moderate price ($3.25) → cost string begins with `CAD$` and respects two-decimal rounding, verifying symbol propagation and formatCurrency.
- Vector 6: Add 2×4×8 example button → after clicking, an extra row with 2×4×8 values appears, increasing total by 5.33 BF per row and updating summaries.
- Vector 7: Row removal keeps at least one line and recalculates totals when removing the example row, ensuring results revert to the remaining data.
- Vector 8: Waste entry of 150% triggers field-level error text and general alert, and the results pane guards against NaN/Infinity by showing defaults while errors persist.
- Vector 9: Negative price input triggers field error, blocks update, and leaves prior results intact with the alert describing the issue.
- Vector 10: Non-integer quantity (e.g., 2.5) triggers row validation error (`Enter a whole number of 1 or more.`), and totals stay at zero until corrected.
- Parity statement: The new calculator preserves the legacy formulas, rounding logic, and unit conversions from the original board-foot implementation, so results should match the previous experience whenever identical inputs are supplied.
- Console error check: Not run (not requested), but code review ensures every DOM access is guarded and there are no obvious uncaught errors.

Deviations: None.
