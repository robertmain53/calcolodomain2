// scripts/upgrade-all-pages.mjs
//
// Batch inject/replace audit spine into ./sito_modificato/*.html
// Requires audit specs in ./audit-specs/<slug>.json
//
// Usage:
//   node scripts/upgrade-all-pages.mjs
//
// Optional flags:
//   --scrubCompetitors=true   (attempt to remove competitor refs automatically; default false)
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

const HTML_DIR = path.resolve("./sito_modificato");
const SPEC_DIR = path.resolve("./audit-specs");
const OUT_CSV = path.resolve("./upgrade-report.csv");

// Brand-precise forbidden patterns.
// IMPORTANT: avoid banning bare "omni" (too many false positives).
const FORBIDDEN_PATTERNS = [
  { name: "Investopedia", re: /\binvestopedia\b/i },
  { name: "Calculator.net", re: /\bcalculator\.net\b/i },
  { name: "OmniCalculator", re: /\bomni\s*calculator\b/i }
];

const SCRUB_COMPETITORS = (getArg("--scrubCompetitors", "false") || "").toLowerCase() === "true";

function listHtmlFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  return entries
    .filter(e => e.isFile() && e.name.toLowerCase().endsWith(".html"))
    .map(e => path.join(dir, e.name));
}

function slugFromFile(filePath) {
  return path.basename(filePath).replace(/\.html$/i, "");
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (ch) => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
  }[ch]));
}

function normalizeISODate(s) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(s || ""))) return null;
  return s;
}

function findForbidden(html) {
  const hits = [];
  for (const p of FORBIDDEN_PATTERNS) {
    if (p.re.test(html)) hits.push(p.name);
  }
  return hits;
}

function ensureAuditCss($) {
  const marker = "/* AUDIT_SPINE_CSS */";
  const headHtml = $("head").html() || "";
  if (headHtml.includes(marker)) return;

  const css = `
<style>
${marker}
.auditspine-note{
  border:1px solid #e5e7eb;
  background:#fff;
  border-radius:12px;
  padding:12px;
  color:#475569;
  font-size:13px;
  line-height:1.5;
}
.auditspine-mono{font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;}
.auditspine-changelog{
  border:1px solid #e5e7eb;
  background:#fff;
  border-left:5px solid #334155;
  border-radius:12px;
  padding:12px;
  font-size:13px;
  color:#475569;
}
.auditspine-formula{
  margin:10px 0;
  background:#0b1220;
  color:#e5e7eb;
  border-radius:12px;
  padding:12px;
  border:1px solid rgba(255,255,255,.12);
  overflow-x:auto;
}
.auditspine-formula pre{margin:8px 0 0; white-space:pre-wrap;}
.auditspine-hr{border:none; border-top:1px solid #e5e7eb; margin:18px 0;}
.auditspine-badge{
  display:inline-block;
  padding:4px 10px;
  border-radius:999px;
  font-size:12px;
  font-weight:600;
  border:1px solid #e5e7eb;
  background:#f8fafc;
  color:#0f172a;
}
.auditspine-badge-warn{
  background:#fff7ed;
  border-color:#fed7aa;
  color:#9a3412;
}
</style>`.trim();

  $("head").append("\n" + css + "\n");
}

