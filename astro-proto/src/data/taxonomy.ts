import fsp from "node:fs/promises";
import nodePath from "node:path";

export interface Cluster {
  slug: string;
  name: string;
  description?: string;
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

type CsvRow = {
  slug: string;
  title: string;
  hub: string;
  cluster: string;
};

const CSV_PATH = nodePath.join(process.cwd(), "..", "calc-2.csv");

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
let _csvRecords: CsvRow[] | null = null;

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function humanizeSlug(slug: string): string {
  return slug
    .split(/[-_]/)
    .filter(Boolean)
    .map((token) => token.charAt(0).toUpperCase() + token.slice(1))
    .join(" ");
}

async function loadCsvRecords(): Promise<CsvRow[]> {
  if (_csvRecords) {
    return _csvRecords;
  }

  try {
    const raw = await fsp.readFile(CSV_PATH, "utf8");
    const lines = raw
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter((line) => line.length > 0);
    if (lines.length < 2) {
      _csvRecords = [];
      return _csvRecords;
    }

    const headers = lines[0]
      .split(",")
      .map((header) => header.trim().toLowerCase());
    const titleIdx = headers.indexOf("title");
    const slugIdx = headers.indexOf("slug");
    const hubIdx = headers.indexOf("hub");
    const clusterIdx = headers.indexOf("cluster");
    if (titleIdx === -1 || slugIdx === -1 || hubIdx === -1 || clusterIdx === -1) {
      _csvRecords = [];
      return _csvRecords;
    }

    _csvRecords = lines.slice(1).map((line) => {
      const cols = line.split(",");
      return {
        title: cols[titleIdx]?.trim() ?? "",
        slug: cols[slugIdx]?.trim() ?? "",
        hub: cols[hubIdx]?.trim() ?? "",
        cluster: cols[clusterIdx]?.trim() ?? "",
      };
    });
    _csvRecords = _csvRecords.filter((row) => row.slug);
    return _csvRecords;
  } catch {
    _csvRecords = [];
    return _csvRecords;
  }
}

export async function getTaxonomy(): Promise<Hub[]> {
  if (_taxonomy) {
    return _taxonomy;
  }

  const calculatorPages = await import.meta.glob<{
    frontmatter: { hub?: string; cluster?: string; title?: string };
    url: string;
  }>("/src/pages/en/*/*/*.astro");

  const csvRecords = await loadCsvRecords();
  const csvMap = new Map(csvRecords.map((row) => [row.slug, row]));

  const hubs: Record<string, Hub> = {};

  for (const hubDef of hubDefinitions) {
    hubs[hubDef.slug] = { ...hubDef, clusters: [] };
  }

  for (const row of csvRecords) {
    const hubSlug = slugify(row.hub);
    if (!hubSlug) continue;
    if (!hubs[hubSlug]) {
      hubs[hubSlug] = {
        slug: hubSlug,
        name: row.hub,
        clusters: [],
      };
    }
  }

  for (const filePath in calculatorPages) {
    if (filePath.endsWith("index.astro")) continue;
    if (filePath.includes("/__")) continue;

    const slug = nodePath.basename(filePath, ".astro");
    const page = await calculatorPages[filePath]();
    const fm = page.frontmatter;
    const csvMeta = slug ? csvMap.get(slug) : undefined;
    const hubSlug =
      fm?.hub ?? (csvMeta?.hub ? slugify(csvMeta.hub) : undefined);
    const clusterSlug =
      fm?.cluster ?? (csvMeta?.cluster ? slugify(csvMeta.cluster) : undefined);
    const title = fm?.title ?? csvMeta?.title ?? slug;

    if (!hubSlug || !clusterSlug) continue;

    if (!hubs[hubSlug]) {
      hubs[hubSlug] = {
        slug: hubSlug,
        name: csvMeta?.hub ?? humanizeSlug(hubSlug),
        clusters: [],
      };
    }

    const hub = hubs[hubSlug];
    let cluster = hub.clusters.find((c) => c.slug === clusterSlug);

    if (!cluster) {
      const clusterName = csvMeta?.cluster ?? humanizeSlug(clusterSlug);
      cluster = { slug: clusterSlug, name: clusterName, tools: [] };
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
