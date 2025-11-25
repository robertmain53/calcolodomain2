#!/usr/bin/env bash
set -euo pipefail

# Usage: ./generate_unit_converters_batch2.sh [OUTPUT_DIR]
OUTPUT_DIR="${1:-.}"

TEMPLATE_FILE="template_master_INTERNA.html"

if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "Error: $TEMPLATE_FILE not found in current directory." >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "Generating batch 2 unit converters into: $OUTPUT_DIR"

OUTPUT_DIR="$OUTPUT_DIR" TEMPLATE_FILE="$TEMPLATE_FILE" python3 << 'PY'
import os
import pathlib
import textwrap

output_dir = os.environ["OUTPUT_DIR"]
template_file = os.environ["TEMPLATE_FILE"]

template = pathlib.Path(template_file).read_text(encoding="utf-8")

HEAD_SCRIPTS_E_META = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-7MB5V1LZRN"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-7MB5V1LZRN');
</script>

<meta name="google-site-verification" content="_tiTZ9ivAdtXcAS9CMnTNJ549Sg39WVqP_ZFbWgglNA" />

<script src="https://cmp.gatekeeperconsent.com/min.js" data-cfasync="false"></script>
<script src="https://the.gatekeeperconsent.com/cmp.min.js" data-cfasync="false"></script>

<script async src="//www.ezojs.com/ezoic/sa.min.js"></script>
<script>
    window.ezstandalone = window.ezstandalone || {};
    ezstandalone.cmd = ezstandalone.cmd || [];
</script>"""

BODY_SCRIPTS_INIZIO = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9476637732224939"
     crossorigin="anonymous"></script>"""

def breadcrumb_html(last_name: str, last_url: str) -> str:
    return textwrap.dedent(f"""\
    <ol class="flex flex-wrap items-center gap-1">
      <li>
        <a href="https://calcdomain.com" class="text-blue-600 hover:underline">Home</a>
        <span class="text-gray-400 mx-1">/</span>
      </li>
      <li>
        <a href="https://calcdomain.com/categories/math-conversions" class="text-blue-600 hover:underline">Math &amp; Conversions</a>
        <span class="text-gray-400 mx-1">/</span>
      </li>
      <li>
        <a href="https://calcdomain.com/subcategories/math-conversions-measurement-unit-conversions" class="text-blue-600 hover:underline">Measurement Unit Conversions</a>
        <span class="text-gray-400 mx-1">/</span>
      </li>
      <li aria-current="page" class="text-gray-500">
        {last_name}
      </li>
    </ol>""")

def schema_breadcrumb(name: str, url: str) -> str:
    return textwrap.dedent(f"""\
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://calcdomain.com/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Math & Conversions",
          "item": "https://calcdomain.com/categories/math-conversions"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "Measurement Unit Conversions",
          "item": "https://calcdomain.com/subcategories/math-conversions-measurement-unit-conversions"
        }},
        {{
          "@type": "ListItem",
          "position": 4,
          "name": "%s",
          "item": "%s"
        }}
      ]
    }}""" % (name, url))

# Sidebar HTML riusabile
SIDEBAR_GENERIC = textwrap.dedent("""\
<div class="bg-white p-5 rounded-lg shadow-md mb-6 card-hover">
  <h2 class="text-lg font-semibold mb-3">Related unit converters</h2>
  <ul class="space-y-2 text-sm">
    <li><a href="https://calcdomain.com/length-unit-converter" class="text-blue-600 hover:underline">Length Unit Converter</a></li>
    <li><a href="https://calcdomain.com/area-unit-converter" class="text-blue-600 hover:underline">Area Unit Converter</a></li>
    <li><a href="https://calcdomain.com/volume-unit-converter" class="text-blue-600 hover:underline">Volume Unit Converter</a></li>
    <li><a href="https://calcdomain.com/weight-unit-converter" class="text-blue-600 hover:underline">Weight Unit Converter</a></li>
    <li><a href="https://calcdomain.com/temperature-unit-converter" class="text-blue-600 hover:underline">Temperature Unit Converter</a></li>
  </ul>
</div>

<div class="bg-white p-5 rounded-lg shadow-md card-hover">
  <h2 class="text-lg font-semibold mb-3">Category: Measurement Unit Conversions</h2>
  <p class="text-sm text-gray-600 mb-3">
    Explore more engineering-grade unit converters for length, area, volume, weight, temperature, speed and more.
  </p>
  <a href="https://calcdomain.com/subcategories/math-conversions-measurement-unit-conversions"
     class="inline-flex items-center px-3 py-2 text-sm font-medium bg-blue-600 text-white rounded-md hover:bg-blue-700">
    Browse all unit converters
  </a>
</div>
""")

pages = []

