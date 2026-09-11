# Die sieben Einstellungsfragen

Jede neue Stelle muss alle sieben bestehen. Fällt eine durch, wird nicht eingestellt — dann
schärfst du einen bestehenden Agenten nach oder schreibst einen Skill.

1. **Fällt die Arbeit wiederholt an?** Eine einmalige Aufgabe braucht keinen Agenten, sondern
   einen Auftrag an einen bestehenden.
2. **Deckt sie wirklich kein vorhandener Agent ab?** Alle Beschreibungen in `.claude/agents/`
   gelesen — nicht geraten. Überschneidung von mehr als einem Drittel heißt: nachschärfen, nicht
   einstellen.
3. **Fehlt ein Können oder nur Wissen?** Fehlt Wissen, gehört es in einen Skill, den mehrere
   Agenten lesen. Nur ein fehlendes *Können* rechtfertigt eine eigene Stelle.
4. **Lässt sich der Auftrag in einem Satz ohne „und" sagen?** Geht das nicht, sind es zwei
   Stellen — oder eine falsch geschnittene.
5. **Ist die Dateihoheit frei?** Welche Dateien schreibt er? Gehören sie schon jemandem, gibt es
   beim Parallelbetrieb kaputte Stände. Erst die Grenze klären, dann einstellen.
6. **Ist die Abnahme prüfbar?** Woran erkennt Björn, dass diese Stelle gute Arbeit geliefert hat?
   Ohne prüfbares Ergebnis entsteht ein Agent, der nur Text produziert.
7. **Wer prüft ihn?** Jede Abteilung hat einen Prüfer (`china-qc-pruefer`, `android-tester`,
   `web-qc-abnahme`). Niemand beurteilt die eigene Arbeit. Fehlt der Prüfer, ist er die
   wichtigere Einstellung.

## Probelauf vor der Übergabe

Ein neuer Agent gilt erst als eingestellt, wenn du beides notiert hast:

- **Auslösesatz** — ein realistischer Satz, wie Björn ihn sagen würde, der genau diesen Agenten
  treffen muss und keinen anderen.
- **Sollergebnis** — was er darauf liefern soll, in zwei Zeilen.

Trifft der Auslösesatz auch einen anderen Agenten, ist die Beschreibung noch nicht scharf genug.
