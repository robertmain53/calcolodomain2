// scripts/migrate-batch.mjs
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

const OUT_DIR = "qa";
const BATCH_DIR = path.join(OUT_DIR, "batches");
const STATE_PATH = path.join(OUT_DIR, "migration-state.json");

const PROMPT_PATH = path.join(OUT_DIR, "codex-prompt.txt");
const CANON_PATH = "sito_modificato/mortgage-payment.html";

const APPLY = process.env.BATCH_APPLY !== "0";
const SANDBOX = process.env.CODEX_SANDBOX || "workspace-write";
const FULL_AUTO = process.env.CODEX_FULL_AUTO !== "0";

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

  const state = readJson(STATE_PATH);
  const runId = `batch-${String(state.nextBatch).padStart(4, "0")}`;
  const batchFile = path.join(BATCH_DIR, `${runId}.json`);

  if (!fs.existsSync(batchFile)) {
    console.log(`[MIGRATE] DONE: no more batches. completed=${state.completedBatches.length}`);
    process.exit(0);
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

  ensureDir(path.join(OUT_DIR, "codex_runs"));
  const runDir = path.join(OUT_DIR, "codex_runs", runId);
  ensureDir(runDir);

  const codexPromptBase = fs.readFileSync(PROMPT_PATH, "utf8").trim();

  const jobPrompt = [
    codexPromptBase,
    ``,
    `WORKSPACE CONTEXT`,
    `- Canon file (must be used as exact layout+behavior reference): ${CANON_PATH}`,
    `- You MUST edit files in-place under sito_modificato/.`,
    `- Only refactor the TARGET FILES listed below. Do not touch any other .html files.`,
    ``,
    `TARGET FILES (${batchPaths.length})`,
    ...batchPaths.map((p) => `- ${p}`),
    ``,
    `STOP CONDITION`,
    `- When all target files are updated AND saved, stop immediately.`,
    ``,
    `REPORTING (WRITE FILE)`,
    `- Create or overwrite: ${path.join(runDir, "codex-report.md")}`,
    `- In that report include:`,
    `  - CHANGELOG (per file: bullet list)`,
    `  - TEST REPORT (>=10 vectors per file OR if infeasible, explain precisely why and include at least 10 total vectors across the batch)`,
    `  - Console error check statement`,
    `  - Any deviations, with justification.`,
    ``
  ].join("\n");

  const jobPromptPath = path.join(runDir, "codex-prompt.batch.txt");
  fs.writeFileSync(jobPromptPath, jobPrompt);

  console.log(`[MIGRATE] Prepared Codex run: ${runId}`);
  console.log(`[MIGRATE] Prompt saved: ${jobPromptPath}`);

  if (!APPLY) {
    console.log(`[MIGRATE] APPLY disabled (BATCH_APPLY=0).`);
    console.log(`[MIGRATE] To run: BATCH_APPLY=1 npm run migrate:batch`);
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

  // ---- Always enforce batch-scoped invariants BEFORE QA gate ----
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

  state.completedBatches.push(state.nextBatch);
  state.nextBatch += 1;
  writeJson(STATE_PATH, state);

  console.log(`[MIGRATE] OK: batch applied + gate passed. nextBatch=${state.nextBatch}`);
  console.log(`[MIGRATE] Artifacts: ${runDir}/codex-report.md and ${runDir}/codex-last-message.txt`);
  process.exit(0);
}

main();
