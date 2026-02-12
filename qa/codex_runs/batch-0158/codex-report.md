# Batch 0158 Report

## CHANGELOG
- `sito_modificato/binomial-option-pricing.html`: Rebuilt the page using the mortgage-payment hero/footer contract, migrated glossary/FAQ content into the methodology section, added verification/meta details, and replaced the legacy script with parse/validate/compute/format/render/update plumbing while preserving the original discounted-price formula.

## TEST REPORT
- Vector 1: Underlying=100, Strike=100, Volatility=20, Risk-Free=5%, Time=1yr → Option Price = 95.12
- Vector 2: Underlying=150, Strike=120, Volatility=30, Risk-Free=3.5%, Time=2yr → Option Price = 139.86
- Vector 3: Underlying=50, Strike=45, Volatility=25, Risk-Free=0%, Time=0.5yr → Option Price = 50.00
- Vector 4: Underlying=200, Strike=220, Volatility=18, Risk-Free=7.25%, Time=5yr → Option Price = 139.19
- Vector 5: Underlying=80, Strike=75, Volatility=40, Risk-Free=1.25%, Time=0.25yr → Option Price = 79.75
- Vector 6: Underlying=123.45, Strike=130, Volatility=22, Risk-Free=4.5%, Time=3yr → Option Price = 107.86
- Vector 7: Underlying=250, Strike=240, Volatility=12, Risk-Free=6%, Time=10yr → Option Price = 137.20
- Vector 8: Underlying=99.99, Strike=100, Volatility=15, Risk-Free=2.2%, Time=4yr → Option Price = 91.57
- Vector 9: Underlying=10, Strike=12, Volatility=60, Risk-Free=10%, Time=0.1yr → Option Price = 9.90
- Vector 10: Underlying=500, Strike=480, Volatility=35, Risk-Free=8.75%, Time=0.75yr → Option Price = 468.24
- Parity: The inline calculator still uses `underlying × exp(-r × t)` as in the legacy script, so numeric outputs remain unchanged for these slices despite the richer UI.
- Console errors: None observed (script validated in Node and relies on browsers for the DOM-managed interactions; no runtime console was available in this environment).

## Deviations
- None.
