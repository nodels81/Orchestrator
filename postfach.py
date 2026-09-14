"""postfach.py — Eigene Mailkonten fuer die Einkaufsabteilungen.

Jede Abteilung schickt aus ihrem eigenen Postfach (Einkauf China, Einkauf Europa)
und liest dort auch die Antworten. Zugangsdaten stehen in config.json (gitignored)
oder in Umgebungsvariablen, nie im Code und nie im Repo.

Aufrufe:
  venv/bin/python postfach.py --test einkauf_china
  venv/bin/python postfach.py --senden sourcing/lieferanten/anfragen-2026-09/cn-01-kingming.md \
      --an sales@example.com --trocken
  venv/bin/python postfach.py --posteingang einkauf_eu --tage 7
"""

import argparse
import email
import imaplib
import mimetypes
import os
import re
import smtplib
import ssl
import sys
from email.message import EmailMessage
from email.header import decode_header, make_header

from abteilung_basis import BASIS, config_laden

SOURCING = os.path.join(BASIS, "sourcing", "bellowerk")

# Welches Postfach zu welchem Dateipraefix gehoert.
PRAEFIX_POSTFACH = {"cn": "einkauf_china", "pl": "einkauf_eu", "de": "einkauf_eu"}


def postfach_laden(name: str, config: dict | None = None) -> dict:
    """Zugangsdaten eines Postfachs. Passwort darf aus der Umgebung nachgereicht werden."""
    config = config or config_laden()
    konten = config.get("postfaecher", {})
    if name not in konten:
        raise KeyError(
            f"Postfach '{name}' fehlt in config.json. Vorlage: config.beispiel.json, "
            f"bekannt sind: {', '.join(sorted(konten)) or 'keine'}"
        )
    konto = dict(konten[name])
    umgebung = f"BELLOWERK_{name.upper()}_PASSWORT"
    konto["passwort"] = os.environ.get(umgebung) or konto.get("passwort", "")
    konto.setdefault("benutzer", konto.get("adresse", ""))
    konto.setdefault("smtp_server", "")
    konto.setdefault("smtp_port", 465)
    konto.setdefault("imap_server", konto["smtp_server"].replace("smtp.", "imap.", 1))
    konto.setdefault("imap_port", 993)
    fehlt = [f for f in ("adresse", "passwort", "smtp_server") if not konto.get(f)]
    if fehlt:
        raise ValueError(
            f"Postfach '{name}' unvollstaendig: {', '.join(fehlt)} fehlt. "
            f"Passwort auch moeglich per Umgebungsvariable {umgebung}."
        )
    return konto


def anfrage_lesen(pfad: str) -> dict:
    """Liest eine Datei aus sourcing/lieferanten/anfragen-*/ als Betreff, Text, Anhaenge."""
    with open(pfad, encoding="utf-8") as f:
        zeilen = f.read().splitlines()

    anhaenge: list[str] = []
    betreff = ""
    text: list[str] = []
    im_text = False
    for zeile in zeilen:
        if not im_text:
            if zeile.startswith("| Anh"):  # Kopfzeile "Anhaenge"
                anhaenge = re.findall(r"`([^`]+)`", zeile)
            treffer = re.match(r"\*\*(?:Subject|Betreff):\*\*\s*(.+)", zeile)
            if treffer:
                betreff = treffer.group(1).strip()
                im_text = True
            continue
        if zeile.strip() == "---" or zeile.startswith("## "):
            text.append("")  # Trenner statt Markdown-Ueberschrift
            continue
        text.append(zeile.replace("**", ""))

    if not betreff:
        raise ValueError(f"{pfad}: keine Betreffzeile (**Subject:** oder **Betreff:**) gefunden.")

    while text and not text[0].strip():
        text.pop(0)
    while text and not text[-1].strip():
        text.pop()
    zusammengefasst: list[str] = []
    for zeile in text:  # mehrere Leerzeilen hintereinander auf eine reduzieren
        if not zeile.strip() and zusammengefasst and not zusammengefasst[-1].strip():
            continue
        zusammengefasst.append(zeile)
    text = zusammengefasst

    praefix = os.path.basename(pfad).split("-", 1)[0]
    return {
        "betreff": betreff,
        "text": "\n".join(text) + "\n",
        "anhaenge": [os.path.join(SOURCING, a) for a in anhaenge],
        "postfach": PRAEFIX_POSTFACH.get(praefix, "einkauf_eu"),
    }


