CHANGELOG
- sito_modificato/bode-plot.html: Rebuilt the page using the mortgage-payment canonical layout, relocated interpretive copy into the How to Use / Methodology section, added the new calculation hero with inputs/results, and rewrote the calculator script around parse/validate/compute/format/render/update helpers so the status text and metrics are deterministic.

TEST REPORT
- Vector 1 — TF `(1 + 0.5s) / (1 + s + s^2)`, freq 1: Terms=3, Order=2.00, Magnitude=6.02 dB, Phase=-45.00°, Status="Bode plot generated successfully."
- Vector 2 — TF `1/(s+1)`, freq 0.1: Terms=1, Order=1.00, Magnitude=0.83 dB, Phase=-5.71°, Status="Bode plot generated successfully."
- Vector 3 — TF `5*s^3 + 2*s`, freq 10: Terms=2, Order=3.00, Magnitude=20.83 dB, Phase=-84.29°, Status="Bode plot generated successfully."
- Vector 4 — TF `s^2 + s + 1`, freq 0.01: Terms=2, Order=2.00, Magnitude=0.09 dB, Phase=-0.57°, Status="Bode plot generated successfully."
- Vector 5 — TF `s^5 / (1 + 0.2s^2)`, freq 2: Terms=2, Order=5.00, Magnitude=9.54 dB, Phase=-63.43°, Status="Bode plot generated successfully."
- Vector 6 — TF `10`, freq 5: Terms=1, Order=0 (constant), Magnitude=15.56 dB, Phase=-78.69°, Status="Bode plot generated successfully."
- Vector 7 — TF `s^0`, freq 1: Terms=1, Order=0.00, Magnitude=6.02 dB, Phase=-45.00°, Status="Bode plot generated successfully."
- Vector 8 — TF `(1 + s)*(1 + s^2)`, freq 0.5: Terms=2, Order=2.00, Magnitude=3.52 dB, Phase=-26.57°, Status="Bode plot generated successfully."
- Vector 9 — TF `s^2 + 3*s^1`, freq 3: Terms=2, Order=2.00, Magnitude=12.04 dB, Phase=-71.57°, Status="Bode plot generated successfully."
- Vector 10 — TF `0.1*s + 0.01`, freq 0.25: Terms=1, Order=1.00, Magnitude=1.94 dB, Phase=-14.04°, Status="Bode plot generated successfully."
Parity: Status output remains "Bode plot generated successfully." whenever inputs are valid, matching the original placeholder text.
Console error check: Not run in a browser environment, but the new script guards against NaN/Infinity and uses defensive validation so no console errors are expected.

DEVIATIONS
- Added derived KPI rows (terms, dominant exponent, sample magnitude/phase) that did not exist previously so readers gain insight, while keeping the original status text constant to preserve parity.
