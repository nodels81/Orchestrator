"""
ausliefern.py — Bringt das Theme auf die Testdomain, und nach Freigabe auf den Shop.

Der ganze Sinn dieser Datei ist eine Trennung: Der Agent darf jederzeit auf
test.bellowerk.de ausliefern, und NIE von sich aus auf bellowerk.de. Der
Schritt auf den echten Shop passiert nur, wenn Bjoern eine Kennung freigibt,
die er vorher gesehen hat.

Warum die Kennung: Ohne sie gibt Bjoern "den Stand von eben" frei, und bis die
Mail ankommt, hat der Agent schon zweimal weitergebaut. Dann geht etwas live,
das nie jemand angesehen hat. Die Kennung bindet die Freigabe an genau den
Stand, der im Bild war.

Aufrufe:
  ausliefern.py --ziel test             Auf die Testdomain, ohne Rueckfrage
  ausliefern.py --ziel live --kennung K Auf den Shop, nur mit passender Kennung
  ausliefern.py --stand                 Was wartet auf Freigabe
  ausliefern.py --ziel test --probe     Zeigen, was passieren wuerde
"""

import argparse
import json
import os
import secrets
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abteilung_basis import BASIS, config_laden
from orchestrator_mail import senden

QUELLE = os.path.join(BASIS, "wordpress", "bellowerk")
ZUSTAND = os.path.join(BASIS, "logs", "auslieferung.json")
PROTOKOLL = os.path.join(BASIS, "logs", "ausliefern.log")

# Dieser Satz muss nach dem Ausliefern auf der Seite stehen. Steht er nicht,
# ist etwas kaputt — dann wird auf dem Shop zurueckgerollt.
STANDARD_MARKER = "im Alten Land bei Hamburg"


# ---------- Protokoll und Zustand ----------

def _protokoll(zeile: str) -> None:
    os.makedirs(os.path.dirname(PROTOKOLL), exist_ok=True)
    stempel = datetime.now().isoformat(timespec="seconds")
    with open(PROTOKOLL, "a", encoding="utf-8") as f:
        f.write(f"{stempel}  {zeile}\n")
    print(zeile)


def zustand_laden() -> dict:
    if not os.path.exists(ZUSTAND):
        return {"wartet_auf_freigabe": None, "test": None, "live": None, "verlauf": []}
    try:
        with open(ZUSTAND, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"wartet_auf_freigabe": None, "test": None, "live": None, "verlauf": []}


def zustand_speichern(daten: dict) -> None:
    os.makedirs(os.path.dirname(ZUSTAND), exist_ok=True)
    temp = ZUSTAND + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2, ensure_ascii=False)
    os.replace(temp, ZUSTAND)


# ---------- Kennung ----------

