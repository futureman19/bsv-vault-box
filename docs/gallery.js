'use strict';
(async () => {
  const grid = document.querySelector('#grid');
  const search = document.querySelector('#search');
  const status = document.querySelector('#status');
  const viewer = document.querySelector('#viewer');
  const fullImage = document.querySelector('#full-image');
  const close = document.querySelector('#close');
  const params = new URLSearchParams(location.search);
  let category = ['All', 'Country', 'Ocean', 'Moon'].includes(params.get('category')) ? params.get('category') : 'All';
  search.value = params.get('q') || '';
  // Native showModal() owns focus containment and restoration.
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[-’']/g, ' ').replace(/\s+/g, ' ').trim();

  // Keep light dismiss in browsers without closedby (notably Safari).
  // A drag beginning inside the image must not dismiss on release outside.
  if (!('closedBy' in HTMLDialogElement.prototype)) {
    const outside = event => {
      const rect = viewer.getBoundingClientRect();
      return event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom;
    };
    let pressedOutside = false, releasedOutside = false;
    viewer.addEventListener('pointerdown', event => {
      pressedOutside = outside(event); releasedOutside = false;
    });
    viewer.addEventListener('pointerup', event => { releasedOutside = outside(event); });
    // Close on click, after touch's compatibility mouse events, so those events
    // cannot steal the focus restored by close() or hit the page underneath.
    viewer.addEventListener('click', () => {
      if (pressedOutside && releasedOutside) viewer.close();
      pressedOutside = releasedOutside = false;
    });
    viewer.addEventListener('pointercancel', () => { pressedOutside = releasedOutside = false; });
  }
  viewer.addEventListener('close', () => {
    fullImage.removeAttribute('src');
    history.replaceState(null, '', location.pathname + location.search);

  });
  fullImage.addEventListener('error', () => {
    if (!fullImage.getAttribute('src')) return;
    fullImage.hidden = true;
    document.querySelector('#image-load').textContent = 'Image unavailable. Close and reopen to try again.';
  });
  fullImage.addEventListener('load', () => { fullImage.hidden = false; document.querySelector('#image-load').textContent = ''; });
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
      image.addEventListener('error', () => {
        image.hidden = true;
        button.classList.add('image-unavailable');
        button.querySelector('.image-type').textContent = `${entry.imageType} · Preview unavailable — open to retry`;
      });
      const caption = document.createElement('span');
      caption.className = 'caption';
      for (const [className, text] of [['category', entry.category], ['name', entry.name], ['image-type', entry.imageType]]) {
        const span = document.createElement('span'); span.className = className; span.textContent = text; caption.append(span);
      }
      button.append(image, caption);
      button.addEventListener('click', () => {
        // Focus the invoking card before opening, including URL-driven opens.
        button.focus({ preventScroll: true });
        document.querySelector('#image-title').textContent = entry.name;
        document.querySelector('#image-note').textContent = entry.imageType === 'Promotional art'
          ? `${entry.provenance.provider === 'xai' ? 'AI-generated promotional art' : 'Promotional art'} · Illustration, not a model screenshot. Details may differ from the actual model.`
          : 'Model preview · Still image rendered from the actual collection model; not an interactive 3D viewer.';
        if (entry.provenance.intentionalRedesign) document.querySelector('#image-note').textContent += ' USA flag-and-fireworks redesign; the canyon-inspired model is unchanged. Stylized flag, not an exact official flag reproduction.';
        history.replaceState(null, '', location.pathname + location.search + '#' + entry.id);
        fullImage.hidden = false;
        document.querySelector('#image-load').textContent = 'Loading image…';
        fullImage.alt = `${entry.name} Box design — ${entry.imageType.toLowerCase()}`;
        fullImage.src = entry.image.src;
        viewer.showModal(); viewer.scrollTop = 0; close.focus();
      });
      grid.append(button);
      return { button, entry, text: normalize(`${entry.name} ${entry.id} ${entry.category}`) };
    });
    const render = () => {
      const query = new URLSearchParams();
      if (search.value.trim()) query.set('q', search.value.trim());
      if (category !== 'All') query.set('category', category);
      history.replaceState(null, '', location.pathname + (query.size ? '?' + query : '') + location.hash);
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
    const openHash = () => {
      const card = cards.find(card => '#' + card.entry.id === location.hash);
      if (!card) { if (viewer.open) viewer.close(); return; }
      if (card.button.hidden) { category = 'All'; search.value = ''; render(); }
      card.button.click();
    };
    render();
    window.addEventListener('hashchange', openHash);
    openHash();
  } catch (error) {
    status.textContent = 'The collection could not load. Please refresh to try again.';
    document.querySelector('#load-retry').hidden = false;
  }
  document.querySelector('#load-retry').addEventListener('click', () => location.reload());
})();
