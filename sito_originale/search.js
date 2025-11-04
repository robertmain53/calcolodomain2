// CalcDomain Search System
// Sistema di ricerca client-side per tutti i calcolatori

(function() {
    'use strict';
    
    class CalcDomainSearch {
        constructor() {
            this.calculators = [];
            this.searchInputs = [];
            this.activeInput = null;
            this.searchInput = null;
            this.searchResults = null;
            this.isInitialized = false;
            
            console.log('CalcDomainSearch: Inizializzazione...');
            this.init();
        }

        async init() {
            try {
                await this.loadCalculators();
                this.setupSearchElements();
                this.bindEvents();
                this.isInitialized = true;
                console.log('CalcDomainSearch: Inizializzato con successo', this.calculators.length, 'calcolatori');
            } catch (error) {
                console.error('CalcDomainSearch: Errore inizializzazione:', error);
            }
        }

        async loadCalculators() {
            try {
                const response = await fetch('/calculators-data.json');
                if (response.ok) {
                    this.calculators = await response.json();
                    console.log('Caricati', this.calculators.length, 'calcolatori da JSON');
                } else {
                    this.calculators = this.getEmbeddedCalculators();
                    console.log('Usando dati embedded:', this.calculators.length, 'calcolatori');
                }
            } catch (error) {
                this.calculators = this.getEmbeddedCalculators();
                console.log('Fallback a dati embedded:', this.calculators.length, 'calcolatori');
            }
        }

        getEmbeddedCalculators() {
            return [
                { slug: "mortgage-payment", url: "https://calcdomain.com/mortgage-payment.html", title: "Mortgage Payment Calculator", category: "Finance", subcategory: "Mortgage & Real Estate", description: "Calculate monthly mortgage payments" },
                { slug: "bmi", url: "https://calcdomain.com/bmi.html", title: "BMI Calculator", category: "Health & Fitness", subcategory: "Health Metrics", description: "Calculate Body Mass Index" },
                { slug: "percentage", url: "https://calcdomain.com/percentage.html", title: "Percentage Calculator", category: "Math & Conversions", subcategory: "Core Math & Algebra", description: "Calculate percentages" },
                { slug: "auto-loan", url: "https://calcdomain.com/auto-loan.html", title: "Auto Loan Calculator", category: "Finance", subcategory: "Loans & Debt", description: "Calculate car loan payments" },
                { slug: "loan-payoff", url: "https://calcdomain.com/loan-payoff.html", title: "Loan Payoff Calculator", category: "Finance", subcategory: "Loans & Debt", description: "Calculate loan payoff strategies" }
            ];
        }

        setupSearchElements() {
            const candidates = Array.from(document.querySelectorAll('[data-search-input="true"], #search-input, input[type="search"]'))
                .filter(input => !input.hasAttribute('data-search-ignore'));

            if (!candidates.length) {
                console.warn('CalcDomainSearch: nessun input di ricerca trovato.');
                return;
            }

            this.searchInputs = candidates;
            this.searchInput = candidates[0];
            this.activeInput = this.searchInput;

            this.searchResults = document.getElementById('search-results');
            if (!this.searchResults) {
                this.createSearchResultsContainer(this.searchInput);
            } else {
                const parent = this.searchInput.closest('.relative') || this.searchInput.parentElement;
                if (parent && !this.searchResults.parentElement) {
                    parent.style.position = parent.style.position || 'relative';
                    parent.appendChild(this.searchResults);
                }
            }
        }

        createSearchResultsContainer(targetInput) {
            const container = document.createElement('div');
            container.id = 'search-results';
            container.className = 'absolute top-full left-0 right-0 bg-white shadow-lg rounded-lg mt-2 max-h-96 overflow-y-auto z-50 hidden';
            
            const input = targetInput || this.searchInput;
            if (input) {
                const parent = input.closest('.relative') || input.parentElement;
                if (parent) {
                    if (!parent.style.position || parent.style.position === 'static') {
                        parent.style.position = 'relative';
                    }
                    parent.appendChild(container);
                    this.searchResults = container;
                }
            }
        }

        bindEvents() {
            if (!this.searchInputs.length) return;

            this.searchInputs.forEach(input => {
                input.addEventListener('input', (e) => {
                    this.activeInput = e.target;
                    const query = e.target.value.trim();
                    this.handleSearch(query);
                });

                input.addEventListener('focus', (e) => {
                    this.activeInput = e.target;
                    this.moveResultsContainer(e.target);
                    const query = e.target.value.trim();
                    if (query.length >= 2) {
                        this.handleSearch(query);
                        this.showResults();
                    }
                });
            });

            document.addEventListener('click', (e) => {
                if (!e.target.closest('#search-results') && !e.target.closest('input[type="search"]')) {
                    this.hideResults();
                }
            });

            this.searchInputs.forEach(input => {
                input.addEventListener('keydown', (e) => this.handleKeyboardNavigation(e));
            });
        }

        moveResultsContainer(targetInput) {
            if (!this.searchResults || !targetInput) return;
            const parent = targetInput.closest('.relative') || targetInput.parentElement;
            if (parent && parent !== this.searchResults.parentElement) {
                if (!parent.style.position || parent.style.position === 'static') {
                    parent.style.position = 'relative';
                }
                parent.appendChild(this.searchResults);
            }
        }

        handleSearch(query) {
            if (query.length < 2) {
                this.hideResults();
                return;
            }

            const results = this.searchCalculators(query);
            this.displayResults(results, query);
            this.showResults();
        }

        searchCalculators(query) {
            const normalizedQuery = query.toLowerCase().trim();
            const words = normalizedQuery.split(/\s+/);

            return this.calculators
                .map(calc => {
                    let score = 0;
                    const titleLower = calc.title.toLowerCase();
                    const descLower = calc.description.toLowerCase();

                    if (titleLower === normalizedQuery) score += 100;
                    else if (titleLower.includes(normalizedQuery)) score += 50;

                    words.forEach(word => {
                        if (titleLower.includes(word)) score += 20;
                        if (descLower.includes(word)) score += 10;
                    });

                    if (titleLower.startsWith(normalizedQuery)) score += 25;

                    return { ...calc, score };
                })
                .filter(calc => calc.score > 0)
                .sort((a, b) => b.score - a.score)
                .slice(0, 10);
        }

        displayResults(results, query) {
            if (!this.searchResults) return;

            if (results.length === 0) {
                this.searchResults.innerHTML = `
                    <div class="p-4 text-center text-gray-500">
                        <p>No calculators found for "${query}"</p>
                        <p class="text-sm mt-1">Try a different search term</p>
                    </div>
                `;
                return;
            }

            const html = results.map(calc => {
                const highlightedTitle = this.highlightMatches(calc.title, query);
                const highlightedDesc = this.highlightMatches(calc.description, query);
                const href = this.resolveCalculatorUrl(calc);
                
                return `
                    <a href="${href}" class="block p-4 hover:bg-gray-50 border-b border-gray-100 last:border-b-0">
                        <div class="flex items-start justify-between">
                            <div class="flex-1">
                                <h3 class="font-semibold text-gray-900 mb-1">${highlightedTitle}</h3>
                                <p class="text-sm text-gray-600 mb-1">${highlightedDesc}</p>
                                <div class="flex items-center text-xs text-gray-500">
                                    <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded">${calc.category}</span>
                                    <span class="mx-2">•</span>
                                    <span>${calc.subcategory}</span>
                                </div>
                            </div>
                        </div>
                    </a>
                `;
            }).join('');

            this.searchResults.innerHTML = html;
        }

        highlightMatches(text, query) {
            if (!query) return text;
            const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
            return text.replace(regex, '<mark class="bg-yellow-200 text-yellow-900">$1</mark>');
        }

        resolveCalculatorUrl(calc) {
            if (calc.url) {
                return calc.url;
            }
            if (!calc.slug) {
                return '#';
            }

            const normalized = calc.slug.replace(/^\//, '');
            if (normalized.endsWith('.html')) {
                return `/${normalized}`;
            }
            return `/${normalized}.html`;
        }

        showResults() {
            if (this.searchResults) {
                this.searchResults.classList.remove('hidden');
            }
        }

        hideResults() {
            if (this.searchResults) {
                this.searchResults.classList.add('hidden');
            }
        }

        handleKeyboardNavigation(e) {
            const results = this.searchResults?.querySelectorAll('a');
            if (!results || results.length === 0) return;

            const currentFocus = document.activeElement;
            let currentIndex = -1;

            results.forEach((result, index) => {
                if (result === currentFocus) currentIndex = index;
            });

            switch (e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    const nextIndex = currentIndex < results.length - 1 ? currentIndex + 1 : 0;
                    results[nextIndex].focus();
                    break;
                
                case 'ArrowUp':
                    e.preventDefault();
                    const prevIndex = currentIndex > 0 ? currentIndex - 1 : results.length - 1;
                    results[prevIndex].focus();
                    break;
                
                case 'Escape':
                    this.hideResults();
                    this.searchInput.blur();
                    break;
            }
        }

        performSearch(query) {
            if (this.searchInput) {
                this.searchInput.value = query;
                this.handleSearch(query);
            }
        }

        addCalculator(calculator) {
            this.calculators.push(calculator);
        }
    }

    // Inizializza quando il DOM è pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.calcSearch = new CalcDomainSearch();
        });
    } else {
        window.calcSearch = new CalcDomainSearch();
    }

    // Funzione globale per ricerca
    window.searchCalculators = function(query) {
        if (window.calcSearch && window.calcSearch.isInitialized) {
            window.calcSearch.performSearch(query);
        }
    };
})();
