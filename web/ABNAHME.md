# Abnahmetor — Shop, Stand 12.09.2026

Geprüft gegen `.claude/skills/website-highend/references/qualitaetstor.md`, 20 Punkte.
Gegenstand: `tokens.css`, Katalog, vier Produktseiten, Warenkorb, Kasse, fünf Rechtsseiten.

**Gesamturteil: nicht bestanden.** Neun Punkte bestanden, vier nicht bestanden, sieben nicht
prüfbar. Das ist erwartbar — ohne echte Fotos, echte Prüfdaten und die Anbieterangaben *kann*
der Shop nicht bestehen. Die Liste sagt, woran es liegt.

Gemessen wurde mit Chromium über Playwright: 13 Seiten × 4 Breiten (320, 768, 1440, 2560 px),
dazu Tastaturdurchlauf, Lauf ohne JavaScript und mit `prefers-reduced-motion: reduce`.
Kontraste gegen WCAG 2.2 gerechnet.

## Gestaltung

| # | Punkt | Urteil |
|---|---|---|
| 1 | Leitidee in einem Satz, jede Sektion zahlt ein | **bestanden.** „Das Leder wurde vor dem Verkauf benutzt." Praxistest hat auf jeder Produktseite eine eigene Sektion, kein Halbsatz. Der Katalog erklärt, warum drei Stücke *nicht* bestellbar sind — auch das zahlt ein. |
| 2 | Ohne Bilder funktioniert die Seite | **bestanden, unfreiwillig bewiesen.** Im Prüflauf waren weder Fotos noch Google Fonts erreichbar. Aufbau und Typografie tragen allein, die Ersatzschriften greifen. |
| 3 | Kein Bauteil erinnert an eine erkennbare Vorlage | **bestanden, mit Notizen** (siehe unten) |
| 4 | Hell und dunkel beide vollständig gestaltet | **nicht bestanden.** Richtung 03 ist bewusst einfarbig dunkel, eine Hell-Variante gibt es nicht. Das war die Entscheidung bei der Richtungswahl, steht so in der Startseite. Entweder der Punkt wird für dieses Projekt gestrichen oder eine Hell-Variante muss gebaut werden. **Entscheidung Björn.** |
| 5 | Alle Zustände: leer, Laden, Fehler, Erfolg, ausverkauft | **bestanden.** Leer: Warenkorb und Bewertungen. Laden: Kaufknopf, Skelett in `tokens.css`. Fehler: Feldfehler an der Kasse, umschaltbar. Ausverkauft: Größe XL und drei Katalogkarten. Erfolg: „Im Warenkorb ✓". |

### Notizen zu Punkt 3

- **Produktseite** ähnelte dem üblichen Galerie-links-Kaufblock-rechts. Geändert: der Preisblock
  trägt die Herkunftsangabe als gleichrangige Zeile statt als Kleingedrucktes, und die drei
  Merkmale unter dem Kaufknopf sind nummeriert wie ein Prüfprotokoll, nicht als Icon-Dreier.
- **Katalog** ähnelte dem Shop-Raster mit Filterleiste. Geändert: die Nummer läuft durch die
  Kollektion statt je Warengruppe, nicht bestellbare Stücke bleiben sichtbar mit Grund, und
  Zubehör steht abgesetzt ohne Nummer.
- **Kasse** ähnelte dem Standard-Checkout. Geändert: Zahlarten stehen vor der Adresse, die
  Telefonnummer ist ausdrücklich kein Pflichtfeld, und der Satz zum Vertragsschluss steht
  *unter* dem Knopf, wo er gelesen wird.
- **Warenkorb** ähnelte der Schublade mit Versandbalken. Geändert: der Balken nennt die Grenze
  in Zahlen statt „nur noch ein bisschen", und der Hinweis auf das Rückgaberecht steht neben
  der Ware, nicht im Fußbereich.

## Technik

