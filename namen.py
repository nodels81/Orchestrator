"""namen.py — Vornamen der Belegschaft.

Eine einzige Stelle fuer die Namen, damit die Abteilungsdateien nah am Repo bleiben.
Der Orchestrator meldet sich bei Bjoern als Gustav; jede Abteilung hat einen eigenen Namen.
"""

ORCHESTRATOR = "Gustav"

# Abteilungsnummer -> Vorname
VORNAMEN = {
    "01": "Merle",    # Innovation
    "02": "Konrad",   # Produkt & Ausfuehrung
    "03": "Silke",    # Vertrieb
    "04": "Lasse",    # Social Media
    "05": "Wiebke",   # Personal
    "06": "Insa",     # Einkauf
    "07": "Henrik",   # Einkauf China
    "08": "Thea",     # Design (Formgestaltung)
    "09": "Almut",    # Qualitaet (prueft die Arbeit der anderen)
}


def vorname(nummer: str) -> str:
    return VORNAMEN.get(str(nummer).strip()[:2], "")
