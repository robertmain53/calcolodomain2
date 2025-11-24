#!/usr/bin/env bash
set -euo pipefail

# Usage: ./generate_unit_converters_batch3.sh [OUTPUT_DIR]
OUTPUT_DIR="${1:-.}"
mkdir -p "$OUTPUT_DIR"

OUTDIR="$OUTPUT_DIR" python3 << 'PY'
import os
import pathlib
import html as html_mod

output_dir = os.environ.get("OUTDIR", ".")

HEAD_SCRIPTS = """<!-- Google tag (gtag.js) -->
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

BODY_SCRIPT = """<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9476637732224939"
     crossorigin="anonymous"></script>"""

def build_html(title: str, description: str, canonical: str, body_content: str) -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>""" + html_mod.escape(title) + """</title>
  <meta name="description" content=\"""" + html_mod.escape(description) + """\">
  <link rel="canonical" href=\"""" + canonical + """\">

  <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="shortcut icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <link rel="manifest" href="/site.webmanifest" />

  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    .card-hover {{ transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; }}
    .card-hover:hover {{ transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.12), 0 4px 6px -2px rgba(0,0,0,0.08); }}
    .formula-box {{ background:#f3f4f6; border:1px solid #d1d5db; border-radius:0.5rem; padding:1rem; overflow-x:auto; font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }}
    .prose p {{ margin-bottom:0.75rem; }}
    .prose h2 {{ margin-top:1.5rem; margin-bottom:0.75rem; font-size:1.25rem; font-weight:600; }}
    .prose h3 {{ margin-top:1rem; margin-bottom:0.5rem; font-weight:600; }}
  </style>

  """ + HEAD_SCRIPTS + """

</head>
<body class="bg-gray-50 text-gray-800">
  """ + BODY_SCRIPT + """
  <div class="min-h-screen flex flex-col">
    <header class="bg-white shadow-sm">
      <div class="container mx-auto px-4 py-4 flex items-center justify-between">
        <a href="https://calcdomain.com" class="text-2xl font-bold text-blue-600">CalcDomain</a>
        <span class="text-sm text-gray-500 hidden sm:inline">Free online calculators & unit converters</span>
      </div>
    </header>

    <main class="flex-1 container mx-auto px-4 py-8 max-w-4xl">
      """ + body_content + """
    </main>

    <footer class="bg-gray-900 text-gray-400 text-sm">
      <div class="container mx-auto px-4 py-6 flex flex-col sm:flex-row justify-between gap-2">
        <p>&copy; 2025 CalcDomain. All rights reserved.</p>
        <p><a href="https://calcdomain.com/privacy" class="hover:text-white">Privacy</a> · <a href="https://calcdomain.com/terms" class="hover:text-white">Terms</a></p>
      </div>
    </footer>
  </div>

  <script>
    window.MathJax = {{
      tex: {{ inlineMath: [['\\\\(','\\\\)'], ['$', '$']], displayMath: [['$','$'], ['\\\\[','\\\\]']] }},
      svg: {{ fontCache: 'global' }}
    }};
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
</body>
</html>"""

pages = []

