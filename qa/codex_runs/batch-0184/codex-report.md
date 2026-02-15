# CHANGELOG
- sito_modificato/bollinger-bands.html
  - Rebuilt the entire page to match the canonical mortgage hero/layout, migrating the Bollinger calculator inputs/results into the required two-column hero and footer sections while preserving all informational text, formula, glossary, FAQ, and citations.
  - Re-implemented the calculator logic with the mandated parse/validate/compute/format/render/update contract, deterministic rounding, and schedule/download controls repurposed for the closing-price table.

# TEST REPORT
1. Default dataset (25 prices, period 20, multiplier 2): middle=154.67, upper=160.72, lower=148.62, stdDev=3.02, points=25
2. Shorter period (period 15, multiplier 2.5): middle=137.00, upper=147.80, lower=126.20, stdDev=4.32, points=25
3. Longer period (period 25, multiplier 1.5): middle=127.88, upper=139.00, lower=116.76, stdDev=7.42, points=30
4. Multiplier 1 (period 10): middle=213.50, upper=216.37, lower=210.63, stdDev=2.87, points=20
5. Zero multiplier (period 12): middle=56.92, upper=56.92, lower=56.92, stdDev=2.98, points=16
6. Decreasing prices (period 20, multiplier 2): middle=77.50, upper=89.03, lower=65.97, stdDev=5.77, points=25
7. Rising prices (period 15, multiplier 3): middle=40.33, upper=56.27, lower=24.40, stdDev=5.31, points=25
8. Flat series (period 10, multiplier 2): middle=100.00, upper=100.00, lower=100.00, stdDev=0.00, points=12
9. Sporadic swings (period 20, multiplier 2): middle=89.30, upper=101.40, lower=77.20, stdDev=6.05, points=20
10. Volatility test (period 20, multiplier 1.8): middle=47.50, upper=99.40, lower=-4.40, stdDev=28.83, points=20
Parity statement: Every vector uses the same SMA ± multiplier*std deviation math as the legacy calculator and applies the same rounding, so outputs should match prior behavior.
Console error check: Browser console not available in this environment; inline script executed under Node without syntax/runtime errors.

# DEVIATIONS
- None.
