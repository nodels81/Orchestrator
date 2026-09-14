---
name: ui-ux-pro-max
description: Entwirft und prüft Oberflächen für Bellowerk — Status-Dashboard, Produkt- und Shopseiten, Landingpages, Artifacts, E-Mail- und Angebotslayouts. Nutzen, wenn eine Seite, ein Bildschirm, ein Formular oder ein Dashboard entsteht oder überarbeitet wird, wenn nach Layout, Typografie, Farben, Kontrast, Barrierefreiheit oder Mobilansicht gefragt wird, und bevor irgendeine Oberfläche gebaut wird.
---

# UI/UX Pro Max

Eine Oberfläche ist gelungen, wenn der Mensch davor sein Ziel erreicht, ohne sie zu bemerken.
Alles andere — Farbe, Schatten, Animation — ist Mittel, nie Zweck.

Du baust nicht "schön". Du baust **entscheidbar**: Wer hier ankommt, sieht in drei Sekunden,
was das ist, was er hier tun kann und was der nächste Schritt ist.

## Reihenfolge (nicht abkürzen)

1. **Ein Satz.** "Wer kommt hierher, um was zu tun, auf welchem Gerät?" Steht der Satz nicht,
   wird nicht gebaut. Beispiel: *Björn, morgens am Telefon, will in 5 Sekunden sehen, ob der
   Nachtlauf durch ist und was offen ist.*
2. **Eine Aufgabe pro Bildschirm.** Alles, was diese Aufgabe nicht voranbringt, fliegt raus oder
   wandert eine Ebene tiefer. Zwei gleichrangige Hauptaktionen heißt: keine.
3. **Inhalt ordnen, bevor gestaltet wird.** Schreibe die Elemente als nummerierte Liste in der
   Reihenfolge, in der sie gelesen werden sollen. Diese Reihenfolge ist danach die DOM-Reihenfolge —
   Tastatur und Screenreader laufen genau so.
4. **Struktur bauen.** Ein Raster, ein Abstandsmaß (4 px), eine Schriftskala. Erst graue Kästen,
   dann echter Inhalt, dann Farbe.
5. **Zustände bauen** — nicht nur den guten Fall (siehe unten).
6. **Prüfen** gegen `references/pruefliste.md`. Ungeprüft = nicht fertig.

## Harte Maße (keine Geschmacksfrage)

| Sache | Wert | Warum |
|---|---|---|
| Kontrast Fließtext | ≥ 4,5:1 | WCAG AA, lesbar in der Sonne |
| Kontrast große Schrift (≥ 24 px / 19 px fett), Icons, Rahmen | ≥ 3:1 | WCAG AA |
| Tippziel | ≥ 44 × 44 px, ≥ 8 px Abstand | Daumen, nicht Mauszeiger |
| Zeilenlänge | 60–75 Zeichen (`max-width: 68ch`) | darüber verliert das Auge die Zeile |
| Zeilenhöhe | 1,5 Fließtext, 1,15–1,25 Überschrift | |
| Schriftgrad mobil | ≥ 16 px Eingabefelder | darunter zoomt iOS-Safari beim Fokus |
| Seitenrand | ≥ 16 px an jeder Kante, auch bei 360 px Breite | |
| Animation | 150–250 ms, `ease-out`; `prefers-reduced-motion` respektieren | |
| Ladezustand | ab 400 ms sichtbar, mit Platzhalter in Zielgröße | verhindert Sprünge |
| Fokusring | immer sichtbar, ≥ 2 px, ≥ 3:1 zum Hintergrund | `outline: none` ohne Ersatz ist ein Fehler |

Abstände und Grade aus einer Skala, nie freihändig:
`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64` px — Schrift `12 · 14 · 16 · 20 · 24 · 32 · 48`.

## Die fünf Zustände — jeder Bildschirm hat sie

1. **Leer** (noch nichts da): erklärt in einem Satz, was hier erscheinen wird, plus die eine Aktion,
   die es füllt. Nie ein leerer Kasten.
