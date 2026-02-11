CHANGELOG
- `sito_modificato/basic-arithmetic.html`: rebuilt the entire page around the mortgage-payment canonical hero+layout while preserving the calculator behavior, explanatory prose, and metadata entries.
- `sito_modificato/basic-arithmetic.html`: reimplemented the arithmetic engine with parse/validate/compute/format/render/update helpers, added tab handling, and carried over formula/citation/changelog content.

TEST REPORT
- 1. Addition 7 + 3 → expected 10, actual 10 (PASS)
- 2. Add with negative second → expected 3, actual 3 (PASS)
- 3. Subtraction decimals (5.5 − 2) → expected 3.5, actual 3.5 (PASS)
- 4. Multiplication decimal (1.5 × 2) → expected 3, actual 3 (PASS)
- 5. Division simple (21 ÷ 3) → expected 7, actual 7 (PASS)
- 6. Division negative (−12 ÷ 4) → expected −3, actual −3 (PASS)
- 7. Zero result (0 + 0) → expected 0, actual 0 (PASS)
- 8. Expression 7 + 3 × 2 → expected 13, actual 13 (PASS)
- 9. Expression 2.5 × (1 + 3) → expected 10, actual 10 (PASS)
- 10. Expression (−3) + 5 ÷ 2 → expected −0.5, actual −0.5 (PASS)
- 11. Expression (4 + 2) × (3 − 1) ÷ 2 → expected 6, actual 6 (PASS)
- 12. Expression 1/3 → expected 0.333333333333, actual 0.333333333333 (PASS)
- Parity: outputs now continue to match the legacy calculator's rounding/formatting for each vector after reorganizing the UX.
- Console errors: not checked (no headless browser available in this context).

DEVIATIONS
- None.
