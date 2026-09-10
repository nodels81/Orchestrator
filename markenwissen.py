"""
markenwissen.py — die eine Markenwahrheit fuer Bellowerk.

Alle Abteilungen lesen von hier (ueber als_kontext()). Der Markenbrief fuer den
Einkauf (sourcing/bellowerk/markenbrief.md) wird aus dieser Datei ERZEUGT:
    .venv/bin/python markenwissen.py --schreibe-markenbrief
Der Tageslauf-Wrapper macht das automatisch. Aendere die Marke also hier, nicht dort.
"""

import os
import sys

# ---------- Marke ----------
MARKE = "Bellowerk"                    # Name auf dem Produkt, darunter klein "Manufaktur"
MARKE_SOCIAL = "Herr Bello und Frau Wuff"   # kundennaher Name / Social-Auftritt
INSTAGRAM = "@herr.bello.und.frau.wuff"
INSTAGRAM_ALT = "@herr_bello_und_fraeulein_klaef"
STANDORT = "Hamburg / Altes Land"
INHABER = "Björn — einziger Entscheider"

POSITIONIERUNG = """
Premium-Lederzubehoer fuer Hunde aus eigener Werkstatt.
Der Unterschied zum Wettbewerb ist nicht das Material, sondern der Praxistest:
Björn führt Gassi-Service, Pension und Training. Jedes Modell haengt vor dem
Verkauf eine Saison lang an fremden Hunden, taeglich, bei jedem Wetter.
Kein Wettbewerber kann das nachmachen, ohne selbst einen Hundebetrieb zu fuehren.
Das ist ein echter Unterschied im Herstellungsprozess, kein Marketingdreh.
"""

ZIELGRUPPE = """
Familien- und Gebrauchshunde mittlerer bis grosser Groesse aus der eigenen
Kundschaft (Gassi-Service, Pension, Training). Nicht Windhunde.
"""

GRUNDSATZ = (
    "Schlichte Produkte, bei denen die Messingringe und -schnallen zur Geltung kommen. "
    "Jedes Produkt wird komplett geliefert: fertig montiert, mit Patch, mit Pflegehinweis, verpackt."
)

BESTEHENDE_LEISTUNGEN = ["Gassi-Service", "Pension", "Hundetraining"]

# ---------- Preise ----------
PREISRAHMEN = {
    "halsband": {"min": 69, "max": 99, "waehrung": "EUR"},
    "leine": {"min": 89, "max": 139, "waehrung": "EUR"},
    "zubehoer": {"min": 25, "max": 59, "waehrung": "EUR"},
}
# Ziel-Einkaufspreis ab Werk, Orientierung bei 100 Stueck (EUR)
ZIEL_EK = {"halsband": 20, "leine": 30, "handschlaufe": 8, "namensschild": 1.5}

# ---------- Gestaltung ----------
GESTALTUNG = {
    "farben": "Oliv, Braun, Kupfer",
    "schrift": "Lora (Serife)",
    "bildsprache": "echte Fotos aus dem Betrieb, ehrliche Verschleissspuren, kein Studio-Look",
}
LOGO_FARBEN = {
    "Waldgruen": "#23352A", "Olivgruen": "#566347",
    "Cognac": "#9A6238", "Messing": "#B08D57",
}
LEDERFARBEN = ["Grau", "Dunkelbraun", "Oliv", "Cognac", "Schwarz"]

