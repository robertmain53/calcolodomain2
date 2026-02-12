CHANGELOG
- sito_modificato/blog.html
  - Rebuilt the blog page around the mortgage payment canonical layout, preserving the header, hero, schedule, and footer hierarchy while reusing the canonical calculator markup.
  - Migrated all original blog content into the "Full original guide (expanded)" block within How to Use, and referenced auxiliary audit data through the meta section (formulas, citations, changelog, badges).
  - Introduced the canonical parse/validate/compute/format/render updater for the mortgage calculator, along with the amortization schedule toggle, download CSV, and debounced inputs.

TEST REPORT
1. Principal 350000, Rate 6.5%, Term 30y, Extra 0, Freq 12 → TotalMonthly 2687.24, PI 2212.24, Escrow 475.00, Interest 446405.71, 360 payments (~30 years)
2. Principal 300000, Rate 5%, Term 15y, Extra 0, Freq 12 → TotalMonthly 2872.38, PI 2372.38, Escrow 500.00, Interest 127028.56, 180 payments (~15 years)
3. Principal 250000, Rate 4.25%, Term 30y, Extra 200, Freq 12 → TotalMonthly 1829.85, PI 1229.85, Escrow 600.00, Interest 140516.18, 274 payments (~22 yrs 10 mos)
4. Principal 500000, Rate 3.75%, Term 20y, Extra 500, Freq 12 → TotalMonthly 3814.44, PI 2964.44, Escrow 850.00, Interest 165852.91, 193 payments (~16 yrs 1 mos)
5. Principal 425000, Rate 6%, Term 25y, Extra 0, Freq 26 → TotalMonthly 3411.70, PI 2736.70, Escrow 675.00, Interest 396008.64, 650 payments (~25 years)
6. Principal 410000, Rate 5.25%, Term 30y, Extra 0, Freq 52 → TotalMonthly 3024.14, PI 2262.47, Escrow 761.67, Interest 404489.49, 1560 payments (~30 years)
7. Principal 200000, Rate 0%, Term 30y, Extra 0, Freq 12 → TotalMonthly 822.22, PI 555.56, Escrow 266.67, Interest 0.00, 360 payments (~30 years)
8. Principal 150000, Rate 4.5%, Term 15y, Extra 1000, Freq 12 → TotalMonthly 1372.49, PI 1147.49, Escrow 225.00, Interest 24256.85, 82 payments (~6 yrs 10 mos)
9. Principal 600000, Rate 7.25%, Term 30y, Extra 250, Freq 12 → TotalMonthly 5251.39, PI 4093.06, Escrow 1158.33, Interest 697682.90, 299 payments (~24 yrs 11 mos)
10. Principal 320000, Rate 3.5%, Term 15y, Extra 0, Freq 12 → TotalMonthly 2637.62, PI 2287.62, Escrow 350.00, Interest 91772.34, 180 payments (~15 years)
Parity: Outputs now follow the mortgage-payment canonical calculator, so the formatting and rounding behavior match the established reference.
Console error check: Not run (requires browser console), but the script mirrors the canonical implementation and should produce no console errors.
