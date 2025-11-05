import os
import glob
import codecs
import json
from bs4 import BeautifulSoup

print("Avvio Fase 2a (v3 - Flat): Costruzione della mappa del sito 'piatta'...")

# --- Configurazione Percorsi ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITO_ORIGINALE_DIR = os.path.join(BASE_DIR, "sito_originale")

# Ripartiamo da zero con un nuovo file di mappa sporca
SITEMAP_FILE_SPORCA = os.path.join(BASE_DIR, "sitemap_data_dirty_flat.json")

sitemap_data = {}

file_list = glob.glob(os.path.join(SITO_ORIGINALE_DIR, "**", "*.html"), recursive=True)
if not file_list:
    print(f"ERRORE: Nessun file .html trovato in {SITO_ORIGINALE_DIR}.")
    exit()

print(f"Trovati {len(file_list)} file HTML. Inizio analisi breadcrumb...")
file_mappati = 0

for file_path in file_list:
    relative_path = os.path.relpath(file_path, SITO_ORIGINALE_DIR).replace(os.path.sep, '/')
    
    # --- NUOVA LOGICA "FLAT URL" ---
    # Ottieni solo il nome del file, es. "mortgage-payment.html"
    file_name = os.path.basename(relative_path)
    
    # Crea l'URL path da quello, es. "/mortgage-payment"
    url_path = '/' + os.path.splitext(file_name)[0]
    # --- FINE NUOVA LOGICA ---

    # Ignora file speciali
    if file_name in ['index.html', 'search.html', 'seach.html', 'privacy.html', 'contact.html', 'about.html', 'terms.html', 'sitemap.html']:
        continue
        
    try:
        with codecs.open(file_path, 'r', 'utf-8') as f_in:
            soup = BeautifulSoup(f_in, 'lxml')

        page_title = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'Titolo Mancante'
        
        breadcrumb_nav = None
        breadcrumb_nav = soup.find('nav', string=lambda t: t and 'Home' in t)
        if not breadcrumb_nav:
             all_links = soup.find_all('a')
             home_link = next((a for a in all_links if a.get_text(strip=True) == 'Home'), None)
             if home_link:
                 breadcrumb_nav = home_link.parent

        if not breadcrumb_nav:
            continue

        links = breadcrumb_nav.find_all('a')
        
        if len(links) >= 2:
            category = links[1].get_text(strip=True)
            subcategory = "Generale" # Default
            if len(links) >= 3:
                subcategory_text = links[2].get_text(strip=True)
                if subcategory_text != page_title:
                    subcategory = subcategory_text
            
            page_info = {
                "title": page_title,
                "url": url_path # Salva il NUOVO URL piatto
            }

            if category not in sitemap_data: sitemap_data[category] = {}
            if subcategory not in sitemap_data[category]: sitemap_data[category][subcategory] = []
                
            sitemap_data[category][subcategory].append(page_info)
            file_mappati += 1
            
    except Exception:
        pass # Salta file che non può analizzare

try:
    with codecs.open(SITEMAP_FILE_SPORCA, 'w', 'utf-8') as f_out:
        json.dump(sitemap_data, f_out, indent=2, ensure_ascii=False)
    
    print(f"\n--- Analisi (v3 - Flat) completata ---")
    print(f"Mappati {file_mappati} file (con la nuova struttura URL).")
    print(f"Mappa SPORCA salvata in: {SITEMAP_FILE_SPORCA}")

except Exception as e:
    print(f"ERRORE CRITICO durante il salvataggio di {SITEMAP_FILE_SPORCA}: {e}")