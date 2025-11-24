#!/usr/bin/env bash
set -euo pipefail

# Usage: ./generate_unit_converters.sh [OUTPUT_DIR]
# If OUTPUT_DIR is not provided, files are created in the current directory.
OUTPUT_DIR="${1:-.}"

mkdir -p "$OUTPUT_DIR"

echo "Generating HTML calculators in: $OUTPUT_DIR"

############################################
# 1) kW to HP Converter (bidirectional)
############################################
cat > "$OUTPUT_DIR/kw-to-hp-converter.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>kW to HP Converter – Convert Kilowatts to Horsepower</title>
    <meta name="description" content="Use this kW to HP converter to quickly convert kilowatts to horsepower and back. Includes formulas, examples and engineering-grade reference values.">
    <link rel="canonical" href="https://calcdomain.com/kw-to-hp-converter">

    <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="shortcut icon" href="/favicon.ico" />
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />

    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .card-hover { transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; }
        .card-hover:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
        .prose { max-width: 65ch; margin-left: auto; margin-right: auto; }
        .prose h2 { font-size: 1.5rem; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem; }
        .prose h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; }
        .prose p { margin-bottom: 1rem; line-height: 1.6; }
        .prose ul, .prose ol { margin-left: 1.5rem; margin-bottom: 1rem; }
        .prose li { margin-bottom: 0.5rem; }
        .formula-box { background: #f3f4f6; border: 1px solid #d1d5db; border-radius: 8px; padding: 1rem; overflow-x: auto; margin: 1rem 0; }
    </style>

    <!-- Google tag (gtag.js) -->
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
    </script>

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "BreadcrumbList",
          "itemListElement": [
            {
              "@type": "ListItem",
              "position": 1,
              "name": "Home",
              "item": "https://calcdomain.com/"
            },
            {
              "@type": "ListItem",
              "position": 2,
              "name": "Math & Conversions",
              "item": "https://calcdomain.com/categories/math-conversions"
            },
            {
              "@type": "ListItem",
              "position": 3,
              "name": "Measurement Unit Conversions",
              "item": "https://calcdomain.com/subcategories/math-conversions-measurement-unit-conversions"
            },
            {
              "@type": "ListItem",
              "position": 4,
              "name": "kW to HP Converter",
              "item": "https://calcdomain.com/kw-to-hp-converter"
            }
          ]
        },
        {
          "@type": "FAQPage",
          "mainEntity": [
            {
              "@type": "Question",
              "name": "How do you convert kW to horsepower?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "To convert kilowatts to mechanical horsepower, multiply power in kW by 1.34102. HP (mechanical) = kW × 1.34102. The calculator on this page applies this formula automatically."
              }
            },
            {
              "@type": "Question",
              "name": "What is the difference between metric and mechanical horsepower?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Mechanical horsepower is defined as 745.699872 watts, while metric horsepower (PS) is defined as 735.49875 watts. For automotive and engineering usage in English-language contexts, mechanical horsepower is the most common choice."
              }
            },
            {
              "@type": "Question",
              "name": "Is this kW to HP converter suitable for motor and engine sizing?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes. The converter uses standard engineering definitions of kilowatt and mechanical horsepower and is appropriate for quick sizing checks of motors, pumps, fans and internal combustion engines."
              }
            }
          ]
        }
      ]
    }
    </script>
