# DelaTec – Logo

Logo-Entwurf für DelaTec (Smart Repair, Dellen- und Lackschaden-Reparatur, Kisdorf).

**Idee:** Ein kräftiges „D“, das diagonal geteilt ist – oben ein rotes, frisch lackiertes Segment,
darunter Weiß, getrennt durch eine feine Fuge wie eine Karosserie-Kante. Steht für „Schaden weg, Lack wie neu“.

| Datei | Verwendung |
|---|---|
| `delatec-logo.svg` / `.png` | Hauptlogo auf hellem Grund (Website, Rechnung, Briefkopf) |
| `delatec-logo-negativ.svg` / `.png` | auf dunklem Grund (Fahrzeugbeschriftung, Banner) |
| `delatec-icon.svg`, `delatec-icon-512.png` | App-/Favicon-Kachel |
| `delatec-instagram-profil.svg`, `delatec-instagram-profil-1080.png` | Instagram-Profilbild (1080×1080, passt in den Kreisausschnitt) |
| `delatec-wortmarke.svg` | nur Schriftzug |

**Farben:** Anthrazit `#1E2227` · Rot `#E3242B` · Weiß `#FFFFFF`

Der Schriftzug ist als Pfad gezeichnet, braucht also keine Schriftart. Nur die Claim-Zeile
(„SMART REPAIR · DELLEN · LACK“) nutzt Helvetica/Arial.

Ändern: `python3 generate.py` erzeugt die SVGs, `NODE_PATH=$(npm root -g) node render.js` die PNGs.
