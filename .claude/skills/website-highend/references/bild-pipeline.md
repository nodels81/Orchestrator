# Bildregie und KI-Pipeline (Nano Banana)

Bilder entscheiden über die Preiswahrnehmung. Ein Halsband für 89 EUR und eines für 19 EUR
unterscheiden sich für den Betrachter zuerst durch das Foto, nicht durch das Leder.

## Die oberste Regel

**Produktbilder sind echte Fotos. Ausnahmslos.**

Das Verkaufsargument von Bellowerk ist der Praxistest an echten Hunden aus Gassi-Service,
Pension und Training. Ein generiertes Produktfoto zerstört genau dieses Argument — und ein
Produkt zu bewerben, das so nie fotografiert wurde, ist wettbewerbsrechtlich angreifbar.
Auf Produkt-, Katalog- und Praxistestseiten steht kein KI-Bild.

## Wofür Nano Banana eingesetzt wird — und das ist viel

1. **Layout-Comps und Moodboards** vor dem Fototermin. Bildschnitt, Licht und Anmutung
   durchspielen, bis feststeht, welches Foto entstehen muss.
2. **Aufnahmeanweisung als Bild.** Statt "Nahaufnahme der Schnalle bei hartem Seitenlicht" ein
   Bild, das Björn beim Fotografieren nachbaut. Spart Termine und Missverständnisse.
3. **Freistellen und Retusche** echter Fotos: Hintergrund säubern, Störer entfernen, Staub weg.
4. **Bildrand erweitern** (Outpainting) für andere Seitenverhältnisse: 16:9 fürs Web,
   4:5 für Instagram, 1:1 fürs Raster — aus einer Aufnahme.
5. **Texturen und Hintergründe**: Papierfaser, Werkstattbeton, Leinen, Rauschebenen,
   Verlaufsflächen. Keine Produktaussage, hier ist Generierung unproblematisch.
6. **Verpackungs- und Schildansichten** für die interne Abstimmung mit dem Hersteller.
7. **Bildvarianten für A/B-Tests** von Sektionshintergründen.

## Prompt-Bauplan

Jedes Feld wird gefüllt, keins ausgelassen:

`[Motiv] · [Material und Zustand] · [Objektiv und Abstand] · [Licht: Quelle, Richtung, Härte] ·
[Hintergrund] · [Farbstimmung] · [Seitenverhältnis] · [was NICHT im Bild sein darf]`

**Beispiel Produkt-Comp**
> Braunes Fettleder-Halsband mit massiver Messingschnalle, leicht gebraucht mit sichtbaren
> Gebrauchsspuren, liegend auf rohem Eichenholz, 85 mm Makro aus 40 cm, hartes Seitenlicht von
> links durch ein Werkstattfenster, Hintergrund unscharf und dunkel, warme gedämpfte Farben,
> 4:5, keine Nähte, keine Nieten, kein Kunststoff, kein Text im Bild.

**Beispiel Hintergrundtextur**
> Rohe Werkstattbetonwand, gleichmäßig ausgeleuchtet, feine Struktur, sehr flacher Kontrast,
> entsättigt warm, kachelbar, 16:9, keine Objekte, kein Text, keine Schatten.

**Was den Unterschied macht**
- Objektiv und Abstand nennen. "Makro 85 mm aus 40 cm" liefert eine andere Bildsprache als "Nahaufnahme".
- Lichtrichtung und -härte nennen. Weiches Frontlicht wirkt billig, hartes Seitenlicht zeigt Struktur.
- Die Negativliste ist so wichtig wie das Motiv. Ausgeschlossene Werkstoffe stehen **immer** drin:
  keine Nähte, keine Nieten, kein Stahl, kein Kunststoff, kein Klickverschluss, kein Gurtband.
- Kein Text im Bild verlangen. Schrift gehört ins HTML, nicht ins Pixel — wegen Übersetzbarkeit,
  Schärfe und Vorlesbarkeit.

## Aufnahmeliste für echte Fotos

Zu jeder Seite gehört eine Liste, die Björn abarbeiten kann. Je Bild:
Motiv · Produkt und Farbe · Ort · Tageszeit und Licht · Bildausschnitt · Seitenverhältnis ·
wofür es verwendet wird. Fehlt ein Foto, wird die Sektion nicht erfunden, sondern das Foto
angefordert.

Die stärksten Motive dieser Marke sind nicht Studioaufnahmen, sondern:
das Halsband am arbeitenden Hund bei Regen · die Kante nach einer Saison · die Werkbank mit
Werkzeug · Björns Hände beim Kürzen · dasselbe Halsband neu und nach zwölf Monaten nebeneinander.

## Ausgabe und Technik

- **AVIF** zuerst, **WebP** als Rückfall, JPEG nur als letzte Ebene. `<picture>` mit `srcset`
  in fünf Breiten (400, 800, 1200, 1600, 2000).
- `width` und `height` immer im Markup, `aspect-ratio` im CSS. Vorgabe für CLS ist 0.00.
- Erstes Bild über der Falz: `fetchpriority="high"`, `loading="eager"`.
  Alles andere: `loading="lazy"`, `decoding="async"`.
- **Kunstgerechter Zuschnitt**: mobil ein anderer Ausschnitt, nicht dasselbe Bild gestaucht.
  Über `<source media="...">` steuern.
- Farbprofil sRGB, eingebettet. Ohne Profil wirken Brauntöne in Safari anders als in Chrome.
- Alternativtext beschreibt das Produkt und die Situation, nicht die Datei. Rein dekorative
  Bilder bekommen `alt=""` und werden damit ausgeblendet.
- Zoom auf der Produktseite: zweite Auflösung erst beim Öffnen laden, nie vorab.

## Kennzeichnung

KI-erzeugte oder KI-veränderte Bilder werden im Dateinamen mit `-ki` geführt und in der
Bildübersicht als solche gelistet. So ist jederzeit prüfbar, dass auf Produktseiten keins liegt.
