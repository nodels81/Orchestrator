"""test_sparmassnahmen.py — sichert die vier Sparmassnahmen gegen Rueckfall.

Laeuft ohne API-Schluessel und ohne Kosten: der Client wird durch eine Attrappe
ersetzt, die den Aufruf nur festhaelt. Aufruf:

    .venv/bin/python -m unittest test_sparmassnahmen -v
"""

import contextlib
import io
import json
import os
import sys
import tempfile
import types
import unittest

# Die Basis bricht ohne das Paket 'anthropic' ab; fuer den Test genuegt eine Huelle.
sys.modules.setdefault("anthropic", types.ModuleType("anthropic"))
sys.modules["anthropic"].Anthropic = lambda **kw: None

import abteilung_basis as ab
import abteilung_einkauf_china as ch
import orchestrator
from abteilung_ausfuehrung import Ausfuehrung
from abteilung_einkauf_china import EinkaufChina
from abteilung_vertrieb import Vertrieb


class Block:
    type = "text"

    def __init__(self, text):
        self.text = text


class FakeAntwort:
    def __init__(self, text, stop_reason="end_turn"):
        self.content = [Block(text)]
        self.stop_reason = stop_reason
        self.usage = types.SimpleNamespace(
            input_tokens=10, output_tokens=20,
            cache_read_input_tokens=0, cache_creation_input_tokens=0,
        )


class FakeClient:
    """Haelt die Aufrufargumente fest, statt die API zu rufen."""

    def __init__(self, antwort):
        self.antwort = antwort
        self.gesehen = None

    @property
    def messages(self):
        return self

    def create(self, **kw):
        self.gesehen = kw
        return self.antwort


GUT = json.dumps({
    "ergebnis": "Dear Sir", "kriterien_erfuellt": [True, True], "blocker": None,
    "anmerkung": None, "zusammenfassung": "x", "fakten": [],
})
AUFTRAG = {"id": "T-1", "ziel": "RFQ fuer HB-01", "kriterien": ["k1", "k2"],
           "frist": "2030-01-01", "rahmen": "keine Ausgaben"}


def bau(klasse, antwort):
    """Abteilung ohne __init__ — kein Schluessel, kein Gedaechtnis, kein Netz."""
    a = object.__new__(klasse)
    a.config = {}
    a.client = FakeClient(antwort)
    a.modell = "claude-sonnet-5"
    a.gedaechtnis_an = False
    a.denktiefe = klasse.DENKTIEFE
    a.cache_lohnt = False
    return a


class KurzeAusgabe(unittest.TestCase):
    def test_wortgrenze_steht_im_prompt(self):
        text = ab.Abteilung.antwortformat(bau(EinkaufChina, FakeAntwort(GUT)))
        self.assertIn(f"hoechstens {EinkaufChina.MAX_WOERTER} Woerter", text)

    def test_keine_wortgrenze_wo_das_ergebnis_lang_sein_soll(self):
        self.assertIsNone(Ausfuehrung.MAX_WOERTER)
        self.assertNotIn("LAENGE", ab.Abteilung.antwortformat(bau(Ausfuehrung, FakeAntwort(GUT))))

    def test_denktiefe_und_dach_gehen_an_die_api(self):
        a = bau(Vertrieb, FakeAntwort(GUT))
        a.bearbeiten(AUFTRAG)
        self.assertEqual(a.client.gesehen["output_config"], {"effort": "low"})
        self.assertEqual(a.client.gesehen["max_tokens"], Vertrieb.MAX_TOKENS)

    def test_abwaegende_abteilung_denkt_tiefer(self):
        a = bau(EinkaufChina, FakeAntwort(GUT))
        a.bearbeiten(AUFTRAG)
        self.assertEqual(a.client.gesehen["output_config"], {"effort": "medium"})

    def test_abgeschnittene_antwort_wird_blocker(self):
        a = bau(EinkaufChina, FakeAntwort('{"ergebnis": "Dear Si', stop_reason="max_tokens"))
        ergebnis = a.bearbeiten(AUFTRAG)
        self.assertIn("abgeschnitten", ergebnis["blocker"])
        self.assertEqual(ergebnis["kriterien_erfuellt"], [False, False])


class Zwischenspeicher(unittest.TestCase):
    def test_kein_vermerk_bei_einzelnem_aufruf(self):
        a = bau(EinkaufChina, FakeAntwort(GUT))
        a.bearbeiten(AUFTRAG)
        self.assertNotIn("cache_control", a.client.gesehen["system"][0])

    def test_vermerk_wenn_die_abteilung_mehrfach_laeuft(self):
        a = bau(EinkaufChina, FakeAntwort(GUT))
        a.cache_lohnt = True
        a.bearbeiten(AUFTRAG)
        self.assertEqual(a.client.gesehen["system"][0].get("cache_control"),
                         {"type": "ephemeral"})

    def test_system_prompt_bleibt_zwischen_auftraegen_gleich(self):
        a = object.__new__(EinkaufChina)
        self.assertEqual(EinkaufChina.system_prompt(a), EinkaufChina.system_prompt(a))


