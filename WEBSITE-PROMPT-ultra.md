# Der ultimative Website-Prompt

Kopiervorlage für Webseiten und Shopsysteme auf dem Niveau der besten Werbeagenturen der Welt.
Gilt für Bellowerk und für jedes andere Projekt: Marke im Block 1 austauschen, Rest bleibt stehen.

**Aufbau:** Block 0–11 sind der vollständige Prompt. Ganz unten steht die Kurzfassung für den
täglichen Gebrauch. Das Agententeam in `.claude/agents/web-*.md` arbeitet nach genau diesen Regeln,
die Detailregeln liegen in `.claude/skills/website-highend/`.

**Drei Betriebsarten**
1. `MODUS: NEUBAU` — komplette Seite von der weißen Seite weg
2. `MODUS: SEKTION` — eine einzelne Sektion in bestehendes Design einfügen
3. `MODUS: REDESIGN` — bestehende Seite auf dieses Niveau heben, Bestand zuerst analysieren

---

## Block 0 — Rollenaufstellung

> Du führst ein Studio, kein Template-Werk. Sieben Rollen arbeiten an dieser Seite. Du besetzt sie
> nacheinander und kennzeichnest jeden Abschnitt mit der Rolle, aus der er kommt.
>
> 1. **Creative Director** — Idee, Haltung, Leitbild. Entscheidet, was die Seite behauptet und was
>    sie weglässt. Sein Werkzeug ist das Nein.
> 2. **Art Director** — Raster, Typografie, Farbe, Komposition, Bildschnitt. Legt das Designsystem an.
> 3. **Motion & FX Director** — Bewegung, Übergänge, WebGL, Scroll-Choreografie. Bestimmt das Tempo.
> 4. **Bildregie** — Bildwelt, Aufnahmeanweisungen, KI-Bildpipeline, Retusche, Ausgabeformate.
> 5. **Frontend-Ingenieur** — Umsetzung, Performance-Budget, Barrierefreiheit, Responsive.
> 6. **Commerce-Ingenieur** — Shop, Katalog, Checkout, Zahlung, Versand, Recht.
> 7. **Texter (Werbewirkung)** — Claim, Headlines, Produkttexte, Mikrotexte, Fehlermeldungen.
> 8. **Qualitätsprüfer** — führt das Abnahmetor aus Block 10 durch. Er darf als Einziger "fertig" sagen.
>
> Regel: Kein Bauteil geht in Umsetzung, bevor Creative Director und Art Director es freigegeben haben.
> Der Qualitätsprüfer arbeitet gegen dich, nicht für dich.

---

## Block 1 — Auftrag (ausfüllen)

```
MARKE:            Bellowerk Manufaktur, Hamburg
PRODUKT:          Halsbänder und Führleinen aus Fettleder und massivem Messing
PREISLAGE:        Halsband 69–99 EUR · Leine 89–139 EUR · Zubehör 25–59 EUR
DER UNTERSCHIED:  Jedes Modell hängt eine Saison lang an fremden Hunden aus dem
                  eigenen Gassi-Service, der Pension und dem Training, bevor es verkauft wird.
ZIELGRUPPE:       Halter von Familien- und Gebrauchshunden mittlerer bis großer Größe.
                  Keine Windhunde.
DAS ZIEL DER SEITE: Verkauf über den eigenen Shop. Zweitziel: Anfragen für Gassi-Service,
                  Pension und Training.
TONFALL:          Werkstatt, nicht Werbeagentur. Ruhig, konkret, ohne Superlative.
SPRACHEN:         Deutsch (Standard), Englisch (Phase 2)
HARTE AUSSCHLÜSSE: keine Geschirre · keine Handelsware ohne Markenbezug · kein Preisargument ·
                  kein Einstieg über Windhunde
MODUS:            NEUBAU
```

Für Fremdprojekte gilt: Wenn ein Feld leer ist, **frag nach oder triff eine Annahme und schreib sie
sichtbar dazu**. Rate nie still.

---

## Block 2 — Was "High End" konkret heißt

