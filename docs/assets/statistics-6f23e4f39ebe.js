/* Independent, accessible viewport counters. Static HTML remains the fallback. */
(() => {
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const fa=number=>String(number).replace(/\d/g,digit=>'۰۱۲۳۴۵۶۷۸۹'[digit]);
 // Native count-up: one viewport-triggered run, independent of Motion and accessible to screen readers.
 const counters=[...document.querySelectorAll('[data-count]')];
 const counterFrames=new Map();let counterObserver;
 const finalCounters=()=>{
  counterObserver?.disconnect();
  counterFrames.forEach(frame=>cancelAnimationFrame(frame));counterFrames.clear();
  counters.forEach(el=>{el.textContent=fa(el.dataset.count);el.dataset.counterState='complete'});
 };
 const countUp=(el,index)=>{
  const target=Number(el.dataset.count),duration=2300,start=performance.now()+index*100;
  el.textContent=fa(0);el.dataset.counterState='running';
  const tick=now=>{
   if(reduced.matches){finalCounters();return}
   const progress=Math.max(0,Math.min(1,(now-start)/duration));
   el.textContent=fa(Math.floor(target*(1-Math.pow(1-progress,3))));
   if(progress<1)counterFrames.set(el,requestAnimationFrame(tick));
   else {el.textContent=fa(target);el.dataset.counterState='complete';counterFrames.delete(el)}
  };
  counterFrames.set(el,requestAnimationFrame(tick));
 };
 if(counters.length&&!reduced.matches&&'IntersectionObserver' in window){
  counters.forEach(el=>el.dataset.counterState='pending');
  counterObserver=new IntersectionObserver(entries=>{
   if(!entries.some(entry=>entry.isIntersecting))return;
   counterObserver.disconnect();counters.forEach(countUp);
  },{threshold:.55,rootMargin:"0px 0px -32px 0px"});
  counterObserver.observe(document.querySelector('.metrics'));
 }else finalCounters();
 reduced.addEventListener('change',event=>{if(event.matches)finalCounters()});
})();
