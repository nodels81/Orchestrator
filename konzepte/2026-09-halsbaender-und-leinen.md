# Konzeptvorlage 01 Innovation — Halsbänder und Leinen

Stand 10.09.2026 · Abteilung 01 Innovation

## Entscheidung Björn, 10.09.2026

| Konzept | Entscheidung | Änderung gegenüber der Vorlage |
|---|---|---|
| **A · NS-01 Namensschild Messing** | **freigegeben** | zusätzlich als Lederpatch, siehe NS-02 |
| **NS-02 Namenspatch Leder** | **neu, freigegeben** | Alternative zum Messingschild, gleicher Preis, gleiche Befestigung |
| **B · KO-01 Koppel für zwei Hunde** | **freigegeben** | — |
| **D · HB-03 Zugstopp-Halsband** | **freigegeben** | Auflage bleibt: keine Windhund-Kommunikation |
| C · WD-01 Werkstattdurchsicht | offen | — |
| E · PF-01 Pflegeset | offen | — |

Dazu die Vorgabe: Die Kollektion bekommt Namen, das Grundmodell heißt **Hamburg No. 1**.
Ausgearbeitet in `konzepte/kollektion-01-hamburg.md`. Dort steht auch die eine Frage, die vor
der Einführung des Namens geklärt sein muss.

**Beide Namensschilder sind bereits spezifiziert.** `sourcing/bellowerk/specs/PATCH-01-markenpatch.md`
enthält Variante N (Hundename in Leder graviert, Versalien mit Serife, bis 10 Zeichen) und
Variante B (Messingschild H62, 1,5 mm, geätzt, gebürstet, unlackiert, zwei Buchschrauben).
Es ist also keine neue Spezifikation nötig, sondern eine Entscheidung im Einkauf: Frage 5 der
RFQ fragt den Hersteller bereits, ob er Einzelstücke auf Zuruf gravieren kann und zu welchem
Preis. Diese Antwort entscheidet, ob NS-01 und NS-02 als Lagerware oder als Anfertigung laufen.

Jedes Konzept hat die sieben Prüffragen aus `abteilung_innovation.py` durchlaufen.
Konzepte, die durchgefallen sind, stehen mit Grund am Ende. Keines dieser Konzepte
verlangt eine Ausgabe: der nächste Schritt ist jeweils ein Muster oder ein Testlauf
im eigenen Betrieb.

---

## A · NS-01 Namensschild aus Messing, zum Anschrauben  ·  FREIGEGEBEN

**Was** Ein graviertes Vollmessingschild, 45 × 12 mm, das mit denselben 5-mm-Buchschrauben
auf jedes Bellowerk-Halsband kommt. Name auf der Vorderseite, Telefonnummer auf der Rückseite.
Abnehmbar, weil geschraubt und nicht genietet.

**Für wen** Jeder Kunde, der schon gekauft hat. Und jeder, der eine Marke am Halsband klappern hört
und das nicht mag.

**Preis** 34 EUR als Zubehör, 29 EUR beim Kauf zusammen mit einem Halsband.

**Warum das trägt** Es verkauft an Bestandskunden, ohne ein neues Material einzuführen. Messing und
Buchschrauben liegen schon in der Stückliste, die Gravur kann derselbe Betrieb machen wie den Patch.
Personalisierung ist der einzige Aufpreis, den Kunden im Premiumsegment fast nie hinterfragen.
Und es löst ein echtes Ärgernis: klappernde Anhänger am Ring.

**Nächster Schritt** Ein Muster über den bestehenden Patch-Lieferanten anfragen, Gravurtiefe und
Kantenbruch prüfen. Spec kann der Agent `china-spec-writer` aus PATCH-01 ableiten.

---

## A2 · NS-02 Namenspatch aus Leder  ·  FREIGEGEBEN

**Was** Derselbe Gedanke wie NS-01, aber in Leder statt Messing: ein Streifen Kontrastleder
in Cognac, mit dem Hundenamen in gesperrten Serifen-Versalien lasergraviert, mit zwei
Buchschrauben aufgeschraubt. Entspricht Variante N in `PATCH-01-markenpatch.md`.

**Für wen** Kunden, denen Messing am Hals zu viel Metall ist, und alle, die den ruhigeren Look
wollen. Erfahrungsgemäß ist das etwa die Hälfte.

