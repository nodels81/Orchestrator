#!/bin/bash
# telegram-einrichten.sh — verbindet Gustav mit Telegram.
#
# Vorher, einmal am Handy: beim @BotFather einen Bot anlegen und den Token
# bereithalten (TELEGRAM.md, Schritt 1). Alles andere erledigt dieses Skript:
#
#   1. prueft die Voraussetzungen
#   2. fragt den Token ab und prueft ihn bei Telegram
#   3. erkennt dein Telegram-Konto — du schreibst dem Bot einmal "hallo"
#   4. traegt beides in /etc/bello/env ein (nur root lesbar), in config.json
#      nur den Verweis darauf
#   5. richtet den Dienst bello-telegram und den Sofortstart ein
#   6. schickt dir zur Probe eine Nachricht aufs Handy
#
#   cd /opt/bello && sudo git pull && sudo bash bin/telegram-einrichten.sh
#
# Kann beliebig oft laufen und aendert dann nur, was fehlt. Vor jeder Aenderung
# eine Sicherung von /etc/bello/env und config.json. Oeffnet keinen Port.
#
#   --pruefen    nur nachsehen, nichts aendern
#   --neu        neuen Token und neues Konto eintragen (z. B. nach /revoke)
#   --entfernen  alles wieder ausbauen
set -uo pipefail

BASIS=/opt/bello
ENV_DATEI=/etc/bello/env
PY="$BASIS/.venv/bin/python"
UNITS=/etc/systemd/system
DROPIN="$UNITS/bello-orchestrator.service.d/telegram.conf"
STEMPEL=$(date +%Y%m%d-%H%M%S)
MODUS="${1:-}"
fehler=0

meldung(){ printf '\n\033[1m%s\033[0m\n' "$*"; }
gut(){ printf '  ok   %s\n' "$*"; }
schlecht(){ printf '  FEHL %s\n' "$*"; fehler=$((fehler+1)); }
hinweis(){ printf '  --   %s\n' "$*"; }

[ "$(id -u)" -eq 0 ] || { echo "Bitte als root ausfuehren: sudo bash bin/telegram-einrichten.sh"; exit 1; }
cd "$BASIS" || { echo "$BASIS nicht gefunden."; exit 1; }

# ---------- Hilfen ----------

env_wert(){   # NAME -> Wert aus /etc/bello/env (ohne umschliessende Anfuehrungszeichen)
  sed -n "s/^$1=//p" "$ENV_DATEI" 2>/dev/null | tail -n 1 | sed -e 's/^"\(.*\)"$/\1/' -e "s/^'\(.*\)'$/\1/"
}

sichern(){    # einmal pro Lauf, und nur wenn wirklich etwas geaendert wird
  [ -n "${GESICHERT:-}" ] && return
  cp -a "$ENV_DATEI" "$ENV_DATEI.bak-$STEMPEL" 2>/dev/null
  cp -a config.json "config.json.bak-$STEMPEL"
  GESICHERT=1
  gut "Sicherung: $ENV_DATEI.bak-$STEMPEL und config.json.bak-$STEMPEL"
}

env_setzen(){ # NAME WERT — ersetzt die Zeile oder haengt sie an; Rechte bleiben
  local tmp
  sichern
  tmp=$(mktemp) || return 1
  grep -v "^$1=" "$ENV_DATEI" > "$tmp" 2>/dev/null
  printf '%s=%s\n' "$1" "$2" >> "$tmp"
  cat "$tmp" > "$ENV_DATEI" && rm -f "$tmp"
}

env_loeschen(){
  local tmp
  grep -q "^$1=" "$ENV_DATEI" 2>/dev/null || return 0
  sichern
  tmp=$(mktemp) || return 1
  grep -v "^$1=" "$ENV_DATEI" > "$tmp"
  cat "$tmp" > "$ENV_DATEI" && rm -f "$tmp"
}

als_bello(){  # laeuft als Betriebsnutzer, mit der Umgebung dieses Skripts
  runuser -u bello --preserve-environment -- "$@"
}

