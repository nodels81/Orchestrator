/* ═══════════════════════════════════════════════════════════════════
   startseite.js — Materialansicht und Größenfinder.

   Ausgelesen aus web/startseite-nachtwerkstatt.html. Der Shader ist der
   eine schwere Effekt dieser Seite; die Abschaltmatrix und der
   Standbild-Ersatz gehören dazu und sind nicht wegzulassen.
   ═══════════════════════════════════════════════════════════════════ */

/* ═══════════════════════════════════════════════════════════════════
   Der eine schwere Effekt: Fettleder im wandernden Streiflicht.
   Abschaltmatrix nach Regelwerk, statischer Ersatz per CSS-Klasse.
   ═══════════════════════════════════════════════════════════════════ */
(function(){
  var leinwand = document.getElementById('leder');
  var hinweis  = document.getElementById('lederHinweis');
  if(!leinwand) return;

  function ersatz(grund){
    leinwand.classList.add('aus');
    if(hinweis) hinweis.textContent = grund;
  }

  var sparsam =
    matchMedia('(prefers-reduced-motion: reduce)').matches ||
    (navigator.hardwareConcurrency || 8) <= 4 ||
    (navigator.connection && navigator.connection.saveData === true);

  if(sparsam){ ersatz('Standbild — Bewegung ist abgeschaltet'); return; }

  var gl = leinwand.getContext('webgl', {antialias:false, alpha:false, powerPreference:'low-power'})
        || leinwand.getContext('experimental-webgl');
  if(!gl){ ersatz('Standbild — kein WebGL verfügbar'); return; }

  var vsQuelle =
    'attribute vec2 p;void main(){gl_Position=vec4(p,0.0,1.0);}';

  var fsQuelle = [
    'precision mediump float;',
    'uniform vec2 u_res; uniform vec2 u_licht;',
    'float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}',
    'float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);',
    ' float a=hash(i),b=hash(i+vec2(1.0,0.0)),c=hash(i+vec2(0.0,1.0)),d=hash(i+vec2(1.0,1.0));',
    ' return mix(mix(a,b,f.x),mix(c,d,f.x),f.y);}',
    'float fbm(vec2 p){float v=0.0,a=0.5;for(int i=0;i<5;i++){v+=a*noise(p);p*=2.03;a*=0.5;}return v;}',
    'float hoehe(vec2 p){return fbm(p*2.1)*0.62+fbm(p*8.5)*0.24;}',
    'void main(){',
    ' vec2 uv=gl_FragCoord.xy/u_res;',
    ' vec2 p=vec2(uv.x*u_res.x/u_res.y,uv.y)*7.5;',
    ' float e=0.012;',
    ' float h=hoehe(p);',
    ' float hx=hoehe(p+vec2(e,0.0));',
    ' float hy=hoehe(p+vec2(0.0,e));',
    ' vec3 n=normalize(vec3((h-hx)*7.0,(h-hy)*7.0,1.0));',
    ' vec3 L=normalize(vec3((u_licht-uv)*vec2(u_res.x/u_res.y,1.0),0.42));',
    ' float diff=max(dot(n,L),0.0);',
    ' vec3 A=normalize(vec3(0.0,0.0,1.0));',
    ' float spec=pow(max(dot(reflect(-L,n),A),0.0),26.0);',
    ' vec3 leder=mix(vec3(0.085,0.062,0.040),vec3(0.36,0.245,0.135),h);',
    ' vec3 farbe=leder*(0.22+0.95*diff)+vec3(0.96,0.84,0.58)*spec*0.5;',
    ' farbe*=1.0-0.55*length(uv-vec2(0.5));',
    ' gl_FragColor=vec4(farbe,1.0);',
    '}'
  ].join('\n');

  function bauen(art, quelle){
    var s = gl.createShader(art);
    gl.shaderSource(s, quelle); gl.compileShader(s);
    if(!gl.getShaderParameter(s, gl.COMPILE_STATUS)) return null;
    return s;
  }
  var vs = bauen(gl.VERTEX_SHADER, vsQuelle);
  var fs = bauen(gl.FRAGMENT_SHADER, fsQuelle);
  if(!vs || !fs){ ersatz('Standbild — Shader nicht verfügbar'); return; }

  var prog = gl.createProgram();
  gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
  if(!gl.getProgramParameter(prog, gl.LINK_STATUS)){ ersatz('Standbild — Shader nicht verfügbar'); return; }
  gl.useProgram(prog);

  var puffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, puffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 3,-1, -1,3]), gl.STATIC_DRAW);
  var ort = gl.getAttribLocation(prog, 'p');
  gl.enableVertexAttribArray(ort);
  gl.vertexAttribPointer(ort, 2, gl.FLOAT, false, 0, 0);

  var uRes = gl.getUniformLocation(prog, 'u_res');
  var uLicht = gl.getUniformLocation(prog, 'u_licht');

  var ziel = {x:0.34, y:0.68}, ist = {x:0.34, y:0.68}, beruehrt = false, laeuft = false, t = 0;

  function messen(){
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var b = leinwand.getBoundingClientRect();
    leinwand.width = Math.max(1, Math.round(b.width * dpr));
    leinwand.height = Math.max(1, Math.round(b.height * dpr));
    gl.viewport(0, 0, leinwand.width, leinwand.height);
    gl.uniform2f(uRes, leinwand.width, leinwand.height);
  }

  function bild(){
    if(!laeuft) return;
    t += 0.006;
    if(!beruehrt){ ziel.x = 0.5 + Math.cos(t) * 0.3; ziel.y = 0.5 + Math.sin(t * 0.8) * 0.22; }
    ist.x += (ziel.x - ist.x) * 0.07;
    ist.y += (ziel.y - ist.y) * 0.07;
    gl.uniform2f(uLicht, ist.x, ist.y);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    requestAnimationFrame(bild);
  }

  leinwand.addEventListener('pointermove', function(ev){
    var b = leinwand.getBoundingClientRect();
    beruehrt = true;
    ziel.x = (ev.clientX - b.left) / b.width;
    ziel.y = 1 - (ev.clientY - b.top) / b.height;
  });
  leinwand.addEventListener('pointerleave', function(){ beruehrt = false; });
  addEventListener('resize', messen, {passive:true});

  /* Läuft nur, solange die Fläche sichtbar ist. */
  var beobachter = new IntersectionObserver(function(eintraege){
    var sichtbar = eintraege[0].isIntersecting;
    if(sichtbar && !laeuft){ laeuft = true; requestAnimationFrame(bild); }
    else if(!sichtbar){ laeuft = false; }
  }, {rootMargin:'120px'});

  messen();
  beobachter.observe(leinwand);
})();
