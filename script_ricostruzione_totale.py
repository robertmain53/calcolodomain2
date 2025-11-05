import os
import glob
import codecs
import json
import csv
import re
from bs4 import BeautifulSoup, Comment

print("AVVIO SCRIPT DI RICOSTRUZIONE TOTALE (v3)")

# --- 1. CONFIGURAZIONE GLOBALE ---

# ⚠️ INCOLLA QUI I TUOI SCRIPT PER HEAD
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

# Percorsi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "template_perfetti")
SITO_ORIGINALE_DIR = os.path.join(BASE_DIR, "sito_originale")
SITO_MODIFICATO_DIR = os.path.join(BASE_DIR, "sito_modificato")

# File di dati (I nostri due "cervelli")
SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap_data_FINAL.json")
REPORT_FILE = os.path.join(BASE_DIR, "template_report.csv")

os.makedirs(SITO_MODIFICATO_DIR, exist_ok=True)

# --- 2. FUNZIONI HELPER (Caricamento Dati) ---

def load_templates(template_dir):
    """Carica i template HTML 'gold standard' in memoria."""
    try:
        with codecs.open(os.path.join(template_dir, "header_perfetto.html"), 'r', 'utf-8') as f:
            header_html = f.read()
        with codecs.open(os.path.join(template_dir, "footer_perfetto.html"), 'r', 'utf-8') as f:
            footer_html = f.read()
        return header_html, footer_html
    except FileNotFoundError as e:
        print(f"ERRORE CRITICO: File template non trovato in '{template_dir}'. {e}")
        return None, None

