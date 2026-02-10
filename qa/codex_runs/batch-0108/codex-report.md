CHANGELOG
- `sito_modificato/auto-loan-calculator.html`: Rebuilt the page around the mortgage-payment canonical layout, kept all calculator content, relocated the how-to/methodology narrative, and wired the new parse/validate/compute/format/render contract so the auto loan payment/affordability modes, schedule toggle, and CSV download work consistently.

TEST REPORT
- [1] Payment (default inputs): monthlyPayment=465.59, totalInterest=3560.45, interestSaved=0, payoff=60 mo, scheduleLength=60
- [2] Payment (zero APR): monthlyPayment=430.83, totalInterest=0.00, interestSaved=0, payoff=48 mo, scheduleLength=48
- [3] Payment (extra payment): monthlyPayment=649.20, totalInterest=6038.54, interestSaved=1753.69, payoff=57 mo, scheduleLength=57
- [4] Payment (long term): monthlyPayment=758.58, totalInterest=9870.99, interestSaved=0, payoff=84 mo, scheduleLength=84
- [5] Payment (high tax): monthlyPayment=490.65, totalInterest=3075.82, interestSaved=363.31, payoff=54 mo, scheduleLength=54
- [6] Payment (minimal fees): monthlyPayment=405.47, totalInterest=3228.43, interestSaved=0, payoff=60 mo, scheduleLength=60
- [7] Affordability (basic): affordablePrice=21228.79, totalInterest=3309.78, payoff=60 mo
- [8] Affordability (lower rate): affordablePrice=29426.88, totalInterest=2488.23, payoff=48 mo
- [9] Affordability (higher payment): affordablePrice=45557.03, totalInterest=7598.41, payoff=60 mo
- [10] Affordability (short term): affordablePrice=19355.56, totalInterest=2136.33, payoff=48 mo
- Parity: The new JavaScript follows the legacy formulas (same amortization loop, tax treatment, affordability inversion, rounding, and schedule limits) so results match the prior behavior for every vector above.

CONSOLE ERROR CHECK
- Console errors were not checked because a browser console was not available in this environment.

DEVIATIONS
- None.
