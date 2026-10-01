# Fortschritt Video-Studio (Stand 2026-10-01)

Auftrag: `video-studio-setup.md` (liegt in diesem Ordner).

## Erledigt
- Auftrag gelesen.
- Umgebung geprüft: Die Cloud-Sitzung ist nicht Björns Windows-PC. Es gibt dort kein ssh/scp, und Port 22 des Servers
  `v220260941368451.powersrv.de` ist von dort nicht erreichbar. **Phase 0 ist daher noch nicht ausgeführt.**
- Entscheidung von Björn: Das Gerüst kommt in ein **neues, privates Repo `video-studio`** (nicht in dieses Repo).

## Offen / Blocker
1. Das Repo konnte nicht per Integration angelegt werden (403). **Björn legt es selbst an:**
   https://github.com/new -> Name `video-studio`, Private, README/.gitignore/Lizenz leer lassen.
2. Danach: Repo per `add_repo` (push-Zugriff) an die Sitzung hängen. Falls abgelehnt: Claude-GitHub-App
   Zugriff geben: https://github.com/apps/claude/installations/select_target
3. Phase 0 (SSH-Schlüssel, `studio-server`) muss auf Björns Windows-PC laufen (Claude Code in PowerShell)
   oder der Server muss anderweitig erreichbar sein.
4. Kein Zugriff auf Björns Browser in der Cloud-Sitzung.

## Nächste Schritte (beim Weitermachen)
- Repo `video-studio` anhängen, dann Phase 2 lokal vorbereiten: Ordnerstruktur, `CLAUDE.md`, `.gitignore`,
  `config/modelle.yaml`, 5 Stil-Steckbriefe, Agenten-Dateien, Skill-Gerüste, `video-studio-setup.md` hineinlegen.
- Danach Phase 0/1 auf dem PC bzw. Server, Phasen einzeln mit „weiter“.