</head>
<body class="bg-gray-50 text-gray-800">

    <script async src="https://pagead2.googlesyndication.com/pagead/js?client=ca-pub-9476637732224939"
         crossorigin="anonymous"></script>

    <header class="bg-white shadow-sm sticky top-0 z-50">
      <nav class="container mx-auto px-4 lg:px-6 py-4" aria-label="Primary">
        <div class="flex justify-between items-center">
          <a href="https://calcdomain.com" class="text-2xl font-bold text-blue-600">CalcDomain</a>
          <div class="w-full max-w-md hidden md:block mx-8">
            <div class="relative">
              <input type="search" id="search-input" placeholder="Search for a calculator..." class="w-full py-2 px-4 pr-10 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" autocomplete="off" />
              <svg class="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
              <div id="search-results" class="absolute top-full left-0 right-0 bg-white shadow-lg rounded-lg mt-2 max-h-96 overflow-y-auto z-50 hidden border border-gray-200"></div>
            </div>
          </div>
          <div class="hidden md:flex items-center space-x-6">
            <a href="https://calcdomain.com/search" class="text-gray-700 hover:text-blue-600 transition-colors">Advanced Search</a>
            <a href="https://calcdomain.com/categories" class="text-gray-700 hover:text-blue-600 transition-colors">Categories</a>
          </div>
          <button id="mobile-menu-toggle" class="md:hidden p-2" aria-controls="mobile-menu" aria-expanded="false" aria-label="Open menu" type="button">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </button>
        </div>
        <nav id="mobile-menu" class="md:hidden mt-4 hidden" aria-label="Mobile menu" role="navigation">
          <div class="mb-4">
            <div class="relative">
              <input type="search" id="mobile-search-input" placeholder="Search calculators..." class="w-full py-3 px-4 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
              <svg class="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
          </div>
          <div class="space-y-2">
            <a href="https://calcdomain.com/search" class="block py-2 text-gray-700 hover:text-blue-600">Advanced Search</a>
            <a href="https://calcdomain.com/categories" class="block py-2 text-gray-700 hover:text-blue-600">Categories</a>
          </div>
        </nav>
      </nav>
    </header>

    <div class="container mx-auto px-4 py-8">
      <nav id="breadcrumb-container" class="text-sm mb-4 text-gray-600" aria-label="Breadcrumb">
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
            kW to HP Converter
          </li>
        </ol>
      </nav>

      <div class="flex flex-col lg:flex-row gap-8">
        <main class="w-full lg:w-2/3">
          <div class="bg-white p-6 rounded-lg shadow-md">
            <header class="mb-6">
              <h1 class="text-2xl md:text-3xl font-bold mb-2">kW to HP Converter</h1>
              <p class="text-gray-600">Convert kilowatts (kW) to mechanical horsepower (HP) and back, using standard engineering conversion factors.</p>
            </header>

            <section aria-labelledby="converter-heading" class="mb-8">
              <h2 id="converter-heading" class="text-xl font-semibold mb-4">Power converter – kilowatts &lt;&rarr; horsepower</h2>

              <div class="grid gap-4 md:grid-cols-2 mb-4">
                <div>
                  <label for="direction" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
                  <select id="direction" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="kw-to-hp">kW → HP (mechanical)</option>
                    <option value="hp-to-kw">HP (mechanical) → kW</option>
                  </select>
                </div>

                <div>
                  <label for="hp-type" class="block text-sm font-medium text-gray-700 mb-1">Horsepower definition</label>
                  <select id="hp-type" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="mechanical">Mechanical HP (745.699872 W)</option>
                    <option value="metric">Metric HP / PS (735.49875 W)</option>
                  </select>
                </div>
              </div>

              <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
                <div>
                  <label for="input-value" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
                  <div class="flex rounded-md shadow-sm">
                    <input id="input-value" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
                    <span id="input-unit" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">kW</span>
                  </div>
                </div>

                <div>
                  <label for="output-value" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
                  <div class="flex rounded-md shadow-sm">
                    <input id="output-value" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
                    <span id="output-unit" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">HP</span>
                  </div>
                </div>
              </div>

              <p id="converter-note" class="text-xs text-gray-500 mb-2">
                Mechanical horsepower: 1 HP = 745.699872 W. Metric horsepower (PS): 1 PS = 735.49875 W.
              </p>

              <button id="swap-direction" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
                Swap direction
              </button>
            </section>

            <section class="prose">
              <h2>How to convert kW to HP</h2>
              <p>
                Power in kilowatts can be expressed in horsepower by applying a constant conversion factor that depends on the horsepower definition.
                This tool supports both <strong>mechanical horsepower</strong> and <strong>metric horsepower (PS)</strong>.
              </p>

              <div class="formula-box">
                <p class="font-semibold mb-2">Mechanical horsepower</p>
                <p class="mb-1"><code>1 HP<sub>mech</sub> = 745.699872 W</code></p>
                <p class="mb-1"><code>1 kW = 1000 W</code></p>
                <p class="mb-1"><code>HP<sub>mech</sub> = kW × 1000 / 745.699872 ≈ kW × 1.34102</code></p>
                <p class="mb-1"><code>kW = HP<sub>mech</sub> × 745.699872 / 1000 ≈ HP × 0.74570</code></p>
              </div>

              <div class="formula-box">
                <p class="font-semibold mb-2">Metric horsepower (PS)</p>
                <p class="mb-1"><code>1 PS = 735.49875 W</code></p>
                <p class="mb-1"><code>HP<sub>metric</sub> = kW × 1000 / 735.49875 ≈ kW × 1.35962</code></p>
                <p class="mb-1"><code>kW = HP<sub>metric</sub> × 735.49875 / 1000 ≈ HP × 0.73550</code></p>
              </div>

              <h3>Example: 5 kW to HP</h3>
              <p>Using mechanical horsepower:</p>
              <p><code>HP = 5 × 1000 / 745.699872 ≈ 6.71 HP</code></p>

              <h3>Engineering use cases</h3>
              <ul>
                <li>Motor and pump sizing for HVAC and industrial equipment.</li>
                <li>Estimating engine horsepower from rated electrical power.</li>
                <li>Comparing European (kW) and US (HP) specifications on datasheets.</li>
              </ul>

              <h2>FAQ</h2>
              <h3>Is 1 kW equal to 1.34 HP?</h3>
              <p>
                Yes, for mechanical horsepower the commonly used rounded factor is 1 kW ≈ 1.341 HP.
                The calculator uses the more precise constant 745.699872 W per HP internally.
              </p>

              <h3>Which horsepower should I use for cars?</h3>
              <p>
                In most English-language documentation and in North America, mechanical horsepower is used.
                In some European countries, metric horsepower (PS) still appears in legacy documentation.
              </p>

              <h3>Can I convert HP to kW with this tool?</h3>
              <p>
                Yes. Change the direction to “HP → kW” or press the swap button and enter the horsepower value.
                The result is shown immediately with the selected horsepower definition.
              </p>
            </section>
          </div>
        </main>

        <aside class="w-full lg:w-1/3">
          <div class="bg-white p-5 rounded-lg shadow-md mb-6 card-hover">
            <h2 class="text-lg font-semibold mb-3">Related unit converters</h2>
            <ul class="space-y-2 text-sm">
              <li><a href="https://calcdomain.com/power-unit-converter" class="text-blue-600 hover:underline">Power Unit Converter (watts, HP, BTU/hr)</a></li>
              <li><a href="https://calcdomain.com/energy-unit-converter" class="text-blue-600 hover:underline">Energy Unit Converter (J, cal, kWh, BTU)</a></li>
              <li><a href="https://calcdomain.com/kw-to-kwh-calculator" class="text-blue-600 hover:underline">kW to kWh Calculator</a></li>
              <li><a href="https://calcdomain.com/hp-to-kw-converter" class="text-blue-600 hover:underline">HP to kW Converter</a></li>
              <li><a href="https://calcdomain.com/pressure-unit-converter" class="text-blue-600 hover:underline">Pressure Unit Converter (Pa, bar, atm, psi)</a></li>
            </ul>
          </div>

          <div class="bg-white p-5 rounded-lg shadow-md card-hover">
            <h2 class="text-lg font-semibold mb-3">Category: Measurement Unit Conversions</h2>
            <p class="text-sm text-gray-600 mb-3">
              Explore more engineering-grade unit converters for power, energy, pressure, temperature and more.
            </p>
            <a href="https://calcdomain.com/subcategories/math-conversions-measurement-unit-conversions"
               class="inline-flex items-center px-3 py-2 text-sm font-medium bg-blue-600 text-white rounded-md hover:bg-blue-700">
              Browse all unit converters
            </a>
          </div>
        </aside>
      </div>
    </div>

    <footer class="bg-gray-900 text-white py-12">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 class="text-2xl font-bold mb-4">CalcDomain</h3>
            <p class="text-gray-400 mb-4">Your trusted source for free online calculators. Accurate, fast, and reliable calculations for every need.</p>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-4">Categories</h4>
            <ul class="space-y-2">
              <li><a href="https://calcdomain.com/finance" class="text-gray-400 hover:text-white">Finance</a></li>
              <li><a href="https://calcdomain.com/health-fitness" class="text-gray-400 hover:text-white">Health &amp; Fitness</a></li>
              <li><a href="https://calcdomain.com/math-conversions" class="text-gray-400 hover:text-white">Math &amp; Conversions</a></li>
              <li><a href="https://calcdomain.com/lifestyle-everyday" class="text-gray-400 hover:text-white">Lifestyle &amp; Everyday</a></li>
              <li><a href="https://calcdomain.com/construction-diy" class="text-gray-400 hover:text-white">Construction &amp; DIY</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-4">Popular Tools</h4>
            <ul class="space-y-2">
              <li><a href="https://calcdomain.com/mortgage-payment" class="text-gray-400 hover:text-white">Mortgage Calculator</a></li>
              <li><a href="https://calcdomain.com/percentage-calculator" class="text-gray-400 hover:text-white">Percentage Calculator</a></li>
              <li><a href="https://calcdomain.com/bmi-calculator" class="text-gray-400 hover:text-white">BMI Calculator</a></li>
              <li><a href="https://calcdomain.com/auto-loan-calculator" class="text-gray-400 hover:text-white">Auto Loan Calculator</a></li>
              <li><a href="https://calcdomain.com/house-affordability" class="text-gray-400 hover:text-white">House Affordability</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-4">Support</h4>
            <ul class="space-y-2">
              <li><a href="https://calcdomain.com/about" class="text-gray-400 hover:text-white">About Us</a></li>
              <li><a href="https://calcdomain.com/contact" class="text-gray-400 hover:text-white">Contact</a></li>
              <li><a href="https://calcdomain.com/privacy" class="text-gray-400 hover:text-white">Privacy Policy</a></li>
              <li><a href="https://calcdomain.com/terms" class="text-gray-400 hover:text-white">Terms of Service</a></li>
              <li><a href="https://calcdomain.com/sitemap" class="text-gray-400 hover:text-white">Site Map</a></li>
            </ul>
          </div>
        </div>
        <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 CalcDomain. All Rights Reserved. | Free Online Calculators for Everyone</p>
        </div>
      </div>
    </footer>

    <script src="/assets/js/script_menu.js" defer></script>
    <script src="/assets/js/script_faq.js" defer></script>
    <script src="search.js" defer></script>

    <script>
      window.MathJax = {
        tex: { inlineMath: [['\\(','\\)'], ['$', '$']], displayMath: [['$','$'], ['\\[','\\]']] },
        svg: { fontCache: 'global' }
      };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

    <script>
      (function () {
        const directionEl = document.getElementById('direction');
        const hpTypeEl = document.getElementById('hp-type');
        const inputEl = document.getElementById('input-value');
        const outputEl = document.getElementById('output-value');
        const inputUnitEl = document.getElementById('input-unit');
        const outputUnitEl = document.getElementById('output-unit');
        const swapBtn = document.getElementById('swap-direction');

        function getHpFactor() {
          // returns W per HP
          return hpTypeEl.value === 'metric' ? 735.49875 : 745.699872;
        }

        function formatNumber(value) {
          if (!isFinite(value)) return '';
          if (Math.abs(value) >= 1000 || Math.abs(value) < 0.001) {
            return value.toExponential(6);
          }
          return value.toFixed(6).replace(/\.?0+$/, '');
        }

        function updateUnits() {
          if (directionEl.value === 'kw-to-hp') {
            inputUnitEl.textContent = 'kW';
            outputUnitEl.textContent = 'HP';
          } else {
            inputUnitEl.textContent = 'HP';
            outputUnitEl.textContent = 'kW';
          }
        }

        function convert() {
          const val = parseFloat(inputEl.value);
          if (isNaN(val)) {
            outputEl.value = '';
            return;
          }
          const wPerHp = getHpFactor();
          let result;
          if (directionEl.value === 'kw-to-hp') {
            const watts = val * 1000;
            result = watts / wPerHp;
          } else {
            const watts = val * wPerHp;
            result = watts / 1000;
          }
          outputEl.value = formatNumber(result);
        }

        directionEl.addEventListener('change', () => {
          updateUnits();
          convert();
        });
        hpTypeEl.addEventListener('change', convert);
        inputEl.addEventListener('input', convert);

        swapBtn.addEventListener('click', () => {
          directionEl.value = directionEl.value === 'kw-to-hp' ? 'hp-to-kw' : 'kw-to-hp';
          updateUnits();
          convert();
        });

        updateUnits();
      })();
    </script>
