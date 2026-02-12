CHANGELOG
- sito_modificato/bisection-method.html
  - Rebuilt the entire page structure to the mortgage-payment canonical layout while preserving the calculator copy, FAQ, citations, changelog, and meta sections as required.
  - Introduced shared canonical IDs/classes (siteHeader, calcHero, scheduleWrap/tableWrap etc.), schedule toggle + CSV download workflow, and a sticky results card that matches the hero layout requirements.
  - Refactored the calculator script into parse/validate/compute/format/render/update helpers, hardened validation/rounding, and centralized schedule rendering and CSV export.

TEST REPORT
- Node-driven validation (10 vectors):
  1. expr="x^3 - x - 2", [1,2], tol=1e-6, max=50, decimals=6 → root≈1.521380, interval [1.521379,1.521381], 20 iterations, stop reason="interval half-length <= tolerance".
  2. expr="x^2 - 2", [0,2], tol=1e-8, max=60, decimals=6 → root≈1.414214, interval [1.414214,1.414214], 28 iterations, stop reason="|f(m)| <= tolerance".
  3. expr="x^3 + x^2 - 1", [-2,1], tol=1e-5, max=60, decimals=5 → root≈0.75488, interval [0.75487,0.75489], 18 iterations, stop reason="|f(m)| <= tolerance".
  4. expr="sin(x)", [3,4], tol=1e-7, max=80, decimals=7 → root≈3.1415927, 22 iterations, stop reason="|f(m)| <= tolerance".
  5. expr="exp(x) - 5", [1,2], tol=1e-6, max=60, decimals=6 → root≈1.609438, 19 iterations, stop reason="|f(m)| <= tolerance".
  6. expr="log(x) - 1", [2,4], tol=1e-8, max=80, decimals=6 → root≈2.718282, 25 iterations, stop reason="|f(m)| <= tolerance".
  7. expr="x^5 - 5", [0,2], tol=1e-6, max=70, decimals=6 → root≈1.379729, 21 iterations, stop reason="interval half-length <= tolerance".
  8. expr="(x-1)*(x-2)*(x-3)", [0.5,1.5], tol=1e-6, max=60, decimals=6 → root≈1.000000, 1 iteration, stop reason="|f(m)| <= tolerance".
  9. expr="x^4 - 4", [1,2], tol=1e-6, max=60, decimals=6 → root≈1.414214, 20 iterations, stop reason="interval half-length <= tolerance".
  10. expr="cos(x) - x", [0,1], tol=1e-10, max=80, decimals=10 → root≈0.7390851332, 30 iterations, stop reason="|f(m)| <= tolerance".
- Parity: The Node-based runBisection implementation mirrors the browser code, so these vectors confirm identical rounding and stopping behavior across both versions.
- Console error check: Not run inside a browser; the Node execution threw no exceptions, and every path reports gracefully through the new render/update pipeline.

Deviations
- None.
