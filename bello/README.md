# Abteilung 05 Einkauf China — Einbau in den Bello-Orchestrator

Der bestehende Agentenbetrieb (`/opt/bello`, Dateien im Drive-Ordner "Bello Agenten") kennt vier
Abteilungen. Diese Datei fügt die fünfte hinzu, ohne den Rest zu ändern.

## Einbau (auf dem netcup-Server)

```bash
cd /opt/bello
cp /pfad/zum/repo/bello/abteilung_einkauf_china.py .
cp -r /pfad/zum/repo/sourcing ./sourcing
```

In `orchestrator.py` im Dict `ABTEILUNGEN` eine Zeile ergänzen:

```python
"05 Einkauf China": ("abteilung_einkauf_china", "EinkaufChina"),
```

Test ohne Orchestrator:

```bash
venv/bin/python abteilung_einkauf_china.py "Erstkontakt/RFQ fuer HB-01 und LE-01 an Wenzhou Vigorous Pet Products, 100 Stueck je Modell" --recherche
```

Auftrag über den Orchestrator:

```bash
venv/bin/python orchestrator.py --auftrag "05 Einkauf China" "Angebote fuer HB-01 von 5 Fabriken der Shortlist einholen" 2026-09-26
```

## Was die Abteilung tut

- Liest Markenbrief, Tech Packs HB-01/LE-01/PATCH-01 und die Shortlist als bindenden Kontext.
- Liefert im Feld `ergebnis`: was getan, sendefertiger Entwurf (englisch), Entscheidungen für Björn,
  nächster Schritt. Der Orchestrator eskaliert das Ergebnis wie gewohnt per Mail.
- Gibt kein Geld aus. Muster, Anzahlung und Bestellung werden als Entscheidung eskaliert.

## Hinweis Markenname

`markenwissen.py` führt noch `MARKE = "Herr Bello und Fraeulein Klaeff"`. Für den Einkauf gilt der
Produktname **Bellowerk / Manufaktur** (siehe `sourcing/bellowerk/markenbrief.md`). Wenn Björn die
Umbenennung im ganzen Betrieb will: `MARKE = "Bellowerk"` in `markenwissen.py` setzen — wirkt sofort
in allen Abteilungen.

## Mehrere Agenten parallel

Im Orchestrator: mehrere `--auftrag`-Zeilen an "05 Einkauf China" anlegen (z. B. je Lieferant einer);
der Tageslauf arbeitet sie nacheinander ab. In Claude Code (dieses Repo): die vier Agenten in
`.claude/agents/` können parallel gestartet werden (Scout, Spec-Writer, Einkäufer, QC-Prüfer).
