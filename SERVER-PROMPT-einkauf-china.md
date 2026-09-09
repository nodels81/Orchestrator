# Prompt: Abteilung 05 Einkauf China auf dem netcup-Server in Betrieb nehmen

## Vorab (einmalig)

Per SSH als root auf den Server, dann:

```
cd /opt/bello && claude
```

Falls Claude Code noch fehlt: `npm install -g @anthropic-ai/claude-code` und
`export ANTHROPIC_API_KEY=...` (Schlüssel liefert Björn). Dann den Prompt unten komplett einfügen.

---

## Der Prompt

Du arbeitest als root auf dem netcup-VPS (Debian 13, Hostname v2202609413684515441.powersrv.de),
auf dem der KI-Agentenbetrieb der Lederwaren-Manufaktur **Bellowerk** unter `/opt/bello` läuft
(orchestrator.py mit den Abteilungen 01–04, systemd-Timer `bello-orchestrator.timer` täglich 07:00,
Betriebsnutzer `bello`, Geheimnisse in `/etc/bello/env` und `/opt/bello/config.json`). Antworte auf
Deutsch. Inhaber und einziger Entscheider ist Björn.

### Ziel

Der Code liegt jetzt in GitHub: `https://github.com/nodels81/Orchestrator` (Branch `main`; falls
`main` nicht existiert, Branch `claude/bellowerk-china-sourcing-dk8k49`). Dort ist die neue
**Abteilung 05 "Einkauf China"** (`abteilung_einkauf_china.py`) bereits in `orchestrator.py`
registriert, dazu der Ordner `sourcing/` mit Markenbrief, Tech Packs, Zeichnungen, Fotos,
Nachrichtenvorlagen und Lieferanten-Shortlist. `/opt/bello` soll ab jetzt ein Klon dieses Repos
sein, damit künftige Änderungen per `git pull` ankommen.

### Arbeitsweise

- Erst lesen, dann ändern. Vor jedem Überschreiben eine Sicherung: `cp -a /opt/bello /opt/bello.bak-$(date +%Y%m%d-%H%M)`.
- Idempotent: ein zweiter Durchlauf darf nichts kaputt machen.
- **Geheimnisse bleiben, wo sie sind.** `config.json`, `/etc/bello/env`, `auftraege.json`, Logs,
  `venv/`, `zeichnungen/` werden nie überschrieben, nie in git eingecheckt, nie in der Ausgabe gezeigt.
- Fehlt dir etwas, das nur Björn hat (GitHub-Zugang, Schlüssel), stopp an der Stelle und frag konkret.
- Keine ausführlichen Erklärungen — arbeiten, am Ende kompakt berichten.

### Aufgaben

1. **Bestandsaufnahme.** `ls -la /opt/bello`, `systemctl status bello-orchestrator.timer`,
   `git -C /opt/bello status` (falls schon ein Repo). Prüfe mit `diff`, ob `orchestrator.py`,
   `abteilung_basis.py`, `orchestrator_mail.py` auf dem Server von der Drive-Version abweichen
   (z. B. Logging aus der Fertigstellung). Notiere Abweichungen.

2. **Sicherung.** `cp -a /opt/bello /opt/bello.bak-$(date +%Y%m%d-%H%M)`.

3. **Repo holen.** `git clone https://github.com/nodels81/Orchestrator /opt/bello.neu`
   (Branch siehe oben; ist das Repo privat, Björn nach Token oder Deploy-Key fragen).

4. **Zusammenführen.** Wenn die Server-Dateien aus Schritt 1 lokale Verbesserungen haben
   (Logging, Retry-Begrenzung, Pfade), übernimm diese Änderungen in die Repo-Dateien in
   `/opt/bello.neu` — nicht umgekehrt. Die Zeile
   `"05 Einkauf China": ("abteilung_einkauf_china", "EinkaufChina"),` im Dict `ABTEILUNGEN`
   muss am Ende vorhanden sein. Dann aus dem alten `/opt/bello` **nur** diese Dinge nach
   `/opt/bello.neu` kopieren: `config.json`, `auftraege.json`, `venv/` bzw. `.venv/`, `logs/`,
   `zeichnungen/`, `BETRIEB.md`, `requirements.txt`. Danach `/opt/bello` gegen `/opt/bello.neu`
   tauschen (`mv`). Rechte wiederherstellen: `chown -R bello:bello /opt/bello`,
   `chmod 640 /opt/bello/config.json`.

5. **Umgebung prüfen.** `venv/bin/pip install anthropic` falls fehlend; `requirements.txt`
   aktualisieren. `venv/bin/python -c "import abteilung_einkauf_china; print('ok')"` muss `ok` liefern.

6. **Probelauf.** `venv/bin/python orchestrator.py --probelauf` und `--stand`. Fehler beheben.

7. **Echtlauf mit kleinem Umfang.** Auftrag anlegen:
   `venv/bin/python orchestrator.py --auftrag "05 Einkauf China" "Erstkontakt/RFQ (Vorlage 01) fuer HB-01 und LE-01 an Wenzhou Vigorous Pet Products, 100 Stueck je Modell, Muster zuerst" 2026-09-19`
   Dann `venv/bin/python orchestrator.py` ausführen. Zeige die tatsächliche Ausgabe (Entwurf der
   Nachricht, Entscheidungen für Björn). Die Eskalationsmail muss bei Björn ankommen; kommt sie
   nicht, `orchestrator_mail.py --test` und die netcup-Mail-Sperre prüfen (siehe BETRIEB.md).

8. **Timer prüfen.** `systemctl list-timers | grep bello` — der Tageslauf muss unverändert aktiv sein
   und auf `/opt/bello/orchestrator.py` zeigen. `journalctl -u bello-orchestrator -n 20`.

9. **Git-Hygiene.** In `/opt/bello`: `git status` darf keine Geheimnisse als untracked zeigen
   (`.gitignore` deckt config.json, auftraege.json, Logs, venv ab — prüfen). `grep -r "sk-ant" /opt/bello --include=*.py --include=*.md` muss leer sein.

10. **BETRIEB.md ergänzen.** Abschnitt "Neue Version holen": `cd /opt/bello && git pull &&
    venv/bin/python orchestrator.py --probelauf`. Abschnitt "Einkauf China beauftragen" mit dem
    Aufruf aus Schritt 7. Kurz, in Björns Sprache.

### Regeln im Betrieb (unverändert)

- Der Orchestrator gibt kein Geld aus. Muster, Anzahlung, Bestellung → Eskalation an Björn.
- Ein Lauf pro Tag. Keine Endlosschleifen.
- Der Server macht Agentenbetrieb, sonst nichts.

### Abschluss — berichte in dieser Form

1. Was jetzt läuft (je Punkt ein belegendes Kommando)
2. Was du geändert oder angelegt hast, Datei für Datei
3. Was Björn selbst tun muss — nummeriert, mit Klickweg oder Kommando
4. Was du bewusst nicht angefasst hast und warum