# ---------- Werkstoffe ----------
WERKSTOFFE_ERLAUBT = [
    "Fettleder: Rindleder, pflanzlich gegerbt (vegetable-tanned), gefettet/gewachst "
    "(oiled / pull-up), Vollnarbe (full grain), feste Narbenseite, durchgefaerbt. "
    "Staerke 3,5-4,0 mm fuer Halsband und Leine, 2,0-2,5 mm fuer den Patch. Leinenbreite 20 mm.",
    "Messing massiv (solid brass, gegossen HPb59-1 / CW617N oder geschmiedet): Rollschnalle, "
    "D-Ring geschweisst, O-Ring geschweisst, Wirbel-Bolzenkarabiner (swivel eye bolt snap), "
    "Riemenschlaufe. Unlackiert, Patina erwuenscht.",
    "Buchschrauben Messing (Chicago screws), gewoelbter Kopf Durchmesser 8-9 mm, Schaft 8 mm, "
    "mit Schraubensicherung.",
    "Flechtung: 3-straengiger Mystery Braid (Trick Braid) aus einem Stueck, V-Muster — so werden "
    "Karabiner und Ringe ohne Naht befestigt. Keine anderen Flechtarten.",
    "Patch: Lederpatch in Cognac/Mittelbraun, lasergraviert 'BELLOWERK' (Versalien, gesperrt) und "
    "darunter 'Manufaktur' in Schreibschrift, 2 Buchschrauben.",
]
WERKSTOFFE_AUSGESCHLOSSEN = [
    "Naehte und Garn", "Nieten", "Stahl (auch vermessingt)", "Zinkdruckguss (zinc alloy / Zamak)",
    "Kunststoff", "Klickverschluesse", "Gurtband / Nylon", "PU-, Spalt- oder Bonded-Leder",
    "Lack auf Messing",
]
AUSNAHME_WERKSTOFF = (
    "Nur mit Björns Freigabe: Paracord oder rundgeflochtenes Leder als eigene Linie."
)

# Harte Ausschluesse auf Konzeptebene — Verstoss = Ablehnung
AUSSCHLUESSE = [
    "keine Geschirre",
    "keine reine Handelsware ohne Markenbezug",
    "kein Verkaufsargument ueber den Preis",
    "kein Einstieg ueber Windhunde",
]

# ---------- Produktprogramm (eine Quelle fuer Modellnummern) ----------
# status: "Serie" | "in Entwicklung" | "zurueckgestellt" | "Entwurf"
PRODUKTE = {
    "HB-01": {"name": "Halsband Fettleder", "status": "Serie",
              "kurz": "einlagig, ohne Naht, S/M/L/XL, 20-40 mm, mit Lederpatch"},
    "LE-01": {"name": "Fuehrleine 3,00 m", "status": "Serie",
              "kurz": "dreifach verstellbar, sechs Fuehrlaengen, Ringe bei 45/140/245 cm, "
                      "Karabiner und Ringe im Mystery Braid"},
    "HB-02": {"name": "Halsband geflochten", "status": "in Entwicklung",
              "kurz": "Halsteil im Mystery Braid (ein- oder zweifarbig), O-Ring, flache Enden "
                      "mit Schnalle und Patch"},
    "HB-03": {"name": "Hamburg No.1", "status": "in Entwicklung", "kollektion": "Kollektion 1",
              "kurz": "Halsband 'Steg': kurze schmale Enden 25 mm, schneller Uebergang auf den "
                      "breiten Steg ca. 40 mm ueber den groessten Teil der Laenge, Steg oben/unten "
                      "leicht gerundet, ein Stueck Fettleder 3,8 mm, 5 Loecher Abstand 25 mm, "
                      "Rollschnalle + D-Ring + 3 Buchschrauben, keine Halteschlaufe. "
                      "Form von Bjoern freigegeben 2026-09-10 (A-2026-006)."},
    "LE-02": {"name": "Fuehrleine rundgeflochten", "status": "zurueckgestellt",
              "kurz": "rundgeflochtene Leine — vorerst nicht anfragen"},
    "HS-01": {"name": "Handschlaufe", "status": "Serie", "kurz": "Zubehoer, Umfang 50 cm"},
    "PATCH-01": {"name": "Lederpatch", "status": "Serie",
                 "kurz": "lasergraviert 'BELLOWERK / Manufaktur', 2 Buchschrauben; "
                         "spaeter Variante mit Hundenamen"},
    "VERP-01": {"name": "Verpackung + Kennzeichnung", "status": "Entwurf",
                "kurz": "Björn entscheidet"},
}
SPAETERE_KANDIDATEN = [
    "Fuehrleine mit fester Handschlaufe",
    "Schluesselanhaenger mit Patch",
    "Messing-Muenzanhaenger am D-Ring",
    "Sonderfarben Pink / Tuerkis / Mint / Gelb / Bordeaux",
]

