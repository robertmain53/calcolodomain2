// scripts/debrand-competitors.mjs
//
// Purpose:
//   Remove/neutralize competitor brand mentions (e.g., OmniCalculator, Investopedia, Calculator.net)
//   across ./sito_modificato/*.html.
//
// Safe-by-default rules:
//   - Removes competitor-domain links (<a href="...">) by converting them to plain text.
//   - Replaces competitor brand tokens in visible text nodes (excludes script/style by default).
//   - Does NOT touch code logic.
//   - Optionally: scrub JSON-LD script blocks too (disabled by default).
//
// Usage:
//   node scripts/debrand-competitors.mjs
//   node scripts/debrand-competitors.mjs --dryRun=true
//   node scripts/debrand-competitors.mjs --scrubJsonLd=true
//   node scripts/debrand-competitors.mjs --dir=./sito_modificato
//
// Output:
//   - ./debrand-report.csv
//
import fs from "node:fs";
import path from "node:path";
import * as cheerio from "cheerio";
import { Worker, isMainThread, parentPort, workerData } from "node:worker_threads";

const SKIPPED_CSV = path.resolve("./debrand-competitors-skipped-pages.csv");
const FILE_TIMEOUT_MS = 120000;

const args = process.argv.slice(2);
const getArg = (k, def = null) => {
  const p = args.find(a => a.startsWith(k + "="));
  return p ? p.split("=").slice(1).join("=") : def;
};

const HTML_DIR = path.resolve(getArg("--dir", "./sito_modificato"));
const DRY_RUN = (getArg("--dryRun", "false") || "").toLowerCase() === "true";
const SCRUB_JSONLD = (getArg("--scrubJsonLd", "false") || "").toLowerCase() === "true";
const OUT_CSV = path.resolve("./debrand-report.csv");

// Competitor domains to remove links to (conservative list; extend as needed)
const COMPETITOR_DOMAINS = [
  "www.omnicalculator.com",
  "omnicalculator.com",
  "www.calculator.net",
  "calculator.net",
  "www.investopedia.com",
  "investopedia.com"
];

// Token replacements in visible content.
// Keep replacements neutral; avoid implying endorsement.
// You can adjust the replacement phrases to match your editorial voice.
const TOKEN_REPLACEMENTS = [
  { name: "OmniCalculator", re: /\bomni\s*calculator\b/gi, repl: "a third-party calculator" },
  { name: "Calculator.net", re: /\bcalculator\.net\b/gi, repl: "a third-party calculator site" },
  { name: "Investopedia", re: /\binvestopedia\b/gi, repl: "a third-party reference site" }
];

function listHtmlFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  return entries
    .filter(e => e.isFile() && e.name.toLowerCase().endsWith(".html"))
    .map(e => path.join(dir, e.name));
}

function slugFromFile(filePath) {
  return path.basename(filePath).replace(/\.html$/i, "");
}

function isCompetitorLink(href) {
  try {
    const u = new URL(href);
    const h = u.hostname.toLowerCase();
    return COMPETITOR_DOMAINS.includes(h);
  } catch {
    return false;
  }
}

function scrubAnchors($) {
  let removedLinks = 0;

  $("a[href]").each((_, a) => {
    const href = String($(a).attr("href") || "");
    if (!href) return;

    if (href.startsWith("http://") || href.startsWith("https://")) {
      if (isCompetitorLink(href)) {
        // replace link with its text content to preserve sentence flow
        const txt = $(a).text() || "";
        $(a).replaceWith(txt);
        removedLinks++;
      }
    }
  });

  return removedLinks;
}

function scrubTextNodes($) {
  let replacements = 0;
  const replacedTokens = new Map(); // tokenName -> count

  $("body").find("*").contents().each((_, node) => {
    if (node.type !== "text") return;

    const parent = node.parent && node.parent.name ? node.parent.name.toLowerCase() : "";
    if (parent === "script" || parent === "style") return;

    let t = node.data || "";
    let changed = false;

    for (const tr of TOKEN_REPLACEMENTS) {
      const before = t;
      t = t.replace(tr.re, tr.repl);
      if (t !== before) {
        changed = true;
        replacements++;
        replacedTokens.set(tr.name, (replacedTokens.get(tr.name) || 0) + 1);
      }
    }

    if (changed) node.data = t;
  });

  return { replacements, replacedTokens };
}

function scrubJsonLdBlocks($) {
  // Only affects <script type="application/ld+json"> content.
  // Disabled by default because it can be sensitive; enable if you still detect forbidden after visible-text pass.
  let jsonldEdits = 0;

  $("script[type='application/ld+json']").each((_, s) => {
    const raw = $(s).html() || "";
    if (!raw) return;

    let out = raw;
    let changed = false;

    for (const tr of TOKEN_REPLACEMENTS) {
      const before = out;
      out = out.replace(tr.re, tr.repl);
      if (out !== before) {
        changed = true;
      }
    }

    if (changed) {
      $(s).text(out);
      jsonldEdits++;
    }
  });

  return jsonldEdits;
}

function findForbiddenInHtml(html) {
  const hits = [];
  const lower = html.toLowerCase();
  if (/\bomni\s*calculator\b/i.test(html)) hits.push("OmniCalculator");
  if (lower.includes("calculator.net")) hits.push("Calculator.net");
  if (/\binvestopedia\b/i.test(html)) hits.push("Investopedia");
  return hits;
}

