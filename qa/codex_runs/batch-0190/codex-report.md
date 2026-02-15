CHANGELOG
- `sito_modificato/born-haber-cycle.html`: Replaced the legacy layout with the mortgage-payment canonical hierarchy, reorganized guidance/formulas/citations, and consolidated the calculator logic into the shared parse/validate/compute/format/render contract.

TEST REPORT
- Vector 1: inputs {enthalpyFormation:-920, ionizationEnergy:520, electronAffinity:-350, bondDissociation:430, sublimationEnergy:200} -> lossSum=800.00, latticeEnergy=-1720.00 kJ/mol
- Vector 2: inputs {enthalpyFormation:-800, ionizationEnergy:450, electronAffinity:-310, bondDissociation:380, sublimationEnergy:180} -> lossSum=700.00, latticeEnergy=-1500.00 kJ/mol
- Vector 3: inputs {enthalpyFormation:-650, ionizationEnergy:600, electronAffinity:-220, bondDissociation:410, sublimationEnergy:210} -> lossSum=1000.00, latticeEnergy=-1650.00 kJ/mol
- Vector 4: inputs {enthalpyFormation:-1200, ionizationEnergy:700, electronAffinity:-400, bondDissociation:500, sublimationEnergy:240} -> lossSum=1040.00, latticeEnergy=-2240.00 kJ/mol
- Vector 5: inputs {enthalpyFormation:-400, ionizationEnergy:200, electronAffinity:-150, bondDissociation:200, sublimationEnergy:150} -> lossSum=400.00, latticeEnergy=-800.00 kJ/mol
- Vector 6: inputs {enthalpyFormation:-150, ionizationEnergy:100, electronAffinity:-80, bondDissociation:120, sublimimationEnergy:90} -> lossSum=230.00, latticeEnergy=-380.00 kJ/mol
- Vector 7: inputs {enthalpyFormation:-100, ionizationEnergy:50, electronAffinity:-40, bondDissociation:60, sublimationEnergy:30} -> lossSum=100.00, latticeEnergy=-200.00 kJ/mol
- Vector 8: inputs {enthalpyFormation:0, ionizationEnergy:10, electronAffinity:0, bondDissociation:20, sublimimationEnergy:30} -> lossSum=60.00, latticeEnergy=-60.00 kJ/mol
- Vector 9: inputs {enthalpyFormation:-2000, ionizationEnergy:980, electronAffinity:-430, bondDissociation:520, sublimationEnergy:260} -> lossSum=1330.00, latticeEnergy=-3330.00 kJ/mol
- Vector 10: inputs {enthalpyFormation:-500, ionizationEnergy:300, electronAffinity:-190, bondDissociation:350, sublimimationEnergy:160} -> lossSum=620.00, latticeEnergy=-1120.00 kJ/mol
- Parity: Recomputed outputs match the legacy formula above with a deterministic two-decimal rounding.
- Console: Not checked (calculator not loaded in a browser environment).

DEVIATIONS
- None.