token_pruefen(){  # TOKEN -> "@botname" oder Grund; Rueckgabe 0 = gueltig
  TELEGRAM_BOT_TOKEN="$1" als_bello "$PY" bin/telegram_bot.py --ich 2>&1 | tail -n 1
  return "${PIPESTATUS[0]}"
}

telegram_block(){  # hinein | heraus | da?
  AKTION="$1" "$PY" - <<'PY'
import json, os, sys
pfad = "/opt/bello/config.json"
with open(pfad, encoding="utf-8") as f:
    config = json.load(f)
aktion = os.environ["AKTION"]
da = isinstance(config.get("telegram"), dict)
if aktion == "da?":
    sys.exit(0 if da else 1)
if aktion == "hinein" and da:
    print("  ok   Block \"telegram\" in config.json ist schon da — bleibt, wie er ist")
    sys.exit(0)
if aktion == "heraus" and not da:
    sys.exit(0)
if aktion == "hinein":
    # Nur Verweise: die Werte selbst bleiben in /etc/bello/env.
    config["telegram"] = {"bot_token": "${TELEGRAM_BOT_TOKEN}", "chat_id": "${TELEGRAM_CHAT_ID}"}
else:
    config.pop("telegram")
temp = pfad + ".tmp"
with open(temp, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)
    f.write("\n")
stat = os.stat(pfad)
os.chmod(temp, stat.st_mode & 0o7777)
os.chown(temp, stat.st_uid, stat.st_gid)
os.replace(temp, pfad)
print("  ok   Block \"telegram\" in config.json " + ("eingetragen (nur Verweise)" if aktion == "hinein" else "entfernt"))
PY
}

lauf_liest_env(){
  systemctl cat bello-orchestrator.service 2>/dev/null | grep -Eq "^EnvironmentFile=-?$ENV_DATEI\$"
}

stand_zeigen(){
  local token konto name
  token=$(env_wert TELEGRAM_BOT_TOKEN)
  konto=$(env_wert TELEGRAM_CHAT_ID)
  if [ -z "$token" ]; then schlecht "kein Token in $ENV_DATEI"
  elif name=$(token_pruefen "$token"); then gut "Token gilt: $name"
  else schlecht "Telegram lehnt den Token ab: $name"; fi
  [ -n "$konto" ] && gut "freigeschaltetes Konto: $konto" || schlecht "kein Konto in $ENV_DATEI (TELEGRAM_CHAT_ID)"
  telegram_block "da?" && gut "config.json hat den Block \"telegram\"" || schlecht "config.json ohne Block \"telegram\""
  lauf_liest_env && gut "der Lauf liest $ENV_DATEI — Ergebnisse kommen aufs Handy" \
    || schlecht "der Lauf liest $ENV_DATEI nicht — Ergebnisse kaemen nur per Mail"
  systemctl is-active --quiet bello-telegram.service && gut "bello-telegram laeuft" || schlecht "bello-telegram laeuft nicht"
  systemctl is-active --quiet bello-orchestrator-anstoss.path && gut "Sofortstart bereit" || schlecht "Sofortstart nicht aktiv"
  echo
  echo "  Letzte Meldungen des Bots:"
  journalctl -u bello-telegram.service -n 6 --no-pager -o cat 2>/dev/null | sed 's/^/    /'
}

# ---------- Nur nachsehen ----------

if [ "$MODUS" = "--pruefen" ]; then
  meldung "Stand der Telegram-Anbindung"
  stand_zeigen
  exit $(( fehler > 0 ))
fi

# ---------- Rueckbau ----------

if [ "$MODUS" = "--entfernen" ]; then
  meldung "Rueckbau der Telegram-Anbindung"
  systemctl disable --now bello-telegram.service bello-orchestrator-anstoss.path >/dev/null 2>&1
  rm -f "$UNITS/bello-telegram.service" "$UNITS/bello-orchestrator-anstoss.path" "$DROPIN"
  rmdir "$(dirname "$DROPIN")" 2>/dev/null
  systemctl daemon-reload
  gut "Dienst und Sofortstart ausgebaut"
  telegram_block "da?" && { sichern; telegram_block heraus; }
  env_loeschen TELEGRAM_BOT_TOKEN
  env_loeschen TELEGRAM_CHAT_ID
  gut "Token und Konto aus $ENV_DATEI entfernt"
  hinweis "Den Bot selbst loeschst du in Telegram beim @BotFather mit /deletebot."
  exit 0
