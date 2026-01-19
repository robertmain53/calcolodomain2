// scripts/seed-formulas.mjs
//
// Purpose:
//   Seed formulas[] in audit specs when missing/empty, using conservative family templates.
//   Converts WARN(MISSING_FORMULAS) -> OK (when sources exist too).
//
// Usage:
//   node scripts/seed-formulas.mjs
//   node scripts/seed-formulas.mjs --force=true
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

function chooseFormulaSeed(slug) {
  const s = String(slug || "").toLowerCase();

  // Fixed-rate mortgage / amortization payment
  if (s.includes("mortgage") || s.includes("amortization") || s.includes("loan-payment") || s.includes("refinance")) {
    return {
      title: "Fixed-rate payment (principal + interest)",
      latex: "M = P\\,\\frac{r(1+r)^{n}}{(1+r)^{n}-1}",
      raw: "M = P * [ r(1+r)^n ] / [ (1+r)^n - 1 ]"
    };
  }

  // Compound interest
  if (s.includes("compound-interest") || s.includes("future-value")) {
    return {
      title: "Compound interest (future value)",
      latex: "A = P\\left(1+\\frac{r}{m}\\right)^{mt}",
      raw: "A = P * (1 + r/m)^(m*t)"
    };
  }

  // ROI
  if (s.includes("roi")) {
    return {
      title: "Return on investment",
      latex: "\\mathrm{ROI} = \\frac{\\mathrm{Gain}-\\mathrm{Cost}}{\\mathrm{Cost}}",
      raw: "ROI = (Gain - Cost) / Cost"
    };
  }

  // Percent change
  if (s.includes("percent") || s.includes("percentage-change") || s.includes("increase") || s.includes("decrease")) {
    return {
      title: "Percentage change",
      latex: "\\%\\Delta = \\frac{\\text{New}-\\text{Old}}{\\text{Old}}\\times 100",
      raw: "%Δ = ((New - Old) / Old) * 100"
    };
  }

  // Unit conversion (generic)
  if (s.includes("to-") || s.includes("converter") || s.includes("conversion")) {
    return {
      title: "Unit conversion",
      latex: "y = x\\cdot k",
      raw: "y = x * k"
    };
  }

  return null;
}

function main() {
  const files = listJsonFiles(SPEC_DIR);
  let updated = 0, skipped = 0, failed = 0;

  for (const filePath of files) {
    const slug = path.basename(filePath).replace(/\.json$/i, "");
    const read = safeReadJson(filePath);
    if (!read.ok) { failed++; continue; }

    const spec = read.data || {};
    const formulas = Array.isArray(spec.formulas) ? spec.formulas : [];
    const hasFormula = formulas.some(f => String(f?.raw || f?.latex || "").trim().length > 0);

    if (hasFormula && !FORCE) { skipped++; continue; }

    const seed = chooseFormulaSeed(slug);
    if (!seed) { skipped++; continue; }

    spec.formulas = [seed]; // conservative: one seed
    safeWriteJson(filePath, spec);
    updated++;
  }

  console.log(`Done. UPDATED=${updated} SKIP=${skipped} FAIL=${failed}`);
}

main();
