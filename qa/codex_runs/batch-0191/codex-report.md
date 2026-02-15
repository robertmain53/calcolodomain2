CHANGELOG
- sito_modificato/bowling-score.html
  - Rebuilt the page using the mortgage-payment canonical layout while preserving the bowling calculator narrative, glossary, FAQ, and audit details.
  - Added structured hero inputs/results plus canonical meta, footer, and validation script that mirrors the original sum-of-frames behavior with safer parsing and deterministic formatting.

TEST REPORT
- Parity statement: The new calculator still sums the ten frame entries exactly like the legacy script, so monthly outputs remain unchanged.
- Test vectors:
  1. frames=[0,0,0,0,0,0,0,0,0,0] → total=0, average=0.0, shortfall=300
  2. frames=[10,10,10,10,10,10,10,10,10,10] → total=100, average=10.0, shortfall=200
  3. frames=[30,30,30,30,30,30,30,30,30,30] → total=300, average=30.0, shortfall=0
  4. frames=[9,8,7,6,5,4,3,2,1,0] → total=45, average=4.5, shortfall=255
  5. frames=[15,15,15,15,15,15,15,15,15,15] → total=150, average=15.0, shortfall=150
  6. frames=[12,9,7,10,14,8,6,5,11,13] → total=95, average=9.5, shortfall=205
  7. frames=[0,30,0,30,0,30,0,30,0,30] → total=150, average=15.0, shortfall=150
  8. frames=[25,20,25,20,25,20,25,20,25,30] → total=235, average=23.5, shortfall=65
  9. frames=[1,2,3,4,5,6,7,8,9,10] → total=55, average=5.5, shortfall=245
 10. frames=[29,29,29,29,29,29,29,29,29,29] → total=290, average=29.0, shortfall=10
- Console error check: Not run (browser console unavailable in this environment, please verify manually after deployment).
- Deviations: None noted; all content was migrated to canonical structure without dropping any original narrative.
