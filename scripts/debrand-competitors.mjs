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

function main() {
  const files = listHtmlFiles(HTML_DIR);
  const rows = [];

  let ok = 0, changed = 0, failed = 0;

  for (const filePath of files) {
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

    if (!DRY_RUN && didChange) {
      fs.writeFileSync(filePath, outHtml, "utf8");
    }

    if (remaining.length === 0) ok++;
    if (didChange) changed++;

    rows.push({
      slug,
      file: filePath,
      status: remaining.length ? "STILL_FORBIDDEN" : "CLEAN",
      removedLinks,
      textReplacements,
      jsonLdEdits,
      tokens: tokensStr,
      remainingForbidden: remaining.join(" | ")
    });
  }

  writeCsv(rows);

  console.log(`Done. CLEAN=${ok} CHANGED=${changed} FAIL=${failed}`);
  console.log(`Report: ${OUT_CSV}`);
  console.log(`DryRun: ${DRY_RUN}  ScrubJSONLD: ${SCRUB_JSONLD}`);
}

main();
