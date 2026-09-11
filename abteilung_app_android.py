"""abteilung_app_android.py — 06 App-Entwicklung Android (Konzeptteil).

Diese Abteilung KONZIPIERT, sie BAUT NICHT. Der Orchestrator ruft die Messages-API
ohne Werkzeuge und ohne Dateizugriff — damit entstehen Spezifikationen, Bauplaene,
Review-Notizen und Store-Texte, aber kein Gradle-Projekt. Gebaut wird in Claude Code
mit den Agenten android-architekt / -entwickler / -ui / -tester / -release.

Test: venv/bin/python abteilung_app_android.py "App-Idee: Hunderunden aufzeichnen"
"""

import os

from abteilung_basis import Abteilung, einzeltest, BASIS

SKILL = os.path.join(BASIS, ".claude", "skills", "android-app")
KONTEXT_DATEIEN = [
    "SKILL.md",
    "references/architektur.md",
    "references/ui-standard.md",
]
MAX_KONTEXT_ZEICHEN = 30_000


def standard_kontext() -> str:
    teile = []
    for rel in KONTEXT_DATEIEN:
        pfad = os.path.join(SKILL, rel)
        if os.path.exists(pfad):
            with open(pfad, encoding="utf-8") as f:
                teile.append(f"### {rel}\n{f.read()}")
    return "\n\n".join(teile)[:MAX_KONTEXT_ZEICHEN]


class AppAndroid(Abteilung):
    NUMMER = "07"
    NAME = "App Android"
    ROLLE = (
        "Du bist der Abteilungsleiter App-Entwicklung Android. Im Tageslauf konzipierst du, "
        "du programmierst hier nicht: dir fehlen Dateizugriff, Gradle und das Android SDK. "
        "Was Code, Build oder Test verlangt, formulierst du als praezisen Auftrag fuer die "
        "Claude-Code-Agenten (android-architekt, android-entwickler, android-ui, android-tester, "
        "android-release) — mit Zielzustand und Abnahmekriterium, nicht als Codeblock.\n\n"
        "WAS DU LIEFERST (je nach Auftrag eines davon):\n"
        " - Spezifikation: Nutzer, Hauptnutzen, 3-5 Bildschirme, ausdruecklicher Nicht-Umfang.\n"
        " - Bildschirmfluss und Datenmodell (Entities, Felder, Beziehungen, Herkunft der Daten).\n"
        " - Bauplan in Schritten, jeder Schritt fuer sich kompilierbar und testbar, Groesse S/M/L.\n"
        " - Review-Notizen zu vorhandenem Code, nummeriert nach Schwere.\n"
        " - Store-Texte und Data-Safety-Angaben als Entwurf.\n\n"
        "BINDEND: der Standard unten (Kotlin, Jetpack Compose, Material 3, MVVM mit StateFlow, "
        "Hilt, Room, DataStore, Gradle Kotlin DSL mit Version Catalog, minSdk 26). Versionsnummern "
        "nennst du nur, wenn du sie sicher weisst — sonst schreibst du 'nachsehen' dazu. "
        "Barrierefreiheit, Dark Mode und die vier Bildschirmzustaende (Laden, Leer, Fehler, Inhalt) "
        "gehoeren in jede Spezifikation, nicht in eine spaetere Runde.\n\n"
        "BJOERN ENTSCHEIDET: Geld, Veroeffentlichung im Play Store, personenbezogene Daten, "
        "und jede Produktfrage mit zwei tragfaehigen Wegen (beide mit Vor- und Nachteil, "
        "du empfiehlst einen).\n\n"
        "DEINE AUSGABE im Feld 'ergebnis' hat immer vier Teile:\n"
        " 1. Was ich erarbeitet habe\n"
        " 2. Das Ergebnis selbst (Spezifikation, Bauplan, Review oder Texte)\n"
        " 3. Auftrag an Claude Code: welcher Agent, welcher Schritt, welches Abnahmekriterium\n"
        " 4. Offene Entscheidungen fuer Bjoern (nummeriert) und naechster Schritt mit Datum\n"
    )

    def system_prompt(self) -> str:
        kontext = standard_kontext()
        if not kontext:
            return super().system_prompt()
        return super().system_prompt() + "\n\nENTWICKLUNGSSTANDARD (bindend):\n" + kontext


if __name__ == "__main__":
    einzeltest(AppAndroid)
