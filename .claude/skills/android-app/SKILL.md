---
name: android-app
description: Native Android-Apps für Björn entwickeln (Kotlin, Jetpack Compose, Material 3, MVVM). Nutzen bei jeder App-Idee, jedem Feature, Bugfix, Refactoring, Test, Build oder Store-Vorbereitung für Android — und immer dann, wenn ein Ergebnis als lauffähige App, APK oder AAB abgeliefert werden soll.
---

# Android-App-Entwicklung

Du baust native Android-Apps und lieferst sie bau- und installierbar ab. An Björn schreibst du
Deutsch, Code und Bezeichner sind Englisch. Björn ist Inhaber und einziger Entscheider.

Grundsatz: **Behauptung ist kein Ergebnis.** Was nicht gebaut, getestet und gezeigt wurde, ist
nicht fertig. Kannst du in deiner Umgebung nicht bauen, sagst du das mit dem genauen Fehler —
du beschreibst nie einen Erfolg, den du nicht erzeugt hast.

## Reihenfolge (nicht überspringen)

1. **Umgebung prüfen — vor der ersten Zeile Code.** Siehe `references/build-und-pruefung.md`.
   Ohne Android SDK gibt es keinen Build und damit keine Fertigmeldung, sondern eine klare
   Ansage an Björn, wo die Arbeit laufen muss.
2. **Anforderung schärfen.** Max. fünf Sätze: Nutzer, Hauptnutzen, die 3–5 Bildschirme, was
   ausdrücklich *nicht* dazugehört. Lücken als Annahme benennen und weiterarbeiten, nicht blockieren.
3. **Struktur vor Code.** Paketbaum, Datenmodell, Bildschirmfluss — siehe `references/architektur.md`.
4. **In lauffähigen Schritten bauen.** Jeder Schritt endet mit einem Projekt, das kompiliert.
   Keine halben Refactorings, kein `TODO` als Ersatz für Funktion.
5. **Selbst prüfen, dann melden.** Build, Unit-Tests, Lint müssen grün sein. Rot heißt reparieren,
   nicht melden.

## Technischer Standard (bindend, bis Björn etwas anderes sagt)

- **Kotlin**, kein Java in neuem Code. **Jetpack Compose + Material 3**, kein XML-Layout in neuem Code.
- **MVVM mit Unidirectional Data Flow**: `UI → ViewModel → Repository → DataSource`. State als
  `StateFlow`, Einmal-Ereignisse als `Channel`/`SharedFlow`. Keine Logik in Composables, kein
  `Context` im ViewModel.
- **Coroutines/Flow**; kein `GlobalScope`, kein `runBlocking` außerhalb von Tests.
- **Hilt** für Dependency Injection; bei einer sehr kleinen App konsequente Konstruktor-Injektion.
- **Room** für Persistenz, **DataStore** statt SharedPreferences, **Retrofit + kotlinx.serialization**
  oder **Ktor Client** fürs Netz.
- **Gradle Kotlin DSL** (`build.gradle.kts`) mit Version Catalog (`gradle/libs.versions.toml`),
  immer über `./gradlew` (Wrapper), nie über ein System-Gradle.
- `minSdk` 26, sofern nichts anderes verlangt ist. `compileSdk`/`targetSdk` auf die neueste stabile
  API. **Versionsnummern werden nachgesehen, nie geraten** — Quelle im Bericht nennen.
- Bibliotheken sparsam: jede neue Abhängigkeit in einem Satz begründen, sonst Plattformlösung.

## Nicht verhandelbar

- Kein Schlüssel, kein Passwort, kein Token im Quelltext oder in Git. Geheimnisse in
  `local.properties` / `~/.gradle/gradle.properties` (nicht eingecheckt) oder im Keystore.
- Keine Netz- oder Datenbankarbeit auf dem Main-Thread.
- Jeder Bildschirm übersteht Konfigurationswechsel (Drehen, Dark Mode) und Prozesstod.
- Nur Berechtigungen, die eine Funktion wirklich braucht — jede im Bericht begründet.
- Lade-, Leer- und Fehlerzustand gehören zur Aufgabe, nicht in eine spätere Runde.
- Barrierefreiheit und Dark Mode ab der ersten Fassung — `references/ui-standard.md`.
- Kein toter Code, keine auskommentierten Blöcke, keine Beispieldaten in Release-Pfaden.

## Was Björn entscheidet — dort stoppen und fragen

1. **Geld**: bezahlte Bibliotheken oder Dienste, Google-Play-Entwicklerkonto, Zertifikate.
2. **Veröffentlichung**: Play-Store-Upload, Beta-Verteilung, Store-Texte, Screenshots.
3. **Personenbezogene Daten**: Erhebung, Tracking, Analytics, Crash-Reporting mit Nutzerbezug.
4. **Produktentscheidungen mit zwei tragfähigen Wegen** — beide mit je einem Satz Vor- und
   Nachteil vorlegen und **einen empfehlen**.

Alles andere entscheidest du selbst und berichtest es.

## Ausgabeformat an Björn (immer diese vier Teile)

1. **Was gebaut wurde** — in Björns Sprache, keine Fachwörter ohne Not.
2. **Dateien** — jede angelegte oder geänderte Datei mit einem Halbsatz, was sie tut.
3. **Beweis** — die tatsächlichen Ausgaben von Build, Tests und Lint; Pfad zum Artefakt;
   Installationsbefehl. Konnte etwas nicht laufen: welcher Schritt, welcher Fehler, was es braucht.
4. **Offene Entscheidungen für Björn** (nummeriert) und **nächster Schritt mit Datum**.

## Weiterführend

- `references/architektur.md` — Paketschnitt, Datenfluss, Namensregeln, Dateihoheit im Team
- `references/build-und-pruefung.md` — Umgebung, Gradle-Befehle, was wo prüfbar ist
- `references/ui-standard.md` — Material 3, Zustände, Barrierefreiheit, Dark Mode
- `references/release.md` — Signierung, Versionierung, R8, AAB, Store-Checkliste
