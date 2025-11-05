import google.generativeai as genai
import os

# --- 1. CONFIGURAZIONE OBBLIGATORIA ---

# ⚠️ INCOLLA QUI LA TUA STESSA CHIAVE API DI GOOGLE AI STUDIO
GOOGLE_API_KEY = "AIzaSyCY6MvFRvSSwS_k0oVH6KugPU5oX7PF_N8"

# --- ESECUZIONE ---

def main():
    if GOOGLE_API_KEY == "INCOLLA_LA_TUA_CHIAVE_API_QUI":
        print("ERRORE: Apri questo script (list_my_models.py) e incolla la tua GOOGLE_API_KEY.")
        return

    try:
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception as e:
        print(f"Errore di configurazione API: {e}")
        return

    print(f"--- Richiesta modelli disponibili per la tua API Key... ---")
    
    found_model = False
    try:
        # Itera su tutti i modelli che la tua chiave può vedere
        for model in genai.list_models():
            # Il nostro script `enrich` usa il metodo 'generateContent'.
            # Dobbiamo trovare un modello che lo supporti.
            if 'generateContent' in model.supported_generation_methods:
                print(f"\n✅ Modello Trovato!")
                print(f"  Nome Modello (da copiare): {model.name}")
                print(f"  Descrizione: {model.description}")
                print(f"  Metodi Supportati: {model.supported_generation_methods}")
                found_model = True

        if not found_model:
            print("\n--- ERRORE ---")
            print("Nessun modello trovato che supporti 'generateContent'.")
            print("Possibili cause:")
            print("1. La tua API key non è corretta o non è ancora attiva.")
            print("2. L'API 'Generative Language' (o 'Vertex AI') non è abilitata nel tuo progetto Google Cloud.")
            print("3. C'è un problema temporaneo con i server di Google.")
        else:
             print("\nCopia uno dei nomi modello '✅ Trovato!' (es. 'models/gemini-1.0-pro') e incollalo nello script 'enrich_sitemap_v3.py'.")

    except Exception as e:
        print(f"\n--- ERRORE DURANTE LA CHIAMATA API 'list_models' ---")
        print(f"Dettagli: {e}")
        print("Questo di solito accade se la chiave API è completamente invalida o bloccata.")

if __name__ == "__main__":
    main()