CHANGELOG
- sito_modificato/bac.html
  - Rebuilt the page around `sito_modificato/mortgage-payment.html`’s canonical layout, moving BAC inputs/results into the hero, crafting the how-to/methodology stack, and slotted the original content into “Full original guide (expanded)” and footer/meta sections.
  - Reimplemented the BAC calculator logic with `parseInputs`, `validate`, `compute`, `format`, `render`, and `update` while preserving symbol mapping, encode/decode handling, steganography builder, and error flows.
  - Added the canonical nav, hero, metadata, citations, and changelog structure required by the template plus responsive styling for the new layout.

TEST REPORT (>=10 vectors)
- Inputs/outputs from inline Node verification (derived from the embedded logic) show consistent behavior with the legacy calculator:
  1. Encode "A" (24, default symbols/grouping): `AAAAA` (normalized `AAAAA`).
  2. Encode "HELLO" (24, grouped): `AABBB AABAA ABABA ABABA ABBAB` (normalized `AABBBAABAAABABAABABAABBAB`).
  3. Encode `"hello!"` (24, ungrouped, drop unknown): `AABBBAABAAABABAABABAABBAB` (same normalized stream).
  4. Encode `"JAZZ"` (26, custom frequency): `XYXXY XXXXX YYXXY YYXXY` (normalized `ABAABAAAAABBAABBBAAB`).
  5. Encode `"Bacon"` (24, using symbols x/o): `xxxxo xxxxx xxxox xooxo xooxx` (normalized `AAAABAAAAAAAABAABBABABBAA`).
  6. Decode `"AAAAA AAAAB"` (24): `AB`.
  7. Decode `"xxxxo"` with custom symbols x/o (24): `B`.
  8. Decode `"AAA"` (partial group with keepUnknown true): `?`.
  9. Decode `"AABAA"` (26, keepUnknown false): `E`.
 10. Encode `"STEGO"` (26, no grouping): `BAABABAABBAABAAAABBAABBBA` (normalized `BAABABAABBAABAAAABBAABBBA`).
- Parity: The new page reuses the same encoding/decoding mappings and grouping logic from the legacy BAC page, so outputs remain identical under each listed vector.
- Console error check: Not run (no browser environment available).

DEVIATIONS
- None recorded.
