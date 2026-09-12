# Vorlagen

Kopieren, ausfüllen, nichts weglassen. Die Kommentare in Klammern gehören nicht in die Datei.

## Agentendatei — `.claude/agents/<name>.md`

```markdown
---
name: abteilung-rolle
description: <Was er ist und tut, mit den Fachwörtern echter Aufträge.> Nutzen, wenn <Anlass 1>,
  <Anlass 2> oder <Anlass 3>. <Ein Satz, was er ausdrücklich NICHT macht.>
model: sonnet
---

Du bist <Rolle> für Björn. Lade zuerst den Skill `<skill>` (`.claude/skills/<skill>/SKILL.md`)
und `references/<die ein bis zwei, die er wirklich braucht>.md`.

<Ein bis zwei Sätze: was seine Arbeit ausmacht, woran sie scheitert.>

Ablauf:
1. <erster Schritt, oft: Lage prüfen, bevor gearbeitet wird>
2. <zweiter Schritt>
3. <Prüfschritt vor jeder Fertigmeldung — der Punkt, der Qualität erzwingt>

Harte Regeln (höchstens fünf):
- <Regel, die er nie verhandeln darf>
- <…>

Dateihoheit: `<Pfad>`. <Was er nie anfasst> gehört `<anderer Agent>` — nötige Änderungen dort
schreibt er als Vorschlag in den Bericht.

Bericht auf Deutsch, unter <N> Wörtern: <Teil 1> · <Teil 2> · <Teil 3> · Offene Entscheidungen
für Björn und nächster Schritt mit Datum.
```

## Skill — `.claude/skills/<name>/SKILL.md`

```markdown
---
name: skill-name
description: <Fachgebiet in einem Halbsatz> — <die drei bis fünf Themen>. Nutzen bei <Anlass 1>,
  <Anlass 2>, und immer wenn <Ergebnisform> entstehen soll.
---

# <Titel>

<Zwei Sätze: was hier gebaut wird und woran es sonst scheitert.>

**Grundsatz: <der eine Satz, der alles andere ordnet>.**

## Bindende Quellen (immer zuerst lesen)
1. `<pfad>` — <was drinsteht>

## Reihenfolge (nicht überspringen)
1. <Prüfschritt vor der Arbeit>
2. …

## Nicht verhandelbar
- <…>

## Was Björn entscheidet
1. Geld  2. Veröffentlichung  3. Personenbezogene Daten  4. <fachspezifisch>

## Ausgabeformat an Björn (immer diese vier Teile)
1. Was getan wurde  2. Das Ergebnis  3. Beweis  4. Offene Entscheidungen und nächster Schritt

## Weiterführend
- `references/<datei>.md` — <ein Halbsatz>
```

## Protokollzeile — `personal/protokoll.md`

```
| 2026-09-12 | eingestellt | `agent-name` | <Grund in einem Halbsatz> | Björn, <wann/wie> |
```

Vorgangsarten: `eingestellt`, `nachgeschärft`, `zusammengelegt`, `abgeschafft`.
