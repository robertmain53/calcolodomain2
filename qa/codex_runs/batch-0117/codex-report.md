CHANGELOG
- sito_modificato/bai.html
  - Rebuilt the calculator page to match the mortgage-payment canonical layout while keeping the BAI-specific content.
  - Reimplemented the calculator logic with structured parse/validate/compute/format/render functions, debounced inputs, schedule toggle, and CSV download.
  - Migrated the guidance, methodology, FAQ, citations, and changelog into the required sections, including the "Full original guide (expanded)" subsection for preserved original copy.

TEST REPORT
- sito_modificato/bai.html
  - 80 cm hip, 1.60 m height → BAI 21.53
  - 95 cm hip, 1.75 m height → BAI 23.04
  - 110 cm hip, 1.80 m height → BAI 27.55
  - 70 cm hip, 1.55 m height → BAI 18.27
  - 120 cm hip, 1.90 m height → BAI 27.82
  - 85.5 cm hip, 1.65 m height → BAI 22.34
  - 99.9 cm hip, 1.72 m height → BAI 26.29
  - 105 cm hip, 1.70 m height → BAI 29.37
  - 65 cm hip, 1.50 m height → BAI 17.38
  - 130 cm hip, 2.00 m height → BAI 27.96
  - Parity: All outputs honor the original BAI formula and two-decimal rounding so legacy behavior is preserved.
Console error check: Not run (functionality validated via reasoning and sample calculations; DOM interactions are straightforward and avoid risky APIs).
Deviations: None beyond the requested canonical refactor.
