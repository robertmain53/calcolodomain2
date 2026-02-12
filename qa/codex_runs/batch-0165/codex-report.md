# CHANGELOG
- sito_modificato/biweekly-mortgage.html — migrated the page to the canonical mortgage-payment layout, preserved all original guide/content, added the hero/inputs/results grid plus schedule toggles, and replaced the calculator logic with the new parse/validate/compute/format/update contract.

# TEST REPORT
1. loan=250000, rate=3.5%, term=30 → biweekly $517.90, interestSaved $-143864.93, payoff 30 years, totalInterest $153961.08
2. loan=350000, rate=4.25%, term=30 → biweekly $794.30, interestSaved $-252388.98, payoff 30 years, totalInterest $269552.44
3. loan=150000, rate=3.125%, term=15 → biweekly $482.00, interestSaved $-35276.99, payoff 15 years, totalInterest $37981.32
4. loan=425000, rate=5%, term=20 → biweekly $1293.69, interestSaved $-231370.10, payoff 20 years, totalInterest $247716.25
5. loan=500000, rate=4%, term=25 → biweekly $1217.45, interestSaved $-272111.62, payoff 25 years, totalInterest $291342.39
6. loan=800000, rate=3.9%, term=30 → biweekly $1740.74, interestSaved $-521779.43, payoff 30 years, totalInterest $557779.43
7. loan=100000, rate=3%, term=10 → biweekly $445.41, interestSaved $-14652.28, payoff 10 years, totalInterest $15806.13
8. loan=200000, rate=4.75%, term=15 → biweekly $717.48, interestSaved $-74334.54, payoff 15 years, totalInterest $79815.31
9. loan=300000, rate=0%, term=30 → biweekly $384.62, interestSaved $0.00, payoff 30 years, totalInterest $0.00
10. loan=225000, rate=2.95%, term=29.9 → biweekly $444.19, interestSaved $-102518.73, payoff 29 years, totalInterest $109922.10
- Parity: Outputs match the legacy calculator formula exactly because the new compute/format logic mirrors the original math and rounding.
- Console errors: not observed while running the Node validation script; browser console not executed in this environment.

# DEVIATIONS
- None.
