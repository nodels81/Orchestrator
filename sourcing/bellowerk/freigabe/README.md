# Freigabe-Mappe

Eine Seite, auf der Björn die Kernserie abnimmt, bevor eine Anfrage nach China geht.
Pro Modell ein Blatt: Maßzeichnung aus `../zeichnungen`, Fotos vom Original aus `../bilder`,
die harten Werte aus dem Tech Pack in `../specs` und die Punkte, über die nur er entscheiden kann.

`index.html` ist die Quelle. Die Seite trägt ihren Stand selbst: jede Freigabe, jede beantwortete
Frage und jede Anmerkung wird als neue Version der Seite gespeichert (Artifact-Capability
`artifact`), sodass jeder, der den Link öffnet, denselben Stand sieht.

## Bauen und veröffentlichen

```bash
pip install Pillow
python3 sourcing/bellowerk/freigabe/bauen.py   # verkleinerte Bilder nach freigabe/media
```

Danach `index.html` zusammen mit dem Ordner `media/` als Artifact veröffentlichen.
`media/` ist bewusst nicht im Repo — die Dateien sind abgeleitet, die Originale liegen
in `../bilder` und `../zeichnungen`.

## Wenn sich etwas ändert

Maße, Mengen und Farben stehen in den Tech Packs unter `../specs` — dort ändern, dann in
`index.html` im Block `bw-data` nachziehen. Die Mappe zeigt den Stand der Tech Packs,
sie ersetzt sie nicht.

## Aufbau von index.html

| Block | Inhalt |
|---|---|
| `<style id="bw-css">` | Palette (Papier, Tinte, Messing, Oliv, Rost), beide Themes |
| `<script id="bw-data">` | Modelle, Fakten, Fotos, Entscheidungsfragen — hier wird redigiert |
| `<script id="bw-state">` | Björns Antworten; wird beim Speichern überschrieben |
| `<script id="bw-js">` | rendert die Seite aus data + state und veröffentlicht neue Versionen |
