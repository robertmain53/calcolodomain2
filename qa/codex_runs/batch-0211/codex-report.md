CHANGELOG
- sito_modificato/btu-to-joules.html: Rebuilt the BTU-to-Joules calculator to match the mortgage-payment canonical hero layout, moved historical and FAQ content into the How-to section, preserved citations/changelog, and implemented the new parse/validate/compute/format/render/update pipeline for the dual energy/power converter.

TEST REPORT
- Energy 1 BTU: summary "1 BTU ≈ 1055.056 Joules" (raw {"btu":1,"j":1055.05585,"kj":1.0550559})
- Energy 100 BTU: summary "100 BTU ≈ 105505.6 Joules" (raw {"btu":100,"j":105505.585,"kj":105.505585})
- Energy 0.5 BTU: summary "0.5 BTU ≈ 527.5279 Joules" (raw {"btu":0.5,"j":527.527925,"kj":0.5275279})
- Energy 123456 J: summary "123456 Joules ≈ 117.0137 BTU" (raw {"btu":117.0137107,"j":123456,"kj":123.456})
- Energy 2 kJ: summary "2 Kilojoules ≈ 1.895634 BTU" (raw {"btu":1.8956342,"j":2000,"kj":2})
- Power 1 BTU/hr: summary "1 BTU/hr ≈ 0.2930711 Watts" (raw {"btu_hr":1,"w":0.2930711,"kw":0.0002931})
- Power 1000 Watts: summary "1000 Watts ≈ 3412.142 BTU/hr" (raw {"btu_hr":3412.1416351,"w":1000,"kw":0.9999998})
- Power 1.5 kW: summary "1.5 Kilowatts ≈ 5118.214 BTU/hr" (raw {"btu_hr":5118.2136752,"w":1500.0003583,"kw":1.5})
- Power 200 BTU/hr: summary "200 BTU/hr ≈ 58.61421 Watts" (raw {"btu_hr":200,"w":58.614214,"kw":0.0586142})
- Power 5 kW: summary "5 Kilowatts ≈ 17060.71 BTU/hr" (raw {"btu_hr":17060.7122506,"w":5000.0011942,"kw":5})
- Parity: All vector outputs match the legacy converter's constants and seven-significant-digit rounding behavior.
- Console error check: Not run (requires browser console).

DEVIATIONS
- None.
