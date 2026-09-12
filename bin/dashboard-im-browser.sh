#!/bin/bash
# dashboard-im-browser.sh — macht Werkbank und Galerie im Browser erreichbar.
#
# Nur diese zwei Seiten, hinter Passwort und HTTPS. Alles andere unter daten/
# (auftraege.json, gedaechtnis.db, markenbrief.md, Zeichnungen) bleibt draussen.
#
#   bash bin/dashboard-im-browser.sh
#
# Rueckbau jederzeit:  bash bin/dashboard-im-browser.sh --entfernen
set -uo pipefail

HOST="${BELLO_HOST:-v2202609413684515441.powersrv.de}"
DATEN=/opt/bello/daten
HTPASSWD=/etc/nginx/bello.htpasswd
ZUGANG=/root/bello-dashboard-zugang.txt
BENUTZER=bjoern

meldung(){ printf '\n\033[1m%s\033[0m\n' "$*"; }
gut(){ printf '  ok   %s\n' "$*"; }
schlecht(){ printf '  FEHL %s\n' "$*"; }

[ "$(id -u)" -eq 0 ] || { echo "Bitte als root ausfuehren."; exit 1; }

# ---------- Rueckbau ----------
if [ "${1:-}" = "--entfernen" ]; then
  meldung "Rueckbau"
  rm -f /etc/nginx/sites-enabled/bello /etc/nginx/sites-available/bello "$HTPASSWD"
  systemctl reload nginx 2>/dev/null
  echo "  nginx-Eintrag entfernt. Das Zertifikat bleibt liegen (schadet nicht)."
  echo "  Ports schliessen, falls gewuenscht: ufw delete allow 80; ufw delete allow 443"
  exit 0
fi

# ---------- 1. Pakete ----------
meldung "1/6  Pakete"
apt-get update -qq
apt-get install -y nginx apache2-utils certbot >/dev/null 2>&1 \
  && gut "nginx, apache2-utils, certbot" || { schlecht "Installation fehlgeschlagen"; exit 1; }

# ---------- 2. Passwort ----------
meldung "2/6  Zugang"
if [ -f "$HTPASSWD" ]; then
  gut "Passwortdatei besteht bereits — bleibt unveraendert"
  PASSWORT="(unveraendert, siehe $ZUGANG)"
else
  PASSWORT="$(openssl rand -base64 18 | tr -d '/+=' | cut -c1-20)"
  htpasswd -bc "$HTPASSWD" "$BENUTZER" "$PASSWORT" >/dev/null 2>&1 \
    && gut "Benutzer '$BENUTZER' angelegt" || schlecht "htpasswd fehlgeschlagen"
  chown root:www-data "$HTPASSWD"; chmod 640 "$HTPASSWD"
  { echo "Bellowerk-Dashboard"
    echo "URL:      https://$HOST/"
    echo "Benutzer: $BENUTZER"
    echo "Passwort: $PASSWORT"
    echo "Angelegt: $(date --iso-8601=seconds)"
  } > "$ZUGANG"
  chmod 600 "$ZUGANG"
  gut "Zugangsdaten in $ZUGANG (nur root lesbar)"
fi

# ---------- 3. Leserechte fuer nginx ----------
meldung "3/6  Leserechte"
# Der Tageslauf schreibt mit umask 027 als Nutzer bello (Dateien 640 bello:bello).
# nginx laeuft als www-data und kommt da sonst nicht heran.
usermod -aG bello www-data 2>/dev/null && gut "www-data ist jetzt in der Gruppe bello"
chmod o+x /opt/bello 2>/dev/null
chmod 750 "$DATEN" 2>/dev/null
gut "Durchgangsrechte auf /opt/bello und daten/ gesetzt"

