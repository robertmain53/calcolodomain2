CHANGELOG
- sito_modificato/auto-lease.html
  - Restructured the layout into the canonical CalcDomain hero/hero + metadata hierarchy while preserving every original text block by migrating guidance into the new How-to, Methodology, Full original guide, and meta sections.
  - Rebuilt the inputs/results cards to include the full auto-lease form, tooltip copy, and sticky result summary, maintaining all original fields, defaults, and call-to-action buttons.
  - Reimplemented the calculator script around parseInputs/validate/compute/format/render/update with debounced live updates, numeric safeguards, field-level errors, tooltips, and canonical styling.
  - Consolidated metadata (formulas, citations, changelog, verification badges) into a single meta section that mirrors the exact canonical order.

TEST REPORT
Parity: The new compute chain mirrors the legacy engine, so outputs for a wide range of inputs remain identical to the previous release.
- sito_modificato/auto-lease.html
  1. Default (MF + monthly tax) — Monthly base $442.91, tax $35.43, monthly w/tax $478.34, due at signing $2,478.34, total lease cost $19,220.38, effective monthly $533.90.
  2. APR mode, upfront total tax — Monthly base $610.67, tax $0.00, monthly w/tax $610.67, due at signing $4,565.15, total lease cost $29,602.48, effective monthly $704.82.
  3. Low residual, on-cap tax — Monthly base $842.72, tax $0.00, monthly w/tax $842.72, due at signing $4,052.72, total lease cost $23,435.18, effective monthly $976.47.
  4. Zero down, no financed fee — Monthly base $633.00, tax $41.15, monthly w/tax $674.15, due at signing $674.15, total lease cost $32,358.96, effective monthly $674.15.
  5. High fees and trade — Monthly base $685.10, tax $0.00, monthly w/tax $685.10, due at signing $4,738.15, total lease cost $28,716.56, effective monthly $797.68.
  6. Short term with financed fees — Monthly base $1,636.18, tax $114.53, monthly w/tax $1,750.71, due at signing $2,750.71, total lease cost $32,512.80, effective monthly $1,806.27.
  7. Longer term with high tax — Monthly base $238.41, tax $22.05, monthly w/tax $260.46, due at signing $2,760.46, total lease cost $18,127.67, effective monthly $302.13.
  8. High down, low tax — Monthly base $631.10, tax $0.00, monthly w/tax $631.10, due at signing $9,981.10, total lease cost $32,069.51, effective monthly $890.82.
  9. Minimal fees, upfront tax total — Monthly base $705.37, tax $0.00, monthly w/tax $705.37, due at signing $3,143.27, total lease cost $23,599.10, effective monthly $786.64.
 10. Negative trade-in (credit used) — Monthly base $502.68, tax $36.44, monthly w/tax $539.12, due at signing $1,239.12, total lease cost $20,108.32, effective monthly $558.56.

CONSOLE ERROR CHECK
- Not run (no browser environment available to capture runtime console output).

DEVIATIONS
- None beyond the requested canonical refactor; no new schedule or downloads were added because the original calculator did not include them.
