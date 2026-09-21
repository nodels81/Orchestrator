"""
orchestrator_mail.py — Verschickt Eskalationsmails per SMTP.

Absender und Empfaenger MUESSEN verschiedene Konten sein, sonst unterdrueckt
Gmail die Handy-Benachrichtigung.

Test:  venv/bin/python orchestrator_mail.py --test
"""

import smtplib
import ssl
import sys
from email.message import EmailMessage

from abteilung_basis import config_laden


def _senden(empfaenger: str, betreff: str, text: str, config: dict,
            cc: str | None = None) -> bool:
    mail = config.get("mail", {})

    absender = mail.get("absender")
    passwort = mail.get("app_passwort")
    server = mail.get("smtp_server", "smtp.gmail.com")
    port = int(mail.get("smtp_port", 465))

    if not (absender and passwort and empfaenger):
        print("[MAIL] Nicht konfiguriert — Nachricht nur im Log:")
        print(f"       An: {empfaenger}\n       {betreff}\n{text}")
        return False

    nachricht = EmailMessage()
    nachricht["From"] = absender
    nachricht["To"] = empfaenger
    if cc:
        nachricht["Cc"] = cc
    nachricht["Subject"] = betreff
    nachricht.set_content(text)

    zeitlimit = int(mail.get("timeout_sekunden", 20))
    try:
        kontext = ssl.create_default_context()
        with smtplib.SMTP_SSL(server, port, context=kontext, timeout=zeitlimit) as smtp:
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


def senden(betreff: str, text: str, config: dict | None = None) -> bool:
    """Eskalation an Bjoern."""
    config = config or config_laden()
    empfaenger = config.get("mail", {}).get("empfaenger")
    return _senden(empfaenger, betreff, text, config)


def senden_lieferant(empfaenger: str, betreff: str, text: str,
                      config: dict | None = None) -> bool:
    """Sendet direkt an einen Lieferanten. Bjoern steht in Cc, damit jede
    ausgehende Nachricht bei ihm ankommt, ohne dass er sie selbst verschicken muss."""
    config = config or config_laden()
    cc = config.get("mail", {}).get("empfaenger")
    return _senden(empfaenger, betreff, text, config, cc=cc)


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
