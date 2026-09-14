#!/usr/bin/env bash
# mailpasswort.sh — neues Gmail-App-Passwort eintragen, ohne dass es auf dem
# Bildschirm erscheint.
#
# Google zeigt App-Passwoerter als "abcd efgh ijkl mnop". Die Leerzeichen sind
# nur Lesehilfe und muessen weg; das ist die haeufigste Ursache fuer ein
# "Invalid credentials" direkt nach dem Anlegen.
#
#   sudo bash autonom/mailpasswort.sh

set -euo pipefail

PFAD="${PFAD:-$PWD}"
cd "$PFAD"

rot()  { printf '\033[31m%s\033[0m\n' "$*"; }
fett() { printf '\033[1m%s\033[0m\n' "$*"; }

[ -f config.json ] || { rot "FEHLER: config.json nicht in $PFAD."; exit 1; }

PYTHON=""
for kandidat in "$PFAD/.venv/bin/python" "$PFAD/venv/bin/python"; do
  [ -x "$kandidat" ] && { PYTHON="$kandidat"; break; }
done
[ -n "$PYTHON" ] || { rot "FEHLER: Kein Python im Betriebsordner gefunden."; exit 1; }

KONTO="$("$PYTHON" -c 'import json;print((json.load(open("config.json")).get("mail") or {}).get("absender",""))')"
[ -n "$KONTO" ] || { rot "FEHLER: mail.absender steht nicht in config.json."; exit 1; }

# --- Sonderfall: das Passwort steht schon da, nur an der falschen Stelle ---
# mailin.py und posteingang.py lesen config.json zuerst und die Umgebung nur
# ersatzweise. Steht in config.json ein veralteter Wert, kommen sie nie bis
# /etc/bello/env -- und melden "Invalid credentials", obwohl das gueltige
# Passwort auf der Platte liegt.
if [ "${1:-}" = "--aus-env" ]; then
  ENVDATEI="/etc/bello/env"
  [ -r "$ENVDATEI" ] || { rot "FEHLER: $ENVDATEI nicht lesbar (sudo?)."; exit 1; }
  PASSWORT="$(sed -n 's/^SMTP_PASSWORT=//p' "$ENVDATEI" | tail -1)"
  PASSWORT="${PASSWORT%\"}"; PASSWORT="${PASSWORT#\"}"
  PASSWORT="${PASSWORT%\'}"; PASSWORT="${PASSWORT#\'}"
  PASSWORT="${PASSWORT//[[:space:]]/}"
  [ -n "$PASSWORT" ] || { rot "FEHLER: SMTP_PASSWORT steht nicht in $ENVDATEI."; exit 1; }
  fett "=== Passwort aus $ENVDATEI pruefen ==="
  echo "  Konto:  $KONTO"
  echo "  Laenge: ${#PASSWORT} Zeichen (der Wert selbst wird nicht angezeigt)"
  echo
else

fett "=== App-Passwort fuer $KONTO ==="
echo
echo "Vorher im Google-Konto von $KONTO anlegen:"
echo "  myaccount.google.com  ->  Sicherheit  ->  App-Passwoerter"
echo "  (setzt Bestaetigung in zwei Schritten voraus)"
echo
echo "Die Eingabe bleibt unsichtbar. Leerzeichen darfst du mittippen,"
echo "sie werden entfernt."
echo

read -r -s -p "Neues App-Passwort: " EINGABE; echo
read -r -s -p "Zur Sicherheit noch einmal: " EINGABE2; echo
[ "$EINGABE" = "$EINGABE2" ] || { rot "FEHLER: Die beiden Eingaben sind nicht gleich."; exit 1; }

PASSWORT="${EINGABE//[[:space:]]/}"
[ -n "$PASSWORT" ] || { rot "FEHLER: Leere Eingabe."; exit 1; }
if [ "${#PASSWORT}" -ne 16 ]; then
  echo
  rot "Achtung: Google-App-Passwoerter haben 16 Zeichen, deins hat ${#PASSWORT}."
  read -r -p "Trotzdem eintragen? Nur 'ja': " WEITER
  [ "$WEITER" = "ja" ] || exit 1
fi

fi  # Ende --aus-env

echo
echo "Anmeldung wird zuerst geprueft, bevor irgendetwas geschrieben wird ..."
if ! PASSWORT="$PASSWORT" KONTO="$KONTO" "$PYTHON" - <<'PYENDE'
import imaplib, json, os, sys
c = json.load(open("config.json", encoding="utf-8"))
a = c.get("autonom") or {}
server = a.get("imap_server", "imap.gmail.com")
port = int(a.get("imap_port", 993))
try:
    imap = imaplib.IMAP4_SSL(server, port, timeout=30)
    imap.login(os.environ["KONTO"], os.environ["PASSWORT"])
    imap.select("INBOX")
    imap.logout()
except Exception as fehler:
    print(f"  Abgelehnt: {fehler}")
    sys.exit(1)
print(f"  Anmeldung bei {server} erfolgreich.")
PYENDE
then
  echo
  rot "Nicht eingetragen — config.json ist unveraendert."
  echo "Haeufigste Ursachen: Passwort fuer das falsche Konto angelegt,"
  echo "oder es wurde inzwischen wieder zurueckgezogen."
  exit 1
fi

SICHERUNG="config.json.vor-mailpasswort-$(date +%Y%m%d-%H%M%S)"
cp config.json "$SICHERUNG"
BESITZER="$(stat -c '%U:%G' config.json)"

PASSWORT="$PASSWORT" "$PYTHON" - <<'PYENDE'
import json, os
with open("config.json", encoding="utf-8") as f:
    c = json.load(f)
c.setdefault("mail", {})["app_passwort"] = os.environ["PASSWORT"]
with open("config.json.tmp", "w", encoding="utf-8") as f:
    json.dump(c, f, indent=2, ensure_ascii=False)
os.replace("config.json.tmp", "config.json")
PYENDE
chmod 600 config.json
chown "$BESITZER" config.json
echo "  config.json aktualisiert (vorher: $SICHERUNG)"

# Manche Dienste ziehen das Passwort aus /etc/bello/env statt aus config.json.
# Steht es dort, muss es mitwandern, sonst laeuft die Haelfte weiter ins Leere.
ENVDATEI="/etc/bello/env"
if [ -w "$ENVDATEI" ] && grep -q '^SMTP_PASSWORT=' "$ENVDATEI"; then
  cp "$ENVDATEI" "$ENVDATEI.vor-mailpasswort-$(date +%Y%m%d-%H%M%S)"
  umask 077
  PASSWORT="$PASSWORT" "$PYTHON" - "$ENVDATEI" <<'PYENDE'
import os, sys
pfad = sys.argv[1]
zeilen = open(pfad, encoding="utf-8").read().splitlines(keepends=True)
neu = []
for z in zeilen:
    if z.startswith("SMTP_PASSWORT="):
        neu.append(f"SMTP_PASSWORT={os.environ['PASSWORT']}\n")
    else:
        neu.append(z)
open(pfad + ".tmp", "w", encoding="utf-8").writelines(neu)
os.replace(pfad + ".tmp", pfad)
PYENDE
  chmod 600 "$ENVDATEI"
  echo "  $ENVDATEI aktualisiert"
fi

echo
fett "=== Fertig ==="
echo "Gegenprobe, beide Dienste:"
echo "  sudo -u bello $PYTHON mailin.py --test-imap"
echo "  sudo -u bello $PYTHON autonom/posteingang.py --probe"
echo
echo "Danach die Dienste einmal von Hand anstossen, statt auf den Timer zu warten:"
echo "  sudo systemctl start bello-posteingang.service"
