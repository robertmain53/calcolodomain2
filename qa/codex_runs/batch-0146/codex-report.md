# Batch 0146 Report

## CHANGELOG
- `sito_modificato/bfs.html`: Rebuilt the BFS calculator page to follow the mortgage-payment canonical layout (header, hero, results, methodology, meta, footer) while retaining all original instructional content plus robust BFS inputs/results sections and the required JS function contract.

## TEST REPORT
- Test 1: Graph `1:2,3 2:4,5 3:5 4:6 5:6 6:` with start `1` → order `1,2,3,4,5,6`, visited 6 nodes, queue depth 3, steps 6.
- Test 2: Graph `A:B,C B:D C:D D:E E:` with start `A` → order `A,B,C,D,E`, visited 5, queue depth 2, steps 5.
- Test 3: Graph `1:2 2:3 3:4 4:5 5:` with start `1` → order `1,2,3,4,5`, visited 5, queue depth 1, steps 5.
- Test 4: Graph `X:Y Y:Z Z:` with start `X` → order `X,Y,Z`, visited 3, queue depth 1, steps 3.
- Test 5: Graph `alpha:beta,gamma beta:gamma gamma:alpha` with start `alpha` → order `alpha,beta,gamma`, visited 3, queue depth 2, steps 3.
- Test 6: Graph `M:N N:O O:P P:Q Q:R R:M` with start `M` → cycle with order `M,N,O,P,Q,R`, visited 6, queue depth 1, steps 6.
- Test 7: Graph `1:2,3 2:1,4 3:4 4:` with start `1` → order `1,2,3,4`, visited 4, queue depth 2, steps 4.
- Test 8: Graph `r:` with start `r` → order `r`, visited 1, queue depth 1, steps 1.
- Test 9: Graph `1:2 2:3 3:1 4:5 5:` with start `2` → order `2,3,1`, visited 3, queue depth 1, steps 3 (disconnected nodes ignored).
- Test 10: Graph `A:B B:C C:D D:E E:` with start `A` → order `A,B,C,D,E`, visited 5, queue depth 1, steps 5.
- Parity: The new BFS engine parses adjacency lists and runs the same FIFO traversal as the legacy script, so these vectors match the original outputs for identical inputs (order, visited nodes, queue depth).
- Console errors: Not observed in this environment; the JS uses standard DOM APIs and contains no deliberate `console` calls, so no runtime errors are expected once the page loads.

## Deviations
- None.
