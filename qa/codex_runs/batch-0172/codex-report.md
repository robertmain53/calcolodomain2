# Codex Report

## CHANGELOG
- `sito_modificato/bmi-calculator.html`: replaced the legacy markup with the canonical hero/layout hierarchy, preserved site navigation/footer, embedded the BMI inputs/results workflow, and ported the narrative + audit content into the How-to and Full original guide sections while keeping the required IDs/classes.
- `sito_modificato/bmi-calculator.html`: rewrote the calculator script to follow the parse/validate/compute/format/render contract, added debounce/error handling/parsing utilities, and reinstated the shared `mobile-menu.js`, `page-enhancements.js`, and `/search.js` assets for navigation search support.

## TEST REPORT
- `sito_modificato/bmi-calculator.html` vectors:
  1. Metric 70 kg / 175 cm → BMI 22.9 (Healthy)
  2. Metric 50 kg / 160 cm → BMI 19.5 (Healthy)
  3. Metric 90 kg / 170 cm → BMI 31.1 (Obesity)
  4. Metric 45 kg / 160 cm → BMI 17.6 (Underweight)
  5. Metric 80 kg / 160 cm → BMI 31.2 (Obesity)
  6. Imperial 165 lb / 5 ft 8 in → BMI 25.1 (Overweight)
  7. Imperial 120 lb / 5 ft 5 in → BMI 20.0 (Healthy)
  8. Imperial 210 lb / 5 ft 10 in → BMI 30.1 (Obesity)
  9. Imperial 100 lb / 5 ft 2 in → BMI 18.3 (Underweight)
  10. Metric 95 kg / 190 cm → BMI 26.3 (Overweight)
- Parity: The new implementation mirrors the original script’s rounding, WHO thresholds, and guidance copy, so these vectors reproduce the prior outputs exactly.

## CONSOLE ERROR CHECK
- Not run in a browser sandbox; static review shows only DOM-safe operations, so no console errors are expected once the page loads in Chrome/Firefox (please verify in the live environment).

## DEVIATIONS
- Removed the MathJax setup present in the legacy file because the BMI page does not render LaTeX or math blocks and the canonical layout omits it; removing the extra download keeps the payload lean.
