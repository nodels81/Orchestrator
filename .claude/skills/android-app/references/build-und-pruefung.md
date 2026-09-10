# Umgebung, Build, Prüfung — was wo möglich ist

## Umgebungs-Gate (Schritt 1 jeder Aufgabe)

```bash
java -version                       # AGP 8.x braucht JDK 17+, JDK 21 ist gut
echo "${ANDROID_HOME:-${ANDROID_SDK_ROOT:-<leer>}}"
ls "$ANDROID_HOME/platforms" 2>/dev/null
command -v adb sdkmanager
./gradlew --version 2>/dev/null || echo "kein Wrapper im Projekt"
```

Ergebnis bestimmt, was du versprechen darfst:

| Lage | Was möglich ist | Was du meldest |
|---|---|---|
| SDK da, Netz zu Google offen | Voller Build, Unit-Tests, Lint, APK | Normale Fertigmeldung mit Beweis |
| SDK da, kein Emulator | Alles außer instrumentierten Tests und Screenshots | „Instrumentiert nicht geprüft, Grund: kein Gerät" |
| Kein SDK oder `dl.google.com` gesperrt | **Kein Build.** Nur Code, Spezifikation, Review | Klare Ansage: Code steht, Build steht aus, hier ist der Befehl für Björn |

Die Sperre erkennst du an `CONNECT tunnel failed, response 403` oder
`Could not resolve androidx…` — das ist eine Regelwerk-Entscheidung, **kein Netzfehler zum
Wiederholen**. Prüfen mit `curl -sS "$HTTPS_PROXY/__agentproxy/status"`. Ausweg für Björn: die App
lokal in Android Studio bauen, oder die Umgebung mit einem Netz-Regelwerk anlegen, das
`dl.google.com` und `maven.google.com` erlaubt (Doku: code.claude.com/docs/en/claude-code-on-the-web).
Nie TLS-Prüfung abschalten, nie `HTTPS_PROXY` löschen.

## Pflichtlauf vor jeder Fertigmeldung

```bash
./gradlew assembleDebug         # kompiliert und baut das APK  (kein --offline beim ersten Lauf)
./gradlew testDebugUnitTest     # JVM-Tests, inkl. Robolectric
./gradlew lintDebug             # Android Lint
```

Danach, wenn im Projekt eingerichtet: `./gradlew ktlintCheck` oder `./gradlew detekt`.

Artefakt und Installation:

```
app/build/outputs/apk/debug/app-debug.apk
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

## Testarten — was wirklich läuft

| Art | Befehl | Braucht | Wofür |
|---|---|---|---|
| Unit (reines Kotlin) | `testDebugUnitTest` | nichts | Repository, Mapping, `domain/` |
| Flow/State | `testDebugUnitTest` + Turbine | nichts | ViewModel-Zustandsfolgen |
| Robolectric | `testDebugUnitTest` | nichts | Android-Klassen und Compose auf der JVM |
| Compose-UI instrumentiert | `connectedDebugAndroidTest` | Emulator/Gerät | echtes Rendern, Gesten |
| Screenshot | `adb exec-out screencap -p > bild.png` | Emulator/Gerät | Sichtprüfung |

Compose-Tests laufen bevorzugt über Robolectric auf der JVM, damit sie ohne Emulator prüfbar sind.
Instrumentierte Tests schreibst du trotzdem, wenn eine Geste oder ein Systemdialog geprüft werden
muss — aber du behauptest nie, sie seien gelaufen, wenn kein Gerät da war.

## Erste Einrichtung eines Projekts

Version Catalog anlegen (`gradle/libs.versions.toml`), AGP/Kotlin/Compose-Versionen **aus der
Google-Maven-Übersicht oder einem frisch von Android Studio erzeugten Projekt übernehmen** —
nicht aus dem Gedächtnis. Wrapper mitliefern (`gradlew`, `gradlew.bat`,
`gradle/wrapper/gradle-wrapper.properties` mit fester Distribution). `local.properties` enthält nur
`sdk.dir` und gehört in `.gitignore`.

## Git

Pro Aufgabe ein Branch, kleine Commits mit Zweck in der ersten Zeile. Vor dem Commit:
`git status` darf keine Geheimnisse zeigen, `grep -rn "sk-\|BEGIN PRIVATE KEY\|keystore.password" --include=*.kt --include=*.kts .`
muss leer sein. Keystore-Dateien werden nie eingecheckt.
