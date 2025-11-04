#!/usr/bin/env python3
"""
CalcDomain Data Generator
Genera automaticamente calculators-data.json e sitemap.xml basandosi sui file HTML esistenti
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
import xml.etree.ElementTree as ET

class DataGenerator:
    def __init__(self, base_dir=".", base_url="https://calcdomain.com"):
        self.base_dir = Path(base_dir)
        self.base_url = base_url.rstrip('/')
        self.calculators = []
        self.all_pages = []
        
        # Mappatura categorie basata sui file patterns
        self.category_mapping = {
            'finance': 'Finance',
            'health-fitness': 'Health & Fitness', 
            'math-conversions': 'Math & Conversions',
            'lifestyle-everyday': 'Lifestyle & Everyday',
            'construction-diy': 'Construction & DIY'
        }
        
        # Mappatura sottocategorie basata sui path
        self.subcategory_mapping = {
            'loans-debt': 'Loans & Debt',
            'mortgage-real-estate': 'Mortgage & Real Estate',
            'investment': 'Investment',
            'retirement': 'Retirement',
            'business-small-biz': 'Business & Small Biz',
            'taxes': 'Taxes',
            'health-metrics': 'Health Metrics',
            'diet-nutrition': 'Diet & Nutrition',
            'fitness': 'Fitness',
            'core-math-algebra': 'Core Math & Algebra',
            'geometry': 'Geometry',
            'measurement-unit-conversions': 'Measurement Unit Conversions',
            'miscellaneous': 'Miscellaneous',
            'hobbies': 'Hobbies',
            'time-date': 'Time & Date',
            'automotive': 'Automotive',
            'project-layout-design': 'Project Layout & Design',
            'materials-estimation': 'Materials Estimation'
        }

    def extract_title_from_html(self, file_path):
        """Estrae il titolo da un file HTML"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Cerca il tag title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if title_match:
            title = title_match.group(1).strip()
            # Pulisci il titolo
            title = re.sub(r'\s+', ' ', title)
            title = title.replace(' - CalcDomain', '').replace(' - Free Tools', '')
            return title
        
        # Fallback: cerca h1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
            return h1_text
        
        # Fallback finale: genera dal filename
        return self.generate_title_from_slug(file_path.stem)

    def extract_description_from_html(self, file_path):
        """Estrae la descrizione da un file HTML"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Cerca meta description
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if desc_match:
            return desc_match.group(1).strip()
        
        # Fallback: cerca primo paragrafo
        p_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
        if p_match:
            p_text = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
            if len(p_text) > 50:
                return p_text[:150] + '...' if len(p_text) > 150 else p_text
        
        # Fallback finale
        title = self.extract_title_from_html(file_path)
        return f"Calculate {title.lower()} quickly and accurately with our free online tool."

    def generate_title_from_slug(self, slug):
        """Genera un titolo dal slug del file"""
        # Rimuovi estensioni e caratteri speciali
        title = slug.replace('-', ' ').replace('_', ' ')
        title = ' '.join(word.capitalize() for word in title.split())
        
        # Aggiungi "Calculator" se non presente
        if 'Calculator' not in title and 'Converter' not in title:
            title += ' Calculator'
        
        return title

    def determine_category_subcategory(self, file_path, title):
        """Determina categoria e sottocategoria basandosi sul path e contenuto"""
        path_str = str(file_path).lower()
        title_lower = title.lower()
        
        # Determina categoria dal path o contenuto
        category = "Math & Conversions"  # Default
        subcategory = "Core Math & Algebra"  # Default
        
        # Categoria da path
        for key, value in self.category_mapping.items():
            if key in path_str:
                category = value
                break
        
        # Categoria da contenuto/titolo
        if any(word in title_lower for word in ['mortgage', 'loan', 'debt', 'finance', 'tax', 'investment', 'retirement', '401k', 'ira']):
            category = "Finance"
        elif any(word in title_lower for word in ['bmi', 'health', 'calorie', 'diet', 'fitness', 'heart', 'weight']):
            category = "Health & Fitness"
        elif any(word in title_lower for word in ['converter', 'conversion', 'unit', 'length', 'weight', 'temperature']):
            category = "Math & Conversions"
        elif any(word in title_lower for word in ['age', 'date', 'time', 'tip', 'grade', 'automotive']):
            category = "Lifestyle & Everyday"
        elif any(word in title_lower for word in ['concrete', 'paint', 'construction', 'lumber', 'material']):
            category = "Construction & DIY"
        
        # Sottocategoria da path
        for key, value in self.subcategory_mapping.items():
            if key in path_str:
                subcategory = value
                break
        
        # Sottocategoria da contenuto
        if category == "Finance":
            if any(word in title_lower for word in ['mortgage', 'home', 'house', 'property']):
                subcategory = "Mortgage & Real Estate"
            elif any(word in title_lower for word in ['loan', 'debt', 'credit', 'payoff']):
                subcategory = "Loans & Debt"
            elif any(word in title_lower for word in ['investment', 'stock', 'portfolio', 'return']):
                subcategory = "Investment"
            elif any(word in title_lower for word in ['retirement', '401k', 'ira', 'pension']):
                subcategory = "Retirement"
            elif any(word in title_lower for word in ['tax', 'income tax', 'deduction']):
                subcategory = "Taxes"
            elif any(word in title_lower for word in ['business', 'profit', 'break even']):
                subcategory = "Business & Small Biz"
        
        elif category == "Health & Fitness":
            if any(word in title_lower for word in ['bmi', 'weight', 'heart', 'blood']):
                subcategory = "Health Metrics"
            elif any(word in title_lower for word in ['calorie', 'diet', 'nutrition', 'protein']):
                subcategory = "Diet & Nutrition"
            elif any(word in title_lower for word in ['workout', 'fitness', 'exercise', 'training']):
                subcategory = "Fitness"
        
        elif category == "Math & Conversions":
            if any(word in title_lower for word in ['area', 'volume', 'circle', 'triangle', 'geometry']):
                subcategory = "Geometry"
            elif any(word in title_lower for word in ['converter', 'conversion', 'unit', 'length', 'weight', 'temperature']):
                subcategory = "Measurement Unit Conversions"
            else:
                subcategory = "Core Math & Algebra"
        
        elif category == "Lifestyle & Everyday":
            if any(word in title_lower for word in ['age', 'date', 'time', 'calendar']):
                subcategory = "Time & Date"
            elif any(word in title_lower for word in ['car', 'gas', 'automotive', 'fuel']):
                subcategory = "Automotive"
            elif any(word in title_lower for word in ['hobby', 'craft', 'knitting']):
                subcategory = "Hobbies"
            else:
                subcategory = "Miscellaneous"
        
        elif category == "Construction & DIY":
            if any(word in title_lower for word in ['concrete', 'paint', 'lumber', 'material']):
                subcategory = "Materials Estimation"
            else:
                subcategory = "Project Layout & Design"
        
        return category, subcategory

    def generate_keywords(self, title, slug, category, subcategory):
        """Genera keywords per il calcolatore"""
        keywords = []
        
        # Keywords dal titolo
        title_words = re.findall(r'\b\w{3,}\b', title.lower())
        keywords.extend([word for word in title_words if word not in ['calculator', 'the', 'and', 'for', 'with']])
        
        # Keywords dal slug
        slug_words = slug.replace('-', ' ').split()
        keywords.extend([word for word in slug_words if len(word) > 2])
        
        # Keywords da categoria
        keywords.append(category.lower().replace(' & ', ' ').replace(' ', ''))
        keywords.append(subcategory.lower().replace(' & ', ' ').replace(' ', ''))
        
        # Rimuovi duplicati e limita
        keywords = list(dict.fromkeys(keywords))[:8]
        
        return keywords

    def scan_html_files(self):
        """Scansiona tutti i file HTML e genera i dati"""
        print("📄 Scansionando file HTML...")
        
        # File da escludere
        exclude_files = {'search.html', 'sitemap.html', '404.html', 'robots.html'}
        
        html_files = []
        
        # Scansiona root
        for file in self.base_dir.glob("*.html"):
            if file.name not in exclude_files:
                html_files.append(file)
        
        # Scansiona subcategories e altre cartelle
        for file in self.base_dir.rglob("*.html"):
            if file.name not in exclude_files and file.parent != self.base_dir:
                html_files.append(file)
        
        print(f"Trovati {len(html_files)} file HTML")
        
        for file_path in html_files:
            try:
                # Estrai dati
                slug = file_path.stem
                title = self.extract_title_from_html(file_path)
                description = self.extract_description_from_html(file_path)
                category, subcategory = self.determine_category_subcategory(file_path, title)
                keywords = self.generate_keywords(title, slug, category, subcategory)
                
                # Genera URL relativo
                if file_path.parent == self.base_dir:
                    url_path = f"{slug}.html"
                else:
                    rel_path = file_path.relative_to(self.base_dir)
                    url_path = str(rel_path).replace('\\', '/')
                
                # Aggiungi ai calcolatori se non è una pagina di categoria
                if not any(cat_key in slug for cat_key in self.category_mapping.keys()):
                    calculator_data = {
                        "slug": slug,
                        "title": title,
                        "category": category,
                        "subcategory": subcategory,
                        "description": description,
                        "keywords": keywords
                    }
                    self.calculators.append(calculator_data)
                
                # Aggiungi a tutte le pagine per sitemap
                page_data = {
                    "url": f"{self.base_url}/{url_path}",
                    "lastmod": datetime.now().strftime('%Y-%m-%d'),
                    "changefreq": "weekly" if any(cat_key in slug for cat_key in self.category_mapping.keys()) else "monthly",
                    "priority": "1.0" if slug == "index" else "0.8" if any(cat_key in slug for cat_key in self.category_mapping.keys()) else "0.6"
                }
                self.all_pages.append(page_data)
                
                print(f"  ✅ {file_path.name} -> {category} / {subcategory}")
                
            except Exception as e:
                print(f"  ❌ Errore processando {file_path}: {e}")

    def generate_calculators_json(self):
        """Genera il file calculators-data.json"""
        print("\n🔧 Generando calculators-data.json...")
        
        # Ordina per categoria e titolo
        self.calculators.sort(key=lambda x: (x['category'], x['subcategory'], x['title']))
        
        json_path = self.base_dir / 'calculators-data.json'
        
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.calculators, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Generato calculators-data.json con {len(self.calculators)} calcolatori")
            
            # Statistiche per categoria
            categories = {}
            for calc in self.calculators:
                cat = calc['category']
                categories[cat] = categories.get(cat, 0) + 1
            
            print("📊 Distribuzione per categoria:")
            for cat, count in sorted(categories.items()):
                print(f"   {cat}: {count} calcolatori")
                
            return True
            
        except Exception as e:
            print(f"❌ Errore generando calculators-data.json: {e}")
            return False

    def generate_sitemap_xml(self):
        """Genera il file sitemap.xml"""
        print("\n🗺️  Generando sitemap.xml...")
        
        # Crea root element
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        # Aggiungi homepage per prima
        home_url = ET.SubElement(urlset, 'url')
        ET.SubElement(home_url, 'loc').text = self.base_url + '/'
        ET.SubElement(home_url, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
        ET.SubElement(home_url, 'changefreq').text = 'daily'
        ET.SubElement(home_url, 'priority').text = '1.0'
        
        # Aggiungi search.html
        search_url = ET.SubElement(urlset, 'url')
        ET.SubElement(search_url, 'loc').text = self.base_url + '/search.html'
        ET.SubElement(search_url, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')
        ET.SubElement(search_url, 'changefreq').text = 'weekly'
        ET.SubElement(search_url, 'priority').text = '0.9'
        
        # Aggiungi tutte le altre pagine
        for page in self.all_pages:
            if page['url'] != f"{self.base_url}/index.html":  # Skip duplicate homepage
                url_element = ET.SubElement(urlset, 'url')
                ET.SubElement(url_element, 'loc').text = page['url']
                ET.SubElement(url_element, 'lastmod').text = page['lastmod']
                ET.SubElement(url_element, 'changefreq').text = page['changefreq']
                ET.SubElement(url_element, 'priority').text = page['priority']
        
        # Salva il file
        sitemap_path = self.base_dir / 'sitemap.xml'
        
        try:
            # Formatta con indentazione
            self.indent_xml(urlset)
            
            tree = ET.ElementTree(urlset)
            tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
            
            print(f"✅ Generato sitemap.xml con {len(self.all_pages) + 2} URL")
            return True
            
        except Exception as e:
            print(f"❌ Errore generando sitemap.xml: {e}")
            return False

    def indent_xml(self, elem, level=0):
        """Indenta il XML per leggibilità"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent_xml(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def generate_robots_txt(self):
        """Genera il file robots.txt"""
        print("\n🤖 Generando robots.txt...")
        
        robots_content = f"""User-agent: *
Allow: /

# Sitemap
Sitemap: {self.base_url}/sitemap.xml

# Disallow admin/test pages
Disallow: /admin/
Disallow: /test/
Disallow: /*.json$
Disallow: /*.log$

# Allow search engines to index all calculators
Allow: /*.html

# Crawl delay (optional)
Crawl-delay: 1
"""
        
        robots_path = self.base_dir / 'robots.txt'
        
        try:
            with open(robots_path, 'w', encoding='utf-8') as f:
                f.write(robots_content)
            
            print("✅ Generato robots.txt")
            return True
            
        except Exception as e:
            print(f"❌ Errore generando robots.txt: {e}")
            return False

    def run_generation(self):
        """Esegue la generazione completa"""
        print("🚀 Avvio generazione dati CalcDomain...")
        
        # Scansiona file
        self.scan_html_files()
        
        # Genera file
        json_success = self.generate_calculators_json()
        sitemap_success = self.generate_sitemap_xml()
        robots_success = self.generate_robots_txt()
        
        print(f"\n🎉 Generazione completata!")
        print(f"📊 Risultati:")
        print(f"   📄 calculators-data.json: {'✅' if json_success else '❌'}")
        print(f"   🗺️  sitemap.xml: {'✅' if sitemap_success else '❌'}")
        print(f"   🤖 robots.txt: {'✅' if robots_success else '❌'}")
        print(f"   📈 Totale calcolatori: {len(self.calculators)}")
        print(f"   🌐 Totale URL sitemap: {len(self.all_pages) + 2}")
        
        return json_success and sitemap_success and robots_success

def main():
    """Funzione principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Genera calculators-data.json e sitemap.xml per CalcDomain")
    parser.add_argument("--base-url", default="https://calcdomain.com", help="URL base del sito")
    parser.add_argument("--dir", default=".", help="Directory del sito")
    
    args = parser.parse_args()
    
    generator = DataGenerator(base_dir=args.dir, base_url=args.base_url)
    success = generator.run_generation()
    
    if success:
        print("\n🎯 Tutti i file sono stati generati con successo!")
        print("Prossimi passi:")
        print("1. Verifica i file generati")
        print("2. Testa il JSON con il sistema di ricerca")
        print("3. Submetti la sitemap a Google Search Console")
    else:
        print("\n⚠️  Alcuni file potrebbero non essere stati generati correttamente")

if __name__ == "__main__":
    main()
