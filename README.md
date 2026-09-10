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
| **06** | **Web & Shop** | `abteilung_web.py` | Webseiten und Shopsystem auf Agenturniveau: Leitidee, Designsystem, Sektionen, FX, Shop, Abnahmetor — liest `WEBSITE-PROMPT-ultra.md` als bindenden Kontext |

Steuerung: `orchestrator.py` (`--stand`, `--auftrag`, `--probelauf`, `--wochenbericht`),
Mail-Eskalation: `orchestrator_mail.py`, Markenwahrheit: `markenwissen.py`.

## Einkaufsunterlagen (`sourcing/`)

```
sourcing/bellowerk/markenbrief.md   Werkstoffe, Ausschlüsse, Patch, Flechtung, Farben
sourcing/bellowerk/specs/           Tech Packs (englisch): HB-01, HB-02, LE-01, HS-01, PATCH-01, VERP-01
sourcing/bellowerk/zeichnungen/     Bemaßte Zeichnungen SVG + PNG
sourcing/bellowerk/bilder/          Referenzfotos für Lieferanten (marke/ = nur Look, nicht senden)
sourcing/vorlagen/                  Sendefertige Nachrichten: RFQ, Nachfassen, Muster, Feedback, Schnittmuster, Reklamation
sourcing/lieferanten/               Shortlist (35 Kandidaten) und Tracker
.claude/skills/china-sourcing/      Skill für Claude Code: Schreibregeln, Ablauf, QC, Lieferantenprüfung
.claude/agents/china-*.md           Vier Claude-Code-Agenten: Einkäufer, Scout, Spec-Writer, QC-Prüfer
```

## Website und Shop (`WEBSITE-PROMPT-ultra.md`)

Der ultimative Auftragsprompt für Seiten auf dem Niveau der besten Werbeagenturen — und das
Designteam, das danach arbeitet.

```
WEBSITE-PROMPT-ultra.md                 Der vollständige Prompt (Block 0–11) + Kurzfassung zum Kopieren
.claude/skills/website-highend/         Arbeitsanweisung und Nachschlagewerk
  references/designsystem.md            Tokens, OKLCH-Farbleitern, Typoskala, Raster, Glanz und Schattenlagen
  references/motion-und-fx.md           GSAP, Lenis, WebGL/Shader, Rive, Abschaltmatrix, Verbote
  references/bild-pipeline.md           Bildwelt, Nano-Banana-Pipeline, Prompt-Bauplan, AVIF-Ausgabe
  references/shop-und-recht.md          Shopify Hydrogen, Bausteine, Zahlarten, deutsche Pflichtangaben
  references/qualitaetstor.md           Budgets und Abnahmetor mit 20 Punkten
.claude/agents/web-*.md                 Acht Agenten: Creative Director, Art Director, Motion & FX,
                                        Bildregie, Frontend, Commerce, Texter, Qualitätsprüfer
```

Ablauf: Leitidee → Designsystem → Bauteilübersicht → Sektionen → FX → Abnahmetor.
Budgets (LCP unter 1,8 s, INP unter 200 ms, CLS unter 0,05, Lighthouse mindestens 95/100/100)
sind Abnahmebedingungen. Reißt ein Wert, fällt der Effekt weg, nicht der Grenzwert.

Produktbilder sind echte Fotos. Nano Banana liefert Comps, Aufnahmeanweisungen, Freisteller,
Retusche und Texturen — nie ein Produktfoto, weil der Praxistest an echten Hunden das
Verkaufsargument ist.

```
Nutze den Agenten web-creative-director: Leitidee und Sektionsfolge für die neue Startseite.
Nutze den Agenten web-art-director: Designsystem und Tokens dazu bauen.
```

## Auf dem Server (`/opt/bello`)

```bash
cd /opt/bello
git pull                                   # neue Abteilungen und Unterlagen holen
venv/bin/python orchestrator.py --probelauf
venv/bin/python orchestrator.py --auftrag "05 Einkauf China" "RFQ fuer HB-01 und LE-01 an die Prio-1-Fabriken der Shortlist" 2026-09-19
venv/bin/python orchestrator.py --auftrag "06 Web & Shop" "Leitidee und Designsystem fuer die neue Startseite" 2026-09-24
venv/bin/python orchestrator.py --stand
```

Einzeltest der Einkaufsabteilung ohne Orchestrator:

```bash
venv/bin/python abteilung_einkauf_china.py "Erstkontakt/RFQ fuer HB-01 an Wenzhou Vigorous Pet Products, 100 Stueck" --recherche
```

Erstinstallation oder Umstellung eines bestehenden `/opt/bello` auf dieses Repo:
`SERVER-PROMPT-einkauf-china.md` in Claude Code auf dem Server einfügen.

## Lokal / in Claude Code

Die zwölf Agenten in `.claude/agents/` (vier Einkauf, acht Web) laufen in jeder Claude-Code-Session mit diesem Repo, auch
parallel (Scout sucht Beschlag-Lieferanten, während der Einkäufer RFQs schreibt):
`Nutze den Agenten china-einkauf: RFQ für HB-01 und LE-01 an Wenzhou Vigorous, Vorlage 01.`

## Regeln

- Keine Abteilung gibt Geld aus. Muster, Anzahlung, Bestellung → Eskalation an Björn.
- `config.json` verlässt den Server nicht. Kein Git, keine Cloud, kein Chat.
- Werkstoffliste und Ausschlüsse in `markenwissen.py` und `sourcing/bellowerk/markenbrief.md` sind bindend.
