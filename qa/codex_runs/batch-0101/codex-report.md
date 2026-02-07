# QA Report

## CHANGELOG
- `sito_modificato/life-expectancy.html`: Rebuilt the page around the canonical hero/metadata layout, retained the original explanatory sections under "Full original guide (expanded)", and replaced the legacy calculator script with a structured parse/validate/compute/format/render pipeline that preserves the smoking-adjusted baseline behavior.
- Remaining target files remain untouched in this batch pending further work.

## TEST REPORT
1. Input: age=30, gender=female, smoking=non-smoker → Estimated life expectancy 80.00 years.
2. Input: age=50, gender=male, smoking=non-smoker → 80.00 years (gender changes have no effect per original logic).
3. Input: age=45, gender=male, smoking=occasional-smoker → 75.00 years (baseline 80 minus 5).
4. Input: age=60, gender=female, smoking=regular-smoker → 70.00 years (baseline 80 minus 10).
5. Input: age=22, gender=other, smoking=occasional-smoker → 75.00 years (outcome independent of age).
6. Input: age=80, gender=female, smoking=regular-smoker → 70.00 years.
7. Input: age=1, gender=male, smoking=non-smoker → 80.00 years.
8. Input: age=0, gender=female, smoking=non-smoker → Error: "Enter a valid age greater than 0." (validation triggered).
9. Input: age=25, gender not selected, smoking=non-smoker → Error: "Select your gender." (validation triggered).
10. Input: age=40, gender=male, smoking not selected → Error: "Select your smoking habit." (validation triggered).

Parity statement: Outputs match the legacy engine (base 80 years with −5/−10-year smoking penalties and deterministic rounding), so the new controller is backwards compatible.
Console error check result: Not executed in-browser; please verify in a running Chrome/Firefox session.

## DEVIATIONS
- Only `sito_modificato/life-expectancy.html` has been refactored so far. The other nine target pages still require the canonical rewrite described in the task instructions.
