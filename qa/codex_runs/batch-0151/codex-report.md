CHANGELOG
- sito_modificato/bike-gear.html
  - Rebuilt the entire page to mirror the mortgage payment canonical layout (header, calc hero, how-to, meta, footer) while moving every piece of original content into the correct section (methodology, glossary, example, FAQ, formulas, citations, changelog).
  - Added a structured calculator card with branded inputs and results plus a new JS engine (parseInputs/validate/compute/format/render/update) that keeps rounding deterministic and prevents NaN/Infinity.
  - Preserved the audit metadata, citations, and changelog entries inside the meta section, then reintroduced related calculators/verification badges consistent with the canon.

TEST REPORT
- sitio_modificato/bike-gear.html
  - Vectors tested (wheelDiameter-crankLength-frontTeeth-rearTeeth => gearRatio, frontRear, wheelCrank, gearInches):
    - 26-170-50-11 => 0.70, 4.55, 0.15, 118.18
    - 27.5-165-52-12 => 0.72, 4.33, 0.17, 119.17
    - 29-175-48-14 => 0.57, 3.43, 0.17, 99.43
    - 26-170-34-32 => 0.16, 1.06, 0.15, 27.63
    - 27-170-36-20 => 0.29, 1.80, 0.16, 48.60
    - 24-160-44-16 => 0.41, 2.75, 0.15, 66.00
    - 29-170-52-11 => 0.81, 4.73, 0.17, 137.09
    - 26.5-168-42-18 => 0.37, 2.33, 0.16, 61.83
    - 28-165-56-13 => 0.73, 4.31, 0.17, 120.62
    - 27-172-38-24 => 0.25, 1.58, 0.16, 42.75
  - Parity: All outputs match the original gear ratio formula rounded to two decimals, so the updated calculator reproduces legacy results for the tested vectors.
  - Console errors: Not checked in a browser; Node-based validation script ran cleanly and no runtime errors were observed in this environment.

DEVIATIONS
- None.
