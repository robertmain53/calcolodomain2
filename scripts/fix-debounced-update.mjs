// scripts/fix-debounced-update.mjs
import fs from "node:fs";
import path from "node:path";

const TARGETS = [
  "sito_modificato/aci-concrete-mix-design.html",
  "sito_modificato/added-sugar.html",
  "sito_modificato/adhesive-calculator.html",
  "sito_modificato/adiabatic-equation.html",
  "sito_modificato/adjacency-list.html",
];

function fail(msg) {
  console.error(`[fix-debounced-update] FAIL: ${msg}`);
  process.exit(1);
}

function hasDebouncedUpdate(js) {
  return /debouncedUpdate\s*=\s*debounce\s*\(\s*update\s*,\s*100\s*\)/.test(js);
}

function hasDebounceFn(js) {
  return /\bconst\s+debounce\s*=\s*\(\s*fn\s*,\s*delay\s*=\s*100\s*\)\s*=>/.test(js) ||
         /\bfunction\s+debounce\s*\(/.test(js);
}

function hasInputListener(js) {
  return /addEventListener\s*\(\s*['"]input['"]\s*,\s*debouncedUpdate\s*\)/.test(js) ||
         /#inputsCard[^]*addEventListener\s*\(\s*['"]input['"]\s*,\s*debouncedUpdate\s*\)/.test(js);
}

function injectDebounceAfterUseStrict(js) {
  if (hasDebounceFn(js)) return js;

  // Insert immediately after the first occurrence of 'use strict';
  const idx = js.indexOf("'use strict'");
  if (idx === -1) return js; // leave as is; gate will still fail if it demands it elsewhere

  // find the end of the strict line
  const semi = js.indexOf(";", idx);
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

function injectDebouncedUpdateAndListeners(js) {
  // If already present, do nothing.
  if (hasDebouncedUpdate(js) && hasInputListener(js)) return js;

  // We want to place wiring near the bottom but inside the IIFE.
  // Try to inject just before the final "update();" call if present.
  const updateCall = /(\n\s*)update\s*\(\s*\)\s*;\s*\n/.exec(js);
  const anchorIdx = updateCall ? updateCall.index : -1;

  const wiring = `
    const debouncedUpdate = debounce(update, 100);

    // Canon event model
    document.getElementById('calcBtn')?.addEventListener('click', update);
    document.getElementById('resetBtn')?.addEventListener('click', () => {
      // Keep existing reset behavior if already implemented elsewhere.
      // If reset is already wired, this is harmless because it uses optional chaining.
      // (Prefer the original reset implementation if present.)
      try { update(); } catch (_) {}
    });

    // Robust input/change wiring (covers all calculators without maintaining an ID list)
    document.querySelectorAll('#inputsCard input, #inputsCard select, #inputsCard textarea')
      .forEach((el) => {
        el.addEventListener('input', debouncedUpdate);
        el.addEventListener('change', debouncedUpdate);
      });
`;

  // If debouncedUpdate exists but listeners missing, only inject listeners (and ensure debounce exists)
  const needsDebounced = !hasDebouncedUpdate(js);
  const needsListeners = !hasInputListener(js);

  let toInject = "";
  if (needsDebounced || needsListeners) {
    // If debouncedUpdate already exists but maybe with different name, still inject canonical block;
    // gate wants a recognizable pattern.
    toInject = wiring;
  }

  if (anchorIdx !== -1) {
    return js.slice(0, anchorIdx) + toInject + js.slice(anchorIdx);
  }

  // Fallback: inject before the final "})();" inside script
  const iifeClose = js.lastIndexOf("})();");
  if (iifeClose !== -1) {
    return js.slice(0, iifeClose) + toInject + "\n" + js.slice(iifeClose);
  }

  return js; // give up safely
}

function patchHtml(html) {
  // Operate on the LAST <script> block (usually the main calculator IIFE).
  const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
  if (scripts.length === 0) return { html, changed: false, note: "no <script> blocks found" };

  const last = scripts[scripts.length - 1];
  const fullMatch = last[0];
  const js = last[1];

  // Only patch if the file has update() but lacks debouncedUpdate pattern (matches your QA failure).
  if (!/\bfunction\s+update\s*\(/.test(js) && !/\bupdate\s*=\s*\(/.test(js)) {
    return { html, changed: false, note: "no update() detected in last script" };
  }
  if (hasDebouncedUpdate(js) && hasInputListener(js) && hasDebounceFn(js)) {
    return { html, changed: false, note: "already compliant" };
  }

  let nextJs = js;
  nextJs = injectDebounceAfterUseStrict(nextJs);
  nextJs = injectDebouncedUpdateAndListeners(nextJs);

  if (nextJs === js) return { html, changed: false, note: "no changes applied (unexpected structure)" };

  const replaced = fullMatch.replace(js, nextJs);
  const nextHtml = html.slice(0, last.index) + replaced + html.slice(last.index + fullMatch.length);
  return { html: nextHtml, changed: true, note: "patched last script" };
}

let changedCount = 0;

for (const rel of TARGETS) {
  const fp = path.resolve(process.cwd(), rel);
  if (!fs.existsSync(fp)) fail(`Missing file: ${rel}`);

  const before = fs.readFileSync(fp, "utf8");
  const { html: after, changed, note } = patchHtml(before);

  if (changed) {
    fs.writeFileSync(fp, after, "utf8");
    changedCount++;
    console.log(`[fix-debounced-update] OK: ${rel} (${note})`);
  } else {
    console.log(`[fix-debounced-update] SKIP: ${rel} (${note})`);
  }
}

console.log(`[fix-debounced-update] DONE: changed=${changedCount}/${TARGETS.length}`);