def load_sitemap(sitemap_path):
    """Carica la mappa sitemap_data_FINAL.json."""
    try:
        with codecs.open(sitemap_path, 'r', 'utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERRORE CRITICO: '{sitemap_path}' non trovato.")
        print("Devi prima eseguire 'build_sitemap.py', 'clean_sitemap.py', e 'enrich_sitemap_v2.py'.")
        return None
    except json.JSONDecodeError:
        print(f"ERRORE CRITICO: '{sitemap_path}' è un JSON non valido.")
        return None

def load_template_report(report_path):
    """Carica il report CSV dei profili e lo trasforma in un dizionario di lookup."""
    try:
        profile_lookup = {}
        with open(report_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Salta l'intestazione
            for row in reader:
                profile_key = row[0]
                # Gli esempi sono in 'file1, file2, file3...'
                # Dobbiamo trovare *tutti* i file per quel profilo, non solo i primi 10
                # Questo è un trucco per trovare tutti i file che corrispondono
                # all'ultimo script 'discover_templates.py'
                pass # N.B: Questo è un segnaposto logico. 
                     # Il report CSV è solo per la *nostra* analisi.
                     # La logica di classificazione vera la rifaremo al volo.
        # Visto che il CSV è solo un riepilogo, è più sicuro
        # ricalcolare il profilo al volo per ogni file.
        print("Report CSV letto per riferimento. I profili verranno calcolati al volo.")
        return True # Diamo solo conferma che esiste
    except FileNotFoundError:
        print(f"ERRORE CRITICO: '{report_path}' non trovato.")
        print("Devi prima eseguire 'discover_templates.py'.")
        return None

def get_page_profile(soup):
    """Analizza la 'soup' e restituisce la stringa del profilo (come nel report)."""
    head_count = len(soup.find_all('head'))
    body_count = len(soup.find_all('body'))
    header_count = len(soup.find_all('header'))
    footer_count = len(soup.find_all('footer'))
    aside_count = len(soup.find_all('aside'))
    breadcrumb_count = 1 if soup.find('a', string=lambda t: t and 'Home' in t) else 0
    
    return (
        f"head:{head_count}, "
        f"body:{body_count}, "
        f"header:{header_count}, "
        f"footer:{footer_count}, "
        f"aside:{aside_count}, "
        f"breadcrumb:{breadcrumb_count}"
    )

def get_page_category_info(url_path, sitemap_data):
    """Cerca nella sitemap_data e restituisce (cat, subcat, title) per un URL."""
    for category, subcategories in sitemap_data.items():
        for subcategory, pages in subcategories.items():
            for page in pages:
                if page['url'] == url_path:
                    return category, subcategory, page['title']
    return None, None, None # Non trovato

# --- 3. FUNZIONI HELPER (Generazione HTML e Iniezione) ---

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
        # Fallback se la categoria non è trovata
        related_links = [
            {"title": "Mortgage", "url": "/mortgage-payment"},
            {"title": "Percentage", "url": "/percentage-calculator"},
            {"title": "BMI", "url": "/bmi-calculator"},
            {"title": "Auto Loan", "url": "/auto-loan-calculator"}
        ]

    # Limita a 10 link per pulizia
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

def inject_scripts_and_cleanup(soup, head_scripts_html, body_scripts_html):
    """Pulisce il vecchio e inietta il nuovo codice in head e body."""
    
    # --- Pulizia HEAD ---
    head_tag = soup.find('head')
    if not head_tag:
        head_tag = soup.new_tag('head')
        soup.insert(0, head_tag)
        
    for old in head_tag.find_all("script", src=lambda s: s and ("ezoic.net" in s or "googletagmanager" in s)):
        old.decompose()
    for old in head_tag.find_all("meta", attrs={"name": "google-site-verification"}):
        old.decompose()
    for old in head_tag.find_all('link', attrs={'rel': 'preload'}):
        if 'mobile-menu.js' in old.get('href', '') or 'page-enhancements.js' in old.get('href', ''):
            old.decompose()
            
    # Inietta script HEAD
    head_tag.append(BeautifulSoup(head_scripts_html, 'lxml'))

    # --- Pulizia BODY ---
    body_tag = soup.find('body')
    if not body_tag:
        body_tag = soup.new_tag('body')
        soup.append(body_tag)
        
    for old in body_tag.find_all("script", src=lambda s: s and "adsbygoogle.js" in s):
        old.decompose()
        
    # Inietta script BODY (all'inizio)
    body_tag.insert(0, BeautifulSoup(body_scripts_html, 'lxml'))
    
    # Inietta script JS (alla fine)
    script_da_aggiungere = ["/assets/js/script_menu.js", "/assets/js/script_faq.js", "search.js"]
    for src in script_da_aggiungere:
        for old in body_tag.find_all('script', src=src):
            old.decompose()
        new_script_tag = soup.new_tag("script", src=src, defer=True)
        body_tag.append(new_script_tag)

def inject_breadcrumbs(soup, category, subcategory, page_title):
    """Genera e inietta sia l'HTML visibile che lo schema JSON-LD per le breadcrumb."""
    
    # 1. Trova il contenitore HTML
    breadcrumb_container = soup.find('nav', id="breadcrumb-container")
    if not breadcrumb_container:
        # Crea il contenitore se non esiste (per le pagine "Rebuild")
        breadcrumb_container = soup.new_tag('nav', id="breadcrumb-container")
        breadcrumb_container['class'] = "container mx-auto px-4 py-2 text-sm text-gray-600"
        if soup.find('header'):
            soup.find('header').insert_after(breadcrumb_container)
        
    # 2. Genera HTML
    html = '<a href="https://calcdomain.com" class="hover:text-blue-600">Home</a>'
    
    # 3. Genera Schema JSON-LD
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://calcdomain.com"}
        ]
    }
    
    if category:
        # Semplice URL-safe-slug (può essere migliorato)
        cat_slug = category.lower().replace(' & ', '-').replace(' ', '-')
        html += f' &raquo; <a href="https://calcdomain.com/{cat_slug}" class="hover:text-blue-600">{category}</a>'
        schema["itemListElement"].append(
            {"@type": "ListItem", "position": 2, "name": category, "item": f"https://calcdomain.com/{cat_slug}"}
        )
        
    if subcategory and subcategory != "Generale":
        sub_slug = subcategory.lower().replace(' & ', '-').replace(' ', '-')
        html += f' &raquo; <a href="https://calcdomain.com/{cat_slug}/{sub_slug}" class="hover:text-blue-600">{subcategory}</a>'
        schema["itemListElement"].append(
            {"@type": "ListItem", "position": 3, "name": subcategory, "item": f"https://calcdomain.com/{cat_slug}/{sub_slug}"}
        )

    # Aggiungi la pagina corrente
    html += f' &raquo; <span>{page_title}</span>'
    
    # Inietta l'HTML
    breadcrumb_container.clear()
    breadcrumb_container.append(BeautifulSoup(html, 'lxml'))
    
    # Inietta lo Schema
    head_tag = soup.find('head')
    if head_tag:
        # Rimuovi vecchi schemi breadcrumb
        for old_schema in head_tag.find_all('script', type="application/ld+json"):
             if "BreadcrumbList" in old_schema.get_text():
                 old_schema.decompose()
                 
        schema_tag = soup.new_tag('script', type="application/ld+json")
        schema_tag.string = json.dumps(schema, indent=2)
        head_tag.append(schema_tag)