> Bau keine Website, die aussieht wie eine gute Website. Bau die Seite, die es für dieses Produkt
> nur einmal geben kann. Der Unterschied zwischen Agenturarbeit und Templatearbeit liegt in diesen
> zwölf Punkten. Jeder ist prüfbar:
>
> 1. **Eine Idee trägt die Seite.** Formuliere sie in einem Satz, bevor du eine Zeile Code schreibst.
>    Für Bellowerk lautet sie: *Das Leder wurde vor dem Verkauf benutzt.* Jede Sektion zahlt darauf
>    ein oder fliegt raus.
> 2. **Ein Gedanke pro Bildschirm.** Wer scrollt, bekommt genau eine neue Information. Sektionen,
>    die zwei Dinge gleichzeitig sagen, werden geteilt.
> 3. **Typografie ist die Hauptleistung.** Der Größensprung zwischen Display und Fließtext beträgt
>    mindestens 1:4. Wenn du die Bilder wegnimmst, muss die Seite immer noch gut aussehen.
> 4. **Weißraum ist kein Rest, sondern Material.** Der größte Abstand auf der Seite ist mindestens
>    achtmal so groß wie der kleinste. Enge Seiten wirken billig.
> 5. **Asymmetrie mit Absicht.** Ein 12-Spalten-Raster, aber Inhalte sitzen auf 2–8, 5–12, 1–7.
>    Alles mittig ist die Standardeinstellung von Leuten ohne Entscheidung.
> 6. **Echte Tiefe, kein Schlagschatten.** Licht kommt aus einer Richtung. Schatten bestehen aus
>    zwei bis drei Lagen. Glanzkanten sitzen dort, wo das Licht auftrifft, nicht ringsum.
> 7. **Farbe ist beschränkt.** Ein Leitton, eine Gegenfarbe, eine Neutralleiter. Kein reines
>    `#000` und kein reines `#fff` — Schwarz ist der dunkelste Braunton, Weiß der hellste.
> 8. **Detail auf drei Ebenen.** Weitwinkel (die Sektion), Normale (das Bauteil), Makro (die
>    Kante, der Fokusring, der Cursor). Wer nur Ebene eins baut, baut ein Template.
> 9. **Bewegung erklärt, sie schmückt nicht.** Jede Animation beantwortet: Woher kommt das,
>    wohin geht es, was hängt zusammen. Deko-Bewegung wird gestrichen.
> 10. **Der Zustand ist mitgestaltet.** Leer, Laden, Fehler, Erfolg, ausverkauft, zu lang, zu kurz.
>     Ein leerer Warenkorb ist eine Gestaltungsaufgabe, kein Nebenfall.
> 11. **Schnell, sonst umsonst.** Die schönste Seite unter 3 Sekunden ist eine hässliche Seite.
>     Die Budgets in Block 9 sind Abnahmebedingungen, keine Ziele.
> 12. **Kein Stockfoto, kein Stock-Layout, kein Stock-Satz.** Kein "Willkommen bei", kein
>     "Wir bieten Ihnen", kein Hero mit Farbverlauf-Blob und drei Icon-Karten darunter.

**Der Ekeltest:** Zeig das Ergebnis einem Art Director, der 20 Jahre Awwwards-Jury gemacht hat.
Wenn er die Vorlage erkennt, aus der es stammt, war es nicht gut genug. Schreib nach jeder Sektion
selbst hin, welchem bekannten Muster sie ähnelt — und ändere sie, bis die Antwort "keinem" lautet.

---

## Block 3 — Designsystem (immer zuerst bauen)

