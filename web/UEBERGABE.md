# Wie du den Shop änderst

Für Björn. Kein Code nötig, außer an einer Stelle — die ist markiert.

Solange kein Shopsystem steht, sind das alles Dateien im Ordner `web/`. Sobald Shopify oder
Medusa läuft, wandern Preis, Bild und Bestand dorthin und du klickst statt zu tippen. Was
gleich bleibt: Texte, Reihenfolge, Struktur.

---

## Preis ändern

Ein Preis steht an drei Stellen, und alle drei müssen gleich sein.

1. `web/vorlagen/seiten_bauen.py` — such den Artikel, ändere `"preis"` **und** `"preis_zahl"`.
   `"preis": "129,00"` ist, was der Kunde sieht. `"preis_zahl": "129.00"` ist, was Google liest
   — mit Punkt, ohne Eurozeichen.
2. `web/katalog.html` — im Kästchen des Stücks die Zeile `<span class="karte-preis tab">`.
3. `web/startseite-nachtwerkstatt.html` — falls das Stück auch dort steht.

Danach **einmal** ausführen, damit die Produktseiten neu entstehen:

```
python3 web/vorlagen/seiten_bauen.py
```

Bei Hamburg No. 1 geht es anders: die Seite ist von Hand gepflegt, dort änderst du den Preis
direkt in `web/produkt-hamburg-no-1.html`.

---

## Text ändern

- **Auf einer Produktseite** (No. 2, 3, 4): in `seiten_bauen.py` beim Artikel. `"einsatz"` ist
  der Satz unter der Überschrift, `"fragen"` sind die aufklappbaren Fragen, `"material"` die
  Liste. Danach den Befehl oben ausführen.
- **Bei Hamburg No. 1**: direkt in der Datei.
- **Auf Katalog, Warenkorb, Kasse, Rechtsseiten**: direkt in der jeweiligen Datei.

Fehlt nach dem Ausführen etwas, bricht der Befehl mit einer Meldung ab und schreibt nichts.
Eine halb gefüllte Seite kommt nicht durch.

---

## Bild tauschen

Die dunklen Flächen sind keine Bilder, sondern **Aufnahmeanweisungen**. In jeder steht, was
fotografiert werden soll. Sobald ein Foto da ist:

1. Foto nach `web/bilder/` legen, Name wie die Nummer: `foto-01.jpg`.
2. In der Datei die Zeile mit `<div class="bildplatz" …>` durch ein Bild ersetzen:
   ```
   <img src="bilder/foto-01.jpg" alt="Halsband Hamburg No. 1 auf roher Eiche, Schnalle vorn">
   ```
3. Der `alt`-Text ist keine Zierde. Er wird vorgelesen und von Suchmaschinen gelesen.
   Beschreib, was zu sehen ist — nicht „Produktfoto".

**Produktfotos sind echte Fotos, ausnahmslos.** Der Praxistest an echten Hunden ist das
Verkaufsargument. Ein generiertes Produktfoto zerstört genau dieses Argument und wäre als
Werbung angreifbar. KI darf danach: Hintergrund säubern, Licht angleichen, Bildrand erweitern.

---

## Neues Stück anlegen

1. In `web/vorlagen/seiten_bauen.py` einen bestehenden Eintrag in `STUECKE` kopieren und
   ausfüllen. Die Felder heißen, wie sie heißen — `name`, `sku`, `preis`, `masse`, `fragen`.
2. Bei `PRUEFZAHLEN` eine Zeile für die neue Artikelnummer ergänzen.
3. `python3 web/vorlagen/seiten_bauen.py` ausführen.
4. In `web/katalog.html` ein Kästchen kopieren, Text ändern, auf die neue Seite verweisen.

Die Nummer läuft durch die ganze Kollektion, nicht je Warengruppe. Das nächste Stück ist
Hamburg No. 8, auch wenn es ein Halsband ist.

---

## Bestand und „ausverkauft"

Im Katalog bekommt das Kästchen `data-stand="ausverkauft"` — dann wird es ruhiger und der
Knopf sagt, was los ist. Eine Größe schaltest du auf der Produktseite ab, indem du beim
Größenknopf `disabled` ergänzt.

**Nie** „nur noch 2 auf Lager" schreiben, wenn es nicht stimmt. Das ist irreführende Werbung
und abmahnfähig.

---

## Bestellung bearbeiten

Gibt es noch nicht — dafür fehlt das Shopsystem. Wenn Shopify steht, läuft das dort:
Bestellung öffnen, Versandschein drucken, Sendungsnummer eintragen, Mail geht automatisch raus.

---

## Was du nicht ohne Rückfrage ändern solltest

| Stelle | Warum |
|---|---|
| Die Zeile „Entworfen, geprüft und gehandelt in Hamburg. Gefertigt in Deutschland." | Sie muss so sichtbar sein wie der Name. Fällt sie weg oder wandert sie ins Kleingedruckte, wird die Herkunftsangabe angreifbar |
| „Gefertigt in Deutschland" | Gilt nur, solange hier zugeschnitten, gelocht und montiert wird. Kommt ein Modell fertig aus China, ändert sich der Satz **für dieses Modell** |
| Der Knopf „Zahlungspflichtig bestellen" | Die Beschriftung ist vorgeschrieben. Nicht „Jetzt kaufen", nicht „Absenden" |
| „Alle ablehnen" im Zustimmungsbanner | Muss genauso leicht sein wie Annehmen: gleiche Ebene, gleiche Größe |
| „inklusive 19 % Umsatzsteuer" | Stimmt nur ohne Kleinunternehmerregelung. Mit Kleinunternehmerregelung muss der Satz überall weg |
| Die Rechtsseiten | Erst füllen, dann anwaltlich prüfen lassen. Muster aus dem Netz sind der häufigste Grund für Abmahnungen |

---

## Wenn etwas kaputt aussieht

Alle Seiten laufen ohne Server — Datei im Browser öffnen genügt. Sieht etwas verrutscht aus:

1. Hast du `python3 web/vorlagen/seiten_bauen.py` nach einer Änderung ausgeführt?
2. Hast du versehentlich eine erzeugte Produktseite direkt geändert? Die wird überschrieben.
   Änderungen gehören in `seiten_bauen.py` oder `vorlagen/produkt.html`.
3. Fehlt ein Anführungszeichen oder eine spitze Klammer? Das ist der häufigste Fehler.

Im Zweifel: `git checkout web/` macht alle Änderungen seit dem letzten Stand rückgängig.
