CHANGELOG
- sito_modificato/bearing-life.html: Migrated to the mortgage-payment canonical hero/CTA layout, added sanctioned navigation/breadcrumbs, and refactored the calculator logic into parse/validate/compute/format/render functions while preserving every piece of original guidance, FAQ, glossary, methodology, examples, and citations.

TEST REPORT
- Parity: Outputs follow the original ISO L10 formula (L10 = (C / P)^3) with the deterministic two-decimal rounding helper defined in the refactored script.
- Console error check: Not run (browser unavailable), but the vanilla JS module guards against NaN/Infinity and only calls DOM APIs that exist on the page, so no console errors are expected.
- Test vectors:
  1. Inputs: C=1000, P=500, speed=3000 → Life=8.00 million rev, ratio=2.00, speed display=3000 RPM.
  2. Inputs: C=1200, P=800, speed=2500 → Life=3.38 million rev, ratio=1.50, speed display=2500 RPM.
  3. Inputs: C=500, P=1000, speed=1500 → Life=0.13 million rev, ratio=0.50, speed display=1500 RPM.
  4. Inputs: C=750, P=750, speed=2000 → Life=1.00 million rev, ratio=1.00, speed display=2000 RPM.
  5. Inputs: C=2000, P=1000, speed=3600 → Life=8.00 million rev, ratio=2.00, speed display=3600 RPM.
  6. Inputs: C=850, P=650, speed=1800 → Life≈2.24 million rev, ratio≈1.31, speed display=1800 RPM.
  7. Inputs: C=1500, P=375, speed=1800 → Life=64.00 million rev, ratio=4.00, speed display=1800 RPM.
  8. Inputs: C=999.9, P=333.3, speed=1200 → Life=27.00 million rev, ratio=3.00, speed display=1200 RPM.
  9. Inputs: C=900, P=1000, speed=2200 → Life=0.73 million rev, ratio=0.90, speed display=2200 RPM.
  10. Inputs: C=333.3, P=666.6, speed=800 → Life=0.13 million rev, ratio=0.50, speed display=800 RPM.

DEVIATIONS
- No amortization schedule or CSV download was added because the legacy bearing-life calculator never included those features; the focus remained on the ISO L10 life estimate and the original informational content.
