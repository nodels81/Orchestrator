#!/usr/bin/env python3
"""telegram_bot.py — Bjoerns Draht zu Gustav, per Telegram.

Der fuenfte Weg ins Auftragsregister, neben Kommandozeile, Mail-Antwort,
Mail-Entscheidung und App. Und wie bei allen anderen gilt: Ein Auftrag aus
Telegram ist ein ganz gewoehnlicher Auftrag. Der Bot ruft dieselben Funktionen
wie die Kommandozeile auf — gleiche Nummer, gleiches Register, gleiche Pruefung
durch Almut, gleiche Mail von Gustav. Es gibt keinen Weg an Gustav vorbei.

Was er kann, und nicht mehr:
  - Stand zeigen, Ergebnisse vorlesen, im Gedaechtnis nachschlagen
  - Auftraege anlegen: "@Henrik RFQ fuer HB-01 ..." oder Freitext, dann Knopf
  - Entscheidungen eintragen: Freigeben, Ueberarbeiten, Verwerfen
  - einen Lauf sofort anstossen — ueber eine Datei, auf die systemd achtet
    (bello-orchestrator-anstoss.path). Der Bot selbst ruft nie die Claude-API
    und startet kein Programm.

Die Ergebnisse schickt nicht er, sondern der Lauf selbst (orchestrator_telegram).
Sie kommen also auch dann aufs Handy, wenn dieser Dienst einmal steht.

Sicherheit:
  - Es zaehlen nur Nachrichten aus dem eigenen Chat der freigeschalteten Konten
    (TELEGRAM_CHAT_ID). Alles andere wird ignoriert und nur im Journal vermerkt.
  - Keine Befehle an die Shell, keine Dateien vom Handy, kein Geld.
  - Er fragt Telegram ab (Long Polling) und oeffnet keinen Port.
  - Auftragstexte landen nicht im Journal, nur Nummern und Abteilungen.

Aufrufe:
  telegram_bot.py                 laeuft als Dienst (bello-telegram.service)
  telegram_bot.py --probe         prueft die Einrichtung und endet
  telegram_bot.py --ich           prueft TELEGRAM_BOT_TOKEN aus der Umgebung
  telegram_bot.py --kennenlernen  wartet auf eine Nachricht und zeigt, wer schreibt
"""

import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import date, datetime, timedelta

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASIS)

import gedaechtnis
import namen
import orchestrator
import orchestrator_telegram as tg
from abteilung_basis import DATEN, config_laden

ZUSTAND = os.path.join(DATEN, "telegram.json")
ANSTOSS = os.path.join(DATEN, "lauf-anstossen")
WARTET = "wartet auf Bjoern"
MAX_ZIEL = 2000                        # wie in der App
RUECKFRAGE_GILT = timedelta(hours=24)  # "Wer soll das uebernehmen?", "Was soll anders werden?"
LAUF_GEDULD = timedelta(minutes=60)    # so lange wartet die Rueckmeldung auf einen Lauf
ID_MUSTER = re.compile(r"A-\d{4}-\d{3,}")
EINRICHTUNG_FEHLT = 78                 # systemd startet dann nicht endlos neu

STAND_WORT = {
    WARTET: "wartet auf dich", "nacharbeit": "in Nacharbeit", "offen": "offen",
    "gestoert": "gestört", "gescheitert": "gescheitert", "abgelehnt": "abgelehnt",
    "verworfen": "verworfen", "freigegeben": "freigegeben", "fertig": "erledigt",
}
AKTIV = [(WARTET, "Wartet auf dich"), ("nacharbeit", "In Nacharbeit"),
         ("offen", "Offen"), ("gestoert", "Gestört")]

BEFEHLE = [
    {"command": "stand", "description": "Was auf dich wartet, was offen ist"},
    {"command": "jetzt", "description": "Offenes sofort abarbeiten"},
    {"command": "ergebnis", "description": "Ein Ergebnis ganz lesen"},
    {"command": "wissen", "description": "Im Gedächtnis nachschlagen"},
    {"command": "team", "description": "Wer macht was"},
    {"command": "hilfe", "description": "Alles, was ich kann"},
]

HILFE = """Ich bin Gustav, der Orchestrator von Bellowerk.

<b>Auftrag geben</b>
Schreib einfach, was zu tun ist — ich frage, wer es übernimmt. Oder gleich mit Namen:
<code>@Henrik RFQ für HB-01 an Kingming, 100 Stück</code>

<b>Ergebnisse</b>
Kommen von selbst hierher (und wie gewohnt per Mail), mit Knöpfen zum Freigeben, Überarbeiten und Verwerfen. Antwortest du auf ein Ergebnis, kann ich deine Antwort als Überarbeitung nehmen.

<b>Befehle</b>
/stand — was auf dich wartet, was offen ist
/jetzt — Offenes sofort abarbeiten statt zur vollen Stunde
/ergebnis — ein Ergebnis ganz lesen, z. B. <code>/ergebnis A-2026-031</code>
/wissen — im Gedächtnis nachschlagen, z. B. <code>/wissen Kingming</code>
/team — wer macht was
/abbrechen — offene Rückfragen vergessen

Tipp: Das Mikrofon auf der Tastatur diktiert. Sprachnachrichten kann ich nicht hören."""


# ---------- Hilfen ----------

def _jetzt() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _zeit(text) -> datetime:
    try:
        return datetime.fromisoformat(str(text))
    except ValueError:
        return datetime.min


def _systemctl(*argumente) -> str:
    """Nur lesende Rueckfragen an systemd. Ohne systemd (Entwicklung): leer."""
    try:
        return subprocess.run(["systemctl", *argumente], capture_output=True, text=True,
                              timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def naechster_lauf() -> str:
    roh = _systemctl("show", "bello-orchestrator.timer",
                     "--property=NextElapseUSecRealtime", "--value")
    t = re.search(r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})", roh)
    if not t:
        if _systemctl("is-active", "bello-orchestrator.timer") in ("inactive", "failed"):
            return "der Zeitplan ist angehalten — nur mit /jetzt"
        return "stündlich 7–19 Uhr"
    tag, uhr = date(int(t[1]), int(t[2]), int(t[3])), f"{t[4]}:{t[5]} Uhr"
    if tag == date.today():
        return f"heute {uhr}"
    if tag == date.today() + timedelta(days=1):
        return f"morgen {uhr}"
    return f"{tag:%d.%m.} {uhr}"


