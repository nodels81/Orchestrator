# Onpage und Schema

## Titel und Beschreibung

| | Titel | Beschreibung |
|---|---|---|
| Länge | 50–60 Zeichen | 140–155 Zeichen |
| Hauptsuchwort | vorne, natürlich formuliert | einmal, natürlich |
| Marke | am Ende (`\| Bellowerk`), außer Startseite | nicht nötig |
| Form | Aussage, keine Frage | Aussagesatz, aktiv |
| Verboten | GROSSBUCHSTABEN, `!`, Emoji, „günstig", „Nr. 1", Suchwortketten | Preis- und Lieferversprechen, Superlative |

Jede Seite bekommt beides **einzeln**. Automatisch erzeugte Titel mit Platzhaltern („Halsband
kaufen — Halsbänder — Bellowerk Shop") sind schlechter als gar keine.

## Überschriften

- **Ein** `h1` je Seite, mit dem Hauptsuchwort in natürlicher Formulierung.
- `h2` gliedert nach Fragen, die der Leser hat — nicht nach Suchwörtern.
- Keine Ebene überspringen (`h2` → `h4`).
- Überschriften beschreiben den Abschnitt, sie werben nicht.

## Text

- Erster Absatz beantwortet die Frage der Seite vollständig. Kein Anlauf, keine Begrüßung.
- Kurze Sätze, aktive Verben, konkrete Zahlen mit Einheit (`25 mm`, `3,00 m`, `3,5–4,0 mm`).
- Tabelle statt Fließtext, wo es Maße gibt.
- Verweise mit sprechendem Linktext („so messen Sie den Halsumfang"), nie „hier" oder „mehr".

## Bilder

| Punkt | Vorgabe |
|---|---|
| Dateiname | sprechend, klein, Bindestriche: `hb-02-geflochten-oliv-am-hund.jpg` |
| Alternativtext | beschreibt, was zu sehen ist — kein Suchwortlager |
| Format | WebP, max. 1600 px Breite, unter 200 kB |
| Laden | `loading="lazy"` überall außer dem ersten sichtbaren Bild |
| Maße | `width` und `height` im HTML, sonst springt das Layout |
| Herkunft | echte Fotos aus dem Betrieb. Keine Stockfotos, keine KI-Bilder. |

## Technik als Bauvorgabe

| Punkt | Vorgabe |
|---|---|
| HTTPS | Pflicht, HTTP per 301 |
| Domainvariante | eine festlegen (mit oder ohne `www`), die andere per 301 |
| URLs | klein, Bindestriche, keine Umlaute, keine Endung, nach dem Start unveränderlich |
| Canonical | jede Seite auf sich selbst |
| `robots.txt` | erlaubt alles außer Warenkorb und Konto, verweist auf die Sitemap |
| `sitemap.xml` | nur Seiten mit Status 200, keine Weiterleitungen, keine `noindex`-Seiten |
| Weiterleitungen | 301, immer direkt aufs Ziel, keine Ketten |
| Ladezeit | größtes Bild unter 2,5 s, kein Layoutsprung, Reaktion unter 200 ms |
| Handy zuerst | Google bewertet die Handy-Ansicht. Dort muss der ganze Inhalt stehen. |
| Cookie-Banner | verdeckt den Inhalt nicht, bevor er lesbar ist |
| `llms.txt` | **nicht anlegen.** Kein Rankingfaktor, keine Wirkung. |

## Schema (JSON-LD)

Gerüste stehen in `seo/vorlagen/03-meta-und-schema.md`. Die Regeln:

1. Schema beschreibt **nur, was sichtbar auf der Seite steht**. Kein Preis im Schema, der nicht
   auf der Seite steht.
2. **`aggregateRating` und `review` nur bei echten, sichtbaren Bewertungen.** Erfundene Sterne
   sind ein Richtlinienverstoß und der schnellste Weg, alle Auszeichnungen zu verlieren.
3. Ein `LocalBusiness` je Betrieb, auf der Startseite, mit `sameAs` auf Instagram und Facebook —
   damit Google Profile und Seite als eine Entität erkennt.
4. `Product` braucht `name`, `brand`, `offers`. `material` und `sku` lohnen sich hier.
5. `FAQPage` nur, wenn die Fragen sichtbar beantwortet werden.
6. `Service` mit `areaServed` für Gassi-Service, Pension, Training — nicht `Product`.
7. Jedes Gerüst vor dem Einbau durch den Rich-Results-Test und den Schema-Validator.

## Prüfliste vor dem Livegang einer Seite

- [ ] Titel und Beschreibung einzeln, in der Länge, ohne Verbotenes
- [ ] ein `h1`, Gliederung ohne Sprünge
- [ ] erster Absatz beantwortet die Frage
- [ ] alle Maße aus dem Tech Pack geprüft
- [ ] Werkstoffangaben stimmen mit dem Markenbrief (keine Naht, keine Niete, kein Stahl)
- [ ] Preis im Rahmen und von Björn freigegeben
- [ ] Bilder: echt, benannt, Alternativtext, WebP, Maße gesetzt
- [ ] zwei Verweise raus (Ratgeber/Produkt), einer rein
- [ ] Schema validiert, kein `aggregateRating`
- [ ] Canonical auf sich selbst, kein `noindex`
- [ ] auf dem Handy vollständig lesbar
- [ ] alle `[TODO Björn]` aufgelöst
