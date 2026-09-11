"""
orchestrator.py — Steuerung: verteilt Auftraege, prueft Ergebnisse, eskaliert.

Grundprinzip: Schweigen ist der Normalzustand. Er meldet sich nur, wenn er ohne
Bjoern nicht weiterkommt. Alles andere sammelt er fuer die Wochenuebersicht.

Aufrufe:
  orchestrator.py                                   Lauf sofort ausloesen
  orchestrator.py --probelauf                       Trockenlauf, keine API-Kosten
  orchestrator.py --stand                           Woran wird gearbeitet
  orchestrator.py --auftrag "01 Innovation" "Ziel" [Frist]
  orchestrator.py --wochenbericht
"""

import json
import os
import sys
from datetime import date, datetime, timedelta

from abteilung_basis import BASIS, config_laden
from orchestrator_mail import senden

ZUSTAND = os.path.join(BASIS, "auftraege.json")
MAX_NACHARBEIT = 2

ABTEILUNGEN = {
    "01 Innovation": ("abteilung_innovation", "Innovation"),
    "02 Produkt & Ausführung": ("abteilung_ausfuehrung", "Ausfuehrung"),
    "03 Vertrieb": ("abteilung_vertrieb", "Vertrieb"),
    "04 Social Media": ("abteilung_social", "Social"),
    "05 Einkauf China": ("abteilung_einkauf_china", "EinkaufChina"),
    "07 App Android": ("abteilung_app_android", "AppAndroid"),
}


# ---------- Zustand ----------

def zustand_laden() -> dict:
    if not os.path.exists(ZUSTAND):
        return {"auftraege": [], "letzter_lauf": None, "letzter_wochenbericht": None}
    with open(ZUSTAND, encoding="utf-8") as f:
        return json.load(f)


def zustand_speichern(daten: dict) -> None:
    temp = ZUSTAND + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2, ensure_ascii=False)
    os.replace(temp, ZUSTAND)


def naechste_id(daten: dict) -> str:
    jahr = date.today().year
    nummern = [
        int(a["id"].split("-")[-1])
        for a in daten["auftraege"]
        if a["id"].startswith(f"A-{jahr}-")
    ]
    return f"A-{jahr}-{max(nummern, default=0) + 1:03d}"


# ---------- Auftraege ----------

def auftrag_anlegen(abteilung: str, ziel: str, frist: str | None = None,
                    kriterien: list[str] | None = None) -> dict:
    if abteilung not in ABTEILUNGEN:
        raise ValueError(f"Unbekannte Abteilung '{abteilung}'. Bekannt: {list(ABTEILUNGEN)}")
    daten = zustand_laden()
    auftrag = {
        "id": naechste_id(daten),
        "abteilung": abteilung,
        "ziel": ziel,
        "kriterien": kriterien or [
            "Ergebnis ist konkret und umsetzbar",
            "Passt zur Marke und zum Preisrahmen",
            "Quelle oder Begruendung genannt",
        ],
        "frist": frist or (date.today() + timedelta(days=7)).isoformat(),
        "rahmen": "keine Ausgaben",
        "stand": "offen",
        "versuche": 0,
        "eskaliert": False,
        "verlauf": [],
        "angelegt": datetime.now().isoformat(timespec="seconds"),
    }
    daten["auftraege"].append(auftrag)
    zustand_speichern(daten)
    print(f"Auftrag {auftrag['id']} an {abteilung} angelegt, Frist {auftrag['frist']}.")
    return auftrag


def abteilung_laden(name: str):
    modul_name, klassen_name = ABTEILUNGEN[name]
    modul = __import__(modul_name)
    return getattr(modul, klassen_name)()


# ---------- Pruefung ----------

