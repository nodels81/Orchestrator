"""abteilung_einkauf_china.py — 07 Auslandseinkauf China.

Liest Markenbrief, Tech Packs, Lieferanten-Shortlist und die Wissensdateien
(Plattformen, Verhandlung, Materialkunde) aus sourcing/ als bindenden Kontext.
Test: .venv/bin/python abteilung_einkauf_china.py "RFQ fuer HB-01 an Wenzhou Vigorous" --recherche
"""

import os
import re

from abteilung_basis import Abteilung, einzeltest, BASIS

SOURCING = os.path.join(BASIS, "sourcing")
SPECS = os.path.join(SOURCING, "bellowerk", "specs")

# Steht in jeder Anfrage und aendert sich nicht zwischen Auftraegen — gehoert in
# den System-Prompt, wo der Zwischenspeicher greift.
KONTEXT_DATEIEN = [
    "bellowerk/markenbrief.md",
    "lieferanten/shortlist.md",
    "wissen/plattformen.md",
    "wissen/verhandlung.md",
    "wissen/materialkunde.md",
]

# Tech Packs haengen am einzelnen Auftrag: eine Anfrage zu HB-01 braucht die
# Leinen-Spec nicht. Sie gehen darum auftragsbezogen in die Nutzernachricht.
# Ohne erkennbares Kuerzel bleibt es bei diesen dreien — dem bisherigen Umfang.
STANDARD_SPECS = ["HB-01", "LE-01", "PATCH-01"]
# Der Patch sitzt auf jedem Produkt; seine Spec gilt immer mit.
IMMER_SPEC = "PATCH-01"
KUERZEL = re.compile(r"\b((?:HB|LE|HS|PATCH|VERP)-\d{2})\b", re.IGNORECASE)

MAX_KONTEXT_ZEICHEN = 60_000


def _pfad(rel: str) -> str:
    """Frischer Markenbrief zuerst. markenwissen.py erzeugt ihn bei jedem Lauf nach
    daten/; die Fassung unter sourcing/ ist der aeltere, versionierte Stand und
    springt nur ein, wenn noch kein Lauf stattgefunden hat."""
    if rel == "bellowerk/markenbrief.md":
        frisch = os.path.join(BASIS, "daten", "markenbrief.md")
        if os.path.exists(frisch):
            return frisch
    return os.path.join(SOURCING, rel)


def sourcing_kontext() -> str:
    """Der feste Teil: Markenbrief, Shortlist, Wissensdateien."""
    teile = []
    for rel in KONTEXT_DATEIEN:
        pfad = _pfad(rel)
        if os.path.exists(pfad):
            with open(pfad, encoding="utf-8") as f:
                teile.append(f"### {rel}\n{f.read()}")
    text = "\n\n".join(teile)
    return text[:MAX_KONTEXT_ZEICHEN]


def spec_dateien() -> dict[str, str]:
    """Kuerzel -> Dateiname, aus dem Ordner gelesen statt fest verdrahtet.
    So steht jede vorhandene Spec zur Verfuegung, auch HB-02, HS-01 oder VERP-01."""
    gefunden = {}
    if os.path.isdir(SPECS):
        for name in sorted(os.listdir(SPECS)):
            treffer = KUERZEL.match(name)
            if name.endswith(".md") and treffer:
                gefunden[treffer.group(1).upper()] = name
    return gefunden


def specs_fuer(ziel: str) -> list[str]:
    """Welche Tech Packs braucht dieser Auftrag? Kuerzel aus dem Ziel lesen."""
    vorhanden = spec_dateien()
    genannt = [k.upper() for k in KUERZEL.findall(ziel or "")]
    gewaehlt = [k for k in genannt if k in vorhanden]
    if not gewaehlt:
        gewaehlt = [k for k in STANDARD_SPECS if k in vorhanden]
    elif IMMER_SPEC in vorhanden and IMMER_SPEC not in gewaehlt:
        gewaehlt.append(IMMER_SPEC)
    # Reihenfolge stabil halten, Doppelte raus.
    return list(dict.fromkeys(gewaehlt))


def spec_kontext(ziel: str) -> str:
    teile = []
    for kuerzel in specs_fuer(ziel):
        pfad = os.path.join(SPECS, spec_dateien()[kuerzel])
        with open(pfad, encoding="utf-8") as f:
            teile.append(f"### specs/{spec_dateien()[kuerzel]}\n{f.read()}")
    if not teile:
        return ""
    return ("TECH PACKS ZU DIESEM AUFTRAG (bindend):\n\n"
            + "\n\n".join(teile))[:MAX_KONTEXT_ZEICHEN]


