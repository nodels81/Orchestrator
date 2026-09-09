"""abteilung_ausfuehrung.py — 02 Spezifikation und bemasste SVG-Zeichnung."""

import os
import re

from abteilung_basis import Abteilung, einzeltest, BASIS

ZEICHNUNGEN = os.path.join(BASIS, "zeichnungen")


class Ausfuehrung(Abteilung):
    NUMMER = "02"
    NAME = "Produkt & Ausfuehrung"
    ROLLE = (
        "Du machst aus einem freigegebenen Konzept eine lieferfertige technische "
        "Zeichnung — Masse, Material, Konstruktion —, damit Bjoern sie nur noch "
        "an den Lieferanten weiterreicht.\n\n"
        "Deine Ausgabe besteht immer aus drei Teilen:\n"
        "  1. Spezifikation (Bauteile, Staerken, Toleranzen)\n"
        "  2. Stueckliste (jedes Teil mit Mass und Material)\n"
        "  3. Bemasste Zeichnung als SVG\n\n"
        "Die SVG-Zeichnung setzt du in das Feld 'ergebnis' zwischen die Marken "
        "<<<SVG>>> und <<</SVG>>>. Sie muss Massangaben als Text enthalten, "
        "masstabsgetreu sein und ohne Farben auskommen (Strichzeichnung).\n\n"
        "Werkstoffe ausserhalb der erlaubten Liste sind unzulaessig. Wenn ein "
        "Konzept ohne ausgeschlossenes Material nicht baubar ist, meldest du das "
        "als Blocker statt es zu umgehen."
    )

    def bearbeiten(self, auftrag: dict, recherche: bool = False) -> dict:
        ergebnis = super().bearbeiten(auftrag, recherche)
        pfad = self._svg_sichern(auftrag.get("id", "ohne-id"), ergebnis.get("ergebnis", ""))
        if pfad:
            ergebnis["zeichnung"] = pfad
        return ergebnis

    @staticmethod
    def _svg_sichern(auftrag_id: str, text: str) -> str | None:
        treffer = re.search(r"<<<SVG>>>(.*?)<<</SVG>>>", text, re.DOTALL)
        if not treffer:
            treffer = re.search(r"(<svg.*?</svg>)", text, re.DOTALL | re.IGNORECASE)
        if not treffer:
            return None
        os.makedirs(ZEICHNUNGEN, exist_ok=True)
        sicher = re.sub(r"[^A-Za-z0-9_-]", "_", auftrag_id)
        pfad = os.path.join(ZEICHNUNGEN, f"{sicher}.svg")
        with open(pfad, "w", encoding="utf-8") as f:
            f.write(treffer.group(1).strip())
        return pfad


if __name__ == "__main__":
    einzeltest(Ausfuehrung)
