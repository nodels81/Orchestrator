"""
markenwissen-abgleich.py — Bringt das Markenwissen auf dem Server in Ordnung,
ohne es zu ueberschreiben.

Warum nicht einfach kopieren: Auf dem Server laufen Abteilungen, die es in
diesem Zweig nicht gibt (07 Einkauf China, 08 Design, 09 Qualitaet,
10 Homepage). Deren markenwissen.py kann Felder enthalten, die hier niemand
kennt. Eine Kopie wuerde sie stillschweigend loeschen. Deshalb aendert dieses
Skript nur die Stellen, die nachweislich falsch sind, und laesst alles andere
unberuehrt.

Belegt falsch, Stand 13.09.2026 (aus Auftrag A-2026-012, Abteilung 10 Homepage):
  - HB-03 wurde dort "Hamburg No.1" genannt. No. 1 ist HB-01.
  - "gefertigt in Hamburg/Altes Land" — der Betrieb sitzt in Harsefeld,
    und die Formulierung widerspricht dem Impressum.
  - Die Verkaufsnamen der Kollektion kamen gar nicht vor.

Aufrufe:
  python3 markenwissen-abgleich.py            zeigt nur an, aendert nichts
  python3 markenwissen-abgleich.py --anwenden aendert nach Rueckfrage
"""

import datetime
import os
import pathlib
import re
import shutil
import subprocess
import sys

DATEI = pathlib.Path("markenwissen.py")

# ── Was stimmen muss. Quelle: konzepte/kollektion-01-hamburg.md und
#    sourcing/bellowerk/markenbrief.md, beide bindend. ────────────────────
SOLL_TEXTE = {
    "STANDORT": "Harsefeld (Altes Land), Landkreis Stade",
    "HERKUNFTSSATZ": (
        "Entworfen, geprueft und gehandelt im Alten Land bei Hamburg. "
        "Gefertigt in Deutschland."
    ),
}

SOLL_BLOECKE = {
    "VERKAUFSNAMEN": '''VERKAUFSNAMEN = {
    "HB-01": "Hamburg No. 1",
    "LE-01": "Hamburg No. 2",
    "HS-01": "Hamburg No. 3",
    "HB-02": "Hamburg No. 4",
    "LE-02": "Hamburg No. 5",
    "HB-03": "Hamburg No. 6",
    "KO-01": "Hamburg No. 7",
}''',
    "FERTIGUNGSORT": '''FERTIGUNGSORT = {
    "HB-01": "Harsefeld, Deutschland",
    "LE-01": "Harsefeld, Deutschland",
    "HS-01": "Harsefeld, Deutschland",
    "HB-02": "Harsefeld, Deutschland",
    "LE-02": "Harsefeld, Deutschland",
    "HB-03": "Harsefeld, Deutschland",
    "KO-01": "Harsefeld, Deutschland",
    "PATCH-01": "Harsefeld, Deutschland",
}''',
}


def rot(s):  return f"\033[31m{s}\033[0m"
def gruen(s): return f"\033[32m{s}\033[0m"
def fett(s): return f"\033[1m{s}\033[0m"


def text_lesen(quelle: str, name: str) -> str | None:
    """Liest eine einfache Zuweisung NAME = "..." heraus."""
    treffer = re.search(rf'^{name}\s*=\s*(["\'])(.*?)\1\s*$', quelle, re.M)
    return treffer.group(2) if treffer else None


def block_finden(quelle: str, name: str) -> tuple[int, int] | None:
    """Findet NAME = { ... } und gibt Anfang und Ende zurueck."""
    anfang = re.search(rf'^{name}\s*=\s*\{{', quelle, re.M)
    if not anfang:
        return None
    tiefe, i = 0, anfang.start()
    while i < len(quelle):
        if quelle[i] == "{":
            tiefe += 1
        elif quelle[i] == "}":
            tiefe -= 1
            if tiefe == 0:
                return anfang.start(), i + 1
        i += 1
    return None


