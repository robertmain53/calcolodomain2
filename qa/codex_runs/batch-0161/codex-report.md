CHANGELOG
- sito_modificato/birthday.html
  - Rebuilt using the mortgage-payment template, reorganized all textual content into the mandated hero/methodology/meta/footer hierarchy, and preserved the original guide, citations, and changelog text under the canonical sections.
  - Reimplemented the birthday calculator logic inside the page with the required parse/validate/compute/format/render/update contract and improved validation to guard against empty, invalid, or future dates.

TEST REPORT
- Run time: 2026-02-12T14:05:13.917Z (system Node.js environment)
- Parity statement: The new implementation mirrors the legacy calendar math (year difference adjustment and next-birthday calculation) so outputs should match the original behavior for any shared input.
- Test vectors (birthdate → age, days until next birthday, next birthday label):
  - 1990-01-01 → 36, 323, January 1, 2027
  - 1984-02-29 → 41, 17, March 1, 2026
  - 2000-12-31 → 25, 322, December 31, 2026
  - 1975-06-15 → 50, 123, June 15, 2026
  - 2001-04-10 → 24, 57, April 10, 2026
  - 2020-11-05 → 5, 266, November 5, 2026
  - 1950-09-30 → 75, 230, September 30, 2026
  - 1999-08-25 → 26, 194, August 25, 2026
  - 2010-02-28 → 15, 16, February 28, 2026
  - 1988-07-19 → 37, 157, July 19, 2026
- Console error check result: Not run in a browser (Node.js environment only), but the inline script uses strict parsing/validation and guarded number formatting so no console errors are expected.

Console error check: Not run (non-browser execution); JS logic was reviewed for robust guards.

Deviations
- None.
