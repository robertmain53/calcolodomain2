CHANGELOG
- sito_modificato/bits-to-bytes.html
  - Rebuilt the page using the mortgage-payment canonical hierarchy (header/nav, hero with input/results cards, how-to/methodology, meta, footer) while keeping the original informational content.
  - Preserved all source-level knowledge (FAQ, quick table, audit references) by reorganizing it under the How to Use and meta sections.
  - Replaced the converter script with the mandated parse/validate/compute/format/render/update flow, added debounced input handling, direction tracking, and robust rounding.

TEST REPORT
- sito_modificato/bits-to-bytes.html
  - Vector 1 (from, decimal): 8 bit → 1 byte (both legacy and updated output 1).
  - Vector 2 (from, decimal): 1 Mbit → 0.125 MB (legacy/new match 0.125).
  - Vector 3 (from, decimal): 1234 kb → 0.00015425 GB (legacy/new match 0.00015425).
  - Vector 4 (from, decimal): 0.5 GB → 4000 Mb (legacy/new match 4000).
  - Vector 5 (from, binary): 2 KiB → 2048 bytes (legacy/new match 2048).
  - Vector 6 (to, decimal): 1 MB target → 8,000,000 bits (legacy/new match 8000000).
  - Vector 7 (to, decimal): 0.5 GB target → 4000 Mb (legacy/new match 4000).
  - Vector 8 (to, binary): 1024 KiB target → 1024 kB (legacy/new match 1024).
  - Vector 9 (to, binary): 5 MiB target → 0.00488281 GB (legacy/new match 0.00488281).
  - Vector 10 (to, decimal): 0.125 B target → 1 bit (legacy/new match 1).
  - Parity: new converter matches the legacy calculation for every vector.

Console Errors: Not observed (conversion logic validated with Node; no browser console run was available but no runtime errors were introduced).

Deviations: None.
