# Anschlüsse (MCP) — Perplexity, Firecrawl, Playwright, Composio

Geprüft am 28. September 2026 nach dem Reel "Claude + 4 Stecker". Anschlüsse geben Claude Werkzeuge:
Websuche, Webseiten auslesen, einen Browser, andere Apps. **Eingerichtet ist davon noch nichts.**
Schon verbunden (claude.ai): Gmail, Google Kalender, Google Drive, Metricool.

| Nr. | Anschluss | Wofür bei Bellowerk | Kosten | Empfehlung |
|---|---|---|---|---|
| 1 | Perplexity | Tiefenrecherche mit Quellen (Innovation) | API-Guthaben | Nein. Claude und der Orchestrator (`web_search` in `abteilung_basis.py`) suchen schon selbst. |
| 2 | Firecrawl | Lieferantenprofile auf Alibaba und Made-in-China prüfen (Fabrik oder Händler, Jahre, MOQ), Wettbewerberpreise, Refero-Stile holen | Kostenloser Einstieg, danach Abo | **Ja, jetzt.** Diese Seiten sind aus Cloud-Sessions gesperrt; der Connector läuft über einen anderen Weg. |
| 3 | Playwright | Browser steuern, Screenshots: Shop auf Handy und Desktop gegen `design/DESIGN.md` prüfen | Kostenlos | **Ja, sobald der Shop gebaut wird.** |
| 4 | Composio (Rube) | Über 500 Apps über einen Anschluss, z. B. Shopify, WhatsApp Business | Konto bei Composio | Später. Gmail, Kalender und Drive sind schon direkt verbunden. |

## Einrichten

**In claude.ai** (Cloud-Sessions, Handy): Einstellungen → Connectors → Firecrawl hinzufügen und
anmelden. Composio geht dort als eigener Connector mit der Adresse `https://rube.app/mcp`.

**In Claude Code auf dem Server oder am Rechner:**

```bash
# 1 Perplexity — Schlüssel aus dem Perplexity-API-Portal
claude mcp add --transport http perplexity https://api.perplexity.ai/mcp --header "Authorization: Bearer <SCHLUESSEL>"

# 2 Firecrawl — Schlüssel von firecrawl.dev
claude mcp add firecrawl -e FIRECRAWL_API_KEY=<SCHLUESSEL> -- npx -y firecrawl-mcp

# 3 Playwright — kostenlos; auf dem Server ohne Bildschirm mit --headless
claude mcp add playwright -- npx -y @playwright/mcp@latest --headless

# 4 Composio (Rube) — danach in Claude Code /mcp aufrufen und im Browser anmelden
claude mcp add --transport http rube -s user https://rube.app/mcp
```

Danach mit `/mcp` prüfen, ob der Anschluss verbunden ist.

## Regeln

- Schlüssel stehen nie im Repo und nie im Chat — sie bleiben auf dem Rechner, wie `config.json`.
- Jede Anmeldung, die Geld kostet, entscheidet Björn.
- Keine automatischen Nachrichten auf Alibaba oder Made-in-China. Nachrichten an Lieferanten sind
  Entwürfe, gesendet wird von Hand (Skill `china-sourcing`).
- Composio leitet Mails und App-Daten über einen weiteren Anbieter. Nur mit Björns Freigabe, keine
  Kundendaten.

## Vorschlag "Einkaufs-Montag" (nicht eingerichtet)

Das "Mo, 10 Uhr" aus dem Reel ist ein fester Zeitplan. Mit Gmail, Kalender und einer Claude-Routine
geht das ohne neue Anschlüsse:

1. Jeden Montag um 10 Uhr Gmail nach Antworten der Lieferanten aus `sourcing/lieferanten/tracker.csv`
   durchsuchen.
2. Angebote in den Tracker übertragen (Preis, MOQ, Musterkosten, Lieferzeit).
3. Wer seit mehr als 5 Werktagen nicht geantwortet hat: Nachfass-Mail nach
   `sourcing/vorlagen/02-nachfassen.md` als Gmail-Entwurf. Nichts wird gesendet.
4. Übersicht an Björn mit den offenen Entscheidungen.

Sinnvoll, sobald die ersten Anfragen verschickt sind — Stand heute steht jeder der 15 Lieferanten
auf "neu". Golden Week (1.–7. Oktober) und chinesisches Neujahr (6. Februar 2027) beachten.
