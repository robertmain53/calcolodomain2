import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import axios from "axios";
import dotenv from "dotenv";
import slugify from "slugify";
import puppeteer from "puppeteer";

dotenv.config();

const SERPER_API_KEY = process.env.SERPER_API_KEY;
if (!SERPER_API_KEY) {
  console.error("❌ Missing SERPER_API_KEY in .env");
  process.exit(1);
}

// ------------ CONFIG ------------
const RESULTS_PER_KEYWORD = 20; // ✅ 20 risultati per keyword
const OUTPUT_DIR = path.join(process.cwd(), "output");
const KEYWORDS_FILE = path.join(process.cwd(), "keywords.txt");
const FETCH_DELAY_MS = 14000;
const PAGE_TIMEOUT_MS = 40000;
// -------------------------------

// map "engine" → { gl, hl }
const ENGINE_MAP = {
  "google.com": { gl: "us", hl: "en" },
  "google.es": { gl: "es", hl: "es" },
  "google.fr": { gl: "fr", hl: "fr" },
  "google.it": { gl: "it", hl: "it" },
  "google.de": { gl: "de", hl: "de" },
};

const toSlug = (value) =>
  slugify(value, {
    lower: true,
    strict: true,
    trim: true,
  });

// small CLI parser
function parseCli() {
  const args = process.argv.slice(2);
  let engine = "google.com";
  const keywordParts = [];

  for (const arg of args) {
    if (arg.startsWith("--engine=")) {
      engine = arg.replace("--engine=", "").trim();
    } else {
      keywordParts.push(arg);
    }
  }

  const singleCliKeyword = keywordParts.join(" ").trim();
  return { engine, singleCliKeyword };
}

const wait = (ms) => new Promise((res) => setTimeout(res, ms));

async function getSerpResults(keyword, engine) {
  const url = "https://google.serper.dev/search";

  const engineCfg = ENGINE_MAP[engine] || ENGINE_MAP["google.com"];

  const payload = {
    q: keyword,
    num: RESULTS_PER_KEYWORD, // ✅ chiediamo 20 risultati
    gl: engineCfg.gl,
    hl: engineCfg.hl,
  };

  const headers = {
    "X-API-KEY": SERPER_API_KEY,
    "Content-Type": "application/json",
  };

  const { data } = await axios.post(url, payload, { headers });
  const organic = data.organic || [];

  // in ogni caso limitiamo a RESULTS_PER_KEYWORD
  return organic.slice(0, RESULTS_PER_KEYWORD).map((item, idx) => ({
    title: item.title,
    url: item.link,
    position: idx + 1,
  }));
}

async function savePageAsMHTML(page, url, filePath) {
  await page.goto(url, {
    waitUntil: "networkidle2",
    timeout: PAGE_TIMEOUT_MS,
  });

  const cdp = await page.target().createCDPSession();
  const { data: mhtml } = await cdp.send("Page.captureSnapshot", {
    format: "mhtml",
  });

  await fsp.writeFile(filePath, mhtml, "utf8");
}

// ⬇️ helper: ricava base name cartella dall’ultima colonna (senza .zip)
function getFolderBaseName(keyword, customName) {
  if (customName && customName.trim()) {
    const parsed = path.parse(customName.trim());
    // se l’ultima colonna è "qualcosa.zip" diventa "qualcosa"
    return parsed.name || keyword;
  }
  return keyword;
}

