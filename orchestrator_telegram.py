"""
orchestrator_telegram.py — Gustav schreibt Bjoern per Telegram.

Das Gegenstueck zu orchestrator_mail.py. Jede Eskalation, die per Mail rausgeht,
kommt zusaetzlich aufs Handy — mit Knoepfen zum Freigeben, Ueberarbeiten und
Verwerfen. Die Mail bleibt, wie sie ist: Telegram ist ein zweiter Kanal, kein
Ersatz, und ein Lauf haengt nie an Telegram.

Den Rueckweg — Bjoerns Nachrichten und Knopfdruecke — bearbeitet
bin/telegram_bot.py. Nur Standardbibliothek, kein zusaetzliches Paket.

An ist Telegram, sobald config.json einen Block "telegram" hat. Die Werte stehen
als Verweis darin und kommen aus /etc/bello/env (bin/telegram-einrichten.sh
traegt beides ein):

  "telegram": {"bot_token": "${TELEGRAM_BOT_TOKEN}", "chat_id": "${TELEGRAM_CHAT_ID}"}

Test:  .venv/bin/python orchestrator_telegram.py --test
"""

import html
import http.client
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid

from abteilung_basis import config_laden
from orchestrator_mail import _svg_als_png
import namen

API = "https://api.telegram.org"

# Telegram nimmt hoechstens 4096 Zeichen je Nachricht. Der Rest geht als Datei.
GRENZE = 4096
GRENZE_TEXT = 3500

# Die Knoepfe unter einem Ergebnis. Ausgewertet werden sie in bin/telegram_bot.py.
FREIGEBEN = "frei"
UEBERARBEITEN = "ueber"
VERWERFEN = "verw"
VERWERFEN_JA = "verw!"
ZURUECK = "zurueck"
ZEIGEN = "zeig"
JETZT = "jetzt"

# Wie ein Anlass auf dem Sperrbildschirm erscheint. Unbekanntes bekommt das Klemmbrett.
ANLAESSE = {
    "Ergebnis liegt vor": "📋 Ergebnis liegt vor",
    "Zweimal Nacharbeit erfolglos": "⚠️ Zweimal Nacharbeit erfolglos",
    "Technischer Fehler": "⛔ Technischer Fehler",
    "Frist ueberschritten": "⏰ Frist überschritten",
}

TOKEN_MUSTER = re.compile(r"\d{5,}:[A-Za-z0-9_-]{20,}")

# Ist Telegram nicht erreichbar, kostet jeder Versuch ein Zeitlimit. Ein Lauf mit
# zehn Ergebnissen soll daran nicht zehnmal haengen: nach dem ersten Netzfehler
# schweigt dieser Kanal eine Weile, die Mail geht weiter.
FUNKSTILLE_SEKUNDEN = 300
_funkstille_bis = 0.0


class TelegramFehler(Exception):
    """Telegram hat abgelehnt oder war nicht erreichbar. Nie mit Token im Text."""

    def __init__(self, text: str, code: int | None = None, warten: int | None = None):
        super().__init__(text)
        self.code = code
        self.warten = warten


# ---------- Zugang ----------

def _wert(roh) -> str:
    """Ein nicht aufgeloester Platzhalter ("${VAR}") zaehlt als leer."""
    text = str(roh or "").strip()
    return "" if text.startswith("${") else text


def chat_ids(roh) -> list[int]:
    """'123', 123, '123, 456' oder [123, 456] -> [123, 456]. Unlesbares faellt weg."""
    teile = roh if isinstance(roh, (list, tuple)) else re.split(r"[,;\s]+", _wert(roh))
    ids = []
    for teil in teile:
        try:
            ids.append(int(str(teil).strip()))
        except ValueError:
            continue
    return ids


