---
version: alpha
name: Bellowerk-Manufaktur
description: >-
  Dunkle Bühne für Fettleder und Messing. Warmes Fast-Schwarz, cremefarbene gesperrte Versalien
  (Jost, nie fett), Lora für alles, was man liest, echte Fotos als einzige Farbfläche. Messing ist der
  einzige Akzent und gehört nur der Hauptaktion, dem Fokus und den zwei Schrauben der Patch-Plakette.
  Waldgrün trägt die Markenbänder und den Fuß. Kaufargument ist der Praxistest — jedes Modell hängt
  eine Saison an fremden Hunden —, nicht das Material.

colors:
  canvas: "#13110E"            # Nacht — Standardgrund jeder Seite und jeder Instagram-Kachel
  surface: "#1C1915"           # Nacht 2 — selten: Warenkorb-Leiste, geöffnete Auswahl
  band: "#23352A"              # Waldgrün — Praxistest-/Manufaktur-Band und Fuß, nur als Fläche
  paper: "#F2EDE4"             # Papier — nur Maßtabelle, Kasse, Rechtstexte, Druck
  ink: "#EEE7DA"               # Talg — Überschriften, Navigation, Haupttext auf Nacht und Waldgrün
  body: "#CBC2B2"              # Fließtext auf Nacht und Waldgrün
  muted: "#948B7D"             # Metadaten — nur auf Nacht (auf Waldgrün zu schwach)
  hairline: "#2E2A24"          # Trennlinie, rein gliedernd
  hairline-on-band: "#3B4E41"  # Trennlinie auf Waldgrün (die Nacht-Linie ist dort unsichtbar)
  edge: "#6B6255"              # Kante von Eingabefeldern und Farbfeld-Ringen (≥ 3:1 auf Nacht)
  accent: "#B08D57"            # Messing — Hauptaktion, Fokus, Patch-Schrauben
  accent-pressed: "#C9A76B"    # Messing poliert — gedrückter Zustand
  on-accent: "#13110E"         # Schrift auf Messing — immer Nacht, nie Talg (2,5:1)
  ink-on-paper: "#1B1814"      # Tinte
  body-on-paper: "#3A342C"
  muted-on-paper: "#5E574C"
  hairline-on-paper: "#D9D1C3"
  error: "#D9674E"
  error-on-paper: "#9E3B28"
  success: "#8DB07A"
  success-on-paper: "#3F6B35"
  leather-grau: "#7B828A"        # Richtwert, siehe "Offene Punkte"
  leather-dunkelbraun: "#4A322B" # Richtwert
  leather-oliv: "#575541"        # Richtwert
  leather-cognac: "#C07848"      # Richtwert
  leather-schwarz: "#1C1A18"     # Richtwert

typography:
  display-xl:
    fontFamily: "Jost, 'Futura PT', Futura, 'Century Gothic', sans-serif"
    fontSize: 56px
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: 0.12em
    textTransform: uppercase
  display-lg:
    fontFamily: "Jost, 'Futura PT', Futura, sans-serif"
    fontSize: 40px
    fontWeight: 400
    lineHeight: 1.15
    letterSpacing: 0.14em
    textTransform: uppercase
  display-md:
    fontFamily: "Jost, 'Futura PT', Futura, sans-serif"
    fontSize: 28px
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: 0.16em
    textTransform: uppercase
  display-sm:
    fontFamily: "Jost, 'Futura PT', Futura, sans-serif"
    fontSize: 20px
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: 0.18em
    textTransform: uppercase
  wordmark:
    fontFamily: "Jost, 'Futura PT', Futura, sans-serif"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1
    letterSpacing: 0.36em
    textTransform: uppercase
  label:
    fontFamily: "Jost, 'Futura PT', Futura, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0.24em
    textTransform: uppercase
  nav:
    fontFamily: "Jost, 'Futura PT', Futura, sans-serif"
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0.24em
    textTransform: uppercase
  button:
    fontFamily: "Jost, 'Futura PT', Futura, sans-serif"
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.22em
    textTransform: uppercase
  measure:
    fontFamily: "Jost, 'Futura PT', Futura, sans-serif"
    fontSize: 28px
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: 0.04em
    fontVariantNumeric: tabular-nums
  price:
    fontFamily: "Jost, 'Futura PT', Futura, sans-serif"
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: 0.06em
    fontVariantNumeric: tabular-nums
  name-engraving:
    fontFamily: "Lora, Georgia, serif"
    fontSize: 22px
    fontWeight: 400
    lineHeight: 1.2
    letterSpacing: 0.2em
    textTransform: uppercase
  lead:
    fontFamily: "Lora, Georgia, serif"
    fontSize: 20px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0
  body:
    fontFamily: "Lora, Georgia, serif"
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: 0
  body-sm:
    fontFamily: "Lora, Georgia, serif"
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0
  quote:
    fontFamily: "Lora, Georgia, serif"
    fontSize: 22px
    fontStyle: italic
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0

