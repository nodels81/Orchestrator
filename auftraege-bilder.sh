#!/usr/bin/env bash
#
# auftraege-bilder.sh — Legt die Auftraege an, die vor dem Shopstart laufen muessen:
# Produktfotos und Produktbeschreibungen.
#
# Auf dem Server ausfuehren, dort liegt auftraege.json:
#   cd /opt/bello && bash auftraege-bilder.sh
#
# Trockenlauf zuerst:
#   bash auftraege-bilder.sh --probe

set -euo pipefail

PROBE=0
[ "${1:-}" = "--probe" ] && PROBE=1
PYTHON="venv/bin/python"
[ -x "$PYTHON" ] || PYTHON="$(command -v python3)"

# Welche Abteilungen kennt dieser Orchestrator wirklich?
BEKANNT="$("$PYTHON" -c 'import orchestrator; print("|".join(orchestrator.ABTEILUNGEN))' 2>/dev/null || echo "")"
if [ -z "$BEKANNT" ]; then
  echo "FEHLER: orchestrator.py nicht lesbar. Im Betriebsordner ausfuehren."
  exit 1
fi
echo "Bekannte Abteilungen: $BEKANNT"
echo

anlegen() {
  local abteilung="$1" ziel="$2" frist="$3"
  if ! printf '%s' "$BEKANNT" | grep -q -- "$abteilung"; then
    echo "  UEBERSPRUNGEN — '$abteilung' kennt dieser Orchestrator nicht:"
    echo "                 $ziel"
    return 0
  fi
  if [ "$PROBE" -eq 1 ]; then
    echo "  [Probe] $abteilung <- $ziel (Frist $frist)"
    return 0
  fi
  "$PYTHON" orchestrator.py --auftrag "$abteilung" "$ziel" "$frist"
}

FRIST_FOTOS="$(date -d '+21 days' +%F 2>/dev/null || date -v+21d +%F)"
FRIST_TEXT="$(date -d '+10 days' +%F 2>/dev/null || date -v+10d +%F)"

echo "=== Fotos ==="
anlegen "02 Produkt & Ausführung" \
  "Die elf Aufnahmen aus web/aufnahmen/aufnahmeliste-und-bildprompts.md planen und durchfuehren. Eine Lichtsituation fuer alle: hartes Seitenlicht von links, dunkler Hintergrund, warme Farben. Zwei Paare muessen neu und getragen zeigen (Nr. 07 und 08). Ergebnis: elf Dateien in web/bilder/, benannt foto-01.jpg bis foto-11.jpg, plus je ein Satz Alternativtext fuer Blinde. Produktfotos sind echte Fotos, ausnahmslos — kein KI-Bild." \
  "$FRIST_FOTOS"

echo
echo "=== Beschreibungen ==="
anlegen "01 Innovation" \
  "Fuer HB-01, LE-01, HS-01 und HB-02 je eine Produktbeschreibung liefern, die ueber die Werkstoffliste hinausgeht: Wofuer ist das Stueck gedacht, fuer welchen Hund, was merkt der Kunde nach einem halben Jahr. Hoechstens 120 Woerter je Stueck. Bindend: sourcing/bellowerk/markenbrief.md. Keine ausgeschlossenen Werkstoffe, kein Preisargument, kein Einstieg ueber Windhunde." \
  "$FRIST_TEXT"

echo
echo "=== Pruefdaten ==="
anlegen "02 Produkt & Ausführung" \
  "Die echten Pruefdaten fuer den Praxistest zusammenstellen: je Modell wie viele Hunde, ueber wie viele Tage, bei welchem Wetter, welche Befunde. Auf den vier Produktseiten stehen zurzeit Platzhalter, die vor der Veroeffentlichung ersetzt werden muessen — oder die Sektion faellt weg. Erfundene Pruefzahlen sind angreifbare Werbung." \
  "$FRIST_TEXT"

cat <<'ABSCHLUSS'

=== Fertig ===

Stand ansehen:
  venv/bin/python orchestrator.py --stand

Kommt eine Zeile "UEBERSPRUNGEN", kennt der Orchestrator diese Abteilung nicht.
Das betrifft "06 Web & Shop": Auf dem Server ist 06 der Einkauf. Siehe
SERVER-ABGLEICH.md, Schritt 2 — die Nummer ist noch nicht entschieden.
ABSCHLUSS
