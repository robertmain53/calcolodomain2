// scripts/qa-template-manifest.mjs
//
// Manifest-driven CI gate for CalcDomain calculator pages.
//
// Run:
//   node scripts/qa-template-manifest.mjs ./qa/template-manifest.json
//
// Requires:
//   npm i -D cheerio fast-glob
//
// Env:
//   QA_FAIL_FAST=1                (default 0)
//   QA_MAX_FILES=5000             (default unlimited)

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
  const raw = fs.readFileSync(p, "utf8");
  return JSON.parse(raw);
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

function ensureOrder(html, orderedIds, label) {
  let prev = -1;
  for (const id of orderedIds) {
    const idx = indexOfId(html, id);
    if (idx < 0) return fail(`${label}: Missing required anchor id="${id}" (order check).`);
    if (idx <= prev) return fail(`${label}: Section order violation at id="${id}". Expected order: ${orderedIds.join(" → ")}`);
    prev = idx;
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

function checkScheduleFeature($, html, requireSchedule, label) {
  const hasSchedule = countIdOccurrencesRaw(html, "scheduleWrap") > 0 || countIdOccurrencesRaw(html, "scheduleBody") > 0;

  if (requireSchedule && !hasSchedule) return fail(`${label}: schedule required but scheduleWrap/scheduleBody not found.`);
  if (!hasSchedule) return ok();

  const uniq = ensureUniqueIds($, html, ["scheduleWrap", "scheduleBody"], `${label} (schedule)`);
  if (!uniq.ok) return uniq;

  const wrap = $("#scheduleWrap");
  if (!wrap.hasClass("tableWrap")) return fail(`${label} (schedule): #scheduleWrap must have class "tableWrap".`);
  if (wrap.find("tbody#scheduleBody").length !== 1) return fail(`${label} (schedule): #scheduleWrap must contain tbody#scheduleBody exactly once.`);

  // Order: scheduleWrap must be after calcHero and before howToUse
  const idxCalc = indexOfId(html, "calcHero");
  const idxHow = indexOfId(html, "howToUse");
  const idxSched = indexOfId(html, "scheduleWrap");
  if (!(idxSched > idxCalc && idxSched < idxHow)) {
    return fail(`${label} (schedule): scheduleWrap must appear after calcHero and before howToUse.`);
  }

  return ok();
}

function checkCsvFeature($, html, requireCsv, label) {
  const hasCsv = countIdOccurrencesRaw(html, "downloadCsv") > 0;
  if (requireCsv && !hasCsv) return fail(`${label}: csv required but #downloadCsv not found.`);
  if (!hasCsv) return ok();

  const uniq = ensureUniqueIds($, html, ["downloadCsv"], `${label} (csv)`);
  if (!uniq.ok) return uniq;

  return ok();
}

function checkMetaDetails($, html, requireMetaDetails, requiredMetaIds, label) {
  const meta = $("#pageMeta");
  if (meta.length !== 1) return fail(`${label}: #pageMeta must exist exactly once.`);

  const metaIds = requiredMetaIds?.length ? requiredMetaIds : ["formulaDetails", "citationDetails", "changelogDetails"];
  const anyPresent = metaIds.some((id) => countIdOccurrencesRaw(html, id) > 0);

  if (requireMetaDetails && !anyPresent) return fail(`${label}: metaDetails required but no meta details blocks found.`);
  if (!anyPresent) return ok();

  for (const id of metaIds) {
    const rawCount = countIdOccurrencesRaw(html, id);
    if (rawCount !== 1) return fail(`${label} (meta): details#${id} must exist exactly once; found ${rawCount}.`);
    if (meta.find(`details#${id}`).length !== 1) return fail(`${label} (meta): #pageMeta must contain details#${id} exactly once.`);
  }

  return ok();
}

function checkButtonsFeature($, html, requireButtons, label) {
  const hasCalc = countIdOccurrencesRaw(html, "calcBtn") > 0;
  const hasReset = countIdOccurrencesRaw(html, "resetBtn") > 0;

  if (requireButtons && (!hasCalc || !hasReset)) {
    return fail(`${label}: buttons required but calcBtn/resetBtn missing.`);
  }

  // If present, must be unique
  for (const id of ["calcBtn", "resetBtn"]) {
    const rawCount = countIdOccurrencesRaw(html, id);
    if (rawCount === 0) continue;
    if (rawCount !== 1) return fail(`${label} (buttons): ID "${id}" must exist exactly once; found ${rawCount}.`);
    if ($(`#${id}`).length !== 1) return fail(`${label} (buttons): DOM #${id} must exist exactly once.`);
  }

  return ok();
}

function checkSafety(html, safetyCfg, label) {
  const cfg = safetyCfg || {};
  const forbid = Array.isArray(cfg.forbidTokens) ? cfg.forbidTokens : [];

  if (cfg.requireStrictIife) {
    const hasIifeStrict =
      /\(\s*\(\s*\)\s*=>\s*\{[\s\S]{0,1500}['"]use strict['"]\s*;/.test(html) ||
      /function\s*\(\s*\)\s*\{[\s\S]{0,1500}['"]use strict['"]\s*;/.test(html);
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

function mergeDefaults(defaults, page) {
  const d = defaults || {};
  const p = page || {};

  const require = { ...(d.require || {}), ...(p.require || {}) };
  const optionalFeatures = { ...(d.optionalFeatures || {}), ...(p.optionalFeatures || {}) };
  const safety = { ...(d.safety || {}), ...(p.safety || {}) };

  const globalIds = Array.isArray(p.globalIds) ? p.globalIds : d.globalIds;
  const globalIdOrder = Array.isArray(p.globalIdOrder) ? p.globalIdOrder : d.globalIdOrder;
  const globalClasses = Array.isArray(p.globalClasses) ? p.globalClasses : d.globalClasses;

  return {
    require,
    optionalFeatures,
    safety,
    globalIds: globalIds || [],
    globalIdOrder: globalIdOrder || [],
    globalClasses: globalClasses || []
  };
}

async function main() {
  const manifestPath = process.argv[2];
  if (!manifestPath) die(`Usage: node scripts/qa-template-manifest.mjs ./qa/template-manifest.json`, 2);

  const absManifest = path.resolve(process.cwd(), manifestPath);
  if (!fs.existsSync(absManifest)) die(`Manifest not found: ${rel(absManifest)}`);

  const manifest = readJson(absManifest);
  if (manifest.version !== 1) die(`Unsupported manifest version: ${manifest.version}`);

  const rootDirs = manifest.rootDirs?.length ? manifest.rootDirs : ["./dist"];
  const defaults = manifest.defaults || {};
  const pages = Array.isArray(manifest.pages) ? manifest.pages : [];
  if (pages.length === 0) die(`Manifest pages[] is empty.`);

  // Resolve matches -> files
  const pageToFiles = [];
  const allFiles = new Set();

  for (const page of pages) {
    const glob = page?.match?.path;
    if (!glob) die(`Page "${page.id || "<no id>"}" missing match.path glob.`);

    const matches = await fg(glob, {
      cwd: process.cwd(),
      onlyFiles: true,
      unique: true,
      absolute: true,
      ignore: ["**/node_modules/**"]
    });

    // If rootDirs are specified, filter to those
    const filtered = matches.filter((fp) => {
      const norm = fp.replace(/\\/g, "/");
      return rootDirs.some((rd) => norm.includes(path.resolve(process.cwd(), rd).replace(/\\/g, "/")));
    });

    if (filtered.length === 0) {
      console.error(`[QA-MANIFEST] WARN: No files matched for page "${page.id}" glob="${glob}" under rootDirs=${rootDirs.join(",")}`);
    }

    for (const f of filtered) allFiles.add(f);
    pageToFiles.push({ page, files: filtered });
  }

  // Detect overlap: same file matched by multiple page entries (usually an error)
  // (If you want allow overlap, remove this block.)
  const fileOwners = new Map();
  for (const { page, files } of pageToFiles) {
    for (const f of files) {
      const prev = fileOwners.get(f);
      if (prev) {
        die(
          `[QA-MANIFEST] FAIL: file matched by multiple page entries:\n  file=${rel(f)}\n  owners=${prev} AND ${page.id}`,
          1
        );
      }
      fileOwners.set(f, page.id || "unknown");
    }
  }

  const filesList = Array.from(allFiles);
  if (filesList.length === 0) die(`[QA-MANIFEST] FAIL: No HTML files were matched by manifest.`);

  if (filesList.length > MAX_FILES) filesList.length = MAX_FILES;

  let passed = 0;
  let failed = 0;

  for (const { page, files } of pageToFiles) {
    const cfg = mergeDefaults(defaults, page);

    for (const fp of files) {
      const html = fs.readFileSync(fp, "utf8");
      const $ = cheerio.load(html);
      const label = `[${page.id || "page"}] ${rel(fp)}`;

      // Global order + global unique IDs + required classes + hero structure
      let r = ensureOrder(html, cfg.globalIdOrder, label);
      if (!r.ok) gotoFail(r);

      r = ensureUniqueIds($, html, cfg.globalIds, label);
      if (!r.ok) gotoFail(r);

      r = ensureClasses($, cfg.globalClasses, label);
      if (!r.ok) gotoFail(r);

      r = checkHeroStructure($, label);
      if (!r.ok) gotoFail(r);

      // Per-page required IDs (calculator-specific)
      if (Array.isArray(page.requiredIds) && page.requiredIds.length > 0) {
        r = ensureIdsPresent($, html, page.requiredIds, `${label} (requiredIds)`);
        if (!r.ok) gotoFail(r);
      }

      // Features
      const requireSchedule = !!cfg.require.schedule;
      const requireCsv = !!cfg.require.csv;
      const requireMetaDetails = cfg.require.metaDetails !== false; // default true in many setups
      const requireButtons = !!cfg.require.buttons;

      r = checkScheduleFeature($, html, requireSchedule, label);
      if (!r.ok) gotoFail(r);

      r = checkCsvFeature($, html, requireCsv, label);
      if (!r.ok) gotoFail(r);

      r = checkButtonsFeature($, html, requireButtons, label);
      if (!r.ok) gotoFail(r);

      r = checkMetaDetails($, html, requireMetaDetails, page.requiredMetaDetailsIds, label);
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
