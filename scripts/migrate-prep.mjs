// scripts/migrate-prep.mjs
import fs from "node:fs";
import path from "node:path";

const ROOT = "sito_modificato";
const OUT_DIR = "qa";
const BATCH_DIR = path.join(OUT_DIR, "batches");
const CANON = path.join(ROOT, "mortgage-payment.html");

const BATCH_SIZE = Number(process.env.BATCH_SIZE || 10);

function listHtml() {
  const files = fs.readdirSync(ROOT)
    .map((f) => path.join(ROOT, f))
    .filter((p) => path.extname(p) === ".html")
    .filter((p) => {
      try {
        return fs.statSync(p).isFile();
      } catch (err) {
        return false;
      }
    })
    .filter((p) => path.basename(p).toLowerCase() !== "index.html")
    .filter((p) => p !== CANON)
    .sort((a, b) => a.localeCompare(b));
  return files;
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function main() {
  ensureDir(OUT_DIR);
  ensureDir(BATCH_DIR);

  const files = listHtml();
  const worklist = files.map((p) => p.replace(/\\/g, "/"));

  fs.writeFileSync(path.join(OUT_DIR, "worklist.json"), JSON.stringify(worklist, null, 2));

  // batches
  let batchIndex = 0;
  for (let i = 0; i < worklist.length; i += BATCH_SIZE) {
    const batch = worklist.slice(i, i + BATCH_SIZE);
    const name = String(batchIndex).padStart(4, "0");
    fs.writeFileSync(path.join(BATCH_DIR, `batch-${name}.json`), JSON.stringify(batch, null, 2));
    batchIndex++;
  }

  // migration state
  const statePath = path.join(OUT_DIR, "migration-state.json");
  if (!fs.existsSync(statePath)) {
    fs.writeFileSync(statePath, JSON.stringify({
      version: 1,
      batchSize: BATCH_SIZE,
      nextBatch: 0,
      completedBatches: [],
      failedPages: []
    }, null, 2));
  }

  console.log(`[MIGRATE-PREP] OK: pages=${worklist.length} batches=${batchIndex} batchSize=${BATCH_SIZE}`);
}

main();
