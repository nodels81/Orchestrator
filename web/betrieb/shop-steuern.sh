#!/usr/bin/env bash
# Setzt die Steuerzonen des Shops: 19 % in Deutschland und der EU, 0 % im Rest
# der Welt. Läuft auf dem netcup-Server, arbeitet über SSH auf dem Webspace.
#
#   bash web/betrieb/shop-steuern.sh --pruefen    # zeigt nur den Ist-Stand
#   bash web/betrieb/shop-steuern.sh              # setzt
#   bash web/betrieb/shop-steuern.sh --ersetzen   # setzt, auch wenn schon Sätze da sind
#
# WARUM SO:
#   Deutschland      19 %  Regelbesteuerung, keine Kleinunternehmerregelung
#   übrige EU        19 %  deutscher Satz, solange die 10.000-EUR-Schwelle hält
#                          und OSS nicht angemeldet ist
#   Drittländer       0 %  Ausfuhr ist steuerfrei, § 4 Nr. 1a i. V. m. § 6 UStG
#
# ACHTUNG: Reisst der EU-Umsatz die 10.000 EUR, gilt der Satz des Ziellandes —
# ab dem Paket, das die Schwelle reisst. Dann muss diese Datei geaendert und OSS
# angemeldet sein. Mit dem Steuerberater klaeren, nicht hier entscheiden.

set -euo pipefail

UMGEBUNG="${ALLINKL_ENV:-/etc/bello/allinkl.env}"
MODUS="setzen"
case "${1:-}" in
  --pruefen)  MODUS="pruefen" ;;
  --ersetzen) MODUS="ersetzen" ;;
  "")         ;;
  *) echo "Unbekannt: $1" >&2; exit 2 ;;
esac

[[ -f "${UMGEBUNG}" ]] || { echo "${UMGEBUNG} fehlt." >&2; exit 1; }
# shellcheck disable=SC1090
set -a; source "${UMGEBUNG}"; set +a

SATZ="19.0000"
NAME="MwSt."

# Deutschland zuerst, dann die übrigen 26 EU-Staaten.
EU=(DE AT BE BG HR CY CZ DK EE FI FR GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE)

wpr() {
  ssh -i "${ALLINKL_KEY}" -o BatchMode=yes "${ALLINKL_USER}@${ALLINKL_HOST}" \
      "wp --path='${SHOP_PFAD}' $*"
}

melde() { printf '\n\033[1m%s\033[0m\n' "$*"; }

# ------------------------------------------------------------------ Ist-Stand

melde "1. Ist-Stand"
PRAEFIX="$(wpr db prefix | tr -d '\r\n')"
TABELLE="${PRAEFIX}woocommerce_tax_rates"
ANZAHL="$(wpr db query "'SELECT COUNT(*) FROM ${TABELLE}'" --skip-column-names | tr -dc '0-9')"
echo "   Steuertabelle: ${TABELLE}"
echo "   vorhandene Sätze: ${ANZAHL:-0}"

echo "   Einstellungen:"
for o in woocommerce_calc_taxes woocommerce_prices_include_tax \
         woocommerce_tax_based_on woocommerce_default_country; do
  printf '     %-38s %s\n' "${o}" "$(wpr option get "${o}" 2>/dev/null | tr -d '\r\n' || echo '(nicht gesetzt)')"
done

if [[ "${MODUS}" == "pruefen" ]]; then
  if (( ${ANZAHL:-0} > 0 )); then
    melde "2. Die vorhandenen Sätze"
    wpr db query "'SELECT tax_rate_country, tax_rate, tax_rate_name, tax_rate_shipping \
      FROM ${TABELLE} ORDER BY tax_rate_order'"
  fi
  melde "Nur geprüft. Nichts verändert."
  exit 0
fi

if (( ${ANZAHL:-0} > 0 )) && [[ "${MODUS}" != "ersetzen" ]]; then
  melde "Abbruch: es stehen schon ${ANZAHL} Steuersätze drin."
  echo "Damit wird nichts stillschweigend überschrieben. Wenn sie weg sollen:"
  echo "  bash \$0 --ersetzen"
  exit 1
fi

# --------------------------------------------------------------------- Setzen

melde "2. Grundeinstellungen"
wpr option update woocommerce_calc_taxes yes
wpr option update woocommerce_prices_include_tax yes
wpr option update woocommerce_tax_based_on shipping      # nach Lieferadresse
wpr option update woocommerce_tax_display_shop incl
wpr option update woocommerce_tax_display_cart incl
wpr option update woocommerce_tax_total_display itemized
echo "   gesetzt"

if [[ "${MODUS}" == "ersetzen" ]]; then
  melde "3. Alte Sätze entfernen"
  wpr db query "'DELETE FROM ${TABELLE}'"
  wpr db query "'DELETE FROM ${PRAEFIX}woocommerce_tax_rate_locations'" 2>/dev/null || true
  echo "   entfernt"
fi

melde "4. Sätze für Deutschland und die EU"

# Bevorzugt über die WooCommerce-Befehle, sonst direkt in die Tabelle.
if wpr wc tax --help >/dev/null 2>&1; then
  WEG="wp wc tax"
else
  WEG="Datenbank"
fi
echo "   Weg: ${WEG}"

ORDNUNG=0
for land in "${EU[@]}"; do
  if [[ "${WEG}" == "wp wc tax" ]]; then
    wpr wc tax create --country="${land}" --rate="${SATZ}" --name="'${NAME}'" \
        --shipping=true --priority=1 --order="${ORDNUNG}" --user=1 --porcelain >/dev/null
  else
    wpr db query "\"INSERT INTO ${TABELLE} \
      (tax_rate_country, tax_rate_state, tax_rate, tax_rate_name, tax_rate_priority, \
       tax_rate_compound, tax_rate_shipping, tax_rate_order, tax_rate_class) \
      VALUES ('${land}', '', ${SATZ}, '${NAME}', 1, 0, 1, ${ORDNUNG}, '')\""
  fi
  printf '   %s' "${land}"
  ORDNUNG=$((ORDNUNG + 1))
done
echo

melde "5. Zwischenspeicher leeren"
wpr transient delete --all >/dev/null 2>&1 || true
wpr cache flush >/dev/null 2>&1 || true
echo "   geleert"

melde "6. Gegenprobe"
wpr db query "'SELECT COUNT(*) AS saetze FROM ${TABELLE}'"

cat <<'TEXT'

Fertig.

  Deutschland und EU   19 %, im Preis enthalten
  alles Übrige          0 %, weil dafür kein Satz eingetragen ist

Genau so ist die Ausfuhr gemeint: kein Satz heisst kein Aufschlag. Ein Kunde in
der Schweiz oder den USA zahlt jetzt keine deutsche Umsatzsteuer mehr.

Offen und nicht von hier zu entscheiden:
  - OSS anmelden, bevor der EU-Umsatz 10.000 EUR im Jahr reisst
  - danach diese Datei auf die Zielland-Saetze umstellen
TEXT
