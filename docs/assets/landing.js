/* Motion 14.9.0, locally bundled under MIT. No CDN or tracking. */
(() => {
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 document.querySelector('#theme')?.addEventListener('click',()=>{
  const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';
  document.documentElement.dataset.theme=theme;
  try{localStorage.setItem('n8n-guide-theme',theme)}catch{}
 });
 const progress=document.querySelector('#reading-progress');
 const updateProgress=()=>{
  const total=document.documentElement.scrollHeight-innerHeight;
  if(progress)progress.style.transform=`scaleX(${total>0?Math.min(1,scrollY/total):0})`;
 };
 addEventListener('scroll',updateProgress,{passive:true});updateProgress();
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
 hover('.feature,.preview-card,.module,.file-list>a,.illustration-gallery>a',el=>{
  if(reduced.matches)return;
  play(el,{y:-5},{duration:.28,ease:'easeOut'});
  return()=>play(el,{y:0},{duration:.35,ease:'easeOut'});
 });
 hover('.button,.nav-download',el=>{
  if(reduced.matches)return;
  play(el,{y:-3,scale:1.015},{duration:.22});
  return()=>play(el,{y:0,scale:1},{duration:.28});
 });
 document.querySelectorAll('.module').forEach(el=>el.addEventListener('toggle',()=>{
  if(el.open&&!reduced.matches)play(el.querySelector('ol'),{opacity:[0,1],y:[-7,0]},{duration:.3});
 }));
 const book=document.querySelector('.book-stage');
 const art=document.querySelector('.hero-art');
 if(book&&art&&matchMedia('(hover:hover) and (pointer:fine)').matches){
  art.addEventListener('pointermove',e=>{
   if(reduced.matches)return;
   const rect=art.getBoundingClientRect();
   const x=(e.clientX-rect.left)/rect.width-.5;
   const y=(e.clientY-rect.top)/rect.height-.5;
   play(book,{rotateY:9+x*9,rotateX:-y*5,rotateZ:-3},{duration:.35,ease:'easeOut'});
  });
  art.addEventListener('pointerleave',()=>play(book,{rotateY:9,rotateX:0,rotateZ:-3},{duration:.6,ease:'easeOut'}));
 }
 reduced.addEventListener('change',e=>{
  if(!e.matches)return;
  active.forEach(control=>control.stop());active.clear();
  document.querySelectorAll('[style]').forEach(el=>{
   if(el!==progress){el.style.removeProperty('opacity');el.style.removeProperty('transform')}
  });
 });
})();
