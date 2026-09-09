# Orchestrator — Bellowerk Auslandseinkauf China

Arbeitsumgebung für den Einkauf kompletter Lederprodukte (Halsbänder, Führleinen, Flechtprodukte,
Handschlaufen) mit Marken-Namensschild "Bellowerk / Manufaktur" bei chinesischen Herstellern.
Alles, was der Einkäufer braucht, liegt hier; alles, was Geld kostet, entscheidet Björn.

## Aufbau

```
.claude/skills/china-sourcing/     Skill: Schreibregeln, Ablauf, Checklisten
  references/kommunikation.md      Kanäle, Sprache, Gesicht, Phrasen-Dekoder, Feiertage
  references/prozess-und-qc.md     Musterstufen, Prüfliste, PO-Klauseln, Incoterms, EU-Recht
  references/lieferanten-pruefung.md  Fabrik vs. Händler, rote Flaggen
.claude/agents/                    Vier Agenten: Einkäufer, Lieferanten-Scout, Spec-Writer, QC-Prüfer
sourcing/bellowerk/markenbrief.md  Markenwahrheit für den Einkauf (Werkstoffe, Ausschlüsse, Patch)
sourcing/bellowerk/specs/          Tech Packs (englisch) HB-01, LE-01, HB-02, LE-02, HS-01, PATCH-01
sourcing/bellowerk/zeichnungen/    Bemaßte Zeichnungen SVG + PNG
sourcing/bellowerk/bilder/         Beispielfotos (Björn legt sie ab, README sagt welche)
sourcing/vorlagen/                 Sendefertige Nachrichten: RFQ, Nachfassen, Muster, Feedback, Schnittmuster, Reklamation
sourcing/lieferanten/shortlist.md  35 recherchierte Kandidaten, priorisiert
sourcing/lieferanten/tracker.csv   Stand je Lieferant
bello/abteilung_einkauf_china.py   Abteilung 05 für den bestehenden Orchestrator auf dem Server
```

## So läuft eine Anfrage

1. Björn bestätigt die Startwerte in `specs/HB-01` und `specs/LE-01` am Referenzstück und legt
   Fotos in `sourcing/bellowerk/bilder/` ab (Dateinamen laut README dort).
2. In Claude Code: `Nutze den Agenten china-einkauf: RFQ für HB-01 und LE-01 an Wenzhou Vigorous
   Pet Products, Vorlage 01.` → sendefertiger Entwurf mit Anhangsliste.
3. Björn schickt die Nachricht (Alibaba-Chat / E-Mail) mit Zeichnung + Foto.
4. Antworten kommen zurück → `china-qc-pruefer` bewertet Angebot/Muster, `china-einkauf` schreibt
   Nachfass/Feedback. Tracker wird fortgeschrieben.
5. Muster, Anzahlung, Bestellung: Björn entscheidet. Schnittmuster mit allen Maßen sind Lieferumfang.

## Mehrere Agenten parallel

In Claude Code können die vier Agenten gleichzeitig laufen (z. B. Scout sucht Beschlag-Lieferanten,
während der Einkäufer RFQs an Lederfabriken schreibt). Auf dem Server: mehrere `--auftrag` an
"05 Einkauf China" anlegen, siehe `bello/README.md`.

## Bekannte Lücken

- Instagram (@herr.bello.und.frau.wuff) und herrbelloundfrauwuff.de sind aus der Cloud-Umgebung
  gesperrt — Fotos müssen manuell abgelegt werden.
- Größentabellen und Lochabstände sind Startwerte aus der Kernserie, nicht vermessen.
- Patch: `markenwissen.py` schließt Nähte aus, daher Messing-Namensschild mit Buchschrauben statt
  Stoff-Patch. Wenn Björn ein genähtes/gewebtes Patch will, muss die Ausschlussliste geändert werden.
