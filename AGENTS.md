# Bellowerk-Orchestrator — Projektbeschreibung für KI-Agenten

Gilt für Codex und Claude Code gleichermaßen (`CLAUDE.md` verweist auf diese Datei).
Eine Quelle, damit beide dieselben Regeln lesen.

## Worum es geht

Agentenbetrieb der Manufaktur Bellowerk (Halsbänder und Leinen aus Fettleder und Messing).
Dieses Repo ist `/opt/bello` auf dem Server. Python, nur Standardbibliothek plus das
`anthropic`-Paket; Sprache von Code, Kommentaren und Doku ist Deutsch (ohne Umlaute im Code,
Umlaute in Markdown).

## Aufbau

- `orchestrator.py` — verteilt Aufträge, prüft Ergebnisse, eskaliert per Mail
- `abteilung_*.py` — eine Datei pro Abteilung, alle erben von `abteilung_basis.Abteilung`
- `ki_anbieter.py` — Claude, ChatGPT und Kimi hinter einer Schnittstelle; `config.json` wählt je Abteilung
- `gegenpruefung.py` — eine andere KI (Ring Claude → ChatGPT → Kimi) nimmt ein Ergebnis ab (`"gegenpruefung": true`)
- `ki_bruecke.py` — Claude Code ↔ Codex: Aufgaben und Gegenlesen, Protokoll in `uebergabe/`
- `gedaechtnis.py` — SQLite-Gedächtnis, Prompt-Cache-Logik; `markenwissen.py` — Markenwahrheit
- `sourcing/` — Einkaufsunterlagen, bindender Kontext für Abteilung 05

## Befehle

```bash
python3 -m unittest discover -p "test_*.py" -v   # alle Tests, ohne Schlüssel, ohne Kosten
python3 orchestrator.py --probelauf               # Trockenlauf
python3 orchestrator.py --anbieter                # welche KI macht was
```

## Harte Regeln

- Keine Abteilung gibt Geld aus. Muster, Anzahlung, Bestellung → Eskalation an Björn.
- `config.json`, `gedaechtnis.db`, `auftraege.json` sind Betriebszustand/Geheimnisse:
  nie committen, nie ausgeben, nie in einen Prompt kopieren.
- Der System-Prompt einer Abteilung darf **nichts Wechselndes** enthalten (Prompt-Cache).
- Werkstoffliste und Ausschlüsse in `markenwissen.py` und `sourcing/bellowerk/markenbrief.md` sind bindend.
- Fällt eine zweite KI oder das Gedächtnis aus, läuft der Auftrag weiter — nie den Betrieb daran aufhängen.

## Zusammenarbeit Claude ↔ Codex

- Wer die Gegenseite fragt, tut das über `python3 ki_bruecke.py an codex|claude "Aufgabe"`
  oder `python3 ki_bruecke.py gegenlesen codex|claude`. Die Gegenseite arbeitet **lesend**.
- Eine Gegenlesung ist ein Befund, kein Auftrag: Änderungen macht, wer die Aufgabe hat.
- Übergaben liegen in `uebergabe/` und gehören nicht in Commits.
