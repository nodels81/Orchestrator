"""abteilung_design.py — 06 Design: Wortmarke, Darstellungen, Bildprompts, Shop-Bilder."""

import os
import re

from abteilung_basis import Abteilung, einzeltest, BASIS

ANSICHTEN = os.path.join(BASIS, "sourcing", "bellowerk", "ansichten")


class Design(Abteilung):
    NUMMER = "06"
    NAME = "Design"
    ROLLE = (
        "Du machst sichtbar, worueber sonst nur geredet wird. Bjoern entscheidet am "
        "Bild, nicht am Fliesstext — jedes Konzept, das ihm vorgelegt wird, hat eine "
        "Darstellung.\n\n"
        "Dein Material:\n"
        "  1. Darstellungen fertiger Produkte als SVG (Leder, Messing, gravierter Patch)\n"
        "  2. Konzeptbilder: Verpackung als Auspack-Sequenz, Beschlaege als Teileuebersicht\n"
        "  3. Wortmarke und Gravurvorlagen, Schrift immer in Pfade gewandelt\n"
        "  4. Bildprompts fuer erzeugte Fotos, mit Negativliste und Pruefliste\n\n"
        "Die SVG-Datei setzt du zwischen die Marken <<<SVG>>> und <<</SVG>>>.\n\n"
        "Zwei Regeln, die nicht verhandelbar sind:\n"
        "  - Eine Darstellung traegt sichtbar den Vermerk, dass sie keine Fotografie "
        "ist. Ein Bild, das als Foto durchgeht, obwohl es keins ist, kostet Vertrauen, "
        "sobald es jemand merkt — im Shop waere es irrefuehrend.\n"
        "  - Masse kommen aus dem Tech Pack, nie aus dem Gedaechtnis. Aendert sich ein "
        "Mass, aendert es sich zuerst in der Spezifikation.\n\n"
        "Du erfindest keine Markenaussagen. Was auf einem Anhaenger, einem Patch oder "
        "einer Verpackung steht, entscheidet Bjoern; du machst Vorschlaege und "
        "kennzeichnest sie als solche."
    )

    def bearbeiten(self, auftrag: dict, recherche: bool = False) -> dict:
        ergebnis = super().bearbeiten(auftrag, recherche)
        pfad = self._svg_sichern(auftrag.get("id", "ohne-id"), ergebnis.get("ergebnis", ""))
        if pfad:
            ergebnis["ansicht"] = pfad
        return ergebnis

    @staticmethod
    def _svg_sichern(auftrag_id: str, text: str) -> str | None:
        treffer = re.search(r"<<<SVG>>>(.*?)<<</SVG>>>", text, re.DOTALL)
        if not treffer:
            treffer = re.search(r"(<svg.*?</svg>)", text, re.DOTALL | re.IGNORECASE)
        if not treffer:
            return None
        os.makedirs(ANSICHTEN, exist_ok=True)
        sicher = re.sub(r"[^A-Za-z0-9_-]", "_", auftrag_id)
        pfad = os.path.join(ANSICHTEN, f"{sicher}.svg")
        with open(pfad, "w", encoding="utf-8") as f:
            f.write(treffer.group(1).strip())
        return pfad


if __name__ == "__main__":
    einzeltest(Design)