def kennung_bauen() -> str:
    """Zeitstempel, Commit und vier Zufallszeichen.

    Die Zufallszeichen sind nicht Zierde: Ohne sie ergaeben zwei
    Auslieferungen in derselben Minute beim selben Commit dieselbe Kennung.
    Bjoerns Freigabe wuerde dann fuer einen Stand gelten, den er nie gesehen
    hat — und genau das soll die Kennung verhindern.
    """
    try:
        commit = subprocess.run(
            ["git", "-C", BASIS, "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=10, check=True,
        ).stdout.strip()
    except (subprocess.SubprocessError, OSError):
        commit = "ohnegit"
    return "{}-{}-{}".format(
        datetime.now().strftime("%Y%m%d-%H%M%S"),
        commit,
        secrets.token_hex(2),
    )


# ---------- Pruefungen vor dem Ausliefern ----------

def php_pruefen() -> list[str]:
    """Jede PHP-Datei durch den Syntaxpruefer. Kaputtes PHP geht nirgendwohin."""
    if not _vorhanden("php"):
        return ["php fehlt — Syntaxpruefung nicht moeglich"]
    kaputt = []
    for wurzel, _, dateien in os.walk(QUELLE):
        for name in dateien:
            if not name.endswith(".php"):
                continue
            pfad = os.path.join(wurzel, name)
            ergebnis = subprocess.run(["php", "-l", pfad], capture_output=True, text=True)
            if ergebnis.returncode != 0:
                kurz = os.path.relpath(pfad, QUELLE)
                kaputt.append(f"{kurz}: {ergebnis.stdout.strip().splitlines()[0]}")
    return kaputt


def _vorhanden(werkzeug: str) -> bool:
    from shutil import which
    return which(werkzeug) is not None


def vorpruefung() -> list[str]:
    maengel = []
    if not os.path.isdir(QUELLE):
        maengel.append(f"{QUELLE} gibt es nicht")
        return maengel
    if not os.path.exists(os.path.join(QUELLE, "style.css")):
        maengel.append("style.css fehlt — das ist kein Theme")
    maengel += php_pruefen()
    for werkzeug in ("rsync", "ssh"):
        if not _vorhanden(werkzeug):
            maengel.append(f"{werkzeug} fehlt")
    return maengel


# ---------- Uebertragen ----------

def _ziel_lesen(config: dict, ziel: str) -> dict:
    angaben = config.get("ausliefern", {}).get(ziel)
    if not angaben:
        raise SystemExit(
            f"In config.json fehlt ausliefern.{ziel}.\n"
            "Erwartet: host, benutzer, pfad, adresse. Siehe autonom/README.md."
        )
    for feld in ("host", "benutzer", "pfad", "adresse"):
        if not angaben.get(feld):
            raise SystemExit(f"In config.json fehlt ausliefern.{ziel}.{feld}")
    return angaben


def uebertragen(angaben: dict, probe: bool = False) -> tuple[bool, str]:
    befehl = [
        "rsync", "-az", "--delete", "--itemize-changes",
        "--exclude", ".DS_Store", "--exclude", "*.swp", "--exclude", ".git*",
        "-e", "ssh",
        QUELLE + "/",
        f"{angaben['benutzer']}@{angaben['host']}:{angaben['pfad']}/",
    ]
    if probe:
        befehl.insert(1, "--dry-run")
    ergebnis = subprocess.run(befehl, capture_output=True, text=True, timeout=600)
    return ergebnis.returncode == 0, (ergebnis.stdout + ergebnis.stderr).strip()


def sichern_auf_server(angaben: dict) -> str | None:
    """Vor dem Ausliefern auf den Shop: den laufenden Stand wegpacken.

    Ohne diese Sicherung gaebe es kein Zurueck, wenn die Pruefung danach
    scheitert. Der Shop steht dann kaputt da, bis jemand von Hand eingreift.
    """
    marke = datetime.now().strftime("%Y%m%d-%H%M%S")
    archiv = f"{angaben['pfad']}.vorher-{marke}.tar.gz"
    befehl = (
        f"cd {angaben['pfad']}/.. && "
        f"tar czf {archiv} $(basename {angaben['pfad']})"
    )
    ergebnis = subprocess.run(
        ["ssh", f"{angaben['benutzer']}@{angaben['host']}", befehl],
        capture_output=True, text=True, timeout=300,
    )
    if ergebnis.returncode != 0:
        _protokoll(f"[AUSLIEFERN] Sicherung auf dem Server scheiterte: {ergebnis.stderr.strip()}")
        return None
    _protokoll(f"[AUSLIEFERN] Sicherung liegt auf dem Server: {archiv}")
    return archiv


def zuruecksetzen(angaben: dict, archiv: str) -> bool:
    befehl = (
        f"cd {angaben['pfad']}/.. && "
        f"rm -rf $(basename {angaben['pfad']}) && "
        f"tar xzf {archiv}"
    )
    ergebnis = subprocess.run(
        ["ssh", f"{angaben['benutzer']}@{angaben['host']}", befehl],
        capture_output=True, text=True, timeout=300,
    )
    return ergebnis.returncode == 0


# ---------- Nachpruefung ----------

def seite_pruefen(adresse: str, marker: str) -> tuple[bool, str]:
    """Seite wirklich abrufen. Ein gelungenes rsync heisst nicht, dass die
    Seite laeuft — ein PHP-Fehler zur Laufzeit zeigt sich erst hier."""
    try:
        anfrage = urllib.request.Request(adresse, headers={"User-Agent": "Bellowerk-Auslieferung"})
        with urllib.request.urlopen(anfrage, timeout=30) as antwort:
            if antwort.status != 200:
                return False, f"HTTP {antwort.status}"
            text = antwort.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as fehler:
        return False, f"HTTP {fehler.code}"
    except Exception as fehler:
        return False, f"nicht erreichbar: {fehler}"

    if marker and marker not in text:
        return False, f"Die Seite laedt, aber der Marker {marker!r} fehlt — Theme nicht aktiv?"
    return True, "Seite laeuft, Marker gefunden"


# ---------- Ablauf ----------

def ausliefern(ziel: str, kennung: str | None = None, probe: bool = False) -> int:
    config = config_laden()
    angaben = _ziel_lesen(config, ziel)
    marker = config.get("ausliefern", {}).get("marker", STANDARD_MARKER)
    daten = zustand_laden()

    if ziel == "live":
        wartend = daten.get("wartet_auf_freigabe")
        if not wartend:
            _protokoll("[AUSLIEFERN] Abgelehnt: es wartet nichts auf Freigabe.")
            return 1
        if kennung and kennung != wartend:
            _protokoll(f"[AUSLIEFERN] Abgelehnt: Kennung {kennung!r} passt nicht zu {wartend!r}.")
            return 1
        kennung = wartend

    kennung = kennung or kennung_bauen()

    maengel = vorpruefung()
    if maengel:
        for m in maengel:
            _protokoll(f"[AUSLIEFERN] Vorpruefung: {m}")
        _protokoll("[AUSLIEFERN] Abbruch. Es wurde nichts uebertragen.")
        return 1

    if probe:
        erfolg, ausgabe = uebertragen(angaben, probe=True)
        print(f"[Probe] Ziel {ziel} · {angaben['adresse']} · Kennung {kennung}")
        print(ausgabe or "(keine Aenderungen)")
        return 0 if erfolg else 1

    archiv = sichern_auf_server(angaben) if ziel == "live" else None

    erfolg, ausgabe = uebertragen(angaben)
    if not erfolg:
        _protokoll(f"[AUSLIEFERN] Uebertragung nach {ziel} scheiterte:\n{ausgabe}")
        senden(f"[Bello] Auslieferung nach {ziel} gescheitert",
               f"Die Uebertragung brach ab.\n\n{ausgabe}", config)
        return 1

    gut, befund = seite_pruefen(angaben["adresse"], marker)
    if not gut:
        _protokoll(f"[AUSLIEFERN] Nachpruefung fehlgeschlagen: {befund}")
        if ziel == "live" and archiv:
            if zuruecksetzen(angaben, archiv):
                _protokoll("[AUSLIEFERN] Shop auf den vorherigen Stand zurueckgesetzt.")
                hinweis = "Der Shop wurde automatisch auf den vorherigen Stand zurueckgesetzt."
            else:
                hinweis = "ACHTUNG: Das Zuruecksetzen ist ebenfalls gescheitert. Der Shop braucht Hilfe von Hand."
        else:
            hinweis = "Die Testdomain bleibt in diesem Zustand stehen."
        senden(f"[Bello] Auslieferung nach {ziel}: Pruefung fehlgeschlagen",
               f"Kennung: {kennung}\nAdresse: {angaben['adresse']}\n\n"
               f"Befund: {befund}\n\n{hinweis}", config)
        return 1

    zeitpunkt = datetime.now().isoformat(timespec="seconds")
    eintrag = {"kennung": kennung, "zeit": zeitpunkt, "adresse": angaben["adresse"]}
    daten[ziel] = eintrag
    daten.setdefault("verlauf", []).insert(0, {"ziel": ziel, **eintrag})
    daten["verlauf"] = daten["verlauf"][:40]

    if ziel == "test":
        daten["wartet_auf_freigabe"] = kennung
        senden(
            "[Bello] Auf der Testdomain: bitte ansehen",
            f"Kennung: {kennung}\n"
            f"Adresse: {angaben['adresse']}\n"
            f"Zeit:    {zeitpunkt}\n\n"
            f"{befund}\n\n"
            "Geaenderte Dateien:\n" + (ausgabe or "(keine)") + "\n\n"
            "Wenn es passt, antworte mit einer Mail an den Orchestrator.\n"
            "Betreff mit Kennwort, erste Zeile im Text:\n\n"
            f"    freigeben {kennung}\n\n"
            "Erst dann geht es auf bellowerk.de. Ohne Freigabe passiert nichts.",
            config,
        )
    else:
        daten["wartet_auf_freigabe"] = None
        senden(
            "[Bello] Der Shop ist auf dem neuen Stand",
            f"Kennung: {kennung}\nAdresse: {angaben['adresse']}\nZeit: {zeitpunkt}\n\n{befund}",
            config,
        )

    zustand_speichern(daten)
    _protokoll(f"[AUSLIEFERN] {ziel}: {kennung} — {befund}")
    return 0


def stand_text() -> str:
    daten = zustand_laden()
    zeilen = ["Auslieferung", ""]
    for ziel in ("test", "live"):
        eintrag = daten.get(ziel)
        if eintrag:
            zeilen.append(f"  {ziel:5} {eintrag['kennung']}  {eintrag['zeit']}")
        else:
            zeilen.append(f"  {ziel:5} noch nie ausgeliefert")
    wartend = daten.get("wartet_auf_freigabe")
    zeilen += ["", f"  Wartet auf Freigabe: {wartend}" if wartend else "  Nichts wartet auf Freigabe."]
    if wartend:
        zeilen += ["", f"  Freigeben mit:  freigeben {wartend}"]
    return "\n".join(zeilen)


def main() -> int:
    zerleger = argparse.ArgumentParser(description=__doc__)
    zerleger.add_argument("--ziel", choices=("test", "live"))
    zerleger.add_argument("--kennung")
    zerleger.add_argument("--probe", action="store_true")
    zerleger.add_argument("--stand", action="store_true")
    args = zerleger.parse_args()

    if args.stand or not args.ziel:
        print(stand_text())
        return 0
    return ausliefern(args.ziel, args.kennung, args.probe)


if __name__ == "__main__":
    sys.exit(main())
