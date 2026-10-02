---
name: ig-plan
description: Instagram-Wochenplan für Bellowerk (/ig-plan). Verteilt Reel, Karussell und Story auf sieben Tage mit Uhrzeiten. Nutzen bei "Wochenplan", "was posten wir diese Woche".
---

# /ig-plan — Wochenplan

Format, wie im Referenz-Reel: Mo–So, je Tag Format + Uhrzeit.

Standardraster (anpassen, sobald echte Daten da sind):
Mo Reel 18:00 · Di Karussell 12:30 · Mi Story 19:00 · Do Reel 18:00 · Fr Karussell 12:30 · Sa Story 10:00 · So Reel 19:00

1. Beste Zeiten: Metricool `getBestTimeToPostByNetwork` (instagram), falls Konto verbunden; sonst Standardraster.
2. Pro Tag: Format, Uhrzeit, Thema, Aufnahmeanweisung für ein **echtes** Foto/Video (Motiv, Ort, Tageszeit, Ausschnitt). Keine KI-Bilder.
3. Themen aus dem Praxistest ziehen (Gassi, Pension, Wetter, Verschleiß). Kein Preis-Argument, keine Geschirre (siehe `markenwissen.py`).
4. Alles bleibt Entwurf. Ins Metricool nur über `createScheduledPostForReview`, nie direkt veröffentlichen.
