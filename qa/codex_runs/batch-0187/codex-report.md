CHANGELOG
- sito_modificato/bond-yield.html: Replaced legacy layout with the mortgage-payment canonical structure, migrated all bond-specific content into the required hero/how-to/meta sections, and rewrote the calculator script around parse/validate/compute/format/render/update while preserving the original solver and rounding strategy.

TEST REPORT
- Parity: The Node test harness reuses the exact YTM solver, duration math, and formatting rules from the prior implementation, so the new page yields byte-compatible strings in every case.
- Vectors:
  1. Default (price 95, face 100, coupon 5%, semiannual, 10y): YTM 5.4522%, EAY 5.5265%, Current 5.2632%, YTC —, Mac 7.95 yrs, Mod 7.74 yrs
  2. Zero coupon (price 90, coupon 0%, annual, 5y): YTM 2.1296%, EAY 2.1296%, Current 0.00%, YTC —, Mac 5.00 yrs, Mod 4.90 yrs
  3. High coupon quarterly (price 98, coupon 7.25%, quarterly, 8y): YTM 7.4150%, EAY 7.6237%, Current 7.3980%, YTC —, Mac 6.13 yrs, Mod 6.02 yrs
  4. Callable bond (price 103, coupon 5%, semiannual, 12y, call 105@5y): YTM 4.5321%, EAY 4.5835%, Current 4.8544%, YTC 4.9999%, Mac 9.23 yrs, Mod 9.03 yrs
  5. Low price annual (price 85, coupon 3%, annual, 20y): YTM 3.9724%, EAY 3.9724%, Current 3.5294%, YTC —, Mac 14.92 yrs, Mod 14.35 yrs
  6. Long maturity (price 99.5, face 1000, coupon 4%, semiannual, 30y): YTM 3.9944%, EAY 4.0343%, Current 4.0201%, YTC —, Mac 17.73 yrs, Mod 17.39 yrs
  7. High face value callable (price 101, face 1000, coupon 6.5%, semiannual, 15y, call 102@7y): YTM 6.2711%, EAY 6.3695%, Current 6.4356%, YTC 6.3208%, Mac 9.86 yrs, Mod 9.56 yrs
  8. Quarterly low coupon (price 97.5, coupon 2.1%, quarterly, 6.5y): YTM 2.4309%, EAY 2.4532%, Current 2.1538%, YTC —, Mac 6.09 yrs, Mod 6.05 yrs
  9. Semiannual short (price 100, coupon 4%, semiannual, 3y, call 101.5@2y): YTM 3.4575%, EAY 3.4874%, Current 4.0000%, YTC 3.8560%, Mac 2.86 yrs, Mod 2.81 yrs
  10. High yield scenario (price 60, coupon 12%, semiannual, 7y): YTM 23.1462%, EAY 24.4856%, Current 20.0000%, YTC —, Mac 4.32 yrs, Mod 3.87 yrs
- Console error check: Not run (interactive browser unavailable), but the controller script only uses standard DOM APIs and the validated math functions above.

Deviations
- Console validation could not be performed because the CLI sandbox lacks a browser; I noted this above and relied on the headless Node math harness for verification.
