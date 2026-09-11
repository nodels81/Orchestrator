# Wie eine Agentendatei gebaut wird

Ablage: `.claude/agents/<name>.md`. Dateiname und `name` im Kopf sind identisch, klein, mit
Bindestrich, mit dem Abteilungspräfix (`china-`, `web-`, `android-`). Stabsstellen ohne Abteilung
tragen ihren Namen ohne Präfix.

## Der Kopf

```
---
name: android-tester
description: Schreibt und fährt die Tests einer Android-App und prüft Fertigmeldungen nach —
  Unit-Tests, Robolectric, Build und Lint. Nutzen nach jedem Feature, vor jedem Release und immer,
  wenn jemand „fertig" gesagt hat.
model: opus
---
```

**Die `description` ist das Wichtigste an der ganzen Datei.** Nach ihr wird der Agent ausgewählt —
ein guter Agent mit schwacher Beschreibung wird nie gerufen. Sie besteht aus zwei Teilen:

1. *Was er ist und tut*, mit den Fachwörtern, die in echten Aufträgen vorkommen
   („Kotlin", „RFQ", „Shopify", „Lint") — daran wird er erkannt.
2. *Wann man ihn nutzt*, wörtlich mit „Nutzen, wenn …" oder „Nutzen für …".

Was nicht hineingehört: Werbung („exzellent", „professionell"), Wiederholung des Namens, und alles,
was ihn mit einem anderen Agenten verwechselbar macht.

## Die Modellwahl

| Modell | Wofür | Beispiele |
|---|---|---|
| `opus` | Wo Fehler teuer sind: Architektur, Code, Prüfung, Texte mit Markenwirkung | `android-entwickler`, `android-tester`, `web-creative-director`, `web-texter` |
| `sonnet` | Regelmäßige Arbeit nach klarer Vorlage: Umsetzung, Recherche, Formatierung | `web-frontend`, `china-lieferanten-scout`, `android-ui` |

Im Zweifel `sonnet` — und `opus` erst, wenn ein Fehler an dieser Stelle echten Schaden anrichtet.

## Der Rumpf: 20 bis 30 Zeilen, nicht mehr

Immer in dieser Reihenfolge:

1. **Wer er ist**, ein bis zwei Sätze, direkt angesprochen („Du bist …").
2. **Was er zuerst liest** — der Skill und die ein bis zwei Referenzen, die er wirklich braucht.
   Fachwissen steht im Skill, nicht in der Agentendatei: sonst driften zwei Agenten auseinander.
3. **Seine harten Regeln** — nur die, die er nicht verhandeln darf. Fünf gute schlagen fünfzehn.
4. **Dateihoheit** — was er schreibt, was er nie anfasst, was er stattdessen als Vorschlag meldet.
5. **Berichtsform** — an Björn auf Deutsch, mit fester Gliederung und einer Längengrenze.

## Wiederkehrende Fehler

- **Zu breit.** „Kümmert sich um alles rund um die App" — der Agent macht dann alles halb.
- **Fachwissen doppelt.** Steht derselbe Standard in drei Agenten, driften die drei auseinander.
  Er gehört in den Skill.
- **Keine Grenze.** Ohne Dateihoheit schreiben zwei Agenten in dieselbe Datei und der Stand ist hin.
- **Keine Berichtsform.** Dann bekommt Björn fünf verschiedene Formate und liest keines.
- **Lob statt Auftrag.** „Du bist ein erstklassiger Entwickler" ändert nichts. „Vor jeder
  Fertigmeldung läuft `./gradlew testDebugUnitTest`" ändert alles.