# 1) meters <-> feet
pages.append({
    "filename": "meters-to-feet-converter.html",
    "LANGUAGE": "en",
    "TITOLO_PAGINA": "Meters to Feet Converter – m to ft and ft to m",
    "DESCRIZIONE_PAGINA": "Convert between meters and feet (m to ft and ft to m) with this precise length unit converter. Includes formula, examples and quick reference values.",
    "URL_CANONICO": "https://calcdomain.com/meters-to-feet-converter",
    "BREADCRUMB_HTML_QUI": breadcrumb_html("Meters to Feet Converter", "https://calcdomain.com/meters-to-feet-converter"),
    "SIDEBAR_HTML_QUI": SIDEBAR_GENERIC,
    "SCHEMA_JSON_LD_QUI": schema_breadcrumb("Meters to Feet Converter", "https://calcdomain.com/meters-to-feet-converter"),
    "CONTENUTO_PRINCIPALE_QUI": textwrap.dedent("""\
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold mb-2">Meters to Feet Converter</h1>
        <p class="text-gray-600">Convert length between meters (m) and feet (ft) using the exact relationship defined by the international yard.</p>
      </header>

      <section aria-labelledby="conv-mf-heading" class="mb-8">
        <h2 id="conv-mf-heading" class="text-xl font-semibold mb-4">Length converter – m &lt;&rarr; ft</h2>

        <div class="grid gap-4 md:grid-cols-2 mb-4">
          <div>
            <label for="direction-mf" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
            <select id="direction-mf" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="m-to-ft">Meters → Feet</option>
              <option value="ft-to-m">Feet → Meters</option>
            </select>
          </div>
          <div>
            <p class="text-xs text-gray-500 mt-6">
              Exact definition: <code>1 m = 3.280839895013123 ft</code>.
            </p>
          </div>
        </div>

        <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
          <div>
            <label for="input-mf" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
            <div class="flex rounded-md shadow-sm">
              <input id="input-mf" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
              <span id="input-unit-mf" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">m</span>
            </div>
          </div>

          <div>
            <label for="output-mf" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
            <div class="flex rounded-md shadow-sm">
              <input id="output-mf" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
              <span id="output-unit-mf" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">ft</span>
            </div>
          </div>
        </div>

        <button id="swap-mf" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
          Swap direction
        </button>
      </section>

      <section class="prose">
        <h2>Meters and feet: core formulas</h2>
        <div class="formula-box">
          <p class="mb-1"><code>1 m = 3.280839895013123 ft</code></p>
          <p class="mb-1"><code>ft = m × 3.280839895013123</code></p>
          <p class="mb-1"><code>m = ft ÷ 3.280839895013123</code></p>
        </div>

        <h3>Example: 2.5 m to ft</h3>
        <p><code>ft = 2.5 × 3.280839895 ≈ 8.2028 ft</code></p>

        <h3>Typical uses</h3>
        <ul>
          <li>Architectural and construction drawings.</li>
          <li>Engineering calculations mixing SI and US customary units.</li>
          <li>Converting height and clearance specifications.</li>
        </ul>
      </section>

      <script>
        (function () {
          const dirEl = document.getElementById('direction-mf');
          const inputEl = document.getElementById('input-mf');
          const outputEl = document.getElementById('output-mf');
          const inUnitEl = document.getElementById('input-unit-mf');
          const outUnitEl = document.getElementById('output-unit-mf');
          const swapBtn = document.getElementById('swap-mf');

          const FT_PER_M = 3.280839895013123;

          function formatNumber(value) {
            if (!isFinite(value)) return '';
            if (Math.abs(value) >= 1000 || Math.abs(value) < 0.001) {
              return value.toExponential(6);
            }
            return value.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
          }

          function updateUnits() {
            if (dirEl.value === 'm-to-ft') {
              inUnitEl.textContent = 'm';
              outUnitEl.textContent = 'ft';
            } else {
              inUnitEl.textContent = 'ft';
              outUnitEl.textContent = 'm';
            }
          }

          function convert() {
            const v = parseFloat(inputEl.value);
            if (isNaN(v)) {
              outputEl.value = '';
              return;
            }
            let res;
            if (dirEl.value === 'm-to-ft') {
              res = v * FT_PER_M;
            } else {
              res = v / FT_PER_M;
            }
            outputEl.value = formatNumber(res);
          }

          dirEl.addEventListener('change', () => { updateUnits(); convert(); });
          inputEl.addEventListener('input', convert);
          swapBtn.addEventListener('click', () => {
            dirEl.value = dirEl.value === 'm-to-ft' ? 'ft-to-m' : 'm-to-ft';
            updateUnits();
            convert();
          });

          updateUnits();
        })();
      </script>
    """)
})

# 2) meters <-> inches
pages.append({
    "filename": "meters-to-inches-converter.html",
    "LANGUAGE": "en",
    "TITOLO_PAGINA": "Meters to Inches Converter – m to in and in to m",
    "DESCRIZIONE_PAGINA": "Convert between meters and inches (m to in and in to m) with high precision. Includes formulas and practical examples.",
    "URL_CANONICO": "https://calcdomain.com/meters-to-inches-converter",
    "BREADCRUMB_HTML_QUI": breadcrumb_html("Meters to Inches Converter", "https://calcdomain.com/meters-to-inches-converter"),
    "SIDEBAR_HTML_QUI": SIDEBAR_GENERIC,
    "SCHEMA_JSON_LD_QUI": schema_breadcrumb("Meters to Inches Converter", "https://calcdomain.com/meters-to-inches-converter"),
    "CONTENUTO_PRINCIPALE_QUI": textwrap.dedent("""\
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold mb-2">Meters to Inches Converter</h1>
        <p class="text-gray-600">Convert length between meters (m) and inches (in) using the exact international definition of the inch.</p>
      </header>

      <section aria-labelledby="conv-mi-heading" class="mb-8">
        <h2 id="conv-mi-heading" class="text-xl font-semibold mb-4">Length converter – m &lt;&rarr; in</h2>

        <div class="grid gap-4 md:grid-cols-2 mb-4">
          <div>
            <label for="direction-mi" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
            <select id="direction-mi" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="m-to-in">Meters → Inches</option>
              <option value="in-to-m">Inches → Meters</option>
            </select>
          </div>
          <div>
            <p class="text-xs text-gray-500 mt-6">
              Exact definition: <code>1 m = 39.37007874015748 in</code>.
            </p>
          </div>
        </div>

        <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
          <div>
            <label for="input-mi" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
            <div class="flex rounded-md shadow-sm">
              <input id="input-mi" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
              <span id="input-unit-mi" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">m</span>
            </div>
          </div>

          <div>
            <label for="output-mi" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
            <div class="flex rounded-md shadow-sm">
              <input id="output-mi" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
              <span id="output-unit-mi" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">in</span>
            </div>
          </div>
        </div>

        <button id="swap-mi" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
          Swap direction
        </button>
      </section>

      <section class="prose">
        <h2>Formula for meters to inches</h2>
        <div class="formula-box">
          <p class="mb-1"><code>1 in = 0.0254 m</code></p>
          <p class="mb-1"><code>1 m = 39.37007874015748 in</code></p>
          <p class="mb-1"><code>in = m ÷ 0.0254</code></p>
          <p class="mb-1"><code>m = in × 0.0254</code></p>
        </div>

        <h3>Example: 1.2 m to in</h3>
        <p><code>in = 1.2 ÷ 0.0254 ≈ 47.2441 in</code></p>
      </section>

      <script>
        (function () {
          const dirEl = document.getElementById('direction-mi');
          const inputEl = document.getElementById('input-mi');
          const outputEl = document.getElementById('output-mi');
          const inUnitEl = document.getElementById('input-unit-mi');
          const outUnitEl = document.getElementById('output-unit-mi');
          const swapBtn = document.getElementById('swap-mi');

          const M_PER_IN = 0.0254;

          function formatNumber(v) {
            if (!isFinite(v)) return '';
            if (Math.abs(v) >= 1000 || Math.abs(v) < 0.001) {
              return v.toExponential(6);
            }
            return v.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
          }

          function updateUnits() {
            if (dirEl.value === 'm-to-in') {
              inUnitEl.textContent = 'm';
              outUnitEl.textContent = 'in';
            } else {
              inUnitEl.textContent = 'in';
              outUnitEl.textContent = 'm';
            }
          }

          function convert() {
            const val = parseFloat(inputEl.value);
            if (isNaN(val)) {
              outputEl.value = '';
              return;
            }
            let res;
            if (dirEl.value === 'm-to-in') {
              res = val / M_PER_IN;
            } else {
              res = val * M_PER_IN;
            }
            outputEl.value = formatNumber(res);
          }

          dirEl.addEventListener('change', () => { updateUnits(); convert(); });
          inputEl.addEventListener('input', convert);
          swapBtn.addEventListener('click', () => {
            dirEl.value = dirEl.value === 'm-to-in' ? 'in-to-m' : 'm-to-in';
            updateUnits();
            convert();
          });

          updateUnits();
        })();
      </script>
    """)
})

