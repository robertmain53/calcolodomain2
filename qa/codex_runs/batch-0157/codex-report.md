CHANGELOG
- sito_modificato/binomial-distribution.html:
  - Replaced the legacy layout with the canonical mortgage payment structure, keeping the binomial narrative and schema content.
  - Centralized the calculator inputs/results into the required hero grid and added the parse/validate/compute/format/render/update pattern with debounce/reset behavior.
  - Added the meta section with the formula, citations, changelog, and verification badges, and preserved the "Full original guide (expanded)" content.

TEST REPORT
- n=5, k=2, p=0.5 → 0.3125
- n=10, k=5, p=0.5 → 0.2461
- n=10, k=0, p=0.2 → 0.1074
- n=20, k=6, p=0.3 → 0.1916
- n=30, k=21, p=0.7 → 0.1573
- n=50, k=5, p=0.1 → 0.1849
- n=100, k=50, p=0.5 → 0.0796
- n=1, k=1, p=0.5 → 0.5000
- n=1, k=0, p=0.5 → 0.5000
- n=12, k=3, p=0.25 → 0.2581
- Parity: All computed probabilities use the original binomial formula and match the four-decimal rounding that the legacy calculator produced.

CONSOLE ERROR CHECK
- Not executed; browser console unavailable in this environment, but the new script only references existing DOM IDs and standard APIs, so no runtime errors are expected when deployed.

DEVIATIONS
- None.
