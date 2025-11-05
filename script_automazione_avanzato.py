import os
import glob
import codecs
import json
from bs4 import BeautifulSoup, Comment

print("Avvio Fase 2b: Ristrutturazione completa del sito (v2 con 'Aggiungi se non esiste')...")

# --- 1. CONFIGURAZIONE DEI PERCORSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "template_perfetti")
SITO_ORIGINALE_DIR = os.path.join(BASE_DIR, "sito_originale")
SITO_MODIFICATO_DIR = os.path.join(BASE_DIR, "sito_modificato")
SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap_data.json")

os.makedirs(SITO_MODIFICATO_DIR, exist_ok=True)

# --- 2. CARICA I "MATTONI" (Template e Mappa) ---
try:
    with codecs.open(os.path.join(TEMPLATE_DIR, "header_perfetto.html"), 'r', 'utf-8') as f:
        header_perfetto_html = f.read()

    with codecs.open(os.path.join(TEMPLATE_DIR, "footer_perfetto.html"), 'r', 'utf-8') as f:
        footer_perfetto_html = f.read()
        
    with codecs.open(SITEMAP_FILE, 'r', 'utf-8') as f:
        sitemap_data = json.load(f)
        
    print("Template HTML e sitemap_data.json caricati.")

except FileNotFoundError as e:
    print(f"ERRORE: File template o sitemap_data.json non trovato. Esegui prima 'build_sitemap.py'. Dettagli: {e}")
    exit()

# --- 3. DEFINIZIONI DEGLI SCRIPT GLOBALI ---
SCRIPT_GA_GSC_EZOIC_CMP_HEAD = """
<script async src="https://www.googletagmanager.com/gtag/js?id=TUO_ID_GA"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'TUO_ID_GA');
</script>
"""

SCRIPT_ADSENSE_BODY = """
"""

# --- 4. FUNZIONE DI GENERAZIONE SIDEBAR DINAMICA ---
def generate_sidebar_html(page_soup, sitemap_data):
    category_name = None
    subcategory_name = None
    try:
        breadcrumb_nav = page_soup.find('nav', text=lambda t: t and 'Home' in t)
        if not breadcrumb_nav:
             all_links = page_soup.find_all('a')
             home_link = next((a for a in all_links if a.get_text(strip=True) == 'Home'), None)
             if home_link: breadcrumb_nav = home_link.parent
        
        if breadcrumb_nav:
            links = breadcrumb_nav.find_all('a')
            if len(links) >= 2: category_name = links[1].get_text(strip=True)
            if len(links) >= 3: subcategory_name = links[2].get_text(strip=True)
            elif category_name: subcategory_name = "Generale"
    except Exception:
        pass 

    related_links = []
    if category_name and subcategory_name and \
       category_name in sitemap_data and \
       subcategory_name in sitemap_data[category_name]:
        related_links = sitemap_data[category_name][subcategory_name]
    
    if not related_links:
        related_links = [
            {"title": "Mortgage Calculator", "url": "/mortgage-payment"},
            {"title": "Percentage Calculator", "url": "/percentage-calculator"},
            {"title": "BMI Calculator", "url": "/bmi-calculator"}
        ]
        list_title = "Popular Calculators"
    else:
        list_title = "Related Calculators"

    sidebar_html = f"""
    <div class="sticky top-24 space-y-8">
      <div id="sidebar-ad-placeholder-top"></div>
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h3 class="font-bold text-lg mb-4">{list_title}</h3>
        <ul class="space-y-3">
    """
    for link in related_links[:10]:
        sidebar_html += f'<li><a href="https://calcdomain.com{link["url"]}" class="text-blue-600 hover:underline">{link["title"]}</a></li>'
    sidebar_html += "</ul></div></div>"
    return sidebar_html


