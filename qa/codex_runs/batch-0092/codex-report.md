# CHANGELOG
- sito_modificato/inverse-square-law-sound.html
  - Rebuilt the page around the canonical CalcDomain hero layout, keeping nav/footer while reorganizing guidance into explicit How to Use/Methodology, Formulas, Citations, and Changelog sections.
  - Replaced the legacy Tailwind/extra DOM with the canonical card grid, alert handling, and MathJax-enabled formula presentation.
  - Implemented the prescribed parsing/validation/compute/render/update flow so that the inverse square law logic (I₂ = I₁/d²) rounds identically to the legacy output.

# TEST REPORT
- Parity: Outputs for all vectors match the original formula-driven behavior (I₂ = I₁/d²) and share the legacy five-decimal rounding strategy.
- Console errors: None observed while exercising the calculator in a modern browser console (Chrome/Firefox devtools, no errors shown).
- Test vectors:
  1. I₁=1.5 W/m², d=10 m → 0.01500 W/m²
  2. I₁=2 W/m², d=5 m → 0.08000 W/m²
  3. I₁=0.75 W/m², d=2.5 m → 0.12000 W/m²
  4. I₁=10 W/m², d=15 m → 0.04444 W/m²
  5. I₁=5 W/m², d=1 m → 5.00000 W/m²
  6. I₁=3.14159 W/m², d=12.34 m → 0.02063 W/m²
  7. I₁=0.001 W/m², d=0.5 m → 0.00400 W/m²
  8. I₁=7.25 W/m², d=3.2 m → 0.70801 W/m²
  9. I₁=9.99 W/m², d=9.99 m → 0.10010 W/m²
  10. I₁=12 W/m², d=100 m → 0.00120 W/m²

# DEVIATIONS
- None.
