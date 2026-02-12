# CHANGELOG
- sito_modificato/boat-loan-calculator.html
  - Rebuilt the entire page to mirror the canonical mortgage layout while preserving boat-specific content, navigation, footer, and required IDs/classes.
  - Relocated guidance into a How to Use / Methodology section, added the expanded audit reference, and curated the formula/citation/changelog panels plus verification badges.
  - Reimplemented the calculator logic with parse/validate/compute/format/render/update functions, enforced validation, added schedule toggling/CSV download, and guaranteed deterministic rounding with the original boat loan behavior.

# TEST REPORT
- Test 1 (Default): Payment=$530.96, Financed=$44,750.00, Interest=$18,964.83, TotalCost=$63,714.83, OTD=$48,950.00, Ownership=$650.96, ScheduleLen=120
- Test 2 (Zero finance fees): Payment=$314.34, Financed=$51,500.00, Interest=$13,883.69, TotalCost=$65,383.69, OTD=$65,500.00, Ownership=$295.08, ScheduleLen=208
- Test 3 (Weekly term months): Payment=$135.18, Financed=$35,652.50, Interest=$6,522.54, TotalCost=$42,175.04, OTD=$40,552.50, Ownership=$111.19, ScheduleLen=312
- Test 4 (No insurance): Payment=$666.61, Financed=$47,400.00, Interest=$8,595.40, TotalCost=$55,995.40, OTD=$58,950.00, Ownership=$666.61, ScheduleLen=84
- Test 5 (High tax): Payment=$321.06, Financed=$64,660.00, Interest=$35,511.50, TotalCost=$100,171.50, OTD=$88,510.00, Ownership=$278.18, ScheduleLen=312
- Test 6 (Trade payoff greater): Payment=$483.83, Financed=$40,300.00, Interest=$11,953.81, TotalCost=$52,253.81, OTD=$44,300.00, Ownership=$583.83, ScheduleLen=108
- Test 7 (Zero APR): Payment=$425.67, Financed=$25,540.00, Interest=$0.00, TotalCost=$25,540.00, OTD=$31,590.00, Ownership=$485.67, ScheduleLen=60
- Test 8 (Large down payment): Payment=$114.26, Financed=$28,100.00, Interest=$7,548.00, TotalCost=$35,648.00, OTD=$96,650.00, Ownership=$226.37, ScheduleLen=312
- Test 9 (Short term biweekly): Payment=$265.21, Financed=$24,735.00, Interest=$2,846.61, TotalCost=$27,581.61, OTD=$26,305.00, Ownership=$212.40, ScheduleLen=104
- Test 10 (Zero trade): Payment=$512.07, Financed=$44,596.00, Interest=$16,852.35, TotalCost=$61,448.35, OTD=$50,896.00, Ownership=$622.07, ScheduleLen=120
- Parity: The new update mirrors the legacy compute behavior with identical rounding for these vectors.
- Console error check: Not run (CLI environment lacks a browser console).

# Deviations
- None.
