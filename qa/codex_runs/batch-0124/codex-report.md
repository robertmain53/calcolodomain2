# CHANGELOG
- `sito_modificato/barrels-to-gallons.html`: Rebuilt the page around the canonical hero layout, relocation of the detailed guide into the How to Use/Methodology section, and a new results card/JS contract that keeps barrels and gallons strictly aligned with deterministic rounding.

# TEST REPORT
- Parity: Outputs derive from the same fixed conversion factors (e.g., 1 US Oil Barrel = 42 US Gallons) so they match the numeric behavior of the prior converter.
- Test vectors:
  1. Oil barrel input 1 → 42.000000 US gallons
  2. Oil barrel input 2.5 → 105.000000 US gallons
  3. Beer barrel input 3 → 93.000000 US gallons
  4. Liquid barrel input 4 → 126.000000 US gallons
  5. Dry barrel input 1 → 28.377590 US gallons
  6. UK barrel input 0.75 → 32.425538 US gallons
  7. Oil gallons input 84 → 2.000000 barrels
  8. Dry gallons input 250 → 8.809769 barrels
  9. Liquid gallons input 63 → 2.000000 barrels
  10. UK gallons input 100 → 2.312992 barrels

# CONSOLE ERROR CHECK
- Not run: requires a browser runtime to exercise the UI and confirm the console remains clean.

# DEVIATIONS
- None.