# --- 4. LE LOGICHE DI RICOSTRUZIONE PER GRUPPO ---

def process_group_standardize(soup, sidebar_html, header_html, footer_html):
    """
    GRUPPO 2: "STANDARDIZE"
    Profilo: head:1, body:1, header:1, footer:1, aside:1, breadcrumb:1
    Azione: Sostituzione 1-a-1. La struttura è già corretta.
    """
    soup.find('header').replace_with(BeautifulSoup(header_html, 'lxml').header)
    soup.find('footer').replace_with(BeautifulSoup(footer_html, 'lxml').footer)
    soup.find('aside').replace_with(BeautifulSoup(sidebar_html, 'lxml').aside)
    
    # Rimuovi vecchi placeholder di annunci
    for old_ad in soup.find_all('div', class_="bg-gray-200"):
        if "Ad Unit" in old_ad.get_text(strip=True):
            old_ad.decompose()

def process_group_rebuild(soup, sidebar_html, header_html, footer_html):
    """
    GRUPPO 1: "REBUILD"
    Profilo: head:1, body:1, header:0, footer:0, aside:0, breadcrumb:0
    Azione: Ricostruzione totale. La pagina è una "tela bianca".
    """
    body_tag = soup.find('body')
    
    # Estrai tutto il contenuto
    main_content_html = "\n".join([str(tag) for tag in body_tag.contents])
    
    # Svuota il body
    body_tag.clear()
    
    # Costruisci la nuova struttura
    nuovo_layout_html = f"""
    <div class="container mx-auto px-4 py-8">
        <div class="flex flex-col lg:flex-row gap-8">
            <main class="w-full lg:w-2/3">
                {main_content_html}
            </main>
            <aside class="w-full lg:w-1/3">
                {sidebar_html}
            </aside>
        </div>
    </div>
    """
    
    # Riempi di nuovo il body
    body_tag.append(BeautifulSoup(header_html, 'lxml').header)
    body_tag.append(BeautifulSoup(nuovo_layout_html, 'lxml'))
    body_tag.append(BeautifulSoup(footer_html, 'lxml').footer)

def process_group_repair(soup, sidebar_html, header_html, footer_html):
    """
    GRUPPO 3: "REPAIR"
    Profilo: Qualsiasi profilo parziale (es. header:2, footer:0, aside:1)
    Azione: Sostituzione forzata. Non tocchiamo la struttura, rimpiazziamo solo i pezzi.
    """
    # Rimuovi *tutti* gli header e aggiungine uno nuovo
    for tag in soup.find_all('header'):
        tag.decompose()
    soup.find('body').insert(0, BeautifulSoup(header_html, 'lxml').header)

    # Rimuovi *tutti* i footer e aggiungine uno nuovo
    for tag in soup.find_all('footer'):
        tag.decompose()
    soup.find('body').append(BeautifulSoup(footer_html, 'lxml').footer)
    
    # Rimuovi *tutte* le sidebar e aggiungine una nuova
    # (Logica più complessa: dove la mettiamo? Per ora, la saltiamo per sicurezza)
    # ⚠️ TODO: Decidere una strategia per la sidebar per questo gruppo.
    # Per ora, la logica più sicura è non aggiungerla per non rompere il layout.
    for tag in soup.find_all('aside'):
        print(f"  > INFO: Trovato e rimosso vecchio <aside>.")
        tag.decompose()
        
    # Rimuovi vecchi placeholder di annunci
    for old_ad in soup.find_all('div', class_="bg-gray-200"):
        if "Ad Unit" in old_ad.get_text(strip=True):
            old_ad.decompose()


# --- 5. ESECUZIONE PRINCIPALE (LA FABBRICA v3) ---

