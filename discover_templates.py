import os
import glob
import codecs
import csv
from bs4 import BeautifulSoup

print("Avvio Script di Diagnosi e Classificazione Template...")

# --- Configurazione Percorsi ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITO_ORIGINALE_DIR = os.path.join(BASE_DIR, "sito_originale")

# Creiamo un report CSV, molto più facile da analizzare
REPORT_FILE = os.path.join(BASE_DIR, "template_report.csv")

# Dizionario per raggruppare i file per "profilo"
template_groups = {}

# --- Scansione File ---
file_list = glob.glob(os.path.join(SITO_ORIGINALE_DIR, "**", "*.html"), recursive=True)

if not file_list:
    print(f"ERRORE: Nessun file .html trovato in {SITO_ORIGINALE_DIR}.")
    exit()

print(f"Trovati {len(file_list)} file HTML. Inizio analisi strutturale...")

file_analizzati = 0
file_con_errori = 0

for file_path in file_list:
    try:
        relative_path = os.path.relpath(file_path, SITO_ORIGINALE_DIR).replace(os.path.sep, '/')
        
        with codecs.open(file_path, 'r', 'utf-8') as f_in:
            soup = BeautifulSoup(f_in, 'lxml')

        # --- 1. ESTRAZIONE DEI "SINTOMI" STRUTTURALI ---
        
        # Usiamo find_all() per CONTARE le occorrenze
        head_count = len(soup.find_all('head'))
        body_count = len(soup.find_all('body'))
        header_count = len(soup.find_all('header'))
        footer_count = len(soup.find_all('footer'))
        aside_count = len(soup.find_all('aside')) # Controlla sidebar esistenti
        
        # Logica di controllo Breadcrumb (semplificata: 0 o 1+)
        breadcrumb_count = 0
        # Usiamo 'string' invece di 'text' per evitare il DeprecationWarning
        home_link = soup.find('a', string=lambda t: t and 'Home' in t)
        if home_link:
            breadcrumb_count = 1 # Trovata!

        # --- 2. CREAZIONE DEL "PROFILO TEMPLATE" ---
        # Creiamo una "chiave" unica per questo set di sintomi
        profile_key = (
            f"head:{head_count}, "
            f"body:{body_count}, "
            f"header:{header_count}, "
            f"footer:{footer_count}, "
            f"aside:{aside_count}, "
            f"breadcrumb:{breadcrumb_count}"
        )

        # --- 3. RAGGRUPPAMENTO ---
        if profile_key not in template_groups:
            template_groups[profile_key] = []
            
        template_groups[profile_key].append(relative_path)
        file_analizzati += 1

    except Exception as e:
        print(f"--- ERRORE durante l'analisi di {relative_path}: {e}")
        file_con_errori += 1

# --- 4. STAMPA DEL REPORT A CONSOLE (SINTESI) ---
print("\n--- Report di Classificazione Template (Sintesi) ---")

# Ordina i gruppi dal più comune al meno comune
sorted_groups = sorted(template_groups.items(), key=lambda item: len(item[1]), reverse=True)

for profile, files in sorted_groups:
    count = len(files)
    print(f"\nProfilo: [{profile}]")
    print(f"  File Trovati: {count}")
    # Mostra i primi 3 file di esempio per questo gruppo
    print(f"  Esempi: {', '.join(files[:3])}...")

# --- 5. SALVATAGGIO DEL REPORT COMPLETO SU CSV ---
try:
    with open(REPORT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Scrivi l'intestazione
        writer.writerow(['Profilo_Template', 'Conteggio_File', 'Esempi_File (primi 10)'])
        
        for profile, files in sorted_groups:
            count = len(files)
            # Prendi fino a 10 esempi
            examples = ", ".join(files[:10])
            writer.writerow([profile, count, examples])
            
    print("\n--- Analisi completata ---")
    print(f"File totali analizzati: {file_analizzati}")
    print(f"File saltati per errori: {file_con_errori}")
    print(f"REPORT COMPLETO SALVATO IN: {REPORT_FILE}")

except Exception as e:
    print(f"ERRORE CRITICO durante il salvataggio del CSV: {e}")