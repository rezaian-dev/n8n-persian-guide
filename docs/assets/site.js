(() => {
 const theme = document.querySelector('#theme');
 theme?.addEventListener('click', () => {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  try {localStorage.setItem('n8n-guide-theme', next)} catch {}
 });
 const progress = document.querySelector('#progress');
 const update = () => {
  const height = document.documentElement.scrollHeight - innerHeight;
  progress.style.width = `${height > 0 ? Math.min(100, Math.max(0, scrollY / height * 100)) : 0}%`;
 };
 addEventListener('scroll', update, {passive:true}); addEventListener('resize', update); update();
 const links = [...document.querySelectorAll('#toc a')];
 document.querySelector('#toc-search')?.addEventListener('input', event => {
  const query = event.target.value.trim().toLocaleLowerCase('fa');
  links.forEach(link => link.hidden = !link.textContent.toLocaleLowerCase('fa').includes(query));
 });
 if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
   entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    links.forEach(link => {
     const active = link.hash === `#${entry.target.id}`;
     link.classList.toggle('active', active);
     if (active) link.setAttribute('aria-current','location'); else link.removeAttribute('aria-current');
    });
   });
  }, {rootMargin:'-12% 0px -65% 0px'});
  document.querySelectorAll('article h2').forEach(h => observer.observe(h));
 }
 document.querySelectorAll('article pre').forEach(pre => {
  const code = pre.querySelector('code'); if (!code) return;
  const language = [...code.classList].find(name => name.startsWith('language-'));
  if (language) {const label=document.createElement('span');label.className='code-lang';label.textContent=language.slice(9);pre.append(label)}
  const button=document.createElement('button');button.type='button';button.className='code-copy';button.textContent='کپی کد';button.setAttribute('aria-label','کپی نمونه کد');
  button.addEventListener('click', async () => {
   try {await navigator.clipboard.writeText(code.textContent);button.textContent='کپی شد ✓'}
   catch {button.textContent='متن را انتخاب و کپی کنید'}
   setTimeout(()=>button.textContent='کپی کد',2200);
  });
  pre.append(button);
 });
})();
