#!/usr/bin/env python3
"""dienst.py — der schmale Dienst hinter der Betriebs-App.

Er kann genau drei Dinge und nicht mehr: den Stand lesen, einen Auftrag anlegen,
eine Entscheidung eintragen. Je weniger er kann, desto weniger kann schiefgehen.

Grundsatz: Ein Auftrag aus der App ist ein ganz gewoehnlicher Auftrag. Deshalb
ruft dieser Dienst dieselben Funktionen wie die Kommandozeile auf, statt sie
nachzubauen — gleiche Nummer, gleiches Register, gleiche Pruefung durch Almut,
gleiche Mail von Gustav. Es gibt keinen zweiten Weg an Gustav vorbei.

Er lauscht nur auf 127.0.0.1. Nach aussen kommt man ausschliesslich ueber nginx,
und das verlangt das Passwort. Der API-Schluessel bleibt hier und taucht nie im
Browser auf.

Aufrufe:
  dienst.py                 lauscht auf 127.0.0.1:8787
  dienst.py --port 9000     anderer Port
  dienst.py --probe         prueft nur, ob alles importierbar ist, und endet
"""

import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, "/opt/bello")

import namen
import orchestrator

PORT = 8787
MAX_KOERPER = 16 * 1024          # mehr als das ist kein Formular, sondern ein Angriff
MAX_ZIEL = 2000
MAX_KOMMENTAR = 1000
ID_MUSTER = re.compile(r"^A-\d{4}-\d{3}$")
DATUM_MUSTER = re.compile(r"^\d{4}-\d{2}-\d{2}$")

ENTSCHEIDUNGEN = {
    "freigeben": orchestrator.freigeben,
    "verwerfen": orchestrator.verwerfen,
    "ablehnen": orchestrator.ablehnen,
}


# ---------------------------------------------------------------- Hilfen

class Wert(Exception):
    """Eingabe des Nutzers war unbrauchbar — wird zu 400, nicht zu 500."""


def abteilungen() -> list[dict]:
    """Die Liste, aus der das Formular waehlen darf — nichts sonst wird angenommen."""
    raus = []
    for lang in orchestrator.ABTEILUNGEN:
        nr = lang[:2]
        raus.append({"nummer": nr, "lang": lang,
                     "fach": lang[3:], "name": namen.vorname(nr)})
    return raus


def stand() -> dict:
    daten = orchestrator.zustand_laden()
    auftraege = []
    for a in daten.get("auftraege", []):
        nr = str(a.get("abteilung", ""))[:2]
        auftraege.append({
            "id": a.get("id"),
            "abteilung": a.get("abteilung"),
            "name": namen.vorname(nr),
            "ziel": a.get("ziel"),
            "stand": a.get("stand"),
            "frist": a.get("frist"),
            "angelegt": a.get("angelegt"),
            # Das Ergebnis kann sehr lang sein; die Liste bekommt nur den Anfang.
            "ergebnis_kurz": (a.get("ergebnis") or "")[:600] or None,
        })
    wartend = [a for a in auftraege if a["stand"] == "wartet auf Bjoern"]
    return {
        "auftraege": auftraege,
        "wartend": len(wartend),
        "gesamt": len(auftraege),
        "in_arbeit": len([a for a in auftraege if a["stand"] == "in Arbeit"]),
        "abteilungen": abteilungen(),
        "orchestrator": namen.ORCHESTRATOR,
        "stand_vom": datetime.now().isoformat(timespec="seconds"),
    }


def auftrag_anlegen(nutzlast: dict) -> dict:
    abteilung = str(nutzlast.get("abteilung", "")).strip()
    ziel = str(nutzlast.get("ziel", "")).strip()
    frist = str(nutzlast.get("frist", "")).strip()

    if not ziel:
        raise Wert("Ohne Ziel kein Auftrag.")
    if len(ziel) > MAX_ZIEL:
        raise Wert(f"Das Ziel ist laenger als {MAX_ZIEL} Zeichen.")

    # Die Abteilung muss aus der festen Liste kommen. abteilung_aufloesen laesst
    # Nummer, Vorname und langen Namen zu und wirft sonst ValueError.
    try:
        lang = orchestrator.abteilung_aufloesen(abteilung)
    except ValueError as fehler:
        raise Wert(str(fehler))

    if frist:
        if not DATUM_MUSTER.match(frist):
            raise Wert("Die Frist muss als JJJJ-MM-TT geschrieben sein.")
        try:
            gesetzt = date.fromisoformat(frist)
        except ValueError:
            raise Wert("Die Frist ist kein gueltiges Datum.")
        if gesetzt < date.today():
            raise Wert("Die Frist liegt in der Vergangenheit.")
    else:
        frist = None

    auftrag = orchestrator.auftrag_anlegen(lang, ziel, frist)
    return {"id": auftrag["id"], "abteilung": lang,
            "name": namen.vorname(lang[:2]), "frist": auftrag["frist"]}


