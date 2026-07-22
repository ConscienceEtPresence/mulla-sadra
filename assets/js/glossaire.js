/* ============================================================
   GLOSSAIRE.JS — filtre instantané à la frappe.
   Les entrées sont dans le HTML (lisible sans JS) ; on masque
   simplement celles qui ne correspondent pas à la recherche.
   ============================================================ */
(function(){
  var input=document.querySelector('.gloss-search');
  var count=document.querySelector('.gloss-count');
  var list=document.querySelector('.gloss-list');
  if(!input||!list)return;
  var entries=Array.prototype.slice.call(list.querySelectorAll('.gloss-entry'));
  var tmpl=count?count.getAttribute('data-tmpl')||'{n}':'{n}';
  var empty=list.getAttribute('data-empty')||'Aucun terme.';
  function norm(s){return (s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');}
  function run(){
    var q=norm(input.value.trim());var n=0;
    entries.forEach(function(e){
      var hay=norm(e.getAttribute('data-search')||e.textContent);
      var ok=!q||hay.indexOf(q)!==-1;e.style.display=ok?'':'none';if(ok)n++;
    });
    if(count)count.textContent=tmpl.replace('{n}',n);
    var ph=list.querySelector('.gloss-empty');
    if(n===0&&!ph){ph=document.createElement('p');ph.className='gloss-empty';ph.textContent=empty;list.appendChild(ph);}
    else if(n>0&&ph){ph.remove();}
  }
  input.addEventListener('input',run);run();
})();
