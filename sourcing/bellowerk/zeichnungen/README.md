# Zeichnungen

Bemaßte Strichzeichnungen je Modell als SVG (Quelle) und PNG (zum Anhängen in Alibaba-Chat,
WeChat, E-Mail). Jede Anfrage an einen Lieferanten bekommt die passende PNG plus ein Foto aus
`../bilder/`.

| Datei | Modell | Stand |
|---|---|---|
| `HB-01-halsband.svg/.png` | Halsband Fettleder, Größe M (30 mm), Schnallenfalte, Lochbild, Patch-Position | v1.1 |
| `LE-01-fuehrleine.svg/.png` | Führleine 3,00 m, Ringe 45/140/245 cm, Mystery-Braid-Anbindung, sechs Führlängen | v1.1 |
| `PATCH-01-lederpatch.svg/.png` | Lederpatch graviert PA-M 85×20 und PA-S 65×14, Bohrbild, Schnitt | v1.2 |
| `HS-01-handschlaufe.svg/.png` | Handschlaufe 50 cm | v1.0 |
| `HB-02-geflochten.svg/.png` | Flechthalsband Größe M (30 mm): flache Enden, Mystery Braid mit O-Ring, Patch | v1.1 |

Startwerte (Größentabellen, Lochabstände) sind aus der Kernserie abgeleitet und von Björn am
Referenzstück zu bestätigen. Änderungen: SVG editieren, dann PNG neu rendern:

```bash
pip install playwright
# in der Claude-Cloud-Umgebung (vorinstalliertes Chromium):
CHROMIUM_PATH=/opt/pw-browsers/chromium python3 sourcing/bellowerk/zeichnungen/render.py
# lokal: playwright install chromium && python3 sourcing/bellowerk/zeichnungen/render.py
```