# 3) centimeters <-> inches
pages.append({
    "filename": "cm-to-inches-converter.html",
    "LANGUAGE": "en",
    "TITOLO_PAGINA": "Centimeters to Inches Converter – cm to in and in to cm",
    "DESCRIZIONE_PAGINA": "Convert between centimeters and inches (cm to in and in to cm) with this precise length converter. Ideal for clothing, design and woodworking.",
    "URL_CANONICO": "https://calcdomain.com/cm-to-inches-converter",
    "BREADCRUMB_HTML_QUI": breadcrumb_html("Centimeters to Inches Converter", "https://calcdomain.com/cm-to-inches-converter"),
    "SIDEBAR_HTML_QUI": SIDEBAR_GENERIC,
    "SCHEMA_JSON_LD_QUI": schema_breadcrumb("Centimeters to Inches Converter", "https://calcdomain.com/cm-to-inches-converter"),
    "CONTENUTO_PRINCIPALE_QUI": textwrap.dedent("""\
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold mb-2">Centimeters to Inches Converter</h1>
        <p class="text-gray-600">Convert length between centimeters (cm) and inches (in) instantly, using the exact definition 1 in = 2.54 cm.</p>
      </header>

      <section aria-labelledby="conv-ci-heading" class="mb-8">
        <h2 id="conv-ci-heading" class="text-xl font-semibold mb-4">Length converter – cm &lt;&rarr; in</h2>

        <div class="grid gap-4 md:grid-cols-2 mb-4">
          <div>
            <label for="direction-ci" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
            <select id="direction-ci" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="cm-to-in">Centimeters → Inches</option>
              <option value="in-to-cm">Inches → Centimeters</option>
            </select>
          </div>
          <div>
            <p class="text-xs text-gray-500 mt-6">
              Exact definition: <code>1 in = 2.54 cm</code>.
            </p>
          </div>
        </div>

        <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
          <div>
            <label for="input-ci" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
            <div class="flex rounded-md shadow-sm">
              <input id="input-ci" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
              <span id="input-unit-ci" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">cm</span>
            </div>
          </div>

          <div>
            <label for="output-ci" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
            <div class="flex rounded-md shadow-sm">
              <input id="output-ci" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
              <span id="output-unit-ci" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">in</span>
            </div>
          </div>
        </div>

        <button id="swap-ci" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
          Swap direction
        </button>
      </section>

      <section class="prose">
        <h2>Formula for cm to inches</h2>
        <div class="formula-box">
          <p class="mb-1"><code>in = cm ÷ 2.54</code></p>
          <p class="mb-1"><code>cm = in × 2.54</code></p>
        </div>

        <h3>Example: 30 cm to in</h3>
        <p><code>in = 30 ÷ 2.54 ≈ 11.811 in</code></p>
      </section>

      <script>
        (function () {
          const dirEl = document.getElementById('direction-ci');
          const inputEl = document.getElementById('input-ci');
          const outputEl = document.getElementById('output-ci');
          const inUnitEl = document.getElementById('input-unit-ci');
          const outUnitEl = document.getElementById('output-unit-ci');
          const swapBtn = document.getElementById('swap-ci');

          const CM_PER_IN = 2.54;

          function formatNumber(v) {
            if (!isFinite(v)) return '';
            if (Math.abs(v) >= 1000 || Math.abs(v) < 0.001) {
              return v.toExponential(6);
            }
            return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
          }

          function updateUnits() {
            if (dirEl.value === 'cm-to-in') {
              inUnitEl.textContent = 'cm';
              outUnitEl.textContent = 'in';
            } else {
              inUnitEl.textContent = 'in';
              outUnitEl.textContent = 'cm';
            }
          }

          function convert() {
            const val = parseFloat(inputEl.value);
            if (isNaN(val)) {
              outputEl.value = '';
              return;
            }
            let res;
            if (dirEl.value === 'cm-to-in') {
              res = val / CM_PER_IN;
            } else {
              res = val * CM_PER_IN;
            }
            outputEl.value = formatNumber(res);
          }

          dirEl.addEventListener('change', () => { updateUnits(); convert(); });
          inputEl.addEventListener('input', convert);
          swapBtn.addEventListener('click', () => {
            dirEl.value = dirEl.value === 'cm-to-in' ? 'in-to-cm' : 'cm-to-in';
            updateUnits();
            convert();
          });

          updateUnits();
        })();
      </script>
    """)
})