function writeCsv(rows) {
  const header = ["slug", "file", "status", "removedLinks", "textReplacements", "jsonLdEdits", "tokens", "remainingForbidden"].join(",");
  const lines = [
    header,
    ...rows.map(r =>
      [
        r.slug,
        r.file,
        r.status,
        r.removedLinks,
        r.textReplacements,
        r.jsonLdEdits,
        `"${String(r.tokens).replace(/"/g, '""')}"`,
        `"${String(r.remainingForbidden).replace(/"/g, '""')}"`
      ].join(",")
    )
  ];
  fs.writeFileSync(OUT_CSV, lines.join("\n") + "\n", "utf8");
}

function writeSkippedCsv(rows) {
  const header = ["slug", "file", "reason"].join(",");
  const lines = [
    header,
    ...rows.map(r =>
      [
        r.slug,
        r.file,
        `"${String(r.reason).replace(/"/g, '""')}"`
      ].join(",")
    )
  ];
  fs.writeFileSync(SKIPPED_CSV, lines.join("\n") + "\n", "utf8");
}

function processFile(html, filePath) {
  const $ = cheerio.load(html, { decodeEntities: false });

  const removedLinks = scrubAnchors($);
  const { replacements: textReplacements, replacedTokens } = scrubTextNodes($);
  const jsonLdEdits = SCRUB_JSONLD ? scrubJsonLdBlocks($) : 0;

  const outHtml = $.html();
  const remaining = findForbiddenInHtml(outHtml);

  const tokensStr = Array.from(replacedTokens.entries())
    .map(([k, v]) => `${k}:${v}`)
    .join(" | ");

  const didChange = removedLinks > 0 || textReplacements > 0 || jsonLdEdits > 0;

  return {
    slug: slugFromFile(filePath),
    file: filePath,
    removedLinks,
    textReplacements,
    jsonLdEdits,
    tokens: tokensStr,
    remainingForbidden: remaining.join(" | "),
    status: remaining.length ? "STILL_FORBIDDEN" : "CLEAN",
    didChange,
    outHtml
  };
}

function runWorker(filePath, html) {
  return new Promise((resolve, reject) => {
    const worker = new Worker(new URL(import.meta.url), {
      workerData: { filePath, html, scrubJsonLd: SCRUB_JSONLD }
    });

    const timer = setTimeout(() => {
      worker.terminate();
      reject(new Error("TIMEOUT"));
    }, FILE_TIMEOUT_MS);

    worker.on("message", msg => {
      clearTimeout(timer);
      resolve(msg);
    });
    worker.on("error", err => {
      clearTimeout(timer);
      reject(err);
    });
    worker.on("exit", code => {
      if (code !== 0) {
        clearTimeout(timer);
        reject(new Error(`Worker exit ${code}`));
      }
    });
  });
}

async function main() {
  const files = listHtmlFiles(HTML_DIR);
  const rows = [];
  const skipped = [];

  let ok = 0, changed = 0, failed = 0;
  const start = Date.now();

  for (const [idx, filePath] of files.entries()) {
    if (idx % 10 === 0) {
      const elapsedMs = Date.now() - start;
      const done = idx + 1;
      const rate = elapsedMs > 0 ? done / (elapsedMs / 1000) : 0;
      const remaining = files.length - done;
      const etaSec = rate > 0 ? Math.round(remaining / rate) : 0;
      console.log(`Processing ${done}/${files.length}... ETA ~${etaSec}s`);
    }
    console.log(`File: ${filePath}`);
    const slug = slugFromFile(filePath);

    let html;
    try {
      html = fs.readFileSync(filePath, "utf8");
    } catch (e) {
      failed++;
      rows.push({
        slug,
        file: filePath,
        status: "FAIL_READ",
        removedLinks: 0,
        textReplacements: 0,
        jsonLdEdits: 0,
        tokens: "",
        remainingForbidden: ""
      });
      continue;
    }

    let result;
    try {
      result = await runWorker(filePath, html);
    } catch (err) {
      skipped.push({
        slug,
        file: filePath,
        reason: err && err.message ? err.message : "UNKNOWN_ERROR"
      });
      rows.push({
        slug,
        file: filePath,
        status: "SKIPPED",
        removedLinks: 0,
        textReplacements: 0,
        jsonLdEdits: 0,
        tokens: "",
        remainingForbidden: "SKIPPED"
      });
      continue;
    }

    if (!DRY_RUN && result.didChange) {
      fs.writeFileSync(filePath, result.outHtml, "utf8");
    }

    if (result.status === "CLEAN") ok++;
    if (result.didChange) changed++;

    rows.push({
      slug: result.slug,
      file: result.file,
      status: result.status,
      removedLinks: result.removedLinks,
      textReplacements: result.textReplacements,
      jsonLdEdits: result.jsonLdEdits,
      tokens: result.tokens,
      remainingForbidden: result.remainingForbidden
    });
  }

  writeCsv(rows);
  writeSkippedCsv(skipped);

  console.log(`Done. CLEAN=${ok} CHANGED=${changed} FAIL=${failed}`);
  console.log(`Report: ${OUT_CSV}`);
  console.log(`Skipped report: ${SKIPPED_CSV}`);
  console.log(`DryRun: ${DRY_RUN}  ScrubJSONLD: ${SCRUB_JSONLD}`);
}

if (!isMainThread) {
  const { filePath, html, scrubJsonLd } = workerData;
  if (scrubJsonLd) {
    // nothing to do; SCRUB_JSONLD is read inside scrubJsonLdBlocks
  }
  const result = processFile(html, filePath);
  parentPort.postMessage(result);
} else {
  main();
}