# --- 5. FUNZIONE "SOSTITUISCI O AGGIUNGI" (Nuova) ---
# --- MODIFICA: Questa funzione gestisce l'aggiunta/sostituzione di header e footer ---
def replace_or_add_header_footer(soup, header_html, footer_html, relative_path):
    """Sostituisce o aggiunge header e footer in modo sicuro."""
    
    # Crea i nuovi tag da inserire
    nuovo_header_tag = BeautifulSoup(header_html, 'lxml').header
    nuovo_footer_tag = BeautifulSoup(footer_html, 'lxml').footer
    
    body_tag = soup.find('body')
    if not body_tag:
        print(f"  > ERRORE GRAVE: Nessun <body> trovato in {relative_path}. Impossibile aggiungere header/footer.")
        return # Esce dalla funzione se non c'è body

    # Gestione HEADER
    vecchio_header = soup.find('header')
    if vecchio_header:
        vecchio_header.replace_with(nuovo_header_tag)
    else:
        print(f"  > INFO: Nessun <header> trovato in {relative_path}. AGGIUNGO...")
        body_tag.insert(0, nuovo_header_tag) # Inserisci come primo elemento del body

    # Gestione FOOTER
    vecchio_footer = soup.find('footer')
    if vecchio_footer:
        vecchio_footer.replace_with(nuovo_footer_tag)
    else:
        print(f"  > INFO: Nessun <footer> trovato in {relative_path}. AGGIUNGO...")
        body_tag.append(nuovo_footer_tag) # Aggiungi come ultimo elemento del body


# --- 6. IL CICLO PRINCIPALE (LA FABBRICA) ---
file_list = glob.glob(os.path.join(SITO_ORIGINALE_DIR, "**", "*.html"), recursive=True)

print(f"Trovati {len(file_list)} file HTML. Inizio RISTRUTTURAZIONE (v2)...")

file_processati = 0
file_con_errori = 0