def zugang(config: dict | None = None) -> tuple[str, list[int]]:
    """(Token, freigeschaltete Konten) — oder ("", []), wenn Telegram nicht eingerichtet ist.

    Ohne Block "telegram" in config.json ist Telegram aus, auch wenn die
    Umgebung einen Token kennt. So schickt kein Test und kein Probelauf aus
    Versehen etwas aufs Handy."""
    if config is None:
        try:
            config = config_laden()
        except Exception:
            return "", []
    tg = config.get("telegram")
    if not isinstance(tg, dict):
        return "", []
    token, chats = _wert(tg.get("bot_token")), chat_ids(tg.get("chat_id"))
    return (token, chats) if token and chats else ("", [])


def diagnose(config: dict | None = None) -> str:
    """Warum Telegram nicht geht — oder "" wenn die Einrichtung vollstaendig ist."""
    try:
        config = config if config is not None else config_laden()
    except Exception as fehler:
        return f"config.json nicht lesbar ({fehler})"
    tg = config.get("telegram")
    if not isinstance(tg, dict):
        return "config.json hat keinen Block \"telegram\" (bin/telegram-einrichten.sh legt ihn an)"
    if not _wert(tg.get("bot_token")):
        return "kein Bot-Token (TELEGRAM_BOT_TOKEN fehlt in /etc/bello/env oder wird nicht geladen)"
    if not chat_ids(tg.get("chat_id")):
        return "kein freigeschaltetes Konto (TELEGRAM_CHAT_ID fehlt in /etc/bello/env)"
    return ""


def ohne_token(text) -> str:
    """Der Token steckt in jeder Adresse der Bot-API. Er darf in keinem Log landen."""
    return TOKEN_MUSTER.sub("***", str(text))


# ---------- Leitung ----------

def _formular(felder: dict, dateien: dict) -> tuple[bytes, str]:
    """multipart/form-data von Hand — fuer Dateien, ohne zusaetzliches Paket."""
    grenze = "bello" + uuid.uuid4().hex
    teile: list[bytes] = []
    for name, wert in felder.items():
        if wert is None:
            continue
        if isinstance(wert, (dict, list)):
            wert = json.dumps(wert, ensure_ascii=False)
        teile += [f"--{grenze}\r\n".encode(),
                  f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                  str(wert).encode("utf-8"), b"\r\n"]
    for name, (dateiname, inhalt, typ) in dateien.items():
        sicher = re.sub(r"[^A-Za-z0-9._-]", "_", dateiname) or "datei"
        teile += [f"--{grenze}\r\n".encode(),
                  f'Content-Disposition: form-data; name="{name}"; filename="{sicher}"\r\n'.encode(),
                  f"Content-Type: {typ}\r\n\r\n".encode(), inhalt, b"\r\n"]
    teile.append(f"--{grenze}--\r\n".encode())
    return b"".join(teile), f"multipart/form-data; boundary={grenze}"


def _http(token: str, methode: str, daten: dict | None, dateien: dict | None,
          zeitlimit: float) -> dict:
    """Ein Aufruf der Bot-API. Liefert die ganze Antwort ({"ok": ..., ...})."""
    if dateien:
        rumpf, typ = _formular(daten or {}, dateien)
    else:
        rumpf = json.dumps(daten or {}, ensure_ascii=False).encode("utf-8")
        typ = "application/json"
    anfrage = urllib.request.Request(f"{API}/bot{token}/{methode}", data=rumpf,
                                     headers={"Content-Type": typ}, method="POST")
    try:
        with urllib.request.urlopen(anfrage, timeout=zeitlimit) as antwort:
            return json.loads(antwort.read().decode("utf-8"))
    except urllib.error.HTTPError as fehler:
        # Auch eine Ablehnung kommt als JSON, mit Grund und ggf. Wartezeit.
        try:
            return json.loads(fehler.read().decode("utf-8"))
        except Exception:
            return {"ok": False, "error_code": fehler.code, "description": f"HTTP {fehler.code}"}


