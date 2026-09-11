"""
tagesbrief.py — Die Morgenmail um 07:00.

Grund: Der Orchestrator schweigt von sich aus. Er meldet sich nur, wenn ein
Auftrag fertig ist, scheitert oder eine Frist reisst. Offene Entscheidungen
erreichen Bjoern damit hoechstens einmal und danach nie wieder. Der Tagesbrief
schliesst diese Luecke: ein Mal am Tag, immer, auch wenn nichts offen ist.

Aufrufe:
  tagesbrief.py            Text ausgeben, nichts senden
  tagesbrief.py --senden   Senden, hoechstens einmal pro Tag
  tagesbrief.py --erzwingen --senden   Auch senden, wenn heute schon einer raus ist
"""

import json
import os
import re
import sys
from datetime import date, datetime, timedelta

from abteilung_basis import BASIS, config_laden
from orchestrator_mail import senden

ZUSTAND = os.path.join(BASIS, "auftraege.json")
REGISTER = os.path.join(BASIS, "entscheidungen", "offen.md")


# ---------- Quellen ----------

def zustand_laden() -> dict:
    if not os.path.exists(ZUSTAND):
        return {"auftraege": [], "letzter_lauf": None}
    with open(ZUSTAND, encoding="utf-8") as f:
        return json.load(f)


def zustand_speichern(daten: dict) -> None:
    temp = ZUSTAND + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2, ensure_ascii=False)
    os.replace(temp, ZUSTAND)


def register_lesen() -> list[tuple[str, str]]:
    """Liest entscheidungen/offen.md.

    Format, bewusst von Hand pflegbar:
      ## Abteilung oder Thema
      - [ ] Offene Frage
      - [x] Erledigte Frage (wird nicht mehr gemeldet)
    """
    if not os.path.exists(REGISTER):
        return []
    thema = "Ohne Zuordnung"
    offen: list[tuple[str, str]] = []
    for zeile in open(REGISTER, encoding="utf-8"):
        zeile = zeile.rstrip()
        if zeile.startswith("## "):
            thema = zeile[3:].strip()
        elif re.match(r"^\s*-\s*\[ \]\s+", zeile):
            offen.append((thema, re.sub(r"^\s*-\s*\[ \]\s+", "", zeile)))
    return offen


# ---------- Text ----------

def text_bauen(daten: dict | None = None, heute: date | None = None) -> str:
    daten = zustand_laden() if daten is None else daten
    heute = heute or date.today()
    auftraege = daten.get("auftraege", [])

    zeilen = [
        f"Tagesbrief {heute.strftime('%d.%m.%Y')} — Bellowerk KI-Betrieb",
        "=" * 52,
        "",
    ]

    wartend = [a for a in auftraege if a.get("stand") == "wartet auf Bjoern"]
    ueberfaellig = [
        a for a in auftraege
        if a.get("stand") in ("offen", "nacharbeit") and a.get("frist", "9999") < heute.isoformat()
    ]
    bald = [
        a for a in auftraege
        if a.get("stand") in ("offen", "nacharbeit")
        and heute.isoformat() <= a.get("frist", "9999") <= (heute + timedelta(days=3)).isoformat()
    ]
    laufend = [a for a in auftraege if a.get("stand") in ("offen", "nacharbeit")]
    gestern = [
        a for a in auftraege
        if a.get("stand") == "fertig"
        and any(str(v.get("zeit", "")).startswith((heute - timedelta(days=1)).isoformat())
                for v in a.get("verlauf", []))
    ]
    register = register_lesen()

    # 1. Was eine Entscheidung braucht
    zeilen += ["1. WARTET AUF DICH", "-" * 52]
    if wartend or register:
        for a in wartend:
            zeilen.append(f"  ! {a['id']}  {a['abteilung']}")
            zeilen.append(f"      {a['ziel']}")
        if wartend and register:
            zeilen.append("")
        thema_zuletzt = None
        for thema, frage in register:
            if thema != thema_zuletzt:
                zeilen.append(f"  {thema}:")
                thema_zuletzt = thema
            zeilen.append(f"      - {frage}")
    else:
        zeilen.append("  Nichts. Keine Entscheidung offen.")
    zeilen.append("")

    # 2. Fristen
    zeilen += ["2. FRISTEN", "-" * 52]
    if ueberfaellig or bald:
        for a in ueberfaellig:
            zeilen.append(f"  UEBERFAELLIG seit {a['frist']}  {a['id']} {a['abteilung']}: {a['ziel'][:60]}")
        for a in bald:
            zeilen.append(f"  faellig {a['frist']}  {a['id']} {a['abteilung']}: {a['ziel'][:60]}")
    else:
        zeilen.append("  Keine Frist in den naechsten drei Tagen.")
    zeilen.append("")

    # 3. Gestern fertig geworden
    zeilen += ["3. GESTERN FERTIG", "-" * 52]
    if gestern:
        for a in gestern:
            zeilen.append(f"  {a['id']}  {a['abteilung']}: {a['ziel'][:70]}")
    else:
        zeilen.append("  Nichts fertig geworden.")
    zeilen.append("")

    # 4. Betrieb
    zeilen += ["4. BETRIEB", "-" * 52]
    letzter = daten.get("letzter_lauf")
    zeilen.append(f"  Letzter Lauf: {letzter or 'nie'}")
    if letzter:
        try:
            alter = datetime.now() - datetime.fromisoformat(letzter)
            if alter > timedelta(hours=26):
                zeilen.append(f"  ACHTUNG: Der letzte Lauf ist {alter.days} Tage her. Laeuft der Cron noch?")
        except ValueError:
            pass
    else:
        zeilen.append("  ACHTUNG: Es gab noch nie einen Lauf. Cron pruefen.")
    zeilen.append(f"  Auftraege insgesamt: {len(auftraege)} · in Arbeit: {len(laufend)} · wartend: {len(wartend)}")
    zeilen += ["", "Stand: " + datetime.now().strftime("%d.%m.%Y %H:%M")]
    return "\n".join(zeilen)


# ---------- Versand ----------

def heute_schon_gesendet(daten: dict, heute: date) -> bool:
    return str(daten.get("letzter_tagesbrief", ""))[:10] == heute.isoformat()


def tagesbrief_senden(erzwingen: bool = False) -> bool:
    heute = date.today()
    daten = zustand_laden()
    if not erzwingen and heute_schon_gesendet(daten, heute):
        print("[TAGESBRIEF] Heute bereits gesendet. Nichts getan.")
        return False

    text = text_bauen(daten, heute)
    wartend = sum(1 for a in daten.get("auftraege", []) if a.get("stand") == "wartet auf Bjoern")
    offen = len(register_lesen())
    if wartend or offen:
        betreff = f"[Bello] Tagesbrief {heute.strftime('%d.%m.')} — {wartend + offen} offen"
    else:
        betreff = f"[Bello] Tagesbrief {heute.strftime('%d.%m.')} — nichts offen"

    erfolg = senden(betreff, text, config_laden())
    if erfolg:
        daten["letzter_tagesbrief"] = datetime.now().isoformat(timespec="seconds")
        zustand_speichern(daten)
    return erfolg


def main() -> None:
    argumente = sys.argv[1:]
    if "--senden" in argumente:
        erfolg = tagesbrief_senden(erzwingen="--erzwingen" in argumente)
        sys.exit(0 if erfolg else 1)
    print(text_bauen())


if __name__ == "__main__":
    main()
