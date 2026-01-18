import os
import glob
import codecs
from bs4 import BeautifulSoup

print("Avvio script di automazione...")

# --- 1. CONFIGURAZIONE DEI PERCORSI ---
# Assicura che lo script trovi i file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "template_perfetti")
SITO_ORIGINALE_DIR = os.path.join(BASE_DIR, "sito_originale")
SITO_MODIFICATO_DIR = os.path.join(BASE_DIR, "sito_modificato")

# Assicurati  che la cartella di destinazione esista
os.makedirs(SITO_MODIFICATO_DIR, exist_ok=True)


# --- 2. CARICA I "MATTONI" (I TEMPLATE) ---
# Leggiamo i nostri file "Gold Standard" una sola volta
try:
    with codecs.open(os.path.join(TEMPLATE_DIR, "header_perfetto.html"), 'r', 'utf-8') as f:
        # Usiamo .prettify() per una formattazione pulita
        header_perfetto_html = f.read()

    with codecs.open(os.path.join(TEMPLATE_DIR, "footer_perfetto.html"), 'r', 'utf-8') as f:
        footer_perfetto_html = f.read()
        
    print("Template 'header_perfetto.html' e 'footer_perfetto.html' caricati.")

except FileNotFoundError as e:
    print(f"ERRORE: File template non trovato. Controlla la cartella 'template_perfetti'. Dettagli: {e}")
    exit()


# --- 3. IL CICLO PRINCIPALE (LA FABBRICA) ---
# Cerca TUTTI i file .html nella cartella di origine
file_list = glob.glob(os.path.join(SITO_ORIGINALE_DIR, "**", "*.html"), recursive=True)

if not file_list:
    print(f"ERRORE: Nessun file .html trovato in {SITO_ORIGINALE_DIR}. Controlla i percorsi.")
    exit()

print(f"Trovati {len(file_list)} file HTML. Inizio elaborazione...")

file_processati = 0
file_con_errori = 0

for file_path in file_list:
    try:
        # Calcola il percorso di salvataggio
        relative_path = os.path.relpath(file_path, SITO_ORIGINALE_DIR)
        output_path = os.path.join(SITO_MODIFICATO_DIR, relative_path)
        
        # Assicura che le sottocartelle esistano (es. /sito_modificato/finance/)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Leggi il file HTML originale
        with codecs.open(file_path, 'r', 'utf-8') as f_in:
            soup = BeautifulSoup(f_in, 'lxml')

        # --- 4. LA CHIRURGIA (TROVA E SOSTITUISCI) ---

        # Sostituisci l'HEADER
        vecchio_header = soup.find('header')
        if vecchio_header:
            # Crea un nuovo tag "header" partendo dal testo del template
            nuovo_header = BeautifulSoup(header_perfetto_html, 'lxml').header
            vecchio_header.replace_with(nuovo_header)
        else:
            print(f"  > ATTENZIONE: Nessun <header> trovato in {relative_path}")

        # Sostituisci il FOOTER
        vecchio_footer = soup.find('footer')
        if vecchio_footer:
            # Crea un nuovo tag "footer" partendo dal testo del template
            nuovo_footer = BeautifulSoup(footer_perfetto_html, 'lxml').footer
            vecchio_footer.replace_with(nuovo_footer)
        else:
            print(f"  > ATTENZIONE: Nessun <footer> trovato in {relative_path}")

        # --- 5. INIEZIONE DEGLI SCRIPT ---
        
        # Rimuovi i vecchi preload inutili (se esistono)
        vecchi_preload = soup.find_all('link', attrs={'rel': 'preload', 'as': 'script'})
        for link in vecchi_preload:
            if 'mobile-menu.js' in link.get('href', '') or 'page-enhancements.js' in link.get('href', ''):
                link.decompose() # Rimuove il tag

        # Trova la fine del <body>
        body_tag = soup.find('body')
        if body_tag:
            # Assicurati che gli script non siano già presenti (per sicurezza)
            script_da_aggiungere = [
                "/assets/js/script_menu.js",
                "/assets/js/script_faq.js",  # Aggiungiamo già quello per le FAQ
                "search.js"  # Necessario per la barra di ricerca nell'header
            ]
            
            for script_src in script_da_aggiungere:
                if not soup.find('script', src=script_src):
                    nuovo_script_tag = soup.new_tag("script", src=script_src)
                    nuovo_script_tag.attrs['defer'] = True # Aggiungi 'defer' per performance
                    body_tag.append(nuovo_script_tag)
        else:
            print(f"  > ATTENZIONE: Nessun <body> trovato in {relative_path}")

        # --- 6. SALVA IL FILE MODIFICATO ---
        with codecs.open(output_path, 'w', 'utf-8') as f_out:
            # Usiamo .prettify() per un output pulito e leggibile
            f_out.write(soup.prettify())
            
        file_processati += 1

    except Exception as e:
        print(f"--- ERRORE DURANTE L'ELABORAZIONE di {file_path} ---")
        print(f"  Dettagli: {e}")
        file_con_errori += 1

# --- 7. RIEPILOGO ---
print("\n--- Elaborazione completata ---")
print(f"File totali processati: {file_processati}")
print(f"File saltati per errori: {file_con_errori}")
print(f"I file modificati si trovano in: {SITO_MODIFICATO_DIR}")