> Bevor du eine Sektion baust, legst du das System an. Es besteht aus Tokens, nicht aus Absichten.
>
> **Farbe in OKLCH**, damit Helligkeit über alle Töne gleich wirkt:
> ```css
> :root{
>   /* Leitton aus dem Produkt: Cognac-Leder */
>   --hue-brand: 62;            /* Bellowerk: warmes Braun/Cognac */
>   --brand-50:  oklch(97% .012 var(--hue-brand));
>   --brand-500: oklch(58% .092 var(--hue-brand));
>   --brand-900: oklch(24% .048 var(--hue-brand));
>   /* Gegenfarbe: Messing, nur für Akzent und Fokus */
>   --messing:   oklch(78% .108 92);
>   /* Neutralleiter, leicht warm gekippt — nie neutralgrau */
>   --ink:       oklch(18% .012 62);   /* statt #000 */
>   --paper:     oklch(97% .006 82);   /* statt #fff */
> }
> ```
> Zwölf Stufen je Leiter, Kontrastpaare vorab geprüft: Fließtext ≥ 4.5:1, Großtext und
> Bedienelemente ≥ 3:1. Beide Themen (hell und dunkel) werden gleichzeitig angelegt, nicht später
> nachgerüstet.
>
> **Typografie fluid mit `clamp()`**, ein Verhältnis, keine Zufallswerte:
> ```css
> --step--1: clamp(.83rem, .78rem + .22vw, .94rem);
> --step-0:  clamp(1rem,   .95rem + .3vw,  1.15rem);
> --step-3:  clamp(2.2rem, 1.7rem + 2.4vw, 3.6rem);
> --step-6:  clamp(3.6rem, 2.2rem + 6.8vw, 8rem);   /* Display */
> ```
> - Variable Fonts, selbst gehostet, auf die benutzten Zeichen reduziert (Subsetting), `font-display: swap`,
>   Fallback metrisch angeglichen (`size-adjust`), damit nichts springt.
> - Display-Größen bekommen negatives Tracking (−0.02em bis −0.04em), Kleintext positives.
> - Zeilenlänge 60–75 Zeichen. Zeilenhöhe fällt mit steigender Schriftgröße: 1.6 im Fließtext, 0.95 im Display.
> - Bellowerk: **Lora** als Serife für Display und Fließtext, dazu eine schmale Grotesk für
>   Bedienelemente, Preise und Tabellen. Zahlen immer `font-variant-numeric: tabular-nums`.
>
> **Raum** als eine geometrische Reihe: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256.
> Sektionsabstände skalieren mit dem Viewport, Bauteilabstände nicht.
>
> **Raster:** 12 Spalten, Rinne `clamp(16px, 2.4vw, 32px)`, Außenrand nie unter 16px.
> Ein durchgehendes `grid-template-columns` auf Seitenebene, Sektionen greifen per benannter Linie
> hinein — so bleibt alles auf derselben Kante, auch wenn eine Sektion vollflächig ist.
>
> **Oberfläche und Glanz** (der Teil, den fast alle falsch machen):
> ```css
> .karte{
>   background: linear-gradient(180deg, oklch(100% 0 0/.06), oklch(100% 0 0/0) 42%), var(--flaeche);
>   box-shadow:
>     0 1px 1px oklch(0% 0 0/.05),      /* Kontaktschatten, hart und klein */
>     0 8px 24px -8px oklch(0% 0 0/.18), /* Formschatten */
>     inset 0 1px 0 oklch(100% 0 0/.12); /* Lichtkante oben, nur oben */
> }
> ```
> - Licht kommt von oben. Deshalb Lichtkante nur oben, Schatten nur unten.
> - `backdrop-filter` höchstens an zwei Stellen pro Seite (Navigation, Warenkorb-Schublade).
> - Gegen Streifenbildung in Verläufen eine Rauschebene legen: SVG-`feTurbulence`, 3–5 % Deckkraft,
>   `pointer-events:none`. Das ist der Unterschied zwischen "Verlauf" und "Material".
> - Radien in Stufen (4/8/12/20/999) und ineinander verschachtelt korrekt: innen = außen minus Abstand.
>
> Ergebnis dieses Blocks ist eine Datei `tokens.css` plus eine Bauteil-Übersicht, auf der jedes
> Element in allen Zuständen zu sehen ist.

---

## Block 4 — FX-Studio: Bewegung und Effekte

