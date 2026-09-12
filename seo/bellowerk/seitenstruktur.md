# Bellowerk — Seitenstruktur als Bauvorgabe

Die Seite ist im Bau. Diese Datei ist die Vorgabe **für** den Bau: URL, Hauptsuchwort, Titel,
Beschreibung, Schema. Wer die Seite baut, arbeitet diese Tabelle ab. Was hier nicht steht, wird
nicht gebaut — jede zusätzliche Seite braucht ein eigenes Suchwort aus `keywords.md`.

**Regeln für URLs:** kleingeschrieben, Bindestriche, keine Umlaute (`halsbaender`, nicht
`halsbänder`), kein Datum, keine Artikelnummer im Pfad der Kategorieseite, keine Endung.
Eine URL wird nach dem Start **nicht mehr geändert**; Änderungen kosten Rankings und brauchen
eine 301-Weiterleitung.

## Ebene 0 — Startseite

| | |
|---|---|
| URL | `/` |
| Hauptsuchwort | bellowerk · hundehalsband manufaktur |
| Titel (≤ 60 Z.) | `Bellowerk — Lederhalsbänder aus Hamburg, im Betrieb getestet` |
| Beschreibung (≤ 155 Z.) | `Halsbänder und Leinen aus Fettleder und Messing, gefertigt in Hamburg. Jedes Modell hängt erst eine Saison an fremden Hunden — dann verkaufen wir es.` |
| Muss oben stehen | Ein Satz, der beide Namen verbindet: Bellowerk = die Manufaktur von Herr Bello und Frau Wuff. |
| Schema | `Organization` + `LocalBusiness`, verschachtelt, mit `sameAs` auf Instagram und Facebook |

## Ebene 1 — Kategorien und Leistungen

| URL | Hauptsuchwort | Titel-Entwurf | Schema |
|---|---|---|---|
| `/halsbaender` | hundehalsband fettleder | `Hundehalsbänder aus Fettleder — ohne Naht, mit Messing \| Bellowerk` | `CollectionPage` + `ItemList` |
| `/leinen` | hundeleine leder | `Führleinen aus Fettleder, 3 m, dreifach verstellbar \| Bellowerk` | `CollectionPage` + `ItemList` |
| `/zubehoer` | handschlaufe leder hund | `Zubehör aus Leder und Messing \| Bellowerk` | `CollectionPage` + `ItemList` |
| `/manufaktur` | hundehalsband manufaktur | `Die Manufaktur — warum jedes Modell eine Saison an fremden Hunden hängt` | `AboutPage` |
| `/gassi-service-hamburg` | gassi service hamburg | `Gassi-Service in Hamburg und im Alten Land \| Herr Bello und Frau Wuff` | `Service` + `areaServed` |
| `/hundepension` | hundepension altes land | `Hundepension im Alten Land — Betreuung in kleiner Gruppe` | `Service` + `areaServed` |
| `/hundetraining` | hundeschule altes land | `Hundetraining im Alten Land \| Herr Bello und Frau Wuff` | `Service` + `areaServed` |
| `/ratgeber` | — (Übersicht) | `Ratgeber: Halsband, Leder, Messing \| Bellowerk` | `CollectionPage` |
| `/kontakt` | bellowerk kontakt | `Kontakt \| Bellowerk Manufaktur, Hamburg` | `ContactPage` |

## Ebene 2 — Produktseiten (je Modell aus der Kernserie)

| URL | Modell | Hauptsuchwort |
|---|---|---|
| `/halsbaender/hb-01-fettleder` | HB-01 Halsband einlagig, ohne Naht, S–XL, 20–40 mm | hundehalsband leder ohne naht |
| `/halsbaender/hb-02-geflochten` | HB-02 Halsteil im Mystery Braid, O-Ring, Schnalle, Patch | hundehalsband geflochten leder |
| `/leinen/le-01-fuehrleine` | LE-01 Führleine 3,00 m, Ringe bei 45/140/245 cm, sechs Führlängen | führleine leder verstellbar |
| `/leinen/le-02-geflochten` | LE-02 Führleine geflochten | hundeleine leder geflochten |
| `/zubehoer/hs-01-handschlaufe` | HS-01 Handschlaufe, Umfang 50 cm | handschlaufe leder hund |
| `/zubehoer/namenspatch` | PATCH-01 Lederpatch cognac, lasergraviert | namensschild hund leder |

