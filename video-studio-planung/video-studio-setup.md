# Auftrag an Claude Code: Video-Studio mit Telegram-Bot

> **Wo du läufst:** Du (Claude Code) läufst auf Björns **Windows-PC** (PowerShell). Der Server wird von hier aus per SSH eingerichtet. Starte mit **Phase 0**. Björn tippt nur dann selbst etwas, wenn du ihn ausdrücklich darum bittest (z. B. einmal das Server-Passwort).

Baue auf diesem Server ein vollautomatisches Video-Studio, das für **jedes beliebige Unternehmen, Produkt oder Thema** Kurzvideos in Top-Qualität produziert und sich mit jedem Video selbst verbessert. Björn bedient es ausschließlich über Telegram: Er gibt eine Beschreibung und optional eine Website an, wählt einen Stil, beantwortet ein kurzes Interview und bekommt am Ende das fertige Video im Chat. Dazwischen hat er mit nichts zu tun.

Björns eigenes Unternehmen **Herr Bellos Rudel** ist nur ein Kunde von vielen und dient als erstes Testprofil.

## Der Ablauf aus Björns Sicht

1. **Vorgabe:** Björn schreibt dem Bot, worum es geht (Text oder Sprachnachricht), optional mit Website, Instagram-Link oder eigenen Fotos/Clips.
   Beispiel: „Imagevideo für die Bäckerei Schulz, www.baeckerei-schulz.de, Fokus auf das neue Frühstücksangebot.“
2. **Recherche (automatisch, im Hintergrund):** Das System liest die Website aus und legt ein Firmenprofil an oder aktualisiert ein vorhandenes.
3. **Stil wählen:** Fünf Knöpfe (aus `stile/` gelesen):
   - **Handgezeichnet** – Stiftzeichnung, die sich vor den Augen aufbaut
   - **Comic** – Comic-Panels mit Menschen, gleichbleibende Figuren, Sprechblasen
   - **High-End Fashion** – Werbespot wie von einer Luxus-Modemarke
   - **Knete-Welt** – 3D-Claymation im Stop-Motion-Look
   - **Mini-Doku** – „Ein Tag bei …“ mit großer bewegter Schrift
   Zusätzlich ein Knopf **„Überrasch mich“**: Das System wählt den Stil, der laut bisherigen Ergebnissen für diese Branche am besten funktioniert.
4. **Interview:** Höchstens 5 Fragen, **nur zu dem, was die Recherche nicht beantworten konnte**, mit Antwort-Knöpfen wo möglich.
5. **Bestätigung:** Zusammenfassung in drei Zeilen mit Knopf „Los“. Das ist der einzige Klick.
6. **Ergebnis:** Fertiges Video, Titelbild und Caption mit Hashtags kommen in den Chat. Darunter optional ⭐ 1–5 zum Bewerten (ein Tipp, kein Muss). Ende.

Nur wenn etwas endgültig scheitert, kommt eine kurze Meldung mit Knopf „Nochmal versuchen“.

## Welche Informationen ein Video braucht

Grundlage für Recherche und Interview. Der `recherche`-Agent füllt so viel wie möglich selbst, der `interviewer` fragt nur die Lücken ab, wichtigste zuerst.

**A. Über das Unternehmen (meist von der Website, gespeichert im Firmenprofil)**
- Name, Branche, Standort bzw. Einzugsgebiet
- Leistungen bzw. Produkte, gern mit Preisen
- Was es besonders macht (Alleinstellung, Geschichte, Werte)
- Zielkunden
- Kontakt: Website, Telefon, Instagram, Adresse
- Markenauftritt: Logo, Farben, Schriften, Tonalität
- Vorhandenes Material: Fotos, Videos, Kundenstimmen, Bewertungen

**B. Über dieses eine Video (aus dem Interview)**
1. **Ziel:** Was soll der Zuschauer danach tun?
2. **Kernbotschaft:** Welcher eine Satz soll hängen bleiben?
3. **Zielgruppe:** Wer genau soll es sehen?
4. **Pflichtinhalte:** Angebot, Preis, Aktion, Datum, Ort
5. **Rahmen:** Länge (15 / 30 / 60 Sek.), Sprecherstimme ja/nein, Plattform

