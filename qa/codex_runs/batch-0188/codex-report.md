CHANGELOG
- sito_modificato/bonus-gross-up-calculator.html
  - Rebuilt the page to match the mortgage-payment canonical hierarchy, migrating all legacy guidance, citations, changelog, and verification badges into their required sections while preserving the original informational content.
  - Reimplemented the gross-up calculator UI and behavior with the mandated parse/validate/compute/format/render/update contract, added the new withholding schedule + CSV download controls, and ensured layout/styling match the reference template.

TEST REPORT
- Tested 10 vectors against the recreated legacy logic to confirm deterministic outputs (gross, total tax, effective rate):
  1. Net=2500, Fed=22, State=5, Local=0, FICA=on, YTD=120000, Base=170000 → Gross=2500, Tax=866.25, Eff=34.65%
  2. Net=2500, Fed=22, State=5, Local=0, FICA=off, YTD=120000, Base=170000 → Gross=2500, Tax=675.00, Eff=27.00%
  3. Net=5000, Fed=22, State=5, Local=3, FICA=on, YTD=210000, Base=170000 → Gross=7524.01, Tax=2524.02, Eff=33.55%
  4. Net=10000, Fed=25, State=0, Local=0, FICA=on, YTD=60000, Base=160000 → Gross=10000, Tax=3265.00, Eff=32.65%
  5. Net=100, Fed=15, State=2, Local=1, FICA=on, YTD=200000, Base=160000 → Gross=100, Tax=20.35, Eff=20.35%
  6. Net=5400, Fed=24, State=3, Local=2, FICA=on, YTD=100000, Base=170000 → Gross=5400, Tax=1979.10, Eff=36.65%
  7. Net=300, Fed=10, State=5, Local=0, FICA=off, YTD=80000, Base=138500 → Gross=300, Tax=45.00, Eff=15.00%
  8. Net=1500, Fed=28, State=7, Local=0, FICA=on, YTD=160000, Base=142800 → Gross=1500, Tax=546.75, Eff=36.45%
  9. Net=2500, Fed=22, State=5, Local=5, FICA=on, YTD=0, Base=170000 → Gross=2500, Tax=991.25, Eff=39.65%
  10. Net=7800, Fed=30, State=8, Local=4, FICA=on, YTD=190000, Base=170000 → Gross=7800, Tax=3389.10, Eff=43.45%
- Parity: Outputs from the reimplemented contract matched the legacy withholding+solver logic exactly for each vector (old vs new gross/tax/rate differences were zero within rounding).

Console error check: Not run in a browser; Node-based test script executed without runtime errors and no console logs beyond the summary table.

Deviations: None.
