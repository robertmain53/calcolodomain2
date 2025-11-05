import os
import glob
import codecs
import json
import time
import re
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- 1. CONFIGURAZIONE OBBLIGATORIA ---


# ⚠️ INCOLLA QUI LA TUA CHIAVE API DI GOOGLE AI STUDIO
GOOGLE_API_KEY = "AIzaSyCY6MvFRvSSwS_k0oVH6KugPU5oX7PF_N8"

BATCH_SIZE = 50

# --- Configurazione Percorsi ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITO_ORIGINALE_DIR = os.path.join(BASE_DIR, "sito_originale")
SITEMAP_FILE_DA_LEGGERE = os.path.join(BASE_DIR, "sitemap_data_CLEANED.json")
SITEMAP_FILE_FINALE = os.path.join(BASE_DIR, "sitemap_data_FINAL.json")

# --- 2. FUNZIONI DELLO SCRIPT ---

def load_map_and_find_orphans(sitemap_path, site_dir):
    """Carica la mappa JSON PULITA e trova tutti i file HTML che non sono ancora mappati."""
    
    try:
        with codecs.open(sitemap_path, 'r', 'utf-8') as f:
            sitemap_data = json.load(f)
    except FileNotFoundError:
        print(f"ERRORE: File '{sitemap_path}' non trovato. Assicurati di aver eseguito 'clean_sitemap.py'.")
        return None, None
    except json.JSONDecodeError:
        print(f"ERRORE: File '{sitemap_path}' corrotto o vuoto.")
        return None, None

    known_urls = set()
    category_list = set()
    
    for category, subcategories in sitemap_data.items():
        for subcategory, pages in subcategories.items():
            category_list.add(f"{category} > {subcategory}")
            for page in pages:
                known_urls.add(page['url'])
    
    print(f"Mappa PULITA caricata. Trovati {len(known_urls)} URL conosciuti.")
    print(f"Trovate {len(category_list)} categorie uniche e pulite.")

    orphans = []
    all_files = glob.glob(os.path.join(site_dir, "**", "*.html"), recursive=True)
    
    for file_path in all_files:
        relative_path = os.path.relpath(file_path, site_dir).replace(os.path.sep, '/')
        url_path = '/' + os.path.splitext(relative_path)[0]
        
        if url_path not in known_urls and relative_path != 'index.html':
            try:
                with codecs.open(file_path, 'r', 'utf-8') as f_in:
                    soup = BeautifulSoup(f_in, 'lxml')
                
                h1_text = "Titolo Mancante"
                if soup.find('h1'):
                    h1_text = soup.find('h1').get_text(strip=True)
                
                h1_text = h1_text.lower().replace("<!doctype html>", "").strip()
                h1_text = re.sub(r'[\.\s]*calculator(s)?$', '', h1_text, flags=re.IGNORECASE).strip()

                if h1_text and "titolo mancante" not in h1_text and "calculator title" not in h1_text:
                    orphans.append({
                        "url": url_path,
                        "title": h1_text
                    })
            except Exception as e:
                print(f"  > Errore leggendo l'orfano {relative_path}: {e}")

    print(f"Trovati {len(orphans)} file 'orfani' puliti da classificare.")
    return sitemap_data, orphans, sorted(list(category_list))