def _anhang_haengen(nachricht: EmailMessage, pfad: str) -> None:
    typ = mimetypes.guess_type(pfad)[0] or "application/octet-stream"
    haupt, _, unter = typ.partition("/")
    with open(pfad, "rb") as f:
        nachricht.add_attachment(
            f.read(), maintype=haupt, subtype=unter, filename=os.path.basename(pfad)
        )


def senden_als(
    postfach: str,
    an: str | list[str],
    betreff: str,
    text: str,
    anhaenge: list[str] | None = None,
    cc: list[str] | None = None,
    trockenlauf: bool = False,
    config: dict | None = None,
) -> bool:
    """Schickt eine Mail aus dem genannten Postfach. trockenlauf=True zeigt sie nur an."""
    empfaenger = [an] if isinstance(an, str) else list(an)
    anhaenge = anhaenge or []

    fehlend = [p for p in anhaenge if not os.path.exists(p)]
    if fehlend:
        print("[POSTFACH] FEHLER: Anhang fehlt: " + ", ".join(fehlend))
        return False

    if trockenlauf:
        konto = {"adresse": f"<{postfach}>", "anzeigename": ""}
        try:
            konto = postfach_laden(postfach, config)
        except (FileNotFoundError, KeyError, ValueError) as fehler:
            print(f"[POSTFACH] (Trockenlauf, Konto noch nicht eingerichtet: {fehler})")
        print("=" * 72)
        print(f"Von:     {konto.get('anzeigename', '')} <{konto.get('adresse')}>")
        print(f"An:      {', '.join(empfaenger)}")
        if cc:
            print(f"Kopie:   {', '.join(cc)}")
        print(f"Betreff: {betreff}")
        print(f"Anhang:  {', '.join(os.path.basename(p) for p in anhaenge) or 'keiner'}")
        print("-" * 72)
        print(text)
        print("=" * 72)
        return True

    konto = postfach_laden(postfach, config)
    nachricht = EmailMessage()
    absender = konto["adresse"]
    if konto.get("anzeigename"):
        absender = f"{konto['anzeigename']} <{konto['adresse']}>"
    nachricht["From"] = absender
    nachricht["To"] = ", ".join(empfaenger)
    if cc:
        nachricht["Cc"] = ", ".join(cc)
    if konto.get("antwort_an"):
        nachricht["Reply-To"] = konto["antwort_an"]
    nachricht["Subject"] = betreff
    nachricht.set_content(text)
    for pfad in anhaenge:
        _anhang_haengen(nachricht, pfad)

    zeitlimit = int(konto.get("timeout_sekunden", 30))
    try:
        kontext = ssl.create_default_context()
        port = int(konto["smtp_port"])
        if port == 587:
            with smtplib.SMTP(konto["smtp_server"], port, timeout=zeitlimit) as smtp:
                smtp.starttls(context=kontext)
                smtp.login(konto["benutzer"], konto["passwort"])
                smtp.send_message(nachricht)
        else:
            with smtplib.SMTP_SSL(konto["smtp_server"], port, context=kontext, timeout=zeitlimit) as smtp:
                smtp.login(konto["benutzer"], konto["passwort"])
                smtp.send_message(nachricht)
    except smtplib.SMTPAuthenticationError:
        print(f"[POSTFACH] FEHLER: Anmeldung fuer {konto['adresse']} abgelehnt "
              "(App-Passwort falsch, oder SMTP im Postfach nicht freigeschaltet).")
        return False
    except Exception as fehler:
        print(f"[POSTFACH] FEHLER beim Senden: {fehler}")
        return False

    print(f"[POSTFACH] {konto['adresse']} -> {', '.join(empfaenger)}: {betreff}")
    return True


