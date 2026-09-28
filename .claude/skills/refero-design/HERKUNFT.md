# Herkunft

Unverändert übernommen aus dem offiziellen Refero-Repository, damit der Skill in jeder
Claude-Code-Session mit diesem Repo zur Verfügung steht.

| | |
|---|---|
| Quelle | https://github.com/referodesign/refero_skill (`skills/refero-design/`) |
| Version | 1.0.2, Commit `a9b54a3e62a6391f5f5ab7a20e4ddb32fb79a27d` |
| Übernommen | 28. September 2026 |
| Lizenz | MIT, siehe `LICENSE` (Copyright 2026 Refero) |
| Weggelassen | `agents/openai.yaml` (nur für Codex) |

## Was der Skill ohne Refero-Konto kann

Die Methodik (erst recherchieren, dann Richtung festlegen, dann bauen, dann prüfen) und die
Handwerksreferenzen in `references/` (Typografie, Farbe, Bewegung, Icons, Texte,
Anti-KI-Einheitslook) funktionieren ohne Konto.

Die Live-Recherche in der Refero-Bibliothek (Stile, 150.000 App-Screens, Flows) braucht den
Refero-MCP-Server und ein **bezahltes Refero-Konto**:

```bash
claude mcp add --transport http refero https://api.refero.design/mcp
# danach in Claude Code: /mcp → refero → im Browser bei Refero anmelden
```

## Vorrang in diesem Repo

Für alles, was Bellowerk betrifft, gilt zuerst `.claude/skills/bellowerk-design/SKILL.md`
mit dem festgelegten Designsystem `design/DESIGN.md`. Wo sich die Regeln widersprechen, hat
die Marke Vorrang (Beispiel: Refero erlaubt KI-generierte Bilder, Bellowerk nicht).

## Aktualisieren

```bash
git clone --depth 1 https://github.com/referodesign/refero_skill /tmp/refero_skill
cp -r /tmp/refero_skill/skills/refero-design/SKILL.md /tmp/refero_skill/skills/refero-design/references .claude/skills/refero-design/
```

Danach Version und Commit oben anpassen.
