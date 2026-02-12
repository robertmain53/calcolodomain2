CHANGELOG
- sito_modificato/bodybuilding-macro.html
  - Rebuilt the page using the mortgage-payment canonical layout while preserving every bit of the original explanatory content and metadata (formulas, citations, changelog, badges).
  - Reimplemented the macro calculator with structured parse/validate/compute/format/render/update hooks, deterministic rounding, and responsive hero/result layout.

TEST REPORT
- sito_modificato/bodybuilding-macro.html
  - Test Vector 1: weight=75 kg, calories=2500, protein=30%, fat=25% → 187.5 g protein, 69.4 g fat, 281.3 g carbs.
  - Test Vector 2: weight=68 kg, calories=2200, protein=35%, fat=20% → 192.5 g protein, 48.9 g fat, 247.5 g carbs.
  - Test Vector 3: weight=82 kg, calories=2800, protein=25%, fat=30% → 175.0 g protein, 93.3 g fat, 315.0 g carbs.
  - Test Vector 4: weight=90 kg, calories=3200, protein=40%, fat=25% → 320.0 g protein, 88.9 g fat, 280.0 g carbs.
  - Test Vector 5: weight=65 kg, calories=1800, protein=25%, fat=20% → 112.5 g protein, 40.0 g fat, 247.5 g carbs.
  - Test Vector 6: weight=80 kg, calories=3000, protein=35%, fat=30% → 262.5 g protein, 100.0 g fat, 262.5 g carbs.
  - Test Vector 7: weight=72 kg, calories=2600, protein=40%, fat=25% → 260.0 g protein, 72.2 g fat, 227.5 g carbs.
  - Test Vector 8: weight=88 kg, calories=3500, protein=30%, fat=25% → 262.5 g protein, 97.2 g fat, 393.8 g carbs.
  - Test Vector 9: weight=70 kg, calories=2100, protein=20%, fat=20% → 105.0 g protein, 46.7 g fat, 315.0 g carbs.
  - Test Vector 10: weight=85 kg, calories=4000, protein=35%, fat=20% → 350.0 g protein, 88.9 g fat, 450.0 g carbs.
  - Parity statement: outputs derive from the same legacy formulas, so rounding and behavior match the original calculator exactly.
  - Console error check: script-only execution generated no runtime errors; no browser console was available for manual interaction testing.

DEVIATIONS
- None.
