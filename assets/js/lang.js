/* ============================================================
   LANG.JS — mémoire de préférence FR/EN.
   Les liens FR/EN sont écrits en dur dans chaque page (miroir /en/),
   donc le site bascule sans JavaScript. Ce script ne fait qu'une chose :
   sur les pages d'accueil, rediriger vers la langue mémorisée.
   ============================================================ */
(function(){
  var KEY='ms_lang';
  var segs=location.pathname.split('/');
  var file=segs[segs.length-1]||'';
  var isEN=segs.indexOf('en')!==-1;
  var atHome=(file===''||file==='index.html');

  // mémorise le choix quand on clique un lien de bascule
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-lang]');
    if(a){try{localStorage.setItem(KEY,a.getAttribute('data-lang'));}catch(e){}}
  });

  if(!atHome) return;
  try{
    var pref=localStorage.getItem(KEY);
    if(pref==='en'&&!isEN){var s=segs.slice();s.pop();s.push('en');location.replace(s.join('/')+'/'+file+location.search+location.hash);}
    if(pref==='fr'&&isEN){var s2=segs.slice();var i=s2.indexOf('en');s2.splice(i,1);location.replace(s2.join('/')+'/'+file+location.search+location.hash);}
  }catch(e){}
})();
