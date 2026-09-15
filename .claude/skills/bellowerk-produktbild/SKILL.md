---
name: bellowerk-produktbild
description: Realistische Darstellungen fertiger Bellowerk-Produkte als SVG bauen und rendern — Leder, Messing, gravierter Patch — für Shop-Entwürfe, Freigaben und Präsentationen. Nutze das, wenn jemand sehen will, wie ein Modell "in echt" oder "fertig" aussieht, wenn ein Bild für die Shop-Seite gebraucht wird oder ein Foto fehlt. Nutze es auch, um ehrlich zu erklären, warum eine Darstellung kein Foto ersetzt.
---

# Produktdarstellungen für Bellowerk

Es gibt keine Bilderzeugung in dieser Umgebung und keine Fotos vom fertigen Stück, solange der Patch
noch den alten Markennamen trägt. Was geht: eine maßstäbliche Darstellung aus dem Tech Pack, mit der
sich Proportion, Patchgröße und Beschläge beurteilen lassen. Das ist nützlich — und es ist kein Foto.

**Die Regel dahinter:** Jede Darstellung trägt sichtbar den Vermerk *"Darstellung nach Tech Pack
HB-XX vX.Y — keine Fotografie"*. Ein Bild, das als Foto durchgeht, obwohl es keins ist, kostet
Vertrauen, sobald es jemand merkt — im Shop wäre es irreführend.

## Stehende Regel: Björn will sehen, worüber geredet wird

Er entscheidet am Bild, nicht am Fließtext (seine Ansage vom 15.9.2026). Also bekommt **jedes
Konzept eine Darstellung**, nicht nur Produkte: Verpackung als Auspack-Sequenz, Beschläge als
Teileübersicht im Maßstab, jedes neue Modell als Ansicht. Wer ein Blatt in der Freigabe-Mappe anlegt
und nur Text hineinschreibt, ist noch nicht fertig. Zwei bis drei Panels reichen meist — die
Reihenfolge zeigen, nicht das Material feiern.

Die fertigen Darstellungen liegen in `sourcing/bellowerk/ansichten/` als SVG und PNG;
`freigabe/bauen.py` verkleinert sie automatisch für Mappe und Shop.

## Aufbau (Vorlage: `sourcing/bellowerk/shop/HB-01-ansicht.svg`)

Maßstab 3 px = 1 mm, damit Beschläge Platz haben. Reihenfolge der Ebenen:

1. **Grund**: heller Verlauf, nicht reinweiß — sonst wirkt alles freigestellt und flach.
2. **Kontur** einmal als `<path id="kontur">` in `<defs>`, danach mehrfach per `<use>`:
   Füllung, Glanz, Kante. Eine Kontur, mehrere Rollen — spart Fehler beim Ändern.
3. **Leder**: senkrechter Verlauf (Licht von oben: dunkel, hell, mittel, dunkler, dunkel) plus
   `feTurbulence` als Narbe. Für Fettleder `baseFrequency` um **0.045**, `numOctaves` 5, Alpha-Slope
   ~0.85; höhere Frequenzen sehen aus wie Rauschen, nicht wie Leder.
4. **Kante**: dunkler Strich auf der Kontur, darunter ein weißer Strich mit 3 px Versatz — das liest
   sich als geschrägte, polierte Kante.
5. **Messing**: linearer Verlauf mit fünf bis sechs Stopps (dunkel/hell/mittel/dunkel/hell/dunkel).
   Ein Zweistopp-Verlauf sieht nach Plastik aus. Schraubenköpfe radial, mit kleinem hellen Punkt
   links oben.
6. **Patch**: eigenes Kornfilter, Gravurtext mit hellem Schatten nach unten (`feDropShadow` in
   Lederfarbe) — so wirkt der Text eingebrannt statt aufgedruckt.
7. **Bildunterschrift** mit Modell, Größe, Farbe und dem Darstellungs-Vermerk.

## Rendern

Playwright mit `executable_path="/opt/pw-browsers/chromium"`, `device_scale_factor=2`, Clip auf die
SVG-Maße. Für Seiten als JPEG bei Qualität 88 exportieren (ein PNG mit Verläufen wird unnötig groß);
`sourcing/bellowerk/freigabe/bauen.py` macht das mit.

## Farben aus dem Markenwissen

Leder grau „washed stone" `#8A8984`, dunkelbraun, oliv, cognac `#9A5B2C`, schwarz.
Messing `#C9A24E` als Mitte. Patch immer cognac/mittelbraun, auf allen Lederfarben gleich.

## Grenze

Sobald es Fotos vom Goldmuster gibt, ersetzen sie die Darstellung — in dieser Reihenfolge:
Vektorlogo → Goldmuster mit richtigem Patch → Shooting nach der Aufnahmeliste auf der Shop-Seite.
Bis dahin hält die Darstellung den Platz frei und zeigt, was hingehört.
