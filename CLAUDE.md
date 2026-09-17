# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Die Sprache des Projekts ist Deutsch: Code-Kommentare, Docstrings, Commit-Nachrichten,
Dokumentation und Variablennamen. Bezeichner im Code stehen ohne Umlaute
(`abteilung_ausfuehrung`, `gedaechtnis`), Fließtext mit.

## Was das hier ist

Der KI-Agentenbetrieb der Lederwaren-Manufaktur Bellowerk. Elf Abteilungen erledigen
Aufträge über die Claude API; `orchestrator.py` verteilt sie, prüft die Ergebnisse
maschinell und eskaliert per Mail an den Inhaber (Björn). Grundprinzip: **Schweigen ist
der Normalzustand** — gemeldet wird nur, was eine Entscheidung braucht.

Dieses Repo **ist** `/opt/bello` auf dem netcup-Server. Ein `git pull` dort bringt
Änderungen in den stündlichen Lauf (07–19 Uhr, systemd). Was hier gemergt wird, geht
also in den laufenden Betrieb.

## Befehle

Das virtuelle Umfeld heißt **`.venv`** (der Server nutzt `/opt/bello/.venv`). Ältere
Dateien schreiben teils noch `venv/bin/python` — beim Anfassen auf `.venv` ziehen.

```bash
.venv/bin/python -m unittest discover -p "test_*.py"      # gesamte Suite, ohne Schlüssel, ohne Kosten
.venv/bin/python -m unittest test_sparmassnahmen -v       # eine Datei
.venv/bin/python -m unittest test_gedaechtnis.GedaechtnisTest   # eine Klasse
.venv/bin/python orchestrator.py --probelauf              # Trockenlauf, keine API-Kosten
.venv/bin/python orchestrator.py --stand                  # woran gearbeitet wird; ! = wartet auf Björn
.venv/bin/python orchestrator.py --gedaechtnis            # Wissensstand und gesparte Tokens
.venv/bin/python abteilung_einkauf_china.py "RFQ fuer HB-01" --recherche   # eine Abteilung einzeln
```

Es gibt keinen Linter und keinen Formatter im Projekt. Beide Testdateien laufen ohne
API-Schlüssel und ohne Netz — `test_sparmassnahmen.py` ersetzt den Client durch eine
Attrappe, die den Aufruf nur festhält. Jeder Test, der die API wirklich riefe, kostet
Geld; halte es bei der Attrappe.

`anthropic` ist in Entwicklungsumgebungen oft nicht installiert, und `abteilung_basis`
bricht dann beim Import ab. Für Messungen und Skripte eine Hülle einschleusen:

```python
import sys, types
sys.modules.setdefault("anthropic", types.ModuleType("anthropic"))
sys.modules["anthropic"].Anthropic = lambda **kw: None
```

## Architektur

**Eine Abteilung = eine Datei.** `abteilung_basis.Abteilung` trägt die ganze Mechanik;
Ableitungen setzen im Wesentlichen `NUMMER`, `NAME`, `ROLLE` und ein paar Grenzen. Neue
Abteilung heißt: Datei anlegen, in `ABTEILUNGEN` in `orchestrator.py` eintragen, Vorname
in `namen.py` ergänzen. `abteilung_basis.py` muss dafür normalerweise nicht angefasst
werden.

**Der Vertrag zwischen Abteilung und Orchestrator ist JSON.** Jede Abteilung liefert
`ergebnis`, `kriterien_erfuellt` (eine Liste mit genau so vielen Einträgen wie der
Auftrag Kriterien hat, in derselben Reihenfolge), `blocker`, `anmerkung`,
`zusammenfassung` und `fakten`. Der Orchestrator *interpretiert nichts* — er liest
`kriterien_erfuellt` und `blocker` und entscheidet danach. Wer dieses Schema ändert,
ändert `antwortformat()`, `pruefen()` und das Gedächtnis zugleich.

**Zustand liegt außerhalb des Arbeitsbaums.** Der Dienst darf nur nach `daten/` und
`logs/` schreiben (`ProtectSystem=strict`), damit `git pull` nie in einen Konflikt
läuft. `config.json`, `auftraege.json` und `gedaechtnis.db` bleiben auf dem Server und
sind per `.gitignore` ausgeschlossen. Nie Code schreiben, der in den Arbeitsbaum
schreibt.

**Das Gedächtnis (`gedaechtnis.py`)** ist SQLite aus der Standardbibliothek. Es hält
Episoden (volltextdurchsuchbar), Fakten (Subjekt–Prädikat–Objekt, mit Gültigkeit statt
Überschreiben) und einen Antwortspeicher. Es darf nie einen Auftrag aufhalten: jeder
Zugriff ist in `try` gefasst, bei Ausfall läuft der Auftrag ohne. Abschaltbar mit
`"gedaechtnis": false`.

