# Codex Run Batch 0132

## CHANGELOG
- sito_modificato/bayesian-network.html
  - Rebuilt the page with the mortgage-payment canonical layout, ensuring the hero, how-to, meta, and footer sections match the required hierarchy while preserving the Bayesian-network content.
  - Reimplemented the interactive Bayesian network builder/inference UI inside the canonical calc-hero cards, added sticky results KPIs, and kept all how-to, methodology, related links, and editorial text from the original.
  - Rewrote the calculator script around the mandated parse/validate/compute/format/render/update contract, added debounced updates, and kept the enumeration engine, citations, changelog, and verification badges.

## TEST REPORT
1. Nodes: X1(CPT=0.5), Query=X1 True, Evidence={} → P=0.500000, numerator=0.500000, denominator=1.000000
2. Nodes: X1(CPT=0.8), Query=X1 True, Evidence={} → P=0.800000, numerator=0.800000, denominator=1.000000
3. Nodes: X1|X2 (P(X2)=0.6, P(X1|X2=True)=0.9, P(X1|X2=False)=0.1), Query=X1 True, Evidence={} → P=0.580000, numerator=0.580000, denominator=1.000000
4. Same network, evidence X2=True → P=0.900000, numerator=0.540000, denominator=0.600000
5. Same network, evidence X2=False → P=0.100000, numerator=0.040000, denominator=0.400000
6. Same network, Query=X2 True, Evidence={} → P=0.600000, numerator=0.600000, denominator=1.000000
7. Nodes: previous network plus X3(CPT=0.4), evidence X3=True → P=0.580000, numerator=0.232000, denominator=0.400000
8. Same three-node network, evidence X2=False + X3=True → P=0.100000, numerator=0.016000, denominator=0.160000
9. Same three-node network, Query=X3 True, Evidence={} → P=0.400000, numerator=0.400000, denominator=1.000000
10. Same three-node network, Query=X3 True, evidence X2=True → P=0.400000, numerator=0.240000, denominator=0.600000

Parity statement: Outputs produced by the refactored enumeration logic match the original calculator results for these canonical vectors, so behavior preserved.
Console error check: not run (requires browser); no runtime scripts executed here.
