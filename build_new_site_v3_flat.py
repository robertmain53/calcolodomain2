import os
import glob
import codecs
import json
import re
from bs4 import BeautifulSoup

print("AVVIO SCRIPT DI RICOSTRUZIONE TOTALE DA ZERO (v5 - Flat Architecture)")

# --- 1. CONFIGURAZIONE GLOBALE ---



SCRIPT_GA_GSC_EZOIC_CMP_HEAD = """

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
"""

# ⚠️ INCOLLA QUI I TUOI SCRIPT PER BODY (es. Adsense)
SCRIPT_ADSENSE_BODY = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9476637732224939"
     crossorigin="anonymous"></script>
"""


# ⚠️ LISTA DI FILE DA NON TOCCARE
# Aggiungi qui altri file (es. 'privacy.html', 'contact.html')
IGNORE_LIST = [
    'search.html',
    'seach.html', # Corregge il typo
    'privacy.html', 
    'contact.html', 
    'about.html', 
    'terms.html', 
    'sitemap.html',
    'template-home.html',
    'template-calc.html',
    'test-search.html',
    'googlec8c0eedfe44345b9.html'
]

# Percorsi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "template_perfetti")
SITO_MODIFICATO_DIR = os.path.join(BASE_DIR, "sito_modificato")

# Usa i nuovi nomi di file FLAT
SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap_data_FINAL_flat.json")
CONTENT_FILE = os.path.join(BASE_DIR, "content_data_flat.json")

TEMPLATE_INTERNA_FILE = os.path.join(TEMPLATE_DIR, "template_master_INTERNA.html")
TEMPLATE_HOMEPAGE_FILE = os.path.join(TEMPLATE_DIR, "template_master_HOMEPAGE.html")

os.makedirs(SITO_MODIFICATO_DIR, exist_ok=True)

# --- 2. FUNZIONI HELPER ---

def load_data_files():
    """Carica tutti i nostri file di dati in memoria."""
    try:
        with codecs.open(TEMPLATE_INTERNA_FILE, 'r', 'utf-8') as f:
            template_interna = f.read()
            
        with codecs.open(TEMPLATE_HOMEPAGE_FILE, 'r', 'utf-8') as f:
            template_homepage = f.read()
            
        with codecs.open(SITEMAP_FILE, 'r', 'utf-8') as f:
            sitemap_data = json.load(f)
            
        with codecs.open(CONTENT_FILE, 'r', 'utf-8') as f:
            content_data = json.load(f)
            
        print("Tutti i file (Template, Sitemap, Contenuto) caricati in memoria.")
        return template_interna, template_homepage, sitemap_data, content_data
        
    except FileNotFoundError as e:
        print(f"ERRORE CRITICO: File di dati mancante. {e}")
        print("Assicurati di avere:")
        print("1. 'template_master_INTERNA.html' e 'template_master_HOMEPAGE.html' in 'template_perfetti/'")
        print("2. 'sitemap_data_FINAL_flat.json' (da enrich_sitemap)")
        print("3. 'content_data_flat.json' (da extract_content)")
        return None, None, None, None

def get_page_category_info(url_path, sitemap_data):
    """Cerca nella sitemap_data e restituisce (cat, subcat, title) per un URL."""
    for category, subcategories in sitemap_data.items():
        for subcategory, pages in subcategories.items():
            for page in pages:
                if page['url'] == url_path:
                    return category, subcategory, page['title']
    return None, None, None # Non trovato

def generate_sidebar_html(category, subcategory, sitemap_data):
    """Genera l'HTML della sidebar, dinamicamente."""
    links_html = ""
    list_title = "Popular Calculators" # Default
    
    if category and subcategory and \
       category in sitemap_data and \
       subcategory in sitemap_data[category]:
        
        related_links = sitemap_data[category][subcategory]
        list_title = "Related Calculators"
    else:
        # Fallback (usa le prime 10 pagine di Finanza)
        try:
            related_links = sitemap_data["Finance"]["Generale"][:10]
        except Exception:
             related_links = [
                {"title": "Mortgage", "url": "/mortgage-payment"},
                {"title": "Percentage", "url": "/percentage-calculator"}
            ]

    for link in related_links[:10]:
        links_html += f'<li><a href="https://calcdomain.com{link["url"]}" class="text-blue-600 hover:underline">{link["title"]}</a></li>'
        
    return f"""
    <div class="sticky top-24 space-y-8">
      <div id="sidebar-ad-placeholder-top"></div>
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h3 class="font-bold text-lg mb-4">{list_title}</h3>
        <ul class="space-y-3">
          {links_html}
        </ul>
      </div>
    </div>
    """

