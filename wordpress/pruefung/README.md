# Prüfung

Zwei Abzüge vom Markup, das WooCommerce für Warenkorb und Kasse ausgibt,
verbunden mit den echten Stilen aus `../bellowerk/assets/`.

```
pip install playwright        # der Browser selbst ist meist schon da
python3 wordpress/pruefung/pruefen.py
```

## Wozu

Beim Anlegen von `shop.css` liefen fünf von acht Messungen über, bis zu
348 px bei 320 px Fensterbreite. Zwei Ursachen, beide unsichtbar beim
bloßen Ansehen am großen Schirm:

1. Eine Rasterspalte `1fr` ist mindestens so breit wie ihr schmalster
   unteilbarer Inhalt. Die Versandzeile „Abholung in Harsefeld nach
   Absprache" machte den Summenblock 586 px breit. Behoben mit
   `minmax(0,1fr)`.
2. Ein `<table>` auf `display:block` behält in Blink eine selbsttätige
   Mindestbreite in Höhe seines Inhalts — hier 520 px in einem 280 px
   breiten Kasten. Die Seite lief dadurch nicht über, der Warenkorb ließ
   sich aber nur noch seitwärts schieben. Behoben mit `min-width:0`.

Der zweite Fall ist der Grund, warum hier nicht nur die Seite gemessen
wird, sondern auch das Formular. Eine Seite, die stillsteht, während ihr
Inhalt wegrutscht, besteht jede oberflächliche Prüfung.

## Was hier nicht geprüft wird

Tastaturführung, Ausgabe ohne JavaScript und die Kontraste. Die Kontraste
lassen sich an dieser Stelle nicht zuverlässig messen, weil Knöpfe auf
einem Verlauf stehen und eine Sonde nur einfarbige Flächen findet — der
Kassenknopf wurde von Hand gerechnet: `--nacht` auf dem dunklen Ende von
`--messing-tief`, 5,58:1.