def pruefen(auftrag: dict, ergebnis: dict) -> tuple[bool, str]:
    erfuellt = ergebnis.get("kriterien_erfuellt", [])
    offen = [
        k for k, ok in zip(auftrag["kriterien"], erfuellt) if not ok
    ]
    if ergebnis.get("blocker"):
        return False, f"Blocker: {ergebnis['blocker']}"
    if offen:
        return False, "Nicht erfuellt: " + "; ".join(offen)
    return True, "Alle Kriterien erfuellt."


def eskalieren(auftrag: dict, grund: str, text: str, config: dict) -> None:
    auftrag["eskaliert"] = True
    auftrag["stand"] = "wartet auf Bjoern"
    betreff = f"[Bello] {auftrag['id']} {auftrag['abteilung']} — {grund}"
    senden(betreff, text, config)


# ---------- Lauf ----------

def lauf(probelauf: bool = False) -> None:
    config = config_laden()
    daten = zustand_laden()
    offen = [a for a in daten["auftraege"] if a["stand"] in ("offen", "nacharbeit")]

    if not offen:
        print("Keine offenen Auftraege. Es bleibt still.")
        if probelauf:
            return
        daten["letzter_lauf"] = datetime.now().isoformat(timespec="seconds")
        zustand_speichern(daten)
        _wochenbericht_faellig(daten, config)
        return

    eskalationen = 0
    for auftrag in offen:
        print(f"\n--- {auftrag['id']} | {auftrag['abteilung']} ---")
        print(f"    Ziel: {auftrag['ziel']}")

        if probelauf:
            print("    [Probelauf] Kein API-Aufruf, kein Mailversand.")
            continue

        try:
            ergebnis = abteilung_laden(auftrag["abteilung"]).bearbeiten(auftrag)
        except Exception as fehler:
            auftrag["stand"] = "gestoert"
            auftrag["verlauf"].append({"zeit": _jetzt(), "fehler": str(fehler)})
            eskalieren(auftrag, "Technischer Fehler",
                       f"Auftrag: {auftrag['ziel']}\n\nFehler: {fehler}", config)
            eskalationen += 1
            continue

        auftrag["versuche"] += 1
        bestanden, begruendung = pruefen(auftrag, ergebnis)
        auftrag["verlauf"].append({
            "zeit": _jetzt(),
            "versuch": auftrag["versuche"],
            "bestanden": bestanden,
            "begruendung": begruendung,
            "ergebnis": ergebnis.get("ergebnis", "")[:4000],
            "anmerkung": ergebnis.get("anmerkung"),
        })

        if bestanden:
            auftrag["stand"] = "fertig"
            print(f"    OK — {begruendung}")
            eskalieren(auftrag, "Ergebnis liegt vor",
                       _bericht(auftrag, ergebnis, begruendung), config)
            eskalationen += 1
        elif auftrag["versuche"] >= MAX_NACHARBEIT:
            auftrag["stand"] = "gescheitert"
            print(f"    Zweimal erfolglos — eskaliert.")
            eskalieren(auftrag, "Zweimal Nacharbeit erfolglos",
                       _bericht(auftrag, ergebnis, begruendung), config)
            eskalationen += 1
        else:
            auftrag["stand"] = "nacharbeit"
            print(f"    Nacharbeit — {begruendung}")

    if probelauf:
        print("\n[Probelauf] Beendet. Nichts veraendert, nichts verschickt.")
        return

    _fristen_pruefen(daten, config)
    daten["letzter_lauf"] = _jetzt()
    zustand_speichern(daten)

    if eskalationen == 0:
        print("\nKeine Eskalation. Es bleibt still.")
    _wochenbericht_faellig(daten, config)


def _fristen_pruefen(daten: dict, config: dict) -> None:
    heute = date.today().isoformat()
    for auftrag in daten["auftraege"]:
        if (auftrag["stand"] in ("offen", "nacharbeit")
                and auftrag["frist"] < heute and not auftrag.get("frist_gemeldet")):
            auftrag["frist_gemeldet"] = True
            eskalieren(auftrag, "Frist ueberschritten",
                       f"Auftrag: {auftrag['ziel']}\nFrist war: {auftrag['frist']}\n"
                       f"Stand: {auftrag['stand']}, Versuche: {auftrag['versuche']}",
                       config)


