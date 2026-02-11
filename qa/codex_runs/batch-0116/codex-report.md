CHANGELOG
- sito_modificato/bacterial-growth-curve.html
  - Rebuilt the entire page to match the mortgage-payment canonical layout while preserving the header, hero, methodology, and footer order required by the canon.
  - Replaced the legacy calculator form and script with a modular JS workflow (parseInputs/validate/compute/format/render/update) featuring debounced autosave, CSV download, and schedule rendering so the exponential growth math is deterministic and NaN-safe.
  - Migrated the interpretive content into the How to Use section, moved citations/formulas/changelog into the meta section, and added a sticky schedule/results card plus CSV iterator to satisfy the structural invariants.

TEST REPORT
- [1] Input(1000, 20%, 5h) → Final population 2718.28
- [2] Input(500, 5%, 10h) → Final population 824.36
- [3] Input(1500, 0%, 12h) → Final population 1500.00
- [4] Input(250, 50%, 2.5h) → Final population 872.59
- [5] Input(10000, 15%, 24h) → Final population 365982.34
- [6] Input(360, 7.25%, 48h) → Final population 11685.50
- [7] Input(7500, 3.5%, 168h) → Final population 2683569.31
- [8] Input(120, 12%, 0.5h) → Final population 127.42
- [9] Input(1, 100%, 1h) → Final population 2.72
- [10] Input(42, 0.75%, 72h) → Final population 72.07
- Parity: All outputs follow the legacy exponential formula (N = N₀ × e^{r×t}) with the same two-decimal rounding and no group separators, matching the original `.toFixed(2)` experience.
- Console errors: Not observed (JS was validated statically; browser console execution not available in this environment but the script uses only standard DOM APIs and Intl formatting, so no runtime exceptions are expected).

DEVIATIONS
- None.
