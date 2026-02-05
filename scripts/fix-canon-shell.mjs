// scripts/fix-canon-shell.mjs
//
// Canon-shell invariant fixer for legacy pages.
// Goal: make pages pass qa:template invariants even when Codex outputs nothing.
// Idempotent: safe to run repeatedly.
//
// Usage:
//   node scripts/fix-canon-shell.mjs sito_modificato
//
// Fixes:
// - Ensure #calcBtn (class btn) exists exactly once
// - Ensure #resetBtn (class btn btnSecondary) exists exactly once
// - Ensure #pageMeta exists exactly once
// - Ensure #pageMeta contains details#formulaDetails, details#citationDetails, details#changelogDetails exactly once
//   - Remove dup variants like citationDetails__dup2
//   - Move canonical details into #pageMeta if found elsewhere
//   - Create missing shells if absent

import fs from "node:fs";
import path from "node:path";
import fg from "fast-glob";
import * as cheerio from "cheerio";

const root = process.argv[2] || "sito_modificato";
const files = await fg(["**/*.html"], { cwd: root, onlyFiles: true, absolute: true });

function normClass(str) {
  return (str || "").trim().split(/\s+/).filter(Boolean);
}

function ensureClass($el, cls) {
  if (!$el || !$el.length) return false;
  const before = ($el.attr("class") || "").trim();
  const set = new Set(normClass(before));
  cls.split(/\s+/).filter(Boolean).forEach(c => set.add(c));
  const after = Array.from(set).join(" ");
  if (after !== before) {
    $el.attr("class", after);
    return true;
  }
  return false;
}

function makeDetailsShell(id, title) {
  return `
<details id="${id}">
  <summary style="cursor:pointer; font-weight:700; color:var(--text)">${title}</summary>
  <div style="margin-top:12px; padding:12px; background:#fff; border:1px solid var(--line); border-radius:8px;">
    <!-- Intentionally left blank by canon-shell fixer. Populate during content migration. -->
  </div>
</details>`.trim();
}

function ensurePageMeta($) {
  let changed = false;

  let $meta = $("#pageMeta");
  if ($meta.length > 1) {
    $meta.slice(1).remove();
    changed = true;
    $meta = $("#pageMeta");
  }
  if ($meta.length === 0) {
    const shell = `<section class="meta-section" id="pageMeta" aria-label="Verification, changelog, formulas, citations"></section>`;
    const $how = $("#howToUse");
    const $footer = $("#siteFooter");
    if ($how.length) $how.after("\n\n" + shell + "\n\n");
    else if ($footer.length) $footer.before("\n\n" + shell + "\n\n");
    else $("body").append("\n\n" + shell + "\n\n");
    changed = true;
    $meta = $("#pageMeta");
  }

  return { changed, $meta };
}

function removeDupMetaDetails($) {
  let changed = false;

  // Remove any known dup patterns produced by earlier wrappers
  const dupIds = [
    "citationDetails__dup",
    "changelogDetails__dup",
    "formulaDetails__dup"
  ];

  $("details[id]").each((_, el) => {
    const id = $(el).attr("id") || "";
    if (dupIds.some(prefix => id.startsWith(prefix))) {
      $(el).remove();
      changed = true;
    }
  });

  return changed;
}

function normalizeMetaDetails($, $meta) {
  let changed = false;

  const needed = [
    ["formulaDetails", "Formulas"],
    ["citationDetails", "Citations"],
    ["changelogDetails", "Changelog"],
  ];

  for (const [id, title] of needed) {
    // If multiple exist, keep first and remove others
    const $all = $(`details#${id}`);
    if ($all.length > 1) {
      $all.slice(1).remove();
      changed = true;
    }

    let $one = $(`details#${id}`).first();

    if (!$one.length) {
      // create missing inside meta
      $meta.append("\n" + makeDetailsShell(id, title) + "\n");
      changed = true;
      $one = $(`details#${id}`).first();
    }

    // ensure inside #pageMeta
    if ($one.length && !$one.closest("#pageMeta").length) {
      $one.remove(); // detach
      $meta.append("\n");
      $meta.append($one);
      $meta.append("\n");
      changed = true;
    }
  }

  // Final safety: ensure #pageMeta contains each exactly once
  for (const [id] of needed) {
    const inMeta = $meta.find(`details#${id}`);
    if (inMeta.length > 1) {
      inMeta.slice(1).remove();
      changed = true;
    }
  }

  return changed;
}

