# Video-Studio – Phase 1 (Server absichern)

Auftrag: siehe `AUFTRAG.md`. Dieses Skript erledigt Phase 1 auf dem Netcup-VPS (Debian 13).

## Ablauf

1. Auf dem eigenen Rechner einen Schluessel anlegen, falls noch keiner existiert: `ssh-keygen -t ed25519`
2. Skript auf den Server kopieren und als root starten:
   ```bash
   scp video-studio/scripts/phase1-server.sh root@<server-ip>:/root/
   ssh root@<server-ip>
   STUDIO_PUBKEY="$(cat)" ./phase1-server.sh   # Inhalt von id_ed25519.pub einfuegen, Strg+D
   ```
   (oder direkt `STUDIO_PUBKEY="ssh-ed25519 AAAA..." ./phase1-server.sh`)
3. **Neues Terminal:** `ssh studio@<server-ip>` – muss ohne Passwort klappen.
4. Erst dann, die alte Root-Sitzung offen lassen: `sudo ./phase1-server.sh --harden-ssh`
5. Als `studio`: `claude` starten und anmelden. Danach geht es dort mit Phase 2 weiter.

## Was das Skript macht

Updates, Benutzer `studio` (sudo ohne Passwort, da nur Key-Login), ufw (nur SSH), fail2ban, automatische Sicherheitsupdates,
ffmpeg, Python+venv, Node 22 LTS, Chromium-Abhaengigkeiten, imagemagick, Schriften (Inter, Montserrat, Playfair Display, Caveat),
Swap (4 GB, falls <8 GB RAM und keiner vorhanden), Claude Code, leerer Ordner `~/video-studio` mit `git init`.

## Offen (klaeren, wenn dran)

- Backup-Ziel (Storage Box, S3, ...)
- Anthropic-Zugang fuer Claude Code auf dem Server
