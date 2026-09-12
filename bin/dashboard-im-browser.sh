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
  # Die URL kann sich geaendert haben (andere Domain), das Passwort nicht.
  if [ -f "$ZUGANG" ]; then
    sed -i "s|^URL:.*|URL:      https://$HOST/|" "$ZUGANG"
    gut "URL in $ZUGANG auf https://$HOST/ gesetzt"
  fi
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
# Ohne Mailadresse verschickt Let's Encrypt keine Warnung, falls die automatische
# Erneuerung einmal scheitert. Mit BELLO_MAIL=... setzen, dann kommt eine.
if [ -n "${BELLO_MAIL:-}" ]; then
  CERTBOT_MAIL=(-m "$BELLO_MAIL" --no-eff-email)
  gut "Ablaufwarnungen gehen an $BELLO_MAIL"
else
  CERTBOT_MAIL=(--register-unsafely-without-email)
  echo "  --   ohne Mailadresse (BELLO_MAIL=... setzen, dann warnt Let's Encrypt)"
fi
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

if [ "${1:-}" = "--selbstsigniert" ]; then
  # Eigenes Zertifikat: der Browser warnt einmal, weil niemand dafuer buergt.
  # Die Verbindung ist trotzdem verschluesselt — das Passwort geht nicht im
  # Klartext ueber die Leitung. Als Zwischenloesung tragbar.
  ZERT=/etc/ssl/bello
  mkdir -p "$ZERT"
  if [ ! -f "$ZERT/fullchain.pem" ]; then
    openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \
      -keyout "$ZERT/privkey.pem" -out "$ZERT/fullchain.pem" \
      -subj "/CN=$HOST" -addext "subjectAltName=DNS:$HOST" >/dev/null 2>&1 \
      && gut "selbstsigniertes Zertifikat erzeugt (10 Jahre)" \
      || { schlecht "openssl fehlgeschlagen"; exit 1; }
  else
    gut "selbstsigniertes Zertifikat besteht bereits"
  fi
  ZERT_PFAD="$ZERT"
elif [ -d "/etc/letsencrypt/live/$HOST" ]; then
  gut "Zertifikat besteht bereits"
  ZERT_PFAD="/etc/letsencrypt/live/$HOST"
else
  AUSGABE=$(certbot certonly --webroot -w /var/www/html -d "$HOST" \
      --non-interactive --agree-tos "${CERTBOT_MAIL[@]}" \
      --deploy-hook "systemctl reload nginx" 2>&1)
  echo "$AUSGABE" | tail -5
  if [ -d "/etc/letsencrypt/live/$HOST" ]; then
    gut "Zertifikat ausgestellt"
    ZERT_PFAD="/etc/letsencrypt/live/$HOST"
  elif echo "$AUSGABE" | grep -q "too many certificates"; then
    schlecht "Let's-Encrypt-Kontingent erschoepft — nicht deine Schuld."
    echo "       powersrv.de ist netcups Sammeldomain fuer alle vServer, und das"
    echo "       Wochenkontingent von 50 Zertifikaten haben andere Kunden verbraucht."
    echo "       Port 80 funktioniert, sonst waere die Anfrage gar nicht angekommen."
    echo
    echo "       Drei Wege:"
    echo "       a) Eigene Domain eintragen (A-Record auf diesen Server), dann"
    echo "          gilt das Kontingent nur fuer dich:"
    echo "          BELLO_HOST=dashboard.deine-domain.de bash bin/dashboard-im-browser.sh"
    echo "       b) Selbstsigniert weitermachen (Browserwarnung beim ersten Besuch,"
    echo "          Verschluesselung aber echt):"
    echo "          bash bin/dashboard-im-browser.sh --selbstsigniert"
    echo "       c) Spaeter noch einmal versuchen — der Zeitpunkt steht oben."
    exit 1
  else
    schlecht "Kein Zertifikat. Haeufigste Ursache: Port 80 von aussen dicht."
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

    ssl_certificate     $ZERT_PFAD/fullchain.pem;
    ssl_certificate_key $ZERT_PFAD/privkey.pem;

    auth_basic           "Bellowerk";
    auth_basic_user_file $HTPASSWD;

    add_header X-Content-Type-Options  nosniff        always;
    add_header X-Frame-Options         DENY           always;
    add_header Referrer-Policy         no-referrer    always;
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header Cache-Control           "no-store"     always;

    root  $DATEN;
    autoindex off;

    # Die App und ihr Zubehoer liegen im Repo, nicht unter daten/.
    location = /app.html            { alias /opt/bello/app/app.html; }
    location = /manifest.webmanifest { alias /opt/bello/app/manifest.webmanifest; }
    location = /app-icon.svg        { alias /opt/bello/app/icon.svg; }

    # Der Dienst hinter der App. Er lauscht nur auf der Rueckschleife; von
    # aussen kommt man nur hier durch, und das Passwort gilt auch dafuer.
    location /api/ {
        proxy_pass http://127.0.0.1:8787;
        proxy_set_header Host $host;
        proxy_read_timeout 30s;
        client_max_body_size 64k;
    }

    # Ausdrueckliche Freigabe: nur diese beiden Seiten aus daten/. Alles andere
    # dort (auftraege.json, gedaechtnis.db, Markenbrief, Zeichnungen) faellt in
    # das 404 am Ende.
    location = /              { return 302 /app.html; }
    location = /dashboard.html { }
    location = /galerie.html   { }
    location /                 { return 404; }
}
NGINX
nginx -t >/dev/null 2>&1 && systemctl reload nginx && gut "Seite ist scharf" \
  || { schlecht "Konfiguration fehlerhaft — nichts uebernommen"; nginx -t; exit 1; }