**Zwei Zwischenschritte im Lauf**, beide leicht zu übersehen: `09 Qualität` prüft die
Ergebnisse der Abteilungen aus `config["qm_gate"]` — das ist ein *zweiter* API-Aufruf
pro Auftrag. Und Nacharbeit (`MAX_NACHARBEIT`) holt sich nie eine gespeicherte Antwort,
sonst käme ewig dasselbe abgelehnte Ergebnis zurück.

## Kosten sind ein Entwurfskriterium

Jeder Aufruf kostet echtes Geld, und Ausgabe-Tokens kosten das Fünffache der Eingabe.
Vier Maßnahmen greifen ineinander; `test_sparmassnahmen.py` sichert sie ab. Wer hier
etwas ändert, prüft die Wirkung mit, statt sie zu schätzen:

- **`MAX_WOERTER`** begrenzt das Feld `ergebnis` und steht so im Prompt. `None` heißt
  keine Grenze — so bei Ausführung, Design, Personal, Homepage und App, deren Ergebnis
  von Natur aus lang ist. Eine Grenze wäre dort Schaden, keine Ersparnis.
- **`DENKTIEFE`** wird als `output_config: {"effort": ...}` mitgegeben. Standard `low`;
  wer wirklich abwägt (Einkauf, Einkauf China, Qualität) oder plant, steht auf `medium`.
  Per `"denktiefe"` in `config.json` global überschreibbar.
- **`MAX_TOKENS`** ist das Dach. Eine am Dach abgeschnittene Antwort wird zum Blocker,
  nicht zum Ergebnis — sonst wandert ein halber Satz als erledigt in die Eskalation.
- **Der Zwischenspeicher** (`cache_control`) wird nur vermerkt, wenn dieselbe Abteilung
  in diesem Lauf mehrfach drankommt; `orchestrator.abteilung_holen` entscheidet das.
  Jede Abteilung hat einen eigenen System-Prompt, Schreiben kostet das 1,25-fache, und
  bei einem einzelnen Aufruf wird nie gelesen. Nacharbeit läuft erst im nächsten Lauf,
  also außerhalb der 5-Minuten-Frist, und trägt den Cache nicht.

Daraus folgt die wichtigste Regel für `system_prompt()`: **dort steht nichts
Wechselndes.** Jedes Zeichen, das sich zwischen zwei Aufrufen ändert, entwertet den
Zwischenspeicher. Auftragsbezogene Unterlagen gehören in `auftrag_kontext(auftrag)` —
der Hook schreibt sie in die Nutzernachricht. `abteilung_einkauf_china` wählt so nur die
Tech Packs aus, deren Kürzel (`HB-01`, `LE-02`, `VERP-01` …) im Auftragsziel vorkommen.

## Inhaltliche Regeln, die der Code durchsetzt

- **Keine Abteilung gibt Geld aus.** Muster, Anzahlung, Bestellung → Eskalation an
  Björn. Das steht in jedem System-Prompt und darf nicht aufgeweicht werden.
- **`markenwissen.py` und `sourcing/bellowerk/markenbrief.md` sind bindend** — Werkstoffe
  (Fettleder pflanzlich gegerbt, Messing massiv; kein Zink, kein Stahl, kein Lack) und
  die harten Ausschlüsse. `markenwissen.py` ist die Quelle, der Markenbrief unter
  `daten/` wird daraus erzeugt; die Fassung unter `sourcing/` ist der ältere
  versionierte Stand und springt nur ein, solange es den frischen nicht gibt.
- **Nach außen gehen nur Entwürfe.** Abteilungen schreiben sendefertige Texte, verschickt
  wird nichts ohne Freigabe.

## Arbeiten in diesem Repo

- Branches immer frisch von `origin/main` aus starten und vor dem Weiterarbeiten
  `git fetch origin main` laufen lassen. `main` bewegt sich schnell; ein Branch, der auf
  einem alten Stand sitzt, wirft beim Mergen den halben Betrieb zurück.
- Änderungen an Prompts, Grenzen oder Kostenlogik gehören mit einem Test abgesichert,
  der ohne API auskommt (Muster: `test_sparmassnahmen.py`).
- `BETRIEB.md` ist die Betriebsanleitung für den Server (Dienst, Sicherung, Dashboard),
  `README.md` die Übersicht. Beide nachziehen, wenn sich Verhalten ändert — im README
  stehen Abteilungsnummern, die bei Umbauten leicht veralten.
