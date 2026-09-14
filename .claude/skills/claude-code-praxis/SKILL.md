---
name: claude-code-praxis
description: Bewährte Praktiken für die Claude-Code-Konfiguration eines Repos, nach dem Setup von Boris Cherny. Nutzen, wenn eine CLAUDE.md, ein Slash-Command, ein Subagent, ein Hook oder ein Permission-Eintrag angelegt oder überarbeitet werden soll, wenn gefragt wird wie man ein Repo für Claude Code einrichtet, oder wenn ein bestehendes .claude/-Setup bewertet werden soll.
---

# Claude-Code-Praxis

Leitlinien für das Einrichten und Pflegen von `.claude/` in einem Repo. Quelle:
das öffentlich geteilte Setup von Boris Cherny (Claude-Code-Erfinder), siehe
`references/boris-setup.md`. Das ist *ein* erprobter Workflow, kein Standard —
Prinzipien übernehmen, Zahlen nicht.

## Die Reihenfolge, die sich lohnt

Wenn ein Repo noch kein oder wenig Claude-Setup hat, in dieser Reihenfolge
vorgehen. Der Nutzen fällt von oben nach unten ab.

1. **CLAUDE.md** — der größte Hebel, und der einzige Punkt, der auch ohne alles
   andere wirkt.
2. **Verifikationsschleife** — wie prüft Claude selbst, ob die Änderung
   funktioniert.
3. **Permissions** in `.claude/settings.json` — weniger Rückfragen.
4. **Slash-Commands** für alles, was mehrmals täglich läuft.
5. **Subagents** für wiederkehrende Teilaufgaben.
6. **Hooks** für den letzten Schliff (Formatierung, Checks).

## 1. CLAUDE.md

Eingecheckt ins Repo, nicht lokal. Sie ist ein *lebendes* Dokument: Wenn Claude
einen Fehler macht, der sich aus dem Code nicht ableiten ließ, gehört die
Korrektur hinein. So wird das Setup über die Zeit besser statt gleich schlecht
zu bleiben.

Hinein gehört, was man aus dem Code nicht in zwei Minuten liest:

- Wie die Teile zusammenspielen und warum sie so geschnitten sind
- Wie man Tests, Linter und die App startet — als exakte Befehle
- Konventionen, die im Code nicht sichtbar sind
- Fallen, in die Claude schon mal getappt ist

Nicht hinein gehört: eine Dateiliste (kann Claude selbst lesen), allgemeine
Programmier-Ratschläge, Copy-Paste aus der README.

**Kurz halten.** Die Datei wird in jeder Session geladen. Was drinsteht,
konkurriert mit dem eigentlichen Kontext.

## 2. Verifikationsschleife — der wichtigste Punkt

> „Wahrscheinlich das Wichtigste für gute Ergebnisse: Claude einen Weg geben,
> die eigene Arbeit zu prüfen. Mit dieser Rückkopplung verdoppelt bis
> verdreifacht sich die Qualität des Endergebnisses."

Praktisch heißt das: Sorge dafür, dass es einen Befehl gibt, der *fehlschlägt
wenn die Änderung falsch ist*, und dass Claude ihn kennt (→ CLAUDE.md). Tests,
ein Typechecker, ein Smoke-Run, ein Skript das die App startet und das Ergebnis
prüft. Ohne das rät Claude, ob es fertig ist.

Bei längeren Aufgaben: am Ende von Claude die eigene Arbeit prüfen lassen,
oder einen Stop-Hook, der es deterministisch erzwingt.

## 3. Permissions

`--dangerously-skip-permissions` ist nicht der Weg. Stattdessen über
`/permissions` die Befehle vorab erlauben, die in dieser Umgebung sicher sind,
und das Ergebnis in `.claude/settings.json` einchecken — dann hat das ganze
Team dieselbe Basis.

Ausnahme: sehr lange Läufe in einer Sandbox, wo eine Rückfrage die Sitzung
blockieren würde.

## 4. Slash-Commands

In `.claude/commands/`, eingecheckt. Kandidat ist jeder Ablauf, den man
mehrmals am Tag anstößt und jedes Mal gleich formuliert.

Zwei Dinge machen sie gut:

- **Inline-Bash vorab rechnen lassen.** Ein Command, der `git status` schon
  eingebettet mitliefert, spart eine komplette Runde.
- **Eng schneiden.** Ein Command mit drei Fallunterscheidungen ist ein Prompt,
  kein Command.

## 5. Subagents

In `.claude/agents/`. Sinnvoll für Teilaufgaben, die *für sich* abgeschlossen
sind und einen eigenen, vollen Kontext brauchen — Aufräumen nach getaner
Arbeit, End-to-End-Prüfung, eine abgegrenzte Recherche.

Nicht sinnvoll, wenn die Aufgabe den Kontext der Hauptsitzung braucht: der
Subagent startet kalt und muss sich alles neu erarbeiten.

## 6. Hooks

Ein `PostToolUse`-Hook, der den Formatter laufen lässt, fängt die letzten
Prozent ab, die sonst erst in CI auffallen. Hooks sind Automatik der Umgebung,
nicht des Modells — sie laufen zuverlässig, gerade weil Claude sie nicht
umgehen kann.

## Arbeitsweise

- **Plan Mode zuerst** (Shift+Tab zweimal) bei allem, was mehr als eine Datei
  anfasst. Erst den Plan gut machen, dann ausführen lassen. Ein guter Plan wird
  meistens in einem Zug umgesetzt; ein schlechter kostet drei Runden.
- **Das größere Modell ist unterm Strich oft das schnellere** — weniger
  Nachsteuern, bessere Werkzeugnutzung.
- **Parallel arbeiten** lohnt sich nur bei sauber getrennten Aufgaben. Wer
  mehrere Sitzungen mit verzahnten Änderungen laufen lässt, verbringt die
  gewonnene Zeit mit Konfliktauflösung.

## Bei der Bewertung eines bestehenden Setups

Der Reihe nach prüfen: Gibt es eine CLAUDE.md, und steht Brauchbares drin?
Gibt es einen Befehl, mit dem Claude die eigene Arbeit prüfen kann? Sind die
Agent- und Skill-`description`s eng genug, dass sie nur in den passenden
Sessions anspringen? Eine zu breit formulierte `description` zieht in jeder
unpassenden Session Kontext ab.
