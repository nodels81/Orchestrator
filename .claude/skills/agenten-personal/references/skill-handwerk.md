# Wann ein Skill das bessere Mittel ist

**Agent = eine Rolle, die arbeitet. Skill = Wissen, das mehrere Rollen teilen.**

Fehlt Wissen, schreibst du einen Skill. Fehlt jemand, der eine bestimmte Arbeit verantwortet,
stellst du einen Agenten ein. Die Faustregel: Sobald zwei Agenten dieselbe Regel bräuchten,
gehört sie in einen Skill — sonst driften die Fassungen auseinander.

## Aufbau

```
.claude/skills/<name>/
  SKILL.md              60–90 Zeilen: Grundsatz, Reihenfolge, harte Regeln, Ausgabeformat
  references/*.md       je 40–80 Zeilen Tiefe, einzeln nachladbar
```

`SKILL.md` trägt einen Kopf mit `name` und `description`. Die `description` entscheidet, ob der
Skill überhaupt geladen wird — sie nennt das Fachgebiet **und** die Anlässe („Nutzen bei jeder
Anfrage, Musterbestellung, Reklamation …").

## Was in SKILL.md gehört

1. **Bindende Quellen zuerst** — welche Dateien im Repo die Wahrheit sind.
2. **Reihenfolge der Arbeit**, nummeriert, mit dem Prüfschritt, der nicht übersprungen werden darf.
3. **Harte Regeln** — was nie passieren darf, in Björns Sprache.
4. **Was Björn entscheidet** — Geld, Veröffentlichung, personenbezogene Daten.
5. **Ausgabeformat** — dieselbe Gliederung für alle Agenten dieser Abteilung.
6. **Verweisliste** auf die Referenzen, je mit einem Halbsatz, was drinsteht.

Tiefe kommt in `references/`, nicht in SKILL.md: die Hauptdatei wird immer gelesen, die Referenzen
nur bei Bedarf. Alles, was ein Agent nur manchmal braucht, gehört nach hinten.

## Prüfung eines fertigen Skills

- Findet ein fremder Agent darin in einer Minute die Regel, die er sucht?
- Steht irgendwo eine Zahl, die niemand nachgeprüft hat? Dann „nachsehen" dazuschreiben.
- Widerspricht er einem anderen Skill? Dann gehört der Widerspruch aufgelöst, nicht verdoppelt.
- Enthält er Fachwissen, das nur ein einziger Agent braucht? Das gehört in dessen Datei.
