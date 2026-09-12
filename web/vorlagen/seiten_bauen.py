"""
seiten_bauen.py — Erzeugt die Produktseiten aus einer gemeinsamen Vorlage.

Grund: Vier Produktseiten von Hand zu pflegen heisst, dass sie nach der
dritten Aenderung auseinanderlaufen. Kopf, Fuss, Preisblock und
Herkunftsangabe kommen deshalb aus einer Quelle. Nur der Inhalt je Stueck
steht unten in STUECKE.

Die Herkunftsangabe steht per Vorlage im selben Block wie Preis und Groesse.
Sie laesst sich nicht versehentlich weglassen, das ist der Sinn der Uebung.
"""
import html
import json
import pathlib
import re

WEB = pathlib.Path("/home/user/Orchestrator/web")
STAND = "12.09.2026"

# ── Inhalt je Stueck. Preise aus konzepte/kollektion-01-hamburg.md. ──────
STUECKE = [
    {
        "datei": "produkt-hamburg-no-2.html",
        "name": "Hamburg No. 2", "sku": "LE-01", "art": "Führleine 3,00 m",
        "preis": "129,00", "preis_zahl": "129.00",
        "augenbraue": "Werkverzeichnis · zweites Stück",
        "einsatz": "Drei Meter, dreifach verstellbar, sechs Führlängen. Eine Leine statt vier.",
        "beschreibung": "Führleine aus pflanzlich gegerbtem Fettleder, 3,00 m lang und dreifach verstellbar. Karabiner und Ringe sind im Mystery Braid eingeflochten, ohne Naht.",
        "bild": "radial-gradient(120% 92% at 28% 20%,#463726,#120F09 76%)",
        "bild_nr": "FOTO 03 · LE-01 an einem Haken hängend<br>Gegenlicht · Halbtotale, ganze Leine",
        "reihe": [("03","hängend","radial-gradient(120% 92% at 28% 20%,#463726,#120F09 76%)"),
                   ("09","Flechtung","radial-gradient(120% 92% at 38% 18%,#5E4A2E,#141009 76%)"),
                   ("06","Karabiner","radial-gradient(120% 92% at 40% 22%,#6B5730,#15110A 76%)"),
                   ("05","im Einsatz","radial-gradient(120% 92% at 26% 20%,#463726,#120F09 76%)")],
        "wahl_titel": "Führlänge", "wahl_vorgabe": "alle sechs Längen inbegriffen",
        "wahl": None,
        "masse_titel": "Sechs Längen aus einer Leine",
        "masse_leit": "Die Ringe sitzen bei 45, 140 und 245 cm. Aus diesen drei Punkten ergeben sich sechs Führlängen, ohne dass etwas umgeschnallt wird.",
        "masse_kopf": ["Führung", "Länge", "Wofür"],
        "masse": [["kurz am Körper","0,45 m","Verkehr, Tierarzt, enge Wege"],
                   ["Standard","1,40 m","Alltag an der Seite"],
                   ["lang","2,45 m","freies Laufen mit Kontrolle"],
                   ["ganz lang","3,00 m","Feld und Wald"],
                   ["über der Schulter","1,40 m","Hände frei"],
                   ["um die Hüfte","2,45 m","Joggen"]],
        "material": [("Leder","Rindfettleder, pflanzlich gegerbt, gefettet. 20 mm breit, 3,5 mm stark."),
                      ("Beschläge","Massives Messing: Wirbel-Bolzenkarabiner, zwei geschweißte O-Ringe."),
                      ("Flechtung","Dreisträngiger Mystery Braid aus einem Stück — so hält der Karabiner ohne Naht."),
                      ("Schrauben","Buchschrauben aus Messing mit Schraubensicherung.")],
        "fragen": [
            ("Warum ist die Leine nicht vernäht?",
             "Weil eine Naht die schwächste Stelle wäre. Der Mystery Braid führt das Leder aus einem Stück um den Ring herum und wieder zurück — es gibt nichts, was aufgehen könnte, weil nichts zusammengefügt ist."),
            ("Drei Meter sind lang. Verheddert sich das nicht?",
             "Nur wenn man alle drei Meter laufen lässt. Im Alltag ist die Leine auf 1,40 m geschnallt und damit kürzer als die meisten festen Leinen. Die volle Länge braucht man im Feld, nicht in der Stadt."),
            ("Hält der Karabiner einen großen Hund?",
             "Der Wirbel-Bolzenkarabiner ist massives Messing. Die Bruchlast steht im Materialdatenblatt des Herstellers. Gerissen ist im Praxistest keiner — bei welcher Last er aufgibt, steht hier erst, wenn es gemessen ist."),
            ("Kann ich die Leine kürzen lassen?",
             "Ja. Schick sie ein, wir nehmen heraus und flechten neu. Die Ringpositionen verschieben sich dann entsprechend."),
        ],
        "praxis_h": "Drei Meter Leder, ein halbes Jahr am Hund.",
        "praxis_p": "Eine Leine merkt man erst nach Wochen an: wie sie in der Hand liegt, ob der Karabiner klemmt, ob die Flechtung sich zieht. Genau deshalb hängt jedes Modell eine Saison im Betrieb, bevor es in den Verkauf geht.",
    },
    {
        "datei": "produkt-hamburg-no-3.html",
        "name": "Hamburg No. 3", "sku": "HS-01", "art": "Handschlaufe",
        "preis": "39,00", "preis_zahl": "39.00",
        "augenbraue": "Werkverzeichnis · drittes Stück",
        "einsatz": "Fünfzig Zentimeter Umfang. Für die Leine am Gürtel oder über der Schulter.",
        "beschreibung": "Handschlaufe aus pflanzlich gegerbtem Fettleder, 50 cm Umfang, mit massivem Messingring.",
        "bild": "radial-gradient(120% 92% at 36% 24%,#413424,#120E08 76%)",
        "bild_nr": "FOTO 04 · HS-01 in der Hand<br>Daumen durch die Schlaufe · Makro",
        "reihe": [("04","in der Hand","radial-gradient(120% 92% at 36% 24%,#413424,#120E08 76%)"),
                   ("06","Ring","radial-gradient(120% 92% at 40% 22%,#6B5730,#15110A 76%)"),
                   ("10","am Gürtel","radial-gradient(120% 92% at 30% 20%,#4A3B27,#131009 76%)"),
                   ("07","getragen","radial-gradient(120% 92% at 34% 18%,#4C3D28,#131009 76%)")],
        "wahl_titel": None, "wahl_vorgabe": None, "wahl": None,
        "masse_titel": "Ein Maß, das passt",
        "masse_leit": "Fünfzig Zentimeter Umfang sind für eine Hand mit Handschuh gerechnet. Ohne Handschuh bleibt Luft, und das ist Absicht.",
        "masse_kopf": ["Maß", "Wert"],
        "masse": [["Umfang","50 cm"],["Breite","20 mm"],["Stärke","3,5 mm"],["Ring","Messing, geschweißt, 25 mm"]],
        "material": [("Leder","Rindfettleder, pflanzlich gegerbt, gefettet, durchgefärbt."),
                      ("Ring","Massives Messing, geschweißt, unlackiert."),
                      ("Schrauben","Zwei Buchschrauben aus Messing.")],
        "fragen": [
            ("Wofür brauche ich die überhaupt?",
             "Damit die Leine an den Gürtel oder über die Schulter kann, ohne dass du sie hältst. Beim Joggen, beim Einkaufen, beim Arbeiten im Garten. Eine Hand frei ist der ganze Zweck."),
            ("Passt sie an jede Leine?",
             "An jede Leine dieser Kollektion. Der Ring nimmt den Karabiner der Hamburg No. 2 auf. Bei fremden Leinen kommt es auf den Karabiner an."),
            ("Ist das nicht teuer für ein Stück Leder?",
             "Es ist derselbe Werkstoff und dieselbe Arbeit wie beim Halsband, nur kürzer. Billiger ginge nur mit dünnerem Leder oder mit einer Naht — beides wollen wir nicht."),
        ],
        "praxis_h": "Das kleinste Stück, am längsten geprüft.",
        "praxis_p": "Eine Handschlaufe scheuert oder sie tut es nicht. Das zeigt sich nicht in der Woche, sondern im Monat — deshalb lief dieses Stück im Betrieb mit, bevor es überhaupt in den Katalog kam.",
    },
    {
        "datei": "produkt-hamburg-no-4.html",
        "name": "Hamburg No. 4", "sku": "HB-02", "art": "Halsband geflochten",
        "preis": "99,00", "preis_zahl": "99.00",
        "augenbraue": "Werkverzeichnis · viertes Stück",
        "einsatz": "Dreisträngiger Mystery Braid aus einem Stück. Geflochten, nicht zusammengesetzt.",
        "beschreibung": "Geflochtenes Halsband aus pflanzlich gegerbtem Fettleder. Das Halsteil ist ein dreisträngiger Mystery Braid aus einem Stück, die Enden bleiben flach.",
        "bild": "radial-gradient(120% 92% at 34% 22%,#4C3D28,#131009 76%)",
        "bild_nr": "FOTO 02 · HB-02 Flechtung schräg von oben<br>Licht quer zur Flechtung · Makro",
        "reihe": [("02","Flechtung","radial-gradient(120% 92% at 34% 22%,#4C3D28,#131009 76%)"),
                   ("06","Schnalle","radial-gradient(120% 92% at 40% 22%,#6B5730,#15110A 76%)"),
                   ("11","zweifarbig","radial-gradient(120% 92% at 30% 18%,#5A462E,#141009 74%)"),
                   ("05","am Hund","radial-gradient(120% 92% at 26% 20%,#463726,#120F09 76%)")],
        "wahl_titel": "Größe", "wahl_vorgabe": "M · 38 bis 46 cm",
        "wahl": [("S","30–38 cm",False),("M","38–46 cm",True),("L","46–54 cm",False),("XL","54–62 cm",False)],
        "masse_titel": "Vier Größen, in Zentimetern",
        "masse_leit": "Gemessen wird der Halsumfang, nicht das alte Halsband. Zwischen Band und Hals müssen zwei Finger passen. Die Flechtung trägt etwas auf — das ist eingerechnet.",
        "masse_kopf": ["Größe", "Halsumfang", "Breite geflochten", "Stärke"],
        "masse": [["S","30–38 cm","22 mm","3,5 mm"],["M","38–46 cm","27 mm","3,5 mm"],
                   ["L","46–54 cm","32 mm","4,0 mm"],["XL","54–62 cm","42 mm","4,0 mm"]],
        "material": [("Leder","Rindfettleder, pflanzlich gegerbt. Ein- oder zweifarbig geflochten."),
                      ("Flechtung","Dreisträngiger Mystery Braid, V-Muster, aus einem Stück geschnitten."),
                      ("Beschläge","Massives Messing: Rollschnalle, geschweißter O-Ring."),
                      ("Schrauben","Buchschrauben aus Messing mit Schraubensicherung.")],
        "fragen": [
            ("Was ist ein Mystery Braid?",
             "Eine Flechtung, bei der das Leder nicht zerschnitten und wieder zusammengesetzt wird. Drei Stränge werden aus einem Stück gestanzt und so verdreht, dass am Ende ein geflochtenes Band steht, das an beiden Enden noch aus einem Stück besteht. Deshalb hält es ohne Naht."),
            ("Sammelt sich in der Flechtung Schmutz?",
             "Weniger als man denkt, weil das Band flach bleibt und keine Hohlräume hat. Nass gewordener Sand wird mit einer trockenen Bürste ausgebürstet, wenn das Leder wieder trocken ist."),
            ("Zweifarbig — wie geht das ohne Naht?",
             "Gar nicht aus einem Stück. Für die zweifarbige Ausführung laufen zwei Lederstreifen nebeneinander durch dieselbe Flechtung, verschraubt an den flachen Enden. Auch hier ohne Naht."),
            ("Hält geflochten genauso wie einlagig?",
             "Die Flechtung verteilt Zug über drei Stränge statt über einen. Schwachstelle ist wie beim einlagigen Band die Schnalle, und die ist massives Messing."),
        ],
        "praxis_h": "Geflochten ist schöner. Hält es auch?",
        "praxis_p": "Genau das war die Frage, wegen der dieses Modell eine ganze Saison länger geprüft wurde als das einlagige. Eine Flechtung, die sich zieht, sieht nach drei Monaten aus wie ein Fehler — und deshalb kam sie erst danach in den Katalog.",
    },
]

