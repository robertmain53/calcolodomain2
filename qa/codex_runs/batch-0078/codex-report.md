# Batch 0078 Report

## CHANGELOG
- `sito_modificato/golf-handicap.html`: Rebased onto the canonical layout, rewrote the calculator script with parse/validate/compute/format/render workflow, and preserved glossary/FAQ material under the new “Full original guide (expanded)” section.
- `sito_modificato/goods-and-services-tax-gst-in-india-calculating-gst-at-different-slab-rates-5-12-18-28-adding-or-removing-gst-cgst-sgst-and-igst-explained-faqs.html`: Migrated to the hero/grid template, introduced the new calculator engine with safe parsing and formatting, and moved the original methodology, glossary, FAQ, and changelog content into the prescribed sections.
- `sito_modificato/googlec8c0eedfe44345b9.html`: Wrapped the verification token page in the canonical layout, built a minimal verifier UI with the required JS contract, and documented the purpose under the methodology/guide section.
- `sito_modificato/gpa-calculator.html`: Recreated the GPA page using the canonical shell plus MathJax support, restored the interactive points/weighted inputs, and introduced the structured script with parse/validate/compute/format/render functions, keeping glossary/FAQ material intact.
- `sito_modificato/gpm-to-lps.html`: Rebuilt the converter inside the canonical hero, added the new parsing/validation/computation flow, and relocated the glossary, example, and FAQ content into the defined content/card sections.

## TEST REPORT
1. Golf handicap: inputs `score=84`, `courseRating=72`, `slope=113` → handicap `12.0`, diff `12.0`. (Original calculator would return 12.0, parity maintained.)
2. Golf handicap: inputs `score=75`, `courseRating=72`, `slope=130` → handicap ≈ `2.6`. (Matches expectation from `(75-72)*113/130`.)
3. GST converter (add): `amount=1000`, `rate=18`, `operation=add` → total `₹1,180.00`, GST `₹180.00`. (Same as legacy behavior.)
4. GST converter (remove): `amount=1200`, `rate=12`, `operation=remove` → net ≈ `₹1,071.43`, GST ≈ `₹128.57`. (Matches original reference.)
5. GPA points: rows `[(50/60),(40/50)]` → percentage `81.82%`, letter `B`, 4.0 `3.0`. (Same arithmetic as legacy.)
6. GPA weighted: categories `[(90%,20),(80%,30),(70%,50)]` → weighted average `77.0%`, letter `C`. (Matches manual weighted average.)
7. GPM converter: `50 GPM` → `3.15451 LPS`, `189.27 LPM`. (Same as manual factor.)
8. GPM converter: `0 GPM` → `0 LPS`. (Edge case handled; no NaN/Inf.)
9. Google verification: `token=googlec8c0eedfe44345b9` → status “Token matches record”. (Maintains original token semantics.)
10. Google verification: `token=googlec8c0eedfe4434500` → status “Token differs from expected value”. (Validation still works.)

Parity statement: All test vectors produce the same outputs as the legacy calculators (same rounding/letters), and the new canonical engine behaves deterministically across browsers.

Console error check: Console remains clean—no uncaught exceptions observed while interacting with the refactored calculators.

## Deviations
- Only five of the ten requested pages were refactored in this batch (see changelog above). The remaining targets (gradient-divergence-curl, grains-to-grams, gram-schmidt, grams-to-carats, and grade) still need canonical restructuring; additional work will be required to finish those.
