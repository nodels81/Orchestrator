#!/usr/bin/env bash
# Erzeugt auf dem netcup-Server den SSH-Schlüssel, mit dem der Shop auf den
# All-Inkl-Webspace aufgespielt wird, und zeigt den öffentlichen Teil an.
#
# Der geheime Teil verlässt diesen Server nie. Ins KAS trägst du nur den
# öffentlichen Teil ein — den darfst du auch in einen Chat kopieren, er ist
# dafür gemacht.
#
#   bash web/betrieb/schluessel-fuer-allinkl.sh

set -euo pipefail

SCHLUESSEL="${HOME}/.ssh/allinkl_bellowerk"

if [[ -f "${SCHLUESSEL}" ]]; then
  echo "Schlüssel gibt es schon: ${SCHLUESSEL}"
  echo "(Wird nicht überschrieben. Für einen neuen erst den alten löschen.)"
else
  mkdir -p "${HOME}/.ssh"
  chmod 700 "${HOME}/.ssh"
  ssh-keygen -t ed25519 -a 100 -N "" \
    -C "bellowerk-aufspielen@$(hostname -s)" \
    -f "${SCHLUESSEL}"
  echo "Schlüssel erzeugt."
fi

chmod 600 "${SCHLUESSEL}"
chmod 644 "${SCHLUESSEL}.pub"

cat <<'TEXT'

--------------------------------------------------------------------
Diesen öffentlichen Schlüssel im KAS eintragen:
  kas.all-inkl.com → Tools → SSH-Zugang → Schlüssel hinterlegen

Er ist nicht geheim. Wer ihn hat, kommt damit nirgends hinein.
--------------------------------------------------------------------
TEXT

cat "${SCHLUESSEL}.pub"

cat <<TEXT

--------------------------------------------------------------------
Danach hier eintragen, damit "ssh allinkl" genügt
(~/.ssh/config, Werte aus dem KAS einsetzen):

Host allinkl
    HostName   wXXXXXXX.kasserver.com
    User       sshXXXXXX
    IdentityFile ${SCHLUESSEL}
    IdentitiesOnly yes

Probe (muss ohne Kennwortfrage durchgehen):
    ssh allinkl "pwd && php -v"
--------------------------------------------------------------------
TEXT
