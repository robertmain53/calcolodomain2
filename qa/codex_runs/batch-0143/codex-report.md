CHANGELOG
- sito_modificato/benzodiazepine-conversion.html:
  - Rebuilt the entire page to follow the mortgage-payment canonical layout while preserving all medical guidance, glossary, FAQ, author, and policy sections.
  - Reimplemented the calculator UI/UX (hero, inputs card, results card, meta sections) plus responsive footer/aside per the reference.
  - Rewrote the JS into parse/validate/compute/format/render/update helpers with deterministic rounding, debounced updates, and validation safeguards.

TEST REPORT
- Diazepam 5 mg → 5.00 mg
- Diazepam 2.75 mg → 2.75 mg
- Diazepam 0.25 mg → 0.25 mg
- Diazepam 10 mg → 10.00 mg
- Diazepam 100 mg → 100.00 mg
- Lorazepam 5 mg → 10.00 mg
- Lorazepam 2 mg → 4.00 mg
- Lorazepam 1.75 mg → 3.50 mg
- Lorazepam 12.5 mg → 25.00 mg
- Lorazepam 0.5 mg → 1.00 mg
- Parity: All converted doses match the legacy ratio-based logic (division by conversion factor) with the same 2-decimal rounding.

CONSOLE ERROR CHECK
- Not run (browser console unavailable); no runtime errors surfaced during the deterministic Node validation script.

DEVIATIONS
- None.