def anstossen() -> None:
    """Schreibt die Datei, auf die bello-orchestrator-anstoss.path achtet.
    systemd startet daraufhin den gewoehnlichen Lauf — denselben wie der Timer."""
    with open(ANSTOSS, "w", encoding="utf-8") as f:
        f.write(_jetzt() + "\n")


def datum(text) -> str:
    try:
        return date.fromisoformat(str(text)[:10]).strftime("%d.%m.")
    except ValueError:
        return str(text or "—")


def zeitpunkt(text) -> str:
    return _zeit(text).strftime("%d.%m. %H:%M") if text else "nie"


def kurz(text, n: int = 70) -> str:
    """Eine Zeile fuer Listen."""
    zeile = " ".join(str(text or "").split())
    return zeile if len(zeile) <= n else zeile[:n - 1].rstrip() + "…"


def vorname(auftrag: dict) -> str:
    abteilung = auftrag.get("abteilung", "")
    return namen.vorname(abteilung) or abteilung


def jetzt_knopf(text: str = "▶️ Jetzt starten") -> list:
    return [[{"text": text, "callback_data": tg.JETZT}]]


def abteilungs_knoepfe(schluessel) -> list:
    """Zwei je Reihe, Name und Fach zusammen — nie nur eine Nummer."""
    knoepfe, reihe = [], []
    for s in schluessel:
        vn = namen.vorname(s[:2])
        reihe.append({"text": f"{vn} · {s[3:]}" if vn else s, "callback_data": f"an:{s[:2]}"})
        if len(reihe) == 2:
            knoepfe.append(reihe)
            reihe = []
    if reihe:
        knoepfe.append(reihe)
    return knoepfe


def adressat(text: str) -> tuple[str | None, str, list[str], str]:
    """'@Henrik RFQ ...' -> ('07 Einkauf China', 'RFQ ...', [], 'Henrik').

    Nimmt Vorname, Nummer oder Fach, auch aus bis zu drei Woertern
    ('@Einkauf China ...'). Nicht eindeutig -> (None, Rest, Kandidaten, Name)."""
    rumpf = text.strip().lstrip("@").strip()
    woerter = list(re.finditer(r"\S+", rumpf))
    if not woerter:
        return None, "", [], ""

    def rest_nach(n: int) -> str:
        return re.sub(r"^[\s:,;–-]+", "", rumpf[woerter[n - 1].end():]).strip()

    for n in (3, 2, 1):
        if len(woerter) < n:
            continue
        name = " ".join(w.group() for w in woerter[:n]).rstrip(":,;–-")
        try:
            return orchestrator.abteilung_aufloesen(name), rest_nach(n), [], name
        except ValueError:
            continue
    name = woerter[0].group().rstrip(":,;–-")
    kandidaten = [s for s in orchestrator.ABTEILUNGEN if name and name.lower() in s.lower()]
    return None, rest_nach(1), kandidaten, name


def karte(a: dict) -> tuple[str, str | None, list[str]]:
    """Ein Auftrag fuers Handy: Kopf, Ziel, letztes Ergebnis.

    Liefert den HTML-Text, den vollen Klartext (nur wenn gekuerzt werden musste)
    und die Zeichnungen des letzten Versuchs."""
    letzter = next((e for e in reversed(a.get("verlauf") or [])
                    if "ergebnis" in e or "fehler" in e), None)
    teile = [("Ziel", a.get("ziel", ""), 400)]
    if letzter and letzter.get("fehler"):
        teile.append(("Technischer Fehler", letzter["fehler"], 1200))
    elif letzter:
        titel = f"Ergebnis (Versuch {letzter.get('versuch', '?')}, {zeitpunkt(letzter.get('zeit'))})"
        teile.append((titel, tg.ohne_svg(letzter.get("ergebnis", "")), 2600))
        if letzter.get("begruendung"):
            teile.append(("Prüfung", letzter["begruendung"], 300))
        if letzter.get("anmerkung"):
            teile.append(("Anmerkung", str(letzter["anmerkung"]), 400))
    else:
        teile.append(("Ergebnis", "Noch keins — der Auftrag wartet auf den nächsten Lauf.", 200))

    kopf = (f"<b>{tg.esc(a.get('id'))} · {tg.esc(tg.wer(a.get('abteilung', '')))}</b>\n"
            f"{tg.esc(STAND_WORT.get(a.get('stand'), a.get('stand')))} · Frist {datum(a.get('frist'))}")
    stuecke, gekuerzt = [kopf], False
    for titel, inhalt, grenze in teile:
        text, geschnitten = tg.kuerzen(str(inhalt or ""), grenze)
        gekuerzt = gekuerzt or geschnitten
        stuecke.append(f"<b>{tg.esc(titel)}</b>\n{tg.esc(text)}")
    if gekuerzt:
        stuecke.append("(Vollständig in der Datei darunter.)")
    voll = None
    if gekuerzt:
        voll = f"{a.get('id')} · {tg.wer(a.get('abteilung', ''))}\n\n" + "\n\n".join(
            f"{titel.upper()}\n{inhalt}" for titel, inhalt, _ in teile)
    return "\n\n".join(stuecke), voll, list((letzter or {}).get("zeichnungen") or [])


def bis_grenze(zeilen: list[str], grenze: int = tg.GRENZE_TEXT) -> str:
    """Haengt Zeilen an, solange sie auf den Bildschirm passen."""
    raus, laenge = [], 0
    for zeile in zeilen:
        laenge += len(tg.klartext(zeile)) + 1
        if laenge > grenze:
            raus.append("…")
            break
        raus.append(zeile)
    return "\n".join(raus)


# ---------- Der Bot ----------

