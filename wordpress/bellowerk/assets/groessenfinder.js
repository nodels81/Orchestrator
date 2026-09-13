/* ═══════════════════════════════════════════════════════════════════
   groessenfinder.js — Halsumfang eingeben, Größe bekommen.

   Aus startseite.js herausgelöst, damit er auch auf der Produktseite
   laufen kann, ohne den Material-Shader mitzuschleppen. Er senkt
   Retouren am stärksten — dann gehört er dorthin, wo gekauft wird.
   ═══════════════════════════════════════════════════════════════════ */

/* ═══ Größenfinder ═══════════════════════════════════════════════ */
(function(){
  var eingabe = document.getElementById('umfang');
  if(!eingabe) return;
  var felder = {
    groesse: document.getElementById('groesse'),
    breite:  document.getElementById('breite'),
    bereich: document.getElementById('bereich'),
    laenge:  document.getElementById('laenge'),
    rat:     document.getElementById('rat')
  };
  var stufen = [
    {gr:'S',  von:28, bis:34, breite:'20 mm', laenge:'400 mm'},
    {gr:'M',  von:34, bis:42, breite:'25 mm', laenge:'480 mm'},
    {gr:'L',  von:42, bis:50, breite:'30 mm', laenge:'560 mm'},
    {gr:'XL', von:50, bis:60, breite:'40 mm', laenge:'660 mm'}
  ];

  function rechnen(){
    var cm = parseFloat(eingabe.value);
    if(isNaN(cm)){ return; }
    var treffer = null;
    for(var i = 0; i < stufen.length; i++){
      if(cm <= stufen[i].bis){ treffer = stufen[i]; break; }
    }
    if(cm < 28){
      felder.groesse.textContent = '–';
      felder.breite.textContent = 'nach Maß';
      felder.bereich.textContent = 'unter 28 cm';
      felder.laenge.textContent = 'nach Maß';
      felder.rat.textContent = 'Bitte anfragen, wir fertigen nach Maß';
      return;
    }
    if(!treffer){
      felder.groesse.textContent = '–';
      felder.breite.textContent = 'nach Maß';
      felder.bereich.textContent = 'über 60 cm';
      felder.laenge.textContent = 'nach Maß';
      felder.rat.textContent = 'Bitte anfragen, wir fertigen nach Maß';
      return;
    }
    felder.groesse.textContent = treffer.gr;
    felder.breite.textContent = treffer.breite;
    felder.bereich.textContent = treffer.von + ' bis ' + treffer.bis + ' cm';
    felder.laenge.textContent = treffer.laenge;
    felder.rat.textContent = 'Hamburg No. 1 in Größe ' + treffer.gr;
  }
  eingabe.addEventListener('input', rechnen);
  rechnen();
})();
