# Web — Entwürfe und gebaute Seiten

Arbeitsstand der Abteilung 06 Web & Shop. Regelwerk: `WEBSITE-PROMPT-ultra.md` und
`.claude/skills/website-highend/`.

| Datei | Was es ist |
|---|---|
| `entwurfsblaetter.html` | Vier Designrichtungen mit Kennwerten, Vergleich und Empfehlung: Werkbank, Prüfstand, Nachtwerkstatt, Werkverzeichnis |
| `startseite-nachtwerkstatt.html` | Die gewählte Richtung 03, ausgebaut zur Startseite |

Beide Dateien laufen ohne Server: im Browser öffnen genügt. Schriften kommen von Google Fonts,
alles andere steckt in der Datei.

## Stand der gewählten Richtung 03 Nachtwerkstatt

Gebaut: Kopfleiste, Kopfbereich mit Messing-Glanzlauf, Materialansicht als WebGL-Shader mit
Abschaltmatrix und Standbild-Ersatz, Prüfbericht, Kollektion, Materialkunde mit Ausschlussliste,
Größenfinder, Leistungen, Fußzeile mit Pflichtangaben.

Noch offen:
1. Echte Fotos. Jede Bildfläche trägt ihre Aufnahmeanweisung als Beschriftung.
2. Echte Prüfdaten statt der Platzhalter in der Tabelle und den Kennzahlen.
3. Lederscan als Textur für den Shader. Bis dahin erzeugt der Shader die Narbenstruktur selbst.
4. Designsystem als eigene `tokens.css` herauslösen, sobald die zweite Seite entsteht.
5. Produktseite, Katalog, Warenkorb, Kasse. Danach Anbindung an Shopify Hydrogen.
6. Rechtsseiten mit echten Inhalten: Impressum, Datenschutz, AGB, Widerruf.
7. Abnahmetor aus `references/qualitaetstor.md` durchlaufen und Messwerte beilegen.

Namen, Prüftage, Befunde und Versandangaben sind bis dahin Platzhalter und stehen so auch auf
der Seite.
