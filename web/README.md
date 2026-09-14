# Web — Entwürfe und gebaute Seiten

Arbeitsstand der Abteilung 06 Web & Shop. Regelwerk: `WEBSITE-PROMPT-ultra.md` und
`.claude/skills/website-highend/`.

Alle Seiten laufen ohne Server: im Browser öffnen genügt. Schriften kommen von Google Fonts,
alles andere steckt in `tokens.css` und den Seiten selbst.

## Was da ist

| Datei | Was es ist |
|---|---|
| `tokens.css` | **Das Designsystem.** Farben, Raum, Typoskala, Bewegung, Oberflächen und alle Bauteile mit allen Zuständen. Seit dem 12.09. die Quelle — nicht mehr die Startseite. |
| `entwurfsblaetter.html` | Vier Designrichtungen mit Kennwerten, Vergleich und Empfehlung |
| `startseite-nachtwerkstatt.html` | Die gewählte Richtung 03, ausgebaut zur Startseite |
| `katalog.html` | Das Werkverzeichnis: sieben Stücke, Filter, Zubehör, Leerzustand |
| `produkt-hamburg-no-1.html` | Produktseite HB-01. Von Hand gebaut, Vorbild für die anderen |
| `produkt-hamburg-no-2.html` | Produktseite LE-01 · erzeugt |
| `produkt-hamburg-no-3.html` | Produktseite HS-01 · erzeugt |
| `produkt-hamburg-no-4.html` | Produktseite HB-02 · erzeugt |
| `warenkorb.html` | Warenkorb, gefüllt und leer, mit Versandschwelle |
| `kasse.html` | Kasse: Gastbestellung, Zahlarten oben, Bestellübersicht, Zustimmungsbanner |
| `recht/` | Impressum, Datenschutz, AGB, Widerruf, Versand — als Gerüst |
| `vorlagen/produkt.html` | Die Vorlage, aus der die Produktseiten entstehen |
| `vorlagen/seiten_bauen.py` | Der Generator. Inhalte je Stück stehen oben in `STUECKE` |

## Produktseiten ändern

Nicht die erzeugten Dateien anfassen — sie werden überschrieben. Stattdessen:

```bash
# Inhalt eines Stücks ändern:  web/vorlagen/seiten_bauen.py, Abschnitt STUECKE
# Aufbau aller Seiten ändern:  web/vorlagen/produkt.html
python3 web/vorlagen/seiten_bauen.py
```

Der Generator bricht ab, wenn eine Marke `§§…§§` unersetzt bleibt. Eine halb gefüllte Seite
kommt damit nicht durch.

`produkt-hamburg-no-1.html` ist bewusst von Hand gepflegt und nicht erzeugt: an ihr wird
entworfen, danach wandert das Ergebnis in die Vorlage.

## Warum die Herkunftsangabe in der Vorlage steht

`konzepte/kollektion-01-hamburg.md` verlangt sie im selben Block wie Preis und Größe, nicht
weggeklappt und nicht nur in der Fußzeile. In der Vorlage kann sie nicht vergessen werden —
das ist der Grund, warum es die Vorlage gibt.

## Prüfen

```bash
python3 - <<'PY'
import re, pathlib, json, html.parser
# HTML parsen, JSON-LD prüfen, jeden internen Verweis und Anker auflösen
PY
```

Der vollständige Prüflauf steht im Sitzungsprotokoll. Beim letzten Durchgang: 14 Seiten,
194 interne Verweise, keine toten Verweise, keine kaputten Anker, keine unersetzten Marken,
JSON-LD auf allen Produktseiten gültig.

## Was noch fehlt

1. **Echte Fotos.** Jede Bildfläche trägt ihre Aufnahmeanweisung als Beschriftung. Ohne die
   elf Aufnahmen aus `web/aufnahmen/` kein Shopstart.
2. **Echte Prüfdaten.** Hunde, Tage, Befunde sind auf allen vier Produktseiten Platzhalter und
   als solche markiert. Entweder echte Zahlen oder die Sektion fällt weg.
3. **Angaben für die Rechtsseiten.** Anbieter, Anschrift, USt-IdNr., zweiter Kontaktweg.
   Alles orange unterstrichen. Danach anwaltlich prüfen lassen.
4. **Zwei Entscheidungen, die durch den ganzen Shop laufen:**
   Kleinunternehmerregelung ja oder nein (ändert jede Preisangabe) und wer die Rücksendekosten
   trägt (muss in Widerrufsbelehrung und Versandseite gleich stehen).
5. **Shopsystem.** Shopify mit Hydrogen oder Next.js mit Medusa. Bis dahin sind diese Seiten
   statisch — sie portieren in beide Richtungen, weil das Designsystem in `tokens.css` steht
   und die Produktseiten schon aus Daten erzeugt werden.
6. **Lederscan** als Textur für den Shader auf der Startseite.
7. **Seiten für Hamburg No. 5, 6 und 7**, sobald die Stücke gebaut sind. Im Katalog stehen sie
   als nicht bestellbar, mit Grund.

## Bilder

Produktbilder sind echte Fotos, ausnahmslos. Der Praxistest an echten Hunden ist das
Verkaufsargument — ein generiertes Produktfoto zerstört genau dieses Argument und ist als
Werbung angreifbar. KI kommt erst danach: Hintergrund säubern, Licht angleichen, Bildrand
erweitern, Texturen. Siehe `web/aufnahmen/`.
