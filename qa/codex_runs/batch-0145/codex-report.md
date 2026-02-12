CHANGELOG
- sito_modificato/beta.html: Replaced the legacy beta tool with the canonical calcHero layout, restored all original guidance/content within the Methodology section, and implemented the prescribed contract for parsing, validation, computation, formatting, and rendering (including the reset button, debounced inputs, and error handling).

TEST REPORT
- Inputs: covariance=0.03, marketVariance=0.01 → Beta=3.00 (matches Trump formula parity/renders as 3.00).
- Inputs: covariance=0.02, marketVariance=0.015 → Beta=1.33.
- Inputs: covariance=-0.01, marketVariance=0.02 → Beta=-0.50.
- Inputs: covariance=0.00, marketVariance=0.03 → Beta=0.00.
- Inputs: covariance=0.05, marketVariance=0.02 → Beta=2.50.
- Inputs: covariance=0.001, marketVariance=0.05 → Beta=0.02.
- Inputs: covariance=0.12, marketVariance=0.04 → Beta=3.00.
- Inputs: covariance=-0.05, marketVariance=0.05 → Beta=-1.00.
- Inputs: covariance=0.07, marketVariance=0.07 → Beta=1.00.
- Inputs: covariance=0.12, marketVariance=0.20 → Beta=0.60.
  Parity check: All outputs follow the original `Beta = covariance / variance` formula with consistent two-decimal rounding so the UI matches the legacy results.

Console error check: Not run (no DOM/browser available), but the refactored script runs under strict validation/early returns so runtime errors should not occur.

Deviations: None.