class Draht:
    """Die Leitung zu Telegram fuer einen Bot-Token.

    Der Transport ist austauschbar, damit die Tests ohne Netz auskommen."""

    def __init__(self, token: str, transport=None):
        self.token = token
        self.transport = transport or _http

    def rufen(self, methode: str, daten: dict | None = None, dateien: dict | None = None,
              zeitlimit: float = 20):
        for versuch in (1, 2):
            try:
                antwort = self.transport(self.token, methode, daten, dateien, zeitlimit)
            except (urllib.error.URLError, http.client.HTTPException, OSError, ValueError) as fehler:
                raise TelegramFehler(ohne_token(f"Telegram nicht erreichbar ({fehler})")) from None
            if antwort.get("ok"):
                return antwort.get("result")
            code = antwort.get("error_code")
            warten = (antwort.get("parameters") or {}).get("retry_after")
            # Zu viele Nachrichten auf einmal: einmal kurz warten, dann aufgeben.
            if code == 429 and warten and warten <= 30 and versuch == 1:
                time.sleep(warten)
                continue
            raise TelegramFehler(ohne_token(antwort.get("description") or "unbekannter Fehler"),
                                 code, warten)

    def nachricht(self, chat: int, text: str, knoepfe: list | None = None,
                  antwort_auf: int | None = None, erzwinge_antwort: str | None = None) -> dict:
        """Schickt HTML-Text. Scheitert Telegram am Markup, geht er als Klartext."""
        daten: dict = {"chat_id": chat, "text": text, "parse_mode": "HTML",
                       "link_preview_options": {"is_disabled": True}}
        if knoepfe:
            daten["reply_markup"] = {"inline_keyboard": knoepfe}
        elif erzwinge_antwort:
            daten["reply_markup"] = {"force_reply": True,
                                     "input_field_placeholder": erzwinge_antwort[:64]}
        if antwort_auf:
            daten["reply_parameters"] = {"message_id": antwort_auf,
                                         "allow_sending_without_reply": True}
        if len(klartext(text)) > GRENZE:
            daten["text"] = klartext(text)[:GRENZE - 2] + " …"
            daten.pop("parse_mode")
        try:
            return self.rufen("sendMessage", daten)
        except TelegramFehler as fehler:
            if fehler.code != 400 or "parse" not in str(fehler).lower() or "parse_mode" not in daten:
                raise
            daten["text"] = klartext(text)[:GRENZE]
            daten.pop("parse_mode")
            return self.rufen("sendMessage", daten)

    def text_aendern(self, chat: int, nachricht_id: int, text: str,
                     knoepfe: list | None = None) -> None:
        daten = {"chat_id": chat, "message_id": nachricht_id, "text": text,
                 "parse_mode": "HTML", "link_preview_options": {"is_disabled": True},
                 "reply_markup": {"inline_keyboard": knoepfe or []}}
        try:
            self.rufen("editMessageText", daten)
        except TelegramFehler as fehler:
            if "not modified" not in str(fehler):
                raise

    def knoepfe_setzen(self, chat: int, nachricht_id: int, knoepfe: list | None = None) -> None:
        """Tauscht die Knoepfe unter einer Nachricht aus; ohne Liste verschwinden sie."""
        daten = {"chat_id": chat, "message_id": nachricht_id,
                 "reply_markup": {"inline_keyboard": knoepfe or []}}
        try:
            self.rufen("editMessageReplyMarkup", daten)
        except TelegramFehler as fehler:
            if "not modified" not in str(fehler):
                raise

    def quittieren(self, rueckruf_id: str, text: str | None = None) -> None:
        """Jeder Knopfdruck will quittiert sein, sonst dreht sich am Knopf die Uhr."""
        daten = {"callback_query_id": rueckruf_id}
        if text:
            daten["text"] = text[:200]
        try:
            self.rufen("answerCallbackQuery", daten)
        except TelegramFehler:
            pass    # nach einigen Minuten verfallen — nichts mehr zu retten

    def datei(self, chat: int, dateiname: str, inhalt: bytes,
              beschriftung: str | None = None) -> dict:
        typ = mimetypes.guess_type(dateiname)[0] or "application/octet-stream"
        return self.rufen("sendDocument", {"chat_id": chat, "caption": beschriftung},
                          {"document": (dateiname, inhalt, typ)}, zeitlimit=60)


# ---------- Text ----------

def esc(text) -> str:
    return html.escape(str(text if text is not None else ""), quote=False)


