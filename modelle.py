"""
modelle.py — Welche KI bearbeitet welchen Auftrag.

Jede Abteilung bekommt das Modell, das fuer ihre Arbeit am besten passt. Die Zuordnung
steht in config.json unter "modelle" und laesst sich ohne Code-Aenderung umstellen:

  "modelle": {
    "standard":  "anthropic:claude-sonnet-5",
    "ausweichen": "anthropic:claude-sonnet-5",
    "zuordnung": {
      "01 Innovation":            "kimi:kimi-k2-0905-preview",
      "02 Produkt & Ausführung":  "openai:gpt-5",
      "05 Einkauf China":         "anthropic:claude-sonnet-5"
    },
    "anbieter": {
      "anthropic": {"api_key": "sk-ant-..."},
      "openai":    {"api_key": "sk-..."},
      "kimi":      {"api_key": "sk-...", "basis_url": "https://api.moonshot.ai/v1"},
      "lokal":     {"basis_url": "http://127.0.0.1:11434/v1", "json_modus": false}
    }
  }

Eine Kennung ist immer "anbieter:modell". Alles ausser Anthropic spricht die
OpenAI-kompatible Chat-Schnittstelle (OpenAI, Moonshot/Kimi, Ollama, OpenRouter, vLLM ...)
und braucht kein zusaetzliches Paket — nur die Standardbibliothek.

Fehlt der Block "modelle" ganz, verhaelt sich alles wie bisher: Anthropic mit
"anthropic_api_key" und "modell" aus config.json.

Schluessel koennen statt in config.json auch in der Umgebung liegen: "api_key_env"
nennt die Variable (Standard: ANTHROPIC_API_KEY, OPENAI_API_KEY, MOONSHOT_API_KEY).
"""

import json
import os
import urllib.error
import urllib.request

try:
    import anthropic
except ImportError:
    anthropic = None

STANDARD_KENNUNG = "anthropic:claude-sonnet-5"
ZEITLIMIT_SEKUNDEN = 300

# Unterhalb dieser Laenge lohnt der Anthropic-Zwischenspeicher nicht.
MIN_CACHE_ZEICHEN = 5_000

VOREINSTELLUNG = {
    "anthropic": {"api_key_env": "ANTHROPIC_API_KEY"},
    "openai": {"basis_url": "https://api.openai.com/v1", "api_key_env": "OPENAI_API_KEY",
               "json_modus": True},
    "kimi": {"basis_url": "https://api.moonshot.ai/v1", "api_key_env": "MOONSHOT_API_KEY",
             "json_modus": True},
    "lokal": {"basis_url": "http://127.0.0.1:11434/v1", "json_modus": False},
}


class ModellFehler(RuntimeError):
    """Ein Anbieter hat nicht geantwortet oder ist nicht eingerichtet."""


# ---------- Konfiguration ----------

def kennung_zerlegen(kennung: str) -> tuple[str, str]:
    """'kimi:kimi-k2' -> ('kimi', 'kimi-k2'). Ohne Anbieter gilt Anthropic."""
    kennung = (kennung or "").strip()
    if ":" not in kennung:
        return "anthropic", kennung or STANDARD_KENNUNG.split(":", 1)[1]
    anbieter, modell = kennung.split(":", 1)
    return anbieter.strip().lower(), modell.strip()


def einstellungen(config: dict) -> dict:
    """Bringt alte und neue config.json auf dieselbe Form."""
    block = dict(config.get("modelle") or {})
    anbieter = {name: dict(werte) for name, werte in (block.get("anbieter") or {}).items()}

    # Alte Felder bleiben gueltig: anthropic_api_key und modell auf oberster Ebene.
    anthropic_alt = anbieter.setdefault("anthropic", {})
    if config.get("anthropic_api_key") and not anthropic_alt.get("api_key"):
        anthropic_alt["api_key"] = config["anthropic_api_key"]

    standard = block.get("standard") or config.get("modell") or STANDARD_KENNUNG
    if ":" not in standard:
        standard = f"anthropic:{standard}"

    return {
        "standard": standard,
        "ausweichen": block.get("ausweichen") or standard,
        "zuordnung": dict(block.get("zuordnung") or {}),
        "anbieter": anbieter,
    }


