#!/usr/bin/env bash
#
# uebernahme.sh — Holt NUR die unbedenklichen neuen Dateien aus dem Website-Zweig
# nach /opt/bello. Kein "git pull", kein Merge, kein Zweigwechsel.
#
# Grund: Ein voller Pull wuerde orchestrator.py ueberschreiben. Dort steht das
# Abteilungsverzeichnis, und der Server kennt Abteilungen (07 Einkauf China,
# 08 Design, 09 Qualitaet, 10 Homepage), die im Zweig fehlen. Nach einem Pull
# wuerde jeder Auftrag an diese Abteilungen mit "Unbekannte Abteilung" abbrechen.
#
# Aufruf auf dem Server, NACH sicherung.sh:
#   cd /opt/bello && bash uebernahme.sh

set -euo pipefail

ZWEIG="${ZWEIG:-claude/ultimate-website-prompt-ira6ls}"
QUELLE="${1:-$PWD}"

# Was gefahrlos uebernommen werden kann: ausschliesslich neue Dateien,
# die es auf dem Server nicht gibt.
UNBEDENKLICH=(
  tagesbrief.py
  sicherung.sh
  uebernahme.sh
  SERVER-ABGLEICH.md
  WEBSITE-PROMPT-ultra.md
  entscheidungen
  konzepte
  web
  .claude/skills/website-highend
)

# Was ausdruecklich NICHT angefasst wird, mit Grund.
cat <<'ENDE'
=== Uebernahme aus dem Website-Zweig ===

Nicht angefasst werden:
  orchestrator.py    enthaelt das Abteilungsverzeichnis. Der Zweig kennt nur 01-06,
                     der Server zusaetzlich 07 bis 10. Wird von Hand zusammengefuehrt.
  abteilung_web.py   waere eine zweite Web-Abteilung neben der bestehenden 10 Homepage.
  markenwissen.py    kann auf dem Server geaendert worden sein. Wird von Hand verglichen.
  README.md          dito.
  config.json        Geheimnisse. Bleiben, wo sie sind.

ENDE

cd "$QUELLE"

if [ ! -f orchestrator.py ] || [ ! -d .git ]; then
  echo "FEHLER: $QUELLE ist nicht der Betriebsordner mit Git. Abbruch."
  exit 1
fi

# --- Sicherung muss existieren und frisch sein ----------------------------
SICHERUNGSORDNER="${SICHERUNG_ZIEL:-/opt/bello-sicherungen}"
NEUESTE="$(find "$SICHERUNGSORDNER" -maxdepth 1 -name 'bello-*.tar.gz' -mmin -1440 2>/dev/null | sort | tail -1 || true)"
if [ -z "$NEUESTE" ]; then
  echo "FEHLER: In $SICHERUNGSORDNER liegt kein Archiv aus den letzten 24 Stunden."
  echo "        Erst sichern:  bash sicherung.sh"
  exit 1
fi
echo "Sicherung gefunden: $NEUESTE"
echo

# --- Zweig holen ----------------------------------------------------------
echo "Hole $ZWEIG ..."
git fetch origin "$ZWEIG" --quiet
FERN="origin/$ZWEIG"

# --- Nur Pfade behalten, die es im Zweig wirklich gibt ---------------------
# Ein einziger fehlender Pfad wuerde sonst den ganzen Vorgang abbrechen lassen.
VORHANDEN=()
for pfad in "${UNBEDENKLICH[@]}"; do
  if [ -n "$(git ls-tree -r --name-only "$FERN" -- "$pfad" 2>/dev/null)" ]; then
    VORHANDEN+=("$pfad")
  else
    echo "Hinweis: $pfad gibt es im Zweig nicht, wird uebersprungen."
  fi
done
if [ ${#VORHANDEN[@]} -eq 0 ]; then
  echo "Nichts zu uebernehmen. Abbruch."
  exit 0
fi

# --- Zeigen, was sich aendern wuerde --------------------------------------
echo
echo "Diese Dateien wuerden geschrieben:"
GEAENDERT="$(git diff --name-status HEAD "$FERN" -- "${VORHANDEN[@]}" || true)"
if [ -z "$GEAENDERT" ]; then
  echo "  Nichts. Alles schon aktuell."
  exit 0
fi
echo "$GEAENDERT" | sed 's/^/  /'
echo
echo "  A = neu, M = ueberschrieben"
echo

read -r -p "Uebernehmen? Nur 'ja' fuehrt aus: " ANTWORT
if [ "$ANTWORT" != "ja" ]; then
  echo "Abgebrochen. Nichts geaendert."
  exit 0
fi

# --- Nur diese Pfade herausziehen -----------------------------------------
git checkout "$FERN" -- "${VORHANDEN[@]}"
echo
echo "Uebernommen. Stand im Arbeitsverzeichnis:"
git status --short | sed 's/^/  /'

# --- Sofort testen --------------------------------------------------------
echo
echo "Probe: Tagesbrief bauen (sendet nichts) ..."
PYTHON="venv/bin/python"
[ -x "$PYTHON" ] || PYTHON="$(command -v python3)"
if "$PYTHON" tagesbrief.py > /tmp/tagesbrief-probe.txt 2>&1; then
  head -12 /tmp/tagesbrief-probe.txt | sed 's/^/  /'
  echo "  ..."
  echo "  Vollstaendig in /tmp/tagesbrief-probe.txt"
else
  echo "  FEHLER beim Probelauf:"
  sed 's/^/  /' /tmp/tagesbrief-probe.txt
  echo "  Die uebernommenen Dateien liegen im Arbeitsverzeichnis und koennen mit"
  echo "  git checkout -- . wieder verworfen werden."
  exit 1
fi

cat <<'ENDE'

=== Fertig ===

Naechste Schritte:
  1. Probelauf ansehen, dann einmal echt senden:
       venv/bin/python tagesbrief.py --senden --erzwingen
  2. Wenn die Mail ankommt, in den Cron eintragen:
       crontab -e
       0 7 * * *  cd /opt/bello && venv/bin/python tagesbrief.py --senden >> logs/tagesbrief.log 2>&1
  3. Serverstand festschreiben, damit er nicht wieder verlorengeht:
       git add -A && git commit -m "Tagesbrief und Unterlagen uebernommen"

orchestrator.py, abteilung_web.py und markenwissen.py bleiben offen. Dafuer muss der
Serverstand erst nach GitHub, siehe SERVER-ABGLEICH.md.
ENDE
