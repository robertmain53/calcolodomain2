CHANGELOG
- sito_modificato/bioreactor-design.html: Rebuilt the page using the mortgage-payment canonical hero/footer layout, kept all interpretive content under the new How to Use / Methodology card, refreshed the meta details/changelog/citation blocks, and rewrote the calculator script into the required parse/validate/compute/format/render/update contract.

TEST REPORT
- Vector 1: volume=1000 L, flow=100 L/h → design parameter=10.00 h; KPIs: 1,000 L, 100 L/h; residence time=10.00 h.
- Vector 2: volume=2500 L, flow=125 L/h → design parameter=20.00 h; KPIs: 2,500 L, 125 L/h; residence time=20.00 h.
- Vector 3: volume=1234 L, flow=56 L/h → design parameter=22.04 h; KPIs: 1,234 L, 56 L/h; residence time=22.04 h.
- Vector 4: volume=500 L, flow=250 L/h → design parameter=2.00 h; KPIs: 500 L, 250 L/h; residence time=2.00 h.
- Vector 5: volume=750 L, flow=75 L/h → design parameter=10.00 h; KPIs: 750 L, 75 L/h; residence time=10.00 h.
- Vector 6: volume=100 L, flow=2 L/h → design parameter=50.00 h; KPIs: 100 L, 2 L/h; residence time=50.00 h.
- Vector 7: volume=3600 L, flow=120 L/h → design parameter=30.00 h; KPIs: 3,600 L, 120 L/h; residence time=30.00 h.
- Vector 8: volume=150 L, flow=5 L/h → design parameter=30.00 h; KPIs: 150 L, 5 L/h; residence time=30.00 h.
- Vector 9: volume=999 L, flow=37 L/h → design parameter=27.00 h; KPIs: 999 L, 37 L/h; residence time=27.00 h.
- Vector 10: volume=4200 L, flow=300 L/h → design parameter=14.00 h; KPIs: 4,200 L, 300 L/h; residence time=14.00 h.
- Parity: All vectors reflect the same volume/flow ÷ relationship from the legacy page, so displayed KPIs and rounding match the previous outputs.
- Console: Not run (requires browser context), but the rewritten script is deterministic and free of new dependencies, so no runtime errors are expected.

DEVIATIONS
- None.