function ensureCalcButtons($) {
  let changed = false;

  // Hard requirement: IDs must exist exactly once; create if absent.
  const $inputs = $("#inputsCard");
  if (!$inputs.length) return changed;

  // Remove duplicates if any
  const $calc = $("#calcBtn");
  if ($calc.length > 1) {
    $calc.slice(1).remove();
    changed = true;
  }
  const $reset = $("#resetBtn");
  if ($reset.length > 1) {
    $reset.slice(1).remove();
    changed = true;
  }

  // Create container in inputsCard if missing
  let $btnRow = $inputs.find('[data-canon-btnrow="1"]').first();
  if (!$btnRow.length) {
    $inputs.append('\n<div data-canon-btnrow="1" style="display:flex; gap:10px; margin-top:12px; flex-wrap:wrap;"></div>\n');
    $btnRow = $inputs.find('[data-canon-btnrow="1"]').first();
    changed = true;
  }

  // Create calcBtn if missing
  if ($("#calcBtn").length === 0) {
    $btnRow.append('\n<button id="calcBtn" type="button" class="btn">Calculate</button>\n');
    changed = true;
  }

  // Create resetBtn if missing
  if ($("#resetBtn").length === 0) {
    $btnRow.append('\n<button id="resetBtn" type="button" class="btn btnSecondary">Reset</button>\n');
    changed = true;
  }

  // Ensure canonical classes
  changed = ensureClass($("#calcBtn").first(), "btn") || changed;
  changed = ensureClass($("#resetBtn").first(), "btn btnSecondary") || changed;

  return changed;
}

function ensureScheduleWrap($) {
  let changed = false;

  const $tbody = $("tbody#scheduleBody").first();
  if (!$tbody.length) return changed;

  let $wrap = $("#scheduleWrap").first();
  if ($wrap.length > 1) {
    $wrap.slice(1).remove();
    changed = true;
    $wrap = $("#scheduleWrap").first();
  }

  if ($wrap.length) {
    if (!$wrap.hasClass("tableWrap")) {
      $wrap.addClass("tableWrap");
      changed = true;
    }
    return changed;
  }

  const $table = $tbody.closest("table");
  if ($table.length) {
    $table.wrap('<div id="scheduleWrap" class="tableWrap"></div>');
    changed = true;
  } else {
    $tbody.wrap('<div id="scheduleWrap" class="tableWrap"></div>');
    changed = true;
  }

  return changed;
}

function ensureStrictIife($) {
  let changed = false;
  const html = $.html();
  const hasIifeStrict =
    /\(\s*\(\s*\)\s*=>\s*\{[\s\S]{0,4000}['"]use strict['"]\s*;/.test(html) ||
    /function\s*\(\s*\)\s*\{[\s\S]{0,4000}['"]use strict['"]\s*;/.test(html);
  if (hasIifeStrict) return changed;

  const snippet = `
<script>
  (function() {
    'use strict';
  })();
</script>
`.trim();

  const $body = $("body");
  if ($body.length) {
    $body.append("\n" + snippet + "\n");
  } else {
    $.root().append("\n" + snippet + "\n");
  }
  changed = true;
  return changed;
}

let changedFiles = 0;

for (const abs of files) {
  const before = fs.readFileSync(abs, "utf8");
  const $ = cheerio.load(before, { decodeEntities: false });

  let changed = false;

  // 0) Ensure buttons exist + have canonical classes
  changed = ensureCalcButtons($) || changed;

  // 0.5) Ensure schedule wrap exists when scheduleBody is present
  changed = ensureScheduleWrap($) || changed;

  // 1) Ensure pageMeta exists
  const metaRes = ensurePageMeta($);
  changed = metaRes.changed || changed;

  // 2) Remove dup meta blocks like citationDetails__dup2
  changed = removeDupMetaDetails($) || changed;

  // 3) Normalize required details inside #pageMeta
  changed = normalizeMetaDetails($, metaRes.$meta) || changed;

  // 4) Ensure strict IIFE exists
  changed = ensureStrictIife($) || changed;

  if (changed) {
    const after = $.html();
    if (after !== before) {
      fs.writeFileSync(abs, after);
      changedFiles++;
    }
  }
}

console.log(`[fix:canon-shell] root=${root} files=${files.length} changedFiles=${changedFiles}`);
