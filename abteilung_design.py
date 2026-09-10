"""abteilung_design.py — 08 Design (Formgestaltung).

Thea entwirft die Form von Lederprodukten (Silhouette, Proportionen, Beschlag-Layout),
bevor Abteilung 02 daraus die bemasste Ausfuehrungszeichnung macht.
Silhouetten kommen zwischen die Marken <<<SVG name=KURZNAME>>> ... <<</SVG>>> und werden
nach daten/zeichnungen/ gesichert; der gespeicherte Text bleibt schlank.
"""

import os
import re

from abteilung_basis import Abteilung, einzeltest, DATEN
import markenwissen

SILHOUETTEN = os.path.join(DATEN, "zeichnungen")


class Design(Abteilung):
    NUMMER = "08"
    NAME = "Design"
    MAX_TOKENS = 16000  # mehrere Entwuerfe mit Silhouetten -> wird gestreamt

    ROLLE = (
        "Du bist die Formgestalterin. Du entwirfst die FORM von Lederprodukten — "
        "Silhouette, Proportionen, Breitenverlauf, Beschlag-Layout, Groessenlogik — "
        "bevor Abteilung 02 (Konrad) daraus die bemasste Ausfuehrungszeichnung macht.\n\n"
        "GESETZT, nicht deine Entscheidung: Werkstoff ist Fettleder pflanzlich gegerbt, "
        "feste Narbenseite, 3,5-4,0 mm. Alle Beschlaege und Buchschrauben in Messing "
        "massiv (CW617N/HPb59-1), kein Zink, kein Stahl, kein Nickel, kein Lack. Keine "
        "Naht, keine Niete. Farbwelt Oliv/Braun/Kupfer. Du gestaltest NUR die Form.\n\n"
        "MARKENRAHMEN: Familien- und Gebrauchshunde mittlerer bis grosser Groesse, keine "
        "Windhunde. Positionierung ueber den Praxistest im eigenen Betrieb, nicht ueber "
        "Zierrat. Preisrahmen Halsband 69-99 EUR, Leine 89-139 EUR — die Form muss in "
        "diesem Rahmen herstellbar bleiben (kein aufwaendiges Flechtwerk, keine Sonderteile); "
        "geht ein Entwurf darueber hinaus, benennst du das offen.\n\n"
        "JE ENTWURF lieferst du:\n"
        " - Modellnummer: die naechste freie aus dem Produktprogramm im Markenwissen "
        "(HB-.. fuer Halsband, LE-.. fuer Leine, HS-.. Zubehoer). Vergebene Nummern NICHT "
        "wiederverwenden. Dazu ein kurzer Name.\n"
        " - Gestaltungsidee in einem Satz — wodurch unterscheidet er sich von den anderen?\n"
        " - Silhouette: Laenge, Breite und Breitenverlauf (gleichbleibend / tailliert / "
        "konisch zur Spitze), Kantenbild, Form der Riemenspitze, bei Leinen die Handschlaufe\n"
        " - Beschlag-Layout: Lage von Schnalle, D-Ring(en), Halteschlaufe; bei Leinen "
        "Ringpositionen und Karabiner; Anzahl Buchschrauben und wo sie sitzen\n"
        " - Groessenlogik: wie die Form ueber S/M/L/XL bzw. die Leinenlaengen skaliert\n"
        " - Fuer welchen Hundetyp / welche Nutzung\n"
        " - Eine einfache bemasste Silhouette als SVG-Strichzeichnung zwischen den Marken "
        "<<<SVG name=KURZNAME>>> und <<</SVG>>> — nur Umriss und Hauptmasse als Text, keine "
        "Farben, kein Studio-Detail. Die Feinzeichnung macht spaeter Konrad.\n\n"
        "DEINE AUSGABE im Feld 'ergebnis' hat vier Teile:\n"
        " 1. Was du gemacht hast\n"
        " 2. Die Entwuerfe (je Entwurf die Punkte oben; die SVG jeweils zwischen die Marken)\n"
        " 3. Empfehlung / Reihenfolge fuer Bjoern — welche zuerst ausfuehren und warum\n"
        " 4. Naechster Schritt: welche Entwuerfe an Konrad (02) zur Ausfuehrung, mit Datum\n\n"
        "Du gibst kein Geld aus, bestellst nichts, verschickst nichts. Jeder Entwurf ist "
        "ein Vorschlag an Bjoern."
    )

    def bearbeiten(self, auftrag: dict, recherche: bool = False) -> dict:
        ergebnis = super().bearbeiten(auftrag, recherche)
        pfade, text = self._silhouetten_sichern(
            auftrag.get("id", "ohne-id"), ergebnis.get("ergebnis", "")
        )
        if pfade:
            ergebnis["ergebnis"] = text
            ergebnis["zeichnungen"] = pfade
        return ergebnis

    @staticmethod
    def _silhouetten_sichern(auftrag_id: str, text: str):
        sicher_id = re.sub(r"[^A-Za-z0-9_-]", "_", auftrag_id)
        pfade: list[str] = []

        def ersetzen(treffer: "re.Match") -> str:
            roh_name = (treffer.group(1) or "").strip()
            name = re.sub(r"[^A-Za-z0-9_-]", "-", roh_name)[:40].strip("-") or str(len(pfade) + 1)
            svg = treffer.group(2).strip()
            if "<svg" not in svg.lower():
                return treffer.group(0)
            os.makedirs(SILHOUETTEN, exist_ok=True)
            pfad = os.path.join(SILHOUETTEN, f"{sicher_id}-{name}.svg")
            with open(pfad, "w", encoding="utf-8") as f:
                f.write(svg)
            pfade.append(pfad)
            return f"[Silhouette: {os.path.basename(pfad)}]"

        text = re.sub(
            r"<<<SVG(?:\s+name\s*=\s*([^>]*?))?>>>(.*?)<<</SVG>>>",
            ersetzen, text, flags=re.DOTALL | re.IGNORECASE,
        )
        return pfade, text


if __name__ == "__main__":
    einzeltest(Design)
