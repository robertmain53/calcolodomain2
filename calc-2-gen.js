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
const DELAY_MS = 10 * 60 * 1000; // 10 minutes between rows
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

Components: src/components/CalculatorIsland.astro (The interactive React/Preact island).

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

Pass strict props.

ASTRO SAFETY RULES (MUST FOLLOW ALL):

- NEVER inline object or array literals directly inside JSX/HTML attributes. This is forbidden:
  - ❌ \`<CalculatorIsland inputConfig={{ ... }} />\`
  - ❌ \`<Component items={[{ label: "A", value: 1 }]} />\`

- ALWAYS define any configuration, arrays, or complex data as top-level \`const\` in the Astro frontmatter, and then pass them by reference:
  - ✅ frontmatter: \`const inputConfig = { /* flat object, no functions */ };\`
  - ✅ JSX: \`<CalculatorIsland inputConfig={inputConfig} />\`

- Keep config objects **flat and small**:
  - Use at most ONE level of nesting (e.g., properties whose values are primitives or simple objects).
  - Do NOT embed functions, arrow functions, or deeply nested objects/arrays inside the .astro file.
  - Prefer multiple simple consts instead of one huge deeply-nested object.

- Do NOT output template literals or backticks inside the Astro page (avoid \`\\\`...\` syntax inside the .astro code).
- Do NOT use string interpolation patterns like \`\${...}\` inside the .astro file content.

- Escape literal \`{\`/\`}\` characters inside any inline math, CSS, or code snippets using HTML entities (&#123;, &#125;) or by wrapping them in string literals so the generated Astro file never introduces stray braces outside JSX expressions.

- When you mention math or CSS code (including LaTeX) always treat it as text content rather than executable code fragments. For example:
  - Use \`<pre class="math-block">$$ x = ... $$</pre>\`
  - Do NOT try to put LaTeX inside JSX expressions or template literals.

- Inside the Astro markup, only use JSX expressions where strictly needed:
  - Simple \`{title}\`, \`{description}\`, \`{faqs.map(...)}\` etc.
  - Avoid complex inline logic; if you need logic, define helper data (arrays/objects) as top-level consts and then use simple maps.

- The only interactive component must be \`CalculatorIsland\`. Do NOT add any extra framework components or Astro hydration directives (\`client:*\`).

- Per inserire JSON-LD o altri script nel <head>, NON usare un tag <head> nella pagina.
- Invece, usa sempre lo slot del Layout:

  ✅ Esempio corretto:
  <Layout ...>
    <Fragment slot="head">
      <script type="application/ld+json">
        {JSON.stringify(webAppSchema)}
      </script>
      <script type="application/ld+json">
        {JSON.stringify(faqSchema)}
      </script>
      <script type="application/ld+json">
        {JSON.stringify(breadcrumbSchema)}
      </script>
    </Fragment>

    <main>...</main>
  </Layout>

  ❌ NON usare:
  <Layout ...>
    <head> ... </head>
    ...
  </Layout>

CalculatorIsland props:

- Pass only:
  - Primitive props (strings, numbers, booleans).
  - References to top-level const objects/arrays defined in frontmatter (e.g., \`fields={fieldsConfig}\`).
- Never construct nested object literals inside the JSX.

CalculatorIsland props (MUST copy the sample exactly):

- Usa SEMPRE la stessa firma del sample btu-to-kwh.astro.
- I props ammessi sono solo questi (adatta i valori, NON i nomi):

  <CalculatorIsland
    id={slug}
    title={pageTitle}
    hub={hub}
    cluster={cluster}
    slug={slug}
    mode="unit-conversion"        // o altro mode se indicato dal CSV/brief
    primaryUnitFrom="millimeter"  // o quelli corretti per il tool corrente
    primaryUnitTo="inch"
    inputConfig={inputConfig}     // oggetto definito nel frontmatter
    behavior={behavior}           // oggetto definito nel frontmatter
    formula={formula}             // oggetto definito nel frontmatter
  />

- NON inventare altri nomi di props come "inputFields", "resultFields" o "config" se non sono presenti nel sample.
- "inputConfig", "behavior" e "formula" DEVONO essere const definiti nel frontmatter, e passati per riferimento nei props, mai oggetti inline.


Content Richness (SEO):

Theory: Write a section explaining the formula using LaTeX formatting inside a \`<pre>\` or \`<code>\` block (e.g., \`<pre>$$ x = ... $$</pre>\`).

FAQ: Generate 3 specific FAQs based on "People Also Ask" intent for this topic. 
Use Cases: Add a "Real World Example" section.

Implementation: Structured Data & Config

Schema.org: Inject WebApplication JSON-LD. applicationCategory: Map correctly (e.g., FinanceApplication, HealthApplication). featureList: List key capabilities (e.g., "Amortization Schedule", "PDF Export").

Generator constraints (apply to every response):

- Always import \`Layout\`/\`CalculatorIsland\` relative to \`src/components\`. The island should be the only interactive block on the page.
- Do not include any Astro hydration directives (\`client:*\`) or inline component frameworks—keep every calculator statically rendered except the \`CalculatorIsland\` behavior.
- Keep calculator configuration small, flat, and defined as top-level consts in frontmatter. Do NOT inline object or array literals inside JSX props.
- Escape literal \`{\`/\`}\` characters inside any inline math, CSS, or code snippets using HTML entities (&#123;, &#125;) or by wrapping them in string literals so the generated Astro file never introduces stray braces outside JSX expressions.
- When you mention math or CSS code (including LaTeX) always treat it as plain text content wrapped in HTML; never as executable JS/TS.
- Keep the assistant output focused: provide the \`.astro\` file contents and the required SEO/redirect/config snippets from these instructions without inventing extra unrelated commands or steps.

Routing: Update src/data/pages.ts. Add specific tier: 'A'. defining relatedTools (cross-link to other tools in the same Cluster).

Code Quality & Refinement

Mobile First: Ensure the CalculatorIsland uses a Sticky Footer for results on mobile if the form height > 100vh.
Error Handling: instead of "Error", show contextual help (e.g., "Interest rate cannot be negative").
Clean Up: Remove all legacy JS dependencies. Use native TypeScript.

Output Format
For this calculator (this single row only), output:

1) Thinking Process: A brief summary of your UX choices (Cockpit vs Wizard, etc.).
2) File Content: The full .astro file code in the src/pages/en/[hub]/[cluster]/[slug].astro
3) Config Update: The exact snippet to append to src/data/pages.ts.
4) Redirect Rule: The JSON line for vercel.json.
5) execute "git add ." and "git commit -m 'Migrate [slug] calculator'" commands.
6) execute "git push origin main" command.

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

  const configMatch = output.match(
    /3\) Config Update:[\s\S]*?```[a-zA-Z]*\n([\s\S]*?)```/m
  );
  if (configMatch) {
    const snippet = configMatch[1].trim();
    if (snippet) {
      const pagesPath = path.join(
        process.cwd(),
        "astro-proto",
        "src",
        "data",
        "pages.ts"
      );
      let pagesCode = await fsp.readFile(pagesPath, "utf8");
      if (!pagesCode.includes(snippet)) {
        const insertPos = pagesCode.lastIndexOf("];");
        if (insertPos === -1) {
          console.warn(
            "⚠️ Unable to find closing ]; in pages.ts to append config snippet."
          );
        } else {
          const before = pagesCode.slice(0, insertPos).trimEnd();
          const after = pagesCode.slice(insertPos);
          const updated = `${before}\n${snippet}\n${after}`;
          await fsp.writeFile(pagesPath, updated, "utf8");
          console.log("✏️ Appended config snippet to src/data/pages.ts");
        }
      } else {
        console.log("ℹ️ Config snippet already exists in pages.ts; skipping.");
      }
    }
  }
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
