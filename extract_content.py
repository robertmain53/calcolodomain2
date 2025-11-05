import os
import glob
import codecs
import json
import re
from bs4 import BeautifulSoup, Tag

print("Avvio Script di Estrazione Contenuto (extract_content.py)...")

# --- 1. CONFIGURAZIONE PERCORSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITO_ORIGINALE_DIR = os.path.join(BASE_DIR, "sito_originale")

# Il file di output dove salveremo tutto il contenuto estratto
CONTENT_FILE_OUT = os.path.join(BASE_DIR, "content_data.json")

# --- 2. LOGICA DI ESTRAZIONE A CASCATA ---

def extract_main_content(soup):
    """
    Tenta di estrarre il contenuto principale usando una serie di selettori,
    dal più probabile al meno probabile.
    """
    content_node = None
    
    # Lista di selettori da provare in ordine
    selectors = [
        "main",                                 # Selettore 1: Il tag <main>
        "article",                              # Selettore 2: Il tag <article>
        "#calculator-ui",                       # Selettore 3: ID dalla pagina 'mortgage'
        ".calculator-container",                # Selettore 4: Classe dalla pagina 'ppp'
        ".prose"                                # Selettore 5: Classe comune per articoli
    ]
    
    for selector in selectors:
        content_node = soup.select_one(selector)
        if content_node:
            print(f"    > Trovato contenuto con: '{selector}'")
            return str(content_node) # Ritorna l'HTML interno come stringa

    # --- FALLBACK LOGIC (Logica di Sicurezza) ---
    # Se nessuno dei selettori ha funzionato, siamo in una pagina "orfana"
    # Prendiamo l'INTERO <body> e rimuoviamo i pezzi che NON vogliamo.
    print(f"    > ATTENZIONE: Nessun selettore primario trovato. Eseguo fallback...")
    body_tag = soup.find('body')
    
    if not body_tag:
        print(f"    > ERRORE: Nessun <body> trovato. Impossibile estrarre contenuto.")
        return None # Non c'è niente da salvare

    # Clona il body per non modificare l'originale
    body_clone = BeautifulSoup(str(body_tag), 'lxml').body

    # Rimuovi tutti i tag spazzatura noti
    tags_da_rimuovere = ['header', 'footer', 'nav', 'aside', 'script', 'style', 'noscript']
    for tag_name in tags_da_rimuovere:
        for tag in body_clone.find_all(tag_name):
            tag.decompose() # Rimuove il tag e tutto il suo contenuto
            
    # Rimuovi commenti
    for comment in body_clone.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Quello che rimane è (si spera) il contenuto principale
    content_html = body_clone.decode_contents()
    
    if not content_html.strip():
        print(f"    > ERRORE: Fallback fallito. Il body è vuoto dopo la pulizia.")
        return None

    return content_html

# --- 3. ESECUZIONE PRINCIPALE ---

def main():
    all_files = glob.glob(os.path.join(SITO_ORIGINALE_DIR, "**", "*.html"), recursive=True)
    if not all_files:
        print(f"ERRORE: Nessun file .html trovato in {SITO_ORIGINALE_DIR}.")
        return

    print(f"Trovati {len(all_files)} file HTML. Inizio estrazione...")
    
    content_data = {} # Il nostro database JSON finale
    files_estratti = 0
    files_con_errori = 0

    for file_path in all_files:
        relative_path = os.path.relpath(file_path, SITO_ORIGINALE_DIR).replace(os.path.sep, '/')
        url_path = '/' + os.path.splitext(relative_path)[0]
        
        print(f"Processando: {relative_path}...")
        
        try:
            with codecs.open(file_path, 'r', 'utf-8') as f_in:
                soup = BeautifulSoup(f_in, 'lxml')

            # 1. Estrai Titolo (H1 è più affidabile del <title> rotto)
            title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Titolo Mancante"
            title = re.sub(r'[\.\s]*calculator(s)?$', '', title, flags=re.IGNORECASE).strip()

            # 2. Estrai Descrizione
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description = description_tag['content'] if description_tag and description_tag.get('content') else f"Scopri di più su {title}."

            # 3. Estrai Lingua (default 'en')
            lang = soup.find('html').get('lang', 'en') if soup.find('html') else 'en'
            
            # 4. Estrai Contenuto Principale (la parte difficile)
            main_content = extract_main_content(soup)
            
            if main_content:
                # 5. Salva i "gioielli" nel nostro database
                content_data[url_path] = {
                    "lang": lang,
                    "title": title,
                    "description": description,
                    "main_html": main_content
                }
                files_estratti += 1
            else:
                print(f"  > ERRORE: Impossibile estrarre il contenuto per {relative_path}.")
                files_con_errori += 1
                
        except Exception as e:
            print(f"--- ERRORE CRITICO durante l'analisi di {relative_path}: {e}")
            files_con_errori += 1

    # --- 4. SALVATAGGIO DEL DATABASE DI CONTENUTO ---
    try:
        with codecs.open(CONTENT_FILE_OUT, 'w', 'utf-8') as f_out:
            json.dump(content_data, f_out, indent=2, ensure_ascii=False)
        
        print("\n--- Estrazione completata! ---")
        print(f"Contenuto estratto con successo da: {files_estratti} file.")
        print(f"File saltati per errori: {files_con_errori}")
        print(f"DATABASE DI CONTENUTO salvato in: {CONTENT_FILE_OUT}")

    except Exception as e:
        print(f"ERRORE CRITICO durante il salvataggio di {CONTENT_FILE_OUT}: {e}")

if __name__ == "__main__":
    main()