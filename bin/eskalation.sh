#!/bin/bash
# Wird von systemd via OnFailure= gestartet. $1 = fehlgeschlagene Unit.
UNIT="${1:-bello-orchestrator.service}"
TAG=$(date +%F)
LOG="/opt/bello/logs/orchestrator-${TAG}.log"
TMP=$(mktemp)
{
  echo "Der automatische Tageslauf ($UNIT) ist FEHLGESCHLAGEN."
  echo "Zeit: $(date --iso-8601=seconds)"
  echo "Host: $(hostname -f)"
  echo
  echo "=== systemctl status ==="
  systemctl --no-pager --full status "$UNIT" 2>&1 | head -n 20
  echo
  echo "=== letzte Journal-Zeilen ($UNIT) ==="
  journalctl -u "$UNIT" -n 40 --no-pager 2>&1
  echo
  echo "=== letzte Zeilen $LOG ==="
  tail -n 40 "$LOG" 2>/dev/null || echo "(keine Tagesdatei)"
} > "$TMP"

cd /opt/bello || exit 1
TXT="$TMP" timeout 90 /opt/bello/.venv/bin/python - <<'PY'
import os
from orchestrator_mail import senden
txt = open(os.environ["TXT"], encoding="utf-8", errors="replace").read()
ok = senden("[Bello] Tageslauf FEHLGESCHLAGEN", txt)
print("[eskalation] Mail gesendet." if ok else "[eskalation] Mail NICHT gesendet (Grund siehe oben).")
PY
rm -f "$TMP"
