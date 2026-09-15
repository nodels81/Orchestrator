"""bauen.py — verkleinert Zeichnungen und Fotos fuer die Freigabe-Mappe.

Die Originale in ../bilder und ../zeichnungen sind bis 1,8 MB gross; als Artifact
duerfen alle Dateien zusammen nicht ausufern. Dieses Skript legt verkleinerte
Kopien in ./media ab — genau die Dateien, die index.html referenziert.

    pip install Pillow
    python3 sourcing/bellowerk/freigabe/bauen.py

Danach die Mappe veroeffentlichen: index.html plus den Ordner media/.
"""

import pathlib

from PIL import Image

ORDNER = pathlib.Path(__file__).parent
QUELLE = ORDNER.parent
ZIEL = ORDNER / "media"

FOTOS = [
    "HB-01-hamburg-patch-detail.jpg",
    "HB-04-farben-patch.jpg",
    "HB-04-detail-dring-namenspatch.jpg",
    "HB-02-geflochten-am-hund.jpg",
    "HB-02-zweifarbig-am-hund.jpg",
    "HB-02-und-LE-01-gruen.jpg",
    "LE-01-detail-karabiner-flechtung.jpg",
    "LE-01-flechtung-ringe-farben.jpg",
    "LE-01-flechtung-karabiner-gruen.jpg",
    "LE-01-ringe-flechtung-pink.jpg",
    "LE-01-farben-pink-tuerkis.jpg",
    "PATCH-01-und-flechtung-detail.jpg",
    "PATCH-01-namensgravur-detail.jpg",
    "PATCH-01-namenspatch-august.jpg",
    "PATCH-01-namenspatch-detail.jpg",
]

ZEICHNUNGEN = [
    "HB-04-halsband.png",
    "HB-02-geflochten.png",
    "HB-01-hamburg.png",
    "LE-01-fuehrleine.png",
    "PATCH-01-lederpatch.png",
]


# Die Darstellung des fertigen Halsbands liegt als SVG im Shop-Ordner und wird
# als JPG mitgeliefert, weil sie in Freigabe-Mappe und Shop-Seite steht.
ANSICHT = ORDNER.parent / "shop" / "HB-01-ansicht.png"


def main() -> None:
    ZIEL.mkdir(exist_ok=True)
    if ANSICHT.exists():
        bild = Image.open(ANSICHT).convert("RGB")
        bild.thumbnail((1960, 1960), Image.LANCZOS)
        bild.save(ZIEL / "HB-01-ansicht.jpg", "JPEG", quality=88, optimize=True, progressive=True)
    gesamt = 0
    for name in FOTOS:
        bild = Image.open(QUELLE / "bilder" / name).convert("RGB")
        bild.thumbnail((1400, 1400), Image.LANCZOS)
        pfad = ZIEL / name
        bild.save(pfad, "JPEG", quality=82, optimize=True, progressive=True)
        gesamt += pfad.stat().st_size
    for name in ZEICHNUNGEN:
        bild = Image.open(QUELLE / "zeichnungen" / name).convert("RGB")
        bild.thumbnail((1800, 1800), Image.LANCZOS)
        pfad = ZIEL / name
        bild.save(pfad, "PNG", optimize=True)
        gesamt += pfad.stat().st_size
    print(f"{len(FOTOS) + len(ZEICHNUNGEN)} Dateien in {ZIEL}, zusammen {gesamt // 1024} KB")


if __name__ == "__main__":
    main()
