---
name: bellowerk-shop
description: Shop-Texte und Produktseiten für Bellowerk schreiben — Beschreibung, Maßtabelle, Pflege, Herstellerangaben, Preis. Nutze das immer, wenn etwas "in den Shop" soll, eine Produktseite, ein Artikeltext, eine Produktbeschreibung oder ein Verkaufstext entsteht oder geändert wird. Prüfe damit auch bestehende Texte gegen die Regeln, denn ein falscher Satz über Herkunft oder Fertigung ist im Shop teurer als ein fehlender.
---

# Shop-Texte für Bellowerk

Quelle für Ton und Rahmen ist `markenwissen.py`, Quelle für jede Zahl das Tech Pack unter
`sourcing/bellowerk/specs/`. Vorlage: `sourcing/bellowerk/shop/index.html`.

## Zwei Sätze, die nicht im Shop stehen dürfen

1. **Nichts, was deutsche Fertigung behauptet.** Kein "Made in Germany", kein "in unserer Werkstatt
   gefertigt", kein Hamburg-Bezug, der als Fertigungsort gelesen wird. Gefertigt wird in China.
   Die Grenze, die Björn am 15.9.2026 gezogen hat: *"Entworfen und geprüft in Hamburg"* — mehr nicht.
2. **Keine Herkunftsangabe.** Kein Fertigungsland, nirgends: nicht im Text, nicht am Anhänger, nicht
   auf der Verpackung. Für Lederwaren ist das in der EU zulässig; eine falsche Angabe wäre es nicht.

Das ist kein Formalkram: Das Verkaufsargument der Marke ist der Herstellungsprozess ("eine Saison an
fremden Hunden getestet"). Wer beim Prozess schummelt, verliert genau das Argument.

## Ton

Björn führt Gassi-Service, Pension und Training; jedes Modell hängt vor dem Verkauf eine Saison an
fremden Hunden. Das ist der Kern jedes Textes — ein Unterschied im Herstellungsprozess, kein
Marketingdreh. Kurze Sätze, konkrete Zahlen, keine Superlative. Nie über den Preis argumentieren.
Was das Produkt nicht hat (keine Naht, keine Niete, kein Kunststoff), sagt oft mehr als Adjektive.

## Pflichtblöcke einer Produktseite

| Block | Inhalt |
|---|---|
| Kopf | Modellname, ein Satz, der die Form erklärt, Preis mit MwSt-Hinweis |
| Auswahl | Farbe und Größe; Größe immer mit Halsumfang in cm |
| Beschreibung | Form, Material, Beschläge, Verschluss, Patch — in dieser Reihenfolge |
| Maßtabelle | Größe, Halsumfang, Breiten, exakt aus dem Tech Pack |
| Pflege | Fettleder trocknen lassen, einfetten; Messing dunkelt nach; keine Waschmaschine |
| Herstellerangaben | Bellowerk Manufaktur + **Postanschrift und E-Mail** (GPSR, Pflicht seit 12/2024), Modellcode, Charge |
| Bilder | echte Fotos; fehlen sie, gestrichelte Platzhalter mit der Angabe, welches Foto hingehört |

## Preisrahmen

Halsband 69–99 €, Leine 89–139 €, Zubehör 25–59 € (`markenwissen.py`). Aufwendigere Modelle nach
oben: Hamburg Nr. 1 braucht eine Stanzform je Größe und mehr Kantenarbeit als das glatte Halsband,
also darf es nicht darunter liegen. Jeder Preis, den Björn nicht bestätigt hat, wird als Vorschlag
gekennzeichnet — lieber sichtbar offen als still gesetzt.

## Fehlende Fotos

Solange es keine Fotos vom Goldmuster gibt, keinen Text schönen: Platzhalter setzen, die sagen,
welches Foto fehlt (Ausschnitt, Licht, Format). Eine Darstellung darf das Hauptbild vertreten, wenn
sie als Darstellung gekennzeichnet ist — siehe Skill `bellowerk-produktbild`.
