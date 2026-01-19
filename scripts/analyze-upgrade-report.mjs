// scripts/analyze-upgrade-report.mjs
//
// Purpose:
//   Analyze ./upgrade-report.csv and output summaries for OK/WARN/FAIL.
//   This version focuses on WARN now that FAIL is ideally 0.
//
// Outputs:
//   - ./upgrade-status-summary.csv
//   - ./upgrade-warn-summary.csv
//   - ./upgrade-warn-by-reason.csv
//   - ./upgrade-forbidden-detected.csv
//
// Usage:
//   node scripts/analyze-upgrade-report.mjs
//   node scripts/analyze-upgrade-report.mjs --in=./upgrade-report.csv
//
import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const getArg = (k, def = null) => {
  const p = args.find(a => a.startsWith(k + "="));
  return p ? p.split("=").slice(1).join("=") : def;
};

const IN_CSV = path.resolve(getArg("--in", "./upgrade-report.csv"));

function parseCsvLine(line) {
  const out = [];
  let cur = "";
  let inQ = false;

  for (let i = 0; i < line.length; i++) {
    const ch = line[i];

    if (ch === '"' && line[i + 1] === '"' && inQ) {
      cur += '"';
      i++;
      continue;
    }
    if (ch === '"') {
      inQ = !inQ;
      continue;
    }
    if (ch === "," && !inQ) {
      out.push(cur);
      cur = "";
      continue;
    }
    cur += ch;
  }
  out.push(cur);
  return out;
}

function bucketWarn(notes) {
  const n = String(notes || "");

  // Forbidden detections
  if (n.includes("Forbidden detected:")) return "FORBIDDEN_DETECTED";

  // Missing content completeness
  if (n.includes("Missing formulas")) return "MISSING_FORMULAS";
  if (n.includes("Missing sources")) return "MISSING_SOURCES";

  // Other common warn types
  if (n.includes("Scrubbed competitor refs")) return "SCRUBBED_COMPETITOR_REFS";

  // Default bucket
  return "WARN_OTHER";
}

function extractForbiddenList(notes) {
  const m = String(notes || "").match(/Forbidden detected:\s*([^;]+)/);
  if (!m) return [];
  return m[1].split("|").map(s => s.trim()).filter(Boolean);
}

function main() {
  if (!fs.existsSync(IN_CSV)) {
    console.error("Not found:", IN_CSV);
    process.exit(1);
  }

  const lines = fs.readFileSync(IN_CSV, "utf8").split(/\r?\n/).filter(Boolean);
  if (lines.length < 2) {
    console.error("CSV appears empty:", IN_CSV);
    process.exit(1);
  }

  const rows = lines.slice(1).map(parseCsvLine).map(cols => ({
    slug: cols[0] || "",
    file: cols[1] || "",
    status: cols[2] || "",
    notes: cols.slice(3).join(",") || ""
  }));

  const totals = {
    OK: rows.filter(r => r.status === "OK").length,
    WARN: rows.filter(r => r.status === "WARN").length,
    FAIL: rows.filter(r => r.status === "FAIL").length
  };

  // Status summary
  const statusSummaryPath = path.resolve("./upgrade-status-summary.csv");
  fs.writeFileSync(
    statusSummaryPath,
    ["status,count", `OK,${totals.OK}`, `WARN,${totals.WARN}`, `FAIL,${totals.FAIL}`].join("\n") + "\n",
    "utf8"
  );

  // WARN analysis
  const warnRows = rows
    .filter(r => r.status === "WARN")
    .map(r => ({ ...r, reason: bucketWarn(r.notes) }));

  const warnCounts = new Map();
  for (const r of warnRows) warnCounts.set(r.reason, (warnCounts.get(r.reason) || 0) + 1);

  const warnSummaryPath = path.resolve("./upgrade-warn-summary.csv");
  fs.writeFileSync(
    warnSummaryPath,
    [
      "reason,count",
      ...Array.from(warnCounts.entries()).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k},${v}`)
    ].join("\n") + "\n",
    "utf8"
  );

  const warnByReasonPath = path.resolve("./upgrade-warn-by-reason.csv");
  fs.writeFileSync(
    warnByReasonPath,
    [
      "slug,file,status,reason,notes",
      ...warnRows.map(r =>
        `${r.slug},${r.file},${r.status},${r.reason},"${String(r.notes).replace(/"/g, '""')}"`
      )
    ].join("\n") + "\n",
    "utf8"
  );

  // Forbidden detected list
  const forbiddenRows = rows
    .filter(r => r.notes.includes("Forbidden detected:"))
    .map(r => ({
      ...r,
      forbidden: extractForbiddenList(r.notes).join(" | ")
    }));

  const forbiddenDetectedPath = path.resolve("./upgrade-forbidden-detected.csv");
  fs.writeFileSync(
    forbiddenDetectedPath,
    [
      "slug,file,status,forbidden,notes",
      ...forbiddenRows.map(r =>
        `${r.slug},${r.file},${r.status},"${String(r.forbidden).replace(/"/g, '""')}","${String(r.notes).replace(/"/g, '""')}"`
      )
    ].join("\n") + "\n",
    "utf8"
  );

  console.log("Totals:", totals);
  console.log("Top WARN reasons:");
  for (const [reason, count] of Array.from(warnCounts.entries()).sort((a, b) => b[1] - a[1]).slice(0, 10)) {
    console.log(`  ${reason}: ${count}`);
  }
  console.log("Wrote:", statusSummaryPath);
  console.log("Wrote:", warnSummaryPath);
  console.log("Wrote:", warnByReasonPath);
  console.log("Wrote:", forbiddenDetectedPath);
}

main();
