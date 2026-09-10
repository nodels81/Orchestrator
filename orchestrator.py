"""
orchestrator.py — Steuerung: verteilt Auftraege, prueft Ergebnisse, eskaliert.

Grundprinzip: Schweigen ist der Normalzustand. Er meldet sich nur, wenn er ohne
Bjoern nicht weiterkommt. Alles andere sammelt er fuer die Wochenuebersicht.

Aufrufe:
  orchestrator.py                                   Lauf sofort ausloesen
  orchestrator.py --probelauf                       Trockenlauf, keine API-Kosten
  orchestrator.py --stand                           Woran wird gearbeitet
  orchestrator.py --auftrag "01 Innovation" "Ziel" [Frist]   (auch "01" oder "Merle")
  orchestrator.py --freigeben A-2026-006 ["Kommentar"]       Ergebnis annehmen
  orchestrator.py --ablehnen  A-2026-006 "was ueberarbeitet werden soll"
  orchestrator.py --wochenbericht
  orchestrator.py --hilfe
"""

import json
import os
import sys
from datetime import date, datetime, timedelta

from abteilung_basis import BASIS, DATEN, config_laden
from orchestrator_mail import senden
import namen

ZUSTAND = os.path.join(DATEN, "auftraege.json")
MAX_NACHARBEIT = 2