# Die Abteilungen lesen das Markenwissen nicht direkt, sondern ueber
# als_kontext(). Steht ein Feld zwar in der Datei, wird aber dort nicht
# genannt, bekommt es niemand zu sehen. Dieser Nachtrag haengt sich hinter
# die vorhandene Funktion, statt sie umzuschreiben — was darin steht, kann
# auf diesem Server anders sein als hier, und daran wird nicht gerueht.
NACHTRAG = r'''

# ── Nachtrag 13.09.2026, angehaengt von markenwissen-abgleich.py ──────────
# Grund: als_kontext() stammt aus einer aelteren Fassung und nennt die
# Verkaufsnamen, den Herkunftssatz und den Fertigungsort nicht. Statt die
# Funktion umzuschreiben, wird sie hier umwickelt. Die alte bleibt unter
# ihrem neuen Namen erhalten und laesst sich jederzeit zurueckholen.
_als_kontext_vor_nachtrag = als_kontext


def als_kontext() -> str:
    zeilen = [_als_kontext_vor_nachtrag()]

    zeilen += ["", "VERKAUFSNAMEN (nach aussen der Name, intern die Nummer):"]
    for kuerzel, name in VERKAUFSNAMEN.items():
        zeilen.append(f"  - {kuerzel} heisst {name}")

    zeilen += ["", "HERKUNFT (bindend, wortgleich verwenden): " + HERKUNFTSSATZ]
    orte = sorted(set(FERTIGUNGSORT.values()))
    if len(orte) == 1:
        zeilen.append(f"  Fertigung aller Artikel: {orte[0]}")
    else:
        for kuerzel, ort in FERTIGUNGSORT.items():
            zeilen.append(f"  {kuerzel}: gefertigt in {ort}")
    zeilen.append("  Kein Satz behauptet Fertigung in Hamburg. Der Betrieb sitzt")
    zeilen.append("  in Harsefeld im Alten Land, rund 40 km von Hamburg.")

    return "\n".join(zeilen)
'''


def kontext_prueft(quelle: str) -> bool:
    """Nennt als_kontext() die neuen Felder schon?"""
    if "_als_kontext_vor_nachtrag" in quelle:
        return True  # Nachtrag liegt bereits an
    anfang = quelle.find("def als_kontext")
    if anfang == -1:
        return True  # keine solche Funktion — dann gibt es nichts zu ergaenzen
    koerper = quelle[anfang:]
    return all(f in koerper for f in ("VERKAUFSNAMEN", "HERKUNFTSSATZ", "FERTIGUNGSORT"))


def pruefen(quelle: str) -> list[dict]:
    befunde = []

    for name, soll in SOLL_TEXTE.items():
        ist = text_lesen(quelle, name)
        if ist is None:
            befunde.append({"name": name, "art": "fehlt", "ist": None, "soll": soll})
        elif ist != soll:
            befunde.append({"name": name, "art": "abweichend", "ist": ist, "soll": soll})

    if not kontext_prueft(quelle):
        befunde.append({
            "name": "als_kontext()", "art": "nennt die neuen Felder nicht",
            "ist": "Die Abteilungen bekommen Verkaufsnamen, Herkunftssatz und "
                   "Fertigungsort nicht zu sehen.",
            "soll": "Nachtrag wird hinten angehaengt, die alte Funktion bleibt erhalten.",
        })

    for name, soll in SOLL_BLOECKE.items():
        stelle = block_finden(quelle, name)
        if stelle is None:
            befunde.append({"name": name, "art": "fehlt", "ist": None, "soll": soll})
        else:
            ist = quelle[stelle[0]:stelle[1]]
            if ist.strip() != soll.strip():
                befunde.append({"name": name, "art": "abweichend", "ist": ist, "soll": soll})

    return befunde


def anwenden(quelle: str, befunde: list[dict]) -> str:
    kontext_nachtragen = any(b["name"] == "als_kontext()" for b in befunde)

    for b in befunde:
        name, soll = b["name"], b["soll"]

        if name == "als_kontext()":
            continue  # kommt zum Schluss, nach allen Konstanten

        if name in SOLL_TEXTE:
            if b["art"] == "abweichend":
                quelle = re.sub(
                    rf'^{name}\s*=\s*(["\']).*?\1\s*$',
                    f'{name} = "{soll}"',
                    quelle, count=1, flags=re.M,
                )
            else:
                quelle = quelle.rstrip() + f'\n\n{name} = "{soll}"\n'
        else:
            stelle = block_finden(quelle, name)
            if stelle:
                quelle = quelle[:stelle[0]] + soll + quelle[stelle[1]:]
            else:
                quelle = quelle.rstrip() + "\n\n" + soll + "\n"

    # Der Nachtrag muss ans Ende: Er benutzt die Konstanten, die oben
    # vielleicht gerade erst dazugekommen sind.
    if kontext_nachtragen:
        quelle = quelle.rstrip() + "\n" + NACHTRAG
    return quelle


