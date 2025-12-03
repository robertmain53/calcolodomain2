import os
import time
import csv
import re

from openai import OpenAI

# ===========================
# CONFIGURAZIONE DI BASE
# ===========================

OPENAI_MODEL = "gpt-5.1"          # modello "top" stile chat
SLEEP_SECONDS = 60                # pausa tra una riga e la successiva
CSV_PATH = "calc.csv"             # file con le richieste
CSV_COLUMN_INDEX = 15             # COLONNA 16 (indice 0-based)
SITEMAP_JSON_PATH = "sitemap_data_FINAL_flat.json"
OUTPUT_DIR = "sito_modificato"

SYSTEM_PROMPT = """
You are ChatGPT, the same assistant the user normally uses on chat.openai.com.

Your role in this workflow is:
- Act as an elite product strategist, UX engineer, SEO specialist and HTML/JS developer for Calcdomain.
- Fully follow and respect the “Fabbrica di Calcolatori v6” manual and assets provided in the user macro-prompt.
- Always answer in the same style as the ChatGPT web UI: concise but thorough, no meta-comments about the API or internal parameters.

General rules:
- If the user prompt is a “RICHIESTA DI CREAZIONE NUOVO CALCOLATORE”, you must return ONE complete, production-ready HTML file for CalcDomain, based on template_master_INTERNA.html.
- Return the HTML wrapped in a single ```html code block, with nothing else before or after.
- The HTML MUST include a single <link rel="canonical" href="https://calcdomain.com/..."> tag with the final flat URL (no trailing slash).
- Respect all placeholder replacement rules described in the macro-prompt (%%BODY_SCRIPTS_INIZIO%%, %%HEAD_SCRIPTS_E_META%%, breadcrumbs, sidebar, JSON-LD, etc.).
- When you need category / subcategory / related calculators, use ONLY the data from sitemap_data_FINAL_flat.json that the user has provided in the macro-prompt.
- Avoid mentioning that you are an AI model or that this is an automated pipeline.
- Prefer English for on-page copy unless the request clearly requires another language.
""".strip()


# === MACRO-PROMPT DI FABBRICA (USER) ===
# Verrà arricchito con il contenuto di sitemap_data_FINAL_flat.json a runtime.

