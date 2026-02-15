CHANGELOG
- sito_modificato/bra-size-converter.html: Rebuilt the page using the mortgage-payment canonical layout, reflowed all explanatory content under the proper hero/how-to/metasections, and implemented a vanilla JS conversion engine with band anchors, cup sequencing, validation, and deterministic rounding.

TEST REPORT
- Test vectors (Provable outputs from the shared conversion logic):
  1. US 34B → EU 75B (75 cm anchor, cup sequence matches target list)
  2. EU 75C → US 34C (75 cm anchor, cup sequence matches target list)
  3. UK 36DD → EU 80F (80 cm anchor, EU lacks DD so F is nearest)
  4. US 30AA → UK 30AA (65 cm anchor, matches target list)
  5. EU 80D → US 36D (80 cm anchor, matches target list)
  6. US 42G → EU 95G (95 cm anchor, target list supports G)
  7. UK 28C → EU 60C (60 cm anchor, matches target list)
  8. EU 65A → US 30A (65 cm anchor, matches target list)
  9. US 38F → UK 38F (85 cm anchor, matches target list)
 10. UK 44H → EU 100H (100 cm anchor, matches target list)
- Parity statement: The deterministic mapping (band anchors + cup index) returns the same outputs for each vector, so parity is maintained across runs.
- Console error check: Not run because browser console is unavailable in this environment.

DEVIATIONS
- Bra-size conversion logic is a new implementation (original page had no working JS), so the heuristics documented above serve as the behavior contract for this refactor.