function renderAuditSpine(spec, completeness) {
  const lastUpdate = normalizeISODate(spec.lastCodeUpdateISO);
  const version = escapeHtml(spec.version || "1.0.0");
  const verifiedByName = escapeHtml(spec.verifiedByName || "Ugo Candido");
  const profileUrl = escapeHtml(spec.verifiedProfileUrl || "https://calcdomain.com/ugocandido");
  const linkedInUrl = escapeHtml(spec.verifiedLinkedInUrl || "https://www.linkedin.com/in/ugocandido92821/");

  const formulas = Array.isArray(spec.formulas) ? spec.formulas : [];
  const variables = Array.isArray(spec.variables) ? spec.variables : [];
  const sources = Array.isArray(spec.sources) ? spec.sources : [];
  const changelog = Array.isArray(spec.changelog) ? spec.changelog : [];

  const formulasHtml = formulas.map(f => {
    const title = escapeHtml(f.title || "Formula");
    const latex = escapeHtml(f.latex || "");
    const raw = escapeHtml(f.raw || f.latex || "");
    // Only render \[...\] if latex is non-empty; otherwise show raw only.
    const latexBlock = latex ? `<div style="margin-top:6px">\\[${latex}\\]</div>` : "";
    return `
<div style="margin:10px 0">
  <div><strong>${title}</strong></div>
  ${latexBlock}
  <pre class="auditspine-mono">${raw || "<em>(empty)</em>"}</pre>
</div>`.trim();
  }).join("\n");

  const varsHtml = variables.map(v => {
    const sym = escapeHtml(v.symbol || "");
    const meaning = escapeHtml(v.meaning || "");
    const units = escapeHtml(v.units || "");
    return `<li><span class="auditspine-mono">${sym}</span> = ${meaning}${units ? ` <em>(${units})</em>` : ""}</li>`;
  }).join("\n");

  const sourcesHtml = sources.map(s => {
    const label = escapeHtml(s.label || "Source");
    const pub = escapeHtml(s.publisher || "");
    const url = escapeHtml(s.url || "");
    const acc = escapeHtml(s.accessedISO || "");
    return `<li><strong>${label}</strong>${pub ? ` — ${pub}` : ""}${acc ? ` · Accessed ${acc}` : ""}<br/><a href="${url}" target="_blank" rel="nofollow noopener">${url}</a></li>`;
  }).join("\n");

  const changelogHtml = changelog.map(c => {
    const dateISO = escapeHtml(c.dateISO || "");
    const ver = escapeHtml(c.version || "");
    const changes = Array.isArray(c.changes) ? c.changes : [];
    return `
<div style="margin-top:10px">
  <strong>${ver}</strong>${dateISO ? ` · ${dateISO}` : ""}
  <ul style="margin:6px 0 0 18px">
    ${changes.map(x => `<li>${escapeHtml(x)}</li>`).join("\n")}
  </ul>
</div>`.trim();
  }).join("\n");

  const verifiedDate = lastUpdate ? lastUpdate : "YYYY-MM-DD";

  // Governance: only show strong "Verified" if complete (formulas + sources).
  const isComplete = completeness.isComplete;
  const badge = isComplete
    ? `<span class="auditspine-badge">Audit: Complete</span>`
    : `<span class="auditspine-badge auditspine-badge-warn">Audit: Needs review</span>`;

  const verificationLine = isComplete
    ? `<strong>Verified by ${verifiedByName} on ${escapeHtml(verifiedDate)}</strong>`
    : `<strong>Verification pending</strong> · Last code update: ${escapeHtml(verifiedDate)}`;

  return `
<!-- AUDIT_SPINE_START -->
<hr class="auditspine-hr"/>
<section aria-label="Formulas, sources, changelog, verification">
  ${badge}

  <details style="margin-top:10px">
    <summary><strong>Formula (LaTeX) + variables + units</strong></summary>
    <div class="auditspine-note" style="margin-top:10px">
      This section shows the formulas used by the calculator engine, plus variable definitions and units.
      ${!isComplete ? "<br/><strong>Note:</strong> This page needs review to confirm formulas and sources." : ""}
    </div>
    <div class="auditspine-formula">
      ${formulasHtml || "<em>No formulas provided in audit spec.</em>"}
      <div style="margin-top:12px"><strong>Variables and units</strong></div>
      <ul style="margin:8px 0 0 18px">
        ${varsHtml || "<li><em>No variables provided in audit spec.</em></li>"}
      </ul>
    </div>
  </details>

  <div class="auditspine-note" style="margin-top:12px">
    <strong>Sources (authoritative):</strong>
    <ul style="margin:8px 0 0 18px">
      ${sourcesHtml || "<li><em>No sources provided in audit spec.</em></li>"}
    </ul>
  </div>

  <div class="auditspine-changelog" style="margin-top:12px">
    <strong>Changelog</strong><br/>
    <div style="margin-top:6px">
      <strong>Version:</strong> ${version}<br/>
      <strong>Last code update:</strong> ${escapeHtml(verifiedDate)}
    </div>
    ${changelogHtml || ""}
  </div>

  <div class="auditspine-note" style="margin-top:12px">
    ${verificationLine}<br/>
    <a href="${profileUrl}" target="_blank" rel="noopener">Profile</a> ·
    <a href="${linkedInUrl}" target="_blank" rel="noopener">LinkedIn</a>
  </div>
</section>
<!-- AUDIT_SPINE_END -->
`.trim();
}

