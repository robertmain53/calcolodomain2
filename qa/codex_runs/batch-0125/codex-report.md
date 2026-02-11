# CHANGELOG
- sito_modificato/base-converter.html
  - Rebuilt the page to match the mortgage-payment canonical layout while preserving nav, hero, and footer hierarchy.
  - Reorganized the interpretive content into a How to Use / Methodology card followed by the original "Full original guide (expanded)", then repositioned the meta details (formulas/citations/changelog).
  - Reimplemented the base conversion logic inside the required parse->validate->compute->format->render->update pipeline, added debounced input handling, and kept all helper buttons/quick links active.

# TEST REPORT
- Parity: New script preserves the existing arithmetic and rounding behavior because the core conversion helpers and formatting mirror the legacy implementation.
- Test vectors (input, from base, to base → converted; normalized; Binary/Octal/Decimal/Hex outputs match the legacy logic):
  1. Input `1011.01`, base 2 → base 10 produces 11.25; normalized `1011.01`; Binary 1011.01; Octal 13.2; Decimal 11.25; Hex B.4.
  2. Input `255`, base 10 → base 16 produces FF; normalized `255`; Binary 11111111; Octal 377; Decimal 255; Hex FF.
  3. Input `-1A.3`, base 16 → base 2 produces -11010.0011; normalized `-1A.3`; Binary -11010.0011; Octal -32.14; Decimal -26.1875; Hex -1A.3.
  4. Input `7F`, base 16 → base 8 produces 177; normalized `7F`; Binary 1111111; Octal 177; Decimal 127; Hex 7F.
  5. Input `123.456`, base 10 → base 2 produces 1111011.0111010010111100; normalized `123.4560000000000030`; Binary 1111011.0111010010111100; Octal 173.3513615237574734; Decimal 123.456; Hex 7B.74BC6A7EF9DC.
  6. Input `100`, base 2 → base 36 produces 4; normalized `100`; Binary 100; Octal 4; Decimal 4; Hex 4.
  7. Input `ABC`, base 13 → base 5 produces 24340; normalized `ABC`; Binary 11100110101; Octal 3465; Decimal 1845; Hex 735.
  8. Input `0`, base 10 → base 2 produces 0; normalized `0`; Binary 0; Octal 0; Decimal 0; Hex 0.
  9. Input `-101`, base 2 → base 10 produces -5; normalized `-101`; Binary -101; Octal -5; Decimal -5; Hex -5.
  10. Input `3A.F`, base 16 → base 10 produces 58.9375; normalized `3A.F`; Binary 111010.1111; Octal 72.74; Decimal 58.9375; Hex 3A.F.
- Console: Node-based conversion script executed without runtime errors; browser console was not available but the same logic drives the UI.

# DEVIATIONS
- None.