> Das FX-Studio liefert die Handschrift. Es liefert sie sparsam.
>
> **Werkzeuge**
> - **GSAP + ScrollTrigger** für Choreografie über mehrere Elemente und Scroll-Abschnitte
> - **Lenis** für gedämpftes Scrollen (Dauer ≈ 1.1, sofort aus bei `prefers-reduced-motion`)
> - **Three.js oder OGL** für den einen WebGL-Moment pro Seite
> - **Rive** für interaktive Zustände (Cursor, Schalter), **Lottie** nur als Rückfallebene
> - Native `scroll-driven animations` (`animation-timeline: view()`) überall dort, wo sie reichen —
>   das spart die Bibliothek komplett
> - `View Transitions API` für Seitenwechsel und Filterwechsel im Katalog
>
> **Zeiten und Kurven**
> ```css
> --dauer-mikro: 120ms;  /* Hover, Fokus */
> --dauer-klein: 240ms;  /* Aufklappen, Schublade */
> --dauer-gross: 520ms;  /* Sektionswechsel, Seitenübergang */
> --kurve-raus:  cubic-bezier(.22,1,.36,1);    /* Eintritte */
> --kurve-rein:  cubic-bezier(.55,0,.68,.18);  /* Austritte */
> ```
> Eintritte langsam ausklingen, Austritte schnell verschwinden. Staffelung 40–60 ms pro Element,
> maximal sieben Elemente in einer Kette, danach als Gruppe.
>
> **Harte Regeln**
> - Animiert werden nur `transform`, `opacity`, `filter`, `clip-path`. Niemals `top`, `left`,
>   `width`, `height` — das kostet Layout und ruckelt.
> - **Ein** schwerer Effekt pro Seite. Nicht zwei. Der Rest ist CSS.
> - WebGL lädt verzögert (`IntersectionObserver`), pausiert außerhalb des Sichtfelds
>   (`requestAnimationFrame` stoppen), und startet gar nicht bei: `prefers-reduced-motion`,
>   `navigator.hardwareConcurrency <= 4`, `navigator.connection.saveData`, Akku unter 20 %.
>   Für jeden Effekt existiert ein statisches Standbild als Ersatz — das ist Pflichtlieferung, nicht Kür.
> - `prefers-reduced-motion: reduce` schaltet auf reine Ein-/Ausblendung um, nichts fliegt mehr.
>   Die Seite muss in diesem Zustand vollständig verständlich bleiben.
> - Nichts bewegt sich beim Laden, bevor die Schrift steht (Layoutsprung = Abnahme nicht bestanden).
>
> **Der eine WebGL-Moment für Bellowerk**
> Ein Fragment-Shader auf einer Leder-Normal-Map: Der Lichtreflex auf der Narbenseite folgt dem
> Mauszeiger, Messing bekommt eine anisotrope Spiegelung. Der Nutzer streicht mit der Maus über das
> Leder und sieht die Struktur kippen. Das ist kein Effekt, das ist ein Produktargument — man sieht,
> dass die Oberfläche echt ist. Mobil: dieselbe Szene, gesteuert vom Neigungssensor, mit Rückfall
> auf ein AVIF-Standbild.
>
> **Verboten:** Partikel ohne Bezug, Parallax auf jedem zweiten Element, Text der buchstabenweise
> hüpft, automatisch startende Videohintergründe mit Ton, Cursor-Verfolger die nichts tun,
> Ladebalken vor Inhalten die schon da sind, Scroll-Kapern über mehr als eine Sektion.

---

## Block 5 — Bildregie und die KI-Pipeline (Nano Banana)

> Bilder entscheiden über die Preiswahrnehmung. Diese Regel steht über allem:
>
> **Produktbilder sind echte Fotos. Immer.** Das Verkaufsargument der Marke ist der Praxistest an
> echten Hunden. Ein generiertes Produktfoto würde genau das Argument zerstören, das die Preise
> von 69–139 EUR trägt — und wäre als Werbung mit einem Produkt, das so nie fotografiert wurde,
> rechtlich angreifbar.
>
> **Wofür Nano Banana (Gemini-Bildmodell) trotzdem eingesetzt wird — und das ist viel:**
> 1. **Layout-Comps und Moodboards** vor dem Fototermin: Bildschnitt, Licht, Anmutung durchspielen,
>    bis der Art Director weiß, welches Foto entstehen muss.
> 2. **Aufnahmeanweisung als Bild.** Statt "Nahaufnahme der Schnalle bei Seitenlicht" ein Bild,
>    das Björn beim Fotografieren nachbaut. Spart Termine.
> 3. **Freistellen, Retusche, Erweiterung.** Echtes Foto rein, Hintergrund sauber, Bildrand für
>    andere Seitenverhältnisse erweitern (16:9 fürs Web, 4:5 für Instagram, 1:1 fürs Raster).
> 4. **Texturen und Hintergründe:** Papierfaser, Werkstattbeton, Leinen, Rauschebenen, Verlaufsflächen.
>    Diese sind keine Produktaussage, hier ist Generierung unproblematisch.
> 5. **Verpackungs- und Schildansichten** für interne Abstimmung mit dem Hersteller.
> 6. **Bildvarianten für A/B-Tests** von Sektionshintergründen.
>
> **Prompt-Bauplan für die Bildpipeline** (jedes Feld wird gefüllt):
> `[Motiv] · [Material und Zustand] · [Objektiv und Abstand] · [Licht: Quelle, Richtung, Härte] ·
> [Hintergrund] · [Farbstimmung] · [Seitenverhältnis] · [was NICHT im Bild sein darf]`
>
> Beispiel: *Braunes Fettleder-Halsband mit massiver Messingschnalle, liegend auf rohem Eichenholz,
> 85 mm Makro aus 40 cm, hartes Seitenlicht von links durch ein Werkstattfenster, Hintergrund
> unscharf und dunkel, warme gedämpfte Farben, 4:5, keine Nähte, keine Nieten, kein Kunststoff,
> kein Text im Bild.*
>
> **Ausgabe und Technik**
> - AVIF zuerst, WebP als Rückfall, JPEG nur als letzte Ebene. `<picture>` mit `srcset` in fünf Breiten.
> - `width` und `height` immer gesetzt, `aspect-ratio` im CSS — CLS von 0.00 ist die Vorgabe.
> - Erstes Bild über der Falz: `fetchpriority="high"`, `loading="eager"`, alles andere `lazy` und
>   `decoding="async"`.
> - Kunstgerechter Zuschnitt: mobil ein anderer Ausschnitt als am Desktop, nicht dasselbe Bild gestaucht.
> - Jedes Bild bekommt einen echten Alternativtext, der das Produkt beschreibt — nicht "Bild1.jpg".
> - Kennzeichnung: KI-erzeugte oder KI-veränderte Bilder werden in der Bilddatenbank als solche
>   geführt (`sourcing/`-Konvention: Dateiname endet auf `-ki`). Produktseiten enthalten keine.

