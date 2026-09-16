(() => {
  const key = 'arl-cookie-consent';
  const settings = document.querySelector('.cookie-settings');
  if (!settings) return;
  settings.setAttribute('aria-label', 'Cookie settings');
  const update = value => window.gtag?.('consent', 'update', {ad_storage:value,ad_user_data:value,ad_personalization:value,analytics_storage:value});
  const save = (value, banner) => {
    try { localStorage.setItem(key, value); } catch (_) {}
    update(value); banner.remove(); settings.hidden = false;
  };
  const show = () => {
    if (document.querySelector('.cookie-banner')) return;
    settings.hidden = true;
    const banner = document.createElement('aside');
    banner.className = 'cookie-banner'; banner.setAttribute('aria-label', 'Cookie choices');
    banner.innerHTML = '<button type="button" class="cookie-close" aria-label="Close cookie notice and reject optional cookies">×</button><p>Allow optional cookies to measure enquiries and advertising?</p><a href="/privacy-policy.html">Privacy policy</a><div class="cookie-actions"><button type="button" data-cookie-choice="denied">Reject</button><button type="button" class="cookie-accept" data-cookie-choice="granted">Accept</button></div>';
    banner.querySelector('.cookie-close').addEventListener('click', () => save('denied', banner));
    banner.querySelector('[data-cookie-choice="denied"]').addEventListener('click', () => save('denied', banner));
    banner.querySelector('[data-cookie-choice="granted"]').addEventListener('click', () => save('granted', banner));
    document.body.appendChild(banner);
  };
  settings.addEventListener('click', show);
  let saved; try { saved = localStorage.getItem(key); } catch (_) {}
  if (saved === 'granted' || saved === 'denied') update(saved); else show();
})();
