# Bilder generieren statt fotografieren (Stand 15. September 2026)

Björns Entscheidung: bis die Prototypen fertig sind, wird nicht fotografiert. Alle Bilder bis dahin
werden erzeugt. Diese Datei sagt, was dafür eingerichtet sein muss und wo die Grenze liegt.

## Was in dieser Umgebung fehlt

Claude hat hier **kein Bildwerkzeug**. Die Darstellungen in `../ansichten/` und `../shop/` sind von
Hand gezeichnete SVGs — gut für Maße und Proportion, aber keine Fotografie. Für erzeugte Fotos
braucht es einen externen Bilddienst, und dafür drei Dinge:

### 1. Ein API-Schlüssel als Umgebungsvariable

Nicht in den Chat, nicht ins Repo — in die **Environment Variables der Claude-Code-Umgebung**.
Übliche Namen: `GEMINI_API_KEY`, `OPENAI_API_KEY`, `BFL_API_KEY`, `REPLICATE_API_TOKEN`, `FAL_KEY`.

| Weg | Was dafür spricht |
|---|---|
| **Aggregator** (Replicate, fal.ai, Atlas Cloud) | ein Schlüssel, viele Modelle, Wechsel per Parameter — richtig, solange wir noch vergleichen |
| Google Gemini / Imagen | derzeit vorn bei Fotorealismus und feinen Texturen (Leder, Messing) |
| Black Forest Labs FLUX | stark bei reiner Produktfotografie ohne Text im Bild |
| OpenAI GPT Image | am zuverlässigsten, wenn **Schrift im Bild** stimmen muss — für den gravierten Patch relevant |
| Midjourney | ästhetisch top, **keine offizielle API** — von hier aus nicht steuerbar |

Kosten liegen je Bild im **Cent-Bereich**. Der Aufwand steckt nicht im Geld, sondern im Prompten und
Aussortieren: von zehn Bildern taugen zwei.

### 2. Netzfreigabe für genau diesen Host

Die Umgebung hat eine Netzsperre. Heute wurden `packhelp.de` und `ff-packaging.com` beim Abruf
blockiert — ein Schlüssel allein nützt also nichts, wenn der API-Host nicht erreichbar ist.
Freizugeben ist der jeweilige Endpunkt (z. B. `generativelanguage.googleapis.com`, `api.openai.com`,
`api.bfl.ai`, `api.replicate.com`, `fal.run`). Das ist eine Einstellung der Umgebung, nicht des Repos:
siehe code.claude.com/docs/en/claude-code-on-the-web.

### 3. Material von Björn — entscheidet mehr über die Qualität als das Modell

| Was | Wofür | Status |
|---|---|---|
| Vektorlogo BELLOWERK / Manufaktur | ohne echte Schrift erfindet jedes Modell Buchstabensalat auf dem Patch | **fehlt** |
| 1–2 Handyfotos je Lederfarbe bei Tageslicht | Farbreferenz; sonst erfindet das Modell Grau und Cognac neu | fehlt |
| Halsband flach mit Lineal | Proportionen, Patchlänge, Lochabstand | fehlt |
| Tech Packs und Zeichnungen | Maße, Beschläge, Konstruktion | vorhanden |
| Markenlook (Instagram-Ordner) | Licht, Stimmung, Bildsprache | vorhanden |

## Zwei Verfahren — der eigentliche Unterschied

**A · Bild komplett erzeugen (Text → Bild).** Schnell, kostet fast nichts, gut für Moodboards,
Konzeptbilder, Stimmung, Instagram. Schwäche: Das Modell erfindet Details. Es zeichnet fünf Löcher
als sieben, macht den Patch kürzer, erfindet eine Schnalle. Für Anschauung reicht das; für den Shop
nicht, solange es das Produkt nicht gibt.

**B · Echtes Produkt freistellen, Szene erzeugen** (Photoroom, Pebblely, Claid, Flair). Das Produkt
bleibt Pixel für Pixel echt, nur Hintergrund und Licht kommen aus der KI. Das ist der Standard im
E-Commerce und die saubere Lösung für Shop-Bilder — **braucht aber ein Foto**, geht also erst ab
dem Goldmuster.

Fahrplan daraus: **jetzt A** für Freigaben, Moodboard und Shop-Entwurf, **ab Goldmuster B** für die
echten Shop-Bilder. Verfahren A ersetzt nie das Foto eines Produkts, das man verkauft.

## Die Grenze, die nicht verhandelbar ist

Ein Produktbild im Shop darf das Produkt nicht falsch zeigen. Das ist keine Frage der Kennzeichnung,
sondern der Irreführung: Ein sauber als KI gekennzeichnetes Bild bleibt irreführend, wenn das
gelieferte Halsband anders aussieht. Farben gehören vor dem Verkauf fotografisch bestätigt.

Dazu kommt die Marke selbst. Das Verkaufsargument von Bellowerk ist der echte Betrieb — eine Saison
an fremden Hunden. Hochglanz-KI-Bilder arbeiten gegen genau diese Geschichte. Für Konzept und
Vorschau sind sie richtig; das Bild, das jemand vor dem Kauf sieht, sollte am Ende das echte Stück
zeigen.

## Wenn Zugang und Material da sind

1. Prompt-Baukasten in den Skill `bellowerk-produktbild` (Material, Licht, Kamera, Hintergrund,
   Markenlook, Negativliste gegen typische Fehler).
2. Je Modell 3–5 Varianten erzeugen, in `../ansichten/generiert/` ablegen, Prompt und Modell im
   Dateinamen führen, damit Treffer wiederholbar sind.
3. Die Varianten in die Freigabe-Mappe hängen — Björn wählt aus, verworfene Bilder bleiben liegen.
4. Ab Goldmuster: Verfahren B, und die erzeugten Bilder wandern aus dem Shop.
