# 03 — Titel, Beschreibung, Schema

Einsatz: für jede neue Seite. Die Bausteine sind Vorlagen mit Platzhaltern in `[ ]` —
**Platzhalter niemals mit ausgeliefern**, und keine Angabe erfinden.

## Titel

| Regel | |
|---|---|
| Länge | 50–60 Zeichen. Länger wird abgeschnitten. |
| Aufbau | `[Was es ist] — [Unterschied] \| Bellowerk` |
| Marke | am Ende, außer auf der Startseite |
| Verboten | ALLE GROSSBUCHSTABEN, Ausrufezeichen, „günstig", „Top", „Nr. 1", Emoji, Suchwortketten |

## Beschreibung

| Regel | |
|---|---|
| Länge | 140–155 Zeichen |
| Inhalt | Was es ist, woraus, und der eine Satz zum Praxistest |
| Form | Aussagesatz, aktiv, kein Fragezeichen, keine Aufzählung |
| Verboten | Preisversprechen, Lieferzeitversprechen, Superlative |

## Schema — welche Seite bekommt was

| Seitentyp | Schema |
|---|---|
| Startseite | `Organization` + `LocalBusiness` (verschachtelt), `sameAs` auf Instagram und Facebook |
| Kategorie | `CollectionPage` + `ItemList` mit den Produkten |
| Produkt | `Product` + `Offer` |
| Ratgeber | `Article`, zusätzlich `FAQPage` nur bei sichtbaren Fragen |
| Leistung | `Service` mit `areaServed` |
| Kontakt | `ContactPage` |
| überall | `BreadcrumbList` |

## Gerüst Startseite

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Bellowerk Manufaktur",
  "alternateName": "Herr Bello und Frau Wuff",
  "description": "Halsbänder und Leinen aus Fettleder und Messing, gefertigt in Hamburg.",
  "url": "[https://DOMAIN]",
  "telephone": "[TODO Björn]",
  "email": "[TODO Björn]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[TODO Björn]",
    "postalCode": "[TODO Björn]",
    "addressLocality": "Hamburg",
    "addressCountry": "DE"
  },
  "areaServed": [{"@type": "City", "name": "Hamburg"}, {"@type": "Place", "name": "Altes Land"}],
  "sameAs": ["[Instagram-URL]", "[Facebook-URL]"],
  "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Product", "name": "Lederhalsband HB-01"}}]
}
```

## Gerüst Produkt

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[Halsband HB-01 Fettleder]",
  "sku": "[HB-01]",
  "brand": {"@type": "Brand", "name": "Bellowerk"},
  "material": "Fettleder pflanzlich gegerbt, Messing massiv",
  "image": ["[Bild-URL]"],
  "description": "[ein Satz]",
  "offers": {
    "@type": "Offer",
    "price": "[79.00]",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock",
    "url": "[Produkt-URL]"
  }
}
```

## Harte Schema-Regeln

1. **`aggregateRating` und `review` nur mit echten, auf der Seite sichtbaren Bewertungen.**
   Erfundene Sterne sind ein Richtlinienverstoß und können die ganze Domain aus den
   Suchergebnis-Auszeichnungen werfen.
2. Schema beschreibt nur, was auf der Seite sichtbar steht. Kein Preis im Schema, der nicht
   auf der Seite steht.
3. `address` nur, wenn die Adresse öffentlich sein soll. Ist sie es nicht, `areaServed` ohne
   `address` verwenden und das Google-Profil als Dienstleister-ohne-Ladenadresse führen.
4. Jedes Gerüst vor dem Einbau durch den Rich-Results-Test von Google und den Schema-Validator.
