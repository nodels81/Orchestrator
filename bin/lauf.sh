#!/bin/bash
set -uo pipefail
cd /opt/bello || exit 1
TAG=$(date +%F)
LOG="/opt/bello/logs/orchestrator-${TAG}.log"
umask 027
{
  echo "===== Lauf $(date --iso-8601=seconds) | args: $* ====="
  /opt/bello/.venv/bin/python -u orchestrator.py "$@"
  rc=$?
  /opt/bello/.venv/bin/python /opt/bello/bin/dashboard.py 2>&1 || echo "[dashboard] Fehler beim Erzeugen"
  echo "----- Ende rc=${rc} $(date --iso-8601=seconds) -----"
  exit $rc
} 2>&1 | tee -a "$LOG"
exit "${PIPESTATUS[0]}"