class TechPackAuswahl(unittest.TestCase):
    def test_nur_die_genannten_specs(self):
        self.assertEqual(ch.specs_fuer("RFQ fuer HB-01 an Wenzhou"), ["HB-01", "PATCH-01"])
        self.assertEqual(ch.specs_fuer("Muster HB-02 und HS-01 pruefen"),
                         ["HB-02", "HS-01", "PATCH-01"])

    def test_kleinschreibung_wird_erkannt(self):
        self.assertEqual(ch.specs_fuer("anfrage zu hb-02"), ["HB-02", "PATCH-01"])

    def test_ohne_kuerzel_der_bisherige_umfang(self):
        self.assertEqual(ch.specs_fuer("Nachfassen beim Lieferanten"),
                         ["HB-01", "LE-01", "PATCH-01"])

    def test_unbekanntes_kuerzel_faellt_zurueck(self):
        self.assertEqual(ch.specs_fuer("RFQ fuer XY-99"), ["HB-01", "LE-01", "PATCH-01"])

    def test_tech_packs_stehen_nicht_im_system_prompt(self):
        a = object.__new__(EinkaufChina)
        self.assertNotIn("HB-01-halsband", EinkaufChina.system_prompt(a))
        self.assertIn("HB-01-halsband", EinkaufChina.auftrag_kontext(a, {"ziel": "RFQ HB-01"}))

    def test_andere_abteilungen_haben_keinen_auftragskontext(self):
        self.assertEqual(ab.Abteilung.auftrag_kontext(bau(Vertrieb, FakeAntwort(GUT)),
                                                      {"ziel": "HB-01"}), "")


class LaufLogik(unittest.TestCase):
    """Der Lauf baut jede Abteilung einmal und vermerkt den Zwischenspeicher nur,
    wo sie mehrfach drankommt — die Zwischenpruefung eingerechnet."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.echt = {
            "ZUSTAND": orchestrator.ZUSTAND, "senden": orchestrator.senden,
            "config_laden": orchestrator.config_laden,
            "abteilung_laden": orchestrator.abteilung_laden,
            "_wochenbericht_faellig": orchestrator._wochenbericht_faellig,
            "_fristen_pruefen": orchestrator._fristen_pruefen,
        }
        orchestrator.ZUSTAND = os.path.join(self.tmp, "auftraege.json")
        orchestrator.senden = lambda *a, **k: None
        orchestrator._wochenbericht_faellig = lambda *a, **k: None
        orchestrator._fristen_pruefen = lambda *a, **k: None
        self.config = {"mail": {}, "qm_gate": []}
        orchestrator.config_laden = lambda: self.config
        self.gebaut = []
        pruefer = self

        class Fake:
            def __init__(self, name):
                self.name = name
                self.cache_lohnt = False
                self.aufrufe = 0
                pruefer.gebaut.append(name)

            def bearbeiten(self, auftrag, recherche=False):
                self.aufrufe += 1
                return {"ergebnis": "x", "blocker": None, "anmerkung": None,
                        "zusammenfassung": "x", "fakten": [],
                        "kriterien_erfuellt": [True] * len(auftrag["kriterien"])}

        orchestrator.abteilung_laden = Fake

    def tearDown(self):
        for name, wert in self.echt.items():
            setattr(orchestrator, name, wert)

    def lauf_mit(self, auftraege, qm_gate=()):
        self.gebaut.clear()
        self.config["qm_gate"] = list(qm_gate)
        with open(orchestrator.ZUSTAND, "w", encoding="utf-8") as f:
            json.dump({"auftraege": auftraege, "letzter_lauf": None,
                       "letzter_wochenbericht": None}, f)
        with contextlib.redirect_stdout(io.StringIO()):   # Laufmeldungen stoeren hier
            orchestrator.lauf()
        return dict(orchestrator._INSTANZEN)

    @staticmethod
    def auftrag(nr, abteilung):
        return {"id": f"A-2026-{nr:03d}", "abteilung": abteilung, "ziel": "z",
                "kriterien": ["k"], "frist": "2030-01-01", "rahmen": "keine Ausgaben",
                "stand": "offen", "versuche": 0, "eskaliert": False, "verlauf": [],
                "angelegt": "2026-01-01T00:00:00"}

    def test_einzelne_auftraege_ohne_vermerk(self):
        inst = self.lauf_mit([self.auftrag(1, "01 Innovation"),
                              self.auftrag(2, "07 Einkauf China")])
        self.assertFalse(any(a.cache_lohnt for a in inst.values()))

    def test_mehrere_auftraege_teilen_eine_instanz(self):
        inst = self.lauf_mit([self.auftrag(3, "07 Einkauf China"),
                              self.auftrag(4, "07 Einkauf China"),
                              self.auftrag(5, "07 Einkauf China"),
                              self.auftrag(6, "01 Innovation")])
        self.assertEqual(self.gebaut.count("07 Einkauf China"), 1)
        self.assertTrue(inst["07 Einkauf China"].cache_lohnt)
        self.assertEqual(inst["07 Einkauf China"].aufrufe, 3)
        self.assertFalse(inst["01 Innovation"].cache_lohnt)

    def test_zwischenpruefung_zaehlt_mit(self):
        inst = self.lauf_mit([self.auftrag(7, "01 Innovation"),
                              self.auftrag(8, "03 Vertrieb")],
                             qm_gate=["01 Innovation", "03 Vertrieb"])
        self.assertEqual(self.gebaut.count("09 Qualität"), 1)
        self.assertTrue(inst["09 Qualität"].cache_lohnt)
        self.assertEqual(inst["09 Qualität"].aufrufe, 2)


if __name__ == "__main__":
    unittest.main()
