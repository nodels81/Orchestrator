"""
posteingang.py — Der Rueckkanal: Bjoern schreibt eine Mail, der Server handelt.

Grund: Der Betrieb laeuft 24/7 auf dem Server, auch wenn kein Rechner an ist.
Damit Bjoern von unterwegs eingreifen kann, ohne SSH und ohne App, liest dieser
Dienst alle paar Minuten das Postfach des Orchestrators und fuehrt genau die
Befehle aus, die unten in BEFEHLE stehen. Die Antwort geht per Mail zurueck.

SICHERHEIT — bitte lesen:
  Ein Absender im Feld "From" ist faelschbar. Er allein schuetzt nichts.
  Deshalb gilt beides gleichzeitig:
    1. Die Absenderadresse muss mail.empfaenger aus config.json sein.
    2. Im Betreff muss das Kennwort aus autonom.kennwort stehen.
  Das Kennwort ist der eigentliche Schutz. Wer es kennt, darf Auftraege
  anlegen — mehr nicht. Es gibt bewusst KEINEN Befehl, der eine Shell oeffnet,
  Dateien schreibt oder Geld ausgibt.

Aufrufe:
  posteingang.py             Einmal abholen und beantworten
  posteingang.py --probe     Zeigen, was passieren wuerde, ohne zu handeln
"""

import email
import imaplib
import io
import os
import re
import ssl
import sys
from contextlib import redirect_stdout
from email.header import decode_header, make_header
from email.utils import parseaddr

# Der Betriebsordner liegt eine Ebene hoeher. Python legt beim Start nur den
# Ordner des Skripts auf den Suchpfad, nicht das Arbeitsverzeichnis — ohne diese
# Zeile findet systemd die Module abteilung_basis, orchestrator und tagesbrief nicht.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from abteilung_basis import BASIS, config_laden
from orchestrator_mail import senden

PROTOKOLL = os.path.join(BASIS, "logs", "posteingang.log")
MAX_MAILS_PRO_LAUF = 10


# ---------- Hilfen ----------

def _protokoll(zeile: str) -> None:
    from datetime import datetime
    os.makedirs(os.path.dirname(PROTOKOLL), exist_ok=True)
    stempel = datetime.now().isoformat(timespec="seconds")
    with open(PROTOKOLL, "a", encoding="utf-8") as f:
        f.write(f"{stempel}  {zeile}\n")
    print(zeile)


def _klartext(rohwert: str | None) -> str:
    if not rohwert:
        return ""
    try:
        return str(make_header(decode_header(rohwert)))
    except Exception:
        return rohwert


def _koerper(nachricht) -> str:
    """Nur den reinen Text nehmen. HTML-Teile werden ignoriert."""
    if not nachricht.is_multipart():
        nutzlast = nachricht.get_payload(decode=True) or b""
        return nutzlast.decode(nachricht.get_content_charset() or "utf-8", "replace")
    for teil in nachricht.walk():
        if teil.get_content_type() == "text/plain":
            nutzlast = teil.get_payload(decode=True) or b""
            return nutzlast.decode(teil.get_content_charset() or "utf-8", "replace")
    return ""


def _ohne_zitat(text: str) -> str:
    """Alles ab der ersten Zitatzeile abschneiden, sonst liest man alte Mails mit."""
    zeilen = []
    for zeile in text.splitlines():
        if zeile.startswith(">") or zeile.startswith("Am ") and " schrieb" in zeile:
            break
        if zeile.strip() in ("--", "-- "):
            break
        zeilen.append(zeile)
    return "\n".join(zeilen).strip()


# ---------- Befehle ----------

def _befehl_stand(_rest: str) -> str:
    import orchestrator
    puffer = io.StringIO()
    with redirect_stdout(puffer):
        orchestrator.stand_zeigen()
    return puffer.getvalue() or "Keine Auftraege."


def _befehl_wochenbericht(_rest: str) -> str:
    import orchestrator
    return orchestrator.wochenbericht_text()


def _befehl_brief(_rest: str) -> str:
    import tagesbrief
    return tagesbrief.text_bauen()


def _befehl_auftrag(rest: str) -> str:
    """auftrag <Abteilung> | <Ziel> [| JJJJ-MM-TT]"""
    import orchestrator
    teile = [t.strip() for t in rest.split("|")]
    if len(teile) < 2 or not teile[0] or not teile[1]:
        return ('Aufbau: auftrag <Abteilung> | <Ziel> [| JJJJ-MM-TT]\n'
                'Beispiel: auftrag 01 Innovation | Pflegeset PF-01 durchrechnen\n\n'
                "Bekannte Abteilungen:\n"
                + "\n".join(f"  {a}" for a in orchestrator.ABTEILUNGEN))
    frist = teile[2] if len(teile) > 2 and teile[2] else None
    if frist and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", frist):
        return f"Frist '{frist}' ist kein Datum im Format JJJJ-MM-TT."
    try:
        auftrag = orchestrator.auftrag_anlegen(teile[0], teile[1], frist)
    except ValueError as fehler:
        return str(fehler)
    return (f"Angelegt: {auftrag['id']}\n"
            f"Abteilung: {auftrag['abteilung']}\n"
            f"Ziel: {auftrag['ziel']}\n"
            f"Frist: {auftrag['frist']}\n\n"
            "Der naechste Lauf nimmt ihn auf.")