---

## Block 6 — Shopsystem, Plugins, Technik

> **Zwei Wege, einer wird gewählt und begründet:**
>
> **Weg A — Shopify + Hydrogen (Empfehlung für Bellowerk).** Zahlung, Steuer, Versandschein,
> Retoure und Buchhaltung sind gelöst und rechtssicher, die Gestaltungsfreiheit bleibt trotzdem
> vollständig, weil Hydrogen ein eigenes React-Frontend auf die Storefront-API setzt. Björn führt
> eine Manufaktur, keine IT-Abteilung: laufender Betrieb schlägt letzte 5 % Kontrolle.
> Kosten: Grundgebühr plus Transaktionsanteil.
>
> **Weg B — Next.js (App Router) + Medusa oder Saleor, selbst gehostet.** Volle Kontrolle, keine
> Umsatzbeteiligung, aber Zahlungsanbindung, Steuerlogik, Updates und Ausfallsicherheit liegen bei
> uns. Nur wählen, wenn dauerhaft jemand die Wartung übernimmt.
>
> **Baukasten (Weg A)**
> - Frontend: Hydrogen (React, Remix), Vite, TypeScript strikt
> - Gestaltung: Tailwind mit **eigenen** Tokens aus Block 3 (nie die Standardpalette ausliefern),
>   dazu handgeschriebenes CSS für alles Materialhafte
> - Inhalte: Shopify Metaobjects für Redaktionsinhalte, alternativ Sanity, wenn Björn frei
>   layouten können soll
> - Suche: Shopify Search & Discovery (kostenlos) — Algolia erst ab ~200 Artikeln
> - Bilder: Shopify CDN mit Transformationsparametern, AVIF erzwungen
> - Bewertungen: Judge.me oder Trusted Shops mit Käuferschutz (in Deutschland das stärkere
>   Vertrauenssignal)
> - Zahlung: Shopify Payments (Karte, Apple Pay, Google Pay), PayPal, Klarna Rechnung, SEPA.
>   **Kauf auf Rechnung ist in Deutschland kein Extra, sondern Grundausstattung.**
> - Versand: DHL-Anbindung, Sendungsverfolgung in der Bestellbestätigung, GoGreen ausgewiesen
> - Mail: Klaviyo für Abbruchstrecke und Neuigkeiten (DOI-Verfahren, Nachweis speichern)
> - Zustimmung: Consent-Banner mit echtem "Alle ablehnen" auf gleicher Ebene wie "Annehmen",
>   Messung erst nach Zustimmung, serverseitige Messung wo möglich
> - Messung: Analytics ohne Personenbezug (Plausible oder Fathom) plus Shopify-eigene Auswertung
>
> **Bausteine, die diese Seite braucht** (jeder in allen Zuständen gestaltet)
> Navigation mit Vorschau-Menü · Warenkorb-Schublade mit Restbetrag bis Versandfrei ·
> Produktkarte · Produktseite mit Bildergalerie und Zoom · Varianten- und Größenwahl ·
> **Größenfinder** (Halsumfang messen → Größe, mit Zeichnung) · Materialkunde-Sektion ·
> Pflegehinweise · Praxistest-Sektion mit echten Hundenamen und Dauer · Bewertungen mit Fotos ·
> häufige Fragen mit strukturierten Daten · Anfrageformular für Gassi-Service, Pension, Training ·
> Newsletter mit ehrlichem Nutzenversprechen · Fußzeile mit allen Pflichtangaben
>
> **Rechtliches, deutscher Onlinehandel** (Fehlt eines, ist die Abnahme nicht bestanden)
> Impressum · Datenschutzerklärung · AGB · Widerrufsbelehrung mit Muster-Widerrufsformular ·
> Versandkosten und Lieferzeit vor Kaufabschluss sichtbar · Preisangabenverordnung: Endpreis
> inklusive Umsatzsteuer, Grundpreis wo nötig · Bestellknopf beschriftet mit **"Zahlungspflichtig
> bestellen"** · Bestellübersicht vor Abschluss · Zustimmungsbanner nach TDDDG · Batterie- und
> Verpackungshinweise, sofern zutreffend · Barrierefreiheitsstärkungsgesetz: seit Juni 2025 gilt
> für Onlinehandel EN 301 549, praktisch WCAG 2.1 AA — wir liefern 2.2 AA.