function replaceAuditSpineIfPresent(html, spine) {
  if (html.includes("<!-- AUDIT_SPINE_START -->") && html.includes("<!-- AUDIT_SPINE_END -->")) {
    return html.replace(
      /<!-- AUDIT_SPINE_START -->([\s\S]*?)<!-- AUDIT_SPINE_END -->/m,
      spine
    );
  }
  return null;
}

function injectIntoArticleOrMain($, spine) {
  const $article = $("main article").first();
  if ($article.length) {
    $article.append("\n" + spine + "\n");
    return "article";
  }
  const $main = $("main").first();
  if ($main.length) {
    $main.append("\n" + spine + "\n");
    return "main";
  }
  $("body").append("\n" + spine + "\n");
  return "body";
}

function loadSpec(slug) {
  const specPath = path.join(SPEC_DIR, `${slug}.json`);
  if (!fs.existsSync(specPath)) return { ok: false, specPath, error: "Missing spec file" };
  try {
    const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
    return { ok: true, specPath, spec };
  } catch {
    return { ok: false, specPath, error: "Invalid JSON spec" };
  }
}

function specCompleteness(spec) {
  const formulas = Array.isArray(spec.formulas) ? spec.formulas : [];
  const sources = Array.isArray(spec.sources) ? spec.sources : [];

  const hasAnyFormula = formulas.length > 0 && formulas.some(f => (String(f.raw || f.latex || "").trim().length > 0));
  const hasAnySource = sources.length > 0 && sources.some(s => String(s.url || "").startsWith("http"));

  return {
    hasAnyFormula,
    hasAnySource,
    isComplete: hasAnyFormula && hasAnySource
  };
}

function specHardQA(spec) {
  // Hard-fail only on truly broken spec fields
  const issues = [];
  if (!normalizeISODate(spec.lastCodeUpdateISO)) issues.push("Spec missing/invalid lastCodeUpdateISO (YYYY-MM-DD).");
  if (!spec.version) issues.push("Spec missing version.");
  if (!spec.verifiedByName) issues.push("Spec missing verifiedByName.");
  if (!spec.verifiedProfileUrl) issues.push("Spec missing verifiedProfileUrl.");
  if (!spec.verifiedLinkedInUrl) issues.push("Spec missing verifiedLinkedInUrl.");
  return issues;
}

function pageHardQA(html) {
  const issues = [];
  if (!html.includes("<!-- AUDIT_SPINE_START -->")) issues.push("Missing AUDIT_SPINE_START marker.");
  if (!html.includes("<!-- AUDIT_SPINE_END -->")) issues.push("Missing AUDIT_SPINE_END marker.");
  // Verification line is now conditional; ensure at least one of the two exists.
  const hasVerified = /Verified by\s+Ugo Candido\s+on\s+\d{4}-\d{2}-\d{2}/.test(html);
  const hasPending = /Verification pending/.test(html);
  if (!hasVerified && !hasPending) issues.push("Missing verification/pending line.");
  return issues;
}

function scrubCompetitorRefs($) {
  // Remove external links to competitor domains and scrub visible brand mentions.
  // Conservative: only touches anchors linking to those domains, and text nodes containing exact brand tokens.
  const competitorDomains = [
    "investopedia.com",
    "calculator.net"
  ];

  $("a[href]").each((_, a) => {
    const href = String($(a).attr("href") || "");
    const lower = href.toLowerCase();
    if (competitorDomains.some(d => lower.includes(d))) {
      // Replace the anchor with its text (no link) to preserve sentence structure.
      const txt = $(a).text() || "";
      $(a).replaceWith(txt);
    }
  });

  // Scrub brand tokens in text-heavy nodes (avoid scripts/styles).
  const scrubMap = [
    { re: /\binvestopedia\b/gi, repl: "a third-party source" },
    { re: /\bcalculator\.net\b/gi, repl: "a third-party calculator" },
    { re: /\bomni\s*calculator\b/gi, repl: "a third-party calculator" }
  ];

  $("body").find("*").contents().each((_, node) => {
    if (node.type !== "text") return;
    const parent = node.parent && node.parent.name ? node.parent.name.toLowerCase() : "";
    if (parent === "script" || parent === "style") return;

    let t = node.data || "";
    let changed = false;
    for (const m of scrubMap) {
      if (m.re.test(t)) {
        t = t.replace(m.re, m.repl);
        changed = true;
      }
    }
    if (changed) node.data = t;
  });
}

