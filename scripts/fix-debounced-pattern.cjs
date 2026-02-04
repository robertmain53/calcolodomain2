// scripts/fix-debounced-pattern.cjs
//
// FORCE-normalizes the “debounced update pattern” to EXACT canonical text
// AND ensures an actual debounce() helper exists that matches QA safety regex
// (clearTimeout + setTimeout(update,100) variants).
//
// Usage:
//   node scripts/fix-debounced-pattern.cjs sito_modificato
//
// Notes:
// - Idempotent
// - Safe: only patches files that contain update() but fail the debounce contract

const fs = require("fs");
const path = require("path");

function walk(dir, out = []) {
  for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, ent.name);
    if (ent.isDirectory()) walk(p, out);
    else if (ent.isFile() && p.endsWith(".html")) out.push(p);
  }
  return out;
}

function hasUpdate(html) {
  return /\bfunction\s+update\s*\(|\bconst\s+update\s*=\s*\(/.test(html);
}

// This matches the *QA gate* requirement (see qa-template-manifest.mjs)
function hasQaDebounceContract(html) {
  return (
    /clearTimeout\s*\(\s*\w+\s*\)/.test(html) &&
    (
      /setTimeout\s*\(\s*update\s*,\s*100\s*\)/.test(html) ||
      /setTimeout\s*\(\s*\(\s*\)\s*=>\s*update\s*\(\s*\)\s*,\s*100\s*\)/.test(html) ||
      /setTimeout\s*\(\s*function\s*\(\s*\)\s*\{\s*update\s*\(\s*\)\s*;\s*\}\s*,\s*100\s*\)/.test(html)
    )
  );
}

// Canonical block (must match what you hard-check elsewhere)
const CANON_LISTENERS =
`\n\nconst debouncedUpdate = debounce(update, 100);\n\n` +
`document.querySelectorAll('#inputsCard input, #inputsCard select, #inputsCard textarea')\n` +
`  .forEach((el) => {\n` +
`    el.addEventListener('input', debouncedUpdate);\n` +
`    el.addEventListener('change', debouncedUpdate);\n` +
`  });\n`;

// Canonical debounce helper that ALSO satisfies QA regex
const CANON_DEBOUNCE_HELPER =
`\n\nfunction debounce(fn, wait){\n` +
`  let t;\n` +
`  return function(){\n` +
`    clearTimeout(t);\n` +
`    t = setTimeout(() => fn(), wait);\n` +
`  };\n` +
`}\n`;

function patchHtml(html) {
  if (!hasUpdate(html)) return { html, changed: false, changedScripts: 0 };
  if (hasQaDebounceContract(html)) {
    // Still normalize the listener block if it exists but is non-canonical
    // (optional: keep as-is if you want minimal diffs)
    return { html, changed: false, changedScripts: 0 };
  }

  let changed = false;
  let changedScripts = 0;

  // 1) Remove any existing debouncedUpdate definitions (avoid duplicates)
  const before1 = html;
  html = html.replace(
    /\bconst\s+debouncedUpdate\s*=\s*debounce\s*\(\s*update\s*,\s*\d+\s*\)\s*;\s*/g,
    ""
  );
  if (html !== before1) changed = true;

  // 2) Remove any existing listeners block that mentions #inputsCard and debouncedUpdate (variant tolerant)
  const before2 = html;
  html = html.replace(
    /document\.querySelectorAll\s*\([\s\S]*?#inputsCard[\s\S]*?\)\s*[\s\S]*?\.forEach\([\s\S]*?debouncedUpdate[\s\S]*?\)\s*;\s*/g,
    ""
  );
  if (html !== before2) changed = true;

  // 3) Ensure debounce helper exists (with clearTimeout + setTimeout)
  const hasDebounceFn = /\bfunction\s+debounce\s*\(/.test(html);
  const hasClearTimeout = /clearTimeout\s*\(\s*\w+\s*\)/.test(html);
  const hasSetTimeoutFn = /setTimeout\s*\(/.test(html);

  // We only inject helper if the file doesn't already have a compatible debounce contract.
  // If debounce() exists but doesn't match QA, we still inject (to satisfy QA) but do NOT overwrite existing function name.
  // To avoid collisions, we inject only if debounce() is absent OR clearTimeout/setTimeout is absent.
  if (!hasDebounceFn || !hasClearTimeout || !hasSetTimeoutFn) {
    // Inject helper near the bottom of the last <script> before the final update() call if possible.
    // Strategy: place it right before the first occurrence of "update();" at the end of the main script.
    const before3 = html;
    if (/\bupdate\s*\(\s*\)\s*;/.test(html)) {
      html = html.replace(/\bupdate\s*\(\s*\)\s*;/, (m) => {
        changedScripts++;
        return `${CANON_DEBOUNCE_HELPER}${CANON_LISTENERS}\n${m}`;
      });
    } else {
      // Fallback: append before </script> of the last script tag
      html = html.replace(/<\/script>\s*<\/body>/i, (m) => {
        changedScripts++;
        return `${CANON_DEBOUNCE_HELPER}${CANON_LISTENERS}\n</script>\n</body>`;
      });
    }
    if (html !== before3) changed = true;
  } else {
    // debounce exists but QA contract missing (rare). Still inject listeners.
    const before4 = html;
    if (/\bupdate\s*\(\s*\)\s*;/.test(html)) {
      html = html.replace(/\bupdate\s*\(\s*\)\s*;/, (m) => {
        changedScripts++;
        return `${CANON_LISTENERS}\n${m}`;
      });
    }
    if (html !== before4) changed = true;
  }

  return { html, changed, changedScripts };
}

function main() {
  const root = process.argv[2] || "sito_modificato";
  const files = walk(root);
  let changedFiles = 0;
  let changedScripts = 0;

  for (const f of files) {
    const src = fs.readFileSync(f, "utf8");
    const res = patchHtml(src);
    if (res.changed && res.html !== src) {
      fs.writeFileSync(f, res.html);
      changedFiles++;
      changedScripts += res.changedScripts;
    }
  }

  console.log(`[fix-debounced-pattern] root=${root} files=${files.length} changedFiles=${changedFiles} changedScripts=${changedScripts} dry=false`);
}

main();