BASE_MACRO_PROMPT = r"""
Read: sitemap_data_FINAL_flat.json

## Message:

### MANUALE DI ISTRUZIONI: Fabbrica di Calcolatori v6

Ho un compito molto specifico e a lungo termine per te. Stiamo per costruire un intero sito di calcolatori, una pagina alla volta.

Il nostro obiettivo è creare file HTML perfetti, validi al 100% e ottimizzati per la SEO, basati su un sistema di template che ti fornirò.

Il tuo compito è agire come la mia "Fabbrica di Assemblaggio". Io ti fornirò un "brief di prodotto" e tu lo assemblerai usando i 3 "Asset" che ti sto dando ora.

Ecco i 3 ASSET FONDAMENTALI per questo progetto:

**ASSET 1: Il Guscio Template (Pagine Interne)**

In allegato trovi il `template_master_INTERNA.html`. Useremo questo per OGNI pagina di calcolatore. Nota i segnaposto `%%NOME_SEGNAPOSTO%%`.

'''

<!DOCTYPE html> <html lang="%%LANGUAGE%%"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%%TITOLO_PAGINA%%</title>
<meta name="description" content="%%DESCRIZIONE_PAGINA%%">
<link rel="canonical" href="%%URL_CANONICO%%">

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

%%HEAD_SCRIPTS_E_META%%

<script type="application/ld+json">
  %%SCHEMA_JSON_LD_QUI%%
</script>
</head> 
<body class="bg-gray-50 text-gray-800">
%%BODY_SCRIPTS_INIZIO%%

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
  <nav id="breadcrumb-container" class="text-sm mb-4 text-gray-600">
    %%BREADCRUMB_HTML_QUI%%
  </nav>
  <div class="flex flex-col lg:flex-row gap-8">
    <main class="w-full lg:w-2/3">
      <div class="bg-white p-6 rounded-lg shadow-md">
        %%CONTENUTO_PRINCIPALE_QUI%%
      </div>
    </main>
    <aside class="w-full lg:w-1/3">
      %%SIDEBAR_HTML_QUI%%
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
          <li><a href="https://calcdomain.com/health-fitness" class="text-gray-400 hover:text-white">Health & Fitness</a></li>
          <li><a href="https://calcdomain.com/math-conversions" class="text-gray-400 hover:text-white">Math & Conversions</a></li>
          <li><a href="https://calcdomain.com/lifestyle-everyday" class="text-gray-400 hover:text-white">Lifestyle & Everyday</a></li>
          <li><a href="https://calcdomain.com/construction-diy" class="text-gray-400 hover:text-white">Construction & DIY</a></li>
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
</body> </html>

'''

ASSET 2: Il Guscio Template (Homepage) Questo è il template_master_HOMEPAGE.html. Lo useremo SOLO per la pagina index.html.
HTML

'''

<!DOCTYPE html> <html lang="%%LANGUAGE%%"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%%TITOLO_PAGINA%%</title>
<meta name="description" content="%%DESCRIZIONE_PAGINA%%">
<link rel="canonical" href="%%URL_CANONICO%%">

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
    .hero-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
</style>

%%HEAD_SCRIPTS_E_META%%

<script type="application/ld+json">
  %%SCHEMA_JSON_LD_QUI%%
</script>

</head> <body class="bg-gray-50 text-gray-800">
%%BODY_SCRIPTS_INIZIO%%

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

%%CONTENUTO_PRINCIPALE_QUI%%

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
          <li><a href="https://calcdomain.com/health-fitness" class="text-gray-400 hover:text-white">Health & Fitness</a></li>
          <li><a href="https://calcdomain.com/math-conversions" class="text-gray-400 hover:text-white">Math & Conversions</a></li>
          <li><a href="https://calcdomain.com/lifestyle-everyday" class="text-gray-400 hover:text-white">Lifestyle & Everyday</a></li>
          <li><a href="https://calcdomain.com/construction-diy" class="text-gray-400 hover:text-white">Construction & DIY</a></li>
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

</body> </html> 

'''

ASSET 3: Il "Cervello" del Sito (Sitemap JSON)

Il file sitemap_data_FINAL_flat.json . Contiene la struttura di navigazione, le categorie e le sottocategorie di TUTTE le pagine. Lo userai per generare dinamicamente le BREADCRUMB e la SIDEBAR.

IL NOSTRO FLUSSO DI LAVORO (I TUOI COMPITI)

Da ora in poi, io ti invierò una richiesta usando questo formato:

*** RICHIESTA DI CREAZIONE NUOVO CALCOLATORE ***

Target (URL Piatto): /nome-pagina

Parola Chiave Principale: Nome Calcolatore

Obiettivo: ...

Concorrenti: [lista]

Quando ricevi questa richiesta, il tuo compito è:

Analizzare i Concorrenti: Analizza i link forniti per capire l'intento dell'utente e le "killer features".
Progettare uno Strumento Superiore: Scrivi il codice HTML e JavaScript per un calcolatore che sia migliore dei concorrenti (es. bidirezionale, multi-unità, ecc.).
Scrivere Contenuto E-E-A-T: Scrivi contenuto originale, autorevole e utile (spiegazione formule, tabelle, FAQ) per battere i concorrenti.
Trovare i Metadati: Cerca il "Target URL" (es. /nome-pagina) dentro l'ASSET 3 (il JSON) per trovare la sua Categoria e Sottocategoria.
Assemblare il File:

Prendi l'ASSET 1 (template_master_INTERNA.html).
Sostituisci %%TITOLO_PAGINA%% e %%DESCRIZIONE_PAGINA%% con il nuovo titolo e la meta description che hai scritto.
Sostituisci %%URL_CANONICO%% con l'URL completo (es. https://calcdomain.com/nome-pagina).
Sostituisci %%CONTENUTO_PRINCIPALE_QUI%% con il codice del Calcolatore (Punto 2) e il Contenuto (Punto 3).
Sostituisci %%BREADCRUMB_HTML_QUI%% usando i dati del Punto 4.
Sostituisci %%SIDEBAR_HTML_QUI%% generando i link "Related" basati sulla Categoria/Sottocategoria del Punto 4.
Sostituisci %%SCHEMA_JSON_LD_QUI%% con gli schemi Breadcrumb, FAQPage, e HowTo (se pertinenti).
Lascia i segnaposto per gli script (%%HEAD_SCRIPTS...%%) così come sono.

Per i prossimi calcolatori ricorda che:

%%BODY_SCRIPTS_INIZIO%% =

'''
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9476637732224939" crossorigin="anonymous"></script>
'''

%%HEAD_SCRIPTS_E_META%% =

'''
<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-7MB5V1LZRN"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-7MB5V1LZRN'); </script> <meta name="google-site-verification" content="_tiTZ9ivAdtXcAS9CMnTNJ549Sg39WVqP_ZFbWgglNA" /> <script src="https://cmp.gatekeeperconsent.com/min.js" data-cfasync="false"></script> <script src="https://the.gatekeeperconsent.com/cmp.min.js" data-cfasync="false"></script> <script async src="//www.ezojs.com/ezoic/sa.min.js"></script> <script> window.ezstandalone = window.ezstandalone || {}; ezstandalone.cmd = ezstandalone.cmd || []; </script>
'''

""".strip()


# ===========================
# FUNZIONI DI SUPPORTO
# ===========================

def build_macro_prompt_with_sitemap() -> str:
    """
    Legge il contenuto di sitemap_data_FINAL_flat.json e lo aggiunge al macro-prompt,
    così il modello può realmente usarlo.
    """
    if not os.path.exists(SITEMAP_JSON_PATH):
        raise FileNotFoundError(f"File sitemap non trovato: {SITEMAP_JSON_PATH}")

    with open(SITEMAP_JSON_PATH, "r", encoding="utf-8") as f:
        sitemap_content = f.read()

    macro = BASE_MACRO_PROMPT + "\n\n\n=== FULL CONTENT OF sitemap_data_FINAL_flat.json ===\n```json\n"
    macro += sitemap_content
    macro += "\n```\n=== END OF sitemap_data_FINAL_flat.json ===\n"
    return macro


