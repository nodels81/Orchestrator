"""
gegenpruefung.py — Die andere KI nimmt das Ergebnis ab.

Hat eine KI gearbeitet, liest die naechste im Ring Claude -> ChatGPT -> Kimi gegen. Zwei Modelle machen
selten denselben Fehler an derselben Stelle. Die Pruefung ist ein einzelner Aufruf
ohne Werkzeuge und kostet nur dann etwas, wenn das Ergebnis die eigene Pruefung
des Orchestrators schon bestanden hat.

Einschalten:  "gegenpruefung": true  in config.json
Sicherheit:   Faellt die zweite KI aus (kein Schluessel, Netz weg), wird das Ergebnis
              NICHT blockiert, sondern mit Hinweis durchgereicht. Die Gegenpruefung
              ist ein Zusatz, keine Schranke, die den Betrieb stillegt.
"""

import json

import ki_anbieter
import markenwissen

SYSTEM = (
    "Du bist unabhaengiger Pruefer im Betrieb {marke}. Eine andere KI hat einen Auftrag "
    "bearbeitet. Du sollst NICHT neu schreiben, sondern abnehmen oder ablehnen.\n\n"
    "Pruefe in dieser Reihenfolge:\n"
    "  1. Verstoss gegen die harten Ausschluesse oder die Werkstoffliste des Markenwissens\n"
    "  2. Erfundene Zahlen, Preise, Zusagen oder Lieferantendaten (nicht belegt = Einwand)\n"
    "  3. Jedes Abnahmekriterium wirklich erfuellt, nicht nur behauptet\n"
    "  4. Geld ausgegeben oder zugesagt, obwohl der Rahmen 'keine Ausgaben' lautet\n\n"
    "Kleinigkeiten in Stil oder Wortwahl sind KEIN Einwand. Lehne nur ab, was Bjoern "
    "Geld, Ruf oder Zeit kosten wuerde.\n\n"
    "MARKENWISSEN (bindend):\n{wissen}\n\n"
    "Antworte ausschliesslich mit JSON, ohne Vorwort und ohne Code-Fences:\n"
    '{{"freigabe": true|false, "einwaende": ["<konkret, mit Fundstelle>", ...]}}\n'
    "Bei freigabe=true ist einwaende leer."
)


def system_prompt() -> str:
    """Wortgleich bei jedem Aufruf, damit der Zwischenspeicher greift."""
    return SYSTEM.format(marke=markenwissen.MARKE, wissen=markenwissen.als_kontext())


def nutzer_text(auftrag: dict, ergebnis: dict) -> str:
    kriterien = "\n".join(f"  {i + 1}. {k}" for i, k in enumerate(auftrag.get("kriterien", [])))
    behauptet = ergebnis.get("kriterien_erfuellt", [])
    return (
        f"AUFTRAG {auftrag.get('id', '?')}\n"
        f"Ziel: {auftrag.get('ziel', '')}\n"
        f"Rahmen: {auftrag.get('rahmen', 'keine Ausgaben')}\n\n"
        f"ABNAHMEKRITERIEN:\n{kriterien}\n"
        f"Die bearbeitende KI behauptet erfuellt: {json.dumps(behauptet)}\n\n"
        f"ERGEBNIS DER BEARBEITENDEN KI:\n{ergebnis.get('ergebnis', '')[:12000]}\n\n"
        f"IHRE ANMERKUNG: {ergebnis.get('anmerkung') or '-'}"
    )


def lesen(text: str) -> dict:
    roh = text.strip()
    anfang, ende = roh.find("{"), roh.rfind("}")
    if anfang == -1 or ende == -1:
        raise ValueError("Pruefer-Antwort war kein JSON")
    daten = json.loads(roh[anfang:ende + 1])
    einwaende = [str(e) for e in (daten.get("einwaende") or []) if str(e).strip()]
    # Eine Ablehnung ohne Begruendung nuetzt der Nacharbeit nichts — dann zaehlt sie nicht.
    freigabe = bool(daten.get("freigabe")) or not einwaende
    return {"freigabe": freigabe, "einwaende": [] if freigabe else einwaende}


def pruefen(auftrag: dict, ergebnis: dict, config: dict, bearbeiter: str,
            pruefer=None) -> dict:
    """Liefert {'freigabe', 'einwaende', 'pruefer', 'verfuegbar'}.

    `bearbeiter` ist die KI, die das Ergebnis geschrieben hat; geprueft wird mit der anderen.
    `pruefer` erlaubt Tests, einen Anbieter ohne Netz einzusetzen.
    """
    name = ki_anbieter.gegenueber(bearbeiter, config)
    try:
        pruefer = pruefer or ki_anbieter.anbieter_bauen(config, name)
        text, _ = pruefer.antworten(system_prompt(), nutzer_text(auftrag, ergebnis),
                                    max_tokens=1500)
        urteil = lesen(text)
    except Exception as fehler:
        return {"freigabe": True, "einwaende": [], "pruefer": name, "verfuegbar": False,
                "hinweis": f"Gegenpruefung durch {name} nicht moeglich: {fehler}"}
    return {**urteil, "pruefer": name, "verfuegbar": True}


def begruendung(urteil: dict) -> str:
    return f"Gegenpruefung durch {urteil['pruefer']}: " + "; ".join(urteil["einwaende"])
