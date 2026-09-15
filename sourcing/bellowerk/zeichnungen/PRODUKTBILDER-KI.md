# Von der Zeichnung zum realistischen Produktbild (KI-Plattformen)

Für Vorab-Visualisierung: Website/Vorbestellung vor der ersten Musterlieferung, Pitch-Decks,
Konzeptabstimmung mit Björn, Referenzbild für Lieferanten zusätzlich zur bemaßten Zeichnung.

**Nicht dafür gedacht:** Instagram-Beiträge. `abteilung_social.py` schreibt es bindend fest —
"Du erfindest keine Bilder und forderst keine KI-Generierung an" — echte Fotos von echten Hunden,
kein Studio-Look. Ein KI-Render ersetzt nie ein Foto vom fertigen Produkt am Hund. Wird ein
KI-Bild trotzdem öffentlich verwendet (Vorbestellseite, Werbung), muss es klar als Visualisierung
gekennzeichnet sein — in der EU seit August 2026 für KI-generierte Bildwerbung ohnehin Pflicht
(AI Act, Transparenzpflichten Art. 50).

## 1. Zeichnung vorbereiten

- Ausgangsmaterial: `HB-01-halsband.png` etc. aus diesem Ordner (bemaßt, schwarz-weiß, mit
  Maßlinien und Beschriftung).
- Für die KI nur die reine Kontur brauchbar — Maßlinien, Bemaßungstext und Titelzeile stören den
  Bildgenerator. Zwei Wege:
  - Schnell: Screenshot des Produktumrisses aus dem SVG zuschneiden (Inkscape/Figma: Maßlinien-
    Ebene ausblenden, dann als PNG exportieren).
  - Sauberer: eigene Silhouette-Ebene im SVG pflegen (`render.py` als Vorlage), ohne Maße — einmal
    anlegen, für jedes Update wiederverwendbar.
- Das bereinigte Umriss-PNG ist das **Referenzbild** (Formvorgabe), nicht der finale Prompt-Text.

## 2. Plattform wählen

| Plattform | Stärke für diesen Zweck | Referenzbild-Funktion | Kosten |
|---|---|---|---|
| **ChatGPT / GPT-Image** (chatgpt.com, API) | Folgt Textvorgaben zu Material/Maßen am genauesten, gut für Chicago-Schrauben, Gravur-Text lesbar | Bild hochladen + "nutze diese Kontur/Proportion als Vorlage" | ab ~20 $/Monat Plus, oder API nach Bild |
| **Midjourney** (v7, discord.com/midjourney.com) | Beste Foto-/Lichtqualität, "Omni Reference" (`--oref`) hält Form über mehrere Varianten stabil | `--oref` (Formreferenz) + `--sref` (Stilreferenz, z. B. eigenes Foto für den Bellowerk-Look) | ab 10 $/Monat |
| **Adobe Firefly** (firefly.adobe.com) | Kommerziell rechtssicher lizenziert (wichtig, falls Bild in Werbung/Anzeigen landet), gute Photoshop-Integration für Nachbearbeitung | "Structure Reference" hält die Kontur der Zeichnung | in Creative-Cloud-Abo enthalten |
| **Leonardo.ai** | Viele Fein-Regler (Material, Beleuchtung), Motion-Referenz für Konsistenz über Produktserien | Image Guidance mit Stärkeregler | kostenloses Kontingent, ab ~10 $/Monat |
| **Stable Diffusion + ControlNet** (lokal oder über Automatic1111/ComfyUI) | Volle Kontrolle: ControlNet "Canny" oder "Lineart" hält die Strichzeichnung exakt als Gerüst | ControlNet-Bild = die Zeichnung selbst | kostenlos, braucht GPU oder Cloud-Miete |

Für den Einstieg reicht **ein** Tool. Empfehlung: ChatGPT/GPT-Image für die ersten Versuche (kein
Zusatz-Tool nötig, gut im Befolgen der Materialvorgaben), Midjourney sobald Bildqualität für einen
Pitch oder eine Landingpage zählt.

## 3. Prompt-Baukasten (Fakten aus `markenbrief.md`, nicht erfinden)

Jeder Prompt bekommt dieselben festen Bausteine — sie stammen aus dem Markenbrief und den Specs,
nicht aus der Fantasie des Bildgenerators:

```
Produkt:      [Modell + Kurzbeschreibung, z. B. "dog collar, size M, 25 mm width"]
Material:     single-layer vegetable-tanned oiled cowhide leather, [Farbe: cognac/oliv/dunkelbraun/
              grau/schwarz], full grain, NO stitching, NO rivets
Beschläge:    solid unlacquered brass hardware with natural patina — roller buckle, welded D-ring,
              Chicago screws with domed heads (NOT nickel, NOT zinc alloy, NOT chrome)
Flechtung:    (nur HB-02/LE-01) 3-strand mystery braid, no other braid pattern
Patch:        engraved leather nameplate "BELLOWERK" in spaced capitals, "Manufaktur" in script below
Farbwelt:     forest green #23352A, olive #566347, cognac #9A6238, brass #B08D57 as accent tones
Look:         daylight, neutral light wood or linen surface, soft shadow, DSLR product photography,
              shallow depth of field — NOT studio white background, NOT glossy/plastic look
Format:       --ar 4:5 (Midjourney) bzw. 4:5 Hochformat
```

Beispiel-Prompt HB-01 (Midjourney mit Formreferenz):

