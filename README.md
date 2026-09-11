# Orchestrator — Bellowerk KI-Betrieb

Der Agentenbetrieb der Manufaktur Bellowerk (Halsbänder und Leinen aus Fettleder und Messing).
Dieses Repo **ist** `/opt/bello` auf dem netcup-Server: ein `git pull` dort bringt neue Abteilungen
und neues Einkaufswissen in den Tageslauf. Geheimnisse (`config.json`) und Betriebszustand
(`auftraege.json`, Logs) bleiben auf dem Server und sind per `.gitignore` ausgeschlossen.

## Abteilungen

| Nr. | Abteilung | Datei | Was sie tut |
|---|---|---|---|
| 01 | Innovation | `abteilung_innovation.py` | Marktbeobachtung, Produktkonzepte |
| 02 | Produkt & Ausführung | `abteilung_ausfuehrung.py` | Spezifikation, Stückliste, SVG-Zeichnung |
| 03 | Vertrieb | `abteilung_vertrieb.py` | Angebote, Kundenantworten als Entwurf |
| 04 | Social Media | `abteilung_social.py` | Beitragstexte, Aufnahmeanweisungen |
| **05** | **Einkauf China** | `abteilung_einkauf_china.py` | RFQs, Angebots- und Musterbewertung, Bestellvorbereitung bei chinesischen Herstellern — liest `sourcing/` als bindenden Kontext |

Steuerung: `orchestrator.py` (`--stand`, `--auftrag`, `--probelauf`, `--wochenbericht`),
Mail-Eskalation: `orchestrator_mail.py`, Markenwahrheit: `markenwissen.py`,
Gedächtnis: `gedaechtnis.py`.

## Gedächtnis (`gedaechtnis.py`)

Bisher fing jeder Auftrag bei null an: Markenwissen und Einkaufsunterlagen wurden jedes Mal
komplett neu bezahlt (Abteilung 05: rund 7.500 Eingabe-Tokens pro Auftrag), und was gestern
herausgefunden wurde, war heute vergessen. Drei Maßnahmen greifen jetzt ineinander:

| Was | Wie | Ersparnis |
|---|---|---|
| **Prompt-Cache** | Der unveränderliche Teil der Anfrage (Markenwissen + `sourcing/`) wird mit `cache_control` markiert. Ab dem zweiten Aufruf liest die API ihn aus dem Zwischenspeicher. | ~90 % der Eingabe-Tokens, sobald derselbe Prompt innerhalb von 5 Minuten wiederkommt — also bei jedem Lauf mit mehreren Aufträgen an dieselbe Abteilung und bei jeder Nacharbeit |
| **Gedächtnis** | Statt aller Unterlagen wandern nur die zum Ziel passenden Fakten und Kurzfassungen früherer Aufträge in den Prompt (max. 2.500 Zeichen). | Wissen aus alten Aufträgen kostet ein paar hundert statt zehntausender Tokens |
| **Antwortspeicher** | Ein wortgleicher Auftrag wird aus der Datenbank beantwortet. | 100 % — kein API-Aufruf |

Deshalb steht im System-Prompt **nichts Wechselndes** mehr: jedes Zeichen, das sich zwischen zwei
Aufrufen ändert, macht den Zwischenspeicher wertlos. Auftrag und Gedächtnis stehen dahinter,
in der Nutzernachricht.

**Was gespeichert wird.** Jedes Ergebnis wird als *Episode* abgelegt und volltextdurchsuchbar
gemacht. Zusätzlich liefert jede Abteilung im JSON ein Feld `fakten` mit bis zu fünf harten
Aussagen (`Wenzhou Vigorous — moq: 100 Stück HB-01`). Die kosten fast nichts, weil das Modell die
Antwort ohnehin schreibt, und ergeben mit der Zeit einen kleinen Wissensgraph.

**Fakten haben eine Gültigkeit.** Ändert ein Lieferant seinen MOQ, wird der alte Wert nicht
überschrieben, sondern auf *abgelöst* gesetzt. Im Prompt landet nur der aktuelle Wert; nachlesen
lässt sich beides — so bleibt nachvollziehbar, was wann galt und wer wann was zugesagt hat.