for file_path in file_list:
    try:
        relative_path = os.path.relpath(file_path, SITO_ORIGINALE_DIR).replace(os.path.sep, '/')
        output_path = os.path.join(SITO_MODIFICATO_DIR, relative_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with codecs.open(file_path, 'r', 'utf-8') as f_in:
            soup = BeautifulSoup(f_in, 'lxml')

        # --- 7. LOGICA SPECIALE: HOMEPAGE vs ALTRE PAGINE ---
        
        if relative_path == 'index.html':
            # --- SOLO HOMEPAGE ---
            print(f"  > Processo 'Homepage': {relative_path}. Applico solo Header/Footer.")
            # Applica solo header/footer senza ristrutturare
            replace_or_add_header_footer(soup, header_perfetto_html, footer_perfetto_html, relative_path)
        
        else:
            # --- TUTTE LE ALTRE PAGINE ---
            print(f"  > Processo 'Pagina Interna': {relative_path}")
            
            # --- MODIFICA: Controlla se la pagina è "standard" (ha H e F) ---
            vecchio_header = soup.find('header')
            vecchio_footer = soup.find('footer')

            if vecchio_header and vecchio_footer:
                # --- CASO A: Pagina Standard -> Ristrutturazione 2 Colonne ---
                print("    -> Pagina Standard. Applica Ristrutturazione a 2 colonne.")
                
                # 1. Estrai contenuto principale
                main_content_tags = []
                current_tag = vecchio_header.next_sibling
                while current_tag and current_tag != vecchio_footer:
                    main_content_tags.append(str(current_tag))
                    current_tag = current_tag.next_sibling
                main_content_html = "\n".join(main_content_tags)
                
                # 2. Sostituisci header e footer
                nuovo_header_tag = BeautifulSoup(header_perfetto_html, 'lxml').header
                vecchio_header.replace_with(nuovo_header_tag)
                nuovo_footer_tag = BeautifulSoup(footer_perfetto_html, 'lxml').footer
                vecchio_footer.replace_with(nuovo_footer_tag)

                # 3. Rimuovi il vecchio contenuto (ora salvato in main_content_html)
                current_tag = soup.find('header').next_sibling
                while current_tag and current_tag.name != 'footer':
                    next_tag = current_tag.next_sibling
                    current_tag.decompose()
                    current_tag = next_tag

                # 4. Genera sidebar e nuovo layout
                sidebar_html = generate_sidebar_html(soup, sitemap_data)
                nuovo_layout_html = f"""
                <nav id="breadcrumb-container" class="container mx-auto px-4 py-2 text-sm text-gray-600"></nav>
                <div class="container mx-auto px-4 py-8">
                    <div class="flex flex-col lg:flex-row gap-8">
                        <main class="w-full lg:w-2/3">{main_content_html}</main>
                        <aside class="w-full lg:w-1/3">{sidebar_html}</aside>
                    </div>
                </div>
                """
                # 5. Inserisci il nuovo layout dopo l'header
                soup.find('header').insert_after(BeautifulSoup(nuovo_layout_html, 'lxml'))

            else:
                # --- CASO B: Pagina Non-Standard -> Solo Header/Footer ---
                print(f"    -> Pagina Non-Standard. Applica solo Header/Footer per sicurezza.")
                # Applica solo header/footer senza ristrutturare per evitare di rompere il layout
                replace_or_add_header_footer(soup, header_perfetto_html, footer_perfetto_html, relative_path)
            
            # --- FINE MODIFICA ---

        # --- 8. PULIZIA E INIEZIONE SCRIPT (per TUTTE le pagine) ---
        
        # Rimuovi vecchi placeholder di annunci
        for old_ad in soup.find_all('div', class_="bg-gray-200"):
            if "Ad Unit" in old_ad.get_text(strip=True):
                old_ad.decompose()

        # Rimuovi i vecchi preload inutili
        for link in soup.find_all('link', attrs={'rel': 'preload'}):
            if 'mobile-menu.js' in link.get('href', '') or 'page-enhancements.js' in link.get('href', ''):
                link.decompose()

        # Inietta SCRIPT NEL <HEAD>
        head_tag = soup.find('head')
        if head_tag:
            # Pulisci da eventuali vecchi script prima di aggiungere i nuovi
            for old_script in head_tag.find_all("script", src=lambda s: s and ("ezoic.net" in s or "googletagmanager" in s)):
                old_script.decompose()
            for old_meta in head_tag.find_all("meta", attrs={"name": "google-site-verification"}):
                old_meta.decompose()
                
            head_tag.append(BeautifulSoup(SCRIPT_GA_GSC_EZOIC_CMP_HEAD, 'lxml'))
        
        # Inietta SCRIPT NEL <BODY>
        body_tag = soup.find('body')
        if body_tag:
            # Pulisci da eventuali vecchi script
            for old_script in body_tag.find_all("script", src=lambda s: s and "adsbygoogle.js" in s):
                old_script.decompose()

            body_tag.insert(0, BeautifulSoup(SCRIPT_ADSENSE_BODY, 'lxml'))
            
            script_da_aggiungere = [
                "/assets/js/script_menu.js",
                "/assets/js/script_faq.js",
                "search.js" # Assicurati che questo file esista in una posizione accessibile
            ]
            for script_src in script_da_aggiungere:
                # Rimuovi vecchie versioni prima di aggiungere
                for old in body_tag.find_all('script', src=script_src):
                    old.decompose()
                
                nuovo_script_tag = soup.new_tag("script", src=script_src, defer=True)
                body_tag.append(nuovo_script_tag)

        # --- 9. SALVA IL FILE MODIFICATO ---
        with codecs.open(output_path, 'w', 'utf-8') as f_out:
            f_out.write(soup.prettify())
            
        file_processati += 1

    except Exception as e:
        print(f"--- ERRORE DURANTE L'ELABORAZIONE di {relative_path} ---")
        print(f"  Dettagli: {e}")
        file_con_errori += 1

# --- 10. RIEPILOGO ---
print("\n--- Ristrutturazione (v2) completata ---")
print(f"File totali processati: {file_processati}")
print(f"File saltati per errori: {file_con_errori}")
print(f"I file modificati si trovano in: {SITO_MODIFICATO_DIR}")