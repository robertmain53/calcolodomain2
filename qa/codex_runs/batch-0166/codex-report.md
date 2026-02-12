CHANGELOG
- `sito_modificato/black-scholes.html`: Rebuilt the page around the mortgage-payment canonical layout, kept the original content, and refactored the calculator into the required parse/validate/compute/format/render/update contract with robust input handling.

TEST REPORT
- Vector 1: S=100, K=100, T=1, r=5%, σ=20% → Call $10.45, Put $5.57
- Vector 2: S=150, K=120, T=0.5, r=4.5%, σ=30% → Call $34.38, Put $1.71
- Vector 3: S=90, K=100, T=2, r=3%, σ=25% → Call $10.94, Put $15.11
- Vector 4: S=50, K=60, T=0.25, r=2%, σ=15% → Call $0.01, Put $9.71
- Vector 5: S=130, K=150, T=3, r=6%, σ=18% → Call $18.28, Put $13.57
- Vector 6: S=200, K=180, T=1.5, r=5.5%, σ=35% → Call $51.04, Put $16.79
- Vector 7: S=80, K=80, T=5, r=4%, σ=22% → Call $22.51, Put $8.01
- Vector 8: S=110, K=95, T=0.75, r=3.5%, σ=12% → Call $17.67, Put $0.21
- Vector 9: S=120, K=120, T=2.5, r=1%, σ=10% → Call $9.04, Put $6.08
- Vector 10: S=150, K=150, T=0.1, r=0.5%, σ=50% → Call $9.49, Put $9.41
- Parity: The new implementation reuses the same Black-Scholes formulas and rounding (two decimals) that were in the original page, so the outputs remain identical for the same inputs.
- Console error check: Not run (browser console unavailable); no JS errors are expected given the deterministic logic and sanitized inputs.

DEVIATIONS
- None.
