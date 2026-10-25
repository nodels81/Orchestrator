#!/usr/bin/env bash
# Phase 1: Server absichern und vorbereiten (Debian 13 "Trixie", als root starten).
# Idempotent: kann mehrfach laufen.
#
#   Schritt 1:  sudo STUDIO_PUBKEY="ssh-ed25519 AAAA... bjoern" ./phase1-server.sh
#   (in neuem Terminal pruefen:  ssh studio@<server-ip>   -> muss ohne Passwort klappen)
#   Schritt 2:  sudo ./phase1-server.sh --harden-ssh
#
# Root- und Passwort-Login werden NUR in Schritt 2 abgeschaltet.
set -euo pipefail

STUDIO_USER="studio"
NODE_MAJOR="22"   # aktuelle LTS; bei Bedarf anpassen
SSH_DROPIN="/etc/ssh/sshd_config.d/10-studio-hardening.conf"

log() { printf '\n==> %s\n' "$*"; }
die() { printf 'FEHLER: %s\n' "$*" >&2; exit 1; }
[ "$(id -u)" -eq 0 ] || die "Bitte als root starten."

harden_ssh() {
  home="/home/${STUDIO_USER}"
  [ -s "${home}/.ssh/authorized_keys" ] || die "Kein SSH-Key fuer ${STUDIO_USER} hinterlegt. Erst Schritt 1 ausfuehren."
  log "SSH haerten: Root- und Passwort-Login aus"
  cat > "$SSH_DROPIN" <<CONF
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
CONF
  sshd -t || { rm -f "$SSH_DROPIN"; die "sshd-Konfiguration ungueltig, Aenderung zurueckgenommen."; }
  systemctl reload ssh
  echo "Fertig. Bestehende Sitzung offen lassen und in neuem Terminal 'ssh ${STUDIO_USER}@<ip>' testen."
}

if [ "${1:-}" = "--harden-ssh" ]; then
  harden_ssh
  exit 0
fi

[ -n "${STUDIO_PUBKEY:-}" ] || die "STUDIO_PUBKEY fehlt (oeffentlicher SSH-Schluessel, z. B. Inhalt von ~/.ssh/id_ed25519.pub)."
case "$STUDIO_PUBKEY" in ssh-*|ecdsa-*|sk-*) ;; *) die "STUDIO_PUBKEY sieht nicht nach einem oeffentlichen Schluessel aus.";; esac

export DEBIAN_FRONTEND=noninteractive

log "System aktualisieren"
apt-get update
apt-get -y full-upgrade

log "Basispakete"
apt-get -y install sudo curl ca-certificates gnupg git ufw fail2ban unattended-upgrades \
  apt-listchanges ffmpeg imagemagick python3 python3-venv python3-pip build-essential \
  unzip jq rsync fontconfig fonts-inter fonts-montserrat fonts-playfair-display \
  fonts-liberation fonts-noto-color-emoji

log "Chromium-Abhaengigkeiten fuer Remotion"
# t64-Namen gelten ab Debian 13; Fallback fuer aeltere Releases
apt-get -y install libnss3 libdbus-1-3 libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 \
  libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
  libasound2t64 libpango-1.0-0 libcairo2 libxshmfence1 \
  || apt-get -y install libnss3 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
       libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
       libasound2 libpango-1.0-0 libcairo2 libxshmfence1

log "Handschrift-Schrift (Caveat) installieren"
if ! fc-list | grep -qi caveat; then
  apt-get -y install fonts-caveat 2>/dev/null || {
    mkdir -p /usr/local/share/fonts/caveat
    curl -fsSL -o /usr/local/share/fonts/caveat/Caveat.ttf \
      "https://github.com/google/fonts/raw/main/ofl/caveat/Caveat%5Bwght%5D.ttf" \
      || echo "WARNUNG: Caveat konnte nicht geladen werden - spaeter nachholen."
  }
fi
fc-cache -f

