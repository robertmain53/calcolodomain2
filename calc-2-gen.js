// index.js
// Run with: node index.js 4   -> start from data row #4 (1-based, excluding header)

// Requirements:
//   npm install openai csv-parse
//   export OPENAI_API_KEY="your-key"
import "dotenv/config";
import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import { parse } from "csv-parse/sync";
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// ------------ CONFIG ------------
const CSV_PATH = path.join(process.cwd(), "calc-2.csv");
const OUTPUT_DIR = path.join(process.cwd(), "ai-output");
const MODEL_NAME = "gpt-4.1-mini"; // adjust if you want a different model
const DELAY_MS = 10 * 60 * 1000; // 10 minutes between rows
// --------------------------------

// Original + adapted prompt (per row). This is the "template" part.
const BASE_PROMPT = String.raw`Role You are a Senior Principal Frontend Engineer and UX Architect specializing in high-performance "Tier A" web tools. Your goal is to migrate legacy calculators into a modern Astro architecture, ensuring the result is better than competitors like Omni Calculator or Calculator.net in terms of UX, SEO, and Performance.

Context & Inputs Project Root: astro-proto/

Legacy HTML: src/legacy/calculators/ (Use logic from here, but discard outdated HTML structure).

Briefs: scripts/generate-zip/output/<slug>/*.txt (Contains specific math logic and requirements).

Template to follow for look and style, to keep UX uniform:  /home/uc/Projects/calcdomain2/astro-proto/src/pages/en/engineering-construction/thermotechnics/btu-to-kwh.astro

Research Standards:

IA/SEO: Use Silo URL structure (/hub/cluster/tool).

UX Pattern: Use "Cockpit" layout for complex tools (dense data) and "Wizard" for simple sequential ones.

Mobile: "Inputmode=decimal" is mandatory. Sticky result bars are mandatory for long forms.

Components: src/components/CalculatorIsland.astro (The interactive React/Preact island).

Task
You are given ONE row from calc-2.csv (shown below as JSON). Treat this row as a single calculator to migrate. 
Do NOT talk about multiple rows. Only process THIS calculator.

Process the row using the following Atomic Workflow:

Analysis & Strategy (Mental Sandbox)
Before writing code, analyze the legacy tool and the Brief:

Determine Tier: Is this a simple converter (Tier B) or a complex decision tool (Tier A)? Treat all assigned rows as Tier A.

UX Archetype:

Finance/Engineering: Use "Cockpit Interface". Show inputs and results side-by-side (desktop) or stacked (mobile). Use "Progressive Disclosure" (Basic vs Advanced toggle) for secondary fields.

Health/Lifestyle: Use "Visual Wizard". Big inputs, clear questions, instant feedback.

Trust Factors: Identify where to place "Verified by" badges and Citations (ISO standards, official formulas) based on the domain.

Implementation: The Astro Page
Create src/pages/en/[hub]/[cluster]/[slug].astro. Strict Requirements:

Layout: Use Layout.astro. Ensure the "Right Rail" (Sidebar) is preserved for high-CPM ad slots () on Desktop.

Hero Section: High-contrast H1, 1-sentence value prop ("Calculate X in seconds..."), and specific Trust Signals (e.g., "Updated for 2025 Tax Rules").

The Tool (CalculatorIsland):

Pass strict props.

Inputs: Use floating labels or top-aligned labels for scanning speed.

Units: Use native for unit switching next to inputs. Visuals: If the tool involves geometry or finance (amortization), generate a responsive SVG or Chart component. Do not output a static image. 

Content Richness (SEO):
Theory: Write a section explaining the formula using LaTeX formatting (e.g., $$x =...$$). 
FAQ: Generate 3 specific FAQs based on "People Also Ask" intent for this topic. 
Use Cases: Add a "Real World Example" section.

Implementation: Structured Data & Config
Schema.org: Inject WebApplication JSON-LD. applicationCategory: Map correctly (e.g., FinanceApplication, HealthApplication). featureList: List key capabilities (e.g., "Amortization Schedule", "PDF Export").

Routing: Update src/data/pages.ts. Add specific tier: 'A'. defining relatedTools (cross-link to other tools in the same Cluster).

Code Quality & Refinement
Mobile First: Ensure the CalculatorIsland uses a Sticky Footer for results on mobile if the form height > 100vh.
Error Handling: instead of "Error", show contextual help (e.g., "Interest rate cannot be negative").
Clean Up: Remove all legacy JS dependencies. Use native TypeScript.

Output Format
For this calculator (this single row only), output:

1) Thinking Process: A brief summary of your UX choices (Cockpit vs Wizard, etc.).
2) File Content: The full .astro file code.
3) Config Update: The exact snippet to append to src/data/pages.ts.
4) Redirect Rule: The JSON line for vercel.json.

Now process the row below.`;

