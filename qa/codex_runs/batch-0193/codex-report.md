# CHANGELOG
- sito_modificato/bpd-to-gpm.html
  - Rebuilt the page using the mortgage payment canonical layout, keeping the calculators hero, nav, meta blocks, and footer while preserving all barrel-to-gallon content.
  - Ported the converter logic into the prescribed parse/validate/compute/format/render/update pattern, added debounced updates, reset behavior, and consistent rounding format.
  - Reorganized the guidance, FAQs, glossary, and audit data into the How to Use, Formulas, Citations, and Changelog panels without losing any original information.

# TEST REPORT
- Vector `bpd=1` → 0.03 gpm
- Vector `bpd=12.5` → 0.36 gpm
- Vector `bpd=50` → 1.46 gpm
- Vector `bpd=123` → 3.59 gpm
- Vector `bpd=250` → 7.29 gpm
- Vector `bpd=999.5` → 29.15 gpm
- Vector `bpd=1000` → 29.17 gpm
- Vector `bpd=2500` → 72.92 gpm
- Vector `bpd=12345` → 360.06 gpm
- Vector `bpd=42000` → 1225.00 gpm
- Parity statement: Each vector replicates the legacy formula `gpm = (bpd × 42) / 1440` with deterministic rounding to two decimals.
- Console errors: Not observed (page not executed in a browser; calculator script uses standard DOM operations and the node-based checks succeeded).

# Deviations
- None.