2. **Lädt**: Platzhalter in der Größe des späteren Inhalts.
3. **Fehler**: was passiert ist, was es für den Nutzer bedeutet, was er jetzt tun kann. Keine
   Fehlernummer ohne Satz daneben.
4. **Zu viel**: 500 Zeilen statt 5 — Paginierung, Filter, Deckel.
5. **Zu lang**: der Firmenname mit 60 Zeichen, die Adresse ohne Leerzeichen. Umbruch oder Kürzung
   mit vollem Text im `title`.

Dazu jedes Mal: Tastaturbedienung (Tab-Reihenfolge, Esc schließt, Enter bestätigt), Dunkelmodus,
400 px Breite.

## Text ist Oberfläche

- Knöpfe tragen das Verb der Handlung: **Muster bestellen**, nicht "OK". **Verwerfen**, nicht "Nein".
- Kein "Ups!", kein Ausrufezeichen, keine Entschuldigung. Sagen, was ist.
- Zahlen im deutschen Format: `1.250,00 EUR`, `14.09.2026`, `25 mm`.
- Fachwörter des Betriebs bleiben stehen (MOQ, EXW, Goldmuster) — einmal erklärt, dann benutzt.
- Labels über dem Feld, nicht als Platzhalter im Feld: Platzhalter verschwinden beim Tippen.

## Bellowerk-Oberflächen

Marke: Schrift **Lora** (Serife, mit Fallback `Georgia, serif`), Farben aus dem Markenbrief.
Nachgerechnete Kontraste (Weiß `#FFFFFF` bzw. Papier `#FAF8F5`):

| Farbe | Hex | auf Weiß | erlaubt für |
|---|---|---|---|
| Waldgrün | `#23352A` | 13,0:1 | alles, Fließtext, dunkler Grund (Papier darauf 12,3:1) |
| Olivgrün | `#566347` | 6,4:1 | Fließtext, Knöpfe mit weißer Schrift |
| Cognac | `#9A6238` | 5,0:1 | Fließtext, Akzent |
| **Messing** | `#B08D57` | **3,1:1** (auf Papier nur 2,9:1) | **nur Flächen und Rahmen auf Weiß — nie Fließtext, auf Papier auch keine große Schrift** |

Messing auf Waldgrün ergibt 4,2:1 — als Akzentfarbe auf dunklem Grund tragfähig, für kleinen
Fließtext auch dort nicht. Bildsprache laut Markenbrief: echte Betriebsfotos, kein Studio-Look —
also Fotos groß und ungefiltert, keine Schlagschatten, keine Farbverläufe über Leder.

**Status-Dashboard** (`daten/dashboard.html` auf dem Server): eine Seite, keine Navigation.
Oben in einer Zeile: läuft / fertig / gescheitert und der Zeitpunkt des letzten Laufs. Darunter
die offenen Aufträge mit Fälligkeit, überfällige zuerst und farblich markiert — Farbe **und**
Wort, nie Farbe allein. Muss auf dem Telefon in einem Blick lesbar sein, ohne Zoom und ohne
Querscrollen.

## Prüfen statt hoffen

- `python3 .claude/skills/ui-ux-pro-max/references/kontrast.py "#B08D57" "#FFFFFF"` rechnet jeden
  Farbwert nach. Jede neue Farbkombination wird gerechnet, nicht geschätzt.
- Volle Liste vor dem Abliefern: `references/pruefliste.md`.
- Ist die Oberfläche im Browser erreichbar, sieh sie dir an (Skill `run`, Playwright/Chromium ist
  installiert): 1× bei 1280 px, 1× bei 390 px, hell und dunkel.

## Grenzen

- Keine erfundene Nutzerforschung. Was niemand weiß, wird als Annahme markiert.
- Keine Bibliothek ohne Not: erst HTML und CSS, ein Framework nur, wenn der Zustand es erzwingt.
- Kein Redesign nebenbei. Was nicht zur Aufgabe gehört, wird genannt, nicht umgebaut.
