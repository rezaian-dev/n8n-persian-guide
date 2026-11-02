/* Shared, dependency-free RTL drawer. Native dialog supplies focus trapping and inert background. */
(() => {
  const trigger = document.querySelector('[data-drawer-trigger]');
  const source = document.querySelector('[data-drawer-source]');
  if (!trigger || !source || typeof HTMLDialogElement === 'undefined') return;
  const root = document.documentElement;
  const reader = document.body.classList.contains('publication-reader');
  const mobile = matchMedia('(max-width:900px)');
  const reduced = matchMedia('(prefers-reduced-motion:reduce)');
  const svg = (paths, className = '') => `<svg class="interface-icon ${className}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths}</svg>`;
  const icons = {
    menu: svg('<path d="M4 7h16M8 12h12M4 17h16"/>'),
    close: svg('<path d="m6 6 12 12M6 18 18 6"/>'),
    arrow: svg('<path d="M19 12H5m6-6-6 6 6 6"/>'),
    book: svg('<path d="M12 6c-3-2-6-2-9-1v14c3-1 6-1 9 1 3-2 6-2 9-1V5c-3-1-6-1-9 1Zm0 0v14"/><path d="M6 9h3m6 0h3"/>'),
    spark: svg('<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5L12 3Z"/>'),
    grid: svg('<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/>'),
    route: svg('<circle cx="6" cy="5" r="2"/><circle cx="18" cy="19" r="2"/><path d="M6 7v8a4 4 0 0 0 4 4h2m6-2V9a4 4 0 0 0-4-4h-2"/>'),
    person: svg('<circle cx="12" cy="8" r="4"/><path d="M4 21v-2a8 8 0 0 1 16 0v2"/>'),
    download: svg('<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>'),
  };
  trigger.innerHTML = icons.menu;
  trigger.hidden = false;
  trigger.setAttribute('aria-controls', 'mobile-drawer');
  trigger.setAttribute('aria-haspopup', 'dialog');
  trigger.setAttribute('aria-expanded', 'false');
  trigger.setAttribute('aria-label', reader ? 'بازکردن فهرست فصل‌ها' : 'بازکردن منوی سایت');
  const dialog = document.createElement('dialog');
  dialog.id = 'mobile-drawer';dialog.className = 'side-drawer';
  dialog.setAttribute('aria-labelledby', 'drawer-title');
  dialog.innerHTML = `<div class="drawer-shell"><div class="drawer-head"><a class="drawer-logo" href="${reader ? '../' : '#about'}"><span class="drawer-logo-icon">${icons.book}</span><span><b dir="ltr">n8n / PERSIAN</b><small>مرجع مهندسی اتوماسیون</small></span></a><button class="drawer-close" type="button" aria-label="بستن منو" autofocus>${icons.close}</button></div><div class="drawer-intro"><span class="drawer-eyebrow">${reader ? 'YOUR READING SPACE' : 'A BETTER WAY TO AUTOMATE'}</span><h2 id="drawer-title">${reader ? 'فصل بعدی،<br><em>یک قدم عمیق‌تر.</em>' : 'از اینجا،<br><em>جریان را بسازید.</em>'}</h2><p>${reader ? '۲۶ فصل کاربردی + پیوست‌ها' : 'یک مرجع فارسی؛ از اولین رویداد تا سیستم قابل‌اعتماد.'}</p></div><nav class="drawer-nav" aria-label="${reader ? 'فهرست فصل‌های کتاب' : 'منوی موبایل'}"></nav><div class="drawer-bottom"><a class="drawer-download" href="${reader ? '../' : ''}N8N-Persian-Guide.pdf" download>${icons.download}<span>دریافت نسخهٔ PDF<small>۷۱ صفحه · همراه شما، آفلاین</small></span>${icons.arrow}</a><p><span></span>بدون ثبت‌نام · بدون ردیابی</p></div></div>`;
  const nav = dialog.querySelector('.drawer-nav');
  const sourceLinks = [...source.querySelectorAll('a')];
  const navigationIcons = ['spark', 'grid', 'book', 'book', 'route', 'person'];
  sourceLinks.forEach((original, index) => {
    const link = document.createElement('a');
    link.href = original.getAttribute('href');link.className = 'drawer-link';
    const badge = document.createElement('span');badge.className = 'drawer-link-icon';
    if (reader) badge.textContent = String(index + 1).padStart(2, '0').replace(/\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]);
    else badge.innerHTML = icons[navigationIcons[index] || 'book'];
    const label = document.createElement('span');label.className = 'drawer-link-label';
    label.textContent = original.textContent.replace(reader ? /^[۰-۹]+\.\s*/ : /^$/, '');
    const arrow = document.createElement('span');arrow.className = 'drawer-link-arrow';arrow.innerHTML = icons.arrow;
    link.append(badge, label, arrow);nav.append(link);
  });
  document.body.append(dialog);
  root.classList.add('drawer-ready');
  let closing = false, timer;
  const close = after => {
    if (!dialog.open || closing) return;
    closing = true;dialog.classList.remove('drawer-visible');
    const finish = () => {
      clearTimeout(timer);dialog.close();closing = false;root.classList.remove('drawer-scroll-lock');
      trigger.setAttribute('aria-expanded', 'false');trigger.focus({preventScroll:true});
      if (typeof after === 'function') after();
    };
    if (reduced.matches) finish();else timer = setTimeout(finish, 300);
  };
  const open = () => {
    if (dialog.open || !mobile.matches) return;
    nav.querySelectorAll('a').forEach((link, index) => {
      if (sourceLinks[index].hasAttribute('aria-current')) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    closing = false;dialog.showModal();root.classList.add('drawer-scroll-lock');trigger.setAttribute('aria-expanded', 'true');
    requestAnimationFrame(() => requestAnimationFrame(() => {if (dialog.open && !closing) dialog.classList.add('drawer-visible');}));
  };
  trigger.addEventListener('click', open);
  dialog.querySelector('.drawer-close').addEventListener('click', () => close());
  dialog.addEventListener('cancel', event => {event.preventDefault();close();});
  dialog.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const focusable = [...dialog.querySelectorAll('a[href],button:not([disabled]),[tabindex="0"]')].filter(element => element.getClientRects().length);
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {event.preventDefault();last.focus();}
    else if (!event.shiftKey && document.activeElement === last) {event.preventDefault();first.focus();}
  });
  dialog.addEventListener('click', event => {
    const rect = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) close();
  });
  dialog.querySelectorAll('a:not([download])').forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    close(() => {
      const url = new URL(link.href);
      if (url.origin === location.origin && url.pathname === location.pathname && url.hash) {
        const target = document.getElementById(decodeURIComponent(url.hash.slice(1)));
        if (target) {history.pushState(null, '', url.hash);target.scrollIntoView({behavior:reduced.matches || Math.abs(target.getBoundingClientRect().top) > innerHeight * 3 ? 'instant' : 'smooth', block:'start'});target.setAttribute('tabindex','-1');target.focus({preventScroll:true});}
      } else location.assign(link.href);
    });
  }));
  dialog.querySelector('[download]').addEventListener('click', () => close());
  const sync = () => {
    trigger.hidden = !mobile.matches;
    if (reader) document.querySelector('.reader-sidebar').hidden = mobile.matches;
    else source.hidden = mobile.matches;
    if (!mobile.matches && dialog.open) {clearTimeout(timer);dialog.close();closing = false;dialog.classList.remove('drawer-visible');root.classList.remove('drawer-scroll-lock');trigger.setAttribute('aria-expanded','false');}
  };
  mobile.addEventListener('change', sync);sync();
})();
