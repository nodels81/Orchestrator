"""
waechter.py — Passt auf, dass der autonome Betrieb wirklich laeuft.

Grund: Ein Dienst, der still ausfaellt, sieht genauso aus wie ein Dienst, der
nichts zu melden hat. Beides ist Schweigen. Der Waechter unterscheidet die
beiden Faelle und meldet nur den ersten.

Geprueft wird:
  1. Hat der Orchestrator in den letzten Stunden ueberhaupt gelaufen?
  2. Ist einer der bello-Dienste in systemd auf "failed"?
  3. Wird der Platz auf der Platte knapp?

Gemeldet wird hoechstens einmal je Befund und Zeitfenster, sonst kaeme
stuendlich dieselbe Mail. Erholt sich ein Befund, geht einmal Entwarnung raus.

Aufrufe:
  waechter.py           Pruefen, bei Befund mailen
  waechter.py --probe   Pruefen und anzeigen, nichts senden
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta

# Der Betriebsordner liegt eine Ebene hoeher. Python legt beim Start nur den
# Ordner des Skripts auf den Suchpfad, nicht das Arbeitsverzeichnis — ohne diese
# Zeile findet systemd die Module abteilung_basis, orchestrator und tagesbrief nicht.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abteilung_basis import BASIS, config_laden
from orchestrator_mail import senden

ZUSTAND = os.path.join(BASIS, "auftraege.json")
GEDAECHTNIS = os.path.join(BASIS, "logs", "waechter-zustand.json")

DIENSTE = [
    "bello-lauf.timer",
    "bello-tagesbrief.timer",
    "bello-posteingang.timer",
]

STUNDEN_OHNE_LAUF = 6      # danach gilt der Betrieb als stehengeblieben
WIEDERVORLAGE_STUNDEN = 12  # so lange wird derselbe Befund nicht erneut gemeldet
PLATZ_MINDEST_MB = 500


# ---------- Gedaechtnis ----------

def _gedaechtnis_laden() -> dict:
    if not os.path.exists(GEDAECHTNIS):
        return {}
    try:
        with open(GEDAECHTNIS, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _gedaechtnis_speichern(daten: dict) -> None:
    os.makedirs(os.path.dirname(GEDAECHTNIS), exist_ok=True)
    temp = GEDAECHTNIS + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2, ensure_ascii=False)
    os.replace(temp, GEDAECHTNIS)


# ---------- Pruefungen ----------

def _letzter_lauf() -> tuple[str, str] | None:
    if not os.path.exists(ZUSTAND):
        return ("kein_zustand",
                f"{ZUSTAND} gibt es nicht. Der Orchestrator hat hier nie gelaufen.")
    try:
        with open(ZUSTAND, encoding="utf-8") as f:
            daten = json.load(f)
    except (json.JSONDecodeError, OSError) as fehler:
        return ("zustand_kaputt", f"{ZUSTAND} laesst sich nicht lesen: {fehler}")

    stempel = daten.get("letzter_lauf")
    if not stempel:
        return None  # frisch aufgesetzt, noch kein Lauf — kein Alarmgrund
    try:
        alter = datetime.now() - datetime.fromisoformat(stempel)
    except ValueError:
        return ("zustand_kaputt", f"letzter_lauf ist kein Zeitstempel: {stempel!r}")

    if alter > timedelta(hours=STUNDEN_OHNE_LAUF):
        stunden = int(alter.total_seconds() // 3600)
        return ("kein_lauf",
                f"Der letzte Lauf war vor {stunden} Stunden ({stempel}).\n"
                f"Erwartet wird mindestens alle {STUNDEN_OHNE_LAUF} Stunden einer.\n\n"
                "Nachsehen:  systemctl status bello-lauf.timer\n"
                "            journalctl -u bello-lauf.service -n 50")
    return None


EINHEITEN_ORDNER = "/etc/systemd/system"


def _dienste_pruefen() -> tuple[str, str] | None:
    if not shutil.which("systemctl"):
        return None
    # Nur pruefen, was autonom.sh wirklich installiert hat. Sonst schlaegt der
    # Waechter vor der Einrichtung und nach --entfernen grundlos Alarm.
    eingerichtet = [d for d in DIENSTE
                    if os.path.exists(os.path.join(EINHEITEN_ORDNER, d))]
    if not eingerichtet:
        return None
    kaputt = []
    for dienst in eingerichtet:
        try:
            ergebnis = subprocess.run(
                ["systemctl", "is-active", dienst],
                capture_output=True, text=True, timeout=10,
            )
        except (subprocess.SubprocessError, OSError) as fehler:
            kaputt.append(f"{dienst}: nicht abfragbar ({fehler})")
            continue
        stand = ergebnis.stdout.strip()
        if stand != "active":
            kaputt.append(f"{dienst}: {stand or 'unbekannt'}")
    if kaputt:
        return ("dienste",
                "Diese Dienste laufen nicht:\n"
                + "\n".join(f"  {z}" for z in kaputt)
                + "\n\nWieder anwerfen:  systemctl start <name>\n"
                  "Ursache:          journalctl -u <name> -n 50")
    return None


def _platz_pruefen() -> tuple[str, str] | None:
    try:
        belegung = shutil.disk_usage(BASIS)
    except OSError:
        return None
    frei_mb = belegung.free // (1024 * 1024)
    if frei_mb < PLATZ_MINDEST_MB:
        return ("platz",
                f"Auf der Platte sind noch {frei_mb} MB frei, Grenze ist "
                f"{PLATZ_MINDEST_MB} MB.\n"
                "Meist sind es die Sicherungen in /opt/bello-sicherungen "
                "oder die Logs.")
    return None


# ---------- Ablauf ----------

def wachen(probe: bool = False) -> int:
    befunde = [b for b in (_letzter_lauf(), _dienste_pruefen(), _platz_pruefen()) if b]
    gedaechtnis = _gedaechtnis_laden()
    jetzt = datetime.now()
    config = config_laden() if not probe else {}

    offene_schluessel = {schluessel for schluessel, _ in befunde}
    zu_melden = []

    for schluessel, text in befunde:
        letzte = gedaechtnis.get(schluessel, {}).get("gemeldet")
        if letzte:
            try:
                if jetzt - datetime.fromisoformat(letzte) < timedelta(hours=WIEDERVORLAGE_STUNDEN):
                    continue
            except ValueError:
                pass
        zu_melden.append((schluessel, text))
        gedaechtnis[schluessel] = {"gemeldet": jetzt.isoformat(timespec="seconds")}

    # Entwarnung fuer alles, was vorher gemeldet war und jetzt wieder geht.
    entwarnungen = [s for s in list(gedaechtnis) if s not in offene_schluessel]
    for schluessel in entwarnungen:
        gedaechtnis.pop(schluessel, None)

    if probe:
        if befunde:
            for schluessel, text in befunde:
                print(f"--- {schluessel} ---\n{text}\n")
        else:
            print("Alles in Ordnung. Es bliebe still.")
        if entwarnungen:
            print(f"Entwarnung faellig fuer: {', '.join(entwarnungen)}")
        return 1 if befunde else 0

    if zu_melden:
        text = "\n\n".join(t for _, t in zu_melden)
        senden(f"[Bello] Waechter: {len(zu_melden)} Befund(e)", text, config)
    if entwarnungen:
        senden("[Bello] Waechter: wieder in Ordnung",
               "Diese Befunde haben sich erledigt:\n"
               + "\n".join(f"  {s}" for s in entwarnungen), config)

    _gedaechtnis_speichern(gedaechtnis)

    if not befunde and not entwarnungen:
        print("Alles in Ordnung. Es bleibt still.")
    return 1 if befunde else 0


if __name__ == "__main__":
    sys.exit(wachen(probe="--probe" in sys.argv))
