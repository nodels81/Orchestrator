# UI-Standard: Material 3, Zustände, Barrierefreiheit

## Theme

- Ein `AppTheme` in `ui/theme/`, das `MaterialTheme` mit eigenem `ColorScheme` versorgt.
  Helles **und** dunkles Schema von Anfang an, `dynamicColor` optional und abschaltbar.
- Farben, Abstände und Formen nur aus dem Theme (`MaterialTheme.colorScheme.primary`), nie als
  fest verdrahtete `Color(0xFF…)` im Bildschirm.
- Abstände in Vielfachen von 4 dp; 8/16 dp sind die Regelfälle.
- Für Bellowerk-Apps: warme Lederfarben, Messington als Akzent, keine grellen Vollflächen.

## Jeder Bildschirm hat vier Zustände

1. **Laden** — Platzhalter oder Indikator, nie leere weiße Fläche.
2. **Leer** — Satz, der sagt was fehlt, plus die Handlung, die hilft („Erste Runde aufzeichnen").
3. **Fehler** — verständlicher Satz ohne Stacktrace, plus Knopf „Erneut versuchen".
4. **Inhalt** — der Normalfall.

Gemeinsame Composables dafür in `ui/common/`, nicht je Bildschirm neu.

## Barrierefreiheit (Prüfliste vor jeder Fertigmeldung)

- `contentDescription` an jedem bedeutungstragenden Bild/Icon; rein dekorative bekommen `null`.
- Tippflächen mindestens 48 dp × 48 dp (`Modifier.minimumInteractiveComponentSize()`).
- Text in `sp`, keine festen Höhen um Text — bei 200 % Schriftgröße darf nichts abgeschnitten sein.
- Kontrast mindestens 4,5:1 für Fließtext.
- Bedienbar per TalkBack: Reihenfolge sinnvoll, Zustände angesagt (`Modifier.semantics`).

## Größen und Drehung

- Ab 360 dp Breite muss alles nutzbar sein; ab 600 dp darf, muss aber nicht, umgebrochen werden.
- Querformat und Drehung ohne Zustandsverlust — `rememberSaveable` für alles, was der Nutzer
  eingegeben hat.
- Lange Texte und lange Listen mit echten Beispieldaten in der Preview prüfen, nicht mit „Test".

## Previews

Jeder Bildschirm bekommt `@Preview` für hell und dunkel:

```kotlin
@Preview(name = "Hell", showBackground = true)
@Preview(name = "Dunkel", uiMode = UI_MODE_NIGHT_YES, showBackground = true)
@Composable
private fun TourListScreenPreview() { AppTheme { TourListScreen(uiState = demoState, onSelect = {}) } }
```

Previews arbeiten mit einem festen `UiState`, nie mit einem echten ViewModel.
