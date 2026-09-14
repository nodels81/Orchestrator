# Designsystem — Tokens vor Bauteilen

Ergebnis dieses Dokuments ist eine Datei `tokens.css` und eine Bauteilübersicht.
Kein Bauteil entsteht vorher.

## 1. Farbe in OKLCH

OKLCH statt HEX, weil dort gleiche Helligkeitswerte über alle Töne auch gleich hell **wirken**.
Eine Leiter mit 12 Stufen je Rolle, gleichmäßiger Helligkeitsverlauf, Buntheit in der Mitte am höchsten.

```css
:root{
  --hue-brand: 62;                                   /* Cognac-Leder */
  --hue-akzent: 92;                                  /* Messing */

  --brand-50:  oklch(97% .012 var(--hue-brand));
  --brand-100: oklch(94% .022 var(--hue-brand));
  --brand-300: oklch(80% .060 var(--hue-brand));
  --brand-500: oklch(58% .092 var(--hue-brand));     /* Leitton */
  --brand-700: oklch(40% .072 var(--hue-brand));
  --brand-900: oklch(24% .048 var(--hue-brand));

  --akzent-400: oklch(78% .108 var(--hue-akzent));   /* Messing, nur Akzent und Fokus */

  --ink:    oklch(18% .012 62);    /* nie #000 */
  --paper:  oklch(97% .006 82);    /* nie #fff */
  --flaeche: oklch(99% .004 82);
  --linie:  oklch(88% .010 72);
}

:root:not([data-theme="light"]){
  @media (prefers-color-scheme: dark){
    --ink: oklch(95% .008 82); --paper: oklch(16% .014 62);
    --flaeche: oklch(21% .016 62); --linie: oklch(30% .018 62);
  }
}
:root[data-theme="dark"]{ /* dieselben Werte, damit der Umschalter in beide Richtungen gewinnt */ }
```

**Regeln**
- Ein Leitton, eine Gegenfarbe, eine Neutralleiter. Mehr wirkt unsicher.
- Neutralgrau wird leicht in den Markenton gekippt (Buntheit .004–.016). Reines Grau ist tot.
- Kontrast vorab prüfen: Fließtext ≥ 4.5:1, Großtext und Bedienelemente ≥ 3:1.
  Paare in eine Tabelle schreiben, nicht hoffen.
- Semantik zusätzlich: Erfolg, Warnung, Fehler, Hinweis — jeweils Fläche, Rand, Text.
- Hell und dunkel gleichzeitig anlegen. Dunkel ist nicht "hell invertiert": Flächen werden heller
  als der Grund, Schatten schwächer, Lichtkanten stärker.

## 2. Typografie

```css
:root{
  --step--2: clamp(.72rem, .69rem + .14vw, .8rem);
  --step--1: clamp(.83rem, .78rem + .22vw, .94rem);
  --step-0:  clamp(1rem,   .95rem + .3vw,  1.15rem);
  --step-1:  clamp(1.2rem, 1.1rem + .5vw,  1.45rem);
  --step-2:  clamp(1.6rem, 1.35rem + 1.1vw, 2.2rem);
  --step-3:  clamp(2.2rem, 1.7rem + 2.4vw, 3.6rem);
  --step-4:  clamp(2.8rem, 1.9rem + 3.8vw, 5rem);
  --step-6:  clamp(3.6rem, 2.2rem + 6.8vw, 8rem);   /* Display */
}
```

- **Variable Fonts**, selbst gehostet, auf die benutzten Zeichen reduziert (Subsetting), `woff2`.
- `font-display: swap` plus metrisch angeglichener Fallback über `size-adjust`,
  `ascent-override`, `descent-override` — sonst springt das Layout beim Schriftwechsel.
- Tracking: Display −0.02em bis −0.04em, Kleintext +0.01em bis +0.02em.
- Zeilenhöhe fällt mit der Größe: 1.6 im Fließtext, 1.15 in Überschriften, 0.95 im Display.
- Zeilenlänge 60–75 Zeichen (`max-width: 68ch`).
- Zahlen und Preise: `font-variant-numeric: tabular-nums`, damit nichts wackelt.
- `text-wrap: balance` für Überschriften, `text-wrap: pretty` für Fließtext.
- Höchstens zwei Familien. Bellowerk: Lora (Serife) plus eine schmale Grotesk.

