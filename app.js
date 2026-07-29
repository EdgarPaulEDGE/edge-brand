/* ============================================================================
   EDGE Brand — Verhalten
   Drei Aufgaben: Zeichen einsetzen, Farbwerte kopieren, Navigation mitführen.
   Keine Einstiegs-Animationen: die Seite steht, sobald sie geladen ist.
   ========================================================================== */

/* ---------- Zeichen (Lucide-Stil, wie in EDGE Tools) ---------- */
const S = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">';
const ZEICHEN = {
  zurueck: S + '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>',
  ja: S + '<path d="M20 6 9 17l-5-5"/></svg>',
  nein: S + '<path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>',
  datei: S + '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>',
  bild: S + '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/></svg>',
  code: S + '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/></svg>',
  paket: S + '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>',
  kopie: S + '<rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>',
};
document.querySelectorAll('[data-ic]').forEach(el => {
  const k = el.dataset.ic;
  if (ZEICHEN[k]) el.innerHTML = ZEICHEN[k];
});

/* ---------- Farbwerte kopieren ---------- */
/* navigator.clipboard braucht einen sicheren Kontext. Auf github.io gegeben,
   bei file:// nicht immer, deshalb der stille Rueckfall auf execCommand. */
function kopiere(text) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(text);
  }
  const feld = document.createElement('textarea');
  feld.value = text;
  feld.style.position = 'fixed';
  feld.style.opacity = '0';
  document.body.appendChild(feld);
  feld.select();
  try { document.execCommand('copy'); } catch (e) { /* dann eben nicht */ }
  feld.remove();
  return Promise.resolve();
}

document.querySelectorAll('.farbe[data-hex]').forEach(kachel => {
  kachel.addEventListener('click', () => {
    const wert = kachel.dataset.hex;
    kopiere(wert).then(() => {
      const hex = kachel.querySelector('.fhex');
      if (!hex) return;
      if (!hex.dataset.orig) hex.dataset.orig = hex.innerHTML;
      hex.classList.add('kopiert');
      hex.textContent = 'Kopiert: ' + wert;
      clearTimeout(kachel._uhr);
      kachel._uhr = setTimeout(() => {
        hex.classList.remove('kopiert');
        hex.innerHTML = hex.dataset.orig;
        /* das Kopier-Zeichen neu einsetzen, innerHTML hat es ersetzt */
        hex.querySelectorAll('[data-ic]').forEach(el => {
          const k = el.dataset.ic;
          if (ZEICHEN[k]) el.innerHTML = ZEICHEN[k];
        });
      }, 1600);
    });
  });
});

/* ---------- Hell/Dunkel-Schalter am Lockup ---------- */
const schalter = document.getElementById('grundSchalter');
const grundBuehne = document.getElementById('grundBuehne');
if (schalter && grundBuehne) {
  schalter.querySelectorAll('button').forEach(b => {
    b.addEventListener('click', () => {
      schalter.querySelectorAll('button').forEach(x => x.classList.toggle('an', x === b));
      grundBuehne.classList.toggle('hell', b.dataset.grund === 'hell');
    });
  });
}

/* ---------- Sprungleiste folgt dem Lesen ---------- */
/* Nur Anzeige-Komfort: faellt der Observer aus, bleiben die Links normale
   Anker und alles funktioniert weiter. */
const links = [...document.querySelectorAll('.sprung a')];
const ziele = links
  .map(a => document.getElementById(a.getAttribute('href').slice(1)))
  .filter(Boolean);
if ('IntersectionObserver' in window && ziele.length) {
  const io = new IntersectionObserver(eintraege => {
    const sichtbar = eintraege.filter(e => e.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
    if (!sichtbar) return;
    links.forEach(a => a.classList.toggle('an', a.getAttribute('href') === '#' + sichtbar.target.id));
  }, { rootMargin: '-25% 0px -60% 0px', threshold: [0, .2, .5] });
  ziele.forEach(z => io.observe(z));
}
