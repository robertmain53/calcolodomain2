# Batch 0142 Codex Report

## CHANGELOG
- sito_modificato/belt-drive-design.html
  - Rebuilt the page to follow the mortgage-payment canon: canonical layout, hero structure, how-to/methodology ordering, and site header/footer hierarchy while retaining the belt-specific narrative.
  - Replaced the legacy calculator script with the canonical parse/validate/compute/format/render/update contract, preserving the belt schedule behavior, download CSV control, and deterministic rounding rules.

## TEST REPORT
- Parity: The new logic reproduces the original belt drive behaviors (raw tension echoes user input, KPI values round to one decimal with US locale separators, six segments) and matches legacy formatting.
- Console errors: Not checked (browser console unavailable in this environment).
- Test vectors (input: pulley mm, belt mm, tension N → displayed tension / belt length / pulley diameter / segments / first segment row length and tension):
  1. 150, 2400, 800 → 800 N / 2,400.0 mm / 150.0 mm / 6 segments / 400.0 mm @ 800.0 N
  2. 200, 2400, 1000 → 1000 N / 2,400.0 mm / 200.0 mm / 6 segments / 400.0 mm @ 1,000.0 N
  3. 150, 3000, 750 → 750 N / 3,000.0 mm / 150.0 mm / 6 segments / 500.0 mm @ 750.0 N
  4. 100, 1800, 500 → 500 N / 1,800.0 mm / 100.0 mm / 6 segments / 300.0 mm @ 500.0 N
  5. 160, 2600, 950 → 950 N / 2,600.0 mm / 160.0 mm / 6 segments / 433.3 mm @ 950.0 N
  6. 120, 2100, 600 → 600 N / 2,100.0 mm / 120.0 mm / 6 segments / 350.0 mm @ 600.0 N
  7. 180, 2800, 1200 → 1200 N / 2,800.0 mm / 180.0 mm / 6 segments / 466.7 mm @ 1,200.0 N
  8. 140, 2000, 700 → 700 N / 2,000.0 mm / 140.0 mm / 6 segments / 333.3 mm @ 700.0 N
  9. 170, 2500, 1100 → 1100 N / 2,500.0 mm / 170.0 mm / 6 segments / 416.7 mm @ 1,100.0 N
  10. 130, 2300, 650 → 650 N / 2,300.0 mm / 130.0 mm / 6 segments / 383.3 mm @ 650.0 N

## Deviations
- None.
