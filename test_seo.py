"""
test_seo.py — Prueft Abteilung 06 SEO ohne API-Schluessel und ohne Kosten.

Aufruf auf dem Server:  venv/bin/python -m unittest test_seo -v
Oder ohne venv:         python3 -m unittest test_seo -v

Getestet wird, was schiefgehen kann, ohne dass es auffaellt: fehlende Unterlagen, ein
verlorener Prompt-Cache, eine Abteilung, die der Orchestrator nicht laden kann, und
Agenten mit kaputtem Kopf.
"""

import os
import re
import unittest

import abteilung_basis
import abteilung_seo
import orchestrator
from abteilung_seo import Seo, seo_kontext

BASIS = abteilung_basis.BASIS


def ohne_config(klasse):
    """Eine Abteilung ohne __init__ — system_prompt braucht weder Schluessel noch Netz."""
    return object.__new__(klasse)


class UnterlagenTest(unittest.TestCase):
    """Die Dateien, ohne die die Abteilung raten wuerde."""

    def test_alle_kontextdateien_vorhanden(self):
        for rel in abteilung_seo.KONTEXT_DATEIEN:
            with self.subTest(rel):
                self.assertTrue(os.path.exists(os.path.join(abteilung_seo.SEO, rel)),
                                f"seo/{rel} fehlt")

    def test_vorlagen_vorhanden(self):
        erwartet = ["01-produkttext.md", "02-ratgeber-brief.md", "03-meta-und-schema.md",
                    "04-google-unternehmensprofil.md", "05-kanaltexte.md"]
        vorhanden = sorted(os.listdir(os.path.join(BASIS, "seo", "vorlagen")))
        self.assertEqual(sorted(erwartet), vorhanden)

    def test_skill_und_referenzen_vorhanden(self):
        skill = os.path.join(BASIS, ".claude", "skills", "seo")
        self.assertTrue(os.path.exists(os.path.join(skill, "SKILL.md")))
        for name in ["keyword-und-struktur.md", "onpage-und-schema.md",
                     "local-hamburg.md", "ki-sichtbarkeit-geo.md"]:
            with self.subTest(name):
                self.assertTrue(os.path.exists(os.path.join(skill, "references", name)))

    def test_kontext_enthaelt_alle_dateien_und_bleibt_im_rahmen(self):
        kontext = seo_kontext()
        self.assertEqual(kontext.count("### bellowerk/"), len(abteilung_seo.KONTEXT_DATEIEN))
        self.assertLessEqual(len(kontext), abteilung_seo.MAX_KONTEXT_ZEICHEN)

    def test_kontext_reihenfolge_ist_stabil(self):
        """Wechselt die Reihenfolge, ist der Prompt-Cache jedes Mal verloren."""
        self.assertEqual(seo_kontext(), seo_kontext())


class AbteilungTest(unittest.TestCase):

    def setUp(self):
        self.seo = ohne_config(Seo)

    def test_nummer_und_name(self):
        self.assertEqual("06", Seo.NUMMER)
        self.assertEqual("SEO", Seo.NAME)

    def test_system_prompt_enthaelt_markenwissen_und_seo_unterlagen(self):
        prompt = self.seo.system_prompt()
        self.assertIn("Bellowerk", prompt)
        self.assertIn("HARTE AUSSCHLUESSE", prompt)          # aus markenwissen.py
        self.assertIn("SEO-UNTERLAGEN (bindend)", prompt)
        self.assertIn("bellowerk/keywords.md", prompt)

    def test_prompt_ist_lang_genug_fuer_den_zwischenspeicher(self):
        bloecke = self.seo._system_bloecke()
        self.assertEqual(1, len(bloecke))
        self.assertIn("cache_control", bloecke[0],
                      "System-Prompt unter der Cache-Grenze — jeder Auftrag zahlt voll")

    def test_harte_regeln_stehen_in_der_rolle(self):
        """Die Regeln, deren Verletzung teuer wird: erfundene Bewertungen und Sterne-Schema."""
        for begriff in ["erfindest NICHTS", "aggregateRating", "llms.txt",
                        "Tech Packs", "veroeffentlichst nichts"]:
            with self.subTest(begriff):
                self.assertIn(begriff, Seo.ROLLE)

    def test_antwortformat_verlangt_fakten_fuers_gedaechtnis(self):
        self.assertIn('"fakten"', self.seo.antwortformat())

    def test_ohne_unterlagen_faellt_die_abteilung_nicht_aus(self):
        """Fehlt der Ordner seo/, laeuft der Auftrag mit Markenwissen weiter statt zu scheitern."""
        echt = abteilung_seo.SEO
        abteilung_seo.SEO = os.path.join(BASIS, "gibt-es-nicht")
        try:
            self.assertEqual("", seo_kontext())
            prompt = ohne_config(Seo).system_prompt()
            self.assertIn("Bellowerk", prompt)
            self.assertNotIn("SEO-UNTERLAGEN", prompt)
        finally:
            abteilung_seo.SEO = echt


class OrchestratorTest(unittest.TestCase):

    def test_abteilung_ist_registriert(self):
        self.assertIn("06 SEO", orchestrator.ABTEILUNGEN)

    def test_modul_und_klasse_sind_ladbar(self):
        modul_name, klassen_name = orchestrator.ABTEILUNGEN["06 SEO"]
        modul = __import__(modul_name)
        self.assertTrue(hasattr(modul, klassen_name),
                        f"{modul_name}.{klassen_name} fehlt — abteilung_laden wuerde scheitern")

    def test_nummern_sind_eindeutig(self):
        nummern = []
        for modul_name, klassen_name in orchestrator.ABTEILUNGEN.values():
            nummern.append(getattr(__import__(modul_name), klassen_name).NUMMER)
        self.assertEqual(len(nummern), len(set(nummern)), f"doppelte Abteilungsnummer: {nummern}")

    def test_unbekannte_abteilung_wird_abgelehnt(self):
        with self.assertRaises(ValueError):
            orchestrator.auftrag_anlegen("07 Gibt Es Nicht", "Ziel")


class AgentenTest(unittest.TestCase):
    """Ein Agent mit kaputtem Kopf wird von Claude Code still ignoriert."""

    def agenten(self):
        ordner = os.path.join(BASIS, ".claude", "agents")
        return [os.path.join(ordner, d) for d in sorted(os.listdir(ordner))
                if d.startswith("seo-")]

    def test_fuenf_seo_agenten(self):
        self.assertEqual(5, len(self.agenten()))

    def test_kopf_ist_vollstaendig_und_name_passt_zur_datei(self):
        for pfad in self.agenten():
            with self.subTest(os.path.basename(pfad)):
                with open(pfad, encoding="utf-8") as f:
                    text = f.read()
                kopf = re.match(r"^---\n(.*?)\n---\n", text, re.S)
                self.assertIsNotNone(kopf, "kein Frontmatter")
                name = re.search(r"^name:\s*(\S+)$", kopf.group(1), re.M)
                self.assertIsNotNone(name, "kein Feld name")
                self.assertEqual(os.path.basename(pfad)[:-3], name.group(1))
                for feld in ("description", "model"):
                    self.assertIsNotNone(
                        re.search(rf"^{feld}:\s*\S", kopf.group(1), re.M),
                        f"kein Feld {feld}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
