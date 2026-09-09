# Prompt: Bellowerk-Server prüfen, dann (erst nach Freigabe) Einkauf China ergänzen

## Vorab (einmalig)

Per SSH als root auf den Server, dann:

```
cd /opt/bello
claude
```

Falls Claude Code noch fehlt: `npm install -g @anthropic-ai/claude-code`, dann Schlüssel aus
`/etc/bello/env` wiederverwenden (`export $(grep ANTHROPIC_API_KEY /etc/bello/env)`) statt einen
neuen anzulegen. Dann den Prompt unten komplett einfügen.

---

## Der Prompt

Du arbeitest als root auf dem netcup-VPS (Debian 13, Hostname v2202609413684515441.powersrv.de),
auf dem der KI-Agentenbetrieb der Lederwaren-Manufaktur **Bellowerk** unter `/opt/bello` läuft:
orchestrator.py mit den Abteilungen 01–04, systemd-Timer `bello-orchestrator.timer` täglich 07:00,
Betriebsnutzer `bello`, Geheimnisse in `/etc/bello/env` und `/opt/bello/config.json`, funktionierende
Mail-Eskalation. Antworte auf Deutsch. Inhaber und einziger Entscheider ist Björn.

Dieser Auftrag hat **zwei Phasen**. Phase 1 ist reine Diagnose — nichts wird verändert, nichts
gelöscht, nichts überschrieben. Danach **stoppst du und wartest auf Björns ausdrückliche Freigabe**
(Björn schreibt "weiter" oder "passt"). Phase 2 (der eigentliche Einbau) beginnst du erst danach.
Weicht in Phase 1 etwas ab oder fehlt etwas, meldest du es und wartest auf Anweisung — du reparierst
nichts eigenmächtig.

### Arbeitsweise (für beide Phasen)

- Erst lesen, dann ändern. Vor jedem Überschreiben eine Sicherung.
- Idempotent: ein zweiter Durchlauf darf nichts kaputt machen.
- **Geheimnisse bleiben, wo sie sind.** `config.json`, `/etc/bello/env`, `auftraege.json`, Logs,
  `venv/`, `zeichnungen/` werden nie überschrieben, nie in git eingecheckt, nie in der Ausgabe gezeigt
  (Passwörter/Keys beim Anzeigen von config.json immer herausfiltern).
- Fehlt dir etwas, das nur Björn hat (GitHub-Zugang, Schlüssel), stopp an der Stelle und frag konkret.
- Keine ausführlichen Erklärungen — arbeiten, kompakt berichten.

---

## Phase 1 — Diagnose (nur lesen, nichts verändern)

1. `ls -la /opt/bello` — welche Dateien/Ordner sind da.
2. `cat /opt/bello/config.json | grep -v -E "password|api_key"` (nur Struktur zeigen, keine Geheimnisse).
3. `systemctl status bello-orchestrator.timer` und `systemctl list-timers | grep bello`.
4. `journalctl -u bello-orchestrator -n 20 --no-pager` — laufen die Tagesläufe.
5. `cd /opt/bello && venv/bin/python orchestrator.py --stand` — welche Aufträge/Abteilungen bekannt sind.
6. `ls /opt/bello/*.py` — welche Abteilungen (01–04) tatsächlich vorhanden sind, mit `diff` prüfen ob
   sie vom Stand in der Drive-Quelle abweichen (lokale Verbesserungen wie Logging notieren, nicht anfassen).
7. `git -C /opt/bello status` — ist dort schon ein Repo, oder nicht.
8. **Optional, nur mit Ansage:** `venv/bin/python orchestrator_mail.py --test` schickt eine echte
   Testmail an Björns Adresse — nur ausführen, wenn du das im Bericht ausdrücklich ankündigst, da es
   eine reale Mail verschickt.

Fasse das Ergebnis für Björn kompakt zusammen: Läuft der Timer, kommt Mail an, welche Abteilungen
sind da, gibt es Abweichungen vom erwarteten Stand. **Dann stoppst du** und schreibst z. B.:
"Alles wie erwartet intakt. Sag 'weiter', wenn ich Abteilung 05 Einkauf China ergänzen soll."

---

## Phase 2 — Einbau (erst nach Björns "weiter"/"passt")

### Ziel

