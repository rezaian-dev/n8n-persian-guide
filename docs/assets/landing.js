(() => {
 document.querySelector('#theme')?.addEventListener('click', () => {
  const next=document.documentElement.dataset.theme==='dark'?'light':'dark';
  document.documentElement.dataset.theme=next;
  try {localStorage.setItem('n8n-guide-theme',next)} catch {}
 });
})();