async function processKeyword(keyword, page, engine, customFolderName = null) {
  // usa l’ultima colonna come base per la cartella, altrimenti la keyword
  const folderBase = getFolderBaseName(keyword, customFolderName);
  const folderSlug = toSlug(folderBase);

  const keywordDir = path.join(OUTPUT_DIR, folderSlug);

  if (fs.existsSync(keywordDir)) {
    console.log(
      `\n⏭️  Skipping "${keyword}" because folder already exists at ${keywordDir}`
    );
    return;
  }

  await fsp.mkdir(keywordDir, { recursive: true });

  console.log(`\n🔎 Keyword: "${keyword}" (engine: ${engine})`);
  console.log(`   📁 Output folder: ${keywordDir}`);

  let results;
  try {
    results = await getSerpResults(keyword, engine);
  } catch (err) {
    console.error("  ❌ Failed SERP:", err.message);
    return;
  }

  const manifest = {
    keyword,
    engine,
    ts: new Date().toISOString(),
    results: [],
  };

  for (const result of results) {
    const safeTitle = slugify(result.title || "page", {
      lower: true,
      strict: true,
      trim: true,
    });

    const filename = `${String(result.position).padStart(
      2,
      "0"
    )}-${safeTitle}.mhtml`;
    const filePath = path.join(keywordDir, filename);

    console.log(`  → [${result.position}] ${result.url}`);

    try {
      await savePageAsMHTML(page, result.url, filePath);
      manifest.results.push({
        ...result,
        file: filename,
        status: "ok",
      });
    } catch (err) {
      console.warn(`    ⚠️ Failed to capture MHTML: ${err.message}`);
      manifest.results.push({
        ...result,
        file: null,
        status: "error",
        error: err.message,
      });
    }

    await wait(FETCH_DELAY_MS);
  }

  const manifestPath = path.join(keywordDir, "manifest.json");
  await fsp.writeFile(manifestPath, JSON.stringify(manifest, null, 2), "utf8");

  console.log(`  ✅ Done. Files saved in folder: ${keywordDir}`);
}

function parseKeywordLine(line, defaultEngine) {
  const parts = line
    .split("|")
    .map((l) => l.trim())
    .filter(Boolean);

  if (!parts.length) return null;

  if (parts.length === 1) {
    return {
      engine: defaultEngine,
      keyword: parts[0],
      filename: null, // nessuna ultima colonna
    };
  }

  if (parts.length === 2) {
    return {
      engine: parts[0] || defaultEngine,
      keyword: parts[1],
      filename: null, // nessuna ultima colonna personalizzata
    };
  }

  const engine = parts[0] || defaultEngine;
  const keyword = parts[1];
  const filename = parts.slice(2).join(" "); // ultima colonna/e → nome cartella grezzo

  return {
    engine,
    keyword,
    filename,
  };
}

async function readKeywordsFromFile(defaultEngine) {
  try {
    const raw = await fsp.readFile(KEYWORDS_FILE, "utf8");
    const lines = raw
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);

    const parsed = lines
      .map((line) => parseKeywordLine(line, defaultEngine))
      .filter(Boolean);

    // filename qui è semplicemente l’ultima colonna (può contenere ".zip" ecc.)
    return parsed.map((entry) => ({
      engine: entry.engine,
      keyword: entry.keyword,
      folderName: entry.filename || null,
    }));
  } catch (err) {
    return [];
  }
}

async function main() {
  await fsp.mkdir(OUTPUT_DIR, { recursive: true });

  const { engine: cliEngine, singleCliKeyword } = parseCli();

  let keywordEnginePairs = [];

  if (singleCliKeyword) {
    // da CLI non hai ultima colonna → usa solo keyword
    keywordEnginePairs = [
      { engine: cliEngine, keyword: singleCliKeyword, folderName: null },
    ];
  } else {
    keywordEnginePairs = await readKeywordsFromFile(cliEngine);
  }

  if (!keywordEnginePairs.length) {
    console.log("ℹ️ No keywords. Examples:");
    console.log(
      '   node index.js --engine=google.it "calcolatore volume cilindro"'
    );
    console.log("   or in keywords.txt:");
    console.log("   google.fr|calcul volume cylindre|volume-cylindre");
    console.log("   google.es|conversor de torque|conversor-torque");
    process.exit(0);
  }

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  const page = await browser.newPage();

  for (const { engine, keyword, folderName } of keywordEnginePairs) {
    await processKeyword(keyword, page, engine, folderName);
  }

  await browser.close();
  console.log("\n🎉 All done.");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