class EinkaufChina(Abteilung):
    NUMMER = "07"
    NAME = "Einkauf China"
    MAX_TOKENS = 4000  # RFQ-Entwurf + Angebotsbewertung + Entscheidungsliste
    MAX_WOERTER = 300  # ein Brieftext plus Entscheidungen, mehr nicht
    DENKTIEFE = "medium"  # Angebote und Muster bewerten heisst abwaegen
    ROLLE = (
        "Du bist der Auslandseinkaeufer fuer chinesische Hersteller. Du schreibst sendefertige "
        "Nachrichten an Lieferanten (Englisch), bewertest Angebote und Muster, und bereitest "
        "Bestellungen vor. Bjoern entscheidet ueber jedes Geld: Muster, Anzahlung, Bestellung.\n\n"
        "KANAELE: Grosshandelsplattformen — Alibaba, Made-in-China, Global Sources, 1688.com "
        "(fuer Preisanker), Canton Fair. Nicht AliExpress (Endkunde/Dropshipping, kein Grosshandel). "
        "Zu jedem Lieferanten nennst du Plattform, Profil-Signale (Jahre, Gold/Assessed Supplier, "
        "Trade Assurance) und einen realistischen Zielpreis-Korridor mit Mengenstaffel.\n\n"
        "SCHREIBREGELN AN LIEFERANTEN:\n"
        " - Kurz, einfaches Englisch, nummerierte Fragen, Antwortfrist nennen, max. 150 Woerter beim Erstkontakt.\n"
        " - Jede Nachricht nennt 1-2 Anhaenge: bemasste Zeichnung + Foto (Dateinamen aus sourcing/bellowerk).\n"
        " - Nie 'cheapest price'. Wir kaufen Qualitaet in kleinen Mengen und sagen das offen.\n"
        " - Gesichtswahrend: Abweichung von der Zeichnung benennen, nie Schuld.\n"
        " - Chat-Absprachen werden per E-Mail zusammengefasst.\n"
        " - Verhandlung, Materialpruefung und Plattform-Details richten sich nach den "
        "Wissensdateien (wissen/verhandlung.md, wissen/materialkunde.md, wissen/plattformen.md).\n\n"
        "PFLICHT IN JEDER ANFRAGE UND BESTELLUNG:\n"
        " - Werkstoffe: Fettleder pflanzlich gegerbt 3,5-4,0 mm; Messing massiv (HPb59-1/CW617N), "
        "kein Zink, kein Stahl, kein Lack; Buchschrauben Messing 5 mm; keine Naht, keine Niete.\n"
        " - Patch: Lederpatch cognac, lasergraviert 'BELLOWERK' / darunter 'Manufaktur' in Schreibschrift, "
        "2 Buchschrauben. Karabiner und Ringe im 3-straengigen Mystery Braid plus 1 Buchschraube.\n"
        " - Schnittmuster PDF 1:1 + DXF mit Laenge, Breite, Lochabstand, Ringpositionen, Materialstaerke "
        "als Lieferumfang.\n"
        " - Zahlung 30 % nach Goldmuster, 70 % nach Endkontrolle vor Versand. AQL 2.5.\n\n"
        "DEINE AUSGABE im Feld 'ergebnis' hat genau drei Teile, ohne Vorrede und ohne "
        "Bericht darueber, was du getan hast:\n"
        " 1. Entwurf der Nachricht (Englisch, sendefertig, mit Anhangsliste). Eine Zeile "
        "davor nennt Plattform und Lieferanten, mehr Begruendung nicht.\n"
        " 2. Offene Entscheidungen fuer Bjoern — nummeriert, hoechstens fuenf, je eine "
        "Zeile, mit Zielpreis/Menge wo relevant und einer klaren Empfehlung\n"
        " 3. Naechster Schritt mit Datum — eine Zeile\n"
        "Teil 2 und 3 zusammen bleiben unter 120 Woertern. Was in der Nachricht steht, "
        "wiederholst du dort nicht.\n"
    )

    def system_prompt(self) -> str:
        """Ohne Tech Packs — die haengen am Auftrag und stehen in auftrag_kontext."""
        kontext = sourcing_kontext()
        if not kontext:
            return super().system_prompt()
        return super().system_prompt() + "\n\nEINKAUFSUNTERLAGEN (bindend):\n" + kontext

    def auftrag_kontext(self, auftrag: dict) -> str:
        """Nur die Tech Packs, die dieser Auftrag nennt. Ohne erkennbares Kuerzel
        die drei Standardspecs. Der Patch gilt immer mit, er sitzt auf jedem
        Produkt."""
        return spec_kontext(auftrag.get("ziel", ""))


if __name__ == "__main__":
    einzeltest(EinkaufChina)
