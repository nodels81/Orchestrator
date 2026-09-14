# Quelle: Das Claude-Code-Setup von Boris Cherny

Boris Cherny ist einer der Erfinder von Claude Code. Er hat sein persönliches
Setup öffentlich geteilt; die folgenden Punkte sind die Zusammenfassung davon.
Er stellt selbst voran: es gibt kein „richtiges" Vorgehen, jede Person im
Claude-Code-Team arbeitet anders, und das Werkzeug funktioniert ohne
Anpassungen bereits gut.

Diese Datei ist Belegmaterial für `../SKILL.md` — dort steht, was davon wir
übernehmen.

## Parallele Sitzungen

Fünf Claude-Instanzen gleichzeitig im Terminal (Tabs 1–5 durchnummeriert),
dazu 5–10 Sitzungen auf claude.ai/code. Systembenachrichtigungen melden, wenn
eine Instanz eine Eingabe braucht. Übergabe zwischen lokal und Web mit `&`,
Verschieben von Sitzungen mit `--teleport`. Sitzungen werden morgens vom
iPhone aus gestartet und später eingesammelt.

## Modellwahl

Opus mit Thinking für alles. Begründung: zwar größer und pro Anfrage langsamer
als Sonnet, aber insgesamt schneller — weniger Nachsteuern, bessere
Werkzeugnutzung, höhere Qualität im ersten Wurf.

## CLAUDE.md

Eine gemeinsame Datei fürs Repo, eingecheckt. Das ganze Team trägt mehrmals
pro Woche etwas ein. Wenn Claude einen Fehler macht, wird er dort dokumentiert.
Verschiedene Teams pflegen je eigene Dateien.

Im Code-Review taggt Boris `@.claude` auf den PRs von Kolleg:innen, um
Einträge als Teil des PR-Prozesses in die CLAUDE.md aufzunehmen (via
Claude-Code-GitHub-Action, `/install-github-action`).

Prinzip dahinter: „Compounding Engineering" — die KI wird über die Zeit besser
im Umgang mit der Codebasis, weil sich Teamwissen ansammelt.

## Plan Mode

Die meisten Sitzungen starten im Plan Mode (Shift+Tab zweimal). Hin und her mit
Claude, bis der Plan überzeugt, dann auf Auto-Accept-Edits umschalten — die
Ausführung gelingt dann meist in einem Zug. „Ein guter Plan ist wirklich
wichtig."

## Slash-Commands

Für jeden „Inner Loop", der mehrmals täglich läuft. Eingecheckt in
`.claude/commands/`. Beispiel `/commit-push-pr`, dutzende Male am Tag im
Einsatz; nutzt Inline-Bash, um `git status` vorab zu berechnen, was eine
Modellrunde spart.

## Subagents

Regelmäßig im Einsatz: `code-simplifier` (räumt auf, nachdem Claude fertig
ist) und `verify-app` (ausführliche Anweisungen für End-to-End-Tests von
Claude Code). Denkweise: Subagents als Automatisierung der häufigsten
Abläufe über die meisten PRs hinweg.

## Hooks

Ein `PostToolUse`-Hook formatiert Claudes Code automatisch. Claude schreibt
meist schon gut formatierten Code; der Hook erledigt die letzten zehn Prozent
und verhindert, dass Formatierungsfehler erst in CI auffallen.

## Permissions

Kein `--dangerously-skip-permissions`. Stattdessen `/permissions`, um
bekanntermaßen sichere Bash-Befehle vorab zu erlauben; die Einträge liegen in
`.claude/settings.json` und sind mit dem Team geteilt.

Ausnahme: sehr lange Läufe in Sandboxes, dort `--permission-mode=dontAsk` oder
`--dangerously-skip-permissions`, damit Claude nicht an einer Rückfrage hängen
bleibt.

## MCP-Anbindung

Claude Code nutzt Boris' gesamtes Werkzeug: Slack durchsuchen und posten (MCP),
BigQuery-Abfragen (`bq`-CLI), Fehlerlogs aus Sentry. Die Slack-MCP-Konfiguration
liegt eingecheckt in `.mcp.json` und ist mit dem Team geteilt.

## Lange Läufe

Claude am Ende die eigene Arbeit von einem Hintergrund-Agenten prüfen lassen;
Stop-Hooks für deterministischere Verifikation; das `ralph-wiggum`-Plugin für
spezielle Langläufer; Permission-Modi wie oben.

## Der wichtigste Punkt: Verifikationsschleifen

> „Wahrscheinlich das Wichtigste, um großartige Ergebnisse aus Claude Code zu
> bekommen — Claude einen Weg geben, die eigene Arbeit zu verifizieren. Wenn
> Claude diese Rückkopplung hat, verdoppelt bis verdreifacht das die Qualität
> des Endergebnisses."

Beispiel: Jede Änderung an claude.ai/code wird von Claude selbst über die
Chrome-Erweiterung getestet — Browser öffnen, UI testen, iterieren bis es
funktioniert.

## Die Prinzipien in einem Satz

1. Parallelisieren, wo Aufgaben unabhängig sind
2. Qualität vor Geschwindigkeit bei der Modellwahl
3. Wissen ansammeln statt Fehler wiederholen
4. Planen vor Ausführen
5. Wiederholungen automatisieren
6. Tief integrieren
7. Die Rückkopplungsschleife schließen

---

Zusammengetragen aus Boris Chernys öffentlichem Thread zu seinem Setup
(Threads, `@boris_cherny`) und der daraus entstandenen Aufbereitung unter
`github.com/moarbetsy/Boris-s-Claude-Code-Setup-Guide`. Stand: September 2026.
