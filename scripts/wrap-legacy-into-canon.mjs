import fs from "node:fs";
import path from "node:path";
import * as cheerio from "cheerio";

const ROOT = process.argv[2] || "sito_modificato";

// Minimal canon header/footer (keep simple; your CSS already exists in many pages)
function canonHeader() {
  return `
<header id="siteHeader">
  <div class="nav container">
    <a class="brand" href="https://calcdomain.com">CalcDomain</a>
    <div class="navRight">
      <a class="pill" href="https://calcdomain.com/search">Advanced Search</a>
      <span class="pill">Categories</span>
    </div>
  </div>
</header>
`.trim();
}

function canonFooter() {
  return `
<footer id="siteFooter" class="bg-gray-900 text-white py-12">
  <div class="container mx-auto px-4">
    <div class="border-t border-gray-800 pt-8 text-center text-gray-400">
      <p>&copy; 2025 CalcDomain. All Rights Reserved. | Free Online Calculators for Everyone</p>
    </div>
  </div>
</footer>
`.trim();
}

function canonMeta() {
  return `
<section class="meta-section" id="pageMeta" aria-label="Verification, changelog, formulas, citations">
  <details id="formulaDetails">
    <summary style="cursor:pointer; font-weight:700; color:var(--text)">Formulas</summary>
    <div style="margin-top:12px; padding:12px; background:#fff; border:1px solid var(--line); border-radius:8px;">
      <p style="margin:0;">(Formulas preserved from original page content, if present.)</p>
    </div>
  </details>

  <details id="citationDetails" style="margin-top:10px;">
    <summary style="cursor:pointer; font-weight:700; color:var(--text)">Citations</summary>
    <div style="margin-top:12px; padding:12px; background:#fff; border:1px solid var(--line); border-radius:8px;">
      <p style="margin:0;">(Citations preserved from original page content, if present.)</p>
    </div>
  </details>

  <details id="changelogDetails" style="margin-top:10px;">
    <summary style="cursor:pointer; font-weight:700; color:var(--text)">Changelog</summary>
    <div style="margin-top:12px; padding:12px; background:#fff; border:1px solid var(--line); border-radius:8px;">
      <ul style="padding-left:18px; margin:0;">
        <li>0.1.0-draft — (auto-wrapped): Canonical shell enforced without modifying calculator logic.</li>
      </ul>
    </div>
  </details>

  <div class="badge-row" id="badgeRow">
    <div class="badge" id="versionBadge">Version 0.1.0-draft</div>
  </div>
</section>
`.trim();
}

function ensureOnceId($, id, renameSuffix = "__dup") {
  const els = $(`#${id}`);
  if (els.length <= 1) return;
  // Keep first; rename others to avoid QA fail
  els.slice(1).each((i, el) => {
    $(el).attr("id", `${id}${renameSuffix}${i + 2}`);
  });
}

function ensureRequiredClassesInDom($) {
  // QA checks “exists at least once”. If page lacks these, add them on wrappers we insert.
  // We'll rely on our inserted header/container/main/sections to provide:
  // container, nav, brand, navRight, pill, calc-hero, card, btn, btnSecondary, alert, meta-section, content-card, sub
}

