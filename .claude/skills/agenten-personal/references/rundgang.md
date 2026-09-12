# Rundgang und Freigabe-Ablauf

## Der Rundgang

Wöchentlich, automatisch: `personal_rundgang.py` liest Organigramm, alle Agenten, alle Skills,
den Auftragsstand und das Personalprotokoll, sucht Schwachstellen und mailt Björn den Bericht.

```bash
venv/bin/python personal_rundgang.py --probelauf   # zeigt nur, was geladen wird
venv/bin/python personal_rundgang.py               # Bericht erzeugen und anzeigen
venv/bin/python personal_rundgang.py --senden      # Bericht erzeugen und mailen
```

Derselbe Rundgang lässt sich jederzeit von Hand auslösen: `Nutze den Agenten wiebke: Rundgang.`

**Der Rundgang stellt niemanden ein.** Er meldet. Eingestellt wird erst nach Björns Freigabe.

### Woran ein Schwachpunkt erkannt wird

| Befund | Woran man ihn sieht | Regelmaßnahme |
|---|---|---|
| Stelle fehlt | Eine Aufgabe taucht in Aufträgen auf, kein Agent deckt sie ab | einstellen |
| Prüfer fehlt | Eine Abteilung hat niemanden, der Fertigmeldungen nachprüft | einstellen, mit Vorrang |
| Doppelbesetzung | Zwei Beschreibungen überlappen um mehr als ein Drittel | zusammenlegen |
| Wird nie gerufen | Agent existiert, taucht in keinem Auftrag auf | Beschreibung nachschärfen |
| Zu breit | Beschreibung braucht drei „und", Arbeit wirkt halb | Zuschnitt verengen oder teilen |
| Wissen driftet | Dieselbe Regel steht in mehreren Agenten | in den Skill verschieben |
| Grenze fehlt | Zwei Agenten schreiben dieselben Dateien | Dateihoheit festlegen |
| Abteilung überfüllt | Mehr als acht Agenten | Zuschnitt der Abteilung prüfen |

**Kein Befund ohne Beleg**: immer Datei oder Agentenname nennen. Und ein ruhiger Bericht ist ein
gutes Ergebnis — ein erfundener Befund kostet Björn mehr Zeit als zwei Sätze „läuft".

## Der Freigabe-Ablauf

Vier Schritte, keiner wird übersprungen. Björn entscheidet zweimal: über die Stelle und über den
fertigen Text.

1. **Vorschlagen.** Was fehlt, warum, was es kostet, welche Alternative es gäbe (fast immer:
   nachschärfen statt einstellen). Als Satz, den Björn mit „ja" beantworten kann.
2. **Warten.** Ohne Björns „ja" wird keine Agentendatei angelegt und nichts committet.
3. **Schreiben und vorlegen.** Die fertige Datei im Wortlaut zeigen, dazu die sieben
   Einstellungsfragen beantwortet und der Probelauf: Auslösesatz und Sollergebnis.
4. **Hochladen.** Erst nach Björns zweiter Freigabe: Datei anlegen, Zeile ins
   `personal/protokoll.md`, Organigramm im `README.md` nachziehen, committen und pushen —
   alles in einem Commit, damit Stellenplan und Protokoll nie auseinanderlaufen.

Abschaffen und Zusammenlegen laufen genauso: vorschlagen, warten, ausführen. Eine bestehende
Agentendatei wird nie ohne Freigabe gelöscht.
