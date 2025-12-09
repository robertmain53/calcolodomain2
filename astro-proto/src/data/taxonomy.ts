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
    slug: "science-and-mathematics",
    name: "Science and mathematics",
    description:
      "Mathematics, physics, and unit conversion tools built for accuracy, proofs, and quick reference.",
    clusters: [
      { slug: "mathematics", name: "Mathematics" },
      { slug: "physics", name: "Physics" },
      { slug: "unit-conversion", name: "Unit Conversion" },
    ],
  },
  {
    slug: "health-and-lifestyle",
    name: "Health and Lifestyle",
    description:
      "Everyday wellness, nutrition, and sports calculators tuned for daily routines and aspirational living.",
    clusters: [
      { slug: "everyday", name: "Everyday" },
      { slug: "health", name: "Health" },
      { slug: "sports", name: "Sports" },
    ],
  },
  {
    slug: "financial",
    name: "Financial",
    description:
      "Business, investments, mortgages, planning, and tax tools that respect compliance and modern finance workflows.",
    clusters: [
      { slug: "business", name: "Business" },
      { slug: "investments", name: "Investments" },
      { slug: "mortgages-and-loans", name: "Mortgages and Loans" },
      { slug: "planning", name: "Planning" },
      { slug: "taxes-and-duties", name: "Taxes and Duties" },
    ],
  },
  {
    slug: "engineering",
    name: "Engineering",
    description:
      "Chemistry, civil & structural, electric, and mechanics calculators shaped for field pros and design teams.",
    clusters: [
      { slug: "chemistry", name: "Chemistry" },
      { slug: "civil-structural", name: "Civil & Structural" },
      { slug: "electric", name: "Electric" },
      { slug: "mechanics", name: "Mechanics" },
    ],
  },
];

export function findHub(slug: string): Hub | undefined {
  return taxonomy.find((h) => h.slug === slug);
}

export function findCluster(hubSlug: string, clusterSlug: string): Cluster | undefined {
  return findHub(hubSlug)?.clusters.find((c) => c.slug === clusterSlug);
}