# 1) square meters <-> square feet
pages.append(dict(
    filename="square-meters-to-square-feet-converter.html",
    title="Square Meters to Square Feet Converter – m² to ft² and ft² to m²",
    desc="Convert between square meters and square feet (m² to ft² and ft² to m²) for real estate, architecture and construction.",
    canon="https://calcdomain.com/square-meters-to-square-feet-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Square Meters to Square Feet Converter</h1>
  <p class="text-gray-600">Convert area between square meters (m²) and square feet (ft²) quickly.</p>
</header>

<section class="mb-8" aria-labelledby="m2ft2-heading">
  <h2 id="m2ft2-heading" class="text-xl font-semibold mb-4">Area converter – m² ↔ ft²</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-m2ft2" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-m2ft2" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="m2-to-ft2">m² → ft²</option>
        <option value="ft2-to-m2">ft² → m²</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Exact factor: <code>1 m² = 10.7639104167 ft²</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-m2ft2" class="block text-sm font-medium text-gray-700 mb-1">Input area</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-m2ft2" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 50">
        <span id="input-unit-m2ft2" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">m²</span>
      </div>
    </div>
    <div>
      <label for="output-m2ft2" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-m2ft2" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-m2ft2" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">ft²</span>
      </div>
    </div>
  </div>

  <button id="swap-m2ft2" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>ft² = m² × 10.7639104167</code></p>
    <p><code>m² = ft² ÷ 10.7639104167</code></p>
  </div>
</section>

<script>
(function () {
  const FACTOR = 10.7639104167;
  const dirEl = document.getElementById('direction-m2ft2');
  const inEl = document.getElementById('input-m2ft2');
  const outEl = document.getElementById('output-m2ft2');
  const inUnit = document.getElementById('input-unit-m2ft2');
  const outUnit = document.getElementById('output-unit-m2ft2');
  const swapBtn = document.getElementById('swap-m2ft2');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-3) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'm2-to-ft2') {
      inUnit.textContent = 'm²';
      outUnit.textContent = 'ft²';
    } else {
      inUnit.textContent = 'ft²';
      outUnit.textContent = 'm²';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'm2-to-ft2') res = val * FACTOR;
    else res = val / FACTOR;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'm2-to-ft2' ? 'ft2-to-m2' : 'm2-to-ft2';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 2) square meters <-> square yards
pages.append(dict(
    filename="square-meters-to-square-yards-converter.html",
    title="Square Meters to Square Yards Converter – m² to yd² and yd² to m²",
    desc="Convert between square meters and square yards (m² to yd² and yd² to m²) for landscaping, sports fields and textiles.",
    canon="https://calcdomain.com/square-meters-to-square-yards-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Square Meters to Square Yards Converter</h1>
  <p class="text-gray-600">Convert area between square meters (m²) and square yards (yd²).</p>
</header>

<section class="mb-8" aria-labelledby="m2yd2-heading">
  <h2 id="m2yd2-heading" class="text-xl font-semibold mb-4">Area converter – m² ↔ yd²</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-m2yd2" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-m2yd2" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="m2-to-yd2">m² → yd²</option>
        <option value="yd2-to-m2">yd² → m²</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Approximate factor: <code>1 m² ≈ 1.1959900463 yd²</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-m2yd2" class="block text-sm font-medium text-gray-700 mb-1">Input area</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-m2yd2" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 100">
        <span id="input-unit-m2yd2" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">m²</span>
      </div>
    </div>
    <div>
      <label for="output-m2yd2" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-m2yd2" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-m2yd2" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">yd²</span>
      </div>
    </div>
  </div>

  <button id="swap-m2yd2" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>yd² ≈ m² × 1.1959900463</code></p>
    <p><code>m² ≈ yd² ÷ 1.1959900463</code></p>
  </div>
</section>

<script>
(function () {
  const FACTOR = 1.1959900463;
  const dirEl = document.getElementById('direction-m2yd2');
  const inEl = document.getElementById('input-m2yd2');
  const outEl = document.getElementById('output-m2yd2');
  const inUnit = document.getElementById('input-unit-m2yd2');
  const outUnit = document.getElementById('output-unit-m2yd2');
  const swapBtn = document.getElementById('swap-m2yd2');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-3) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'm2-to-yd2') {
      inUnit.textContent = 'm²';
      outUnit.textContent = 'yd²';
    } else {
      inUnit.textContent = 'yd²';
      outUnit.textContent = 'm²';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'm2-to-yd2') res = val * FACTOR;
    else res = val / FACTOR;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'm2-to-yd2' ? 'yd2-to-m2' : 'm2-to-yd2';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 3) cubic meters <-> cubic feet
pages.append(dict(
    filename="cubic-meters-to-cubic-feet-converter.html",
    title="Cubic Meters to Cubic Feet Converter – m³ to ft³ and ft³ to m³",
    desc="Convert between cubic meters and cubic feet (m³ to ft³ and ft³ to m³) for HVAC, storage and shipping.",
    canon="https://calcdomain.com/cubic-meters-to-cubic-feet-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Cubic Meters to Cubic Feet Converter</h1>
  <p class="text-gray-600">Convert volume between cubic meters (m³) and cubic feet (ft³).</p>
</header>

<section class="mb-8" aria-labelledby="m3ft3-heading">
  <h2 id="m3ft3-heading" class="text-xl font-semibold mb-4">Volume converter – m³ ↔ ft³</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-m3ft3" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-m3ft3" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="m3-to-ft3">m³ → ft³</option>
        <option value="ft3-to-m3">ft³ → m³</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Approximate factor: <code>1 m³ ≈ 35.3146667215 ft³</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-m3ft3" class="block text-sm font-medium text-gray-700 mb-1">Input volume</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-m3ft3" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 2">
        <span id="input-unit-m3ft3" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">m³</span>
      </div>
    </div>
    <div>
      <label for="output-m3ft3" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-m3ft3" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-m3ft3" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">ft³</span>
      </div>
    </div>
  </div>

  <button id="swap-m3ft3" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>ft³ ≈ m³ × 35.3146667215</code></p>
    <p><code>m³ ≈ ft³ ÷ 35.3146667215</code></p>
  </div>
</section>

<script>
(function () {
  const FACTOR = 35.3146667215;
  const dirEl = document.getElementById('direction-m3ft3');
  const inEl = document.getElementById('input-m3ft3');
  const outEl = document.getElementById('output-m3ft3');
  const inUnit = document.getElementById('input-unit-m3ft3');
  const outUnit = document.getElementById('output-unit-m3ft3');
  const swapBtn = document.getElementById('swap-m3ft3');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-3) return v.toExponential(6);
    return v.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'm3-to-ft3') {
      inUnit.textContent = 'm³';
      outUnit.textContent = 'ft³';
    } else {
      inUnit.textContent = 'ft³';
      outUnit.textContent = 'm³';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'm3-to-ft3') res = val * FACTOR;
    else res = val / FACTOR;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'm3-to-ft3' ? 'ft3-to-m3' : 'm3-to-ft3';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 4) mL <-> fl oz (US)
pages.append(dict(
    filename="milliliters-to-fluid-ounces-converter.html",
    title="Milliliters to Fluid Ounces Converter – mL to fl oz and fl oz to mL",
    desc="Convert between milliliters and US fluid ounces (mL to fl oz and fl oz to mL) for recipes and beverages.",
    canon="https://calcdomain.com/milliliters-to-fluid-ounces-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Milliliters to Fluid Ounces Converter</h1>
  <p class="text-gray-600">Convert volume between milliliters (mL) and US fluid ounces (fl oz).</p>
</header>

<section class="mb-8" aria-labelledby="mlfloz-heading">
  <h2 id="mlfloz-heading" class="text-xl font-semibold mb-4">Volume converter – mL ↔ fl oz (US)</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-mlfloz" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-mlfloz" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="ml-to-floz">mL → fl oz</option>
        <option value="floz-to-ml">fl oz → mL</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Approximate factor: <code>1 mL ≈ 0.0338140227 fl oz</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-mlfloz" class="block text-sm font-medium text-gray-700 mb-1">Input volume</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-mlfloz" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 250">
        <span id="input-unit-mlfloz" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">mL</span>
      </div>
    </div>
    <div>
      <label for="output-mlfloz" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-mlfloz" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-mlfloz" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">fl oz</span>
      </div>
    </div>
  </div>

  <button id="swap-mlfloz" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>fl oz ≈ mL × 0.0338140227</code></p>
    <p><code>mL ≈ fl oz ÷ 0.0338140227</code></p>
  </div>
</section>

<script>
(function () {
  const FACTOR = 0.0338140227;
  const dirEl = document.getElementById('direction-mlfloz');
  const inEl = document.getElementById('input-mlfloz');
  const outEl = document.getElementById('output-mlfloz');
  const inUnit = document.getElementById('input-unit-mlfloz');
  const outUnit = document.getElementById('output-unit-mlfloz');
  const swapBtn = document.getElementById('swap-mlfloz');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'ml-to-floz') {
      inUnit.textContent = 'mL';
      outUnit.textContent = 'fl oz';
    } else {
      inUnit.textContent = 'fl oz';
      outUnit.textContent = 'mL';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'ml-to-floz') res = val * FACTOR;
    else res = val / FACTOR;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'ml-to-floz' ? 'floz-to-ml' : 'ml-to-floz';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 5) kPa <-> PSI
pages.append(dict(
    filename="kpa-to-psi-converter.html",
    title="kPa to PSI Converter – kilopascals to pounds per square inch",
    desc="Convert between kilopascals and pounds per square inch (kPa to PSI and PSI to kPa) for tire pressure and hydraulics.",
    canon="https://calcdomain.com/kpa-to-psi-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">kPa to PSI Converter</h1>
  <p class="text-gray-600">Convert pressure between kilopascals (kPa) and pounds per square inch (PSI).</p>
</header>

<section class="mb-8" aria-labelledby="kpapsi-heading">
  <h2 id="kpapsi-heading" class="text-xl font-semibold mb-4">Pressure converter – kPa ↔ PSI</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-kpapsi" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-kpapsi" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="kpa-to-psi">kPa → PSI</option>
        <option value="psi-to-kpa">PSI → kPa</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Approximate factor: <code>1 kPa ≈ 0.1450377377 PSI</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-kpapsi" class="block text-sm font-medium text-gray-700 mb-1">Input pressure</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-kpapsi" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 220">
        <span id="input-unit-kpapsi" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">kPa</span>
      </div>
    </div>
    <div>
      <label for="output-kpapsi" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-kpapsi" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-kpapsi" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">PSI</span>
      </div>
    </div>
  </div>

  <button id="swap-kpapsi" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>PSI ≈ kPa × 0.1450377377</code></p>
    <p><code>kPa ≈ PSI ÷ 0.1450377377</code></p>
  </div>
</section>

<script>
(function () {
  const PSI_PER_KPA = 0.1450377377;
  const dirEl = document.getElementById('direction-kpapsi');
  const inEl = document.getElementById('input-kpapsi');
  const outEl = document.getElementById('output-kpapsi');
  const inUnit = document.getElementById('input-unit-kpapsi');
  const outUnit = document.getElementById('output-unit-kpapsi');
  const swapBtn = document.getElementById('swap-kpapsi');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'kpa-to-psi') {
      inUnit.textContent = 'kPa';
      outUnit.textContent = 'PSI';
    } else {
      inUnit.textContent = 'PSI';
      outUnit.textContent = 'kPa';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'kpa-to-psi') res = val * PSI_PER_KPA;
    else res = val / PSI_PER_KPA;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'kpa-to-psi' ? 'psi-to-kpa' : 'kpa-to-psi';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 6) bar <-> PSI
pages.append(dict(
    filename="bar-to-psi-converter.html",
    title="Bar to PSI Converter – bar to pounds per square inch",
    desc="Convert pressure between bar and PSI (bar to PSI and PSI to bar) for hydraulics and industrial systems.",
    canon="https://calcdomain.com/bar-to-psi-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Bar to PSI Converter</h1>
  <p class="text-gray-600">Convert pressure between bar and pounds per square inch (PSI).</p>
</header>

<section class="mb-8" aria-labelledby="barpsi-heading">
  <h2 id="barpsi-heading" class="text-xl font-semibold mb-4">Pressure converter – bar ↔ PSI</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-barpsi" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-barpsi" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="bar-to-psi">bar → PSI</option>
        <option value="psi-to-bar">PSI → bar</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Approximate factor: <code>1 bar ≈ 14.5037738 PSI</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-barpsi" class="block text-sm font-medium text-gray-700 mb-1">Input pressure</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-barpsi" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 10">
        <span id="input-unit-barpsi" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">bar</span>
      </div>
    </div>
    <div>
      <label for="output-barpsi" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-barpsi" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-barpsi" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">PSI</span>
      </div>
    </div>
  </div>

  <button id="swap-barpsi" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>PSI ≈ bar × 14.5037738</code></p>
    <p><code>bar ≈ PSI ÷ 14.5037738</code></p>
  </div>
</section>

<script>
(function () {
  const PSI_PER_BAR = 14.5037738;
  const dirEl = document.getElementById('direction-barpsi');
  const inEl = document.getElementById('input-barpsi');
  const outEl = document.getElementById('output-barpsi');
  const inUnit = document.getElementById('input-unit-barpsi');
  const outUnit = document.getElementById('output-unit-barpsi');
  const swapBtn = document.getElementById('swap-barpsi');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'bar-to-psi') {
      inUnit.textContent = 'bar';
      outUnit.textContent = 'PSI';
    } else {
      inUnit.textContent = 'PSI';
      outUnit.textContent = 'bar';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'bar-to-psi') res = val * PSI_PER_BAR;
    else res = val / PSI_PER_BAR;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'bar-to-psi' ? 'psi-to-bar' : 'bar-to-psi';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 7) joules <-> calories
pages.append(dict(
    filename="joules-to-calories-converter.html",
    title="Joules to Calories Converter – J to cal and cal to J",
    desc="Convert energy between joules and small calories (J to cal and cal to J) for physics and chemistry.",
    canon="https://calcdomain.com/joules-to-calories-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Joules to Calories Converter</h1>
  <p class="text-gray-600">Convert energy between joules (J) and thermochemical calories (cal).</p>
</header>

<section class="mb-8" aria-labelledby="jcal-heading">
  <h2 id="jcal-heading" class="text-xl font-semibold mb-4">Energy converter – J ↔ cal</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-jcal" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-jcal" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="j-to-cal">J → cal</option>
        <option value="cal-to-j">cal → J</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Thermochemical value: <code>1 cal ≈ 4.184 J</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-jcal" class="block text-sm font-medium text-gray-700 mb-1">Input energy</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-jcal" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 1000">
        <span id="input-unit-jcal" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">J</span>
      </div>
    </div>
    <div>
      <label for="output-jcal" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-jcal" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-jcal" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">cal</span>
      </div>
    </div>
  </div>

  <button id="swap-jcal" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>cal ≈ J ÷ 4.184</code></p>
    <p><code>J ≈ cal × 4.184</code></p>
  </div>
</section>

<script>
(function () {
  const J_PER_CAL = 4.184;
  const dirEl = document.getElementById('direction-jcal');
  const inEl = document.getElementById('input-jcal');
  const outEl = document.getElementById('output-jcal');
  const inUnit = document.getElementById('input-unit-jcal');
  const outUnit = document.getElementById('output-unit-jcal');
  const swapBtn = document.getElementById('swap-jcal');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'j-to-cal') {
      inUnit.textContent = 'J';
      outUnit.textContent = 'cal';
    } else {
      inUnit.textContent = 'cal';
      outUnit.textContent = 'J';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'j-to-cal') res = val / J_PER_CAL;
    else res = val * J_PER_CAL;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'j-to-cal' ? 'cal-to-j' : 'j-to-cal';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 8) kJ <-> kcal
pages.append(dict(
    filename="kilojoules-to-kilocalories-converter.html",
    title="Kilojoules to Kilocalories Converter – kJ to kcal and kcal to kJ",
    desc="Convert energy between kilojoules and food kilocalories (kJ to kcal and kcal to kJ) for nutrition labels and diet planning.",
    canon="https://calcdomain.com/kilojoules-to-kilocalories-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Kilojoules to Kilocalories Converter</h1>
  <p class="text-gray-600">Convert energy between kilojoules (kJ) and kilocalories (kcal).</p>
</header>

<section class="mb-8" aria-labelledby="kjkcal-heading">
  <h2 id="kjkcal-heading" class="text-xl font-semibold mb-4">Energy converter – kJ ↔ kcal</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-kjkcal" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-kjkcal" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="kj-to-kcal">kJ → kcal</option>
        <option value="kcal-to-kj">kcal → kJ</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Nutrition standard: <code>1 kcal ≈ 4.184 kJ</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-kjkcal" class="block text-sm font-medium text-gray-700 mb-1">Input energy</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-kjkcal" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 840">
        <span id="input-unit-kjkcal" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">kJ</span>
      </div>
    </div>
    <div>
      <label for="output-kjkcal" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-kjkcal" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-kjkcal" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">kcal</span>
      </div>
    </div>
  </div>

  <button id="swap-kjkcal" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>kcal ≈ kJ ÷ 4.184</code></p>
    <p><code>kJ ≈ kcal × 4.184</code></p>
  </div>
</section>

<script>
(function () {
  const KJ_PER_KCAL = 4.184;
  const dirEl = document.getElementById('direction-kjkcal');
  const inEl = document.getElementById('input-kjkcal');
  const outEl = document.getElementById('output-kjkcal');
  const inUnit = document.getElementById('input-unit-kjkcal');
  const outUnit = document.getElementById('output-unit-kjkcal');
  const swapBtn = document.getElementById('swap-kjkcal');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'kj-to-kcal') {
      inUnit.textContent = 'kJ';
      outUnit.textContent = 'kcal';
    } else {
      inUnit.textContent = 'kcal';
      outUnit.textContent = 'kJ';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'kj-to-kcal') res = val / KJ_PER_KCAL;
    else res = val * KJ_PER_KCAL;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'kj-to-kcal' ? 'kcal-to-kj' : 'kj-to-kcal';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# write files
pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
for p in pages:
    html = build_html(p["title"], p["desc"], p["canon"], p["content"])
    out_path = pathlib.Path(output_dir) / p["filename"]
    out_path.write_text(html, encoding="utf-8")
    print(f"Created {out_path}")

PY

echo "Done generating batch 3 converters."
