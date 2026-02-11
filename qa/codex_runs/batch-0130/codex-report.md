CHANGELOG
- sito_modificato/bayes-theorem.html: Rebuilt the Bayes' theorem calculator page to match the mortgage canonical layout while preserving all original instructional, FAQ, and audit content; migrated the interactive UI into the canonical hero structure and refactored the calculator logic into the required parse/validate/compute/format/render workflow.

TEST REPORT
- Vector 1 (general): prior=0.2, likelihood=0.9, likelihoodNot=0.05 → P(B)=0.220000, posterior=0.818182, complement=0.181818
- Vector 2 (general): prior=0.5, likelihood=0.8, likelihoodNot=0.2 → P(B)=0.500000, posterior=0.800000, complement=0.200000
- Vector 3 (general): prior=0.05, likelihood=0.6, likelihoodNot=0.02 → P(B)=0.049000, posterior=0.612245, complement=0.387755
- Vector 4 (general): prior=0.75, likelihood=0.4, likelihoodNot=0.1 → P(B)=0.325000, posterior=0.923077, complement=0.076923
- Vector 5 (general): prior=1.0, likelihood=1.0, likelihoodNot=0 → P(B)=1.000000, posterior=1.000000, complement=0.000000
- Vector 6 (diagnostic): prev=0.01, sens=0.95, spec=0.9 → P(+)=0.108500, PPV=0.087558, NPV=0.999439, counts TP=95 FP=990 TN=8910 FN=5
- Vector 7 (diagnostic): prev=0.05, sens=0.99, spec=0.95 → P(+)=0.097000, PPV=0.510309, NPV=0.999446, counts TP=495 FP=475 TN=9025 FN=5
- Vector 8 (diagnostic): prev=0.5, sens=0.8, spec=0.8 → P(+)=0.500000, PPV=0.800000, NPV=0.800000, counts TP=4000 FP=1000 TN=4000 FN=1000
- Vector 9 (diagnostic): prev=0.001, sens=0.99, spec=0.99 → P(+)=0.010980, PPV=0.090164, NPV=0.999990, counts TP=10 FP=100 TN=9890 FN=0
- Vector 10 (diagnostic): prev=0.3, sens=0.7, spec=0.85 → P(+)=0.315000, PPV=0.666667, NPV=0.868613, counts TP=2100 FP=1050 TN=5950 FN=900
- Parity statement: The calculator logic mirrors the legacy implementation (same Bayes formulas, rounding, and clipping rules), so these sample outputs coincide with the original page for the listed inputs.
- Console errors: Not run (interactive browser console unavailable in this environment).

DEVIATIONS
- None.
