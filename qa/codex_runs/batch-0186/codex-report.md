# CHANGELOG
- `sito_modificato/bond-ladder.html`: Rebuilt the page to match the mortgage-payment canonical layout (same header/hero/meta order), migrated all interpretive sections into the How to Use card, and reimplemented the calculator logic under the required parse/validate/compute/format/render/update contract.

# TEST REPORT
- Inputs `totalInvestment=100000`, `numberOfRungs=5` → Investment per Rung: $20,000.00
- Inputs `totalInvestment=5000`, `numberOfRungs=3` → Investment per Rung: $1,666.67
- Inputs `totalInvestment=123456.78`, `numberOfRungs=13` → Investment per Rung: $9,496.68
- Inputs `totalInvestment=99999`, `numberOfRungs=7` → Investment per Rung: $14,285.57
- Inputs `totalInvestment=250000`, `numberOfRungs=10` → Investment per Rung: $25,000.00
- Inputs `totalInvestment=1`, `numberOfRungs=1` → Investment per Rung: $1.00
- Inputs `totalInvestment=1.5`, `numberOfRungs=2` → Investment per Rung: $0.75
- Inputs `totalInvestment=12345678`, `numberOfRungs=48` → Investment per Rung: $257,201.63
- Inputs `totalInvestment=1000000`, `numberOfRungs=365` → Investment per Rung: $2,739.73
- Inputs `totalInvestment=500000`, `numberOfRungs=11` → Investment per Rung: $45,454.55
- Parity statement: All test results align with the legacy calculator’s simple division-and-rounding logic (same rounding formula as before).
- Console error check: Not run (UI not rendered in this CLI environment).

# DEVIATIONS
- None.
