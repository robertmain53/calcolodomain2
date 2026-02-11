CHANGELOG
- sito_modificato/awg-to-mm.html: Rebuilt around the mortgage-payment hero/metadata structure, moved AWG-specific guidance into the methodology/how-to and “Full original guide (expanded)” areas, kept all original tables, citations, and changelog notes, and replaced the converter script with the mandated parse/validate/compute/format/render/update flow while preserving rounding and numeric behavior.

TEST REPORT
- Test vectors (rounded values follow the canonical rounding strategy; no browser console available so these are deduced from the new JS logic):
  1. AWG 0 → Diameter 8.2515 mm, Area 53.4751 mm²
  2. AWG 12 → Diameter 2.0525 mm, Area 3.3088 mm²
  3. AWG 20 → Diameter 0.8118 mm, Area 0.5176 mm²
  4. AWG -3 (4/0) → Diameter 11.6840 mm, Area 107.2193 mm²
  5. AWG 40 → Diameter 0.0799 mm, Area 0.0050 mm²
  6. 2.053 mm → AWG 12.00, Area 3.3103 mm²
  7. 0.5 mm → AWG 24.18, Area 0.1963 mm²
  8. 6.0 mm → AWG 2.75, Area 28.2743 mm²
  9. 3.31 mm² → Diameter 2.0529 mm, AWG 12.00
 10. 10.0 mm² → Diameter 3.5682 mm, AWG 7.23
- Parity: Outputs follow the original AWG conversion formulas (same constants and rounding strategy) so results stay consistent with the legacy implementation.
- Console errors: Not run (browser console unavailable in this CLI environment).

Deviations
- None.
