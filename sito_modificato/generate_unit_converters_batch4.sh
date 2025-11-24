#!/usr/bin/env bash
set -euo pipefail

# Usage: ./generate_unit_converters_batch4.sh [OUTPUT_DIR]
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
        <span class="text-sm text-gray-500 hidden sm:inline">Engineering & scientific unit converters</span>
      </div>
    </header>

    <main class="flex-1 container mx-auto px-4 py-8 max-w-4xl">
      """ + body_content + """
    </main>

    <footer class="bg-gray-900 text-gray-400 text-sm">
      <div class="container mx-auto px-4 py-6 flex flex-col sm:flex-row justify-between gap-2">
        <p>&copy; 2025 CalcDomain. All rights reserved.</p>
        <p><a href="https://calcdomain.com/engineering-unit-converters" class="hover:text-white">More engineering converters</a></p>
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

# 1) Pascals <-> bar
pages.append(dict(
    filename="pascals-to-bar-converter.html",
    title="Pascals to Bar Converter – Pa to bar and bar to Pa",
    desc="Convert pressure between pascals (Pa) and bar (Pa to bar and bar to Pa) for engineering applications.",
    canon="https://calcdomain.com/pascals-to-bar-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Pascals to Bar Converter</h1>
  <p class="text-gray-600">Convert pressure between pascals (Pa) and bar using the exact definition 1 bar = 100 000 Pa.</p>
</header>

<section class="mb-8" aria-labelledby="pabar-heading">
  <h2 id="pabar-heading" class="text-xl font-semibold mb-4">Pressure converter – Pa ↔ bar</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-pabar" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-pabar" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="pa-to-bar">Pa → bar</option>
        <option value="bar-to-pa">bar → Pa</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Exact: <code>1 bar = 100&nbsp;000 Pa</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-pabar" class="block text-sm font-medium text-gray-700 mb-1">Input pressure</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-pabar" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 101325">
        <span id="input-unit-pabar" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">Pa</span>
      </div>
    </div>
    <div>
      <label for="output-pabar" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-pabar" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-pabar" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">bar</span>
      </div>
    </div>
  </div>

  <button id="swap-pabar" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>bar = Pa ÷ 100000</code></p>
    <p><code>Pa = bar × 100000</code></p>
  </div>
</section>

<script>
(function () {
  const PA_PER_BAR = 100000;
  const dirEl = document.getElementById('direction-pabar');
  const inEl = document.getElementById('input-pabar');
  const outEl = document.getElementById('output-pabar');
  const inUnit = document.getElementById('input-unit-pabar');
  const outUnit = document.getElementById('output-unit-pabar');
  const swapBtn = document.getElementById('swap-pabar');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e8 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'pa-to-bar') {
      inUnit.textContent = 'Pa';
      outUnit.textContent = 'bar';
    } else {
      inUnit.textContent = 'bar';
      outUnit.textContent = 'Pa';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'pa-to-bar') res = val / PA_PER_BAR;
    else res = val * PA_PER_BAR;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'pa-to-bar' ? 'bar-to-pa' : 'pa-to-bar';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 2) Pascals <-> PSI
pages.append(dict(
    filename="pascals-to-psi-converter.html",
    title="Pascals to PSI Converter – Pa to PSI and PSI to Pa",
    desc="Convert pressure between pascals (Pa) and pounds per square inch (PSI) for engineering and fluid power.",
    canon="https://calcdomain.com/pascals-to-psi-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Pascals to PSI Converter</h1>
  <p class="text-gray-600">Convert pressure between pascals (Pa) and pounds per square inch (PSI).</p>
</header>

<section class="mb-8" aria-labelledby="papsi-heading">
  <h2 id="papsi-heading" class="text-xl font-semibold mb-4">Pressure converter – Pa ↔ PSI</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-papsi" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-papsi" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="pa-to-psi">Pa → PSI</option>
        <option value="psi-to-pa">PSI → Pa</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Approximate factor: <code>1 Pa ≈ 0.0001450377377 PSI</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-papsi" class="block text-sm font-medium text-gray-700 mb-1">Input pressure</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-papsi" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 101325">
        <span id="input-unit-papsi" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">Pa</span>
      </div>
    </div>
    <div>
      <label for="output-papsi" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-papsi" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-papsi" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">PSI</span>
      </div>
    </div>
  </div>

  <button id="swap-papsi" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>PSI ≈ Pa × 0.0001450377377</code></p>
    <p><code>Pa ≈ PSI ÷ 0.0001450377377</code></p>
  </div>
</section>

<script>
(function () {
  const PSI_PER_PA = 0.0001450377377;
  const dirEl = document.getElementById('direction-papsi');
  const inEl = document.getElementById('input-papsi');
  const outEl = document.getElementById('output-papsi');
  const inUnit = document.getElementById('input-unit-papsi');
  const outUnit = document.getElementById('output-unit-papsi');
  const swapBtn = document.getElementById('swap-papsi');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e8 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(6).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'pa-to-psi') {
      inUnit.textContent = 'Pa';
      outUnit.textContent = 'PSI';
    } else {
      inUnit.textContent = 'PSI';
      outUnit.textContent = 'Pa';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'pa-to-psi') res = val * PSI_PER_PA;
    else res = val / PSI_PER_PA;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'pa-to-psi' ? 'psi-to-pa' : 'pa-to-psi';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 3) atm <-> kPa
pages.append(dict(
    filename="atmospheres-to-kpa-converter.html",
    title="Atmospheres to kPa Converter – atm to kPa and kPa to atm",
    desc="Convert pressure between standard atmospheres (atm) and kilopascals (kPa).",
    canon="https://calcdomain.com/atmospheres-to-kpa-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Atmospheres to kPa Converter</h1>
  <p class="text-gray-600">Convert pressure between atmospheres (atm) and kilopascals (kPa).</p>
</header>

<section class="mb-8" aria-labelledby="atmkpa-heading">
  <h2 id="atmkpa-heading" class="text-xl font-semibold mb-4">Pressure converter – atm ↔ kPa</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-atmkpa" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-atmkpa" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="atm-to-kpa">atm → kPa</option>
        <option value="kpa-to-atm">kPa → atm</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Exact: <code>1 atm = 101.325 kPa</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-atmkpa" class="block text-sm font-medium text-gray-700 mb-1">Input pressure</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-atmkpa" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 1">
        <span id="input-unit-atmkpa" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">atm</span>
      </div>
    </div>
    <div>
      <label for="output-atmkpa" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-atmkpa" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-atmkpa" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">kPa</span>
      </div>
    </div>
  </div>

  <button id="swap-atmkpa" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>kPa = atm × 101.325</code></p>
    <p><code>atm = kPa ÷ 101.325</code></p>
  </div>
</section>

<script>
(function () {
  const KPA_PER_ATM = 101.325;
  const dirEl = document.getElementById('direction-atmkpa');
  const inEl = document.getElementById('input-atmkpa');
  const outEl = document.getElementById('output-atmkpa');
  const inUnit = document.getElementById('input-unit-atmkpa');
  const outUnit = document.getElementById('output-unit-atmkpa');
  const swapBtn = document.getElementById('swap-atmkpa');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'atm-to-kpa') {
      inUnit.textContent = 'atm';
      outUnit.textContent = 'kPa';
    } else {
      inUnit.textContent = 'kPa';
      outUnit.textContent = 'atm';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'atm-to-kpa') res = val * KPA_PER_ATM;
    else res = val / KPA_PER_ATM;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'atm-to-kpa' ? 'kpa-to-atm' : 'atm-to-kpa';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 4) atm <-> PSI
pages.append(dict(
    filename="atmospheres-to-psi-converter.html",
    title="Atmospheres to PSI Converter – atm to PSI and PSI to atm",
    desc="Convert pressure between atmospheres (atm) and pounds per square inch (PSI).",
    canon="https://calcdomain.com/atmospheres-to-psi-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Atmospheres to PSI Converter</h1>
  <p class="text-gray-600">Convert pressure between atmospheres (atm) and pounds per square inch (PSI).</p>
</header>

<section class="mb-8" aria-labelledby="atmpsi-heading">
  <h2 id="atmpsi-heading" class="text-xl font-semibold mb-4">Pressure converter – atm ↔ PSI</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-atmpsi" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-atmpsi" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="atm-to-psi">atm → PSI</option>
        <option value="psi-to-atm">PSI → atm</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Approximate: <code>1 atm ≈ 14.6959488 PSI</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-atmpsi" class="block text-sm font-medium text-gray-700 mb-1">Input pressure</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-atmpsi" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 1">
        <span id="input-unit-atmpsi" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">atm</span>
      </div>
    </div>
    <div>
      <label for="output-atmpsi" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-atmpsi" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-atmpsi" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">PSI</span>
      </div>
    </div>
  </div>

  <button id="swap-atmpsi" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>PSI ≈ atm × 14.6959488</code></p>
    <p><code>atm ≈ PSI ÷ 14.6959488</code></p>
  </div>
</section>

<script>
(function () {
  const PSI_PER_ATM = 14.6959488;
  const dirEl = document.getElementById('direction-atmpsi');
  const inEl = document.getElementById('input-atmpsi');
  const outEl = document.getElementById('output-atmpsi');
  const inUnit = document.getElementById('input-unit-atmpsi');
  const outUnit = document.getElementById('output-unit-atmpsi');
  const swapBtn = document.getElementById('swap-atmpsi');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'atm-to-psi') {
      inUnit.textContent = 'atm';
      outUnit.textContent = 'PSI';
    } else {
      inUnit.textContent = 'PSI';
      outUnit.textContent = 'atm';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'atm-to-psi') res = val * PSI_PER_ATM;
    else res = val / PSI_PER_ATM;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'atm-to-psi' ? 'psi-to-atm' : 'atm-to-psi';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 5) BTU <-> joules
pages.append(dict(
    filename="btu-to-joules-converter.html",
    title="BTU to Joules Converter – BTU to J and J to BTU",
    desc="Convert energy between British thermal units (BTU) and joules (J) for heating and cooling calculations.",
    canon="https://calcdomain.com/btu-to-joules-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">BTU to Joules Converter</h1>
  <p class="text-gray-600">Convert energy between BTU (International Table) and joules (J).</p>
</header>

<section class="mb-8" aria-labelledby="btuj-heading">
  <h2 id="btuj-heading" class="text-xl font-semibold mb-4">Energy converter – BTU ↔ J</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-btuj" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-btuj" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="btu-to-j">BTU → J</option>
        <option value="j-to-btu">J → BTU</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Approximate IT value: <code>1 BTU ≈ 1055.05585262 J</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-btuj" class="block text-sm font-medium text-gray-700 mb-1">Input energy</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-btuj" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 500">
        <span id="input-unit-btuj" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">BTU</span>
      </div>
    </div>
    <div>
      <label for="output-btuj" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-btuj" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-btuj" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">J</span>
      </div>
    </div>
  </div>

  <button id="swap-btuj" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>J ≈ BTU × 1055.05585262</code></p>
    <p><code>BTU ≈ J ÷ 1055.05585262</code></p>
  </div>
</section>

<script>
(function () {
  const J_PER_BTU = 1055.05585262;
  const dirEl = document.getElementById('direction-btuj');
  const inEl = document.getElementById('input-btuj');
  const outEl = document.getElementById('output-btuj');
  const inUnit = document.getElementById('input-unit-btuj');
  const outUnit = document.getElementById('output-unit-btuj');
  const swapBtn = document.getElementById('swap-btuj');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e9 || Math.abs(v) < 1e-3) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'btu-to-j') {
      inUnit.textContent = 'BTU';
      outUnit.textContent = 'J';
    } else {
      inUnit.textContent = 'J';
      outUnit.textContent = 'BTU';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'btu-to-j') res = val * J_PER_BTU;
    else res = val / J_PER_BTU;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'btu-to-j' ? 'j-to-btu' : 'btu-to-j';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 6) kWh <-> MJ
pages.append(dict(
    filename="kwh-to-megajoules-converter.html",
    title="kWh to Megajoules Converter – kWh to MJ and MJ to kWh",
    desc="Convert energy between kilowatt-hours (kWh) and megajoules (MJ).",
    canon="https://calcdomain.com/kwh-to-megajoules-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">kWh to Megajoules Converter</h1>
  <p class="text-gray-600">Convert energy between kilowatt-hours (kWh) and megajoules (MJ) for electricity and fuel calculations.</p>
</header>

<section class="mb-8" aria-labelledby="kwhmj-heading">
  <h2 id="kwhmj-heading" class="text-xl font-semibold mb-4">Energy converter – kWh ↔ MJ</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-kwhmj" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-kwhmj" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="kwh-to-mj">kWh → MJ</option>
        <option value="mj-to-kwh">MJ → kWh</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Exact: <code>1 kWh = 3.6 MJ</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-kwhmj" class="block text-sm font-medium text-gray-700 mb-1">Input energy</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-kwhmj" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 5">
        <span id="input-unit-kwhmj" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">kWh</span>
      </div>
    </div>
    <div>
      <label for="output-kwhmj" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-kwhmj" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-kwhmj" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">MJ</span>
      </div>
    </div>
  </div>

  <button id="swap-kwhmj" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>MJ = kWh × 3.6</code></p>
    <p><code>kWh = MJ ÷ 3.6</code></p>
  </div>
</section>

<script>
(function () {
  const MJ_PER_KWH = 3.6;
  const dirEl = document.getElementById('direction-kwhmj');
  const inEl = document.getElementById('input-kwhmj');
  const outEl = document.getElementById('output-kwhmj');
  const inUnit = document.getElementById('input-unit-kwhmj');
  const outUnit = document.getElementById('output-unit-kwhmj');
  const swapBtn = document.getElementById('swap-kwhmj');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'kwh-to-mj') {
      inUnit.textContent = 'kWh';
      outUnit.textContent = 'MJ';
    } else {
      inUnit.textContent = 'MJ';
      outUnit.textContent = 'kWh';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'kwh-to-mj') res = val * MJ_PER_KWH;
    else res = val / MJ_PER_KWH;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'kwh-to-mj' ? 'mj-to-kwh' : 'kwh-to-mj';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 7) Watts <-> horsepower
pages.append(dict(
    filename="watts-to-horsepower-converter.html",
    title="Watts to Horsepower Converter – W to hp and hp to W",
    desc="Convert power between watts (W) and mechanical horsepower (hp).",
    canon="https://calcdomain.com/watts-to-horsepower-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Watts to Horsepower Converter</h1>
  <p class="text-gray-600">Convert power between watts (W) and mechanical horsepower (hp).</p>
</header>

<section class="mb-8" aria-labelledby="whp-heading">
  <h2 id="whp-heading" class="text-xl font-semibold mb-4">Power converter – W ↔ hp</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-whp" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-whp" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="w-to-hp">W → hp</option>
        <option value="hp-to-w">hp → W</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Mechanical horsepower: <code>1 hp ≈ 745.6998716 W</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-whp" class="block text-sm font-medium text-gray-700 mb-1">Input power</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-whp" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 1500">
        <span id="input-unit-whp" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">W</span>
      </div>
    </div>
    <div>
      <label for="output-whp" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-whp" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-whp" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">hp</span>
      </div>
    </div>
  </div>

  <button id="swap-whp" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>hp ≈ W ÷ 745.6998716</code></p>
    <p><code>W ≈ hp × 745.6998716</code></p>
  </div>
</section>

<script>
(function () {
  const W_PER_HP = 745.6998716;
  const dirEl = document.getElementById('direction-whp');
  const inEl = document.getElementById('input-whp');
  const outEl = document.getElementById('output-whp');
  const inUnit = document.getElementById('input-unit-whp');
  const outUnit = document.getElementById('output-unit-whp');
  const swapBtn = document.getElementById('swap-whp');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'w-to-hp') {
      inUnit.textContent = 'W';
      outUnit.textContent = 'hp';
    } else {
      inUnit.textContent = 'hp';
      outUnit.textContent = 'W';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'w-to-hp') res = val / W_PER_HP;
    else res = val * W_PER_HP;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'w-to-hp' ? 'hp-to-w' : 'w-to-hp';
    updateUnits();
    convert();
  });

  updateUnits();
})();
</script>
"""
))

# 8) N·m <-> ft·lbf
pages.append(dict(
    filename="newton-meters-to-foot-pounds-converter.html",
    title="Newton-meters to Foot-pounds Converter – N·m to ft·lbf and ft·lbf to N·m",
    desc="Convert torque between newton-meters (N·m) and foot-pounds (ft·lbf).",
    canon="https://calcdomain.com/newton-meters-to-foot-pounds-converter",
    content="""<header class="mb-6">
  <h1 class="text-3xl font-bold mb-2">Newton-meters to Foot-pounds Converter</h1>
  <p class="text-gray-600">Convert torque between newton-meters (N·m) and foot-pounds (ft·lbf).</p>
</header>

<section class="mb-8" aria-labelledby="nmftlb-heading">
  <h2 id="nmftlb-heading" class="text-xl font-semibold mb-4">Torque converter – N·m ↔ ft·lbf</h2>

  <div class="grid gap-4 md:grid-cols-2 mb-4">
    <div>
      <label for="direction-nmftlb" class="block text-sm font-medium text-gray-700 mb-1">Direction</label>
      <select id="direction-nmftlb" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="nm-to-ftlb">N·m → ft·lbf</option>
        <option value="ftlb-to-nm">ft·lbf → N·m</option>
      </select>
    </div>
    <div class="text-xs text-gray-500 flex items-end">
      <p>Approximate: <code>1 N·m ≈ 0.7375621493 ft·lbf</code>.</p>
    </div>
  </div>

  <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
    <div>
      <label for="input-nmftlb" class="block text-sm font-medium text-gray-700 mb-1">Input torque</label>
      <div class="flex rounded-md shadow-sm">
        <input id="input-nmftlb" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. 100">
        <span id="input-unit-nmftlb" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">N·m</span>
      </div>
    </div>
    <div>
      <label for="output-nmftlb" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
      <div class="flex rounded-md shadow-sm">
        <input id="output-nmftlb" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100" placeholder="0.00">
        <span id="output-unit-nmftlb" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">ft·lbf</span>
      </div>
    </div>
  </div>

  <button id="swap-nmftlb" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
    Swap direction
  </button>
</section>

<section class="prose">
  <h2>Formula</h2>
  <div class="formula-box">
    <p><code>ft·lbf ≈ N·m × 0.7375621493</code></p>
    <p><code>N·m ≈ ft·lbf ÷ 0.7375621493</code></p>
  </div>
</section>

<script>
(function () {
  const FTLB_PER_NM = 0.7375621493;
  const dirEl = document.getElementById('direction-nmftlb');
  const inEl = document.getElementById('input-nmftlb');
  const outEl = document.getElementById('output-nmftlb');
  const inUnit = document.getElementById('input-unit-nmftlb');
  const outUnit = document.getElementById('output-unit-nmftlb');
  const swapBtn = document.getElementById('swap-nmftlb');

  function format(v) {
    if (!isFinite(v)) return '';
    if (Math.abs(v) >= 1e6 || Math.abs(v) < 1e-4) return v.toExponential(6);
    return v.toFixed(4).replace(/\\.0+$/, '').replace(/\\.(?=\\D|$)/, '');
  }

  function updateUnits() {
    if (dirEl.value === 'nm-to-ftlb') {
      inUnit.textContent = 'N·m';
      outUnit.textContent = 'ft·lbf';
    } else {
      inUnit.textContent = 'ft·lbf';
      outUnit.textContent = 'N·m';
    }
  }

  function convert() {
    const val = parseFloat(inEl.value);
    if (isNaN(val)) { outEl.value = ''; return; }
    let res;
    if (dirEl.value === 'nm-to-ftlb') res = val * FTLB_PER_NM;
    else res = val / FTLB_PER_NM;
    outEl.value = format(res);
  }

  dirEl.addEventListener('change', () => { updateUnits(); convert(); });
  inEl.addEventListener('input', convert);
  swapBtn.addEventListener('click', () => {
    dirEl.value = dirEl.value === 'nm-to-ftlb' ? 'ftlb-to-nm' : 'nm-to-ftlb';
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

echo "Done generating batch 4 converters."
