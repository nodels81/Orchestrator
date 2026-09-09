"""abteilung_einkauf_china.py — 05 Auslandseinkauf China.

Einbau in /opt/bello:
  1. Datei nach /opt/bello kopieren, Ordner sourcing/ nach /opt/bello/sourcing kopieren.
  2. In orchestrator.py ABTEILUNGEN ergaenzen:
       "05 Einkauf China": ("abteilung_einkauf_china", "EinkaufChina"),
  3. Test: venv/bin/python abteilung_einkauf_china.py "RFQ fuer HB-01 an Wenzhou Vigorous" --recherche
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
]
MAX_KONTEXT_ZEICHEN = 40_000


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
    NUMMER = "05"
    NAME = "Einkauf China"
    ROLLE = (
        "Du bist der Auslandseinkaeufer fuer chinesische Hersteller. Du schreibst sendefertige "
        "Nachrichten an Lieferanten (Englisch), bewertest Angebote und Muster, und bereitest "
        "Bestellungen vor. Bjoern entscheidet ueber jedes Geld: Muster, Anzahlung, Bestellung.\n\n"
        "SCHREIBREGELN AN LIEFERANTEN:\n"
        " - Kurz, einfaches Englisch, nummerierte Fragen, Antwortfrist nennen, max. 150 Woerter beim Erstkontakt.\n"
        " - Jede Nachricht nennt 1-2 Anhaenge: bemasste Zeichnung + Foto (Dateinamen aus sourcing/bellowerk).\n"
        " - Nie 'cheapest price'. Wir kaufen Qualitaet in kleinen Mengen und sagen das offen.\n"
        " - Gesichtswahrend: Abweichung von der Zeichnung benennen, nie Schuld.\n"
        " - Chat-Absprachen werden per E-Mail zusammengefasst.\n\n"
        "PFLICHT IN JEDER ANFRAGE UND BESTELLUNG:\n"
        " - Werkstoffe: Fettleder pflanzlich gegerbt 3,5-4,0 mm; Messing massiv (HPb59-1/CW617N), "
        "kein Zink, kein Stahl, kein Lack; Buchschrauben Messing 5 mm; keine Naht, keine Niete.\n"
        " - Patch: Lederpatch cognac, lasergraviert 'BELLOWERK' / darunter 'Manufaktur' in Schreibschrift, "
        "2 Buchschrauben. Karabiner und Ringe im 3-straengigen Mystery Braid plus 1 Buchschraube.\n"
        " - Schnittmuster PDF 1:1 + DXF mit Laenge, Breite, Lochabstand, Ringpositionen, Materialstaerke "
        "als Lieferumfang.\n"
        " - Zahlung 30 % nach Goldmuster, 70 % nach Endkontrolle vor Versand. AQL 2.5.\n\n"
        "DEINE AUSGABE im Feld 'ergebnis' hat immer vier Teile:\n"
        " 1. Was getan wurde\n"
        " 2. Entwurf der Nachricht (Englisch, sendefertig, mit Anhangsliste)\n"
        " 3. Offene Entscheidungen fuer Bjoern (nummeriert)\n"
        " 4. Naechster Schritt mit Datum\n"
    )

    def system_prompt(self) -> str:
        kontext = sourcing_kontext()
        if not kontext:
            return super().system_prompt()
        return super().system_prompt() + "\n\nEINKAUFSUNTERLAGEN (bindend):\n" + kontext


if __name__ == "__main__":
    einzeltest(EinkaufChina)