**C. Optional:** No-Gos, Vorbilder, eigenes Material nachschicken.

Fehlt danach noch etwas, trifft das System eine sinnvolle Annahme und vermerkt sie im Briefing.

## Kontext

- Server: Netcup VPS Lite 1 G12s, Debian 13 (Trixie) minimal, eher wenig Leistung
- Inhaber: Björn, Hamburg, spricht Deutsch, nutzt viel Sprachnachrichten
- Björns eigenes Unternehmen: **Herr Bellos Rudel** – Gassi-Service, Hundepension, Hundetraining, Fettleder-Zubehör (erstes Firmenprofil)
- Björn nutzt Metricool für Social Media (für die Lernschleife, Phase 7)
- Ausgabe: MP4, 1080×1920 (9:16), Untertitel eingebrannt, Standardsprache Deutsch

## Arbeitsregeln für dich (Claude Code)

1. Arbeite die Phasen nacheinander ab. Nach jeder Phase kurze Zusammenfassung auf Deutsch, dann auf „weiter“ warten.
2. Vor Löschen, Zugangsänderungen oder kostenpflichtigen Aktionen: fragen.
3. Ressourcen zuerst prüfen, bei wenig RAM Swap anlegen. Rechenintensives (Bilder, Videoclips, Stimme) läuft über APIs. Nach dem ersten Testvideo misst du Renderzeit, RAM-Spitze und CPU-Last und sagst Björn klar, ob der Server reicht oder ein Upgrade lohnt (mehr RAM/Kerne, keine GPU nötig). Achtung: Remotion rendert mit einem Headless-Chrome und braucht deutlich mehr RAM als reines ffmpeg.
4. Für Bild- und Videogenerierung: recherchiere die aktuell besten verfügbaren Modelle (z. B. über fal.ai oder Replicate), schlage Björn je Stil eins vor mit grober Kostenangabe pro Video und lass ihn entscheiden. Modellnamen stehen nur in `config/modelle.yaml`, damit ein Wechsel eine Zeile ist.
5. Schlüssel nur in `~/video-studio/.env` (Rechte 600), nie in Code, Logs oder Git.
6. Kostenbremse: `MAX_KOSTEN_PRO_VIDEO=5` (Euro) in `.env`. Jeder API-Aufruf wird vorher geschätzt und danach verbucht. Droht das Limit überschritten zu werden, weicht der Kosten-Wächter zuerst auf günstigere Optionen aus; reicht das nicht, stoppt die Produktion mit kurzer Meldung.
7. Bildrechte: Fotos, Logos und Clips von fremden Websites nur verwenden, wenn Björn einmal pro Firma bestätigt, dass der Auftraggeber die Rechte hat. Sonst nur Fakten übernehmen und Bilder generieren. Musik nur lizenzfrei mit dokumentierter Quelle.
8. Fremder Code: Nur die Repos aus der Werkzeugliste unten verwenden. Vor der Installation Lizenz und letzte Aktivität prüfen, Versionen festschreiben. Community-MCP-Server nie mit API-Schlüsseln füttern, ohne den Code vorher durchgesehen zu haben – im Zweifel lieber die offiziellen Python-Clients in `scripts/` nutzen.

### Sparregeln (verbindlich)