**Preis** 34 EUR als Zubehör, 29 EUR zusammen mit einem Halsband. Gleicher Preis wie NS-01,
damit die Wahl eine Geschmacksfrage bleibt und keine Preisfrage wird.

**Maße** PA-M 85 × 18 mm für Bänder von 25 bis 40 mm, PA-S 65 × 14 mm für 20 mm.
Namen über 10 Zeichen brauchen PA-L 110 × 18 mm. Versalhöhe 6 mm bei PA-M, 5 mm bei PA-S,
Sperrung +20 Prozent.

**Warum die zwei Varianten zusammengehören** Sie teilen Lochabstand, Schraube und Position auf
dem Band. Der Kunde kann später tauschen, ohne ein neues Halsband zu kaufen. Genau das ist das
Verkaufsargument: geschraubt statt genietet, also austauschbar. Ein zweites Schild ist damit ein
naheliegender Nachkauf, etwa wenn ein zweiter Hund dazukommt.

**Nächster Schritt** Keine neue Spezifikation nötig. Im Einkauf beide Varianten in die
Musterbestellung aufnehmen und Frage 5 der RFQ beantworten lassen.

---

## B · KO-01 Koppel für zwei Hunde  ·  FREIGEGEBEN

**Was** Ein Y-Stück aus Fettleder mit drei Messingringen, das zwei Hunde an eine Leine bringt.
Zwei Schenkel je 30 cm, mittlerer Ring für den Karabiner der LE-01.

**Für wen** Mehrhundehalter und die eigene Kundschaft aus Gassi-Service und Pension.

**Preis** 79 EUR.

**Warum das trägt** Das ist das einzige Konzept der Liste, für das Björn der Kunde selbst ist. Wer
täglich zwei fremde Hunde führt, weiß binnen einer Woche, ob die Schenkellänge stimmt und wo sich
das Leder dreht. Der Praxistest ist hier nicht Marketing, sondern Entwicklungsarbeit. Am Markt gibt
es Koppeln fast nur aus Gurtband oder mit Stahlwirbel, also genau in den Werkstoffen, die wir
ohnehin ausschließen.

**Achtung** Ein Wirbel gegen das Verdrehen wäre der naheliegende Beschlag, ist aber als Stahlteil
ausgeschlossen. Entweder ein Messingwirbel ist beschaffbar, oder die Verdrehung wird über die
Geometrie gelöst. Das ist die entscheidende Frage im Muster.

**Nächster Schritt** Zwei Wochen Eigenbau und Selbsttest im Gassi-Service, bevor irgendetwas
angefragt wird.

---

## C · WD-01 Werkstattdurchsicht

**Was** Kein Produkt, sondern eine Leistung. Der Kunde schickt sein Halsband nach zwei Jahren ein.
Wir fetten nach, prüfen Löcher und Kanten, ziehen die Buchschrauben nach, polieren das Messing und
schicken es mit einem kurzen Befund zurück.

**Für wen** Jeder Käufer, zwei Jahre nach dem Kauf. Anschreiben aus der Bestellhistorie.

**Preis** 29 EUR inklusive Rückversand.

**Warum das trägt** Es macht aus dem Satz "Reparatur statt Ersatz" eine Rechnung. Es bringt
Bestandskunden nach zwei Jahren zurück, genau dann, wenn sie über ein zweites Halsband nachdenken.
Und es erzeugt nebenbei das wertvollste Material, das die Marke hat: Vorher-Nachher-Bilder von echten
Halsbändern nach zwei Jahren Gebrauch, mit Befund. Genau die Bilder braucht die Website, und niemand
kann sie erfinden.

**Nächster Schritt** Ablauf und Rückversandweg festlegen, dann bei den nächsten zehn Bestellungen
eine Karte beilegen.

---

## D · HB-03 Zugstopp-Halsband aus Fettleder  ·  FREIGEGEBEN

**Was** Halsband mit Zugstoppschlaufe, komplett aus Leder und Messing, ohne Kette. Zieht sich bei
Zug auf Halsumfang zusammen und nicht weiter, damit der Hund nicht herausrutscht.

**Für wen** Hunde mit schmalem Kopf im Verhältnis zum Hals und Hunde, die beim Rückwärtsgehen aus
dem Halsband schlüpfen. Das betrifft viele Gebrauchs- und Mischlingshunde.