# 4) miles <-> kilometers
pages.append({
    "filename": "miles-to-kilometers-converter.html",
    "LANGUAGE": "en",
    "TITOLO_PAGINA": "Miles to Kilometers Converter – mi to km and km to mi",
    "DESCRIZIONE_PAGINA": "Convert between miles and kilometers (mi to km and km to mi) using exact constants. Ideal for travel, navigation and mapping.",
    "URL_CANONICO": "https://calcdomain.com/miles-to-kilometers-converter",
    "BREADCRUMB_HTML_QUI": breadcrumb_html("Miles to Kilometers Converter", "https://calcdomain.com/miles-to-kilometers-converter"),
    "SIDEBAR_HTML_QUI": SIDEBAR_GENERIC,
    "SCHEMA_JSON_LD_QUI": schema_breadcrumb("Miles to Kilometers Converter", "https://calcdomain.com/miles-to-kilometers-converter"),
    "CONTENUTO_PRINCIPALE_QUI": textwrap.dedent("""\
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold mb-2">Miles to Kilometers Converter</h1>
        <p class="text-gray-600">Convert distance between miles (mi) and kilometers (km) using the exact definition 1 mile = 1.609344 km.</p>
      </header>

      <section aria-labelledby="conv-mk-heading" class="mb-8">
        <h2 id="conv-mk-heading" class="text-xl font-semibold mb-4">Distance converter – mi &lt;&rarr; km</h2>

        <div class="grid gap-4 md:grid-cols-2 mb-4">
          <div>
            <label for="direction-mk" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
            <select id="direction-mk" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="mi-to-km">Miles → Kilometers</option>
              <option value="km-to-mi">Kilometers → Miles</option>
            </select>
          </div>
          <div>
            <p class="text-xs text-gray-500 mt-6">
              Exact definition: <code>1 mi = 1.609344 km</code>.
            </p>
          </div>
        </div>

        <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
          <div>
            <label for="input-mk" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
            <div class="flex rounded-md shadow-sm">
              <input id="input-mk" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
              <span id="input-unit-mk" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">mi</span>
            </div>
          </div>

          <div>
            <label for="output-mk" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
            <div class="flex rounded-md shadow-sm">
              <input id="output-mk" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
              <span id="output-unit-mk" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">km</span>
            </div>
          </div>
        </div>

        <button id="swap-mk" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
          Swap direction
        </button>
      </section>

      <section class="prose">
        <h2>Formula for miles to kilometers</h2>
        <div class="formula-box">
          <p class="mb-1"><code>1 mi = 1.609344 km</code></p>
          <p class="mb-1"><code>km = mi × 1.609344</code></p>
          <p class="mb-1"><code>mi = km ÷ 1.609344</code></p>
        </div>

        <h3>Example: 100 mi to km</h3>
        <p><code>km = 100 × 1.609344 = 160.9344 km</code></p>
      </section>

      <script>
        (function () {
          const dirEl = document.getElementById('direction-mk');
          const inputEl = document.getElementById('input-mk');
          const outputEl = document.getElementById('output-mk');
          const inUnitEl = document.getElementById('input-unit-mk');
          const outUnitEl = document.getElementById('output-unit-mk');
          const swapBtn = document.getElementById('swap-mk');

          const KM_PER_MI = 1.609344;

          function formatNumber(v) {
            if (!isFinite(v)) return '';
            if (Math.abs(v) >= 1000 || Math.abs(v) < 0.001) {
              return v.toExponential(6);
            }
            return v.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
          }

          function updateUnits() {
            if (dirEl.value === 'mi-to-km') {
              inUnitEl.textContent = 'mi';
              outUnitEl.textContent = 'km';
            } else {
              inUnitEl.textContent = 'km';
              outUnitEl.textContent = 'mi';
            }
          }

          function convert() {
            const val = parseFloat(inputEl.value);
            if (isNaN(val)) {
              outputEl.value = '';
              return;
            }
            let res;
            if (dirEl.value === 'mi-to-km') {
              res = val * KM_PER_MI;
            } else {
              res = val / KM_PER_MI;
            }
            outputEl.value = formatNumber(res);
          }

          dirEl.addEventListener('change', () => { updateUnits(); convert(); });
          inputEl.addEventListener('input', convert);
          swapBtn.addEventListener('click', () => {
            dirEl.value = dirEl.value === 'mi-to-km' ? 'km-to-mi' : 'mi-to-km';
            updateUnits();
            convert();
          });

          updateUnits();
        })();
      </script>
    """)
})

# 5) liters <-> US gallons
pages.append({
    "filename": "liters-to-us-gallons-converter.html",
    "LANGUAGE": "en",
    "TITOLO_PAGINA": "Liters to US Gallons Converter – L to gal (US)",
    "DESCRIZIONE_PAGINA": "Convert between liters and US gallons (L to gal and gal to L) with this volume unit converter. Uses exact US liquid gallon definition.",
    "URL_CANONICO": "https://calcdomain.com/liters-to-us-gallons-converter",
    "BREADCRUMB_HTML_QUI": breadcrumb_html("Liters to US Gallons Converter", "https://calcdomain.com/liters-to-us-gallons-converter"),
    "SIDEBAR_HTML_QUI": SIDEBAR_GENERIC,
    "SCHEMA_JSON_LD_QUI": schema_breadcrumb("Liters to US Gallons Converter", "https://calcdomain.com/liters-to-us-gallons-converter"),
    "CONTENUTO_PRINCIPALE_QUI": textwrap.dedent("""\
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold mb-2">Liters to US Gallons Converter</h1>
        <p class="text-gray-600">Convert volume between liters (L) and US liquid gallons (gal) using exact constants for fluid calculations and fuel estimates.</p>
      </header>

      <section aria-labelledby="conv-lgus-heading" class="mb-8">
        <h2 id="conv-lgus-heading" class="text-xl font-semibold mb-4">Volume converter – L &lt;&rarr; gal (US)</h2>

        <div class="grid gap-4 md:grid-cols-2 mb-4">
          <div>
            <label for="direction-lgus" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
            <select id="direction-lgus" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="l-to-gal">Liters → US gallons</option>
              <option value="gal-to-l">US gallons → Liters</option>
            </select>
          </div>
          <div>
            <p class="text-xs text-gray-500 mt-6">
              Approximate constant: <code>1 L ≈ 0.2641720524 gal (US)</code>.
            </p>
          </div>
        </div>

        <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
          <div>
            <label for="input-lgus" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
            <div class="flex rounded-md shadow-sm">
              <input id="input-lgus" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
              <span id="input-unit-lgus" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">L</span>
            </div>
          </div>

          <div>
            <label for="output-lgus" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
            <div class="flex rounded-md shadow-sm">
              <input id="output-lgus" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
              <span id="output-unit-lgus" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">gal (US)</span>
            </div>
          </div>
        </div>

        <button id="swap-lgus" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
          Swap direction
        </button>
      </section>

      <section class="prose">
        <h2>Formula for liters to US gallons</h2>
        <div class="formula-box">
          <p class="mb-1"><code>gal (US) ≈ L × 0.2641720524</code></p>
          <p class="mb-1"><code>L ≈ gal (US) ÷ 0.2641720524</code></p>
        </div>

        <h3>Example: 50 L to gal (US)</h3>
        <p><code>gal ≈ 50 × 0.2641720524 ≈ 13.209 gal</code></p>
      </section>

      <script>
        (function () {
          const dirEl = document.getElementById('direction-lgus');
          const inputEl = document.getElementById('input-lgus');
          const outputEl = document.getElementById('output-lgus');
          const inUnitEl = document.getElementById('input-unit-lgus');
          const outUnitEl = document.getElementById('output-unit-lgus');
          const swapBtn = document.getElementById('swap-lgus');

          const GAL_PER_L = 0.2641720524;

          function formatNumber(v) {
            if (!isFinite(v)) return '';
            if (Math.abs(v) >= 1000 || Math.abs(v) < 0.001) {
              return v.toExponential(6);
            }
            return v.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
          }

          function updateUnits() {
            if (dirEl.value === 'l-to-gal') {
              inUnitEl.textContent = 'L';
              outUnitEl.textContent = 'gal (US)';
            } else {
              inUnitEl.textContent = 'gal (US)';
              outUnitEl.textContent = 'L';
            }
          }

          function convert() {
            const val = parseFloat(inputEl.value);
            if (isNaN(val)) {
              outputEl.value = '';
              return;
            }
            let res;
            if (dirEl.value === 'l-to-gal') {
              res = val * GAL_PER_L;
            } else {
              res = val / GAL_PER_L;
            }
            outputEl.value = formatNumber(res);
          }

          dirEl.addEventListener('change', () => { updateUnits(); convert(); });
          inputEl.addEventListener('input', convert);
          swapBtn.addEventListener('click', () => {
            dirEl.value = dirEl.value === 'l-to-gal' ? 'gal-to-l' : 'l-to-gal';
            updateUnits();
            convert();
          });

          updateUnits();
        })();
      </script>
    """)
})

