export interface Cluster {
  slug: string;
  name: string;
  description?: string;
}

export interface Hub {
  slug: string;
  name: string;
  description?: string;
  clusters: Cluster[];
}

export const taxonomy: Hub[] = [
  {
    slug: "finance-business",
    name: "Finance & Business",
    description:
      "Mutui, investimenti, fiscalita e KPI aziendali organizzati in cluster semantici per decisioni rapide.",
    clusters: [
      { slug: "mortgages", name: "Mutui" },
      { slug: "investments", name: "Investimenti" },
      { slug: "taxes-it", name: "Tasse (IT)" },
      { slug: "planning", name: "Pianificazione & Pensione" },
      { slug: "business", name: "Aziendale & KPI" },
    ],
  },
  {
    slug: "engineering-construction",
    name: "Engineering & Construction",
    description:
      "Strutturale, calcestruzzo, impianti elettrici e termotecnica con strumenti a densita informativa elevata.",
    clusters: [
      { slug: "structural", name: "Strutturale" },
      { slug: "concrete", name: "Calcestruzzo" },
      { slug: "hydraulics", name: "Idraulica" },
      { slug: "electrical", name: "Elettrica" },
      { slug: "thermotechnics", name: "Termotecnica & HVAC" },
    ],
  },
  {
    slug: "math-science",
    name: "Math & Science",
    description:
      "Geometria, algebra, fisica e conversioni di unita con spiegazioni teoriche e notazione scientifica.",
    clusters: [
      { slug: "unit-conversions", name: "Conversione Unita" },
      { slug: "geometry", name: "Geometria" },
      { slug: "algebra", name: "Algebra" },
      { slug: "statistics", name: "Statistica" },
      { slug: "percentages", name: "Percentuali" },
      { slug: "physics", name: "Fisica" },
      { slug: "chemistry", name: "Chimica" },
      { slug: "typography", name: "Tipografia & CSS Units" },
    ],
  },
  {
    slug: "health-sport",
    name: "Health & Sport",
    description:
      "Benessere, sport e bisogni quotidiani mobile-first con metriche chiare e conversioni rapide.",
    clusters: [
      { slug: "body", name: "Corpo & Benessere" },
      { slug: "nutrition", name: "Nutrizione & Metabolismo" },
      { slug: "sport", name: "Sport & Prestazioni" },
      { slug: "everyday-cooking", name: "Everyday & Cucina" },
      { slug: "pregnancy", name: "Gravidanza" },
    ],
  },
];

export function findHub(slug: string): Hub | undefined {
  return taxonomy.find((h) => h.slug === slug);
}

export function findCluster(hubSlug: string, clusterSlug: string): Cluster | undefined {
  return findHub(hubSlug)?.clusters.find((c) => c.slug === clusterSlug);
}
