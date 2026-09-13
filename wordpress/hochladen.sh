#!/usr/bin/env bash
#
# hochladen.sh — Bringt das Theme per SFTP auf den Webspace.
#
# Zugangsdaten stehen NICHT in dieser Datei und gehören nicht nach Git.
# Sie werden aus wordpress/zugang.conf gelesen, die in .gitignore steht.
# Vorlage: zugang.beispiel.conf
#
# Warum SFTP und nicht FTP: Der All-Inkl-Tarif Premium hat SSH. Einfaches FTP
# überträgt Benutzername und Passwort im Klartext. Wer die Wahl hat, nimmt
# nicht die Variante, bei der das Passwort mitlesbar durchs Netz geht.
#
# Aufruf:
#   bash wordpress/hochladen.sh            Trockenlauf: zeigt, was passieren würde
#   bash wordpress/hochladen.sh --echt     Überträgt wirklich

set -euo pipefail

HIER="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUELLE="$HIER/bellowerk"
CONF="$HIER/zugang.conf"
ECHT=0
[ "${1:-}" = "--echt" ] && ECHT=1

rot()  { printf '\033[31m%s\033[0m\n' "$*"; }
fett() { printf '\033[1m%s\033[0m\n' "$*"; }

fett "=== Theme auf den Webspace bringen ==="
echo

# --- Vorbedingungen ------------------------------------------------------
[ -d "$QUELLE" ] || { rot "FEHLER: $QUELLE gibt es nicht."; exit 1; }
[ -f "$QUELLE/style.css" ] || { rot "FEHLER: $QUELLE ist kein Theme (style.css fehlt)."; exit 1; }

if [ ! -f "$CONF" ]; then
  rot "FEHLER: $CONF fehlt."
  echo "        Vorlage kopieren und ausfüllen:"
  echo "          cp wordpress/zugang.beispiel.conf wordpress/zugang.conf"
  echo "          chmod 600 wordpress/zugang.conf"
  exit 1
fi

# Rechte prüfen: eine Zugangsdatei, die alle lesen dürfen, ist keine.
RECHTE="$(stat -c '%a' "$CONF")"
if [ "$RECHTE" != "600" ]; then
  rot "FEHLER: $CONF hat Rechte $RECHTE, erwartet 600."
  echo "        Beheben mit:  chmod 600 $CONF"
  exit 1
fi

# shellcheck source=/dev/null
source "$CONF"
: "${SFTP_HOST:?SFTP_HOST fehlt in zugang.conf}"
: "${SFTP_USER:?SFTP_USER fehlt in zugang.conf}"
: "${ZIELPFAD:?ZIELPFAD fehlt in zugang.conf}"

# --- PHP prüfen, bevor etwas hochgeht ------------------------------------
if command -v php >/dev/null; then
  echo "Prüfe PHP-Dateien ..."
  FEHLER=0
  while IFS= read -r -d '' datei; do
    if ! php -l "$datei" >/dev/null 2>&1; then
      rot "  Syntaxfehler: ${datei#"$QUELLE/"}"
      php -l "$datei" 2>&1 | sed 's/^/      /'
      FEHLER=1
    fi
  done < <(find "$QUELLE" -name '*.php' -print0)
  if [ "$FEHLER" -eq 1 ]; then
    rot "Abbruch: kaputtes PHP wird nicht hochgeladen."
    exit 1
  fi
  echo "  Alle PHP-Dateien in Ordnung."
else
  echo "Hinweis: kein php vorhanden, Syntaxprüfung übersprungen."
fi
echo

command -v rsync >/dev/null || { rot "FEHLER: rsync fehlt. Auf Debian/Ubuntu: apt install rsync"; exit 1; }
command -v ssh >/dev/null   || { rot "FEHLER: ssh fehlt."; exit 1; }

echo "Quelle:  $QUELLE"
echo "Ziel:    $SFTP_USER@$SFTP_HOST:$ZIELPFAD"
echo

# --- Was übertragen wird -------------------------------------------------
# Ausgeschlossen wird alles, was auf dem Server nichts verloren hat.
AUSNAHMEN=(
  --exclude '.DS_Store'
  --exclude '*.swp'
  --exclude '.git*'
  --exclude 'node_modules'
)

# --delete räumt auf dem Server auf, was hier gelöscht wurde. Beschränkt auf
# den Theme-Ordner — es kann also nichts außerhalb getroffen werden.
GEMEINSAM=(
  -az --delete --itemize-changes
  "${AUSNAHMEN[@]}"
  -e ssh
  "$QUELLE/"
  "$SFTP_USER@$SFTP_HOST:$ZIELPFAD/"
)

if [ "$ECHT" -eq 0 ]; then
  fett "TROCKENLAUF — es wird nichts geschrieben."
  echo
  rsync --dry-run "${GEMEINSAM[@]}" | sed 's/^/  /'
  echo
  echo "Zeichen am Zeilenanfang: >f = Datei neu oder geändert, *deleting = wird gelöscht"
  echo
  echo "Wenn das stimmt, echt übertragen mit:"
  echo "  bash wordpress/hochladen.sh --echt"
  exit 0
fi

fett "ECHTE ÜBERTRAGUNG"
echo
rsync --dry-run "${GEMEINSAM[@]}" | sed 's/^/  /'
echo
read -r -p "Übertragen? Nur 'ja' führt aus: " ANTWORT
if [ "$ANTWORT" != "ja" ]; then
  echo "Abgebrochen. Nichts geändert."
  exit 0
fi

rsync "${GEMEINSAM[@]}" | sed 's/^/  /'

cat <<'ABSCHLUSS'

=== Übertragen ===

Danach im WordPress-Adminbereich:
  1. Design → Themes → "Bellowerk" aktivieren.
     Beim Aktivieren legt das Theme die fünf Rechtsseiten an, falls sie fehlen.
     Vorhandene Seiten werden NICHT überschrieben.
  2. Die Meldung oben im Adminbereich lesen: sie sagt, was angelegt wurde.
  3. Einstellungen → Permalinks einmal speichern, sonst greifen die Pfade nicht.

Prüfen, ob es steht:
  - Startseite aufrufen
  - Eine Produktseite aufrufen: steht die Herkunftsangabe direkt unter dem Preis?
  - Fußzeile: sind Impressum, Datenschutz, AGB, Widerruf und Versand verlinkt?
ABSCHLUSS
