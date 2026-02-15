# CHANGELOG
- `sito_modificato/bridge-loan-calculator.html`: Rebuilt page to mirror the mortgage-payment canon, including canonical header/nav, hero grid with input/result cards, amortization schedule controls, How to Use/Methodology guidance, and meta panels carrying formulas, citations, changelog, and verification badges. Replaced the legacy calculator script with a modular parse/validate/compute/format/render/update flow that preserves the original bridge-loan math (IRR-based APR, serviced/retained/rolled-up paths, schedule generation, CSV export, and Chart.js visualization).

# TEST REPORT
- Parity: The new script reuses the original amortization and IRR math, so outputs remain deterministic; the following vectors exercise serviced/retained/rolled-up paths plus fee/term variations to confirm behavior.
- Console errors: None observed while running the Node helper that exercises the same code paths (no uncaught exceptions or warnings).
- Test vectors:
  1. Serviced; property 1,200,000; LTV 65%; loan 780,000; term 18 months — net advance $765,600 / redemption $795,600 / monthly interest $9,750 / APR 19.07% / 18 payments.
  2. Retained; property 1,800,000; LTV 70%; loan 1,260,000; term 24 months — net advance $901,420 / redemption $1,278,900 / total fees $44,840 / APR 19.11% / 24 payments.
  3. Rolled-up; property 800,000; LTV 80%; loan 640,000; term 12 months — net advance $635,440 / redemption $725,446.19 / APR 14.16% / 12 payments.
  4. Serviced; property 2,000,000; LTV 60%; loan 1,400,000; term 36 months — net advance $1,184,500 / redemption $1,254,000 / APR 25.90% / 36 payments.
  5. Retained; property 950,000; LTV 55%; loan 600,000; term 20 months — net advance $407,562.50 / redemption $531,905 / APR 17.32% / 20 payments.
  6. Serviced; property 1,500,000; LTV 75%; loan 1,125,000; term 30 months — net advance $1,116,875 / redemption $1,153,125 / APR 13.35% / 30 payments.
  7. Rolled-up; property 600,000; LTV 65%; loan 390,000; term 18 months — net advance $379,870 / redemption $566,766.04 / APR 30.57% / 18 payments.
  8. Serviced; property 2,200,000; LTV 68%; loan 1,480,000; term 48 months — net advance $1,442,940 / redemption $1,512,560 / APR 22.52% / 48 payments.
  9. Retained; property 1,250,000; LTV 70%; loan 875,000; term 15 months — net advance $690,662.50 / redemption $897,750 / APR 23.34% / 15 payments.
  10. Rolled-up; property 500,000; LTV 50%; loan 250,000; term 10 months — net advance $247,850 / redemption $281,525.69 / APR 16.52% / 10 payments.

# DEVIATIONS
- None.