class Bot:
    def __init__(self, draht: tg.Draht, erlaubt, pfad: str = ZUSTAND):
        self.draht = draht
        self.erlaubt = set(erlaubt)
        self.pfad = pfad
        self.zustand = self._laden()

    # ---------- Zustand (daten/telegram.json) ----------

    def _laden(self) -> dict:
        try:
            with open(self.pfad, encoding="utf-8") as f:
                zustand = json.load(f)
        except (OSError, ValueError):
            zustand = {}
        zustand.setdefault("offset", None)
        zustand.setdefault("fragen", {})         # Nachricht "Wer soll das uebernehmen?" -> Text
        zustand.setdefault("ueberarbeiten", {})  # Nachricht "Was soll anders werden?" -> Auftrag
        zustand.setdefault("beobachten", None)   # angestossener Lauf, auf dessen Ende wir warten
        return zustand

    def _speichern(self) -> None:
        grenze = datetime.now() - RUECKFRAGE_GILT
        for fach in ("fragen", "ueberarbeiten"):
            self.zustand[fach] = {k: v for k, v in self.zustand[fach].items()
                                  if _zeit(v.get("zeit")) > grenze}
        temp = self.pfad + ".tmp"
        with open(temp, "w", encoding="utf-8") as f:
            json.dump(self.zustand, f, indent=1, ensure_ascii=False)
        os.replace(temp, self.pfad)

    # ---------- Schleife ----------

    def schleife(self) -> None:
        pause = 5
        while True:
            anfrage = {"timeout": 25, "allowed_updates": ["message", "callback_query"]}
            if self.zustand.get("offset"):
                anfrage["offset"] = self.zustand["offset"]
            try:
                updates = self.draht.rufen("getUpdates", anfrage, zeitlimit=35) or []
                pause = 5
            except tg.TelegramFehler as fehler:
                if fehler.code == 401:
                    print("[TELEGRAM] Token ungueltig (beim BotFather zurueckgezogen?). "
                          "Neu einrichten: bash bin/telegram-einrichten.sh --neu")
                    sys.exit(EINRICHTUNG_FEHLT)
                if fehler.code == 409:
                    print("[TELEGRAM] Ein zweites Programm fragt mit demselben Token ab.")
                print(f"[TELEGRAM] {fehler} — neuer Versuch in {pause} s")
                time.sleep(pause)
                pause = min(pause * 2, 60)
                continue
            for update in updates:
                # Vor dem Bearbeiten sichern: bricht es mittendrin ab, geht lieber
                # eine Nachricht verloren, als dass ein Auftrag doppelt entsteht.
                self.zustand["offset"] = update["update_id"] + 1
                self._speichern()
                self.bearbeiten(update)
            self.lauf_beobachten()

    def bearbeiten(self, update: dict) -> None:
        try:
            if "callback_query" in update:
                self._knopf(update["callback_query"])
            elif "message" in update:
                self._nachricht(update["message"])
        except (Exception, SystemExit) as fehler:
            # SystemExit auch: freigeben() & Co. beenden bei fehlendem Auftrag das
            # Programm. Fuer die Kommandozeile richtig, fuer einen Dienst toedlich.
            print(f"[TELEGRAM] Fehler bei Update {update.get('update_id')}: {tg.ohne_token(fehler)}")
            quelle = update.get("message") or (update.get("callback_query") or {}).get("message") or {}
            chat = (quelle.get("chat") or {}).get("id")
            if chat in self.erlaubt:
                try:
                    self.draht.nachricht(chat, "Da ist etwas schiefgegangen: "
                                         f"{tg.esc(kurz(tg.ohne_token(fehler), 200))}\n"
                                         "/stand zeigt, was angekommen ist.")
                except tg.TelegramFehler:
                    pass

    def _erlaubt(self, von: dict | None, chat: dict | None = None) -> bool:
        if (von or {}).get("id") not in self.erlaubt:
            return False
        return chat is None or chat.get("type") == "private"

    # ---------- Nachrichten ----------

    def _nachricht(self, msg: dict) -> None:
        chat, von = msg.get("chat") or {}, msg.get("from") or {}
        if not self._erlaubt(von, chat):
            print(f"[TELEGRAM] Nachricht von fremdem Konto {von.get('id')} ignoriert.")
            return
        cid, mid = chat["id"], msg.get("message_id")
        text = (msg.get("text") or "").strip()
        bezug_auf = (msg.get("reply_to_message") or {})
        if not text:
            self._kein_text(cid, msg)
        elif text.startswith("/"):
            self._befehl(cid, text)
        elif str(bezug_auf.get("message_id")) in self.zustand["ueberarbeiten"]:
            offen = self.zustand["ueberarbeiten"][str(bezug_auf["message_id"])]
            self._ueberarbeiten(cid, offen["id"], text)
        else:
            t = ID_MUSTER.search(bezug_auf.get("text") or "")
            bezug = t.group() if t else None
            if text.startswith("@"):
                self._auftrag_an(cid, text, mid, bezug)
            else:
                self._wer_soll(cid, text, mid, bezug=bezug)

    def _kein_text(self, cid: int, msg: dict) -> None:
        if any(k in msg for k in ("voice", "audio", "video_note")):
            text = ("Sprachnachrichten kann ich nicht abhören. Nimm das Mikrofon auf der "
                    "Tastatur — dann diktierst du, und es kommt als Text an.")
        else:
            text = ("Ich nehme nur Text an — Bilder und Dateien reiche ich nicht weiter. "
                    "Beschreib den Auftrag in Worten.")
        self.draht.nachricht(cid, text)

    def _befehl(self, cid: int, text: str) -> None:
        t = re.match(r"/(\w+)(?:@\w+)?\s*(.*)", text, re.S)
        befehl, rest = (t.group(1).lower(), t.group(2).strip()) if t else ("", "")
        wege = {
            "start": self._hilfe, "hilfe": self._hilfe, "help": self._hilfe,
            "stand": self._stand, "team": self._team, "jetzt": self._jetzt,
            "abbrechen": self._abbrechen, "auftrag": self._auftrag_befehl,
            "ergebnis": self._ergebnis, "wissen": self._wissen,
            "freigeben": self._freigeben_befehl, "verwerfen": self._verwerfen_befehl,
            "ueberarbeiten": self._ueberarbeiten_befehl,
            "überarbeiten": self._ueberarbeiten_befehl,
            "ablehnen": self._ueberarbeiten_befehl,
        }
        weg = wege.get(befehl)
        if weg:
            weg(cid, rest)
        else:
            self.draht.nachricht(cid, "Den Befehl kenne ich nicht. /hilfe zeigt, was geht.")

    def _hilfe(self, cid: int, _rest: str = "") -> None:
        self.draht.nachricht(cid, HILFE)

    def _team(self, cid: int, _rest: str = "") -> None:
        zeilen = ["<b>Die Belegschaft</b>"]
        for s in orchestrator.ABTEILUNGEN:
            zeilen.append(f"{s[:2]} <b>{tg.esc(namen.vorname(s[:2]))}</b> — {tg.esc(s[3:])}")
        zeilen += ["", f"Dahinter {namen.ORCHESTRATOR}, der verteilt, prüft und dir schreibt.",
                   "Ansprechen mit <code>@Vorname</code>, z. B. "
                   "<code>@Thea Drei Formentwürfe Halsband</code>"]
        self.draht.nachricht(cid, "\n".join(zeilen))

    def _stand(self, cid: int, _rest: str = "") -> None:
        daten = orchestrator.zustand_laden()
        auftraege = daten.get("auftraege", [])
        zeilen = [f"<b>Stand</b> · letzter Lauf {zeitpunkt(daten.get('letzter_lauf'))}"]
        knoepfe = []
        for stand, titel in AKTIV:
            liste = [a for a in auftraege if a.get("stand") == stand]
            if not liste:
                continue
            zeilen += ["", f"<b>{titel} ({len(liste)})</b>"]
            if len(liste) > 10:
                zeilen.append(f"… {len(liste) - 10} ältere, dann:")
            zeilen += [f"{tg.esc(a['id'])} · {tg.esc(vorname(a))} — {tg.esc(kurz(a.get('ziel')))}"
                       for a in liste[-10:]]
            if stand == WARTET:
                knoepfe += [[{"text": f"{a['id']} · {vorname(a)} ansehen",
                              "callback_data": f"{tg.ZEIGEN}:{a['id']}"}] for a in liste[-8:]]
        erledigt = Counter(a.get("stand") for a in auftraege
                           if a.get("stand") not in dict(AKTIV))
        if erledigt:
            zeilen += ["", "Erledigt: " + ", ".join(
                f"{STAND_WORT.get(s, s)} {n}" for s, n in sorted(erledigt.items()))]
        if not auftraege:
            zeilen += ["", "Noch keine Aufträge im Register."]
        if any(a.get("stand") in ("offen", "nacharbeit") for a in auftraege):
            zeilen += ["", f"Nächster Lauf: {naechster_lauf()}"]
            knoepfe += jetzt_knopf()
        self.draht.nachricht(cid, bis_grenze(zeilen), knoepfe or None)

    def _ergebnis(self, cid: int, rest: str) -> None:
        t = ID_MUSTER.search(rest.upper())
        if t:
            self._karte(cid, t.group())
            return
        auftraege = orchestrator.zustand_laden().get("auftraege", [])
        auswahl = ([a for a in auftraege if a.get("stand") == WARTET]
                   or [a for a in auftraege if tg.hat_ergebnis(a)])
        if not auswahl:
            self.draht.nachricht(cid, "Es liegt noch kein Ergebnis vor.")
            return
        knoepfe = [[{"text": f"{a['id']} · {vorname(a)} — {kurz(a.get('ziel'), 28)}",
                     "callback_data": f"{tg.ZEIGEN}:{a['id']}"}] for a in auswahl[-8:]]
        self.draht.nachricht(cid, "Welches Ergebnis? Oder gleich: <code>/ergebnis A-2026-031</code>",
                             knoepfe)

    def _karte(self, cid: int, auftrag_id: str) -> None:
        a = self._finden(auftrag_id)
        if not a:
            self.draht.nachricht(cid, f"{tg.esc(auftrag_id)} gibt es nicht.")
            return
        text, voll, bilder = karte(a)
        knoepfe = tg.entscheidungs_knoepfe(a) if a.get("stand") == WARTET else None
        self.draht.nachricht(cid, text, knoepfe)
        if voll:
            self.draht.datei(cid, f"{a['id']}.txt", voll.encode("utf-8"))
        tg.bilder_senden(self.draht, cid, bilder)

    def _wissen(self, cid: int, begriff: str) -> None:
        if not begriff:
            self.draht.nachricht(cid, "Wonach soll ich suchen? Zum Beispiel <code>/wissen Kingming</code>")
            return
        try:
            with gedaechtnis.Gedaechtnis() as g:
                treffer = g.suchen(begriff)
        except Exception as fehler:
            self.draht.nachricht(cid, f"Das Gedächtnis ist gerade nicht lesbar ({tg.esc(kurz(fehler, 120))}).")
            return
        if not treffer["fakten"] and not treffer["episoden"]:
            self.draht.nachricht(cid, f"Nichts zu «{tg.esc(begriff)}» im Gedächtnis.")
            return
        zeilen = []
        if treffer["fakten"]:
            zeilen.append("<b>Fakten</b>")
            for f in treffer["fakten"]:
                stand = "gilt" if f["gueltig_bis"] is None else f"abgelöst {datum(f['gueltig_bis'])}"
                quelle = f", {tg.esc(f['quelle'])}" if f["quelle"] else ""
                zeilen.append(f"• {tg.esc(f['aussage'])} <i>({stand}, seit "
                              f"{datum(f['gueltig_ab'])}{quelle})</i>")
        if treffer["episoden"]:
            zeilen += ["", "<b>Frühere Aufträge</b>"]
            for e in treffer["episoden"]:
                wer_war = namen.vorname(e["abteilung"] or "") or e["abteilung"]
                zeilen.append(f"• {tg.esc(e['auftrag_id'])} · {tg.esc(wer_war)}, {datum(e['zeit'])}: "
                              f"{tg.esc(kurz(e['ziel'], 60))}\n  {tg.esc(kurz(e['zusammenfassung'], 220))}")
        self.draht.nachricht(cid, bis_grenze(zeilen))

    def _abbrechen(self, cid: int, _rest: str = "") -> None:
        offen = [k for fach in ("fragen", "ueberarbeiten")
                 for k, v in self.zustand[fach].items() if v.get("chat") == cid]
        for fach in ("fragen", "ueberarbeiten"):
            for k in offen:
                self.zustand[fach].pop(k, None)
        for k in offen:
            self._knoepfe_weg(cid, int(k))
        self._speichern()
        self.draht.nachricht(cid, "Offene Rückfragen vergessen." if offen
                             else "Es war nichts offen.")

    # ---------- Auftraege ----------

    def _auftrag_befehl(self, cid: int, rest: str) -> None:
        if not rest:
            self.draht.nachricht(cid, "Schreib einfach, was zu tun ist — ich frage dann, wer es "
                                      "übernimmt. Oder gleich mit Namen: "
                                      "<code>@Henrik RFQ für HB-01 an Kingming</code>")
            return
        # Ohne "@" zaehlt das erste Wort nur, wenn es eindeutig eine Abteilung ist.
        # Sonst wuerde aus "/auftrag In drei Tagen ..." eine Rueckfrage zu allem,
        # was "in" im Namen traegt — und das "In" fehlte im Auftrag.
        abteilung, ziel, _, _ = adressat(rest)
        if abteilung:
            self._auftrag_an(cid, "@" + rest.lstrip("@"))
        else:
            self._wer_soll(cid, rest.lstrip("@"))

    def _auftrag_an(self, cid: int, text: str, mid: int | None = None,
                    bezug: str | None = None) -> None:
        abteilung, ziel, kandidaten, name = adressat(text)
        if not ziel:
            wen = namen.vorname(abteilung) if abteilung else name
            self.draht.nachricht(cid, f"Was soll {tg.esc(wen or 'wer')} tun? Schreib den Auftrag "
                                      f"gleich dahinter: <code>@{tg.esc(wen or 'Henrik')} …</code>")
        elif abteilung:
            self._anlegen(cid, abteilung, ziel, bezug=bezug)
        elif kandidaten:
            self._wer_soll(cid, ziel, mid, kandidaten, f"«{name}» passt auf mehrere.", bezug)
        else:
            self._wer_soll(cid, ziel, mid, hinweis=f"«{name}» kenne ich nicht.", bezug=bezug)

    def _wer_soll(self, cid: int, text: str, mid: int | None = None,
                  kandidaten: list[str] | None = None, hinweis: str = "",
                  bezug: str | None = None) -> None:
        """Fragt mit Knoepfen, an wen der Text als Auftrag geht."""
        text = text.strip()
        if len(text) > MAX_ZIEL:
            self.draht.nachricht(cid, f"Das sind {len(text)} Zeichen — höchstens {MAX_ZIEL}. "
                                      "Bitte kürzer fassen.")
            return
        knoepfe = []
        ueber = self._ueberarbeitbar(cid, bezug)
        if ueber and not kandidaten:
            knoepfe.append([{"text": f"✏️ Als Überarbeitung zu {ueber}",
                             "callback_data": f"als-ueber:{ueber}"}])
        knoepfe += abteilungs_knoepfe(kandidaten or orchestrator.ABTEILUNGEN)
        knoepfe.append([{"text": "✖️ Abbrechen", "callback_data": "weg"}])
        frage = self.draht.nachricht(cid, (f"{tg.esc(hinweis)}\n" if hinweis else "")
                                     + "Wer soll das übernehmen?", knoepfe, antwort_auf=mid)
        self.zustand["fragen"][str(frage["message_id"])] = {
            "text": text, "bezug": bezug, "chat": cid, "zeit": _jetzt()}
        self._speichern()

    def _ueberarbeitbar(self, cid: int, bezug: str | None) -> str | None:
        """Welcher Auftrag sich als Ueberarbeitung anbietet: der, auf dessen
        Ergebnis Bjoern antwortet — sonst der, zu dem zuletzt gefragt wurde."""
        if bezug:
            a = self._finden(bezug)
            if a and a.get("stand") == WARTET:
                return bezug
        offen = sorted((v for v in self.zustand["ueberarbeiten"].values() if v.get("chat") == cid),
                       key=lambda v: v.get("zeit", ""))
        return offen[-1]["id"] if offen else None

    def _anlegen(self, cid: int, abteilung: str, ziel: str, bearbeite: int | None = None,
                 bezug: str | None = None) -> None:
        ziel = ziel.strip()
        if len(ziel) > MAX_ZIEL:
            self.draht.nachricht(cid, f"Das sind {len(ziel)} Zeichen — höchstens {MAX_ZIEL}. "
                                      "Bitte kürzer fassen.")
            return
        if bezug:
            ziel += f"\n\n(Bezug: {bezug})"
        auftrag = orchestrator.auftrag_anlegen(abteilung, ziel)
        text = (f"✅ <b>{auftrag['id']}</b> an {tg.esc(tg.wer(auftrag['abteilung']))} · "
                f"Frist {datum(auftrag['frist'])}\n\n{tg.esc(tg.kuerzen(ziel, 600)[0])}\n\n"
                f"Läuft beim nächsten Lauf ({naechster_lauf()}). "
                "Das Ergebnis kommt hierher und per Mail.")
        if bearbeite:
            self.draht.text_aendern(cid, bearbeite, text, jetzt_knopf())
        else:
            self.draht.nachricht(cid, text, jetzt_knopf())

    # ---------- Knoepfe ----------

    def _knopf(self, rueckruf: dict) -> None:
        nachricht = rueckruf.get("message") or {}
        if not self._erlaubt(rueckruf.get("from"), nachricht.get("chat") or {}):
            print(f"[TELEGRAM] Knopf von fremdem Konto {(rueckruf.get('from') or {}).get('id')} ignoriert.")
            self.draht.quittieren(rueckruf["id"])
            return
        cid, mid, rid = nachricht["chat"]["id"], nachricht.get("message_id"), rueckruf["id"]
        art, _, wert = (rueckruf.get("data") or "").partition(":")
        if art == tg.FREIGEBEN:
            self._freigeben(cid, wert, mid, rid)
        elif art == tg.UEBERARBEITEN:
            self._ueberarbeiten_fragen(cid, wert, mid, rid)
        elif art == tg.VERWERFEN:
            if self._wartend(cid, wert, mid, rid):
                self.draht.quittieren(rid, "Wirklich verwerfen?")
                self.draht.knoepfe_setzen(cid, mid, [
                    [{"text": "🗑 Ja, endgültig verwerfen", "callback_data": f"{tg.VERWERFEN_JA}:{wert}"}],
                    [{"text": "↩️ Zurück", "callback_data": f"{tg.ZURUECK}:{wert}"}]])
        elif art == tg.VERWERFEN_JA:
            self._verwerfen(cid, wert, mid, rid)
        elif art == tg.ZURUECK:
            a = self._wartend(cid, wert, mid, rid)
            if a:
                self.draht.quittieren(rid)
                self.draht.knoepfe_setzen(cid, mid, tg.entscheidungs_knoepfe(a))
        elif art == tg.ZEIGEN:
            self.draht.quittieren(rid)
            self._karte(cid, wert)
        elif art == tg.JETZT:
            self.draht.quittieren(rid)
            self._jetzt(cid)
        elif art in ("an", "als-ueber", "weg"):
            self._frage_beantwortet(cid, mid, rid, art, wert)
        else:
            self.draht.quittieren(rid, "Dieser Knopf ist veraltet.")

    def _frage_beantwortet(self, cid: int, mid: int, rid: str, art: str, wert: str) -> None:
        frage = self.zustand["fragen"].pop(str(mid), None)
        if not frage:
            self.draht.quittieren(rid, "Schon erledigt oder abgelaufen — schick es bitte nochmal.")
            self._knoepfe_weg(cid, mid)
            return
        self._speichern()
        self.draht.quittieren(rid)
        if art == "weg":
            self.draht.text_aendern(cid, mid, "✖️ Nichts angelegt.")
        elif art == "als-ueber":
            self._ueberarbeiten(cid, wert, frage["text"], bearbeite=mid)
        else:
            self._anlegen(cid, orchestrator.abteilung_aufloesen(wert), frage["text"],
                          bearbeite=mid, bezug=frage.get("bezug"))

    # ---------- Entscheidungen ----------

    def _finden(self, auftrag_id: str) -> dict | None:
        return orchestrator._auftrag_finden(orchestrator.zustand_laden(), auftrag_id)

    def _wartend(self, cid: int, auftrag_id: str, mid: int | None = None,
                 rid: str | None = None) -> dict | None:
        """Entschieden wird nur, was auf Bjoern wartet. Sonst koennte ein alter
        Knopf eine laengst erledigte Sache ein zweites Mal ueberarbeiten lassen."""
        a = self._finden(auftrag_id)
        if a and a.get("stand") == WARTET:
            return a
        grund = (f"{auftrag_id} gibt es nicht." if not a else
                 f"{auftrag_id} ist schon {STAND_WORT.get(a.get('stand'), a.get('stand'))}.")
        if rid:
            self.draht.quittieren(rid, grund)
            if mid:
                self._knoepfe_weg(cid, mid)
        else:
            self.draht.nachricht(cid, tg.esc(grund))
        return None

    def _knoepfe_weg(self, cid: int, mid: int | None) -> None:
        if not mid:
            return
        try:
            self.draht.knoepfe_setzen(cid, mid, None)
        except tg.TelegramFehler:
            pass    # Nachricht geloescht oder zu alt — die Entscheidung gilt trotzdem

    def _freigeben(self, cid: int, auftrag_id: str, mid: int | None = None,
                   rid: str | None = None, kommentar: str = "per Telegram") -> None:
        if not self._wartend(cid, auftrag_id, mid, rid):
            return
        orchestrator.freigeben(auftrag_id, kommentar)
        self._knoepfe_weg(cid, mid)
        if rid:
            self.draht.quittieren(rid, "Freigegeben")
        self.draht.nachricht(cid, f"✅ {auftrag_id} ist freigegeben.", antwort_auf=mid)

    def _verwerfen(self, cid: int, auftrag_id: str, mid: int | None = None,
                   rid: str | None = None, grund: str = "per Telegram") -> None:
        if not self._wartend(cid, auftrag_id, mid, rid):
            return
        orchestrator.verwerfen(auftrag_id, grund)
        self._knoepfe_weg(cid, mid)
        if rid:
            self.draht.quittieren(rid, "Verworfen")
        self.draht.nachricht(cid, f"🗑 {auftrag_id} ist verworfen.", antwort_auf=mid)

    def _ueberarbeiten_fragen(self, cid: int, auftrag_id: str, mid: int | None = None,
                              rid: str | None = None) -> None:
        a = self._wartend(cid, auftrag_id, mid, rid)
        if not a:
            return
        if rid:
            self.draht.quittieren(rid)
        frage = self.draht.nachricht(
            cid, f"✏️ Was soll {tg.esc(vorname(a))} an {auftrag_id} ändern? "
                 "Schreib es als Antwort auf diese Nachricht.",
            erzwinge_antwort="Was soll anders werden?")
        self.zustand["ueberarbeiten"][str(frage["message_id"])] = {
            "id": auftrag_id, "karte": mid, "chat": cid, "zeit": _jetzt()}
        self._speichern()

    def _ueberarbeiten(self, cid: int, auftrag_id: str, kommentar: str,
                       bearbeite: int | None = None) -> None:
        kommentar = kommentar.strip()
        if len(kommentar) > MAX_ZIEL:
            self.draht.nachricht(cid, f"Das sind {len(kommentar)} Zeichen — höchstens {MAX_ZIEL}. "
                                      "Bitte kürzer fassen.")
            return
        karten = [v.get("karte") for k, v in self.zustand["ueberarbeiten"].items()
                  if v.get("id") == auftrag_id]
        self.zustand["ueberarbeiten"] = {k: v for k, v in self.zustand["ueberarbeiten"].items()
                                         if v.get("id") != auftrag_id}
        self._speichern()
        if not self._wartend(cid, auftrag_id):
            self._knoepfe_weg(cid, bearbeite)
            return
        neu = orchestrator.ablehnen(auftrag_id, kommentar)
        for karte_id in karten:
            self._knoepfe_weg(cid, karte_id)
        text = (f"✏️ {auftrag_id} geht zur Überarbeitung: neuer Auftrag <b>{neu['id']}</b> an "
                f"{tg.esc(tg.wer(neu['abteilung']))}.\nLäuft beim nächsten Lauf ({naechster_lauf()}).")
        if bearbeite:
            self.draht.text_aendern(cid, bearbeite, text, jetzt_knopf())
        else:
            self.draht.nachricht(cid, text, jetzt_knopf())

    def _id_und_rest(self, cid: int, rest: str, beispiel: str) -> tuple[str | None, str]:
        t = ID_MUSTER.match(rest.upper())
        if not t:
            self.draht.nachricht(cid, f"Welcher Auftrag? Zum Beispiel <code>{tg.esc(beispiel)}</code>")
            return None, ""
        return t.group(), re.sub(r"^[\s:,;–-]+", "", rest[t.end():]).strip()

    def _freigeben_befehl(self, cid: int, rest: str) -> None:
        auftrag_id, kommentar = self._id_und_rest(cid, rest, "/freigeben A-2026-031 passt so")
        if auftrag_id:
            self._freigeben(cid, auftrag_id, kommentar=kommentar or "per Telegram")

    def _verwerfen_befehl(self, cid: int, rest: str) -> None:
        auftrag_id, grund = self._id_und_rest(cid, rest, "/verwerfen A-2026-031 brauchen wir nicht")
        if auftrag_id:
            self._verwerfen(cid, auftrag_id, grund=grund or "per Telegram")

    def _ueberarbeiten_befehl(self, cid: int, rest: str) -> None:
        auftrag_id, kommentar = self._id_und_rest(
            cid, rest, "/ueberarbeiten A-2026-031 bitte mit Messingschnalle")
        if not auftrag_id:
            return
        if kommentar:
            self._ueberarbeiten(cid, auftrag_id, kommentar)
        else:
            self._ueberarbeiten_fragen(cid, auftrag_id)

    # ---------- Sofortstart ----------

    def _jetzt(self, cid: int, _rest: str = "") -> None:
        daten = orchestrator.zustand_laden()
        ids = [a["id"] for a in daten.get("auftraege", [])
               if a.get("stand") in ("offen", "nacharbeit")]
        if not ids:
            self.draht.nachricht(cid, "Gerade liegt nichts Offenes an — Gustav hat nichts zu tun.")
            return
        if _systemctl("is-active", "bello-orchestrator-anstoss.path") != "active":
            self.draht.nachricht(
                cid, "Der Sofortstart ist auf dem Server nicht eingerichtet. Die Aufträge laufen "
                     f"beim nächsten Lauf ({naechster_lauf()}).\n"
                     "Einrichten: <code>bash bin/telegram-einrichten.sh</code>")
            return
        laeuft = _systemctl("is-active", "bello-orchestrator.service") in ("active", "activating")
        if not laeuft:
            anstossen()
        wache = self.zustand.get("beobachten")
        if wache:
            wache["ids"] = sorted(set(wache["ids"]) | set(ids))
        else:
            self.zustand["beobachten"] = {"chat": cid, "seit": daten.get("letzter_lauf") or "",
                                          "zeit": _jetzt(), "ids": ids, "nachgestartet": False}
        self._speichern()
        anzahl = "1 Auftrag" if len(ids) == 1 else f"{len(ids)} Aufträge"
        if laeuft:
            text = (f"⏳ Gustav arbeitet gerade schon. Danach kommen {anzahl} dran — "
                    "ich sage Bescheid, wenn alles durch ist.")
        else:
            text = (f"▶️ Lauf ist angestoßen: {anzahl}. Die Ergebnisse kommen hierher, "
                    "meist nach wenigen Minuten.")
        self.draht.nachricht(cid, text)

    def lauf_beobachten(self) -> None:
        """Nach einem angestossenen Lauf: kurz Bescheid geben, wie es ausging.
        Lagen die Auftraege noch nicht im Register, als ein Lauf schon lief,
        wird einmal nachgestartet."""
        wache = self.zustand.get("beobachten")
        if not wache:
            return
        try:
            daten = orchestrator.zustand_laden()
            letzter = daten.get("letzter_lauf") or ""
            if letzter > (wache.get("seit") or ""):
                auftraege = {a["id"]: a for a in daten.get("auftraege", [])}
                liegen = [i for i in wache["ids"] if auftraege.get(i, {}).get("stand") == "offen"]
                if liegen and not wache.get("nachgestartet"):
                    anstossen()
                    wache.update(seit=letzter, zeit=_jetzt(), nachgestartet=True)
                    self._speichern()
                    return
                self.zustand["beobachten"] = None
                self._speichern()
                self._lauf_bericht(wache["chat"], [auftraege[i] for i in wache["ids"] if i in auftraege])
            elif datetime.now() - _zeit(wache.get("zeit")) > LAUF_GEDULD:
                self.zustand["beobachten"] = None
                self._speichern()
                self.draht.nachricht(
                    wache["chat"], "Der angestoßene Lauf hat sich nach einer Stunde nicht "
                                   "zurückgemeldet. /stand zeigt den Stand; auf dem Server: "
                                   "<code>journalctl -u bello-orchestrator -n 30</code>")
        except Exception as fehler:
            print(f"[TELEGRAM] Laufbeobachtung: {tg.ohne_token(fehler)}")

    def _lauf_bericht(self, chat: int, auftraege: list[dict]) -> None:
        zeilen, knoepfe, nochmal = ["🏁 <b>Lauf fertig</b>"], [], False
        for a in auftraege:
            stand = a.get("stand")
            wie = STAND_WORT.get(stand, stand)
            if stand == WARTET:
                knoepfe.append([{"text": f"{a['id']} · {vorname(a)} ansehen",
                                 "callback_data": f"{tg.ZEIGEN}:{a['id']}"}])
            elif stand == "nacharbeit":
                wie, nochmal = "in Nacharbeit — neuer Versuch beim nächsten Lauf", True
            elif stand == "offen":
                wie, nochmal = "noch offen", True
            zeilen.append(f"{tg.esc(a['id'])} · {tg.esc(vorname(a))} — {tg.esc(wie)}")
        if nochmal:
            knoepfe += jetzt_knopf("▶️ Nochmal anstoßen")
        self.draht.nachricht(chat, bis_grenze(zeilen), knoepfe or None)


