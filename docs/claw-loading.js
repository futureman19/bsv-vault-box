// Keep fallback art hidden until the final presentation is selected.
(function () {
  const wrap = document.querySelector('.machine-wrap');
  const play = document.getElementById('playBtn');
  let state = 'loading';
  const timer = setTimeout(() => settle('fallback'), 12000);
  function settle(next) {
    if (state !== 'loading') return;
    state = next;
    clearTimeout(timer);
    wrap.dataset.presentation = next;
    wrap.classList.remove('claw-loading');
    wrap.removeAttribute('aria-busy');
    play.disabled = false;
    play.textContent = 'PLAY';
  }
  window.clawPresentation = { settle, get state() { return state; } };
})();
