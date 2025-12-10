// index.js
// Run with: node index.js 4   -> start from data row #4 (1-based, excluding header)

import "dotenv/config";
import fsp from "node:fs/promises";
import path from "node:path";
import { parse } from "csv-parse/sync";
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// ------------ CONFIG ------------
const CSV_PATH = path.join(process.cwd(), "calc-2.csv");
const MODEL_NAME = "gpt-5.1";
const DELAY_MS = 5 * 60 * 1000; // 5 minute between rows
// --------------------------------

// FIXED: I have added backslashes (\) before every backtick (`) inside this string
// so the code doesn't think the string has ended early.

const BASE_PROMPT = `Role You are a Senior Principal Frontend Engineer and UX Architect specializing in high-performance "Tier A" web tools. Your goal is to migrate legacy calculators into a modern Astro architecture, ensuring the result is better than competitors like Omni Calculator or Calculator.net in terms of UX, SEO, and Performance.

Context & Inputs Project Root: astro-proto/
Domain name: calcdomain.com
Legacy HTML: src/legacy/calculators/ (Use logic from here, but discard outdated HTML structure).
Project Requirements: Ottimizzazione Struttura Sito Calcolatori Online_pro.pdf , Ottimizzazione UX_UI per Siti di Calcolatori.pdf
Briefs: scripts/generate-zip/output/<slug>/*.txt (Contains specific math logic and requirements).

Sample calculator (can be used to 'copy' common parts and keep style and layout uniform):  /home/uc/Projects/calcdomain2/astro-proto/src/pages/en/engineering/mechanics/btu-to-kwh.astro

Research Standards:

IA/SEO: Use Silo URL structure (/hub/cluster/tool).

UX Pattern: Use "Cockpit" layout for complex tools (dense data) and "Wizard" for simple sequential ones.

Mobile: "inputmode=\\"decimal\\"" is mandatory. Sticky result bars are mandatory for long forms.


Components: src/components/CalculatorIsland.astro (pre-built interactive calculator island that receives configuration props from each page).


Task
You are given ONE row from calc-2.csv (shown below as JSON). Treat this row as a single calculator to migrate. 
Do NOT talk about multiple rows. Only process THIS calculator.

Process the row using the following Atomic Workflow:

Analysis & Strategy (Mental Sandbox)
Before writing code, analyze the legacy tool, the Brief, the Project Requirements, the Sample Calculator:

Determine Related calculators from same category (cluster)

Determine Related calculators from other category (cross-cluster)

UX Archetype:

Show inputs and results side-by-side (desktop) or stacked (mobile). Use "Progressive Disclosure" (Basic vs Advanced toggle) for secondary fields.

Big inputs, clear questions, instant feedback.

Autocalculate on input change, with a "Calculate" button for heavy computations.

"Verified by" badges and Citations (ISO standards, official formulas) 

Add microinteractions for better engagement (e.g., input focus animations, result highlight on change).

Add tips/tooltips for input fields.

Show keyboard numeric keypad on mobile (inputmode="decimal").

Add a "Reset" button to clear all inputs.

add a "Share" button to copy URL with current inputs as query params.

json-LD: use FAQPage, WebApplication schema and BreadcrumbList.

Create rich SEO content around the calculator topic (theory, FAQs, use cases). You have all competitors content in the Project Requirements PDF and you already start from a good content from the legacy file.

Implementation: The Astro Page (code-ready details)

Create src/pages/en/[hub]/[cluster]/[slug].astro. Strict Requirements:

Imports: always reference components via the existing \`src/components\` directory (e.g., \`import Layout from "../../../../components/Layout.astro";\`, \`import CalculatorIsland from "../../../../components/CalculatorIsland.astro";\`). Never try to go up to \`layouts/\` or other directories that do not exist in this repo.

Layout: Use Layout.astro. Ensure the "Right Rail" (Sidebar) is preserved for high-CPM ad slots on Desktop.

Frontmatter: The page frontmatter is critical for dynamic taxonomy. It MUST include:
- \`hub\`: The hub slug from the CSV row.
- \`cluster\`: The cluster slug from the CSV row.

Hero Section: High-contrast H1, 1-sentence value prop ("Calculate X in seconds..."), and specific Trust Signals (e.g., "Updated for 2025 Tax Rules").


 The Tool (CalculatorIsland):

- CalculatorIsland.astro is a generic interactive island.
- The PAGE is responsible for defining the calculator configuration and formulas in the frontmatter.

In the frontmatter of each .astro page you MUST define:

  const hub = "<hub-from-CSV>";
  const cluster = "<cluster-from-CSV>";
  const slug = "<slug-from-CSV>";
  const pageTitle = "...";
  const pageDescription = "...";

  // Calculator config (example)
  const calculatorConfig = {
    mode: "unit-conversion",
    primaryUnitFrom: "millimeter",
    primaryUnitTo: "inch",
    formula: {
      type: "linear",
      expression: "inches = millimeters / 25.4",
      factor: 1 / 25.4
    },
    // ...other fields needed by CalculatorIsland
  };

Then use CalculatorIsland like this:

  <CalculatorIsland
    slug={slug}
    config={calculatorConfig}
  />

ASTRO SAFETY RULES:
- Define config objects as top-level consts in frontmatter.
- DO NOT inline object literals inside JSX props (no \`<Component config={{ ... }}>\`).
- In math text, DO NOT use backslashes or LaTeX; use only plain ASCII math like \`inches = millimeters / 25.4\`.


ASTRO SAFETY RULES (MUST FOLLOW ALL):

- NEVER inline object or array literals directly inside JSX/HTML attributes.
  - ✅ Use top-level consts in frontmatter: \`const faqs = [ … ];\`
  - ✅ Pass them only in simple expressions like \`{faqs.map(...)}\`.
  - ❌ Do NOT do \`<Component config={{ ... }}>\`.
 
- For JSON-LD and scripts in the head:
  - Use only the Layout slot pattern:

    <Layout ...>
      <Fragment slot="head">
        <script type="application/ld+json">
          {JSON.stringify(webAppSchema)}
        </script>
        ...
      </Fragment>
      <main>...</main>
    </Layout>

  - NEVER output a \`<head>\` tag inside the page content.

- Avoid backticks and template literals inside the Astro file (do not use patterns like the template literal placeholder with a dollar sign followed by curly braces).
- Escape literal \`{\` / \`}\` inside text/math with HTML entities (&#123;, &#125;) if needed.
- Treat LaTeX as plain text inside \`<pre>\`/\`<code>\` blocks, never as JS code.

- NEVER output backslashes (the "\\" character) inside page content sections (<pre>, <code>, <p>, etc.).
- If a formula would normally require LaTeX notation, rewrite it in plain-text ASCII math.
- This rule exists to prevent Astro/esbuild syntax errors.

Content Richness (SEO):

Theory: Write a section explaining the formula using plain-text math ONLY.

ASTRO-SAFE MATH RULES (MANDATORY):
- DO NOT use LaTeX commands such as \\text, \\frac, \\times, \\div, \\cdot, etc.
- DO NOT use backslashes ("\\\\") in math content.
- DO NOT use $$ ... $$ blocks with LaTeX syntax.
- Express formulas in plain ASCII text inside <pre> or <code> blocks.

✅ Valid examples:
<pre>inches = millimeters / 25.4</pre>
<pre>meters = kilometers * 1000</pre>
<pre>power (W) = voltage (V) * current (A)</pre>

❌ Forbidden examples:
<pre>$$ \\text{inches} = \\frac{\\text{millimeters}}{25.4} $$</pre>
<pre>y = \\frac{x}{n}</pre>

FAQ: Generate 3 specific FAQs based on "People Also Ask" intent for this topic. 
Use Cases: Add a "Real World Example" section.

Implementation: Structured Data & Config

Schema.org: Inject WebApplication JSON-LD. applicationCategory: Map correctly (e.g., FinanceApplication, HealthApplication). featureList: List key capabilities (e.g., "Amortization Schedule", "PDF Export").

Generator constraints (apply to every response):

- Always import \`Layout\`/\`CalculatorIsland\` relative to \`src/components\`. The island should be the only interactive block on the page.
- Do not include any Astro hydration directives (\`client:*\`) or inline component frameworks—keep every calculator statically rendered except the \`CalculatorIsland\` behavior.
- Keep frontmatter configuration (faqs, schemas, titles) small and flat. Do NOT inline object or array literals inside JSX props.
- Escape literal \`{\`/\`}\` characters inside any inline math, CSS, or code snippets using HTML entities (&#123;, &#125;) or by wrapping them in string literals so the generated Astro file never introduces stray braces outside JSX expressions.
- When you mention math or CSS code (including LaTeX) always treat it as plain text content wrapped in HTML; never as executable JS/TS.
- Keep the assistant output focused: provide the \`.astro\` file contents and the required SEO/redirect/config snippets from these instructions without inventing extra unrelated commands or steps.

Code Quality & Refinement

Mobile First: Ensure the overall page layout is mobile-first and that the calculator section leaves space for a sticky result area on mobile if the form height > 100vh.
Error Handling: instead of generic "Error" messages in copy, provide contextual help in the page text (e.g., "Interest rate cannot be negative").
Clean Up: Remove all legacy JS dependencies. Use native TypeScript.

Output Format
For this calculator (this single row only), output:

1) Thinking Process: A brief summary of your UX choices (Cockpit vs Wizard, etc.).
2) File Content: The full .astro file code in the src/pages/en/[hub]/[cluster]/[slug].astro
3) Redirect Rule: The JSON line for vercel.json.
4) execute "git add ." and "git commit -m 'Migrate [slug] calculator'" commands.
5) execute "git push origin main" command.

Important: 
- Do NOT fabricate any details. Use ONLY the data from this row and the provided context.
- Stick to the specified output format. No extra commentary.

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

async function writeGeneratedFiles(output) {
  const fileMatch = output.match(
    /2\) File Content: `([^`]+)`\s*```[^\n]*\n([\s\S]*?)```/m
  );
  if (fileMatch) {
    const relativePath = fileMatch[1];
    const fileContent = fileMatch[2].trimEnd();
    const targetPath = path.join(process.cwd(), "astro-proto", relativePath);
    await fsp.mkdir(path.dirname(targetPath), { recursive: true });
    await fsp.writeFile(targetPath, fileContent.trim() + "\n", "utf8");
    console.log(`✏️ Wrote generated file: ${targetPath}`);
  } else {
    console.warn("⚠️ No file content section found in the model output.");
  }

  // The logic to update pages.ts has been removed as it is now obsolete.
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
      await writeGeneratedFiles(content);
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