| # | Punkt | Urteil |
|---|---|---|
| 6 | Alle Budgets eingehalten, Messwerte beiliegend | **nicht bestanden.** CSS 5,6 KB gzip (Grenze 60) ✓. JavaScript höchstens 1,9 KB pro Seite, keine Bibliothek (Grenze 180) ✓. **Schriften: drei Familien, Grenze sind zwei.** Archivo, Bodoni Moda, IBM Plex Mono. Vorschlag: IBM Plex Mono streichen und die Monoschrift durch Archivo mit Sperrung ersetzen — betrifft Artikelnummern, Preise und Augenbrauen. Kostet Charakter, hält das Budget. **Entscheidung Björn.** LCP, INP, CLS, TTFB und Lighthouse sind von hier aus nicht messbar (kein Server, keine Netzdrosselung). |
| 7 | Bei 320 px kein waagerechtes Scrollen, bei 2560 px keine leere Fläche | **bestanden, nach vier Korrekturen.** Erster Lauf: alle 13 Seiten liefen bei 320 px über, bis zu 222 px. Ursachen: fehlendes `min-width:0` an Rasterkindern, Wortmarke und Warenkorbknopf nebeneinander zu breit, `white-space:nowrap` im Warenkorbpreis, Unterstrich-Ketten im Muster-Widerrufsformular. Alle vier behoben, zweiter Lauf sauber auf 13 Seiten × 4 Breiten. |
| 8 | Tastatur vollständig, Fokusring sichtbar, Reihenfolge logisch, Sprungmarke | **bestanden.** Erste Tabulatorstation ist „Zum Inhalt springen". Zwölf Stationen durchlaufen, überall 2 px Fokusring in Messing, Reihenfolge folgt dem Lesefluss. |
| 9 | `prefers-reduced-motion: reduce` geprüft | **bestanden.** Übergangsdauer fällt auf 0,00001 s, die Seite bleibt vollständig verständlich. Der Messing-Glanzlauf auf der Startseite steht still. |
| 10 | Ohne JavaScript Inhalte und Navigation erreichbar | **bestanden.** Ohne JavaScript: Startseite 5.294 Zeichen Text und 25 Verweise, Produktseite 4.494 Zeichen und 24 Verweise, Katalog 3.547 Zeichen und 23 Verweise. Verloren gehen nur Komfortfunktionen: Filter, Mengenwähler, Galerieumschaltung. |
| 11 | Geprüft in Safari, Chrome, Firefox | **nicht prüfbar.** Nur Chromium vorhanden. Besonders zu prüfen bleiben `backdrop-filter` in der Kopfleiste, `:has()` in der Zahlartenwahl und der WebGL-Shader auf der Startseite. |
| 12 | Bildschirmleser-Durchgang | **nicht prüfbar.** Vorbereitet ist: Sprungmarke, `aria-label` an allen Knöpfen ohne Text, `aria-live` an Mengen und Trefferzahl, `aria-current` in der Navigation, Tabellen mit `caption`, `h1` auf jeder Seite (an der Kasse für Bildschirmleser, optisch tragen die Schritte). |

## Shop

| # | Punkt | Urteil |
|---|---|---|
| 13 | Vollständiger Kauf durchgespielt bis Bestätigungsmail | **nicht prüfbar.** Es gibt noch kein Shopsystem. Der Weg Katalog → Produkt → Warenkorb → Kasse ist als Entwurf durchklickbar und endet dort mit einem Hinweis. |
| 14 | Versandkosten und Lieferzeit vor Kaufabschluss sichtbar | **bestanden.** Beides steht im Preisblock jeder Produktseite, im Warenkorb, an der Kasse und in der Fußzeile jeder Seite. Maschinell geprüft. |
| 15 | Bestellknopf heißt „Zahlungspflichtig bestellen" | **bestanden.** Genau einmal vorhanden, genau so beschriftet. |
| 16 | Impressum, Datenschutz, AGB, Widerruf vorhanden und aus der Fußzeile erreichbar | **nicht bestanden.** Vorhanden und von jeder Seite mit einem Klick erreichbar, aber **inhaltlich unvollständig**: Anbietername, Anschrift, Kontaktweg und USt-IdNr. fehlen, weil ich sie nicht kenne und nicht erfinde. Alle Lücken sind auf der Seite orange unterstrichen. Vor der Veröffentlichung anwaltlich prüfen lassen. |
| 17 | Zustimmungsbanner mit gleichrangigem „Alle ablehnen", keine Messung vorher | **bestanden** als Entwurf: gleiche Ebene, gleiche Größe, gleiche Gestaltungswertigkeit, kein vorangekreuztes Kästchen. Dass wirklich nichts vor der Zustimmung misst, entscheidet sich erst am eingebauten Shopsystem. |

## Marke

| # | Punkt | Urteil |
|---|---|---|
| 18 | Kein ausgeschlossener Werkstoff abgebildet oder erwähnt | **bestanden.** Nähte, Nieten, Stahl, Zinkdruckguss, Kunststoff, Klickverschlüsse und Gurtband kommen nur in der Ausschlussliste vor — als das, was nicht verbaut wird. Maschinell durchsucht. |
| 19 | Keine Geschirre, keine Handelsware, kein Preisargument, kein Einstieg über Windhunde; Preise im Rahmen | **bestanden.** Keine Geschirre. Kein Rabatt, kein Countdown, kein durchgestrichener Preis. Windhunde kommen einmal vor — als ausdrückliche Absage auf der Produktseite. Preise: 39 / 89 / 99 / 129 €, alle im Rahmen. |
| 20 | Kein KI-erzeugtes Bild auf Produkt-, Katalog- oder Praxistestseite | **bestanden.** Es gibt überhaupt kein Bild. Jede Bildfläche trägt ihre Aufnahmeanweisung als Beschriftung. |

## Was bis zur Abnahme fehlt

1. Elf echte Fotos aus `web/aufnahmen/`
2. Echte Prüfdaten für den Praxistest auf vier Produktseiten — oder die Sektion fällt weg
3. Anbieterangaben für die Rechtsseiten, danach anwaltliche Durchsicht
4. **Kleinunternehmerregelung ja oder nein.** Ändert jede Preisangabe im ganzen Shop
5. **Wer trägt die Rücksendekosten.** Muss in Widerrufsbelehrung und Versandseite gleich stehen
6. Entscheidung zu Punkt 4 (Hell-Variante) und Punkt 6 (dritte Schriftfamilie)
7. Shopsystem, danach Punkt 13 und 17 erneut prüfen
8. Prüfung in Safari und Firefox, Bildschirmleser-Durchgang
9. Startseite auf `tokens.css` umstellen — sie trägt ihr Designsystem noch als Kopie im Kopf,
   und zwei Kopien laufen auseinander. Bei der 320-px-Korrektur ist das schon passiert: die
   Änderung musste an zwei Stellen gemacht werden.
