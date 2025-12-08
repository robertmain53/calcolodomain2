import type { Locale } from "../config/site";
import { hubs } from "../config/site";

export type Hub = (typeof hubs)[number];

export type TemplateType =
  | "visual"
  | "scientific"
  | "wizard"
  | "table"
  | "cockpit";

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
    slug: ["math-science", "unit-conversions", "mm-to-inches"],
    title: "Millimeters to Inches Converter",
    description:
      "Convert millimeters to inches with fractional output, sig figs, and the exact 25.4 mm standard.",
    primary: { hub: "Math & Science", cluster: "Conversione Unita" },
    template: "visual",
    content: {
      intro:
        "High-precision mm -> inch converter with fractional (1/16) view, sig figs, and context on the exact inch definition.",
      theory: [
        "Exact factor: 1 in = 25.4 mm, standardized in 1959 to remove rounding ambiguity.",
        "Formula: inches = millimeters / 25.4; reverse: millimeters = inches x 25.4 with sig-fig aware rounding.",
        "Fractional inches (1/16) align with imperial drawings; keep a reserved result area to avoid layout shift.",
        "Context: machining, 3D printing, and electronics footprints often bridge metric input to imperial specs.",
      ],
      variables: [
        "Millimeters or inches",
        "Direction (mm <-> in)",
        "Significant figures",
        "Fractional rounding (1/16 inch)",
      ],
      examples: [
        "50 mm -> 1.9685 in ~ 1 31/32 for tolerance checks on machined parts.",
        "220 mm -> 8.6614 in for PCB or display dimensions; the fraction clarifies drill template spacing.",
      ],
      faqs: [
        {
          q: "Why is 25.4 mm exact?",
          a: "The international yard and pound agreement fixed 1 inch at 25.4 mm in 1959; avoid rounded factors.",
        },
        {
          q: "Can I see both decimal and fraction?",
          a: "Yes. Decimal plus 1/16 fraction helps reconcile metric specs with imperial shop drawings.",
        },
        {
          q: "How do sig figs help?",
          a: "They carry measurement uncertainty through the conversion instead of showing misleading precision.",
        },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "typography", "typography-converter"],
    title: "Typography Unit Converter (px, pt, em, rem, %)",
    description:
      "Convert typography units with live preview, relative vs absolute guidance, and accessibility context.",
    primary: { hub: "Math & Science", cluster: "Tipografia & CSS Units" },
    template: "visual",
    content: {
      intro:
        "Convert px, pt, em, rem, and % with a live preview that shows how base font size affects everything else.",
      theory: [
        "Absolute units: px, pt. Relative: em/rem/% depend on parent or root font size; vw/vh use viewport.",
        "1 pt = 1/72 inch; browsers commonly map 16 px ~ 12 pt at default settings.",
        "Using rem/em is a WCAG-friendly pattern: text scales with user preferences instead of breaking layouts.",
        "Rem ties to the root (<html>) font size; em stacks on the parent, so nesting multiplies values.",
      ],
      variables: ["Base font size", "px", "pt", "rem", "em", "% preview"],
      examples: [
        "16 px base -> 1 rem = 16 px = 12 pt = 100%.",
        "20 px heading with 16 px base -> 1.25 rem; lowering base to 15 px keeps rem proportional.",
      ],
      faqs: [
        {
          q: "When to use rem vs em?",
          a: "Use rem for global consistency (typography scale); use em for contextual scaling inside components.",
        },
        {
          q: "How does user zoom affect this?",
          a: "Relative units respect user zoom and OS accessibility settings, keeping line wraps and contrast predictable.",
        },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "unit-conversions", "kg-to-lbs"],
    title: "Kilograms to Pounds Converter",
    description:
      "Convert kilograms to pounds, highlight mass vs weight, and show planetary gravity effects.",
    primary: { hub: "Math & Science", cluster: "Conversione Unita" },
    template: "scientific",
    content: {
      intro:
        "Convert kg <-> lb with a gravity selector to show how weight changes on Earth, Moon, Mars, or Jupiter.",
      theory: [
        "Mass is intrinsic (kg); weight is force: F = m x g. 1 kg ~ 2.20462 lb (mass) under standard gravity.",
        "Gravity differs by body (Earth 9.80665 m/s^2, Moon 1.62, Mars 3.71, Jupiter 24.79), so weight changes while mass stays constant.",
        "Keep mass constant across bodies to highlight the physics difference vs weight-based forces.",
      ],
      variables: [
        "Mass in kg or lb",
        "Direction (kg <-> lb)",
        "Gravity body selector",
      ],
      examples: [
        "70 kg -> 154.324 lb; weight on the Moon ~ 113.4 N vs Earth ~ 686 N.",
        "150 lb -> 68.0389 kg; on Mars the same mass would weigh ~ 252 N.",
      ],
      faqs: [
        {
          q: "Is pound a mass or force?",
          a: "Pound (avoirdupois) is used for mass; pound-force is the force under standard gravity.",
        },
        {
          q: "Why include gravity?",
          a: "It turns an ordinary converter into a quick physics lesson on mass vs weight.",
        },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "unit-conversions", "cm-to-inches"],
    title: "Centimeters to Inches Converter",
    description:
      "Convert centimeters to inches with fractional output, feet+inches helper, and visual ruler.",
    primary: { hub: "Math & Science", cluster: "Conversione Unita" },
    template: "visual",
    content: {
      intro:
        "Convert cm <-> in with fractional output, a feet+inches helper, and visuals for clothing sizes, human height, and paper formats.",
      theory: [
        "Exact factor: 1 inch = 2.54 cm (international inch standard).",
        "Formulas: inches = centimeters / 2.54; centimeters = inches x 2.54; feet = inches / 12 for mixed units.",
        "Fractions (1/16) align with tape measures; reserve stable result space to avoid CLS.",
        "Context: apparel sizing, body measurements, paper standards (A-series), and woodworking.",
      ],
      variables: [
        "Centimeters or inches",
        "Direction (cm <-> in)",
        "Fractional inches (1/16)",
        "Feet+inches helper",
      ],
      examples: [
        "170 cm -> 66.929 in ~ 5 ft 6.9 in (height reference).",
        "21 x 29.7 cm (A4) -> 8.27 x 11.69 in; 30 cm shelf depth -> 11.81 in.",
      ],
      faqs: [
        {
          q: "Why show fractions?",
          a: "Imperial plans and tape measures use fractions; this bridges them with metric inputs.",
        },
        {
          q: "Can I switch to feet+inches?",
          a: "Use the helper to express decimal inches as ft+in for quick readability.",
        },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "unit-conversions", "lbs-to-kg"],
    title: "Pounds to Kilograms Converter",
    description:
      "Convert pounds to kilograms with imperial context, slug unit mention, and gravity insights.",
    primary: { hub: "Math & Science", cluster: "Conversione Unita" },
    template: "scientific",
    content: {
      intro:
        "Convert lb -> kg, highlight the pound's history, and show gravity-weight differences for an imperial-first audience.",
      theory: [
        "Exact factor: 1 lb = 0.45359237 kg; 1 slug = 32.174 lb (rare, but shows imperial mass standard).",
        "Mass vs weight: pound-force vs pound-mass; SI anchor is the kilogram.",
        "Cultural context: US/UK still use pounds widely; scientific work defaults to SI kilograms/Newtons.",
      ],
      variables: [
        "Mass in lb or kg",
        "Direction (lb <-> kg)",
        "Gravity selector",
      ],
      examples: [
        "150 lb -> 68.0389 kg; on the Moon the same mass weighs ~ 110.2 N.",
        "20 lb dumbbell -> 9.0718 kg; confirms gym plates vs metric equipment.",
      ],
      faqs: [
        {
          q: "What is a slug?",
          a: "A slug is the imperial mass unit where 1 slug = 32.174 lb; it keeps F=ma consistent in imperial equations.",
        },
        {
          q: "Who still uses pounds?",
          a: "Primarily the US and parts of the UK/Canada; SI kilograms are standard in science and trade elsewhere.",
        },
      ],
    },
  },
  {
    locale: "en",
    slug: ["engineering-construction", "thermotechnics", "btu-to-kwh"],
    title: "BTU to kWh Converter",
    description:
      "Convert BTU <-> kWh with clear separation of energy vs power and HVAC-ready examples.",
    primary: {
      hub: "Engineering & Construction",
      cluster: "Termotecnica & HVAC",
    },
    secondary: [{ hub: "Math & Science", cluster: "Conversione Unita" }],
    template: "scientific",
    content: {
      intro:
        "Convert BTU and kWh with sig figs, explain BTU vs BTU/h, and anchor the results in HVAC and electrical contexts.",
      theory: [
        "Energy link: 1 kWh ~ 3412 BTU; inverse 1 BTU ~ 0.00029307107 kWh.",
        "Definitions: BTU heats 1 lb of water by 1 degF; kWh is 1 kW sustained for one hour.",
        "Energy vs power: kWh/BTU are energy; kW/BTU/h are rates. Avoid mixing them when sizing equipment.",
        "Standardization note: use decimal precision and stabilize result layout to avoid CLS when toggling direction.",
      ],
      variables: [
        "Energy value",
        "Direction (BTU <-> kWh)",
        "Significant figures",
      ],
      examples: [
        "12,000 BTU/h AC ~ 3.52 kW cooling capacity (energy per hour when steady).",
        "5 kWh from a home battery ~ 17,060 BTU of stored energy.",
      ],
      faqs: [
        {
          q: "BTU or BTU/h?",
          a: "BTU is energy; BTU/h is power. This tool converts energy-size equipment with BTU/h or kW separately.",
        },
        {
          q: "Where does 3412 come from?",
          a: "It ties the joule definition to the mechanical equivalent of heat linking watt-hours and BTU.",
        },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "unit-conversions", "angstrom-to-nm"],
    title: "Angstrom to Nanometer Converter",
    description:
      "Convert A <-> nm with scientific notation for spectroscopy, crystallography, and nano-tech.",
    primary: { hub: "Math & Science", cluster: "Conversione Unita" },
    template: "scientific",
    content: {
      intro:
        "Convert Angstrom <-> nanometer with scientific notation and nano-scale context for optics, materials, and biology.",
      theory: [
        "Relationship: 1 nm = 10 A. Both are sub-microscopic units used for atomic spacing and wavelengths.",
        "Scale context: visible light spans ~380-750 nm (3,800-7,500 A); DNA helix diameter ~ 2.4 nm (24 A).",
        "Notation: scientific notation (e.g., 1.54e-10 m) is standard for reporting A-level distances.",
        "History: the angstrom honors Anders Jonas Angstrom, a spectroscopy pioneer.",
      ],
      variables: [
        "Value",
        "Direction (A <-> nm)",
        "Scientific notation output",
        "Significant figures",
      ],
      examples: [
        "1.54 A (C-C bond) = 0.154 nm.",
        "550 nm (green light) = 5500 A; a 3 A lattice spacing = 0.3 nm.",
      ],
      faqs: [
        {
          q: "Why still use A?",
          a: "A is common shorthand in crystallography and spectroscopy; nm is SI-preferred for publication.",
        },
        {
          q: "Can I trust sci-notation output?",
          a: "Yes-use it to keep numbers readable while retaining magnitude and sig figs.",
        },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "unit-conversions", "kelvin-to-fahrenheit"],
    title: "Kelvin to Fahrenheit Converter",
    description:
      "Convert K <-> F with zero-absolute context, combined formula, and scale comparisons.",
    primary: { hub: "Math & Science", cluster: "Conversione Unita" },
    template: "visual",
    content: {
      intro:
        "Convert Kelvin to Fahrenheit (and back) with the combined formula, zero-absolute reminder, and examples across lab and astrophysics ranges.",
      theory: [
        "Kelvin is absolute: 0 K = absolute zero. Celsius offset: C = K - 273.15; Fahrenheit: F = C x 9/5 + 32.",
        "Combined forward: F = (K - 273.15) x 9/5 + 32; inverse: K = (F - 32) x 5/9 + 273.15.",
        "Usage: Kelvin in thermodynamics, astrophysics, and cryogenics; Fahrenheit in US everyday contexts.",
      ],
      variables: ["Temperature in K or F", "Direction (K <-> F)"],
      examples: [
        "300 K -> 80.33 F (room temp ~ 293 K = 68 F).",
        "77 F -> 298.15 K (~ 25 C, lab ambient); 4 K (liquid helium) -> -452.47 F.",
      ],
      faqs: [
        {
          q: "Why Kelvin instead of Celsius?",
          a: "Absolute temperatures make thermodynamic equations valid (ideal gas law, entropy, black-body radiation).",
        },
        {
          q: "What is absolute zero?",
          a: "0 K is the theoretical minimum thermal energy; particles have minimal motion.",
        },
      ],
    },
  },
  {
    locale: "en",
    slug: ["math-science", "unit-conversions", "degrees-to-radians"],
    title: "Degrees to Radians Converter",
    description:
      "Convert degrees <-> radians with a unit-circle visual, pi multiples, and trig outputs.",
    primary: { hub: "Math & Science", cluster: "Conversione Unita" },
    template: "visual",
    content: {
      intro:
        "Convert degrees and radians with unit-circle visuals, pi-based forms, and live trig values to reinforce the natural radian definition.",
      theory: [
        "Radians link arc length to radius: 360 deg = 2pi rad -> rad = deg x pi/180; deg = rad x 180/pi.",
        "Radians simplify calculus and physics (derivatives/integrals of trig functions, angular velocity).",
        "Visual aid: label common angles (30 deg, 45 deg, 60 deg, 90 deg, 180 deg) as multiples of pi to speed recall.",
      ],
      variables: [
        "Degrees or radians",
        "Direction (deg <-> rad)",
        "Trig outputs (sin, cos, tan)",
      ],
      examples: [
        "90 deg -> pi/2 rad, sin=1, cos=0.",
        "30 deg -> pi/6 rad, sin=0.5, cos~0.8660; 2 rad -> 114.592 deg.",
      ],
      faqs: [
        {
          q: "Why use radians?",
          a: "They are the natural angle unit for calculus, physics, and engineering formulas.",
        },
        {
          q: "How to express in pi form?",
          a: "Divide by pi to see multiples (e.g., pi/6, pi/4, pi/3) and reduce fractions.",
        },
      ],
    },
  },
  {
    locale: "en",
    slug: ["health-sport", "everyday-cooking", "cups-to-tablespoons"],
    title: "Cups to Tablespoons Converter",
    description:
      "Convert cups <-> tablespoons with regional standards, mL output, and a dry vs liquid warning.",
    primary: { hub: "Health & Sport", cluster: "Everyday & Cucina" },
    template: "visual",
    content: {
      intro:
        "Convert cups and tablespoons with selectable standards (US customary/legal, metric, imperial), show mL, and remind when to use weight for dry goods.",
      theory: [
        "Factors depend on the standard: US customary 1 cup = 236.588 mL and 1 tbsp = 14.7868 mL -> 16 tbsp per cup.",
        "Metric: 1 cup = 250 mL, 1 tbsp = 15 mL; Imperial: 1 cup = 284.131 mL, 1 tbsp = 17.7582 mL.",
        "Volume conversions suit liquids; dry ingredients vary by density, so grams are safer for baking accuracy.",
      ],
      variables: [
        "System selection",
        "Value",
        "Direction (cups <-> tbsp)",
        "Milliliter output",
      ],
      examples: [
        "1 US cup -> 16 US tbsp -> 236.59 mL (sauces, stock).",
        "4 tbsp (metric) -> 0.24 metric cup ~ 60 mL; 2 imperial tbsp -> ~1/8 imperial cup.",
      ],
      faqs: [
        {
          q: "Which standard do you use?",
          a: "Pick US customary/legal, metric, or imperial to avoid regional mismatches.",
        },
        {
          q: "Dry vs liquid?",
          a: "Use weight (grams) for flour/sugar; volume is accurate for liquids and thin batters.",
        },
        {
          q: "Can I convert to teaspoons or ounces?",
          a: "Use the standards table to infer tsp and fl oz; stick to one system per recipe.",
        },
      ],
    },
  },
];

export function findPage(
  locale: Locale,
  segments: string[]
): PageEntry | undefined {
  return pages.find(
    (p) =>
      p.locale === locale &&
      p.slug.length === segments.length &&
      p.slug.every((part, idx) => part === segments[idx])
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
        (p.primary.cluster === cluster || p.primary.hub === hub)
    )
    .slice(0, 5);
}