def klartext(html_text: str) -> str:
    """HTML-Nachricht zurueck in Klartext — fuer den Notfall ohne Markup."""
    return html.unescape(re.sub(r"<[^>]+>", "", html_text))


def ohne_svg(text) -> str:
    """Zeichnungen stehen als SVG im Ergebnis. Auf dem Handy waeren das Seiten
    voller Zahlen; die Zeichnung selbst kommt als Bild hinterher."""
    text = re.sub(r"<<<SVG>>>.*?<<</SVG>>>", "[Zeichnung]", str(text or ""), flags=re.S)
    return re.sub(r"<svg.*?</svg>", "[Zeichnung]", text, flags=re.S | re.I)


def kuerzen(text: str, grenze: int = GRENZE_TEXT) -> tuple[str, bool]:
    """Kuerzt an einer Absatz-, Zeilen- oder Wortgrenze. Zweiter Wert: gekuerzt?"""
    text = (text or "").strip()
    if len(text) <= grenze:
        return text, False
    schnitt = text[:grenze]
    for trenner in ("\n\n", "\n", " "):
        stelle = schnitt.rfind(trenner)
        if stelle > grenze * 0.6:
            return schnitt[:stelle].rstrip() + " …", True
    return schnitt.rstrip() + " …", True


def fuers_handy(text: str, auftrag: dict) -> str:
    """Der Mailtext beginnt mit Auftrag und Abteilung — auf dem Handy stehen beide
    schon im Kopf. Und Spalten, die in der Mail buendig sind, sehen in einer
    Proportionalschrift zerrupft aus."""
    doppelt = {f"Auftrag: {auftrag.get('id')}", f"Abteilung: {auftrag.get('abteilung')}"}
    zeilen = []
    for zeile in ohne_svg(text).splitlines():
        zeile = re.sub(r"^(\w+):\s{2,}", r"\1: ", zeile)
        if zeile.strip() not in doppelt:
            zeilen.append(zeile)
    return "\n".join(zeilen).strip()


def wer(abteilung: str) -> str:
    """'07 Einkauf China' -> 'Henrik (07 Einkauf China)'."""
    vn = namen.vorname(abteilung or "")
    return f"{vn} ({abteilung})" if vn else str(abteilung or "")


def hat_ergebnis(auftrag: dict) -> bool:
    return any(e.get("ergebnis") for e in auftrag.get("verlauf") or [])


def entscheidungs_knoepfe(auftrag: dict) -> list:
    """Freigeben nur, wo es etwas freizugeben gibt — nicht bei einem technischen
    Fehler oder einer Frist, die ohne Ergebnis abgelaufen ist."""
    nr = auftrag["id"]
    oben = [{"text": "✏️ Überarbeiten", "callback_data": f"{UEBERARBEITEN}:{nr}"}]
    if hat_ergebnis(auftrag):
        oben.insert(0, {"text": "✅ Freigeben", "callback_data": f"{FREIGEBEN}:{nr}"})
    return [oben, [{"text": "🗑 Verwerfen", "callback_data": f"{VERWERFEN}:{nr}"}]]


# ---------- Bilder ----------

def bilder_senden(draht: Draht, chat: int, pfade) -> None:
    """Zeichnungen als Bild in den Verlauf. SVG kann Telegram nicht zeigen:
    dann die PNG daneben (rendert orchestrator_mail) oder die SVG als Datei."""
    for pfad in pfade or []:
        if not pfad or not os.path.isfile(pfad):
            continue
        ziel = (_svg_als_png(pfad) if pfad.lower().endswith(".svg") else None) or pfad
        with open(ziel, "rb") as f:
            inhalt = f.read()
        name = os.path.basename(ziel)
        typ = mimetypes.guess_type(name)[0] or "application/octet-stream"
        if typ in ("image/png", "image/jpeg"):
            try:
                draht.rufen("sendPhoto", {"chat_id": chat, "caption": os.path.basename(pfad)},
                            {"photo": (name, inhalt, typ)}, zeitlimit=60)
                continue
            except TelegramFehler:
                pass    # zu gross oder zu schmal fuer ein Foto — dann als Datei
        draht.datei(chat, name, inhalt)