</body>
</html>
EOF

############################################
# 2) Joules to kWh Converter (bidirectional)
############################################
cat > "$OUTPUT_DIR/joules-to-kwh.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Joules to kWh Converter – Convert Energy Units</title>
    <meta name="description" content="Convert Joules to kilowatt-hours (kWh) and back with this precise energy unit converter. Includes formulas, worked examples and typical engineering use cases.">
    <link rel="canonical" href="https://calcdomain.com/joules-to-kwh">

    <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="shortcut icon" href="/favicon.ico" />
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />

    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .card-hover { transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; }
        .card-hover:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
        .prose { max-width: 65ch; margin-left: auto; margin-right: auto; }
        .prose h2 { font-size: 1.5rem; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem; }
        .prose h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; }
        .prose p { margin-bottom: 1rem; line-height: 1.6; }
        .prose ul, .prose ol { margin-left: 1.5rem; margin-bottom: 1rem; }
        .prose li { margin-bottom: 0.5rem; }
        .formula-box { background: #f3f4f6; border: 1px solid #d1d5db; border-radius: 8px; padding: 1rem; overflow-x: auto; margin: 1rem 0; }
    </style>

    <!-- Google tag (gtag.js) -->
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
    </script>

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "BreadcrumbList",
          "itemListElement": [
            {
              "@type": "ListItem",
              "position": 1,
              "name": "Home",
              "item": "https://calcdomain.com/"
            },
            {
              "@type": "ListItem",
              "position": 2,
              "name": "Math & Conversions",
              "item": "https://calcdomain.com/categories/math-conversions"
            },
            {
              "@type": "ListItem",
              "position": 3,
              "name": "Measurement Unit Conversions",
              "item": "https://calcdomain.com/subcategories/math-conversions-measurement-unit-conversions"
            },
            {
              "@type": "ListItem",
              "position": 4,
              "name": "Joules to kWh Converter",
              "item": "https://calcdomain.com/joules-to-kwh"
            }
          ]
        },
        {
          "@type": "FAQPage",
          "mainEntity": [
            {
              "@type": "Question",
              "name": "How do you convert Joules to kWh?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "To convert Joules to kilowatt-hours, divide energy in Joules by 3,600,000. kWh = J / 3,600,000. The calculator applies this conversion automatically."
              }
            },
            {
              "@type": "Question",
              "name": "Why is 1 kWh equal to 3,600,000 Joules?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "One kilowatt is 1000 watts, and one hour is 3600 seconds. Since 1 watt = 1 joule per second, 1 kWh = 1000 joules/second × 3600 seconds = 3,600,000 joules."
              }
            },
            {
              "@type": "Question",
              "name": "Is this converter suitable for electricity billing estimates?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes. Electricity meters bill in kWh. Converting Joules to kWh lets you estimate consumption and cost based on physical or simulated energy values."
              }
            }
          ]
        }
      ]
    }
    </script>