# 6) liters <-> UK gallons
pages.append({
    "filename": "liters-to-uk-gallons-converter.html",
    "LANGUAGE": "en",
    "TITOLO_PAGINA": "Liters to UK Gallons Converter – L to gal (UK)",
    "DESCRIZIONE_PAGINA": "Convert between liters and imperial (UK) gallons with this volume converter. Uses the exact UK gallon definition.",
    "URL_CANONICO": "https://calcdomain.com/liters-to-uk-gallons-converter",
    "BREADCRUMB_HTML_QUI": breadcrumb_html("Liters to UK Gallons Converter", "https://calcdomain.com/liters-to-uk-gallons-converter"),
    "SIDEBAR_HTML_QUI": SIDEBAR_GENERIC,
    "SCHEMA_JSON_LD_QUI": schema_breadcrumb("Liters to UK Gallons Converter", "https://calcdomain.com/liters-to-uk-gallons-converter"),
    "CONTENUTO_PRINCIPALE_QUI": textwrap.dedent("""\
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold mb-2">Liters to UK Gallons Converter</h1>
        <p class="text-gray-600">Convert volume between liters (L) and imperial gallons (UK) using exact constants for fuel and storage calculations.</p>
      </header>

      <section aria-labelledby="conv-lguk-heading" class="mb-8">
        <h2 id="conv-lguk-heading" class="text-xl font-semibold mb-4">Volume converter – L &lt;&rarr; gal (UK)</h2>

        <div class="grid gap-4 md:grid-cols-2 mb-4">
          <div>
            <label for="direction-lguk" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
            <select id="direction-lguk" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="l-to-gal-uk">Liters → UK gallons</option>
              <option value="gal-uk-to-l">UK gallons → Liters</option>
            </select>
          </div>
          <div>
            <p class="text-xs text-gray-500 mt-6">
              Approximate constant: <code>1 L ≈ 0.2199692483 gal (UK)</code>.
            </p>
          </div>
        </div>

        <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
          <div>
            <label for="input-lguk" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
            <div class="flex rounded-md shadow-sm">
              <input id="input-lguk" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
              <span id="input-unit-lguk" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">L</span>
            </div>
          </div>

          <div>
            <label for="output-lguk" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
            <div class="flex rounded-md shadow-sm">
              <input id="output-lguk" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
              <span id="output-unit-lguk" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">gal (UK)</span>
            </div>
          </div>
        </div>

        <button id="swap-lguk" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
          Swap direction
        </button>
      </section>

      <section class="prose">
        <h2>Formula for liters to UK gallons</h2>
        <div class="formula-box">
          <p class="mb-1"><code>gal (UK) ≈ L × 0.2199692483</code></p>
          <p class="mb-1"><code>L ≈ gal (UK) ÷ 0.2199692483</code></p>
        </div>
      </section>

      <script>
        (function () {
          const dirEl = document.getElementById('direction-lguk');
          const inputEl = document.getElementById('input-lguk');
          const outputEl = document.getElementById('output-lguk');
          const inUnitEl = document.getElementById('input-unit-lguk');
          const outUnitEl = document.getElementById('output-unit-lguk');
          const swapBtn = document.getElementById('swap-lguk');

          const GALUK_PER_L = 0.2199692483;

          function formatNumber(v) {
            if (!isFinite(v)) return '';
            if (Math.abs(v) >= 1000 || Math.abs(v) < 0.001) {
              return v.toExponential(6);
            }
            return v.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
          }

          function updateUnits() {
            if (dirEl.value === 'l-to-gal-uk') {
              inUnitEl.textContent = 'L';
              outUnitEl.textContent = 'gal (UK)';
            } else {
              inUnitEl.textContent = 'gal (UK)';
              outUnitEl.textContent = 'L';
            }
          }

          function convert() {
            const val = parseFloat(inputEl.value);
            if (isNaN(val)) {
              outputEl.value = '';
              return;
            }
            let res;
            if (dirEl.value === 'l-to-gal-uk') {
              res = val * GALUK_PER_L;
            } else {
              res = val / GALUK_PER_L;
            }
            outputEl.value = formatNumber(res);
          }

          dirEl.addEventListener('change', () => { updateUnits(); convert(); });
          inputEl.addEventListener('input', convert);
          swapBtn.addEventListener('click', () => {
            dirEl.value = dirEl.value === 'l-to-gal-uk' ? 'gal-uk-to-l' : 'l-to-gal-uk';
            updateUnits();
            convert();
          });

          updateUnits();
        })();
      </script>
    """)
})

