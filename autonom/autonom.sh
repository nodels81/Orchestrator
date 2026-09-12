#!/usr/bin/env bash
#
# autonom.sh — Macht aus dem Orchestrator einen Dauerbetrieb.
#
# Nach diesem Skript laeuft der Betrieb 24/7 auf dem Server, unabhaengig davon,
# ob Bjoerns Rechner an ist:
#   bello-lauf          alle zwei Stunden Auftraege abarbeiten
#   bello-tagesbrief    07:00 die Morgenmail
#   bello-posteingang   alle 5 Minuten das Postfach lesen und handeln
#   bello-waechter      stuendlich pruefen, ob das alles wirklich laeuft
#
# Was dieses Skript NICHT anfasst, aus demselben Grund wie uebernahme.sh:
#   orchestrator.py    enthaelt das Abteilungsverzeichnis (Server kennt 07-10)
#   abteilung_web.py   waere eine zweite Web-Abteilung neben 10 Homepage
#   markenwissen.py    kann auf dem Server geaendert worden sein
#   config.json        Geheimnisse — wird nur gelesen, und nur nach Rueckfrage ergaenzt
#
# Aufruf auf dem Server, als root, NACH sicherung.sh:
#   cd /opt/bello && bash autonom/autonom.sh
#
# Rueckbau jederzeit:
#   bash autonom/autonom.sh --entfernen

set -euo pipefail

PFAD="${PFAD:-$PWD}"
EINHEITEN="/etc/systemd/system"
DIENSTE=(lauf tagesbrief posteingang waechter)

rot()  { printf '\033[31m%s\033[0m\n' "$*"; }
fett() { printf '\033[1m%s\033[0m\n' "$*"; }

# --- Rueckbau ------------------------------------------------------------
if [ "${1:-}" = "--entfernen" ]; then
  fett "=== Autonom-Betrieb abbauen ==="
  for name in "${DIENSTE[@]}"; do
    systemctl disable --now "bello-${name}.timer" 2>/dev/null || true
    rm -f "$EINHEITEN/bello-${name}.timer" "$EINHEITEN/bello-${name}.service"
    echo "  entfernt: bello-${name}"
  done
  systemctl daemon-reload
  echo
  echo "Abgebaut. config.json, auftraege.json und logs/ sind unberuehrt."
  exit 0
fi

fett "=== Autonom-Betrieb einrichten ==="
echo

# --- Vorbedingungen ------------------------------------------------------
[ "$(id -u)" -eq 0 ] || { rot "FEHLER: Muss als root laufen (systemd-Einheiten schreiben)."; exit 1; }
command -v systemctl >/dev/null || { rot "FEHLER: Kein systemd auf diesem Server."; exit 1; }

cd "$PFAD"
[ -f orchestrator.py ] || { rot "FEHLER: $PFAD ist nicht der Betriebsordner (orchestrator.py fehlt)."; exit 1; }
[ -d autonom/systemd ] || { rot "FEHLER: autonom/systemd fehlt. Erst uebernahme.sh laufen lassen."; exit 1; }

PYTHON="$PFAD/venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  rot "FEHLER: $PYTHON fehlt."
  echo "        Anlegen mit:  python3 -m venv venv && venv/bin/pip install anthropic"
  exit 1
fi

if [ ! -f config.json ]; then
  rot "FEHLER: config.json fehlt. Vorlage: config.beispiel.json"
  exit 1
fi

# --- Sicherung muss frisch sein, wie bei uebernahme.sh --------------------
SICHERUNGSORDNER="${SICHERUNG_ZIEL:-/opt/bello-sicherungen}"
NEUESTE="$(find "$SICHERUNGSORDNER" -maxdepth 1 -name 'bello-*.tar.gz' -mmin -1440 2>/dev/null | sort | tail -1 || true)"
if [ -z "$NEUESTE" ]; then
  rot "FEHLER: In $SICHERUNGSORDNER liegt kein Archiv aus den letzten 24 Stunden."
  echo "        Erst sichern:  bash sicherung.sh"
  exit 1
fi
echo "Sicherung gefunden: $NEUESTE"

# --- Wem gehoert der Ordner ----------------------------------------------
BENUTZER="$(stat -c '%U' orchestrator.py)"
echo "Dienste laufen als Benutzer: $BENUTZER"
mkdir -p logs
chown -R "$BENUTZER" logs

# --- config.json: Abschnitt autonom --------------------------------------
echo
echo "Pruefe config.json ..."
FEHLEND="$("$PYTHON" - <<'PYENDE'
import json, sys
try:
    with open("config.json", encoding="utf-8") as f:
        c = json.load(f)
except Exception as fehler:
    print(f"UNLESBAR:{fehler}"); sys.exit(0)
mangel = []
mail = c.get("mail", {})
for feld in ("absender", "app_passwort", "empfaenger"):
    if not mail.get(feld):
        mangel.append(f"mail.{feld}")
if not c.get("anthropic_api_key"):
    mangel.append("anthropic_api_key")
if not c.get("autonom", {}).get("kennwort"):
    mangel.append("autonom.kennwort")
print(",".join(mangel))
PYENDE
)"

case "$FEHLEND" in
  UNLESBAR:*) rot "FEHLER: config.json ist kein gueltiges JSON — ${FEHLEND#UNLESBAR:}"; exit 1 ;;
esac

