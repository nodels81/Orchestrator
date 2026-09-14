#!/usr/bin/env bash
# produkte-einspielen.sh — Spielt produkte.csv in die WooCommerce-Installation
# auf dem Webspace ein, ohne Adminbereich und ohne Browser.
#
#   bash wordpress/produkte-einspielen.sh           auf die Baustelle
#   ZIEL=live bash wordpress/produkte-einspielen.sh auf den Shop
#
# Laeuft mehrfach ohne Schaden: gesucht wird ueber die Artikelnummer, ein
# schon vorhandener Artikel wird aktualisiert statt doppelt angelegt.

set -euo pipefail

HIER="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZUGANG="$HIER/zugang.conf"
CSV="$HIER/produkte.csv"
PHP="$HIER/produkte-import.php"

rot()  { printf '\033[31m%s\033[0m\n' "$*"; }
fett() { printf '\033[1m%s\033[0m\n' "$*"; }

[ -f "$ZUGANG" ] || { rot "FEHLER: $ZUGANG fehlt. Vorlage: zugang.beispiel.conf"; exit 1; }
[ -f "$CSV" ]    || { rot "FEHLER: $CSV fehlt. Erzeugen mit: python3 wordpress/produkte.py"; exit 1; }
[ -f "$PHP" ]    || { rot "FEHLER: $PHP fehlt."; exit 1; }

# 600 ist Pflicht: in der Datei steht, wo und als wer wir uns anmelden.
RECHTE="$(stat -c '%a' "$ZUGANG")"
[ "$RECHTE" = "600" ] || { rot "FEHLER: $ZUGANG hat Rechte $RECHTE, noetig sind 600."; echo "        chmod 600 $ZUGANG"; exit 1; }

# shellcheck disable=SC1090
. "$ZUGANG"
: "${SFTP_HOST:?SFTP_HOST fehlt in zugang.conf}"
: "${SFTP_USER:?SFTP_USER fehlt in zugang.conf}"
: "${ZIELPFAD:?ZIELPFAD fehlt in zugang.conf}"

# ZIELPFAD zeigt auf das Theme. Die WordPress-Wurzel liegt drei Ebenen hoeher.
WURZEL="${ZIELPFAD%/wp-content/themes/*}"
if [ "$WURZEL" = "$ZIELPFAD" ]; then
  rot "FEHLER: Aus ZIELPFAD laesst sich keine WordPress-Wurzel ableiten."
  echo "        Erwartet wird .../wp-content/themes/NAME, da steht: $ZIELPFAD"
  exit 1
fi

fett "=== Produkte einspielen ==="
echo "Ziel:    $SFTP_USER@$SFTP_HOST:$WURZEL"
echo "Quelle:  $CSV"
echo "Artikel: $(($(wc -l < "$CSV") - 1)) Zeile(n)"
echo

FERN="/tmp/bellowerk-produkte"
scp -q "$CSV" "$SFTP_USER@$SFTP_HOST:$FERN.csv"
scp -q "$PHP" "$SFTP_USER@$SFTP_HOST:$FERN.php"

# Aufraeumen auch dann, wenn der Import abbricht: die CSV hat auf einem
# Webspace nichts verloren, schon gar nicht unter einem ratbaren Namen.
aufraeumen() { ssh "$SFTP_USER@$SFTP_HOST" "rm -f $FERN.csv $FERN.php" 2>/dev/null || true; }
trap aufraeumen EXIT

set +e
ssh "$SFTP_USER@$SFTP_HOST" "cd '$WURZEL' && wp eval-file $FERN.php"
ERGEBNIS=$?
set -e

if [ "$ERGEBNIS" -ne 0 ]; then
  rot "Der Import meldet Fehler. Oben steht, welche Zeilen."
  exit "$ERGEBNIS"
fi

echo
fett "Stand danach:"
ssh "$SFTP_USER@$SFTP_HOST" "cd '$WURZEL' && wp post list --post_type=product --fields=ID,post_title,post_status --format=table"