**Preis** 99 EUR.

**Warum das trägt** Technisch ein kleiner Schritt von HB-01 aus, weil nur eine zweite Schlaufe und
zwei Ringe dazukommen. Löst ein Sicherheitsproblem, das Halter wirklich haben, und ist deshalb
leichter zu verkaufen als eine weitere Farbe.

**Auflage** Zugstoppbänder sind am Markt eng mit Windhunden verknüpft, und dort sitzt Bolleband vor
Ort. Dieses Modell wird ausschließlich über Gebrauchs- und Familienhunde kommuniziert. Keine
Windhundbilder, keine Windhundgrößen, keine Ansprache in dieser Richtung. Ohne diese Auflage
verstößt es gegen den harten Ausschluss.

**Nächster Schritt** Zeichnung als Ableitung von HB-01, ein Muster, eine Saison Praxistest.

---

## E · PF-01 Pflegeset mit Werkstattanleitung

**Was** Lederfett, Poliertuch für Messing und eine gedruckte Anleitung aus der Werkstatt, im
Bellowerk-Karton. Die Anleitung sagt, wie oft, wie viel und was man gerade nicht tun soll.

**Für wen** Jeder Käufer, direkt beim Kauf als Zusatz.

**Preis** 44 EUR.

**Warum das trägt** Es ist die Verlängerung des Verkaufsarguments: Ein Produkt, das besser wird,
braucht Pflege, und wer pflegt, bindet sich. Gleichzeitig senkt es Reklamationen wegen hart
gewordenen Leders.

**Auflage** Fett und Tuch sind zugekauft. Ohne eigene Anleitung, eigene Verpackung und eigene
Dosierempfehlung wäre das reine Handelsware und damit ausgeschlossen. Der Markenbezug muss aus der
Anleitung kommen, nicht aus einem aufgeklebten Etikett.

**Nächster Schritt** Ein Fett auswählen, das zum eigenen Fettleder passt, und die Anleitung
schreiben. Erst danach über Einkauf reden.

---

## Reihenfolge der Umsetzung nach der Freigabe

1. **NS-01 und NS-02** — zusammen als ein Vorgang. Spezifikation liegt vor, es fehlt nur die
   Antwort des Herstellers auf die Einzelgravur. Schnellster Weg zu neuem Umsatz.
2. **KO-01 Koppel** — zwei Wochen Eigenbau und Selbsttest im Gassi-Service, bevor angefragt wird.
   Offene Frage bleibt der Wirbel.
3. **HB-03 Zugstopp** — Zeichnung als Ableitung von HB-01, dann Muster, dann eine Saison Praxistest.
4. C und E, sobald entschieden.

---

## Nicht vorgelegt, mit Grund

- **Schleppleine 5 bis 10 m aus Fettleder** — Prüffrage 3 und 6. Leder in dieser Länge wiegt zu viel,
  saugt sich im Nassen voll und schleift über Boden. Das Produkt wäre schlechter als die Alternative
  aus Gurtband, und dieses Material ist ausgeschlossen. Kein guter Kompromiss verfügbar.
- **Geschirr in jeder Form** — harter Ausschluss aus `markenwissen.py`.
- **Halsband mit Schnellverschluss** — Prüffrage 3. Ein Klickverschluss ist ausgeschlossen, und in
  Messing gäbe es ihn nur als Steckschloss, das bei Zug klemmt. Die Schnalle bleibt besser.
- **Halterung für GPS-Tracker oder AirTag** — Prüffrage 3 und 6. Kunststoff ist ausgeschlossen, und
  eine Tasche aus Messing schirmt genau das Funksignal ab, das das Gerät braucht. Technisch nicht
  sinnvoll lösbar.
- **Weitere Lederfarbe** — Prüffrage 2 und 7. Fünf Farben genügen. Eine sechste bindet Kapital im
  Lager, ohne einen neuen Kunden zu gewinnen. Die bessere Alternative ist NS-01.

---

## Was noch offen ist

1. Ob die Koppel gebaut wird, falls sich kein Messingwirbel finden lässt. Stahl ist ausgeschlossen.
2. Ob C (Werkstattdurchsicht) und E (Pflegeset) kommen.
3. Die Herkunftsfrage zum Kollektionsnamen, siehe `konzepte/kollektion-01-hamburg.md`.