Der Code liegt in GitHub: `https://github.com/nodels81/Orchestrator` (Branch `main`; falls `main`
nicht existiert, Branch `claude/bellowerk-china-sourcing-dk8k49`). Dort ist die neue **Abteilung 05
"Einkauf China"** (`abteilung_einkauf_china.py`) bereits in `orchestrator.py` registriert, dazu der
Ordner `sourcing/` mit Markenbrief, Tech Packs, Zeichnungen, Fotos, Nachrichtenvorlagen und
Lieferanten-Shortlist. `/opt/bello` soll danach ein Klon dieses Repos sein, damit künftige Änderungen
per `git pull` ankommen — bei laufender Mail-Eskalation und ohne Abteilungen 01–04 zu verlieren.

### Aufgaben

1. **Sicherung.** `cp -a /opt/bello /opt/bello.bak-$(date +%Y%m%d-%H%M)`.

2. **Repo holen.** `git clone https://github.com/nodels81/Orchestrator /opt/bello.neu`
   (Branch siehe oben; ist das Repo privat, Björn nach Token oder Deploy-Key fragen).

3. **Zusammenführen.** Lokale Verbesserungen aus Phase 1 Punkt 6 (Logging, Retry-Begrenzung, Pfade)
   in die Repo-Dateien in `/opt/bello.neu` übernehmen — nicht umgekehrt. Die Zeile
   `"05 Einkauf China": ("abteilung_einkauf_china", "EinkaufChina"),` im Dict `ABTEILUNGEN` muss am
   Ende vorhanden sein. Dann aus dem alten `/opt/bello` **nur** diese Dinge nach `/opt/bello.neu`
   kopieren: `config.json`, `auftraege.json`, `venv/` bzw. `.venv/`, `logs/`, `zeichnungen/`,
   `BETRIEB.md`, `requirements.txt`. Danach `/opt/bello` gegen `/opt/bello.neu` tauschen (`mv`).
   Rechte wiederherstellen: `chown -R bello:bello /opt/bello`, `chmod 640 /opt/bello/config.json`.

4. **Umgebung prüfen.** `venv/bin/pip install anthropic` falls fehlend; `requirements.txt`
   aktualisieren. `venv/bin/python -c "import abteilung_einkauf_china; print('ok')"` muss `ok` liefern.

5. **Probelauf.** `venv/bin/python orchestrator.py --probelauf` und `--stand`. Fehler beheben.

6. **Echtlauf mit kleinem Umfang.** Auftrag anlegen:
   `venv/bin/python orchestrator.py --auftrag "05 Einkauf China" "Erstkontakt/RFQ (Vorlage 01) fuer HB-01 und LE-01 an Wenzhou Vigorous Pet Products, 100 Stueck je Modell, Muster zuerst" 2026-09-19`
   Dann `venv/bin/python orchestrator.py` ausführen. Zeige die tatsächliche Ausgabe (Entwurf der
   Nachricht, Entscheidungen für Björn). Die Eskalationsmail muss bei Björn ankommen; kommt sie
   nicht, `orchestrator_mail.py --test` und die netcup-Mail-Sperre prüfen (siehe BETRIEB.md).

7. **Timer und Abteilungen 01–04 erneut prüfen.** `systemctl list-timers | grep bello`,
   `venv/bin/python orchestrator.py --stand`. Vergleiche mit Phase 1 — nichts darf fehlen.

8. **Git-Hygiene.** In `/opt/bello`: `git status` darf keine Geheimnisse als untracked zeigen
   (`.gitignore` deckt config.json, auftraege.json, Logs, venv ab — prüfen).
   `grep -r "sk-ant" /opt/bello --include=*.py --include=*.md` muss leer sein.

9. **BETRIEB.md ergänzen.** Abschnitt "Neue Version holen": `cd /opt/bello && git pull &&
   venv/bin/python orchestrator.py --probelauf`. Abschnitt "Einkauf China beauftragen" mit dem
   Aufruf aus Schritt 6. Kurz, in Björns Sprache.

### Regeln im Betrieb (unverändert)

- Der Orchestrator gibt kein Geld aus. Muster, Anzahlung, Bestellung → Eskalation an Björn.
- Ein Lauf pro Tag. Keine Endlosschleifen.
- Der Server macht Agentenbetrieb, sonst nichts.

### Abschluss — berichte in dieser Form

1. Was jetzt läuft (je Punkt ein belegendes Kommando)
2. Was du geändert oder angelegt hast, Datei für Datei
3. Was Björn selbst tun muss — nummeriert, mit Klickweg oder Kommando
4. Was du bewusst nicht angefasst hast und warum
