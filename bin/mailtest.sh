#!/bin/bash
# Testet den Eskalations-Mailweg. Muss als root laufen (liest /etc/bello/env).
set -a; . /etc/bello/env; set +a
cd /opt/bello || exit 1
exec runuser -u bello --preserve-environment -- \
  /opt/bello/.venv/bin/python orchestrator_mail.py --test
