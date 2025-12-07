import type { Locale } from "../config/site";
import { hubs } from "../config/site";

export type Hub = (typeof hubs)[number];

export type TemplateType = "visual" | "scientific" | "wizard" | "table" | "cockpit";

export interface FAQ {
  q: string;
  a: string;
}

export interface PageContent {
  intro: string;
  theory: string[];
  variables: string[];
  examples: string[];
  faqs: FAQ[];
}

export interface Taxonomy {
  hub: Hub;
  cluster: string;
}

export interface PageEntry {
  locale: Locale;
  slug: string[];
  title: string;
  description: string;
  primary: Taxonomy;
  secondary?: Taxonomy[];
  template: TemplateType;
  monetization?: string[];
  content: PageContent;
}

export const pages: PageEntry[] = [
  {
    locale: "en",
    slug: ["math-science", "length", "mm-to-inches"],
    title: "Millimeters to Inches Converter",
    description: "Convert millimeters to inches with decimal and fractional output plus significant figures.",
    primary: { hub: "Math & Science", cluster: "Length Conversions" },
    template: "visual",
    content: {
      intro:
        "High-precision mm → inch converter with decimal and fractional output, plus significant figures control.",
      theory: [
        "Exact factor: 1 inch = 25.4 mm (standardized in 1959 by international agreement).",
        "Formula: inches = millimeters / 25.4; reverse: millimeters = inches × 25.4.",
        "Use significant figures to reflect measurement uncertainty.",
      ],
      variables: ["Value", "Direction (mm ↔ in)", "Significant figures", "Fractional rounding (nearest 1/16)"],
      examples: [
        "50 mm → 1.9685 in (≈ 1 31/32) for 3D printing tolerances.",
        "200 mm → 7.8740 in for mechanical parts or displays.",
      ],
      faqs: [
        { q: "Why 25.4 is exact?", a: "The international inch was fixed at 25.4 mm in 1959; it is not an approximation." },
        { q: "Can I see fractional inches?", a: "Yes, output includes the nearest 1/16 inch and the decimal value." },
        { q: "How do significant figures work?", a: "Pick sig figs to match your input precision; results round accordingly." },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "typography", "typography-converter"],
    title: "Typography Unit Converter (px, pt, em, rem, %)",
    description: "Convert typography units with accessibility context and live preview.",
    primary: { hub: "Math & Science", cluster: "Typography & CSS Units" },
    template: "visual",
    content: {
      intro:
        "Convert px, pt, em, rem, and % with a live preview. Clarifies absolute vs relative units for accessible design.",
      theory: [
        "Absolute units: px, pt. Relative: em/rem/% depend on base font size (root or parent).",
        "1 pt = 1/72 inch; common mapping: 16 px ≈ 12 pt (browser default).",
        "Using rem/em supports WCAG: users can scale text without breaking layout.",
      ],
      variables: ["Base font size", "Size in px", "Size in pt", "Size in rem/em", "Percent"],
      examples: [
        "16 px with 16 px base → 1 rem = 12 pt = 100%.",
        "24 px heading → 1.5 rem; improves readability and accessibility.",
      ],
      faqs: [
        { q: "When to use rem vs em?", a: "Use rem for consistent sizing across components; em for contextual scaling within components." },
        { q: "Are px bad for accessibility?", a: "Px are absolute; rem/em adapt to user preferences, so they are recommended for text." },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "mass", "kg-to-lbs"],
    title: "Kilograms to Pounds Converter",
    description: "Convert kilograms to pounds and show weight under different gravity fields.",
    primary: { hub: "Math & Science", cluster: "Mass Conversions" },
    template: "scientific",
    content: {
      intro:
        "Convert kg to lb with a gravity selector to highlight mass vs weight on Earth, Moon, Mars, or Jupiter.",
      theory: [
        "Mass is intrinsic (kg); weight is force (N) = m × g. 1 kg ≈ 2.20462 lb (mass).",
        "Gravity differs by body; weight changes but mass stays constant.",
      ],
      variables: ["Mass in kg or lb", "Direction (kg ↔ lb)", "Gravity body (Earth, Moon, Mars, Jupiter)"],
      examples: [
        "70 kg → 154.324 lb; weight on Mars ≈ 259 N vs Earth ≈ 686 N.",
      ],
      faqs: [
        { q: "Is pound a mass unit?", a: "Pound (avoirdupois) is used for mass; weight in imperial is pound-force." },
        { q: "Why show gravity?", a: "To illustrate the difference between mass (constant) and weight (depends on g)." },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "length", "cm-to-inches"],
    title: "Centimeters to Inches Converter",
    description: "Convert centimeters to inches with decimal and fractional output and dual metric/imperial context.",
    primary: { hub: "Math & Science", cluster: "Length Conversions" },
    template: "visual",
    content: {
      intro:
        "Convert cm ↔ inches with fractional output and context for height, clothing, and paper sizes.",
      theory: [
        "Exact factor: 1 inch = 2.54 cm (1959 standard).",
        "Formula: inches = centimeters / 2.54; reverse: centimeters = inches × 2.54.",
        "Fractions help when working with feet/inches formats.",
      ],
      variables: ["Value", "Direction (cm ↔ in)", "Significant figures", "Fractional rounding"],
      examples: [
        "170 cm → 66.929 in (5 ft 6.9 in) for human height.",
      ],
      faqs: [
        { q: "Why fractions?", a: "Imperial drawings often use 1/16 in marks; fractions improve usability." },
        { q: "Paper sizes?", a: "Include A-series context (A4 is 21×29.7 cm ≈ 8.27×11.69 in)." },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "mass", "lbs-to-kg"],
    title: "Pounds to Kilograms Converter",
    description: "Convert pounds to kilograms with historical context and mass/weight distinction.",
    primary: { hub: "Math & Science", cluster: "Mass Conversions" },
    template: "scientific",
    content: {
      intro:
        "Convert lb → kg and see weight under different gravity; includes brief history of the pound.",
      theory: [
        "Factor: 1 lb = 0.45359237 kg exactly.",
        "Mass vs weight: pound-force vs pound-mass; SI mass is the kilogram.",
      ],
      variables: ["Mass in lb or kg", "Direction (lb ↔ kg)", "Gravity body selector"],
      examples: [
        "150 lb → 68.0389 kg; weight on Earth ≈ 667 N; on Moon ≈ 110 N.",
      ],
      faqs: [
        { q: "What is a slug?", a: "A slug is the imperial mass unit where 1 slug = 32.174 lb; rarely used outside engineering." },
        { q: "Who uses pounds today?", a: "Primarily US/UK; many countries have shifted to SI for trade and science." },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "energy", "btu-to-kwh"],
    title: "BTU to kWh Converter",
    description: "Convert BTU ↔ kWh with clarity on energy vs power and HVAC examples.",
    primary: { hub: "Math & Science", cluster: "Energy Conversions" },
    template: "scientific",
    content: {
      intro:
        "Convert BTU and kWh, with reminders on energy vs power (BTU/h vs kW) and HVAC/electrical contexts.",
      theory: [
        "1 kWh ≈ 3412 BTU; 1 BTU ≈ 0.00029307107 kWh.",
        "BTU: energy to raise 1 lb water by 1°F. kWh: 1 kW over one hour.",
        "Energy vs power: kWh/BTU measure energy; kW/BTU/h measure rate.",
      ],
      variables: ["Value", "Direction (BTU ↔ kWh)", "Significant figures"],
      examples: [
        "12,000 BTU/h AC ≈ 3.52 kW cooling capacity.",
        "1 kWh from a 1 kW load running for an hour ≈ 3412 BTU of energy.",
      ],
      faqs: [
        { q: "BTU or BTU/h?", a: "BTU is energy; BTU/h is power. This tool converts energy; use rates separately." },
        { q: "Why does the factor exist?", a: "It derives from mechanical equivalent of heat linking joules, BTU, and watt-hours." },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "length", "angstrom-to-nm"],
    title: "Ångström to Nanometer Converter",
    description: "Convert Å ↔ nm with scientific notation for nanoscience and spectroscopy contexts.",
    primary: { hub: "Math & Science", cluster: "Nano Scale Conversions" },
    template: "scientific",
    content: {
      intro:
        "Convert Ångström ↔ nanometer with scientific notation; includes context for crystallography, optics, and nano-tech.",
      theory: [
        "Relationship: 10 Å = 1 nm. Å and nm are both sub-micrometer length scales.",
        "Use scientific notation for clarity (e.g., 1.5e-10 m).",
      ],
      variables: ["Value", "Direction (Å ↔ nm)", "Significant figures", "Scientific notation"],
      examples: [
        "1.54 Å (C–C bond length) → 0.154 nm.",
        "500 nm (green light) → 5000 Å (visible spectrum context).",
      ],
      faqs: [
        { q: "Where is Å used?", a: "Common in crystallography and spectroscopy; nm dominates in nano-tech and biology." },
        { q: "Who was Ångström?", a: "Anders Jonas Ångström, pioneer in spectroscopy; the unit honors his work." },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "temperature", "kelvin-to-fahrenheit"],
    title: "Kelvin to Fahrenheit Converter",
    description: "Convert Kelvin ↔ Fahrenheit with Celsius intermediate and absolute-zero context.",
    primary: { hub: "Math & Science", cluster: "Temperature Conversions" },
    template: "scientific",
    content: {
      intro:
        "Convert K ↔ °F with Celsius intermediate, highlighting absolute zero and thermodynamic scale.",
      theory: [
        "Two-step: °C = K − 273.15; °F = °C × 9/5 + 32. Combined: °F = (K − 273.15) × 9/5 + 32.",
        "Kelvin is absolute (starts at 0 K); Fahrenheit is empirical; Celsius is water-based.",
      ],
      variables: ["Value", "Direction (K ↔ °F)", "Intermediate °C"],
      examples: [
        "300 K → 80.33 °F (26.85 °C) for ambient lab conditions.",
      ],
      faqs: [
        { q: "What is absolute zero?", a: "0 K is theoretical minimum thermal energy; −273.15 °C, −459.67 °F." },
        { q: "Where is Kelvin used?", a: "Astrophysics, materials science, cryogenics, gas laws." },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "angle", "degrees-to-radians"],
    title: "Degrees to Radians Converter",
    description: "Convert degrees ↔ radians with trig outputs and π relationships.",
    primary: { hub: "Math & Science", cluster: "Angles & Trigonometry" },
    template: "visual",
    content: {
      intro:
        "Convert angles between degrees and radians, with instant trig values and π-based intuition.",
      theory: [
        "Relationship: 360° = 2π rad → rad = deg × π/180; deg = rad × 180/π.",
        "Radians are the natural unit for calculus and physics (arc length equals radius).",
      ],
      variables: ["Degrees or radians", "Direction (deg ↔ rad)", "Trig outputs (sin, cos, tan)"],
      examples: [
        "90° → π/2 rad, sin=1, cos=0.",
        "45° → π/4 rad, sin=cos≈0.7071.",
      ],
      faqs: [
        { q: "Why use radians?", a: "They simplify derivatives/integrals of trig functions and model circular motion naturally." },
        { q: "How to express in π form?", a: "Divide by π to see multiples (e.g., π/6, π/4, π/3)." },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "volume", "cups-to-tablespoons"],
    title: "Cups to Tablespoons Converter",
    description: "Convert cups ↔ tablespoons with regional standards and mL output.",
    primary: { hub: "Math & Science", cluster: "Cooking & Volume" },
    template: "visual",
    content: {
      intro:
        "Convert cups and tablespoons with selectable standards (US, metric, imperial) and milliliter output.",
      theory: [
        "Factors depend on standard: e.g., US customary 1 cup = 236.588 mL and 1 tbsp = 14.7868 mL → 16 tbsp per cup.",
        "Volume conversions are exact for liquids; for dry ingredients, weight (grams) is more reliable.",
      ],
      variables: ["System selection", "Value", "Direction (cups ↔ tbsp)"],
      examples: [
        "1 US cup → 16 US tbsp → 236.59 mL.",
        "4 tbsp (metric) → 0.24 metric cup (≈ 60 mL).",
      ],
      faqs: [
        { q: "Which standard do you use?", a: "Choose US customary/legal, metric, or imperial to get the right factor." },
        { q: "Dry vs liquid?", a: "Use weight (grams) for dry goods; volume is best for liquids." },
      ],
    },
  },
];

export function findPage(
  locale: Locale,
  segments: string[],
): PageEntry | undefined {
  return pages.find(
    (p) =>
      p.locale === locale &&
      p.slug.length === segments.length &&
      p.slug.every((part, idx) => part === segments[idx]),
  );
}

export function relatedPages(page: PageEntry): PageEntry[] {
  const cluster = page.primary.cluster;
  const hub = page.primary.hub;
  return pages
    .filter(
      (p) =>
        p !== page &&
        p.locale === page.locale &&
        (p.primary.cluster === cluster || p.primary.hub === hub),
    )
    .slice(0, 5);
}
