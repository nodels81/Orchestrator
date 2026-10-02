---
name: ig-profile
description: Instagram-Profil-Check für Bellowerk (/ig-profile). Bewertet Bio, Name, Highlights und Raster, gibt einen Score 0–100 und eine konkrete neue Bio. Nutzen bei "Profil prüfen", "Bio verbessern".
---

# /ig-profile — Profil-Check

Quelle der Marke: `markenwissen.py` (Positionierung, Ausschlüsse). Konto: `@herr.bello.und.frau.wuff`.

1. Profildaten holen: Metricool (`getAnalyticsDataByMetrics`, network `instagram`, connector `info`), sonst Björn um Screenshot/Text bitten. Nichts erfinden.
2. Bewerten (je 0–20, Summe = Score): Bio-Klarheit (Nutzen statt Floskel), Positionierung (Praxistest an fremden Hunden), Highlights, Raster-Konsistenz (Leder-Look, echte Fotos), Handlungsaufforderung/Link.
3. Ausgabe: Score, Bio **alt → neu** (alt durchgestrichen, neu mit konkretem Nutzen, max. 150 Zeichen), drei Verbesserungen nach Hebel sortiert.

Bio-Regel: Nutzen statt "Ich helfe …". Beispiel-Muster: "Leder-Zubehör, das eine Saison an fremden Hunden getestet wurde. Hamburg."
