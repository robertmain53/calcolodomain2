CHANGELOG
- sito_modificato/bike-cadence.html: Rebuilt the calculator page to follow the mortgage-payments canonical layout, preserved every informational section, and replaced the legacy script with a structured parse/validate/compute/format/render/update flow that mirrors the reference behavior.

TEST REPORT
- wheel=27,gear=3,speed=30 => cadence=117.89 RPM, circ=2.155 m, mpm=500.0 m/min
- wheel=26,gear=3.5,speed=25 => cadence=87.45 RPM, circ=2.075 m, mpm=416.7 m/min
- wheel=29,gear=2.9,speed=40 => cadence=151.40 RPM, circ=2.314 m, mpm=666.7 m/min
- wheel=28,gear=4.2,speed=22 => cadence=59.55 RPM, circ=2.234 m, mpm=366.7 m/min
- wheel=27.5,gear=3.25,speed=35 => cadence=124.65 RPM, circ=2.194 m, mpm=583.3 m/min
- wheel=26.5,gear=3.8,speed=18 => cadence=56.90 RPM, circ=2.115 m, mpm=300.0 m/min
- wheel=24,gear=2.5,speed=45 => cadence=238.73 RPM, circ=1.915 m, mpm=750.0 m/min
- wheel=28,gear=2.7,speed=50 => cadence=210.52 RPM, circ=2.234 m, mpm=833.3 m/min
- wheel=26,gear=3,speed=0 => cadence=0.00 RPM, circ=2.075 m, mpm=0.0 m/min
- wheel=29,gear=5,speed=60 => cadence=131.71 RPM, circ=2.314 m, mpm=1000.0 m/min
- Parity: All computed ranges match the original formula and rounding behavior (cadence is rounded to 2 decimals, auxiliary KPIs keep consistent precision).
- Console errors: Not available in this environment, but the renderer sanitizes every numeric path and there are no synchronous alerts or runtime logs.
- Deviations: None.