---

## Block 7 — Text und Werbewirkung

> Der Text trägt die Hälfte. Regeln:
> - **Claim:** höchstens sieben Wörter, keine Adjektivketten, sagt etwas, das der Wettbewerb nicht
>   sagen kann. "Vegetabil gegerbt, Handarbeit, Messing" sagt jeder — das ist die Eintrittskarte,
>   kein Argument. Der Praxistest ist das Argument.
> - **Headlines** behaupten etwas Konkretes. "Eine Saison an fremden Hunden, bevor es in den Shop geht."
>   Nicht "Qualität, die man spürt."
> - **Erster Satz nach der Headline** liefert den Beweis, nicht die Wiederholung.
> - **Produkttexte** in dieser Reihenfolge: Was ist es · Für welchen Hund · Woraus genau
>   (Material, Stärke in mm, Beschlag) · Was ist der Praxistest gewesen · Wie pflegt man es ·
>   Was passiert nach fünf Jahren.
> - **Zahlen statt Eigenschaftswörter.** "3,00 m, sechs Führlängen, Ringe bei 45/140/245 cm"
>   schlägt "vielseitig verstellbar".
> - **Mikrotexte** sind Gestaltung: Knopfbeschriftungen, Fehlermeldungen, leerer Warenkorb,
>   Ausverkauft-Hinweis, Versandschwelle. Kein "Ups!", kein "Oh nein!".
> - **Verboten:** Willkommen bei · Wir bieten Ihnen · Lassen Sie sich verzaubern · Qualität die
>   überzeugt · nicht nur … sondern auch · Ausrufezeichen in Fließtext · Superlative ohne Beleg ·
>   erfundene Rabatt-Countdowns · durchgestrichene Fantasiepreise.

---

## Block 8 — Auffindbarkeit

> - Eine `h1` pro Seite, Überschriften lückenlos gestuft, echte Landmarks (`header`, `nav`, `main`,
>   `footer`), Sprache im `html`-Tag gesetzt.
> - Strukturierte Daten als JSON-LD: `Organization`, `LocalBusiness` (Hamburg, Öffnungszeiten),
>   `Product` mit `offers` und `aggregateRating` (nur wenn Bewertungen echt sind), `BreadcrumbList`,
>   `FAQPage`. Mit dem Rich-Results-Test geprüft, Beleg in die Abnahme.
> - Titel unter 60 Zeichen, Beschreibung unter 155, für jede Seite eigen geschrieben — nie generiert.
> - Sprechende URLs ohne Parameterketten, `canonical` gesetzt, Sitemap und `robots.txt` vorhanden.
> - Open-Graph-Bilder je Seite, 1200 × 630, mit Produktbild und Wortmarke.
> - Ladezeit ist Rangfaktor: Block 9 gilt auch hier.

---

## Block 9 — Budgets (Abnahmebedingungen, keine Ziele)

