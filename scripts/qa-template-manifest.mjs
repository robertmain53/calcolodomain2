// scripts/qa-template-manifest.mjs
//
// Manifest-driven template invariants gate for CalcDomain pages under sito_modificato/.
//
// Run:
//   node scripts/qa-template-manifest.mjs qa/template-manifest.json
//
// Optional:
//   QA_ARTIFACT_PATH="qa/qa-template-manifest.artifact.json" node scripts/qa-template-manifest.mjs qa/template-manifest.json
//
// Install deps:
//   npm i -D cheerio fast-glob
//
// Env:
//   QA_FAIL_FAST=1                 (default 0)
//   QA_MAX_FILES=5000              (default unlimited)
//   QA_ONLY_FILES="a.html,b.html"  (optional; batch-scoped gate)
//   QA_ARTIFACT_PATH="..."         (optional; where to write artifact json)
//   QA_BUILD_STAMP="..."           (optional; deterministic build stamp)

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import * as cheerio from "cheerio";
import fg from "fast-glob";

const FAIL_FAST = process.env.QA_FAIL_FAST === "1";
const MAX_FILES = process.env.QA_MAX_FILES
  ? Number.parseInt(process.env.QA_MAX_FILES, 10)
  : Infinity;

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

function isObject(x) {
  return !!x && typeof x === "object" && !Array.isArray(x);
}
function isNonEmptyString(x) {
  return typeof x === "string" && x.trim().length > 0;
}
function isStringArray(x) {
  return Array.isArray(x) && x.every((v) => typeof v === "string");
}

function validateFeatureModeObj(obj, label, errors) {
  if (obj == null) return;
  if (!isObject(obj)) {
    errors.push(`${label} must be an object.`);
    return;
  }
  const allowed = new Set(["require", "if-present-then-validate", "ignore"]);
  for (const [k, v] of Object.entries(obj)) {
    if (!isNonEmptyString(v) || !allowed.has(v)) {
      errors.push(
        `${label}.${k} must be one of: require | if-present-then-validate | ignore (got ${JSON.stringify(v)})`
      );
    }
  }
}

function validateRequireObj(obj, label, errors) {
  if (obj == null) return;
  if (!isObject(obj)) {
    errors.push(`${label} must be an object.`);
    return;
  }
  for (const [k, v] of Object.entries(obj)) {
    if (typeof v !== "boolean") errors.push(`${label}.${k} must be boolean (got ${JSON.stringify(v)})`);
  }
}

function validateSafetyObj(obj, label, errors) {
  if (obj == null) return;
  if (!isObject(obj)) {
    errors.push(`${label} must be an object.`);
    return;
  }
  const boolKeys = ["requireStrictIife", "requireDebounceIfUpdateExists"];
  for (const k of boolKeys) {
    if (k in obj && typeof obj[k] !== "boolean") {
      errors.push(`${label}.${k} must be boolean (got ${JSON.stringify(obj[k])})`);
    }
  }
  if ("forbidTokens" in obj) {
    if (!isStringArray(obj.forbidTokens)) {
      errors.push(`${label}.forbidTokens must be an array of strings.`);
    }
  }
}

