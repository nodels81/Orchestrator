#!/usr/bin/env python3
"""KAS-API von All-Inkl: den Webspace lesen und einrichten, ohne Klicken.

Läuft auf dem netcup-Server, nicht auf dem Webspace. Zugangsdaten kommen aus
/etc/bello/kas.env und stehen nirgends sonst — nicht in diesem Repo, nicht in
einem Chat, nicht in der Ausgabe.

    venv/bin/python web/betrieb/kas.py --stand
    venv/bin/python web/betrieb/kas.py --einrichten            # zeigt nur, was es täte
    venv/bin/python web/betrieb/kas.py --einrichten --wirklich # legt an

Ohne --wirklich wird nichts angelegt. Das ist Absicht: der erste Lauf gegen ein
fremdes System ist ein Lauf zum Zusehen.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

AUTH_WSDL = "https://kasapi.kasserver.com/soap/wsdl/KasAuth.wsdl"
API_WSDL = "https://kasapi.kasserver.com/soap/wsdl/KasApi.wsdl"

ZUGANG = Path("/etc/bello/kas.env")

# Was der Shop braucht. Namen bewusst sprechend, damit im KAS später jeder
# Eintrag erklärt, wozu er da ist.
PLAN = {
    "subdomain": "bau",
    "datenbank_kommentar": "bellowerk-shop",
    "ftp_kommentar": "bellowerk-aufspielen",
    "postfach": "info",
}

# Nur lesende Aufrufe. Die sind belegt und können nichts kaputtmachen.
LESEN = [
    ("Konto", "get_accountressources", {}),
    ("Domains", "get_domains", {}),
    ("Subdomains", "get_subdomains", {}),
    ("Datenbanken", "get_databases", {}),
    ("FTP-Zugänge", "get_ftpusers", {}),
    ("Postfächer", "get_mailaccounts", {}),
    ("DNS", "get_dns_settings", {}),
]


def zugangsdaten(pfad=ZUGANG):
    """KAS_USER und KAS_PASSWORD aus einer Datei lesen, die nur root gehört."""
    if not pfad.exists():
        raise SystemExit(
            f"{pfad} fehlt. Anlegen mit:\n"
            f"  install -m 600 /dev/null {pfad}\n"
            f"  printf 'KAS_USER=w01xxxxx\\nKAS_PASSWORD=...\\n' > {pfad}\n"
            "Die Datei gehört root, wird nie eingecheckt und nie angezeigt."
        )
    if pfad.stat().st_mode & 0o077:
        raise SystemExit(f"{pfad} ist zu offen. chmod 600 {pfad}")

    werte = {}
    for zeile in pfad.read_text().splitlines():
        zeile = zeile.strip()
        if not zeile or zeile.startswith("#") or "=" not in zeile:
            continue
        schluessel, _, wert = zeile.partition("=")
        werte[schluessel.strip()] = wert.strip().strip("\"'")

    fehlt = {"KAS_USER", "KAS_PASSWORD"} - werte.keys()
    if fehlt:
        raise SystemExit(f"In {pfad} fehlt: {', '.join(sorted(fehlt))}")
    return werte["KAS_USER"], werte["KAS_PASSWORD"]


def _client(wsdl):
    try:
        from zeep import Client
    except ImportError:
        raise SystemExit("zeep fehlt:  venv/bin/pip install zeep")
    return Client(wsdl)


def anmelden(benutzer, passwort, dauer=1800):
    """Sitzungsschlüssel holen. Das Kennwort geht nur als SHA1 über die Leitung."""
    antwort = _client(AUTH_WSDL).service.KasAuth(
        Params=json.dumps(
            {
                "KasUser": benutzer,
                "KasAuthType": "sha1",
                "KasPassword": hashlib.sha1(passwort.encode()).hexdigest(),
                "SessionLifeTime": dauer,
                "SessionUpdateLifeTime": "N",
            }
        )
    )
    return antwort


def ruf(benutzer, sitzung, art, params=None):
    antwort = _client(API_WSDL).service.KasApi(
        Params=json.dumps(
            {
                "KasUser": benutzer,
                "KasAuthType": "session",
                "KasAuthData": sitzung,
                "KasRequestType": art,
                "KasRequestParams": params or {},
            }
        )
    )
    if isinstance(antwort, dict):
        return antwort.get("Response", {}).get("ReturnInfo", antwort)
    return antwort


def stand(benutzer, sitzung):
    for titel, art, params in LESEN:
        print(f"\n=== {titel} ({art}) ===")
        try:
            ergebnis = ruf(benutzer, sitzung, art, params)
        except Exception as fehler:  # die API meldet Unbekanntes deutlich
            print(f"  nicht abrufbar: {fehler}")
            continue
        if not ergebnis:
            print("  (leer)")
            continue
        print(json.dumps(ergebnis, indent=2, ensure_ascii=False, default=str))


def einrichten(benutzer, sitzung, domain, wirklich):
    """Datenbank, Baustellen-Subdomain, FTP-Zugang und Postfach anlegen.

    Die Parameternamen stehen in der KAS-Dokumentation unter
    kasapi.kasserver.com/dokumentation/. Vom Bau-Rechner aus ist sie nicht
    erreichbar, deshalb läuft dieser Teil erst trocken und meldet, was er
    vorhat — auf dem Server wird er gegen die Doku bestätigt.
    """
    schritte = [
        (
            "Datenbank für den Shop",
            "add_database",
            {"database_password": "<erzeugt>", "database_comment": PLAN["datenbank_kommentar"]},
        ),
        (
            f"Baustellen-Subdomain {PLAN['subdomain']}.{domain}",
            "add_subdomain",
            {"subdomain": PLAN["subdomain"], "domain_name": domain, "php_version": "8.3"},
        ),
        (
            "FTP-Zugang nur fürs Aufspielen",
            "add_ftpuser",
            {"ftp_password": "<erzeugt>", "ftp_comment": PLAN["ftp_kommentar"]},
        ),
        (
            f"Postfach {PLAN['postfach']}@{domain}",
            "add_mailaccount",
            {"mail_password": "<erzeugt>", "local_part": PLAN["postfach"], "domain_part": domain},
        ),
    ]

    for titel, art, params in schritte:
        if not wirklich:
            print(f"[Probe] {titel}\n        {art} {json.dumps(params, ensure_ascii=False)}")
            continue
        print(f"[Anlegen] {titel} … ", end="", flush=True)
        try:
            ruf(benutzer, sitzung, art, params)
            print("fertig")
        except Exception as fehler:
            print(f"abgebrochen: {fehler}")
            print("  Nichts Weiteres angelegt. Erst diesen Schritt klären.")
            return 1

    if not wirklich:
        print("\nNichts angelegt. Mit --wirklich ausführen, wenn das oben stimmt.")
    return 0


def main():
    p = argparse.ArgumentParser(description="KAS-API von All-Inkl")
    p.add_argument("--stand", action="store_true", help="Konto auslesen, nichts ändern")
    p.add_argument("--einrichten", action="store_true", help="Shop-Bausteine anlegen")
    p.add_argument("--wirklich", action="store_true", help="wirklich schreiben")
    p.add_argument("--domain", default="bellowerk.de")
    args = p.parse_args()

    if not (args.stand or args.einrichten):
        p.print_help()
        return 2

    benutzer, passwort = zugangsdaten()
    sitzung = anmelden(benutzer, passwort)
    print(f"Angemeldet als {benutzer}.")

    if args.stand:
        stand(benutzer, sitzung)
    if args.einrichten:
        return einrichten(benutzer, sitzung, args.domain, args.wirklich)
    return 0


if __name__ == "__main__":
    sys.exit(main())
