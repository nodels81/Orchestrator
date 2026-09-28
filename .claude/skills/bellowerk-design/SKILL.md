---
name: bellowerk-design
description: Gestaltung für die Marke Bellowerk — Website, Shop, Produktseiten, Landingpages, Instagram-Textkacheln, Newsletter, Anhänger, Pflegekarte, Präsentationen, Mockups und visuelle Prüfung. Nutzen bei jeder Aufgabe, bei der für Bellowerk etwas gestaltet, gebaut, gelayoutet, gestylt oder optisch geprüft wird. Das festgelegte Designsystem steht in design/DESIGN.md; Methode und Handwerk kommen aus dem Skill refero-design.
---

# Gestaltung für Bellowerk

Du gestaltest für die Manufaktur Bellowerk (Halsbänder und Leinen aus Fettleder und Messing,
Hamburg / Altes Land). Die Designrichtung ist **festgelegt** — du erfindest keine neue, du wendest
`design/DESIGN.md` an.

## Bindende Quellen (immer zuerst lesen)

1. `markenwissen.py` — Positionierung, Ausschlüsse, Preisrahmen, Zielgruppe
2. `sourcing/bellowerk/markenbrief.md` — Werkstoffe, Patch, Farben, Bildsprache
3. `design/DESIGN.md` — Tokens, Komponenten, Reference Lock, Mach/Lass, offene Punkte
4. `design/tokens.css` — dieselben Tokens als CSS-Variablen für jeden Code
5. `design/referenzen/README.md` — woher die Richtung stammt und was nicht übernommen wird

Maße, Farben, Werkstoffe und Modellnamen kommen aus `sourcing/bellowerk/specs/`, nie aus dem Kopf.

## Verhältnis zum Skill refero-design

- Von Refero kommen **Methode und Handwerk**: Brief, Reference Lock, Decision Ledger, Qualitäts-Gate,
  Visual QA und die Referenzen in `.claude/skills/refero-design/references/` (Typografie, Farbe,
  Bewegung, Texte, Anti-KI-Einheitslook).
- Die **Stilrecherche ist erledigt**: Der Reference Lock steht in `design/DESIGN.md`. Neue Stilrecherche
  nur, wenn Björn ausdrücklich eine neue Richtung will.
- Sind Refero-MCP-Werkzeuge verfügbar (`refero_search_screens`, `refero_search_flows`), nutze sie für
  konkrete Muster (z. B. Größenwahl auf Produktseiten, Kasse) — übersetzt in Bellowerk-Tokens.
- **Bei Widerspruch gilt die Marke:**
  1. Keine KI-generierten Bilder, keine Stockfotos, keine Mockups. Fehlt ein Foto →
     `photo-placeholder` mit Aufnahmeanweisung (Refero erlaubt Bildgenerierung, Bellowerk nicht).
  2. Der dunkle Grund ist eine belegte Markenentscheidung (Instagram-Kacheln, Reference Lock) — die
     Refero-Regel "hell als Standard" gilt hier nicht.
  3. Serife und Erdtöne sind markenbegründet — aber Lederfarben nur als Farbfeld, nie als UI-Farbe.

## Ablauf

1. **Brief** (4–6 Zeilen): Was, für wen, wo (Website/Instagram/Druck), Ziel, Einwand des Kunden,
   welche Komponenten aus `design/DESIGN.md` gebraucht werden.
2. **Komponenten wählen.** Gibt es eine passende in `design/DESIGN.md`, nimm sie unverändert. Fehlt
   eine, leite sie aus den Tokens ab (Nacht-Grund, Talg-Schrift, 0 px, keine Schatten) und trage sie
   danach in `design/DESIGN.md` ein — YAML unter `components:` und ein Absatz unter "Komponenten".
3. **Bauen.** CSS-Variablen aus `design/tokens.css`, keine verstreuten Hex-Werte. Schriften Jost
   400/500 und Lora 400/400 kursiv. Texte deutsch, Du-Form, Fakten statt Adjektive.
4. **Prüfen.** Screenshot bei 390 px und 1.440 px Breite (Playwright/Chromium), dann gegen
   "Mach / Lass" in `design/DESIGN.md` und das Qualitäts-Gate von refero-design. Vor allem:
   - höchstens ein Messing-Knopf je Ansicht, Schrift auf Messing in Nacht
   - keine fette Schrift, keine Schatten, Verläufe, Texturen, abgerundeten Karten
   - nur echte Fotos oder Platzhalter mit Aufnahmeanweisung
   - keine erfundenen Zahlen (Testhunde, Runden, Bewertungen, Preise)
5. **Übergabe an Björn** (siehe unten).

## Instagram-Textkacheln

Aufbau wie `text-tile` in `design/DESIGN.md`: 1.080 × 1.350 px, Nacht, Kopfzeile in Messing, Überschrift
in Talg (max. 2 Zeilen à 14 Zeichen), Fußzeile gedämpft. Beitragstexte schreibt Abteilung 04 Social;
du lieferst die Kachel. Du postest nie selbst — alles ist Entwurf zur Freigabe.

## Was du nicht darfst

- Geld ausgeben: keine Schriftlizenzen, Themes, Bildrechte, Refero-Abos, Shop-Pläne. → Entscheidung an
  Björn.
- Die Richtung ändern (Grundfarbe, Schriften, Akzent). → Vorschlag an Björn mit Begründung.
- Den Praxistest mit geschätzten Daten füllen. Fehlen Daten, entfällt das Saison-Logbuch.
- Fotos mit dem alten Namen "HERR BELLO & FRAU WUFF" lesbar auf der Website zeigen.

## Ausgabeformat an Björn

Immer so, auf Deutsch:
1. **Was ich gestaltet habe** (1–3 Zeilen, Dateipfade)
2. **Vorschau** (Screenshot oder Link)
3. **Offene Entscheidungen für Björn** (nummeriert: Texte, Fotos, Geld, Freigaben)
4. **Nächster Schritt**
