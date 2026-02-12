CHANGELOG
- sito_modificato/blasting-vibration.html: Rebuilt the page to match the mortgage-payment canonical layout (header, hero, methodology, meta, footer) while migrating the blasting vibration content into the appropriate sections, rerouting the JS into the parse/validate/compute/format/render/update contract, and adding a representative schedule/profile with CSV export toggles.

TEST REPORT
- Distance 100 m, Charge 50 kg → 0.04 mm/s
- Distance 250 m, Charge 75 kg → 0.02 mm/s
- Distance 10 m, Charge 20 kg → 0.27 mm/s
- Distance 1 m, Charge 1 kg → 1.00 mm/s
- Distance 500 m, Charge 200 kg → 0.01 mm/s
- Distance 30 m, Charge 5 kg → 0.06 mm/s
- Distance 120 m, Charge 150 kg → 0.04 mm/s
- Distance 8.5 m, Charge 60 kg → 0.46 mm/s
- Distance 400 m, Charge 10 kg → 0.01 mm/s
- Distance 67.3 m, Charge 43.2 kg → 0.05 mm/s
- Parity: Each vector uses the same formula (<code>k × W¹ᐟ³ / D</code> with <code>k=1</code>) and rounding (two decimal places) that the legacy page enforced, so the outputs stay in sync.

CONSOLE ERROR CHECK
- Not run (CLI environment lacks a browser console), but the new JS uses vanilla APIs without dynamic imports and should not throw errors once the page loads.

DEVIATIONS
- Introduced the canonical schedule/profile table plus toggle and CSV download even though the original page lacked a schedule; this is required by the mortgage-payment layout contract and the controls are tied to the same compute results without altering the core vibration model.
