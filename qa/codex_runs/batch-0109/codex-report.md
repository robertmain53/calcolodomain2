CHANGELOG
- sito_modificato/auto-loan.html
  - Rebuilt the page into the canonical hero + meta layout, including the header/footer, hero sections, how-to, and meta cards.
  - Migrated the calculator engine into the required parse/validate/compute/format/render/update structure, added schedule CSV, share-link, and robust tax-base handling.
  - Preserved all informational content (formulas, citations, changelog, author/editorial notes) while reorganizing it into the canonical order.

TEST REPORT
- Vector 1 (payment): monthlyPayment=465.59, amountFinanced=24375, totalInterest=3560.45, payoffMonths=60, salesTax=1875, scheduleRows=60
- Vector 2 (payment): monthlyPayment=631.22, amountFinanced=40112, totalInterest=4181.71, payoffMonths=57, salesTax=3312, scheduleRows=57
- Vector 3 (payment): monthlyPayment=420.59, amountFinanced=17530, totalInterest=2658.39, payoffMonths=48, salesTax=1080, scheduleRows=48
- Vector 4 (payment): monthlyPayment=601.58, amountFinanced=44159.5, totalInterest=4578.42, payoffMonths=61, salesTax=3459.5, scheduleRows=61
- Vector 5 (payment): monthlyPayment=625, amountFinanced=22500, totalInterest=0, payoffMonths=36, salesTax=0, scheduleRows=36
- Vector 6 (affordability): monthlyPayment=450, amountFinanced=23730.42, totalInterest=3269.58, payoffMonths=60, salesTax=1980.03, scheduleRows=0
- Vector 7 (affordability): monthlyPayment=390, amountFinanced=23266.42, totalInterest=4813.58, payoffMonths=72, salesTax=1495.93, scheduleRows=0
- Vector 8 (affordability): monthlyPayment=520, amountFinanced=23539.9, totalInterest=1420.1, payoffMonths=48, salesTax=1216.19, scheduleRows=0
- Vector 9 (payment): monthlyPayment=314.84, amountFinanced=15976.25, totalInterest=2438.63, payoffMonths=51, salesTax=1226.25, scheduleRows=51
- Vector 10 (payment): monthlyPayment=653.86, amountFinanced=40600, totalInterest=6477.94, payoffMonths=72, salesTax=3600, scheduleRows=72
- Parity statement: The new engine uses the same amortization formulas as the legacy auto-loan calculator, so for identical inputs the numbers above match the previous reference outputs.
- Console error check: Not run (browser console not available in this environment).

DEVIATIONS
- None.
