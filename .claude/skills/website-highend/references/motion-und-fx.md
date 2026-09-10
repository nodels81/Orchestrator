# FX-Studio — Bewegung und Effekte

Bewegung ist die Handschrift. Sie wird sparsam eingesetzt, sonst wird sie zum Kostüm.

## Grundsatz

Jede Animation beantwortet eine von drei Fragen: **Woher kommt das? Wohin geht es? Was gehört
zusammen?** Beantwortet sie keine, wird sie gestrichen. Deko-Bewegung erkennt man daran, dass
niemand sie vermisst, wenn sie weg ist — probier es aus, bevor du sie behältst.

## Werkzeuge und wann welches

| Werkzeug | Wofür | Wann nicht |
|---|---|---|
| CSS `transition` / `@keyframes` | Hover, Fokus, Aufklappen, alles Kleine | nie ersetzen durch JS |
| `animation-timeline: view()` | Einblenden beim Scrollen, Fortschrittsbalken, Sticky-Effekte | wenn Safari-Version zu alt, dann Rückfall auf IntersectionObserver |
| **GSAP + ScrollTrigger** | Choreografie über mehrere Elemente, Zeitleisten, Pinning | für einzelne Einblendungen — dafür ist es zu schwer |
| **Lenis** | gedämpftes Scrollen, Dauer ≈ 1.1 | bei `prefers-reduced-motion` sofort aus |
| **Three.js / OGL** | der eine WebGL-Moment pro Seite | für alles, was ein Video oder AVIF auch kann |
| **Rive** | interaktive Zustände, die auf Eingaben reagieren | für lineare Abspielsequenzen |
| **Lottie** | Rückfallebene für lineare Sequenzen | wenn Rive verfügbar ist |
| **View Transitions API** | Seitenwechsel, Filterwechsel im Katalog, Bild zu Produktseite | mit Rückfall auf harten Wechsel |

## Zeiten und Kurven

```css
:root{
  --dauer-mikro: 120ms;   /* Hover, Fokus, Umschalter */
  --dauer-klein: 240ms;   /* Aufklappen, Schublade, Menü */
  --dauer-gross: 520ms;   /* Sektionswechsel, Seitenübergang */
  --kurve-raus: cubic-bezier(.22,1,.36,1);      /* Eintritte: schnell an, sanft aus */
  --kurve-rein: cubic-bezier(.55,0,.68,.18);    /* Austritte: sofort weg */
  --kurve-weich: cubic-bezier(.65,0,.35,1);     /* Zustandswechsel */
}
```

- Eintritte klingen aus, Austritte verschwinden schnell. Gleiche Dauer in beide Richtungen wirkt träge.
- Staffelung 40–60 ms pro Element, höchstens sieben Glieder. Danach bewegt sich die Gruppe als Block.
- Nichts dauert über 600 ms, außer es ist ein Seitenwechsel.
- Elemente kommen aus der Richtung, in die man gescrollt hat, nicht von irgendwo.

## Harte technische Regeln

1. Animiert werden nur `transform`, `opacity`, `filter`, `clip-path`.
   Niemals `top`, `left`, `width`, `height`, `margin` — das erzwingt Layout und ruckelt.
2. `will-change` nur kurz vor der Animation setzen und danach entfernen. Dauerhaft gesetzt
   verbraucht es Speicher und macht die Seite langsamer, nicht schneller.
3. **Ein** schwerer Effekt pro Seite. Nicht zwei. Der Rest ist CSS.
4. Nichts bewegt sich beim Laden, bevor die Schrift steht. Layoutsprung = Abnahme nicht bestanden.
5. Scroll-Kapern über höchstens eine Sektion, und dort mit sichtbarem Fortschritt und Ausstieg.

## Abschaltmatrix — für jeden schweren Effekt Pflicht

```js
const sparsam =
  matchMedia('(prefers-reduced-motion: reduce)').matches ||
  (navigator.hardwareConcurrency ?? 8) <= 4 ||
  navigator.connection?.saveData === true ||
  (await navigator.getBattery?.())?.level < 0.2;

if (sparsam) { standbildZeigen(); } else { effektLaden(); }
```

- WebGL lädt verzögert über `IntersectionObserver`, nie im ersten Bundle.
- Außerhalb des Sichtfelds wird die `requestAnimationFrame`-Schleife gestoppt, nicht nur versteckt.
  Ein laufender Shader auf einem unsichtbaren Canvas frisst Akku.
- Zu **jedem** Effekt gehört ein statisches AVIF-Standbild als Ersatz. Das ist Pflichtlieferung.
- Bei `prefers-reduced-motion: reduce` bleibt nur Ein- und Ausblenden. Die Seite muss in diesem
  Zustand vollständig verständlich sein — das wird geprüft, nicht behauptet.

## Der eine WebGL-Moment (Bellowerk)

Fragment-Shader auf einer Normal-Map der echten Lederoberfläche. Der Lichtreflex auf der
Narbenseite folgt dem Mauszeiger, Messing bekommt eine anisotrope Spiegelung mit engem Glanzlicht.
Der Nutzer streicht über das Leder und sieht die Struktur kippen.

Das ist kein Effekt, sondern ein Produktargument: Man sieht, dass die Oberfläche echt ist und wie
sie auf Licht reagiert. Genau das kann ein Foto im Shop sonst nicht zeigen.

- Grundlage ist eine Aufnahme des echten Materials, keine erfundene Textur.
- Mobil: dieselbe Szene, gesteuert vom Neigungssensor; bei fehlender Berechtigung Standbild.
- Budget: unter 120 KB inklusive Textur, Ladezeit erst nach dem ersten sinnvollen Bildaufbau.

## Verbotene Muster

- Partikel ohne inhaltlichen Bezug
- Parallax auf jedem zweiten Element (einmal pro Seite, mit Bedacht)
- Text, der buchstabenweise hüpft, bei mehr als einer Überschrift
- Automatisch startende Videohintergründe mit Ton
- Cursor-Verfolger, die nichts anzeigen
- Ladeanimationen vor Inhalten, die längst geladen sind
- Sanftes Scrollen, das Tastatur- und Ankernavigation kaputt macht
- Effekte, die den Fokusring verdecken oder die Tabreihenfolge durcheinanderbringen
