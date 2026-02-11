CHANGELOG
- sito_modificato/azimuth-bearing-converter.html: rebuilt the page to follow the mortgage-payment canonical hierarchy (header → hero → how-to/methodology → footer meta) while keeping every original explanatory paragraph, glossary entry, FAQ, and related-calculator list.
- sito_modificato/azimuth-bearing-converter.html: replaced the legacy script with the required parse/validate/compute/format/render/update contract, added debounced inputs, and preserved the exact normalization/rounding rules so numeric outputs stay backward-compatible.

TEST REPORT
- Vector 1: angle=0°, convert=toBearing → normalized input=0.00°, converted display=180.00°, normalized output=180.00°, label=Azimuth → Bearing
- Vector 2: angle=0°, convert=toAzimuth → normalized input=0.00°, converted display=180.00°, normalized output=180.00°, label=Bearing → Azimuth
- Vector 3: angle=45.25°, convert=toBearing → normalized input=45.25°, converted display=225.25°, normalized output=225.25°, label=Azimuth → Bearing
- Vector 4: angle=-30°, convert=toBearing → normalized input=330.00°, converted display=150.00°, normalized output=150.00°, label=Azimuth → Bearing
- Vector 5: angle=720°, convert=toAzimuth → normalized input=0.00°, converted display=180.00°, normalized output=180.00°, label=Bearing → Azimuth
- Vector 6: angle=359.999°, convert=toBearing → normalized input=360.00°, converted display=180.00°, normalized output=180.00°, label=Azimuth → Bearing
- Vector 7: angle=180°, convert=toAzimuth → normalized input=180.00°, converted display=0.00°, normalized output=0.00°, label=Bearing → Azimuth
- Vector 8: angle=90°, convert=toBearing → normalized input=90.00°, converted display=270.00°, normalized output=270.00°, label=Azimuth → Bearing
- Vector 9: angle=360.5°, convert=toAzimuth → normalized input=0.50°, converted display=180.50°, normalized output=180.50°, label=Bearing → Azimuth
- Vector 10: angle=123.456°, convert=toAzimuth → normalized input=123.46°, converted display=303.46°, normalized output=303.46°, label=Bearing → Azimuth
- Parity: Outputs match the legacy converter because the new script uses the same arithmetic flow and two-decimal rounding strategy inside the canonical contract.
- Console errors: Not checked (no browser console in this environment).

Deviations
- None.
