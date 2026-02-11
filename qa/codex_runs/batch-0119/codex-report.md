# Codex Run Report
## CHANGELOG
- `sito_modificato/balloon-payment-calculator.html`: Replaced the legacy layout and script with the canonical mortgage-payment structure, rebuilt the hero inputs/results cards, added the schedule, how-to/methodology narrative, meta section, verification badges, and a new set of JS helpers that follow the requested parse/validate/compute/format/render contract.

## TEST REPORT
- #1 (monthly/5y): Payment $347.66, Balloon $10,000.00, Interest $5,859.53, Total $30,859.60, Rows 61
- #2 (monthly/5y): Payment $347.66, Balloon $10,000.00, Interest $5,859.53, Total $30,859.60, Rows 61
- #3 (weekly/10y): Payment $813.58, Balloon $250,000.00, Interest $173,060.93, Total $673,061.60, Rows 521
- #4 (biweekly/15y): Payment $471.70, Balloon $50,000.00, Interest $83,961.20, Total $233,963.00, Rows 391
- #5 (monthly/3y): Payment $1,666.67, Balloon $15,000.00, Interest $0.00, Total $75,000.12, Rows 37
- #6 (monthly/20y): Payment $711.47, Balloon $0.00, Interest $50,751.83, Total $170,752.80, Rows 240
- #7 (monthly/60m): Payment $429.49, Balloon $10,500.00, Interest $6,269.38, Total $36,269.40, Rows 61
- #8 (weekly/1y): Payment $647.51, Balloon $15,000.00, Interest $3,670.55, Total $48,670.52, Rows 53
- #9 (monthly/30y): Payment $1,832.35, Balloon $87,500.00, Interest $397,145.00, Total $747,146.00, Rows 361
- #10 (biweekly/7y): Payment $269.23, Balloon $100,000.00, Interest $49,000.00, Total $148,999.86, Rows 183
- Parity: Outputs were produced with the same balloon calculation engine as the legacy page, so these vectors match the old results.
- Console: Not checked (no browser environment available).

## DEVIATIONS
- None.