LIEFERUMFANG_PFLICHT = [
    "Fertige Ware nach Goldmuster",
    "Schnittmuster je Modell und Groesse: PDF 1:1 und DXF, mit Laenge, Breite, Lochabstand, "
    "Lochdurchmesser, Ringpositionen, Materialstaerke, Schrauben-Positionen",
    "Materialdatenblatt Leder (Gerbung, Staerke, Herkunft) und Messing (Legierung, Bruchlast)",
    "Testbericht REACH Chrom VI (Leder) und Blei (Messing) — oder Erlaubnis zum Selbsttest",
    "Fotos jedes Modells vor Versand",
]

# ---------- Wettbewerb ----------
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


# ---------- Helfer ----------
def naechste_modellnummer(praefix: str) -> str:
    """z. B. naechste_modellnummer('HB') -> 'HB-03', wenn HB-01 und HB-02 vergeben sind."""
    praefix = praefix.upper().rstrip("-")
    nummern = [
        int(code.split("-")[1])
        for code in PRODUKTE
        if code.upper().startswith(praefix + "-") and code.split("-")[1].isdigit()
    ]
    return f"{praefix}-{max(nummern, default=0) + 1:02d}"


def als_kontext() -> str:
    """Markenwissen als Textblock fuer die System-Prompts aller Abteilungen."""
    z = [
        f"MARKE (Produkt/Manufaktur): {MARKE}  —  darunter klein: Manufaktur",
        f"KUNDENNAHER NAME / SOCIAL: {MARKE_SOCIAL}  ({INSTAGRAM})",
        f"STANDORT: {STANDORT}   INHABER: {INHABER}",
        "",
        "POSITIONIERUNG:" + POSITIONIERUNG,
        "MARKTLAGE:" + MARKTLUECKE,
        "ZIELGRUPPE:" + ZIELGRUPPE,
        f"GRUNDSATZ: {GRUNDSATZ}",
        "",
        "PREISRAHMEN (VK):",
    ]
    for artikel, p in PREISRAHMEN.items():
        z.append(f"  - {artikel}: {p['min']}-{p['max']} {p['waehrung']}")
    z += ["  Ziel-EK ab Werk (100 Stk): "
          + ", ".join(f"{k} <= {v} EUR" for k, v in ZIEL_EK.items())]

    z += ["", "PRODUKTPROGRAMM (Modellnummern sind vergeben — keine doppelt verwenden):"]
    for code, d in PRODUKTE.items():
        koll = f", {d['kollektion']}" if d.get("kollektion") else ""
        z.append(f"  - {code} {d['name']} [{d['status']}{koll}]: {d['kurz']}")
    z += ["  Spaetere Kandidaten (nicht jetzt): " + "; ".join(SPAETERE_KANDIDATEN)]

    z += ["", "HARTE AUSSCHLUESSE (Konzept, Verstoss = Ablehnung):"]
    z += [f"  - {a}" for a in AUSSCHLUESSE]

    z += ["", "WERKSTOFFE ERLAUBT:"]
    z += [f"  - {w}" for w in WERKSTOFFE_ERLAUBT]
    z += ["", "WERKSTOFFE AUSGESCHLOSSEN (Verstoss = Ablehnung):"]
    z += ["  - " + ", ".join(WERKSTOFFE_AUSGESCHLOSSEN), f"  - {AUSNAHME_WERKSTOFF}"]
    z += ["", f"LEDERFARBEN: {', '.join(LEDERFARBEN)}"]

    z += ["", "GESTALTUNG: Farben " + GESTALTUNG["farben"]
          + " | Schrift " + GESTALTUNG["schrift"]
          + " | Logo-Farben " + ", ".join(f"{k} {v}" for k, v in LOGO_FARBEN.items())
          + " | " + GESTALTUNG["bildsprache"]]

    z += ["", "LIEFERUMFANG JE BESTELLUNG (Pflicht):"]
    z += [f"  {i+1}. {p}" for i, p in enumerate(LIEFERUMFANG_PFLICHT)]

    z += ["", "WETTBEWERB:"]
    for name, beschreibung in WETTBEWERB.items():
        z.append(f"  - {name}: {beschreibung}")
    z += ["", "BESTEHENDE LEISTUNGEN: " + ", ".join(BESTEHENDE_LEISTUNGEN)]
    return "\n".join(z)


