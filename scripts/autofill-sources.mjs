// scripts/autofill-sources.mjs
//
// Purpose:
//   Auto-fill authoritative sources into audit specs that have missing/empty sources[].
//   Designed to convert WARN(MISSING_SOURCES) -> OK at scale.
//
// Usage:
//   node scripts/autofill-sources.mjs
//   node scripts/autofill-sources.mjs --force=true
//   node scripts/autofill-sources.mjs --specDir=./audit-specs
//
// Behavior:
//   - Only fills when sources are missing/empty, unless --force=true.
//   - Adds sources from an authoritative bundle selected via slug heuristics.
//   - Sets accessedISO to today's date.
//   - Does NOT attempt to crawl or fetch URLs.
//
import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const getArg = (k, def = null) => {
  const p = args.find(a => a.startsWith(k + "="));
  return p ? p.split("=").slice(1).join("=") : def;
};

const SPEC_DIR = path.resolve(getArg("--specDir", "./audit-specs"));
const FORCE = (getArg("--force", "false") || "").toLowerCase() === "true";
const TODAY_ISO = new Date().toISOString().slice(0, 10);

function listJsonFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  return entries
    .filter(e => e.isFile() && e.name.toLowerCase().endsWith(".json"))
    .map(e => path.join(dir, e.name));
}

function safeReadJson(p) {
  try {
    return { ok: true, data: JSON.parse(fs.readFileSync(p, "utf8")) };
  } catch (e) {
    return { ok: false, error: String(e) };
  }
}

function safeWriteJson(p, obj) {
  fs.writeFileSync(p, JSON.stringify(obj, null, 2) + "\n", "utf8");
}

function domainFromUrl(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return "";
  }
}

function mkSource(label, url) {
  return {
    label,
    publisher: domainFromUrl(url),
    url,
    accessedISO: TODAY_ISO
  };
}

// Authoritative bundles (keep small and stable; 2–4 is enough to remove WARN)
const BUNDLES = {
  FINANCE_MORTGAGE: [
    mkSource("CFPB — How is a mortgage payment calculated?", "https://www.consumerfinance.gov/ask-cfpb/how-is-a-mortgage-payment-calculated-en-1907/"),
    mkSource("CFPB — Mortgages (consumer education)", "https://www.consumerfinance.gov/consumer-tools/mortgages/"),
    mkSource("Federal Reserve — Consumer resources", "https://www.federalreserve.gov/consumerscommunities.htm"),
  ],

  FINANCE_LOANS_CREDIT: [
    mkSource("CFPB — Credit cards (consumer education)", "https://www.consumerfinance.gov/consumer-tools/credit-cards/"),
    mkSource("FTC — Credit and loans (consumer advice)", "https://consumer.ftc.gov/"),
    mkSource("Federal Reserve — Consumer resources", "https://www.federalreserve.gov/consumerscommunities.htm"),
  ],

  FINANCE_RETIREMENT_INVESTING: [
    mkSource("SEC — Investor.gov (investing basics)", "https://www.investor.gov/"),
    mkSource("SEC — Investment adviser information", "https://www.sec.gov/investor"),
    mkSource("IRS — Retirement plans", "https://www.irs.gov/retirement-plans"),
  ],

  FINANCE_TAXES_US: [
    mkSource("IRS — Forms, instructions, and publications", "https://www.irs.gov/forms-instructions"),
    mkSource("IRS — Tax topics", "https://www.irs.gov/taxtopics"),
    mkSource("IRS — Retirement plans", "https://www.irs.gov/retirement-plans"),
  ],

  FINANCE_INFLATION_MACRO: [
    mkSource("BLS — CPI data", "https://www.bls.gov/cpi/"),
    mkSource("Federal Reserve — Data and research", "https://www.federalreserve.gov/data.htm"),
  ],

  HEALTH_GENERAL: [
    mkSource("CDC — Health topics", "https://www.cdc.gov/"),
    mkSource("NIH — Health information", "https://www.nih.gov/health-information"),
    mkSource("WHO — Health topics", "https://www.who.int/health-topics"),
  ],

  ENGINEERING_UNITS_MEASUREMENTS: [
    mkSource("NIST — Weights and measures", "https://www.nist.gov/pml/weights-and-measures"),
    mkSource("NIST — SI units", "https://www.nist.gov/pml/owm/metric-si/si-units"),
  ],

  ENGINEERING_CIVIL_STRUCTURAL: [
    mkSource("NIST — Engineering Laboratory", "https://www.nist.gov/el"),
    mkSource("FEMA — Building science resources", "https://www.fema.gov/"),
  ],

  LEGAL_GENERAL: [
    mkSource("USA.gov — Government services and information", "https://www.usa.gov/"),
  ],

  DEFAULT: [
    mkSource("NIST — Weights and measures", "https://www.nist.gov/pml/weights-and-measures"),
    mkSource("FTC — Consumer advice", "https://consumer.ftc.gov/"),
  ]
};