def posteingang(postfach: str, tage: int = 7, max_anzahl: int = 20,
                config: dict | None = None) -> list[dict]:
    """Liest die juengsten Antworten im Postfach (IMAP, nur lesend)."""
    konto = postfach_laden(postfach, config)
    seit = (__import__("datetime").date.today()
            - __import__("datetime").timedelta(days=tage)).strftime("%d-%b-%Y")
    treffer: list[dict] = []
    with imaplib.IMAP4_SSL(konto["imap_server"], int(konto["imap_port"])) as imap:
        imap.login(konto["benutzer"], konto["passwort"])
        imap.select("INBOX", readonly=True)
        _, daten = imap.search(None, f'(SINCE "{seit}")')
        nummern = daten[0].split()[-max_anzahl:]
        for nummer in reversed(nummern):
            _, roh = imap.fetch(nummer, "(RFC822)")
            nachricht = email.message_from_bytes(roh[0][1])
            koerper = ""
            if nachricht.is_multipart():
                for teil in nachricht.walk():
                    if teil.get_content_type() == "text/plain":
                        koerper = teil.get_payload(decode=True).decode(
                            teil.get_content_charset() or "utf-8", "replace")
                        break
            else:
                koerper = nachricht.get_payload(decode=True).decode(
                    nachricht.get_content_charset() or "utf-8", "replace")
            treffer.append({
                "von": str(make_header(decode_header(nachricht.get("From", "")))),
                "betreff": str(make_header(decode_header(nachricht.get("Subject", "")))),
                "datum": nachricht.get("Date", ""),
                "text": koerper.strip()[:2000],
            })
    return treffer


def _hauptprogramm() -> int:
    parser = argparse.ArgumentParser(description="Postfaecher der Einkaufsabteilungen")
    parser.add_argument("--test", metavar="POSTFACH", help="Testmail an das eigene Postfach")
    parser.add_argument("--senden", metavar="DATEI", help="Anfrage-Datei aus anfragen-*/ senden")
    parser.add_argument("--an", metavar="ADRESSE", help="Empfaenger fuer --senden")
    parser.add_argument("--postfach", metavar="NAME", help="Postfach abweichend vom Dateipraefix")
    parser.add_argument("--trocken", action="store_true", help="nur anzeigen, nicht senden")
    parser.add_argument("--posteingang", metavar="POSTFACH", help="Antworten lesen")
    parser.add_argument("--tage", type=int, default=7, help="Zeitraum fuer --posteingang")
    argumente = parser.parse_args()

    if argumente.test:
        konto = postfach_laden(argumente.test)
        erfolg = senden_als(
            argumente.test, konto["adresse"],
            "[Bellowerk] Testmail " + argumente.test,
            "Wenn diese Mail ankommt, kann die Abteilung selbst senden und empfangen.\n",
            trockenlauf=argumente.trocken,
        )
        return 0 if erfolg else 1

    if argumente.senden:
        if not argumente.an:
            print("--senden braucht --an ADRESSE")
            return 2
        anfrage = anfrage_lesen(argumente.senden)
        erfolg = senden_als(
            argumente.postfach or anfrage["postfach"], argumente.an,
            anfrage["betreff"], anfrage["text"], anfrage["anhaenge"],
            trockenlauf=argumente.trocken,
        )
        return 0 if erfolg else 1

    if argumente.posteingang:
        for eintrag in posteingang(argumente.posteingang, argumente.tage):
            print(f"--- {eintrag['datum']} | {eintrag['von']}\n{eintrag['betreff']}\n")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(_hauptprogramm())
