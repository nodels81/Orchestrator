# Zeichnungen

Bemaßte Strichzeichnungen je Modell als SVG (Quelle) und PNG (zum Anhängen in Alibaba-Chat,
WeChat, E-Mail). Jede Anfrage an einen Lieferanten bekommt die passende PNG plus ein Foto aus
`../bilder/`.

| Datei | Modell | Stand |
|---|---|---|
| `HB-01-halsband.svg/.png` | Halsband Fettleder, Größe M, Schnallenfalte, Lochbild, Patch-Position | v1.0 |
| `LE-01-fuehrleine.svg/.png` | Führleine 2,60 m (Blatt 1/3): Ringe 80/168/245 cm, Ø 30/30/40 mm, Bleed-Knot-Anbindung | v3.0 |
| `LE-01-detail-flechtung.svg/.png` | Führleine (Blatt 2/3): **1:1-Prüfblatt** zum Auflegen der fertigen Leine, A4 quer, Kontrollbalken 100 mm | v3.0 |
| `LE-01-flechtung-schritte.svg/.png` | Führleine (Blatt 3/3): **Bleed Knot Schritt für Schritt**, farbig, A3 quer. Erzeugt von `mkbraid.py` | v3.0 |
| `PATCH-01-lederpatch.svg/.png` | Lederpatch graviert PA-L 110×18 (Leine), PA-M 85×18, PA-S 65×14, Bohrbild, Schnitt | v1.2 |
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

## Knotentechnik LE-01

Die Anbindung an der Führleine ist **kein Flechtzopf**, sondern der **Bleed Knot** (auch Blood Knot):
ein Längsschlitz, durch den der volle Riemen durch sich selbst gezogen wird. Der Riemen wird nie in
Stränge geschlitzt und nie durchtrennt. Aneinandergereiht ergibt der Knoten das V-Muster, das wie eine
Flechtung aussieht. Belegt am Goldmuster (`bilder/LE-01-goldmuster-*.jpg`, sichtbare Fleischseite in
jedem V) und durch die Technik, die als "bleed knot leather dog leash" verbreitet ist.
