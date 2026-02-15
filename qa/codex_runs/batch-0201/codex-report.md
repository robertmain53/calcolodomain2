# Batch 0201 Report

## CHANGELOG
- `sito_modificato/bridge-load-rating.html`: Rebuilt the bridge load rating page on the mortgage-payment canonical layout while keeping all original guidance, adding a structured calculator flow, schedule table, and metadata section consistent with CalcDomain standards.

## TEST REPORT
- Parity: Every vector matches the legacy formula `(spanLength × loadDistributionFactor) / safetyFactor`, rounded consistently to two decimal places.
- Console: Node-based compute verification used for the vectors produced no runtime errors (browser console not available in this environment).
- Test vectors:
  1. span=30, dist=2.5, safety=1.5 → 50.00 tons
  2. span=20, dist=3, safety=1.5 → 40.00 tons
  3. span=50, dist=1.8, safety=1.5 → 60.00 tons
  4. span=34.2, dist=2.1, safety=1.5 → 47.88 tons
  5. span=100, dist=4.2, safety=2 → 210.00 tons
  6. span=12.75, dist=3.4, safety=1.25 → 34.68 tons
  7. span=60, dist=1.2, safety=1.8 → 40.00 tons
  8. span=45, dist=2.75, safety=1.75 → 70.71 tons
  9. span=27.5, dist=3.1, safety=1.6 → 53.28 tons
  10. span=88.4, dist=2.05, safety=1.4 → 129.44 tons
  11. span=15.3, dist=2.4, safety=1.2 → 30.60 tons

## Deviations
- None.
