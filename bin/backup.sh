#!/bin/bash
set -uo pipefail
ZIEL=/var/backups/bello
TS=$(date +%Y-%m-%d_%H%M%S)
umask 077
mkdir -p "$ZIEL"; chmod 700 "$ZIEL"
ARCHIV="$ZIEL/bello-$TS.tar.gz"
tar -czf "$ARCHIV" -C / \
  opt/bello/daten \
  opt/bello/config.json \
  etc/bello/env
chmod 600 "$ARCHIV"
ln -sfn "bello-$TS.tar.gz" "$ZIEL/bello-neueste.tar.gz"
# Rotation: alles aelter als 14 Tage weg
find "$ZIEL" -maxdepth 1 -type f -name 'bello-*.tar.gz' -mtime +14 -delete
echo "[backup] $ARCHIV  ($(du -h "$ARCHIV" | cut -f1))"
tar -tzf "$ARCHIV" | sed 's/^/[backup]   /'