def markenbrief_md() -> str:
    """Erzeugt den Markenbrief fuer den Einkauf aus den Konstanten oben."""
    L = ["# Bellowerk — Markenbrief für den Einkauf", "",
         "**AUTOMATISCH ERZEUGT aus `markenwissen.py` — nicht von Hand ändern.**",
         "Änderungen an der Marke gehören in `markenwissen.py`.", "",
         "## Marke", "", "| | |", "|---|---|",
         f"| Markenname auf dem Produkt | **{MARKE}** — darunter klein: **Manufaktur** |",
         f"| Kundennaher Name / Social | {MARKE_SOCIAL} ({INSTAGRAM}, {INSTAGRAM_ALT}) |",
         f"| Standort | {STANDORT} |",
         f"| Inhaber, einziger Entscheider | {INHABER} |",
         f"| Positionierung | {' '.join(POSITIONIERUNG.split())} |",
         f"| Zielgruppe | {' '.join(ZIELGRUPPE.split())} |",
         "| Preisrahmen VK | "
         + ", ".join(f"{k.capitalize()} {p['min']}–{p['max']} EUR" for k, p in PREISRAHMEN.items())
         + " |",
         "| Ziel-EK ab Werk (100 Stück) | "
         + ", ".join(f"{k} ≤ {v} EUR" for k, v in ZIEL_EK.items()) + " |",
         f"| Gestaltung | Farben {GESTALTUNG['farben']}; Schrift {GESTALTUNG['schrift']}; "
         "Logo-Farben " + ", ".join(f"{k} {v}" for k, v in LOGO_FARBEN.items()) + " |",
         f"| Lederfarben | {', '.join(LEDERFARBEN)} |",
         f"| Bildsprache | {GESTALTUNG['bildsprache']} |", "",
         "## Werkstoffe — erlaubt", ""]
    L += [f"- {w}" for w in WERKSTOFFE_ERLAUBT]
    L += ["", "## Werkstoffe — ausgeschlossen (Verstoß = Ablehnung)", "",
          " · ".join(WERKSTOFFE_AUSGESCHLOSSEN), "", AUSNAHME_WERKSTOFF, "",
          "## Harte Ausschlüsse (Konzept)", "", " · ".join(AUSSCHLUESSE), "",
          "## Produktprogramm", "", "| Modell | Beschreibung | Status |", "|---|---|---|"]
    L += [f"| {c} | {d['name']} — {d['kurz']} | {d['status']} |" for c, d in PRODUKTE.items()]
    L += ["", f"Grundsatz: {GRUNDSATZ}", "",
          "Spätere Kandidaten (nicht jetzt anfragen): " + "; ".join(SPAETERE_KANDIDATEN), "",
          "## Lieferumfang je Bestellung (Pflicht)", ""]
    L += [f"{i+1}. {p}" for i, p in enumerate(LIEFERUMFANG_PFLICHT)]
    L += ["", "## Was der Einkäufer darf und nicht darf", "",
          "- Darf: anfragen, verhandeln, Muster vorschlagen, Entwürfe schreiben, Lieferanten bewerten.",
          "- Darf nicht: Geld ausgeben, Preise zusagen, Muster ohne Freigabe bestellen, Materialliste aufweichen.",
          "- Jede Entscheidung mit Geld oder Freigabe geht nummeriert an Björn.", ""]
    return "\n".join(L)


if __name__ == "__main__":
    if "--schreibe-markenbrief" in sys.argv:
        ziel = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "sourcing", "bellowerk", "markenbrief.md")
        if os.path.isdir(os.path.dirname(ziel)):
            with open(ziel, "w", encoding="utf-8") as f:
                f.write(markenbrief_md())
            print(f"geschrieben: {ziel}")
        else:
            print("sourcing/bellowerk/ fehlt — nichts geschrieben")
    else:
        print(als_kontext())