log "Node.js ${NODE_MAJOR} (NodeSource)"
if ! command -v node >/dev/null || [ "$(node -p 'process.versions.node.split(".")[0]')" != "$NODE_MAJOR" ]; then
  curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash -
  apt-get -y install nodejs
fi

log "Benutzer ${STUDIO_USER}"
id "$STUDIO_USER" >/dev/null 2>&1 || adduser --disabled-password --gecos "" "$STUDIO_USER"
usermod -aG sudo "$STUDIO_USER"
# sudo ohne Passwort, weil der Benutzer kein Passwort hat (nur Key-Login)
echo "${STUDIO_USER} ALL=(ALL) NOPASSWD:ALL" > "/etc/sudoers.d/90-${STUDIO_USER}"
chmod 440 "/etc/sudoers.d/90-${STUDIO_USER}"
visudo -cf "/etc/sudoers.d/90-${STUDIO_USER}" >/dev/null
home="/home/${STUDIO_USER}"
install -d -m 700 -o "$STUDIO_USER" -g "$STUDIO_USER" "${home}/.ssh"
grep -qxF "$STUDIO_PUBKEY" "${home}/.ssh/authorized_keys" 2>/dev/null || echo "$STUDIO_PUBKEY" >> "${home}/.ssh/authorized_keys"
chown "$STUDIO_USER:$STUDIO_USER" "${home}/.ssh/authorized_keys"
chmod 600 "${home}/.ssh/authorized_keys"

log "Firewall (nur SSH)"
ufw default deny incoming
ufw default allow outgoing
ufw allow OpenSSH
ufw --force enable

log "fail2ban"
cat > /etc/fail2ban/jail.d/sshd.local <<CONF
[sshd]
enabled = true
backend = systemd
maxretry = 5
bantime = 1h
findtime = 10m
CONF
systemctl enable --now fail2ban
systemctl restart fail2ban

log "Automatische Sicherheitsupdates"
cat > /etc/apt/apt.conf.d/20auto-upgrades <<CONF
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
CONF
systemctl enable --now unattended-upgrades

log "Swap pruefen"
mem_mb=$(awk '/MemTotal/{print int($2/1024)}' /proc/meminfo)
if [ "$(swapon --show --noheadings | wc -l)" -eq 0 ]; then
  if [ "$mem_mb" -lt 8192 ]; then
    fallocate -l 4G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
    grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "4 GB Swap angelegt (RAM: ${mem_mb} MB)."
  fi
else
  echo "Swap vorhanden."
fi

log "Claude Code fuer ${STUDIO_USER} (offizieller Installer)"
if ! su - "$STUDIO_USER" -c 'command -v claude' >/dev/null 2>&1; then
  su - "$STUDIO_USER" -c 'curl -fsSL https://claude.ai/install.sh | bash' \
    || echo "WARNUNG: Installer fehlgeschlagen - als ${STUDIO_USER} manuell nachholen (siehe docs.claude.com)."
fi

log "Projektordner"
su - "$STUDIO_USER" -c 'mkdir -p ~/video-studio && cd ~/video-studio && (git rev-parse >/dev/null 2>&1 || git init -q)'

log "Zusammenfassung"
echo "Ressourcen: $(nproc) Kerne, ${mem_mb} MB RAM"; free -h | sed -n '1,2p'; df -h / | tail -1
echo "ufw:";       ufw status | head -5
echo "fail2ban:";  fail2ban-client status sshd | head -4 || true
echo "node $(node -v), ffmpeg $(ffmpeg -version | head -1 | cut -d' ' -f3), python $(python3 -V | cut -d' ' -f2)"
cat <<MSG

NAECHSTE SCHRITTE
1. Neues Terminal:  ssh ${STUDIO_USER}@<server-ip>   (muss ohne Passwort klappen)
2. Erst dann:       sudo ./phase1-server.sh --harden-ssh
3. Als ${STUDIO_USER}: 'claude' starten und anmelden.
MSG
