---
name: website-highend
description: Webseiten und Shopsysteme auf Werbeagentur-Niveau bauen — Designsystem, Typografie, Motion und WebGL-FX, KI-Bildpipeline (Nano Banana), Shopify/Hydrogen-Shop, deutsches Onlinehandelsrecht, Performance- und Barrierefreiheits-Budgets. Nutzen bei jeder Landingpage, Startseite, Produktseite, Shop, Sektion, Redesign, jedem Designsystem, jeder Scroll-Animation oder Bildstrecke fürs Web.
---

# High-End-Websites und Shops

Du baust Seiten, die aussehen, als hätte sie die beste Werbeagentur der Welt gemacht — und die
gleichzeitig schnell, bedienbar und rechtssicher sind. Beides, nie nur eins.

Der vollständige Auftragsprompt liegt in `WEBSITE-PROMPT-ultra.md` im Wurzelverzeichnis.
Diese Datei ist die Arbeitsanweisung dazu.

## Reihenfolge — nie überspringen

1. **Leitidee** in einem Satz. Was behauptet diese Seite, das kein Wettbewerber behaupten kann?
   Bei Bellowerk: *Das Leder wurde vor dem Verkauf benutzt.* Ohne diesen Satz fängst du nicht an.
2. **Designsystem** (`references/designsystem.md`) — Tokens, bevor irgendein Bauteil entsteht.
3. **Bauteilübersicht** — jedes Element in allen Zuständen, auf einer eigenen Seite.
4. **Sektionen** — eine nach der anderen, jede gegen die Leitidee geprüft.
5. **FX** (`references/motion-und-fx.md`) — zuletzt und sparsam, ein schwerer Effekt pro Seite.
6. **Abnahmetor** (`references/qualitaetstor.md`) — Punkt für Punkt, schriftlich.

## Die sechs Regeln, an denen Templatearbeit scheitert

1. Ein Gedanke pro Bildschirm. Zwei Aussagen in einer Sektion werden geteilt.
2. Typografie trägt, nicht das Bild. Sprung Display zu Fließtext mindestens 1:4.
   Nimm die Bilder weg — sieht es immer noch gut aus, stimmt der Aufbau.
3. Größter Abstand mindestens achtmal der kleinste. Enge Seiten wirken billig.
4. Asymmetrie mit Absicht auf 12 Spalten. Alles mittig ist keine Entscheidung.
5. Licht kommt aus **einer** Richtung: Lichtkante oben, Schatten unten, nie ringsum.
6. Kein reines `#000`, kein reines `#fff`. Schwarz ist der dunkelste Markenton.

## Selbstprüfung nach jeder Sektion

Schreib in einem Satz hin, welcher bekannten Vorlage die Sektion ähnelt (Stripe-Hero,
Icon-Karten-Dreier, Verlaufs-Blob, Logo-Wolke). Überarbeite, bis die Antwort "keiner" lautet.
Diesen Satz behältst du nicht für dich, er kommt in die Übergabe.

## Nachschlagen

| Thema | Datei |
|---|---|
| Tokens, Farbe in OKLCH, Typoskala, Raster, Glanz und Oberfläche | `references/designsystem.md` |
| Bewegung, GSAP, Lenis, WebGL, Rive, Rückfallebenen, Verbote | `references/motion-und-fx.md` |
| Bildwelt, Nano-Banana-Pipeline, Prompt-Bauplan, Ausgabeformate | `references/bild-pipeline.md` |
| Shopify/Hydrogen, Bausteine, Zahlung, Versand, deutsches Recht | `references/shop-und-recht.md` |
| Budgets, Messung, Abnahmetor mit 20 Punkten | `references/qualitaetstor.md` |

## Marke Bellowerk — bindend

`markenwissen.py` und `sourcing/bellowerk/markenbrief.md` gelten unverändert auch fürs Web:

- Werkstoffe: Fettleder, Messing massiv, Buchschrauben. **Nicht** abbilden oder erwähnen:
  Nähte, Nieten, Stahl, Kunststoff, Klickverschlüsse, Gurtband.
- Ausschlüsse: keine Geschirre, keine Handelsware ohne Markenbezug, kein Preisargument,
  kein Einstieg über Windhunde.
- Preisrahmen: Halsband 69–99, Leine 89–139, Zubehör 25–59 EUR.
- Bildsprache: echte Fotos aus dem Betrieb, ehrliche Verschleißspuren, kein Studio-Look.
  **Produktbilder sind nie KI-erzeugt** — der Praxistest ist das Verkaufsargument, ein generiertes
  Produktfoto zerstört genau dieses Argument.
- Schrift: Lora als Serife, dazu eine schmale Grotesk für Bedienelemente und Preise.
- Farben: Grau, Dunkelbraun, Oliv, Cognac, Schwarz; Akzent Oliv, Braun, Kupfer/Messing.

## Was du nicht tust

- Kein Geld ausgeben. Tarife, Domains, kostenpflichtige Erweiterungen, Fototermine gehen als
  Entscheidung mit Preis und Begründung an Björn.
- Nichts veröffentlichen. Jede Seite ist ein Entwurf zur Freigabe.
- Keinen Grenzwert aus dem Budget anheben, um einen Effekt zu retten. Der Effekt fliegt.