</head>
<body class="bg-gray-50 text-gray-800">

    <script async src="https://pagead2.googlesyndication.com/pagead/js?client=ca-pub-9476637732224939"
         crossorigin="anonymous"></script>

    <header class="bg-white shadow-sm sticky top-0 z-50">
      <nav class="container mx-auto px-4 lg:px-6 py-4" aria-label="Primary">
        <div class="flex justify-between items-center">
          <a href="https://calcdomain.com" class="text-2xl font-bold text-blue-600">CalcDomain</a>
          <div class="w-full max-w-md hidden md:block mx-8">
            <div class="relative">
              <input type="search" id="search-input" placeholder="Search for a calculator..." class="w-full py-2 px-4 pr-10 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" autocomplete="off" />
              <svg class="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
              <div id="search-results" class="absolute top-full left-0 right-0 bg-white shadow-lg rounded-lg mt-2 max-h-96 overflow-y-auto z-50 hidden border border-gray-200"></div>
            </div>
          </div>
          <div class="hidden md:flex items-center space-x-6">
            <a href="https://calcdomain.com/search" class="text-gray-700 hover:text-blue-600 transition-colors">Advanced Search</a>
            <a href="https://calcdomain.com/categories" class="text-gray-700 hover:text-blue-600 transition-colors">Categories</a>
          </div>
          <button id="mobile-menu-toggle" class="md:hidden p-2" aria-controls="mobile-menu" aria-expanded="false" aria-label="Open menu" type="button">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </button>
        </div>
        <nav id="mobile-menu" class="md:hidden mt-4 hidden" aria-label="Mobile menu" role="navigation">
          <div class="mb-4">
            <div class="relative">
              <input type="search" id="mobile-search-input" placeholder="Search calculators..." class="w-full py-3 px-4 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
              <svg class="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
          </div>
          <div class="space-y-2">
            <a href="https://calcdomain.com/search" class="block py-2 text-gray-700 hover:text-blue-600">Advanced Search</a>
            <a href="https://calcdomain.com/categories" class="block py-2 text-gray-700 hover:text-blue-600">Categories</a>
          </div>
        </nav>
      </nav>
    </header>

    <div class="container mx-auto px-4 py-8">
      <nav id="breadcrumb-container" class="text-sm mb-4 text-gray-600" aria-label="Breadcrumb">
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
            Joules to kWh Converter
          </li>
        </ol>
      </nav>

      <div class="flex flex-col lg:flex-row gap-8">
        <main class="w-full lg:w-2/3">
          <div class="bg-white p-6 rounded-lg shadow-md">
            <header class="mb-6">
              <h1 class="text-2xl md:text-3xl font-bold mb-2">Joules to kWh Converter</h1>
              <p class="text-gray-600">Convert energy between Joules (J) and kilowatt-hours (kWh) using the exact physical relationship.</p>
            </header>

            <section aria-labelledby="converter-heading" class="mb-8">
              <h2 id="converter-heading" class="text-xl font-semibold mb-4">Energy converter – Joules &lt;&rarr; kWh</h2>

              <div class="grid gap-4 md:grid-cols-2 mb-4">
                <div>
                  <label for="direction-jk" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
                  <select id="direction-jk" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="j-to-kwh">J → kWh</option>
                    <option value="kwh-to-j">kWh → J</option>
                  </select>
                </div>
                <div>
                  <p class="text-xs text-gray-500 mt-6">
                    Exact definition: <code>1 kWh = 3,600,000 J</code>.
                  </p>
                </div>
              </div>

              <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
                <div>
                  <label for="input-jk" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
                  <div class="flex rounded-md shadow-sm">
                    <input id="input-jk" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
                    <span id="input-unit-jk" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">J</span>
                  </div>
                </div>

                <div>
                  <label for="output-jk" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
                  <div class="flex rounded-md shadow-sm">
                    <input id="output-jk" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
                    <span id="output-unit-jk" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">kWh</span>
                  </div>
                </div>
              </div>

              <button id="swap-jk" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
                Swap direction
              </button>
            </section>

            <section class="prose">
              <h2>Joules and kilowatt-hours: the relationship</h2>
              <p>
                Joule (J) is the SI unit of energy, while kilowatt-hour (kWh) is a practical unit widely used for
                electricity billing and energy metering.
              </p>

              <div class="formula-box">
                <p class="font-semibold mb-2">Core formulas</p>
                <p class="mb-1"><code>1 kWh = 1000 W × 3600 s = 3,600,000 J</code></p>
                <p class="mb-1"><code>kWh = J / 3,600,000</code></p>
                <p class="mb-1"><code>J = kWh × 3,600,000</code></p>
              </div>

              <h3>Example: 500,000 J to kWh</h3>
              <p>
                <code>kWh = 500,000 ÷ 3,600,000 ≈ 0.1389 kWh</code>
              </p>

              <h3>Typical applications</h3>
              <ul>
                <li>Converting simulated or measured energy (in J) to kWh for cost estimates.</li>
                <li>Checking laboratory calorimetry results against electrical energy usage.</li>
                <li>Comparing energy from batteries, solar panels and grid electricity.</li>
              </ul>

              <h2>FAQ</h2>
              <h3>Is this converter exact?</h3>
              <p>
                Yes. It uses the exact relationship 1 kWh = 3.6 × 10<sup>6</sup> J, with floating-point arithmetic.
                Small rounding differences may occur only due to display formatting.
              </p>

              <h3>Can I use it for very small or very large values?</h3>
              <p>
                Yes. Results are formatted in fixed or scientific notation depending on magnitude,
                so you can work from micro-scale Joules up to MWh-scale energies.
              </p>

              <h3>What about watt-hours (Wh)?</h3>
              <p>
                1 kWh = 1000 Wh and 1 Wh = 3600 J. If you prefer, you can mentally convert kWh to Wh and
                then to J, but this calculator handles the entire chain directly.
              </p>
            </section>
          </div>
        </main>

        <aside class="w-full lg:w-1/3">
          <div class="bg-white p-5 rounded-lg shadow-md mb-6 card-hover">
            <h2 class="text-lg font-semibold mb-3">Related energy &amp; power converters</h2>
            <ul class="space-y-2 text-sm">
              <li><a href="https://calcdomain.com/energy-unit-converter" class="text-blue-600 hover:underline">Energy Unit Converter (J, cal, kWh, BTU)</a></li>
              <li><a href="https://calcdomain.com/btu-to-kwh" class="text-blue-600 hover:underline">BTU to kWh Converter</a></li>
              <li><a href="https://calcdomain.com/kwh-to-joules" class="text-blue-600 hover:underline">kWh to Joules Converter</a></li>
              <li><a href="https://calcdomain.com/joules-to-btu" class="text-blue-600 hover:underline">Joules to BTU Converter</a></li>
              <li><a href="https://calcdomain.com/power-unit-converter" class="text-blue-600 hover:underline">Power Unit Converter (watts, HP, BTU/hr)</a></li>
            </ul>
          </div>

          <div class="bg-white p-5 rounded-lg shadow-md card-hover">
            <h2 class="text-lg font-semibold mb-3">Category: Measurement Unit Conversions</h2>
            <p class="text-sm text-gray-600 mb-3">
              Browse more unit converters for power, energy, pressure, temperature and other physical quantities.
            </p>
            <a href="https://calcdomain.com/subcategories/math-conversions-measurement-unit-conversions"
               class="inline-flex items-center px-3 py-2 text-sm font-medium bg-blue-600 text-white rounded-md hover:bg-blue-700">
              Browse all unit converters
            </a>
          </div>
        </aside>
      </div>
    </div>

    <footer class="bg-gray-900 text-white py-12">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 class="text-2xl font-bold mb-4">CalcDomain</h3>
            <p class="text-gray-400 mb-4">Your trusted source for free online calculators. Accurate, fast, and reliable calculations for every need.</p>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-4">Categories</h4>
            <ul class="space-y-2">
              <li><a href="https://calcdomain.com/finance" class="text-gray-400 hover:text-white">Finance</a></li>
              <li><a href="https://calcdomain.com/health-fitness" class="text-gray-400 hover:text-white">Health &amp; Fitness</a></li>
              <li><a href="https://calcdomain.com/math-conversions" class="text-gray-400 hover:text-white">Math &amp; Conversions</a></li>
              <li><a href="https://calcdomain.com/lifestyle-everyday" class="text-gray-400 hover:text-white">Lifestyle &amp; Everyday</a></li>
              <li><a href="https://calcdomain.com/construction-diy" class="text-gray-400 hover:text-white">Construction &amp; DIY</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-4">Popular Tools</h4>
            <ul class="space-y-2">
              <li><a href="https://calcdomain.com/mortgage-payment" class="text-gray-400 hover:text-white">Mortgage Calculator</a></li>
              <li><a href="https://calcdomain.com/percentage-calculator" class="text-gray-400 hover:text-white">Percentage Calculator</a></li>
              <li><a href="https://calcdomain.com/bmi-calculator" class="text-gray-400 hover:text-white">BMI Calculator</a></li>
              <li><a href="https://calcdomain.com/auto-loan-calculator" class="text-gray-400 hover:text-white">Auto Loan Calculator</a></li>
              <li><a href="https://calcdomain.com/house-affordability" class="text-gray-400 hover:text-white">House Affordability</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-4">Support</h4>
            <ul class="space-y-2">
              <li><a href="https://calcdomain.com/about" class="text-gray-400 hover:text-white">About Us</a></li>
              <li><a href="https://calcdomain.com/contact" class="text-gray-400 hover:text-white">Contact</a></li>
              <li><a href="https://calcdomain.com/privacy" class="text-gray-400 hover:text-white">Privacy Policy</a></li>
              <li><a href="https://calcdomain.com/terms" class="text-gray-400 hover:text-white">Terms of Service</a></li>
              <li><a href="https://calcdomain.com/sitemap" class="text-gray-400 hover:text-white">Site Map</a></li>
            </ul>
          </div>
        </div>
        <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 CalcDomain. All Rights Reserved. | Free Online Calculators for Everyone</p>
        </div>
      </div>
    </footer>

    <script src="/assets/js/script_menu.js" defer></script>
    <script src="/assets/js/script_faq.js" defer></script>
    <script src="search.js" defer></script>

    <script>
      window.MathJax = {
        tex: { inlineMath: [['\\(','\\)'], ['$', '$']], displayMath: [['$','$'], ['\\[','\\]']] },
        svg: { fontCache: 'global' }
      };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

    <script>
      (function () {
        const dirEl = document.getElementById('direction-jk');
        const inputEl = document.getElementById('input-jk');
        const outputEl = document.getElementById('output-jk');
        const inUnitEl = document.getElementById('input-unit-jk');
        const outUnitEl = document.getElementById('output-unit-jk');
        const swapBtn = document.getElementById('swap-jk');

        const J_PER_KWH = 3600000;

        function formatNumber(value) {
          if (!isFinite(value)) return '';
          if (Math.abs(value) >= 1000 || Math.abs(value) < 0.001) {
            return value.toExponential(6);
          }
          return value.toFixed(8).replace(/\.?0+$/, '');
        }

        function updateUnits() {
          if (dirEl.value === 'j-to-kwh') {
            inUnitEl.textContent = 'J';
            outUnitEl.textContent = 'kWh';
          } else {
            inUnitEl.textContent = 'kWh';
            outUnitEl.textContent = 'J';
          }
        }

        function convert() {
          const val = parseFloat(inputEl.value);
          if (isNaN(val)) {
            outputEl.value = '';
            return;
          }
          let result;
          if (dirEl.value === 'j-to-kwh') {
            result = val / J_PER_KWH;
          } else {
            result = val * J_PER_KWH;
          }
          outputEl.value = formatNumber(result);
        }

        dirEl.addEventListener('change', () => {
          updateUnits();
          convert();
        });
        inputEl.addEventListener('input', convert);
        swapBtn.addEventListener('click', () => {
          dirEl.value = dirEl.value === 'j-to-kwh' ? 'kwh-to-j' : 'j-to-kwh';
          updateUnits();
          convert();
        });

        updateUnits();
      })();
    </script>