ABTEILUNGEN = {
    "01 Innovation": ("abteilung_innovation", "Innovation"),
    "02 Produkt & Ausführung": ("abteilung_ausfuehrung", "Ausfuehrung"),
    "03 Vertrieb": ("abteilung_vertrieb", "Vertrieb"),
    "04 Social Media": ("abteilung_social", "Social"),
    "05 Personal": ("abteilung_personal", "Personal"),
    "06 Einkauf": ("abteilung_einkauf", "Einkauf"),
    "07 Einkauf China": ("abteilung_einkauf_china", "EinkaufChina"),
    "08 Design": ("abteilung_design", "Design"),
    "09 Qualität": ("abteilung_qualitaet", "Qualitaet"),
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

def abteilung_aufloesen(eingabe: str) -> str:
    """Nimmt den langen Schluessel ('07 Einkauf China'), die Nummer ('07'),
    den Vornamen ('Henrik') oder ein eindeutiges Wortstueck und liefert den
    kanonischen Schluessel aus ABTEILUNGEN. Sonst ValueError mit Liste."""
    e = (eingabe or "").strip()
    if e in ABTEILUNGEN:
        return e
    ekl = e.lower()
    # nach Nummer
    for schluessel in ABTEILUNGEN:
        if schluessel[:2] == e.zfill(2) or schluessel.split(" ", 1)[0] == e:
            return schluessel
    # nach Vorname
    for nr, vn in namen.VORNAMEN.items():
        if vn.lower() == ekl:
            for schluessel in ABTEILUNGEN:
                if schluessel.startswith(nr + " "):
                    return schluessel
    # eindeutiges Wortstueck im langen Namen
    treffer = [s for s in ABTEILUNGEN if ekl and ekl in s.lower()]
    if len(treffer) == 1:
        return treffer[0]
    moeglich = ", ".join(f"{s} ({namen.vorname(s)})" for s in ABTEILUNGEN)
    raise ValueError(f"Abteilung '{eingabe}' nicht eindeutig. Moeglich: {moeglich}")


def auftrag_anlegen(abteilung: str, ziel: str, frist: str | None = None,
                    kriterien: list[str] | None = None) -> dict:
    abteilung = abteilung_aufloesen(abteilung)
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
    vn = namen.vorname(abteilung)
    wer = f"{abteilung} ({vn})" if vn else abteilung
    print(f"Auftrag {auftrag['id']} an {wer} angelegt, Frist {auftrag['frist']}.")
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


def _qm_pruefung(auftrag: dict, ergebnis: dict, config: dict) -> str | None:
    """Optionaler Zwischenschritt: Almut (09) prueft das Ergebnis, bevor es zu Bjoern geht.
    Aktiv nur fuer Abteilungen in config['qm_gate']."""
    gate = config.get("qm_gate") or []
    abt = auftrag.get("abteilung", "")
    if abt not in gate or abt.startswith("09"):
        return None
    try:
        qm_auftrag = {
            "id": auftrag["id"], "abteilung": "09 Qualität",
            "ziel": (f"Pruefe dieses Ergebnis von {abt} zu Auftrag {auftrag['id']}.\n\n"
                     f"--- ZU PRUEFEN ---\n{ergebnis.get('ergebnis', '')}"
                     + (f"\n\nANMERKUNG der Abteilung: {ergebnis['anmerkung']}"
                        if ergebnis.get("anmerkung") else "")),
            "kriterien": ["Pruefung ist konkret und vollstaendig",
                          "Nachbesserungspunkte sind umsetzbar benannt",
                          "Pruefbuch-Eintrag vorhanden"],
            "frist": date.today().isoformat(), "rahmen": "keine Ausgaben",
        }
        qe = abteilung_laden("09 Qualität").bearbeiten(qm_auftrag)
        return qe.get("ergebnis") or None
    except Exception as fehler:
        print(f"    [QM] Zwischenpruefung uebersprungen: {fehler}")
        return None


def _zeichnungen(ergebnis: dict) -> list[str]:
    pfade = list(ergebnis.get("zeichnungen") or [])
    if ergebnis.get("zeichnung"):
        pfade.append(ergebnis["zeichnung"])
    return [p for p in pfade if p]


def eskalieren(auftrag: dict, grund: str, text: str, config: dict,
               anhaenge: list[str] | None = None) -> None:
    auftrag["eskaliert"] = True
    auftrag["stand"] = "wartet auf Bjoern"
    betreff = f"[Bello] {auftrag['id']} {auftrag['abteilung']} — {grund}"
    vn = namen.vorname(auftrag.get("abteilung", ""))
    fuss = f"\n\n— {namen.ORCHESTRATOR} (Orchestrator)"
    if vn:
        fuss = f"\n\nBearbeitet von {vn}.{fuss}"
    senden(betreff, text + fuss, config, anhaenge=anhaenge)


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
        zeichnungen = _zeichnungen(ergebnis)
        auftrag["verlauf"].append({
            "zeit": _jetzt(),
            "versuch": auftrag["versuche"],
            "bestanden": bestanden,
            "begruendung": begruendung,
            "ergebnis": ergebnis.get("ergebnis", "")[:12000],
            "anmerkung": ergebnis.get("anmerkung"),
            "zeichnungen": zeichnungen or None,
        })

        if bestanden:
            auftrag["stand"] = "fertig"
            print(f"    OK — {begruendung}")
            bericht = _bericht(auftrag, ergebnis, begruendung)
            qm = _qm_pruefung(auftrag, ergebnis, config)
            if qm:
                bericht += "\n\n" + "=" * 40 + "\nQUALITAETSPRUEFUNG (Almut, 09):\n" + qm
            # Ergebnisse werden nach aussen sichtbar -> immer Bjoerns Freigabe
            eskalieren(auftrag, "Ergebnis liegt vor", bericht, config, anhaenge=zeichnungen)
            eskalationen += 1
        elif auftrag["versuche"] >= MAX_NACHARBEIT:
            auftrag["stand"] = "gescheitert"
            print(f"    Zweimal erfolglos — eskaliert.")
            eskalieren(auftrag, "Zweimal Nacharbeit erfolglos",
                       _bericht(auftrag, ergebnis, begruendung), config,
                       anhaenge=zeichnungen)
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
    if ergebnis.get("zeichnungen"):
        zeilen += ["", "ZEICHNUNGEN:"]
        zeilen += [f"  {p}" for p in ergebnis["zeichnungen"]]
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
    zeilen += ["", f"— {namen.ORCHESTRATOR} (Orchestrator)"]
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


# ---------- Freigabe / Ablehnung ----------

def _auftrag_finden(daten: dict, auftrag_id: str) -> dict | None:
    return next((a for a in daten["auftraege"] if a["id"] == auftrag_id), None)


def freigeben(auftrag_id: str, kommentar: str = "") -> None:
    daten = zustand_laden()
    a = _auftrag_finden(daten, auftrag_id)
    if not a:
        print(f"Auftrag {auftrag_id} nicht gefunden."); sys.exit(1)
    a["stand"] = "freigegeben"
    a["verlauf"].append({"zeit": _jetzt(), "entscheidung": "freigegeben",
                         "kommentar": kommentar or None})
    zustand_speichern(daten)
    print(f"{auftrag_id} freigegeben." + (f" ({kommentar})" if kommentar else ""))


def ablehnen(auftrag_id: str, kommentar: str) -> None:
    daten = zustand_laden()
    a = _auftrag_finden(daten, auftrag_id)
    if not a:
        print(f"Auftrag {auftrag_id} nicht gefunden."); sys.exit(1)
    a["stand"] = "abgelehnt"
    a["verlauf"].append({"zeit": _jetzt(), "entscheidung": "abgelehnt",
                         "kommentar": kommentar})
    zustand_speichern(daten)
    print(f"{auftrag_id} abgelehnt.")
    # Ueberarbeitungs-Auftrag an dieselbe Abteilung
    neu = auftrag_anlegen(
        a["abteilung"],
        f"Ueberarbeitung zu {auftrag_id}. Bjoerns Rueckmeldung: {kommentar}\n\n"
        f"Urspruengliches Ziel war: {a['ziel']}",
        (date.today() + timedelta(days=7)).isoformat(),
    )
    print(f"Ueberarbeitung als {neu['id']} angelegt.")


# ---------- Einstieg ----------

def main() -> None:
    argumente = sys.argv[1:]
    if "--hilfe" in argumente or "--help" in argumente or "-h" in argumente:
        print(__doc__.strip())
    elif "--stand" in argumente:
        stand_zeigen()
    elif "--wochenbericht" in argumente:
        print(wochenbericht_text())
    elif "--auftrag" in argumente:
        rest = argumente[argumente.index("--auftrag") + 1:]
        if len(rest) < 2:
            print('Aufruf: orchestrator.py --auftrag "07 Einkauf China" "Ziel" [JJJJ-MM-TT]')
            print('        (statt "07 Einkauf China" gehen auch "07" oder "Henrik")')
            sys.exit(1)
        try:
            auftrag_anlegen(rest[0], rest[1], rest[2] if len(rest) > 2 else None)
        except ValueError as fehler:
            print(fehler)
            sys.exit(1)
    elif "--freigeben" in argumente:
        rest = argumente[argumente.index("--freigeben") + 1:]
        if not rest:
            print('Aufruf: orchestrator.py --freigeben A-2026-006 ["Kommentar"]'); sys.exit(1)
        freigeben(rest[0], rest[1] if len(rest) > 1 else "")
    elif "--ablehnen" in argumente:
        rest = argumente[argumente.index("--ablehnen") + 1:]
        if len(rest) < 2:
            print('Aufruf: orchestrator.py --ablehnen A-2026-006 "was ueberarbeitet werden soll"'); sys.exit(1)
        ablehnen(rest[0], rest[1])
    else:
        lauf(probelauf="--probelauf" in argumente)


if __name__ == "__main__":
    main()
