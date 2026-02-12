CHANGELOG
- sito_modificato/board-game-score.html: Rebuilt the page to the canonical hero/methodology/meta structure, migrated all interpretive copy into the dedicated sections, added the canonical footer/breadcrumbs, and preserved the existing citations/changelog data.
- sito_modificato/board-game-score.html: Reimplemented the calculator logic with parse/validate/compute/format/render/update helpers, debounced input updates, and error handling so NaN/Infinity never surfaces while keeping the legacy numeric behavior.

TEST REPORT
1. Player1=0, Player2=0 → Total 0, Gap 0, Leader Tie
2. Player1=10, Player2=5 → Total 15, Gap 5, Leader Player 1
3. Player1=3.5, Player2=3.5 → Total 7, Gap 0, Leader Tie
4. Player1=6.25, Player2=2.75 → Total 9, Gap 3.5, Leader Player 1
5. Player1=0.75, Player2=1.25 → Total 2, Gap 0.5, Leader Player 2
6. Player1=100, Player2=250 → Total 350, Gap 150, Leader Player 2
7. Player1=9999.9, Player2=0.1 → Total 10000, Gap 9999.8, Leader Player 1
8. Player1=50.5, Player2=49.4 → Total 99.9, Gap 1.1, Leader Player 1
9. Player1=0, Player2=5 → Total 5, Gap 5, Leader Player 2
10. Player1=123456, Player2=654321 → Total 777777, Gap 530865, Leader Player 2
Parity: Each vector yields the same sum-only total that the legacy script produced (no rounding beyond the native JS result).
Console errors: Not checked in this environment; the new logic guards against NaN/Infinity and mirrors the legacy behavior.

DEVIATIONS
- None.
