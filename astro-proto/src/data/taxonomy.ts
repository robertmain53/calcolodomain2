export interface Cluster {
  slug: string;
  name: string;
  description?: string;
  // We'll add a 'tools' property to hold the calculators for this cluster
  tools?: {
    url: string;
    title: string;
  }[];
}

export interface Hub {
  slug: string;
  name: string;
  description?: string;
  clusters: Cluster[];
}

const hubDefinitions: Omit<Hub, "clusters">[] = [
  {
    slug: "science-and-mathematics",
    name: "Science and mathematics",
    description:
      "Mathematics, physics, and unit conversion tools built for accuracy, proofs, and quick reference.",
  },
  {
    slug: "health-and-lifestyle",
    name: "Health and Lifestyle",
    description:
      "Everyday wellness, nutrition, and sports calculators tuned for daily routines and aspirational living.",
  },
  {
    slug: "financial",
    name: "Financial",
    description:
      "Business, investments, mortgages, planning, and tax tools that respect compliance and modern finance workflows.",
  },
  {
    slug: "engineering",
    name: "Engineering",
    description:
      "Chemistry, civil & structural, electric, and mechanics calculators shaped for field pros and design teams.",
  },
];

let _taxonomy: Hub[];

export async function getTaxonomy(): Promise<Hub[]> {
  if (_taxonomy) {
    return _taxonomy;
  }

  const calculatorPages = await import.meta.glob<{
    frontmatter: { hub: string; cluster: string; title: string };
    url: string;
  }>("/src/pages/en/*/*/*.astro");

  const hubs: Record<string, Hub> = {};

  for (const hubDef of hubDefinitions) {
    hubs[hubDef.slug] = { ...hubDef, clusters: [] };
  }

  for (const path in calculatorPages) {
    const page = await calculatorPages[path]();
    const { hub: hubSlug, cluster: clusterSlug, title } = page.frontmatter;

    if (!hubSlug || !clusterSlug || !hubs[hubSlug]) continue;

    const hub = hubs[hubSlug];
    let cluster = hub.clusters.find((c) => c.slug === clusterSlug);

    if (!cluster) {
      // Create a capitalized name from the slug for the cluster name
      const name = clusterSlug
        .replace(/-/g, " ")
        .replace(/\b\w/g, (l) => l.toUpperCase());
      cluster = { slug: clusterSlug, name, tools: [] };
      hub.clusters.push(cluster);
    }

    cluster.tools = cluster.tools || [];
    cluster.tools.push({ url: page.url, title });
  }

  _taxonomy = Object.values(hubs).filter((hub) => hub.clusters.length > 0);
  _taxonomy.forEach((hub) =>
    hub.clusters.sort((a, b) => a.name.localeCompare(b.name))
  );

  return _taxonomy;
}

export async function findHub(slug: string): Promise<Hub | undefined> {
  const taxonomy = await getTaxonomy();
  return taxonomy.find((h) => h.slug === slug);
}

export async function findCluster(
  hubSlug: string,
  clusterSlug: string
): Promise<Cluster | undefined> {
  const hub = await findHub(hubSlug);
  return hub?.clusters.find((c) => c.slug === clusterSlug);
}
