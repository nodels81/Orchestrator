# Release: Signierung, Versionierung, Store

Nichts in dieser Datei wird ohne Björns ausdrückliche Freigabe ausgeführt. Du bereitest vor,
er entscheidet und veröffentlicht.

## Versionierung

- `versionCode`: ganze Zahl, bei jedem Release +1, nie rückwärts.
- `versionName`: `MAJOR.MINOR.PATCH` (`1.2.0`), im Version Catalog oder in `gradle.properties`
  an genau einer Stelle gepflegt.
- Jeder Release bekommt einen Git-Tag `v1.2.0` und einen Absatz in `docs/CHANGELOG.md` in Björns
  Sprache — was der Nutzer merkt, nicht was im Code passiert ist.

## Signierung

- Keystore liegt **außerhalb des Repos**, Pfad und Passwörter in `~/.gradle/gradle.properties`.
  Der `signingConfig` liest sie über `providers.gradleProperty(...)`, mit klarer Fehlermeldung,
  wenn sie fehlen.
- Keystore und Passwörter erzeugt und verwahrt Björn. Geht der Keystore verloren, ist eine
  Aktualisierung der Store-App unmöglich — deshalb im Bericht immer an die Sicherung erinnern.
- Play App Signing empfehlen: Björn behält den Upload-Key, Google den Verteilschlüssel.

## Release-Build

```bash
./gradlew bundleRelease          # AAB für den Play Store
./gradlew assembleRelease        # APK für Direktverteilung
```

- `isMinifyEnabled = true` und `isShrinkResources = true` im Release-Block.
- R8 bricht gern Reflexion: nach jedem Regelwechsel den Release-Build **installieren und
  durchklicken**, nicht nur bauen. Nötige `-keep`-Regeln in `proguard-rules.pro` mit Kommentar,
  warum sie nötig sind.
- `debuggable false`, kein Logging von Nutzerdaten, keine Testendpunkte im Release.

## Store-Vorbereitung (Entwurf für Björn, kein Upload)

- Titel (max. 30 Zeichen), Kurzbeschreibung (max. 80), Beschreibung (max. 4000).
- Grafik: App-Symbol 512×512, Feature-Grafik 1024×500, mindestens zwei Screenshots je Formfaktor.
- **Data Safety**: Welche Daten erhoben, wofür, ob geteilt, ob löschbar — muss zur App passen,
  sonst Ablehnung. Erhebt die App nichts, wird das ausdrücklich so erklärt.
- Datenschutzerklärung nötig, sobald Daten erhoben werden — Entwurf liefern, URL besorgt Björn.
- Zielgruppe/Inhaltseinstufung, Berechtigungsbegründungen für alles Heikle.

Ablage: `docs/store/` — Texte als Markdown, Grafikliste mit Soll-Maßen und Status.
