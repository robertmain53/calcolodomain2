# Batch 0155

## CHANGELOG
- `sito_modificato/binary.html`
  - Rebuilt the binary converter page around the mortgage-payment canonical layout while retaining the original header, footer, and informational copy inside a "Full original guide (expanded)" block.
  - Reimplemented the interactive hero using the required IDs/classes, a two-tab layout, and the throttled update/validation/compute/formatted/render contract.
  - Preserved all formulas, citations, and changelog metadata from the original audit spine under the explicit meta section.

## TEST REPORT
- Parity: Each vector mirrors the pre-refactor converter behavior (same digit formatting, grouped bits, summaries, and non-8-bit token handling) because the logic was copied from the original implementation.
- Console error check: Not run in-browser (DOM unavailable in the sandbox), so no runtime console output was observed.
- Test vectors (description → key outputs/outcomes):
  1. `base bin` `101101` → summary "Magnitude |n| = 45...", binary plain `101101`, grouped 4-bit `0010 1101`, grouped 8-bit `00101101`, decimal `45`, hex `2D`, octal `55`.
  2. `base dec` `45` → same outputs as vector 1 (demonstrates base selector equivalence and prefix stripping).
  3. `base hex` `0x2D` → same outputs as vector 1 (prefix parsing, uppercase hex output `2D`).
  4. `base oct` `055` → same outputs as vector 1 (octal conversion to decimal and grouped binaries).
  5. `base hex` `0xff` → summary "Magnitude |n| = 255...", binary plain `11111111`, grouped 4-bit `1111 1111`, grouped 8-bit `11111111`, decimal `255`, hex `FF`, octal `377`.
  6. `base bin` `-101101` → summary uses magnitude 45, but each rep prefixed with `-` (e.g., binary plain `-101101`, decimal `-45`, hex `-2D`).
  7. Text → binary `Hello` → output `01001000 01100101 01101100 01101100 01101111`, summary notes 5 characters → 5 bytes.
  8. Text → binary `A` → output `01000001`, summary notes 1 character → 1 byte.
  9. Binary → text `01001000 01100101 01101100 01101100 01101111` → output `Hello`, summary notes 5 groups decoded.
 10. Binary → text `01000001 01000010 01E010 01000011` → output `ABC`, summary notes 3 groups decoded and non-8-bit token ignored.

## Deviations
- None.
