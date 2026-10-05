---
name: bellowerk-zeichnung
description: Bemaßte Werkstattzeichnungen für Bellowerk-Produkte als SVG anlegen, ändern und als PNG rendern. Nutze das immer, wenn an einem Halsband, einer Leine, einem Patch oder einem Beschlagteil ein Maß, eine Position oder eine Größe geändert wird, wenn ein neues Modell gezeichnet werden soll, oder wenn jemand nach der Zeichnung für ein Modell fragt — auch dann, wenn nur beiläufig "mach das 30 % breiter" oder "der Ring sitzt woanders" gesagt wird.
---

# Werkstattzeichnungen für Bellowerk

Die Zeichnung ist das, wonach eine fremde Fabrik baut. Sie hängt an jeder Anfrage, und wenn ein Maß
darauf falsch ist, kommt das Goldmuster falsch zurück. Deshalb: Quelle ist immer das Tech Pack unter
`sourcing/bellowerk/specs/`, nie das Gedächtnis.

## Reihenfolge

1. Tech Pack lesen. Ändert sich ein Maß, ändert es sich **zuerst dort** — die Zeichnung bildet ab,
   was spezifiziert ist, nicht umgekehrt.
2. SVG in `sourcing/bellowerk/zeichnungen/<CODE>-<name>.svg` anlegen oder ändern.
3. Rendern: `CHROMIUM_PATH=/opt/pw-browsers/chromium python3 sourcing/bellowerk/zeichnungen/render.py`
4. Das gerenderte PNG **ansehen**. Textkollisionen und aus dem Bild laufende Bemaßungen sieht man
   nur im Bild, nicht im Quelltext. Einmal schauen, einmal aufräumen, fertig.
5. Tabelle in `sourcing/bellowerk/zeichnungen/README.md` nachziehen.

## Modellcodes

`HB-01` Hamburg Nr. 1 (Mittelverbreiterung) · `HB-02` Flechthalsband · `HB-04` Hamburg Nr. 4 (glatt) ·
`LE-01` Führleine · `PATCH-01` Lederpatch · `BES-01` Beschläge · `VERP-01` Verpackung.
Der Code steht im Dateinamen, im Titel der Zeichnung und im Tech Pack gleich — daran hängt alles.

## Konventionen

- **Maßstab 1:2**, also 1 mm = 2 px. Steht im Titel. Bei kleinen Teilen (Patch) 4:1.
- Weißer Grund, `Arial, Helvetica, sans-serif`, `fill="none" stroke="#000"`, Grundstärke 2.
- Titelzeile 26 px fett: `CODE "Name" — was — Größe M — scale 1:2 — Bellowerk Manufaktur, vX.Y, TT Mon JJJJ`.
- Zweite Zeile 16 px: Material und die harten Ausschlüsse — `NO stitching · NO rivets · Chicago screws only`.
  Diese Zeile ist wichtiger als sie aussieht: sie steht auf jedem Ausdruck, der in der Fabrik liegt.
- Kontur 2.5, Bemaßung 1.5 mit Anschlagstrichen, Maßzahlen 13–14 px.
- Alle Maße in mm, ohne Einheit an der Zahl, Einheit einmal im Text.
- Unten zwei Blöcke: **Schnitt** (zeigt den Lagenaufbau) und **Größentabelle** mit Toleranzen.
- Ist ein Wert nicht am Original gemessen, schreib es hin: *"starting values — confirm on Björn's
  reference piece"*. Erfundene Präzision ist schlimmer als eine offene Frage.

## Was erfahrungsgemäß schiefgeht

- **Textkollisionen** zwischen Hinweisblöcken und der Größentabelle. Hinweise unter den Block setzen,
  nicht daneben.
- **Bemaßung im Bauteil**: Die Kontur ist ungefüllt, Maßlinien dürfen innen liegen — das ist oft
  klarer als außen und spart Platz.
- **Lochreihe im Bogen**: Bei verbreiterten Modellen prüfen, dass die Löcher im schmalen Teil liegen.
  Aufteilung der Länge einmal durchrechnen, bevor gezeichnet wird.
- Ändert sich ein Patchmaß, ändert sich auch der **Lochabstand** (Lochmitte 7 mm vom Ende).