# 7) kilograms <-> pounds
pages.append({
    "filename": "kilograms-to-pounds-converter.html",
    "LANGUAGE": "en",
    "TITOLO_PAGINA": "Kilograms to Pounds Converter – kg to lb and lb to kg",
    "DESCRIZIONE_PAGINA": "Convert between kilograms and pounds (kg to lb and lb to kg) with exact constants for body weight, logistics and engineering.",
    "URL_CANONICO": "https://calcdomain.com/kilograms-to-pounds-converter",
    "BREADCRUMB_HTML_QUI": breadcrumb_html("Kilograms to Pounds Converter", "https://calcdomain.com/kilograms-to-pounds-converter"),
    "SIDEBAR_HTML_QUI": SIDEBAR_GENERIC,
    "SCHEMA_JSON_LD_QUI": schema_breadcrumb("Kilograms to Pounds Converter", "https://calcdomain.com/kilograms-to-pounds-converter"),
    "CONTENUTO_PRINCIPALE_QUI": textwrap.dedent("""\
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold mb-2">Kilograms to Pounds Converter</h1>
        <p class="text-gray-600">Convert mass between kilograms (kg) and pounds (lb) using the exact definition 1 kg = 2.20462262185 lb.</p>
      </header>

      <section aria-labelledby="conv-kglb-heading" class="mb-8">
        <h2 id="conv-kglb-heading" class="text-xl font-semibold mb-4">Mass converter – kg &lt;&rarr; lb</h2>

        <div class="grid gap-4 md:grid-cols-2 mb-4">
          <div>
            <label for="direction-kglb" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
            <select id="direction-kglb" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="kg-to-lb">Kilograms → Pounds</option>
              <option value="lb-to-kg">Pounds → Kilograms</option>
            </select>
          </div>
          <div>
            <p class="text-xs text-gray-500 mt-6">
              Exact definition: <code>1 kg = 2.20462262185 lb</code>.
            </p>
          </div>
        </div>

        <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
          <div>
            <label for="input-kglb" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
            <div class="flex rounded-md shadow-sm">
              <input id="input-kglb" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
              <span id="input-unit-kglb" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">kg</span>
            </div>
          </div>

          <div>
            <label for="output-kglb" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
            <div class="flex rounded-md shadow-sm">
              <input id="output-kglb" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
              <span id="output-unit-kglb" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">lb</span>
            </div>
          </div>
        </div>

        <button id="swap-kglb" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
          Swap direction
        </button>
      </section>

      <section class="prose">
        <h2>Formula for kilograms to pounds</h2>
        <div class="formula-box">
          <p class="mb-1"><code>lb = kg × 2.20462262185</code></p>
          <p class="mb-1"><code>kg = lb ÷ 2.20462262185</code></p>
        </div>
      </section>

      <script>
        (function () {
          const dirEl = document.getElementById('direction-kglb');
          const inputEl = document.getElementById('input-kglb');
          const outputEl = document.getElementById('output-kglb');
          const inUnitEl = document.getElementById('input-unit-kglb');
          const outUnitEl = document.getElementById('output-unit-kglb');
          const swapBtn = document.getElementById('swap-kglb');

          const LB_PER_KG = 2.20462262185;

          function formatNumber(v) {
            if (!isFinite(v)) return '';
            if (Math.abs(v) >= 1000 || Math.abs(v) < 0.001) {
              return v.toExponential(6);
            }
            return v.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
          }

          function updateUnits() {
            if (dirEl.value === 'kg-to-lb') {
              inUnitEl.textContent = 'kg';
              outUnitEl.textContent = 'lb';
            } else {
              inUnitEl.textContent = 'lb';
              outUnitEl.textContent = 'kg';
            }
          }

          function convert() {
            const val = parseFloat(inputEl.value);
            if (isNaN(val)) {
              outputEl.value = '';
              return;
            }
            let res;
            if (dirEl.value === 'kg-to-lb') {
              res = val * LB_PER_KG;
            } else {
              res = val / LB_PER_KG;
            }
            outputEl.value = formatNumber(res);
          }

          dirEl.addEventListener('change', () => { updateUnits(); convert(); });
          inputEl.addEventListener('input', convert);
          swapBtn.addEventListener('click', () => {
            dirEl.value = dirEl.value === 'kg-to-lb' ? 'lb-to-kg' : 'kg-to-lb';
            updateUnits();
            convert();
          });

          updateUnits();
        })();
      </script>
    """)
})

