'use strict';
(async () => {
  const grid = document.querySelector('#grid');
  const search = document.querySelector('#search');
  const status = document.querySelector('#status');
  const viewer = document.querySelector('#viewer');
  const fullImage = document.querySelector('#full-image');
  const close = document.querySelector('#close');
  let category = 'All';
  let opener;
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[-’']/g, ' ').replace(/\s+/g, ' ').trim();
  close.addEventListener('click', () => viewer.close());
  // Close is the dialog's only interactive control; keep both Tab directions here.
  viewer.addEventListener('keydown', event => {
    if (event.key === 'Tab') { event.preventDefault(); close.focus(); }
  });
  viewer.addEventListener('click', event => {
    const rect = viewer.getBoundingClientRect();
    if (event.target === viewer && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) viewer.close();
  });
  viewer.addEventListener('close', () => { fullImage.removeAttribute('src'); opener?.focus(); });
  fullImage.addEventListener('error', () => { document.querySelector('#image-note').textContent = 'This image could not load. Close and try again.'; });
  try {
    const response = await fetch('assets/gallery/manifest.json');
    if (!response.ok) throw new Error('Collection unavailable');
    const { entries } = await response.json();
    const cards = entries.map(entry => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = `design${entry.imageType === 'Promotional art' ? ' art' : ''}`;
      button.dataset.id = entry.id;
      button.setAttribute('aria-label', `View ${entry.name} — ${entry.imageType}`);
      const image = document.createElement('img');
      image.src = entry.thumbnail.src;
      image.width = entry.thumbnail.width;
      image.height = entry.thumbnail.height;
      image.alt = '';
      image.loading = 'lazy';
      image.decoding = 'async';
      const caption = document.createElement('span');
      caption.className = 'caption';
      for (const [className, text] of [['category', entry.category], ['name', entry.name], ['image-type', entry.imageType]]) {
        const span = document.createElement('span'); span.className = className; span.textContent = text; caption.append(span);
      }
      button.append(image, caption);
      button.addEventListener('click', () => {
        opener = button;
        document.querySelector('#image-title').textContent = entry.name;
        document.querySelector('#image-note').textContent = entry.imageType === 'Promotional art'
          ? `${entry.provenance.provider === 'xai' ? 'AI-generated promotional art' : 'Promotional art'} · Illustration, not a model screenshot. Details may differ from the actual model.`
          : 'Model preview · Still image rendered from the actual collection model; not an interactive 3D viewer.';
        fullImage.alt = `${entry.name} Box design — ${entry.imageType.toLowerCase()}`;
        fullImage.src = entry.image.src;
        viewer.showModal(); viewer.scrollTop = 0; close.focus();
      });
      grid.append(button);
      return { button, entry, text: normalize(`${entry.name} ${entry.id} ${entry.category}`) };
    });
    const render = () => {
      const words = normalize(search.value).split(' ').filter(Boolean);
      let count = 0;
      for (const card of cards) {
        card.button.hidden = !(category === 'All' || card.entry.category === category) || !words.every(word => card.text.includes(word));
        if (!card.button.hidden) count++;
      }
      status.textContent = `${count} of ${entries.length} designs`;
      document.querySelector('#empty').hidden = count !== 0;
      document.querySelectorAll('[data-category]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.category === category)));
    };
    search.addEventListener('input', render);
    document.querySelectorAll('[data-category]').forEach(button => button.addEventListener('click', () => { category = button.dataset.category; render(); }));
    document.querySelector('#reset').addEventListener('click', () => { category = 'All'; search.value = ''; render(); search.focus(); });
    render();
  } catch (error) {
    status.textContent = 'The collection could not load. Please refresh to try again.';
  }
})();