if [[ "$FEHLEND" == *"autonom.kennwort"* ]]; then
  KENNWORT="$("$PYTHON" -c 'import secrets; print(secrets.token_urlsafe(9))')"
  echo
  echo "Der Posteingang braucht ein Kennwort. Es muss in jedem Betreff stehen,"
  echo "den du an den Orchestrator schickst. Ein Absender allein schuetzt nicht,"
  echo "weil das Feld From faelschbar ist."
  echo
  echo "  Vorschlag: $KENNWORT"
  echo
  read -r -p "In config.json eintragen? Nur 'ja' traegt ein: " ANTWORT
  if [ "$ANTWORT" = "ja" ]; then
    cp config.json "config.json.vor-autonom-$(date +%Y%m%d-%H%M%S)"
    KENNWORT="$KENNWORT" "$PYTHON" - <<'PYENDE'
import json, os
with open("config.json", encoding="utf-8") as f:
    c = json.load(f)
c.setdefault("autonom", {})
c["autonom"]["kennwort"] = os.environ["KENNWORT"]
c["autonom"].setdefault("imap_server", "imap.gmail.com")
c["autonom"].setdefault("imap_port", 993)
with open("config.json.tmp", "w", encoding="utf-8") as f:
    json.dump(c, f, indent=2, ensure_ascii=False)
os.replace("config.json.tmp", "config.json")
print("  Eingetragen.")
PYENDE
    chmod 600 config.json
    chown "$BENUTZER" config.json
    echo
    fett "  MERKEN: $KENNWORT"
    echo "  Steht ab jetzt auch in config.json. Nicht per Mail verschicken."
    FEHLEND="${FEHLEND//autonom.kennwort/}"
  else
    echo "  Uebersprungen. Der Posteingang bleibt dann abgeschaltet."
  fi
fi

RESTMANGEL="$(echo "$FEHLEND" | tr ',' '\n' | grep -v '^$' || true)"
if [ -n "$RESTMANGEL" ]; then
  echo
  rot "In config.json fehlt noch:"
  echo "$RESTMANGEL" | sed 's/^/    /'
  echo "  Die Dienste werden trotzdem eingerichtet, melden aber Fehler, bis das steht."
fi

# --- Einheiten schreiben -------------------------------------------------
echo
echo "Schreibe systemd-Einheiten nach $EINHEITEN ..."

# ProtectHome sperrt /home und /root. Liegt der Betrieb dort, muss es aus.
SCHUTZ_HOME="true"
case "$PFAD" in
  /home/*|/root*) SCHUTZ_HOME="false"
                  echo "  Hinweis: $PFAD liegt unter /home oder /root, ProtectHome wird abgeschaltet." ;;
esac

for name in "${DIENSTE[@]}"; do
  for art in service timer; do
    quelle="autonom/systemd/bello-${name}.${art}"
    [ -f "$quelle" ] || { rot "FEHLER: $quelle fehlt."; exit 1; }
    sed -e "s|@PFAD@|$PFAD|g" \
        -e "s|@BENUTZER@|$BENUTZER|g" \
        -e "s|^ProtectHome=true$|ProtectHome=$SCHUTZ_HOME|" \
        "$quelle" > "$EINHEITEN/bello-${name}.${art}"
  done
  echo "  bello-${name}.service + .timer"
done

systemctl daemon-reload

# --- Alte Cron-Eintraege melden, nicht heimlich loeschen -----------------
for wessen in root "$BENUTZER"; do
  TREFFER="$(crontab -l -u "$wessen" 2>/dev/null | grep 'tagesbrief\.py' || true)"
  if [ -n "$TREFFER" ]; then
    echo
    rot "ACHTUNG: Im Cron von $wessen steht noch ein Eintrag fuer tagesbrief.py."
    echo "         Sonst kommt die Morgenmail doppelt. Entfernen mit: crontab -e -u $wessen"
    echo "$TREFFER" | sed 's/^/         /'
  fi
done

# --- Anwerfen ------------------------------------------------------------
echo
echo "Starte die Zeitgeber ..."
GESCHEITERT=0
for name in "${DIENSTE[@]}"; do
  if systemctl enable --now "bello-${name}.timer" >/dev/null 2>&1; then
    echo "  bello-${name}.timer aktiv"
  else
    rot "  bello-${name}.timer liess sich nicht starten"
    systemctl status "bello-${name}.timer" --no-pager -n 5 2>&1 | sed 's/^/      /' || true
    GESCHEITERT=1
  fi
done
if [ "$GESCHEITERT" -eq 1 ]; then
  echo
  rot "Mindestens ein Zeitgeber laeuft nicht. Die Einheiten liegen in $EINHEITEN."
  echo "Ursache suchen mit:  journalctl -xe"
  exit 1
fi

echo
fett "=== Eingerichtet ==="
systemctl list-timers 'bello-*' --no-pager || true

cat <<'ABSCHLUSS'

Naechste Schritte, in dieser Reihenfolge:

  1. Mailweg pruefen (sendet eine Testmail):
       venv/bin/python orchestrator_mail.py --test

  2. Posteingang trocken pruefen (liest, fuehrt nichts aus):
       venv/bin/python autonom/posteingang.py --probe

  3. Waechter trocken pruefen:
       venv/bin/python autonom/waechter.py --probe

  4. Vom Handy eine Mail an die Orchestrator-Adresse schicken.
     Betreff: irgendwas, in dem das Kennwort vorkommt
     Text, erste Zeile:  stand
     Innerhalb von fuenf Minuten kommt die Antwort zurueck.

Nachsehen, wenn etwas klemmt:
       systemctl list-timers 'bello-*'
       journalctl -u bello-lauf.service -n 50
       tail -40 logs/posteingang.log

Abbauen:
       bash autonom/autonom.sh --entfernen
ABSCHLUSS
