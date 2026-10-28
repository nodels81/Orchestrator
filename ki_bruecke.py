"""
ki_bruecke.py — Claude Code und Codex im selben Repo, ohne Copy & Paste dazwischen.

Beide Werkzeuge lesen dieselbe Projektbeschreibung (AGENTS.md; CLAUDE.md verweist darauf)
und koennen sich ueber diese Datei gegenseitig anstossen:

  ki_bruecke.py an codex  "Aufgabe"            Codex bekommt eine Aufgabe, Antwort kommt hierher
  ki_bruecke.py an claude "Aufgabe"            dasselbe in die andere Richtung
  ki_bruecke.py gegenlesen codex               Codex liest den aktuellen git-Diff gegen
  ki_bruecke.py gegenlesen claude              Claude Code liest ihn gegen

Jede Uebergabe landet als Markdown in uebergabe/ — wer als Naechstes arbeitet (Mensch
oder KI), sieht, was gefragt und was geantwortet wurde. Die Gegenseite arbeitet im
Lesemodus: sie darf pruefen und vorschlagen, aber keine Dateien aendern.
"""

import os
import subprocess
import sys
from datetime import datetime

BASIS = os.path.dirname(os.path.abspath(__file__))
UEBERGABE = os.path.join(BASIS, "uebergabe")
ZEITLIMIT = 900  # Sekunden; ein Codex-/Claude-Lauf darf dauern, aber nicht ewig

# Lesemodus der Gegenseite. Beide CLIs kennen ihn als Startoption.
BEFEHLE = {
    "claude": lambda aufgabe: ["claude", "-p", aufgabe, "--permission-mode", "plan"],
    "codex": lambda aufgabe: ["codex", "exec", "--sandbox", "read-only", aufgabe],
}

RAHMEN = (
    "Du wirst von einer anderen KI ({von}) im Projekt Bellowerk-Orchestrator um Hilfe gebeten. "
    "Lies zuerst AGENTS.md. Aendere keine Dateien; antworte mit Befund und konkretem Vorschlag, "
    "kurz und mit Dateiname:Zeile.\n\nAUFGABE:\n{aufgabe}"
)


class BrueckeFehler(RuntimeError):
    pass


def gegenseite(von: str) -> str:
    return "codex" if von == "claude" else "claude"


def frage(an: str, aufgabe: str, von: str = "claude", ausfuehren=None) -> str:
    """Schickt `aufgabe` an das CLI `an` und gibt dessen Antwort zurueck.

    `ausfuehren` ersetzt subprocess.run — fuer Tests ohne installierte CLIs."""
    if an not in BEFEHLE:
        raise BrueckeFehler(f"Unbekanntes Ziel '{an}'. Moeglich: {', '.join(BEFEHLE)}")
    befehl = BEFEHLE[an](RAHMEN.format(von=von, aufgabe=aufgabe))
    ausfuehren = ausfuehren or subprocess.run
    try:
        lauf = ausfuehren(befehl, cwd=BASIS, capture_output=True, text=True, timeout=ZEITLIMIT)
    except FileNotFoundError as fehler:
        raise BrueckeFehler(
            f"'{befehl[0]}' ist nicht installiert oder nicht im PATH. "
            f"Codex: npm i -g @openai/codex — Claude Code: npm i -g @anthropic-ai/claude-code"
        ) from fehler
    except subprocess.TimeoutExpired as fehler:
        raise BrueckeFehler(f"{an} hat nach {ZEITLIMIT} s nicht geantwortet.") from fehler
    if lauf.returncode != 0:
        raise BrueckeFehler(f"{an} endete mit Code {lauf.returncode}: "
                            f"{(lauf.stderr or lauf.stdout or '').strip()[:500]}")
    antwort = (lauf.stdout or "").strip()
    _ablegen(von, an, aufgabe, antwort)
    return antwort


def diff_aufgabe(ausfuehren=None) -> str:
    """Aufgabentext fuer eine Gegenlesung des aktuellen Standes (Diff gegen HEAD, sonst letzter Commit)."""
    ausfuehren = ausfuehren or subprocess.run
    diff = ausfuehren(["git", "diff", "HEAD"], cwd=BASIS, capture_output=True, text=True).stdout
    quelle = "die uncommitteten Aenderungen (git diff HEAD)"
    if not diff.strip():
        diff = ausfuehren(["git", "show", "HEAD"], cwd=BASIS, capture_output=True, text=True).stdout
        quelle = "den letzten Commit (git show HEAD)"
    if not diff.strip():
        raise BrueckeFehler("Nichts zum Gegenlesen: kein Diff und kein Commit.")
    return (f"Lies {quelle} gegen. Suche Fehler, die Tests nicht fangen: falsche Annahmen, "
            f"verlorene Daten, Verstoesse gegen die Regeln in AGENTS.md. Stil ist egal.\n\n"
            f"```diff\n{diff[:60000]}\n```")


def _ablegen(von: str, an: str, aufgabe: str, antwort: str) -> str:
    os.makedirs(UEBERGABE, exist_ok=True)
    zeit = datetime.now()
    pfad = os.path.join(UEBERGABE, f"{zeit:%Y%m%d-%H%M%S}-{von}-an-{an}.md")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(f"# {von} -> {an}, {zeit:%Y-%m-%d %H:%M}\n\n## Aufgabe\n\n{aufgabe}\n\n"
                f"## Antwort\n\n{antwort}\n")
    return pfad


def main(argumente: list[str]) -> int:
    if len(argumente) >= 2 and argumente[0] in ("an", "gegenlesen"):
        modus, ziel = argumente[0], argumente[1]
        von = gegenseite(ziel)
        try:
            if modus == "an":
                if len(argumente) < 3:
                    raise BrueckeFehler("Aufgabe fehlt.")
                aufgabe = " ".join(argumente[2:])
            else:
                aufgabe = diff_aufgabe()
            print(frage(ziel, aufgabe, von=von))
            return 0
        except BrueckeFehler as fehler:
            print(f"[Bruecke] {fehler}")
            return 1
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
