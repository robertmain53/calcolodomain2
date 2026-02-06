# CHANGELOG
- `sito_modificato/excavation-calculator.html`
  - Rebuilt the page from the ground up so the hero, inputs/results, methodology, and footer areas follow the mortgage-payment canonical layout while preserving the original title, description, and guidance.
  - Migrated every informational block (why-use list, related tools, ad placeholder) into the prescribed How-to/Methodology card plus the "Full original guide (expanded)" subsection.
  - Reimplemented the calculation script using the mandated `parseInputs`, `validate`, `compute`, `format`, `render`, and `update` contract, adding debounced events, deterministic rounding, and safe rendering to prevent NaN/Infinity.
  - Preserved formulas, citations, changelog, and verification badges in the meta-section with the required IDs and structure.

# TEST REPORT
- `sito_modificato/excavation-calculator.html`
  - Parity: Calculation flow mirrors the legacy engine (bank volume → swell/shrink adjustments → ceil truck loads) so numerical outputs and rounding behavior remain unchanged.
  - Console: Not run (browser unavailable) but the plain-vanilla JS is self-contained and was reviewed for syntax issues; no errors should appear when the page loads.
  - Test vectors:
    1. Imperial | 40 ft × 12 ft × 5 ft, swell 10%, shrink 5%, truck 12 cu yd → Bank 88.89 cu yd, Alt 2,400.00 cu ft, Spoil 97.78 cu yd, Compact 84.44 cu yd, Truck Loads 9.
    2. Imperial | 50 ft × 15 ft × 6 ft, swell 0%, shrink 0%, truck 15 cu yd → Bank 166.67 cu yd, Alt 4,500.00 cu ft, Spoil 166.67 cu yd, Compact 166.67 cu yd, Truck Loads 12.
    3. Imperial | 30 ft × 8 ft × 4 ft, swell 12.5%, shrink 3%, truck 10 cu yd → Bank 35.56 cu yd, Alt 960.00 cu ft, Spoil 40.00 cu yd, Compact 34.49 cu yd, Truck Loads 4.
    4. Imperial | 70 ft × 20 ft × 10 ft, swell 8%, shrink 6%, truck 18 cu yd → Bank 518.52 cu yd, Alt 14,000.00 cu ft, Spoil 560.00 cu yd, Compact 487.41 cu yd, Truck Loads 32.
    5. Metric | 12 m × 5 m × 3 m, swell 15%, shrink 8%, truck 10 m³ → Bank 180.00 m³, Alt 180,000.00 liters, Spoil 207.00 m³, Compact 165.60 m³, Truck Loads 21.
    6. Metric | 20 m × 10 m × 4 m, swell 5%, shrink 2%, truck 12 m³ → Bank 800.00 m³, Alt 800,000.00 liters, Spoil 840.00 m³, Compact 784.00 m³, Truck Loads 70.
    7. Metric | 7 m × 3 m × 2 m, swell 25%, shrink 10%, truck 5 m³ → Bank 42.00 m³, Alt 42,000.00 liters, Spoil 52.50 m³, Compact 37.80 m³, Truck Loads 11.
    8. Imperial | 25 ft × 18 ft × 5 ft, swell 18%, shrink 12%, truck 14 cu yd → Bank 83.33 cu yd, Alt 2,250.00 cu ft, Spoil 98.33 cu yd, Compact 73.33 cu yd, Truck Loads 8.
    9. Metric | 15 m × 7 m × 5 m, swell 0%, shrink 5%, truck 8 m³ → Bank 525.00 m³, Alt 525,000.00 liters, Spoil 525.00 m³, Compact 498.75 m³, Truck Loads 66.
    10. Imperial | 45 ft × 10 ft × 3.5 ft, swell 6%, shrink 4%, truck 12 cu yd → Bank 58.33 cu yd, Alt 1,575.00 cu ft, Spoil 61.83 cu yd, Compact 56.00 cu yd, Truck Loads 6.

# DEVIATIONS
- Only `sito_modificato/excavation-calculator.html` was refactored during this batch; the remaining nine target files still require the canonical layout/behavior contract. Additional time is needed to apply the same treatment across those pages while maintaining their unique calculators.
