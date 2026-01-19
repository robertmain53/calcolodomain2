// scripts/generate-audit-specs.mjs
//
// Generate *draft* per-page audit specs from ./sito_modificato/*.html
// Output: ./audit-specs/<slug>.json (does NOT overwrite unless --force)
//
// Usage:
//   node scripts/generate-audit-specs.mjs
//   node scripts/generate-audit-specs.mjs --force
//   node scripts/generate-audit-specs.mjs --date=2026-01-19
//   node scripts/generate-audit-specs.mjs --input=./sito_modificato --out=./audit-specs
//
// Dependency:
//   npm i cheerio
//
import fs from "node:fs";
import path from "node:path";
import * as cheerio from "cheerio";

const args = process.argv.slice(2);
const getArg = (k, def = null) => {
  const p = args.find(a => a.startsWith(k + "="));
  return p ? p.split("=").slice(1).join("=") : def;
};

const INPUT_DIR = path.resolve(getArg("--input", "./sito_modificato"));
const OUT_DIR = path.resolve(getArg("--out", "./audit-specs"));
const FORCE = args.includes("--force");
const DATE_OVERRIDE = getArg("--date", null);

const TODAY_ISO = (() => {
  if (DATE_OVERRIDE) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(DATE_OVERRIDE)) {
      throw new Error(`--date must be YYYY-MM-DD, got: ${DATE_OVERRIDE}`);
    }
    return DATE_OVERRIDE;
  }
  return new Date().toISOString().slice(0, 10);
})();

const VERIFIED = {
  verifiedByName: "Ugo Candido",
  verifiedProfileUrl: "https://calcdomain.com/ugocandido",
  verifiedLinkedInUrl: "https://www.linkedin.com/in/ugocandido92821/"
};

const AUTH_DOMAINS = [
  "consumerfinance.gov",
  "cfpb.gov",
  "irs.gov",
  "sec.gov",
  "investor.gov",
  "federalreserve.gov",
  "hud.gov",
  "ftc.gov",
  "bls.gov",
  "nih.gov",
  "cdc.gov",
  "who.int",
  "europa.eu",
  "ec.europa.eu",
  "ons.gov.uk",
  "bankofengland.co.uk",
  "bancaditalia.it",
  "istat.it",
  "normattiva.it",
  "nasa.gov",
  "nist.gov",
  "iso.org"
];

function listHtmlFiles(dir) {
  if (!fs.existsSync(dir)) throw new Error(`Input directory not found: ${dir}`);
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  return entries
    .filter(e => e.isFile() && e.name.toLowerCase().endsWith(".html"))
    .map(e => path.join(dir, e.name));
}

function slugFromFile(filePath) {
  return path.basename(filePath).replace(/\.html$/i, "");
}

function safeJsonWrite(filePath, obj, force = false) {
  if (fs.existsSync(filePath) && !force) return { wrote: false, reason: "exists" };
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(obj, null, 2) + "\n", "utf8");
  return { wrote: true };
}

function normalizeUrl(u) {
  try {
    const url = new URL(u);
    url.hash = "";
    return url.toString();
  } catch {
    return null;
  }
}

function domainOf(u) {
  try {
    return new URL(u).hostname.replace(/^www\./, "").toLowerCase();
  } catch {
    return "";
  }
}

function isExternalHttpUrl(u) {
  const nu = normalizeUrl(u);
  return !!nu && (nu.startsWith("http://") || nu.startsWith("https://"));
}

function isLikelyAuthoritative(u) {
  const d = domainOf(u);
  return AUTH_DOMAINS.some(ad => d === ad || d.endsWith("." + ad));
}

function textClean(s) {
  return String(s || "").replace(/\s+/g, " ").replace(/\u00a0/g, " ").trim();
}

function extractCanonical($) {
  const href = $('link[rel="canonical"]').attr("href");
  return href && isExternalHttpUrl(href) ? normalizeUrl(href) : null;
}

function extractTitle($) {
  const t = textClean($("title").first().text());
  if (t) return t;
  const h1 = textClean($("h1").first().text());
  return h1 || null;
}

function extractFormulaLatexBlocks(rawHtml) {
  const out = [];
  const re1 = /\\\[((?:.|\n)*?)\\\]/g;
  const re2 = /\$\$((?:.|\n)*?)\$\$/g;

  for (const m of rawHtml.matchAll(re1)) {
    const body = textClean(m[1]);
    if (body) out.push(body);
  }
  for (const m of rawHtml.matchAll(re2)) {
    const body = textClean(m[1]);
    if (body) out.push(body);
  }
  return [...new Set(out)];
}

function extractFormulaTextBlocks($) {
  const blocks = [];
  const candidates = [".formula-box", ".formulaBox", "[class*='formula']"];

  for (const sel of candidates) {
    $(sel).each((_, el) => {
      const txt = textClean($(el).text());
      if (txt && /[=^]/.test(txt) && txt.length >= 20) blocks.push(txt);
    });
  }

  return [...new Set(blocks)].slice(0, 6);
}

function buildFormulas(latexBlocks, formulaTexts) {
  const formulas = [];

  for (const ltx of latexBlocks.slice(0, 6)) {
    formulas.push({ title: "Formula (extracted LaTeX)", latex: ltx, raw: ltx });
  }
  for (const txt of formulaTexts.slice(0, 6)) {
    formulas.push({ title: "Formula (extracted text)", latex: "", raw: txt });
  }

  const seen = new Set();
  return formulas.filter(f => {
    const key = (f.raw || "").trim();
    if (!key) return false;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  }).slice(0, 10);
}

