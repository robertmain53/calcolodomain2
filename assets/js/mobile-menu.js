<script>
(function () {
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const btn   = $('#mobile-menu-toggle');
  const panel = $('#mobile-menu');
  if (!btn || !panel) return;

  // ARIA baseline
  btn.setAttribute('aria-controls', panel.id);
  btn.setAttribute('aria-expanded', btn.getAttribute('aria-expanded') || 'false');
  panel.setAttribute('role', panel.getAttribute('role') || 'navigation');

  // Helpers
  const isHidden = () => panel.classList.contains('hidden') || panel.style.display === 'none';
  const show = () => {
    panel.classList.remove('hidden');
    panel.classList.add('block'); // Tailwind: garantisce la visibilità
    btn.setAttribute('aria-expanded', 'true');
    document.documentElement.classList.add('overflow-hidden'); // lock scroll
  };
  const hide = () => {
    panel.classList.remove('block');
    panel.classList.add('hidden');
    btn.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('overflow-hidden');
  };
  const toggle = () => (isHidden() ? show() : hide());

  // Wire up toggle
  btn.addEventListener('click', (e) => { e.preventDefault(); toggle(); });
  btn.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
  });

  // Chiudi con Esc
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !isHidden()) hide();
  });

  // Chiudi su click fuori
  document.addEventListener('click', (e) => {
    if (isHidden()) return;
    const t = e.target;
    if (t === btn || btn.contains(t)) return;
    if (panel.contains(t)) return;
    hide();
  });

  // Chiudi quando clicchi un link nel menu
  $$('#mobile-menu a[href]').forEach((a) => {
    a.addEventListener('click', () => hide());
  });

  // (Opzionale) Sincronizza le ricerche: mobile ↔ header/hero
  const mobileSearch  = $('#mobile-search-input');
  const headerSearch  = $('#search-input');
  const heroSearch    = $('#hero-search-input');
  const sync = (from, others) => {
    if (!from) return;
    from.addEventListener('input', (e) => {
      const q = e.target.value;
      others.forEach(o => { if (o) o.value = q; });
      if (window.calcSearch && window.calcSearch.isInitialized && q.length >= 2) {
        window.calcSearch.performSearch(q);
        if (window.calcSearch.showResults) window.calcSearch.showResults();
      }
    });
  };
  sync(mobileSearch, [headerSearch, heroSearch]);
  sync(headerSearch, [mobileSearch, heroSearch]);
  sync(heroSearch,   [mobileSearch, headerSearch]);
})();
</script>
