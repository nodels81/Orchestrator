#!/usr/bin/env bash
# Spielt WordPress und WooCommerce auf den All-Inkl-Webspace, von netcup aus.
#
# Läuft über SSH mit dem Schlüssel aus schluessel-fuer-allinkl.sh. Drüben steht
# WP-CLI bereit, deshalb braucht es keinen Browser und keinen Assistenten.
#
#   bash web/betrieb/shop-aufspielen.sh --pruefen   # nur nachsehen, nichts tun
#   bash web/betrieb/shop-aufspielen.sh             # aufspielen
#
# Zugangsdaten stehen in /etc/bello/allinkl.env und nirgends sonst.

set -euo pipefail

UMGEBUNG="${ALLINKL_ENV:-/etc/bello/allinkl.env}"
NURPRUEFEN=0
[[ "${1:-}" == "--pruefen" ]] && NURPRUEFEN=1

# ---------------------------------------------------------------- Zugangsdaten

if [[ ! -f "${UMGEBUNG}" ]]; then
  cat >&2 <<TEXT
${UMGEBUNG} fehlt. Anlegen mit:

  install -m 600 /dev/null ${UMGEBUNG}
  nano ${UMGEBUNG}

Inhalt (die Werte stehen im KAS, das Kennwort kommt aus deinem Passwortmanager):

  ALLINKL_HOST=w022114f.kasserver.com
  ALLINKL_USER=ssh-w022114f
  ALLINKL_KEY=/root/.ssh/allinkl_bellowerk
  SHOP_PFAD=/www/htdocs/w022114f/bau
  SHOP_URL=https://bau.bellowerk.de
  DB_NAME=d0xxxxxx
  DB_USER=d0xxxxxx
  DB_HOST=localhost
  DB_PASS=...
  WP_TITEL=Bellowerk
  WP_ADMIN=bjoern
  WP_ADMIN_MAIL=info@bellowerk.de
  WP_ADMIN_PASS=...
TEXT
  exit 1
fi

if [[ "$(stat -c '%a' "${UMGEBUNG}")" != "600" ]]; then
  echo "${UMGEBUNG} ist zu offen. chmod 600 ${UMGEBUNG}" >&2
  exit 1
fi

# shellcheck disable=SC1090
set -a; source "${UMGEBUNG}"; set +a

for pflicht in ALLINKL_HOST ALLINKL_USER ALLINKL_KEY SHOP_PFAD SHOP_URL \
               DB_NAME DB_USER DB_HOST DB_PASS WP_TITEL WP_ADMIN WP_ADMIN_MAIL WP_ADMIN_PASS; do
  [[ -n "${!pflicht:-}" ]] || { echo "In ${UMGEBUNG} fehlt: ${pflicht}" >&2; exit 1; }
done

# ------------------------------------------------------------------- Werkzeuge

drueben() {
  ssh -i "${ALLINKL_KEY}" -o BatchMode=yes \
      "${ALLINKL_USER}@${ALLINKL_HOST}" "$@"
}

wp() {
  drueben "wp --path='${SHOP_PFAD}' $*"
}

melde() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# --------------------------------------------------------------------- Prüfung

melde "1. Verbindung"
drueben "echo '   Verbindung steht als '\$(whoami)"

melde "2. Werkzeuge drüben"
drueben "php -v | head -1; wp --version"

melde "3. Zielverzeichnis ${SHOP_PFAD}"
if drueben "test -d '${SHOP_PFAD}'"; then
  echo "   ist da"
else
  echo "   fehlt noch — wird beim Aufspielen angelegt"
fi

melde "4. Datenbank ${DB_NAME}"
if drueben "mysql -h'${DB_HOST}' -u'${DB_USER}' -p'${DB_PASS}' -e 'SELECT 1' '${DB_NAME}'" >/dev/null 2>&1; then
  echo "   erreichbar"
else
  echo "   NICHT erreichbar. Name, Benutzer oder Kennwort stimmen nicht," >&2
  echo "   oder die Datenbank ist im KAS noch in Bearbeitung." >&2
  exit 1
fi

melde "5. Steht dort schon ein WordPress?"
if wp core is-installed >/dev/null 2>&1; then
  SCHON_DA=1
  echo "   ja — es wird nichts überschrieben"
else
  SCHON_DA=0
  echo "   nein"
fi

if (( NURPRUEFEN )); then
  melde "Nur geprüft. Nichts verändert."
  exit 0
fi

if (( SCHON_DA )); then
  melde "Abbruch: dort steht bereits ein WordPress."
  echo "Das ist kein Fehler, sondern der Schutz davor, einen laufenden Shop zu überschreiben."
  echo "Soll wirklich neu aufgesetzt werden, erst drüben aufräumen."
  exit 1
fi

# ------------------------------------------------------------------ Aufspielen

melde "6. WordPress holen"
drueben "mkdir -p '${SHOP_PFAD}'"
wp core download --locale=de_DE

melde "7. Konfiguration schreiben"
wp config create \
  --dbname="'${DB_NAME}'" --dbuser="'${DB_USER}'" \
  --dbpass="'${DB_PASS}'" --dbhost="'${DB_HOST}'" \
  --locale=de_DE --skip-check

melde "8. WordPress einrichten"
wp core install \
  --url="'${SHOP_URL}'" \
  --title="'${WP_TITEL}'" \
  --admin_user="'${WP_ADMIN}'" \
  --admin_password="'${WP_ADMIN_PASS}'" \
  --admin_email="'${WP_ADMIN_MAIL}'" \
  --skip-email

melde "9. Suchmaschinen aussperren, solange gebaut wird"
wp option update blog_public 0

melde "10. WooCommerce"
wp plugin install woocommerce --activate

melde "11. Laden auf Deutschland und Regelbesteuerung stellen"
wp option update woocommerce_default_country DE:NI
wp option update woocommerce_currency EUR
wp option update woocommerce_currency_pos right_space
wp option update woocommerce_price_decimal_sep ,
wp option update woocommerce_price_thousand_sep .
wp option update woocommerce_calc_taxes yes
wp option update woocommerce_prices_include_tax yes
wp option update woocommerce_tax_display_shop incl
wp option update woocommerce_tax_display_cart incl

melde "12. Aufräumen: nichts Fremdes im Laden"
wp plugin delete akismet hello 2>/dev/null || true
wp theme install storefront --activate

melde "Fertig."
cat <<TEXT

Der Shop steht auf ${SHOP_URL}
Anmeldung: ${SHOP_URL}/wp-admin  (Benutzer ${WP_ADMIN})

Suchmaschinen sind ausgesperrt, solange gebaut wird — das wird erst beim
Umlegen auf die richtige Domain zurückgenommen, bewusst und nicht nebenbei.

Als Nächstes: das eigene Theme statt Storefront, die sieben Stücke als
Produkte, Steuerzonen für Drittländer, Versandzonen nach der DHL-Liste.
TEXT
