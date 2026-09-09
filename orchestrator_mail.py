"""
orchestrator_mail.py — Verschickt Eskalationsmails per SMTP.

Absender und Empfaenger MUESSEN verschiedene Konten sein, sonst unterdrueckt
Gmail die Handy-Benachrichtigung.

Test:  venv/bin/python orchestrator_mail.py --test
"""

import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

from abteilung_basis import config_laden


def senden(betreff: str, text: str, config: dict | None = None) -> bool:
    config = config or config_laden()
    mail = config.get("mail", {})

    absender = mail.get("absender")
    passwort = mail.get("app_passwort")
    empfaenger = mail.get("empfaenger")
    server = mail.get("smtp_server", "smtp.gmail.com")
    passwort = passwort or os.environ.get("SMTP_PASSWORT")
    port = int(mail.get("smtp_port", 587))

    if not (absender and passwort and empfaenger):
        print("[MAIL] Nicht konfiguriert — Eskalation nur im Log:")
        print(f"       {betreff}\n{text}")
        return False

    nachricht = EmailMessage()
    nachricht["From"] = absender
    nachricht["To"] = empfaenger
    nachricht["Subject"] = betreff
    nachricht["Date"] = formatdate(localtime=True)
    nachricht["Message-ID"] = make_msgid(domain="gmail.com")
    nachricht["Reply-To"] = absender
    nachricht.set_content(text)

    zeitlimit = int(mail.get("timeout_sekunden", 20))
    try:
        kontext = ssl.create_default_context()
        if port == 465:
            with smtplib.SMTP_SSL(server, port, context=kontext, timeout=zeitlimit) as smtp:
                smtp.login(absender, passwort)
                smtp.send_message(nachricht)
        else:
            with smtplib.SMTP(server, port, timeout=zeitlimit) as smtp:
                smtp.ehlo()
                smtp.starttls(context=kontext)
                smtp.ehlo()
                smtp.login(absender, passwort)
                smtp.send_message(nachricht)
        print(f"[MAIL] Gesendet an {empfaenger}: {betreff}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("[MAIL] FEHLER: App-Passwort falsch oder 2FA im Absenderkonto aus.")
        return False
    except Exception as fehler:
        print(f"[MAIL] FEHLER: {fehler}")
        return False


if __name__ == "__main__":
    if "--test" in sys.argv:
        erfolg = senden(
            "[Bello] Testmail",
            "Wenn diese Mail ankommt, funktioniert der Eskalationskanal.\n"
            "Absender und Empfaenger sind verschiedene Konten — die "
            "Handy-Benachrichtigung sollte durchkommen.",
        )
        sys.exit(0 if erfolg else 1)
    print('Aufruf: python orchestrator_mail.py --test')
