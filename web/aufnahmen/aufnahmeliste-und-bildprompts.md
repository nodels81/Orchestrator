# Aufnahmeliste und Bildprompts — Richtung 03 Nachtwerkstatt

Gehört zu `web/startseite-nachtwerkstatt.html`. Jede Bildfläche auf der Seite trägt ihre
Nummer als Beschriftung. Ist ein Foto gemacht, ersetzt es die Fläche.

## Grundregel

Produktfotos sind echte Fotos. Nano Banana kommt erst danach: Hintergrund säubern, Licht
angleichen, Bildrand für andere Seitenverhältnisse erweitern, Texturen und Hintergründe erzeugen.
Kein generiertes Produktfoto, kein generiertes Gesicht.

## Das Licht dieser Richtung

Alle Aufnahmen folgen einer Lichtsituation, sonst zerfällt die Seite: **hartes Seitenlicht von
links, dunkler Hintergrund, warme Farben.** Beste Zeit ist die Stunde vor Sonnenuntergang oder
ein Werkstattfenster ohne Vorhang. Kein Blitz, kein Deckenlicht, keine helle Wand dahinter.

---

## Aufnahmeliste

| Nr. | Motiv | Ausschnitt | Format | Verwendung |
|---|---|---|---|---|
| 01 | HB-01 liegend auf roher Eiche, Schnalle vorn | Makro 85 mm aus 40 cm | 5:4 | Kollektion, erste Karte |
| 02 | HB-02 Flechtung schräg von oben, Licht quer zur Flechtung | Makro, halbes Band im Bild | 5:4 | Kollektion |
| 03 | LE-01 an einem Haken hängend, Gegenlicht | Halbtotale, ganze Leine | 5:4 | Kollektion |
| 04 | HS-01 in der Hand, Daumen durch die Schlaufe | Makro, Hand angeschnitten | 5:4 | Kollektion |
| 05 | Halsband am arbeitenden Hund, Regen oder nasses Fell | Halbtotale, Hals scharf | 4:5 | Praxistest |
| 06 | Schnalle im Streiflicht, Messing matt angelaufen | Makro aus 25 cm | 16:9 | Materialkunde |
| 07 | Dasselbe Halsband neu | Aufsicht, gleiche Position wie 08 | 21:9 | Vergleich neu und getragen |
| 08 | Dasselbe Halsband nach einer Saison, ungeputzt | Aufsicht, gleiche Position wie 07 | 21:9 | Vergleich neu und getragen |
| 09 | Werkbank mit Werkzeug, kein Produkt im Fokus | Totale von oben | 16:9 | Werkstatt |
| 10 | Hände beim Kürzen oder Lochen | Makro, Gesicht nicht im Bild | 4:5 | Werkstatt |
| 11 | Kind mit Hund, Hand am Halsband | Halbtotale, Halsband scharf | 16:9 **und** 4:5 | Kopfbereich |

**Zu 07 und 08:** Stativposition, Abstand und Brennweite müssen identisch sein, sonst funktioniert
der Vergleichsschieber nicht. Am besten dieselbe Stelle auf dem Boden markieren.

**Zu 11:** Kind kniend oder sitzend neben dem Hund, eine Hand am Halsband oder an der Leine.
Der Hund schaut zur Kamera, das Kind zum Hund. Nicht beide in die Kamera. Hintergrund dunkel:
Waldrand, dunkle Hecke, Backsteinwand im Schatten. Zwei getrennte Aufnahmen für quer und hoch,
kein Beschnitt aus einem Bild. Nicht im Bild: Kunststoff, Gurtband, Klickverschlüsse,
fremde Marken, Spielzeug.

---

## Nachbearbeitung mit Nano Banana

Immer das **echte Foto** hochladen und nur die genannte Änderung verlangen. Gesicht, Hund und
Produkt werden nie neu erzeugt, sondern maskiert und ausgenommen.

### Hintergrund abdunkeln und auf die CI bringen

```
Bearbeite dieses Foto. Verändere Personen, Hund und Lederprodukt nicht, weder Form noch Farbe
noch Position. Dunkle nur den Hintergrund ab, bis er fast schwarz mit warmem Braunstich ist.
Verstärke das vorhandene Seitenlicht von links leicht, sodass die Kante des Leders und das
Messing ein schmales Glanzlicht bekommen. Warme, gedämpfte Farben, keine kühlen Blautöne.
Kein zusätzliches Licht von vorn. Kein Text im Bild. Kein neues Objekt.
```

### Bildrand erweitern für ein anderes Seitenverhältnis

```
Erweitere dieses Foto auf 16:9, ohne den vorhandenen Bildinhalt zu verändern oder zu skalieren.
Ergänze nur links und rechts denselben dunklen, unscharfen Hintergrund in gleicher Körnung und
gleicher Lichtrichtung. Keine neuen Objekte, keine Personen, keine Tiere, kein Text.
```

Dasselbe mit `4:5` für Instagram und `21:9` für den Vergleichsstreifen.

### Störer entfernen

```
Entferne aus diesem Foto nur den Gegenstand im Hintergrund rechts oben und ersetze ihn durch
die Fortsetzung des vorhandenen Hintergrunds. Verändere sonst nichts, insbesondere nicht das
Halsband, den Hund und die Person.
```

### Prüfung nach jeder Bearbeitung

1. Zählt die Zahl der Löcher noch? Sitzt die Schnalle wie im Original?
2. Ist die Flechtung noch dreisträngig und läuft in dieselbe Richtung?
3. Ist am Beschlag noch Messing zu sehen und kein silbriges Metall?
4. Hat sich das Gesicht verändert? Wenn ja, verwerfen und mit engerer Maske wiederholen.
5. Datei mit `-ki` am Ende benennen und in dieser Liste vermerken.

---

## Hintergründe und Texturen — hier ist Erzeugen unproblematisch

Diese Bilder zeigen kein Produkt und keine Person, sie sind Flächen.

### Dunkle Werkstattwand

```
Rohe Backsteinwand einer Werkstatt im Schatten, gleichmäßig dunkel, feine Struktur, sehr flacher
Kontrast, warm entsättigt, fast schwarz. Kachelbar. 16:9. Keine Objekte, keine Schrift,
keine harten Schatten.
```

### Lederstruktur für den Shader

```
Pflanzlich gegerbtes Fettleder, Narbenseite, cognacbraun, makroscharf und formatfüllend,
gleichmäßig ausgeleuchtet ohne Glanzlicht, sichtbare Poren und feine Falten, kachelbar,
quadratisch. Keine Naht, keine Niete, kein Beschlag, kein Text, kein Objekt.
```

Dieses Bild ersetzt später die vom Shader erzeugte Struktur in
`web/startseite-nachtwerkstatt.html`.

### Papier für Verpackung und Beileger

```
Ungebleichtes Packpapier, feine Faser im Streiflicht, warm beige, sehr flacher Kontrast,
kachelbar, quadratisch. Kein Aufdruck, kein Text, kein Knick, kein Objekt.
```

---

## Stand

| Nr. | Status |
|---|---|
| 01 bis 11 | offen, noch nicht fotografiert |
| Hintergründe und Texturen | offen |

Solange eine Nummer offen ist, steht auf der Seite die Bildfläche mit dieser Aufnahmeanweisung.
