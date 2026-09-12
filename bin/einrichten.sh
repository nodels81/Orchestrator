#!/bin/bash
# einrichten.sh — bringt den Server auf den Stand des Repos.
#
# Gefahrlos: aendert nichts am Betrieb ausser dem Zeitplan, legt vorher eine
# Sicherung an und kann beliebig oft laufen. Oeffnet keinen Netzwerkdienst.
#
#   cd /opt/bello && git pull && bash bin/einrichten.sh
set -uo pipefail

BASIS=/opt/bello
fehler=0
meldung() { printf '\n\033[1m%s\033[0m\n' "$*"; }
gut()     { printf '  ok   %s\n' "$*"; }
schlecht(){ printf '  FEHL %s\n' "$*"; fehler=$((fehler+1)); }

# ---------- 1. Vorbedingungen ----------
meldung "1/6  Vorbedingungen"
[ "$(id -u)" -eq 0 ] || { echo "Bitte als root ausfuehren."; exit 1; }
cd "$BASIS" || { echo "$BASIS nicht gefunden."; exit 1; }
gut "als root in $BASIS"

if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  schlecht "Arbeitsbaum ist nicht sauber — bitte erst klaeren:"
  git status --short | head
  echo
  echo "Abbruch. Es wurde nichts veraendert."
  exit 1
fi
gut "Git-Arbeitsbaum sauber ($(git rev-parse --short HEAD))"

# ---------- 2. Sicherung ----------
meldung "2/6  Sicherung"
if [ -x bin/backup.sh ]; then
  bash bin/backup.sh >/dev/null 2>&1 && gut "bin/backup.sh gelaufen" || schlecht "backup.sh meldete einen Fehler"
else
  schlecht "bin/backup.sh fehlt"
fi

# ---------- 3. Units sichern (damit sie versioniert sind) ----------
meldung "3/6  systemd-Units ins Repo sichern"
mkdir -p systemd/vom-server
for unit in bello-orchestrator.service bello-orchestrator.timer \
            bello-mailin.service bello-mailin.timer; do
  if systemctl cat "$unit" >"systemd/vom-server/${unit}.txt" 2>/dev/null; then
    gut "$unit gesichert"
  else
    rm -f "systemd/vom-server/${unit}.txt"
    printf '  --   %s gibt es nicht (kein Problem)\n' "$unit"
  fi
done
echo "  Diese Dateien sind der einzige Teil des Betriebs, der bisher nirgends"
echo "  versioniert war. Nach dem Lauf mit 'git add systemd/ && git commit' sichern."

# ---------- 4. Zeitplan ----------
meldung "4/6  Zeitplan: stuendlich 07-19 Uhr"
ZIEL=/etc/systemd/system/bello-orchestrator.timer.d
mkdir -p "$ZIEL"
if cp systemd/bello-orchestrator-haeufiger.conf "$ZIEL/haeufiger.conf"; then
  gut "Drop-in nach $ZIEL/haeufiger.conf"
else
  schlecht "Drop-in konnte nicht kopiert werden"
fi
systemctl daemon-reload && gut "daemon-reload" || schlecht "daemon-reload"
systemctl restart bello-orchestrator.timer 2>/dev/null \
  && gut "Timer neu geladen" || schlecht "Timer liess sich nicht neu laden"

# ---------- 5. Probelauf ----------
meldung "5/6  Probelauf (schreibt nur nach daten/)"
systemctl start bello-orchestrator.service
sleep 3
if journalctl -u bello-orchestrator --since "-2 min" --no-pager 2>/dev/null | grep -q "Read-only file system"; then
  schlecht "es wird immer noch in den Git-Baum geschrieben — bitte Ausgabe schicken"
else
  gut "keine Schreibfehler mehr"
fi
if [ -n "$(git status --porcelain)" ]; then
  schlecht "der Lauf hat den Git-Baum veraendert:"
  git status --short | head
else
  gut "Git-Arbeitsbaum ist nach dem Lauf immer noch sauber"
fi

# ---------- 6. Stand ----------
meldung "6/6  Stand"
systemctl list-timers 'bello-*' --no-pager 2>/dev/null | head -5
echo
ls -la daten/dashboard.html daten/markenbrief.md 2>/dev/null

meldung "Ergebnis"
if [ "$fehler" -eq 0 ]; then
  echo "Alles in Ordnung. Der Betrieb laeuft jetzt stuendlich von 07 bis 19 Uhr."
  echo "Gustav meldet sich per Mail, sobald etwas zu entscheiden ist."
else
  echo "$fehler Punkt(e) offen — bitte die Ausgabe oben schicken."
fi
exit 0
