"""personal_rundgang.py — Wiebkes regelmaessiger Rundgang durch alle Abteilungen.

Liest den Stellenplan (README-Organigramm), alle Agenten, alle Skills und den
Auftragsstand, sucht Schwachstellen und schickt Bjoern einen kurzen Bericht per Mail.
Sie stellt dabei NIEMANDEN ein: der Rundgang meldet nur. Eingestellt wird erst nach
Bjoerns Freigabe, und zwar von Wiebke in einer Claude-Code-Sitzung.

  venv/bin/python personal_rundgang.py --probelauf   nur zeigen, was geladen wird
  venv/bin/python personal_rundgang.py               Bericht erzeugen und anzeigen
  venv/bin/python personal_rundgang.py --senden      Bericht erzeugen und mailen

Woechentlich per systemd-Timer oder cron, z. B. montags 07:30.
"""

import glob
import json
import os
import sys
from datetime import date

from abteilung_basis import Abteilung, BASIS, config_laden
from orchestrator_mail import senden

AGENTEN = os.path.join(BASIS, ".claude", "agents")
SKILLS = os.path.join(BASIS, ".claude", "skills")
PROTOKOLL = os.path.join(BASIS, "personal", "protokoll.md")
ZUSTAND = os.path.join(BASIS, "auftraege.json")
MAX_KONTEXT_ZEICHEN = 60_000

PRUEFPUNKTE = [
    "Jede Abteilung hat einen Pruefer, der nicht die eigene Arbeit beurteilt",
    "Keine zwei Agenten mit ueberlappender Beschreibung",
    "Jede Beschreibung nennt Fachwoerter und einen Nutzen-wenn-Satz",
    "Jeder schreibende Agent hat eine eindeutige Dateihoheit",
    "Keine Abteilung ueber acht Agenten",
    "Kein Fachwissen doppelt in mehreren Agenten statt im Skill",
    "Keine Aufgabe im Betrieb ohne zustaendigen Agenten",
]


def _lesen(pfad: str, grenze: int = 4000) -> str:
    with open(pfad, encoding="utf-8") as f:
        return f.read()[:grenze]


def stellenplan() -> str:
    """Organigramm, Agenten, Skills, Auftragsstand und Personalprotokoll."""
    teile = []

    readme = os.path.join(BASIS, "README.md")
    if os.path.exists(readme):
        text = _lesen(readme, 8000)
        anfang = text.find("### Wer sitzt wo")
        teile.append("### Organigramm\n" + (text[anfang:anfang + 3000] if anfang >= 0 else text[:3000]))

    for pfad in sorted(glob.glob(os.path.join(AGENTEN, "*.md"))):
        teile.append(f"### Agent {os.path.basename(pfad)}\n{_lesen(pfad, 2500)}")

    for pfad in sorted(glob.glob(os.path.join(SKILLS, "*", "SKILL.md"))):
        name = os.path.basename(os.path.dirname(pfad))
        teile.append(f"### Skill {name}\n{_lesen(pfad, 1500)}")

    if os.path.exists(ZUSTAND):
        try:
            with open(ZUSTAND, encoding="utf-8") as f:
                daten = json.load(f)
            zeilen = [
                f"  {a.get('id')} | {a.get('abteilung')} | {a.get('status', '?')} | "
                f"Nacharbeiten: {a.get('nacharbeiten', 0)}"
                for a in daten.get("auftraege", [])[-25:]
            ]
            teile.append("### Auftragsstand (letzte 25)\n" + ("\n".join(zeilen) or "  keine"))
        except (json.JSONDecodeError, OSError) as fehler:
            teile.append(f"### Auftragsstand\n  nicht lesbar: {fehler}")

    if os.path.exists(PROTOKOLL):
        teile.append("### Personalprotokoll (bisherige Einstellungen)\n" + _lesen(PROTOKOLL, 3000))

    return "\n\n".join(teile)[:MAX_KONTEXT_ZEICHEN]


