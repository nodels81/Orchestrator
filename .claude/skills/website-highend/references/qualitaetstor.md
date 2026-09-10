# Budgets und Abnahmetor

## Budgets — Abnahmebedingungen, keine Ziele

| Größe | Grenze | Gemessen mit |
|---|---|---|
| Largest Contentful Paint (mobil, 4G gedrosselt) | ≤ 1.8 s | Lighthouse, Feldwerte |
| Interaction to Next Paint | ≤ 200 ms | CrUX, web-vitals |
| Cumulative Layout Shift | ≤ 0.05 | Lighthouse |
| Time to First Byte | ≤ 600 ms | WebPageTest |
| JavaScript beim ersten Laden, gzip | ≤ 180 KB | Bundle-Analyse |
| CSS gesamt, gzip | ≤ 60 KB | Bundle-Analyse |
| Schriften | ≤ 2 Familien, ≤ 120 KB gesamt | Netzwerk-Auswertung |
| Größtes Bild über der Falz | ≤ 200 KB AVIF | Netzwerk-Auswertung |
| Lighthouse Leistung (mobil) | ≥ 95 | Lighthouse |
| Lighthouse Barrierefreiheit / SEO | 100 / 100 | Lighthouse |
| Kontrast Fließtext | ≥ 4.5:1 | axe DevTools |
| Fehler in axe | 0 | axe DevTools |

**Reißt ein Wert, wird der Effekt gestrichen, nicht der Grenzwert erhöht.**
Lighthouse allein reicht nicht: INP ist nur im Feld ehrlich messbar, deshalb `web-vitals`
einbauen und nach zwei Wochen nachmessen.

## Abnahmetor — 20 Punkte

Der Qualitätsprüfer schreibt zu jedem Punkt **bestanden** oder **nicht bestanden, Grund**.
Ohne vollständig ausgefüllte Liste gibt es kein "fertig". Er arbeitet gegen den Entwurf, nicht für ihn.

### Gestaltung
1. Die Leitidee lässt sich in einem Satz sagen, und jede Sektion zahlt darauf ein.
2. Ohne Bilder funktioniert die Seite immer noch — Aufbau und Typografie tragen allein.
3. Kein Bauteil erinnert an eine erkennbare Vorlage. Zu jeder Sektion ist notiert, welchem
   Muster sie ähnelte und was dagegen geändert wurde.
4. Hell und dunkel sind beide vollständig gestaltet, nicht invertiert.
5. Alle Zustände existieren: leer, Laden, Fehler, Erfolg, ausverkauft, zu lange Texte, fehlende Bilder.

### Technik
6. Alle Budgets eingehalten, Messwerte liegen bei.
7. Bei 320 px kein waagerechtes Scrollen, bei 2560 px keine leere Fläche.
8. Tastaturbedienung vollständig, Fokusring immer sichtbar und gestaltet, Reihenfolge logisch,
   Sprungmarke zum Inhalt vorhanden.
9. `prefers-reduced-motion: reduce` geprüft — Seite bleibt vollständig verständlich.
10. Ohne JavaScript sind Inhalte und Navigation weiter erreichbar.
11. Geprüft in Safari (iOS und macOS), Chrome und Firefox. Besonders: `backdrop-filter`,
    WebGL, `View Transitions`, `scroll-driven animations`.
12. Bildschirmleser-Durchgang über Startseite und Produktseite gemacht (VoiceOver oder NVDA).

### Shop
13. Vollständiger Kauf durchgespielt: Warenkorb → Kasse → Zahlung im Testmodus → Bestätigungsmail.
14. Versandkosten und Lieferzeit vor dem Kaufabschluss sichtbar.
15. Bestellknopf heißt "Zahlungspflichtig bestellen".
16. Impressum, Datenschutz, AGB, Widerruf vorhanden und aus der Fußzeile erreichbar.
17. Zustimmungsbanner mit gleichrangigem "Alle ablehnen"; keine Messung vor Zustimmung.

### Marke
18. Kein ausgeschlossener Werkstoff abgebildet oder erwähnt: Nähte, Nieten, Stahl, Kunststoff,
    Klickverschlüsse, Gurtband.
19. Keine Geschirre, keine reine Handelsware ohne Markenbezug, kein Preisargument,
    kein Einstieg über Windhunde. Preise im Rahmen 69–99 / 89–139 / 25–59 EUR.
20. Kein KI-erzeugtes Bild auf einer Produkt-, Katalog- oder Praxistestseite.

## Übergabe

Zum Abschluss gehört eine Seite Anleitung für Björn: Produkt anlegen, Preis ändern, Bild tauschen,
Text ändern, Bestellung bearbeiten. Geschrieben für jemanden, der Leder verarbeitet, nicht Code.