rounded:
  none: 0px
  patch: 6px
  pill: 9999px
  full: 50%

spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 64px
  section: 120px
  section-mobile: 72px
  gutter: 24px
  gutter-desktop: 40px

motion:
  feedback: 120ms
  state: 240ms
  reveal: 480ms
  ease-out: "cubic-bezier(0.0, 0.0, 0.2, 1)"
  ease-weighted: "cubic-bezier(0.625, 0.05, 0, 1)"

components:
  top-nav:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.nav}"
    height: 64px
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.on-accent}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: 16px 32px
    height: 48px
  button-primary-pressed:
    backgroundColor: "{colors.accent-pressed}"
    textColor: "{colors.on-accent}"
    rounded: "{rounded.pill}"
  button-secondary:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    borderColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: 15px 31px
    height: 48px
  button-primary-on-paper:
    backgroundColor: "{colors.ink-on-paper}"
    textColor: "{colors.paper}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: 16px 32px
    height: 48px
  text-link:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    typography: "{typography.body}"
  hero-photo:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-xl}"
    padding: 0
  text-input:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    borderColor: "{colors.edge}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: 12px 0
    height: 48px
  product-tile:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    typography: "{typography.display-sm}"
    rounded: "{rounded.none}"
    padding: 0
  leather-swatch:
    size: 24px
    rounded: "{rounded.full}"
    borderColor: "{colors.edge}"
  leather-swatch-selected:
    size: 24px
    rounded: "{rounded.full}"
    borderColor: "{colors.ink}"
  patch-plakette:
    backgroundColor: transparent
    textColor: "{colors.ink}"
    borderColor: "{colors.body}"
    screwColor: "{colors.accent}"
    typography: "{typography.label}"
    rounded: "{rounded.patch}"
    padding: 12px 40px
  saison-logbuch:
    backgroundColor: "{colors.band}"
    textColor: "{colors.ink}"
    valueTypography: "{typography.measure}"
    labelTypography: "{typography.label}"
    padding: 24px 0
  band-praxistest:
    backgroundColor: "{colors.band}"
    textColor: "{colors.ink}"
    typography: "{typography.display-lg}"
    padding: 120px 0
  measure-table:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink-on-paper}"
    valueTypography: "{typography.measure}"
    labelTypography: "{typography.label}"
    rowBorder: "{colors.hairline-on-paper}"
    padding: 64px 0
  text-tile:
    width: 1080px
    height: 1350px
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    padding: 96px
  photo-placeholder:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.muted}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
  footer:
    backgroundColor: "{colors.band}"
    textColor: "{colors.body}"
    typography: "{typography.body-sm}"
    padding: 64px 0
---

# Bellowerk — Designsystem

Gilt für alles, was die Marke nach außen zeigt: Website und Shop, Produktseiten, Instagram-Kacheln,
Newsletter, Anhänger und Pflegekarte. Markenwahrheit bleibt `markenwissen.py` und
`sourcing/bellowerk/markenbrief.md`; dieses Dokument legt fest, **wie** die Marke aussieht.
Wer etwas gestaltet, arbeitet mit `.claude/skills/bellowerk-design/SKILL.md`.

## Überblick