# ---------- Einrichtung ----------

def _token_aus_umgebung() -> str:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    return "" if token.startswith("${") else token


def ich_bin() -> int:
    """Fuer das Einrichtungsskript: taugt der Token aus der Umgebung?"""
    token = _token_aus_umgebung()
    if not token:
        print("kein Token in TELEGRAM_BOT_TOKEN")
        return 2
    try:
        ich = tg.Draht(token).rufen("getMe")
    except tg.TelegramFehler as fehler:
        print(fehler)
        return EINRICHTUNG_FEHLT if fehler.code in (401, 404) else 1
    print(f"@{ich.get('username')}")
    return 0


def kennenlernen(geduld: int = 300) -> int:
    """Fuer das Einrichtungsskript: wer schreibt dem Bot?

    Hinweise gehen nach stderr, das Ergebnis als NAME=... und CHAT_ID=...
    nach stdout. Was schon vorher geschrieben wurde, zaehlt nicht."""
    token = _token_aus_umgebung()
    if not token:
        print("TELEGRAM_BOT_TOKEN fehlt in der Umgebung.", file=sys.stderr)
        return 2
    draht = tg.Draht(token)
    try:
        ich = draht.rufen("getMe")
        draht.rufen("deleteWebhook")
        alt = draht.rufen("getUpdates", {"timeout": 0}) or []
    except tg.TelegramFehler as fehler:
        print(f"Telegram: {fehler}", file=sys.stderr)
        return 1
    offset = alt[-1]["update_id"] + 1 if alt else None
    print(f"\n  Öffne jetzt Telegram auf dem Handy, such nach @{ich.get('username')}\n"
          f"  und tippe auf START (oder schreib »hallo«). Ich warte bis zu "
          f"{geduld // 60} Minuten ...\n", file=sys.stderr)
    ende = time.time() + geduld
    while time.time() < ende:
        anfrage = {"timeout": 20, "allowed_updates": ["message"]}
        if offset:
            anfrage["offset"] = offset
        try:
            updates = draht.rufen("getUpdates", anfrage, zeitlimit=30) or []
        except tg.TelegramFehler as fehler:
            print(f"  Telegram: {fehler} — ich versuche es weiter.", file=sys.stderr)
            time.sleep(3)
            continue
        if updates:
            offset = updates[-1]["update_id"] + 1
        for update in updates:
            msg = update.get("message") or {}
            von = msg.get("from") or {}
            if (msg.get("chat") or {}).get("type") != "private" or not von.get("id"):
                continue
            try:
                # Abhaken, damit der Dienst "hallo" spaeter nicht als Auftrag liest.
                draht.rufen("getUpdates", {"offset": offset, "timeout": 0})
                draht.nachricht(von["id"], "👋 Hallo! Ich habe dich erkannt. "
                                           "Bestätige jetzt bitte am Server.")
            except tg.TelegramFehler:
                pass
            name = " ".join(t for t in (von.get("first_name"), von.get("last_name")) if t)
            if von.get("username"):
                name += f" (@{von['username']})"
            print(f"NAME={name}")
            print(f"CHAT_ID={von['id']}")
            return 0
    print("  In der Zeit ist keine Nachricht angekommen.", file=sys.stderr)
    return 3


