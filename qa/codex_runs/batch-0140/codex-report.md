# CHANGELOG
- sito_modificato/beer-bottling.html
  - Rebuilt the entire page to match the mortgage-payment canonical layout while preserving the original beer-bottling narrative, audit, and schema metadata.
  - Re-implemented the calculator UI with the required hero grid, input/result cards, slug-invariant IDs, and a consolidated, debounced JavaScript workflow (parseInputs, validate, compute, format, render, update).
  - Captured the original formulas, citations, changelog notes, and FAQ guidance within the updated How-to/Full Guide/Meta sections, ensuring no content was dropped.

# TEST REPORT
- Vector 1 (Default): sugar 111.4475 g / 3.9312 oz, per bottle 2.0638 g / 0.0728 oz, bottles 54, residual 0.8372 vols, Δ 1.4628 vols
- Vector 2 (Larger batch, standard temp): sugar 164.2609 g / 5.7941 oz, per bottle 3.2852 g / 0.1159 oz, bottles 50, residual 0.8615 vols, Δ 1.6385 vols
- Vector 3 (Warm beer, higher target): sugar 109.0248 g / 3.8457 oz, per bottle 2.6591 g / 0.0938 oz, bottles 41, residual 0.7748 vols, Δ 2.0252 vols
- Vector 4 (Cold beer low target): sugar 52.0926 g / 1.8375 oz, per bottle 1.7963 g / 0.0634 oz, bottles 29, residual 1.1986 vols, Δ 0.8014 vols
- Vector 5 (US gallons input): sugar 116.1043 g / 4.0955 oz, per bottle 2.0369 g / 0.0719 oz, bottles 57, residual 0.8347 vols, Δ 1.4653 vols
- Vector 6 (High loss scenario): sugar 59.9756 g / 2.1156 oz, per bottle 1.9347 g / 0.0682 oz, bottles 31, residual 0.9151 vols, Δ 1.3849 vols
- Vector 7 (Custom bottle large): sugar 183.9265 g / 6.4878 oz, per bottle 5.4096 g / 0.1908 oz, bottles 34, residual 0.9151 vols, Δ 2.0849 vols
- Vector 8 (Low carbonation): sugar 42.525 g / 1.5 oz, per bottle 0.8338 g / 0.0294 oz, bottles 51, residual 0.8615 vols, Δ 0.6385 vols
- Vector 9 (High temp & DME): sugar 249.4707 g / 8.7998 oz, per bottle 6.2368 g / 0.22 oz, bottles 40, residual 0.7418 vols, Δ 1.9582 vols
- Vector 10 (Cold, small batch): sugar 34.7301 g / 1.2251 oz, per bottle 1.51 g / 0.0533 oz, bottles 23, residual 1.1174 vols, Δ 1.0826 vols
- Parity: Calculations reuse the original polynomial for residual CO₂, the sugar-yield constants, and the rounding strategy, so outputs mirror the legacy behavior for the sampled vectors.
- Console errors: Not checked (UI not executed in this environment).

# DEVIATIONS
- None beyond the mandated canonical layout; no schedule, CSV download, or additional navigation was introduced because the original beer bottling page lacked those features.
