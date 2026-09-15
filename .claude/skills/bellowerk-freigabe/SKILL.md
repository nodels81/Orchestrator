---
name: bellowerk-freigabe
description: Die Bellowerk-Freigabe-Mappe pflegen — das Artifact, in dem Björn Modelle freigibt, Entscheidungsfragen beantwortet und Anmerkungen hinterlässt. Nutze das immer, bevor du an der Mappe etwas änderst oder sie neu veröffentlichst, und wenn ein Modell, eine Zeichnung, ein Foto oder eine beantwortete Frage dort nachgezogen werden soll. Es steht drin, wie man seine Häkchen nicht überschreibt und welcher Fehler die Seite schon einmal unbedienbar gemacht hat.
---

# Freigabe-Mappe pflegen

Quelle: `sourcing/bellowerk/freigabe/index.html`, veröffentlicht als Artifact. Die Seite ist ihr
eigenes Protokoll: Björns Freigaben, Antworten und Notizen liegen im Block `bw-state`, und wenn er
klickt, **veröffentlicht die Seite sich selbst neu**. Daraus folgt alles Weitere.

## Aufbau

| Block | Inhalt |
|---|---|
| `<style id="bw-css">` | Palette, beide Themes |
| `<script id="bw-data">` | Modelle, Fakten, Fotos, Fragen — hier wird redigiert |
| `<script id="bw-state">` | **Björns Antworten. Niemals von Hand neu erfinden.** |
| `<script id="bw-js">` | rendert aus data + state und baut beim Speichern das neue Dokument |

## Vor jeder Veröffentlichung: seinen Stand holen

Er klickt zwischen unseren Sitzungen. Wer die eigene Kopie hochlädt, ohne vorher zu schauen, wirft
Freigaben weg, von denen er annimmt, sie seien gespeichert.

1. `Artifact action:"read_file"` mit `path:"index.html"` → die Datei landet im Scratchpad, ohne den
   ganzen Seitentext in den Kontext zu ziehen.
2. Den `bw-state`-Block mit `grep` herausholen und **in die eigene Kopie übernehmen** (beide: Repo
   und Arbeitskopie).
3. Erst dann veröffentlichen.

Kommt beim Veröffentlichen "refused — newer version saved from inside the page": Das ist genau
dieser Fall. Die Antwort enthält die Live-Fassung; den Stand übernehmen, dann erneut hochladen.
Schlägt es ein zweites Mal mit "identical content" fehl, einmal `action:"read"` auf die URL — danach
geht es durch. `force:true` nur, wenn Björn ausdrücklich sagt, dass etwas verworfen werden darf.

## Der Fehler, der die Mappe lahmgelegt hat

Die Lupe (Vollbild für Zeichnungen) wird über das `hidden`-Attribut versteckt. Im Kopf, den die
Umgebung um unsere Datei baut, steht `[hidden]{display:none!important}` — im Kopf, den die Seite
sich beim Selbstspeichern **selbst** baut, stand er nicht. Ergebnis: Nach dem ersten Klick auf
"Freigegeben" lag eine schwarze Fläche über der ganzen Seite, und Björn kam nicht mehr weiter.

Merke: **Alles, worauf die Seite sich verlässt, muss in `bw-css` stehen**, nicht im Kopf der
Umgebung. Wer `baueDokument()` ändert, prüft, ob der erzeugte Kopf noch alles enthält, was das CSS
voraussetzt.

## Zweiter Fehler: der Freigabe-Schalter

Die drei Statusknöpfe waren Umschalter — ein zweiter Klick auf "Freigegeben" setzte still zurück auf
"offen". In einem Abnahmedokument ist das die falsche Richtung: Eine Freigabe verschwindet leise,
und niemand merkt es, bis die Anfrage nicht rausgeht. Seit 15.9.2026 setzen die Knöpfe nur noch;
zurückgenommen wird über "Zurücksetzen" daneben. Wer Interaktionen ergänzt, fragt sich bei jeder:
Was passiert, wenn jemand zweimal klickt?

## Redigieren

- Beantwortete Fragen **entfernen** und die Entscheidung als Zeile in `fakten` festhalten, mit Datum.
  Eine Mappe voller erledigter Fragen liest niemand mehr.
- Frage-IDs stabil halten (`hb01-breite`), sonst verliert eine gegebene Antwort ihren Anker.
- Modellreihenfolge nach Code.
- Bilder: `python3 sourcing/bellowerk/freigabe/bauen.py` erzeugt die verkleinerten Dateien nach
  `freigabe/media/`; beim Veröffentlichen `root: "sourcing/bellowerk/freigabe"` setzen und geänderte
  Dateien in `files` mitgeben. Entfernte Bilder mit `null` abräumen.
- Ändert sich ein Maß, gehört es **zuerst** ins Tech Pack — die Mappe zeigt dessen Stand.