def classify_pages_with_ai(orphans_batch, category_list_str):
    """Chiama l'API Gemini per classificare un blocco di titoli."""
    
    titles_to_classify = [f"'{page['title']}' (URL: {page['url']})" for page in orphans_batch]
    titles_list_str = "\n".join(titles_to_classify)
    
    prompt = f"""
    Sei un assistente esperto di architettura di siti web e SEO.
    Il tuo compito è classificare un elenco di nuovi titoli di pagina in un *elenco esistente* di categorie.

    ELENCO CATEGORIE ESISTENTI:
    ---
    {category_list_str}
    ---

    PAGINE DA CLASSIFICARE:
    ---
    {titles_list_str}
    ---

    ISTRUZIONI:
    1.  Rispondi *ESCLUSIVAMENTE* con un oggetto JSON valido.
    2.  NON creare nuove categorie. Se un titolo non corrisponde perfettamente, scegli la categoria "Generale" più vicina (es. "Finance > Generale").
    3.  La chiave del JSON deve essere l'URL della pagina (che ti ho fornito tra parentesi).
    4.  Il valore deve essere la stringa *esatta* della categoria scelta.
    5.  Se un titolo è spazzatura (es. "Titolo Mancante", URL di test), classificalo come "IGNORE".

    ESEMPIO DI OUTPUT:
    {{
      "/purchasing-power-parity": "Finance > Generale",
      "/project-roi": "Finance > Generale",
      "/rems-to-pixels": "Math & Conversions > Unit Conversions",
      "/googlec8c0eedfe44345b9": "IGNORE"
    }}
    """
    
    # --- ⬇️ ECCO LA MODIFICA ⬇️ ---
    # Sostituiamo il modello 'gemini-1.5-flash-latest' con 'gemini-pro'
    # che è il modello standard, stabile e ampiamente disponibile.
    model = genai.GenerativeModel('gemini-pro')
    # --- ⬆️ FINE DELLA MODIFICA ⬆️ ---
    
    try:
        response = model.generate_content(prompt)
        json_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(json_response)
    
    except Exception as e:
        print(f"    ERRORE API: {e}")
        return {page['url']: "ERROR" for page in orphans_batch}

# --- 3. ESECUZIONE PRINCIPALE (MAIN) ---
def main():
    if GOOGLE_API_KEY == "INCOLLA_LA_TUA_CHIAVE_API_QUI":
        print("ERRORE: Devi inserire la tua GOOGLE_API_KEY nello script prima di eseguirlo.")
        return

    try:
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception as e:
        print(f"Errore di configurazione API: {e}")
        return

    sitemap_data, orphans, category_list = load_map_and_find_orphans(SITEMAP_FILE_DA_LEGGERE, SITO_ORIGINALE_DIR)
    
    if sitemap_data is None or not orphans:
        print("Mappa non trovata o nessun orfano da processare. Uscita.")
        return

    category_list_str = "\n".join(category_list)
    total_orphans = len(orphans)
    classified_count = 0
    
    for i in range(0, total_orphans, BATCH_SIZE):
        batch = orphans[i:i + BATCH_SIZE]
        print(f"\nProcessando blocco {i//BATCH_SIZE + 1} di {total_orphans//BATCH_SIZE + 1} (file {i+1}-{min(i+BATCH_SIZE, total_orphans)})...")
        
        results = classify_pages_with_ai(batch, category_list_str)
        
        for orphan_page in batch:
            page_url = orphan_page['url']
            
            if page_url in results:
                classification = results[page_url]
                
                if classification not in ["IGNORE", "ERROR"]:
                    try:
                        category, subcategory = classification.split(' > ')
                        
                        page_info = {
                            "title": orphan_page['title'],
                            "url": page_url
                        }
                        
                        if category not in sitemap_data: sitemap_data[category] = {}
                        if subcategory not in sitemap_data[category]: sitemap_data[category][subcategory] = []
                        
                        if page_info not in sitemap_data[category][subcategory]:
                            sitemap_data[category][subcategory].append(page_info)
                            classified_count += 1
                        
                    except ValueError:
                        print(f"  > Errore di formato AI per {page_url}: classificazione '{classification}' scartata (probabilmente non conteneva ' > ').")
                    except Exception as e:
                        print(f"  > Errore inserimento mappa per {page_url}: {e}")
                else:
                    print(f"  > Classificazione '{classification}' per {page_url}. Scartato.")
            else:
                print(f"  > ATTENZIONE: L'AI non ha restituito una classificazione per {page_url}.")

        # Pausa per rispettare i rate limit
        time.sleep(1) 

    # 4. Salva la mappa FINALE
    try:
        with codecs.open(SITEMAP_FILE_FINALE, 'w', 'utf-8') as f_out:
            json.dump(sitemap_data, f_out, indent=2, ensure_ascii=False)
        
        print("\n--- Arricchimento completato! ---")
        print(f"Classificati e aggiunti con successo {classified_count} nuovi file.")
        print(f"La tua mappa del sito completa è stata salvata in: {SITEMAP_FILE_FINALE}")

    except Exception as e:
        print(f"ERRORE CRITICO durante il salvataggio della mappa aggiornata: {e}")

if __name__ == "__main__":
    main()