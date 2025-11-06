#!/usr/bin/env python3
"""
Fix Homepage Hero Search
Aggiunge lo script necessario per far funzionare la ricerca nella homepage
"""

from pathlib import Path
import re

def fix_homepage_search():
    """Aggiunge lo script per la hero search nella homepage"""
    
    index_path = Path("index.html")
    
    if not index_path.exists():
        print("❌ index.html non trovato")
        return False
    
    print("Leggendo index.html...")
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Script da aggiungere per la hero search
    hero_search_script = """
<script>
// Hero Search Integration
document.addEventListener('DOMContentLoaded', function() {
    const heroSearchInput = document.getElementById('hero-search-input');
    const headerSearchInput = document.getElementById('search-input');
    
    if (heroSearchInput) {
        console.log('Hero search input trovato, configurando...');
        
        // Gestisce input in tempo reale
        heroSearchInput.addEventListener('input', function(e) {
            const query = e.target.value;
            
            // Sincronizza con header search
            if (headerSearchInput) {
                headerSearchInput.value = query;
            }
            
            // Attiva la ricerca se il sistema è pronto
            if (window.calcSearch && window.calcSearch.isInitialized && query.length >= 2) {
                window.calcSearch.performSearch(query);
                
                // Scroll alla sezione dei risultati (nell'header)
                if (window.calcSearch.searchResults) {
                    window.calcSearch.showResults();
                }
            }
        });
        
        // Gestisce Enter per andare alla pagina di ricerca avanzata
        heroSearchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const query = e.target.value.trim();
                if (query) {
                    window.location.href = `search.html?q=${encodeURIComponent(query)}`;
                }
            }
        });
        
        // Gestisce focus
        heroSearchInput.addEventListener('focus', function(e) {
            const query = e.target.value.trim();
            if (window.calcSearch && window.calcSearch.isInitialized && query.length >= 2) {
                window.calcSearch.performSearch(query);
                window.calcSearch.showResults();
            }
        });
        
        console.log('Hero search configurato correttamente');
    } else {
        console.warn('Hero search input non trovato nella pagina');
    }
    
    // Quick search buttons
    const quickSearchButtons = document.querySelectorAll('.quick-search-btn');
    if (quickSearchButtons.length > 0) {
        console.log('Configurando', quickSearchButtons.length, 'quick search buttons');
        quickSearchButtons.forEach(button => {
            button.addEventListener('click', function() {
                const query = this.dataset.query;
                window.location.href = `search.html?q=${encodeURIComponent(query)}`;
            });
        });
    }
});
</script>"""
    
    # Controlla se lo script è già presente
    if 'hero-search-input' in content and 'Hero Search Integration' in content:
        print("✅ Script hero search già presente")
        return True
    
    # Rimuovi vecchi script hero search se presenti
    content = re.sub(r'<script>.*?hero-search-input.*?</script>', '', content, flags=re.DOTALL)
    
    # Aggiungi lo script prima di </body>
    if '</body>' in content:
        content = content.replace('</body>', hero_search_script + '\n</body>')
        print("✅ Script hero search aggiunto")
    else:
        print("❌ Tag </body> non trovato")
        return False
    
    # Verifica che ci sia l'input hero-search
    if 'id="hero-search-input"' not in content:
        print("⚠️  ATTENZIONE: id='hero-search-input' non trovato nella homepage")
        print("    Aggiungendo hero search input...")
        
        # Cerca la sezione hero
        hero_pattern = r'(<section[^>]*hero[^>]*>.*?)(</section>)'
        if re.search(hero_pattern, content, re.DOTALL | re.IGNORECASE):
            hero_search_html = """
        <!-- HERO SEARCH BAR -->
        <div class="max-w-2xl mx-auto mb-8">
            <div class="relative">
                <input 
                    type="search" 
                    id="hero-search-input" 
                    placeholder="Search calculators, e.g. 'mortgage', 'BMI', 'percentage'..." 
                    class="w-full py-4 px-6 pr-12 text-lg text-gray-800 rounded-full focus:outline-none focus:ring-4 focus:ring-white focus:ring-opacity-50 shadow-lg"
                    autocomplete="off"
                >
                <button type="button" class="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-600 text-white p-3 rounded-full hover:bg-blue-700 transition-colors">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                </button>
            </div>
        </div>
"""
            
            # Inserisci prima dei bottoni Browse Categories
            browse_pattern = r'(<div class="flex flex-col sm:flex-row gap-4 justify-center">)'
            if re.search(browse_pattern, content):
                content = re.sub(browse_pattern, hero_search_html + r'\n        \1', content)
                print("✅ Hero search input aggiunto alla pagina")
    
    # Salva il file
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ Homepage aggiornata con successo!")
    print("\nProssimi passi:")
    print("1. Ricarica index.html nel browser")
    print("2. Apri la console (F12)")
    print("3. Cerca il messaggio: 'Hero search configurato correttamente'")
    print("4. Prova a digitare nell'input hero")
    print("5. I risultati dovrebbero apparire nell'header")
    
    return True