// Small helper: sleep/delay
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Read and parse CSV into array of objects
async function loadCsvRecords() {
  const raw = await fsp.readFile(CSV_PATH, "utf8");
  const records = parse(raw, {
    columns: true, // use first row as header
    skip_empty_lines: true,
  });
  return records;
}

// Ensure output directory exists
async function ensureOutputDir() {
  if (!fs.existsSync(OUTPUT_DIR)) {
    await fsp.mkdir(OUTPUT_DIR, { recursive: true });
  }
}

// Build the full prompt for this specific row
function buildPromptForRow(row, rowIndex) {
  const rowJson = JSON.stringify(row, null, 2);

  const rowContext = `
Row metadata:
- Row index (1-based, excluding header): ${rowIndex + 1}

Row data (JSON):
${rowJson}

Important:
- Use the fields from this row (e.g., hub, cluster, slug, legacy paths) to decide file paths and routing.
- Do NOT guess unrelated calculators. Stay strictly within the semantics of this row.
`;

  return `${BASE_PROMPT}\n\n${rowContext}`;
}

// Call OpenAI for one row
async function callModelForRow(row, rowIndex) {
  const prompt = buildPromptForRow(row, rowIndex);

  const response = await client.chat.completions.create({
    model: MODEL_NAME,
    messages: [
      {
        role: "user",
        content: prompt,
      },
    ],
    temperature: 0.2,
  });

  const content = response.choices?.[0]?.message?.content || "";
  return content.trim();
}

// Save the result to a file
async function saveResult(row, rowIndex, content) {
  await ensureOutputDir();

  // Optional: use slug column if it exists, otherwise fallback to row index
  const slugSafe = (
    row.slug ||
    row.Slug ||
    row.slug_en ||
    `row-${rowIndex + 1}`
  )
    .toString()
    .replace(/[^a-zA-Z0-9-_]+/g, "-")
    .toLowerCase();

  const filename = `row-${rowIndex + 1}-${slugSafe}.txt`;
  const filePath = path.join(OUTPUT_DIR, filename);

  const header = `=== calc-2.csv row ${rowIndex + 1} (${slugSafe}) ===\n\n`;
  await fsp.writeFile(filePath, header + content, "utf8");

  console.log(`✅ Saved output for row ${rowIndex + 1} to ${filePath}`);
}

// Main runner: process rows sequentially with 10-minute gaps
async function main() {
  const records = await loadCsvRecords();

  if (records.length === 0) {
    console.error("❌ No records found in calc-2.csv");
    process.exit(1);
  }

  // CLI arg: starting row (1-based, excluding header)
  const arg = process.argv[2];
  if (!arg) {
    console.error(
      "Usage: node index.js <startRow>\nExample: node index.js 4  (starts from data row #4)"
    );
    process.exit(1);
  }

  const startRowNumber = Number(arg);
  if (Number.isNaN(startRowNumber) || startRowNumber < 1) {
    console.error("❌ <startRow> must be a positive integer (1-based).");
    process.exit(1);
  }

  const startIndex = startRowNumber - 1; // records[] is 0-based
  if (startIndex >= records.length) {
    console.error(
      `❌ startRow=${startRowNumber} is beyond the last data row (${records.length}).`
    );
    process.exit(1);
  }

  console.log(
    `Starting from data row #${startRowNumber} (0-based index ${startIndex}), total rows: ${records.length}`
  );
  console.log(
    `A new row will be processed every ${DELAY_MS / 60000} minutes.\n`
  );

  for (let i = startIndex; i < records.length; i++) {
    const row = records[i];

    console.log(`🚀 Processing row ${i + 1}/${records.length}...`);

    try {
      const content = await callModelForRow(row, i);
      await saveResult(row, i, content);
    } catch (err) {
      console.error(`❌ Error processing row ${i + 1}:`, err);
    }

    // Don't wait after the last row
    if (i < records.length - 1) {
      console.log(
        `⏲️ Waiting ${DELAY_MS / 60000} minutes before processing next row...\n`
      );
      await delay(DELAY_MS);
    }
  }

  console.log("🎉 All rows processed (from chosen start to end).");
}

// Run
main().catch((err) => {
  console.error("Fatal error in main():", err);
  process.exit(1);
});