def main():
    # 1. Carica tutti i dati in memoria
    print("Caricamento dati...")
    header_html, footer_html = load_templates(TEMPLATE_DIR)
    sitemap_data = load_sitemap(SITEMAP_FILE)
    template_report_ok = load_template_report(REPORT_FILE)
    
    if not header_html or not sitemap_data or not template_report_ok:
        print("Errore nel caricamento dei file. Uscita.")
        return

    all_files = glob.glob(os.path.join(SITO_ORIGINALE_DIR, "**", "*.html"), recursive=True)
    print(f"Trovati {len(all_files)} file HTML. Inizio RICOSTRUZIONE TOTALE...")
    
    file_processati = 0
    file_con_errori = 0
    file_saltati = 0

    # 2. Inizia il ciclo
    for file_path in all_files:
        try:
            relative_path = os.path.relpath(file_path, SITO_ORIGINALE_DIR).replace(os.path.sep, '/')
            output_path = os.path.join(SITO_MODIFICATO_DIR, relative_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with codecs.open(file_path, 'r', 'utf-8') as f_in:
                soup = BeautifulSoup(f_in, 'lxml')

            # --- 3. CLASSIFICAZIONE E DATI ---
            
            # 3a. Trova il profilo di layout
            page_profile = get_page_profile(soup)
            
            # 3b. Trova i dati della categoria
            url_path = '/' + os.path.splitext(relative_path)[0]
            category, subcategory, title = get_page_category_info(url_path, sitemap_data)
            
            if not title:
                title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Pagina"

            # 3c. Genera la sidebar dinamicamente
            sidebar_html = generate_sidebar_html(category, subcategory, sitemap_data)

            # --- 4. LOGICA DI AZIONE BASATA SUL PROFILO ---
            
            # GRUPPO 4: IGNORE (File rotti o spazzatura)
            if "head:0" in page_profile or "body:0" in page_profile or "body:2" in page_profile or "googlec8c0eedfe44345b9" in relative_path:
                print(f"  > [IGNORA] File malformato: {relative_path} ({page_profile}). Correggere a mano.")
                file_saltati += 1
                continue
            
            # GRUPPO 2: STANDARDIZE (Pagina "Gold")
            elif page_profile == "head:1, body:1, header:1, footer:1, aside:1, breadcrumb:1":
                print(f"  > [STANDARDIZZA] File: {relative_path}")
                process_group_standardize(soup, sidebar_html, header_html, footer_html)
            
            # GRUPPO 1: REBUILD (Orfano Pulito)
            elif page_profile == "head:1, body:1, header:0, footer:0, aside:0, breadcrumb:0":
                print(f"  > [RICOSTRUISCI] File: {relative_path}")
                process_group_rebuild(soup, sidebar_html, header_html, footer_html)

            # GRUPPO 3: REPAIR (Tutti gli altri casi parziali)
            else:
                print(f"  > [RIPARA] File: {relative_path} ({page_profile})")
                process_group_repair(soup, sidebar_html, header_html, footer_html)

            # --- 5. AZIONI FINALI (per tutti i file processati) ---
            
            # Inietta Breadcrumb (HTML + JSON-LD)
            inject_breadcrumbs(soup, category, subcategory, title)
            
            # Inietta Script di Analisi/Monetizzazione e pulizia
            inject_scripts_and_cleanup(soup, SCRIPT_GA_GSC_EZOIC_CMP_HEAD, SCRIPT_ADSENSE_BODY)
            
            # --- 6. SALVATAGGIO ---
            with codecs.open(output_path, 'w', 'utf-8') as f_out:
                f_out.write(soup.prettify())
                
            file_processati += 1

        except Exception as e:
            print(f"--- ERRORE CRITICO DURANTE L'ELABORAZIONE di {relative_path} ---")
            print(f"  Dettagli: {e}")
            file_con_errori += 1

    # --- 7. RIEPILOGO FINALE ---
    print("\n--- RICOSTRUZIONE COMPLETATA ---")
    print(f"File totali processati: {file_processati}")
    print(f"File saltati (malformati): {file_saltati}")
    print(f"File falliti (errori script): {file_con_errori}")
    print(f"La nuova versione del sito si trova in: {SITO_MODIFICATO_DIR}")

if __name__ == "__main__":
    main()