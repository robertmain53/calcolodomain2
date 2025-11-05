import os
import codecs
import json
import re

print("Avvio Script di Pulizia Mappa (clean_sitemap.py)...")

# --- 1. CONFIGURAZIONE PERCORSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rinomina il file che hai appena creato in "_dirty.json"
FILE_MAPPA_SPORCA = os.path.join(BASE_DIR, "sitemap_data_dirty.json") 
FILE_MAPPA_PULITA = os.path.join(BASE_DIR, "sitemap_data_CLEANED.json")

# --- 2. ⚠️ LE REGOLE DI PULIZIA ---
# Qui definiamo come unire le categorie.
# 'Nome Sporco': 'Nome Pulito Corretto'
# AGGIUNGI QUI ALTRE REGOLE CHE NOTI
REGOLE_DI_UNIONE = {
    # Categorie Principali
    "Math & Conversion": "Math & Conversions",
    "Math & Conversion Calculators": "Math & Conversions",
    "Math": "Math & Conversions",
    
    "Everyday Life": "Lifestyle & Everyday",
    "Lifestyle": "Lifestyle & Everyday",
    "Lifestyle Everyday": "Lifestyle & Everyday",
    "Lifestyle & Everyday Calculators": "Lifestyle & Everyday",
    "Lifestyle & Everyday Life": "Lifestyle & Everyday",
    
    "Health & Fitness Calculators": "Health & Fitness",
    
    "Construction DIY": "Construction & DIY",
    "Construction": "Construction & DIY",
    "Construction & DIY Calculators": "Construction & DIY",

    "Finance Calculators": "Finance",
    
    "Science Calculators": "Science",
    "Chemistry": "Science",
    "Physics": "Science",
    "Biology": "Science",

    # Sottocategorie (Esempi)
    "Time and Date": "Time & Date",
    "Time and date": "Time & Date",
    "Health metrics": "Health Metrics",
    "Mortgages": "Mortgage & Real Estate",
    "Personal Loans": "Loans & Debt",
    "Retirement Calculators": "Retirement",
    
    # Rimuovi categorie spazzatura
    "Category": "IGNORE",
    "About": "IGNORE",
}

# Lista di titoli spazzatura da rimuovere
TITOLI_SPAZZATURA = [
    "titolo mancante",
    "<!doctype html>",
    "calculator title"
]

# --- 3. FUNZIONE DI PULIZIA ---

def clean_sitemap(dirty_data):
    clean_data = {}
    stats = {"unite": 0, "pulite": 0, "spazzatura_rimossa": 0}

    for category_sporco, subcategories in dirty_data.items():
        
        # 1. Pulisci il nome della Categoria Principale
        category_pulito = REGOLE_DI_UNIONE.get(category_sporco, category_sporco)
        
        if category_pulito == "IGNORE":
            stats["spazzatura_rimossa"] += len(subcategories)
            continue
            
        if category_pulito not in clean_data:
            clean_data[category_pulito] = {}

        for sub_sporco, pages in subcategories.items():
            
            # 2. Pulisci il nome della Sottocategoria
            sub_pulito = REGOLE_DI_UNIONE.get(sub_sporco, sub_sporco)
            
            if sub_pulito == "IGNORE":
                stats["spazzatura_rimossa"] += len(pages)
                continue
                
            if sub_pulito not in clean_data[category_pulito]:
                clean_data[category_pulito][sub_pulito] = []

            # 3. Pulisci le singole Pagine (titoli, ecc.)
            for page in pages:
                # Pulisci il titolo
                page_title_lower = page['title'].lower().strip()
                
                # Controlla se è un titolo spazzatura
                is_junk = False
                for junk in TITOLI_SPAZZATURA:
                    if junk in page_title_lower:
                        is_junk = True
                        stats["spazzatura_rimossa"] += 1
                        break
                
                if not is_junk:
                    # Rimuovi "calculator" o "calculators" dalla fine dei titoli, se presente
                    page['title'] = re.sub(r'[\.\s]*calculator(s)?$', '', page['title'], flags=re.IGNORECASE).strip()
                    
                    # Aggiungi la pagina pulita alla mappa pulita
                    # Evita duplicati (alcune pagine erano in più categorie)
                    if page not in clean_data[category_pulito][sub_pulito]:
                        clean_data[category_pulito][sub_pulito].append(page)
                        stats["pulite"] += 1
                
            if category_sporco != category_pulito or sub_sporco != sub_pulito:
                stats["unite"] += len(pages)

    return clean_data, stats

# --- 4. ESECUZIONE PRINCIPALE ---

def main():
    # Carica la mappa sporca
    try:
        with codecs.open(FILE_MAPPA_SPORCA, 'r', 'utf-8') as f:
            sitemap_data_dirty = json.load(f)
    except FileNotFoundError:
        print(f"ERRORE: File '{FILE_MAPPA_SPORCA}' non trovato.")
        print("Per favore, rinomina il tuo file 'sitemap_data.json' in 'sitemap_data_dirty.json' e riprova.")
        return
    except Exception as e:
        print(f"ERRORE durante la lettura del file JSON: {e}")
        return

    # Esegui la pulizia
    sitemap_data_cleaned, stats = clean_sitemap(sitemap_data_dirty)

    # Salva la mappa pulita
    try:
        with codecs.open(FILE_MAPPA_PULITA, 'w', 'utf-8') as f_out:
            json.dump(sitemap_data_cleaned, f_out, indent=2, ensure_ascii=False)
        
        print("\n--- Pulizia completata! ---")
        print(f"Pagine unite sotto nuove categorie: {stats['unite']}")
        print(f"Titoli/Pagine spazzatura rimossi: {stats['spazzatura_rimossa']}")
        print(f"Totale pagine pulite mappate: {stats['pulite']}")
        print(f"MAPPA PULITA salvata in: {FILE_MAPPA_PULITA}")

    except Exception as e:
        print(f"ERRORE CRITICO durante il salvataggio della mappa pulita: {e}")

if __name__ == "__main__":
    main()