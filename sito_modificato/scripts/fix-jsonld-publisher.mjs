// scripts/fix-jsonld-publisher.mjs
//
// Purpose:
//   Fix incorrect competitor "publisher" attribution inside JSON-LD blocks.
//   Replaces publisher.name matching competitor brands with CalcDomain.
//
// Usage:
//   node scripts/fix-jsonld-publisher.mjs
//   node scripts/fix-jsonld-publisher.mjs --dir=./sito_modificato
//   node scripts/fix-jsonld-publisher.mjs --dryRun=true
//
import fs from "node:fs";
import path from "node:path";
import * as cheerio from "cheerio";

const args = process.argv.slice(2);
const getArg = (k, def = null) => {
  const p = args.find(a => a.startsWith(k + "="));
  return p ? p.split("=").slice(1).join("=") : def;
};

const HTML_DIR = path.resolve(getArg("--dir", "./sito_modificato"));
const DRY_RUN = (getArg("--dryRun", "false") || "").toLowerCase() === "true";
const OUT_CSV = path.resolve("./jsonld-publisher-fix-report.csv");

const COMPETITOR_PUBLISHERS = new Set([
  "omnicalculator",
  "omnicalculator.com",
  "calculator.net",
  "investopedia"
]);

const CALCDOMAIN_PUBLISHER = {
  "@type": "Organization",
  "name": "CalcDomain",
  "url": "https://calcdomain.com",
  "logo": "https://calcdomain.com/apple-touch-icon.png"
};

function listHtmlFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  return entries
    .filter(e => e.isFile() && e.name.toLowerCase().endsWith(".html"))
    .map(e => path.join(dir, e.name));
}

function slugFromFile(filePath) {
  return path.basename(filePath).replace(/\.html$/i, "");
}

function normName(s) {
  return String(s || "").trim().toLowerCase();
}

function isCompetitorPublisher(pubObj) {
  if (!pubObj || typeof pubObj !== "object") return false;
  const n = normName(pubObj.name);
  if (!n) return false;
  // catch "OmniCalculator" exactly and also URLish names
  if (COMPETITOR_PUBLISHERS.has(n)) return true;
  // also catch "OmniCalculator" without lowercasing issues
  if (n.includes("omni") && n.includes("calculator")) return true;
  return false;
}

function patchNode(node) {
  // node can be object or array
  let changed = 0;

  function walk(x) {
    if (!x || typeof x !== "object") return;

    if (Array.isArray(x)) {
      x.forEach(walk);
      return;
    }

    // Patch publisher if competitor
    if (x.publisher && isCompetitorPublisher(x.publisher)) {
      x.publisher = { ...CALCDOMAIN_PUBLISHER };
      changed++;
    }

    // Walk all keys
    for (const k of Object.keys(x)) walk(x[k]);
  }

  walk(node);
  return changed;
}

function writeCsv(rows) {
  const header = ["slug", "file", "status", "blocksPatched", "notes"].join(",");
  const lines = [
    header,
    ...rows.map(r =>
      [r.slug, r.file, r.status, r.blocksPatched, `"${String(r.notes).replace(/"/g, '""')}"`].join(",")
    )
  ];
  fs.writeFileSync(OUT_CSV, lines.join("\n") + "\n", "utf8");
}

function main() {
  const files = listHtmlFiles(HTML_DIR);
  const rows = [];

  let changedFiles = 0, okFiles = 0, failFiles = 0;

  for (const filePath of files) {
    const slug = slugFromFile(filePath);
    let html;

    try {
      html = fs.readFileSync(filePath, "utf8");
    } catch {
      failFiles++;
      rows.push({ slug, file: filePath, status: "FAIL_READ", blocksPatched: 0, notes: "" });
      continue;
    }

    const $ = cheerio.load(html, { decodeEntities: false });

    let patchedBlocks = 0;
    let parseErrors = 0;

    $("script[type='application/ld+json']").each((_, s) => {
      const raw = ($(s).html() || "").trim();
      if (!raw) return;

      let data;
      try {
        data = JSON.parse(raw);
      } catch {
        parseErrors++;
        return;
      }

      const changed = patchNode(data);
      if (changed > 0) {
        patchedBlocks += changed;
        // Write back pretty JSON to stabilize diffs
        $(s).text(JSON.stringify(data, null, 2));
      }
    });

    const outHtml = $.html();
    const didChange = patchedBlocks > 0;

    if (didChange) {
      changedFiles++;
      if (!DRY_RUN) fs.writeFileSync(filePath, outHtml, "utf8");
      rows.push({
        slug,
        file: filePath,
        status: DRY_RUN ? "WOULD_PATCH" : "PATCHED",
        blocksPatched: patchedBlocks,
        notes: parseErrors ? `JSON parse errors in ${parseErrors} JSON-LD blocks` : ""
      });
    } else {
      okFiles++;
      rows.push({
        slug,
        file: filePath,
        status: "NO_CHANGE",
        blocksPatched: 0,
        notes: parseErrors ? `JSON parse errors in ${parseErrors} JSON-LD blocks` : ""
      });
    }
  }

  writeCsv(rows);

  console.log(`Done. PATCHED_FILES=${changedFiles} NO_CHANGE=${okFiles} FAIL=${failFiles}`);
  console.log(`Report: ${OUT_CSV}`);
  console.log(`DryRun: ${DRY_RUN}`);
}

main();