function writeCsv(rows) {
  const header = ["slug", "file", "status", "notes"].join(",");
  const lines = [header, ...rows.map(r =>
    [r.slug, r.file, r.status, `"${String(r.notes).replace(/"/g, '""')}"`].join(",")
  )];
  fs.writeFileSync(OUT_CSV, lines.join("\n"), "utf8");
}

function main() {
  const files = listHtmlFiles(HTML_DIR);
  const rows = [];

  for (const filePath of files) {
    const slug = slugFromFile(filePath);

    let html = fs.readFileSync(filePath, "utf8");

    // Forbidden detection can be WARN (preferred) or FAIL. Here: WARN, unless you want to hard-stop.
    const forbiddenFound = findForbidden(html);

    const specRes = loadSpec(slug);
    if (!specRes.ok) {
      rows.push({ slug, file: filePath, status: "FAIL", notes: `${specRes.error} (${specRes.specPath})` });
      continue;
    }

    const hardSpecIssues = specHardQA(specRes.spec);
    if (hardSpecIssues.length) {
      rows.push({ slug, file: filePath, status: "FAIL", notes: `Spec Hard QA: ${hardSpecIssues.join(" ; ")}` });
      continue;
    }

    const completeness = specCompleteness(specRes.spec);
    const spine = renderAuditSpine(specRes.spec, completeness);

    // Replace path: string replace if existing spine
    const replaced = replaceAuditSpineIfPresent(html, spine);
    if (replaced != null) {
      html = replaced;

      const $ = cheerio.load(html, { decodeEntities: false });
      ensureAuditCss($);
      if (SCRUB_COMPETITORS) scrubCompetitorRefs($);
      html = $.html();

      const pageIssues = pageHardQA(html);
      fs.writeFileSync(filePath, html, "utf8");

      if (pageIssues.length) {
        rows.push({ slug, file: filePath, status: "FAIL", notes: `Page Hard QA: ${pageIssues.join(" ; ")} (replace)` });
        continue;
      }

      const status =
        forbiddenFound.length ? "WARN" :
        completeness.isComplete ? "OK" : "WARN";

      const notesParts = [];
      notesParts.push("Replaced audit spine");
      if (forbiddenFound.length) notesParts.push(`Forbidden detected: ${forbiddenFound.join(" | ")}`);
      if (!completeness.isComplete) {
        if (!completeness.hasAnyFormula) notesParts.push("Missing formulas (review needed)");
        if (!completeness.hasAnySource) notesParts.push("Missing sources (review needed)");
      }
      if (SCRUB_COMPETITORS) notesParts.push("Scrubbed competitor refs");

      rows.push({ slug, file: filePath, status, notes: notesParts.join(" ; ") });
      continue;
    }

    // Inject path
    const $ = cheerio.load(html, { decodeEntities: false });
    ensureAuditCss($);
    if (SCRUB_COMPETITORS) scrubCompetitorRefs($);

    const where = injectIntoArticleOrMain($, spine);
    const outHtml = $.html();

    const pageIssues = pageHardQA(outHtml);
    fs.writeFileSync(filePath, outHtml, "utf8");

    if (pageIssues.length) {
      rows.push({ slug, file: filePath, status: "FAIL", notes: `Page Hard QA: ${pageIssues.join(" ; ")} (injected into ${where})` });
      continue;
    }

    const status =
      forbiddenFound.length ? "WARN" :
      completeness.isComplete ? "OK" : "WARN";

    const notesParts = [];
    notesParts.push(`Injected audit spine into ${where}`);
    if (forbiddenFound.length) notesParts.push(`Forbidden detected: ${forbiddenFound.join(" | ")}`);
    if (!completeness.isComplete) {
      if (!completeness.hasAnyFormula) notesParts.push("Missing formulas (review needed)");
      if (!completeness.hasAnySource) notesParts.push("Missing sources (review needed)");
    }
    if (SCRUB_COMPETITORS) notesParts.push("Scrubbed competitor refs");

    rows.push({ slug, file: filePath, status, notes: notesParts.join(" ; ") });
  }

  writeCsv(rows);

  const ok = rows.filter(r => r.status === "OK").length;
  const warn = rows.filter(r => r.status === "WARN").length;
  const fail = rows.filter(r => r.status === "FAIL").length;

  console.log(`Done. OK=${ok} WARN=${warn} FAIL=${fail}`);
  console.log(`Report: ${OUT_CSV}`);

  if (fail > 0) process.exit(2);
}

main();