```
[Kontur-PNG als --oref] product photography of a leather dog collar, size M, 25mm width,
single-layer vegetable-tanned oiled cowhide, cognac color, full grain, no stitching, no rivets,
solid unlacquered brass roller buckle and welded D-ring with natural patina, brass Chicago screws
domed head, engraved leather nameplate "BELLOWERK / Manufaktur", laid flat on light oak wood
surface, soft natural daylight from the side, shallow depth of field, DSLR macro,
shot on Hasselblad --ar 4:5 --oref [URL des Konturbilds] --ow 200
```

Negativ-Liste (Stable Diffusion/Firefly) bzw. anhängen "no ... " (Midjourney/GPT-Image):
`stitching, seams, rivets, nylon webbing, plastic buckle, zinc alloy, chrome plating, studio
white background, glossy render, cartoon, illustration`

## 4. Formtreue sicherstellen (Referenzbild statt nur Text)

Reiner Text erzeugt oft ein plausibles, aber falsch proportioniertes Halsband. Deshalb immer das
bereinigte Konturbild aus Schritt 1 als Bildreferenz mitgeben:

- **Midjourney**: `--oref <Bild-URL> --ow 100–300` (Omni Reference; höherer `--ow`-Wert = Kontur
  wird stärker erzwungen). Bild vorher irgendwo hochladen (z. B. als Discord-Anhang).
- **ChatGPT/GPT-Image**: Konturbild im Chat anhängen, dazuschreiben "behalte Proportionen, Loch-
  abstand und Schnallenposition exakt wie im Referenzbild bei".
- **Adobe Firefly**: "Structure Reference" hochladen, Regler auf mittel-hoch.
- **Stable Diffusion**: ControlNet-Modell "Lineart" oder "Canny", Konturbild als Input, Denoising
  0.6–0.8.

## 5. Konsistenz über mehrere Motive (Farben, Größen, Serie)

Für ein zusammenhängendes Set (z. B. HB-01 in allen fünf Farben, oder HB-01 + LE-01 + PATCH-01
zusammen):

- Gleicher Seed/gleiche Referenz wiederverwenden, nur den Farb-Begriff im Prompt austauschen.
- Midjourney: zusätzlich `--sref <eigenes Vorbild-Foto>` setzen (z. B. eines der Fotos aus
  `../bilder/`) für denselben Licht-/Oberflächen-Look über alle Varianten.
- Ergebnisse nebeneinanderlegen und gegen `markenbrief.md` prüfen (Schritt 6), bevor sie irgendwo
  verwendet werden — Serien wirken erst stimmig, wenn alle dieselben Fehler *nicht* haben.

## 6. Qualitätskontrolle gegen die Spec (nicht überspringen)

KI-Bildgeneratoren erfinden gern Details, die dem Markenbrief widersprechen. Vor Verwendung jedes
Bild gegenchecken:

- [ ] Naht sichtbar? → Ablehnen (Fettleder ist nahtlos, nur Chicago-Schrauben)
- [ ] Nieten sichtbar? → Ablehnen
- [ ] Beschläge glänzend/verchromt/silbern statt mattes Messing mit Patina? → Ablehnen oder Inpainting
- [ ] Schnalle als Klickverschluss statt Rollschnalle? → Ablehnen
- [ ] Gravurtext lesbar und korrekt ("BELLOWERK", nicht "BELLOWERK" verzerrt/falsch geschrieben)? →
      Gravur-Text macht KI oft falsch, ggf. in Photoshop/Firefly nachträglich einsetzen
      (generative Fill nur auf den Patch-Bereich)
- [ ] Flechtung (falls HB-02/LE-01): 3-strängiger Mystery Braid, nicht x-beliebiges Flechtmuster
- [ ] Maßverhältnis plausibel zur Zeichnung (Breite/Länge/Lochabstand)?

Für falsche Details lohnt sich gezieltes **Inpainting** (nur den betroffenen Bildbereich neu
generieren lassen, z. B. nur die Schnalle) statt das ganze Bild zu verwerfen — in ChatGPT per
Bildmaskierung, in Midjourney per "Vary (Region)", in Firefly per "Generative Fill".

## 7. Nachbearbeitung

- Auflösung hochskalieren: Midjourney "Upscale", Firefly "Enhance", oder Topaz/Real-ESRGAN für
  Druck-/Web-Qualität.
- Hintergrund/Beleuchtung feinjustieren in Photoshop oder Firefly (generative Fill für Hintergrund,
  falls er zu clean/studiohaft wirkt — der Markenlook ist bewusst nicht steril).
- Für Web: als JPG exportieren, Dateigröße wie bei Lieferantenfotos im Blick behalten (siehe
  `../bilder/README.md`), aber deutlich als Konzeptbild/Visualisierung kennzeichnen, nicht als
  Produktfoto ausgeben.

## Kurzfassung

1. Zeichnung ohne Maßlinien als Konturbild exportieren.
2. Plattform wählen (Einstieg: ChatGPT/GPT-Image; für Pitch-Qualität: Midjourney mit `--oref`).
3. Prompt aus dem Baukasten (Schritt 3) mit den Fakten aus `markenbrief.md` füllen — nichts dazu-
   erfinden.
4. Konturbild als Formreferenz mitgeben, nicht nur Text.
5. Gegen die Spec-Checkliste prüfen, falsche Details gezielt per Inpainting korrigieren.
6. Als Visualisierung kennzeichnen, nicht als Ersatz für die "echtes Foto"-Regel der Abteilung
   Social Media.