- **Code statt KI, wo möglich:** Schnitt, Untertitel-Timing, Musikauswahl, Lautheit, Versand, Kostenzähler sind feste Skripte ohne Sprachmodell. Claude nur für kreative und bewertende Schritte.
- **Modell nach Aufgabe:** Einfache Schritte (Caption, Recherche-Zusammenfassung, Interviewfragen) mit Haiku, Skript, Regie und Prüfung mit Sonnet, großes Modell nur in Ausnahmefällen. Modell je Agent in dessen Datei festlegen.
- **Kurzer Kontext:** Jeder Agent bekommt nur die Dateien, die er braucht. `CLAUDE.md` und Steckbriefe knapp halten.
- **Wiederverwenden:** Firmenprofile, Charakterblätter und gelungene Clips pro Firma speichern.
- **Billig vor teuer:** Standbild mit Bewegung statt generiertem Videoclip, wo der Stil es erlaubt. Teure Videogenerierung nur für Schlüsselszenen.
- **Prüfer sparsam:** wenige Einzelbilder in geringer Auflösung, höchstens 2 Korrekturrunden.
- **Kosten sichtbar:** Pro Video Tokens und API-Kosten je Agent loggen (zusätzlich `ccusage` für Claude-Verbrauch).

---

## Werkzeugkasten (GitHub & Co.)

Diese Bausteine verwenden. Vor dem Einbau jeweils Lizenz, Aktualität und Systemanforderungen prüfen.