fi

# ---------- 1. Voraussetzungen ----------

meldung "1/6  Voraussetzungen"
[ -x "$PY" ] || { schlecht "$PY fehlt"; exit 1; }
if [ ! -f bin/telegram_bot.py ] || [ ! -f systemd/bello-telegram.service ]; then
  schlecht "Der Code ist zu alt — erst: cd /opt/bello && sudo git pull"
  exit 1
fi
id bello >/dev/null 2>&1 || { schlecht "Betriebsnutzer bello fehlt"; exit 1; }
"$PY" -c "import json; json.load(open('config.json', encoding='utf-8'))" 2>/dev/null \
  || { schlecht "config.json fehlt oder ist kein gueltiges JSON"; exit 1; }
if [ ! -f "$ENV_DATEI" ]; then
  install -d -m 700 "$(dirname "$ENV_DATEI")"
  install -m 600 /dev/null "$ENV_DATEI"
  gut "$ENV_DATEI angelegt"
fi
gut "Code, config.json, $ENV_DATEI und Nutzer bello da"
if systemctl cat bello-orchestrator.service >/dev/null 2>&1; then
  gut "bello-orchestrator.service vorhanden"
else
  hinweis "bello-orchestrator.service nicht gefunden — der Sofortstart greift erst, wenn es ihn gibt"
fi

# ---------- 2. Token ----------

meldung "2/6  Bot-Token"
ALTER_TOKEN=$(env_wert TELEGRAM_BOT_TOKEN)
TOKEN="$ALTER_TOKEN"
if [ -n "$TOKEN" ] && [ "$MODUS" != "--neu" ]; then
  if NAME=$(token_pruefen "$TOKEN"); then
    gut "vorhandener Token gilt: $NAME"
  else
    hinweis "vorhandener Token gilt nicht mehr ($NAME)"
    TOKEN=""
  fi
else
  TOKEN=""
fi
if [ -z "$TOKEN" ]; then
  if [ ! -t 0 ]; then
    schlecht "Hier muss der Token eingegeben werden — bitte direkt im Terminal starten,"
    echo "       nicht aus einem anderen Programm heraus: sudo bash bin/telegram-einrichten.sh"
    exit 1
  fi
  echo "  Den Token hat dir der @BotFather geschickt (Form 123456789:ABCdef...)."
  for versuch in 1 2 3; do
    read -r -s -p "  Token einfuegen (bleibt unsichtbar), dann Enter: " EINGABE
    echo
    EINGABE=$(printf '%s' "$EINGABE" | tr -d '[:space:]')
    if ! [[ "$EINGABE" =~ ^[0-9]{5,}:[A-Za-z0-9_-]{30,}$ ]]; then
      hinweis "Das sieht nicht nach einem Token aus — bitte die ganze Zeile mit Doppelpunkt kopieren."
      continue
    fi
    if NAME=$(token_pruefen "$EINGABE"); then
      TOKEN="$EINGABE"
      break
    fi
    hinweis "Telegram lehnt ab: $NAME"
  done
  [ -n "$TOKEN" ] || { schlecht "kein gueltiger Token — Skript einfach noch einmal starten"; exit 1; }
  env_setzen TELEGRAM_BOT_TOKEN "$TOKEN"
  gut "Token gilt: $NAME — steht jetzt in $ENV_DATEI (nur root lesbar)"
fi

# ---------- 3. Konto ----------

meldung "3/6  Dein Telegram-Konto"
KONTO=$(env_wert TELEGRAM_CHAT_ID)
# Ein Bot darf nur schreiben, wem er schon einmal geantwortet hat. Ein neuer Bot
# (andere Nummer vor dem Doppelpunkt) braucht darum ein neues "hallo".
if [ -n "$KONTO" ] && [ "$MODUS" != "--neu" ] && [ "${ALTER_TOKEN%%:*}" = "${TOKEN%%:*}" ]; then
  gut "freigeschaltet: Konto $KONTO"