def reihenfolge(config: dict, abteilung: str | None, auftrag: dict | None = None) -> list[str]:
    """Welche Kennungen fuer diesen Auftrag versucht werden, in dieser Reihenfolge."""
    e = einstellungen(config)
    erste = ((auftrag or {}).get("modell")
             or e["zuordnung"].get(abteilung or "")
             or e["standard"])
    folge = [erste]
    if e["ausweichen"] != erste:
        folge.append(e["ausweichen"])
    return folge


def schluessel_fuer(name: str, config: dict) -> str | None:
    e = einstellungen(config)
    werte = {**VOREINSTELLUNG.get(name, {}), **e["anbieter"].get(name, {})}
    if werte.get("api_key"):
        return werte["api_key"]
    variable = werte.get("api_key_env")
    return os.environ.get(variable) if variable else None


def uebersicht(config: dict, abteilungen: list[str]) -> str:
    """Fuer 'orchestrator.py --modelle': wer arbeitet womit, ohne Schluessel zu zeigen."""
    e = einstellungen(config)
    zeilen = ["Modell-Zuordnung", ""]
    for abteilung in abteilungen:
        folge = reihenfolge(config, abteilung)
        zusatz = f"  (Ausweich: {folge[1]})" if len(folge) > 1 else ""
        zeilen.append(f"  {abteilung:<24} {folge[0]}{zusatz}")
    zeilen += ["", "Anbieter"]
    namen = sorted(set(VOREINSTELLUNG) | set(e["anbieter"]))
    for name in namen:
        werte = {**VOREINSTELLUNG.get(name, {}), **e["anbieter"].get(name, {})}
        if name == "anthropic":
            ziel = "Anthropic SDK"
        else:
            ziel = werte.get("basis_url", "?")
        hat = "Schluessel vorhanden" if schluessel_fuer(name, config) else "kein Schluessel"
        if name == "lokal" and not schluessel_fuer(name, config):
            hat = "ohne Schluessel (lokal)"
        zeilen.append(f"  {name:<10} {ziel:<40} {hat}")
    return "\n".join(zeilen)


# ---------- Anbieter ----------

class Anbieter:
    name = "basis"

    def __init__(self, werte: dict, config: dict):
        self.werte = werte
        self.config = config

    def anfragen(self, modell: str, system: str, nutzer: str,
                 max_tokens: int, recherche: bool = False) -> tuple[str, dict]:
        """Liefert (Antworttext, Verbrauch). Verbrauch: ein, aus, cache_gelesen, cache_geschrieben."""
        raise NotImplementedError


class Anthropic(Anbieter):
    name = "anthropic"

    def __init__(self, werte: dict, config: dict):
        super().__init__(werte, config)
        if anthropic is None:
            raise ModellFehler("Paket 'anthropic' fehlt. Nachinstallieren mit: "
                               "venv/bin/pip install anthropic")
        schluessel = schluessel_fuer("anthropic", config)
        if not schluessel:
            raise ModellFehler("Kein Anthropic-Schluessel in config.json oder ANTHROPIC_API_KEY.")
        self.client = anthropic.Anthropic(api_key=schluessel)

    def anfragen(self, modell, system, nutzer, max_tokens, recherche=False):
        block: dict = {"type": "text", "text": system}
        if len(system) >= MIN_CACHE_ZEICHEN:
            block["cache_control"] = {"type": "ephemeral"}
        argumente = {
            "model": modell,
            "max_tokens": max_tokens,
            "system": [block],
            "messages": [{"role": "user", "content": nutzer}],
        }
        if recherche:
            argumente["tools"] = [{"type": "web_search_20250305", "name": "web_search"}]
        try:
            antwort = self.client.messages.create(**argumente)
        except Exception as fehler:
            raise ModellFehler(f"anthropic:{modell}: {fehler}") from fehler
        text = "".join(b.text for b in antwort.content if getattr(b, "type", "") == "text")
        nutzung = getattr(antwort, "usage", None)
        hole = lambda feld: int(getattr(nutzung, feld, 0) or 0) if nutzung else 0
        return text, {
            "ein": hole("input_tokens"),
            "aus": hole("output_tokens"),
            "cache_gelesen": hole("cache_read_input_tokens"),
            "cache_geschrieben": hole("cache_creation_input_tokens"),
        }


