CHANGELOG
- sito_modificato/btu-to-calories.html: Rebuilt the page on the canonical mortgage-payment layout, centralized hero inputs/results, preserved every informational block (expanded guide, tables, audit notes), and replaced the legacy tabbed JS with the mandated parse/validate/compute/update contract while keeping citations/changelog/formulas intact.

TEST REPORT
- Vector 1: BTU → cal, 1 BTU (IT) to cal (thermochemical) → 252.164401 cal, 1055.0559 J.
- Vector 2: BTU → cal, 2 BTU (thermochemical) to cal (IT) → 503.654469 cal, 2108.7005 J.
- Vector 3: BTU → cal, 5 BTU (mean) to kcal (nutritional) → 1.261795 kcal, 5279.35 J.
- Vector 4: BTU → cal, 10 BTU (IT) to cal (15°C) → 2520.7403 cal, 10550.5585 J.
- Vector 5: cal → BTU, 100 cal (thermochemical) to BTU (IT) → 0.396567 BTU, 418.4 J.
- Vector 6: cal → BTU, 250 cal (IT) to BTU (thermochemical) → 0.992744 BTU, 1046.7 J.
- Vector 7: cal → BTU, 0.252164 kcal to BTU (mean) → 0.999227 BTU, 1055.0542 J.
- Vector 8: cal → BTU, 418.4 cal (thermochemical) to BTU (IT) → 1.659235 BTU, 1750.5856 J.
- Vector 9: Table row, 1 BTU (IT) → 0.252164 kcal, 252.164 cal.
- Vector 10: Table row, 2 BTU (IT) → 0.504329 kcal, 504.329 cal.
- Vector 11: Table row, 5 BTU (IT) → 1.260822 kcal, 1260.822 cal.
- Vector 12: Table row, 10 BTU (IT) → 2.521644 kcal, 2521.644 cal.
- Parity: All outputs match the legacy page's numeric behavior and rounding rules; values were recomputed with the canonical factors and formatting pipeline before and after refactor.
- Console: None observed during interaction (no runtime errors from the new script).
- Deviations: None.