def _befehl_hilfe(_rest: str) -> str:
    return (
        "Befehle. Einer pro Mail, in der ersten Zeile des Textes.\n"
        "Das Kennwort muss im Betreff stehen.\n\n"
        "  stand            Woran wird gerade gearbeitet\n"
        "  brief            Den Tagesbrief sofort schicken\n"
        "  wochenbericht    Die Wochenuebersicht\n"
        "  auftrag <Abteilung> | <Ziel> [| JJJJ-MM-TT]\n"
        "  hilfe            Diese Liste\n\n"
        "Absichtlich nicht vorhanden: Shell, Dateien schreiben, Geld ausgeben,\n"
        "Bestellungen ausloesen. Das bleibt bei dir."
    )


BEFEHLE = {
    "stand": _befehl_stand,
    "brief": _befehl_brief,
    "tagesbrief": _befehl_brief,
    "wochenbericht": _befehl_wochenbericht,
    "auftrag": _befehl_auftrag,
    "hilfe": _befehl_hilfe,
}


# ---------- Ablauf ----------

def _pruefen(config: dict, absender: str, betreff: str) -> str | None:
    """Gibt den Ablehnungsgrund zurueck, oder None wenn alles stimmt."""
    autonom = config.get("autonom", {})
    kennwort = autonom.get("kennwort", "")
    erlaubt = (config.get("mail", {}).get("empfaenger") or "").lower().strip()

    if not kennwort:
        return "autonom.kennwort fehlt in config.json — Eingang ist abgeschaltet"
    if not erlaubt:
        return "mail.empfaenger fehlt in config.json"
    if parseaddr(absender)[1].lower().strip() != erlaubt:
        return f"Absender {absender!r} ist nicht {erlaubt}"
    if kennwort.lower() not in betreff.lower():
        return "Kennwort fehlt im Betreff"
    return None


def _ausfuehren(text: str, probe: bool = False) -> tuple[str, str]:
    """Erste nicht leere Zeile ist der Befehl. Gibt (Befehlsname, Antwort).

    Im Probelauf wird der Befehl nur benannt, nicht ausgefuehrt. Sonst wuerde
    'auftrag' auch beim Probieren einen Auftrag in auftraege.json schreiben.
    """
    zeilen = [z for z in _ohne_zitat(text).splitlines() if z.strip()]
    if not zeilen:
        return "leer", _befehl_hilfe("")
    erste = zeilen[0].strip()
    wort = erste.split()[0].lower().rstrip(":")
    rest = erste[len(wort):].lstrip(" :")
    funktion = BEFEHLE.get(wort)
    if not funktion:
        return wort, f"Unbekannter Befehl {wort!r}.\n\n" + _befehl_hilfe("")
    if probe:
        return wort, f"(Probelauf — nicht ausgefuehrt) {wort} {rest}".strip()
    return wort, funktion(rest)


def abholen(probe: bool = False) -> int:
    config = config_laden()
    mail = config.get("mail", {})
    autonom = config.get("autonom", {})

    konto = mail.get("absender")
    passwort = mail.get("app_passwort")
    server = autonom.get("imap_server", "imap.gmail.com")
    port = int(autonom.get("imap_port", 993))
    # Ohne Zeitlimit haengt der Dienst bei gestoertem Postfach, bis systemd ihn
    # nach TimeoutStartSec abwuergt. Lieber nach 30 Sekunden aufgeben und es in
    # fuenf Minuten noch einmal versuchen.
    zeitlimit = int(autonom.get("timeout_sekunden", 30))

    if not (konto and passwort):
        _protokoll("[EINGANG] Nicht konfiguriert (mail.absender / mail.app_passwort).")
        return 1

    kontext = ssl.create_default_context()
    try:
        with imaplib.IMAP4_SSL(server, port, ssl_context=kontext,
                               timeout=zeitlimit) as imap:
            imap.login(konto, passwort)
            imap.select("INBOX")
            _, antwort = imap.search(None, "UNSEEN")
            kennungen = antwort[0].split()[:MAX_MAILS_PRO_LAUF]

            if not kennungen:
                print("Nichts Neues im Postfach.")
                return 0

            for kennung in kennungen:
                _, daten = imap.fetch(kennung, "(RFC822)")
                nachricht = email.message_from_bytes(daten[0][1])
                absender = _klartext(nachricht.get("From"))
                betreff = _klartext(nachricht.get("Subject"))

                grund = _pruefen(config, absender, betreff)
                if grund:
                    _protokoll(f"[EINGANG] Abgewiesen: {grund} | Betreff: {betreff!r}")
                    if not probe:
                        imap.store(kennung, "+FLAGS", "\\Seen")
                    continue

                wort, antworttext = _ausfuehren(_koerper(nachricht), probe=probe)
                if probe:
                    print(f"[Probe] Wuerde ausfuehren: {wort}\n{antworttext}")
                    continue

                _protokoll(f"[EINGANG] Ausgefuehrt: {wort} | Betreff: {betreff!r}")
                senden(f"[Bello] Antwort: {wort}", antworttext, config)
                imap.store(kennung, "+FLAGS", "\\Seen")

    except imaplib.IMAP4.error as fehler:
        _protokoll(f"[EINGANG] FEHLER Anmeldung: {fehler}")
        return 1
    except (TimeoutError, OSError) as fehler:
        _protokoll(f"[EINGANG] Postfach nicht erreichbar: {fehler}")
        return 1
    except Exception as fehler:
        _protokoll(f"[EINGANG] FEHLER: {fehler}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(abholen(probe="--probe" in sys.argv))