</body>
</html>
EOF

############################################
# 3) PSI to kPa Converter (bidirectional)
############################################
cat > "$OUTPUT_DIR/psi-to-kpa.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>PSI to kPa Converter – Pressure Unit Conversion</title>
    <meta name="description" content="Convert between PSI and kilopascals (kPa) with this precise pressure unit converter. Ideal for tires, hydraulics, pneumatics and industrial applications.">
    <link rel="canonical" href="https://calcdomain.com/psi-to-kpa">

    <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="shortcut icon" href="/favicon.ico" />
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />

    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .card-hover { transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; }
        .card-hover:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
        .prose { max-width: 65ch; margin-left: auto; margin-right: auto; }
        .prose h2 { font-size: 1.5rem; font-weight: 600; margin-top: 2rem; margin-bottom: 1rem; }
        .prose h3 { font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; }
        .prose p { margin-bottom: 1rem; line-height: 1.6; }
        .prose ul, .prose ol { margin-left: 1.5rem; margin-bottom: 1rem; }
        .prose li { margin-bottom: 0.5rem; }
        .formula-box { background: #f3f4f6; border: 1px solid #d1d5db; border-radius: 8px; padding: 1rem; overflow-x: auto; margin: 1rem 0; }
    </style>

    <!-- Google tag (gtag.js) -->
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
    </script>

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "BreadcrumbList",
          "itemListElement": [
            {
              "@type": "ListItem",
              "position": 1,
              "name": "Home",
              "item": "https://calcdomain.com/"
            },
            {
              "@type": "ListItem",
              "position": 2,
              "name": "Math & Conversions",
              "item": "https://calcdomain.com/categories/math-conversions"
            },
            {
              "@type": "ListItem",
              "position": 3,
              "name": "Measurement Unit Conversions",
              "item": "https://calcdomain.com/subcategories/math-conversions-measurement-unit-conversions"
            },
            {
              "@type": "ListItem",
              "position": 4,
              "name": "PSI to kPa Converter",
              "item": "https://calcdomain.com/psi-to-kpa"
            }
          ]
        },
        {
          "@type": "FAQPage",
          "mainEntity": [
            {
              "@type": "Question",
              "name": "How do you convert PSI to kPa?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "To convert PSI to kilopascals, multiply pressure in PSI by 6.894757. kPa = PSI × 6.894757. The calculator uses the precise constant 6.894757293168361 internally."
              }
            },
            {
              "@type": "Question",
              "name": "How do you convert kPa to PSI?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "To convert kPa to PSI, divide pressure in kilopascals by 6.894757. PSI = kPa ÷ 6.894757. This tool switches direction automatically when you change the conversion mode."
              }
            },
            {
              "@type": "Question",
              "name": "What are typical PSI and kPa values for car tires?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Passenger car tires are commonly specified between about 30 and 35 PSI, which corresponds roughly to 207–241 kPa. Always use the manufacturer\u2019s recommended pressure printed on the tire or vehicle door label."
              }
            }
          ]
        }
      ]
    }
    </script>
