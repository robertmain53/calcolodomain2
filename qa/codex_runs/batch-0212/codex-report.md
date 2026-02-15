CHANGELOG
- sito_modificato/btu-to-kwh.html
  - Rebuilt the entire page to follow the mortgage-payment layout hierarchy, kept the same header/breadcrumb/footer, and transplanted all guidance into the canonical hero → how-to → meta order.
  - Reimplemented the BTU/hr-to-cost calculator in the required parse/validate/compute/format/render pattern plus the energy converter tool within the "Full original guide (expanded)" area.
  - Preserved the original structured data, citations, formulas, and FAQ content, and added badges/metadata that reflect the original audit notes.

TEST REPORT
- Vector 1: BTU/hr 10000, hours 8, rate 0.15 → kW 2.93, kWh/day 23.45, cost $3.52
- Vector 2: BTU/hr 15000, hours 5.5, rate 0.18 → kW 4.40, kWh/day 24.18, cost $4.35
- Vector 3: BTU/hr 8000, hours 10, rate 0.13 → kW 2.34, kWh/day 23.45, cost $3.05
- Vector 4: BTU/hr 12000, hours 6, rate 0.20 → kW 3.52, kWh/day 21.10, cost $4.22
- Vector 5: BTU/hr 5000, hours 4, rate 0.11 → kW 1.47, kWh/day 5.86, cost $0.64
- Vector 6: BTU/hr 22000, hours 3, rate 0.16 → kW 6.45, kWh/day 19.34, cost $3.09
- Vector 7: BTU/hr 6500, hours 7.25, rate 0.14 → kW 1.90, kWh/day 13.81, cost $1.93
- Vector 8: BTU/hr 3000, hours 2, rate 0.19 → kW 0.88, kWh/day 1.76, cost $0.33
- Vector 9: BTU/hr 18000, hours 9, rate 0.17 → kW 5.28, kWh/day 47.48, cost $8.07
- Vector 10: BTU/hr 10500, hours 5, rate 0.165 → kW 3.08, kWh/day 15.39, cost $2.54
- Parity: These values match the legacy calculator’s conversion constants and rounding to two decimal places.
- Console errors: Not inspected (browser console unavailable). No script errors observed during CLI validation.

DEVIATIONS
- None.
