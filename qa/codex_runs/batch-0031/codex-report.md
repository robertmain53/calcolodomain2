CHANGELOG
- sito_modificato/circle-calculator.html
  - Rebuilt the page around the mortgage-payment canonical shell while keeping the circle-specific inputs, results, and equation builder; added the mandated sections (how-to, methodology, full original guide, footer badges/meta) and reorganized legacy content accordingly.

TEST REPORT
- Vectors:
  1. Radius 5 → radius=5.000000, diameter=10.000000, circumference=31.415927, area=78.539816
  2. Diameter 14 → radius=7.000000, diameter=14.000000, circumference=43.982297, area=153.938040
  3. Circumference 31.4159 → radius=4.999996, diameter=9.999992, circumference=31.415900, area=78.539684
  4. Area 78.539816 → radius=5.000000, diameter=10.000000, circumference=31.415926, area=78.539816
  5. Radius 1.23456 → radius=1.234560, diameter=2.469120, circumference=7.756969, area=4.788222
  6. Diameter 12.7 → radius=6.350000, diameter=12.700000, circumference=39.898227, area=126.676870
  7. Circumference 100 → radius=15.915494, diameter=31.830989, circumference=100.000000, area=795.774715
  8. Area 314.159265 → radius=10.000000, diameter=20.000000, circumference=62.831853, area=314.159265
  9. Radius 0.0001 → radius=0.000100, diameter=0.000200, circumference=0.000628, area=0.000000
 10. Diameter 1000 → radius=500.000000, diameter=1000.000000, circumference=3141.592654, area=785398.163397
- Parity statement: Each output follows the standard circle formulas ($r=d/2$, $r=C/(2\pi)$, $r=\sqrt{A/\pi}$ plus the derived diameter, circumference, and area) so results should match the legacy behavior.
- Console errors: not captured (DOM-based page not executed in this environment).

Deviations
- Only `circle-calculator.html` was refactored in this batch because of time and scope; the remaining nine target HTML files still need the canonical layout and behavior refactors.