</head>
<body class="bg-gray-50 text-gray-800">

    <script async src="https://pagead2.googlesyndication.com/pagead/js?client=ca-pub-9476637732224939"
         crossorigin="anonymous"></script>

    <header class="bg-white shadow-sm sticky top-0 z-50">
      <nav class="container mx-auto px-4 lg:px-6 py-4" aria-label="Primary">
        <div class="flex justify-between items-center">
          <a href="https://calcdomain.com" class="text-2xl font-bold text-blue-600">CalcDomain</a>
          <div class="w-full max-w-md hidden md:block mx-8">
            <div class="relative">
              <input type="search" id="search-input" placeholder="Search for a calculator..." class="w-full py-2 px-4 pr-10 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" autocomplete="off" />
              <svg class="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
              <div id="search-results" class="absolute top-full left-0 right-0 bg-white shadow-lg rounded-lg mt-2 max-h-96 overflow-y-auto z-50 hidden border border-gray-200"></div>
            </div>
          </div>
          <div class="hidden md:flex items-center space-x-6">
            <a href="https://calcdomain.com/search" class="text-gray-700 hover:text-blue-600 transition-colors">Advanced Search</a>
            <a href="https://calcdomain.com/categories" class="text-gray-700 hover:text-blue-600 transition-colors">Categories</a>
          </div>
          <button id="mobile-menu-toggle" class="md:hidden p-2" aria-controls="mobile-menu" aria-expanded="false" aria-label="Open menu" type="button">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </button>
        </div>
        <nav id="mobile-menu" class="md:hidden mt-4 hidden" aria-label="Mobile menu" role="navigation">
          <div class="mb-4">
            <div class="relative">
              <input type="search" id="mobile-search-input" placeholder="Search calculators..." class="w-full py-3 px-4 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
              <svg class="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
          </div>
          <div class="space-y-2">
            <a href="https://calcdomain.com/search" class="block py-2 text-gray-700 hover:text-blue-600">Advanced Search</a>
            <a href="https://calcdomain.com/categories" class="block py-2 text-gray-700 hover:text-blue-600">Categories</a>
          </div>
        </nav>
      </nav>
    </header>

    <div class="container mx-auto px-4 py-8">
      <nav id="breadcrumb-container" class="text-sm mb-4 text-gray-600" aria-label="Breadcrumb">
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
            PSI to kPa Converter
          </li>
        </ol>
      </nav>

      <div class="flex flex-col lg:flex-row gap-8">
        <main class="w-full lg:w-2/3">
          <div class="bg-white p-6 rounded-lg shadow-md">
            <header class="mb-6">
              <h1 class="text-2xl md:text-3xl font-bold mb-2">PSI to kPa Converter</h1>
              <p class="text-gray-600">Convert pressure between pounds per square inch (PSI) and kilopascals (kPa) for tires, hydraulics and industrial systems.</p>
            </header>

            <section aria-labelledby="converter-heading" class="mb-8">
              <h2 id="converter-heading" class="text-xl font-semibold mb-4">Pressure converter – PSI &lt;&rarr; kPa</h2>

              <div class="grid gap-4 md:grid-cols-2 mb-4">
                <div>
                  <label for="direction-pk" class="block text-sm font-medium text-gray-700 mb-1">Conversion direction</label>
                  <select id="direction-pk" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="psi-to-kpa">PSI → kPa</option>
                    <option value="kpa-to-psi">kPa → PSI</option>
                  </select>
                </div>
                <div>
                  <p class="text-xs text-gray-500 mt-6">
                    Exact constant: <code>1 PSI = 6.894757293168361 kPa</code>.
                  </p>
                </div>
              </div>

              <div class="grid gap-4 md:grid-cols-2 items-end mb-4">
                <div>
                  <label for="input-pk" class="block text-sm font-medium text-gray-700 mb-1">Input value</label>
                  <div class="flex rounded-md shadow-sm">
                    <input id="input-pk" type="number" step="any" class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Enter value">
                    <span id="input-unit-pk" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">PSI</span>
                  </div>
                </div>

                <div>
                  <label for="output-pk" class="block text-sm font-medium text-gray-700 mb-1">Result</label>
                  <div class="flex rounded-md shadow-sm">
                    <input id="output-pk" type="text" readonly class="flex-1 border border-gray-300 rounded-l-md px-3 py-2 bg-gray-100 text-gray-800" placeholder="0.00">
                    <span id="output-unit-pk" class="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 bg-gray-50 text-gray-700 text-sm">kPa</span>
                  </div>
                </div>
              </div>

              <button id="swap-pk" type="button" class="inline-flex items-center px-3 py-2 text-sm font-medium border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50">
                Swap direction
              </button>
            </section>

            <section class="prose">
              <h2>From PSI to kPa: the formula</h2>
              <p>
                PSI (pounds per square inch) is common in the US and in automotive contexts, while kilopascal (kPa)
                is an SI-derived unit used in engineering and on many technical datasheets.
              </p>

              <div class="formula-box">
                <p class="font-semibold mb-2">Core formulas</p>
                <p class="mb-1"><code>1 PSI = 6.894757293168361 kPa</code></p>
                <p class="mb-1"><code>kPa = PSI × 6.894757293168361</code></p>
                <p class="mb-1"><code>PSI = kPa ÷ 6.894757293168361</code></p>
              </div>

              <h3>Example: 32 PSI to kPa (car tire)</h3>
              <p><code>kPa = 32 × 6.894757 ≈ 220.6 kPa</code></p>

              <h3>Typical applications</h3>
              <ul>
                <li>Converting tire pressure between PSI and kPa.</li>
                <li>Interpreting hydraulic and pneumatic specifications in different unit systems.</li>
                <li>Converting legacy documentation (PSI) to SI-based units used in calculations.</li>
              </ul>

              <h2>FAQ</h2>
              <h3>Is 1 bar the same as 100 kPa?</h3>
              <p>
                1 bar is defined as exactly 100 kPa. For rough comparisons: 1 bar ≈ 14.5038 PSI.
              </p>

              <h3>Can I use this for gauge and absolute pressure?</h3>
              <p>
                Yes. The converter operates on numerical values only. Whether a reading is gauge or absolute
                depends on your measurement reference, not on the unit itself.
              </p>

              <h3>What precision does the calculator use?</h3>
              <p>
                Internally it uses the full constant 6.894757293168361. Results are displayed with a reasonable
                number of decimal places or in scientific notation for very large or small values.
              </p>
            </section>
          </div>
        </main>

        <aside class="w-full lg:w-1/3">
          <div class="bg-white p-5 rounded-lg shadow-md mb-6 card-hover">
            <h2 class="text-lg font-semibold mb-3">Related pressure converters</h2>
            <ul class="space-y-2 text-sm">
              <li><a href="https://calcdomain.com/pressure-unit-converter" class="text-blue-600 hover:underline">Pressure Unit Converter (Pa, bar, atm, psi)</a></li>
              <li><a href="https://calcdomain.com/psi-to-pascals" class="text-blue-600 hover:underline">PSI to Pascals Converter</a></li>
              <li><a href="https://calcdomain.com/pascals-to-psi" class="text-blue-600 hover:underline">Pascals to PSI Converter</a></li>
              <li><a href="https://calcdomain.com/bar-to-psi" class="text-blue-600 hover:underline">Bar to PSI Converter</a></li>
              <li><a href="https://calcdomain.com/atm-to-psi" class="text-blue-600 hover:underline">Atmospheres to PSI Converter</a></li>
            </ul>
          </div>

          <div class="bg-white p-5 rounded-lg shadow-md card-hover">
            <h2 class="text-lg font-semibold mb-3">Category: Measurement Unit Conversions</h2>
            <p class="text-sm text-gray-600 mb-3">
              Discover more unit converters for pressure, flow, density and other process engineering variables.
            </p>
            <a href="https://calcdomain.com/subcategories/math-conversions-measurement-unit-conversions"
               class="inline-flex items-center px-3 py-2 text-sm font-medium bg-blue-600 text-white rounded-md hover:bg-blue-700">
              Browse all unit converters
            </a>
          </div>
        </aside>
      </div>
    </div>

    <footer class="bg-gray-900 text-white py-12">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 class="text-2xl font-bold mb-4">CalcDomain</h3>
            <p class="text-gray-400 mb-4">Your trusted source for free online calculators. Accurate, fast, and reliable calculations for every need.</p>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-4">Categories</h4>
            <ul class="space-y-2">
              <li><a href="https://calcdomain.com/finance" class="text-gray-400 hover:text-white">Finance</a></li>
              <li><a href="https://calcdomain.com/health-fitness" class="text-gray-400 hover:text-white">Health &amp; Fitness</a></li>
              <li><a href="https://calcdomain.com/math-conversions" class="text-gray-400 hover:text-white">Math &amp; Conversions</a></li>
              <li><a href="https://calcdomain.com/lifestyle-everyday" class="text-gray-400 hover:text-white">Lifestyle &amp; Everyday</a></li>
              <li><a href="https://calcdomain.com/construction-diy" class="text-gray-400 hover:text-white">Construction &amp; DIY</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-4">Popular Tools</h4>
            <ul class="space-y-2">
              <li><a href="https://calcdomain.com/mortgage-payment" class="text-gray-400 hover:text-white">Mortgage Calculator</a></li>
              <li><a href="https://calcdomain.com/percentage-calculator" class="text-gray-400 hover:text-white">Percentage Calculator</a></li>
              <li><a href="https://calcdomain.com/bmi-calculator" class="text-gray-400 hover:text-white">BMI Calculator</a></li>
              <li><a href="https://calcdomain.com/auto-loan-calculator" class="text-gray-400 hover:text-white">Auto Loan Calculator</a></li>
              <li><a href="https://calcdomain.com/house-affordability" class="text-gray-400 hover:text-white">House Affordability</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-lg font-semibold mb-4">Support</h4>
            <ul class="space-y-2">
              <li><a href="https://calcdomain.com/about" class="text-gray-400 hover:text-white">About Us</a></li>
              <li><a href="https://calcdomain.com/contact" class="text-gray-400 hover:text-white">Contact</a></li>
              <li><a href="https://calcdomain.com/privacy" class="text-gray-400 hover:text-white">Privacy Policy</a></li>
              <li><a href="https://calcdomain.com/terms" class="text-gray-400 hover:text-white">Terms of Service</a></li>
              <li><a href="https://calcdomain.com/sitemap" class="text-gray-400 hover:text-white">Site Map</a></li>
            </ul>
          </div>
        </div>
        <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 CalcDomain. All Rights Reserved. | Free Online Calculators for Everyone</p>
        </div>
      </div>
    </footer>

    <script src="/assets/js/script_menu.js" defer></script>
    <script src="/assets/js/script_faq.js" defer></script>
    <script src="search.js" defer></script>

    <script>
      window.MathJax = {
        tex: { inlineMath: [['\\(','\\)'], ['$', '$']], displayMath: [['$','$'], ['\\[','\\]']] },
        svg: { fontCache: 'global' }
      };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>

    <script>
      (function () {
        const dirEl = document.getElementById('direction-pk');
        const inputEl = document.getElementById('input-pk');
        const outputEl = document.getElementById('output-pk');
        const inUnitEl = document.getElementById('input-unit-pk');
        const outUnitEl = document.getElementById('output-unit-pk');
        const swapBtn = document.getElementById('swap-pk');

        const KPA_PER_PSI = 6.894757293168361;

        function formatNumber(value) {
          if (!isFinite(value)) return '';
          if (Math.abs(value) >= 1000 || Math.abs(value) < 0.001) {
            return value.toExponential(6);
          }
          return value.toFixed(6).replace(/\.?0+$/, '');
        }

        function updateUnits() {
          if (dirEl.value === 'psi-to-kpa') {
            inUnitEl.textContent = 'PSI';
            outUnitEl.textContent = 'kPa';
          } else {
            inUnitEl.textContent = 'kPa';
            outUnitEl.textContent = 'PSI';
          }
        }

        function convert() {
          const val = parseFloat(inputEl.value);
          if (isNaN(val)) {
            outputEl.value = '';
            return;
          }
          let result;
          if (dirEl.value === 'psi-to-kpa') {
            result = val * KPA_PER_PSI;
          } else {
            result = val / KPA_PER_PSI;
          }
          outputEl.value = formatNumber(result);
        }

        dirEl.addEventListener('change', () => {
          updateUnits();
          convert();
        });
        inputEl.addEventListener('input', convert);
        swapBtn.addEventListener('click', () => {
          dirEl.value = dirEl.value === 'psi-to-kpa' ? 'kpa-to-psi' : 'psi-to-kpa';
          updateUnits();
          convert();
        });

        updateUnits();
      })();
    </script>
</body>
</html>
EOF

echo "Done. Created:"
echo " - $OUTPUT_DIR/kw-to-hp-converter.html"
echo " - $OUTPUT_DIR/joules-to-kwh.html"
echo " - $OUTPUT_DIR/psi-to-kpa.html"
EOF`

---

Se vuoi, nel prossimo step possiamo:

- aggiungere altri converter della mappa gap nello stesso `.sh`  
- oppure creare una versione che scrive i file direttamente nella struttura reale del progetto (es. `/public` o root Vercel).
::contentReference[oaicite:1]{index=1}
