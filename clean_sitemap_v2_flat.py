import os
import codecs
import json
import re

print("Avvio Script di Pulizia Mappa (clean_sitemap_v2_flat)...")

# --- 1. CONFIGURAZIONE PERCORSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- MODIFICA: Legge il nuovo file "flat" ---
FILE_MAPPA_SPORCA = os.path.join(BASE_DIR, "sitemap_data_dirty_flat.json") 
# --- MODIFICA: Salva in un nuovo file "flat" ---
FILE_MAPPA_PULITA = os.path.join(BASE_DIR, "sitemap_data_CLEANED_flat.json")

# --- 2. REGOLE DI PULIZIA ---
REGOLE_DI_UNIONE = {
    # Categorie Principali
    "Math & Conversion": "Math & Conversions",
    "Math & Conversion Calculators": "Math & Conversions",
    "Math": "Math & Conversions",
    "Unit Conversions": "Math & Conversions", # Sposta da sub a main
    "Coordinate Conversions": "Math & Conversions", # Sposta da sub a main
    "Speed Conversions": "Math & Conversions", # Sposta da sub a main
    "Energy Conversions": "Math & Conversions", # Sposta da sub a main
    "Geometry": "Math & Conversions", # Sposta da sub a main
    "Basic Arithmetic": "Math & Conversions", # Sposta da sub a main
    "Pressure": "Math & Conversions", # Sposta da sub a main
    
    "Everyday Life": "Lifestyle & Everyday",
    "Lifestyle": "Lifestyle & Everyday",
    "Lifestyle Everyday": "Lifestyle & Everyday",
    "Lifestyle & Everyday Calculators": "Lifestyle & Everyday",
    "Lifestyle & Everyday Life": "Lifestyle & Everyday",
    "Hobbies": "Lifestyle & Everyday", # Sposta da sub a main
    
    "Health & Fitness Calculators": "Health & Fitness",
    "Nutrition": "Health & Fitness", # Sposta da sub a main

    "Construction DIY": "Construction & DIY",
    "Construction": "Construction & DIY",
    "Construction & DIY Calculators": "Construction & DIY",
    "Materials": "Construction & DIY", # Sposta da sub a main
    "Concrete Mix Design": "Construction & DIY", # Sposta da sub a main
    
    "Finance Calculators": "Finance",
    "Business": "Finance", # Sposta da sub a main
    "Investment": "Finance", # Sposta da sub a main
    "Loans & Debt": "Finance", # Sposta da sub a main
    "Mortgage & Real Estate": "Finance", # Sposta da sub a main
    "Taxation": "Finance", # Sposta da sub a main
    "US Taxation (Federal)": "Finance", # Sposta da sub a main
    "US Taxation (State)": "Finance", # Sposta da sub a main
    "UK Taxation": "Finance", # Sposta da sub a main
    "German Taxation": "Finance", # Sposta da sub a main

    "Science Calculators": "Science",
    "Chemistry": "Science", # Sposta da sub a main
    "Physics": "Science", # Sposta da sub a main
    "Biology": "Science", # Sposta da sub a main
    
    "Structural": "Engineering", # Sposta da sub a main
    "Mechanical": "Engineering", # Sposta da sub a main
    "Electrical (US NEC)": "Engineering", # Sposta da sub a main
    "Civil (ASCE 7-22)": "Engineering", # Sposta da sub a main
    "CCTV & Surveillance": "Engineering", # Sposta da sub a main
    "Networking": "Engineering", # Sposta da sub a main

    # Rimuovi categorie spazzatura
    "Category": "IGNORE",
    "About": "IGNORE",
    "Miscellaneous": "IGNORE", # Troppo generico, meglio lasciare che l'AI classifichi
    "Statistics & Probability": "IGNORE" # Troppo vago, unisci a Math
}

TITOLI_SPAZZATURA = [
    "titolo mancante",
    "<!doctype html>",
    "calculator title",
    "blog & resources",
    "frequently asked questions",
    "accessibility statement",
    "help center",
    "about calcdomain"
]

# --- 3. FUNZIONE DI PULIZIA ---
def clean_sitemap(dirty_data):
    clean_data = {}
    stats = {"unite": 0, "pulite": 0, "spazzatura_rimossa": 0}

    for category_sporco, subcategories in dirty_data.items():
        
        category_pulito = REGOLE_DI_UNIONE.get(category_sporco, category_sporco)
        
        if category_pulito == "IGNORE":
            stats["spazzatura_rimossa"] += sum(len(pages) for pages in subcategories.values())
            continue
            
        if category_pulito not in clean_data:
            clean_data[category_pulito] = {}

        for sub_sporco, pages in subcategories.items():
            
            # Se la subcategoria è stata unita alla categoria principale, 
            # usa "Generale" come nuova sottocategoria.
            if category_sporco != category_pulito:
                 sub_pulito = "Generale"
            else:
                 sub_pulito = REGOLE_DI_UNIONE.get(sub_sporco, sub_sporco)
            
            if sub_pulito == "IGNORE":
                stats["spazzatura_rimossa"] += len(pages)
                continue
                
            if sub_pulito not in clean_data[category_pulito]:
                clean_data[category_pulito][sub_pulito] = []

            for page in pages:
                page_title_lower = page['title'].lower().strip()
                is_junk = False
                for junk in TITOLI_SPAZZATURA:
                    if junk in page_title_lower:
                        is_junk = True
                        stats["spazzatura_rimossa"] += 1
                        break
                
                if not is_junk:
                    page['title'] = re.sub(r'[\.\s]*calculator(s)?$', '', page['title'], flags=re.IGNORECASE).strip()
                    
                    if page not in clean_data[category_pulito][sub_pulito]:
                        clean_data[category_pulito][sub_pulito].append(page)
                        stats["pulite"] += 1
                
            if category_sporco != category_pulito or sub_sporco != sub_pulito:
                stats["unite"] += len(pages)

    return clean_data, stats

# --- 4. ESECUZIONE PRINCIPALE ---
def main():
    try:
        with codecs.open(FILE_MAPPA_SPORCA, 'r', 'utf-8') as f:
            sitemap_data_dirty = json.load(f)
    except FileNotFoundError:
        print(f"ERRORE: File '{FILE_MAPPA_SPORCA}' non trovato.")
        print("Assicurati di aver prima eseguito 'build_sitemap_v3_flat.py'.")
        return
    except Exception as e:
        print(f"ERRORE durante la lettura del file JSON: {e}")
        return

    sitemap_data_cleaned, stats = clean_sitemap(sitemap_data_dirty)

    try:
        with codecs.open(FILE_MAPPA_PULITA, 'w', 'utf-8') as f_out:
            json.dump(sitemap_data_cleaned, f_out, indent=2, ensure_ascii=False)
        
        print("\n--- Pulizia (v2 - Flat) completata! ---")
        print(f"Pagine unite sotto nuove categorie: {stats['unite']}")
        print(f"Titoli/Pagine spazzatura rimossi: {stats['spazzatura_rimossa']}")
        print(f"Totale pagine pulite mappate: {stats['pulite']}")
        print(f"MAPPA PULITA salvata in: {FILE_MAPPA_PULITA}")

    except Exception as e:
        print(f"ERRORE CRITICO durante il salvataggio della mappa pulita: {e}")

if __name__ == "__main__":
    main()