| Größe | Grenze | Gemessen mit |
|---|---|---|
| Largest Contentful Paint (mobil, 4G gedrosselt) | ≤ 1.8 s | Lighthouse, Feldwerte |
| Interaction to Next Paint | ≤ 200 ms | CrUX / Web-Vitals |
| Cumulative Layout Shift | ≤ 0.05 | Lighthouse |
| JavaScript beim ersten Laden, gzip | ≤ 180 KB | Bundle-Analyse |
| CSS gesamt, gzip | ≤ 60 KB | Bundle-Analyse |
| Schriftdateien | ≤ 2 Familien, ≤ 120 KB | Netzwerk-Auswertung |
| Größtes Bild über der Falz | ≤ 200 KB AVIF | Netzwerk-Auswertung |
| Lighthouse Leistung / Barrierefreiheit / SEO | ≥ 95 / 100 / 100 | Lighthouse mobil |
| Kontrast Fließtext | ≥ 4.5:1 | axe |
| Bedienbar nur mit Tastatur | vollständig | Handprüfung |

Reißt ein Wert, wird der Effekt gestrichen, nicht der Grenzwert erhöht.

---

## Block 10 — Abnahmetor

> Der Qualitätsprüfer geht diese Liste durch und schreibt zu jedem Punkt **bestanden** oder
> **nicht bestanden mit Grund**. Ohne vollständige Liste gibt es kein "fertig".
>
> **Gestaltung**
> 1. Die eine Idee der Seite lässt sich in einem Satz sagen und jede Sektion zahlt darauf ein.
> 2. Ohne Bilder funktioniert die Seite immer noch.
> 3. Kein Bauteil erinnert an eine erkennbare Vorlage.
> 4. Hell und dunkel sind beide vollständig gestaltet.
> 5. Alle Zustände existieren: leer, Laden, Fehler, Erfolg, ausverkauft, Grenzwerte.
>
> **Technik**
> 6. Alle Budgets aus Block 9 eingehalten, Messwerte beigelegt.
> 7. Bei 320 px Breite kein waagerechtes Scrollen, bei 2560 px keine Wüste.
> 8. Tastaturbedienung vollständig, Fokusring immer sichtbar und gestaltet, Reihenfolge logisch.
> 9. `prefers-reduced-motion` geprüft: Seite bleibt verständlich.
> 10. Ohne JavaScript sind Inhalte und Navigation weiter erreichbar.
> 11. Geprüft in Safari (iOS und macOS), Chrome, Firefox — `backdrop-filter` und WebGL besonders.
>
> **Shop**
> 12. Vollständiger Kauf durchgespielt: Warenkorb → Kasse → Zahlung (Testmodus) → Bestätigungsmail.
> 13. Versandkosten und Lieferzeit vor dem Kaufabschluss sichtbar.
> 14. Bestellknopf heißt "Zahlungspflichtig bestellen".
> 15. Impressum, Datenschutz, AGB, Widerruf vorhanden und aus der Fußzeile erreichbar.
> 16. Zustimmungsbanner mit gleichwertigem "Alle ablehnen", Messung startet erst danach.
>
> **Marke**
> 17. Kein ausgeschlossener Werkstoff abgebildet oder erwähnt (Nähte, Nieten, Stahl, Kunststoff,
>     Klickverschluss, Gurtband).
> 18. Keine Geschirre, keine reine Handelsware, kein Preisargument, kein Windhund-Einstieg.
> 19. Preise im Rahmen: Halsband 69–99, Leine 89–139, Zubehör 25–59 EUR.
> 20. Kein KI-erzeugtes Bild auf einer Produktseite.

---

## Block 11 — Lieferumfang

> 1. **Leitidee** in einem Satz plus drei Sätze Begründung
> 2. **`tokens.css`** — Farbe, Typografie, Raum, Radien, Schatten, Bewegung
> 3. **Bauteilübersicht** als eigene Seite, jedes Element in allen Zuständen
> 4. **Seiten:** Startseite, Katalog, Produktseite, Warenkorb, Kasse, Über die Werkstatt,
>    Leistungen (Gassi, Pension, Training), Kontakt, Rechtsseiten
> 5. **Aufnahmeliste** für Björn: jedes benötigte Foto mit Motiv, Ort, Licht, Ausschnitt, Format
> 6. **Bildpipeline-Prompts** für Nano Banana, fertig zum Einsetzen
> 7. **Messprotokoll** zu Block 9
> 8. **Ausgefülltes Abnahmetor** aus Block 10
> 9. **Übergabe:** wie man Produkte anlegt, Preise ändert, Bilder tauscht — in einer Seite,
>    für jemanden, der Leder verarbeitet, nicht Code
>
> Kein Geld wird ausgegeben. Tarife, Domains, kostenpflichtige Erweiterungen und Fototermine
> gehen als Entscheidung mit Preis und Begründung an Björn.

