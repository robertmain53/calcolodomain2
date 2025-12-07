import fs from "node:fs";
import path from "node:path";

type MetricEntry = {
  pagePath: string;
  views: number;
  engagements?: number;
  conversions?: number;
};

const CSV_PATH = path.join(process.cwd(), "Reports_snapshot.csv");

function parseCsvRow(row: string): string[] {
  const parts: string[] = [];
  let current = "";
  let inQuotes = false;
  for (let i = 0; i < row.length; i++) {
    const ch = row[i];
    if (ch === '"' && row[i + 1] === '"') {
      current += '"';
      i++;
      continue;
    }
    if (ch === '"') {
      inQuotes = !inQuotes;
      continue;
    }
    if (ch === "," && !inQuotes) {
      parts.push(current);
      current = "";
      continue;
    }
    current += ch;
  }
  parts.push(current);
  return parts.map((p) => p.trim());
}

function loadMetrics(): MetricEntry[] {
  if (!fs.existsSync(CSV_PATH)) return [];
  try {
    const raw = fs.readFileSync(CSV_PATH, "utf8");
    const lines = raw.split(/\r?\n/).filter((l) => l.trim().length > 0);
    if (lines.length < 2) return [];
    const header = parseCsvRow(lines[0]).map((h) => h.toLowerCase());
    const pathIdx = header.findIndex((h) => h.includes("page path") || h === "path");
    const viewIdx = header.findIndex((h) => h.includes("view"));
    const engageIdx = header.findIndex((h) => h.includes("engagement"));
    const convIdx = header.findIndex((h) => h.includes("conversion") || h.includes("goal"));
    if (pathIdx === -1 || viewIdx === -1) return [];
    const rows: MetricEntry[] = [];
    for (let i = 1; i < lines.length; i++) {
      const cols = parseCsvRow(lines[i]);
      const pagePath = cols[pathIdx];
      const views = Number(cols[viewIdx] || 0);
      const engagements = engageIdx >= 0 ? Number(cols[engageIdx] || 0) : undefined;
      const conversions = convIdx >= 0 ? Number(cols[convIdx] || 0) : undefined;
      rows.push({ pagePath, views, engagements, conversions });
    }
    return rows;
  } catch {
    return [];
  }
}

const metrics = loadMetrics();

const viewThreshold = (() => {
  if (!metrics.length) return 0;
  const sorted = metrics.map((m) => m.views).sort((a, b) => a - b);
  const idx = Math.max(0, Math.floor(sorted.length * 0.8) - 1);
  return sorted[idx];
})();

export function metricForPath(pathname: string) {
  const m = metrics.find((m) => m.pagePath === pathname || m.pagePath === `${pathname}/`);
  const views = m?.views ?? 0;
  const engagements = m?.engagements ?? 0;
  const conversions = m?.conversions ?? 0;
  const isPopular = viewThreshold > 0 ? views >= viewThreshold : false;
  const isHighImpact = conversions > 0 ? true : isPopular && engagements > 0;
  return { views, engagements, conversions, isPopular, isHighImpact };
}