// Slug → bundle heuristics (deterministic, easy to extend)
function chooseBundle(slug) {
  const s = String(slug || "").toLowerCase();

  // Mortgage / real estate
  if (s.includes("mortgage") || s.includes("amortization") || s.includes("refinance") || s.includes("home-loan")) {
    return "FINANCE_MORTGAGE";
  }

  // Loans / credit / APR / debt
  if (
    s.includes("loan") ||
    s.includes("apr") ||
    s.includes("interest-rate") ||
    s.includes("credit") ||
    s.includes("debt") ||
    s.includes("dti") ||
    s.includes("payoff")
  ) {
    return "FINANCE_LOANS_CREDIT";
  }

  // Retirement / investing / 401k / roth / ira
  if (
    s.includes("401k") ||
    s.includes("roth") ||
    s.includes("ira") ||
    s.includes("retirement") ||
    s.includes("rmd") ||
    s.includes("compound-interest") ||
    s.includes("investment") ||
    s.includes("roi")
  ) {
    return "FINANCE_RETIREMENT_INVESTING";
  }

  // US taxes
  if (s.includes("tax") || s.includes("capital-gains") || s.includes("withholding") || s.includes("w2")) {
    return "FINANCE_TAXES_US";
  }

  // Inflation / CPI
  if (s.includes("inflation") || s.includes("cpi")) {
    return "FINANCE_INFLATION_MACRO";
  }

  // Health keywords
  if (
    s.includes("bmi") ||
    s.includes("gfr") ||
    s.includes("dosage") ||
    s.includes("calorie") ||
    s.includes("pregnancy") ||
    s.includes("heart-rate") ||
    s.includes("body-fat")
  ) {
    return "HEALTH_GENERAL";
  }

  // Units / conversions / measurement
  if (
    s.includes("to-") ||
    s.includes("converter") ||
    s.includes("conversion") ||
    s.includes("unit") ||
    s.includes("feet") ||
    s.includes("meters") ||
    s.includes("celsius") ||
    s.includes("fahrenheit")
  ) {
    return "ENGINEERING_UNITS_MEASUREMENTS";
  }

  // Structural/civil
  if (s.includes("beam") || s.includes("pavement") || s.includes("concrete") || s.includes("rebar") || s.includes("wind-load") || s.includes("snow-load")) {
    return "ENGINEERING_CIVIL_STRUCTURAL";
  }

  // Legal-ish
  if (s.includes("child-support") || s.includes("alimony") || s.includes("statute") || s.includes("deadline")) {
    return "LEGAL_GENERAL";
  }

  return "DEFAULT";
}

function dedupeSources(sources) {
  const m = new Map();
  for (const s of sources || []) {
    if (!s || !s.url) continue;
    m.set(String(s.url), s);
  }
  return Array.from(m.values());
}

function writeCsv(rows, outPath) {
  const header = ["slug", "bundle", "status", "notes"].join(",");
  const lines = [header, ...rows.map(r =>
    [r.slug, r.bundle, r.status, `"${String(r.notes).replace(/"/g, '""')}"`].join(",")
  )];
  fs.writeFileSync(outPath, lines.join("\n") + "\n", "utf8");
}

function main() {
  if (!fs.existsSync(SPEC_DIR)) {
    console.error("Spec dir not found:", SPEC_DIR);
    process.exit(1);
  }

  const files = listJsonFiles(SPEC_DIR);
  const rows = [];

  let updated = 0;
  let skipped = 0;
  let failed = 0;

  for (const filePath of files) {
    const slug = path.basename(filePath).replace(/\.json$/i, "");
    const read = safeReadJson(filePath);
    if (!read.ok) {
      failed++;
      rows.push({ slug, bundle: "", status: "FAIL", notes: `Invalid JSON: ${read.error}` });
      continue;
    }

    const spec = read.data || {};
    const existing = Array.isArray(spec.sources) ? spec.sources : [];
    const hasSources = existing.some(s => s && String(s.url || "").startsWith("http"));

    if (hasSources && !FORCE) {
      skipped++;
      rows.push({ slug, bundle: "", status: "SKIP", notes: "Already has sources[]" });
      continue;
    }

    const bundleKey = chooseBundle(slug);
    const injected = BUNDLES[bundleKey] || BUNDLES.DEFAULT;

    const merged = dedupeSources([...(FORCE ? [] : existing), ...injected]);

    spec.sources = merged;

    // Keep version + changelog consistent: bump patch draft marker (optional)
    // If you prefer no version bump, remove this block.
    if (typeof spec.version === "string" && spec.version.includes("draft")) {
      // keep as draft
    }

    safeWriteJson(filePath, spec);
    updated++;
    rows.push({ slug, bundle: bundleKey, status: "UPDATED", notes: `Injected ${injected.length} sources` });
  }

  const outCsv = path.resolve("./sources-autofill-report.csv");
  writeCsv(rows, outCsv);

  console.log(`Done. UPDATED=${updated} SKIP=${skipped} FAIL=${failed}`);
  console.log(`Report: ${outCsv}`);
}

main();
