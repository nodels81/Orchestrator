# Zeichnungen

Bemaßte Strichzeichnungen je Modell als SVG (Quelle) und PNG (zum Anhängen in Alibaba-Chat,
WeChat, E-Mail). Jede Anfrage an einen Lieferanten bekommt die passende PNG plus ein Foto aus
`../bilder/`.

| Datei | Modell | Stand |
|---|---|---|
| `HB-01-halsband.svg/.png` | Halsband Fettleder, Größe M, Schnallenfalte, Lochbild, Patch-Position | v1.0 |
| `LE-01-fuehrleine.svg/.png` | Führleine 3,00 m, Ringe 45/140/245 cm, Mystery-Braid-Anbindung, sechs Führlängen | v1.1 |
| `PATCH-01-lederpatch.svg/.png` | Lederpatch graviert PA-M 85×18 und PA-S 65×14, Bohrbild, Schnitt | v1.1 |
| `HS-01-handschlaufe.svg/.png` | Handschlaufe 50 cm | v1.0 |
| `HB-02-geflochten.svg/.png` | Flechthalsband: flache Enden, Mystery Braid mit O-Ring, Patch | v1.0 |
| `RC-01-regencape.svg/.png` | **Schnittmuster** Regencape Oilskin: Rücken, Vorderteil, Kapuze, Kragen, Tasche, Riegel, 3 Größen | v1.0 |
| `HM-01-hundemantel.svg/.png` | **Schnittmuster** Hundemantel gefüttert: Rückenteil, Kragen, Bauchgurt, Passe, 4 Größen | v1.0 |

Die beiden Schnittmuster gehören zur **Textillinie — noch nicht von Björn freigegeben**
(`specs/RC-01-…`, `specs/HM-01-…`, jeweils Abschnitt 8). Sie zeigen die Netto-Linien mit allen
Maßen; die 1:1-PDF- und DXF-Dateien liefert der Hersteller, siehe `../../vorlagen/05-schnittmuster-anfordern.md`.

Startwerte (Größentabellen, Lochabstände) sind aus der Kernserie abgeleitet und von Björn am
Referenzstück zu bestätigen. Änderungen: SVG editieren, dann PNG neu rendern:

```bash
pip install playwright
# in der Claude-Cloud-Umgebung (vorinstalliertes Chromium):
CHROMIUM_PATH=/opt/pw-browsers/chromium python3 sourcing/bellowerk/zeichnungen/render.py
# lokal: playwright install chromium && python3 sourcing/bellowerk/zeichnungen/render.py
```

Aus einer Zeichnung ein realistisches Konzeptbild machen (Website vor Musterlieferung, Pitch,
Lieferantenreferenz): `PRODUKTBILDER-KI.md`. Kein Ersatz für echte Fotos — die Abteilung Social
Media verwendet ausschließlich echte Aufnahmen.
