# CHANGELOG
- `sito_modificato/batch-reactor-design.html`: Rebuilt the page to the canonical mortgage-layout structure, migrated the narrative content into the hero, how-to, and meta sections, and implemented the required parse/validate/compute/update workflow for the batch reactor calculator with deterministic rounding.

# TEST REPORT
- Vector 1: k=0.1, C₀=1, t=10 → C=0.3679 mol/L, % reacted=63.21%, k×t=1.0000
- Vector 2: k=0.05, C₀=2, t=30 → C=0.4463 mol/L, % reacted=77.69%, k×t=1.5000
- Vector 3: k=0.0, C₀=1.5, t=20 → C=1.5000 mol/L, % reacted=0.00%, k×t=0.0000
- Vector 4: k=0.2, C₀=0, t=10 → C=0.0000 mol/L, % reacted=0.00%, k×t=2.0000
- Vector 5: k=0.15, C₀=5, t=0 → C=5.0000 mol/L, % reacted=0.00%, k×t=0.0000
- Vector 6: k=0.3, C₀=0.8, t=5 → C=0.1785 mol/L, % reacted=77.69%, k×t=1.5000
- Vector 7: k=0.07, C₀=2.5, t=100 → C=0.0023 mol/L, % reacted=99.91%, k×t=7.0000
- Vector 8: k=1.2, C₀=0.2, t=0.5 → C=0.1098 mol/L, % reacted=45.12%, k×t=0.6000
- Vector 9: k=0.01, C₀=4, t=200 → C=0.5413 mol/L, % reacted=86.47%, k×t=2.0000
- Vector 10: k=0.5, C₀=1, t=2 → C=0.3679 mol/L, % reacted=63.21%, k×t=1.0000
- Parity note: The outputs match the legacy C = C₀ × e^{-kt} calculation with the same rounding commitments (4 decimals on concentration, 2 decimals on percent conversion, 4 decimals on k×t).
- Console error check: Not run (no browser environment during this batch run).

# DEVIATIONS
- None.
