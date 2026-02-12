CHANGELOG
- sito_modificato/blood-pressure-calculator.html
  - Replaced the legacy layout with the mortgage-payment canonical structure while preserving all original informational copy, notices, and verification statements.
  - Implemented the blood-pressure calculator inputs/results inside the mandated hero grid, ensuring the cards, action buttons, and meta sections match the layout contract.
  - Rebuilt the JavaScript around parseInputs/validate/compute/format/render/update, matching the original classification logic and adding deterministic rounding-safe handling.

TEST REPORT
- Test vectors (Systolic / Diastolic → Category):
  1. 115 / 75 → Normal (Continue monitoring and maintain a healthy lifestyle.)
  2. 118 / 65 → Normal (Continue monitoring and maintain a healthy lifestyle.)
  3. 125 / 78 → Elevated (Adopt healthy habits like reducing sodium and exercising.)
  4. 128 / 70 → Elevated (Adopt healthy habits like reducing sodium and exercising.)
  5. 132 / 86 → High Blood Pressure (Stage 1) (Monitor regularly and discuss treatment with your provider.)
  6. 135 / 79 → High Blood Pressure (Stage 1) (Monitor regularly and discuss treatment with your provider.)
  7. 140 / 90 → High Blood Pressure (Stage 2) (Talk to your doctor about medications and lifestyle changes.)
  8. 138 / 92 → High Blood Pressure (Stage 2) (Talk to your doctor about medications and lifestyle changes.)
  9. 182 / 121 → Hypertensive Crisis (Call 911 or go to the emergency room.)
  10. 120 / 90 → High Blood Pressure (Stage 2) (Talk to your doctor about medications and lifestyle changes.)
- Parity: Each vector produces the same category, explanation, and guidance text as the original script, so behavior is preserved under the new layout contract.
- Console error check: Not run (browser console unavailable in this environment).

DEVIATIONS
- None; the refactor was limited to the requested file and followed the canonical structure precisely.
