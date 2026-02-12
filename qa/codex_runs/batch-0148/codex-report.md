CHANGELOG
- sito_modificato/big-number.html: Rebuilt the page using the mortgage-payment canonical structure, preserved all original content (inputs, methodology, audit details, citations, footer), and rewrote the calculator script to follow the canonical parse/validate/compute/format/render/update contract while keeping the large-integer math logic intact.

TEST REPORT
- sito_modificato/big-number.html:
  1. Add 123 + 456 → raw 579, grouped 579, sci 5.79 × 10^2, name "five hundred seventy-nine".
  2. Subtract 1 from 100000000000000000000 → raw 99999999999999999999, grouped 99,999,999,999,999,999,999, sci 9.999999999999 × 10^19, multi-word name for ninety-nine quintillion ... .
  3. Multiply 999999999999999 × 999999999999999 → raw 999999999999998000000000000001, grouped 999,999,999,999,998,000,000,000,000,001, sci 9.999999999999 × 10^29, name begins "nine hundred ninety-nine octillion...".
  4. Format 123456789012345678901234567890 → raw 123456789012345678901234567890, grouped 123,456,789,012,345,678,901,234,567,890, sci 1.234567890123 × 10^29, name begins "one hundred twenty-three octillion...".
  5. Add 0 + 123456789 → raw 123456789, grouped 123,456,789, sci 1.23456789 × 10^8, name "one hundred twenty-three million...".
  6. Subtract 12345 − 12345 → raw 0, grouped 0, sci 0, name "zero".
  7. Multiply 1 × 1 → raw 1, grouped 1, sci 1 × 10^0, name "one".
  8. Add 3141592653589793 + 2718281828459045 → raw 5859874482048838, grouped 5,859,874,482,048,838, sci 5.859874482048 × 10^15, name begins "five quadrillion...".
  9. Multiply 9999 × 2 → raw 19998, grouped 19,998, sci 1.9998 × 10^4, name "nineteen thousand nine hundred ninety-eight".
 10. Format 100200300400500600700800 → raw 100200300400500600700800, grouped 100,200,300,400,500,600,700,800, sci 1.002003004005 × 10^23, name begins "one hundred sextillion...".
  - Parity: The new script reuses the legacy big-number math helpers, so the above vectors were verified using a Node script that mirrors the page logic and produced identical outputs.
  - Console errors: Not run (browser not available in this environment).

Console error check statement:
- Console was not inspected; please validate manually in a browser.

Deviations:
- None beyond the required layout refactor; console logging was not captured because there was no browser session.
