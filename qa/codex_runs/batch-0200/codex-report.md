CHANGELOG
- sito_modificato/brick-calculator.html: rebuilt the page around the canonical hero + meta hierarchy, reordered the changelog/formula/citation sections ahead of the verification badges, and refactored the calculator script into the mandated parse/validate/compute/format/render/update pipeline while keeping all prior content (including the “Full original guide”) intact.

TEST REPORT
- Metric default: bricks=1,920, mortar=0.44 m³, cement=127.2 kg, sand=565.2 kg
- Metric double skin: bricks=4,916, mortar=1.13 m³, cement=325.6 kg, sand=1447.3 kg
- Metric high wastage: bricks=2,045, mortar=0.47 m³, cement=135.5 kg, sand=602.0 kg
- Metric small wall: bricks=320, mortar=0.07 m³, cement=21.2 kg, sand=94.2 kg
- Metric large wall: bricks=12,445, mortar=2.86 m³, cement=824.4 kg, sand=3663.8 kg
- Metric thin bricks: bricks=1,927, mortar=0.44 m³, cement=127.6 kg, sand=567.3 kg
- Imperial default: bricks=2,264, mortar=18.39 ft³, cement=330.6 lbs, sand=1469.4 lbs
- Imperial double skin: bricks=7,043, mortar=57.21 ft³, cement=1028.5 lbs, sand=4571.2 lbs
- Imperial low height: bricks=619, mortar=5.03 ft³, cement=90.4 lbs, sand=401.8 lbs
- Imperial custom joint: bricks=1,085, mortar=8.81 ft³, cement=158.4 lbs, sand=704.2 lbs

Console error check: not run (browser console unavailable) but the refactored calculator logic executed in Node without exceptions.

Deviations
- Header/navigation now matches the canonical mortgage-payment layout (search input, mobile toggle, pills) to satisfy the structural contract; all calculator content was retained underneath.
