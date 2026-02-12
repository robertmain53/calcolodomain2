CHANGELOG
- sito_modificato/beaufort-scale.html
  - Rebuilt the page around the canonical mortgage-hero hierarchy (header, breadcrumbs, calc hero with two cards, toggleable schedule table, how-to/methodology content, and meta footer) while preserving the original site metadata.
  - Replaced the legacy script with the mandated parse/validate/compute/format/render/update pipeline, added a schedule toggle + CSV download controls, and ensured the calculator never renders NaN/Infinity.
  - Relocated guidance, formulas, sources, and supplemental notes/links under the How to Use card and meta details while keeping every piece of original content (extra material labeled "Full original guide (expanded)").

TEST REPORT
- sito_modificato/beaufort-scale.html
  - 0 kmh -> B0 (Calm), range 0.0 – 1.0 km/h, normalized km/h 0.0, normalized m/s 0.0
  - 0.3 mps -> B1 (Light air), range 0.3 – 1.4 m/s, normalized km/h 1.1, normalized m/s 0.3
  - 10 kmh -> B2 (Light breeze), range 6.0 – 11.0 km/h, normalized km/h 10.0, normalized m/s 2.8
  - 25 mph -> B6 (Strong breeze), range 24.2 – 30.4 mph, normalized km/h 40.2, normalized m/s 11.2
  - 30 kn -> B7 (Near gale), range 27.0 – 32.9 knots, normalized km/h 55.6, normalized m/s 15.4
  - 50 mph -> B9 (Strong gale), range 46.6 – 54.7 mph, normalized km/h 80.5, normalized m/s 22.4
  - 70 kmh -> B8 (Gale), range 62.0 – 74.0 km/h, normalized km/h 70.0, normalized m/s 19.4
  - 100 kmh -> B10 (Storm), range 89.0 – 102.0 km/h, normalized km/h 100.0, normalized m/s 27.8
  - 150 kmh -> B12 (Hurricane), range 118.0+ km/h, normalized km/h 150.0, normalized m/s 41.7
  - 80 kn -> B12 (Hurricane), range 63.7+ knots, normalized km/h 148.2, normalized m/s 41.2
  - Parity: all outputs (Beaufort, description, range, normalized km/h/m/s) match the legacy compute logic with the same rounding strategy.
  - Console error check: Not run (page not loaded in a browser; static analysis only).

Deviations: None.
