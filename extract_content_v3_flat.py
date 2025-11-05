import os
import glob
import codecs
import json
import re
from bs4 import BeautifulSoup, Tag, Comment

print("Avvio Script di Estrazione Contenuto (extract_content_v3 - Chirurgo)...")

# --- 1. CONFIGURAZIONE PERCORSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITO_ORIGINALE_DIR = os.path.join(BASE_DIR, "sito_originale")

# Il file di output dove salveremo tutto il contenuto estratto
CONTENT_FILE_OUT = os.path.join(BASE_DIR, "content_data_flat.json")

# Lista di file da ignorare (non estrarremo contenuto da questi)
IGNORE_LIST = [
    'search.html',
    'seach.html',
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

# --- 2. LOGICA DI ESTRAZIONE E PULIZIA CHIRURGICA ---

def clean_extracted_content(content_node):
    """
    PULIZIA CHIRURGICA v2: Rimuove i layout annidati e spazzatura.
    """
    if not content_node:
        return None, []

    old_schemas = []

    # Rimuovi i tag di layout indesiderati
    # Questa è la modifica chiave: rimuoviamo ANCHE main e article
    tags_da_rimuovere = ['header', 'footer', 'nav', 'aside', 'main', 'article']
    for tag_name in tags_da_rimuovere:
        for tag in content_node.find_all(tag_name):
            tag.decompose() # Rimuove il tag e tutto il suo contenuto

    # Estrai e rimuovi i vecchi schemi JSON-LD
    for tag in content_node.find_all('script', attrs={'type': 'application/ld+json'}):
        try:
            # Rimuovi eventuali commenti CDATA se presenti
            tag_string = tag.string
            if tag_string:
                tag_string = tag_string.strip()
                if tag_string.startswith('//<![CDATA[') and tag_string.endswith('//]]>'):
                    tag_string = tag_string[len('//<![CDATA['):-len('//]]>')]
            
            schema_json = json.loads(tag_string)
            
            if isinstance(schema_json, dict) and schema_json.get('@type') in ['FAQPage', 'HowTo']:
                old_schemas.append(schema_json)
            elif isinstance(schema_json, list):
                 for item in schema_json:
                     if isinstance(item, dict) and item.get('@type') in ['FAQPage', 'HowTo']:
                         old_schemas.append(item)
        except Exception:
            pass # Ignora JSON non valido o script non JSON
        tag.decompose() # Rimuovi lo script dello schema

    # Rimuovi commenti
    for comment in content_node.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
        
    # Rimuovi i tag script di menu duplicati (che hai visto nel log di 'vat')
    for tag in content_node.find_all('script'):
        if tag.string and 'mobile-menu-toggle' in tag.string:
            tag.decompose()
            
    content_html = content_node.decode_contents().strip()
    
    if not content_html:
        return None, []

    return content_html, old_schemas


def extract_main_content(soup, relative_path):
    """
    Tenta di estrarre il contenuto principale e poi lo PULISCE.
    """
    
    # --- LOGICA SPECIALE PER HOMEPAGE (Migliorata) ---
    if relative_path == 'index.html':
        print("    > Rilevata Homepage. Estraggo il body e lo pulisco...")
        body_tag = soup.find('body')
        if not body_tag:
            print(f"    > ERRORE Homepage: Nessun <body> trovato.")
            return None, []
        return clean_extracted_content(body_tag)

    # Logica per tutte le ALTRE pagine
    # Prova prima con selettori specifici, che sono più "stretti"
    selectors = [
        "#calculator-ui",        # Selettore 1: ID dalla pagina 'mortgage'
        ".calculator-container", # Selettore 2: Classe dalla pagina 'ppp'
        ".prose"                 # Selettore 3: Classe comune per articoli
    ]
    
    content_node = None
    for selector in selectors:
        content_node = soup.select_one(selector)
        if content_node:
            print(f"    > Trovato contenuto con selettore stretto: '{selector}'. Pulisco...")
            return clean_extracted_content(content_node)

    # Se fallisce, prova con tag semantici più ampi
    wide_selectors = ["main", "article"]
    for selector in wide_selectors:
        content_node = soup.select_one(selector)
        if content_node:
            print(f"    > Trovato contenuto con selettore ampio: '{selector}'. Pulisco...")
            return clean_extracted_content(content_node)

    # --- FALLBACK LOGIC (Logica di Sicurezza) ---
    print(f"    > ATTENZIONE: Nessun selettore trovato. Eseguo fallback sul body intero.")
    body_tag = soup.find('body')
    if not body_tag:
        print(f"    > ERRORE: Nessun <body> trovato.")
        return None, []
        
    return clean_extracted_content(body_tag)

# --- 3. ESECUZIONE PRINCIPALE ---
def main():
    all_files = glob.glob(os.path.join(SITO_ORIGINALE_DIR, "**", "*.html"), recursive=True)
    if not all_files:
        print(f"ERRORE: Nessun file .html trovato in {SITO_ORIGINALE_DIR}.")
        return

    print(f"Trovati {len(all_files)} file HTML. Inizio estrazione (v3 - Chirurgo)...")
    
    content_data = {} 
    files_estratti = 0
    files_saltati = 0
    files_con_errori = 0

    for file_path in all_files:
        relative_path = os.path.relpath(file_path, SITO_ORIGINALE_DIR).replace(os.path.sep, '/')
        
        # --- NUOVA LOGICA "FLAT URL" ---
        file_name = os.path.basename(relative_path)
        
        # Salta i file della ignore list
        if file_name in IGNORE_LIST:
            print(f"  > [IGNORA] File '{file_name}' è nella ignore list. Saltato.")
            files_saltati += 1
            continue
            
        url_path = '/' + os.path.splitext(file_name)[0]
        if file_name == 'index.html':
            url_path = "/" # Gestione speciale Homepage
        # --- FINE NUOVA LOGICA ---
        
        print(f"Processando: {relative_path} (come URL: {url_path})")
        
        try:
            with codecs.open(file_path, 'r', 'utf-8') as f_in:
                soup = BeautifulSoup(f_in, 'lxml')

            # 1. Estrai Titolo
            title = "Titolo Mancante"
            if soup.find('title'):
                title = soup.find('title').get_text(strip=True)
            elif soup.find('h1'):
                title = soup.find('h1').get_text(strip=True)
            title = re.sub(r'[\.\s]*calculator(s)?$', '', title, flags=re.IGNORECASE).strip()

            # 2. Estrai Descrizione
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description = description_tag['content'] if description_tag and description_tag.get('content') else f"Scopri di più su {title}."

            # 3. Estrai Lingua
            lang = soup.find('html').get('lang', 'en') if soup.find('html') else 'en'
            
            # 4. Estrai Contenuto Principale e Schemi Vecchi
            main_content, old_schemas = extract_main_content(soup, relative_path)
            
            if main_content:
                content_data[url_path] = {
                    "lang": lang,
                    "title": title,
                    "description": description,
                    "main_html": main_content,
                    "old_schemas": old_schemas
                }
                files_estratti += 1
            else:
                print(f"  > ERRORE: Impossibile estrarre il contenuto per {relative_path}.")
                files_con_errori += 1
                
        except Exception as e:
            print(f"--- ERRORE CRITICO durante l'analisi di {relative_path}: {e}")
            files_con_errori += 1

    try:
        with codecs.open(CONTENT_FILE_OUT, 'w', 'utf-8') as f_out:
            json.dump(content_data, f_out, indent=2, ensure_ascii=False)
        
        print("\n--- Estrazione (v3 - Chirurgo) completata! ---")
        print(f"Contenuto estratto con successo da: {files_estratti} file.")
        print(f"File saltati (ignore list): {files_saltati}")
        print(f"File falliti (errori di estrazione): {files_con_errori}")
        print(f"DATABASE DI CONTENUTO (FLAT) salvato in: {CONTENT_FILE_OUT}")

    except Exception as e:
        print(f"ERRORE CRITICO durante il salvataggio di {CONTENT_FILE_OUT}: {e}")

if __name__ == "__main__":
    main()