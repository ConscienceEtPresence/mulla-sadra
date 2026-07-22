/* ============================================================
   NOTION.JS — profondeur (5 niveaux), translittération, infobulles.
   Le contenu reste lisible sans JS : tous les niveaux existent dans
   le HTML ; ce script ne fait que montrer un niveau à la fois.
   ============================================================ */
(function(){
  var LANG = document.documentElement.lang === 'en' ? 'en' : 'fr';

  /* --- sélecteur de profondeur --- */
  function setLevel(n){
    document.querySelectorAll('.depth button').forEach(function(b){b.classList.toggle('on',+b.dataset.lv===n);b.setAttribute('aria-selected',+b.dataset.lv===n);});
    document.querySelectorAll('.level').forEach(function(l){l.classList.toggle('on',+l.dataset.lv===n);});
    var t=document.querySelector('.temps');if(t)t.scrollIntoView({behavior:'smooth',block:'start'});
    try{history.replaceState(null,'','#n'+n);}catch(e){}
  }
  document.querySelectorAll('.depth button').forEach(function(b){b.addEventListener('click',function(){setLevel(+b.dataset.lv);});});
  // niveau initial depuis l'ancre #n3
  var m=(location.hash||'').match(/^#n([1-5])$/);
  if(m) setLevel(+m[1]);

  /* --- translittération repliable (niveau IV) --- */
  document.querySelectorAll('[data-tr-toggle]').forEach(function(btn){
    var row=document.getElementById(btn.getAttribute('data-tr-toggle'));
    var show=btn.getAttribute('data-show')||'Afficher la translittération';
    var hide=btn.getAttribute('data-hide')||'Masquer la translittération';
    btn.addEventListener('click',function(){
      var on=row.classList.toggle('show');btn.classList.toggle('on',on);btn.textContent=on?hide:show;
    });
  });

  /* --- infobulles de termes arabes --- */
  var TERMS={
    wujud:{ar:'وُجُود',tr:'al-wujūd',fr:"L'existence, l'acte d'être.",en:'Existence, the act of being.'},
    mahiyya:{ar:'مَاهِيَّة',tr:'māhiyya',fr:"L'essence, la quiddité — « ce qu'est » une chose.",en:'Essence, quiddity — "what a thing is".'},
    asil:{ar:'أَصِيل',tr:'aṣīl',fr:'Fondamental : ce qui a la réalité par soi.',en:'Fundamental: what has reality by itself.'},
    itibari:{ar:'اِعْتِبَارِيّ',tr:'iʿtibārī',fr:"De raison : posé par la considération de l'esprit.",en:'Of the mind: posited by mental consideration.'},
    tashkik:{ar:'تَشْكِيك',tr:'tashkīk',fr:"La gradation analogique de l'existence, par degrés d'intensité.",en:'The analogical gradation of existence, by degrees of intensity.'},
    haraka:{ar:'حَرَكَة جَوْهَرِيَّة',tr:'ḥaraka jawhariyya',fr:'Le mouvement substantiel : la substance même se renouvelle.',en:'Substantial motion: substance itself is renewed.'},
    nafs:{ar:'نَفْس',tr:'nafs',fr:"L'âme, corporelle dans son apparition, spirituelle dans sa subsistance.",en:'The soul, bodily in origin, spiritual in subsistence.'},
    maad:{ar:'مَعَاد',tr:'maʿād',fr:'Le retour, la résurrection — terme du quatrième voyage.',en:'The return, resurrection — end of the fourth journey.'}
  };
  var tip=document.createElement('div');tip.className='tip';document.body.appendChild(tip);
  function show(el){
    var t=TERMS[el.dataset.term];if(!t)return;
    tip.innerHTML='<span class="ar">'+t.ar+'</span><span class="tr">'+t.tr+'</span><div class="df">'+(LANG==='fr'?t.fr:t.en)+'</div>';
    tip.classList.add('show');
    var r=el.getBoundingClientRect(),top=r.bottom+8,left=Math.min(r.left,window.innerWidth-tip.offsetWidth-14);
    if(top+tip.offsetHeight>window.innerHeight-10)top=r.top-tip.offsetHeight-8;
    tip.style.top=Math.max(8,top)+'px';tip.style.left=Math.max(8,left)+'px';
  }
  function hide(){tip.classList.remove('show');}
  document.addEventListener('mouseover',function(e){var t=e.target.closest('.term');if(t)show(t);});
  document.addEventListener('mouseout',function(e){if(e.target.closest('.term'))hide();});
  document.addEventListener('focusin',function(e){var t=e.target.closest('.term');if(t)show(t);});
  document.addEventListener('focusout',hide);
})();
