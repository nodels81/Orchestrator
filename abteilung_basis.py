"""
abteilung_basis.py — Gemeinsame Mechanik. Muss nie angefasst werden.

Jede Abteilung erbt von Abteilung und liefert dieselbe Status-Struktur zurueck,
damit der Orchestrator maschinell pruefen kann statt zu interpretieren.
"""

import json
import os
import re
import sys

try:
    import anthropic
except ImportError:
    print("FEHLER: Paket 'anthropic' fehlt. Mit venv/bin/pip install anthropic nachinstallieren.")
    sys.exit(1)

import markenwissen

BASIS = os.path.dirname(os.path.abspath(__file__))
DATEN = os.path.join(BASIS, "daten")
os.makedirs(DATEN, exist_ok=True)
CONFIG_PFAD = os.path.join(BASIS, "config.json")
STANDARD_MODELL = "claude-sonnet-5"


def _env_aufloesen(wert):
    """Ersetzt "${VAR}" rekursiv durch os.environ["VAR"]. Fehlt die
    Variable, bleibt der Platzhalter stehen; der Aufrufer meldet das dann."""
    if isinstance(wert, dict):
        return {k: _env_aufloesen(v) for k, v in wert.items()}
    if isinstance(wert, list):
        return [_env_aufloesen(v) for v in wert]
    if isinstance(wert, str):
        t = re.fullmatch(r"\$\{([A-Z0-9_]+)\}", wert.strip())
        if t:
            return os.environ.get(t.group(1), wert)
    return wert


def config_laden() -> dict:
    if not os.path.exists(CONFIG_PFAD):
        raise FileNotFoundError(
            f"{CONFIG_PFAD} fehlt. Vorlage: config.beispiel.json kopieren und ausfuellen."
        )
    with open(CONFIG_PFAD, encoding="utf-8") as f:
        return _env_aufloesen(json.load(f))


