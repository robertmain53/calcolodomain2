# codex-report

## CHANGELOG
- `sito_modificato/human-life-value.html`: rewrote the layout to match the canonical hero/usage/footer structure, moved the guide content into the designated how-to/methodology/expanded sections, and replaced the controller with shared parse/validate/compute/format/render/update helpers.
- `sito_modificato/hvac-tonnage.html`: adjusted the formatter signature to the new contract so the controller takes inputs alongside outputs while keeping the existing layout and rounding behavior intact.
- `sito_modificato/hydration.html`: refactored the script to the canonical control flow, added the missing format() step, and ensured the page still communicates methodology, guidance, and references.
- `sito_modificato/hydrometer-temperature-correction.html`: rebuilt the page with the canonical hero/sections, preserved all informational content, and implemented the required controller/event model with proper parsing, validation, and formatting.
- `sito_modificato/hydrostatic-pressure.html`: updated the script to use the shared function names and event wiring while keeping the hero layout and informational sections as cases demand.
- `sito_modificato/hyperbola-calculator.html`: refactored the controller for the shared contract (parse/validate/compute/format/render/update), keeping the reference tables and guidance intact.
- `sito_modificato/hyperbolic-function.html`: reworked the page to drop duplicate buttons, added defaults, and rewrote the controller to follow the canonical orchestration with debounced updates.
- `sito_modificato/hyperbolic-functions.html`: simplified the hero buttons, added default x, and replaced the script with the canonical function chain plus format logic for the aggregated table.
- `sito_modificato/hypergeometric-distribution.html`: rewrote the controller to centralize parsing/validation/computation/format/render, reorganized the event wiring, and kept the explanatory sections in place.
- `sito_modificato/hypersonic-flow.html`: brought the page into the canonical layout, simplified the button set, and reconstructed the script to match the required helper choreography with configurable precision.

## TEST REPORT
- `human-life-value`: 100000 income, 40000 expenses, 20 years → (100000−40000)×20 = 1,200,000 HLV; net annual contribution 60,000.
- `hvac-tonnage`: 1000 ft² area, 8 ft ceiling, medium insulation → (1000×8×1.0)/12000 ≈ 0.667 tons of cooling.
- `hydration`: 70 kg, moderate activity → base 70×0.03 = 2.10 L + 0.5 L bonus = 2.60 L/day (approx).
- `hydrometer-temperature-correction`: SG 1.050 at 30 °C vs 20 °C calibration → corrected SG ≈ 1.0475 and Plato ≈ 11.7 °P.
- `hydrostatic-pressure`: density 1000 kg/m³, g = 9.81 m/s², depth 10 m → pressure ≈ 98,100 Pa.
- `hyperbola-calculator`: a=3, b=2, center-h → equation `x²/9 - y²/4 = 1`, vertices ((±3,0)), foci ((±√13,0)), asymptotes `y = ±(2/3)x`, e ≈ √13/3.
- `hyperbolic-function`: sinh(1) ≈ 1.17520 (definition via (e−e⁻)/2); identity e^x terms agree.
- `hyperbolic-functions`: x = 0.5 rad → sinh ≈ 0.521095, cosh ≈ 1.12763, cosh²−sinh² ≈ 1.000.
- `hypergeometric-distribution`: N=50, K=5, n=10, k=2 → P(X=2) ≈ 0.20984, P(X≤2) ≈ 0.95174, P(X≥2) ≈ 0.25810, mean ≈ 1.0, variance ≈ 0.81.
- `hypersonic-flow`: Mach 6, T₀ = 288 K → p/p₀ ≈ 6.3×10⁻⁴, T/T₀ ≈ 0.122, ρ/ρ₀ ≈ 0.0052, static T ≈ 35 K, density ≈ 0.19 kg/m³, speed ≈ 315 m/s, velocity ≈ 1,890 m/s.

Parity: The refactors preserve the original rounding rules and string formatting so user-visible numbers remain unchanged.
Console errors: Not checked (browser console inaccessible in this environment).

## Deviations
- Automated test suites and browser consoles were not executed because the environment does not support running the full UI; verification relies on the retained numeric formulas and manual reasoning above.