class OpenAIKompatibel(Anbieter):
    """OpenAI, Moonshot/Kimi, Ollama, OpenRouter, vLLM — alle sprechen /chat/completions."""

    def __init__(self, name: str, werte: dict, config: dict):
        super().__init__(werte, config)
        self.name = name
        self.basis_url = (werte.get("basis_url") or "").rstrip("/")
        if not self.basis_url:
            raise ModellFehler(f"Anbieter '{name}': basis_url fehlt in config.json.")
        self.schluessel = schluessel_fuer(name, config)
        if not self.schluessel and name != "lokal" and not self.basis_url.startswith("http://"):
            raise ModellFehler(f"Anbieter '{name}': kein Schluessel in config.json "
                               f"oder {werte.get('api_key_env', 'Umgebung')}.")
        self.json_modus = bool(werte.get("json_modus", False))

    def anfragen(self, modell, system, nutzer, max_tokens, recherche=False):
        if recherche:
            print(f"    [{self.name}] Web-Recherche gibt es nur bei Anthropic — laeuft ohne.")
        koerper: dict = {
            "model": modell,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": nutzer},
            ],
            "max_tokens": max_tokens,
        }
        if self.json_modus:
            koerper["response_format"] = {"type": "json_object"}
        daten = self._senden(koerper)
        try:
            text = daten["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError) as fehler:
            raise ModellFehler(f"{self.name}:{modell}: unerwartete Antwort {str(daten)[:300]}") from fehler
        nutzung = daten.get("usage") or {}
        details = nutzung.get("prompt_tokens_details") or {}
        return text, {
            "ein": int(nutzung.get("prompt_tokens") or 0),
            "aus": int(nutzung.get("completion_tokens") or 0),
            "cache_gelesen": int(details.get("cached_tokens") or 0),
            "cache_geschrieben": 0,
        }

    def _senden(self, koerper: dict) -> dict:
        kopf = {"Content-Type": "application/json"}
        if self.schluessel:
            kopf["Authorization"] = f"Bearer {self.schluessel}"
        anfrage = urllib.request.Request(
            f"{self.basis_url}/chat/completions",
            data=json.dumps(koerper).encode("utf-8"),
            headers=kopf,
            method="POST",
        )
        try:
            with urllib.request.urlopen(anfrage, timeout=ZEITLIMIT_SEKUNDEN) as antwort:
                return json.loads(antwort.read().decode("utf-8"))
        except urllib.error.HTTPError as fehler:
            inhalt = fehler.read().decode("utf-8", "replace")[:300]
            raise ModellFehler(f"{self.name}: HTTP {fehler.code} — {inhalt}") from fehler
        except (urllib.error.URLError, TimeoutError, OSError) as fehler:
            raise ModellFehler(f"{self.name}: nicht erreichbar ({fehler})") from fehler


def anbieter_bauen(name: str, config: dict) -> Anbieter:
    e = einstellungen(config)
    werte = {**VOREINSTELLUNG.get(name, {}), **e["anbieter"].get(name, {})}
    if name == "anthropic":
        return Anthropic(werte, config)
    return OpenAIKompatibel(name, werte, config)


# ---------- Auswahl ----------

class Auswahl:
    """Versucht die Kennungen der Reihe nach; die erste, die antwortet, gewinnt."""

    def __init__(self, config: dict, abteilung: str | None, auftrag: dict | None = None):
        self.config = config
        self.kennungen = reihenfolge(config, abteilung, auftrag)
        self._anbieter: dict[str, Anbieter] = {}

    @property
    def kennung(self) -> str:
        return self.kennungen[0]

    def anfragen(self, system: str, nutzer: str, max_tokens: int,
                 recherche: bool = False) -> tuple[str, dict, str]:
        """Liefert (Text, Verbrauch, benutzte Kennung)."""
        letzter: Exception | None = None
        for kennung in self.kennungen:
            name, modell = kennung_zerlegen(kennung)
            try:
                anbieter = self._anbieter.get(name) or anbieter_bauen(name, self.config)
                self._anbieter[name] = anbieter
                text, verbrauch = anbieter.anfragen(modell, system, nutzer, max_tokens, recherche)
                return text, verbrauch, kennung
            except ModellFehler as fehler:
                letzter = fehler
                if kennung != self.kennungen[-1]:
                    print(f"    [Modell] {kennung} ausgefallen ({fehler}) — weiche aus.")
        raise ModellFehler(f"Kein Modell hat geantwortet. Letzter Fehler: {letzter}")
