# Vor-Ort-Checkliste — gemeinsam durch die Datenlage

**Stand:** 11. September 2026 · **Für:** Operator und Besitzerin gemeinsam · **Zweck:** ansehen, entscheiden, aufschreiben — nichts verändert sich von allein.

## Die drei Grundregeln

1. **Alle Werkzeuge lesen nur.** Es wird nichts gelöscht, verschoben oder umbenannt — außer die Besitzerin tut es selbst.
2. **Keine Kopie wird bevorzugt.** „Beides behalten" ist immer eine erlaubte Antwort.
3. **Nichts ist eilig.** Eine halbe Runde ist eine ganze Runde, und jede Frage darf mit „weiß ich nicht" enden.

## Die Unterlagen — diese Dokumente gehören dazu

Alle Dokumente liegen im Projekt auf GitHub: **https://github.com/56eli/tanjaspeicherrepo**.
Name, Pfad im Projekt und Link stehen hier; bei der ersten Erwähnung in der Liste stehen sie noch einmal dabei.

- **Diese Checkliste** — `plans/drafts/vor-ort-checkliste-2026-09-11.md`
  https://github.com/56eli/tanjaspeicherrepo/blob/main/plans/drafts/vor-ort-checkliste-2026-09-11.md — das Blatt, das Sie gerade lesen.
- **Der Gesamtüberblick** — `plans/drafts/tanja-hauptdokument-2.md`
  https://github.com/56eli/tanjaspeicherrepo/blob/main/plans/drafts/tanja-hauptdokument-2.md — die Datenlage auf Deutsch, zum gemeinsamen Durchsehen.
- **Die Cloud-Anleitung** — `plans/drafts/tanja-cloud-pruefung.md`
  https://github.com/56eli/tanjaspeicherrepo/blob/main/plans/drafts/tanja-cloud-pruefung.md — gehört zu Schritt 2.
- **Die erste Entscheidungsrunde** — `plans/drafts/tanja-entscheidungsrunde-1.md`
  https://github.com/56eli/tanjaspeicherrepo/blob/main/plans/drafts/tanja-entscheidungsrunde-1.md — gehört zu Schritt 3.
- **Die Entscheidungskarten** — `plans/drafts/tanja-entscheidungskarten.md`
  https://github.com/56eli/tanjaspeicherrepo/blob/main/plans/drafts/tanja-entscheidungskarten.md — gehört zu Schritt 4, eine Karte je Lage.
- **Der Wartungsleitfaden** — `plans/drafts/tanja-wartungsleitfaden.md`
  https://github.com/56eli/tanjaspeicherrepo/blob/main/plans/drafts/tanja-wartungsleitfaden.md — gehört zu Schritt 5, was nach ihren Änderungen geschieht.
- **Das Koffer-Handbuch** (Englisch, für den Operator) — `docs/anydesk-20-minute-harvest.md`
  https://github.com/56eli/tanjaspeicherrepo/blob/main/docs/anydesk-20-minute-harvest.md — gehört zu Schritt 1 und 6, mit der Status-Tabelle für das Koffer-Fenster.
- **Der Ernte-Leitfaden** (Englisch, für den Operator) — `docs/foundational-facts-harvest.md`
  https://github.com/56eli/tanjaspeicherrepo/blob/main/docs/foundational-facts-harvest.md — die feste Kette der Koffer-Schritte und was jeder Schritt ausgibt.

## Zeitplan-Vorschlag (rund 75 Minuten)

| Minuten | Was | Wer |
|---|---|---|
| 0:00–0:05 | Koffer übertragen, auspacken, starten | Operator |
| 0:05–0:25 | Der Blick in die Cloud | gemeinsam |
| 0:25–0:40 | Die erste Entscheidungsrunde (drei Fragen) | gemeinsam |
| 0:40–1:05 | Entscheidungskarten, so weit Sie kommen | gemeinsam |
| 1:05–1:10 | Koffer beenden, Ergebnis verpacken | Operator |
| 1:10–1:15 | Änderungen notieren, verabschieden | gemeinsam |

## Vor dem Termin — zu Hause (Operator)

- [ ] Den 20-Minuten-Koffer bauen: `python scripts/build_harvest_kit.py` im Projektordner — https://github.com/56eli/tanjaspeicherrepo/blob/main/scripts/build_harvest_kit.py. Die fertige ZIP liegt danach unter `scripts/harvest-kit-<Datum>.zip` (etwa 20 MB).
- [ ] Koffer-ZIP bereitlegen: USB-Stick oder die Dateiübertragung der Fernwartung.
- [ ] Diese Checkliste mitnehmen (ausgedruckt oder auf dem Handy) — Link oben unter „Die Unterlagen".
- [ ] Notizblock oder Änderungsbuch bereit — alle Antworten werden in ihren Worten aufgeschrieben.
- [ ] Optional ausdrucken: die erste Entscheidungsrunde `plans/drafts/tanja-entscheidungsrunde-1.md` und die Entscheidungskarten `plans/drafts/tanja-entscheidungskarten.md` — Links oben unter „Die Unterlagen".
- [ ] Der Besitzerin vorher sagen: Für den Blick in die Cloud wird das Cloud-Passwort gebraucht (Anmeldung im Browser).