function validateManifest(manifest) {
  const errors = [];

  if (!isObject(manifest)) errors.push(`Manifest root must be an object.`);
  if (manifest?.version !== 1) errors.push(`Unsupported manifest version: ${manifest?.version} (expected 1)`);

  if ("defaults" in manifest && manifest.defaults != null && !isObject(manifest.defaults)) {
    errors.push(`defaults must be an object if present.`);
  }

  const d = manifest.defaults || {};
  if ("globalIds" in d && d.globalIds != null && !isStringArray(d.globalIds)) errors.push(`defaults.globalIds must be string[].`);
  if ("globalIdOrder" in d && d.globalIdOrder != null && !isStringArray(d.globalIdOrder))
    errors.push(`defaults.globalIdOrder must be string[].`);
  if ("globalClasses" in d && d.globalClasses != null && !isStringArray(d.globalClasses))
    errors.push(`defaults.globalClasses must be string[].`);

  validateRequireObj(d.require, "defaults.require", errors);
  validateFeatureModeObj(d.featureMode, "defaults.featureMode", errors);
  validateSafetyObj(d.safety, "defaults.safety", errors);

  if ("pages" in manifest && manifest.pages != null) {
    if (!Array.isArray(manifest.pages)) {
      errors.push(`pages must be an array if present.`);
    } else {
      manifest.pages.forEach((p, i) => {
        const label = `pages[${i}]`;
        if (!isObject(p)) {
          errors.push(`${label} must be an object.`);
          return;
        }
        if ("id" in p && p.id != null && !isNonEmptyString(p.id)) errors.push(`${label}.id must be a non-empty string.`);
        if (!isObject(p.match)) errors.push(`${label}.match must be an object.`);
        if (!isNonEmptyString(p?.match?.path)) errors.push(`${label}.match.path must be a non-empty string.`);

        if ("globalIds" in p && p.globalIds != null && !isStringArray(p.globalIds)) errors.push(`${label}.globalIds must be string[].`);
        if ("globalIdOrder" in p && p.globalIdOrder != null && !isStringArray(p.globalIdOrder))
          errors.push(`${label}.globalIdOrder must be string[].`);
        if ("globalClasses" in p && p.globalClasses != null && !isStringArray(p.globalClasses))
          errors.push(`${label}.globalClasses must be string[].`);

        if ("requiredIds" in p && p.requiredIds != null && !isStringArray(p.requiredIds))
          errors.push(`${label}.requiredIds must be string[].`);
        if ("requiredMetaDetailsIds" in p && p.requiredMetaDetailsIds != null && !isStringArray(p.requiredMetaDetailsIds))
          errors.push(`${label}.requiredMetaDetailsIds must be string[].`);

        validateRequireObj(p.require, `${label}.require`, errors);
        validateFeatureModeObj(p.featureMode, `${label}.featureMode`, errors);
        validateSafetyObj(p.safety, `${label}.safety`, errors);
      });
    }
  }

  if ("autoDiscover" in manifest && manifest.autoDiscover != null) {
    if (!isObject(manifest.autoDiscover)) {
      errors.push(`autoDiscover must be an object if present.`);
    } else {
      if (!isStringArray(manifest.autoDiscover.include) || manifest.autoDiscover.include.length === 0) {
        errors.push(`autoDiscover.include must be a non-empty string[].`);
      }
      if ("exclude" in manifest.autoDiscover && manifest.autoDiscover.exclude != null && !isStringArray(manifest.autoDiscover.exclude)) {
        errors.push(`autoDiscover.exclude must be string[] if present.`);
      }
    }
  }

  if (errors.length) {
    die(`[QA-MANIFEST] FAIL: invalid manifest\n- ${errors.join("\n- ")}`, 2);
  }
}

function countIdOccurrencesRaw(html, id) {
  return (html.match(new RegExp(`\\bid\\s*=\\s*["']${id}["']`, "gi")) || []).length;
}

// DOM order index: robust vs raw source mentions (scripts/comments/etc.)
function domOrderIndexOfId($, id) {
  // First match of an element that actually has id=<id>
  const withId = $(`[id="${id}"]`).first();
  if (!withId.length) return -1;

  // Cheerio returns nodes in document order.
  // We use [id] as our traversal backbone; it's stable and avoids raw-text mentions.
  const all = $("[id]").toArray();
  for (let i = 0; i < all.length; i++) {
    const el = all[i];
    const $el = $(el);
    if (($el.attr("id") || "") === id) return i;
  }

  // Fallback (should not happen if selector matched)
  return -1;
}

function mergeDefaults(defaults, page) {
  const d = defaults || {};
  const p = page || {};
  return {
    globalIds: Array.isArray(p.globalIds) ? p.globalIds : (d.globalIds || []),
    globalIdOrder: Array.isArray(p.globalIdOrder) ? p.globalIdOrder : (d.globalIdOrder || []),
    globalClasses: Array.isArray(p.globalClasses) ? p.globalClasses : (d.globalClasses || []),

    require: { ...(d.require || {}), ...(p.require || {}), ...(page?.require || {}) },
    featureMode: { ...(d.featureMode || {}), ...(p.featureMode || {}) },
    safety: { ...(d.safety || {}), ...(p.safety || {}) }
  };
}

