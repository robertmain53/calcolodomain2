CHANGELOG
- `sito_modificato/bayesian-inference.html`: Rebuilt the page to match the mortgage-payment canonical layout, preserved the Bayesian inference inputs/results cards, reorganized the narrative into the mandated hero → how-to → meta order, and rewrote the script around the required parse/validate/compute/format/render/update contract while keeping all original informational content (HowTo guidance, theory, FAQs, formulas, citations, changelog, and audit text).

TEST REPORT
- Test 1 (Uniform default, n=50, x=18, 95%): posterior mean 0.365385, mode 0.36, credible interval [0.235744, 0.495025], predictive 0.365385. Legacy/new diff for mean/interval = 0.
- Test 2 (Jeffreys, n=100, x=30, 90%): posterior mean 0.30198, mode 0.29798, credible interval [0.227206, 0.376754], predictive 0.30198. Legacy/new diff = 0.
- Test 3 (Custom α=2.5, β=3.75, n=20, x=5, 99%): posterior mean 0.285714, mode 0.268041, credible interval [0.062801, 0.508627], predictive 0.285714. Legacy/new diff = 0.
- Test 4 (Uniform, n=10, x=0, 50%): posterior mean 0.083333, mode undefined (mode on boundary), credible interval [0.03163, 0.135037], predictive 0.083333. Legacy/new diff = 0.
- Test 5 (Uniform, n=10, x=10, 99.9%): posterior mean 0.916667, mode undefined (mode on boundary), credible interval [0.66443, 1], predictive 0.916667. Legacy/new diff = 0.
- Test 6 (Uniform, n=1000, x=500, 95%): posterior mean 0.5, mode 0.5, credible interval [0.469057, 0.530943], predictive 0.5. Legacy/new diff = 0.
- Test 7 (Custom α=5, β=1, n=12, x=8, 92.5%): posterior mean 0.722222, mode 0.75, credible interval [0.539269, 0.905176], predictive 0.722222. Legacy/new diff = 0.
- Test 8 (Jeffreys, n=1, x=0, 95%): posterior mean 0.25, mode undefined (mode on boundary), credible interval [0, 0.739991], predictive 0.25. Legacy/new diff = 0.
- Test 9 (Custom α=0.7, β=0.7, n=25, x=10, 80%): posterior mean 0.405303, mode 0.397541, credible interval [0.285105, 0.525501], predictive 0.405303. Legacy/new diff = 0.
- Test 10 (Uniform, n=5, x=2, 60%): posterior mean 0.428571, mode 0.4, credible interval [0.281318, 0.575824], predictive 0.428571. Legacy/new diff = 0.
- Parity statement: The Node script compares the legacy and updated calculators for every vector and reports zero discrepancy in the posterior mean and interval, so the updated page mirrors the legacy output exactly.
- Console error check: Node-based test harness runs without errors; no browser console was available for this static refactor.
