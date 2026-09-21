# Betriebswissen für Claude Code in diesem Repo

Diese Datei wird bei jeder neuen Session automatisch gelesen. Alles, was hier nicht steht,
ist beim nächsten Mal vergessen — jede Session läuft in einem frischen, ephemeren Container.
Etwas dauerhaft merken heißt: hier (oder in `sourcing/`, `markenwissen.py`) committen, nicht
nur im Chat erwähnen.

## Björn

- Björn Bulko, Inhaber Bellowerk Manufaktur (vormals „Herr Bello und Frau Wuff Manufaktur"), Hamburg.
- Privates/geschäftliches Gmail-Konto: **pijoern.nodels@googlemail.com**. Wenn ein
  Gmail-MCP-Werkzeug in der Session verfügbar ist, ist das dieses Konto — nicht nachfragen,
  einfach nutzen (z. B. `mcp__Gmail__search_threads`, um Lieferantenkontakte oder frühere
  Korrespondenz zu finden, bevor eine Adresse als „unbekannt" gilt).
- Ob der Gmail-Connector in einer Session überhaupt verfügbar ist, entscheidet die Plattform,
  nicht diese Datei — falls die Tools fehlen, kurz sagen, dass kein Mail-Zugriff besteht,
  statt es stillschweigend zu versuchen.
- Nach jedem Versand an einen neuen Lieferanten kurz danach (gleiche Antwort, nicht erst am
  Ende der Session) per `mcp__Gmail__search_threads` nach `from:(mailer-daemon OR postmaster)`
  suchen. Kommt ein Bounce ("Adresse nicht gefunden"/"Non-Delivery"): nicht nur melden, sondern
  sofort reagieren — eine bekannte Alternativadresse derselben Firma probieren, sonst kurz
  nachrecherchieren (Impressum/Kontaktseite) oder ein weiteres Unternehmen aus der Liste
  anschreiben. Das Ergebnis (welche Adresse tatsächlich zugestellt wurde) in die jeweilige
  Lieferantendatei eintragen, nicht nur im Chat erwähnen.

## Lieferanten-Wissen ist Dateiwissen, kein Chat-Wissen

- China-Lieferanten: `sourcing/lieferanten/shortlist.md` + `tracker.csv`.
- Deutsche/europäische Lieferanten (Auftragsarbeit): `sourcing/lieferanten-deutschland/*.md`,
  ein File pro Lieferant. Neuer Lieferant → neue Datei nach demselben Muster wie
  `maly-leder.md` (Kontext, Status, ggf. E-Mail-Adresse, sendefertiger Text).
- Wird eine Kontakt-E-Mail-Adresse herausgefunden (Gmail-Suche, Websuche, Björns Angabe),
  sofort in die jeweilige Lieferantendatei eintragen. Erst dann kann Abteilung 05/06 sie
  automatisch anschreiben (`lieferant.email` im JSON-Ergebnis, siehe README
  „Mail an Lieferanten").
- `sourcing/antworten-uebersicht.md` ist die laufende Kurzübersicht über alle Anfragen
  (Status, Preis, MOQ, Muster, Lieferzeit) über alle Kategorien und Länder hinweg. Trifft
  eine Lieferantenantwort per Mail ein (Gmail-Suche nach Absenderdomain), Konditionen dort
  eintragen UND in der jeweiligen Einzeldatei — nicht nur im Chat zusammenfassen.

## Sonst

- Markenfakten (Preise, Ausschlüsse, Werkstoffe) stehen bindend in `markenwissen.py` und
  `sourcing/bellowerk/markenbrief.md` — nicht aus dem Gedächtnis raten, dort nachlesen.
- Architekturregeln der Abteilungen: siehe `abteilung_basis.py`-Kopfkommentar — diese Datei
  nie ändern, abteilungsspezifisches Verhalten gehört in die jeweilige `abteilung_*.py`.
