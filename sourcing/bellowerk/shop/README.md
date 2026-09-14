# Shop-Seite Hamburg Nr. 1

`index.html` ist der verkaufsfertige Entwurf der Produktseite für HB-01 „Hamburg Nr. 1“:
Text, Maßtabelle, Pflegehinweis, Herstellerangaben, Preisvorschlag — und an jeder Stelle,
an der ein Produktfoto hingehört, steht, welches Foto das sein muss.

Die Bilder selbst fehlen. Sie müssen am fertigen Stück fotografiert werden; die Liste der
acht Aufnahmen steht am Ende der Seite. Bis dahin zeigt die Bühne die Werkstattzeichnung
aus `../zeichnungen/HB-01-hamburg.svg`.

## Offen, bevor die Seite online geht

1. Herkunftsangabe — „aus eigener Werkstatt“ passt nicht mehr, wenn in China gefertigt wird.
2. GPSR: Name und Postanschrift des Inverkehrbringers.
3. Patch trägt noch den alten Markennamen; erst Vektorlogo, dann Goldmuster, dann Shooting.
4. Preis 99 € bestätigen und gegen Hamburg Nr. 4 staffeln.

## Bauen

Die Seite referenziert `media/HB-01-hamburg.png` — dieselbe verkleinerte Zeichnung wie die
Freigabe-Mappe. Mit `python3 sourcing/bellowerk/freigabe/bauen.py` erzeugen und beim
Veröffentlichen aus `../freigabe/media` mitgeben.
