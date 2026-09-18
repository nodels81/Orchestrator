# Zeichnungen

Bemaßte Strichzeichnungen je Modell als SVG (Quelle) und PNG (zum Anhängen in Alibaba-Chat,
WeChat, E-Mail). Jede Anfrage an einen Lieferanten bekommt die passende PNG plus ein Foto aus
`../bilder/`.

| Datei | Modell | Stand |
|---|---|---|
| `HB-01-halsband.svg/.png` | Halsband Fettleder, Größe M — Draufsicht + Schnitt A–A, Stückliste | v1.1 |
| `LE-01-fuehrleine.svg/.png` | Führleine 3,00 m, Ringe 45/140/245 cm, Mystery-Braid-Anbindung — Draufsicht + Schnitt C–C, Stückliste | v1.2 |
| `PATCH-01-lederpatch.svg/.png` | Lederpatch graviert PA-M 85×18 und PA-S 65×14, Bohrbild, Schnitt | v1.1 |
| `HS-01-handschlaufe.svg/.png` | Handschlaufe 50 cm — Draufsicht + Schnitt D–D, Stückliste | v1.1 |
| `HB-02-geflochten.svg/.png` | Flechthalsband: flache Enden, Mystery Braid mit O-Ring — Draufsicht + Schnitt B–B, Stückliste | v1.1 |

Jede Zeichnung ist jetzt ein vollständiges **Fertigungsblatt** mit zwei Ansichten (Draufsicht +
Schnittansicht mit Lederdicke/-breite) und einer **Stückliste / Bill of Materials** unten (Pos,
Bezeichnung, Menge, Material/Spezifikation, Referenz). Positionen mit "Foto bestätigt" sind gegen ein
scharfes Referenzfoto aus `../bilder/hardware-*.jpg` abgeglichen — für diese Teile gilt das Foto,
nicht die schematische Linie, als verbindliche Formvorgabe.

Startwerte (Größentabellen, Lochabstände) sind aus der Kernserie abgeleitet und von Björn am
Referenzstück zu bestätigen. Änderungen: SVG editieren, dann PNG neu rendern:

```bash
pip install playwright
# in der Claude-Cloud-Umgebung (vorinstalliertes Chromium):
CHROMIUM_PATH=/opt/pw-browsers/chromium python3 sourcing/bellowerk/zeichnungen/render.py
# lokal: playwright install chromium && python3 sourcing/bellowerk/zeichnungen/render.py
```
