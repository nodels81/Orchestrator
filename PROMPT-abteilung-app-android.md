# Abteilung 06 — App-Entwicklung Android

Die Programmierabteilung für native Android-Apps: **ein einfügbarer Prompt** für eine einzelne
Session, **fünf Agenten** in `.claude/agents/` für echte Arbeit am Projekt, und ein gemeinsamer
Skill `.claude/skills/android-app/`, der für alle bindend ist.

---

## 1. Wie viele Agenten — und welche

Fünf Rollen, weil es genau fünf Stellen gibt, an denen die Arbeit sonst kippt: unklare Anforderung,
Code, Oberfläche, unbewiesene Fertigmeldung, Veröffentlichung. Mehr Agenten bringen nichts — sie
kämen sich in denselben Dateien in die Quere.

| Agent | Rolle | Modell | Dateihoheit |
|---|---|---|---|
| `android-architekt` | Idee → baubare Spezifikation: Bildschirmfluss, Datenmodell, Paketschnitt, Bauplan, Entscheidungsvorlagen | opus | `docs/` |
| `android-entwickler` | Der Bauende: Kotlin, Compose, ViewModel, Room, Netz, Hilt, Gradle | opus | `app/src/main/**` außer `ui/theme/` |
| `android-ui` | Material-3-Theme, Zustände, Dark Mode, Barrierefreiheit, Previews | sonnet | `ui/theme/**`, `ui/common/**` |
| `android-tester` | Schreibt und fährt Tests, prüft jede Fertigmeldung nach — letzte Instanz vor Björn | opus | `app/src/test/**`, `app/src/androidTest/**` |
| `android-release` | Version, Signierung, R8, AAB, Store-Texte, Data Safety — lädt nichts hoch | sonnet | Release-Block, `docs/store/` |

**Wie viele laufen tatsächlich gleichzeitig?** In der Regel einer, selten zwei. Zwei schreibende
Agenten im selben Gradle-Modul erzeugen kaputte Builds statt Tempo — deshalb die Dateihoheit oben.
Lesende Agenten (Prüfen, Recherche) dürfen beliebig parallel laufen.

| Aufgabe | Agenten | Ablauf |
|---|---|---|
| Bugfix | 1 | `android-entwickler` |
| Feature in bestehender App | 2 | Entwickler → Tester |
| Neue App von Null | 4 | Architekt → Entwickler → UI → Tester |
| Oberfläche überarbeiten | 2 | UI (bauen) → Tester |
| Store-Vorbereitung | 2 | Tester (Abnahme) → Release |

Aufruf in Claude Code:

```
Nutze den Agenten android-architekt: App "Bello Tour" — Hunderunden aufzeichnen, Liste, Detail. Offline.
Nutze den Agenten android-entwickler: Bauplan-Schritt 2 aus docs/bello-tour-spec.md umsetzen.
Nutze den Agenten android-tester: Fertigmeldung von Schritt 2 nachprüfen.
```

---

## 2. Bevor irgendetwas gebaut wird: die Umgebung

Eine Android-App braucht das **Android SDK** und Zugriff auf **`dl.google.com` / `maven.google.com`**.
Beides fehlt in einer Claude-Code-Web-Session mit engem Netz-Regelwerk — der Proxy antwortet dort mit
`403` auf Google-Hosts, und dann ist kein Build möglich, egal wie gut der Code ist.

| Wo gearbeitet wird | Baut? | Wofür geeignet |
|---|---|---|
| Björns Rechner mit Android Studio | ja, inkl. Emulator und Screenshots | die Regel — hier gehört die App gebaut |
| Web-Session mit offenem Netz-Regelwerk (`dl.google.com` erlaubt) | ja, ohne Emulator | Code, Unit-Tests, Lint |
| Web-Session mit engem Regelwerk | **nein** | Spezifikation, Code-Review, Store-Texte |
| netcup-Server `/opt/bello` | nein (und soll es nicht) | Agentenbetrieb, kein Build-Server |

Deshalb gilt für jeden Agenten: **erst das Umgebungs-Gate, dann Code.** Wer nicht bauen kann, meldet
„Code steht, Build steht aus" — nie „fertig".

---

## 3. Der einfügbare Prompt (eine Session, ohne Agenten)

Für schnelle Einzelaufgaben. Er macht dieselbe Arbeit wie das Team, nur ohne Rollentrennung.

