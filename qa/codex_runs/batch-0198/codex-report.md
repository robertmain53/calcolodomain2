CHANGELOG
- sito_modificato/break-even-calculator.html
  - Rebuilt the page into the canonical hero/how-to/meta layout with required IDs, keeping the calculator inputs/results pairing and validation behavior.
  - Preserved the original guidance, formulas, citations, and changelog content, and moved supplemental material into the “Full original guide (expanded)” panel with a new vanilla canvas chart.

TEST REPORT
- sito_modificato/break-even-calculator.html
  - Vector 1: fixed=2000, price=150, variable=100 → units=40, revenue=$6,000.00
  - Vector 2: fixed=5000, price=75, variable=25 → units=100, revenue=$7,500.00
  - Vector 3: fixed=10000, price=120, variable=80 → units=250, revenue=$30,000.00
  - Vector 4: fixed=0, price=10, variable=5 → units=0, revenue=$0.00
  - Vector 5: fixed=3000, price=50, variable=45 → units=600, revenue=$30,000.00
  - Vector 6: fixed=8000, price=45, variable=30 → units=534, revenue=$24,030.00
  - Vector 7: fixed=15000, price=200, variable=150 → units=300, revenue=$60,000.00
  - Vector 8: fixed=500, price=20, variable=10 → units=50, revenue=$1,000.00
  - Vector 9: fixed=3000, price=33.33, variable=11.11 → units=136, revenue=$4,532.88
  - Vector 10: fixed=1000, price=100, variable=99.5 → units=2,000, revenue=$200,000.00
  - Parity: The new implementation reuses the same contribution-margin math (ceil for units, per-unit revenue multiplication) so outputs match the original calculator.
  - Console errors: Node test harness reported none; browser console was not available for a live check.

DEVIATIONS
- Replaced the original Chart.js dependency with a lightweight vanilla canvas renderer to keep the page dependency-free while still depicting the revenue/cost lines.