function ensureOrder($, orderedIds, label) {
  let prev = -1;
  for (const id of orderedIds) {
    const idx = domOrderIndexOfId($, id);
    if (idx < 0) return fail(`${label}: Missing required anchor id="${id}" (DOM order check).`);
    if (idx <= prev) {
      return fail(`${label}: Section order violation at id="${id}". Expected order: ${orderedIds.join(" → ")}`);
    }
    prev = idx;
  }

  // If scheduleWrap exists, enforce it is after calcHero and before howToUse (DOM-based).
  const idxSched = domOrderIndexOfId($, "scheduleWrap");
  if (idxSched >= 0) {
    const idxCalc = domOrderIndexOfId($, "calcHero");
    const idxHow = domOrderIndexOfId($, "howToUse");
    if (!(idxSched > idxCalc && idxSched < idxHow)) {
      return fail(`${label}: scheduleWrap must appear after calcHero and before howToUse (DOM order).`);
    }
  }

  return ok();
}

function ensureUniqueIds($, html, ids, label) {
  for (const id of ids) {
    const rawCount = countIdOccurrencesRaw(html, id);
    if (rawCount !== 1) return fail(`${label}: ID "${id}" must exist exactly once; found ${rawCount}.`);
    if ($(`#${id}`).length !== 1) {
      return fail(`${label}: DOM ID "${id}" must exist exactly once; found ${$(`#${id}`).length}.`);
    }
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
    return fail(
      `${label}: #calcHero must have exactly two direct child <section class="card">; found ${directSections.length}.`
    );
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
function checkScheduleFeature($, html, mode, requireFlag, label) {
  if (mode === "ignore") return ok();

  const hasSchedule =
    countIdOccurrencesRaw(html, "scheduleWrap") > 0 ||
    countIdOccurrencesRaw(html, "scheduleBody") > 0;

  const required = mode === "require" ? true : !!requireFlag;

  if (required && !hasSchedule) return fail(`${label}: schedule required but scheduleWrap/scheduleBody not found.`);
  if (!hasSchedule) return ok();

  const uniq = ensureUniqueIds($, html, ["scheduleWrap", "scheduleBody"], `${label} (schedule)`);
  if (!uniq.ok) return uniq;

  const wrap = $("#scheduleWrap");
  if (!wrap.hasClass("tableWrap")) return fail(`${label} (schedule): #scheduleWrap must have class "tableWrap".`);
  if (wrap.find("tbody#scheduleBody").length !== 1)
    return fail(`${label} (schedule): #scheduleWrap must contain tbody#scheduleBody exactly once.`);

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
    if (meta.find(`details#${id}`).length !== 1)
      return fail(`${label} (meta): #pageMeta must contain details#${id} exactly once.`);
  }

  return ok();
}

function extractInlineScripts(html) {
  const scripts = [];
  const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  let match;
  while ((match = re.exec(html)) !== null) {
    const attrs = match[1] || "";
    if (/\bsrc\s*=/.test(attrs)) continue;
    if (/type\s*=\s*["']application\/ld\+json["']/.test(attrs)) continue;
    scripts.push(match[2] || "");
  }
  return scripts;
}

function checkDebouncedUpdateContract(html) {
  const scripts = extractInlineScripts(html);
  const scriptsInlineCount = scripts.length;

  const updateFnRe = /\bfunction\s+update\s*\(|\bconst\s+update\s*=\s*\(/;
  const candidateScriptsWithUpdate = scripts.filter((s) => updateFnRe.test(s)).length;
  const hasUpdate = candidateScriptsWithUpdate > 0;

  const hasInputsCardSelector = scripts.some((s) => /#inputsCard\b/.test(s) || /inputsCard/.test(s));
  const hasAddEventListenerInput = scripts.some((s) => /addEventListener\s*\(\s*['"]input['"]/.test(s));
  const hasAddEventListenerChange = scripts.some((s) => /addEventListener\s*\(\s*['"]change['"]/.test(s));

  let handlersResolveToUpdate = false;
  const handlerNames = new Set();
  const addEvtRe = /addEventListener\s*\(\s*['"](?:input|change)['"]\s*,\s*([a-zA-Z_$][\w$]*)/g;
  for (const s of scripts) {
    let m;
    while ((m = addEvtRe.exec(s)) !== null) handlerNames.add(m[1]);
  }

  const directHandlerToUpdate = scripts.some((s) =>
    /addEventListener\s*\(\s*['"](?:input|change)['"]\s*,\s*update\s*\)/.test(s)
  );

  let debouncedUpdateLinksToUpdate = false;
  let debounceDelayMs = null;
  let debounceDelayConflict = false;
  const debounceAssignRe = /\bconst\s+([a-zA-Z_$][\w$]*)\s*=\s*debounce\s*\(\s*([a-zA-Z_$][\w$]*)\s*,\s*(\d+)\s*\)/g;
  for (const s of scripts) {
    let m;
    while ((m = debounceAssignRe.exec(s)) !== null) {
      const handler = m[1];
      const target = m[2];
      const delay = Number.parseInt(m[3], 10);
      if (debounceDelayMs == null) debounceDelayMs = delay;
      else if (debounceDelayMs !== delay) debounceDelayConflict = true;
      if (target === "update") {
        if (handlerNames.has(handler)) debouncedUpdateLinksToUpdate = true;
      } else {
        const targetRe = new RegExp(
          `function\\s+${target}\\s*\\([^)]*\\)\\s*\\{[\\s\\S]*?\\bupdate\\s*\\(`,
          "m"
        );
        const targetArrowRe = new RegExp(
          `\\bconst\\s+${target}\\s*=\\s*\\([^)]*\\)\\s*=>\\s*\\{?[\\s\\S]*?\\bupdate\\s*\\(`,
          "m"
        );
        if ((targetRe.test(s) || targetArrowRe.test(s)) && handlerNames.has(handler)) {
          debouncedUpdateLinksToUpdate = true;
        }
      }
    }
  }

  for (const name of handlerNames) {
    if (name === "update") {
      handlersResolveToUpdate = true;
      break;
    }
    const fnRe = new RegExp(`function\\s+${name}\\s*\\([^)]*\\)\\s*\\{[\\s\\S]*?\\bupdate\\s*\\(`, "m");
    const arrowRe = new RegExp(`\\bconst\\s+${name}\\s*=\\s*\\([^)]*\\)\\s*=>\\s*\\{?[\\s\\S]*?\\bupdate\\s*\\(`, "m");
    if (scripts.some((s) => fnRe.test(s) || arrowRe.test(s))) {
      handlersResolveToUpdate = true;
      break;
    }
  }
  if (directHandlerToUpdate || debouncedUpdateLinksToUpdate) handlersResolveToUpdate = true;

  const hasDebounceCall = scripts.some((s) => /\bdebounce\s*\(/.test(s));

  let hasSetTimeout100 = false;
  let setTimeoutDelayMs = null;
  let setTimeoutDelayConflict = false;
  const setTimeoutRe = /setTimeout\s*\(\s*(?:update|\(\s*\)\s*=>\s*update\s*\(|function\s*\(\s*\)\s*\{\s*update\s*\()([\s\S]*?),\s*(\d+)\s*\)/g;
  for (const s of scripts) {
    let m;
    while ((m = setTimeoutRe.exec(s)) !== null) {
      const delay = Number.parseInt(m[2], 10);
      if (setTimeoutDelayMs == null) setTimeoutDelayMs = delay;
      else if (setTimeoutDelayMs !== delay) setTimeoutDelayConflict = true;
      if (delay === 100) hasSetTimeout100 = true;
    }
  }
  const hasClearTimeoutPattern = scripts.some((s) => /clearTimeout\s*\(\s*\w+\s*\)/.test(s));

  let effectiveDelayMs = null;
  if (debounceDelayConflict || setTimeoutDelayConflict) {
    effectiveDelayMs = "other";
  } else if (debounceDelayMs != null) {
    effectiveDelayMs = debounceDelayMs;
  } else if (setTimeoutDelayMs != null) {
    effectiveDelayMs = setTimeoutDelayMs;
  }

  const reasons = [];
  if (hasUpdate) {
    if (!hasInputsCardSelector || !hasAddEventListenerInput || !hasAddEventListenerChange) {
      reasons.push("update() found but no #inputsCard event wiring");
    }
    if (!handlersResolveToUpdate) {
      reasons.push("handlers do not resolve to update()");
    }
    const hasDebounceDelay100 = effectiveDelayMs === 100 || hasSetTimeout100;
    if (!hasDebounceDelay100) {
      reasons.push("event wiring found but 100ms debounce not detected");
    }
  }

  const ok = !hasUpdate || reasons.length === 0;
  return {
    ok,
    reasons,
    details: {
      hasUpdate,
      scriptsInlineCount,
      candidateScriptsWithUpdate,
      wiring: {
        hasInputsCardSelector,
        hasAddEventListenerInput,
        hasAddEventListenerChange,
        handlersResolveToUpdate
      },
      debounce: {
        hasDebounceCall,
        hasSetTimeout100,
        hasClearTimeoutPattern,
        effectiveDelayMs
      }
    }
  };
}

function checkSafety(html, safetyCfg, label) {
  const cfg = safetyCfg || {};

  if (cfg.requireStrictIife) {
    const hasIifeStrict =
      /\(\s*\(\s*\)\s*=>\s*\{[\s\S]{0,4000}['"]use strict['"]\s*;/.test(html) ||
      /function\s*\(\s*\)\s*\{[\s\S]{0,4000}['"]use strict['"]\s*;/.test(html);
    if (!hasIifeStrict) return fail(`${label}: JS must contain an IIFE that sets 'use strict';`);
  }

  if (cfg.requireDebounceIfUpdateExists) {
    const result = checkDebouncedUpdateContract(html);
    if (result.details.hasUpdate && !result.ok) {
      return fail(`${label}: update() exists but debounced update pattern not found.`);
    }
  }

  // IMPORTANT:
  // We do NOT forbid code tokens NaN/Infinity because legitimate guards exist (Number.isNaN, etc.).
  // We forbid *string literals* that would strongly imply rendering "NaN"/"Infinity" in the UI.
  if (cfg.forbidTokens && Array.isArray(cfg.forbidTokens)) {
    for (const token of cfg.forbidTokens) {
      const re = new RegExp(`['"]${token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}['"]`, "g");
      if (re.test(html)) return fail(`${label}: forbidden string literal "${token}" found in source.`);
    }
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
      return { id: base, match: { path: relPath } };
    });
}

function parseOnlyFilesEnv() {
  const onlyFilesEnv = process.env.QA_ONLY_FILES;
  if (!onlyFilesEnv || !onlyFilesEnv.trim()) return null;

  return onlyFilesEnv
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

function parseDebugArgs(argv) {
  const DEBUG_FLAG = "--debug-debounce";
  const debug = argv.includes(DEBUG_FLAG);
  if (!debug) return { debug: false, files: [] };
  const files = argv.filter((arg) => arg !== DEBUG_FLAG);
  return { debug: true, files };
}

function printDebugUsage() {
  console.log(
    [
      "Usage:",
      "  node scripts/qa-template-manifest.mjs --debug-debounce <file1> [file2 ...]",
      "  QA_ONLY_FILES=\"file1,file2\" node scripts/qa-template-manifest.mjs --debug-debounce"
    ].join("\n")
  );
}

function printDebounceDebugReport(filePath, result) {
  const details = result.details;
  const verdict = result.ok ? "PASS" : "FAIL";
  console.log(`[DEBUG-DEBOUNCE] file: ${filePath}`);
  console.log(`- hasUpdate: ${details.hasUpdate}`);
  console.log(`- scriptsInlineCount: ${details.scriptsInlineCount}`);
  console.log(`- candidateScriptsWithUpdate: ${details.candidateScriptsWithUpdate}`);
  console.log(`- wiring:`);
  console.log(`  - hasInputsCardSelector: ${details.wiring.hasInputsCardSelector}`);
  console.log(`  - hasAddEventListenerInput: ${details.wiring.hasAddEventListenerInput}`);
  console.log(`  - hasAddEventListenerChange: ${details.wiring.hasAddEventListenerChange}`);
  console.log(`  - handlersResolveToUpdate: ${details.wiring.handlersResolveToUpdate}`);
  console.log(`- debounce:`);
  console.log(`  - hasDebounceCall: ${details.debounce.hasDebounceCall}`);
  console.log(`  - hasSetTimeout100: ${details.debounce.hasSetTimeout100}`);
  console.log(`  - hasClearTimeoutPattern: ${details.debounce.hasClearTimeoutPattern}`);
  console.log(`  - effectiveDelayMs: ${details.debounce.effectiveDelayMs === null ? "null" : details.debounce.effectiveDelayMs}`);
  console.log(`- verdict: ${verdict}`);
  console.log(`- failReasons:`);
  if (result.reasons.length) {
    for (const reason of result.reasons) console.log(`  - ${reason}`);
  } else {
    console.log(`  - (none)`);
  }
}

function writeArtifact(artifactPath, artifact) {
  try {
    fs.mkdirSync(path.dirname(artifactPath), { recursive: true });
    fs.writeFileSync(artifactPath, JSON.stringify(artifact, null, 2) + "\n", "utf8");
  } catch (e) {
    console.error(`[QA-MANIFEST] WARN: failed to write artifact at ${artifactPath}`, e);
  }
}

async function main() {
  const argv = process.argv.slice(2);
  const debugArgs = parseDebugArgs(argv);
  if (debugArgs.debug) {
    const filesFromArgs = debugArgs.files;
    const filesFromEnv = parseOnlyFilesEnv();
    const files = filesFromArgs.length ? filesFromArgs : (filesFromEnv || []);
    if (!files.length) {
      printDebugUsage();
      process.exit(2);
    }

    let anyFail = false;
    for (const file of files) {
      const abs = path.resolve(process.cwd(), file);
      if (!fs.existsSync(abs)) {
        anyFail = true;
        const result = {
          ok: false,
          reasons: ["file not found/unreadable"],
          details: {
            hasUpdate: false,
            scriptsInlineCount: 0,
            candidateScriptsWithUpdate: 0,
            wiring: {
              hasInputsCardSelector: false,
              hasAddEventListenerInput: false,
              hasAddEventListenerChange: false,
              handlersResolveToUpdate: false
            },
            debounce: {
              hasDebounceCall: false,
              hasSetTimeout100: false,
              hasClearTimeoutPattern: false,
              effectiveDelayMs: null
            }
          }
        };
        printDebounceDebugReport(file, result);
        continue;
      }
      let html;
      try {
        html = fs.readFileSync(abs, "utf8");
      } catch {
        anyFail = true;
        const result = {
          ok: false,
          reasons: ["file not found/unreadable"],
          details: {
            hasUpdate: false,
            scriptsInlineCount: 0,
            candidateScriptsWithUpdate: 0,
            wiring: {
              hasInputsCardSelector: false,
              hasAddEventListenerInput: false,
              hasAddEventListenerChange: false,
              handlersResolveToUpdate: false
            },
            debounce: {
              hasDebounceCall: false,
              hasSetTimeout100: false,
              hasClearTimeoutPattern: false,
              effectiveDelayMs: null
            }
          }
        };
        printDebounceDebugReport(file, result);
        continue;
      }
      const result = checkDebouncedUpdateContract(html);
      if (!result.ok) anyFail = true;
      printDebounceDebugReport(file, result);
    }
    process.exit(anyFail ? 1 : 0);
  }

  const manifestPath = argv[0];
  if (!manifestPath) die(`Usage: node scripts/qa-template-manifest.mjs qa/template-manifest.json`, 2);

  const absManifest = path.resolve(process.cwd(), manifestPath);
  if (!fs.existsSync(absManifest)) die(`Manifest not found: ${rel(absManifest)}`);

  const manifest = readJson(absManifest);
  validateManifest(manifest);

  const defaults = manifest.defaults || {};

  // Artifact defaults to same folder as manifest (qa/...)
  const artifactPath =
    process.env.QA_ARTIFACT_PATH ||
    path.join(path.dirname(absManifest), "qa-template-manifest.artifact.json");

  const buildStamp =
    process.env.QA_BUILD_STAMP ||
    process.env.GITHUB_SHA ||
    process.env.VERCEL_GIT_COMMIT_SHA ||
    new Date().toISOString();

  const artifact = {
    tool: "qa-template-manifest",
    version: 1,
    buildStamp,
    manifestPath: rel(absManifest),
    effectiveEnv: {
      QA_FAIL_FAST: process.env.QA_FAIL_FAST || "0",
      QA_MAX_FILES: process.env.QA_MAX_FILES || "",
      QA_ONLY_FILES: process.env.QA_ONLY_FILES || "",
      QA_ARTIFACT_PATH: process.env.QA_ARTIFACT_PATH || "",
      QA_BUILD_STAMP: process.env.QA_BUILD_STAMP || ""
    },
    totals: {
      total: 0,
      passed: 0,
      failed: 0,
      skippedMissing: 0
    },
    failures: [],
    skipped: []
  };

  // If batch-scoped, do NOT expand autoDiscover. Just validate the explicit list (+ canon).
  const onlyFiles = parseOnlyFilesEnv();
  let pages = [];

  if (onlyFiles) {
    pages = onlyFiles.map((p) => {
      const base = path.basename(p, ".html");
      return { id: base, match: { path: p } };
    });

    // Always include canon in the same run (optional but useful to ensure canon never regresses)
    const canonRel = "sito_modificato/mortgage-payment.html";
    if (!pages.some((x) => x.match.path === canonRel)) {
      pages.unshift({ id: "mortgage-payment", match: { path: canonRel } });
    }
  } else {
    pages = Array.isArray(manifest.pages) ? manifest.pages.slice() : [];
    if (manifest.autoDiscover) {
      const discovered = await autoDiscoverPages(manifest.autoDiscover);
      const explicitPaths = new Set(pages.map((p) => p?.match?.path).filter(Boolean));
      for (const d of discovered) {
        if (!explicitPaths.has(d.match.path)) pages.push(d);
      }
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
      const msg = `[QA-MANIFEST] WARN: file not found for page "${page.id}": ${p}`;
      console.error(msg);
      artifact.totals.skippedMissing++;
      artifact.skipped.push({ pageId: page.id || "unknown", path: p, reason: "missing-file" });
      continue;
    }

    const prev = fileOwners.get(abs);
    if (prev) die(`[QA-MANIFEST] FAIL: file matched by multiple page entries: ${p} owners=${prev} AND ${page.id}`, 1);
    fileOwners.set(abs, page.id || "unknown");
    expanded.push({ page, abs });
  }

  if (!expanded.length) {
    artifact.totals.total = 0;
    writeArtifact(artifactPath, artifact);
    die(`[QA-MANIFEST] FAIL: No existing files were resolved from manifest.`, 1);
  }

  for (const { page, abs } of expanded) {
    const cfg = mergeDefaults(defaults, page);
    const html = fs.readFileSync(abs, "utf8");
    const $ = cheerio.load(html);
    const label = `[${page.id || "page"}] ${rel(abs)}`;

    let r = ensureOrder($, cfg.globalIdOrder, label);
    if (!r.ok) gotoFail(r);

    r = ensureUniqueIds($, html, cfg.globalIds, label);
    if (!r.ok) gotoFail(r);

    r = ensureClasses($, cfg.globalClasses, label);
    if (!r.ok) gotoFail(r);

    r = checkHeroStructure($, label);
    if (!r.ok) gotoFail(r);

    if (Array.isArray(page.requiredIds) && page.requiredIds.length) {
      r = ensureIdsPresent($, html, page.requiredIds, `${label} (requiredIds)`);
      if (!r.ok) gotoFail(r);
    }

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

    r = checkSafety(html, cfg.safety, label);
    if (!r.ok) gotoFail(r);

    artifact.totals.passed++;
    continue;

    function gotoFail(res) {
      artifact.totals.failed++;
      const msg = res.msg;
      console.error(`[QA-MANIFEST] FAIL: ${msg}`);
      artifact.failures.push({
        pageId: page.id || "unknown",
        path: rel(abs),
        msg
      });
      if (FAIL_FAST) {
        artifact.totals.total = artifact.totals.passed + artifact.totals.failed + artifact.totals.skippedMissing;
        writeArtifact(artifactPath, artifact);
        process.exit(1);
      }
    }
  }

  artifact.totals.total = artifact.totals.passed + artifact.totals.failed + artifact.totals.skippedMissing;

  // Always write artifact, even on fail
  writeArtifact(artifactPath, artifact);

  if (artifact.totals.failed > 0) {
    console.error(
      `[QA-MANIFEST] SUMMARY: total=${artifact.totals.total} passed=${artifact.totals.passed} failed=${artifact.totals.failed} skippedMissing=${artifact.totals.skippedMissing}`
    );
    process.exit(1);
  }

  console.log(
    `[QA-MANIFEST] OK: All checks passed. total=${artifact.totals.total} passed=${artifact.totals.passed} skippedMissing=${artifact.totals.skippedMissing}`
  );
  process.exit(0);
}

main().catch((e) => {
  console.error(`[QA-MANIFEST] ERROR:`, e);
  process.exit(1);
});
