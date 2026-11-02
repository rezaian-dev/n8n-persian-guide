/* Motion 14.9.0, locally bundled under MIT. No CDN or tracking. */
(() => {
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const themeButton=document.querySelector('#theme');
 const syncTheme=()=>{
  const dark=document.documentElement.dataset.theme==='dark';
  themeButton?.setAttribute('aria-pressed',String(dark));
  themeButton?.setAttribute('aria-label',dark?'فعال‌کردن تم روشن':'فعال‌کردن تم تیره');
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content',dark?'#0b1725':'#f7f7f2');
 };
 syncTheme();
 const header=document.querySelector('.site-header');
 const menu=document.querySelector('#menu-toggle');
 const nav=document.querySelector('#primary-nav');
 if(header&&menu&&nav){
  const links=[...nav.querySelectorAll('a')];
  const observer=new IntersectionObserver(entries=>{
   const entry=entries.filter(e=>e.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];
   if(!entry)return;
   links.forEach(link=>{if(link.hash==='#'+entry.target.id)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current')});
  },{rootMargin:'-15% 0px -60% 0px',threshold:0});
  links.forEach(link=>{const target=link.hash?document.getElementById(link.hash.slice(1)):null;if(target)observer.observe(target)});
 }

 document.querySelector('#theme')?.addEventListener('click',()=>{
  const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';
  document.documentElement.dataset.theme=theme;syncTheme();
  try{localStorage.setItem('n8n-theme',theme);localStorage.setItem('n8n-guide-theme',theme)}catch{}
 });
 const progress=document.querySelector('#reading-progress');
 const updateProgress=()=>{
  const total=document.documentElement.scrollHeight-innerHeight;
  if(progress)progress.style.transform=`scaleX(${total>0?Math.min(1,scrollY/total):0})`;
 };
 addEventListener('scroll',updateProgress,{passive:true});updateProgress();
 // Useful interactions work independently of the animation library.
 const normalize=value=>value.toLowerCase().replace(/ي/g,'ی').replace(/ك/g,'ک').trim();
 const search=document.querySelector('#chapter-search');
 const modules=[...document.querySelectorAll('.module')];
 const status=document.querySelector('#chapter-status');
 const reset=document.querySelector('#reset-search');
 const fa=value=>String(value).replace(/[0-9]/g,d=>'۰۱۲۳۴۵۶۷۸۹'[d]);
 const filterChapters=()=>{
  const term=normalize(search.value);let count=0;
  modules.forEach(module=>{
   let matches=0;
   module.querySelectorAll('li').forEach(row=>{
    const text=row.querySelector('.chapter-link>span:nth-child(2)')?.textContent||'';
    const show=!term||normalize(text).includes(term);row.hidden=!show;if(show)matches++;
   });
   module.hidden=matches===0;
   if(term)module.open=matches>0;else module.open=false;
   module.removeAttribute('data-selected');count+=matches;
  });
  status.textContent=term?`${fa(count)} فصل پیدا شد`:'۲۶ فصل در ۶ بخش';
  reset.hidden=!term;document.querySelector('#no-results').hidden=count!==0;
 };
 if(search){
  document.querySelector('.curriculum-tools').hidden=false;
  search.addEventListener('input',filterChapters);
  reset.addEventListener('click',()=>{search.value='';filterChapters();search.focus()});
  document.addEventListener('keydown',e=>{
   if(e.key==='/'&&!e.ctrlKey&&!e.metaKey&&!e.altKey&&!document.querySelector('dialog[open]')&&!e.target.closest('input,textarea,[contenteditable]')){
    e.preventDefault();search.scrollIntoView({block:'center',behavior:reduced.matches?'instant':'smooth'});search.focus({preventScroll:true});
   }
  });
 }
 const trackModules={start:[0,1],reliable:[2,3],ai:[4,5]};
 document.querySelectorAll('[data-track]').forEach(link=>link.addEventListener('click',()=>{
  search.value='';filterChapters();
  trackModules[link.dataset.track].forEach(index=>{modules[index].open=true;modules[index].dataset.selected='true'});
  status.textContent=`مسیر انتخاب‌شده: ${link.querySelector('h3').textContent}`;
 }));
 const dialog=document.querySelector('#page-preview');
 const pages=JSON.parse(document.querySelector('#preview-data').textContent);
 let currentPage=0;
 const showPage=index=>{
  currentPage=(index+pages.length)%pages.length;const item=pages[currentPage];
  const image=document.querySelector('#preview-image');image.src=item.src;image.alt=item.title;
  document.querySelector('#preview-caption').textContent=item.title;
  document.querySelector('#preview-position').textContent=`${fa(currentPage+1)} از ${fa(pages.length)}`;
  document.querySelector('#preview-pdf-link').href=`N8N-Persian-Guide.pdf#page=${item.page}`;
 };
 document.querySelectorAll('[data-preview]').forEach(button=>{
  if(typeof dialog.showModal!=='function')return;
  button.hidden=false;
  button.addEventListener('click',()=>{showPage(Number(button.dataset.preview));dialog.showModal();document.documentElement.style.overflow='hidden';mobileDownload.hidden=true});
 });
 document.querySelector('#preview-close').addEventListener('click',()=>dialog.close());
 document.querySelector('#preview-prev').addEventListener('click',()=>showPage(currentPage-1));
 document.querySelector('#preview-next').addEventListener('click',()=>showPage(currentPage+1));
 dialog.addEventListener('keydown',e=>{
  if(e.key==='ArrowLeft'){e.preventDefault();showPage(currentPage+1)}
  if(e.key==='ArrowRight'){e.preventDefault();showPage(currentPage-1)}
 });
 dialog.addEventListener('click',e=>{
  const rect=dialog.getBoundingClientRect();
  if(e.target===dialog&&(e.clientX<rect.left||e.clientX>rect.right||e.clientY<rect.top||e.clientY>rect.bottom))dialog.close();
 });
 const mobileDownload=document.querySelector('#mobile-download');
 const updateDownload=()=>{
  const hero=document.querySelector('.hero').getBoundingClientRect();
  const end=document.querySelector('#download').getBoundingClientRect();
  mobileDownload.hidden=hero.bottom>0||end.top<innerHeight||dialog.open;
 };
 addEventListener('scroll',updateDownload,{passive:true});addEventListener('resize',updateDownload);
 dialog.addEventListener('close',()=>{document.documentElement.style.removeProperty('overflow');updateDownload()});updateDownload();
 if(!window.Motion)return;
 const {animate,stagger,inView,hover}=Motion;
 const active=new Set();
 const play=(target,values,options)=>{
  if(reduced.matches)return;
  const control=animate(target,values,options);active.add(control);
  Promise.resolve(control).then(()=>active.delete(control)).catch(()=>{});
  return control;
 };
 // Everything remains visible if JavaScript, Motion, or animation support fails.
 if(!reduced.matches){
  play('.hero-copy > *',{opacity:[0,1],y:[18,0]},{duration:.75,delay:stagger(.075),ease:[.22,1,.36,1]});
  play('.hero-art',{opacity:[0,1],y:[25,0]},{duration:1.1,delay:.18,ease:[.22,1,.36,1]});
  const targets=document.querySelectorAll('.feature,.section-head,.preview-card,.module,.file-list>a,.author-section,.faq details,.download-section .wrap');
  inView(targets,el=>{
   if(reduced.matches)return;
   const values=el.matches('.section-head,.author-section,.download-section .wrap')?{opacity:[.25,1],y:[24,0]}:{opacity:[.25,1]};
   play(el,values,{duration:.7,ease:[.22,1,.36,1]});
  },{amount:.12});
 }
 hover('.feature,.preview-card,.module,.file-list>a,.illustration-gallery>a,.path-card',el=>{
  if(reduced.matches)return;
  play(el,{y:-5},{duration:.28,ease:'easeOut'});
  return()=>play(el,{y:0},{duration:.35,ease:'easeOut'});
 });
 // Magnetic motion is deliberately small and only runs with a fine pointer.
 hover('.button,.nav-download',el=>{
  if(reduced.matches||!matchMedia('(hover:hover) and (pointer:fine)').matches)return;
  const bounds=el.getBoundingClientRect();let frame=0;let point=null;
  const spring={type:'spring',stiffness:320,damping:28,mass:.6};
  play(el,{y:-2,scale:1.015},spring);
  const move=e=>{
   if(reduced.matches)return;
   point={x:Math.max(-1,Math.min(1,(e.clientX-bounds.left)/bounds.width*2-1)),y:Math.max(-1,Math.min(1,(e.clientY-bounds.top)/bounds.height*2-1))};
   if(frame)return;
   frame=requestAnimationFrame(()=>{frame=0;if(!reduced.matches&&point)play(el,{x:point.x*6,y:point.y*4-2,scale:1.015},spring)});
  };
  el.addEventListener('pointermove',move);
  return()=>{el.removeEventListener('pointermove',move);cancelAnimationFrame(frame);play(el,{x:0,y:0,scale:1},spring)};
 });
 document.querySelectorAll('.module').forEach(el=>el.addEventListener('toggle',()=>{
  if(el.open&&!reduced.matches)play(el.querySelector('ol'),{opacity:[0,1],y:[-7,0]},{duration:.3});
 }));
 reduced.addEventListener('change',e=>{
  if(!e.matches)return;
  active.forEach(control=>control.stop());active.clear();
  document.querySelectorAll('[style]').forEach(el=>{
   if(el!==progress){el.style.removeProperty('opacity');el.style.removeProperty('transform')}
  });
 });
})();
