import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

const OUT_DIR = "qa";
const BATCH_DIR = path.join(OUT_DIR, "batches");
const STATE_PATH = path.join(OUT_DIR, "migration-state.json");
const PROMPT_PATH = path.join(OUT_DIR, "codex-prompt.txt");
const CANON_PATH = "sito_modificato/mortgage-payment.html";
const VERSION = "1.5.0";
const APPLY = process.env.BATCH_APPLY !== "0";
const SANDBOX = process.env.CODEX_SANDBOX || "workspace-write";
const FULL_AUTO = process.env.CODEX_FULL_AUTO !== "0";
const RUN_ALL_FLAG = "--all";

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}
function writeJson(p, v) {
  fs.writeFileSync(p, JSON.stringify(v, null, 2));
}
function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function shCapture(cmd, args, inputStr) {
  return spawnSync(cmd, args, {
    input: inputStr,
    encoding: "utf8",
    stdio: ["pipe", "inherit", "inherit"],
    maxBuffer: 1024 * 1024 * 50
  });
}

function sh(cmd, args, opts = {}) {
  const r = spawnSync(cmd, args, { stdio: "inherit", ...opts });
  if (r.status !== 0) process.exit(r.status ?? 1);
}

const VERSION_BADGE_REGEX = /(<div[^>]*id=["']versionBadge["'][^>]*>)([\s\S]*?)(<\/div>)/i;
const PAGE_META_REGEX = /(<section[^>]+id=["']pageMeta["'][^>]*>)([\s\S]*?)(<\/section>)/i;
const BODY_CLOSE_REGEX = /(<\/body>)/i;

function buildJobPrompt(codexPromptBase, batchPaths, runId) {
  const canonicalGuidance = [
    "WORKSPACE CONTEXT",
    `- Canon file (must be used as exact layout+behavior reference): ${CANON_PATH}`,
    `- ALWAYS copy the mortgage payment layout hierarchy: siteHeader → mainContent → pageTitle → pageSub → errorBox → calcHero (with exactly two <section class=\"card\"> children) → howToUse → pageMeta → siteFooter.`,
    "- Retain the nav/container rows, hero action buttons, cards, schedule table, download/modal controls, and meta section structure (changelog/citations/formulas + version badge).",
    "- Do NOT reuse the three-phase-power layout or any other previous template; keep the canonical hero, CTA buttons, and meta order in every target file.",
    "- You MUST edit files in-place under sito_modificato/.",
    "- Only refactor the TARGET FILES listed below. Do not touch any other .html files.",
    ""
  ];

  const targetSection = [
    `TARGET FILES (${batchPaths.length})`,
    ...batchPaths.map((p) => `- ${p}`),
    ""
  ];

  const reportingSection = [
    "STOP CONDITION",
    "- When all target files are updated AND saved, stop immediately.",
    "",
    "REPORTING (WRITE FILE)",
    `- Create or overwrite: ${path.join(OUT_DIR, "codex_runs", runId, "codex-report.md")}`,
    "- In that report include:",
    "  - CHANGELOG (per file: bullet list)",
    "  - TEST REPORT (>=10 vectors per file OR if infeasible, explain precisely why and include at least 10 total vectors across the batch)",
    "  - Console error check statement",
    "  - Any deviations, with justification.",
    ""
  ];

  return [
    codexPromptBase,
    "",
    ...canonicalGuidance,
    ...targetSection,
    ...reportingSection
  ].join("\n");
}

function stampVersionBadge(filePath) {
  let content = fs.readFileSync(filePath, "utf8");
  let updated = false;

  if (VERSION_BADGE_REGEX.test(content)) {
    const replaced = content.replace(VERSION_BADGE_REGEX, `$1Version ${VERSION}$3`);
    if (replaced !== content) {
      content = replaced;
      updated = true;
    }
  } else {
    const replacedMeta = content.replace(PAGE_META_REGEX, (match, open, inner, close) => {
      if (inner.includes('id="versionBadge"')) return match;
      return `${open}${inner}\n          <div class="badge" id="versionBadge">Version ${VERSION}</div>${close}`;
    });
    if (replacedMeta !== content) {
      content = replacedMeta;
      updated = true;
    } else {
      const fallback = content.replace(BODY_CLOSE_REGEX, `  <div class="badge" id="versionBadge">Version ${VERSION}</div>\n$1`);
      if (fallback !== content) {
        content = fallback;
        updated = true;
      }
    }
  }

  if (updated) {
    fs.writeFileSync(filePath, content, "utf8");
    console.log(`[MIGRATE] Stamped Version ${VERSION} into ${filePath}`);
  }
}

function stampVersionBadges(batchPaths) {
  for (const filePath of batchPaths) {
    if (!fs.existsSync(filePath)) continue;
    stampVersionBadge(filePath);
  }
}

function processBatchForId(state, runId, batchPaths, codexPromptBase) {
  ensureDir(path.join(OUT_DIR, "codex_runs"));
  const runDir = path.join(OUT_DIR, "codex_runs", runId);
  ensureDir(runDir);

  const jobPrompt = buildJobPrompt(codexPromptBase, batchPaths, runId);
  const jobPromptPath = path.join(runDir, "codex-prompt.batch.txt");
  fs.writeFileSync(jobPromptPath, jobPrompt);

  console.log(`[MIGRATE] Prepared Codex run: ${runId}`);
  console.log(`[MIGRATE] Prompt saved: ${jobPromptPath}`);

  if (!APPLY) {
    console.log(`[MIGRATE] APPLY disabled (BATCH_APPLY=0).`);
    console.log(`[MIGRATE] To run: BATCH_APPLY=1 npm run migrate:batch ${RUN_ALL_FLAG}`);
    process.exit(0);
  }

  const codexArgs = [
    "exec",
    ...(FULL_AUTO ? ["--full-auto"] : []),
    "--sandbox",
    SANDBOX,
    "--cd",
    ".",
    "-",
    "--output-last-message",
    path.join(runDir, "codex-last-message.txt")
  ];

  console.log(`[MIGRATE] Running: npx -y @openai/codex ${codexArgs.join(" ")}`);
  const r = shCapture("npx", ["-y", "@openai/codex", ...codexArgs], jobPrompt);
  if (r.status !== 0) {
    console.error(`[MIGRATE] Codex failed. Exit code: ${r.status}`);
    process.exit(r.status ?? 1);
  }

  const only = batchPaths.join(",");
  console.log(`[MIGRATE] Enforcing canonical shell (batch-scoped)...`);
  sh("npm", ["run", "-s", "fix:canon-shell"], {
    env: { ...process.env, QA_ONLY_FILES: only }
  });

  console.log(`[MIGRATE] Enforcing debounce contract (batch-scoped)...`);
  sh("npm", ["run", "-s", "fix:debounce-contract"], {
    env: { ...process.env, QA_ONLY_FILES: only }
  });

  console.log(`[MIGRATE] Running template invariants gate (batch-scoped)...`);
  sh("npm", ["run", "-s", "qa:template"], {
    env: { ...process.env, QA_ONLY_FILES: only }
  });

  stampVersionBadges(batchPaths);

  state.completedBatches.push(state.nextBatch);
  state.nextBatch += 1;
  writeJson(STATE_PATH, state);

  console.log(`[MIGRATE] OK: batch applied + gate passed. nextBatch=${state.nextBatch}`);
  console.log(`[MIGRATE] Artifacts: ${runDir}/codex-report.md and ${runDir}/codex-last-message.txt`);
}

function main() {
  if (!fs.existsSync(STATE_PATH)) {
    console.error(`[MIGRATE] Missing ${STATE_PATH}. Run: npm run migrate:prep`);
    process.exit(1);
  }
  if (!fs.existsSync(PROMPT_PATH)) {
    console.error(`[MIGRATE] Missing ${PROMPT_PATH}. Put your tightened Codex prompt here.`);
    process.exit(1);
  }
  if (!fs.existsSync(CANON_PATH)) {
    console.error(`[MIGRATE] Missing canon file: ${CANON_PATH}`);
    process.exit(1);
  }

  const codexPromptBase = fs.readFileSync(PROMPT_PATH, "utf8").trim();
  const runAll = process.argv.includes(RUN_ALL_FLAG);

  while (true) {
    const state = readJson(STATE_PATH);
    const runId = `batch-${String(state.nextBatch).padStart(4, "0")}`;
    const batchFile = path.join(BATCH_DIR, `${runId}.json`);

    if (!fs.existsSync(batchFile)) {
      console.log(`[MIGRATE] DONE: no more batches. completed=${state.completedBatches.length}`);
      break;
    }

    const batchPaths = readJson(batchFile);
    if (!Array.isArray(batchPaths) || batchPaths.length === 0) {
      console.error(`[MIGRATE] Empty or invalid batch file: ${batchFile}`);
      process.exit(1);
    }

    const missing = batchPaths.filter((p) => !fs.existsSync(p));
    if (missing.length) {
      console.error(`[MIGRATE] Missing files in batch:\n- ${missing.join("\n- ")}`);
      process.exit(1);
    }

    processBatchForId(state, runId, batchPaths, codexPromptBase);
    if (!runAll) break;
  }
}

main();