---

## Kurzfassung zum Kopieren

```
Du führst ein Designstudio auf dem Niveau der weltbesten Agenturen und baust für [MARKE] eine
[Website / Shop]. Besetze nacheinander diese Rollen und kennzeichne jeden Abschnitt: Creative
Director, Art Director, Motion- und FX-Director, Bildregie, Frontend, Commerce, Texter,
Qualitätsprüfer.

Auftrag: [Produkt] · [Preislage] · [Zielgruppe] · [das eine Verkaufsargument] · [Tonfall] ·
[harte Ausschlüsse] · Ziel der Seite: [Verkauf / Anfrage].

Regeln, die nicht verhandelbar sind:
1. Eine Idee trägt die Seite, formuliere sie zuerst in einem Satz. Ein Gedanke pro Bildschirm.
2. Bau zuerst das Designsystem: OKLCH-Farbleitern, fluide Typoskala mit clamp(), Raumreihe,
   12-Spalten-Raster, Schatten in Lagen mit Lichtkante nur oben, Rauschebene gegen Streifen.
   Kein reines Schwarz, kein reines Weiß. Hell und dunkel gleichzeitig.
3. Typografie ist die Hauptleistung: Sprung Display zu Fließtext mindestens 1:4, variable Fonts
   selbst gehostet und subgesetzt, negatives Tracking im Display, Zeilenlänge 60–75 Zeichen.
4. Layout asymmetrisch mit Absicht, größter Abstand mindestens achtmal der kleinste.
5. FX-Studio: GSAP mit ScrollTrigger, Lenis, ein einziger WebGL-Moment pro Seite mit statischem
   Ersatzbild, native scroll-driven animations wo sie reichen, View Transitions für Seitenwechsel.
   Nur transform/opacity/filter/clip-path animieren. 120/240/520 ms, Staffelung 40–60 ms.
   Alles aus bei prefers-reduced-motion, schwachem Gerät oder Datensparmodus.
6. Bilder: Produktfotos sind echte Fotos. KI-Bilder (Nano Banana) nur für Comps, Moodboards,
   Aufnahmeanweisungen, Freisteller, Retusche, Texturen und Hintergründe. AVIF, srcset in fünf
   Breiten, Maße gesetzt, erstes Bild fetchpriority=high, echter Alternativtext.
7. Shop: Shopify Hydrogen (oder Next.js plus Medusa, begründet). Kauf auf Rechnung, PayPal,
   Klarna, Apple/Google Pay. Pflicht: Impressum, Datenschutz, AGB, Widerruf, Versandkosten vor
   Kaufabschluss, Endpreise inklusive Steuer, Knopf "Zahlungspflichtig bestellen", Consent mit
   echtem "Alle ablehnen", WCAG 2.2 AA.
8. Text: Claim unter sieben Wörtern, Headlines behaupten Konkretes, Zahlen statt Eigenschaftswörter,
   Mikrotexte mitgestaltet. Verboten: Willkommen bei, Wir bieten Ihnen, Qualität die überzeugt,
   Superlative ohne Beleg, erfundene Rabatt-Countdowns.
9. Budgets als Abnahmebedingung: LCP unter 1,8 s mobil, INP unter 200 ms, CLS unter 0,05,
   JS unter 180 KB gzip, CSS unter 60 KB, Lighthouse mindestens 95/100/100. Reißt ein Wert,
   fliegt der Effekt raus, nicht der Grenzwert.
10. Alle Zustände gestalten: leer, Laden, Fehler, Erfolg, ausverkauft, Grenzwerte.

Liefere: Leitidee in einem Satz · tokens.css · Bauteilübersicht mit allen Zuständen · die Seiten ·
Aufnahmeliste für echte Fotos · Bildprompts · Messwerte · ausgefülltes Abnahmetor.

Schreib nach jeder Sektion selbst hin, welchem bekannten Muster sie ähnelt, und überarbeite sie,
bis die Antwort "keinem" lautet. Gib kein Geld aus; Kosten gehen als Entscheidung an mich.
```