# ---------- 6. Gegenprobe ----------
meldung "6/7  Dienst fuer die App"
if [ -f /opt/bello/systemd/bello-dienst.service ]; then
  cp /opt/bello/systemd/bello-dienst.service /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable --now bello-dienst.service >/dev/null 2>&1
  sleep 2
  if systemctl is-active --quiet bello-dienst.service; then
    gut "bello-dienst laeuft auf 127.0.0.1:8787"
  else
    schlecht "bello-dienst startet nicht — journalctl -u bello-dienst -n 20"
  fi
else
  echo "  --   systemd/bello-dienst.service fehlt (aelterer Stand? git pull)"
fi

meldung "7/7  Gegenprobe"
# Bei selbstsigniertem Zertifikat muss curl die Pruefung ueberspringen, sonst
# scheitert die Gegenprobe am Zertifikat statt an dem, was sie pruefen soll.
CURL_OPT=(-s -o /dev/null -w '%{http_code}')
[ "${1:-}" = "--selbstsigniert" ] && CURL_OPT+=(-k)

ohne=$(curl "${CURL_OPT[@]}" "https://$HOST/dashboard.html")
mit=$(curl "${CURL_OPT[@]}" -u "$BENUTZER:${PASSWORT}" "https://$HOST/dashboard.html" 2>/dev/null)
geheim=$(curl "${CURL_OPT[@]}" "https://$HOST/auftraege.json")
[ "$ohne" = "401" ] && gut "ohne Passwort: 401 (abgewiesen)" || schlecht "ohne Passwort: $ohne — erwartet 401"
[ "$geheim" = "401" ] || [ "$geheim" = "404" ] && gut "auftraege.json: $geheim (nicht erreichbar)" \
  || schlecht "auftraege.json liefert $geheim — BITTE MELDEN"
case "$mit" in 200) gut "mit Passwort: 200" ;; *) echo "  --   mit Passwort: $mit (bei bestehender Passwortdatei normal)" ;; esac

# Die API darf ohne Passwort genauso wenig erreichbar sein wie die Seiten.
api=$(curl "${CURL_OPT[@]}" "https://$HOST/api/stand")
[ "$api" = "401" ] && gut "API ohne Passwort: 401 (abgewiesen)" \
  || schlecht "API ohne Passwort: $api — erwartet 401, BITTE MELDEN"
# Und der Dienst muss von aussen unerreichbar sein, auch am Port vorbei.
direkt=$(curl -s -o /dev/null -w '%{http_code}' --max-time 4 "http://$HOST:8787/api/stand" 2>/dev/null || echo "kein")
[ "$direkt" = "kein" ] || [ "$direkt" = "000" ] && gut "Port 8787 von aussen dicht" \
  || schlecht "Port 8787 antwortet von aussen ($direkt) — BITTE MELDEN"

meldung "Fertig"
echo "  https://$HOST/          (die App)"
echo "  https://$HOST/dashboard.html  (die alte Werkbank)"
echo "  Benutzer: $BENUTZER"
echo "  Passwort: siehe $ZUGANG   (cat $ZUGANG)"
echo
echo "  Die Seite zeigt immer den letzten Lauf — sie wird stuendlich neu geschrieben."
echo "  Rueckbau: bash bin/dashboard-im-browser.sh --entfernen"
