'use strict';
(() => {
  const $ = id => document.getElementById(id);
  const root = document.documentElement;
  const store = {get(key) {try {return localStorage.getItem(key);} catch {return null;}}, set(key, value) {try {localStorage.setItem(key, value);} catch {/* Reading works without storage. */}}};
  const fa = number => String(number).replace(/\d/g, digit => '۰۱۲۳۴۵۶۷۸۹'[digit]);
  const theme = $('reader-theme');
  theme.hidden = false;
  const themeLabel = () => {theme.textContent = root.dataset.theme === 'dark' ? 'تم روشن' : 'تم تیره'; theme.setAttribute('aria-pressed', String(root.dataset.theme === 'dark'));};
  themeLabel();
  theme.addEventListener('click', () => {root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';store.set('n8n-reader-theme', root.dataset.theme);themeLabel();});
  document.querySelector('.reader-tools').hidden = false;
  let size = Number(store.get('n8n-reader-size')) || 18;
  if (size < 14 || size > 24) size = 18;
  const resize = () => {root.style.setProperty('--reading-size', `${size}px`);$('font-value').value = fa(size);$('font-less').disabled = size <= 14;$('font-more').disabled = size >= 24;store.set('n8n-reader-size', size);};
  $('font-less').addEventListener('click', () => {size = Math.max(14, size - 1);resize();});
  $('font-more').addEventListener('click', () => {size = Math.min(24, size + 1);resize();});
  resize();

  const toc = $('reader-toc');
  const mobile = window.matchMedia('(max-width:760px)');
  toc.open = !mobile.matches;
  mobile.addEventListener('change', () => {toc.open = !mobile.matches;});
  const chapters = [...document.querySelectorAll('.reader-chapter')];
  const links = [...toc.querySelectorAll('a')];
  links.forEach(link => link.addEventListener('click', () => {if (mobile.matches) toc.open = false;}));
  const saved = store.get('n8n-reader-chapter');
  if (chapters.some(chapter => chapter.id === saved)) {
    const resume = $('reader-resume');
    resume.href = `#${saved}`;resume.hidden = false;
    resume.textContent = `ادامهٔ مطالعه: ${document.querySelector(`#${saved} h2`).textContent} ←`;
  }
  let active = '', scheduled = false;
  const updateReading = () => {
    scheduled = false;
    const offset = document.querySelector('.reader-header').offsetHeight + 70;
    let current = chapters[0];
    for (const chapter of chapters) {if (chapter.getBoundingClientRect().top <= offset) current = chapter;else break;}
    if (current.id !== active) {
      active = current.id;
      links.forEach(link => {if (link.hash === `#${active}`) link.setAttribute('aria-current', 'true');else link.removeAttribute('aria-current');});
      store.set('n8n-reader-chapter', active);
    }
    const total = document.documentElement.scrollHeight - innerHeight;
    $('reader-progress').style.width = `${total > 0 ? Math.max(0, Math.min(100, scrollY / total * 100)) : 0}%`;
  };
  window.addEventListener('scroll', () => {if (!scheduled) {scheduled = true;requestAnimationFrame(updateReading);}}, {passive:true});
  window.addEventListener('load', updateReading);

  document.querySelectorAll('.reader-chapter pre').forEach(pre => {
    const code = pre.querySelector('code');
    if (!code || !navigator.clipboard || !window.isSecureContext) return;
    const button = document.createElement('button');
    button.type = 'button';button.className = 'copy-code';button.textContent = 'کپی کد';
    button.setAttribute('aria-label', 'کپی کردن این قطعه کد');
    button.addEventListener('click', async () => {
      try {await navigator.clipboard.writeText(code.textContent);button.textContent = 'کپی شد ✓';}
      catch {button.textContent = 'کپی نشد؛ متن را انتخاب کنید';}
      setTimeout(() => {button.textContent = 'کپی کد';}, 2200);
    });
    pre.prepend(button);
  });

  // Literal matching only; never inject user input as HTML or a regular expression.
  const normalize = text => text.toLowerCase().replace(/ي/g, 'ی').replace(/ك/g, 'ک').replace(/\u200c/g, ' ').replace(/[۰-۹]/g, digit => String('۰۱۲۳۴۵۶۷۸۹'.indexOf(digit)));
  let matches = [], selected = -1;
  const status = $('search-status');
  const clear = () => {
    matches.forEach(mark => {const parent = mark.parentNode;mark.replaceWith(document.createTextNode(mark.textContent));parent.normalize();});
    matches = [];selected = -1;
    status.parentElement.classList.remove('has-results');
    ['match-prev', 'match-next', 'search-clear'].forEach(id => {$(id).hidden = true;});
    status.textContent = '';
  };
  const select = index => {
    if (!matches.length) return;
    if (selected >= 0) matches[selected].classList.remove('current-match');
    selected = (index + matches.length) % matches.length;
    matches[selected].classList.add('current-match');
    matches[selected].scrollIntoView({block:'center', behavior:'instant'});
    status.textContent = `${fa(selected + 1)} از ${fa(matches.length)} نتیجه${matches.length >= 1000 ? ' · سقف نمایش ۱۰۰۰ نتیجه؛ عبارت دقیق‌تری بنویسید' : ''}`;
  };
  $('reader-search-form').addEventListener('submit', event => {
    event.preventDefault();clear();
    const query = normalize($('reader-search').value.trim());
    if (query.length < 2) {status.textContent = 'دست‌کم دو نویسه وارد کنید.';return;}
    const nodes = [];
    chapters.forEach(chapter => {
      const walker = document.createTreeWalker(chapter, NodeFilter.SHOW_TEXT, {acceptNode: node => node.parentElement.closest('button,script,style') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT});
      let node;while ((node = walker.nextNode())) nodes.push(node);
    });
    for (const node of nodes) {
      const text = node.nodeValue, normalized = normalize(text);
      if (!normalized.includes(query)) continue;
      const fragment = document.createDocumentFragment();
      let from = 0, position;
      while ((position = normalized.indexOf(query, from)) !== -1 && matches.length < 1000) {
        fragment.append(document.createTextNode(text.slice(from, position)));
        const mark = document.createElement('mark');mark.textContent = text.slice(position, position + query.length);fragment.append(mark);matches.push(mark);from = position + query.length;
      }
      fragment.append(document.createTextNode(text.slice(from)));node.replaceWith(fragment);
      if (matches.length >= 1000) break;
    }
    $('search-clear').hidden = false;
    if (!matches.length) {status.textContent = 'نتیجه‌ای پیدا نشد.';return;}
    status.parentElement.classList.add('has-results');
    $('match-prev').hidden = false;$('match-next').hidden = false;select(0);
  });
  $('match-prev').addEventListener('click', () => select(selected - 1));
  $('match-next').addEventListener('click', () => select(selected + 1));
  $('search-clear').addEventListener('click', () => {clear();$('reader-search').value = '';$('reader-search').focus();});
  $('reader-search').addEventListener('search', () => {if (!$('reader-search').value) clear();});
})();
