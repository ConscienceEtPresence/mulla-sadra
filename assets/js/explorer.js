/* ============================================================
   EXPLORER.JS — la carte conceptuelle (« galaxie »).
   Lit window.MAP (défini dans la page, localisé) : nœuds + liens.
   Survol/clic d'un nœud → met en avant ce dont il dépend (amont)
   et ce qu'il rend possible (aval) ; ouvre sa fiche si elle existe.
   ============================================================ */
(function(){
  var M = window.MAP; if(!M) return;
  var svg = document.getElementById('galaxy'); if(!svg) return;
  var card = document.getElementById('galaxy-card');
  var T = M.i18n;
  var NS = 'http://www.w3.org/2000/svg';
  var W = 900, H = 560;
  svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);

  var byId = {}; M.nodes.forEach(function(n){ byId[n.id] = n; });
  function el(name, attrs){ var e = document.createElementNS(NS, name); for(var k in attrs) e.setAttribute(k, attrs[k]); return e; }

  // --- liens (aval = rend possible) ---
  var edgeEls = {};
  M.links.forEach(function(l, i){
    var a = byId[l.from], b = byId[l.to]; if(!a||!b) return;
    var line = el('line', { x1:a.x, y1:a.y, x2:b.x, y2:b.y, class:'g-edge' });
    line.dataset.from = l.from; line.dataset.to = l.to;
    svg.appendChild(line); edgeEls[l.from+'>'+l.to] = line;
  });

  // --- nœuds ---
  M.nodes.forEach(function(n){
    var g = el('g', { class:'g-node' + (n.url?'':' is-soon'), tabindex:0, role:'button' });
    g.dataset.id = n.id;
    g.appendChild(el('circle', { class:'halo', cx:n.x, cy:n.y, r:26 }));
    g.appendChild(el('circle', { class:'core', cx:n.x, cy:n.y, r:(n.big?7:5) }));
    var label = el('text', { class:'g-label', x:n.x, y:n.y - 16, 'text-anchor':'middle' });
    label.textContent = n.label;
    g.appendChild(label);
    var ar = el('text', { class:'g-ar', x:n.x, y:n.y + 30, 'text-anchor':'middle' });
    ar.setAttribute('lang','ar'); ar.textContent = n.ar;
    g.appendChild(ar);
    svg.appendChild(g);
    g.addEventListener('mouseenter', function(){ focus(n.id); });
    g.addEventListener('focus', function(){ focus(n.id); });
    g.addEventListener('click', function(){ if(n.url) location.href = n.url; else focus(n.id); });
    g.addEventListener('keydown', function(e){ if((e.key==='Enter'||e.key===' ')&&n.url){ e.preventDefault(); location.href=n.url; } });
  });
  svg.addEventListener('mouseleave', reset);

  function neighbors(id){
    var up=[], down=[];
    M.links.forEach(function(l){ if(l.to===id) up.push(l.from); if(l.from===id) down.push(l.to); });
    return { up:up, down:down };
  }
  function focus(id){
    var nb = neighbors(id);
    var lit = {}; lit[id]=1; nb.up.forEach(function(x){lit[x]=1;}); nb.down.forEach(function(x){lit[x]=1;});
    svg.querySelectorAll('.g-node').forEach(function(g){
      g.classList.toggle('dim', !lit[g.dataset.id]);
      g.classList.toggle('active', g.dataset.id===id);
    });
    svg.querySelectorAll('.g-edge').forEach(function(ln){
      ln.classList.toggle('lit', ln.dataset.from===id||ln.dataset.to===id);
      ln.classList.toggle('dim', !(ln.dataset.from===id||ln.dataset.to===id));
    });
    if(card) renderCard(id, nb);
  }
  function reset(){
    svg.querySelectorAll('.g-node').forEach(function(g){ g.classList.remove('dim','active'); });
    svg.querySelectorAll('.g-edge').forEach(function(ln){ ln.classList.remove('lit','dim'); });
    if(card) card.innerHTML = '<p class="g-hint">'+T.hint+'</p>';
  }
  function chip(id){ var n=byId[id]; return n?'<span class="g-chip"><span lang="ar">'+n.ar+'</span> '+n.label+'</span>':''; }
  function renderCard(id, nb){
    var n = byId[id];
    var html = '<div class="g-card-head"><span class="g-card-ar" lang="ar">'+n.ar+'</span>'+
      '<span class="g-card-tr">'+(n.tr||'')+'</span></div>'+
      '<h3>'+n.label+'</h3>';
    if(nb.up.length) html += '<p class="g-k up">↑ '+T.up+'</p><div class="g-chips">'+nb.up.map(chip).join('')+'</div>';
    if(nb.down.length) html += '<p class="g-k down">↓ '+T.down+'</p><div class="g-chips">'+nb.down.map(chip).join('')+'</div>';
    html += n.url ? '<a class="g-go" href="'+n.url+'">'+T.open+' →</a>' : '<p class="g-soon">'+T.soon+'</p>';
    card.innerHTML = html;
  }
  reset();
})();
