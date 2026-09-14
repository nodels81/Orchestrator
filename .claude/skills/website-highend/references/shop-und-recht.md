# Shopsystem, Bausteine, deutsches Onlinehandelsrecht

## Systemwahl

**Weg A — Shopify + Hydrogen (Empfehlung für Bellowerk).**
Zahlung, Steuersätze, Versandscheine, Retouren und Buchhaltungsschnittstelle sind gelöst und
rechtssicher. Die Gestaltungsfreiheit bleibt trotzdem vollständig, weil Hydrogen ein eigenes
React-Frontend auf die Storefront-API setzt — es sieht nichts nach Shopify aus, wenn man es
nicht will. Björn führt eine Manufaktur, keine IT-Abteilung: laufender Betrieb schlägt die
letzten fünf Prozent Kontrolle. Kosten: Grundgebühr plus Transaktionsanteil.

**Weg B — Next.js (App Router) + Medusa oder Saleor, selbst gehostet.**
Volle Kontrolle, keine Umsatzbeteiligung. Aber Zahlungsanbindung, Steuerlogik, Sicherheits-
aktualisierungen und Ausfallsicherheit liegen dann bei uns. Nur wählen, wenn dauerhaft jemand
die Wartung übernimmt.

Die Wahl wird **begründet** geliefert, nicht stillschweigend getroffen.

## Baukasten (Weg A)

| Schicht | Wahl | Anmerkung |
|---|---|---|
| Frontend | Hydrogen (React, Remix), Vite, TypeScript strikt | eigenes Frontend, kein Theme |
| Gestaltung | Tailwind mit **eigenen** Tokens aus dem Designsystem | Standardpalette nie ausliefern |
| Materialhaftes | handgeschriebenes CSS | Schatten, Glanz, Rauschen |
| Redaktion | Shopify Metaobjects, alternativ Sanity | Sanity, wenn Björn frei layouten soll |
| Suche | Shopify Search & Discovery | Algolia erst ab etwa 200 Artikeln |
| Bilder | Shopify CDN mit Transformationsparametern | AVIF erzwingen |
| Bewertungen | Judge.me oder Trusted Shops mit Käuferschutz | in Deutschland das stärkere Vertrauenssignal |
| Zahlung | Shopify Payments (Karte, Apple Pay, Google Pay), PayPal, Klarna Rechnung, SEPA | Rechnungskauf ist hier Grundausstattung, kein Extra |
| Versand | DHL-Anbindung, Sendungsverfolgung in der Bestätigung | GoGreen ausweisen |
| Mail | Klaviyo für Abbruchstrecke und Neuigkeiten | Double-Opt-in, Nachweis speichern |
| Zustimmung | Consent-Banner mit echtem "Alle ablehnen" gleichrangig | Messung erst nach Zustimmung |
| Messung | Plausible oder Fathom plus Shopify-Auswertung | ohne Personenbezug |

## Bausteine dieser Seite

Jeder in allen Zuständen gestaltet: Ruhe, Hover, Fokus, Laden, Fehler, leer, ausverkauft.

- Navigation mit Vorschau-Menü
- Warenkorb-Schublade mit Restbetrag bis Versandfrei
- Produktkarte, Produktseite mit Galerie und Zoom
- Varianten- und Größenwahl
- **Größenfinder**: Halsumfang messen → Größe, mit bemaßter Zeichnung. Senkt Retouren am stärksten.
- Materialkunde, Pflegehinweise, Reparaturhinweis
- **Praxistest-Sektion**: welcher Hund, wie lange, bei welchem Wetter. Das Alleinstellungsmerkmal
  bekommt eine eigene Sektion, keinen Halbsatz.
- Bewertungen mit Kundenfotos
- Häufige Fragen mit strukturierten Daten
- Anfrageformular für Gassi-Service, Pension, Training
- Newsletter mit ehrlichem Nutzenversprechen (kein "10 % Rabatt" — das widerspricht der Positionierung)
- Fußzeile mit allen Pflichtangaben

## Pflichtangaben und Recht (Deutschland)

Fehlt eines davon, ist die Abnahme nicht bestanden.

1. **Impressum** nach § 5 DDG, aus jeder Seite mit einem Klick erreichbar
2. **Datenschutzerklärung** nach DSGVO, inklusive aller eingesetzten Dienste
3. **AGB** und **Widerrufsbelehrung** mit Muster-Widerrufsformular
4. **Versandkosten und Lieferzeit** vor Abschluss der Bestellung sichtbar, nicht erst im Checkout
5. **Preisangabenverordnung**: Endpreis inklusive Umsatzsteuer, Hinweis auf Versandkosten,
   Grundpreis wo einschlägig
6. **Bestellknopf** beschriftet mit **"Zahlungspflichtig bestellen"** (Button-Lösung, § 312j BGB).
   Nicht "Jetzt kaufen", nicht "Absenden".
7. **Bestellübersicht** unmittelbar vor Abschluss: Ware, Menge, Preis, Versand, Gesamtsumme
8. **Zustimmung nach TDDDG**: Ablehnen genauso leicht wie Annehmen, gleiche Ebene, gleiche
   Gestaltungswertigkeit. Kein vorangekreuztes Kästchen. Keine Messung vor Zustimmung.
9. **Newsletter** nur mit Double-Opt-in, Bestätigung protokolliert, Abmeldung in jeder Mail
10. **Barrierefreiheitsstärkungsgesetz**: seit Juni 2025 gilt für den Onlinehandel EN 301 549,
    praktisch WCAG 2.1 AA. Wir liefern 2.2 AA — der Abstand ist die Sicherheitsreserve.
11. Verpackungsregister- und Rücknahmehinweise, sofern zutreffend
12. Keine erfundenen Rabatt-Countdowns, keine durchgestrichenen Fantasiepreise, keine
    "nur noch 2 auf Lager"-Anzeige ohne echten Bestandsbezug — das ist irreführende Werbung

## Kaufabschluss ohne Reibung

- Gastbestellung ohne Kontozwang
- Adressvervollständigung, Postleitzahl prüft Ort
- Zahlungsarten oben zeigen, nicht erst nach der Adresse
- Fehlermeldungen stehen am Feld, sagen was zu tun ist, und löschen keine Eingaben
- Keine Pflichtfelder ohne Grund. Die Telefonnummer ist keins.
- Bestellbestätigung mit Sendungsverfolgung, Pflegehinweis und Kontaktweg

## Was Geld kostet — geht als Entscheidung an Björn

Shopify-Tarif · Domain · Trusted-Shops-Mitgliedschaft · Klaviyo ab Schwellenwert ·
kostenpflichtige Erweiterungen · Fototermin · Schriftlizenzen für kommerzielle Nutzung.
Jeweils mit Preis, Nutzen und Alternative vorlegen. Nichts davon selbst buchen.