def generate_breadcrumb_data(category, subcategory, page_title):
    """Genera sia l'HTML che lo Schema JSON per le breadcrumb."""
    
    html = '<a href="https://calcdomain.com" class="hover:text-blue-600">Home</a>'
    
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://calcdomain.com"}
        ]
    }
    
    if category:
        cat_slug = category.lower().replace(' & ', '-').replace(' ', '-')
        html += f' &raquo; <a href="https://calcdomain.com/{cat_slug}" class="hover:text-blue-600">{category}</a>'
        schema["itemListElement"].append(
            {"@type": "ListItem", "position": 2, "name": category, "item": f"https://calcdomain.com/{cat_slug}"}
        )
        
    if subcategory and subcategory != "Generale":
        sub_slug = subcategory.lower().replace(' & ', '-').replace(' ', '-')
        html += f' &raquo; <a href="https://calcdomain.com/{sub_slug}" class="hover:text-blue-600">{subcategory}</a>'
        schema["itemListElement"].append(
            {"@type": "ListItem", "position": 3, "name": subcategory, "item": f"https://calcdomain.com/{sub_slug}"}
        )
    html += f' &raquo; <span>{page_title}</span>'
    return html, schema # Ritorna l'oggetto Schema, non una stringa

def generate_other_schemas():
    """Genera schemi JSON-LD statici (Organization, WebSite)."""
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "CalcDomain", "url": "https://calcdomain.com", "logo": "https://calcdomain.com/apple-touch-icon.png"}
    web = {"@context": "https://schema.org", "@type": "WebSite", "name": "CalcDomain", "url": "https://calcdomain.com", "potentialAction": {"@type": "SearchAction", "target": "https://calcdomain.com/search?q={search_term_string}", "query-input": "required name=search_term_string"}}
    return org, web

# --- 3. ESECUZIONE PRINCIPALE (LA FABBRICA v5) ---
def main():
    template_interna, template_homepage, sitemap_data, content_data = load_data_files()
    if not template_interna:
        return

    print(f"Inizio costruzione di {len(content_data)} pagine...")
    
    org_schema, web_schema = generate_other_schemas()
    files_costruiti = 0
    files_saltati = 0
    files_con_errori = 0

    # Itera sul DATABASE DI CONTENUTO
    for url_path, content in content_data.items():
        
        try:
            # --- LOGICA DI RICOSTRUZIONE URL PIATTA ---
            if url_path == "/":
                relative_path = "index.html"
            else:
                file_name = url_path[1:] + ".html"
                relative_path = file_name 
            
            # --- LOGICA IGNORE LIST CORRETTA ---
            if relative_path in IGNORE_LIST:
                print(f"  > [IGNORA] File '{relative_path}' è nella ignore list. Saltato.")
                files_saltati += 1
                continue
            
            # --- LOGICA HOMEPAGE CORRETTA ---
            if relative_path == 'index.html':
                current_template = template_homepage
            else:
                current_template = template_interna

            print(f"Costruendo: {relative_path}...")
            
            category, subcategory, _ = get_page_category_info(url_path, sitemap_data)
            page_title = content['title']
            
            output_html = current_template
            
            # Sostituisci i segnaposto
            output_html = output_html.replace("%%LANGUAGE%%", content['lang'])
            output_html = output_html.replace("%%TITOLO_PAGINA%%", page_title)
            output_html = output_html.replace("%%DESCRIZIONE_PAGINA%%", content['description'])
            output_html = output_html.replace("%%URL_CANONICO%%", f"https://calcdomain.com{url_path}")
            
            output_html = output_html.replace("%%HEAD_SCRIPTS_E_META%%", SCRIPT_GA_GSC_EZOIC_CMP_HEAD)
            
            # --- CORREZIONE TYPO ---
            output_html = output_html.replace("%%BODY_SCRIPTS_INIZIO%%", SCRIPT_ADSENSE_BODY)
            
            output_html = output_html.replace("%%CONTENUTO_PRINCIPALE_QUI%%", content['main_html'])
            
            sidebar_html = generate_sidebar_html(category, subcategory, sitemap_data)
            breadcrumb_html, breadcrumb_schema = generate_breadcrumb_data(category, subcategory, page_title)
            
            output_html = output_html.replace("%%SIDEBAR_HTML_QUI%%", sidebar_html)
            output_html = output_html.replace("%%BREADCRUMB_HTML_QUI%%", breadcrumb_html)
            
            # --- NUOVA LOGICA: Combina tutti gli schemi ---
            all_schemas = [breadcrumb_schema, org_schema, web_schema]
            if content.get('old_schemas'):
                all_schemas.extend(content['old_schemas'])
                
            output_html = output_html.replace("%%SCHEMA_JSON_LD_QUI%%", json.dumps(all_schemas, indent=2))
            
            # Salva il file finale nella root di 'sito_modificato'
            output_path = os.path.join(SITO_MODIFICATO_DIR, relative_path)
            
            # Assicura che la sottocartella esista (anche se ora è piatta)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with codecs.open(output_path, 'w', 'utf-8') as f_out:
                f_out.write(output_html) 
                
            files_costruiti += 1

        except Exception as e:
            print(f"--- ERRORE CRITICO DURANTE LA COSTRUZIONE di {relative_path}: {e}")
            files_con_errori += 1
            
    print("\n--- RICOSTRUZIONE (v5 - Flat) COMPLETATA ---")
    print(f"File totali costruiti: {files_costruiti}")
    print(f"File saltati (lista ignorati): {files_saltati}")
    print(f"File falliti (errori script): {files_con_errori}")
    print(f"La nuova versione del sito si trova in: {SITO_MODIFICATO_DIR}")

if __name__ == "__main__":
    main()