# ---------- Was der Orchestrator ruft ----------

def _an_alle(config: dict | None, schicken) -> bool:
    """Ruft schicken(draht, chat) fuer jedes freigeschaltete Konto. Wirft nie.

    Ist Telegram nicht erreichbar, schweigt der Kanal danach eine Weile, statt
    jede weitere Meldung dieses Laufs ins Zeitlimit laufen zu lassen."""
    global _funkstille_bis
    try:
        token, chats = zugang(config)
        if not token:
            return False
        if time.time() < _funkstille_bis:
            print("[TELEGRAM] uebersprungen — Telegram war eben nicht erreichbar, die Mail geht")
            return False
        draht = Draht(token)
        alles_gut = True
        for chat in chats:
            try:
                schicken(draht, chat)
            except TelegramFehler as fehler:
                print(f"[TELEGRAM] FEHLER: {fehler}")
                alles_gut = False
                if fehler.code is None:     # das Netz, nicht Telegram
                    _funkstille_bis = time.time() + FUNKSTILLE_SEKUNDEN
                    break
        return alles_gut
    except Exception as fehler:
        print(f"[TELEGRAM] FEHLER: {ohne_token(fehler)}")
        return False


def melden(auftrag: dict, grund: str, text: str, config: dict | None = None,
           anhaenge: list[str] | None = None) -> bool:
    """Eine Eskalation aufs Handy: Anlass, Bericht, Knoepfe, Zeichnungen.

    Wirft nie. Ist Telegram nicht eingerichtet oder nicht erreichbar, bleibt es
    bei der Mail — der Lauf geht in jedem Fall weiter."""
    nr = auftrag.get("id") or ""

    def schicken(draht: Draht, chat: int) -> None:
        kopf = (f"<b>{esc(ANLAESSE.get(grund, '📋 ' + grund))}</b>\n"
                f"{esc(nr)} · {esc(wer(auftrag.get('abteilung', '')))}")
        voll = fuers_handy(text, auftrag)
        rumpf, gekuerzt = kuerzen(voll)
        if gekuerzt:
            rumpf += "\n\n(Vollständig in der Datei darunter und in der Mail.)"
        draht.nachricht(chat, f"{kopf}\n\n{esc(rumpf)}",
                        knoepfe=entscheidungs_knoepfe(auftrag) if nr else None)
        if gekuerzt:
            draht.datei(chat, f"{nr or 'bericht'}.txt", voll.encode("utf-8"))
        bilder_senden(draht, chat, anhaenge)

    erfolg = _an_alle(config, schicken)
    if erfolg:
        print(f"[TELEGRAM] Gemeldet: {nr} — {grund}")
    return erfolg


def senden(text: str, config: dict | None = None, titel: str | None = None) -> bool:
    """Klartext an alle freigeschalteten Konten — Wochenuebersicht, Stoerung.
    Zu Langes kommt zusaetzlich als Datei. Wirft nie."""

    def schicken(draht: Draht, chat: int) -> None:
        rumpf, gekuerzt = kuerzen(text)
        draht.nachricht(chat, (f"<b>{esc(titel)}</b>\n\n" if titel else "") + esc(rumpf))
        if gekuerzt:
            draht.datei(chat, "bericht.txt", text.encode("utf-8"))

    return _an_alle(config, schicken)


if __name__ == "__main__":
    if "--test" in sys.argv:
        grund = diagnose()
        if grund:
            print(f"[TELEGRAM] Nicht eingerichtet: {grund}")
            sys.exit(1)
        erfolg = senden("Wenn diese Nachricht ankommt, funktioniert der Weg vom Server "
                        "aufs Handy.", titel="Testnachricht von Gustav")
        print("[TELEGRAM] Testnachricht gesendet." if erfolg
              else "[TELEGRAM] Testnachricht NICHT gesendet (Grund siehe oben).")
        sys.exit(0 if erfolg else 1)
    print("Aufruf: python orchestrator_telegram.py --test")
