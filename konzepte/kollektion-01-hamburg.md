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

## Herkunft — entschieden am 10.09.2026

**Entscheidung Björn: ein Name für alles. Hamburg bleibt.** Begründung: Idee und Handel sitzen
in Hamburg.

Damit gilt Weg 2 aus der Vorlage. Der Name bezieht sich erkennbar auf Entwurf, Prüfung und
Handel, nicht auf die Fertigung. Das hält, aber nur unter einer Bedingung: **Die Herkunftsangabe
muss genauso sichtbar sein wie der Name.** Versteckt im Fußbereich reicht nicht, und genau daran
scheitern die meisten Abmahnfälle.

Verbindlich ab sofort:

1. **Auf jeder Produktseite**, im selben Block wie Preis und Größe, nicht darunter weggeklappt:
   `Entworfen, geprüft und gehandelt in Hamburg · Gefertigt in [Land]`
2. **In der Fußzeile jeder Seite**, einmal ausgeschrieben.
3. **Am Etikett und auf dem Beileger** derselbe Satz.
4. **Kein Satz behauptet Fertigung in Hamburg**, wenn das Stück nicht dort gefertigt wurde.
   Betroffen sind die Formulierungen "aus eigener Werkstatt" und "in unserer Werkstatt gefertigt".
   Erlaubt und wahr bleibt: "in Hamburg entworfen", "in Hamburg geprüft", "aus dem eigenen Betrieb
   geprüft", "eine Saison an fremden Hunden getragen".
5. **Der Praxistest bleibt der Beweis.** Er findet wirklich in Hamburg statt und ist damit die
   Herkunftsaussage, die trägt. Sie ersetzt die Fertigungsbehauptung vollständig und ist stärker,
   weil kein Wettbewerber sie kopieren kann.

Offen bleibt eine Formulierung: `markenwissen.py` sagt in POSITIONIERUNG
"Premium-Lederzubehoer fuer Hunde aus eigener Werkstatt". Sobald ein Modell aus China kommt, ist
der Satz für dieses Modell nicht mehr wahr. Vorschlag zur Ersetzung, wortgleich einsetzbar:

> Premium-Lederzubehör für Hunde, in Hamburg entworfen und im eigenen Betrieb geprüft.

Das Wort **Manufaktur** im Markennamen bleibt davon unberührt, solange die Werkstatt existiert
und dort gearbeitet wird.

## Was daraus folgt, wenn der Name kommt

1. `markenwissen.py`: Verkaufsnamen als `VERKAUFSNAMEN` neben `KERNSERIE` aufgenommen. Erledigt.
2. Website: Produktkarten und Produktseiten zeigen Name groß, Nummer klein.
   Betrifft `web/startseite-nachtwerkstatt.html`.
3. Patch: Der Markenpatch bleibt "BELLOWERK / Manufaktur". Die Kollektionsnummer kommt nicht auf
   das Produkt, sonst wird aus einem Gebrauchsgegenstand ein Sammlerstück, das niemand benutzt.
4. Einkauf: Die Hersteller arbeiten weiter ausschließlich mit HB-01, LE-01 und so weiter.
   Verkaufsnamen tauchen in keiner RFQ und in keinem Tech Pack auf.
