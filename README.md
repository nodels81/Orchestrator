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
| **07** | **App Android** | `abteilung_app_android.py` | Spezifikationen, Baupläne, Code-Reviews und Store-Texte für Android-Apps — konzipiert im Tageslauf, gebaut wird in Claude Code |

Steuerung: `orchestrator.py` (`--stand`, `--auftrag`, `--probelauf`, `--wochenbericht`),
Mail-Eskalation: `orchestrator_mail.py`, Markenwahrheit: `markenwissen.py`.

### Wer sitzt wo

Alles gehört zu Bellowerk. Jede Abteilung ist eigenständig; die Agenten in `.claude/agents/`
gehören immer **einer** Abteilung — erkennbar am Namensanfang.

```
Bellowerk  (Björn entscheidet)
│
├─ wiebke  — Personalerin, Stabsstelle neben der Hierarchie
│           wöchentlicher Rundgang durch alle Abteilungen, meldet Schwachstellen per Mail;
│           stellt nach Björns Freigabe ein, schärft nach, legt zusammen
│           Skill: agenten-personal · Protokoll: personal/protokoll.md
│
├─ 01 Innovation            abteilung_innovation.py
├─ 02 Produkt & Ausführung  abteilung_ausfuehrung.py
├─ 03 Vertrieb              abteilung_vertrieb.py
├─ 04 Social Media          abteilung_social.py
│
├─ 05 Einkauf China         abteilung_einkauf_china.py   Skill: china-sourcing
│   ├─ china-einkauf             schreibt an Lieferanten, bewertet Angebote
│   ├─ china-lieferanten-scout   sucht und prüft Hersteller
│   ├─ china-qc-pruefer          Muster, Endkontrolle, Reklamation
│   └─ china-spec-writer         Tech Packs und Zeichnungen
│
├─ 06 Web & Shop            abteilung_web.py             Skill: website-highend
│   ├─ web-creative-director     Leitidee der Seite, Sektionsfolge
│   ├─ web-art-director          Designsystem, Farbleitern, Typoskala, Raster
│   ├─ web-bildregie             Bildwelt, Aufnahmeanweisungen für echte Fotos
│   ├─ web-texter                Claim, Headlines, Produkttexte, Mikrotexte
│   ├─ web-frontend              setzt Designsystem und Sektionen als Code um
│   ├─ web-motion-fx             Scroll-Choreografie, Übergänge, WebGL
│   ├─ web-shop-commerce         das Shopsystem (Shopify Hydrogen / Next.js + Medusa)
│   └─ web-qc-abnahme            Abnahmetor mit 20 Punkten
│
└─ 07 App Android           abteilung_app_android.py     Skill: android-app
    ├─ android-architekt         Spezifikation, Datenmodell, Bauplan
    ├─ android-entwickler        programmiert: Kotlin, Compose, Daten, Netz
    ├─ android-ui                Layout: Theme, Dark Mode, Barrierefreiheit
    ├─ android-tester            Tests, Build, Lint — prüft Fertigmeldungen nach
    └─ android-release           Version, Signierung, AAB, Store-Unterlagen
```

Die Abteilungsdatei ist der Kopf: sie konzipiert im Tageslauf und verteilt Aufträge an ihre
Agenten. Die Agenten arbeiten in Claude Code am Repo. Abteilungen 01–04 haben keine Agenten,
sie laufen nur im Tageslauf.

Wiebke gehört keiner Abteilung. Fehlt für eine Aufgabe der passende Agent, oder liefert einer
schlechte Arbeit, ist sie zuständig: `Nutze den Agenten wiebke: …`

Ihr Rundgang läuft ohne Nachfrage und schickt Björn den Bericht per Mail:

```bash
venv/bin/python personal_rundgang.py --probelauf   # zeigt nur, was geladen wird
venv/bin/python personal_rundgang.py --senden      # Bericht erzeugen und mailen
```

Wöchentlich per Timer, z. B. montags 07:30. **Der Rundgang stellt niemanden ein** — er meldet.
Eingestellt wird in vier Schritten: vorschlagen, Björns „ja" abwarten, Datei schreiben und im
Wortlaut vorlegen, erst nach der zweiten Freigabe hochladen. Jede Änderung landet als Zeile in
`personal/protokoll.md`.

**Achtung, noch nicht zusammengeführt:** Abteilung 06 Web & Shop liegt auf Branch
`claude/ultimate-website-prompt-ira6ls`, Abteilung 07 App Android auf
`claude/android-app-dev-prompt-2suf67`. Beide waren ursprünglich als „06" angelegt — App Android
ist deshalb auf 07 umnummeriert, damit sich beim Zusammenführen keine Abteilung verdrängt.

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
```

Einzeltest der Einkaufsabteilung ohne Orchestrator:

```bash
venv/bin/python abteilung_einkauf_china.py "Erstkontakt/RFQ fuer HB-01 an Wenzhou Vigorous Pet Products, 100 Stueck" --recherche
```

Erstinstallation oder Umstellung eines bestehenden `/opt/bello` auf dieses Repo:
`SERVER-PROMPT-einkauf-china.md` in Claude Code auf dem Server einfügen.

## App-Entwicklung Android (Abteilung 07)

Zweigeteilt, weil `abteilung_basis.py` die API ohne Werkzeuge und ohne Dateizugriff ruft: die
Abteilung im Tageslauf **konzipiert** (Spezifikation, Bauplan, Review, Store-Texte), **gebaut** wird
in Claude Code mit fünf Agenten:

| Agent | Rolle |
|---|---|
| `android-architekt` | Idee → Spezifikation, Bildschirmfluss, Datenmodell, Bauplan |
| `android-entwickler` | Kotlin, Compose, ViewModel, Room, Netz, Gradle |
| `android-ui` | Material-3-Theme, Zustände, Dark Mode, Barrierefreiheit |
| `android-tester` | Tests, Build, Lint — prüft jede Fertigmeldung nach |
| `android-release` | Version, Signierung, AAB, Store-Unterlagen (lädt nichts hoch) |

Standard und Prüfregeln: `.claude/skills/android-app/` — die Abteilung liest ihn als bindenden
Kontext, die Agenten laden ihn als Skill. Rollenverteilung, Umgebungsvoraussetzungen und der
einfügbare Einzel-Prompt: `PROMPT-abteilung-app-android.md`.

```bash
venv/bin/python orchestrator.py --auftrag "07 App Android" "Spezifikation fuer App Bello Tour" 2026-09-25
venv/bin/python abteilung_app_android.py "App-Idee: Hunderunden aufzeichnen"
```

Ein Build braucht Android SDK und Zugriff auf `dl.google.com` — in einer Web-Session mit engem
Netz-Regelwerk ist beides gesperrt. Dort entstehen Spezifikation und Code, gebaut wird auf Björns
Rechner mit Android Studio.

## Lokal / in Claude Code

Die vier Agenten in `.claude/agents/` laufen in jeder Claude-Code-Session mit diesem Repo, auch
parallel (Scout sucht Beschlag-Lieferanten, während der Einkäufer RFQs schreibt):
`Nutze den Agenten china-einkauf: RFQ für HB-01 und LE-01 an Wenzhou Vigorous, Vorlage 01.`

## Regeln

- Keine Abteilung gibt Geld aus. Muster, Anzahlung, Bestellung → Eskalation an Björn.
- `config.json` verlässt den Server nicht. Kein Git, keine Cloud, kein Chat.
- Werkstoffliste und Ausschlüsse in `markenwissen.py` und `sourcing/bellowerk/markenbrief.md` sind bindend.
