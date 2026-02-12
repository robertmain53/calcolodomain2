CHANGELOG
- sito_modificato/body-fat.html: Rebuilt the page around the mortgage-payment canonical layout, introduced the new hero inputs/results structure, and moved all interpretive content into the How-to section with glossary, FAQ, and methodology plus verification metadata in pageMeta.
- sito_modificato/body-fat.html: Reimplemented the calculator script with the mandated parse/validate/compute/format/render contract, deterministic rounding, unit conversions, and the new radio-driven UI behavior while keeping all original citations and audit metadata.

TEST REPORT
- Metric male navy: bodyFat=16.2% (Fitness), fatMass=13.2 kg, leanMass=68.8 kg, BMI=25.3.
- Metric female navy: bodyFat=27.7% (Acceptable), fatMass=18.8 kg, leanMass=49.2 kg, BMI=25.0.
- US male navy: bodyFat=16.7% (Fitness), fatMass=15.1 kg, leanMass=75.6 kg, BMI=27.1.
- US female navy: bodyFat=29.2% (Acceptable), fatMass=19.9 kg, leanMass=48.2 kg, BMI=25.7.
- Metric male BMI: bodyFat=26.3% (Obese), fatMass=22.4 kg, leanMass=62.6 kg, BMI=26.8.
- Metric female BMI: bodyFat=34.2% (Obese), fatMass=23.9 kg, leanMass=46.1 kg, BMI=25.7.
- US male BMI: bodyFat=28.0% (Obese), fatMass=24.1 kg, leanMass=62.0 kg, BMI=27.3.
- US female BMI: bodyFat=39.1% (Obese), fatMass=26.6 kg, leanMass=41.4 kg, BMI=26.6.
- Metric male navy light: bodyFat=12.8% (Athlete), fatMass=9.2 kg, leanMass=62.8 kg, BMI=23.5.
- Metric female navy no weight: bodyFat=29.0% (Acceptable), fatMass=—, leanMass=—, BMI=— (weight optional).
- Parity statement: All vectors follow the original Navy and Deurenberg formulas, and the refactored script reproduces the same rounding behavior (fixed 1 decimal where expected) across units, sexes, and methods.
- Console error check: Node-based compute script finished without errors; no runtime errors were emitted during the test suite.
