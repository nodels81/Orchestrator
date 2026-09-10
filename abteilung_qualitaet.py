"""abteilung_qualitaet.py — 09 Qualitaet.

Almut prueft die Arbeit der anderen Abteilungen, BEVOR Bjoern entscheidet:
gegen die harten Ausschluesse, den Preisrahmen, die Praxistauglichkeit
("nah an HB-01/LE-01, schnoerkellos") und die Betriebsregeln.

Auftrag: "pruefe A-2026-006" (Almut holt sich das Ergebnis dieses Auftrags aus
daten/auftraege.json). Steht keine Auftragsnummer drin, prueft sie den Text im Ziel.
Jede Pruefung wird als Zeile ins Pruefbuch (daten/pruefbuch.md) geschrieben.
"""

import datetime
import json
import os
import re

from abteilung_basis import Abteilung, einzeltest, DATEN

ZUSTAND = os.path.join(DATEN, "auftraege.json")
PRUEFBUCH = os.path.join(DATEN, "pruefbuch.md")

PRUEFPUNKTE = [
    "Keine ausgeschlossenen Werkstoffe/Techniken (Naht, Niete, Stahl, Zink/Zamak, "
    "Kunststoff, Klickverschluss, Gurtband, Lack auf Messing, PU-/Spalt-/Bonded-Leder).",
    "Im Preisrahmen herstellbar (Halsband 69-99, Leine 89-139, Zubehoer 25-59 EUR) — "
    "kein aufwaendiges Sonderteil, kein Mehraufwand ohne Nutzen.",
    "Praktikabel und schnoerkellos: nah an der Kernserie HB-01/LE-01, mit vorhandener "
    "Werkstattausstattung baubar, kein Zierrat um seiner selbst willen.",
    "Passt zur Positionierung (Praxistest statt Preis; Familien-/Gebrauchshunde; keine Windhunde) "
    "und zur Farbwelt/Bildsprache.",
    "Schaetzungen sind als Schaetzungen gekennzeichnet, Quelle oder Begruendung genannt, "
    "Masse plausibel.",
    "Keine eigenstaendige Ausgabe, kein Versand nach aussen, keine verbindliche Preiszusage.",
    "Ergebnis ist vollstaendig und fuer Bjoern in unter 10 Minuten entscheidbar.",
]


class Qualitaet(Abteilung):
    NUMMER = "09"
    NAME = "Qualitaet"
    MAX_TOKENS = 6000

    ROLLE = (
        "Du bist die Qualitaetspruefung. Du kontrollierst die Arbeit der anderen "
        "Abteilungen, bevor sie Bjoern vorgelegt wird — nuechtern, konkret, ohne "
        "Schoenrederei und ohne Erbsenzaehlen. Dein Massstab: schnoerkellose, "
        "praxistaugliche Loesungen nah an dem, was der Betrieb schon hat (HB-01, LE-01). "
        "Du entwirfst nichts selbst und schreibst nichts um; du benennst, was noch "
        "fehlt oder nicht passt, und an welche Abteilung es zurueck muss.\n\n"
        "DU PRUEFST GEGEN DIESE PUNKTE:\n"
        + "\n".join(f"  {i+1}. {p}" for i, p in enumerate(PRUEFPUNKTE))
        + "\n\nDEINE AUSGABE im Feld 'ergebnis' hat vier Teile:\n"
        " 1. Was geprueft (welcher Auftrag / welche Abteilung)\n"
        " 2. Pruefergebnis: BESTANDEN / BESTANDEN MIT AUFLAGEN / DURCHGEFALLEN — dazu "
        "je Pruefpunkt eine Zeile ([ok] / [Auflage: ...] / [Fehler: ...])\n"
        " 3. Nachbesserung: nummerierte, konkrete Punkte, jeweils mit Ziel-Abteilung "
        "(z. B. 'zurueck an Konrad (02): ...'). Nichts erfinden, nur was wirklich fehlt.\n"
        " 4. Pruefbuch-Eintrag: eine Zeile im Format "
        "'<Auftrag> (<Abteilung>) -> <Ergebnis>: <Kernaussage in max. 15 Woertern>'\n\n"
        "Wenn dir fuer eine belastbare Pruefung Angaben fehlen, sag das und pruefe die "
        "uebrigen Punkte trotzdem. Kein Geld, kein Versand, nichts nach aussen."
    )

    def bearbeiten(self, auftrag: dict, recherche: bool = False) -> dict:
        ziel = auftrag.get("ziel", "")
        treffer = re.search(r"A-\d{4}-\d+", ziel)
        geprueft_id = treffer.group(0) if treffer else None
        pruefstoff = self._auftrag_ergebnis(geprueft_id) if geprueft_id else None
        if pruefstoff:
            auftrag = dict(auftrag)
            auftrag["ziel"] = (
                f"{ziel}\n\n--- ZU PRUEFEN: Ergebnis von {geprueft_id} "
                f"(Abteilung {pruefstoff['abteilung']}) ---\n{pruefstoff['ergebnis']}"
                + (f"\n\nANMERKUNG der Abteilung: {pruefstoff['anmerkung']}"
                   if pruefstoff.get("anmerkung") else "")
            )
        ergebnis = super().bearbeiten(auftrag, recherche)
        self._pruefbuch(geprueft_id, pruefstoff, ergebnis.get("ergebnis", ""))
        return ergebnis

    @staticmethod
    def _auftrag_ergebnis(auftrag_id: str):
        if not os.path.exists(ZUSTAND):
            return None
        daten = json.load(open(ZUSTAND, encoding="utf-8"))
        a = next((x for x in daten.get("auftraege", []) if x.get("id") == auftrag_id), None)
        if not a or not a.get("verlauf"):
            return None
        v = a["verlauf"][-1]
        return {
            "abteilung": a.get("abteilung", "?"),
            "ergebnis": v.get("ergebnis") or v.get("fehler") or "(kein Ergebnistext)",
            "anmerkung": v.get("anmerkung"),
        }

    @staticmethod
    def _pruefbuch(geprueft_id, pruefstoff, ergebnis_text: str) -> None:
        m = re.search(r"Pruefbuch-Eintrag[:\s]*\n?\s*['\"]?(.+)", ergebnis_text, re.I)
        zeile = m.group(1).strip().strip("'\"") if m else None
        if not zeile:
            kopf = geprueft_id or "freier Text"
            abt = pruefstoff["abteilung"] if pruefstoff else "?"
            zeile = f"{kopf} ({abt}) -> geprueft"
        heute = datetime.date.today().isoformat()
        os.makedirs(DATEN, exist_ok=True)
        neu = not os.path.exists(PRUEFBUCH)
        with open(PRUEFBUCH, "a", encoding="utf-8") as f:
            if neu:
                f.write("# Pruefbuch — Qualitaetspruefungen (Almut, 09)\n\n")
            f.write(f"- {heute} · {zeile}\n")


if __name__ == "__main__":
    einzeltest(Qualitaet)