## 3. Raum

Eine Reihe, keine Zufallswerte: `4 8 12 16 24 32 48 64 96 128 192 256`.

- Bauteilabstände bleiben fest.
- Sektionsabstände skalieren: `--sektion: clamp(64px, 9vw, 192px)`.
- Der größte Abstand auf der Seite ist mindestens achtmal der kleinste.
- Optischer Ausgleich schlägt gemessenen: Über einer Überschrift steht mehr Luft als darunter,
  Verhältnis etwa 3:1. Das bindet die Überschrift an ihren Text.

## 4. Raster

```css
.seite{
  display: grid;
  grid-template-columns:
    [voll-start] minmax(16px,1fr)
    [inhalt-start] repeat(12, minmax(0, 5.5rem)) [inhalt-ende]
    minmax(16px,1fr) [voll-ende];
  column-gap: clamp(16px, 2.4vw, 32px);
}
```

Sektionen greifen per benannter Linie hinein (`grid-column: inhalt-start / inhalt-ende` oder
`voll-start / voll-ende`). So sitzt alles auf derselben Kante, auch bei vollflächigen Sektionen.

- Inhalte auf 2–8, 5–12, 1–7 setzen. Nicht immer 1–12.
- Mobil bricht auf eine Spalte, aber nicht alles: Bild bleibt vollflächig, Text bekommt Rand.
- Außenrand nie unter 16px, an keiner Breite.

## 5. Oberfläche, Tiefe, Glanz

Der Teil, an dem "hochwertig" oder "nach Baukasten" entschieden wird.

```css
.karte{
  background:
    linear-gradient(180deg, oklch(100% 0 0/.06), oklch(100% 0 0/0) 42%),
    var(--flaeche);
  border: 1px solid var(--linie);
  border-radius: 12px;
  box-shadow:
    0 1px 1px oklch(0% 0 0/.05),           /* Kontaktschatten: klein, hart, nah */
    0 8px 24px -8px oklch(0% 0 0/.18),     /* Formschatten: groß, weich, versetzt */
    inset 0 1px 0 oklch(100% 0 0/.12);     /* Lichtkante: nur oben */
}
```

- **Licht kommt von oben.** Deshalb Lichtkante oben, Schatten unten. Ein Leuchten ringsum sieht
  nach Bootstrap aus.
- Schatten immer aus zwei bis drei Lagen. Eine Lage ist ein Schlagschatten, kein Volumen.
- Schattenfarbe ist nie neutralschwarz, sondern der abgedunkelte Markenton.
- `backdrop-filter` höchstens zweimal pro Seite (Navigation, Warenkorb-Schublade). Es kostet
  Rechenzeit und sieht auf iOS anders aus als anderswo — dort prüfen.
- **Rauschebene gegen Streifenbildung**: SVG-`feTurbulence`, 3–5 % Deckkraft, `pointer-events:none`,
  über großen Verläufen. Der Unterschied zwischen "Verlauf" und "Material".
- Radien in Stufen `4 8 12 20 999`. Verschachtelt korrekt: innerer Radius = äußerer minus Abstand.
- Ränder sind halbtransparentes Weiß oder Schwarz, keine Vollfarbe — dann passen sie auf jeden Grund.

## 6. Zustände und Fokus

Jedes bedienbare Element braucht: Ruhe, Hover, Aktiv, Fokus, Deaktiviert, Laden.

```css
:where(a,button,[tabindex]):focus-visible{
  outline: 2px solid var(--akzent-400);
  outline-offset: 2px;
  border-radius: inherit;
}
```

Der Fokusring wird gestaltet, nie entfernt. Er ist auf hellem **und** dunklem Grund sichtbar.
Trefferfläche mindestens 44 × 44 px, auch wenn das Element optisch kleiner ist.

## 7. Bauteilübersicht

Eine eigene Seite, die jedes Element in jedem Zustand zeigt, hell und dunkel, plus die
Typoskala, die Farbleitern mit Kontrastwerten und die Raumreihe. Sie ist Liefergegenstand
und dient bei jeder späteren Änderung als Prüfstand.