function extractSources($) {
  const scope = $("main").length ? $("main") : $.root();
  const links = [];

  scope.find("a[href]").each((_, a) => {
    const href = $(a).attr("href");
    if (!href) return;

    const nu = normalizeUrl(href);
    if (!nu || !isExternalHttpUrl(nu)) return;

    const label = textClean($(a).text()) || nu;
    links.push({
      label: label.slice(0, 140),
      publisher: domainOf(nu),
      url: nu,
      accessedISO: TODAY_ISO,
      authoritative: isLikelyAuthoritative(nu)
    });
  });

  const byUrl = new Map();
  for (const l of links) if (!byUrl.has(l.url)) byUrl.set(l.url, l);

  const arr = Array.from(byUrl.values());
  arr.sort((a, b) => Number(b.authoritative) - Number(a.authoritative));

  return arr.slice(0, 8).map(({ authoritative, ...rest }) => rest);
}

function extractVariableHints($) {
  const hints = new Map();

  const COMMON = [
    { symbol: "P", meaning: "principal (loan amount)", units: "currency" },
    { symbol: "r", meaning: "periodic interest rate (annual rate ÷ payments per year)", units: "1" },
    { symbol: "n", meaning: "total number of payments (years × payments per year)", units: "count" },
    { symbol: "M", meaning: "periodic payment for principal + interest", units: "currency" },
  ];

  const bodyText = textClean($("body").text()).toLowerCase();

  if (bodyText.includes("amortization")) COMMON.forEach(v => hints.set(v.symbol, v));
  if (bodyText.includes("tax")) hints.set("T", { symbol: "T", meaning: "property tax (annual or monthly depending on input)", units: "currency" });
  if (bodyText.includes("insurance")) hints.set("I", { symbol: "I", meaning: "homeowners insurance (annual or monthly depending on input)", units: "currency" });
  if (bodyText.includes("pmi")) hints.set("PMI", { symbol: "PMI", meaning: "private mortgage insurance (monthly)", units: "currency" });
  if (bodyText.includes("hoa")) hints.set("HOA", { symbol: "HOA", meaning: "homeowners association dues (monthly)", units: "currency" });
  if (bodyText.includes("extra principal")) hints.set("E", { symbol: "E", meaning: "extra principal payment per period", units: "currency" });

  const order = ["P","r","n","M","E","T","I","PMI","HOA"];
  const vars = Array.from(hints.values());
  vars.sort((a,b) => order.indexOf(a.symbol) - order.indexOf(b.symbol));
  return vars;
}

function buildSpec({ slug, title, canonical, formulas, variables, sources }) {
  return {
    slug,
    title: title || slug,
    canonical: canonical || null,

    version: "0.1.0-draft",
    lastCodeUpdateISO: TODAY_ISO,

    ...VERIFIED,

    formulas,
    variables,
    sources,

    changelog: [
      {
        dateISO: TODAY_ISO,
        version: "0.1.0-draft",
        changes: [
          "Initial audit spec draft generated from HTML extraction (review required).",
          "Verify formulas match the calculator engine and convert any text-only formulas to LaTeX.",
          "Confirm sources are authoritative and relevant to the calculator methodology."
        ]
      }
    ]
  };
}

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const files = listHtmlFiles(INPUT_DIR);
  const report = [];

  for (const filePath of files) {
    const slug = slugFromFile(filePath);
    const outPath = path.join(OUT_DIR, `${slug}.json`);

    const html = fs.readFileSync(filePath, "utf8");
    const $ = cheerio.load(html, { decodeEntities: false });

    const canonical = extractCanonical($);
    const title = extractTitle($);

    const latexBlocks = extractFormulaLatexBlocks(html);
    const formulaTexts = extractFormulaTextBlocks($);
    const formulas = buildFormulas(latexBlocks, formulaTexts);

    const sources = extractSources($);
    const variables = extractVariableHints($);

    const spec = buildSpec({ slug, title, canonical, formulas, variables, sources });
    const res = safeJsonWrite(outPath, spec, FORCE);

    const flags = [];
    if (!res.wrote) flags.push("SKIPPED_EXISTS");
    if (!canonical) flags.push("NO_CANONICAL");
    if (!formulas.length) flags.push("NO_FORMULAS");
    if (!sources.length) flags.push("NO_SOURCES");
    if (sources.length && sources.every(s => !isLikelyAuthoritative(s.url))) flags.push("NO_AUTHORITATIVE_SOURCE_DETECTED");

    report.push({
      slug,
      file: path.relative(process.cwd(), filePath),
      spec: path.relative(process.cwd(), outPath),
      status: res.wrote ? "WROTE" : "SKIPPED",
      flags: flags.join("|")
    });
  }

  const reportPath = path.resolve("./spec-generator-report.csv");
  const lines = [
    "slug,file,spec,status,flags",
    ...report.map(r => `${r.slug},${r.file},${r.spec},${r.status},"${r.flags.replace(/"/g, '""')}"`)
  ];
  fs.writeFileSync(reportPath, lines.join("\n") + "\n", "utf8");

  const wrote = report.filter(r => r.status === "WROTE").length;
  const skipped = report.filter(r => r.status === "SKIPPED").length;

  console.log(`Done. WROTE=${wrote} SKIPPED=${skipped}`);
  console.log(`Report: ${reportPath}`);
  console.log(`Specs folder: ${OUT_DIR}`);
}

main();
