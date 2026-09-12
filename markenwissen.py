"""
markenwissen.py — Die Datei, die am ehesten geaendert wird.

Preise, Ausschluesse, Herkunftsregel, Wettbewerb.
Gilt fuer alle Abteilungen. Aenderungen hier wirken sofort ueberall.
Quelle: Blatt 3 (Wettbewerbsrecherche) und Blatt 5 (Kernserie Fettleder).
"""

MARKE = "Bellowerk Manufaktur"
MARKE_BISHER = "Herr Bello und Frau Wuff / Fraeulein Klaeff"
INSTAGRAM = "@herr.bello.und.frau.wuff"
STANDORT = "Harsefeld (Altes Land), Landkreis Stade"

POSITIONIERUNG = """
Premium-Lederzubehoer fuer Hunde aus eigener Werkstatt.
Der Unterschied zum Wettbewerb ist nicht das Material, sondern der Praxistest:
Björn führt Gassi-Service, Pension und Training. Jedes Modell haengt vor dem
Verkauf eine Saison lang an fremden Hunden, taeglich, bei jedem Wetter.
Kein Wettbewerber kann das nachmachen, ohne selbst einen Hundebetrieb zu fuehren.
Das ist ein echter Unterschied im Herstellungsprozess, kein Marketingdreh.
"""

PREISRAHMEN = {
    "halsband": {"min": 69, "max": 99, "waehrung": "EUR"},
    "leine": {"min": 89, "max": 139, "waehrung": "EUR"},
    "zubehoer": {"min": 25, "max": 59, "waehrung": "EUR"},
}

# Harte Ausschluesse — ein Konzept, das hiergegen verstoesst, wird abgelehnt.
AUSSCHLUESSE = [
    "keine Geschirre",
    "keine reine Handelsware ohne Markenbezug",
    "kein Verkaufsargument ueber den Preis",
    "kein Einstieg ueber Windhunde (Nische besetzt Bolleband vor Ort)",
]

WERKSTOFFE_ERLAUBT = [
    "Fettleder (pflanzlich gegerbt, feste Narbenseite)",
    "Messing massiv (Schnalle, Ringe, Karabiner)",
    "Buchschrauben Messing Durchmesser 5 mm",
]

WERKSTOFFE_AUSGESCHLOSSEN = [
    "Nieten", "Naehte und Garn", "Stahl",
    "Kunststoff", "Klickverschluesse", "Gurtband",
]

WETTBEWERB = {
    "CopcoPet": "16-46 EUR, Fettleder geflochten und glatt, preislich nahe Massenware",
    "MAUL Ledermanufaktur": "20-62 EUR, Vollrindleder, 40+ Jahre Fertigung, breites Sortiment",
    "roots Ledermanufaktur": "59 EUR einheitlich, vegetabil gegerbt, Laenge nach Mass 30-70 cm",
    "Bolleband Hamburg": "Preis unbekannt, Massanfertigung, Showroom, Fokus Windhunde/Jagdhunde, direkter Nachbar",
    "Das Lederband": "Fachhandel, etablierte Modellreihen, breite Haendlerdistribution",
}

MARKTLUECKE = """
Unter 60 EUR draengen sich alle Anbieter. Die Zone 69-99 EUR ist bei Anbietern
mit offenen Preisen kaum besetzt. 'Vegetabil gegerbt, Handarbeit, Messing' sagt
inzwischen jeder — das ist die Eintrittskarte ins Segment, kein Kaufargument.
"""

ZIELGRUPPE = """
Familien- und Gebrauchshunde mittlerer bis grosser Groesse aus der eigenen
Kundschaft (Gassi-Service, Pension, Training). Nicht Windhunde.
"""

BESTEHENDE_LEISTUNGEN = ["Gassi-Service", "Pension", "Hundetraining"]

KERNSERIE = {
    "HB-01": "Halsband Fettleder, einlagig, ohne Naht, Groessen S/M/L/XL, 20-40 mm",
    "LE-01": "Fuehrleine 3,00 m, dreifach verstellbar, sechs Fuehrlaengen, Ringe bei 45/140/245 cm",
    "HS-01": "Handschlaufe, Zubehoer, Umfang 50 cm",
    "HB-02": "Halsband geflochten: Halsteil im 3-straengigen Mystery Braid, O-Ring, flache Enden mit Schnalle und Patch",
    "PATCH-01": "Lederpatch cognac, lasergraviert 'BELLOWERK' / 'Manufaktur', 2 Buchschrauben; Karabiner und Ringe der Leine im Mystery Braid",
}

# Verkaufsnamen der Kollektion 01 "Hamburg" (Entscheidung Bjoern, 10.09.2026).
# Nach aussen der Name, intern und gegenueber Herstellern immer die Artikelnummer.
# Herkunftsregel: Der Kollektionsname bleibt 'Hamburg' — ein Produktname, der auf
# eine Region verweist, ist keine Herkunftsbehauptung. Der Betrieb sitzt aber in
# Harsefeld im Alten Land, nicht in Hamburg, deshalb nennt der HERKUNFTSSATZ seit
# dem 12.09.2026 das Alte Land. Siehe konzepte/kollektion-01-hamburg.md.
VERKAUFSNAMEN = {
    "HB-01": "Hamburg No. 1",
    "LE-01": "Hamburg No. 2",
    "HS-01": "Hamburg No. 3",
    "HB-02": "Hamburg No. 4",
    "LE-02": "Hamburg No. 5",
    "HB-03": "Hamburg No. 6",
    "KO-01": "Hamburg No. 7",
}