Bellowerk sieht aus wie eine Werkstatt am Abend: dunkler, warmer Grund (`{colors.canvas}` — Nacht
#13110E), darauf cremefarbene, weit gesperrte Versalien und echte Fotos im tiefen Sonnenlicht. Nichts
glänzt außer dem, was auch am Produkt glänzt: **Messing** (`{colors.accent}` — #B08D57). Es sitzt nur
dort, wo etwas bedient wird — die Hauptaktion, der Fokusrahmen, die zwei Schrauben der Patch-Plakette —
so wie am Halsband nur Schnalle, Ring und Schrauben aus Messing sind.

Die Schrift folgt dem Patch: **Jost** (geometrische Grotesk im Futura-Stil, wie PATCH-01 für
"BELLOWERK" vorgibt) in Versalien, Gewicht 400, weit gesperrt, für Überschriften, Navigation, Labels
und Maße. **Lora** (die Markenschrift aus `markenwissen.py`) für alles, was man liest. Die
Schreibschrift "Manufaktur" kommt nur aus dem Logo und wird nie als Schrift gesetzt.

**Waldgrün** (`{colors.band}` — #23352A) ist die einzige zweite Fläche: das Praxistest-Band und der
Fuß jeder Seite. Die Lederfarben (Grau, Dunkelbraun, Oliv, Cognac, Schwarz) erscheinen nur im Foto und
in den Farbfeldern der Produktauswahl — nie als Flächen, Linien oder Schriftfarben.

Das Kaufargument ist der Praxistest, nicht das Material. "Pflanzlich gegerbt, Handarbeit, Messing" sagt
jeder Wettbewerber (`markenwissen.py`, MARKTLUECKE) — bei Bellowerk ist das der Beleg im Kleingedruckten.
Die Schlagzeile gehört der Saison an fremden Hunden.

**Kennzeichen:**
- Dunkle Bühne: Nacht als Grund jeder Seite und jeder Instagram-Textkachel. Kein reines Schwarz.
- Versalien in Jost 400 mit 0,12–0,36 em Sperrung. Nie fett — Gewicht 500 nur für Labels, Navigation
  und Knöpfe bis 14 px, damit sie auf Dunkel lesbar bleiben.
- Lora für Lesetext, echte Zitate und Hundenamen (Namensgravur in gesperrten Serifen-Versalien).
- Ein Akzent: Messing. Höchstens eine Messing-Aktion pro Bildschirmansicht.
- Ecken 0 px. Nur Knöpfe sind Pillen (wie ein abgerundetes Riemenende), nur die Patch-Plakette hat 6 px
  (wie der echte Patch mit 3 mm Radius).
- Keine Schatten, keine Verläufe, keine Leder- oder Holztexturen. Tiefe kommt aus dem Foto.
- 120 px Luft zwischen Abschnitten. Das Produkt braucht Platz, nicht Deko.
- Das eine Detail, das nur Bellowerk haben kann: **Patch-Plakette + Saison-Logbuch** auf jeder
  Produktseite — mit echten Daten aus dem Praxistest.

## Reference Lock

Festgelegt nach der Refero-Methode (`.claude/skills/refero-design/`). Wer davon abweicht, braucht
Björns Freigabe.

```text
Primärreferenz: Bugatti (design/referenzen/bugatti.DESIGN.md) — strenge dunkle Bühne
Erhalten:       dunkler Grund · gesperrte Versalien in 400 · Serifen-Fließtext · Foto als einzige
                Farbfläche · 0-px-Ecken, Knöpfe als Pille · 120 px zwischen Abschnitten
Nur übernehmen: Ferrari — genau ein knapper Akzent auf warmem Fast-Schwarz (bei uns Messing)
                Starbucks — Tiefgrün nur für Bänder und Fuß (bei uns Waldgrün)
Rollenregeln:   Messing = Hauptaktion, Fokus, Patch-Schrauben · Waldgrün = Fläche, nie Schrift ·
                Lederfarben = nur Foto und Farbfeld · Papier = nur Maßtabelle, Kasse, Recht, Druck
Bildstrategie:  echte Fotos aus Gassi-Service, Pension, Training; tief stehende Sonne; Messing-Details
                auf dunklem Grund; fehlt ein Foto → Platzhalter mit Aufnahmeanweisung, nie KI-Bild
Verworfen:      Creme-Papier als Grundfläche · Oliv/Terrakotta als UI-Farben · abgerundete Karten ·
                Schatten · Verläufe · Leder-/Holztexturen · gesetzte Schreibschrift · Monospace (Bugatti) ·
                eisblaue Links (Bugatti) · Rot/Gelb (Ferrari) · Pillen-Karten und Schatten (Starbucks)
Token-Zusagen:  Nacht / Talg / Messing / Waldgrün / Papier wie oben · Jost + Lora · 0 px / Pille ·
                keine Schatten
```

## Entscheidungen und ihre Quellen

| Entscheidung | Quelle | Rollenregel | Warum |
|---|---|---|---|
| Dunkle Bühne, Nacht #13110E | Bugatti; eure Instagram-Textkacheln ("THE NEW HUNTSMAN", "MEET & MESSURE") | Nacht ist Grund, nie Akzent | Die Marke hat diesen Look schon; Fotos und Messing leuchten auf Dunkel |
| Warmes statt reines Schwarz | Ferrari ("never pure black"); Refero-Stil ORYZO ("Walnut Shadow") | — | Leder und geölte Eiche statt Autolack |
| Jost, Versalien, 400, gesperrt | PATCH-01 ("Futura/Josefin style, tracking +20 %"); Bugatti | Überschriften, Navigation, Labels, Maße | Liest sich wie die Lasergravur auf dem Patch |
| Lora für Lesetext | `markenwissen.py` (Markenschrift); Bugatti (Serifen-Fließtext) | Lesetext, Zitate, Hundenamen | Markenschrift bleibt; Kontrast zu den Versalien |
| Messing als einziger Akzent | Ferrari (ein knapper Akzent); Logo-Farbe #B08D57 | Hauptaktion (max. 1 je Ansicht), Fokus, Patch-Schrauben | Wie am Produkt: Messing ist der Beschlag |
| Waldgrün für Band und Fuß | Starbucks (House Green nur für tiefe Bänder und Fuß); Logo-Farbe #23352A | Nur Fläche, nie Schrift, nie Knopf | Grüne Klammer um die Seite, Bezug zu Revier und Altem Land |
| Lederfarben nur als Farbfeld | Refero Anti-KI-Einheitslook ("Oliv/Terrakotta auf Autopilot") | Foto und Farbwahl | Sonst kippt es in den austauschbaren Erdton-Look |
| 0 px, Knöpfe als Pille | Bugatti | Pille nur für Knöpfe | Präzise wie eine Stanzkante; Knöpfe sofort erkennbar |
| Keine Schatten, Verläufe, Texturen | Bugatti | — | Tiefe kommt aus dem Foto; Lederimitat wirkt billig |
| Patch-Plakette + Saison-Logbuch | `markenwissen.py` (POSITIONIERUNG); PATCH-01 | Nur Produktseite und Praxistest-Band, nur echte Daten | Das Detail, das kein Wettbewerber nachmachen kann |
| Nur echte Fotos | Markenbrief (Bildsprache); Abteilung 04 Social ("keine KI-Generierung") | Fehlt ein Foto: Platzhalter mit Aufnahmeanweisung | Der Praxistest ist nur glaubwürdig mit echten Bildern |
| Langsame, gewichtete Bewegung | Refero-Stil Sequel (`cubic-bezier(0.625, 0.05, 0, 1)`) | Nur Bild-Einblendungen; Bedienung bleibt schnell | Wie ein langsamer Zoom auf ein Standbild |

## Farben

### Grund und Flächen
- **Nacht** (`{colors.canvas}` — #13110E): Grund jeder Seite, jeder Instagram-Textkachel, jedes Fotorands.
- **Nacht 2** (`{colors.surface}` — #1C1915): Nur wo sich etwas öffnet (Warenkorb-Leiste, Auswahlmenü)
  und für Foto-Platzhalter. Kein Kartengrund.
- **Waldgrün** (`{colors.band}` — #23352A): Praxistest-Band, Manufaktur-Band, Fuß. Nur als Fläche.
- **Papier** (`{colors.paper}` — #F2EDE4): Nur Maßtabelle / "Hund vermessen", Kasse, Rechtstexte und
  Druck. Auf Papier gilt die Tinte-Reihe (`ink-on-paper`, `body-on-paper`, `muted-on-paper`).

### Schrift
- **Talg** (`{colors.ink}` — #EEE7DA): Überschriften, Navigation, Hauptaussagen. 15,3:1 auf Nacht,
  10,6:1 auf Waldgrün.
- **Fließtext** (`{colors.body}` — #CBC2B2): 10,7:1 auf Nacht, 7,4:1 auf Waldgrün.
- **Gedämpft** (`{colors.muted}` — #948B7D): Metadaten, Bildunterschriften — **nur auf Nacht** (5,6:1).
  Auf Waldgrün wären es 3,9:1, also dort `{colors.body}` nehmen.

### Messing — der einzige Akzent
- **Messing** (`{colors.accent}` — #B08D57): 6,1:1 auf Nacht.
- Erlaubt: `{component.button-primary}` (höchstens einer je Bildschirmansicht), Fokusrahmen 2 px,
  die zwei Schraubenpunkte der `{component.patch-plakette}`, die Kopfzeile einer Instagram-Textkachel
  (Kacheln haben keine Knöpfe — das ist die einzige Textrolle).
- Verboten: Fließtext, Überschriften, Flächen, Linien, Verläufe, Symbole, Preise.
- Schrift auf Messing ist immer Nacht (`{colors.on-accent}`, 6,1:1). Talg auf Messing hat nur 2,5:1.
- Auf Papier gibt es kein Messing als Schrift oder Knopf (2,65:1) — dort ist die Hauptaktion
  `{component.button-primary-on-paper}` in Tinte.

### Lederfarben — nur Farbfeld
`leather-grau`, `leather-dunkelbraun`, `leather-oliv`, `leather-cognac`, `leather-schwarz` erscheinen
ausschließlich als runde Farbfelder in der Produktauswahl und in Farblegenden. Die Werte sind aus einem
Foto gemessen und müssen am echten Leder bestätigt werden.

### Zustände
Fehler `{colors.error}` / auf Papier `{colors.error-on-paper}`, Erfolg `{colors.success}` / auf Papier
`{colors.success-on-paper}` — nur für Formularmeldungen, immer mit Text, nie als Deko.

## Typografie

### Schriften
1. **Jost** (Google Fonts, frei) — Überschriften, Wortmarke, Navigation, Knöpfe, Labels, Maße, Preise.
   Immer Versalien außer bei Maßen und Preisen. Weil PATCH-01 die Wortmarke als "Futura/Josefin style"
   beschreibt: Ist die echte Logo-Schrift bekannt, ersetzt sie Jost.
2. **Lora** (Google Fonts, frei, Markenschrift) — Lesetext, Einleitungen, echte Zitate, Hundenamen.
3. **Schreibschrift** — nur im Logo "Manufaktur" (Vektorgrafik). Nie als Webfont.

Mehr Schriften gibt es nicht. Laden: Jost 400/500, Lora 400/400 kursiv, `font-display: swap`.

### Hierarchie

| Token | Größe | Gewicht | Zeilenhöhe | Sperrung | Einsatz |
|---|---|---|---|---|---|
| `{typography.display-xl}` | 56 px | 400 | 1,1 | 0,12 em | Hero-Überschrift, max. 2 Zeilen |
| `{typography.display-lg}` | 40 px | 400 | 1,15 | 0,14 em | Abschnittsüberschrift, Praxistest-Band |
| `{typography.display-md}` | 28 px | 400 | 1,2 | 0,16 em | Unterabschnitte, Modellname auf der Produktseite |
| `{typography.display-sm}` | 20 px | 400 | 1,3 | 0,18 em | Modellname in der Übersicht |
| `{typography.wordmark}` | 15 px | 400 | 1 | 0,36 em | Gesetzte Wortmarke — nur solange das Logo als SVG fehlt |
| `{typography.label}` | 12 px | 500 | 1,4 | 0,24 em | Kopfzeilen über Überschriften, Bildunterschriften, Logbuch-Labels |
| `{typography.nav}` | 12 px | 500 | 1,4 | 0,24 em | Navigation |
| `{typography.button}` | 13 px | 500 | 1 | 0,22 em | Knöpfe |
| `{typography.measure}` | 28 px | 400 | 1,1 | 0,04 em | Maße und Logbuch-Werte ("20 MM", "3,00 M", "45 · 140 · 245 CM") |
| `{typography.price}` | 18 px | 400 | 1,3 | 0,06 em | Preise |
| `{typography.name-engraving}` | 22 px | 400 | 1,2 | 0,2 em | Hundename wie auf dem Namenspatch (Lora-Versalien) |
| `{typography.lead}` | 20 px | 400 | 1,6 | 0 | Einleitung unter einer Überschrift |
| `{typography.body}` | 17 px | 400 | 1,65 | 0 | Lesetext, max. 62 Zeichen je Zeile |
| `{typography.body-sm}` | 15 px | 400 | 1,6 | 0 | Fuß, Pflegehinweise, Kleingedrucktes |
| `{typography.quote}` | 22 px | 400 kursiv | 1,5 | 0 | Nur echte Zitate von Kundinnen und Kunden |

### Regeln
- Hervorhebung durch Größe, Sperrung und Luft — nie durch Fettdruck.
- Überschriften kurz: höchstens 6 Wörter, höchstens 2 Zeilen (mobil 3), `text-wrap: balance`.
- Keine Einzelwort-Hervorhebung in Kursiv, Farbe oder anderer Schrift.
- Zahlen mit Einheit und geschütztem Leerzeichen: `20 mm`, `3,00 m`, `69 €`; Maße und Preise mit
  `tabular-nums`.

## Layout

### Abstände
Basis 4 px: `{spacing.xxs}` 4 · `{spacing.xs}` 8 · `{spacing.sm}` 12 · `{spacing.md}` 16 · `{spacing.lg}` 24 ·
`{spacing.xl}` 40 · `{spacing.xxl}` 64 · `{spacing.section}` 120 (mobil `{spacing.section-mobile}` 72).

### Raster
- Inhalt max. 1.280 px, 12 Spalten, Rinne 24 px (ab 1.024 px: 40 px). Fotos laufen randlos.
- Lesetext höchstens 62 Zeichen breit.
- Produktübersicht: 3 Spalten ab 640 px, darunter 1 — nie eine einzelne Kachel allein in einer Reihe.
  Keine Kartenrahmen.

### Seitenrhythmus (Startseite)
1. Hero: randloses Foto (Hund mit Produkt, tief stehende Sonne), Überschrift und eine Aktion.
2. Produkte: 3 Modelle, Foto 4:5, darunter Name, eine Zeile Material, Preis.
3. **Praxistest-Band** (Waldgrün): Foto im Einsatz, Saison-Logbuch, ein Satz, wie getestet wird.
4. Messing-Detail: ein Makrofoto der Beschläge auf dunklem Grund, drei nüchterne Fakten.
5. Manufaktur: Björn, der Betrieb, Hamburg / Altes Land — echte Fotos, kurzer Text.
6. Fuß (Waldgrün).

Nicht: Hero → Feature-Raster → Preise → FAQ → CTA nach Schema. Jeder Abschnitt muss eine Frage
beantworten, die ein Hundehalter vor dem Kauf hat.

## Bildsprache

Das Foto ist die einzige Farbfläche dieses Systems. Deshalb gelten strenge Regeln:

- **Nur echte Fotos** aus Gassi-Service, Pension und Training. Keine KI-Bilder, keine Stockfotos,
  keine Produkt-Mockups, keine Studiofotos auf Weiß für die Website.
- Licht: tief stehende Sonne, Gegenlicht, Abend. Oder Messing-Details auf dunklem Grund.
- Ehrliche Gebrauchsspuren zeigen — sie sind der Beleg für den Praxistest.
- Hunde: mittel bis groß, Familien- und Gebrauchshunde (Zielgruppe). Keine Windhunde als Hauptmotiv.
- Menschen nur angeschnitten (Hände, Beine, Mantel) oder mit Einwilligung.
- Formate: Hero 16:9 (mobil 4:5), Produkt 4:5, Detail 1:1, Instagram 4:5 (1.080 × 1.350 px).
- Text auf Fotos nur auf ruhigen, dunklen Bildstellen; sonst steht er unter dem Bild auf Nacht.
  Keine Abdunkelungs-Verläufe.
- Solange Patches noch "HERR BELLO & FRAU WUFF" tragen: auf der Website keine Nahaufnahmen, auf denen
  der alte Name lesbar ist.
- **Fehlt ein Foto:** `{component.photo-placeholder}` im richtigen Format mit Aufnahmeanweisung
  (Motiv, Ort, Tageszeit, Ausschnitt) — genauso, wie Abteilung 04 Social sie schreibt.

## Tiefe

Keine Schatten, kein Glas, keine Verläufe, keine Texturen. Ebenen entstehen nur durch
Flächenwechsel (Nacht → Waldgrün → Papier) und durch das Foto selbst. Trennlinien 1 px in
`{colors.hairline}` (auf Waldgrün `{colors.hairline-on-band}`, auf Papier `{colors.hairline-on-paper}`).

## Formen

| Token | Wert | Einsatz |
|---|---|---|
| `{rounded.none}` | 0 px | Alles: Fotos, Bänder, Eingabefelder, Tabellen, Platzhalter |
| `{rounded.patch}` | 6 px | Nur `{component.patch-plakette}` — Echo des echten Patches (3 mm Radius) |
| `{rounded.pill}` | 9999 px | Nur Knöpfe — wie ein abgerundetes Riemenende |
| `{rounded.full}` | 50 % | Farbfelder, Schraubenpunkte, runde Symbol-Knöpfe |

## Komponenten

### Navigation
**`top-nav`** — 64 px, transparent über dem Hero-Foto. Links "KOLLEKTION", Mitte das Logo
(Vektor; bis dahin `{typography.wordmark}` "BELLOWERK"), rechts "WARENKORB". Alle Einträge in
`{typography.nav}`, Talg. Mobil: "MENÜ" links, Logo Mitte, Warenkorb rechts.

### Knöpfe
**`button-primary`** — Messing, Schrift Nacht, Pille, 48 px hoch, 16 × 32 px Innenabstand,
`{typography.button}`. Gedrückt: `{component.button-primary-pressed}` (Messing poliert) und
`transform: scale(0.98)`. **Höchstens einer pro Bildschirmansicht.** Beschriftung = Handlung +
Gegenstand: "Halsbänder ansehen", "In den Warenkorb", "Hund vermessen lassen".

**`button-secondary`** — Transparent, 1 px Talg-Rahmen, Talg-Schrift, Pille. Für alles Zweitrangige
("Wie wir testen").

**`button-primary-on-paper`** — Tinte-Fläche, Papier-Schrift. Hauptaktion auf Papierflächen (Kasse).

**`text-link`** — Talg, 1 px Unterstreichung mit 4 px Abstand. Keine eigene Linkfarbe.

Fokus überall: 2 px Messing-Rahmen mit 3 px Abstand, nur bei `:focus-visible`.

### Produkt
**`product-tile`** — Keine Karte: Foto 4:5 direkt auf Nacht, darunter mit 16 px Abstand der Name in
`{typography.display-sm}`, eine Zeile Material in `{typography.body-sm}` / `{colors.body}`
("Fettleder, 3,5 mm · Messing massiv"), Preis in `{typography.price}`, Farbfelder. Die ganze Fläche
ist ein Link.

**`leather-swatch`** — 24 px Kreis in der Lederfarbe, 1 px Ring in `{colors.edge}`. Ausgewählt
(`leather-swatch-selected`): 1 px Talg-Ring mit 3 px Abstand. Name der Farbe als `{typography.label}`
daneben oder als `aria-label`.

**`patch-plakette`** — Das Markenzeichen der Oberfläche, abgeleitet vom Lederpatch: Rechteck mit
6 px Radius, 1 px Rahmen in `{colors.body}`, links und rechts je ein 8-px-Messingpunkt (die
Buchschrauben), dazwischen in `{typography.label}`: "PRAXISTEST · 1 SAISON". Nur auf der Produktseite
(einmal, beim Modellnamen) und im Praxistest-Band. Nie als allgemeines Abzeichen.

**`saison-logbuch`** — Auf Waldgrün eine Zeile mit 3–4 Messwerten, getrennt durch Haarlinien in
`{colors.hairline-on-band}`:
Wert in `{typography.measure}`, Beschriftung darunter in `{typography.label}`. Beispiel für die
Struktur: SAISON / HERBST–WINTER 2026 · HUNDE / [Anzahl] · GASSIRUNDEN / [Anzahl] · WETTER / REGEN,
SCHLAMM, ELBSTRAND. **Nur echte Daten aus dem Betrieb — nie schätzen, nie erfinden.** Fehlen sie,
entfällt das Logbuch.

**`measure-table`** — Auf Papier: Größentabelle S/M/L/XL mit Halsumfang, Breite, Lochabstand; Werte in
`{typography.measure}` (verkleinert auf 20 px), Beschriftung `{typography.label}`, Zeilen mit
Haarlinie. Werte kommen aus `sourcing/bellowerk/specs/`, nie aus dem Kopf.

### Bänder
**`hero-photo`** — Randloses Foto, darunter oder auf einer dunklen Bildstelle: Kopfzeile
(`{typography.label}`, `{colors.body}`), Überschrift (`{typography.display-xl}`), eine Zeile
`{typography.lead}`, ein `button-primary`, optional ein `button-secondary`.

**`band-praxistest`** — Waldgrün, 120 px oben und unten. Überschrift `{typography.display-lg}`,
`patch-plakette`, `saison-logbuch`, ein Foto im Einsatz, zwei bis drei Sätze Lora.

**`footer`** — Waldgrün, 64 px. Vier Spalten (Kollektion · Manufaktur · Pflege · Kontakt), Logo,
Pflichtangaben. `{typography.body-sm}` in `{colors.body}`.

### Formulare
**`text-input`** — Transparent, nur Unterkante 1 px in `{colors.edge}`, 48 px hoch, Lora 17 px.
Fokus: Unterkante 2 px Messing. Beschriftung darüber in `{typography.label}`. Fehler: Text in
`{colors.error}` unter dem Feld, mit Lösung ("Bitte den Halsumfang in cm angeben, z. B. 42").

### Platzhalter
**`photo-placeholder`** — Nacht-2-Fläche im Zielformat, darin in `{typography.label}` die
Aufnahmeanweisung: "FOTO FEHLT · HB-01 COGNAC AM HUND · ABENDS, GEGENLICHT · AUSSCHNITT HALS BIS
SCHULTER". Nie ein Ersatzbild.

## Instagram

**`text-tile`** (1.080 × 1.350 px) — genau der Aufbau eurer bisherigen Textkacheln:
- Grund Nacht, Rand 96 px.
- Oben: Kopfzeile Jost 500, 26 px, Sperrung 0,3 em, **Messing** (einzige Textrolle für Messing).
- Mitte: Überschrift Jost 400, 88 px, Sperrung 0,12 em, Talg, höchstens 2 Zeilen à 14 Zeichen.
- Unten: Fußzeile Jost 500, 26 px, Sperrung 0,3 em, `{colors.muted}`.
- Keine Logos-Wand, keine Hashtags im Bild, keine Emojis.

Fotobeiträge: echtes Foto, kein Text im Bild — der Text steht im Beitrag (Abteilung 04).

## Druck (Anhänger, Pflegekarte)

Einfarbig in Tinte (#1B1814) auf Kraftkarton, wie VERP-01 Option A vorsieht. Jost-Versalien für
"BELLOWERK", Modell und Größe; Lora für Pflegetext und Pflichtangaben. Messing nur, falls Björn
Heißfolie freigibt. Mindestschrift 7 pt.

## Bewegung

- Rückmeldung (Druck, Hover, Fokus): 120 ms, `ease-out`.
- Zustandswechsel (Auswahl, Aufklappen): 240 ms, `ease-weighted`.
- Bild-Einblendung beim Scrollen: Deckkraft 0 → 1 und 1,04 → 1 Skalierung, 480 ms, `ease-weighted` —
  wie ein langsamer Zoom auf ein Standbild. Nie Springen, nie Federn, nie Farbanimation.
- `prefers-reduced-motion`: nur Überblenden, 120 ms.

## Texte

- Du-Form, wie auf Instagram ("Wir vermessen deinen Hund").
- Fakten statt Adjektive: "3,5 mm Fettleder, pflanzlich gegerbt", "Messing massiv", "ohne Naht".
- Nie über den Preis verkaufen: kein "günstig", kein Rabatt-Banner, kein durchgestrichener Preis.
- Verboten: "Premium", "hochwertig", "einzigartig", "nachhaltig" ohne Beleg, "Liebe zum Detail".
- Überschriften in Versalien sind Aussagen, keine Werbesprüche.
- Vorschlag für die Hero-Überschrift (Björn entscheidet): **"JEDES MODELL: EINE SAISON AM HUND."**
  Darunter: "Bevor ein neues Modell in den Verkauf geht, tragen es eine Saison lang fremde Hunde: im
  Gassi-Service, in der Pension, im Training. Täglich, bei jedem Wetter."
- Immer "jedes Modell" schreiben, nie "jedes Halsband": Getestet wird das Modell, verkauft wird neue
  Ware. Sonst klingt es nach gebrauchter Ware.

## Mach / Lass

### Mach
- Jede Seite mit einem echten Foto eröffnen; das Foto trägt die Farbe.
- Überschriften in Jost-Versalien 400 mit Sperrung, Lesetext in Lora.
- Messing nur für die eine Hauptaktion, den Fokus und die Patch-Schrauben.
- Waldgrün für das Praxistest-Band und den Fuß.
- Auf jeder Produktseite Patch-Plakette und Saison-Logbuch — mit echten Daten.
- 120 px zwischen Abschnitten lassen.
- Token-Namen statt Hex-Werten verwenden.

### Lass
- Keine fette Schrift, keine Einzelwort-Hervorhebung.
- Keine Schatten, Verläufe, Glaseffekte, Leder-, Holz- oder Papiertexturen.
- Keine abgerundeten Karten, keine Kartenraster mit Rahmen.
- Keine Lederfarben als Flächen, Linien oder Schrift. Kein Indigo, kein Violett.
- Kein zweiter Messing-Knopf in derselben Ansicht.
- Keine KI-Bilder, Stockfotos, Mockups, Emojis.
- Kein heller Creme-Grund als Standard — Papier ist nur für Maßtabelle, Kasse, Recht und Druck.
- Keine erfundenen Zahlen (Testhunde, Runden, Bewertungen).

## Responsiv

| Name | Breite | Änderungen |
|---|---|---|
| Mobil | < 640 px | Hero-Foto 4:5; `display-xl` 56 → 32 px, Sperrung 0,12 → 0,08 em; Produkte 1-spaltig; Logbuch 2 × 2; Abschnitte 72 px |
| Tablet | 640–1.023 px | Produkte 3-spaltig (schmal); Hero 16:9; `display-xl` 44 px |
| Desktop | ≥ 1.024 px | Produkte 3-spaltig; Rinne 40 px; Inhalt max. 1.280 px |

- Tippflächen mindestens 48 × 48 px.
- Gesperrte Versalien dürfen auf 320 px Breite nicht umbrechen, wo sie nicht sollen — lange Wörter
  ("GASSIRUNDEN") in `display-md` statt `display-lg` setzen.
- Bilder mit festen Seitenverhältnissen (`aspect-ratio`) und Breite/Höhe, damit nichts springt.

## Anleitung für Agenten

1. Erst `markenwissen.py` und `sourcing/bellowerk/markenbrief.md` lesen, dann dieses Dokument.
2. Eine Komponente nach der anderen; auf den YAML-Schlüssel verweisen (`{component.patch-plakette}`).
3. Neue Komponenten starten bei `{rounded.none}`, Nacht-Grund, Talg-Schrift.
4. Varianten als eigene Einträge unter `components:`.
5. Nie Hex-Werte im Code verstreuen — CSS-Variablen aus den Tokens erzeugen.
6. Vor der Übergabe: Screenshot bei 390 px und 1.440 px Breite gegen die "Mach / Lass"-Liste prüfen
   (Visual QA nach `.claude/skills/refero-design/references/visual-workflow.md`).

## Geprüfte Alternativen (nicht gewählt)

| Richtung | Idee | Warum nicht |
|---|---|---|
| **Revier** | Waldgrün als Grundfläche, Messing-Akzent, Talg-Schrift | Warme Abendfotos (Braun, Gold) verlieren auf Grün an Kraft; Grün + Messing kippt schnell in Jagdausstatter-Katalog. Waldgrün bleibt als Band. |
| **Werkstatt-Journal** | Heller Papiergrund, Lora-Überschriften, Fotos in Kinoformat (Refero: Parallel) | Genau der Creme-Serife-Oliv-Einheitslook, vor dem Refero warnt; bricht mit den schwarzen Instagram-Kacheln. Papier bleibt für Maßtabelle und Kasse. |

## Offene Punkte für Björn

1. **Logo als Vektor** fehlt (`sourcing/bellowerk/bilder/PATCH-01-artwork.svg`). Bis dahin steht die
   Wortmarke gesetzt in Jost; "Manufaktur" in Schreibschrift erscheint erst mit dem Logo.
2. **Logo-Schrift:** Ist sie bekannt (Futura, Josefin Sans …)? Dann ersetzt sie Jost.
3. **Lederfarben** sind aus einem Foto unter Kunstlicht gemessen (`LE-01-flechtung-ringe-farben.jpg`)
   — an echten Lederproben nachmessen.
4. **Praxistest-Daten** je Modell festhalten (Saison, Anzahl Hunde, Gassirunden, Wetter). Ohne sie
   bleibt das Saison-Logbuch leer.
5. **Fotos in voller Auflösung:** Fast alle Bilder liegen nur als Handy-Screenshots vor. Und auf vielen
   Patches steht noch der alte Name.
6. **Shop-System** (z. B. Shopify) — die Kasse übernimmt die Papier-Regeln.
7. **Hero-Überschrift** "JEDES MODELL: EINE SAISON AM HUND." — freigeben oder ändern.
