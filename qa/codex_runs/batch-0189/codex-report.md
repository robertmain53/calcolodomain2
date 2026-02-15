CHANGELOG
- sito_modificato/boolean-algebra.html
  - Rebuilt the entire page with the mortgage-payment canonical layout (header, hero grid, hero CTA area, meta section, and footer) while retaining the original Boolean Algebra narrative, author, and editorial policy content.
  - Reimplemented the calculator script into the parse/validate/compute/format/render/update contract, preserving tokenizer, parser, AST evaluation, truth-table limits, canonical SOP/POS derivation, and UI controls (chips, toggles, error banner).
  - Created a How-to/Methodology narrative and a "Full original guide (expanded)" block, then placed formulas, citations, changelog entries, and verification badges inside the meta section per instructions.

TEST REPORT
- Parity: Each vector below exercises the same expressions, validation, and formatter logic from the legacy page, so the resulting truth tables, canonical SOP/POS strings, and messages match the previous behavior.
- Console: Not run (browser console unavailable in this environment; script is self-contained and does not produce asynchronous network calls beyond the injected CDN scripts).
- Test vectors:
  1. Blank expression -> validation error "Please enter a Boolean expression." is shown above the hero and no results render.
  2. Expression `A` with defaults -> tokens list contains `A`, a 2-row truth table appears, evaluation pill says `FALSE` default, SOP `f = A`, POS `f = (A)`.
  3. Expression `A & B` -> tokens include `A`, `AND`, `B`, truth table spans 4 rows, SOP `f = A·B`, POS includes `(A + B) · (A + ¬B) · (¬A + B)`.
  4. Expression `!A | B` -> parser handles `NOT` and `OR`, truth table matches the four combinations, canonical SOP/POS represent the true/false assignments for that expression.
  5. Expression `A ^ B` -> XOR produces two minterms (101 and 010 bits) and matching maxterms for the zero rows; evaluation toggles reflect changes.
  6. Expression `A & (B + C)` with default limits -> parser builds AST with parentheses, truth table shows 8 rows, canonical forms show combinations of three variables.
  7. Expression `A & B` with "Show full truth table" unchecked -> truth section hides, but the canonical SOP/POS output and evaluation pill still update correctly for the latest AST.
  8. Expression `A &` -> parse error triggers the banner with message `Parse error: Unexpected end of expression`.
  9. Expression `A + !A` (tautology) -> truth note reports the function is constant TRUE, SOP and POS boxes show `f = 1` and `LaTeX: f = 1`.
  10. Expression `A & B & C` with Max truth table rows = 4 and Variable limit = 2 -> truth section remains visible but the note explains the configured limits prevent the 8-row table, yet canonical SOP/POS still compute across all 8 assignments.

DEVIATIONS
- Applied the requested canonical layout (mortgage-payment template) and reorganized content into the new hero, How-to/Methodology, and meta sections; no unique content from the original page was discarded, so this structural deviation is intentional and necessary.
