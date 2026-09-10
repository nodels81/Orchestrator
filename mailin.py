"""mailin.py — liest Gustavs Postfach und macht aus Bjoerns Mail-Antworten Auftraege.

Sicherheitsmodell (Variante A, ruhig):
  - NUR Mails von der Absender-Allowlist (Bjoern) werden verarbeitet.
  - Nur Antworten auf "[Bello] A-2026-NNN <Abteilung>"-Threads.
  - Eine Antwort wird nur dann ein Auftrag, wenn ihre erste Zeile mit
    "@Abteilung ..." oder "Auftrag: ..." beginnt. Sonst: ignoriert.
  - Der Auftrag laeuft im normalen Tageslauf um 07:00. Kein Shell-Zugriff,
    keine eigenstaendigen Ausgaben — alles laeuft durch die ueblichen Regeln.
  - Jede schon gesehene Message-ID wird gemerkt, nichts wird doppelt verarbeitet;
    der Gelesen-Status der Mails wird nicht angefasst.
"""

import email
import email.utils
import imaplib
import json
import os
import re
import sys
from email.header import decode_header, make_header

from abteilung_basis import config_laden, DATEN
import orchestrator
from orchestrator_mail import senden

ALLOWLIST = {
    "pijoern.nodels@gmail.com",
    "pijoern.nodels@googlemail.com",
}
STATE = os.path.join(DATEN, "mailin_verarbeitet.json")
BETREFF_RE = re.compile(r"\[Bello\]\s+(A-\d{4}-\d+)\s+(.+?)\s+[—-]")


def _state_laden() -> set:
    try:
        return set(json.load(open(STATE, encoding="utf-8")))
    except Exception:
        return set()


def _state_speichern(s: set) -> None:
    tmp = STATE + ".tmp"
    json.dump(sorted(s), open(tmp, "w", encoding="utf-8"), indent=1)
    os.replace(tmp, STATE)


def _klartext(msg) -> str:
    if msg.is_multipart():
        for teil in msg.walk():
            if (teil.get_content_type() == "text/plain"
                    and "attachment" not in str(teil.get("Content-Disposition", ""))):
                roh = teil.get_payload(decode=True) or b""
                return roh.decode(teil.get_content_charset() or "utf-8", "replace")
        return ""
    roh = msg.get_payload(decode=True) or b""
    return roh.decode(msg.get_content_charset() or "utf-8", "replace")


def _entzitieren(text: str) -> str:
    zeilen = []
    for z in text.splitlines():
        s = z.strip()
        if s.startswith(">"):
            break
        if re.match(r"^(Am .+ schrieb|On .+ wrote|-{2,}\s*Forwarded|Von:\s|From:\s|Gesendet von)", s):
            break
        zeilen.append(z)
    return "\n".join(zeilen).strip()


def _absender(msg) -> str:
    _, addr = email.utils.parseaddr(msg.get("From", ""))
    return addr.lower()


def _betreff(msg) -> str:
    try:
        return str(make_header(decode_header(msg.get("Subject", ""))))
    except Exception:
        return msg.get("Subject", "") or ""