# 8) grams <-> ounces
pages.append({
    "filename": "grams-to-ounces-converter.html",
    "LANGUAGE": "en",
    "TITOLO_PAGINA": "Grams to Ounces Converter – g to oz and oz to g",
    "DESCRIZIONE_PAGINA": "Convert between grams and ounces (g to oz and oz to g) with this mass converter. Useful for recipes, lab work and packaging.",
    "URL_CANONICO": "https://calcdomain.com/grams-to-ounces-converter",
    "BREADCRUMB_HTML_QUI": breadcrumb_html("Grams to Ounces Converter", "https://calcdomain.com/grams-to-ounces-converter"),
    "SIDEBAR_HTML_QUI": SIDEBAR_GENERIC,
    "SCHEMA_JSON_LD_QUI": schema_breadcrumb("Grams to Ounces Converter", "https://calcdomain.com/grams-to-ounces-converter"),
    "CONTENUTO_PRINCIPALE_QUI": textwrap.dedent("""\
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold mb-2">Grams to Ounces Converter</h1>
        <p class="text-gray-600">Convert mass between grams (g) and ounces (oz) for cooking, laboratory work and product labeling.</p>
      </header>

      <section aria-labelledby="conv-go-heading" class="mb-8">
        <h2 id="conv-go-heading" class="text-xl font-semibold mb-4">Mass converter – g &lt;&rarr; oz</h2>

        <div class="grid gap-4 md:grid-cols-2 mb-4">
          <div>
            <label for="direction-go" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
            <select id="direction-go" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="g-to-oz">Grams → Ounces</option>
              <option value="oz-to-g">Ounces → Grams</option>
            </select>
          </div>
          <div>
            <p class="text-xs text-gray-500 mt-6">
              Approximate constant: <code>1 g ≈ 0.03527396195 oz</code>.
            </p>
          </div>
        </div>

        <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
          <div>
            <label for="input-go" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
            <div class="flex rounded-md shadow-sm">
              <input id="input-go" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
              <span id="input-unit-go" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">g</span>
            </div>
          </div>

          <div>
            <label for="output-go" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
            <div class="flex rounded-md shadow-sm">
              <input id="output-go" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
              <span id="output-unit-go" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">oz</span>
            </div>
          </div>
        </div>

        <button id="swap-go" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
          Swap direction
        </button>
      </section>

      <section class="prose">
        <h2>Formula for grams to ounces</h2>
        <div class="formula-box">
          <p class="mb-1"><code>oz ≈ g × 0.03527396195</code></p>
          <p class="mb-1"><code>g ≈ oz ÷ 0.03527396195</code></p>
        </div>
      </section>

      <script>
        (function () {
          const dirEl = document.getElementById('direction-go');
          const inputEl = document.getElementById('input-go');
          const outputEl = document.getElementById('output-go');
          const inUnitEl = document.getElementById('input-unit-go');
          const outUnitEl = document.getElementById('output-unit-go');
          const swapBtn = document.getElementById('swap-go');

          const OZ_PER_G = 0.03527396195;

          function formatNumber(v) {
            if (!isFinite(v)) return '';
            if (Math.abs(v) >= 1000 || Math.abs(v) < 0.001) {
              return v.toExponential(6);
            }
            return v.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
          }

          function updateUnits() {
            if (dirEl.value === 'g-to-oz') {
              inUnitEl.textContent = 'g';
              outUnitEl.textContent = 'oz';
            } else {
              inUnitEl.textContent = 'oz';
              outUnitEl.textContent = 'g';
            }
          }

          function convert() {
            const val = parseFloat(inputEl.value);
            if (isNaN(val)) {
              outputEl.value = '';
              return;
            }
            let res;
            if (dirEl.value === 'g-to-oz') {
              res = val * OZ_PER_G;
            } else {
              res = val / OZ_PER_G;
            }
            outputEl.value = formatNumber(res);
          }

          dirEl.addEventListener('change', () => { updateUnits(); convert(); });
          inputEl.addEventListener('input', convert);
          swapBtn.addEventListener('click', () => {
            dirEl.value = dirEl.value === 'g-to-oz' ? 'oz-to-g' : 'g-to-oz';
            updateUnits();
            convert();
          });

          updateUnits();
        })();
      </script>
    """)
})

# 9) Celsius <-> Fahrenheit
pages.append({
    "filename": "celsius-to-fahrenheit-converter.html",
    "LANGUAGE": "en",
    "TITOLO_PAGINA": "Celsius to Fahrenheit Converter – °C to °F and °F to °C",
    "DESCRIZIONE_PAGINA": "Convert between Celsius and Fahrenheit (°C to °F and °F to °C) with this temperature converter. Includes the exact formulas and examples.",
    "URL_CANONICO": "https://calcdomain.com/celsius-to-fahrenheit-converter",
    "BREADCRUMB_HTML_QUI": breadcrumb_html("Celsius to Fahrenheit Converter", "https://calcdomain.com/celsius-to-fahrenheit-converter"),
    "SIDEBAR_HTML_QUI": SIDEBAR_GENERIC,
    "SCHEMA_JSON_LD_QUI": schema_breadcrumb("Celsius to Fahrenheit Converter", "https://calcdomain.com/celsius-to-fahrenheit-converter"),
    "CONTENUTO_PRINCIPALE_QUI": textwrap.dedent("""\
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold mb-2">Celsius to Fahrenheit Converter</h1>
        <p class="text-gray-600">Convert temperature between degrees Celsius (°C) and degrees Fahrenheit (°F) using the well-known linear formulas.</p>
      </header>

      <section aria-labelledby="conv-cf-heading" class="mb-8">
        <h2 id="conv-cf-heading" class="text-xl font-semibold mb-4">Temperature converter – °C &lt;&rarr; °F</h2>

        <div class="grid gap-4 md:grid-cols-2 mb-4">
          <div>
            <label for="direction-cf" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
            <select id="direction-cf" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="c-to-f">Celsius → Fahrenheit</option>
              <option value="f-to-c">Fahrenheit → Celsius</option>
            </select>
          </div>
          <div>
            <p class="text-xs text-gray-500 mt-6">
              Core formula: <code>°F = (°C × 9/5) + 32</code>.
            </p>
          </div>
        </div>

        <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
          <div>
            <label for="input-cf" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
            <div class="flex rounded-md shadow-sm">
              <input id="input-cf" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
              <span id="input-unit-cf" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">°C</span>
            </div>
          </div>

          <div>
            <label for="output-cf" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
            <div class="flex rounded-md shadow-sm">
              <input id="output-cf" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
              <span id="output-unit-cf" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">°F</span>
            </div>
          </div>
        </div>

        <button id="swap-cf" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
          Swap direction
        </button>
      </section>

      <section class="prose">
        <h2>Celsius–Fahrenheit conversion formulas</h2>
        <div class="formula-box">
          <p class="mb-1"><code>°F = (°C × 9 / 5) + 32</code></p>
          <p class="mb-1"><code>°C = (°F − 32) × 5 / 9</code></p>
        </div>
      </section>

      <script>
        (function () {
          const dirEl = document.getElementById('direction-cf');
          const inputEl = document.getElementById('input-cf');
          const outputEl = document.getElementById('output-cf');
          const inUnitEl = document.getElementById('input-unit-cf');
          const outUnitEl = document.getElementById('output-unit-cf');
          const swapBtn = document.getElementById('swap-cf');

          function formatNumber(v) {
            if (!isFinite(v)) return '';
            return v.toFixed(2).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
          }

          function updateUnits() {
            if (dirEl.value === 'c-to-f') {
              inUnitEl.textContent = '°C';
              outUnitEl.textContent = '°F';
            } else {
              inUnitEl.textContent = '°F';
              outUnitEl.textContent = '°C';
            }
          }

          function convert() {
            const val = parseFloat(inputEl.value);
            if (isNaN(val)) {
              outputEl.value = '';
              return;
            }
            let res;
            if (dirEl.value === 'c-to-f') {
              res = (val * 9 / 5) + 32;
            } else {
              res = (val - 32) * 5 / 9;
            }
            outputEl.value = formatNumber(res);
          }

          dirEl.addEventListener('change', () => { updateUnits(); convert(); });
          inputEl.addEventListener('input', convert);
          swapBtn.addEventListener('click', () => {
            dirEl.value = dirEl.value === 'c-to-f' ? 'f-to-c' : 'c-to-f';
            updateUnits();
            convert();
          });

          updateUnits();
        })();
      </script>
    """)
})

