# Entscheidung 13.09.2026 — der Shop wird die Nachtwerkstatt

**Entscheidung Björn: Richtung 03 „Nachtwerkstatt".** Der Storefront-Aufbau von
Abteilung 10 Homepage wird nicht weitergebaut.

## Worum es ging

Zwei Bauten für denselben Shop liefen nebeneinander, ohne voneinander zu wissen.

| | 10 Homepage (A-2026-011/012) | Nachtwerkstatt |
|---|---|---|
| Theme | Storefront + Child-Theme | eigenes Theme |
| Farbwelt | hell, #F7F3EC / Waldgrün / Cognac | dunkel, #0E0C0A / Messing |
| Produkttitel | „Halsband Fettleder HB-01" | „Hamburg No. 1" |
| Preis | Staffel 69/79/89/99 nach Breite | 89 fest |
| Zahlung | nur Vorkasse | PayPal und Überweisung |
| Stand | Plan, sehr vollständig | gebaut und gemessen |

## Warum die Nachtwerkstatt

1. **Sie trägt das Verkaufsargument baulich.** Der Praxistest hat auf jeder
   Produktseite eine eigene Sektion, die Herkunftsangabe hängt am Haken und kann
   beim Ändern einer Vorlage nicht verlorengehen, die Ausschlussliste steht
   sichtbar. Bei Storefront wäre das ein Absatz unter vielen.
2. **Sie ist gebaut und geprüft**, nicht geplant: 14 Seiten, vier Breiten,
   Tastaturdurchlauf, Kontraste gegen WCAG gerechnet, Lauf ohne JavaScript.
3. **Die Richtung wurde am 11.09. aus vier Entwürfen gewählt**, nebeneinander
   gesehen. Diese Entscheidung wiegt schwerer als eine spätere Meinung.

## Was aus der Arbeit von 10 Homepage übernommen wird

Sie hat sauber gearbeitet — mit einem Markenwissen, das auf dem Server veraltet
war. Das ist nicht ihr Fehler. Vier Dinge sind gut genug, um sie zu behalten:

1. **Der Kaufweg-Testplan**, neun Punkte, konkret am Bestellknopf. Übernommen in
   `web/ABNAHME.md`.
2. **Passwortschutz bis zum Start.** Übernommen in `wordpress/EINRICHTEN.md`.
3. **Das Foto-Briefing mit acht Motiven.** Deckt sich weitgehend mit
   `web/aufnahmen/`; zwei Motive fehlten dort — Werkstatt und Verschleiß-Detail.
4. **Der Hinweis, Schriften selbst zu hosten statt von Google zu laden.** Genau
   diese Lücke hatte das Theme: Es verlangte Bodoni Moda, lieferte aber keine
   Schriftdatei mit.

## Was offen bleibt

Der eine Punkt, an dem 10 Homepage recht behält: **Pflegbarkeit.** Storefront
pflegt Automattic, das eigene Theme pflegt niemand von selbst. Wer den Shop in
zwei Jahren aktualisiert, muss das Theme mit aktualisieren. Das ist der Preis
für eine Seite, die aussieht wie diese Marke und nicht wie ein Baukasten.
Bewusst bezahlt, nicht übersehen.
