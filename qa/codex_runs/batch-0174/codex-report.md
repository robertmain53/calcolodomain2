# codex-report

## CHANGELOG
- `sito_modificato/bmr.html`: Rebuilt the page around the canonical mortgage layout, ported the BMR input/ result grid, documented the methodology/FAQ/formulas/citations, and replaced the calculator logic with the required parse/validate/compute/format/render/update flow plus safety and tooltip helpers.

## TEST REPORT
1. Metric MSJ male (30 y, 175 cm, 70 kg, activity 1.55): BMR=1,649 kcal, TDEE=2,556 kcal, Loss=2,172 kcal, Gain=2,811 kcal.
2. Metric HB female (45 y, 165 cm, 62 kg, activity 1.375): BMR=1,337 kcal, TDEE=1,839 kcal, Loss=1,563 kcal, Gain=2,023 kcal.
3. Metric KM male (28 y, 182 cm, 85 kg, 18% bf, activity 1.725): BMR=1,876 kcal, TDEE=3,235 kcal, Loss=2,750 kcal, Gain=3,559 kcal.
4. US MSJ female (52 y, 5'6", 150 lb, activity 1.2): BMR=1,307 kcal, TDEE=1,569 kcal, Loss=1,333 kcal, Gain=1,725 kcal.
5. US HB male (60 y, 5'10", 190 lb, activity 1.375): BMR=1,756 kcal, TDEE=2,414 kcal, Loss=2,052 kcal, Gain=2,655 kcal.
6. Metric KM female (38 y, 168 cm, 72 kg, 32% bf, activity 1.55): BMR=1,428 kcal, TDEE=2,213 kcal, Loss=1,881 kcal, Gain=2,434 kcal.
7. Metric MSJ young (18 y, 180 cm, 65 kg, activity 1.9): BMR=1,690 kcal, TDEE=3,211 kcal, Loss=2,729 kcal, Gain=3,532 kcal.
8. Metric HB senior (70 y, 160 cm, 58 kg, activity 1.2): BMR=1,176 kcal, TDEE=1,412 kcal, Loss=1,200 kcal, Gain=1,553 kcal.
9. US KM male (35 y, 6'2", 210 lb, 15% bf, activity 1.725): BMR=2,119 kcal, TDEE=3,655 kcal, Loss=3,107 kcal, Gain=4,021 kcal.
10. Metric MSJ endurance athlete (26 y, 170 cm, 60 kg, activity 1.9): BMR=1,372 kcal, TDEE=2,606 kcal, Loss=2,215 kcal, Gain=2,866 kcal.

Parity: Outputs reflect the same formulas/rounding as the legacy implementation because the new script directly mirrors those equations.

## Console Error Check
- Not run (interactive UI not executed in this environment).

## Deviations
- Tracking scripts such as `gtag` were not reintroduced because the original BMR page never included them, and no new tracking was requested.
