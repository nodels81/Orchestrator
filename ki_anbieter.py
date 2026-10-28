"""
ki_anbieter.py — Eine Schnittstelle, zwei KIs: Claude (Anthropic) und ChatGPT (OpenAI).

Die Abteilungen wissen nicht, wer antwortet. Sie rufen anbieter.antworten(system, nutzer)
und bekommen Text plus den echten Verbrauch zurueck. Welche KI sie bekommen, steht in
config.json:

  "anbieter": "claude"                          Standard fuer alle Abteilungen
  "anbieter_je_abteilung": {"05": "openai"}     Ausnahmen nach Abteilungsnummer
  "openai": {"api_key": "...", "modell": "gpt-5"}

OpenAI wird ueber die HTTP-Schnittstelle angesprochen (nur Standardbibliothek) —
kein zusaetzliches Paket auf dem Server.
"""

import json
import os
import urllib.error
import urllib.request

try:
    import anthropic
except ImportError:
    # Kein Abbruch: --probelauf und --stand muessen ohne das Paket laufen.
    anthropic = None

CLAUDE = "claude"
OPENAI = "openai"
BEKANNT = (CLAUDE, OPENAI)

STANDARD_MODELL = {CLAUDE: "claude-sonnet-5", OPENAI: "gpt-5"}
OPENAI_BASIS_URL = "https://api.openai.com/v1"

# Unterhalb dieser Laenge lohnt der Zwischenspeicher nicht: die API legt erst ab
# rund 1.000 Tokens etwas ab. Vier Zeichen sind grob ein Token.
MIN_CACHE_ZEICHEN = 5_000


class Anbieter:
    """Basis. Ableitungen setzen NAME und liefern (text, verbrauch) zurueck."""

    NAME = ""

    def __init__(self, modell: str):
        self.modell = modell

    def antworten(self, system: str, nutzer: str, recherche: bool = False,
                  max_tokens: int = 4000) -> tuple[str, dict]:
        raise NotImplementedError


def verbrauch_leer() -> dict:
    return {"ein": 0, "aus": 0, "cache_gelesen": 0, "cache_geschrieben": 0}


class ClaudeAnbieter(Anbieter):
    NAME = CLAUDE

    def __init__(self, modell: str, schluessel: str):
        super().__init__(modell)
        if anthropic is None:
            raise RuntimeError(
                "Paket 'anthropic' fehlt. Nachinstallieren mit: venv/bin/pip install anthropic"
            )
        self.client = anthropic.Anthropic(api_key=schluessel)

    def antworten(self, system, nutzer, recherche=False, max_tokens=4000):
        block: dict = {"type": "text", "text": system}
        if len(system) >= MIN_CACHE_ZEICHEN:
            block["cache_control"] = {"type": "ephemeral"}
        argumente = {
            "model": self.modell,
            "max_tokens": max_tokens,
            "system": [block],
            "messages": [{"role": "user", "content": nutzer}],
        }
        if recherche:
            argumente["tools"] = [{"type": "web_search_20250305", "name": "web_search"}]
        antwort = self.client.messages.create(**argumente)
        text = "".join(b.text for b in antwort.content if getattr(b, "type", "") == "text")
        return text, _claude_verbrauch(antwort)