```bash
venv/bin/python orchestrator.py --gedaechtnis            # Stand und gesparte Tokens
venv/bin/python orchestrator.py --wissen "Wenzhou Vigorous"   # nachschlagen, auch die Historie
venv/bin/python orchestrator.py --vergessen 180          # alte Episoden weg, Fakten bleiben
venv/bin/python -m unittest test_gedaechtnis -v          # 19 Tests, ohne Schlüssel, ohne Kosten
```

`gedaechtnis.db` ist reines SQLite aus der Standardbibliothek — kein zusätzliches Paket, kein
Server, keine Cloud. Die Datei bleibt wie `config.json` auf dem Server und ist per `.gitignore`
ausgeschlossen. Abschalten mit `"gedaechtnis": false` in `config.json`; fällt die Datenbank aus,
läuft jeder Auftrag ohne sie weiter, statt zu scheitern.

## Einkaufsunterlagen (`sourcing/`)

```
sourcing/bellowerk/markenbrief.md   Werkstoffe, Ausschlüsse, Patch, Flechtung, Farben
sourcing/bellowerk/specs/           Tech Packs (englisch): HB-01, HB-02, LE-01, HS-01, PATCH-01, VERP-01
sourcing/bellowerk/zeichnungen/     Bemaßte Zeichnungen SVG + PNG
sourcing/bellowerk/bilder/          Referenzfotos für Lieferanten (marke/ = nur Look, nicht senden)
sourcing/vorlagen/                  Sendefertige Nachrichten: RFQ, Nachfassen, Muster, Feedback, Schnittmuster, Reklamation
sourcing/lieferanten/               Shortlist (35 Kandidaten) und Tracker
.claude/skills/china-sourcing/      Skill für Claude Code: Schreibregeln, Ablauf, QC, Lieferantenprüfung
.claude/agents/                     Vier Claude-Code-Agenten: Einkäufer, Scout, Spec-Writer, QC-Prüfer
```

## Auf dem Server (`/opt/bello`)

```bash
cd /opt/bello
git pull                                   # neue Abteilungen und Unterlagen holen
venv/bin/python orchestrator.py --probelauf
venv/bin/python orchestrator.py --auftrag "05 Einkauf China" "RFQ fuer HB-01 und LE-01 an die Prio-1-Fabriken der Shortlist" 2026-09-19
venv/bin/python orchestrator.py --stand
venv/bin/python orchestrator.py --gedaechtnis
```

Einzeltest der Einkaufsabteilung ohne Orchestrator:

```bash
venv/bin/python abteilung_einkauf_china.py "Erstkontakt/RFQ fuer HB-01 an Wenzhou Vigorous Pet Products, 100 Stueck" --recherche
```

Erstinstallation oder Umstellung eines bestehenden `/opt/bello` auf dieses Repo:
`SERVER-PROMPT-einkauf-china.md` in Claude Code auf dem Server einfügen.

## Lokal / in Claude Code

Die vier Agenten in `.claude/agents/` laufen in jeder Claude-Code-Session mit diesem Repo, auch
parallel (Scout sucht Beschlag-Lieferanten, während der Einkäufer RFQs schreibt):
`Nutze den Agenten china-einkauf: RFQ für HB-01 und LE-01 an Wenzhou Vigorous, Vorlage 01.`

## Regeln

- Keine Abteilung gibt Geld aus. Muster, Anzahlung, Bestellung → Eskalation an Björn.
- `config.json` und `gedaechtnis.db` verlassen den Server nicht. Kein Git, keine Cloud, kein Chat.
- Nacharbeit holt sich nie eine gespeicherte Antwort — sonst käme ewig dasselbe abgelehnte
  Ergebnis zurück.
- Werkstoffliste und Ausschlüsse in `markenwissen.py` und `sourcing/bellowerk/markenbrief.md` sind bindend.
