// scripts/qa-template-manifest.mjs
//
// Manifest-driven template invariants gate for CalcDomain pages under sito_modificato/.
//
// Run:
//   node scripts/qa-template-manifest.mjs qa/template-manifest.json
//
// Install deps:
//   npm i -D cheerio fast-glob
//
// Env:
//   QA_FAIL_FAST=1        (default 0)
//   QA_MAX_FILES=5000     (default unlimited)

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import * as cheerio from "cheerio";
import fg from "fast-glob";

const FAIL_FAST = process.env.QA_FAIL_FAST === "1";
const MAX_FILES = process.env.QA_MAX_FILES ? Number.parseInt(process.env.QA_MAX_FILES, 10) : Infinity;

function die(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}
function readJson(p) {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}
function rel(p) {
  return path.relative(process.cwd(), p);
}
function fail(msg) {
  return { ok: false, msg };
}
function ok() {
  return { ok: true };
}

function indexOfId(html, id) {
  const re = new RegExp(`\\bid\\s*=\\s*["']${id}["']`, "i");
  const m = re.exec(html);
  return m ? m.index : -1;
}
function countIdOccurrencesRaw(html, id) {
  return (html.match(new RegExp(`\\bid\\s*=\\s*["']${id}["']`, "gi")) || []).length;
}

function mergeDefaults(defaults, page) {
  const d = defaults || {};
  const p = page || {};
  return {
    globalIds: Array.isArray(p.globalIds) ? p.globalIds : (d.globalIds || []),
    globalIdOrder: Array.isArray(p.globalIdOrder) ? p.globalIdOrder : (d.globalIdOrder || []),
    globalClasses: Array.isArray(p.globalClasses) ? p.globalClasses : (d.globalClasses || []),

    require: { ...(d.require || {}), ...(p.require || {}) },
    featureMode: { ...(d.featureMode || {}), ...(p.featureMode || {}) },
    safety: { ...(d.safety || {}), ...(p.safety || {}) }
  };
}

function ensureOrder(html, orderedIds, label) {
  let prev = -1;
  for (const id of orderedIds) {
    const idx = indexOfId(html, id);
    if (idx < 0) return fail(`${label}: Missing required anchor id="${id}" (order check).`);
    if (idx <= prev) return fail(`${label}: Section order violation at id="${id}". Expected order: ${orderedIds.join(" → ")}`);
    prev = idx;
  }

  // If scheduleWrap exists, enforce it is after calcHero and before howToUse.
  const idxSched = indexOfId(html, "scheduleWrap");
  if (idxSched >= 0) {
    const idxCalc = indexOfId(html, "calcHero");
    const idxHow = indexOfId(html, "howToUse");
    if (!(idxSched > idxCalc && idxSched < idxHow)) {
      return fail(`${label}: scheduleWrap must appear after calcHero and before howToUse.`);
    }
  }

  return ok();
}