**Pflichtbestandteile jeder Produktseite** — fehlt einer, geht die Seite nicht live:

1. H1 mit Modellname und Hauptsuchwort in natürlicher Formulierung
2. Maßtabelle aus dem Tech Pack in `sourcing/bellowerk/specs/` (Länge, Breite, Lochabstand,
   Ringpositionen, Materialstärke) — **die Zahlen kommen aus dem Tech Pack, nie aus dem Kopf**
3. Werkstoffe im Klartext: Fettleder pflanzlich gegerbt 3,5–4,0 mm, Messing massiv, Buchschrauben,
   **keine Naht, keine Niete**
4. Ein Absatz Praxistest: was dieses Modell im eigenen Betrieb hinter sich hat
5. Größenhilfe mit Verweis auf `/ratgeber/halsband-messen`
6. Pflegehinweis mit Verweis auf `/ratgeber/fettleder-pflege`
7. Preis im Rahmen (Halsband 69–99 €, Leine 89–139 €, Zubehör 25–59 €)
8. Echte Fotos aus dem Betrieb, Dateiname sprechend (`hb-02-geflochten-oliv-am-hund.jpg`),
   Alternativtext beschreibend statt suchwortgestopft
9. `Product`-Schema mit `brand`, `material`, `offers` — **ohne** `aggregateRating`, solange es keine
   echten Bewertungen gibt

## Ebene 2 — Ratgeber (der Teil, den KI-Antworten zitieren)

| URL | Frage |
|---|---|
| `/ratgeber/halsband-messen` | Wie messe ich den Hals meines Hundes richtig? |
| `/ratgeber/halsband-breite` | Welche Breite für welchen Hund? |
| `/ratgeber/fettleder-pflege` | Wie pflege ich Fettleder, und was mache ich, wenn es nass wurde? |
| `/ratgeber/messing-beschlaege` | Messing oder Edelstahl — was hält länger? |
| `/ratgeber/ohne-naht` | Warum ein Halsband ohne Naht und ohne Nieten? |
| `/ratgeber/haltbarkeit` | Wie lange hält ein Lederhalsband im Alltag? |
| `/ratgeber/leder-gerbung` | Pflanzlich gegerbt — was heißt das für den Hund? |

Aufbau jedes Ratgebers: **Antwort in den ersten 40–60 Wörtern**, dann Begründung, dann Tabelle oder
Schrittfolge, dann ein Absatz Praxiserfahrung aus dem Betrieb, am Ende Verweis auf das passende
Produkt. `FAQPage`-Schema nur für Fragen, die auf der Seite auch sichtbar beantwortet werden.

## Verlinkung

- Jede Produktseite verlinkt auf mindestens zwei Ratgeber, jeder Ratgeber auf mindestens ein Produkt.
- `/manufaktur` wird von jeder Produktseite verlinkt — dort steht der Praxistest ausführlich.
- Die Leistungsseiten verlinken auf die Produkte („die Halsbänder, die unsere Pensionshunde tragen").
- Kein Link mit dem Text „hier" oder „mehr". Der Linktext nennt das Ziel.

## Technische Vorgaben an den Bau

| Punkt | Vorgabe |
|---|---|
| Domain | **TODO Björn** — danach: eine Variante festlegen (mit oder ohne `www`), die andere per 301 darauf |
| HTTPS | Pflicht, HTTP per 301 auf HTTPS |
| `robots.txt` | erlaubt alles außer Warenkorb/Konto; verweist auf die Sitemap |
| `sitemap.xml` | automatisch erzeugt, nur Seiten mit Status 200, keine Weiterleitungen darin |
| Canonical | jede Seite auf sich selbst |
| Titel/Beschreibung | je Seite einzeln, keine Vorlage mit Platzhaltern, keine Doppelung |
| Bilder | WebP, Breite max. 1600 px, `loading="lazy"` außer dem ersten Bild, `width`/`height` gesetzt |
| Kein `noindex` | auf Produkt-, Kategorie-, Ratgeber- und Leistungsseiten |
| `llms.txt` | **nicht nötig.** Keine Suchmaschine und kein KI-Anbieter wertet sie aus. Aufwand ohne Wirkung. |
| Cookie-Banner | darf den Inhalt nicht verdecken, bevor er gelesen werden kann |
