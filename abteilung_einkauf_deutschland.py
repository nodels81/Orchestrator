"""abteilung_einkauf_deutschland.py — 06 Einkauf Deutschland (Auftragsarbeit).

Liest Markenbrief, Tech Packs und die deutschen Lieferantenprofile aus
sourcing/lieferanten-deutschland/ als bindenden Kontext.
Test: venv/bin/python abteilung_einkauf_deutschland.py "Anfrage Auftragsarbeit an Mali-Leder"
"""

import glob
import os

from abteilung_basis import Abteilung, einzeltest, BASIS

SOURCING = os.path.join(BASIS, "sourcing")
KONTEXT_DATEIEN = [
    "bellowerk/markenbrief.md",
    "bellowerk/specs/HB-01-halsband.md",
    "bellowerk/specs/LE-01-fuehrleine.md",
]
LIEFERANTEN_ORDNER = os.path.join(SOURCING, "lieferanten-deutschland")
MAX_KONTEXT_ZEICHEN = 40_000


def sourcing_kontext() -> str:
    teile = []
    for rel in KONTEXT_DATEIEN:
        pfad = os.path.join(SOURCING, rel)
        if os.path.exists(pfad):
            with open(pfad, encoding="utf-8") as f:
                teile.append(f"### {rel}\n{f.read()}")
    for pfad in sorted(glob.glob(os.path.join(LIEFERANTEN_ORDNER, "*.md"))):
        rel = os.path.relpath(pfad, SOURCING)
        with open(pfad, encoding="utf-8") as f:
            teile.append(f"### {rel}\n{f.read()}")
    text = "\n\n".join(teile)
    return text[:MAX_KONTEXT_ZEICHEN]


class EinkaufDeutschland(Abteilung):
    NUMMER = "06"
    NAME = "Einkauf Deutschland"
    ROLLE = (
        "Du bist der Einkaeufer fuer deutsche und europaeische Werkstaetten/Manufakturen "
        "(Auftragsarbeit, Lohnfertigung, Bestandslieferanten). Du schreibst sendefertige "
        "Nachrichten auf Deutsch, foermlich (Sie), und bewertest Antworten. Bjoern entscheidet "
        "ueber jedes Geld: Muster, Anzahlung, Bestellung.\n\n"
        "SCHREIBREGELN AN LIEFERANTEN:\n"
        " - Kurz, foermliches Deutsch (Sie), nummerierte Fragen, max. 150 Woerter beim Erstkontakt.\n"
        " - Bestehende Geschaeftsbeziehungen (z. B. fruehere Bestellungen unter dem alten Namen "
        "'Herr Bello und Frau Wuff Manufaktur') immer erwaehnen, wenn im Gedaechtnis oder "
        "Lieferantenprofil vermerkt.\n"
        " - Nie 'billigster Preis'. Wir kaufen Qualitaet, auch in kleinen Mengen, und sagen "
        "das offen.\n"
        " - Telefon- oder Chat-Absprachen werden per E-Mail zusammengefasst.\n\n"
        "PFLICHT IN JEDER ANFRAGE:\n"
        " - Werkstoffe: Fettleder pflanzlich gegerbt 3,5-4,0 mm; Messing massiv, kein Zink, "
        "kein Stahl, kein Lack; keine Naht, keine Niete.\n"
        " - Kernfragen: Nimmt der Lieferant Auftragsarbeit an (auch kleine Stueckzahlen)? "
        "Mindestbestellmengen? Lederarten/-staerken im Sortiment? Aktuelle Lieferzeiten?\n\n"
        "DEINE AUSGABE im Feld 'ergebnis' hat immer vier Teile:\n"
        " 1. Was getan wurde\n"
        " 2. Entwurf der Nachricht (Deutsch, sendefertig)\n"
        " 3. Offene Entscheidungen fuer Bjoern (nummeriert)\n"
        " 4. Naechster Schritt mit Datum\n\n"
        "Markierst du eine Nachricht im Feld 'lieferant' als versandbereit, verschickt der "
        "Betrieb sie automatisch per E-Mail an den Lieferanten — Bjoern bekommt nur noch eine "
        "Kopie zur Kenntnis, muss aber nichts mehr selbst abschicken. Deshalb: versandbereit "
        "ausschliesslich bei Erstkontakt, Nachfassen, Musteranfrage oder Musterfeedback. Nie "
        "bei Bestellung, Anzahlung oder jeder Form von Zahlungszusage.\n"
    )

    def system_prompt(self) -> str:
        kontext = sourcing_kontext()
        if not kontext:
            return super().system_prompt()
        return super().system_prompt() + "\n\nEINKAUFSUNTERLAGEN (bindend):\n" + kontext

    # Ueberschreibt (statt erweitert) den Basis-Antwortformat-Text, weil
    # abteilung_basis.py laut eigener Doku nie angefasst werden soll: das
    # zusaetzliche Feld 'lieferant' muss also hier definiert werden.
    def antwortformat(self) -> str:
        return (
            "Antworte ausschliesslich mit diesem JSON-Objekt:\n"
            "{\n"
            '  "ergebnis": "<deine Arbeit, ausformuliert>",\n'
            '  "kriterien_erfuellt": [true, false, ...],\n'
            '  "blocker": null,\n'
            '  "anmerkung": "<Einschraenkungen oder Hinweise, sonst null>",\n'
            '  "zusammenfassung": "<dein Ergebnis in hoechstens zwei Saetzen>",\n'
            '  "fakten": [\n'
            '    {"subjekt": "<worueber>", "praedikat": "<was>", "objekt": "<Wert>"}\n'
            "  ],\n"
            '  "lieferant": {\n'
            '    "email": "<bekannte Empfaenger-Adresse oder null, wenn unbekannt>",\n'
            '    "betreff": "<E-Mail-Betreff>",\n'
            '    "nachricht": "<reiner Nachrichtentext, identisch mit dem Entwurf aus ergebnis Punkt 2>",\n'
            '    "versandbereit": false\n'
            "  }\n"
            "}\n"
            "Die Liste kriterien_erfuellt hat genau so viele Eintraege wie Kriterien "
            "im Auftrag, in derselben Reihenfolge.\n\n"
            "Zu 'fakten': hoechstens fuenf harte, kurze Aussagen, die spaeter noch "
            "gelten — Mengen, Preise, Fristen, Zusagen, Namen. Beispiel: "
            '{"subjekt": "Mali-Leder", "praedikat": "email", "objekt": "info@mali-leder.example"}. '
            "Keine Absichten, keine Vermutungen, keine Wiederholung des Auftrags. "
            "Weisst du nichts Bleibendes, gib eine leere Liste.\n\n"
            "Zu 'lieferant': 'email' nur setzen, wenn dir eine echte Empfaenger-Adresse aus "
            "dem Auftrag, dem Gedaechtnis oder dem Lieferantenprofil bekannt ist, sonst null. "
            "'versandbereit' ist nur dann true, wenn 'email' gesetzt ist UND die Nachricht "
            "Erstkontakt, Nachfassen, Musteranfrage oder Musterfeedback ist. Bei Bestellung, "
            "Anzahlung oder jeder Zahlungszusage bleibt 'versandbereit' immer false, "
            "unabhaengig davon ob 'email' bekannt ist — das entscheidet ausschliesslich Bjoern."
        )


if __name__ == "__main__":
    einzeltest(EinkaufDeutschland)
