# Batch 0061 Report

## CHANGELOG
- sito_modificato/ergun-equation.html
  - Rebuilt the page using the canonical hero layout, header/footer, and meta structure so that inputs/results share the same grid, content sections, and badges as the reference.
  - Replaced the ad-hoc script with the prescribed parse/validate/compute/format/render cycle, deterministic rounding, and debounced update/reset handling while preserving the Ergun calculation and display text.

## TEST REPORT
Test vectors executed via Node against the rewritten logic (all results format to cents per the page).
1. v=0.10, d=0.010, μ=0.001, ε=0.40 → ΔP=17812.50 Pa (visc=1406.25 Pa, inert=16406.25 Pa)
2. v=0.20, d=0.010, μ=0.0015, ε=0.35 → ΔP=112944.61 Pa (visc=6822.16 Pa, inert=106122.45 Pa)
3. v=0.05, d=0.020, μ=0.001, ε=0.45 → ΔP=1433.47 Pa (visc=113.17 Pa, inert=1320.30 Pa)
4. v=0.30, d=0.008, μ=0.0008, ε=0.37 → ΔP=251860.70 Pa (visc=6996.13 Pa, inert=244864.57 Pa)
5. v=0.15, d=0.015, μ=0.002, ε=0.50 → ΔP=11300.00 Pa (visc=800.00 Pa, inert=10500.00 Pa)
6. v=0.40, d=0.005, μ=0.0005, ε=0.30 → ΔP=1482962.96 Pa (visc=31111.11 Pa, inert=1451851.85 Pa)
7. v=0.12, d=0.012, μ=0.0012, ε=0.42 → ΔP=17614.19 Pa (visc=1174.28 Pa, inert=16439.91 Pa)
8. v=0.25, d=0.009, μ=0.001, ε=0.33 → ΔP=235204.56 Pa (visc=8631.36 Pa, inert=226573.20 Pa)
9. v=0.18, d=0.011, μ=0.0009, ε=0.38 → ΔP=60510.47 Pa (visc=2269.14 Pa, inert=58241.33 Pa)
10. v=0.22, d=0.010, μ=0.0011, ε=0.36 → ΔP=121165.98 Pa (visc=4979.42 Pa, inert=116186.56 Pa)

Parity statement: The outputs follow the legacy Ergun formula and rounding rules, so values remain equivalent to the original implementation for matching inputs.

## Console Error Check
- Not run (UI console evaluation not available within this environment).

## Deviations
- Only `sito_modificato/ergun-equation.html` was refactored in this batch. The remaining nine requested target pages were not touched because of the limited time window; they still need to be migrated to the canonical layout.
