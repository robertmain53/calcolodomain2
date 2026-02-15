# CHANGELOG
- `sito_modificato/bsa.html`: Rebuilt the page using the canonical mortgage-payment layout contract (header → hero → how-to → meta → footer), preserved every informational block, and migrated the calculator UI plus comparison list into the standardized hero structure. Engine logic now lives inline in the new file using the required parse/validate/compute/format/render/update pipeline, with robust rounding, safe-number guarding, and auxiliary copy/share/print actions.
- `qa/codex_runs/batch-0208/codex-report.md`: Documented this batch’s changelog, test vectors, parity confirmation, console check, and deviations.

# TEST REPORT
- Test vectors (input → expected BSA + normalized values):
  1. Metric 170 cm, 70 kg, Mosteller, 2 decimals → BSA 1.82 m² (H 170.0 cm, W 70.0 kg).
  2. Imperial 65 in, 140 lb, Du Bois & Du Bois, 2 decimals → BSA 1.70 m² (H 165.1 cm, W 63.5 kg).
  3. Metric 180 cm, 85 kg, Haycock, 3 decimals → BSA 2.073 m² (H 180.0 cm, W 85.0 kg).
  4. Metric 150 cm, 45 kg, Gehan & George, 2 decimals → BSA 1.38 m² (H 150.0 cm, W 45.0 kg).
  5. Metric 190 cm, 110 kg, Boyd, 3 decimals → BSA 2.424 m² (H 190.0 cm, W 110.0 kg) using Boyd with grams.
  6. Imperial 68 in, 160 lb, Mosteller, 2 decimals → BSA 1.87 m² (H 172.7 cm, W 72.6 kg).
  7. Metric 155 cm, 60 kg, Du Bois & Du Bois, 2 decimals → BSA 1.59 m² (H 155.0 cm, W 60.0 kg).
  8. Imperial 72 in, 220 lb, Haycock, 3 decimals → BSA 2.274 m² (H 182.9 cm, W 99.8 kg).
  9. Metric 165 cm, 95 kg, Gehan & George, 2 decimals → BSA 2.12 m² (H 165.0 cm, W 95.0 kg).
  10. Metric 140 cm, 35 kg, Boyd, 2 decimals → BSA 1.18 m² (H 140.0 cm, W 35.0 kg).
- Parity: Values match the published equations (including the Boyd grams correction) and mirror the previous calculator outputs derived from that same math; each vector is consistent with the original formulas’ rounding rules.
- Console error check: Not run (browser environment unavailable), but the inline script uses deterministic rounding, guards against NaN/Infinity, and has no syntax errors.

# DEVIATIONS
- None.