class Abteilung:
    """Basisklasse. Ableitungen setzen NUMMER, NAME, ROLLE."""

    NUMMER = "00"
    NAME = "Basis"
    ROLLE = "Keine Rolle definiert."
    MAX_TOKENS = 4000  # Ableitungen duerfen hochsetzen (z. B. lange Entwuerfe)

    def __init__(self, config: dict | None = None):
        self.config = config or config_laden()
        schluessel = self.config.get("anthropic_api_key") or os.environ.get("ANTHROPIC_API_KEY")
        if not schluessel:
            raise ValueError("Kein API-Schluessel in config.json oder ANTHROPIC_API_KEY.")
        # gebremst: hoechstens 2 Wiederholungen, hartes Zeitlimit pro Aufruf
        self.client = anthropic.Anthropic(
            api_key=schluessel, max_retries=2, timeout=900.0
        )
        self.modell = self.config.get("modell", STANDARD_MODELL)

    # ---------- Prompt ----------

    def system_prompt(self) -> str:
        return (
            f"Du bist Abteilung {self.NUMMER} ({self.NAME}) im Betrieb "
            f"{markenwissen.MARKE}.\n\n"
            f"DEINE ROLLE:\n{self.ROLLE}\n\n"
            f"MARKENWISSEN (bindend):\n{markenwissen.als_kontext()}\n\n"
            "REGELN:\n"
            "- Du gibst NUR gueltiges JSON zurueck, kein Vorwort, keine Code-Fences.\n"
            "- Du gibst niemals Geld aus und sagst keine Preise nach aussen zu.\n"
            "- Was du nicht sicher weisst, kennzeichnest du als Schaetzung.\n"
            "- Verstoesst etwas gegen die harten Ausschluesse, lehnst du es ab "
            "und begruendest das im Feld 'anmerkung'.\n"
        )

    def antwortformat(self) -> str:
        return (
            "Antworte ausschliesslich mit diesem JSON-Objekt:\n"
            "{\n"
            '  "ergebnis": "<deine Arbeit, ausformuliert>",\n'
            '  "kriterien_erfuellt": [true, false, ...],\n'
            '  "blocker": null,\n'
            '  "anmerkung": "<Einschraenkungen oder Hinweise, sonst null>"\n'
            "}\n"
            "Die Liste kriterien_erfuellt hat genau so viele Eintraege wie Kriterien "
            "im Auftrag, in derselben Reihenfolge."
        )

    # ---------- Ausfuehrung ----------

    def bearbeiten(self, auftrag: dict, recherche: bool = False) -> dict:
        kriterien = auftrag.get("kriterien", [])
        nutzer = (
            f"AUFTRAG {auftrag.get('id', '?')}\n"
            f"Ziel: {auftrag.get('ziel', '')}\n"
            f"Rahmen: {auftrag.get('rahmen', 'keine Ausgaben')}\n"
            f"Frist: {auftrag.get('frist', 'offen')}\n\n"
            "ABNAHMEKRITERIEN:\n"
            + "\n".join(f"  {i+1}. {k}" for i, k in enumerate(kriterien))
            + "\n\n" + self.antwortformat()
        )

        argumente = {
            "model": self.modell,
            "max_tokens": self.MAX_TOKENS,
            "system": self.system_prompt(),
            "messages": [{"role": "user", "content": nutzer}],
        }
        if recherche:
            argumente["tools"] = [{"type": "web_search_20250305", "name": "web_search"}]

        if self.MAX_TOKENS > 8000:
            # lange Antworten (Zeichnungen, Stellenbeschreibungen): streamen, sonst Timeout
            with self.client.messages.stream(**argumente) as strom:
                antwort = strom.get_final_message()
        else:
            antwort = self.client.messages.create(**argumente)
        if getattr(antwort, "stop_reason", "") == "max_tokens":
            print(f"    [API] Antwort am Tokenlimit ({self.MAX_TOKENS}) abgeschnitten.")
        text = "".join(b.text for b in antwort.content if getattr(b, "type", "") == "text")
        return self._json_lesen(text, len(kriterien))

    def _json_lesen(self, text: str, anzahl_kriterien: int) -> dict:
        roh = text.strip()
        if roh.startswith("```"):
            roh = roh.split("```")[1]
            if roh.startswith("json"):
                roh = roh[4:]
            roh = roh.strip()
        try:
            daten = json.loads(roh)
        except json.JSONDecodeError:
            anfang, ende = roh.find("{"), roh.rfind("}")
            if anfang == -1 or ende == -1:
                return {
                    "ergebnis": text[:2000],
                    "kriterien_erfuellt": [False] * anzahl_kriterien,
                    "blocker": "Antwort war kein JSON",
                    "anmerkung": "Modellantwort konnte nicht gelesen werden.",
                }
            daten = json.loads(roh[anfang:ende + 1])

        erfuellt = daten.get("kriterien_erfuellt") or []
        if len(erfuellt) < anzahl_kriterien:
            erfuellt += [False] * (anzahl_kriterien - len(erfuellt))
        daten["kriterien_erfuellt"] = erfuellt[:anzahl_kriterien]
        daten.setdefault("ergebnis", "")
        daten.setdefault("blocker", None)
        daten.setdefault("anmerkung", None)
        return daten


def einzeltest(klasse) -> None:
    """Erlaubt: venv/bin/python abteilung_xyz.py "Ziel ..." [--recherche]"""
    argumente = [a for a in sys.argv[1:] if a != "--recherche"]
    if not argumente:
        print(f'Aufruf: python {sys.argv[0]} "Ziel des Auftrags" [--recherche]')
        return
    auftrag = {
        "id": "TEST-001",
        "abteilung": f"{klasse.NUMMER} {klasse.NAME}",
        "ziel": argumente[0],
        "kriterien": ["Ergebnis ist konkret", "Passt zur Marke", "Keine Ausgaben noetig"],
        "frist": "offen",
        "rahmen": "keine Ausgaben",
    }
    ergebnis = klasse().bearbeiten(auftrag, recherche="--recherche" in sys.argv)
    print(json.dumps(ergebnis, indent=2, ensure_ascii=False))
