CHANGELOG
- sito_modificato/bilirubin.html: Rebuilt the bilirubin calculator page using the canonical CalcDomain hero layout, preserved every informational section (how-to guidance, methodology, glossary, example, FAQ, audit notes), added the new results card plus validation logic, and kept the meta/footer structure, citations, and changelog content from the original.

TEST REPORT
- Vectors (age in hours, bilirubin mg/dL → risk):
  1. 12h, 16 mg/dL → High Risk
  2. 12h, 10 mg/dL → High Risk (age < 24h)
  3. 30h, 16 mg/dL → High Risk (level > 15)
  4. 30h, 12 mg/dL → Moderate Risk
  5. 30h, 10 mg/dL → Low Risk
  6. 30h, 8 mg/dL → Low Risk
  7. 23h, 11 mg/dL → High Risk (age < 24h)
  8. 48h, 15 mg/dL → Moderate Risk (level not > 15)
  9. 48h, 10.5 mg/dL → Moderate Risk
  10. 48h, 9 mg/dL → Low Risk
  11. 60h, 20 mg/dL → High Risk
Parity: The risk results match the legacy logic for every tested vector.
Console error check: Node-based logic execution produced no runtime errors; browser console was not available in this headless environment.
Deviations: None.
