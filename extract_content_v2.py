import os
import glob
import codecs
import json
import re
from bs4 import BeautifulSoup, Tag, Comment

print("Avvio Script di Estrazione Contenuto (extract_content_v2)...")

# --- 1. CONFIGURAZIONE PERCORSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITO_ORIGINALE_DIR = os.path.join(BASE_DIR, "sito_originale")
CONTENT_FILE_OUT = os.path.join(BASE_DIR, "content_data.json")

# --- 2. FUNZIONI DI PULIZIA E ESTRAZIONE ---

def clean_extracted_content(content_node):
    """
    PULIZIA CHIRURGICA: Rimuove i "contenitori" del vecchio layout
    dall'interno del blocco di contenuto estratto, ma PRESERVA
    gli script necessari come MathJax.
    """
    if not content_node:
        return None, []

    old_schemas = []

    # Rimuovi i tag di layout indesiderati
    tags_da_rimuovere = ['header', 'footer', 'nav', 'aside']
    for tag_name in tags_da_rimuovere:
        for tag in content_node.find_all(tag_name):
            tag.decompose() # Rimuove il tag e tutto il suo contenuto

    # Estrai e rimuovi i vecchi schemi JSON-LD
    for tag in content_node.find_all('script', attrs={'type': 'application/ld+json'}):
        try:
            schema_json = json.loads(tag.string)
            # Salviamo solo gli schemi utili (FAQ/HowTo)
            if isinstance(schema_json, dict) and schema_json.get('@type') in ['FAQPage', 'HowTo']:
                old_schemas.append(schema_json)
            elif isinstance(schema_json, list): # Gestisce schemi multipli
                 for item in schema_json:
                     if isinstance(item, dict) and item.get('@type') in ['FAQPage', 'HowTo']:
                         old_schemas.append(item)
        except Exception:
            pass # Ignora JSON non valido
        tag.decompose() # Rimuovi lo script dello schema

    # Rimuovi commenti
    for comment in content_node.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
        
    # Ottieni l'HTML pulito
    content_html = content_node.decode_contents().strip()
    
    if not content_html:
        return None, []

    return content_html, old_schemas


def extract_main_content(soup, relative_path):
    """
    Tenta di estrarre il contenuto principale e poi lo PULISCE.
    """
    content_node = None
    
    # Logica per la Homepage
    if relative_path == 'index.html':
        print("    > Rilevata Homepage. Estraggo sezioni 'hero', 'popular', 'categories', 'features'.")
        sections = soup.find_all('section', id=lambda x: x in ['popular', 'categories', 'features'])
        hero = soup.find('section', class_='hero-gradient')
        
        # Crea un nuovo div "wrapper" per contenere tutto
        wrapper_div = soup.new_tag('div')
        if hero:
            wrapper_div.append(hero)
        for section in sections:
            wrapper_div.append(section)
            
        if not wrapper_div.contents:
             print(f"    > ERRORE Homepage: Impossibile trovare sezioni. Eseguo fallback sul body.")
             return extract_main_content_fallback(soup)
        
        # Passa il wrapper alla pulizia (anche se probabilmente è già pulito)
        return clean_extracted_content(wrapper_div)

    # Logica per tutte le ALTRE pagine
    selectors = [
        "main",                  # Selettore 1: Il tag <main>
        "article",               # Selettore 2: Il tag <article>
        "#calculator-ui",        # Selettore 3: ID dalla pagina 'mortgage'
        ".calculator-container", # Selettore 4: Classe dalla pagina 'ppp'
        ".prose"                 # Selettore 5: Classe comune per articoli
    ]
    
    for selector in selectors:
        content_node = soup.select_one(selector)
        if content_node:
            print(f"    > Trovato contenuto con: '{selector}'. Avvio pulizia...")
            return clean_extracted_content(content_node)

    # --- FALLBACK LOGIC (Logica di Sicurezza) ---
    print(f"    > ATTENZIONE: Nessun selettore primario trovato. Eseguo fallback sul body.")
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

    print(f"Trovati {len(all_files)} file HTML. Inizio estrazione (v2)...")
    
    content_data = {} 
    files_estratti = 0
    files_con_errori = 0

    for file_path in all_files:
        relative_path = os.path.relpath(file_path, SITO_ORIGINALE_DIR).replace(os.path.sep, '/')
        url_path = '/' + os.path.splitext(relative_path)[0]
        
        if relative_path == 'index.html':
            url_path = "/"
        
        print(f"Processando: {relative_path}...")
        
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
                    "old_schemas": old_schemas # Salva gli schemi FAQ/HowTo
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
        
        print("\n--- Estrazione (v2) completata! ---")
        print(f"Contenuto estratto con successo da: {files_estratti} file.")
        print(f"File saltati per errori: {files_con_errori}")
        print(f"DATABASE DI CONTENUTO salvato in: {CONTENT_FILE_OUT}")

    except Exception as e:
        print(f"ERRORE CRITICO durante il salvataggio di {CONTENT_FILE_OUT}: {e}")

if __name__ == "__main__":
    main()