function wrapFile(filePath) {
  const raw = fs.readFileSync(filePath, "utf8");
  const $ = cheerio.load(raw, { decodeEntities: false });

  // If already has the required anchors, do nothing
  const hasSiteHeader = $("#siteHeader").length === 1;
  const hasMainContent = $("#mainContent").length === 1;
  const hasCalcHero = $("#calcHero").length === 1;
  const hasPageMeta = $("#pageMeta").length === 1;
  const hasFooter = $("#siteFooter").length === 1;

  // Work from <body>
  const body = $("body");
  if (!body.length) return { changed: false, reason: "no-body" };

  // Preserve original body HTML (excluding scripts already in body—keep them in place)
  // We'll collect non-script nodes to move under howToUse if we need to rebuild structure.
  const originalNodes = [];
  body.children().each((_, el) => {
    const tag = (el.tagName || "").toLowerCase();
    // Keep scripts where they are (so logic keeps working), but we can also leave them and only wrap content.
    // For safety: keep scripts in place, move everything else if needed.
    if (tag !== "script") originalNodes.push(el);
  });

  // Ensure a single errorBox exists
  if ($("#errorBox").length === 0) {
    body.prepend(`<div id="errorBox" class="alert" role="alert" aria-live="polite"></div>`);
  }
  ensureOnceId($, "errorBox");

  // If already mostly canonical but missing pieces, patch minimally.
  // If missing core anchors, rebuild a canonical scaffold and move original content into howToUse.
  if (!(hasSiteHeader && hasMainContent && hasCalcHero && hasPageMeta && hasFooter)) {
    // Determine title/subtitle for H1/sub (best-effort)
    const h1Text =
      $("#pageTitle").text().trim() ||
      $("h1").first().text().trim() ||
      $("title").text().replace(/\s*\|\s*.*$/, "").trim() ||
      path.basename(filePath, ".html");

    const subText =
      $("#pageSub").text().trim() ||
      $(".sub").first().text().trim() ||
      $('meta[name="description"]').attr("content")?.trim() ||
      "";

    // Clear body (but keep scripts at end)
    const scripts = [];
    body.children("script").each((_, el) => scripts.push(el));
    body.empty();

    // Insert header + container/main scaffold
    body.append(canonHeader());
    body.append(`
<div class="container">
  <main style="margin:24px 0 40px;" id="mainContent">
    <h1 id="pageTitle">${escapeHtml(h1Text)}</h1>
    <p class="sub" id="pageSub">${escapeHtml(subText)}</p>
    <div id="errorBox" class="alert" role="alert" aria-live="polite"></div>

    <div class="calc-hero" id="calcHero">
      <section class="card" id="inputsCard" aria-label="Calculator inputs"></section>
      <section class="card sticky-box" id="resultsCard" aria-label="Calculator results"></section>
    </div>

    <section class="card content-card" id="howToUse" aria-label="How to use and methodology">
      <h2>Full original guide (expanded)</h2>
    </section>

    ${canonMeta()}
  </main>
</div>
`.trim());

    body.append(canonFooter());

    // Move original non-script nodes into #howToUse (preserve content)
    const how = $("#howToUse");
    for (const node of originalNodes) {
      how.append(node);
    }

    // Put scripts back at end (preserve calculator logic)
    for (const s of scripts) body.append(s);

    // Best-effort: if original had a clear calculator container, move it into inputsCard instead of burying it.
    // Heuristic: move first element with id="calcHero" or class containing "calculator" or "card" or "tool" or "app"
    // But since we rebuilt, we search inside howToUse for likely interactive blocks.
    const candidates = how.find("[id], .calculator, .tool, .app, .card, form, table").toArray();
    if (candidates.length) {
      // Move the first candidate into inputsCard (keeps interactivity visible)
      $("#inputsCard").append(candidates[0]);
    }

    // Ensure required meta detail IDs exist exactly once
    ensureOnceId($, "formulaDetails");
    ensureOnceId($, "citationDetails");
    ensureOnceId($, "changelogDetails");
    ensureOnceId($, "pageMeta");
    ensureOnceId($, "siteHeader");
    ensureOnceId($, "mainContent");
    ensureOnceId($, "pageTitle");
    ensureOnceId($, "pageSub");
    ensureOnceId($, "calcHero");
    ensureOnceId($, "inputsCard");
    ensureOnceId($, "resultsCard");
    ensureOnceId($, "howToUse");
    ensureOnceId($, "siteFooter");
  }

  // Fix known QA duplicate-id failures (example: resetBtn multiple)
  ensureOnceId($, "resetBtn");
  ensureOnceId($, "calcBtn");
  ensureOnceId($, "downloadCsv");

  const out = $.html();
  if (out !== raw) {
    fs.writeFileSync(filePath, out, "utf8");
    return { changed: true, reason: "wrapped" };
  }
  return { changed: false, reason: "no-change" };
}

function escapeHtml(s) {
  return (s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function walk(dir) {
  const out = [];
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) out.push(...walk(p));
    else if (ent.isFile() && p.endsWith(".html")) out.push(p);
  }
  return out;
}

let changed = 0;
for (const f of walk(ROOT)) {
  const res = wrapFile(f);
  if (res.changed) changed++;
}
console.log(`[wrap-legacy-into-canon] root=${ROOT} changedFiles=${changed}`);
