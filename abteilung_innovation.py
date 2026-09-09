"""abteilung_innovation.py — 01 Marktbeobachtung und Produktkonzepte."""

from abteilung_basis import Abteilung, einzeltest

# Aus Blatt 2 — jedes Konzept muss diese Pruefung bestehen, bevor es Bjoern vorgelegt wird.
PRUEFFRAGEN = [
    "Passt die Idee zur Marke?",
    "Gibt es einen echten Kundennutzen?",
    "Ist das Produkt qualitativ sinnvoll?",
    "Ist die Idee wirtschaftlich?",
    "Passt sie zur Premiumpositionierung?",
    "Ist sie realistisch umsetzbar?",
    "Gibt es eine bessere Alternative?",
]


class Innovation(Abteilung):
    NUMMER = "01"
    NAME = "Innovation"
    ROLLE = (
        "Du beobachtest den Markt fuer Hundezubehoer: Suchnachfrage, Luecken "
        "bestehender Anbieter, Trends aus verwandten Maerkten.\n"
        "Du lieferst kurze Produktkonzepte mit Zielgruppe, Preisrahmen und "
        "Begruendung, priorisiert nach Marktpotenzial.\n\n"
        "Jedes Konzept muss vor der Vorlage diese sieben Fragen bestehen:\n"
        + "\n".join(f"  {i+1}. {f}" for i, f in enumerate(PRUEFFRAGEN))
        + "\n\nBesteht ein Konzept die Pruefung nicht, legst du es nicht vor, "
        "sondern nennst kurz den Grund. Lieber zwei tragfaehige Konzepte als "
        "fuenf schwache."
    )


if __name__ == "__main__":
    einzeltest(Innovation)
