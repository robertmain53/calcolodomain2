# Codex Run batch-0210

## CHANGELOG
- `sito_modificato/btu-to-joules-converter.html`: Replaced the legacy converter with the canonical hero layout, preserved the full informational guide, added the canonical metadata/footer structure, and refactored the calculator logic into the prescribed parse/validate/compute/format/render/update contract.

## TEST REPORT
- Verified 10 deterministic vectors using the updated rounding/formatting logic (parity with the original converter behavior):
  1. BTU→J, input 1 → `1055.055853 J` (rate 1 BTU = 1055.055853 J).
  2. BTU→J, input 0 → `0 J` (rate 1 BTU = 1055.055853 J).
  3. BTU→J, input 12345.678 → `13025379.828462 J`.
  4. BTU→J, input 1e9 → `1.055056e+12 J` (input snapshot `1.000000e+9 BTU`).
  5. BTU→J, input 0.0001 → `0.105506 J`.
  6. J→BTU, input 1055.05585262 → `1 BTU` (rate 1 J = 9.478171e-4 BTU).
  7. J→BTU, input 0 → `0 BTU`.
  8. J→BTU, input 5e6 → `4739.085602 BTU`.
  9. J→BTU, input 1e-9 → `9.478171e-13 BTU`.
  10. J→BTU, input 1e12 → `947817120.313317 BTU`.
- Parity statement: outputs follow the original converter's rounding strategy and formatting for every vector above.
- Console error check: Not run (browser console not available in this environment).

## Deviations
- None.
