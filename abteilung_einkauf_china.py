"""abteilung_einkauf_china.py — 07 Auslandseinkauf China.

Liest Markenbrief, Tech Packs, Lieferanten-Shortlist und die Wissensdateien
(Plattformen, Verhandlung, Materialkunde) aus sourcing/ als bindenden Kontext.
Test: .venv/bin/python abteilung_einkauf_china.py "RFQ fuer HB-01 an Wenzhou Vigorous" --recherche
"""

import os

from abteilung_basis import Abteilung, einzeltest, BASIS

SOURCING = os.path.join(BASIS, "sourcing")
KONTEXT_DATEIEN = [
    "bellowerk/markenbrief.md",
    "bellowerk/specs/HB-01-halsband.md",
    "bellowerk/specs/LE-01-fuehrleine.md",
    "bellowerk/specs/PATCH-01-markenpatch.md",
    "lieferanten/shortlist.md",
    "wissen/plattformen.md",
    "wissen/verhandlung.md",
    "wissen/materialkunde.md",
]
MAX_KONTEXT_ZEICHEN = 60_000


def sourcing_kontext() -> str:
    teile = []
    for rel in KONTEXT_DATEIEN:
        pfad = os.path.join(SOURCING, rel)
        if os.path.exists(pfad):
            with open(pfad, encoding="utf-8") as f:
                teile.append(f"### {rel}\n{f.read()}")
    text = "\n\n".join(teile)
    return text[:MAX_KONTEXT_ZEICHEN]


class EinkaufChina(Abteilung):
    NUMMER = "07"
    NAME = "Einkauf China"
    MAX_TOKENS = 8000  # RFQ-Entwurf + Angebotsbewertung + Entscheidungsliste laufen lang
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
        "DEINE AUSGABE im Feld 'ergebnis' hat immer vier Teile:\n"
        " 1. Was getan wurde (inkl. Plattform + warum dieser Lieferant)\n"
        " 2. Entwurf der Nachricht (Englisch, sendefertig, mit Anhangsliste)\n"
        " 3. Offene Entscheidungen fuer Bjoern (nummeriert, mit Zielpreis/Menge wo relevant)\n"
        " 4. Naechster Schritt mit Datum\n"
    )

    def system_prompt(self) -> str:
        kontext = sourcing_kontext()
        if not kontext:
            return super().system_prompt()
        return super().system_prompt() + "\n\nEINKAUFSUNTERLAGEN (bindend):\n" + kontext


if __name__ == "__main__":
    einzeltest(EinkaufChina)
