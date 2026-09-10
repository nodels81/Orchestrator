# Kollektion 01 "Hamburg" — Namensschema

Stand 10.09.2026 · Abteilung 01 Innovation, Vorlage an Marketing
Vorgabe Björn: Das Grundmodell heißt **Hamburg No. 1**.

## Der Gedanke

Artikelnummern wie HB-01 sind Werkstattsprache. Sie bleiben in Spezifikation, Einkauf und Lager
stehen, weil der Hersteller sie braucht. Nach außen bekommt jedes Stück einen Namen, und die
Nummer läuft durch die ganze Kollektion, nicht je Warengruppe. Das ist die Logik eines
Werkverzeichnisses: No. 1 ist das zuerst gebaute Stück, nicht das erste Halsband.

Das hat drei Vorteile. Der Kunde merkt sich "Hamburg No. 1" und nicht "HB-01". Neue Stücke hängen
sich hinten an, ohne dass ein Schema bricht. Und die Nummer erzählt die Reihenfolge, in der die
Werkstatt gewachsen ist, was zur Marke passt.

## Das Register

| Name | Artikel | Was es ist | Preis |
|---|---|---|---|
| **Hamburg No. 1** | HB-01 | Halsband Fettleder, einlagig, ohne Naht | 89 EUR |
| **Hamburg No. 2** | LE-01 | Führleine 3,00 m, sechs Führlängen | 129 EUR |
| **Hamburg No. 3** | HS-01 | Handschlaufe, Umfang 50 cm | 39 EUR |
| **Hamburg No. 4** | HB-02 | Halsband geflochten, Mystery Braid | 99 EUR |
| **Hamburg No. 5** | LE-02 | Führleine geflochten | 139 EUR |
| **Hamburg No. 6** | HB-03 | Zugstopp-Halsband | 99 EUR |
| **Hamburg No. 7** | KO-01 | Koppel für zwei Hunde | 79 EUR |

Zubehör bekommt keine Nummer, sondern einen sachlichen Namen: **Namensschild Messing** (NS-01)
und **Namenspatch Leder** (NS-02). Ein Schild ist kein Werkstück der Kollektion, sondern eine
Zutat. Alles zu nummerieren würde die Nummer entwerten.

## Schreibweise

- **Hamburg No. 1**, mit Leerzeichen und Punkt, No. abgekürzt und groß.
- Nicht "Hamburg Nr. 1", nicht "Hamburg #1", nicht "HAMBURG NO.1".
- Im Fließtext beim ersten Mal voll ausschreiben, danach "No. 1" allein.
- Auf der Produktseite steht der Name groß, die Artikelnummer klein darunter in Mono.
  Beide müssen auffindbar sein, weil Bestandskunden nach HB-01 suchen werden.

## Die eine Frage, die vorher geklärt sein muss

Ein Kollektionsname mit einem Ortsnamen ist eine Herkunftsaussage, sobald das Publikum ihn so
versteht. Zusammen mit dem Wort "Manufaktur" im Markennamen und dem Satz "aus eigener Werkstatt"
entsteht der Eindruck: hier in Hamburg gefertigt.

Parallel läuft Abteilung 05 Einkauf China und bereitet an, dass HB-01, HB-02, LE-01 und die
Patches bei chinesischen Herstellern produziert werden. Beides zusammen ist angreifbar. Eine
irreführende Herkunftsangabe ist ein Fall für eine Abmahnung durch Wettbewerber, und die Nachbarn
in Hamburg sind Wettbewerber.

**Drei Wege, einer muss gewählt werden:**

1. **Hamburg bleibt der Werkstattlinie vorbehalten.** Nur Stücke, die Björn selbst fertigt,
   heißen Hamburg No. X. Die zugekaufte Serie bekommt einen eigenen Namen ohne Ortsbezug.
   Sauberste Lösung, kostet aber die schöne Nummer für die Massenartikel.
2. **Hamburg für alles, mit offener Herkunftsangabe.** Auf jeder Produktseite und am Etikett steht,
   wo gefertigt wurde: "Entworfen und geprüft in Hamburg, gefertigt in ...". Der Name bezieht sich
   dann erkennbar auf Entwurf und Prüfung, nicht auf die Fertigung. Funktioniert nur, wenn die
   Angabe genauso sichtbar ist wie der Name, nicht im Fußbereich versteckt.
3. **Kein Ortsname.** Die Kollektion heißt anders, etwa nach der Straße der Werkstatt oder nach der
   Serie selbst. Verschenkt Substanz, hat aber kein Risiko.

**Empfehlung: Weg 1.** Er passt zum Verkaufsargument. Der Praxistest findet in Hamburg statt, die
Fertigung nicht überall. Wenn Hamburg No. 1 heißt "aus dieser Werkstatt", dann trägt der Name
etwas. Wenn er auf allem klebt, trägt er nichts, und angreifbar ist er obendrein.

Das Wort **Manufaktur** im Markennamen steht unter derselben Frage und sollte mitentschieden
werden.

## Was daraus folgt, wenn der Name kommt

1. `markenwissen.py`: Verkaufsnamen neben die Artikelnummern in `KERNSERIE` aufnehmen.
2. Website: Produktkarten und Produktseiten zeigen Name groß, Nummer klein.
   Betrifft `web/startseite-nachtwerkstatt.html`.
3. Patch: Der Markenpatch bleibt "BELLOWERK / Manufaktur". Die Kollektionsnummer kommt nicht auf
   das Produkt, sonst wird aus einem Gebrauchsgegenstand ein Sammlerstück, das niemand benutzt.
4. Einkauf: Die Hersteller arbeiten weiter ausschließlich mit HB-01, LE-01 und so weiter.
   Verkaufsnamen tauchen in keiner RFQ und in keinem Tech Pack auf.
