# CHANGELOG
- `sito_modificato/belt-drive-design.html`: Rebuilt the page to match the mortgage-payment canonical layout, reintroduced the belt-drive content (how-to guidance, glossary, FAQ, sources, changelog) and implemented a new input/result hero that maintains the original tension echo behavior plus a schedule toggle/CSV download.

# TEST REPORT
- `sito_modificato/belt-drive-design.html`:
  1. Pulley 150 mm, Belt 2400 mm, Tension "800" → Output "800 N" (6 segments)
  2. Pulley 120.25 mm, Belt 1999.5 mm, Tension "123.456" → Output "123.456 N" (6 segments)
  3. Pulley 75 mm, Belt 1800 mm, Tension "250.00" → Output "250.00 N" (6 segments)
  4. Pulley 250 mm, Belt 3600 mm, Tension "1e3" → Output "1e3 N" (6 segments)
  5. Pulley 12 mm, Belt 600 mm, Tension "15.5" → Output "15.5 N" (6 segments)
  6. Pulley 200 mm, Belt 4000 mm, Tension "0.75" → Output "0.75 N" (6 segments)
  7. Pulley 320.1 mm, Belt 5000 mm, Tension "999.99" → Output "999.99 N" (6 segments)
  8. Pulley 64 mm, Belt 0.05 mm, Tension "0.1" → Output "0.1 N" (6 segments)
  9. Pulley 400 mm, Belt 8000 mm, Tension "1000.000" → Output "1000.000 N" (6 segments)
  10. Pulley 88 mm, Belt 2333 mm, Tension "300.3" → Output "300.3 N" (6 segments)
- Parity: All vectors echo the tension input (including formatting) to match the legacy placeholder behavior.
- Console: No runtime errors were introduced; the logic is a pure DOM/JS implementation that ran without issues in the Node-based regression script and has no console output.
- Deviations: None.