function ensureUniqueIds($, html, ids, label) {
  for (const id of ids) {
    const rawCount = countIdOccurrencesRaw(html, id);
    if (rawCount !== 1) return fail(`${label}: ID "${id}" must exist exactly once; found ${rawCount}.`);
    if ($(`#${id}`).length !== 1) return fail(`${label}: DOM ID "${id}" must exist exactly once; found ${$(`#${id}`).length}.`);
  }
  return ok();
}

function ensureIdsPresent($, html, ids, label) {
  for (const id of ids) {
    const rawCount = countIdOccurrencesRaw(html, id);
    if (rawCount < 1) return fail(`${label}: Missing required id="${id}".`);
    if ($(`#${id}`).length < 1) return fail(`${label}: Missing DOM element #${id}.`);
  }
  return ok();
}

function ensureClasses($, classes, label) {
  for (const cls of classes) {
    if ($(`.${cls}`).length < 1) return fail(`${label}: Required class ".${cls}" not found.`);
  }
  return ok();
}

function checkHeroStructure($, label) {
  const hero = $("#calcHero");
  if (hero.length !== 1) return fail(`${label}: #calcHero must exist exactly once.`);

  const directSections = hero.children("section.card");
  if (directSections.length !== 2) {
    return fail(`${label}: #calcHero must have exactly two direct child <section class="card">; found ${directSections.length}.`);
  }

  const inputsOk = hero.children("section#inputsCard.card").length === 1;
  const resultsOk = hero.children("section#resultsCard.card").length === 1;
  if (!inputsOk || !resultsOk) {
    return fail(`${label}: #calcHero must contain direct children: section#inputsCard.card and section#resultsCard.card.`);
  }

  return ok();
}

// Feature modes:
// - "require" => must exist and must validate
// - "if-present-then-validate" => validate only if present
// - "ignore" => skip entirely
function shouldRequire(mode, explicitRequire) {
  if (mode === "require") return true;
  if (mode === "ignore") return false;
  // if-present-then-validate
  return !!explicitRequire;
}

function checkScheduleFeature($, html, mode, requireFlag, label) {
  if (mode === "ignore") return ok();

  const hasSchedule = countIdOccurrencesRaw(html, "scheduleWrap") > 0 || countIdOccurrencesRaw(html, "scheduleBody") > 0;
  const required = mode === "require" ? true : !!requireFlag;

  if (required && !hasSchedule) return fail(`${label}: schedule required but scheduleWrap/scheduleBody not found.`);
  if (!hasSchedule) return ok();

  const uniq = ensureUniqueIds($, html, ["scheduleWrap", "scheduleBody"], `${label} (schedule)`);
  if (!uniq.ok) return uniq;

  const wrap = $("#scheduleWrap");
  if (!wrap.hasClass("tableWrap")) return fail(`${label} (schedule): #scheduleWrap must have class "tableWrap".`);
  if (wrap.find("tbody#scheduleBody").length !== 1) return fail(`${label} (schedule): #scheduleWrap must contain tbody#scheduleBody exactly once.`);

  return ok();
}

function checkCsvFeature($, html, mode, requireFlag, label) {
  if (mode === "ignore") return ok();

  const hasCsv = countIdOccurrencesRaw(html, "downloadCsv") > 0;
  const required = mode === "require" ? true : !!requireFlag;

  if (required && !hasCsv) return fail(`${label}: csv required but #downloadCsv not found.`);
  if (!hasCsv) return ok();

  return ensureUniqueIds($, html, ["downloadCsv"], `${label} (csv)`);
}

function checkButtonsFeature($, html, mode, requireFlag, label) {
  if (mode === "ignore") return ok();

  const hasCalc = countIdOccurrencesRaw(html, "calcBtn") > 0;
  const hasReset = countIdOccurrencesRaw(html, "resetBtn") > 0;
  const required = mode === "require" ? true : !!requireFlag;

  if (required && (!hasCalc || !hasReset)) return fail(`${label}: buttons required but calcBtn/resetBtn missing.`);

  // If present, must be unique
  for (const id of ["calcBtn", "resetBtn"]) {
    const rawCount = countIdOccurrencesRaw(html, id);
    if (rawCount === 0) continue;
    if (rawCount !== 1) return fail(`${label} (buttons): ID "${id}" must exist exactly once; found ${rawCount}.`);
    if ($(`#${id}`).length !== 1) return fail(`${label} (buttons): DOM #${id} must exist exactly once.`);
  }

  return ok();
}

function checkMetaDetails($, html, mode, requireFlag, requiredMetaIds, label) {
  if (mode === "ignore") return ok();

  const meta = $("#pageMeta");
  if (meta.length !== 1) return fail(`${label}: #pageMeta must exist exactly once.`);

  const metaIds = (requiredMetaIds && requiredMetaIds.length)
    ? requiredMetaIds
    : ["formulaDetails", "citationDetails", "changelogDetails"];

  const anyPresent = metaIds.some((id) => countIdOccurrencesRaw(html, id) > 0);
  const required = mode === "require" ? true : !!requireFlag;

  if (required && !anyPresent) return fail(`${label}: metaDetails required but none found.`);
  if (!anyPresent) return ok();

  for (const id of metaIds) {
    const rawCount = countIdOccurrencesRaw(html, id);
    if (rawCount !== 1) return fail(`${label} (meta): details#${id} must exist exactly once; found ${rawCount}.`);
    if (meta.find(`details#${id}`).length !== 1) return fail(`${label} (meta): #pageMeta must contain details#${id} exactly once.`);
  }

  return ok();
}

function checkSafety(html, safetyCfg, label) {
  const cfg = safetyCfg || {};
  const forbid = Array.isArray(cfg.forbidTokens) ? cfg.forbidTokens : [];

  if (cfg.requireStrictIife) {
    const hasIifeStrict =
      /\(\s*\(\s*\)\s*=>\s*\{[\s\S]{0,2000}['"]use strict['"]\s*;/.test(html) ||
      /function\s*\(\s*\)\s*\{[\s\S]{0,2000}['"]use strict['"]\s*;/.test(html);
    if (!hasIifeStrict) return fail(`${label}: JS must contain an IIFE that sets 'use strict';`);
  }

  if (cfg.requireDebounceIfUpdateExists) {
    const hasUpdate = /\bfunction\s+update\s*\(|\bconst\s+update\s*=\s*\(/.test(html);
    if (hasUpdate) {
      const hasDebounce = /clearTimeout\s*\(\s*\w+\s*\)/.test(html) && /setTimeout\s*\(\s*update\s*,\s*100\s*\)/.test(html);
      if (!hasDebounce) return fail(`${label}: update() exists but debounced update pattern not found.`);
    }
  }

  for (const token of forbid) {
    const re = new RegExp(`\\b${token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`);
    if (re.test(html)) return fail(`${label}: forbidden token "${token}" found in source.`);
  }

  return ok();
}

async function autoDiscoverPages(autoDiscover) {
  const include = autoDiscover?.include || [];
  const exclude = autoDiscover?.exclude || [];
  if (!include.length) return [];

  const matches = await fg(include, {
    cwd: process.cwd(),
    onlyFiles: true,
    unique: true,
    absolute: true,
    ignore: ["**/node_modules/**", ...exclude]
  });

  return matches
    .slice(0, MAX_FILES)
    .map((abs) => {
      const relPath = path.relative(process.cwd(), abs).replace(/\\/g, "/");
      const base = path.basename(relPath, ".html");
      return {
        id: base,
        match: { path: relPath }
      };
    });
}

async function main() {
  const manifestPath = process.argv[2];
  if (!manifestPath) die(`Usage: node scripts/qa-template-manifest.mjs qa/template-manifest.json`, 2);

  const absManifest = path.resolve(process.cwd(), manifestPath);
  if (!fs.existsSync(absManifest)) die(`Manifest not found: ${rel(absManifest)}`);

  const manifest = readJson(absManifest);
  if (manifest.version !== 1) die(`Unsupported manifest version: ${manifest.version}`);

  const defaults = manifest.defaults || {};
  let pages = Array.isArray(manifest.pages) ? manifest.pages.slice() : [];

  if (manifest.autoDiscover) {
    const discovered = await autoDiscoverPages(manifest.autoDiscover);
    const explicitPaths = new Set(pages.map((p) => p?.match?.path).filter(Boolean));
    for (const d of discovered) {
      if (!explicitPaths.has(d.match.path)) pages.push(d);
    }
  }

  if (!pages.length) die(`No pages found. Provide pages[] or autoDiscover.include[].`);

  // Build file list and ensure no overlap
  const fileOwners = new Map();
  const expanded = [];

  for (const page of pages) {
    const p = page?.match?.path;
    if (!p) die(`Page "${page.id || "<no id>"}" missing match.path.`);

    const abs = path.resolve(process.cwd(), p);
    if (!fs.existsSync(abs)) {
      console.error(`[QA-MANIFEST] WARN: file not found for page "${page.id}": ${p}`);
      continue;
    }

    const prev = fileOwners.get(abs);
    if (prev) die(`[QA-MANIFEST] FAIL: file matched by multiple page entries: ${p} owners=${prev} AND ${page.id}`, 1);
    fileOwners.set(abs, page.id || "unknown");
    expanded.push({ page, abs });
  }

  if (!expanded.length) die(`[QA-MANIFEST] FAIL: No existing files were resolved from manifest.`);

  let passed = 0;
  let failed = 0;

  for (const { page, abs } of expanded) {
    const cfg = mergeDefaults(defaults, page);
    const html = fs.readFileSync(abs, "utf8");
    const $ = cheerio.load(html);
    const label = `[${page.id || "page"}] ${rel(abs)}`;

    // Global invariants
    let r = ensureOrder(html, cfg.globalIdOrder, label);
    if (!r.ok) gotoFail(r);

    r = ensureUniqueIds($, html, cfg.globalIds, label);
    if (!r.ok) gotoFail(r);

    r = ensureClasses($, cfg.globalClasses, label);
    if (!r.ok) gotoFail(r);

    r = checkHeroStructure($, label);
    if (!r.ok) gotoFail(r);

    // Per-page requiredIds (optional)
    if (Array.isArray(page.requiredIds) && page.requiredIds.length) {
      r = ensureIdsPresent($, html, page.requiredIds, `${label} (requiredIds)`);
      if (!r.ok) gotoFail(r);
    }

    // Features (manifest-controlled)
    const scheduleMode = cfg.featureMode?.schedule || "if-present-then-validate";
    const csvMode = cfg.featureMode?.csv || "if-present-then-validate";
    const metaMode = cfg.featureMode?.metaDetails || "require";
    const buttonsMode = cfg.featureMode?.buttons || "if-present-then-validate";

    r = checkScheduleFeature($, html, scheduleMode, cfg.require?.schedule, label);
    if (!r.ok) gotoFail(r);

    r = checkCsvFeature($, html, csvMode, cfg.require?.csv, label);
    if (!r.ok) gotoFail(r);

    r = checkButtonsFeature($, html, buttonsMode, cfg.require?.buttons, label);
    if (!r.ok) gotoFail(r);

    r = checkMetaDetails($, html, metaMode, cfg.require?.metaDetails, page.requiredMetaDetailsIds, label);
    if (!r.ok) gotoFail(r);

    // Safety
    r = checkSafety(html, cfg.safety, label);
    if (!r.ok) gotoFail(r);

    passed++;
    continue;

    function gotoFail(res) {
      failed++;
      console.error(`[QA-MANIFEST] FAIL: ${res.msg}`);
      if (FAIL_FAST) process.exit(1);
    }
  }

  const total = passed + failed;
  if (failed > 0) {
    console.error(`[QA-MANIFEST] SUMMARY: total=${total} passed=${passed} failed=${failed}`);
    process.exit(1);
  }

  console.log(`[QA-MANIFEST] OK: All checks passed. total=${total}`);
  process.exit(0);
}

main().catch((e) => {
  console.error(`[QA-MANIFEST] ERROR:`, e);
  process.exit(1);
});