# Prüfzahlen je Stück. Alle Platzhalter, auf der Seite als solche markiert.
PRUEFZAHLEN = {"LE-01": ("9", "168"), "HS-01": ("11", "203"), "HB-02": ("7", "154")}


def masse_tabelle(kopf, zeilen):
    kopfteil = "".join(f"<th>{html.escape(k)}</th>" for k in kopf)
    koerper = []
    for z in zeilen:
        zellen = "".join(
            ('<td class="tab">' if i else "<td>") + html.escape(str(w)) + "</td>"
            for i, w in enumerate(z))
        koerper.append(f"<tr>{zellen}</tr>")
    return kopfteil, "\n              ".join(koerper)


def galerie(reihe):
    teile = []
    for i, (nr, was, farbe) in enumerate(reihe):
        teile.append(
            f'<button aria-current="{"true" if i == 0 else "false"}" '
            f'aria-label="Ansicht {i+1}: {html.escape(was)}">\n'
            f'          <div class="bildplatz" style="--flaeche-bild:{farbe}">'
            f'<span>{nr}<br>{html.escape(was)}</span></div>\n        </button>')
    return "\n        ".join(teile)


def wahlblock(s):
    """Groessenwahl, Hinweis ohne Wahl, oder gar nichts."""
    if s["wahl"]:
        knoepfe = []
        for kurz, _spanne, gewaehlt in s["wahl"]:
            kid = f"g-{kurz.lower()}"
            knoepfe.append(
                f'<input type="radio" name="groesse" id="{kid}" value="{kurz}"'
                f'{" checked" if gewaehlt else ""}><label for="{kid}">{kurz}</label>')
        return f"""      <div class="wahlblock">
        <div class="wahlkopf">
          <span>{s["wahl_titel"]} — <span class="gewaehlt" id="groesse-gewaehlt">{s["wahl_vorgabe"]}</span></span>
          <a href="startseite-nachtwerkstatt.html#finder">Größe finden</a>
        </div>
        <div class="wahl" role="radiogroup" aria-label="{s["wahl_titel"]}">
          {"".join(knoepfe)}
        </div>
      </div>
"""
    if s["wahl_titel"]:
        return f"""      <div class="wahlblock">
        <div class="wahlkopf"><span>{s["wahl_titel"]} — <span class="gewaehlt">{s["wahl_vorgabe"]}</span></span></div>
        <p class="feld-hinweis">Alle sechs Längen stecken in derselben Leine. Es gibt nichts auszuwählen.</p>
      </div>
"""
    return ""


