import os
import codecs
import json
from bs4 import BeautifulSoup

print("AVVIO SCRIPT DI RICOSTRUZIONE PAGINE INDICE (v5.0 - Senza Sottocartelle)")

# --- CONFIGURAZIONE PERCORSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "template_perfetti")
SITO_MODIFICATO_DIR = os.path.join(BASE_DIR, "sito_modificato")

# File di dati
SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap_data_FINAL_flat.json")
TEMPLATE_INTERNA_FILE = os.path.join(TEMPLATE_DIR, "template_master_INTERNA.html")
TEMPLATE_HOMEPAGE_FILE = os.path.join(TEMPLATE_DIR, "template_master_HOMEPAGE.html")

# Non cancella la cartella, ma la crea se non esiste
os.makedirs(SITO_MODIFICATO_DIR, exist_ok=True)

# --- 1. FUNZIONI HELPER ---

def load_assets():
    """Carica i template e il JSON del sito."""
    try:
        with codecs.open(SITEMAP_FILE, 'r', 'utf-8') as f:
            sitemap_data = json.load(f)
        with codecs.open(TEMPLATE_INTERNA_FILE, 'r', 'utf-8') as f:
            template_interna = f.read()
        with codecs.open(TEMPLATE_HOMEPAGE_FILE, 'r', 'utf-8') as f:
            template_homepage = f.read()
        return sitemap_data, template_interna, template_homepage
    except FileNotFoundError as e:
        print(f"ERRORE CRITICO: Asset mancante. Assicurati che '{e.filename}' esista.")
        return None, None, None

def slugify(text):
    """Converte un titolo in uno slug pulito."""
    text = text.lower().replace(' & ', '-').replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '').replace('--', '-')
    return text.strip('-')

def create_index_page(filename, title, description, category_title, html_content, template_content):
    """Assembla e salva la pagina come file .html nella root di sito_modificato."""
    
    output_path = os.path.join(SITO_MODIFICATO_DIR, filename)
    slug_name = filename.replace('.html', '')
    
    # URL Canonico senza / finale né .html
    canonical_url = f"https://calcdomain.com/{slug_name}"
    
    # Costruisce Breadcrumb: Home > Categoria (Per la Home, è solo Home)
    breadcrumb_html = f'<a href="https://calcdomain.com">Home</a>'
    if filename != 'index.html':
        breadcrumb_html += f' &raquo; <span>{category_title}</span>'
        
    final_html = template_content
    final_html = final_html.replace("%%TITOLO_PAGINA%%", title)
    final_html = final_html.replace("%%DESCRIZIONE_PAGINA%%", description)
    final_html = final_html.replace("%%URL_CANONICO%%", canonical_url)
    final_html = final_html.replace("%%BREADCRUMB_HTML_QUI%%", breadcrumb_html)
    
    final_html = final_html.replace("%%CONTENUTO_PRINCIPALE_QUI%%", html_content)
    final_html = final_html.replace("%%SIDEBAR_HTML_QUI%%", '<div id="index-page-sidebar-placeholder"></div>') 
    
    final_html = final_html.replace('%%HEAD_SCRIPTS_E_META%%', '')
    final_html = final_html.replace('%%BODY_SCRIPTS_INIZIO%%', '')
    final_html = final_html.replace('%%SCHEMA_JSON_LD_QUI%%', '[]')
    
    with codecs.open(output_path, 'w', 'utf-8') as f_out:
        f_out.write(final_html)
        
    return True

# --- 2. LOGICA DI GENERAZIONE CONTENUTO ---

def build_category_content(sitemap_data, category):
    """Genera l'HTML per la pagina indice di una categoria (es. /finance.html)."""
    subcategories = sitemap_data[category]
    
    html = f'<h1 class="text-3xl font-bold mb-6">{category} Hub: All Tools</h1>'
    html += f'<p class="text-lg text-gray-600 mb-8">Navigate all {category} calculation tools organized by specialty:</p>'

    html += '<div class="space-y-8">'
    
    # Ordina per mettere "Generale" per primo
    sorted_subcategories = sorted(subcategories.items(), key=lambda item: item[0] != "Generale")
    
    for subcategory, pages in sorted_subcategories:
        if not pages: continue
        
        # L'URL per i link nel corpo è il path della categoria (es. /finance)
        category_slug = slugify(category)
        
        # Usiamo un URL fittizio per l'hub (non serve una pagina sottocategoria separata)
        # Basterà il link al primo elemento della sottocategoria
        
        html += f"""
        <div class="border p-4 rounded-lg shadow-md">
            <h3 class="text-2xl font-semibold text-blue-800 mb-3">{subcategory} ({len(pages)} Tools)</h3>
            <ul class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-2 list-disc list-inside">
        """
        
        # Elenca tutti i post e li linka senza estensione
        for page in pages:
            html += f"""
                <li class="hover:text-blue-600">
                    <a href="https://calcdomain.com{page['url']}" class="text-gray-700 hover:underline">{page['title']}</a>
                </li>
            """
        html += '</ul></div>'
        
    html += '</div>'
    return html

# --- 3. LOGICA PRINCIPALE (MAIN) ---

def main():
    sitemap_data, template_interna, template_homepage = load_assets()
    if not sitemap_data: return

    # 1. GENERAZIONE HOMEPAGE
    print("\n--- 1. Generazione Homepage (index.html) ---")
    
    homepage_title = "The Ultimate Collection of Free Online Calculators"
    homepage_desc = "Fast, accurate, and easy-to-use calculators for Finance, Math, Conversions, Health, and Engineering. Solve every problem instantly."
    
    homepage_content = '<div class="container mx-auto px-4 py-8">'
    homepage_content += '<h1 class="text-3xl font-bold mb-6 text-center">Solve Any Problem: Our Top Categories</h1>'
    homepage_content += '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">'
    
    for category in sitemap_data.keys():
        cat_slug = slugify(category)
        # Link alla NUOVA struttura (es. /finance)
        homepage_content += f"""
        <a href="https://calcdomain.com/{cat_slug}" class="block bg-white p-6 rounded-lg shadow-lg card-hover transition-all duration-300">
            <h3 class="text-xl font-semibold text-blue-600 mb-2">{category}</h3>
            <p class="text-sm text-gray-600">Explore all tools for {category}.</p>
        </a>
        """
    homepage_content += '</div></div>'
    
    create_index_page(
        'index.html',
        homepage_title,
        homepage_desc,
        'Home', 
        homepage_content,
        template_homepage
    )
    print("  > Generata: /index.html")

    # 2. GENERAZIONE PAGINE CATEGORIA PRINCIPALE (File .html nella root)
    print("\n--- 2. Generazione Pagine Categoria Principale (Hubs) ---")
    
    for category in sitemap_data.keys():
        category_slug = slugify(category)
        filename = f'{category_slug}.html'
        
        title = f'Top {category} Calculators and Conversion Tools'
        description = f'A complete list of all subcategories, core tools, and conversions within the {category} section.'
        
        html_content = build_category_content(sitemap_data, category)
        
        create_index_page(
            filename,
            title,
            description,
            category,
            html_content,
            template_interna
        )
        print(f"  > Generata Categoria: /{category_slug}.html")
        
    print("\n✅ Generazione Indici completata.")
    print("------------------------------------------------------------------")
    print("PROSSIMO PASSO:")
    print("1. ESEGUIRE NUOVAMENTE TUTTI I TUOI 100 CALCOLATORI NELLA CARTELLA 'sito_modificato'.")
    print("2. I link cablati (es. /finance) punteranno ora a /finance.html (che Vercel servirà come /finance).")


if __name__ == "__main__":
    main()