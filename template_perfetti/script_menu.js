/* ========================================================================
 * CalcDomain Universal Mobile Menu Toggle
 * ========================================================================
 * Questo script gestisce l'apertura e la chiusura del menu mobile.
 * Cerca un pulsante con id="mobile-menu-toggle" e un pannello
 * con id="mobile-menu".
 * ======================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  
  // Trova gli elementi necessari nella pagina
  const menuButton = document.getElementById('mobile-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');

  // Controlla che entrambi esistano prima di fare qualsiasi cosa
  if (menuButton && mobileMenu) {
    
    // Aggiungi l'evento 'click' al pulsante
    menuButton.addEventListener('click', () => {
      
      // Aggiungi o rimuovi la classe 'hidden' di Tailwind
      mobileMenu.classList.toggle('hidden');

      // Aggiorna l'attributo ARIA per l'accessibilità
      // Controlla se il menu è ora visibile (cioè NON ha la classe 'hidden')
      const isExpanded = !mobileMenu.classList.contains('hidden');
      
      // Imposta aria-expanded a 'true' o 'false'
      menuButton.setAttribute('aria-expanded', isExpanded);
    });
  }
  
});