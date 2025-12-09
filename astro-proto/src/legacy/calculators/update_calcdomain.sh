#!/bin/bash

# CalcDomain Complete Update Script
# Esegue tutti gli aggiornamenti necessari per il sistema di ricerca

set -e  # Exit on error

echo "========================================"
echo "CalcDomain Complete Update Script"
echo "========================================"
echo ""

# Check if required scripts exist
check_dependencies() {
    echo "Verificando dipendenze..."
    
    if [ ! -f "update_calcdomain_site.py" ]; then
        echo "ERRORE: update_calcdomain_site.py non trovato"
        echo "Assicurati di aver scaricato tutti gli script necessari"
        exit 1
    fi
    
    if [ ! -f "generate_data_files.py" ]; then
        echo "ERRORE: generate_data_files.py non trovato"
        echo "Assicurati di aver scaricato tutti gli script necessari"
        exit 1
    fi
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        if ! command -v python &> /dev/null; then
            echo "ERRORE: Python non trovato"
            echo "Installa Python 3.x per continuare"
            exit 1
        else
            PYTHON_CMD="python"
        fi
    else
        PYTHON_CMD="python3"
    fi
    
    echo "Dipendenze verificate con successo"
    echo "Usando: $($PYTHON_CMD --version)"
    echo ""
}