def _bericht(auftrag: dict, ergebnis: dict, begruendung: str) -> str:
    zeilen = [
        f"Auftrag:   {auftrag['id']}",
        f"Abteilung: {auftrag['abteilung']}",
        f"Ziel:      {auftrag['ziel']}",
        f"Pruefung:  {begruendung}",
        "",
        "KRITERIEN:",
    ]
    for kriterium, ok in zip(auftrag["kriterien"], ergebnis.get("kriterien_erfuellt", [])):
        zeilen.append(f"  [{'x' if ok else ' '}] {kriterium}")
    zeilen += ["", "ERGEBNIS:", ergebnis.get("ergebnis", "")]
    if ergebnis.get("anmerkung"):
        zeilen += ["", "ANMERKUNG:", str(ergebnis["anmerkung"])]
    if ergebnis.get("zeichnung"):
        zeilen += ["", f"ZEICHNUNG: {ergebnis['zeichnung']}"]
    return "\n".join(zeilen)


def _wochenbericht_faellig(daten: dict, config: dict) -> None:
    letzter = daten.get("letzter_wochenbericht")
    if letzter and (datetime.now() - datetime.fromisoformat(letzter)).days < 7:
        return
    if not daten["auftraege"]:
        return
    senden("[Bello] Wochenuebersicht", wochenbericht_text(daten), config)
    daten["letzter_wochenbericht"] = _jetzt()
    zustand_speichern(daten)


def wochenbericht_text(daten: dict | None = None) -> str:
    daten = daten or zustand_laden()
    zaehler: dict[str, int] = {}
    for auftrag in daten["auftraege"]:
        zaehler[auftrag["stand"]] = zaehler.get(auftrag["stand"], 0) + 1
    zeilen = ["Wochenuebersicht KI-Betrieb", ""]
    zeilen += [f"  {stand}: {anzahl}" for stand, anzahl in sorted(zaehler.items())]
    wartend = [a for a in daten["auftraege"] if a["stand"] == "wartet auf Bjoern"]
    if wartend:
        zeilen += ["", "Wartet auf deine Entscheidung:"]
        zeilen += [f"  ! {a['id']} {a['abteilung']}: {a['ziel']}" for a in wartend]
    return "\n".join(zeilen)


# ---------- Anzeige ----------

def stand_zeigen() -> None:
    daten = zustand_laden()
    if not daten["auftraege"]:
        print("Keine Auftraege angelegt.")
        return
    print(f"Letzter Lauf: {daten.get('letzter_lauf') or 'nie'}\n")
    for auftrag in daten["auftraege"]:
        marke = "!" if auftrag["stand"] == "wartet auf Bjoern" else " "
        print(f"{marke} {auftrag['id']}  {auftrag['stand']:<20} "
              f"{auftrag['abteilung']:<22} {auftrag['ziel'][:50]}")
    print("\nEin ! heisst: wartet auf Bjoerns Entscheidung.")


def _jetzt() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ---------- Einstieg ----------

def main() -> None:
    argumente = sys.argv[1:]
    if "--stand" in argumente:
        stand_zeigen()
    elif "--wochenbericht" in argumente:
        print(wochenbericht_text())
    elif "--auftrag" in argumente:
        rest = argumente[argumente.index("--auftrag") + 1:]
        if len(rest) < 2:
            print('Aufruf: orchestrator.py --auftrag "01 Innovation" "Ziel" [JJJJ-MM-TT]')
            sys.exit(1)
        auftrag_anlegen(rest[0], rest[1], rest[2] if len(rest) > 2 else None)
    else:
        lauf(probelauf="--probelauf" in argumente)


if __name__ == "__main__":
    main()
