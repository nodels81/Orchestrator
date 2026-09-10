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
  orchestrator.py --gedaechtnis                     Was der Betrieb weiss und was das spart
  orchestrator.py --wissen "Wenzhou Vigorous"       Im Gedaechtnis nachschlagen
  orchestrator.py --vergessen [Tage]                Alte Episoden wegraeumen (Standard 180)
"""

import json
import os
import sys
from datetime import date, datetime, timedelta

import gedaechtnis
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
    zeilen += ["", _gedaechtnis_zeile()]
    return "\n".join(zeilen)


def _gedaechtnis_zeile() -> str:
    """Eine Zeile Gedaechtnis fuer die Wochenuebersicht. Faellt sie aus, faellt nur sie aus."""
    try:
        with gedaechtnis.Gedaechtnis() as g:
            s = g.statistik()
    except Exception as fehler:
        return f"Gedaechtnis: nicht lesbar ({fehler})."
    return (f"Gedaechtnis: {s['episoden']} Episoden, {s['fakten_aktuell']} gueltige Fakten, "
            f"{s['gespart_gesamt']} Tokens gespart.")


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


def wissen_zeigen(suchbegriff: str) -> None:
    with gedaechtnis.Gedaechtnis() as g:
        treffer = g.suchen(suchbegriff)
    if not treffer["fakten"] and not treffer["episoden"]:
        print(f"Nichts zu '{suchbegriff}' im Gedaechtnis.")
        return
    if treffer["fakten"]:
        print("FAKTEN:")
        for f in treffer["fakten"]:
            stand = "gilt" if f["gueltig_bis"] is None else f"abgeloest {f['gueltig_bis'][:10]}"
            print(f"  [{stand}] {f['aussage']}  (seit {(f['gueltig_ab'] or '')[:10]}, "
                  f"{f['quelle'] or 'ohne Quelle'})")
    if treffer["episoden"]:
        print("\nFRUEHERE AUFTRAEGE:")
        for e in treffer["episoden"]:
            print(f"  {e['auftrag_id']} {(e['zeit'] or '')[:10]} {e['abteilung']}: {e['ziel'][:60]}")
            print(f"     {e['zusammenfassung']}")


def _jetzt() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ---------- Einstieg ----------

def main() -> None:
    argumente = sys.argv[1:]
    if "--stand" in argumente:
        stand_zeigen()
    elif "--gedaechtnis" in argumente:
        print(gedaechtnis.bericht())
    elif "--wissen" in argumente:
        rest = argumente[argumente.index("--wissen") + 1:]
        if not rest:
            print('Aufruf: orchestrator.py --wissen "Suchbegriff"')
            sys.exit(1)
        wissen_zeigen(" ".join(rest))
    elif "--vergessen" in argumente:
        rest = argumente[argumente.index("--vergessen") + 1:]
        tage = int(rest[0]) if rest and rest[0].isdigit() else 180
        with gedaechtnis.Gedaechtnis() as g:
            geloescht = g.vergessen(tage)
        print(f"{geloescht} Episoden aelter als {tage} Tage weggeraeumt. Fakten bleiben.")
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