# ---------- 4. Zertifikat holen (noch ohne HTTPS-Block) ----------
meldung "4/6  Zertifikat fuer $HOST"
mkdir -p /var/www/html
cat > /etc/nginx/sites-available/bello <<NGINX
server {
    listen 80;
    listen [::]:80;
    server_name $HOST;
    location /.well-known/acme-challenge/ { root /var/www/html; }
    location / { return 404; }
}
NGINX
ln -sf /etc/nginx/sites-available/bello /etc/nginx/sites-enabled/bello
rm -f /etc/nginx/sites-enabled/default
nginx -t >/dev/null 2>&1 && systemctl reload nginx && gut "nginx laeuft (nur Port 80)" \
  || { schlecht "nginx-Konfiguration fehlerhaft"; nginx -t; exit 1; }

if [ -d "/etc/letsencrypt/live/$HOST" ]; then
  gut "Zertifikat besteht bereits"
else
  certbot certonly --webroot -w /var/www/html -d "$HOST" \
      --non-interactive --agree-tos --register-unsafely-without-email \
      --deploy-hook "systemctl reload nginx" 2>&1 | tail -5
  if [ -d "/etc/letsencrypt/live/$HOST" ]; then
    gut "Zertifikat ausgestellt"
  else
    schlecht "Kein Zertifikat. Meist ist Port 80 von aussen dicht."
    echo "       Pruefen: netcup-Kundenpanel -> Server -> Firewall, und 'ufw status'."
    echo "       Der Rest wird uebersprungen; nichts ist kaputt."
    exit 1
  fi
fi

# ---------- 5. Die eigentliche Seite ----------
meldung "5/6  Seite einrichten"
cat > /etc/nginx/sites-available/bello <<NGINX
server {
    listen 80;
    listen [::]:80;
    server_name $HOST;
    location /.well-known/acme-challenge/ { root /var/www/html; }
    location / { return 301 https://\$host\$request_uri; }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name $HOST;

    ssl_certificate     /etc/letsencrypt/live/$HOST/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$HOST/privkey.pem;

    auth_basic           "Bellowerk";
    auth_basic_user_file $HTPASSWD;

    add_header X-Content-Type-Options  nosniff        always;
    add_header X-Frame-Options         DENY           always;
    add_header Referrer-Policy         no-referrer    always;
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header Cache-Control           "no-store"     always;

    root  $DATEN;
    autoindex off;

    # Ausdrueckliche Freigabe: nur diese beiden Seiten. Alles andere unter
    # daten/ (auftraege.json, gedaechtnis.db, Markenbrief, Zeichnungen) faellt
    # in das 404 am Ende.
    location = /              { return 302 /dashboard.html; }
    location = /dashboard.html { }
    location = /galerie.html   { }
    location /                 { return 404; }
}
NGINX
nginx -t >/dev/null 2>&1 && systemctl reload nginx && gut "Seite ist scharf" \
  || { schlecht "Konfiguration fehlerhaft — nichts uebernommen"; nginx -t; exit 1; }

# ---------- 6. Gegenprobe ----------
meldung "6/6  Gegenprobe"
ohne=$(curl -s -o /dev/null -w '%{http_code}' "https://$HOST/dashboard.html")
mit=$(curl -s -o /dev/null -w '%{http_code}' -u "$BENUTZER:${PASSWORT}" "https://$HOST/dashboard.html" 2>/dev/null)
geheim=$(curl -s -o /dev/null -w '%{http_code}' "https://$HOST/auftraege.json")
[ "$ohne" = "401" ] && gut "ohne Passwort: 401 (abgewiesen)" || schlecht "ohne Passwort: $ohne — erwartet 401"
[ "$geheim" = "401" ] || [ "$geheim" = "404" ] && gut "auftraege.json: $geheim (nicht erreichbar)" \
  || schlecht "auftraege.json liefert $geheim — BITTE MELDEN"
case "$mit" in 200) gut "mit Passwort: 200" ;; *) echo "  --   mit Passwort: $mit (bei bestehender Passwortdatei normal)" ;; esac

meldung "Fertig"
echo "  https://$HOST/"
echo "  Benutzer: $BENUTZER"
echo "  Passwort: siehe $ZUGANG   (cat $ZUGANG)"
echo
echo "  Die Seite zeigt immer den letzten Lauf — sie wird stuendlich neu geschrieben."
echo "  Rueckbau: bash bin/dashboard-im-browser.sh --entfernen"