def extract_html_from_response(content: str) -> str:
    """
    Estrae il blocco ```html ... ``` dalla risposta dell'API.
    Se non trova il blocco, restituisce il contenuto intero.
    """
    code_block_match = re.search(r"```html(.*?)```", content, re.DOTALL | re.IGNORECASE)
    if code_block_match:
        return code_block_match.group(1).strip()
    return content.strip()


def extract_slug_from_html(html: str) -> str:
    """
    Trova il valore di canonical:
    <link rel="canonical" href="https://calcdomain.com/QUALCOSA">
    e ritorna "QUALCOSA" (senza slash iniziale/finale).
    """
    m = re.search(
        r'<link\s+rel="canonical"\s+href="https://calcdomain\.com/([^"]+)"',
        html,
        re.IGNORECASE
    )
    if not m:
        raise ValueError("Impossibile trovare il canonical con dominio calcdomain.com nella risposta HTML.")
    slug = m.group(1).strip()
    slug = slug.strip("/")
    if not slug:
        raise ValueError("Slug vuoto estratto dal canonical.")
    return slug


def send_request(client: OpenAI, macro_prompt: str, row_prompt: str) -> str:
    """
    Invia al modello:
    - system prompt (clone chat)
    - macro prompt (Fabbrica v6 + sitemap)
    - prompt di riga (*** RICHIESTA... dal CSV)
    e ritorna il contenuto della risposta.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": macro_prompt},
        {"role": "user", "content": row_prompt},
    ]

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.3,
    )
    return response.choices[0].message.content


def process_csv_from_row(start_row: int):
    """
    Legge calc.csv, parte dalla riga start_row (1-based),
    prende la colonna 16 per ogni riga, la invia all'API e salva il file HTML.
    Si ferma alla prima riga in cui la colonna 16 è vuota.
    """
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"File CSV non trovato: {CSV_PATH}")

    # Setup OpenAI client
    client = OpenAI()

    # Costruisco una sola volta il macro-prompt con dentro il JSON della sitemap
    macro_prompt = build_macro_prompt_with_sitemap()

    # Leggo il CSV
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    total_rows = len(reader)
    if start_row < 1 or start_row > total_rows:
        raise ValueError(f"start_row fuori range. Il file ha {total_rows} righe.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Totale righe nel CSV: {total_rows}")
    print(f"Inizio dalla riga {start_row} (1-based).")
    print("Premi CTRL+C per interrompere.\n")

    for idx in range(start_row - 1, total_rows):
        row_number = idx + 1  # 1-based per output umano
        row = reader[idx]

        # Gestione lunghezza riga
        if len(row) <= CSV_COLUMN_INDEX:
            print(f"[Riga {row_number}] Colonna 16 mancante. Interrompo.")
            break

        cell_value = (row[CSV_COLUMN_INDEX] or "").strip()
        if not cell_value:
            print(f"[Riga {row_number}] Colonna 16 vuota. Interrompo.")
            break

        print(f"=== Riga {row_number} ===")
        print("Invio a ChatGPT il seguente prompt (colonna 16):")
        print(cell_value[:500] + ("..." if len(cell_value) > 500 else ""))
        print()

        try:
            raw_response = send_request(client, macro_prompt, cell_value)
            html = extract_html_from_response(raw_response)
            slug = extract_slug_from_html(html)
            filename = f"{slug}.html"
            filepath = os.path.join(OUTPUT_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as out_f:
                out_f.write(html)

            print(f"File salvato: {filepath}")
        except Exception as e:
            print(f"ERRORE alla riga {row_number}: {e}")
            print("Proseguo con la riga successiva.\n")
            continue

        print(f"Attendo {SLEEP_SECONDS} secondi prima di passare alla riga successiva...\n")
        try:
            time.sleep(SLEEP_SECONDS)
        except KeyboardInterrupt:
            print("\nInterrotto dall'utente durante l'attesa. Stop.")
            break


def main():
    print("=== Calcdomain Factory Runner (API) ===")
    print(f"CSV: {CSV_PATH} | Sitemap JSON: {SITEMAP_JSON_PATH} | Output dir: {OUTPUT_DIR}")
    print("Assicurati di avere OPENAI_API_KEY impostata nelle variabili d'ambiente.\n")

    start_row_str = input("Inserisci il numero di riga di partenza (1 = prima riga del file): ").strip()
    try:
        start_row = int(start_row_str)
    except ValueError:
        print("Valore non valido. Devi inserire un numero intero.")
        return

    try:
        process_csv_from_row(start_row)
    except KeyboardInterrupt:
        print("\nInterrotto dall'utente.")
    except Exception as e:
        print(f"Errore fatale: {e}")


if __name__ == "__main__":
    main()
