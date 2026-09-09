"""
markenwissen.py — Die Datei, die am ehesten geaendert wird.

Preise, Ausschluesse, Herkunftsregel, Wettbewerb.
Gilt fuer alle Abteilungen. Aenderungen hier wirken sofort ueberall.
Quelle: Blatt 3 (Wettbewerbsrecherche) und Blatt 5 (Kernserie Fettleder).
"""

MARKE = "Bellowerk Manufaktur"
MARKE_BISHER = "Herr Bello und Frau Wuff / Fraeulein Klaeff"
INSTAGRAM = "@herr.bello.und.frau.wuff"
STANDORT = "Hamburg"

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
    zeilen += ["", "KERNSERIE:"]
    for kuerzel, beschreibung in KERNSERIE.items():
        zeilen.append(f"  - {kuerzel}: {beschreibung}")

    zeilen += [
        "",
        "GESTALTUNG: Farben " + GESTALTUNG["farben"]
        + " | Schrift " + GESTALTUNG["schrift"]
        + " | " + GESTALTUNG["bildsprache"],
    ]
    return "\n".join(zeilen)