# Backup current files
create_backup() {
    echo "Creando backup dei file attuali..."
    
    BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup HTML files
    if ls *.html 1> /dev/null 2>&1; then
        cp *.html "$BACKUP_DIR/" 2>/dev/null || true
    fi
    
    # Backup subcategories if exists
    if [ -d "subcategories" ]; then
        mkdir -p "$BACKUP_DIR/subcategories"
        cp subcategories/*.html "$BACKUP_DIR/subcategories/" 2>/dev/null || true
    fi
    
    # Backup data files if they exist
    cp calculators-data.json "$BACKUP_DIR/" 2>/dev/null || true
    cp sitemap.xml "$BACKUP_DIR/" 2>/dev/null || true
    cp robots.txt "$BACKUP_DIR/" 2>/dev/null || true
    
    echo "Backup creato in: $BACKUP_DIR"
    echo ""
}

# Update HTML files with new search system
update_html_files() {
    echo "========================================"
    echo "STEP 1: Aggiornamento file HTML"
    echo "========================================"
    echo ""
    
    echo "Aggiornando tutti i file HTML con il nuovo sistema di ricerca..."
    echo "Questo processo:"
    echo "- Sostituira' tutti gli header esistenti"
    echo "- Aggiungera' il CSS inline per la ricerca"
    echo "- Includera' search.js in tutte le pagine"
    echo "- Aggiornera' la homepage con hero search"
    echo ""
    
    read -p "Continuare? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        $PYTHON_CMD update_calcdomain_site.py
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "SUCCESS: File HTML aggiornati con successo"
        else
            echo ""
            echo "ERRORE: Problema durante l'aggiornamento dei file HTML"
            exit 1
        fi
    else
        echo "Aggiornamento HTML saltato"
    fi
    
    echo ""
}

# Generate data files
generate_data_files() {
    echo "========================================"
    echo "STEP 2: Generazione file dati"
    echo "========================================"
    echo ""
    
    echo "Generando calculators-data.json, sitemap.xml e robots.txt..."
    echo "Scansionera' tutti i file HTML esistenti per creare i metadati"
    echo ""
    
    # Get base URL from user
    read -p "Inserisci l'URL base del sito (default: https://calcdomain.com): " BASE_URL
    BASE_URL=${BASE_URL:-"https://calcdomain.com"}
    
    echo "Usando URL base: $BASE_URL"
    echo ""
    
    $PYTHON_CMD generate_data_files.py --base-url "$BASE_URL" --dir "."
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "SUCCESS: File dati generati con successo"
        
        # Show statistics
        if [ -f "calculators-data.json" ]; then
            CALC_COUNT=$(grep -o '"slug":' calculators-data.json | wc -l)
            echo "- calculators-data.json: $CALC_COUNT calcolatori"
        fi
        
        if [ -f "sitemap.xml" ]; then
            URL_COUNT=$(grep -c '<url>' sitemap.xml)
            echo "- sitemap.xml: $URL_COUNT URL"
        fi
        
        if [ -f "robots.txt" ]; then
            echo "- robots.txt: generato"
        fi
    else
        echo ""
        echo "ERRORE: Problema durante la generazione dei file dati"
        exit 1
    fi
    
    echo ""
}

# Test the search system
test_search_system() {
    echo "========================================"
    echo "STEP 3: Test sistema di ricerca"
    echo "========================================"
    echo ""
    
    echo "Verificando l'integrita' del sistema di ricerca..."
    
    # Check if search.js exists
    if [ ! -f "search.js" ]; then
        echo "ATTENZIONE: search.js non trovato"
        echo "Assicurati di aver creato search.js come indicato"
    else
        echo "- search.js: presente"
    fi
    
    # Check if search.html exists
    if [ ! -f "search.html" ]; then
        echo "ATTENZIONE: search.html non trovato"
        echo "Assicurati di aver creato search.html come indicato"
    else
        echo "- search.html: presente"
    fi
    
    # Check if calculators-data.json is valid
    if [ -f "calculators-data.json" ]; then
        if $PYTHON_CMD -m json.tool calculators-data.json > /dev/null 2>&1; then
            echo "- calculators-data.json: JSON valido"
        else
            echo "ERRORE: calculators-data.json non e' un JSON valido"
        fi
    fi
    
    # Check if sitemap.xml is valid
    if [ -f "sitemap.xml" ]; then
        if command -v xmllint &> /dev/null; then
            if xmllint --noout sitemap.xml 2>/dev/null; then
                echo "- sitemap.xml: XML valido"
            else
                echo "ATTENZIONE: sitemap.xml potrebbe avere problemi di formato"
            fi
        else
            echo "- sitemap.xml: presente (xmllint non disponibile per validazione)"
        fi
    fi
    
    echo ""
    echo "Test completati"
    echo ""
}

# Show next steps
show_next_steps() {
    echo "========================================"
    echo "PROSSIMI PASSI"
    echo "========================================"
    echo ""
    echo "1. Test locale:"
    echo "   - Apri il sito in un browser locale"
    echo "   - Testa la ricerca nell'header"
    echo "   - Visita search.html e testa la ricerca avanzata"
    echo "   - Verifica che i link ai calcolatori funzionino"
    echo ""
    echo "2. Deploy:"
    echo "   - Carica tutti i file sul tuo server"
    echo "   - Verifica che search.js e search.html siano accessibili"
    echo "   - Testa su dispositivi mobili"
    echo ""
    echo "3. SEO:"
    echo "   - Submetti sitemap.xml a Google Search Console"
    echo "   - Verifica robots.txt su Google Search Console"
    echo "   - Monitora l'indicizzazione delle nuove pagine"
    echo ""
    echo "4. Automazione GitHub (opzionale):"
    echo "   - Crea la cartella .github/workflows/"
    echo "   - Copia il file update-calcdomain.yml nella cartella"
    echo "   - Ad ogni push, i dati saranno aggiornati automaticamente"
    echo ""
    echo "5. Monitoring:"
    echo "   - Configura Google Analytics per tracciare le ricerche"
    echo "   - Monitora le query di ricerca piu' popolari"
    echo "   - Ottimizza i risultati basandoti sui dati utenti"
    echo ""
}

# Git operations
git_operations() {
    echo "========================================"
    echo "OPERAZIONI GIT (opzionale)"
    echo "========================================"
    echo ""
    
    if [ ! -d ".git" ]; then
        echo "Repository Git non trovato, saltando operazioni Git"
        return 0
    fi
    
    echo "Repository Git trovato"
    
    read -p "Vuoi fare commit delle modifiche? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Preparando commit..."
        
        # Add files
        git add .
        
        # Check if there are changes
        if git diff --cached --quiet; then
            echo "Nessuna modifica da committare"
        else
            # Create commit message
            TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
            
            if [ -f "calculators-data.json" ]; then
                CALC_COUNT=$(grep -o '"slug":' calculators-data.json | wc -l)
            else
                CALC_COUNT="unknown"
            fi
            
            git commit -m "feat: Implement CalcDomain search system

- Updated all HTML files with new search header
- Added inline CSS for search functionality  
- Generated calculators-data.json ($CALC_COUNT calculators)
- Created sitemap.xml and robots.txt
- Implemented responsive search with mobile support

Updated: $TIMESTAMP"
            
            echo "Commit creato con successo"
            
            read -p "Vuoi fare push al repository remoto? (y/N): " -n 1 -r
            echo ""
            
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                git push
                echo "Push completato"
            fi
        fi
    fi
    
    echo ""
}

# Main execution
main() {
    echo "Questo script aggiornera' completamente il tuo sito CalcDomain"
    echo "con il nuovo sistema di ricerca avanzato"
    echo ""
    
    # Check dependencies
    check_dependencies
    
    # Create backup
    read -p "Creare backup dei file attuali? (Y/n): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        create_backup
    fi
    
    # Run updates
    update_html_files
    generate_data_files
    test_search_system
    
    # Git operations
    git_operations
    
    # Show next steps
    show_next_steps
    
    echo "========================================"
    echo "AGGIORNAMENTO COMPLETATO"
    echo "========================================"
    echo ""
    echo "Il sistema di ricerca CalcDomain e' stato implementato con successo!"
    echo ""
    echo "File modificati:"
    echo "- Tutti i file HTML (header aggiornato)"
    echo "- calculators-data.json (database calcolatori)"
    echo "- sitemap.xml (mappa del sito)"
    echo "- robots.txt (istruzioni crawler)"
    echo ""
    echo "Il tuo sito ora include:"
    echo "- Ricerca in tempo reale nell'header"
    echo "- Pagina di ricerca avanzata (search.html)"
    echo "- Sistema responsive per mobile"
    echo "- SEO ottimizzato"
    echo "- Database automatico dei calcolatori"
    echo ""
}

# Run main function
main "$@"