## Schritt 1 — Der Koffer läuft an (Operator, etwa 5 Minuten)

- [ ] Koffer-ZIP auf den Schreibtisch des PCs übertragen.
- [ ] Rechtsklick → „Alle extrahieren" → nach `C:\HarvestKit`.
- [ ] Optional — die zwei Manifest-Dateien der alten Projektkopie:
  - In der alten Projektkopie auf dem PC den Ordner `data/external-hashes/run-full/` öffnen. Gesucht sind genau zwei Dateien:
    - die große Liste jeder geprüften Datei der externen Platte: `detailed-verified-external-duplicates-2026-09-09-220307.csv.gz` — sie kann über 100 MB groß sein, das ist normal; sie liegt bereits auf dem PC, das Ziehen ist nur eine lokale Kopie, es wird nichts übertragen.
    - die kleine Begleitdatei: `verified-external-hash-metadata-2026-09-09-220307.json` — sie gehört dazu.
  - Nur diese beiden in `C:\HarvestKit\data\external-hashes\run-full\` ziehen. Weitere Dateien in dem Ordner (z. B. die Zusammenfassung und Begleitnotizen) werden nicht gebraucht und bleiben liegen.
  - Danach meldet die Summen-Stufe die geprüfte Gesamtsumme. Die beiden Dateien kommen nicht ins Ergebnisse-Paket zurück — das Paket enthält nur die frisch gesammelten Ergebnisse.
  - Nicht gefunden? Einfach überspringen — das ist ein erwartetes Ergebnis.
- [ ] Doppelklick auf `C:\HarvestKit\scripts\harvest_foundational_facts.cmd`. Das Fenster bleibt offen und arbeitet allein weiter. Getippt wird nichts.
- [ ] Das Fenster einfach laufen lassen — weiter mit Schritt 2.

## Schritt 2 — Der Blick in die Cloud (gemeinsam, während der Koffer läuft, 15–20 Minuten)

- [ ] Die Anleitung `plans/drafts/tanja-cloud-pruefung.md` — https://github.com/56eli/tanjaspeicherrepo/blob/main/plans/drafts/tanja-cloud-pruefung.md — öffnen (ausgedruckt oder auf dem Handy).
- [ ] Browser öffnen und beim Cloud-Dienst anmelden (OneDrive — das Passwort hat die Besitzerin).
- [ ] Ansehen: Liegen dort echte Dateien — oder sind nur Namen zu sehen, deren Inhalt woanders liegt?
- [ ] Ansehen: Wie voll ist der Speicher? Was zeigt der Dienst selbst an?
- [ ] Aufschreiben, was die Besitzerin sieht, in ihren Worten. „Ich konnte mich nicht einloggen" ist auch ein gültiges, wichtiges Ergebnis.
- [ ] Beim Ansehen **nichts ändern** — nichts löschen, nichts hochladen, nichts „zum Testen" anklicken.
- [ ] Diese vier Fragen kann ihr Blick klären: Was liegt wirklich in der Cloud? In welche Richtung arbeitet die Cloud (PC → Cloud, Cloud → PC, oder beides)? Was hat es mit den Dateien auf sich, die auf dem PC nur zu sehen sind? Ist versehentlich etwas heruntergeladen worden?

*Dieser Schritt ist der einzige Teil der Datenlage, den nur die Besitzerin klären kann — der ganze Rest ist im Projekt schon aufgeschrieben.*

## Schritt 3 — Die erste Entscheidungsrunde (gemeinsam, etwa 15 Minuten)

- [ ] Den Ablauf `plans/drafts/tanja-entscheidungsrunde-1.md` — https://github.com/56eli/tanjaspeicherrepo/blob/main/plans/drafts/tanja-entscheidungsrunde-1.md — öffnen; die drei Fragen stehen dort.
- [ ] **Frage 1 — die Reihenfolge:** erst die Inhalte entscheiden, danach die Struktur · Ordner für Ordner beides zusammen · erst die Struktur, danach die Inhalte. Sie wählt — keine Möglichkeit wird bevorzugt.
- [ ] **Frage 2 — der Ablage-Ort:** ein Ablage-Ordner auf der externen Platte · ein Ablage-Ordner auf einer Platte im PC · ohne Zwischenablage (dann gilt jede Änderung direkt, und das wird ausdrücklich aufgeschrieben). Sie wählt.
- [ ] **Frage 3 — zurückgeholte Ordner:** immer zurück in die Ablage · von Fall zu Fall entscheiden · dauerhaft im PC behalten. Sie wählt.
- [ ] Jede Antwort wird in ihren eigenen Worten aufgeschrieben — genau so, wie sie sie sagt.

## Schritt 4 — Die Entscheidungskarten (gemeinsam, so weit Sie kommen)

- [ ] Die Karten `plans/drafts/tanja-entscheidungskarten.md` — https://github.com/56eli/tanjaspeicherrepo/blob/main/plans/drafts/tanja-entscheidungskarten.md — öffnen. Eine Karte je Lage; die Reihenfolge folgt der internen Liste des Projekts.
- [ ] Die klarste Gruppe (21 Lagen) kommt in den Gesprächen zuerst dran.
- [ ] Karte für Karte: die Beschreibung lesen, dann die drei Möglichkeiten: **Beides behalten · Bereinigen · Parken.**
- [ ] Sie entscheidet. Keine Kopie wird bevorzugt, und keine Karte muss heute beantwortet werden.
- [ ] Entscheidet sie „Bereinigen": **Heute passiert damit noch nichts.** Es folgt ein eigener Schritt — erst ihre Freigabe und ein Eintrag im Änderungsbuch, dann führt sie selbst aus, dann eine neue Prüfung.
- [ ] Jede Entscheidung wird notiert. Eine beantwortete Karte wird festgehalten, eine offene bleibt offen.
- [ ] Aufhören dürfen Sie immer — eine halbe Runde ist eine ganze Runde.

## Schritt 5 — Wenn die Besitzerin selbst etwas ändert

- [ ] Sie darf jederzeit löschen, verschieben oder umbenennen — es sind ihre Daten. Niemand hält sie auf, und es braucht keine Begründung.
- [ ] Jede Änderung kommt kurz ins Änderungsbuch: was, wann — in ihren Worten.
- [ ] Nach ihren Änderungen wird neu gesammelt: den Koffer aus Schritt 1 noch einmal starten (wieder rund 20 Minuten, liest nur).
- [ ] Bis die neue Sammlung durch ist, gilt der betroffene Eintrag als „noch nicht erneut geprüft" — und wird auch so gezeigt. Nichts wird stillschweigend als aktuell ausgegeben.
- [ ] Der Wartungsleitfaden `plans/drafts/tanja-wartungsleitfaden.md` — https://github.com/56eli/tanjaspeicherrepo/blob/main/plans/drafts/tanja-wartungsleitfaden.md — erklärt das Ganze für sie in Ruhe.

## Schritt 6 — Der Koffer wird fertig (Operator, etwa 5 Minuten)

- [ ] Fenster prüfen: Steht die letzte Zeile da (`Finished … Final exit code`)? Fertig.
- [ ] Anderer Status im Fenster? Die Status-Tabelle im Koffer-Handbuch `docs/anydesk-20-minute-harvest.md` — https://github.com/56eli/tanjaspeicherrepo/blob/main/docs/anydesk-20-minute-harvest.md — sagt, was jeder Status bedeutet — grob: „skipped - output already present" ist gut · „skipped - drive not uniquely identifiable" heißt: keinen Buchstaben raten · „failed \| exit=2" beim Summen-Helfer ist erwartet, wenn die zwei Manifest-Dateien aus Schritt 1 fehlen.
- [ ] Hartes Stoppen: **Minute 15** — läuft die Bestandsaufnahme noch, einfach laufen lassen (sie liest nur). **Minute 17** — fehlt die letzte Zeile noch, Fenster schließen und trotzdem einpacken; im Bericht notieren, welcher Schritt nicht fertig wurde.
- [ ] Doppelklick auf `C:\HarvestKit\scripts\pack_results.cmd` → das Paket `harvest-results-<Zeitstempel>.zip` liegt auf dem Schreibtisch (sonst im Koffer-Ordner).
- [ ] Das Paket mitnehmen — USB-Stick oder Übertragung zurück.

## Nach dem Termin — zu Hause (Operator)

- [ ] Sichtung: den Inhalt des Pakets ansehen (Sammelprotokoll, Topologie-Bericht, neue Bestandsdateien). Datenschutz-Regel aus `README.md` — https://github.com/56eli/tanjaspeicherrepo/blob/main/README.md: keine Dateizeilen und keine langen Pfade in irgendeinen Text kopieren.
- [ ] Hochladen über den üblichen Weg — delegierte PR nach der Sichtung, **nie vom PC der Besitzerin aus**.
- [ ] Ihre Antworten aus Schritt 2 bis 4 eintragen, in ihren Worten — das Entscheidungs-Log entsteht jetzt mit ihren echten Antworten.
- [ ] Das Änderungsbuch auf den neuen Stand bringen.
- [ ] Prüfen: Passt der aufgeschriebene Stand jetzt wieder zur Wirklichkeit? Falls keine neue Sammlung möglich war, die betroffenen Einträge als „noch nicht erneut geprüft" markieren.

---

**Die Versprechen:** Jedes Werkzeug liest nur. Außer der Besitzerin ändert niemand etwas. Jeder Eintrag trägt ein Datum. Veraltetes wird gezeigt, nicht versteckt. Sie bleibt die Chefin über ihre Daten.