def verarbeiten() -> int:
    cfg = config_laden()
    m = cfg.get("mail", {})
    pw = m.get("app_passwort") or os.environ.get("SMTP_PASSWORT")
    user = m.get("absender")
    host = m.get("imap_server", "imap.gmail.com")
    port = int(m.get("imap_port", 993))
    if not (user and pw):
        print("[MAILIN] nicht konfiguriert — nichts zu tun")
        return 0

    verarbeitet = _state_laden()
    erst_lauf = not verarbeitet
    neu = 0
    imap = imaplib.IMAP4_SSL(host, port, timeout=30)
    try:
        imap.login(user, pw)
        imap.select("INBOX")
        typ, daten = imap.search(None, '(SUBJECT "[Bello]")')
        ids = daten[0].split()[-50:] if daten and daten[0] else []
        for i in ids:
            typ, roh = imap.fetch(i, "(RFC822)")
            if typ != "OK" or not roh or not roh[0]:
                continue
            msg = email.message_from_bytes(roh[0][1])
            mid = (msg.get("Message-ID") or "").strip()
            if not mid or mid in verarbeitet:
                continue
            verarbeitet.add(mid)
            if erst_lauf:
                # beim allerersten Lauf nur den Stand merken, nicht ruecklaeufig abarbeiten
                continue
            if _absender(msg) not in ALLOWLIST:
                print(f"[MAILIN] ignoriert — Absender {_absender(msg)} nicht in der Allowlist")
                continue
            betreff = _betreff(msg)
            mt = BETREFF_RE.search(betreff)
            if not mt:
                continue
            parent, betreff_abt = mt.group(1), mt.group(2).strip()
            koerper = _entzitieren(_klartext(msg))
            if not koerper:
                print(f"[MAILIN] {parent}: leere Antwort — ignoriert")
                continue
            zeilen = koerper.splitlines()
            erste = zeilen[0].strip()
            rest_zeilen = "\n".join(zeilen[1:]).strip()
            m_at = re.match(r"@\s*([A-Za-zÄÖÜäöüß0-9 &]+?)\s*[:,\-\s]\s*(.*)", erste)
            m_auf = re.match(r"(?i)^auftrag\s*[:\-]?\s*(.+)", erste)
            if m_at:
                ziel_abt = m_at.group(1).strip()
                text = (m_at.group(2).strip() + "\n" + rest_zeilen).strip()
            elif m_auf:
                ziel_abt = betreff_abt
                text = (m_auf.group(1).strip() + "\n" + rest_zeilen).strip()
            else:
                print(f"[MAILIN] {parent}: Antwort ohne '@Abteilung' oder 'Auftrag:' — ignoriert")
                continue
            try:
                kanon = orchestrator.abteilung_aufloesen(ziel_abt)
            except ValueError as fehler:
                print(f"[MAILIN] {parent}: Abteilung '{ziel_abt}' unklar — {fehler}")
                senden(f"[Bello] Mail-Auftrag nicht zugeordnet ({parent})",
                       f"Deine Antwort konnte keiner Abteilung zugeordnet werden.\n"
                       f"Erste Zeile war: {erste!r}\n\n{fehler}", cfg)
                continue
            ziel = f"{text}\n\n(per Mail-Antwort auf {parent})"
            auftrag = orchestrator.auftrag_anlegen(kanon, ziel)
            neu += 1
            print(f"[MAILIN] {parent} -> {auftrag['id']} an {kanon}")
            senden(f"[Bello] {auftrag['id']} aus deiner Mail — an {kanon}",
                   f"Deine Antwort auf {parent} ist als Auftrag {auftrag['id']} angelegt "
                   f"und geht an {kanon}.\n\nZiel:\n{text}\n\n"
                   f"Er laeuft beim naechsten Tageslauf (07:00). Ergebnis kommt per Mail.\n"
                   f"— {getattr(__import__('namen'), 'ORCHESTRATOR', 'Gustav')}", cfg)
        try:
            imap.logout()
        except Exception:
            pass
    finally:
        _state_speichern(verarbeitet)
    print(f"[MAILIN] fertig — {neu} neue Auftraege"
          + (" (Erstlauf: nur Stand gemerkt)" if erst_lauf else ""))
    return neu


if __name__ == "__main__":
    if "--test-imap" in sys.argv:
        cfg = config_laden().get("mail", {})
        pw = cfg.get("app_passwort") or os.environ.get("SMTP_PASSWORT")
        imap = imaplib.IMAP4_SSL(cfg.get("imap_server", "imap.gmail.com"),
                                 int(cfg.get("imap_port", 993)), timeout=30)
        imap.login(cfg.get("absender"), pw)
        imap.select("INBOX")
        typ, d = imap.search(None, '(SUBJECT "[Bello]")')
        print("IMAP OK — [Bello]-Mails in Gustavs INBOX:", len((d[0] or b"").split()))
        imap.logout()
        sys.exit(0)
    verarbeiten()
