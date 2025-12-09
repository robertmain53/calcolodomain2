#!/usr/bin/env python3
"""
CalcDomain Site Updater
Aggiorna automaticamente tutti i file HTML del sito con il nuovo sistema di ricerca
"""

import os
import re
import glob
from pathlib import Path
import json
from urllib.parse import quote
from datetime import datetime

class CalcDomainUpdater:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.css_styles = self.get_search_css()
        self.header_template = self.get_header_template()
        
    def get_search_css(self):
        """Ritorna il CSS per la ricerca da inserire inline"""
        return """
        /* CalcDomain Search Styles */
        .search-highlight {
            background: linear-gradient(120deg, #fbbf24 0%, #f59e0b 100%);
            padding: 2px 4px;
            border-radius: 4px;
            font-weight: 600;
            color: #78350f;
        }
        
        #search-results {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            max-height: 400px;
            overflow-y: auto;
        }
        
        #search-results a {
            display: block;
            padding: 16px;
            border-bottom: 1px solid #f3f4f6;
            transition: all 0.2s ease;
            text-decoration: none;
        }
        
        #search-results a:last-child {
            border-bottom: none;
        }
        
        #search-results a:hover {
            background-color: #f8fafc;
            transform: translateX(4px);
        }
        
        #search-results a:focus {
            background-color: #eff6ff;
            outline: 2px solid #3b82f6;
            outline-offset: -2px;
        }
        
        #search-results h3 {
            margin: 0 0 8px 0;
            font-size: 16px;
            font-weight: 600;
            color: #1f2937;
        }
        
        #search-results p {
            margin: 0 0 8px 0;
            font-size: 14px;
            color: #6b7280;
            line-height: 1.4;
        }
        
        #search-results .bg-blue-100 {
            background-color: #dbeafe !important;
            color: #1e40af !important;
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: 500;
        }
        
        input[type="search"]:focus {
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            border-color: #3b82f6;
        }
        
        @media (max-width: 768px) {
            #search-results {
                max-height: 300px;
                margin-top: 8px;
                border-radius: 8px;
            }
            
            #search-results a {
                padding: 12px;
            }
            
            #search-results h3 {
                font-size: 15px;
            }
            
            #search-results p {
                font-size: 13px;
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        #search-results.show {
            animation: fadeInUp 0.3s ease-out;
        }
        
        #search-results::-webkit-scrollbar {
            width: 6px;
        }
        
        #search-results::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        
        #search-results::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 3px;
        }
        
        #search-results::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        """

    def get_header_template(self):
        """Ritorna il template dell'header aggiornato"""
        return """<header class="bg-white shadow-sm sticky top-0 z-50">
    <nav class="container mx-auto px-4 lg:px-6 py-4">
        <!-- TOP ROW -->
        <div class="flex justify-between items-center">
            <!-- LOGO -->
            <a href="index.html" class="text-2xl font-bold text-blue-600">CalcDomain</a>
            
            <!-- DESKTOP SEARCH -->
            <div class="w-full max-w-md hidden md:block mx-8">
                <div class="relative">
                    <input 
                        type="search" 
                        id="search-input"
                        placeholder="Search for a calculator..." 
                        class="w-full py-2 px-4 pr-10 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        autocomplete="off"
                    >
                    <svg class="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                    <!-- CONTAINER RISULTATI RICERCA -->
                    <div id="search-results" class="absolute top-full left-0 right-0 bg-white shadow-lg rounded-lg mt-2 max-h-96 overflow-y-auto z-50 hidden border border-gray-200"></div>
                </div>
            </div>
            
            <!-- NAVIGATION LINKS -->
            <div class="hidden md:flex items-center space-x-6">
                <a href="search.html" class="text-gray-700 hover:text-blue-600 transition-colors">Advanced Search</a>
                <a href="#categories" class="text-gray-700 hover:text-blue-600 transition-colors">Categories</a>
            </div>
            
            <!-- MOBILE TOGGLE -->
            <button id="mobile-menu-toggle" class="md:hidden p-2">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
            </button>
        </div>
        
        <!-- MOBILE MENU -->
        <div id="mobile-menu" class="md:hidden mt-4 hidden">
            <div class="mb-4">
                <div class="relative">
                    <input 
                        type="search" 
                        id="mobile-search-input"
                        placeholder="Search calculators..." 
                        class="w-full py-3 px-4 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                    <svg class="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                </div>
            </div>
            <div class="space-y-2">
                <a href="search.html" class="block py-2 text-gray-700 hover:text-blue-600">Advanced Search</a>
                <a href="#categories" class="block py-2 text-gray-700 hover:text-blue-600">Categories</a>
            </div>
        </div>
    </nav>
</header>"""

    def get_mobile_script(self):
        """Ritorna lo script per la gestione mobile"""
        return """<script>
// Mobile menu toggle and search sync
document.addEventListener('DOMContentLoaded', function() {
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileToggle && mobileMenu) {
        mobileToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Sync mobile search with main search
    const mobileSearchInput = document.getElementById('mobile-search-input');
    const mainSearchInput = document.getElementById('search-input');
    
    if (mobileSearchInput && mainSearchInput) {
        mobileSearchInput.addEventListener('input', function(e) {
            if (window.calcSearch && window.calcSearch.isInitialized) {
                window.calcSearch.performSearch(e.target.value);
            }
        });
        
        mainSearchInput.addEventListener('input', function(e) {
            mobileSearchInput.value = e.target.value;
        });
    }
});
</script>"""

    def update_html_file(self, file_path):
        """Aggiorna un singolo file HTML"""
        print(f"Aggiornando: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Skip se è search.html (già creato dall'utente)
        if 'search.html' in str(file_path):
            print(f"  Saltato search.html (già esistente)")
            return True
            
        # 1. Aggiungi search.js se non presente
        if 'search.js' not in content:
            # Cerca </head> e aggiungi prima
            content = content.replace('</head>', '    <script src="search.js" defer></script>\n</head>')
        
        # 2. Aggiungi CSS inline se non presente
        if 'search-highlight' not in content:
            css_block = f"    <style>{self.css_styles}    </style>\n"
            content = content.replace('</head>', css_block + '</head>')
        
        # 3. Sostituisci header completo
        # Pattern per trovare l'header esistente
        header_pattern = r'<header.*?</header>'
        if re.search(header_pattern, content, re.DOTALL):
            content = re.sub(header_pattern, self.header_template, content, flags=re.DOTALL)
        else:
            # Se non trova header, cerca nav e sostituisci quello
            nav_pattern = r'<nav.*?</nav>'
            if re.search(nav_pattern, content, re.DOTALL):
                content = re.sub(nav_pattern, self.header_template, content, flags=re.DOTALL)
        
        # 4. Aggiungi script mobile prima di </body>
        if 'mobile-menu-toggle' not in content:
            content = content.replace('</body>', f"{self.get_mobile_script()}\n</body>")
        
        # 5. Aggiorna link relativi per sottocartelle
        if '/subcategories/' in str(file_path):
            # Aggiusta i path per le sottocartelle
            content = content.replace('href="index.html"', 'href="https://calcdomain.com/index.html"')
            content = content.replace('href="search.html"', 'href="https://calcdomain.com/search.html"')
            content = content.replace('src="search.js"', 'src="https://calcdomain.com/search.js"')
        
        # Salva il file aggiornato
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Aggiornato con successo")
        return True

    def update_index_page(self):
        """Aggiorna specificamente la homepage con hero search"""
        index_path = self.base_dir / 'index.html'
        if not index_path.exists():
            print("❌ index.html non trovato")
            return False
            
        print("Aggiornando homepage con hero search...")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cerca la sezione hero e aggiungi search bar
        hero_search = '''
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
        </div>'''
        
        # Inserisci prima dei bottoni del hero
        if 'flex flex-col sm:flex-row gap-4 justify-center' in content:
            content = content.replace(
                '<div class="flex flex-col sm:flex-row gap-4 justify-center">',
                hero_search + '\n        <div class="flex flex-col sm:flex-row gap-4 justify-center">'
            )
        
        # Aggiungi link Advanced Search nei bottoni hero
        if 'Browse Categories' in content and 'Advanced Search' not in content:
            buttons_replacement = '''<div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="#categories" class="bg-white text-blue-600 px-8 py-3 rounded-full font-semibold hover:bg-gray-100 transition-colors">Browse Categories</a>
                <a href="#popular" class="border-2 border-white text-white px-8 py-3 rounded-full font-semibold hover:bg-white hover:text-blue-600 transition-colors">Popular Calculators</a>
                <a href="search.html" class="bg-blue-700 text-white px-8 py-3 rounded-full font-semibold hover:bg-blue-800 transition-colors flex items-center justify-center">
                    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                    Advanced Search
                </a>
            </div>'''
            
            # Sostituisci i bottoni esistenti
            button_pattern = r'<div class="flex flex-col sm:flex-row gap-4 justify-center">.*?</div>'
            content = re.sub(button_pattern, buttons_replacement, content, flags=re.DOTALL)
        
        # Aggiungi hero search script
        hero_script = '''<script>
document.addEventListener('DOMContentLoaded', function() {
    const heroSearchInput = document.getElementById('hero-search-input');
    if (heroSearchInput) {
        heroSearchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const query = e.target.value.trim();
                if (query) {
                    window.location.href = `search.html?q=${encodeURIComponent(query)}`;
                }
            }
        });
        
        // Sync with header search
        heroSearchInput.addEventListener('input', function(e) {
            const headerSearch = document.getElementById('search-input');
            if (headerSearch) {
                headerSearch.value = e.target.value;
            }
        });
    }
});
</script>'''
        
        if 'hero-search-input' not in content:
            content = content.replace('</body>', hero_script + '\n</body>')
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("  ✅ Homepage aggiornata con hero search")
        return True

    def find_html_files(self):
        """Trova tutti i file HTML nel repository"""
        html_files = []
        
        # Root directory
        for file in self.base_dir.glob("*.html"):
            html_files.append(file)
        
        # Subdirectories
        for file in self.base_dir.rglob("*.html"):
            if file.parent != self.base_dir:  # Evita duplicati dalla root
                html_files.append(file)
        
        return html_files

    def run_update(self):
        """Esegue l'aggiornamento di tutti i file"""
        print("🚀 Avvio aggiornamento CalcDomain...")
        
        # Trova tutti i file HTML
        html_files = self.find_html_files()
        print(f"📄 Trovati {len(html_files)} file HTML")
        
        success_count = 0
        
        for file_path in html_files:
            try:
                if self.update_html_file(file_path):
                    success_count += 1
            except Exception as e:
                print(f"❌ Errore aggiornando {file_path}: {e}")
        
        # Aggiorna specificamente index.html
        try:
            self.update_index_page()
        except Exception as e:
            print(f"❌ Errore aggiornando index.html: {e}")
        
        print(f"\n✅ Aggiornamento completato!")
        print(f"📊 File aggiornati: {success_count}/{len(html_files)}")
        print(f"📍 CSS aggiunto inline a tutti i file")
        print(f"🔧 Script search.js incluso in tutti i file")
        print(f"📱 Header responsive aggiornato")
        print(f"🏠 Homepage con hero search aggiornata")
        
        return success_count == len(html_files)

def main():
    """Funzione principale"""
    updater = CalcDomainUpdater()
    success = updater.run_update()
    
    if success:
        print("\n🎉 Tutti i file sono stati aggiornati con successo!")
        print("\nProssimi passi:")
        print("1. Testa il sito localmente")
        print("2. Verifica che search.js e search.html funzionino")
        print("3. Fai commit e push delle modifiche")
    else:
        print("\n⚠️  Alcuni file potrebbero non essere stati aggiornati correttamente")
        print("Controlla i messaggi di errore sopra")

if __name__ == "__main__":
    main()