def bauen(s, vorlage):
    kopfteil, zeilen = masse_tabelle(s["masse_kopf"], s["masse"])
    hunde, tage = PRUEFZAHLEN[s["sku"]]

    werte = {
        "NAME": s["name"], "SKU": s["sku"], "ART": s["art"], "PREIS": s["preis"],
        "AUGENBRAUE": s["augenbraue"], "EINSATZ": s["einsatz"],
        "BESCHREIBUNG": s["beschreibung"], "BILD": s["bild"], "BILDNR": s["bild_nr"],
        "REIHE": galerie(s["reihe"]), "WAHLBLOCK": wahlblock(s),
        "MASSE_TITEL": s["masse_titel"], "MASSE_LEIT": s["masse_leit"],
        "MASSE_KOPF": kopfteil, "MASSE_ZEILEN": zeilen,
        "MATERIAL": "\n          ".join(
            f"<li><b>{html.escape(b)}</b><span>{html.escape(w)}</span></li>"
            for b, w in s["material"]),
        "FRAGEN": "\n      ".join(
            f'<details class="klapp">\n        <summary>{html.escape(f)}</summary>\n'
            f'        <div class="klapp-inhalt"><p>{html.escape(a)}</p></div>\n      </details>'
            for f, a in s["fragen"]),
        "PRAXIS_H": s["praxis_h"], "PRAXIS_P": s["praxis_p"],
        "HUNDE": hunde, "TAGE": tage, "STAND": STAND,
        "LD_PRODUKT": json.dumps({
            "@context": "https://schema.org", "@type": "Product",
            "name": s["name"], "sku": s["sku"], "description": s["beschreibung"],
            "brand": {"@type": "Brand", "name": "Bellowerk"},
            "material": "Rindfettleder, pflanzlich gegerbt; Messing massiv",
            "countryOfOrigin": "DE",
            "offers": {"@type": "Offer", "priceCurrency": "EUR",
                       "price": s["preis_zahl"],
                       "availability": "https://schema.org/InStock"},
        }, ensure_ascii=False, indent=2),
        "LD_FRAGEN": json.dumps({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": f,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for f, a in s["fragen"]],
        }, ensure_ascii=False, indent=2),
    }

    seite = vorlage
    for marke, wert in werte.items():
        seite = seite.replace(f"§§{marke}§§", wert)

    uebrig = set(re.findall(r"§§[A-Z_]+§§", seite))
    if uebrig:
        raise SystemExit(f"FEHLER {s['datei']}: nicht ersetzt: {sorted(uebrig)}")
    return seite


def main():
    vorlage = (WEB / "vorlagen" / "produkt.html").read_text(encoding="utf-8")
    for s in STUECKE:
        (WEB / s["datei"]).write_text(bauen(s, vorlage), encoding="utf-8")
        print(f"  gebaut: {s['datei']:28} {s['name']} · {s['sku']} · {s['preis']} €")


if __name__ == "__main__":
    main()