# 10) km/h <-> mph
pages.append({
    "filename": "kmh-to-mph-converter.html",
    "LANGUAGE": "en",
    "TITOLO_PAGINA": "km/h to mph Converter – Kilometers per Hour to Miles per Hour",
    "DESCRIZIONE_PAGINA": "Convert speed between kilometers per hour (km/h) and miles per hour (mph). Useful for road speed limits, vehicle specs and navigation.",
    "URL_CANONICO": "https://calcdomain.com/kmh-to-mph-converter",
    "BREADCRUMB_HTML_QUI": breadcrumb_html("km/h to mph Converter", "https://calcdomain.com/kmh-to-mph-converter"),
    "SIDEBAR_HTML_QUI": SIDEBAR_GENERIC,
    "SCHEMA_JSON_LD_QUI": schema_breadcrumb("km/h to mph Converter", "https://calcdomain.com/kmh-to-mph-converter"),
    "CONTENUTO_PRINCIPALE_QUI": textwrap.dedent("""\
      <header class="mb-6">
        <h1 class="text-2xl md:text-3xl font-bold mb-2">km/h to mph Converter</h1>
        <p class="text-gray-600">Convert speed between kilometers per hour (km/h) and miles per hour (mph) using exact factors.</p>
      </header>

      <section aria-labelledby="conv-kmph-heading" class="mb-8">
        <h2 id="conv-kmph-heading" class="text-xl font-semibold mb-4">Speed converter – km/h &lt;&rarr; mph</h2>

        <div class="grid gap-4 md:grid-cols-2 mb-4">
          <div>
            <label for="direction-kmph" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
            <select id="direction-kmph" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option value="kmh-to-mph">km/h → mph</option>
              <option value="mph-to-kmh">mph → km/h</option>
            </select>
          </div>
          <div>
            <p class="text-xs text-gray-500 mt-6">
              Approximate constant: <code>1 km/h ≈ 0.6213711922 mph</code>.
            </p>
          </div>
        </div>

        <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
          <div>
            <label for="input-kmph" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
            <div class="flex rounded-md shadow-sm">
              <input id="input-kmph" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
              <span id="input-unit-kmph" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">km/h</span>
            </div>
          </div>

          <div>
            <label for="output-kmph" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
            <div class="flex rounded-md shadow-sm">
              <input id="output-kmph" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
              <span id="output-unit-kmph" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">mph</span>
            </div>
          </div>
        </div>

        <button id="swap-kmph" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
          Swap direction
        </button>
      </section>

      <section class="prose">
        <h2>Formula for km/h to mph</h2>
        <div class="formula-box">
          <p class="mb-1"><code>mph ≈ km/h × 0.6213711922</code></p>
          <p class="mb-1"><code>km/h ≈ mph ÷ 0.6213711922</code></p>
        </div>
      </section>

      <script>
        (function () {
          const dirEl = document.getElementById('direction-kmph');
          const inputEl = document.getElementById('input-kmph');
          const outputEl = document.getElementById('output-kmph');
          const inUnitEl = document.getElementById('input-unit-kmph');
          const outUnitEl = document.getElementById('output-unit-kmph');
          const swapBtn = document.getElementById('swap-kmph');

          const MPH_PER_KMH = 0.6213711922;

          function formatNumber(v) {
            if (!isFinite(v)) return '';
            if (Math.abs(v) >= 1000 || Math.abs(v) < 0.001) {
              return v.toExponential(6);
            }
            return v.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
          }

          function updateUnits() {
            if (dirEl.value === 'kmh-to-mph') {
              inUnitEl.textContent = 'km/h';
              outUnitEl.textContent = 'mph';
            } else {
              inUnitEl.textContent = 'mph';
              outUnitEl.textContent = 'km/h';
            }
          }

          function convert() {
            const val = parseFloat(inputEl.value);
            if (isNaN(val)) {
              outputEl.value = '';
              return;
            }
            let res;
            if (dirEl.value === 'kmh-to-mph') {
              res = val * MPH_PER_KMH;
            } else {
              res = val / MPH_PER_KMH;
            }
            outputEl.value = formatNumber(res);
          }

          dirEl.addEventListener('change', () => { updateUnits(); convert(); });
          inputEl.addEventListener('input', convert);
          swapBtn.addEventListener('click', () => {
            dirEl.value = dirEl.value === 'kmh-to-mph' ? 'mph-to-kmh' : 'kmh-to-mph';
            updateUnits();
            convert();
          });

          updateUnits();
        })();
      </script>
    """)
})

# --- generate files ---
pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

for page in pages:
    html = template
    mapping = {
        "LANGUAGE": page["LANGUAGE"],
        "TITOLO_PAGINA": page["TITOLO_PAGINA"],
        "DESCRIZIONE_PAGINA": page["DESCRIZIONE_PAGINA"],
        "URL_CANONICO": page["URL_CANONICO"],
        "BREADCRUMB_HTML_QUI": page["BREADCRUMB_HTML_QUI"],
        "SIDEBAR_HTML_QUI": page["SIDEBAR_HTML_QUI"],
        "SCHEMA_JSON_LD_QUI": page["SCHEMA_JSON_LD_QUI"],
        "CONTENUTO_PRINCIPALE_QUI": page["CONTENUTO_PRINCIPALE_QUI"],
        "HEAD_SCRIPTS_E_META": HEAD_SCRIPTS_E_META,
        "BODY_SCRIPTS_INIZIO": BODY_SCRIPTS_INIZIO,
    }
    for key, value in mapping.items():
        html = html.replace(f"%%{key}%%", value)
    out_path = pathlib.Path(output_dir) / page["filename"]
    out_path.write_text(html, encoding="utf-8")
    print(f"Created {out_path}")

PY

echo "Done generating batch 2 converters."
