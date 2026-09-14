# Prüfliste — vor dem Abliefern jeder Oberfläche

Abhaken heißt: nachgesehen, nicht angenommen. Was nicht geprüft wurde, gilt als kaputt.

## 1. Aufgabe

- [ ] Der eine Satz ("wer, wozu, auf welchem Gerät") steht und die Seite erfüllt ihn.
- [ ] Genau eine Hauptaktion, optisch stärker als alles andere.
- [ ] Ein Fremder erkennt in drei Sekunden, was das ist und was er hier tun kann.

## 2. Struktur

- [ ] Überschriften in Rangfolge: ein `h1`, darunter `h2`, keine Ebene übersprungen.
- [ ] DOM-Reihenfolge = Leserichtung (nicht per CSS umsortiert).
- [ ] Abstände aus der Skala (4/8/12/16/24/32/48/64), keine krummen Werte.
- [ ] Zusammengehöriges steht enger beieinander als Getrenntes.

## 3. Lesbarkeit

- [ ] Fließtext ≥ 4,5:1 Kontrast, große Schrift/Icons/Rahmen ≥ 3:1 — mit `kontrast.py` gerechnet.
- [ ] Zeilenlänge 60–75 Zeichen, Zeilenhöhe 1,5.
- [ ] Keine Information nur über Farbe (überfällig = rot **und** das Wort "überfällig").
- [ ] Kein Text als Bestandteil eines Bildes.

## 4. Zustände

- [ ] Leer: Satz + Aktion, kein leerer Kasten.
- [ ] Lädt: Platzhalter in Zielgröße, ab 400 ms sichtbar, kein Sprung beim Nachladen.
- [ ] Fehler: was war, was es bedeutet, was jetzt zu tun ist.
- [ ] Zu viele Einträge: Filter, Paginierung oder Deckel.
- [ ] Zu langer Text: bricht um oder wird gekürzt, ohne das Layout zu sprengen.

## 5. Bedienung

- [ ] Alles per Tastatur erreichbar, Tab-Reihenfolge sinnvoll, Fokusring sichtbar (≥ 2 px, ≥ 3:1).
- [ ] Esc schließt, Enter bestätigt, kein Fokus, der im Dialog verloren geht.
- [ ] Tippziele ≥ 44 × 44 px mit ≥ 8 px Abstand.
- [ ] Eingabefelder ≥ 16 px Schrift, Label über dem Feld, Fehler am Feld statt nur oben.
- [ ] Formular: bereits Eingegebenes geht bei einem Fehler nicht verloren.

## 6. Geräte und Vorlieben

- [ ] 390 px Breite: kein Querscrollen, ≥ 16 px Rand an jeder Kante.
- [ ] 1280 px: Inhalt nicht auf die volle Breite gezerrt (`max-width` setzen).
- [ ] Dunkelmodus geprüft — Hintergrund und Schrift ausdrücklich gesetzt, nicht geerbt.
- [ ] `prefers-reduced-motion`: Animationen aus.
- [ ] Bilder mit `alt`; dekorative Bilder `alt=""`.
- [ ] Seite funktioniert ohne Bilder und ohne Webfont (Fallback `Georgia, serif`).

## 7. Letzter Blick

- [ ] Selbst durchgeklickt, im Browser, in beiden Breiten, hell und dunkel.
- [ ] Zahlen und Datumsangaben im deutschen Format.
- [ ] Keine Blindtexte, keine Platzhalterlogos, keine erfundenen Werte in der Auslieferung.
