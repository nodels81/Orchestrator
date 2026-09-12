# 01 — Produkttext

Einsatz: eine Produktseite aus der Kernserie. Vorher lesen: das Tech Pack des Modells in
`sourcing/bellowerk/specs/`, `seo/bellowerk/basisdaten.md`, die Zeile des Modells in
`seo/bellowerk/seitenstruktur.md`. **Alle Maße aus dem Tech Pack, keine aus dem Kopf.**
Platzhalter in `[ ]` ersetzen. Ergebnis ist ein Entwurf für Björn.

---

**URL:** `[/halsbaender/hb-01-fettleder]`
**Hauptsuchwort:** `[hundehalsband leder ohne naht]`
**Titel (≤ 60 Zeichen):** `[HB-01 Hundehalsband Fettleder — ohne Naht | Bellowerk]`
**Beschreibung (≤ 155 Zeichen):** `[Einlagiges Halsband aus Fettleder, 3,5–4 mm, Messing massiv, ohne Naht und Niete. In unserer Hundepension eine Saison getragen, dann verkauft.]`

## H1
`[Halsband HB-01 aus Fettleder — einlagig, ohne Naht]`

## Erster Absatz (der Absatz, der zitiert wird)
Zwei bis drei Sätze, die die Frage „was ist das und warum dieses" vollständig beantworten.
Konstruktion und Werkstoff stehen drin, der Praxistest wird angekündigt. Kein Werbeeinstieg,
keine Frage an den Leser, kein „Willkommen bei".

## Praxistest (der Teil, den kein Wettbewerber hat)
Ein Absatz: Welche Hunde, wie lange, bei welchem Wetter, was das mit dem Leder gemacht hat.
**Nur belegbare Aussagen.** Fehlt die Erfahrung zu diesem Modell: `[TODO Björn: welche Hunde
haben HB-01 getragen, wie lange?]` — nicht erfinden.

## Maße
Tabelle 1:1 aus dem Tech Pack: Größe, Halsumfang, Breite, Lochabstand, Gesamtlänge.
Darunter ein Satz mit Verweis auf `/ratgeber/halsband-messen`.

## Werkstoffe
- Fettleder, pflanzlich gegerbt, gefettet, Vollnarbe, `[Stärke]` mm, durchgefärbt
- Messing massiv: `[Rollschnalle, D-Ring geschweißt]` — unlackiert, Patina erwünscht
- Buchschrauben Messing 5 mm
- **Keine Naht, keine Niete, kein Stahl, kein Kunststoff**

## Pflege
Zwei Sätze, Verweis auf `/ratgeber/fettleder-pflege`.

## Preis
`[79] €` — innerhalb des Rahmens (Halsband 69–99 €). **Gilt erst nach Björns Freigabe.**

## Bilder (aus `sourcing/bellowerk/bilder/`)
1. `[HB-01-detail-patch.jpg]` — Alternativtext: `[Halsband HB-01 in Cognac mit Lederpatch und Messingschnalle]`
2. `[HB-02-geflochten-am-hund.jpg]` — Alternativtext: `[Hund trägt das geflochtene Halsband HB-02 in Oliv]`

Fehlt ein passendes Foto: benennen, welches Björn aufnehmen soll (Motiv, Ort, Tageszeit,
Bildausschnitt) — keine KI-Bilder, keine Stockfotos.

## Verweise im Text
- auf `/manufaktur` (Praxistest ausführlich)
- auf mindestens zwei Ratgeber
- auf das passende Zubehör

## Schema
`Product` mit `name`, `brand: Bellowerk`, `material`, `image`, `offers` (`price`, `priceCurrency: EUR`,
`availability`). **Kein `aggregateRating`, keine `review`** — es gibt keine echten Bewertungen.
