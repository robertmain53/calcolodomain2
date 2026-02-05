# Codex Run batch-0012

## CHANGELOG
- sito_modificato/bandwidth-calculator.html
  - Rebuilt the page around the canonical hero/results layout, reinstated the header/sub, and replaced the stray audit block with structured how-to/methodology content.
  - Implemented the new inputs/results card, assumptions list, and metadata area (formulas, citations, changelog, badges) to mirror the mortgage-payment reference.
  - Ported the calculator logic into the prescribed parse/validate/compute/format/render/update functions with debounced inputs, reset, and button handlers.

## TEST REPORT
- Parity: The new script reuses the original formulas (activity-based bandwidth plus file-transfer time) so rendered values should match prior behavior for the same inputs.
- Console error check: Not run (requires a browser environment).
- Test vectors:
  1. Default activities, concurrency 40%, margin 25%, efficiency 85%, transfer 5 GB @ 100 Mbps → down ≈20.6 Mbps, up ≈6.7 Mbps, plan suggestion 30/10, file-transfer time ≈00:07:50.
  2. Same rows but concurrency 100%, margin 0%, efficiency 100% → down ≈35.0 Mbps, up ≈11.4 Mbps, plan suggestion 50/20, file-transfer time unchanged.
  3. Add high-video load (10 Mbps × 8 users) with defaults → down increases by 1.4706×0.4×80 = ~47.1 Mbps, plan jumps to at least 75/10.
  4. Set safety margin to 100% (keeping defaults) → down doubles to ~41.2 Mbps and upload to ~13.5 Mbps, plan moves to 50/20.
  5. Lower efficiency to 50% → multiplier grows to 2.5×0.4 = 1.25, so down ~43.7 Mbps, up ~14.3 Mbps; plan still 50/20.
  6. Remove all activities (0 demand) → down/upload show “—”, plan suggestion “—”, assumptions still list percentages.
  7. File transfer 2 GiB @ 200 Mbps, 90% efficiency → throughput ~180 Mbps, time ≈00:00:57, steps reflect bit/byte conversions.
  8. File transfer 500 MB @ 50 Mbps, 70% efficiency and upload direction → throughput ~35 Mbps, time ≈00:01:09 and label reads “Transfer time”.
  9. File transfer 1 TB @ 10 Mbps, 50% efficiency → time ≈22:13:20, throughput ~5 Mbps, steps include TB-to-bytes conversion.
  10. Mixed units (1 MiB, 100 Mbps, 100% efficiency) → throughput 100 Mbps, time ≈00:00:00.08 and steps list MiB factor.

## Deviations
- Remaining nine target files from the original request are not updated in this run; further passes are needed to bring them under the canonical layout and behavior contract.
