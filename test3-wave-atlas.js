(() => {
  'use strict';
  const body = document.querySelector('#wave-atlas-body');
  if (!body) return;
  let payload = null;
  let activeFilter = 'all';

  const language = () => document.documentElement.dataset.language === 'en' ? 'en' : 'zh';
  const setDownloads = () => {
    const en = language() === 'en';
    const png = document.querySelector('#wave-atlas-png');
    const csv = document.querySelector('#wave-atlas-csv');
    const imageLink = document.querySelector('#wave-atlas-image-link');
    if (png) png.href = `assets/waves/ocean_atmosphere_wave_atlas${en ? '-en' : ''}.png`;
    if (csv) csv.href = `assets/waves/ocean_atmosphere_wave_atlas${en ? '-en' : ''}.csv`;
    if (imageLink) imageLink.href = `assets/waves/ocean_atmosphere_wave_atlas${en ? '-en' : ''}.png`;
  };
  const render = () => {
    if (!payload) return;
    const lang = language();
    const rows = payload.rows.filter(row => activeFilter === 'all' || row.group.en === activeFilter);
    body.replaceChildren(...rows.map(row => {
      const tr = document.createElement('tr');
      tr.dataset.group = row.group.en;
      payload.fields.forEach((field, index) => {
        const cell = document.createElement(index < 2 ? 'th' : 'td');
        cell.scope = index < 2 ? 'row' : '';
        const parts = row[field][lang].split('\n');
        parts.forEach((part, partIndex) => {
          if (partIndex) cell.append(document.createElement('br'));
          cell.append(document.createTextNode(part));
        });
        tr.append(cell);
      });
      return tr;
    }));
    const count = document.querySelector('#wave-atlas-visible-count');
    if (count) count.textContent = String(rows.length);
    const symbols = document.querySelector('#wave-atlas-symbols');
    if (symbols) symbols.textContent = payload.symbols[lang];
    setDownloads();
  };

  document.querySelectorAll('[data-wave-filter]').forEach(button => {
    button.addEventListener('click', () => {
      activeFilter = button.dataset.waveFilter;
      document.querySelectorAll('[data-wave-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      render();
    });
  });

  fetch('assets/waves/ocean_atmosphere_wave_atlas.json?v=20261023-atlas')
    .then(response => {
      if (!response.ok) throw new Error(`Wave-atlas data HTTP ${response.status}`);
      return response.json();
    })
    .then(data => { payload = data; render(); })
    .catch(error => {
      body.innerHTML = `<tr><td colspan="12">${error.message}</td></tr>`;
      console.error(error);
    });
  window.addEventListener('site-language-change', render);
  setDownloads();
})();
