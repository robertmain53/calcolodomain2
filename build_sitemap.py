import os
import glob
import codecs
import json
from bs4 import BeautifulSoup

# --- CONFIGURAZIONE DEBUG ---
# Imposta questo a True per vedere quali file vengono saltati e perché
MODALITA_DEBUG = True
# --------------------------

print("Avvio Fase 2a: Costruzione della mappa del sito (v2 con Debug)...")

# --- Configurazione Percorsi ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITO_ORIGINALE_DIR = os.path.join(BASE_DIR, "sito_originale")
SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap_data.json")

sitemap_data = {}

# --- Scansione File ---
file_list = glob.glob(os.path.join(SITO_ORIGINALE_DIR, "**", "*.html"), recursive=True)

if not file_list:
    print(f"ERRORE: Nessun file .html trovato in {SITO_ORIGINALE_DIR}.")
    exit()

print(f"Trovati {len(file_list)} file HTML. Inizio analisi breadcrumb...")

file_mappati = 0
file_saltati = 0

for file_path in file_list:
    relative_path = os.path.relpath(file_path, SITO_ORIGINALE_DIR).replace(os.path.sep, '/')
    
    if relative_path == 'index.html':
        continue
        
    url_path = '/' + os.path.splitext(relative_path)[0]

    try:
        with codecs.open(file_path, 'r', 'utf-8') as f_in:
            soup = BeautifulSoup(f_in, 'lxml')

        # --- Estrazione Dati ---
        page_title = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'Titolo Mancante'
        
        # --- Logica di ricerca Breadcrumb (Aggiornata) ---
        breadcrumb_nav = None
        
        # Tentativo 1: Cerca una nav che contenga la stringa "Home" 
        # (MODIFICA: 'text' -> 'string')
        if not breadcrumb_nav:
            breadcrumb_nav = soup.find('nav', string=lambda t: t and 'Home' in t)
        
        # Tentativo 2: Cerca una nav con una classe che contenga 'breadcrumb'
        if not breadcrumb_nav:
            breadcrumb_nav = soup.find('nav', class_=lambda c: c and 'breadcrumb' in c)
        
        # Tentativo 3: Cerca un link 'Home' e usa il suo genitore
        if not breadcrumb_nav:
             all_links = soup.find_all('a')
             home_link = next((a for a in all_links if a.get_text(strip=True) == 'Home'), None)
             if home_link:
                 breadcrumb_nav = home_link.parent # Spesso il genitore è <nav> o <div>

        if not breadcrumb_nav:
            if MODALITA_DEBUG:
                print(f"  [DEBUG] Saltato: {relative_path} (Motivo: Nessuna <nav> breadcrumb trovata.)")
            file_saltati += 1
            continue

        links = breadcrumb_nav.find_all('a')
        
        if len(links) < 2:
            if MODALITA_DEBUG:
                print(f"  [DEBUG] Saltato: {relative_path} (Motivo: Trovata <nav> breadcrumb, ma con meno di 2 link.)")
            file_saltati += 1
            continue

        # Logica di estrazione (rimane invariata)
        category = links[1].get_text(strip=True)
        subcategory = "Generale" # Default
        if len(links) >= 3:
            subcategory_text = links[2].get_text(strip=True)
            # A volte il 3° link è la pagina stessa, non una sottocategoria
            # Questo controllo è imperfetto, ma un inizio
            if subcategory_text != page_title:
                subcategory = subcategory_text
        
        page_info = { "title": page_title, "url": url_path }

        if category not in sitemap_data: sitemap_data[category] = {}
        if subcategory not in sitemap_data[category]: sitemap_data[category][subcategory] = []
            
        sitemap_data[category][subcategory].append(page_info)
        file_mappati += 1
            
    except Exception as e:
        print(f"--- ERRORE durante l'analisi di {relative_path}: {e}")
        file_saltati += 1

# --- Salvataggio Mappa ---
try:
    with codecs.open(SITEMAP_FILE, 'w', 'utf-8') as f_out:
        json.dump(sitemap_data, f_out, indent=2, ensure_ascii=False)
    
    print(f"\n--- Analisi (v2) completata ---")
    print(f"File MAPPATI: {file_mappati}")
    print(f"File SALTATI: {file_saltati}")
    print(f"Mappa del sito salvata in: {SITEMAP_FILE}")

except Exception as e:
    print(f"ERRORE CRITICO durante il salvataggio di {SITEMAP_FILE}: {e}")