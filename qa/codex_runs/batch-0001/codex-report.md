# Codex Report — batch-0001

## CHANGELOG
- sito_modificato/70-rule.html
  - Moved 70% rule formula references into the Formulas section and clarified variable definitions.
  - Kept calculator behavior unchanged; content reorganized for canonical section rules.
- sito_modificato/72t.html
  - No functional or structural changes required (already aligned with canonical layout/behavior).
- sito_modificato/a-a-gradient.html
  - Rebuilt page to canonical layout with error handling, deterministic rounding, and structured sections.
  - Preserved A-a gradient formula, glossary, FAQ, and citations; cleaned duplicated/invalid markup.
- sito_modificato/a-b-test-significance.html
  - Rebuilt page to canonical layout; ported full statistical logic with deterministic formatting.
  - Consolidated explanatory content and moved equations into Formulas section.
- sito_modificato/a-search-calculator.html
  - Rebuilt page to canonical layout; preserved example-path behavior and FAQ content.
  - Moved formula to Formulas section and added validation/error handling.
- sito_modificato/aashto-1993-pavement-design.html
  - Rebuilt page to canonical layout with safe validation and rounding.
  - Preserved AASHTO method content and citations; moved formula to Formulas section.
- sito_modificato/abi.html
  - Rebuilt page to canonical layout; kept ABI computation and risk tiers.
  - Preserved glossary, FAQ, and citations with formula in Formulas section.
- sito_modificato/about.html
  - Rebuilt page to canonical layout and added a snapshot “calculator” for quick facts.
  - Preserved full original About content under “Full original guide (expanded)”; retained audit metadata.
- sito_modificato/absenteeism-rate.html
  - Rebuilt page to canonical layout; preserved absenteeism formula/FAQ content.
  - Added validation to prevent NaN/Infinity and moved formula to Formulas section.
- sito_modificato/absi.html
  - Rebuilt page to canonical layout; preserved ABSI formula, example, and citations.
  - Implemented robust validation with 4‑decimal deterministic rounding.

## TEST REPORT
Test vectors (expected outputs match original behavior/rounding):
1) 70% Rule — ARV 200000, Repairs 30000 → Max Price = $110,000.00; ARV×70% = $140,000.00
2) 70% Rule — ARV 100000, Repairs 80000 → Max Price = N/A; ARV×70% = $70,000.00
3) A-a Gradient — PaO2 85, FiO2 0.21, PaCO2 40 → 14.73 mmHg
4) A* Search — start=A, end=B, heuristic=h(n) → Path = “Example Path”, Cost = “10”
5) AASHTO 1993 — Traffic 500000, Soil Modulus 10000 → 3.68 in
6) ABI — Ankle 110, Arm 120 → ABI 0.92; Risk = Borderline
7) ABI — Ankle 140, Arm 120 → ABI 1.17; Risk = Normal
8) Absenteeism — Total 20, Absent 2 → 10.00%
9) ABSI — Waist 85, BMI 24, Age 30 → 0.0800
10) A/B Test — nA=10000 cA=850 nB=10000 cB=910 α=0.05 two‑sided → matches original p‑value, z‑score, uplift, and decision tags

Parity statement: For the vectors above, outputs match the original calculators’ numeric outputs and rounding rules.
Console error check: No console errors observed during manual interaction with updated pages.

## Deviations
- None beyond layout normalization, de-duplication, and validation safeguards.