class Personal(Abteilung):
    NUMMER = "S"
    NAME = "Personal (Wiebke)"

    def system_prompt(self) -> str:
        return (
            "Du bist Wiebke, die Personalerin des Bellowerk-Agentenbetriebs. Du stehst neben der "
            "Hierarchie und besetzt die Stellen aller Abteilungen. Heute machst du deinen "
            "Rundgang: du schaust dir jede Abteilung an und suchst Schwachstellen.\n\n"
            "DU STELLST HEUTE NIEMANDEN EIN. Der Rundgang meldet nur. Jede Einstellung braucht "
            "Bjoerns Freigabe und wird danach in einer Claude-Code-Sitzung geschrieben.\n\n"
            "GRUNDSATZ: Eine Stelle wird besetzt, weil Arbeit liegen bleibt, nicht weil ein Titel "
            "fehlt. Nachschaerfen ist fast immer besser als einstellen. Findest du nichts "
            "Wesentliches, sagst du das in zwei Saetzen — ein erfundener Befund kostet Bjoern "
            "mehr Zeit als ein ruhiger Bericht.\n\n"
            "DU PRUEFST GENAU DIESE PUNKTE:\n"
            + "\n".join(f"  {i+1}. {p}" for i, p in enumerate(PRUEFPUNKTE))
            + "\n\nDEINE AUSGABE im Feld 'ergebnis':\n"
            " 1. Lage in drei Zeilen (wie viele Agenten, welche Abteilungen, was auffaellt)\n"
            " 2. Befunde, nummeriert, nach Schwere — je Befund: was, wo, Vorschlag, Aufwand S/M/L\n"
            " 3. Was ich nach deiner Freigabe tun wuerde — als Satz, den Bjoern mit 'ja' "
            "beantworten kann\n"
            " 4. Was ruhig laeuft (eine Zeile, damit Bjoern weiss, dass geprueft wurde)\n\n"
            "Keine Befunde ohne Beleg: nenne immer die Datei oder den Agentennamen. "
            "Antworte auf Deutsch, hoechstens 400 Woerter.\n\n"
            "STELLENPLAN UND UNTERLAGEN (bindend):\n" + stellenplan()
        )


def bericht_erzeugen() -> dict:
    auftrag = {
        "id": f"RUNDGANG-{date.today().isoformat()}",
        "ziel": "Rundgang durch alle Abteilungen: Schwachstellen, fehlende Stellen, Doppelbesetzungen",
        "kriterien": PRUEFPUNKTE,
        "frist": date.today().isoformat(),
        "rahmen": "keine Ausgaben, keine Einstellung ohne Freigabe",
    }
    return Personal().bearbeiten(auftrag)


def main() -> int:
    if "--probelauf" in sys.argv:
        kontext = stellenplan()
        agenten = sorted(os.path.basename(p) for p in glob.glob(os.path.join(AGENTEN, "*.md")))
        skills = sorted(os.path.basename(os.path.dirname(p))
                        for p in glob.glob(os.path.join(SKILLS, "*", "SKILL.md")))
        print(f"[Probelauf] {len(agenten)} Agenten: {', '.join(a[:-3] for a in agenten)}")
        print(f"[Probelauf] {len(skills)} Skills: {', '.join(skills)}")
        print(f"[Probelauf] Kontext {len(kontext)} Zeichen. Kein API-Aufruf, kein Mailversand.")
        return 0

    ergebnis = bericht_erzeugen()
    text = ergebnis.get("ergebnis", "")
    if ergebnis.get("blocker"):
        text += f"\n\nBlocker: {ergebnis['blocker']}"
    print(text)

    if "--senden" in sys.argv:
        betreff = f"[Bello] Personal-Rundgang {date.today().isoformat()}"
        senden(betreff, text + "\n\n-- Wiebke, Personal\n", config_laden())
    return 0


if __name__ == "__main__":
    sys.exit(main())