def main() -> int:
    if not DATEI.exists():
        print(rot(f"FEHLER: {DATEI} gibt es hier nicht."))
        print("        Im Betriebsordner ausfuehren, etwa /opt/bello.")
        return 1

    quelle = DATEI.read_text(encoding="utf-8")
    befunde = pruefen(quelle)

    print(fett("=== Markenwissen abgleichen ==="))
    print(f"Datei: {DATEI.resolve()}\n")

    if not befunde:
        print(gruen("Alles in Ordnung. Nichts zu aendern."))
        return 0

    for b in befunde:
        print(fett(f"{b['name']} — {b['art']}"))
        if b["ist"] is not None:
            for zeile in str(b["ist"]).splitlines():
                print(rot("  - " + zeile))
        for zeile in str(b["soll"]).splitlines():
            print(gruen("  + " + zeile))
        print()

    print(f"{len(befunde)} Stelle(n) weichen ab.")
    print("Alles andere in der Datei bleibt unberuehrt — auch Felder, die es")
    print("nur auf diesem Server gibt.\n")

    if "--anwenden" not in sys.argv:
        print("Nichts geaendert. Zum Anwenden:")
        print("  python3 markenwissen-abgleich.py --anwenden")
        return 0

    antwort = input("Aendern? Nur 'ja' fuehrt aus: ")
    if antwort != "ja":
        print("Abgebrochen. Nichts geaendert.")
        return 0

    # Vorher pruefen, ob sich die Datei ueberhaupt laden laesst. Sonst wuerde
    # ein fehlendes Paket spaeter wie ein Fehler dieser Aenderung aussehen,
    # und eine richtige Aenderung fiele zu Unrecht zurueck.
    vorher_ladbar = subprocess.run(
        [sys.executable, "-c", "import markenwissen"],
        capture_output=True, text=True, cwd=os.getcwd(),
    ).returncode == 0
    if not vorher_ladbar:
        print("Hinweis: markenwissen.py laesst sich schon jetzt nicht laden.")
        print("         Nach der Aenderung wird deshalb nur die Syntax geprueft.")

    marke = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    sicherung = DATEI.with_suffix(f".py.vorher-{marke}")
    shutil.copy2(DATEI, sicherung)
    print(f"Sicherung: {sicherung}")

    DATEI.write_text(anwenden(quelle, befunde), encoding="utf-8")

    # Syntax immer pruefen. Laden nur, wenn es vorher auch ging.
    pruefbefehl = (
        "import markenwissen; print(markenwissen.STANDORT)" if vorher_ladbar
        else "import ast; ast.parse(open('markenwissen.py', encoding='utf-8').read()); "
             "print('Syntax in Ordnung')"
    )
    probe = subprocess.run(
        [sys.executable, "-c", pruefbefehl],
        capture_output=True, text=True, cwd=os.getcwd(),
    )
    if probe.returncode != 0:
        shutil.copy2(sicherung, DATEI)
        print(rot("FEHLER: Die geaenderte Datei ist kaputt."))
        print(probe.stderr.strip())
        print(gruen("Zurueckgesetzt. Die Datei ist wieder wie vorher."))
        return 1

    print(gruen("Geaendert und geprueft."))
    print(f"  {probe.stdout.strip()}")
    print()
    if vorher_ladbar:
        probe2 = subprocess.run(
            [sys.executable, "-c",
             "import markenwissen as m; t = m.als_kontext(); "
             "print('Verkaufsnamen im Kontext:', 'Hamburg No. 1' in t); "
             "print('Herkunftssatz im Kontext:', 'Alten Land' in t)"],
            capture_output=True, text=True, cwd=os.getcwd(),
        )
        for zeile in probe2.stdout.strip().splitlines():
            print("  " + zeile)
        print()

    print("Die Abteilungen lesen das beim naechsten Auftrag. Ergebnisse, die")
    print("vorher entstanden sind — etwa A-2026-011 und A-2026-012 von")
    print("10 Homepage — tragen weiterhin die alten Angaben.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
