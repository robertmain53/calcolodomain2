// scripts/migrate-batch.mjs
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

const OUT_DIR = "qa";
const BATCH_DIR = path.join(OUT_DIR, "batches");
const STATE_PATH = path.join(OUT_DIR, "migration-state.json");
const CANON_PATH = "sito_modificato/mortgage-payment.html";
const PROMPT_PATH = path.join(OUT_DIR, "codex-prompt.txt"); // put your tightened prompt here

function readJson(p) { return JSON.parse(fs.readFileSync(p, "utf8")); }
function writeJson(p, v) { fs.writeFileSync(p, JSON.stringify(v, null, 2)); }

function exec(cmd, args) {
  const r = spawnSync(cmd, args, { stdio: "inherit" });
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
    console.error(`[MIGRATE] Missing canon file ${CANON_PATH}.`);
    process.exit(1);
  }

  const state = readJson(STATE_PATH);
  const batchFile = path.join(BATCH_DIR, `batch-${String(state.nextBatch).padStart(4, "0")}.json`);
  if (!fs.existsSync(batchFile)) {
    console.log(`[MIGRATE] DONE: no more batches.`);
    process.exit(0);
  }

  const batch = readJson(batchFile);
  const prompt = fs.readFileSync(PROMPT_PATH, "utf8");
  const canon = fs.readFileSync(CANON_PATH, "utf8");

  // Produce a single deterministic “job payload” file you feed to Codex.
  // This avoids ad-hoc copy/paste drift.
  const jobPath = path.join(OUT_DIR, `codex-job-batch-${String(state.nextBatch).padStart(4, "0")}.txt`);
  const job = [
    `# CODEX JOB — Batch ${state.nextBatch}`,
    `# Canon path: ${CANON_PATH}`,
    `# Pages in batch: ${batch.length}`,
    ``,
    `# CANON HTML (mortgage-payment.html)`,
    canon,
    ``,
    `# PROMPT`,
    prompt,
    ``,
    `# INPUT PAGES (ORIGINAL_PAGE.html blocks)`,
    ...batch.map((p) => {
      const html = fs.readFileSync(p, "utf8");
      return `\n\n===== ORIGINAL_PAGE_PATH: ${p} =====\n` + html;
    })
  ].join("\n");

  fs.writeFileSync(jobPath, job);
  console.log(`[MIGRATE] Wrote Codex job payload: ${jobPath}`);
  console.log(`[MIGRATE] NEXT STEP: run Codex on that payload and overwrite each ORIGINAL_PAGE_PATH file with its UPDATED_PAGE.html output.`);
  console.log(`[MIGRATE] After writing files, re-run: npm run migrate:batch`);

  // If you set MIGRATE_APPLY=1, we assume files are already updated and we run the gate + advance state.
  if (process.env.MIGRATE_APPLY !== "1") return;

  // Run gate
  exec("npm", ["run", "-s", "qa:template"]);

  // Advance state
  state.completedBatches.push(state.nextBatch);
  state.nextBatch += 1;
  writeJson(STATE_PATH, state);

  console.log(`[MIGRATE] OK: batch applied and gate passed. nextBatch=${state.nextBatch}`);
}

main();
