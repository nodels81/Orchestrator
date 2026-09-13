"""
produkte.py — Erzeugt produkte.csv fuer den WooCommerce-Import.

Grund: Vier Produkte mit Beschreibung, Masstabelle, Pflegehinweis und
Eigenschaften von Hand im Adminbereich anzulegen dauert eine Stunde und
enthaelt danach Tippfehler. Der Importer von WooCommerce liest eine CSV,
und die kommt aus denselben Daten wie die Entwurfsseiten.

Die Daten fuer Hamburg No. 2, 3 und 4 werden aus web/vorlagen/seiten_bauen.py
importiert, damit Preis und Text nicht an zwei Stellen gepflegt werden. Nur
HB-01 steht hier zusaetzlich, weil seine Seite von Hand gepflegt wird.

Aufruf:
  python3 wordpress/produkte.py            schreibt wordpress/produkte.csv
  python3 wordpress/produkte.py --zeigen   nur anzeigen, nichts schreiben
"""

import csv
import html
import pathlib
import re
import sys

BASIS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASIS / "web" / "vorlagen"))

from seiten_bauen import STUECKE  # noqa: E402

ZIEL = BASIS / "wordpress" / "produkte.csv"

# HB-01 wird von Hand gepflegt und steht deshalb nicht in STUECKE.
HB01 = {
    "name": "Hamburg No. 1",
    "sku": "HB-01",
    "art": "Halsband Fettleder",
    "preis": "89,00",
    "preis_zahl": "89.00",
    "einsatz": "Einlagig, ohne Naht, aus einem Stück geschnitten. Was nicht zusammengenäht ist, kann nicht aufgehen.",
    "beschreibung": "Halsband aus pflanzlich gegerbtem Fettleder, einlagig und ohne Naht aus einem Stück geschnitten. Beschläge aus massivem Messing.",
    "masse_kopf": ["Größe", "Halsumfang", "Breite", "Stärke"],
    "masse": [["S", "30–38 cm", "20 mm", "3,5 mm"],
              ["M", "38–46 cm", "25 mm", "3,5 mm"],
              ["L", "46–54 cm", "30 mm", "4,0 mm"],
              ["XL", "54–62 cm", "40 mm", "4,0 mm"]],
    "material": [
        ("Leder", "Rindfettleder, pflanzlich gegerbt, gefettet, Vollnarbe, durchgefärbt. 3,5 bis 4,0 mm."),
        ("Beschläge", "Massives Messing, unlackiert: Rollschnalle, geschweißter D-Ring."),
        ("Schrauben", "Buchschrauben aus Messing mit gewölbtem Kopf, mit Schraubensicherung."),
        ("Patch", "Lederpatch, lasergraviert, mit zwei Buchschrauben befestigt."),
    ],
    "wahl": [("S", "30–38 cm", False), ("M", "38–46 cm", True),
             ("L", "46–54 cm", False), ("XL", "54–62 cm", False)],
}

LEDERFARBEN = "Grau | Dunkelbraun | Oliv | Cognac | Schwarz"

PFLEGE = (
    "<h3>Pflege</h3>"
    "<p>Zwei- bis dreimal im Jahr mit Lederfett einreiben, dünn und mit der Hand. "
    "Nass geworden? Bei Zimmertemperatur trocknen lassen, nie an der Heizung. "
    "Das Messing läuft an — das ist die Patina und schützt vor weiterer Oxidation. "
    "Wer es blank mag, reibt es mit einem Tuch und etwas Zitronensäure ab.</p>"
)

NICHT_DRIN = (
    "<h3>Kommt nicht vor</h3>"
    "<p>Nähte und Garn · Nieten · Stahl, auch vermessingt · Zinkdruckguss · "
    "Kunststoff und Klickverschlüsse · Gurtband und Nylon</p>"
)


def _tabelle(kopf: list[str], zeilen: list[list[str]]) -> str:
    k = "".join(f"<th>{html.escape(x)}</th>" for x in kopf)
    r = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(w))}</td>" for w in z) + "</tr>"
        for z in zeilen
    )
    return f"<h3>Maße</h3><table><thead><tr>{k}</tr></thead><tbody>{r}</tbody></table>"


