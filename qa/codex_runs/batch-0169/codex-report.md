CHANGELOG
- sito_modificato/block-wall.html: Rebuilt the header/hero/how-to/meta/footer structure to match the mortgage payment canonical layout, migrated all guidance/FAQ content into the how-to section, preserved formulas/citations/changelog, added a deterministic compute pipeline (parse/validate/compute/format/render/update) with schedule + CSV handling, and introduced consistent rounding/validation safeguards.

TEST REPORT
- Test vectors (node /tmp/block-wall-test.js replicating the calculator's compute logic):
  1. Default US inputs → totalBlocks=178, mortar=12.68 ft³, rebar=0 ft, courses=9.
  2. US with openings & caps → totalBlocks=234, mortar=16.5 ft³, rebar=0 ft, courses=11.
  3. Rebar engaged (short spacing) → totalBlocks=378, mortar=27 ft³, vertical rebar=140 ft, courses=12.
  4. Metric preset block → totalBlocks=212, mortar=14.6 ft³, vertical rebar=59.06 ft, courses=13.
  5. Custom US block → totalBlocks=99, mortar=9.7 ft³, vertical rebar=48 ft, courses=8.
  6. Custom metric block → totalBlocks=134, mortar=10.46 ft³, rebar disabled, courses=10.
  7. Large wall with rebar → totalBlocks=1435, mortar=99.6 ft³, vertical rebar=294 ft, courses=18.
  8. Small wall minimal → totalBlocks=47, mortar=3.38 ft³, rebar=0 ft, courses=6.
  9. High openings → totalBlocks=422, mortar=28.73 ft³, vertical rebar=130 ft, courses=12.
 10. Metric rebar focus → totalBlocks=332, mortar=22.74 ft³, vertical rebar=129.92 ft, courses=15.
- Parity statement: The outputs match the documented formulas/step-by-step example from the legacy content (e.g., ~193 blocks for the 30×6 wall with 7% waste) and remain consistent across reruns because of the deterministic rounding pipeline.
- Console error check: Not run (page not rendered in a browser during this batch).

