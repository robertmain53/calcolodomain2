# CHANGELOG
- `sito_modificato/bs-7671-voltage-drop.html`: Rebuilt the entire document around the mortgage-payment canonical hero and meta structure, preserved every piece of explanatory content in the "How to Use" and "Methodology" sections, moved formulas/sources/changelog into their dedicated detail panels, added the required schedule/table controls, and replaced the calculator engine with the new parse/validate/compute/format/render/update contract plus schedule + CSV handling.

# TEST REPORT
- File: `sito_modificato/bs-7671-voltage-drop.html`
  - Test 1: ΔV=4.50 V, ΔV%=1.96%, Max L=46.00 m, Compliance=Compliant (1.96% ≤ 3%), Min CSA=4 mm² (7.50 mV/A/m)
  - Test 2: ΔV=3.60 V, ΔV%=0.90%, Max L=222.22 m, Compliance=Compliant (0.9% ≤ 5%), Min CSA=2.5 mm² (6.80 mV/A/m)
  - Test 3: ΔV=3.78 V, ΔV%=1.64%, Max L=54.76 m, Compliance=Compliant (1.64% ≤ 3%), Min CSA=10 mm² (3.10 mV/A/m)
  - Test 4: ΔV=7.35 V, ΔV%=3.20%, Max L=109.52 m, Compliance=Compliant (3.2% ≤ 5%), Min CSA=1.5 mm² (16.10 mV/A/m)
  - Test 5: ΔV=3.60 V, ΔV%=0.90%, Max L=200.00 m, Compliance=Compliant (0.9% ≤ 3%), Min CSA=10 mm² (1.70 mV/A/m)
  - Test 6: ΔV=2.55 V, ΔV%=1.11%, Max L=90.20 m, Compliance=Compliant (1.11% ≤ 5%), Min CSA=1.5 mm² (17.80 mV/A/m)
  - Test 7: ΔV=2.89 V, ΔV%=0.72%, Max L=242.42 m, Compliance=Compliant (0.72% ≤ 5%), Min CSA=6 mm² (2.70 mV/A/m)
  - Test 8: ΔV=32.00 V, ΔV%=13.91%, Max L=17.25 m, Compliance=Exceeds limit (13.91% > 3%), Min CSA=Custom coefficient – use tabulated value to search
  - Test 9: ΔV=0.52 V, ΔV%=0.13%, Max L=388.35 m, Compliance=Compliant (0.13% ≤ 5%), Min CSA=1.5 mm² (10.30 mV/A/m)
  - Test 10: ΔV=2.07 V, ΔV%=0.90%, Max L=50.00 m, Compliance=Compliant (0.9% ≤ 3%), Min CSA=2.5 mm² (10.50 mV/A/m)
- Parity: Legacy HTML shipped without an inline calculator script, so parity with prior outputs could not be confirmed; the new values strictly follow the BS 7671 tabulated formulas.
- Console: Node CLI script executing the same `compute` logic ran successfully with no uncaught errors.

# DEVIATIONS
- Introduced the canonical schedule table and CSV controls despite the legacy page lacking such a section, to satisfy the required hero layout and interactions. There is no legacy schedule data to preserve, so the new rows offer proportional ΔV per length for user guidance.