def beschreibung_bauen(s: dict) -> str:
    teile = [f"<p>{html.escape(s['beschreibung'])}</p>"]
    teile.append(_tabelle(s["masse_kopf"], s["masse"]))
    werkstoff = "".join(
        f"<li><strong>{html.escape(b)}</strong> — {html.escape(w)}</li>"
        for b, w in s["material"]
    )
    teile.append(f"<h3>Material</h3><ul>{werkstoff}</ul>")
    teile.append(PFLEGE)
    teile.append(NICHT_DRIN)
    return "".join(teile)


def groessen(s: dict) -> str:
    if not s.get("wahl"):
        return ""
    return " | ".join(kurz for kurz, _, _ in s["wahl"])


SPALTEN = [
    "Type", "SKU", "Name", "Published", "Is featured?", "Visibility in catalog",
    "Short description", "Description", "Tax status", "Tax class",
    "In stock?", "Backorders allowed?", "Regular price", "Categories",
    "Allow customer reviews?", "Position",
    "Attribute 1 name", "Attribute 1 value(s)", "Attribute 1 visible", "Attribute 1 global",
    "Attribute 2 name", "Attribute 2 value(s)", "Attribute 2 visible", "Attribute 2 global",
]


def zeile(s: dict, position: int, kategorie: str) -> dict:
    gr = groessen(s)
    return {
        "Type": "simple",
        "SKU": s["sku"],
        "Name": s["name"],
        "Published": 1,
        "Is featured?": 0,
        "Visibility in catalog": "visible",
        "Short description": s["einsatz"],
        "Description": beschreibung_bauen(s),
        "Tax status": "taxable",
        "Tax class": "",
        "In stock?": 1,
        "Backorders allowed?": 0,
        "Regular price": s["preis_zahl"],
        "Categories": kategorie,
        "Allow customer reviews?": 1,
        "Position": position,
        "Attribute 1 name": "Größe" if gr else "",
        "Attribute 1 value(s)": gr,
        "Attribute 1 visible": 1 if gr else "",
        "Attribute 1 global": 1 if gr else "",
        "Attribute 2 name": "Leder",
        "Attribute 2 value(s)": LEDERFARBEN,
        "Attribute 2 visible": 1,
        "Attribute 2 global": 1,
    }


KATEGORIEN = {
    "HB-01": "Halsbänder", "HB-02": "Halsbänder",
    "LE-01": "Leinen", "HS-01": "Zubehör",
}


def zeilen_bauen() -> list[dict]:
    alle = [HB01] + list(STUECKE)
    # Reihenfolge wie im Werkverzeichnis: No. 1, 2, 3, 4
    alle.sort(key=lambda s: int(re.search(r"No\. (\d+)", s["name"]).group(1)))
    return [
        zeile(s, i, KATEGORIEN.get(s["sku"], "Kollektion"))
        for i, s in enumerate(alle)
    ]


def main() -> int:
    zeilen = zeilen_bauen()

    if "--zeigen" in sys.argv:
        for z in zeilen:
            print(f"  {z['Position']}  {z['SKU']:8} {z['Name']:16} "
                  f"{z['Regular price']:>7} EUR  {z['Categories']:12} "
                  f"Größen: {z['Attribute 1 value(s)'] or '—'}")
        return 0

    with open(ZIEL, "w", encoding="utf-8-sig", newline="") as f:
        schreiber = csv.DictWriter(f, fieldnames=SPALTEN)
        schreiber.writeheader()
        schreiber.writerows(zeilen)

    print(f"{ZIEL.relative_to(BASIS)} geschrieben: {len(zeilen)} Produkte")
    for z in zeilen:
        print(f"  {z['SKU']:8} {z['Name']:16} {z['Regular price']:>7} EUR")
    return 0


if __name__ == "__main__":
    sys.exit(main())
