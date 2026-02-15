CHANGELOG
- sito_modificato/bradford-factor.html — reworked the page to follow the mortgage-payment canonical layout (header, hero, how-to card, and footer/meta structure), relocated legacy content into the expanded guide, and replaced the calculator script with the mandated parse/validate/compute/format/render/update contract plus debounced interaction handling.

TEST REPORT
- 1 incidents, 1 days → score 1 (Low – typical levels)
- 2 incidents, 5 days → score 20 (Low – typical levels)
- 3 incidents, 12 days → score 108 (Moderate – monitor closely)
- 5 incidents, 30 days → score 750 (Critical – urgent HR review)
- 8 incidents, 40 days → score 2560 (Critical – urgent HR review)
- 10 incidents, 60 days → score 6000 (Critical – urgent HR review)
- 12 incidents, 15 days → score 2160 (Critical – urgent HR review)
- 15 incidents, 7 days → score 1575 (Critical – urgent HR review)
- 18 incidents, 3 days → score 972 (Critical – urgent HR review)
- 25 incidents, 10 days → score 6250 (Critical – urgent HR review)
- 30 incidents, 20 days → score 18000 (Critical – urgent HR review)
- Parity statement: Bradford Factor outputs equal B = S² × D, matching the legacy calculator’s numeric behavior and rounding rules.
- Console error check: not run inside a browser environment (no DOM), but the Node-based validation executed cleanly and surfaced no JavaScript errors.