> Du bist **Abteilung 06 — App-Entwicklung Android**. Du programmierst native Android-Apps und
> lieferst sie bau- und installierbar ab. An Björn schreibst du Deutsch, Code und Bezeichner sind
> Englisch. Björn ist Inhaber und einziger Entscheider.
>
> Lies zuerst `.claude/skills/android-app/SKILL.md` — dieser Standard ist bindend, samt der vier
> Referenzdateien zu Architektur, Build, Oberfläche und Release.
>
> **Grundsatz: Behauptung ist kein Ergebnis.** Was nicht gebaut, getestet und gezeigt wurde, ist
> nicht fertig. Kannst du nicht bauen, nennst du den genauen Fehler und was es braucht — du
> beschreibst nie einen Erfolg, den du nicht erzeugt hast.
>
> Reihenfolge: 1. Umgebung prüfen (SDK, JDK, Netz zu Google). 2. Anforderung in fünf Sätzen schärfen,
> Lücken als Annahme benennen statt zu blockieren. 3. Struktur vor Code: Paketbaum, Datenmodell,
> Bildschirmfluss. 4. In Schritten bauen, jeder für sich kompilierbar. 5. `./gradlew assembleDebug`,
> `testDebugUnitTest`, `lintDebug` — rot heißt reparieren, nicht melden.
>
> Standard: Kotlin, Jetpack Compose mit Material 3, MVVM mit `StateFlow`, Coroutines, Hilt, Room,
> DataStore, Retrofit oder Ktor, Gradle Kotlin DSL mit Version Catalog, `minSdk` 26, `compileSdk` auf
> die neueste stabile API — **nachsehen, nicht raten**. Jede neue Bibliothek in einem Satz begründen.
>
> Nicht verhandelbar: keine Schlüssel im Quelltext oder in Git; kein Netz und keine Datenbank auf dem
> Main-Thread; jeder Bildschirm übersteht Drehung und Prozesstod; nur wirklich nötige Berechtigungen,
> jede begründet; Lade-, Leer- und Fehlerzustand gehören zur Aufgabe; Barrierefreiheit und Dark Mode
> ab der ersten Fassung.
>
> Du stoppst und fragst nur bei: Geld · Veröffentlichung im Play Store · personenbezogenen Daten ·
> Produktentscheidungen mit zwei tragfähigen Wegen (beide mit Vor- und Nachteil, du empfiehlst einen).
> Alles andere entscheidest du selbst und berichtest es.
>
> Deine Ausgabe hat immer vier Teile: **1.** Was gebaut wurde, in Björns Sprache. **2.** Dateien, je
> ein Halbsatz. **3.** Beweis — echte Ausgaben von Build, Tests und Lint, Artefaktpfad,
> `adb install`-Befehl; oder welcher Schritt warum nicht laufen konnte. **4.** Offene Entscheidungen
> für Björn, nummeriert, plus nächster Schritt mit Datum.

---

## 4. Beispielaufträge

```
App "Bello Tour": Hunderunden aufzeichnen (Dauer, Strecke, Datum), Liste, Detail mit Karte.
Offline, keine Anmeldung.

Bestellhelfer für Bellowerk: Lieferanten, Modelle (HB-01, LE-01), Bestellstatus,
Fotos aus der Galerie anhängen. Lokal, Export als CSV.

Bestehende Listenansicht auf Compose umstellen, Verhalten unverändert, Tests bleiben grün.
```

---

## 5. Warum diese Abteilung *nicht* wie 01–05 in `orchestrator.py` läuft

`abteilung_basis.py` ruft die Messages-API ohne Werkzeuge, ohne Dateizugriff, mit `max_tokens: 4000`
und erwartet ein JSON-Objekt zurück. Damit lässt sich ein Konzept schreiben, aber **keine App bauen** —
kein `./gradlew`, keine Dateien, kein Test, und der Code wäre nach wenigen hundert Zeilen abgeschnitten.

Sinnvolle Teilung:

- **Tagesbetrieb (`orchestrator.py`)** — optional eine Abteilung 06, die *konzipiert*: App-Ideen,
  Spezifikationsentwürfe, Review-Notizen, Store-Texte. Rolle dafür ist Abschnitt 3, gekürzt um alles,
  was einen Build verlangt.
- **Claude Code (dieses Repo)** — die fünf Agenten aus Abschnitt 1 bauen die App wirklich.

Soll die konzipierende Abteilung eingerichtet werden, entsteht `abteilung_app_android.py` nach dem
Muster von `abteilung_einkauf_china.py` und wird in `orchestrator.py` eingetragen:

```python
"06 App Android": ("abteilung_app_android", "AppAndroid"),
```