class OpenAIAnbieter(Anbieter):
    NAME = OPENAI

    def __init__(self, modell: str, schluessel: str, basis_url: str = OPENAI_BASIS_URL,
                 zeitlimit: int = 180):
        super().__init__(modell)
        self.schluessel = schluessel
        self.basis_url = basis_url.rstrip("/")
        self.zeitlimit = zeitlimit

    def antworten(self, system, nutzer, recherche=False, max_tokens=4000):
        if recherche:
            # Die Websuche haengt an Claudes Werkzeug; ChatGPT antwortet hier aus Wissen.
            print("    [OpenAI] Websuche nicht angebunden — Antwort ohne Recherche.")
        # Gleichbleibender Anfang zuerst: OpenAI cached gleiche Praefixe automatisch.
        koerper = {
            "model": self.modell,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": nutzer},
            ],
            "response_format": {"type": "json_object"},
            "max_completion_tokens": max_tokens,
        }
        antwort = self._post("/chat/completions", koerper)
        try:
            text = antwort["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError) as fehler:
            raise RuntimeError(f"OpenAI-Antwort unlesbar ({fehler}): {str(antwort)[:300]}") from fehler
        return text, _openai_verbrauch(antwort.get("usage"))

    def _post(self, pfad: str, koerper: dict) -> dict:
        anfrage = urllib.request.Request(
            self.basis_url + pfad,
            data=json.dumps(koerper).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.schluessel}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(anfrage, timeout=self.zeitlimit) as antwort:
                return json.loads(antwort.read().decode("utf-8"))
        except urllib.error.HTTPError as fehler:
            detail = fehler.read().decode("utf-8", errors="replace")[:400]
            raise RuntimeError(f"OpenAI antwortet mit HTTP {fehler.code}: {detail}") from fehler
        except urllib.error.URLError as fehler:
            raise RuntimeError(f"OpenAI nicht erreichbar: {fehler.reason}") from fehler


def _claude_verbrauch(antwort) -> dict:
    nutzung = getattr(antwort, "usage", None)
    hole = lambda feld: int(getattr(nutzung, feld, 0) or 0) if nutzung else 0
    return {
        "ein": hole("input_tokens"),
        "aus": hole("output_tokens"),
        "cache_gelesen": hole("cache_read_input_tokens"),
        "cache_geschrieben": hole("cache_creation_input_tokens"),
    }


def _openai_verbrauch(nutzung: dict | None) -> dict:
    """OpenAI zaehlt Cache-Treffer innerhalb von prompt_tokens; Claude getrennt.
    Auf Claudes Schema gebracht, damit das Gedaechtnis beide gleich verbucht."""
    if not nutzung:
        return verbrauch_leer()
    gesamt = int(nutzung.get("prompt_tokens") or 0)
    details = nutzung.get("prompt_tokens_details") or {}
    gecached = int(details.get("cached_tokens") or 0)
    return {
        "ein": max(gesamt - gecached, 0),
        "aus": int(nutzung.get("completion_tokens") or 0),
        "cache_gelesen": gecached,
        "cache_geschrieben": 0,
    }


# ---------- Auswahl ----------

def anbieter_name(config: dict, nummer: str | None = None) -> str:
    """Welche KI bearbeitet Abteilung `nummer`? Ausnahme vor Standard vor Claude."""
    je_abteilung = config.get("anbieter_je_abteilung") or {}
    name = (je_abteilung.get(nummer) if nummer else None) or config.get("anbieter") or CLAUDE
    name = str(name).lower()
    if name not in BEKANNT:
        raise ValueError(f"Unbekannter Anbieter '{name}'. Bekannt: {', '.join(BEKANNT)}")
    return name


def gegenueber(name: str) -> str:
    """Die jeweils andere KI."""
    return OPENAI if name == CLAUDE else CLAUDE


def schluessel_vorhanden(config: dict, name: str) -> bool:
    return bool(_schluessel(config, name))


def _schluessel(config: dict, name: str) -> str | None:
    if name == CLAUDE:
        return config.get("anthropic_api_key") or os.environ.get("ANTHROPIC_API_KEY")
    block = config.get("openai") or {}
    return block.get("api_key") or os.environ.get("OPENAI_API_KEY")


def modell_name(config: dict, name: str) -> str:
    if name == CLAUDE:
        return config.get("modell") or STANDARD_MODELL[CLAUDE]
    return (config.get("openai") or {}).get("modell") or STANDARD_MODELL[OPENAI]


def anbieter_bauen(config: dict, name: str) -> Anbieter:
    schluessel = _schluessel(config, name)
    if not schluessel:
        quelle = "anthropic_api_key / ANTHROPIC_API_KEY" if name == CLAUDE \
            else "openai.api_key / OPENAI_API_KEY"
        raise ValueError(f"Kein Schluessel fuer {name}: {quelle} in config.json oder Umgebung setzen.")
    modell = modell_name(config, name)
    if name == CLAUDE:
        return ClaudeAnbieter(modell, schluessel)
    basis = (config.get("openai") or {}).get("basis_url") or OPENAI_BASIS_URL
    return OpenAIAnbieter(modell, schluessel, basis)


def anbieter_waehlen(config: dict, nummer: str | None = None) -> Anbieter:
    return anbieter_bauen(config, anbieter_name(config, nummer))