| Baustein | Wofür | Hinweis |
|---|---|---|
| [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | Videos als Code (React): wiederverwendbare Stil-Vorlagen, animierte Schrift, Untertitel, Markenfarben | Herzstück für alle Stile. Lizenzbedingungen für Firmen prüfen und Björn sagen, ob er eine Lizenz braucht |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | Offizielle Agent-Skills, damit Claude Code gute Remotion-Videos baut | `npx skills add remotion-dev/skills` im Studio-Ordner |
| [gyoridavid/short-video-maker](https://github.com/gyoridavid/short-video-maker) | Fertige Pipeline (Remotion + Whisper + Pexels + ffmpeg), MIT-Lizenz | Als **Vorlage und Ideenquelle** für Struktur und Untertitel nutzen, nicht 1:1 übernehmen: die eingebaute Stimme (Kokoro) kann nur Englisch, und es braucht ca. 3–4 GB RAM |
| [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) | Website → sauberes Markdown für den Recherche-Agenten | Zuerst einfacher Modus ohne Browser, Browser nur wenn nötig |
| [m-bain/whisperX](https://github.com/m-bain/whisperx) | Wortgenaue Zeitstempel für animierte Untertitel | Nur nötig, wo die Stimme keine Zeitstempel liefert (eigene Clips, Original-Ton). Auf dem kleinen Server: über API oder auf Björns PC |
| [elevenlabs/elevenlabs-mcp](https://github.com/elevenlabs/elevenlabs-mcp) + offizielles ElevenLabs-Python-SDK | Deutsche Sprecherstimme, Soundeffekte | Stimme **mit Zeitstempeln** abrufen, dann entfällt die Transkription |
| fal.ai bzw. Replicate (offizielle Python-Clients) | Bild- und Videogenerierung, Hochskalieren, Hintergrund entfernen, Musik | Community-MCP z. B. [raveenb/fal-mcp-server](https://github.com/raveenb/fal-mcp-server) nur nach Code-Prüfung |
| [Breakthrough/PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | Findet in Björns eigenen Clips die Szenenwechsel und besten Momente | Für Mini-Doku wichtig |
| [WyattBlue/auto-editor](https://github.com/WyattBlue/auto-editor) | Schneidet Stille und tote Stellen aus Rohclips | Für eigenes Material |
| [danielgatis/rembg](https://github.com/danielgatis/rembg) | Produktfotos freistellen (Fashion-Stil) | Läuft lokal, kleines Modell wählen |
| [librosa/librosa](https://github.com/librosa/librosa) | Beats in der Musik finden → Schnitte auf den Takt | Für Fashion und Knete besonders wirksam |
| [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) | Telegram-Bot | |
| [anthropics/skills](https://github.com/anthropics/skills) | Enthält u. a. `skill-creator` zum Bauen und Testen eigener Skills | Für alle eigenen Skills unten |
| [ryoppippi/ccusage](https://github.com/ryoppippi/ccusage) | Zeigt Claude-Code-Verbrauch | Für Kosten-Wächter und Wochenbericht |
| Metricool-API | Liefert Aufrufe, Wiedergabezeit, Speicherungen pro Video | Für die Lernschleife (Phase 7), nur falls Björns Tarif die API enthält |

Suche zusätzlich selbst auf GitHub nach Neuerem (Stichworte: „remotion template reels“, „kinetic typography remotion“, „tiktok captions remotion“, „whiteboard animation python“) und schlage Björn Funde mit kurzer Begründung vor.

## Was die Videos besser macht (Qualitätsregeln)

Diese Regeln gehören als Skills in `.claude/skills/` und als Checkliste in den Prüfer.

1. **Hook-Wettbewerb:** Das Skript erzeugt 5 Hooks, der Prüfer bewertet sie gegen die Bibliothek in `wissen/hooks.md`, der beste gewinnt.
2. **Bewährte Dramaturgie:** Hook (0–2 s) → Problem → Lösung → Beweis (Kundenstimme, Zahl, Vorher/Nachher) → klare Handlungsaufforderung.
3. **Tempo:** Bildwechsel alle 2–3 Sekunden, alle 5–7 Sekunden ein Muster-Unterbrecher (Zoom, Schriftwechsel, Soundeffekt).
4. **Animierte Wort-für-Wort-Untertitel:** aktuelles Wort hervorgehoben, in Markenfarben, Stil passend.
5. **Sichere Zonen:** Kein Text unter den Instagram-/TikTok-Bedienelementen (unten ca. 20 %, rechts ca. 15 %, oben ca. 10 % frei halten).
6. **Ton-Profi-Standard:** Lautheit auf −14 LUFS normalisieren, Musik automatisch leiser unter der Stimme (Ducking), Schnitte auf den Takt.
7. **Bildqualität:** Generierte Bilder bei Bedarf hochskalieren, Produktfotos freistellen, einheitliche Farbstimmung über alle Szenen.
8. **Titelbild:** Eigenes Cover mit großem Text, weil es im Profilraster sichtbar bleibt.
9. **Mehrere Formate auf Wunsch:** 9:16 Standard, 1:1 und 16:9 als Zusatz ohne neue Generierung.
10. **Marke immer erkennbar:** Logo, Farben und Schrift aus dem Firmenprofil in jedem Stil.

## Phase 0 – Verbindung vom PC zum Server

Server: `root@v220260941368451.powersrv.de` (Netcup, Debian 13 minimal)

1. Prüfen, ob `ssh` und `scp` auf dem PC vorhanden sind (Windows-OpenSSH). Falls nicht: Björn erklären, wie er „OpenSSH-Client“ unter Windows-Einstellungen → Optionale Features aktiviert.
2. SSH-Schlüssel ohne Passphrase erzeugen: `%USERPROFILE%\.ssh\video_studio` (ed25519). Vorhandene Schlüssel nicht überschreiben.
3. **Einziger Handgriff für Björn:** Gib ihm genau einen fertigen Befehl, den er in einem eigenen PowerShell-Fenster ausführt. Der Befehl kopiert den öffentlichen Schlüssel auf den Server (`~/.ssh/authorized_keys`), Björn tippt dabei einmal das Root-Passwort. Klappt das Passwort nicht: Björn setzt es im Netcup-Kundenbereich (SCP) neu, dann noch einmal.
4. In `%USERPROFILE%\.ssh\config` den Eintrag `studio-server` anlegen (Host, User root, IdentityFile video_studio). Test: `ssh studio-server "echo ok"`.
5. Diese Datei per `scp` auf den Server kopieren (`/root/video-studio-setup.md`, nach Phase 1 nach `~/video-studio/` des Benutzers `studio`).
6. Ab jetzt führst du alle Phasen per `ssh studio-server "<befehl>"` aus. Lange Befehle (Installationen, Renderings) mit `nohup` bzw. in `tmux` starten und den Fortschritt abfragen, damit nichts an Zeitlimits abbricht. Dateien schreibst du lokal und überträgst sie per `scp`, oder direkt per Heredoc über SSH.
7. Claude Code wird in Phase 1 zusätzlich **auf dem Server** installiert, weil die Produktion dort später ohne PC läuft (`claude -p`). Für den automatischen Betrieb dort einen Anthropic-API-Schlüssel in `.env` verwenden; frag Björn danach, wenn es so weit ist.

Wenn Phase 0 steht: kurz melden, auf „weiter“ warten.

## Phase 1 – Server absichern

- System aktualisieren, Benutzer `studio` mit sudo anlegen
- Den Schlüssel aus Phase 0 auch für `studio` hinterlegen, SSH-Config auf dem PC auf `studio` umstellen; erst wenn das nachweislich funktioniert, Root- und Passwort-Login abschalten
- ufw (nur SSH offen), fail2ban, automatische Sicherheitsupdates
- Installieren: git, ffmpeg, Python 3 + venv, Node.js LTS, Chromium-Abhängigkeiten für Remotion, imagemagick, Schriften (Inter, Montserrat, Playfair Display, eine Handschrift-Schrift)
- Claude Code für `studio` über den offiziellen Installer einrichten
- Tägliches Backup von `firmen/`, `wissen/`, `stile/`, `templates/` und `.claude/` (Ziel mit Björn klären)

## Phase 2 – Struktur

```
~/video-studio/
├── CLAUDE.md
├── .env
├── config/
│   └── modelle.yaml        # welche Modelle für Bild, Video, Stimme, Claude je Agent
├── .claude/
│   ├── agents/             # Agenten (Phase 3)
│   └── skills/             # eigene Skills + remotion-dev/skills
├── stile/                  # Stil-Steckbriefe (siehe unten)
├── templates/              # Remotion-Projekt: eine Vorlage pro Stil + gemeinsame Bausteine
│   ├── gemeinsam/          # Untertitel, Logo-Einblendung, Abspann, Titelbild
│   └── <stil>/
├── firmen/
│   └── herr-bellos-rudel/
│       ├── profil.md
│       ├── logo/
│       ├── farben.json
│       └── material/
├── wissen/
│   ├── hooks.md            # Hook-Bibliothek, wächst mit
│   ├── erfolgsrezepte.md   # was nachweislich funktioniert (aus Phase 7)
│   └── fehler.md           # was schiefging und wie es gelöst wurde
├── evals/
│   ├── briefings/          # 5 feste Test-Briefings
│   └── ergebnisse/         # Bewertungen pro Version
├── musik/                  # lizenzfrei, nach Stimmung und Tempo (BPM) sortiert
├── bot/
├── scripts/
├── produktion/<datum>-<firma>-<kurzname>/
├── archiv/
└── logs/
```

**Eigenes Git-Repo** `video-studio` anlegen (kein Unterordner eines anderen Projekts). `.env`, `produktion/`, `archiv/`, `musik/`, `logs/`, `firmen/*/material/` in `.gitignore`. Zusätzlich als **privates GitHub-Repo** sichern (Björn erstellt dafür einen GitHub-Zugang bzw. Token, wenn die Phase dran ist). Jede Änderung, auch die des `lernen`-Agenten, wird mit kurzer deutscher Beschreibung committet und automatisch gepusht, damit jeder Stand wiederherstellbar ist.

**Modular bauen:** Neuer Stil = Steckbrief in `stile/` + Vorlage in `templates/` + Skill. Neue Firma = Ordner in `firmen/`, wird automatisch angelegt und beim nächsten Auftrag wiedererkannt.

### `CLAUDE.md`

```markdown
# Video-Studio

Produziert Kurzvideos für beliebige Firmen, Produkte und Themen, vollautomatisch. Björn sieht nur Start und Ergebnis.

Ablauf: Vorgabe → Recherche → Firmenprofil → Interview (nur Lücken) → Briefing → Regie → Skript → Art-Direction → Bild/Animation + Ton (parallel) → Schnitt (Remotion) → Prüfung → Versand → Lernen.

Regeln:
- Ein Auftrag = ein Ordner in produktion/. Übergaben nur über Dateien. Jeder Schritt schreibt in status.md.
- Vor jedem Auftrag wissen/erfolgsrezepte.md und wissen/fehler.md lesen.
- Firmenwissen gehört in firmen/<firma>/profil.md.
- Nach dem Interview nie Rückfragen an Björn. Bei Unklarheit Annahme treffen und im Briefing notieren.
- Stil-Steckbrief und Qualitätsregeln sind verbindlich, Markenauftritt der Firma fließt in jeden Stil ein.
- Fremde Bilder nur mit bestätigten Rechten.
- Kosten laufend mitzählen, Limit aus .env einhalten.
```

### Stil-Steckbriefe

Alle Stile übernehmen Farben, Logo und Tonalität aus dem Firmenprofil und nutzen die gemeinsamen Remotion-Bausteine.

**`stile/handgezeichnet.md`** – Erklärvideos, Abläufe
- Schwarze Stiftlinien auf Papier, wenige Akzentfarben aus der Marke
- Bilder im Sketch-Stil generieren, dann „Zeichnen“-Effekt (Linien bauen sich auf), sanfte Übergänge, Hand mit Stift optional
- Ruhige Stimme, leichte Akustik-Musik, Handschrift-Schrift

**`stile/comic.md`** – Kundenproblem → Lösung, kleine Geschichten
- Farbige Panels, klare Outlines, wiederkehrende Figuren aus einem Charakterblatt
- Panels mit leichter Bewegung, Sprechblasen als Remotion-Baustein, Panel-Übergänge
- Lebendige Stimme, verspielte Musik, Soundeffekte

**`stile/fashion.md`** – Produkte, Premium, Markenimage
- Cinematisch, Zeitlupe, gedämpfte Farben, viel Raum, Produkte wie Designerstücke
- Generierte Clips mit Produktfotos als Referenz, freigestellte Produktfotos, Schnitte auf den Takt
- Sehr wenig Text, große Serif-Schrift, Markenname zum Schluss, atmosphärische Musik

**`stile/knete.md`** – sympathische Vorstellung, Aufmerksamkeit im Feed
- 3D-Claymation, Fingerabdrücke sichtbar, Miniatur-Kulissen passend zum Standort, warmes Licht
- Charakterblatt zuerst, Bild-zu-Video, danach auf 12 fps für echten Stop-Motion-Effekt
- Humorvolle Stimme, verspielte Musik, Geräusche

**`stile/mini-doku.md`** – Vertrauen, Dienstleister, Team, Recruiting
- „Ein Tag bei <Firma>“, natürliches Licht, Handkamera-Gefühl, echte Momente
- Zuerst eigenes Material (beste Momente per PySceneDetect, Stille raus per auto-editor), Lücken mit realistischen Clips füllen
- Kernaussagen als große Kinetic Typography in Markenfarben, Schluss mit Kontakt

## Phase 3 – Agenten (`.claude/agents/`)

Jeder Agent hat eine schmale Aufgabe und ein festgelegtes Modell. Übergabe nur über Dateien.

**Verstehen**

| Agent | Aufgabe | Liefert |
|---|---|---|
| `recherche` | Liest Website (Start, Leistungen, Über uns, Kontakt, Impressum) mit crawl4ai aus, sammelt Fakten zu Teil A, Logo, Farben, Schriften, Bilder, Kundenstimmen | `recherche.md`, Rohmaterial |
| `marken-profil` | Legt `profil.md` an oder ergänzt es, ermittelt Farben und Tonalität, markiert Lücken | `profil.md`, `farben.json`, `luecken.json` |
| `interviewer` | Macht aus den Lücken und Teil B höchstens 5 Fragen, fasst alles zum Briefing zusammen | `briefing.json` |

**Planen**

| Agent | Aufgabe | Liefert |
|---|---|---|
| `regie` | Plant das Video anhand von Briefing, Stil und Erfolgsrezepten, verteilt Aufgaben, lässt parallel laufen, wiederholt Fehlschläge | `plan.md`, `status.md` |
| `kosten-waechter` | Schätzt und verbucht Kosten, hält das 5-€-Limit | `kosten.json` |

**Inhalt**

| Agent | Aufgabe | Liefert |
|---|---|---|
| `skript` | 5 Hooks, Sprechertext nach Dramaturgie-Regel, Szenenliste mit Zeiten, Pflichtinhalte, Handlungsaufforderung | `skript.md`, `hooks.md` |
| `art-director` | Bild-Prompts aus Skript, Stil und Marke, Charakterblätter, einheitliche Farbstimmung | `prompts.md`, `charaktere/` |
| `caption` | Plattform-Text, Hashtags nach Branche und Standort, Handlungsaufforderung | `caption.txt` |

**Produktion**

| Agent | Aufgabe | Liefert |
|---|---|---|
| `bild` | Szenenbilder per API, eigenes Material wo erlaubt, Hochskalieren und Freistellen bei Bedarf | `szenen/` |
| `animation` | Bewegung: Bild-zu-Video, Zoom/Pan, Zeichnen-Effekt, Stop-Motion | `clips/` |
| `stimme` | ElevenLabs mit Zeitstempeln, Stimmtyp nach Tonalität | `stimme.mp3`, `woerter.json` |
| `musik-sound` | Musik nach Stimmung und Tempo, Beats erkennen, Soundeffekte | `musik.mp3`, `beats.json`, `sfx/` |
| `schnitt` | Füllt die Remotion-Vorlage des Stils mit allen Teilen, Wort-Untertitel, sichere Zonen, Schnitte auf den Takt, Lautheit −14 LUFS mit Ducking, Logo, Abspann, Titelbild | `video.mp4`, `cover.jpg` |

**Abschluss**

| Agent | Aufgabe | Liefert |
|---|---|---|
| `pruefer` | Bewertet Einzelbilder und Tonspur nach den Qualitätsregeln mit Punktzahl (0–100). Unter 75: zurück an den zuständigen Agenten, höchstens 2 Runden. Prüft Fakten gegen das Profil | `pruefung.md` |
| `versand` | Schickt Video, Titelbild und Caption per Telegram, archiviert, räumt auf | Nachricht an Björn |
| `lernen` | Siehe Phase 7 | `lernlog.md`, Änderungsvorschläge |
| `analyst` | Holt Statistiken der veröffentlichten Videos (Metricool), verbindet sie mit Stil, Hook, Länge, Branche | `wissen/erfolgsrezepte.md` |

Technik als getestete Python- bzw. TypeScript-Skripte in `scripts/` und `templates/`, die Agenten rufen nur auf.

### Eigene Skills (mit `skill-creator` bauen und testen)

- `hook-schreiben` – Hook-Formeln, Bewertungsregeln, Beispiele
- `reel-dramaturgie` – Aufbau, Tempo, Muster-Unterbrecher
- `wort-untertitel` – Remotion-Baustein + Gestaltungsregeln je Stil
- `ton-mischen` – Lautheit, Ducking, Beat-Schnitt
- `marken-anwenden` – Profil → Farben, Schrift, Logo in die Vorlage
- `website-auslesen` – Ablauf und Grenzen für crawl4ai
- `video-pruefen` – Checkliste mit Punktzahl
- je Stil ein Skill, z. B. `stil-knete`, der Prompts, Bewegung und Fallen dieses Stils kennt

## Phase 4 – Telegram-Bot

- Python, systemd-Dienst mit Autostart, reagiert nur auf Björns Chat-ID
- Ablauf: Vorgabe → Recherche startet sofort im Hintergrund → Stil-Knöpfe + „Überrasch mich“ → Interview (nur Lücken) → Zusammenfassung mit „Los“ → Produktion
- Sprachnachrichten transkribieren; geschickte Fotos/Videos landen im Material-Ordner der Firma
- Bekannte Firmen am Namen oder an der Website erkennen
- Startet die Regie headless (`claude -p`)
- Ergebnis: Video, Titelbild, Caption, optional ⭐ 1–5
- Befehle: `/neu`, `/firmen`, `/status`, `/abbrechen`, `/bericht` (Kosten und Erfolge der letzten 7 Tage)
- Warteschlange für mehrere Aufträge

## Phase 5 – Testläufe

- Firmenprofil Herr Bellos Rudel anlegen
- Je Stil ein Testvideo für Herr Bellos Rudel, Björn startet alle fünf selbst
- Ein Testvideo für eine fremde Firma nur über deren Website
- Bericht an Björn: Dauer, Kosten, Prüfer-Punktzahl pro Stil, Serverlast, was nachjustiert wurde

## Phase 6 – Qualitätssicherung (Evals)

- 5 feste Test-Briefings in `evals/briefings/` (verschiedene Branchen und Stile)
- Skript `scripts/eval.py`: produziert alle 5 günstig (Vorschau-Auflösung, Standbilder statt Clips) und lässt den Prüfer Punkte vergeben
- **Jede Änderung an Skills, Steckbriefen oder Vorlagen muss vorher den Eval bestehen** (Punktzahl nicht schlechter als die aktuelle Version), sonst wird sie verworfen
- Ergebnisse je Version in `evals/ergebnisse/`

## Phase 7 – Kontinuierliche Verbesserung

Drei Lernquellen, ausgewertet vom `lernen`-Agenten:

1. **Nach jeder Produktion:** Was musste der Prüfer zurückschicken, wo gab es Fehler, was hat es gekostet → Einträge in `wissen/fehler.md`, Vorschläge für Skills.
2. **Björns Sterne:** Bewertungen mit Stil, Hook und Länge verknüpfen.
3. **Echte Zahlen:** Der `analyst` holt 2 und 7 Tage nach Veröffentlichung Aufrufe, Wiedergabezeit, Speicherungen und Teilen pro Video und schreibt Muster nach `wissen/erfolgsrezepte.md` (z. B. „Bei Dienstleistern funktionieren Frage-Hooks besser als Zahlen-Hooks“).

Einmal pro Woche:
- `lernen` erstellt konkrete Verbesserungen an Skills, Hooks und Steckbriefen
- Jede Verbesserung läuft durch den Eval (Phase 6), nur bestandene werden übernommen und in Git gespeichert
- Wochenbericht an Björn per Telegram: Videos, Kosten, Durchschnittspunktzahl, bestes Video, was verbessert wurde
- Recherche nach neuen Werkzeugen und Trends (GitHub, Remotion-Neuerungen, neue Bild-/Videomodelle) mit Vorschlag an Björn, nichts ohne seine Freigabe installieren

## Phase 8 – Feinschliff

- Logs nach 30 Tagen, Produktionsordner nach 14 Tagen aufräumen (fertige Videos vorher ins Archiv)
- `ANLEITUNG.md`: neuen Stil hinzufügen, Firmenprofil bearbeiten, Eval starten
- Optional: Björns PC mit Grafikkarte als Rechenhelfer anbinden (Untertitel, Freistellen, Bilder), falls Björn das möchte

---

## Was Björn bereitstellen muss (erst abfragen, wenn die Phase dran ist)

- [ ] Einmal das Root-Passwort des Servers (Phase 0)
- [ ] Anthropic-Zugang für Claude Code auf dem Server
- [ ] Telegram-Bot-Token (über @BotFather) und seine Chat-ID
- [ ] fal.ai- oder Replicate-Zugang (nach deinem Vorschlag)
- [ ] ElevenLabs-API-Schlüssel
- [ ] Pixabay-API-Schlüssel (kostenlos, für Stockfotos und -videos; Pexels vergibt derzeit keine neuen Schlüssel). Stock-Anbieter in `config/modelle.yaml` austauschbar halten, damit Pexels später ergänzt werden kann
- [ ] Metricool-API-Zugang (Phase 7, falls im Tarif)
- [ ] Für Herr Bellos Rudel: Website, Logo, Markenfarben, Produktfotos der Fettleder-Serie, eigene Hundefotos und -clips
- [ ] 3–5 Beispielvideos, die ihm richtig gut gefallen (als Qualitätsmaßstab für Prüfer und Evals)
- [ ] GitHub-Zugang für das private Repo `video-studio`

Beginne jetzt mit Phase 0.