else
  if [ ! -t 0 ]; then
    schlecht "Hier musst du bestaetigen — bitte direkt im Terminal starten."
    exit 1
  fi
  # Nur einer darf Telegram abfragen; ein laufender Bot wuerde "hallo" wegschnappen.
  systemctl stop bello-telegram.service 2>/dev/null
  AUSGABE=$(TELEGRAM_BOT_TOKEN="$TOKEN" als_bello "$PY" bin/telegram_bot.py --kennenlernen) \
    || { schlecht "keine Nachricht erkannt — Skript einfach noch einmal starten"; exit 1; }
  KONTO=$(printf '%s\n' "$AUSGABE" | sed -n 's/^CHAT_ID=//p')
  WER=$(printf '%s\n' "$AUSGABE" | sed -n 's/^NAME=//p')
  [[ "$KONTO" =~ ^[0-9]+$ ]] || { schlecht "keine Kontonummer erkannt"; exit 1; }
  echo "  Nachricht von: $WER — Konto $KONTO"
  read -r -p "  Ist das dein Konto? [j/N] " ANTWORT
  case "$ANTWORT" in
    j|J|ja|Ja|JA) ;;
    *) echo "  Abbruch. Niemand wurde freigeschaltet."; exit 1 ;;
  esac
  env_setzen TELEGRAM_CHAT_ID "$KONTO"
  gut "Konto $KONTO freigeschaltet — nur von dort nimmt der Bot etwas an"
fi

# ---------- 4. config.json ----------

meldung "4/6  config.json"
telegram_block "da?" || sichern
telegram_block hinein || schlecht "config.json liess sich nicht schreiben"

# ---------- 5. Dienst und Sofortstart ----------

meldung "5/6  Dienst und Sofortstart"
install -m 644 systemd/bello-telegram.service systemd/bello-orchestrator-anstoss.path "$UNITS/"
gut "Units nach $UNITS kopiert"
# Die Ergebnisse schickt der Lauf selbst — dafuer muss er den Token kennen.
if lauf_liest_env; then
  gut "der Lauf liest $ENV_DATEI schon"
else
  mkdir -p "$(dirname "$DROPIN")"
  printf '# von bin/telegram-einrichten.sh: der Lauf braucht TELEGRAM_BOT_TOKEN\n[Service]\nEnvironmentFile=-%s\n' \
    "$ENV_DATEI" > "$DROPIN"
  gut "Drop-in $DROPIN: der Lauf liest jetzt $ENV_DATEI"
fi
systemctl daemon-reload
systemctl enable --now bello-orchestrator-anstoss.path >/dev/null 2>&1 \
  && gut "Sofortstart bereit (/jetzt in Telegram)" || schlecht "Sofortstart liess sich nicht aktivieren"
systemctl enable bello-telegram.service >/dev/null 2>&1
systemctl restart bello-telegram.service
sleep 4
if systemctl is-active --quiet bello-telegram.service; then
  gut "bello-telegram laeuft"
else
  schlecht "bello-telegram startet nicht — die letzten Zeilen:"
  journalctl -u bello-telegram.service -n 15 --no-pager -o cat | sed 's/^/       /'
fi

# ---------- 6. Probe ----------

meldung "6/6  Probe"
if ( set -a; . "$ENV_DATEI"; set +a; als_bello "$PY" orchestrator_telegram.py --test ) | sed 's/^/  /'; then
  gut "Testnachricht verschickt — schau aufs Handy"
else
  schlecht "Testnachricht ging nicht raus (Grund steht oben)"
fi

meldung "Ergebnis"
if [ "$fehler" -eq 0 ]; then
  echo "  Fertig. Schreib deinem Bot in Telegram /hilfe — er antwortet sofort."
  echo "  Ergebnisse kommen ab dem naechsten Lauf auch aufs Handy, die Mail bleibt."
  echo "  Nachsehen: sudo bash bin/telegram-einrichten.sh --pruefen"
else
  echo "  $fehler Punkt(e) offen — bitte die Ausgabe oben schicken."
fi
exit 0