def add_quick_search_section():
    """Aggiunge la sezione Quick Search se non presente"""
    
    index_path = Path("index.html")
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'quick-search-btn' in content:
        print("\n✅ Sezione Quick Search già presente")
        return True
    
    print("\n📝 Aggiungendo sezione Quick Search...")
    
    quick_search_html = """
<!-- QUICK SEARCH SECTION -->
<section class="py-16 bg-gray-100">
    <div class="container mx-auto px-4">
        <div class="text-center mb-12">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">Quick Search</h2>
            <p class="text-lg text-gray-600">Click on any topic to find related calculators instantly</p>
        </div>
        
        <div class="flex flex-wrap justify-center gap-4 max-w-4xl mx-auto">
            <button class="quick-search-btn bg-white hover:bg-blue-50 text-gray-800 px-6 py-3 rounded-full shadow-md hover:shadow-lg transition-all" data-query="mortgage">
                🏠 Mortgage
            </button>
            <button class="quick-search-btn bg-white hover:bg-blue-50 text-gray-800 px-6 py-3 rounded-full shadow-md hover:shadow-lg transition-all" data-query="loan">
                💰 Loans
            </button>
            <button class="quick-search-btn bg-white hover:bg-blue-50 text-gray-800 px-6 py-3 rounded-full shadow-md hover:shadow-lg transition-all" data-query="bmi">
                🏃 BMI
            </button>
            <button class="quick-search-btn bg-white hover:bg-blue-50 text-gray-800 px-6 py-3 rounded-full shadow-md hover:shadow-lg transition-all" data-query="percentage">
                📊 Percentage
            </button>
            <button class="quick-search-btn bg-white hover:bg-blue-50 text-gray-800 px-6 py-3 rounded-full shadow-md hover:shadow-lg transition-all" data-query="investment">
                📈 Investment
            </button>
            <button class="quick-search-btn bg-white hover:bg-blue-50 text-gray-800 px-6 py-3 rounded-full shadow-md hover:shadow-lg transition-all" data-query="tax">
                🧾 Tax
            </button>
            <button class="quick-search-btn bg-white hover:bg-blue-50 text-gray-800 px-6 py-3 rounded-full shadow-md hover:shadow-lg transition-all" data-query="retirement">
                👴 Retirement
            </button>
            <button class="quick-search-btn bg-white hover:bg-blue-50 text-gray-800 px-6 py-3 rounded-full shadow-md hover:shadow-lg transition-all" data-query="area">
                📐 Area
            </button>
            <button class="quick-search-btn bg-white hover:bg-blue-50 text-gray-800 px-6 py-3 rounded-full shadow-md hover:shadow-lg transition-all" data-query="converter">
                🔄 Converter
            </button>
            <button class="quick-search-btn bg-white hover:bg-blue-50 text-gray-800 px-6 py-3 rounded-full shadow-md hover:shadow-lg transition-all" data-query="construction">
                🏗️ Construction
            </button>
        </div>
    </div>
</section>
"""
    
    # Trova dove inserire (dopo la sezione Popular Calculators)
    popular_section_pattern = r'(<!-- Popular Calculators Section -->.*?</section>)'
    if re.search(popular_section_pattern, content, re.DOTALL):
        content = re.sub(popular_section_pattern, r'\1\n' + quick_search_html, content, flags=re.DOTALL)
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Sezione Quick Search aggiunta")
        return True
    else:
        print("⚠️  Sezione Popular Calculators non trovata, Quick Search non aggiunto")
        return False

def main():
    print("="*50)
    print("Fix Homepage Hero Search")
    print("="*50)
    print()
    
    # Fix hero search
    success = fix_homepage_search()
    
    if success:
        # Aggiungi quick search
        add_quick_search_section()
        
        print("\n" + "="*50)
        print("COMPLETATO!")
        print("="*50)
        print("\nTest della hero search:")
        print("1. Apri index.html nel browser")
        print("2. Apri console (F12)")
        print("3. Digita nell'input hero (sotto il titolo principale)")
        print("4. I risultati dovrebbero apparire nell'header in alto")
        print("5. Premi Enter per andare a search.html con la query")
        print("\nTest quick search buttons:")
        print("1. Scroll alla sezione 'Quick Search'")
        print("2. Clicca su un bottone (es. 'Mortgage')")
        print("3. Dovresti essere reindirizzato a search.html con la query")
    else:
        print("\n❌ Errore durante il fix della homepage")

if __name__ == "__main__":
    main()