# Fertigungsort je Artikel. Steht bewusst hier und nicht als ein Satz fuer alles:
# sobald ein einziges Modell im Ausland gefertigt wird, aendert sich nur diese eine Zeile,
# und die Herkunftsangabe auf Website und Etikett bleibt fuer alle anderen wahr.
FERTIGUNGSORT = {
    "HB-01": "Harsefeld, Deutschland",
    "LE-01": "Harsefeld, Deutschland",
    "HS-01": "Harsefeld, Deutschland",
    "HB-02": "Harsefeld, Deutschland",
    "LE-02": "Harsefeld, Deutschland",
    "HB-03": "Harsefeld, Deutschland",
    "KO-01": "Harsefeld, Deutschland",
    "PATCH-01": "Harsefeld, Deutschland",
}

HERKUNFTSSATZ = "Entworfen, geprueft und gehandelt im Alten Land bei Hamburg. Gefertigt in Deutschland."

# Stand 11.09.2026: gilt fuer alle Artikel. Aendert sich, sobald der Einkauf China liefert.
HERKUNFT_REGEL = """
Die Angabe 'Gefertigt in Deutschland' gilt nur, solange der wesentliche Fertigungsschritt
(Zuschnitt, Lochung, Kantenbearbeitung, Montage der Beschlaege) in der eigenen Werkstatt stattfindet.
Wird ein Modell im Ausland gefertigt, wird FERTIGUNGSORT fuer dieses Modell geaendert und
die Angabe auf Website, Etikett und Beileger folgt automatisch. Fertige Ware einzukaufen und
nur den Patch anzuschrauben genuegt nicht fuer 'Made in Germany'.
"""

GESTALTUNG = {
    "farben": "Leder: Grau, Dunkelbraun, Oliv, Cognac, Schwarz; Logo: Oliv, Braun, Kupfer/Messing",
    "schrift": "Lora (Serife)",
    "bildsprache": "echte Fotos aus dem Betrieb, ehrliche Verschleissspuren, kein Studio-Look",
}


def als_kontext() -> str:
    """Gibt das Markenwissen als Textblock fuer die System-Prompts der Abteilungen."""
    zeilen = [
        f"MARKE: {MARKE} ({INSTAGRAM}), {STANDORT} — bisheriger Name: {MARKE_BISHER}",
        "",
        "POSITIONIERUNG:" + POSITIONIERUNG,
        "MARKTLAGE:" + MARKTLUECKE,
        "ZIELGRUPPE:" + ZIELGRUPPE,
        "",
        "PREISRAHMEN:",
    ]
    for artikel, p in PREISRAHMEN.items():
        zeilen.append(f"  - {artikel}: {p['min']}-{p['max']} {p['waehrung']}")

    zeilen += ["", "HARTE AUSSCHLUESSE (Verstoss = Ablehnung):"]
    zeilen += [f"  - {a}" for a in AUSSCHLUESSE]

    zeilen += ["", "WERKSTOFFE ERLAUBT:"]
    zeilen += [f"  - {w}" for w in WERKSTOFFE_ERLAUBT]
    zeilen += ["", "WERKSTOFFE AUSGESCHLOSSEN:"]
    zeilen += [f"  - {w}" for w in WERKSTOFFE_AUSGESCHLOSSEN]

    zeilen += ["", "WETTBEWERB:"]
    for name, beschreibung in WETTBEWERB.items():
        zeilen.append(f"  - {name}: {beschreibung}")

    zeilen += ["", "BESTEHENDE LEISTUNGEN: " + ", ".join(BESTEHENDE_LEISTUNGEN)]
    zeilen += ["", "KERNSERIE (Verkaufsname / Artikelnummer):"]
    for kuerzel, beschreibung in KERNSERIE.items():
        name = VERKAUFSNAMEN.get(kuerzel)
        vorn = f"{name} ({kuerzel})" if name else kuerzel
        zeilen.append(f"  - {vorn}: {beschreibung}")

    zeilen += ["", "HERKUNFT (bindend): " + HERKUNFTSSATZ]
    orte = sorted(set(FERTIGUNGSORT.values()))
    if len(orte) == 1:
        zeilen.append(f"  Fertigung aller Artikel: {orte[0]}")
    else:
        for kuerzel, ort in FERTIGUNGSORT.items():
            zeilen.append(f"  {kuerzel}: gefertigt in {ort}")
    zeilen += ["  " + z.strip() for z in HERKUNFT_REGEL.strip().splitlines()]

    zeilen += [
        "",
        "GESTALTUNG: Farben " + GESTALTUNG["farben"]
        + " | Schrift " + GESTALTUNG["schrift"]
        + " | " + GESTALTUNG["bildsprache"],
    ]
    return "\n".join(zeilen)
