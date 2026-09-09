# Zeichnungen

Bemaßte Strichzeichnungen je Modell als SVG (Quelle) und PNG (zum Anhängen in Alibaba-Chat,
WeChat, E-Mail). Jede Anfrage an einen Lieferanten bekommt die passende PNG plus ein Foto aus
`../bilder/`.

| Datei | Modell | Stand |
|---|---|---|
| `HB-01-halsband.svg/.png` | Halsband Fettleder, Größe M, Schnallenfalte, Lochbild, Namensschild | v1.0 |
| `LE-01-fuehrleine.svg/.png` | Führleine 3,00 m, Ringe 45/140/245 cm, Ringfalte, sechs Führlängen | v1.0 |
| `PATCH-01-namensschild.svg/.png` | Messing-Namensschild PL-S 40×14 und PL-M 50×18, Bohrbild | v1.0 |
| `HS-01-handschlaufe.svg/.png` | Handschlaufe 50 cm | v1.0 |
| `HB-02-geflochten.svg/.png` | Halsband geflochten, Übergang Flechtung/flaches Ende | v0.9 Entwurf |

Startwerte (Größentabellen, Lochabstände) sind aus der Kernserie abgeleitet und von Björn am
Referenzstück zu bestätigen. Änderungen: SVG editieren, dann PNG neu rendern:

```bash
pip install playwright
# in der Claude-Cloud-Umgebung (vorinstalliertes Chromium):
CHROMIUM_PATH=/opt/pw-browsers/chromium python3 sourcing/bellowerk/zeichnungen/render.py
# lokal: playwright install chromium && python3 sourcing/bellowerk/zeichnungen/render.py
```
