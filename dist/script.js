// Dark mode toggle
(function(){
  const btn = document.getElementById('toggleTheme');
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const saved = localStorage.getItem('report-theme');
  if(saved){ document.body.classList.toggle('dark', saved === 'dark'); }
  else if(prefersDark){ document.body.classList.add('dark'); }
  function updateLabel(){ btn.textContent = document.body.classList.contains('dark') ? 'Light Mode' : 'Dark Mode'; }
  btn.addEventListener('click', ()=>{
    document.body.classList.toggle('dark');
    localStorage.setItem('report-theme', document.body.classList.contains('dark') ? 'dark' : 'light');
    updateLabel();
  });
  updateLabel();
})();