def entscheiden(nutzlast: dict) -> dict:
    auftrag_id = str(nutzlast.get("id", "")).strip()
    was = str(nutzlast.get("entscheidung", "")).strip()
    kommentar = str(nutzlast.get("kommentar", "")).strip()[:MAX_KOMMENTAR]

    if not ID_MUSTER.match(auftrag_id):
        raise Wert("Das ist keine Auftragsnummer.")
    if was not in ENTSCHEIDUNGEN:
        raise Wert("Moeglich sind nur freigeben, ablehnen und verwerfen.")
    if was == "ablehnen" and not kommentar:
        raise Wert("Beim Ablehnen gehoert dazu, was ueberarbeitet werden soll.")

    # Die Funktionen im Orchestrator beenden das Programm, wenn der Auftrag
    # fehlt. Fuer die Kommandozeile ist das richtig, fuer einen Dienst toedlich —
    # deshalb hier vorher nachsehen.
    daten = orchestrator.zustand_laden()
    if not orchestrator._auftrag_finden(daten, auftrag_id):
        raise Wert(f"Auftrag {auftrag_id} gibt es nicht.")

    ENTSCHEIDUNGEN[was](auftrag_id, kommentar)
    return {"id": auftrag_id, "entscheidung": was}


# ---------------------------------------------------------------- HTTP

class Griff(BaseHTTPRequestHandler):
    server_version = "bello-dienst"
    sys_version = ""

    def _senden(self, code: int, nutzlast: dict) -> None:
        roh = json.dumps(nutzlast, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(roh)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(roh)

    def _lesen(self) -> dict:
        laenge = int(self.headers.get("Content-Length") or 0)
        if laenge <= 0:
            raise Wert("Leere Anfrage.")
        if laenge > MAX_KOERPER:
            raise Wert("Anfrage zu gross.")
        try:
            return json.loads(self.rfile.read(laenge).decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            raise Wert("Anfrage war kein lesbares JSON.")

    def do_GET(self) -> None:
        if self.path.rstrip("/") == "/api/stand":
            try:
                self._senden(200, stand())
            except Exception as fehler:
                self._senden(500, {"fehler": f"Stand nicht lesbar: {fehler}"})
        else:
            self._senden(404, {"fehler": "Unbekannter Weg."})

    def do_POST(self) -> None:
        wege = {"/api/auftrag": auftrag_anlegen, "/api/entscheidung": entscheiden}
        arbeit = wege.get(self.path.rstrip("/"))
        if not arbeit:
            self._senden(404, {"fehler": "Unbekannter Weg."})
            return
        try:
            self._senden(200, arbeit(self._lesen()))
        except Wert as fehler:
            self._senden(400, {"fehler": str(fehler)})
        except Exception as fehler:
            self._senden(500, {"fehler": f"Unerwartet: {fehler}"})

    def log_message(self, muster, *args):
        # Ohne Nutzlast, damit keine Auftragstexte im Journal landen.
        sys.stderr.write("%s %s\n" % (self.address_string(), muster % args))


def main() -> None:
    port = PORT
    if "--port" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
    if "--probe" in sys.argv:
        s = stand()
        print(f"{len(s['abteilungen'])} Abteilungen, {s['gesamt']} Auftraege, "
              f"{s['wartend']} warten. Alles lesbar.")
        return
    # Nur auf 127.0.0.1: von aussen kommt man ausschliesslich ueber nginx,
    # und das verlangt das Passwort.
    ThreadingHTTPServer(("127.0.0.1", port), Griff).serve_forever()


if __name__ == "__main__":
    main()
