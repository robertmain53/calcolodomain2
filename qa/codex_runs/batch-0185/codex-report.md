# Batch 0185 report

## CHANGELOG
- sito_modificato/bolt-torque.html: Rebuilt the page to match the mortgage-payment canonical layout, moved all legacy reference content into the new How-to section, preserved FAQ/chart/related-links, and replaced the calculator logic with the mandated parse/validate/compute/format/render/update contract.

## TEST REPORT
- Vector 1: metric M6, grade metric_88, dry lubrication, 75% preload → 10.5 Nm | 7.7 ft-lb | 93 in-lb | 8.74 kN
- Vector 2: metric M10, grade metric_129, lubed, 75% preload → 63.3 Nm | 46.7 ft-lb | 560 in-lb | 42.20 kN
- Vector 3: imperial 1/4"-20, grade imperial_5, dry, 70% preload → 10.7 Nm | 7.9 ft-lb | 95 in-lb | 8.42 kN
- Vector 4: imperial 1/2"-13, grade imperial_8, lubed, 80% preload → 115.4 Nm | 85.1 ft-lb | 1022 in-lb | 60.60 kN
- Vector 5: metric M16, grade metric_109, dry, 60% preload → 250.2 Nm | 184.5 ft-lb | 2214 in-lb | 78.19 kN
- Vector 6: imperial 3/8"-16, grade imperial_5, lubed, 65% preload → 27.2 Nm | 20.1 ft-lb | 241 in-lb | 19.05 kN
- Vector 7: metric M24, grade metric_129, dry, 90% preload → 1479.2 Nm | 1091.0 ft-lb | 13092 in-lb | 308.17 kN
- Vector 8: imperial 5/8"-11, grade imperial_8, dry, 50% preload → 191.5 Nm | 141.2 ft-lb | 1695 in-lb | 60.32 kN
- Vector 9: metric M12, grade metric_88, lubed, 55% preload → 48.4 Nm | 35.7 ft-lb | 428 in-lb | 26.89 kN
- Vector 10: imperial 3/4"-10, grade imperial_8, lubed, 90% preload → 458.5 Nm | 338.2 ft-lb | 4058 in-lb | 160.46 kN
- Parity: Manual vectors follow the original calculation routine and rounding rules so outputs remain consistent with legacy behavior.
- Console error check: Not run (interactive browser not available in this environment); static review found no glaring runtime issues.

## Deviations
- Console/DOM error checking was not executed because the sandbox lacks a browser environment (listed under TEST REPORT above).
