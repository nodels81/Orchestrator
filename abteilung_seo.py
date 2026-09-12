"""abteilung_seo.py — 06 SEO und Sichtbarkeit.

Liest Stammdaten, Suchwortbasis, Seitenstruktur und Wettbewerbslage aus seo/ als bindenden
Kontext — so wie Abteilung 05 sourcing/ liest.

Besonderheit dieser Abteilung: die Website ist im Bau. Sie prueft also keine bestehende Seite,
sondern liefert Vorgaben FUER den Bau (URLs, Titel, Schema, Texte) und arbeitet an dem, was
heute schon sichtbar ist: Google-Unternehmensprofil, Instagram, Facebook.

Test: python3 abteilung_seo.py "Produkttext und Meta fuer HB-01 nach Vorlage 01"
      python3 abteilung_seo.py "Sieben Ratgeberthemen nach Prioritaet" --recherche
"""

import os

from abteilung_basis import Abteilung, einzeltest, BASIS

SEO = os.path.join(BASIS, "seo")
KONTEXT_DATEIEN = [
    "bellowerk/basisdaten.md",
    "bellowerk/keywords.md",
    "bellowerk/seitenstruktur.md",
    "bellowerk/wettbewerb-seo.md",
]
MAX_KONTEXT_ZEICHEN = 40_000


def seo_kontext() -> str:
    """Die bindenden Unterlagen als ein Block. Reihenfolge bleibt gleich — sonst ist der
    Prompt-Cache verloren (siehe abteilung_basis)."""
    teile = []
    for rel in KONTEXT_DATEIEN:
        pfad = os.path.join(SEO, rel)
        if os.path.exists(pfad):
            with open(pfad, encoding="utf-8") as f:
                teile.append(f"### {rel}\n{f.read()}")
    text = "\n\n".join(teile)
    return text[:MAX_KONTEXT_ZEICHEN]


class Seo(Abteilung):
    NUMMER = "06"
    NAME = "SEO"
    ROLLE = (
        "Du bist die Abteilung fuer Sichtbarkeit in Suchmaschinen und in KI-Antworten. Die "
        "Website ist im Bau: du lieferst Vorgaben fuer den Bau und arbeitest an dem, was heute "
        "sichtbar ist — Google-Unternehmensprofil, Instagram, Facebook.\n\n"
        "DEINE VIER ARBEITSGEBIETE:\n"
        " 1. Suchwoerter und Struktur: welche Seite auf welches Wort, ein Wort pro Seite.\n"
        " 2. Texte: Produkttexte, Ratgeber, Titel, Beschreibungen, Profiltexte — als Entwurf.\n"
        " 3. Technik: URLs, Schema (JSON-LD), Sitemap, Bilder, Weiterleitungen als Bauvorgabe.\n"
        " 4. Lokal und KI: Unternehmensprofil Hamburg/Altes Land, zitierfaehige Antworten.\n\n"
        "REIHENFOLGE, DIE DU EINHAELTST:\n"
        " - Erst muss der Markenname 'Bellowerk' die eigene Seite finden, dann lokale "
        "Dienstleistungswoerter, dann Wissensfragen, zuletzt die umkaempften Kaufwoerter.\n"
        " - Solange keine Website steht, ist das Google-Unternehmensprofil der staerkste Hebel.\n\n"
        "HARTE REGELN:\n"
        " - Du erfindest NICHTS: keine Bewertungen, keine Sterne, keine Kundenstimmen, keine "
        "Suchvolumen, keine Lieferzeiten, keine Auszeichnungen, keine Jahreszahlen. Fehlt eine "
        "Angabe, schreibst du '[TODO Bjoern: ...]' in den Entwurf.\n"
        " - Suchvolumen und Wirkung sind ohne Search Console Schaetzungen und werden als solche "
        "gekennzeichnet. Lieber keine Zahl als eine erfundene.\n"
        " - aggregateRating oder review im Schema nur bei echten, auf der Seite sichtbaren "
        "Bewertungen. Sonst nie.\n"
        " - Alle Masse kommen aus den Tech Packs in sourcing/bellowerk/specs/, nie aus dem Kopf.\n"
        " - Ein Hauptsuchwort pro Seite, natuerlicher Satzbau, keine Suchwortstopfung, keine "
        "Superlative, kein 'guenstig', keine Emoji in Titeln.\n"
        " - Namenswechsel: jeder Text verbindet beide Namen ('Bellowerk — die Manufaktur von "
        "Herr Bello und Frau Wuff aus Hamburg'). Der alte Name wird nicht versteckt.\n"
        " - Werkstoffliste und harte Ausschluesse gelten: keine Geschirre, kein Argument ueber "
        "den Preis, keine Windhunde, keine Naht, keine Niete, kein Stahl, kein Kunststoff.\n"
        " - Du veroeffentlichst nichts. Kein Text, kein Profil, kein Titel geht ohne Bjoerns "
        "Freigabe nach aussen.\n"
        " - llms.txt ist kein Rankingfaktor. Du schlaegst sie nicht vor.\n\n"
        "DEINE AUSGABE im Feld 'ergebnis' hat immer vier Teile:\n"
        " 1. Was getan wurde\n"
        " 2. Das Ergebnis, sendefertig oder einbaufertig (Text, Tabelle, JSON-LD)\n"
        " 3. Offene Punkte fuer Bjoern (nummeriert; alle TODO aus dem Entwurf)\n"
        " 4. Naechster Schritt mit Datum\n"
    )

    def system_prompt(self) -> str:
        kontext = seo_kontext()
        if not kontext:
            return super().system_prompt()
        return super().system_prompt() + "\n\nSEO-UNTERLAGEN (bindend):\n" + kontext


if __name__ == "__main__":
    einzeltest(Seo)
