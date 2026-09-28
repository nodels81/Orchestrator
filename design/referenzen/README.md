# Referenzen für das Bellowerk-Designsystem

Hier liegen die fremden Designsysteme, aus denen `design/DESIGN.md` abgeleitet ist. Sie sind
**Zutaten, keine Vorlage**: Bellowerk übernimmt einzelne, benannte Eigenschaften (siehe
"Reference Lock" in `design/DESIGN.md`) und kopiert keine Seite.

## Abgelegt (Volltext, MIT-Lizenz)

Quelle: [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md), Commit
`f6961238d5cddcf8042a74a70fc400ec67181abb` (21. September 2026), Lizenz in
`LICENSE-awesome-design-md`. Die Dateien sind Analysen der öffentlichen Websites, keine offiziellen
Unterlagen der Marken. Logos, Schriften und Bilder der Marken werden nicht verwendet.

| Datei | Rolle für Bellowerk | Was wir übernehmen | Was wir nicht übernehmen |
|---|---|---|---|
| `bugatti.DESIGN.md` | **Primärreferenz** | Dunkler Grund, gesperrte Versalien in Gewicht 400 (nie fett), Serifen-Fließtext, Foto als einzige Farbe, 0-px-Ecken, Knöpfe als Pille ohne Füllung, 120 px zwischen Abschnitten | Reines Schwarz (bei uns warm), Monospace-Schrift, eisblaue Links |
| `ferrari.DESIGN.md` | Nebenreferenz | Genau **ein** knapper Akzent auf fast schwarzem, leicht warmem Grund; helle Flächen nur für Listen und Tabellen | Rosso Corsa, eckige gefüllte Knöpfe, Verläufe |
| `starbucks.DESIGN.md` | Nebenreferenz | Tiefgrün (#1E3932, fast gleich Waldgrün #23352A) **nur** für Bänder und Fuß; Gold (bei uns Messing) nicht als Allzweck-Akzent | Heller Grund, Pillen-Karten, Schatten, freundlicher Einzelhandels-Ton |

## Refero Styles — passende Stile zum Nachladen

[styles.refero.design](https://styles.refero.design) (über 2.000 Stile, DESIGN.md im Beta kostenlos)
war aus der Cloud-Umgebung dieser Session gesperrt. Diese Stile passen laut Refero-Beschreibung und
sollten beim nächsten Mal als DESIGN.md hier abgelegt werden (Seite öffnen → DESIGN.md herunterladen →
als `<name>.DESIGN.md` in diesen Ordner):

| Stil | Link | Warum passend |
|---|---|---|
| ORYZO AI — "Darkroom product editorial" | [Stil öffnen](https://styles.refero.design/style/1f204e95-454a-437e-845b-c1b169d35607) | Ein Produkt wie ein Museumsstück auf warmem Dunkel ("Walnut Shadow"), cremefarbene Schrift, Versalien als Museumsschild-Stimme, jedes Produkt bekommt einen ganzen Bildschirm. Am nächsten an unserer Richtung. |
| Sequel — "private screening after dark" | [Stil öffnen](https://styles.refero.design/style/1bd3b2ba-9ad9-44ed-9130-03f9d94de821) | Schwarz, warmes Kinolicht auf Porträts, gesperrte Versalien-Labels, langsame gewichtete Bewegung. Quelle unserer Bewegungskurve. |
| ARKET — weiße Galerie | [Stil öffnen](https://styles.refero.design/style/3c605c8e-daf2-4d46-94d7-2cb705a93b7b) | Falls der Shop-Bereich später hell werden soll: Farbe nur im Foto, Haarlinien, sonst nichts. |
| Parallel — "warm editorial atelier" | auf styles.refero.design nach "Parallel" suchen | Helle Alternative (Papiergrund, Kinofotos mit Bernsteinlicht). Geprüft und verworfen, siehe `design/DESIGN.md`. |

Nicht passend, obwohl Hundemarke: **Bark** (Refero) — dunkel, aber gestauchte Versalien und aggressive
Haltung, das Gegenteil von Manufaktur.

Damit Claude die Stile selbst holen kann, gibt es zwei Wege:

1. In den Einstellungen der Cloud-Umgebung unter Netzwerkzugriff `styles.refero.design` freigeben.
2. Refero-MCP mit bezahltem Refero-Konto verbinden (siehe `.claude/skills/refero-design/HERKUNFT.md`).
