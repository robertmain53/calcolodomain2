CHANGELOG
- sito_modificato/balloon-loan.html: Rebuilt the page around the canonical mortgage layout (header, hero, how-to, meta + footer) while preserving all existing guidance and citations; rewrote the calculator UI and logic to rely on the mandatory parse/validate/compute/format/render/update contract, added robust schedule handling, and reintroduced verification/changelog/citation metadata.

TEST REPORT
1. loan=10000, rate=5, years=5, balloonPct=30 → monthly=188.71, balloon=3000
2. loan=25000, rate=4.5, years=7, balloonPct=20 → monthly=347.50, balloon=5000
3. loan=50000, rate=3.25, years=3, balloonPct=10 → monthly=1459.58, balloon=5000
4. loan=150000, rate=5.75, years=10, balloonPct=25 → monthly=1646.54, balloon=37500
5. loan=100000, rate=0, years=5, balloonPct=50 → monthly=1666.67, balloon=50000 (zero interest branch)
6. loan=300000, rate=6.25, years=30, balloonPct=20 → monthly=1847.15, balloon=60000
7. loan=75000, rate=8.5, years=4, balloonPct=40 → monthly=1848.62, balloon=30000
8. loan=20000, rate=7, years=2, balloonPct=5 → monthly=895.45, balloon=1000
9. loan=85000, rate=5.5, years=8, balloonPct=15 → monthly=1096.44, balloon=12750
10. loan=120000, rate=4.1, years=6.5, balloonPct=35 → monthly=1755.17, balloon=42000
- Parity: Node script mirrors the legacy monthly payment formula and balloon calculation so the numerical outputs align with the previous implementation’s rounding rules.

Console error check: Not run (browser console unavailable in this environment).

Deviations: None.