PROFIL_KURZ = "Gustav, der Orchestrator der Bellowerk Manufaktur. Privater Bot."
PROFIL_LANG = ("Privater Draht zu Gustav, dem Orchestrator der Bellowerk Manufaktur. "
               "Antwortet nur freigeschalteten Konten.")


def vorbereiten(draht: tg.Draht) -> None:
    """Befehlsmenue und Profiltext setzen, einen etwaigen Webhook abmelden
    (sonst liefert getUpdates nichts). Schadet nicht, wenn es schon so ist."""
    for methode, daten in (("deleteWebhook", {}), ("setMyCommands", {"commands": BEFEHLE}),
                           ("setMyShortDescription", {"short_description": PROFIL_KURZ}),
                           ("setMyDescription", {"description": PROFIL_LANG})):
        try:
            draht.rufen(methode, daten)
        except tg.TelegramFehler as fehler:
            print(f"[TELEGRAM] {methode}: {fehler}")


def main() -> None:
    argumente = sys.argv[1:]
    if "--kennenlernen" in argumente:
        sys.exit(kennenlernen())
    if "--ich" in argumente:
        sys.exit(ich_bin())
    try:
        config = config_laden()
    except Exception as fehler:
        print(f"[TELEGRAM] config.json nicht lesbar: {fehler}")
        sys.exit(EINRICHTUNG_FEHLT)
    grund = tg.diagnose(config)
    if grund:
        print(f"[TELEGRAM] Nicht eingerichtet: {grund}")
        sys.exit(EINRICHTUNG_FEHLT)
    token, erlaubt = tg.zugang(config)
    draht = tg.Draht(token)
    try:
        ich = draht.rufen("getMe")
    except tg.TelegramFehler as fehler:
        print(f"[TELEGRAM] {fehler}")
        sys.exit(EINRICHTUNG_FEHLT if fehler.code in (401, 404) else 1)
    if "--probe" in argumente:
        anstoss = _systemctl("is-active", "bello-orchestrator-anstoss.path") or "unbekannt"
        print(f"Bot:           @{ich.get('username')}")
        print(f"Konten:        {len(erlaubt)} freigeschaltet")
        print(f"Sofortstart:   {anstoss}")
        print(f"Nächster Lauf: {naechster_lauf()}")
        print("Alles lesbar.")
        return
    vorbereiten(draht)
    print(f"[TELEGRAM] Bereit als @{ich.get('username')} — "
          f"{len(erlaubt)} Konto/Konten freigeschaltet.")
    Bot(draht, erlaubt).schleife()


if __name__ == "__main__":
    main()
