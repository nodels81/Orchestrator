# Architektur, Paketschnitt, Dateihoheit

## Paketbaum (Ausgangsform, ein Modul)

```
com.bellowerk.<app>/
  MainActivity.kt              Einstieg, setContent { AppTheme { AppNavHost() } }
  di/                          Hilt-Module (Bindings, Provider)
  data/
    local/                     Room: Entity, Dao, Database, Converters
    remote/                    Retrofit/Ktor: Api-Interface, DTOs
    repository/                Repository-Implementierungen, Mapping DTO/Entity → Domain
  domain/
    model/                     reine Kotlin-Datenklassen, kein Android-Import
    usecase/                   nur wenn Logik über ein Repository hinausgeht
  ui/
    theme/                     Color, Type, Shape, AppTheme
    navigation/                NavHost, Routen als typisierte Objekte
    <feature>/                 <Feature>Screen.kt, <Feature>ViewModel.kt, <Feature>UiState.kt
    common/                    wiederverwendete Composables (LoadingState, ErrorState, EmptyState)
```

Erst aufteilen (Multi-Module), wenn der Build spürbar langsam wird oder zwei Teams parallel
arbeiten — nicht vorsorglich.

## Datenfluss

- `UiState` ist **eine** unveränderliche Datenklasse je Bildschirm, mit `isLoading`, `error`,
  `data` — keine losen `MutableState`-Felder über den Screen verstreut.
- ViewModel legt `val uiState: StateFlow<UiState>` offen, erzeugt mit
  `stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), UiState())`.
- Composables bekommen `uiState` und Lambdas (`onSave: (String) -> Unit`) — nie das ViewModel selbst
  in tiefere Composables durchreichen.
- Repository liefert `Flow<T>` aus Room, Netzfehler kommen als `Result`/`sealed class`, nicht als
  geworfene Exception durch die UI.
- `domain/model` importiert nichts aus `android.*` — das macht es JVM-testbar.

## Namensregeln

| Sache | Muster | Beispiel |
|---|---|---|
| Bildschirm | `<Feature>Screen` | `TourListScreen` |
| ViewModel | `<Feature>ViewModel` | `TourListViewModel` |
| Zustand | `<Feature>UiState` | `TourListUiState` |
| Room-Entity | `<Name>Entity` | `TourEntity` |
| DTO | `<Name>Dto` | `TourDto` |
| Testklasse | `<Klasse>Test` | `TourRepositoryTest` |

## Dateihoheit im Team (verhindert kaputte Builds)

Arbeiten mehrere Agenten am selben Projekt, gehört jede Datei genau einem:

| Agent | Schreibt in | Fasst nie an |
|---|---|---|
| `android-architekt` | `docs/`, `README.md` | `app/src/**` |
| `android-entwickler` | `app/src/main/**` außer `ui/theme/` | `src/test/**`, `src/androidTest/**` |
| `android-ui` | `app/src/main/**/ui/theme/**`, `ui/common/**` | Repository-, Daten- und DI-Schicht |
| `android-tester` | `app/src/test/**`, `app/src/androidTest/**` | `app/src/main/**` |
| `android-release` | `app/build.gradle.kts` (Release-Block), `proguard-rules.pro`, `docs/store/` | Feature-Code |

**Nie zwei schreibende Agenten gleichzeitig in derselben Datei oder demselben Gradle-Modul.**
Lesende Agenten dürfen jederzeit parallel laufen. Muss ein Agent außerhalb seiner Hoheit ändern,
schreibt er den Vorschlag in den Bericht, statt selbst zu greifen.
