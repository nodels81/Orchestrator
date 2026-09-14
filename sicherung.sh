#!/usr/bin/env bash
#
# sicherung.sh — Vollsicherung von /opt/bello, bevor gepullt wird.
#
# Macht drei Dinge und nichts sonst. Es wird nichts geloescht, nichts gepullt,
# nichts ueberschrieben:
#   1. Tararchiv des ganzen Ordners (ohne venv und Caches)
#   2. Getrennte Kopie der Geheimnisse und des Betriebszustands
#   3. Den Servercode auf einen eigenen Git-Zweig legen und hochladen
#
# Aufruf auf dem Server:
#   cd /opt/bello && bash sicherung.sh
#
# Liegt das Repo woanders:  bash sicherung.sh /pfad/zum/ordner

set -euo pipefail

QUELLE="${1:-$PWD}"
ZIEL="${SICHERUNG_ZIEL:-/opt/bello-sicherungen}"
STEMPEL="$(date +%Y-%m-%d-%H%M)"
ARCHIV="$ZIEL/bello-$STEMPEL.tar.gz"
ZWEIG="server-stand-$(date +%Y-%m-%d)"

echo "=== Sicherung Bellowerk-Orchestrator ==="
echo "Quelle: $QUELLE"
echo "Ziel:   $ZIEL"
echo

# --- Prüfen, ob das überhaupt der richtige Ordner ist ---------------------
if [ ! -f "$QUELLE/orchestrator.py" ]; then
  echo "FEHLER: In $QUELLE liegt keine orchestrator.py."
  echo "        Bitte im Ordner des Betriebs aufrufen, sonst: bash sicherung.sh /opt/bello"
  exit 1
fi

mkdir -p "$ZIEL"
chmod 700 "$ZIEL"

# --- 1. Tararchiv ---------------------------------------------------------
echo "[1/3] Archiv wird geschrieben ..."
tar --exclude="./venv" \
    --exclude="./.venv" \
    --exclude="./__pycache__" \
    --exclude="*/__pycache__" \
    --exclude="./node_modules" \
    --exclude="./.git/objects/pack/tmp_*" \
    -czf "$ARCHIV" -C "$QUELLE" .
chmod 600 "$ARCHIV"
GROESSE="$(du -h "$ARCHIV" | cut -f1)"
echo "      $ARCHIV  ($GROESSE)"

# Archiv sofort auf Lesbarkeit prüfen — ein kaputtes Archiv ist keine Sicherung
if tar -tzf "$ARCHIV" >/dev/null 2>&1; then
  ANZAHL="$(tar -tzf "$ARCHIV" | wc -l)"
  echo "      Archiv lesbar, $ANZAHL Eintraege."
else
  echo "      FEHLER: Archiv ist nicht lesbar. Abbruch, nichts weiter tun."
  exit 1
fi

# --- 2. Geheimnisse und Betriebszustand getrennt ---------------------------
echo "[2/3] Geheimnisse und Zustand werden getrennt gesichert ..."
EXTRA="$ZIEL/extra-$STEMPEL"
mkdir -p "$EXTRA"
chmod 700 "$EXTRA"
for datei in config.json auftraege.json; do
  if [ -f "$QUELLE/$datei" ]; then
    cp -p "$QUELLE/$datei" "$EXTRA/$datei"
    chmod 600 "$EXTRA/$datei"
    echo "      $datei gesichert"
  else
    echo "      $datei nicht vorhanden, uebersprungen"
  fi
done
if [ -d "$QUELLE/logs" ]; then
  cp -rp "$QUELLE/logs" "$EXTRA/logs" 2>/dev/null || true
  echo "      logs/ gesichert"
fi

# --- 3. Servercode auf einen eigenen Zweig ---------------------------------
echo "[3/3] Servercode wird auf den Zweig $ZWEIG gelegt ..."
cd "$QUELLE"

if [ ! -d .git ]; then
  echo "      Kein Git-Repo. Schritt uebersprungen, das Archiv reicht als Sicherung."
else
  AKTUELL="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unbekannt)"
  echo "      Aktueller Zweig: $AKTUELL"

  if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
    echo "      Nichts Ungesichertes im Arbeitsverzeichnis."
  else
    git checkout -b "$ZWEIG" 2>/dev/null || git checkout "$ZWEIG"
    git add -A
    git -c user.name="Bellowerk Server" -c user.email="server@bellowerk.local" \
        commit -q -m "Serverstand $STEMPEL: Abteilungen und Aenderungen von /opt/bello" || true
    echo "      Festgeschrieben auf $ZWEIG"

    if git push -u origin "$ZWEIG" 2>/dev/null; then
      echo "      Hochgeladen nach origin/$ZWEIG"
    else
      echo "      Hochladen nicht moeglich (keine Zugangsdaten auf dem Server?)."
      echo "      Der Stand liegt lokal auf dem Zweig $ZWEIG und im Archiv. Das genuegt."
    fi
  fi
fi

# --- Zusammenfassung -------------------------------------------------------
cat <<ENDE

=== Fertig ===

Archiv:       $ARCHIV
Geheimnisse:  $EXTRA/
Git-Zweig:    $ZWEIG

Wiederherstellen, falls der Pull etwas kaputt macht:

  sudo systemctl stop bello.timer 2>/dev/null || crontab -l   # Laeufe anhalten
  mkdir -p /opt/bello-wiederhergestellt
  tar -xzf $ARCHIV -C /opt/bello-wiederhergestellt
  # pruefen, dann zurueckschieben:
  # mv /opt/bello /opt/bello-kaputt && mv /opt/bello-wiederhergestellt /opt/bello
  cp $EXTRA/config.json /opt/bello/config.json
  cp $EXTRA/auftraege.json /opt/bello/auftraege.json

Erst danach pullen. Und vorher SERVER-ABGLEICH.md lesen: das
Abteilungsverzeichnis in orchestrator.py wird durch einen Pull ueberschrieben.
ENDE
