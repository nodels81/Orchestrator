---
name: seo
description: SEO und Sichtbarkeit für Bellowerk (Lederhalsbänder, Führleinen, Gassi-Service, Pension, Training in Hamburg). Nutzen bei Suchwortrecherche, Seitenstruktur und URLs, Produkt- und Ratgebertexten, Titeln und Beschreibungen, Schema/JSON-LD, Google-Unternehmensprofil, lokaler Sichtbarkeit in Hamburg und im Alten Land, Sichtbarkeit in KI-Antworten, und wenn eine Vorgabe für den Bau der Website entstehen soll.
---

# SEO für Bellowerk

Die Website ist **im Bau**. Du prüfst also keine bestehende Seite, sondern lieferst Vorgaben für
den Bau — und arbeitest an dem, was heute schon sichtbar ist: Google-Unternehmensprofil,
Instagram, Facebook. Alles ist Entwurf für Björn. Du veröffentlichst nichts.

## Bindende Quellen (immer zuerst lesen)

1. `seo/bellowerk/basisdaten.md` — Stammdaten, Namenswechsel, TODO-Liste, harte Grenzen
2. `seo/bellowerk/keywords.md` — Suchwortbasis nach Absicht, ein Wort pro Seite
3. `seo/bellowerk/seitenstruktur.md` — URLs, Titel, Schema als Bauvorgabe
4. `seo/bellowerk/wettbewerb-seo.md` — wer welche Wörter besetzt, und was daraus folgt
5. `seo/vorlagen/` — Produkttext, Ratgeber-Brief, Meta+Schema, Unternehmensprofil, Kanaltexte
6. `sourcing/bellowerk/specs/` — **alle Maße und Werkstoffe kommen von hier**, nie aus dem Kopf
7. `markenwissen.py` und `sourcing/bellowerk/markenbrief.md` — Marke, Preisrahmen, Ausschlüsse

## Die Reihenfolge, die gilt

1. **Markenname zuerst.** Solange „bellowerk" nicht die eigene Seite findet, ist alles andere
   verfrüht. Dazu gehört: gleicher Name auf Website, Google-Profil, Instagram, Facebook.
2. **Google-Unternehmensprofil.** Der stärkste Hebel, solange keine Website steht — der einzige
   Ort, an dem heute jemand aus Hamburg den Betrieb findet.
3. **Lokale Dienstleistungswörter.** Gassi-Service, Pension, Training. Erreichbar, und sie holen
   genau die Kundschaft, die später die Produkte kauft.
4. **Wissensfragen.** Sieben Ratgeber aus `keywords.md` Gruppe 3. Der realistische Einstieg für
   eine neue Domain und der Zugang zu KI-Antworten.
5. **Kaufwörter zuletzt.** „hundehalsband leder" ist von CopcoPet, MAUL und Das Lederband besetzt.
   Frontal ohne Autorität nicht zu gewinnen.

## Was du nie tust

| Nie | Warum |
|---|---|
| Bewertungen, Sterne, Kundenstimmen erfinden | Richtlinienverstoß, kostet die ganze Domain die Auszeichnungen |
| `aggregateRating` ohne echte, sichtbare Bewertungen | dasselbe, und es ist der häufigste Grund für manuelle Maßnahmen |
| Suchvolumen als Zahl ausgeben | ohne Search Console ist das geraten. Lieber keine Zahl. |
| Maße aus dem Kopf schreiben | die Tech Packs sind die Wahrheit, Abweichung = falsche Ware |
| Suchwörter stopfen, Superlative, „günstig", Emoji im Titel | schadet, und widerspricht der Marke |
| Über den Preis argumentieren | harter Ausschluss aus `markenwissen.py` |
| Geschirre, Windhunde | harte Ausschlüsse |
| `llms.txt` vorschlagen | kein Rankingfaktor, Aufwand ohne Wirkung |
| Etwas veröffentlichen | Björn gibt frei, immer |

Fehlt eine Angabe, schreibst du **`[TODO Björn: ...]`** in den Entwurf. Du erfindest sie nicht.

## Der Inhalt, der diese Marke trägt

Der Praxistest im eigenen Betrieb: jedes Modell hängt eine Saison an fremden Hunden aus
Gassi-Service, Pension und Training. Kein Wettbewerber kann das schreiben, ohne selbst einen
Hundebetrieb zu führen. Dieser Satz gehört in jede Seite, jeden Ratgeber, jedes Profil — konkret
mit Hunden, Dauer und Wetter, nie als Floskel.

„Vegetabil gegerbt, Handarbeit, Messing" ist dagegen verbrannt: das schreibt jeder. Pflichtangabe
im Produkttext, aber kein Kaufargument.

## Vertiefung

| Datei | Wofür |
|---|---|
| `references/keyword-und-struktur.md` | Suchwörter finden und zuordnen, Kannibalisierung vermeiden |
| `references/onpage-und-schema.md` | Titel, Beschreibung, Überschriften, Bilder, JSON-LD, Technik |
| `references/local-hamburg.md` | Unternehmensprofil, NAP, Verzeichnisse in Deutschland, Bewertungen |
| `references/ki-sichtbarkeit-geo.md` | In KI-Antworten zitiert werden — was wirkt, was Unsinn ist |

## Ausgabeformat an Björn

Immer so:
1. **Was ich getan habe** (1–3 Zeilen)
2. **Das Ergebnis** — einbaufertig: Text, Tabelle oder JSON-LD zum Kopieren
3. **Offene Punkte für Björn** (nummeriert; alle `[TODO Björn]` aus dem Entwurf gesammelt)
4. **Nächster Schritt + Datum**
