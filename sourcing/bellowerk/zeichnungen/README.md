# Zeichnungen

Bemaßte Strichzeichnungen je Modell als SVG (Quelle) und PNG (zum Anhängen in Alibaba-Chat,
WeChat, E-Mail). Jede Anfrage an einen Lieferanten bekommt die passende PNG plus ein Foto aus
`../bilder/`.

| Datei | Modell | Stand |
|---|---|---|
| `HB-01-halsband.svg/.png` | Halsband Fettleder, Größe M, Schnallenfalte, Lochbild, Patch-Position | v1.0 |
| `LE-01-fuehrleine.svg/.png` | Führleine 2,60 m (Blatt 1/2): Ringe 80/168/245 cm, Ø 30/30/40 mm, alle 5 Anbindungen geflochten | v2.0 |
| `LE-01-detail-flechtung.svg/.png` | Führleine (Blatt 2/2): Flechtanbindung **Maßstab 1:1**, A4 quer, mit Kontrollbalken 100 mm | v2.0 |
| `PATCH-01-lederpatch.svg/.png` | Lederpatch graviert PA-M 85×18 und PA-S 65×14, Bohrbild, Schnitt | v1.1 |
| `HS-01-handschlaufe.svg/.png` | Handschlaufe 50 cm | v1.0 |
| `HB-02-geflochten.svg/.png` | Flechthalsband: flache Enden, Mystery Braid mit O-Ring, Patch | v1.0 |

Startwerte (Größentabellen, Lochabstände) sind aus der Kernserie abgeleitet und von Björn am
Referenzstück zu bestätigen. Änderungen: SVG editieren, dann PNG neu rendern:

```bash
pip install playwright
# in der Claude-Cloud-Umgebung (vorinstalliertes Chromium):
CHROMIUM_PATH=/opt/pw-browsers/chromium python3 sourcing/bellowerk/zeichnungen/render.py
# lokal: playwright install chromium && python3 sourcing/bellowerk/zeichnungen/render.py
```
