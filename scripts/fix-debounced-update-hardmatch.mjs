// scripts/fix-debounced-update-hardmatch.mjs
import fs from "node:fs";
import path from "node:path";

function parseOnlyFilesEnv() {
  const onlyFilesEnv = process.env.QA_ONLY_FILES;
  if (!onlyFilesEnv || !onlyFilesEnv.trim()) return null;
  return onlyFilesEnv
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

const TARGETS = parseOnlyFilesEnv() || [
  "sito_modificato/aci-concrete-mix-design.html",
  "sito_modificato/added-sugar.html",
  "sito_modificato/adhesive-calculator.html",
  "sito_modificato/adiabatic-equation.html",
  "sito_modificato/adjacency-list.html",
];

function read(fp) { return fs.readFileSync(fp, "utf8"); }
function write(fp, s) { fs.writeFileSync(fp, s, "utf8"); }

function lastScriptBlock(html) {
  const matches = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
  if (!matches.length) return null;
  const m = matches[matches.length - 1];
  return { full: m[0], js: m[1], index: m.index };
}

function ensureDebounceFn(js) {
  // If any debounce() already exists, keep it.
  if (/\bdebounce\s*=\s*\(\s*fn\s*,\s*delay\s*=/.test(js) || /\bfunction\s+debounce\s*\(/.test(js)) return js;

  // Insert right after first 'use strict'; inside last script (canonical style)
  const strictIdx = js.indexOf("'use strict'");
  if (strictIdx === -1) return js;

  const semi = js.indexOf(";", strictIdx);
  if (semi === -1) return js;

  const insertAt = semi + 1;
  const snippet = `

    const debounce = (fn, delay = 100) => {
      let t;
      return (...args) => {
        clearTimeout(t);
        t = setTimeout(() => fn(...args), delay);
      };
    };
`;
  return js.slice(0, insertAt) + snippet + js.slice(insertAt);
}

function ensureDebouncedUpdateAndListeners(js) {
  const wantLine = "const debouncedUpdate = debounce(update, 100);";

  const hasDebouncedUpdate = new RegExp(
    String.raw`\bconst\s+debouncedUpdate\s*=\s*debounce\s*\(\s*update\s*,\s*100\s*\)\s*;`
  ).test(js);

  const hasInputsCardListeners =
    /querySelectorAll\s*\(\s*['"]#inputsCard input, #inputsCard select, #inputsCard textarea['"]\s*\)/.test(js) &&
    /addEventListener\s*\(\s*['"]input['"]\s*,\s*debouncedUpdate\s*\)/.test(js) &&
    /addEventListener\s*\(\s*['"]change['"]\s*,\s*debouncedUpdate\s*\)/.test(js);

  if (hasDebouncedUpdate && hasInputsCardListeners) return js;

  // Remove any previous debouncedUpdate definition to avoid duplicates / mismatched regex
  js = js.replace(
    /\bconst\s+debouncedUpdate\s*=\s*debounce\s*\(\s*update\s*,\s*\d+\s*\)\s*;\s*/g,
    ""
  );

  // Also remove any previous broad listeners that mention debouncedUpdate on inputsCard selectors (optional cleanup)
  js = js.replace(
    /document\.querySelectorAll\s*\(\s*['"]#inputsCard[^'"]*['"]\s*\)[\s\S]*?debouncedUpdate[\s\S]*?\)\s*;\s*/g,
    ""
  );

  const block = `
    ${wantLine}

    document.querySelectorAll('#inputsCard input, #inputsCard select, #inputsCard textarea')
      .forEach((el) => {
        el.addEventListener('input', debouncedUpdate);
        el.addEventListener('change', debouncedUpdate);
      });
`;

  // Insert block just BEFORE the first "update();" call (common canonical anchor).
  const m = js.match(/(\n\s*)update\s*\(\s*\)\s*;\s*\n/);
  if (m && m.index != null) {
    const idx = m.index;
    return js.slice(0, idx) + block + js.slice(idx);
  }

  // Fallback: insert before final "})();"
  const closeIdx = js.lastIndexOf("})();");
  if (closeIdx !== -1) {
    return js.slice(0, closeIdx) + block + "\n" + js.slice(closeIdx);
  }

  return js;
}

function patchFile(rel) {
  const fp = path.resolve(process.cwd(), rel);
  const html = read(fp);
  const script = lastScriptBlock(html);
  if (!script) return { rel, changed: false, note: "no script" };

  let js = script.js;
  if (!/\bfunction\s+update\s*\(|\bupdate\s*=\s*\(/.test(js)) {
    return { rel, changed: false, note: "no update() in last script" };
  }

  const before = js;

  js = ensureDebounceFn(js);
  js = ensureDebouncedUpdateAndListeners(js);

  if (js === before) return { rel, changed: false, note: "already ok or no anchor" };

  const replacedScript = script.full.replace(script.js, js);
  const out = html.slice(0, script.index) + replacedScript + html.slice(script.index + script.full.length);
  write(fp, out);
  return { rel, changed: true, note: "patched" };
}

let changed = 0;
for (const rel of TARGETS) {
  const r = patchFile(rel);
  if (r.changed) changed++;
  console.log(`[fix-debounced-update-hardmatch] ${r.changed ? "OK" : "SKIP"}: ${r.rel} (${r.note})`);
}
console.log(`[fix-debounced-update-hardmatch] DONE: changed=${changed}/${TARGETS.length}`);
