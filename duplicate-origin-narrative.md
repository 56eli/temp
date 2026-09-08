# Wie Ihre doppelten Dateien entstanden sind — eine Spurensuche

**Stand:** 8. September 2026 · **Für:** Tanja, die Besitzerin des PCs · **Zweck:** verstehen, woher die Kopien kommen — nicht löschen.

> Dies ist eine **Deutung, kein Beweis**. Wir haben uns die Ordnernamen, Laufwerke und Daten Ihrer großen doppelten Dateien angesehen und daraus die wahrscheinlichste Geschichte rekonstruiert, wie jede Kopie entstanden sein könnte. Ordnernamen und Pfade geben starke Hinweise, aber wir können nicht beweisen, was vor Jahren genau passiert ist. Ziel ist, dass Sie Ihre eigenen Ordner wiedererkennen und sicherer entscheiden können, welche Ablage Ihnen am wichtigsten ist.

Sie müssen dafür nichts am PC tun. Lesen Sie in Ruhe — ein Stift für Notizen reicht. Welche Kopie Sie behalten möchten, halten Sie anschließend im Leitfaden `plans/drafts/duplicate-resolution-guide.md` fest.

---

## 1. Einleitung

Bei der Inhaltsprüfung mit SHA-256-Hashes haben wir 753 Gruppen von Dateien gefunden, die Byte für Byte identisch sind — insgesamt rund 212 GB logische Daten, davon lägen rechnerisch bis zu rund 125 GB in überzähligen Kopien (Obergrenze, kein Versprechen). Fast alle liegen auf D: („Große Platte“, 8 % frei) und E: („Lahme Platte“, 13 % frei).

Der Leitfaden `duplicate-resolution-guide.md` zeigt **wo** die Kopien liegen. Dieses Dokument fragt **wie** sie dorthin gekommen sein könnten.

Dafür haben wir für die größten Situationen ausgewertet:

- die **Ordnernamen** (der zuverlässigste Hinweis auf Absicht — z. B. „BACKUP“, „vom Handy gesichert“, „OneDrive“, „ALLE“, „Archiv“),
- die **Verschachtelung** (ein Ordner, der in seinem eigenen Unterordner noch einmal auftaucht, ist meist später hineinkopiert worden),
- die **Laufwerksbeziehung** (D: ist die Haupt-Platte, E: heißt „BACKUP lahme Platte (D)“ und sieht nach Sicherung von D: aus; Kopien D:→E: sind eher Sicherungen, Kopien innerhalb desselben Laufwerks eher organisatorisches Doppel-Ablegen),
- die **Änderungsdaten** (mit Vorsicht — Kopieren kann Daten erhalten oder neu setzen; gleiche Daten beim Kopieren sind aber ein Hinweis auf einen Kopiervorgang in einem Rutsch),
- die **Vollständigkeit** (hat Ordner A 500 Dateien und Ordner B nur 480 derselben Dateien, ist A eher die vollständigere Ablage).

**Wichtig:** Jede Geschichte unten nennt, worauf sie sich stützt, und wie sicher wir sind. Wir unterscheiden:

- **Sicher** — die Pfade zeigen es eindeutig.
- **Wahrscheinlich** — starke Hinweise, aber nicht bewiesen.
- **Vermutung** — plausibel, aber unsicher.

Sie kennen Ihre Ordner am besten. Wenn eine Geschichte zu Ihrer Erinnerung passt, können Sie ihr mehr vertrauen. Wenn sie nicht passt, kreuzen Sie im Leitfaden „Beides behalten“ an — das ist immer die sichere Wahl.

---

## 2. So lesen Sie dieses Dokument

- Jede nummerierte **Situation** unten beschreibt **eine große Doppel-Ablage** — sortiert nach Datenmenge, die größte zuerst.
- **Ursprung** = der Ort, der am ehesten das Original ist.
- **Kopierkette** = die wahrscheinliche Reihenfolge, in der die Kopien entstanden sind.
- **Empfehlung** = welche Kopie beim Durchblättern am ehesten als Haupt-Ablage in Frage kommt — **keine Anweisung**, etwas zu löschen oder zu verschieben.
- **Vertrauen:** *Sicher / Wahrscheinlich / Vermutung* (siehe oben).
- **Größen** sind gerundet in GB (1 GB = 1.024³ Byte, wie im Explorer). „Möglicher Platzgewinn“ ist immer eine **rechnerische Obergrenze**.
- **Pfade** sind gekürzt wie im Leitfaden: `D:\Ordner\…\Unterordner` — die drei Punkte stehen für ausgelassene Zwischenordner. So finden Sie den Ordner wieder, ohne dass hier vollständige Privatpfade stehen.
- Es wurden **nur Dateien ab etwa 25 MB** geprüft — meist Videos. Kleinere Fotos (oft nur wenige MB) wurden nicht verglichen.
- Zahlen verschiedener Situationen dürfen **nicht addiert** werden — dieselbe Datei kann in mehreren Situationen vorkommen.

---

## 3. Die großen Spuren — 17 Situationen mit der größten Wirkung

> Reihenfolge nach geprüfter Datenmenge (logische Bytes). Alle Zahlen beruhen auf dem Prüfprotokoll `data/hashes/duplicate-candidate-hashes.csv.gz` und der Übersicht `data/hashes/folder-overlap-summary.csv`.

### Situation 1: Handy-Videos und OneDrive-Sicherung — die größte Doppelung (rund 25 GB)

**Betroffene Dateien:** 134 Dateien, insgesamt ~24,9 GB
**Betroffene Laufwerke:** D: und D: (zwei Ordner auf derselben Platte)

**Was ist das?**
Handy-Videos aus 2024 bis Anfang 2026, erkennbar an Namen wie `VID_20250214_154505.mp4`, `VID_20250506_155438.mp4`, `VID_20250616_083352.mp4`. Etwa die Hälfte der zwanzig größten Duplikate des ganzen PCs gehört hierher.

**Wo liegen die Kopien?**

- `D:\2026 vom Handy gesichert\Camera` — ~24,9 GB (134 von 269 großen Dateien dieses Ordners)
- `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien\Eigene Aufnahmen` — ~24,9 GB (134 von 197 großen Dateien)

**Wie ist das vermutlich passiert?**

- **2024–2026 — Videos wurden mit dem Handy aufgenommen und landeten im Ordner „2026 vom Handy gesichert\Camera“.** *Sicher.* Evidence: Ordnername „vom Handy gesichert“, Dateinamen `VID_…` mit Datumsstempel, Änderungsdaten der Camera-Kopien verteilen sich natürlich über August 2024 bis Februar 2026 — genau wie Aufnahmezeiten.
- **25.–26. Februar 2026 — derselbe Bestand wurde in „OneDrive Backup 2026 Februar\…\Eigene Aufnahmen“ abgelegt.** *Wahrscheinlich.* Evidence: 122 der 134 OneDrive-Kopien tragen exakt das Datum **2026-02-25**, weitere 12 den **2026-02-26**; die Camera-Originale tragen dagegen ihre jeweiligen Aufnahmedaten. Eine solche Tages-Bündelung ist typisch für eine Sicherungs- oder Synchronisierungs-Aktion an ein oder zwei Tagen. Der Ordnername „OneDrive Backup 2026 Februar“ nennt den Vorgang selbst.
- **Eine Kopie stammt von der anderen, nicht zwei unabhängige Aufnahmen.** *Sicher.* Evidence: SHA-256 identisch, Byte für Byte — kein zweimaliges Filmen, keine Bearbeitung.

**Welche Kopie ist das Original?**
Der Ordner `D:\2026 vom Handy gesichert\Camera` wirkt wie die **direkte Handy-Ablage** — die Daten verteilen sich über viele Monate, wie bei einem laufenden Import. Der OneDrive-Ordner wirkt wie die **spätere Zweitablage**. *Wahrscheinlich.*

**Welche Kopien sind „Unfälle“?**
Keine ist ein Fehler im technischen Sinn — vermutlich wollten Sie Ihre Handy-Videos **sichern**. Dass nun auf derselben Platte D: zwei vollständige Ablagen liegen, ist eher die unbeabsichtigte Folge: einmal direkt vom Handy, einmal über OneDrive. *Wahrscheinlich.*

**Empfehlung für die Durchsicht:**
Wenn Ihnen eine Haupt-Ablage lieber ist, ist `D:\2026 vom Handy gesichert\Camera` vermutlich die natürlichere — sie enthält zusätzlich 131 große Dateien, die es im OneDrive-Ordner **nicht** gibt, während umgekehrt nur 6 große Dateien im OneDrive-Ordner einzigartig sind (jeweils im ≥25-MB-Prüfbereich). Schauen Sie, ob Sie den OneDrive-Ordner als „Sicherung vom Februar 2026“ wiedererkennen.

---

### Situation 2: Altes Fotoarchiv auf E: — dieselbe Sammlung in zwei Zweigen (rund 23 GB)

**Betroffene Dateien:** 132 + 62 Dateien, zusammen ~23,0 GB (zwei Paare, die zusammengehören)
**Betroffene Laufwerke:** E: und E: (beide im selben Archiv `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv`)

**Was ist das?**
Alte Fotos und Videos, überwiegend 2010–2016 (`100_2436.MOV`, `Butterfly.Effect.DC.German.AC3D.HDRip.x264-FuN.mp4`, `20160101_000639.mp4`, `.thumbdata3--1967290299`). Viele Ordnernamen tragen Jahreszahlen, „Diverses“, „Fotos von anno dazumal bis 2016“, „ICH“.

**Wo liegen die Kopien?**

- Zweig A „Fotos_Archiv“:
  - `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\…\Fotos_Archiv\Fotos\Diverses\Fotos von anno dazumal bis 2016` ↔
  - `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\Tanjas Ordner 2014_2015_2016\Fotos` — 132 Dateien, ~14,8 GB, **jede große Datei der einen Seite hat einen Zwilling auf der anderen** (*Sicher* — 132 von 132).
- Zweig B „Diverses“:
  - `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\…\Fotos_Archiv\Fotos\Diverses` ↔
  - `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\Tanjas Ordner 2014_2015_2016` — 62 Dateien, ~8,2 GB.

Beide Zweige sind ähnlich groß (rund 71 GB bzw. 57 GB, je ~20.000 Dateien im Vollbestand).

**Wie ist das vermutlich passiert?**

- **2010–2016 — Sammlung wuchs auf D:** *Vermutung.* Evidence: Fotos/Videos tragen Daten von 2010–2016, Ordnernamen wie „Tanjas Ordner 2014_2015_2016“ deuten auf zeitliche Sortierung. Direkter Beweis auf D: liegt nicht mehr im Prüfbereich — E: heißt aber „BACKUP lahme Platte (D)“.
- **Später — D: wurde nach E: gesichert, dabei entstanden innerhalb von E: zwei parallele Abbilder desselben Bestands.** *Wahrscheinlich.* Evidence: Beide Kopien liegen **innerhalb desselben E:-Archivs**, tragen **identische Änderungsdaten** (z. B. 2014-07-28 identisch auf beiden Seiten; bei anderen Dateien exakt 1 Stunde Unterschied — typisch für Sommer-/Winterzeit beim Kopieren zwischen Dateisystemen, nicht für neues Fotografieren). Dass *jede* geprüfte große Datei beidseitig vorhanden ist, spricht für einen Ordner-weise Kopiervorgang, nicht für zufälliges Doppel-Speichern.
- **Umsortierung oder „Sicherung der Sicherung“ führte zur Verdopplung.** *Vermutung.* Evidence: Namen „Fotos_Archiv“ und „Tanjas Ordner 2014_2015_2016“ sehen nach zwei Ordnungsversuchen derselben Zeit aus.

**Welche Kopie ist das Original?**
Keine ist eindeutig das Original — beide liegen auf E:, beide tragen die alten Aufnahme-/Bearbeitungsdaten. Der ursprünglichere Ort lag vermutlich **früher auf D:** und ist heute nur noch als diese beiden E:-Abbilder vorhanden. *Vermutung.*

**Welche Kopien sind „Unfälle“?**
Die Zweiteilung innerhalb von E: wirkt wie ein **organisatorischer Unfall**: dieselbe alte Sammlung wurde in zwei Strukturen abgelegt und dann beide Strukturen mitgesichert. *Wahrscheinlich.*

**Empfehlung für die Durchsicht:**
Schauen Sie, ob Ihnen „Fotos_Archiv“ vs. „Tanjas Ordner 2014_2015_2016“ als zwei Sortierversuche bekannt vorkommt. Wenn Sie einen Zweig als Haupt-Ablage wählen, ist der andere — zumindest für die geprüften großen Dateien — eine vollständige Zweitkopie. Weil **beide Kopien auf derselben Platte E:** liegen, schützt die zweite Kopie nicht vor Plattendefekt — eine Kopie auf einem anderen Gerät wäre wichtiger als die Wahl zwischen den beiden E:-Zweigen.

---

### Situation 3: „VW Zeit 1.11.2015–11.11.2016“ — Kopie im eigenen Unterordner (rund 5,0 GB)

**Betroffene Dateien:** 16 Dateien, ~5,0 GB
**Betroffene Laufwerke:** E: und E: (verschachtelt)

**Was ist das?**
16 Videos aus der VW-Zeit (`MVI_1386.MOV`, `MVI_1375.MOV`, `MVI_1389.MOV` u. a.), alle aus dem Ordner „VW Zeit 1.11.2015-11.11.2016“.

**Wo liegen die Kopien?**

- Äußerer Ordner: `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\…\Fotos\2015\VW Zeit 1.11.2015-11.11.2016` — 16 von 32 großen Dateien
- Innerer Ordner (liegt **darin**): `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\…\VW Zeit 1.11.2015-11.11.2016\Newsletter Markenvertreter` — 16 von 16 großen Dateien

**Wie ist das vermutlich passiert?**

- **2015–2016 — Videos entstanden und wurden in „VW Zeit …“ gesammelt.** *Wahrscheinlich.* Evidence: Ordnername mit Datumsbereich, Videonamen `MVI_…`.
- **Später — ein Unterordner „Newsletter Markenvertreter“ wurde angelegt und 16 Videos dorthin (nochmals) hineinkopiert, während die Originale oben liegen blieben.** *Wahrscheinlich.* Evidence: **Verschachtelung** (innerer Pfad liegt physisch im äußeren), **identische Änderungsdaten** bis auf die Sekunde (z. B. 2016-06-03T06:55:54Z beidseitig), und die Abdeckung: *alle* großen Dateien des inneren Ordners sind auch oben vorhanden, aber nur die Hälfte der äußeren Dateien ist innen — typisch für „Teilmenge für Newsletter herauskopiert“.
- *Vermutung zur Absicht:* Für einen Newsletter wurden ausgewählte Videos in einen eigenen Unterordner kopiert — die Kopie im Unterordner ist also eine **Zweck-Kopie**.

**Welche Kopie ist das Original?**
Der **äußere Ordner** ist vermutlich das Original-Sammelbecken. *Wahrscheinlich.*

**Welche Kopien sind „Unfälle“?**
Der innere Ordner wirkt wie eine **bewusste, aber später vergessene Zweitablage** — kein technischer Fehler, aber eine Doppelung, die nach Newsletter-Versand hätte aufgelöst werden können.

**Empfehlung für die Durchsicht:**
Wenn Sie den Newsletter-Kontext wiedererkennen, ist der äußere „VW Zeit“-Ordner die vollständigere Ablage. Der innere „Newsletter Markenvertreter“ enthält nur die 16 ausgewählten Videos.

---

### Situation 4: „ALLE“-Sammelordner — dieselben Videos in drei parallelen „ALLE“-Ordnern (je ~4,7 GB)

**Betroffene Dateien:** 43 Dateien, je Paar ~4,7 GB; insgesamt 9 Dateien zusätzlich in zwei „Spanien Präs“-Ordnern (~1,1 GB)
**Betroffene Laufwerke:** E: und E:

**Was ist das?**
43 alte Videos (`100_2428.MOV`, `Anka Mediator.MOV`, `100_2405.MOV` u. a.). Einzelne Dateien dieser Familie existieren **fünf-, sieben- und in einem Fall zehnmal** auf dem PC — die Datei `flecky 29.08..MOV` / `100_1764.MOV` (112.744.282 Byte) liegt neunmal auf E: und einmal auf D:. Weitere Dateien wie `100_3151.MOV`, `100_3122.MOV` liegen sieben- bis neunmal vor.

**Wo liegen die Kopien?**

- `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\Fotos_Archiv\ALLE_archiv` — 43 Dateien
- `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\…\Diverses\Fotos von anno dazumal bis 2016\ALLE` — 43 Dateien
- `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\…\Tanjas Ordner 2014_2015_2016\Fotos\ALLE` — 43 Dateien

Jeweils paarweise **43 von 43** großen Dateien identisch. Zwei der drei „ALLE“-Ordner gehören zum Zweig „Fotos_Archiv“, einer zum Zweig „Tanjas Ordner 2014_2015_2016“ (Situation 2).

Zusätzlich: `…\Spanien Präs` in denselben beiden Zweigen (je 9 Dateien, ~1,1 GB, z. B. `100_3151.MOV`) enthält 9 der 43 „ALLE“-Videos nochmals — teils sogar **im USB-Unterordner** noch einmal.

**Wie ist das vermutlich passiert?**

- **Um 2010–2012 — „ALLE“ als Sammelordner „alle Fotos an einem Ort“ angelegt.** *Wahrscheinlich.* Evidence: Name „ALLE“/„ALLE_archiv“ deutet auf Sammelabsicht; Dateinamen `100_…MOV` sind Kamera-Standardnamen, Daten um 2010–2011.
- **Im Lauf der Jahre — „ALLE“ wurde bei jeder größeren Sicherung/Umsortierung mitkopiert, ohne die alte „ALLE“-Ablage zu ersetzen.** *Wahrscheinlich.* Evidence: Drei parallele „ALLE“-Ordner mit **43 von 43** Übereinstimmung und **nahezu identischen Änderungsdaten** (z. B. 2010-12-09T11:41:14Z vs. 12:41:14Z — 1 Stunde Versatz). „Spanien Präs“ als thematischer Unterordner wurde offenbar ebenfalls in beide Zweige kopiert.
- **Extreme Mehrfachablage (10 Kopien) entstand durch Kombination: D: → E: Sicherung plus interne E:-Verdopplung.** *Wahrscheinlich.* Evidence: Die 10-fache Datei liegt einmal auf `D:\BACKUP große Platte (F)\Tanjas Ordner 2019- Ende 2023\flecky 29.08..MOV` und neunmal verteilt über E: (`ALLE`, `Booker`, `Flecky`, `Dateien 2014 Archiv`). Mtimes identisch (2010-08-29).

**Welche Kopie ist das Original?**
Vermutlich `…\Fotos_Archiv\ALLE_archiv` — er trägt die **älteste** Zeit der drei (11:41 vs. 12:41 Uhr) und liegt im „Fotos_Archiv“-Zweig, der in Situation 2 als älterer Archiv-Zweig wirkt. *Vermutung.*

**Welche Kopien sind „Unfälle“?**
Die beiden anderen „ALLE“-Ordner sehen nach **mitgewanderten Kopien** aus. „ALLE“ als Sammelordner war vermutlich einmal sinnvoll; dass er heute **dreifach** existiert, ist eher unbeabsichtigt.

**Empfehlung für die Durchsicht:**
Entscheiden Sie, welchen „ALLE“-Ort Sie als Sammelort behalten möchten — inhaltlich sind die drei für die geprüften großen Videos **austauschbar**. Die Entscheidung hängt mit Situation 2 zusammen: Wer dort einen Zweig wählt, hat einen Teil dieser Frage schon beantwortet.

---

### Situation 5: Das Hochzeitsvideo — eine Datei, vier Kopien (je ~2,2 GB)

**Betroffene Dateien:** 1 Datei (`Hochzeit_T&D.mov`, 2.328.950.450 Byte), 4 Kopien
**Betroffene Laufwerke:** D: und D:

**Was ist das?**
Das Hochzeitsvideo vom 18.06.2024 — die größte einzelne Datei mit Duplikaten im ganzen Bestand.

**Wo liegen die Kopien?**

1. `D:\BACKUP große Platte (F)\HOCHZEIT 18.06.2024` — mtime 2024-06-28
2. `D:\BACKUP große Platte (F)\HOCHZEIT 18.06.2024\Hochzeitsvideo` (Unterordner von 1) — mtime 2024-06-28
3. `D:\Downloads` — mtime 2026-02-23
4. `D:\OneDrive Backup 2026 Februar\TanjaDirk - Geteilt` — mtime 2026-02-23

Alle vier sind byte-identisch (SHA-256 `b6c88…`).

**Wie ist das vermutlich passiert?**

- **Juni 2024 — Video erhalten/erstellt und in den Hochzeits-Ordner einsortiert; zusätzlich im Unterordner „Hochzeitsvideo“ abgelegt.** *Wahrscheinlich.* Evidence: Zwei BACKUP-Kopien tragen **identisches altes Datum** 2024-06-28, eine liegt **verschachtelt** im Unterordner der anderen — typisch „habe die Datei noch in den passenden Unterordner kopiert, Original oben vergessen“.
- **23. Februar 2026 — erneut heruntergeladen/bereitgestellt (Downloads) und über OneDrive geteilt.** *Wahrscheinlich.* Evidence: Downloads- und OneDrive-Kopien tragen **identisches neues Datum** 2026-02-23T18:11:25Z, exakt den gleichen Tag wie viele andere OneDrive-Kopien (Situation 1, 6, 11). Ordnername „Geteilt“ deutet auf Teilen über OneDrive.
- Zwischen 2024 und 2026 lag die Datei also bereits im BACKUP — Downloads ist **nicht** die erste Quelle. *Wahrscheinlich.*

**Welche Kopie ist das Original?**
Der Ordner `D:\BACKUP große Platte (F)\HOCHZEIT 18.06.2024` wirkt wie die **erste sortierte Ablage**. *Wahrscheinlich.*

**Welche Kopien sind „Unfälle“?**
Der Unterordner „Hochzeitsvideo“ ist eine **verschachtelte Doppelung** (Ordner in Ordner), `Downloads` ist typisch eine **vergessene Download-Kopie**, „Geteilt“ die **geteilte Kopie**. Keine ist technisch „falsch“, aber alle drei zusätzlich zur Hauptablage sind vermutlich unbeabsichtigt liegen geblieben.

**Empfehlung für die Durchsicht:**
Prüfen Sie, ob Sie das Video bewusst in Downloads und in „Geteilt“ behalten wollten (z. B. zum Weitergeben). Für die reine Aufbewahrung reicht **eine** der vier Kopien — die beiden von 2024 tragen das ältere, vermutlich ursprünglichere Datum.

---

### Situation 6: Lose Dateien oben in „BACKUP große Platte (F)“ und ihre Zwillinge (rund 7,5 GB)

**Betroffene Dateien:** 21 Dateien (~3,1 GB) + BINGO-Sendung 25.12.2023 (3 Kopien, ~1,3 GB) + TV-Mitschnitt 15.03.2026 (3 Kopien, ~1,45 GB, teils umbenannt)
**Betroffene Laufwerke:** D: und D:

**Was ist das?**
Eine Mischung: Private Videos (`VID_20250704_122253.mp4`, `20250705_204239.mp4`) sowie zwei Fernsehmitschnitte der BINGO-Sendung.

**Wo liegen die Kopien?**

- Lose/oberste Ebene `D:\BACKUP große Platte (F)` (teils direkt, teils in gleichnamigen Unterordnern) ↔ `D:\OneDrive Backup 2026 Februar\TanjaDirk - Geteilt` — 21 Dateien, ~3,1 GB.
- **BINGO 25.12.2023:** `D:\BACKUP große Platte (F)\BINGO__-…mp4` (lose) + `D:\BACKUP große Platte (F)\BINGO Sendung 25.12.2023\BINGO__-…mp4` + `D:\OneDrive Backup 2026 Februar\TanjaDirk - Geteilt\BINGO Sendung 25.12.2023\BINGO__-…mp4` — je ~1,3 GB, mtimes 2025-10-17 vs. 2026-02-23.
- **TV 15.03.2026:** `D:\BACKUP große Platte (F)\TV-20260315-1659-3511.1080.mp4` ↔ `D:\BACKUP große Platte (F)\TanjaDirkBingoMärz2026.mp4` (umbenannt!) ↔ `D:\BACKUP große Platte (F)\Fotos ab 2020\…\2026\Xiaomi 13T Pro\Diverse Fotos\TV-20260315-1659-3511.1080.mp4` — je ~1,45 GB, mtimes 2026-03-19/21.

**Wie ist das vermutlich passiert?**

- **Herbst 2025–Frühjahr 2026 — Mitschnitte wurden erst lose oben in BACKUP abgelegt, dann in einen benannten Unterordner sortiert — dabei blieb die lose Kopie liegen.** *Wahrscheinlich.* Evidence: Bei BINGO liegt eine Kopie **lose direkt in** `D:\BACKUP große Platte (F)` und eine **im Unterordner** mit gleichem Namen, beide mit identischem Datum 2025-10-17T13:32:29Z — typisch „in Ordner verschoben/kopiert, Original oben vergessen“. Bei März-2026 liegt sogar eine **umbenannte** Kopie (`TanjaDirkBingoMärz2026.mp4`) mit fast gleichem Datum daneben — SHA-256 beweist trotz anderem Namen identische Bytes.
- **23. Februar 2026 — OneDrive-Backup-Tag legte die geteilte Kopie an.** *Wahrscheinlich.* Evidence: OneDrive-Kopie trägt wieder 2026-02-23, wie in Situation 1 und 5.
- **März 2026 — der TV-Mitschnitt wurde zusätzlich in den neuen Handy-Ordner „Xiaomi 13T Pro\Diverse Fotos“ kopiert.** *Wahrscheinlich.* Evidence: Dritter Pfad liegt tief in `…\2026\Xiaomi 13T Pro\Diverse Fotos`, mtime 2026-03-19 — ein damals aktueller Handy-Import-Ordner.

**Welche Kopie ist das Original?**
Für BINGO: die **benannte Unterordner-Ablage** wirkt am ordentlichsten; die lose Kopie oben in BACKUP sieht nach Vorstufe aus. Für die 21 privaten Videos: schwer zu sagen — Name und Datum sind gleich. *Vermutung.*

**Welche Kopien sind „Unfälle“?**
Lose Dateien auf der obersten BACKUP-Ebene sind oft **Zwischenablagen** beim Sortieren. Dass sie später noch einmal als benannte Ordner und noch einmal über OneDrive vorliegen, ist typisch für „erst schnell ablegen, dann ordentlich sortieren, dann teilen — und nichts aufräumen“.

**Empfehlung für die Durchsicht:**
Schauen Sie, ob Ihnen die losen Dateien oben in „BACKUP große Platte (F)“ als „noch nicht einsortiert“ bekannt vorkommen. Die benannten Unterordner und die OneDrive-Geteilt-Ablage sind meist die besseren Haupt-Ablagen.

---

### Situation 7: „Camera Stand 21.9.23“ und „Videos 2023“ — Aussortierte Videosammlung (rund 2,2 GB)

**Betroffene Dateien:** 20 Dateien, ~2,2 GB
**Betroffene Laufwerke:** D: und D:

**Was ist das?**
20 Videos aus Sommer 2023 (`VID_20230723_113841.mp4`, `VID_20230831_101951.mp4` u. a.).

**Wo liegen die Kopien?**

- `D:\BACKUP große Platte (F)\Fotos ab 2020\Camera Stand 21.9.23` — 20 von 21 großen Dateien
- `D:\BACKUP große Platte (F)\Videos 2023` — 20 von 20 großen Dateien

**Wie ist das vermutlich passiert?**

- **Sommer 2023 — Videos aufgenommen (vermutlich Handy/Kamera).** *Wahrscheinlich.* Evidence: Dateinamen mit Datum Juli/August 2023.
- **21. September 2023 — Stand „Camera Stand 21.9.23“ als Sammelordner angelegt.** *Wahrscheinlich.* Evidence: Ordnername trägt exakt das Datum 21.9.23, Änderungsdaten beider Ordner-Enden **identisch** 2022-12-01T16:05:22Z bis 16:25:40Z — Kopiervorgang an einem Tag mit Erhalt der Daten.
- **Danach — 20 Videos wurde zusätzlich in „Videos 2023“ sortiert, blieb aber auch im Camera-Ordner.** *Wahrscheinlich.* Evidence: **Vollständige Überschneidung** — alle 20 großen Dateien von „Videos 2023“ sind auch in „Camera Stand…“ vorhanden; „Camera Stand…“ hat nur eine zusätzliche große Datei.

**Welche Kopie ist das Original?**
`…\Camera Stand 21.9.23` wirkt wie die **Sammelablage direkt vom Gerät**, `Videos 2023` wie die **thematische Sortierung** danach. *Wahrscheinlich.*

**Welche Kopien sind „Unfälle“?**
Nicht unbedingt Unfall — eher **Doppel-Sortierung**: einmal nach Quelle (Camera), einmal nach Jahr. Dass beide auf D: bleiben, ist eine bewusste oder vergessene Doppelung.

**Empfehlung für die Durchsicht:**
Wenn Sie nach Jahr sortieren („Videos 2023“), ist das der thematische Hauptort. Wenn Sie nach Gerät/Import sortieren, ist „Camera Stand…“ der Hauptort.

---

### Situation 8: Kaninchenvideos quer über zwei Platten — D: und E: gleichzeitig (rund 3,5 GB)

**Betroffene Dateien:** 24 + 7 + 8 Dateien, zusammen ~3,5 GB
**Betroffene Laufwerke:** D: und E: (kreuzweise)

**Was ist das?**
39 Kaninchen-Videos 2015/2016 und 2020 (`20151206_145527.mp4`, `20160306_185259.mp4`, `VID_20200508_090942.mp4` u. a.), u. a. „Lotti und Merlin 17. November 2014“.

**Wo liegen die Kopien?**

- `D:\BACKUP große Platte (F)\Meine Kaninchen\…\Mein tolles Trio\Lotti und Merlin 17. November 2014\Nins` ↔ `E:\BACKUP lahme Platte (D)\Kaninchenvideos` — 24 Dateien, ~1,8 GB, mtimes identisch (z. B. 2018-03-24).
- `D:\BACKUP große Platte (F)\Meine Kaninchen\2020\Kaninchenliebe 🐰❤ Stand Juni 2020` ↔ `E:\BACKUP lahme Platte (D)\Kaninchenvideos` — 7 Dateien, ~0,9 GB, mtimes identisch 2020-05-08 / 2020-05-25.
- `D:\BACKUP große Platte (F)\Meine Kaninchen\…\Tierarzt Feb 2016` ↔ `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\…\Diverses\Handyfotos 2015 2016\Camera` **und** ↔ `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\…\Tanjas Ordner 2014_2015_2016\Handyfotos 2015 2016\Camera` — 8 Dateien, ~0,9 GB, auf E: **in beiden Archiv-Zweigen** (Situation 2).

**Wie ist das vermutlich passiert?**

- **2015–2020 — Kaninchenvideos wuchsen in „Meine Kaninchen“ auf D:.** *Wahrscheinlich.* Evidence: Ordnerstruktur „Meine Kaninchen“ ist tief und thematisch (Nins, Tierarzt, 2020), mtimes passen zu Aufnahmejahren.
- **Separat — auf E: wurde ein Sammelordner „Kaninchenvideos“ gepflegt.** *Wahrscheinlich.* Evidence: Ordnername „Kaninchenvideos“ auf E: ist flach und sammelnd, enthält Videos aus mehreren D:-Unterordnern gebündelt.
- **Beim Sichern D:→E: (oder teils E:→D:) wurden die Kaninchenvideos abgeglichen — dabei landeten sie auf beiden Platten.** *Wahrscheinlich.* Evidence: **Kreuz-Laufwerk** D:+E:, **identische mtimes** (2015–2020er Daten identisch beidseitig), SHA-256 identisch. Dass die Tierarzt-Videos auf E: **in beiden Archiv-Zweigen** liegen, zeigt die E:-interne Verdopplung aus Situation 2 wirkt auch hier.
- *Vermutung:* E: diente zeitweise als **Kaninchen-Archiv**, D: als Arbeitsplatte — beim Hin- und Herkopieren entstanden beidseitige Kopien.

**Welche Kopie ist das Original?**
Für die meisten: **D: „Meine Kaninchen“** ist thematisch tiefer sortiert und wirkt wie das Original-Arbeitsverzeichnis; `E:\Kaninchenvideos` wirkt wie die Zusammenfassung. *Wahrscheinlich, aber nicht sicher.*

**Welche Kopien sind „Unfälle“?**
Weniger Unfall als bei rein internen Doppelungen — **zwei Geräte zu haben ist grundsätzlich gut**. Dass zusätzlich die E:-interne Verdopplung (beide Archiv-Zweige) dieselben 8 Videos nochmals enthält, ist dagegen ein E:-interner Unfall.

**Empfehlung für die Durchsicht:**
Weil hier **zwei verschiedene Platten** betroffen sind, schützt die zweite Kopie bei Plattendefekt — „Beides behalten“ ist hier besonders gut vertretbar und die sicherste Wahl, bis die externe Festplatte geprüft ist. Wenn Sie reduzieren möchten, achten Sie darauf, dass Sie **mindestens eine Platte als Haupt-Ablage** vollständig behalten.

---

### Situation 9: London September 2022 — Fotos-Ordner und Videos-Ordner nebeneinander (rund 1,5 GB)

**Betroffene Dateien:** 29 Dateien, ~1,5 GB
**Betroffene Laufwerke:** D: und D:

**Was ist das?**
29 London-Videos September 2022 (`VID_20220925_105721.mp4`, `VID_20220923_122856.mp4` u. a.).

**Wo liegen die Kopien?**

- `D:\BACKUP große Platte (F)\ENGLAND Reisen\1_ Sept_2022 1. Reise nach London\London Fotos Tanja`
- `D:\BACKUP große Platte (F)\ENGLAND Reisen\1_ Sept_2022 1. Reise nach London\London Videos`

Alle 29 großen Dateien des Videos-Ordners sind auch im Foto-Ordner vorhanden.

**Wie ist das vermutlich passiert?**

- **September 2022 — London-Reise aufgenommen.** *Sicher.* Evidence: Ordnernamen tragen Reise-Datum, mtimes passen.
- **Danach — Videos wurden aus dem Foto-Ordner in einen eigenen Videos-Ordner sortiert, blieben aber auch im Foto-Ordner liegen.** *Wahrscheinlich.* Evidence: Direkt **benachbarte Ordner** im selben Reise-Verzeichnis, identische Dateinamen, vollständige Überschneidung wie bei Situation 7 — typisch „nach Medientyp trennen, Original nicht gelöscht“.

**Welche Kopie ist das Original?**
Der **Foto-Ordner** wirkt wie die erste Ablage (er enthält Fotos plus Videos), der **Videos-Ordner** wie die spätere reine Videos-Ablage. *Vermutung.*

**Welche Kopien sind „Unfälle“?**
Eher **Sortier-Doppelung** — kein Fehler, aber unnötig doppelt.

**Empfehlung für die Durchsicht:**
Wenn Sie Fotos und Videos getrennt mögen, behalten Sie den Videos-Ordner als Videos-Hauptort und wissen, dass im Foto-Ordner dieselben Videos noch einmal liegen.

---

### Situation 10: KATE ANTONIA — dieselben Videos in bis zu vier Ablagen (rund 5 GB verteilt)

**Betroffene Dateien:** ~60 verschiedene Videos 2024–2026 (`VID_20251024_160041.mp4`, `VID_20250826_074728.mp4`, `VID_20241231_233002.mp4` u. a.), verteilt auf viele Paare
**Betroffene Laufwerke:** D: und D:

**Was ist das?**
Familienvideos von Kate Antonia (2024–2026), systematisch in Personen-Ordner, Jahresordner und OneDrive.

**Wo liegen die Kopien? (Auswahl der größten Paare)**

- `D:\BACKUP große Platte (F)\1. KATE ANTONIA` ↔ `D:\BACKUP große Platte (F)\Fotos ab 2020` — 19 Dateien, ~1,5 GB
- `D:\2026 vom Handy gesichert` ↔ `D:\BACKUP große Platte (F)\1. KATE ANTONIA\2026` — 4 Dateien, ~1,2 GB
- `D:\BACKUP große Platte (F)\Fotos ab 2020` ↔ `D:\OneDrive Backup 2026 Februar\TanjaDirk - Geteilt\Kate Antonia` — 13 Dateien, ~1,0 GB
- `D:\BACKUP große Platte (F)\Fotos ab 2020\2024\16. Silvester 2024_2025` ↔ `D:\OneDrive Backup 2026 Februar\TanjaDirk - Geteilt\Kate Antonia` — 8 Dateien, ~0,9 GB
- dazu weitere Paare: Handy↔Fotos ab 2020, Handy↔KATE ANTONIA\2025, KATE ANTONIA↔OneDrive, usw.

Ordnernamen wie „Kates 1. Geburtstag“, „Oktober 24“, „Spielplatz“, „Halloween 2025“ zeigen die gleiche feine Sortierung in allen vier Ablagen.

**Wie ist das vermutlich passiert?**

- **2024–2026 — Videos laufend aufgenommen.** *Sicher.* Evidence: Dateinamen tragen Datumsstempel 2024–2026, mtimes passen (z. B. 2025-08-26T05:50:10Z beidseitig).
- **Parallel — dieselben Videos wurden in den Personen-Ordner `1. KATE ANTONIA`, in die Jahresordner `Fotos ab 2020\2025` bzw. `\2024`, in die Handy-Sicherung `2026 vom Handy gesichert` und in die OneDrive-Freigabe übernommen.** *Wahrscheinlich.* Evidence: **Vier parallele Benennungen** für denselben Tag (z. B. 2025-10-24 Video erscheint in `Handy\…`, `1. KATE ANTONIA\2025`, `Fotos ab 2020\2025`, `OneDrive\…Eigene Aufnahmen` mit teils identischen, teils OneDrive-typischen mtimes 2026-02-25). Ordnernamen „1. KATE ANTONIA“ deutet auf bewusstes Sortieren nach Person.
- **Teils echte Duplikate, teils gewollte Doppel-Sortierung.** *Vermutung.* Evidence: Viele Paare haben **identische mtimes** (2025-06-30T08:59:11Z beidseitig), einige OneDrive-Kopien tragen wieder 2026-02-25 — Hinweis auf späteren Backup-Schritt.

**Welche Kopie ist das Original?**
Schwer zu sagen — wahrscheinlich ist **`D:\2026 vom Handy gesichert`** der **erste Import**, `1. KATE ANTONIA` die **bewusste Personen-Sortierung**. *Vermutung.*

**Welche Kopien sind „Unfälle“?**
Kaum Unfall — eher **Mehrfach-Sortierung nach verschiedenen Logiken** (nach Person, nach Jahr, nach Gerät, nach Freigabe). Dass alles auf **derselben Platte D:** liegt, macht es unübersichtlich, aber nicht automatisch falsch.

**Empfehlung für die Durchsicht:**
Überlegen Sie, nach welcher Logik Sie Kate-Antonia-Videos künftig finden wollen: nach **Person** (`1. KATE ANTONIA`) oder nach **Jahr** (`Fotos ab 2020\2025`). Die OneDrive-Kopie ist — wie in Situation 1 — vermutlich die **Februar-2026-Sicherung** und wirkt am ehesten als Zweitablage.

---

### Situation 11: Mallorca 14.–22. Mai 2024 — Urlaub in drei Ablagen (rund 4 GB)

**Betroffene Dateien:** 17 Urlaubsvideos (~1,5 GB) + 4 Videos vom 22.5.2024 (~1,1 GB) + viele Fotos im selben Urlaubsverbund (nicht in der 25-MB-Prüfung, aber als Pfade sichtbar)
**Betroffene Laufwerke:** D: und D:

**Was ist das?**
Mallorca-Urlaub Mai 2024 (`VID_20240517_221813.mp4`, `VID_20240520_213531.mp4` u. a., Panos vom 15.5., 18.5.).

**Wo liegen die Kopien?**

- `D:\BACKUP große Platte (F)\Fotos ab 2020\2024\9. Mallorca 14.5.-22.5.2024` (mit Unterordner `Videos Malle 24`)
- `D:\OneDrive Backup 2026 Februar\TanjaDirk - Geteilt\Mallorca 14.5.-22.5.24` (mit gleichem Unterordner `Videos Malle 24`)
- `D:\BACKUP große Platte (F)\Xiaomi Redmi Note 8 GALERIE Stand 08.2024\DCIM\Camera` (und Nachbarordner `…\22.5.24`, `…\Malle 15.5.24`, `…\Pictures`, `…\ROSSMANN\Schon erledigt`)

Beispiel: `VID_20240522_121808.mp4` liegt in `Xiaomi …\22.5.24` und `…\DCIM\Camera` identisch; `PANO_20240515_114710.jpg` liegt in vier Varianten des Urlaubs- und Galerie-Baums mit identischen Daten 2024-05-15.

**Wie ist das vermutlich passiert?**

- **Mai 2024 — Urlaub aufgenommen.** *Sicher.*
- **Mai/Juni 2024 — Galerie-Sicherung „Xiaomi Redmi Note 8 GALERIE Stand 08.2024“ angelegt (DCIM\Camera + sortierte Tagesordner 15.5., 18.5., 22.5.).** *Wahrscheinlich.* Evidence: Ordnername mit Stand-Datum 08.2024, mtimes der Galerie-Kopien 2024-05-14/15/22, teils 2024-06-06.
- **Mai 2024 — Urlaubsordner `Fotos ab 2020\2024\9. Mallorca…` als sortierte Ablage angelegt (mit Unterordnern 15.05.24, 18.5.24, Videos Malle 24, ROSSMANN).** *Wahrscheinlich.* Evidence: Tief gegliederter Urlaubsordner mit Tages-Unterordnern und „ROSSMANN\Schon erledigt“ — typisch für Fotobuch-/Abzugs-Sortierung. mtimes identisch zu Galerie-Originalen (2024-05-15T09:47:32Z beidseitig).
- **24. Februar 2026 — OneDrive-Backup legte die dritte Kopie in `…\Mallorca 14.5.-22.5.24` an.** *Wahrscheinlich.* Evidence: OneDrive-mtimes **2026-02-24** gebündelt (06:32–06:33 Uhr), wie in Situation 1.

**Welche Kopie ist das Original?**
Die **Handy-Galerie** (`Xiaomi Redmi Note 8 GALERIE …\DCIM\Camera`) wirkt wie der **erste Export vom Gerät**, der **Urlaubsordner** wie die **ordentliche Sortierung**. *Wahrscheinlich.*

**Welche Kopien sind „Unfälle“?**
Die **OneDrive-Kopie** ist vermutlich die **Februar-2026-Zweitablage**. Dass der Urlaub zusätzlich im ROSSMANN-Zweig noch einmal liegt (gleiche Panos in `…\ROSSMANN\Schon erledigt\Teil 3/6`), ist typisch „für Abzüge/Fotobuch herauskopiert und liegen lassen“.

**Empfehlung für die Durchsicht:**
Wenn Sie Urlaub nach Reise sortieren, ist der **Urlaubsordner unter „Fotos ab 2020“** der natürlichste Hauptort. Die Handy-Galerie von 08.2024 ist die ältere Sammelablage, OneDrive die Sicherung.

---

### Situation 12: „Allgemeine Dateien“ und „What is Love“ — gleicher Zeitraum dreifach (rund 2,8 GB)

**Betroffene Dateien:** 23 Dateien, je Paar ~1,35 GB, dreifach vorhanden
**Betroffene Laufwerke:** E: und E:

**Was ist das?**
23 Videos Anfang 2014 (`einfach Gerede.mp4`, `Let it go - …mp4`, `VID_20140319_123104.mp4`), Zeitraum **05.01.14–23.03.2014** — erkennbar an Ordnernamen.

**Wo liegen die Kopien?**

- `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\Tanjas Ordner 2014_2015_2016\Allgemeine Dateien` — 23 Dateien
- dessen Unterordner `…\Allgemeine Dateien\05.01.14-23.03.2014` — 23 Dateien
- `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\What is Love\B_Christopher T.- 05.01.14-23.03.2014` — 23 Dateien

Je **dreifach** vorhanden, mit **1-Stunden-Versatz** (z. B. 2014-01-11T14:24:18Z / 15:24:18Z / 16:24:18Z) — typischer Kopier-Versatz.

**Wie ist das vermutlich passiert?**

- **Jan–März 2014 — Zeitraum entstand.** *Sicher.* Evidence: Ordnernamen tragen exakt den Zeitraum 05.01.14-23.03.2014.
- **Später — derselbe Zeitraum wurde einmal als Unterordner, einmal oben in „Allgemeine Dateien“ und einmal unter „What is Love\B_Christopher T.“ abgelegt.** *Wahrscheinlich.* Evidence: **Dreifache identische Dateiliste** mit nur Stunden-Versatz, Pfade liegen **innerhalb desselben E:-Archivs**, teils **verschachtelt** (Unterordner liegt im äußeren). Namen „What is Love“ und „B_Christopher T.“ deuten auf **thematische/personenbezogene Sortierung** desselben Zeitraums.
- *Vermutung:* „Allgemeine Dateien“ war die erste Sammelablage, „05.01.14-23.03.2014“ die zeitliche Sortierung, „What is Love“ die thematische — alle drei blieben erhalten.

**Welche Kopie ist das Original?**
Schwer zu sagen — die **„Allgemeine Dateien“ (oberer Ordner)** wirkt wie die erste Sammelablage. *Vermutung.*

**Welche Kopien sind „Unfälle“?**
Die beiden anderen sehen nach **Doppel-Sortierung nach Datum und nach Thema** aus — bewusst angelegt, aber später nicht bereinigt.

**Empfehlung für die Durchsicht:**
Wenn Ihnen „What is Love“ als Projekt/Person bekannt ist, ist das der thematische Hauptort; wenn Sie chronologisch sortieren, ist `…\05.01.14-23.03.2014` der Hauptort.

---

### Situation 13: Kaninchen-Ordner auf D: und OneDrive „Tanja - Eigene Dateien“ (rund 3,6 GB verteilt)

**Betroffene Dateien:** 12 + 3 + 6 + 6 Dateien, zusammen ~3,6 GB
**Betroffene Laufwerke:** D: und D:

**Was ist das?**
Kaninchen-Videos (u. a. Frodo 25.3.2017–2.11.2024, M&L 5. und 9. Geburtstag — `VID_20231120_224104.mp4`, `VID_20241027_183957.mp4`).

**Wo liegen die Kopien? (Beispiele)**

- `D:\BACKUP große Platte (F)\Meine Kaninchen` ↔ `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien` — 12 Dateien, ~1,35 GB
- `D:\BACKUP große Platte (F)\Meine Kaninchen\Frodo 25.3.2017-2.11.2024` ↔ `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien\Eigene Aufnahmen` (und ↔ `…\Frodo 25.3.2017-2.11.2024`) — 3 Dateien, dreifach, ~0,6 GB
- „M&L 9. Geburtstag“ — 6 Dateien in **vier** Ablagen: `…\Meine Kaninchen\M&L 9. Geburtstag\Fotos`, `…\M&L 9. Geb\Handy Ordner\M&L 9.Geburtstag`, `…\Xiaomi Redmi Note 8 GALERIE Stand 08.2024\DCIM\M&L 9.Geburtstag`, `D:\OneDrive Backup 2026 Februar\…\M&L 9. Geb\Handy Ordner\M&L 9.Geburtstag` — je ~0,5 GB
- „M&L 5. Geburtstag“ — `…\Meine Kaninchen\…\Kaninchen_2020\M&L 5️⃣Geburtstag` ↔ `…\Tanjas Ordner 2019- Ende 2023\…\Fotos\2_2019\Merlin & Lottis 5. Geburtstag` — 6 Dateien, ~0,6 GB

**Wie ist das vermutlich passiert?**

- **2019–2024 — Kaninchen-Sammlung wuchs in „Meine Kaninchen“ auf D:.** *Wahrscheinlich.* Evidence: Tief gestaffelte Kaninchen-Ordner mit Namen und Daten.
- **Parallel — Handy-Galerie-Sicherung (Xiaomi 08.2024) und OneDrive-Backup (Februar 2026) legten je eine weitere Ablage an.** *Wahrscheinlich.* Evidence: M&L-9.-Geburtstags-Videos liegen **vierfach** mit identischen mtimes, aber auf drei verschiedenen Pfad-Familien (BACKUP, Galerie, OneDrive) — typisch „von Handy importiert → in Kaninchen-Ordner sortiert → Galerie-Sicherung behielt Kopie → OneDrive sicherte im Februar 2026“.
- **Älterer Jahresordner „Tanjas Ordner 2019- Ende 2023“ enthält 5.-Geburtstags-Videos zusätzlich.** *Wahrscheinlich.* Evidence: Gleicher Satz 6 Videos in Jahresordner 2_2019 — früherer Sortierstand.

**Welche Kopie ist das Original?**
`D:\BACKUP große Platte (F)\Meine Kaninchen` wirkt wie die **bewusst gepflegte Haupt-Sammlung**. *Wahrscheinlich.*

**Welche Kopien sind „Unfälle“?**
Die **OneDrive- und Galerie-Kopien** sind vermutlich **mitgewanderte Sicherungen**, der **Jahresordner** ein **älterer Sortierrest**.

**Empfehlung für die Durchsicht:**
Wenn Sie Kaninchen nach Tier/Anlass suchen, ist „Meine Kaninchen“ der natürlichste Hauptort. Die OneDrive-Ablage wirkt — wie in Situation 1 — als Februar-2026-Sicherung.

---

### Situation 14: Reise- und Feier-Ordner auf D: mit Zwilling in der OneDrive-Sicherung (zusammen rund 6 GB)

**Betroffene Dateien:** viele kleine Pakete, zusammen ~6 GB
**Betroffene Laufwerke:** D: und D: (teils E: als dritte Kopie)

**Was ist das?**
Gleiche Muster wie Situation 1, nur für Reisen/Feiern: Silvester, England, Portugal, Schottland, plus WhatsApp-Archiv.

**Wo liegen die Kopien? (Auswahl)**

- `D:\BACKUP große Platte (F)\ENGLAND Reisen\5_Silvester 2023_2024` ↔ `D:\OneDrive Backup 2026 Februar\TanjaDirk - Geteilt\2023_12_Silvester_Tanjas Fotos` — 21 Dateien, ~1,2 GB
- `D:\BACKUP Desktop\Signal Stand 6.8.2024` ↔ `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien` — 16 Dateien, ~0,7 GB
- `D:\BACKUP große Platte (F)\Fotos ab 2020\…\2023\9_Portugal 8.7.-16.7.2023\Fotos` ↔ `D:\OneDrive Backup 2026 Februar\TanjaDirk - Geteilt\Portugal Tanjas Fotos` — 16 Dateien, ~0,6 GB
- `D:\BACKUP große Platte (F)\Fotos ab 2020` ↔ `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien` — 2 Videos 25.05.2024, ~0,6 GB
- `D:\BACKUP große Platte (F)\ENGLAND Reisen\4_SÜDENGLAND 30.9.-7.10.2023` ↔ `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien\Südengland 30.9.-7.10.23` — 9 Dateien, ~0,6 GB
- `D:\BACKUP große Platte (F)\SCHOTTLAND 2025\6.9. Highland Games` ↔ `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien\Eigene Aufnahmen` — 6 Dateien, ~0,5 GB
- WhatsApp-Archiv `WhatsApp Chat - Tanja.zip` (~0,6 GB) **dreifach**: `D:\BACKUP große Platte (F)\WA Chat mit Monique`, `…\Xiaomi Redmi Note 8 GALERIE Stand 08.2024\Dokumente`, `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien\Spaceloop USB Stick`

Einige Südengland-Videos haben zusätzlich eine **dritte Kopie auf E:** in `E:\BACKUP lahme Platte (D)\Selphy Drucker USB\Südengland 2023`.

**Wie ist das vermutlich passiert?**

- **2023–2025 — Reisen/Feiern wurden in thematischen Ordnern auf D: sortiert (ENGLAND, Portugal, Schottland, Silvester).** *Wahrscheinlich.* Evidence: Ordnernamen tragen Reise-/Feier-Daten, mtimes passen zu Reisezeiten (z. B. Silvester 2023/2024).
- **Februar 2026 — OneDrive-Backup legte die Zweitablage in „OneDrive Backup 2026 Februar\…“ an.** *Wahrscheinlich.* Evidence: Durchgehend **OneDrive-mtimes 2026-02-22 bis 2026-02-25**, während BACKUP-mtimes die jeweiligen Reisedaten tragen — gleiches Tages-Bündel wie Situation 1.
- **Signal/WhatsApp-Archive wurden von verschiedenen Quellen (Handy-Galerie, Spaceloop USB, WA Chat) zusammengeführt und dabei mehrfach abgelegt.** *Wahrscheinlich.* Evidence: Zip liegt in drei thematisch verschiedenen Zweigen mit mtimes 2021-11-11 vs. 2024-06-25 vs. 2026-02-22 — drei Zeitpunkte, drei Quellen.

**Welche Kopie ist das Original?**
Die **thematischen Ordner unter „BACKUP große Platte (F)“ bzw. „BACKUP Desktop“** wirken wie die **sortierten Originale**; die OneDrive-Ordner wie die **Sicherung**. *Wahrscheinlich.*

**Welche Kopien sind „Unfälle“?**
Die OneDrive-Zweitablage ist vermutlich die **Februar-2026-Sicherung** — kein Fehler, aber doppelt auf derselben Platte D:.

**Empfehlung für die Durchsicht:**
Wenn Sie Reisen nach Ziel sortieren, sind die Ordner unter „BACKUP große Platte (F)“ die natürlicheren Haupt-Ablagen. Die OneDrive-Ablage ist die Sicherung — prüfen Sie, ob Sie sie als solche wiedererkennen.

---

### Situation 15: WhatsApp- und Signal-Archive — dreifach auf D: (rund 1,8 GB)

**Betroffene Dateien:** 1 Zip (~0,6 GB) dreifach + 16 Signal-Dateien (~0,7 GB)
**Betroffene Laufwerke:** D: und D:

**Was ist das?**
`WhatsApp Chat - Tanja.zip` (613.461.876 Byte) und Signal-Anhänge aus `BACKUP Desktop\Signal Stand 6.8.2024\attachments`.

**Wo liegen die Kopien?**

- WhatsApp Zip: `D:\BACKUP große Platte (F)\WA Chat mit Monique` (2021-11-11) ↔ `D:\BACKUP große Platte (F)\Xiaomi Redmi Note 8 GALERIE Stand 08.2024\Dokumente` (2024-06-25) ↔ `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien\Spaceloop USB Stick` (2026-02-22)
- Signal: `D:\BACKUP Desktop\Signal Stand 6.8.2024` ↔ `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien` — 16 Dateien, ~722 MB

**Wie ist das vermutlich passiert?**

- **2021 — WhatsApp-Chat exportiert nach `WA Chat mit Monique`.** *Wahrscheinlich.* Evidence: Älteste mtime 2021-11-11, Ordnername nennt den Chat-Partner.
- **2024 — beim Anlegen der Handy-Galerie-Sicherung (Stand 08.2024) wanderte der Zip in `…\Dokumente` mit.** *Wahrscheinlich.* Evidence: Pfad `Xiaomi Redmi Note 8 GALERIE Stand 08.2024\Dokumente`, mtime 2024-06-25.
- **2026-02 — OneDrive-Backup sicherte den Stick-Ordner.** *Wahrscheinlich.* Evidence: mtime 2026-02-22, wie andere OneDrive-Kopien.

**Welche Kopie ist das Original?**
`D:\BACKUP große Platte (F)\WA Chat mit Monique` wirkt wie das **erste Export-Ziel**. *Wahrscheinlich.*

**Welche Kopien sind „Unfälle“?**
Die beiden anderen sind **mitgewanderte Sicherungen** des gleichen Exports.

**Empfehlung für die Durchsicht:**
Chat-Archive sind **besonders schützenswert** (nicht reproduzierbar). Bewahren Sie mindestens eine Kopie als „Archiv“ — welche, ist weniger wichtig, aber halten Sie den Zusammenhang zu `Spaceloop USB Stick` im Kopf (evtl. Stick als Quelle).

---

### Situation 16: Schottland Highland Games und Südengland — D: ↔ OneDrive, teils E: (rund 1,6 GB)

**Betroffene Dateien:** 6 + 9 + 3 Dateien, zusammen ~1,6 GB
**Betroffene Laufwerke:** D: und D:, teils E:

**Was ist das?**
Schottland 2025 „6.9. Highland Games“ (6 Videos, ~0,5 GB) und Südengland 30.9.–7.10.2023 (9 Videos, ~0,6 GB, plus 3 Videos vom 4.10. Bristol, ~0,16 GB mit zusätzlicher E:-Kopie).

**Wo liegen die Kopien?**

- `D:\BACKUP große Platte (F)\SCHOTTLAND 2025\6.9. Highland Games` ↔ `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien\Eigene Aufnahmen` — 6 Dateien, ~0,5 GB
- `D:\BACKUP große Platte (F)\ENGLAND Reisen\4_SÜDENGLAND 30.9.-7.10.2023` ↔ `D:\OneDrive Backup 2026 Februar\Tanja - Eigene Dateien\Südengland 30.9.-7.10.23` — 9 Dateien, ~0,6 GB
- `D:\BACKUP große Platte (F)\ENGLAND Reisen\…\Fotos Tanja\4.10.23 Bristol` (+ OneDrive-Zwilling) ↔ `E:\BACKUP lahme Platte (D)\Selphy Drucker USB\Südengland 2023\4.10. Bristol` — 3 Dateien, ~0,16 GB je Seite

**Wie ist das vermutlich passiert?**

- **2023 bzw. 2025 — Reisen aufgenommen und thematisch sortiert auf D:.** *Sicher.*
- **Februar 2026 — OneDrive-Backup spiegelte sie nach `…\Eigene Aufnahmen` bzw. `…\Südengland 30.9.-7.10.23`.** *Wahrscheinlich.* Evidence: OneDrive-mtimes 2026-02-25, BACKUP-mtimes 2023/2025.
- **Zusätzlich — Südengland 4.10. wanderte nach `E:\Selphy Drucker USB` (Drucker-Stick).** *Wahrscheinlich.* Evidence: Pfad `Selphy Drucker USB` deutet auf **Drucker-/Stick-Vorbereitung**, E: als Ziel — dritte Kopie auf anderer Platte.

**Welche Kopie ist das Original?**
Die **Reise-Ordner auf D:** sind die thematischen Originale. *Wahrscheinlich.*

**Welche Kopien sind „Unfälle“?**
OneDrive ist die **Sicherung**, Selphy-Stick die **Druck-Vorbereitung** — beide bewusst, aber liegen geblieben.

**Empfehlung für die Durchsicht:**
Reise-Ordner auf D: als Haupt-Ablage ist natürlich. OneDrive und Selphy sind Zweitablagen für Sicherung/Druck.

---

### Situation 17: Hundeausstellung Hannover 2013 und Silvester 2015 — vierfach im E:-Archiv (je rund 0,4 GB)

**Betroffene Dateien:** 7 + 1 + 1 Dateien, je ~0,4 GB, vierfach vorhanden
**Betroffene Laufwerke:** E: und E:

**Was ist das?**
Ältere Event-Videos: Hundeausstellung Hannover 26.10.2013 (7 Videos, ~0,4 GB) und Silvester 2015/2016 (`20160101_000639.mp4`, ~0,4 GB, sowie `Silvester 2015 2016` ↔ `Handyfotos 2015 2016`).

**Wo liegen die Kopien?**

- Hundeausstellung: `…\Fotos_Archiv\Fotos\2013\Hundeausstellung Hannover 2013\Videos` ↔ `…\Diverses\Fotos von anno dazumal bis 2016\Hundeausstellung 2013` ↔ `…\Fotos von anno dazumal bis 2016\Fotos Huawei\Camera` ↔ `…\Tanjas Ordner 2014_2015_2016\Fotos\Fotos Huawei\Camera` — sowie jeweils noch einmal im **zweiten Archiv-Zweig** (also insgesamt sechs Pfade, aber vier logische Ablagen je 7 Dateien). Auf beiden Zweigen aus Situation 2 identisch.
- Silvester 2015: `E:\BACKUP lahme Platte (D)\Tanjas Ordner_Archiv\…\Diverses\Fotos von anno dazumal bis 2016\Silvester 2015 2016` ↔ `…\Diverses\Handyfotos 2015 2016\Camera` ↔ `…\Tanjas Ordner 2014_2015_2016\Fotos\Silvester 2015 2016` ↔ `…\Tanjas Ordner 2014_2015_2016\Handyfotos 2015 2016\Camera` — 1 Datei, vierfach.

Beide gehören inhaltlich zu **Situation 2** (altes Archiv) — wer dort einen Zweig wählt, beantwortet diese Frage gleich mit.

**Wie ist das vermutlich passiert?**

- **2013 bzw. 2015 — Aufnahmen entstanden.** *Sicher.*
- **Später — beim Aufbau der E:-Archiv-Zweige wurde derselbe Event in die thematische Struktur (`Hundeausstellung…\Videos`), in die Sammelablage (`Diverses\Hundeausstellung 2013`) und in die Handy-Camera-Ablage (`Fotos Huawei\Camera`) einsortiert — und das in beiden Zweigen.** *Wahrscheinlich.* Evidence: **Vier parallele Pfad-Muster** mit identischen Dateinamen und mtimes 2013-10-26 bzw. 2015-12-31 identisch — typisch für **Mehrfach-Sortierung nach Event vs. nach Quelle**.
- *Vermutung:* „Fotos Huawei\Camera“ war die Handy-Import-Ablage, „Hundeausstellung“ die Event-Sortierung.

**Welche Kopie ist das Original?**
Vermutlich **`…\Fotos Huawei\Camera`** als Import, **Event-Ordner** als Sortierung. *Vermutung.*

**Welche Kopien sind „Unfälle“?**
Die **vierfache Ausbreitung** ist die Folge der **E:-internen Verdopplung** (Situation 2) kombiniert mit **Doppel-Sortierung** — nicht ein einzelner Fehler, sondern zwei sich verstärkende Muster.

**Empfehlung für die Durchsicht:**
Wenn Sie Situation 2 entscheiden, ist diese Situation automatisch mit entschieden. Wenn Sie separat schauen, ist der **Event-Ordner** die thematisch schönere Haupt-Ablage.

---

## 4. Wiederkehrende Muster

Diese fünf Muster tauchen in fast allen Situationen wieder auf. Wenn Sie sie wiedererkennen, verstehen Sie viele Einzelgeschichten auf einmal.

### Muster 1: OneDrive-Synchronisierung — „Handy ↔ OneDrive“ auf D:

**Was passiert?** Dieselben Videos liegen einmal in einem **direkten Handy-/Kamera-Import** (`2026 vom Handy gesichert`, `Xiaomi GALERIE`, `Fotos ab 2020`) und einmal in **`OneDrive Backup 2026 Februar`** — oft mit Ordnernamen `Tanja - Eigene Dateien\Eigene Aufnahmen` oder `TanjaDirk - Geteilt`.

**Wie erkennt man es?** OneDrive-Kopien tragen fast alle **25./26. Februar 2026** als Änderungsdatum, während die Gegenstücke ihre natürlichen Aufnahme-Daten tragen (2024, 2025 …). *Sicher.* Die Pfade enthalten `OneDrive Backup 2026 Februar`.

**Beispiele:** Situation 1 (Handy-Videos, 134 Dateien), Situation 5 (Hochzeit), Situation 6 (BINGO), Situation 10 (KATE ANTONIA), Situation 11 (Mallorca), Situation 14/16 (Reisen).

**Deutung:** Vermutlich wurde **im Februar 2026** ein OneDrive-Backup oder eine Synchronisierung angestoßen, die viele bestehende Ordner noch einmal nach `OneDrive Backup 2026 Februar` spiegelte. *Wahrscheinlich.* Die OneDrive-Kopie ist dann die **Zweitablage**, die direkte Ablage das **Original**.

---

### Muster 2: Backup von Backup — E: enthält sich selbst mehrfach

**Was passiert?** Innerhalb von `E:\BACKUP lahme Platte (D)` existieren **zwei große Zweige** (`Fotos_Archiv` und `Tanjas Ordner 2014_2015_2016`), die **denselben alten Bestand** enthalten — plus drei parallele „ALLE“-Ordner und doppelte „Spanien Präs“-Ordner.

**Wie erkennt man es?** Auf E: sind **672 von 676 geprüften großen Dateien** dupliziert (99,4 %), davon **~90 % innerhalb von E:** selbst (*Sicher*). Die Zweige sind ähnlich groß (71 vs. 57 GB) und enthalten **43 von 43** identische „ALLE“-Videos. Änderungsdaten sind identisch oder um exakt 1 Stunde versetzt.

**Beispiele:** Situation 2 (altes Archiv), Situation 4 (ALLE), Situation 12 (Allgemeine Dateien ↔ What is Love), Situation 17 (Hundeausstellung/Silvester kreuzweise in beiden Zweigen).

**Deutung:** E: war als **Sicherung von D:** gedacht (Name!), wurde aber im Lauf der Jahre **selbst noch einmal gesichert/umorganisiert**, ohne den alten Stand zu löschen — so wanderte dieselbe Sammlung **zwei- bis dreimal** in E: hinein. *Wahrscheinlich.*

---

### Muster 3: Ordner-in-Ordner — Kopie im eigenen Unterordner

**Was passiert?** Ein Ordner enthält **sich selbst** noch einmal tiefer — Unterordner mit identischen Dateien.

**Wie erkennt man es?** Pfade sind **verschachtelt** (Unterordner liegt physisch im Oberordner), Dateien sind byte-identisch, oft mit **identischen mtimes**. In unserer Prüfung 22 solcher Fälle (*Sicher*).

**Beispiele:** Situation 3 (VW Zeit → Newsletter Markenvertreter, 16 Dateien), Situation 5 (HOCHZEIT → Hochzeitsvideo, 1 Datei), Situation 6 (BACKUP → BINGO Sendung), Situation 12 (Allgemeine Dateien → 05.01.14-23.03.2014), Situation 17 (teilweise).

**Deutung:** Typisch „für einen Zweck (Newsletter, Unterordner, Sortierung) herauskopiert, Original oben vergessen“. *Wahrscheinlich.*

---

### Muster 4: Sammelordner — „ALLE“, „Diverses“, „Fotos von anno dazumal“ wandern mit

**Was passiert?** Ein **Sammelname** wie `ALLE`, `ALLE_archiv`, `Diverses`, `Fotos von anno dazumal bis 2016`, `Fotos Huawei\Camera` sammelt „alles“ und wird bei jeder Sicherung **komplett mitkopiert**.

**Wie erkennt man es?** Name „ALLE“ taucht **dreifach** mit **100 % Überschneidung** auf; „Diverses“ zieht jahrelang mit. Dateien wie `100_1764.MOV` liegen **zehnfach** vor, weil sie in **jedem** Sammelordner stecken.

**Beispiele:** Situation 4 (ALLE), Situation 2/17 (Fotos von anno dazumal ↔ Fotos Huawei).

**Deutung:** Sammelordner waren einmal praktisch, wurden aber **nie aufgeräumt**, sondern bei jeder Umorganisation **mitgeschleppt**. *Wahrscheinlich.*

---

### Muster 5: Thematische Doppel-Sortierung — „nach Person“ und „nach Jahr“ gleichzeitig

**Was passiert?** Dieselben Videos liegen einmal **nach Person/Ereignis** (`1. KATE ANTONIA`, `Meine Kaninchen`, `ENGLAND Reisen`) und einmal **nach Jahr** (`Fotos ab 2020\2025`, `Tanjas Ordner 2019- Ende 2023`) oder **nach Quelle** (`2026 vom Handy gesichert`, `Xiaomi GALERIE`).

**Wie erkennt man es?** Gleicher Dateiname, gleiches Datum, aber **unterschiedliche Oberordner-Logiken** — z. B. `VID_20241027_183957.mp4` in `Meine Kaninchen\Frodo …` und in `OneDrive\…\Frodo …` und in `Meine Kaninchen\…\Handy Ordner\M&L 9.Geburtstag`.

**Beispiele:** Situation 10 (KATE ANTONIA), Situation 13 (Kaninchen), Situation 7/9 (Camera/Videos, London Fotos/Videos).

**Deutung:** Sie haben vermutlich **bewusst nach verschiedenen Kriterien sortiert** (Person vs. Jahr vs. Gerät) und dabei **Kopien** statt **Verknüpfungen** angelegt. *Vermutung.* Keine ist „falsch“ — es ist eine Frage, wie Sie suchen möchten.

---

## 5. Was wir nicht wissen können

Ehrlichkeit ist wichtig — auch dieses Dokument hat Grenzen:

- **Änderungsdaten können täuschen.** Beim Kopieren kann ein System das alte Datum **bewahren** (dann sehen Original und Kopie gleich alt aus) oder ein **neues Datum** setzen (dann wirkt die Kopie jünger). Wir haben beides gesehen: E:-interne Kopien behalten alte Daten (2010–2015), OneDrive-Kopien tragen neue Daten (2026-02). Wir können nicht für jede Datei sagen, was passiert ist. *Sicher, dass Daten irreführen können.*
- **Wir können nicht beweisen, wann oder warum genau kopiert wurde.** Ordnernamen und Tages-Bündelungen (z. B. 25. Februar 2026) sind starke Hinweise, aber kein Protokoll. Ob Sie selbst kopiert haben oder eine Software (OneDrive-Sync) automatisch gespiegelt hat, lässt sich aus Pfaden allein nicht sicher sagen.
- **OneDrive-Verhalten bleibt ungeprüft.** Ob die Dateien heute noch in der Cloud liegen, wie groß Ihr Cloud-Speicher ist und ob die Synchronisierung in beide Richtungen wirkt (lokales Löschen → Cloud-Löschen), haben wir **nicht** geprüft. Der Ordner „OneDrive Backup 2026 Februar“ liegt auf Ihrer **Festplatte D:** — nicht in der Cloud.
- **Manche Doppelungen können Absicht sein.** Zwei Kopien auf demselben Laufwerk *können* bewusst als „schnelle zweite Sicherung“ gemeint gewesen sein. Nichts in diesem Dokument sagt, eine Kopie sei überflüssig — nur, dass sie existiert.
- **Nur große Dateien wurden geprüft (≥ 25 MB).** Das sind vor allem Videos und große Archive. Die allermeisten Fotos sind kleiner (wenige MB) und wurden *nicht* auf Inhalt verglichen. Dort kann es **weitere** Doppelungen geben, die wir hier nicht sehen — Beispiel: `D:\2026 vom Handy gesichert\Camera` enthält ~7.200 Fotos (~25 GB) unterhalb der Prüfgrenze.
- **Externe Festplatte und Cloud sind nicht enthalten.** Ob dieselben Videos bereits auf Ihrer externen 1-TB-Platte liegen, wissen wir nicht — und können daher nicht sagen, was schon gesichert ist.
- **Gleiche Inhalte mit anderem Namen sind nur teilweise erfasst.** Wir haben über Hashes gleiche Bytes gefunden, auch wenn der Name abweicht (z. B. `TV-20260315-1659-3511.1080.mp4` ↔ `TanjaDirkBingoMärz2026.mp4`), aber die Ordner-Überlappungstabelle zählt nur Paare mit **gleichem Dateinamen** — der Rest ist in den Gruppenzahlen enthalten, aber nicht als Ordnerpaar ausgewiesen.

---

## 6. Wie Sie dieses Dokument nutzen

1. **Lesen Sie Situation für Situation** und prüfen Sie: *Kenne ich diese Ordner? Passt die Geschichte zu meiner Erinnerung?*
   - Wenn ja — Sie können sich beim Leitfaden `duplicate-resolution-guide.md` sicherer für die **Haupt-Ablage** entscheiden.
   - Wenn nein — kreuzen Sie **„Beides behalten“** an. Wir schauen dann später gemeinsam genauer hin. Das ist immer erlaubt.

2. **Tragen Sie Ihre Entscheidung im Leitfaden ein**, nicht hier. Die 14 Karten im Leitfaden decken die wichtigsten Doppelungen ab; die 17 Situationen hier geben Ihnen den Hintergrund dazu:
   - Situation 1 → Karte 1 (Handy ↔ OneDrive)
   - Situation 2, 4, 17 → Karte 2 + 4 (altes E:-Archiv, ALLE)
   - Situation 3 → Karte 3 (VW Zeit)
   - Situation 5 → Karte 5 (Hochzeit)
   - Situation 6 → Karte 6 (lose Dateien/BINGO)
   - Situation 7 → Karte 7 (Camera Stand)
   - Situation 8 → Karte 8 (Kaninchen D↔E)
   - Situation 9 → Karte 9 (London)
   - Situation 10 → Karte 10 (KATE ANTONIA)
   - Situation 11 → Karte 11 (Mallorca)
   - Situation 12 → Karte 12 (Allgemeine/What is Love)
   - Situation 13 → Karte 13 (Kaninchen ↔ OneDrive)
   - Situation 14+16 → Karte 14 (Reisen ↔ OneDrive)
   - Situation 15 → Karte 6/14 (WhatsApp/Signal — in Karten 6 und 14 enthalten)

3. **Wenn Sie unsicher sind, behalten Sie beide.** Keine Entscheidung in diesem Dokument löst etwas aus — es ist nur Lesestoff.

4. **Löschen oder verschieben Sie nichts selbst** anhand dieses Dokuments. Nach Ihrer Durchsicht prüfen wir gemeinsam: Sind die „Behalten“-Kopien vollständig und lesbar? Erst danach wird — nur mit Ihrer ausdrücklichen Zustimmung — eine gestufte, sichere Umsetzung geplant (erst kopieren & prüfen, dann entfernen, nie direkt löschen). Siehe Abschnitt 8 im Leitfaden.

5. **Nutzen Sie die Muster aus Abschnitt 4 als Abkürzung.** Wenn Sie z. B. verstehen, dass viele OneDrive-Kopien vom **25. Februar 2026** stammen, können Sie für alle Reisen/Feiern (Situationen 1, 5, 6, 10, 11, 14, 16) ähnlich entscheiden.

---

## Anhang: Herkunft der Zahlen (für die technische Prüfung)

Dieser Anhang muss nicht gelesen werden — er zeigt, woher jede Zahl stammt.

Alle Situationen beruhen auf dem detaillierten Prüfprotokoll `data/hashes/duplicate-candidate-hashes.csv.gz` (Run `498bdf69b7c04191b76b834be0ff4f97`, 753 Gruppen, 1.868 Dateien, ~212 GB logisch) und der daraus abgeleiteten Übersicht `data/hashes/folder-overlap-summary.csv` (75 Zeilen, sortiert nach `total_logical_bytes`). Größen sind dortige `total_logical_bytes` (logisch, in GiB gerundet). Paar-Überschneidungen wurden dort über **gleichen Dateinamen + maximalen gemeinsamen Pfad-Suffix** ermittelt — daher kredenzt ein Duplikat mit umbenanntem Namen (z. B. Situation 6, TV-Mitschnitt) zwar zur Gruppenzahl, aber nicht als Ordnerpaar.

| Situation | Zeilen der Übersichtstabelle | Ergänzende Quelle |
|---|---|---|
| 1 | 1 | Ordner-Überlappung Abschnitt 3 Detail 1 (Abdeckung 134/269 vs. 134/197); mtime-Bündelung 2026-02-25 aus Detailprotokoll |
| 2 | 2, 3, 37 | Zweiggrößen aus `data/processed/top-folders.csv`; mtimes identisch/1h-Versatz aus Detailprotokoll |
| 3 | 4 | Abschnitt 5 (verschachtelt, 5,00 GiB) |
| 4 | 5, 6, 30–35 | Abschnitt 5 (Datei mit zehn Kopien, ALLE-Familie) |
| 5 | 9–14 | Abschnitt 6 (Datei Nr. 1, vier Kopien, 2,33 GB) |
| 6 | 7, 19, 26, 27 | Abschnitt 6 (Dateien Nr. 3+4, je drei Kopien, BINGO) |
| 7 | 8 | Abschnitt 3 Detail 6 |
| 8 | 15, 40, 41, 42 | Abschnitt 4 (kreuz-Laufwerk) |
| 9 | 16 | — |
| 10 | 17, 28, 38, 39, 44, 46, 52–54, 66 | — |
| 11 | 18, 20, 21, 36 | plus Pfade `ROSSMANN`, `Malle`, `Pictures` aus Detailprotokoll |
| 12 | 22–24 | — |
| 13 | 25, 48, 49, 51, 60–64 | — |
| 14 | 29, 47, 50, 55–59, 65 | plus `Selphy Drucker USB` als E:-Dritt-Kopie |
| 15 | 60, 57–59, 47 (WhatsApp Zip), 47 (Signal) | Abschnitt 6 (Zip-Gruppe mit 3 Kopien) |
| 16 | 65, 57, 42 (teilweise) | Schottland/Südengland E:-Kopie |
| 17 | 67–75, 68–71 | Abschnitt 5 (vierfach, Hundeausstellung/Silvester) |

Weitere Quellen: freier Speicher und Laufwerkslabels aus `data/collected/storage-topology-report.md` (08.09.2026 12:14:42, D: 74,57 GiB frei / 8 %, E: 39,99 GiB frei / 13 %); Gesamtzahlen (753 Gruppen, ~212 GB, Obergrenzen ~125 GB gesamt / ~74 GB D: / ~45 GB E:) aus `plans/drafts/folder-overlap-assessment.md` Abschnitte 1,2,7. Fotos unter 25 MB aus `data/processed/photo-summary-by-folder.csv`. Wo eine Situation mehrere Zeilen zusammenfasst, wurde die Obergrenze so angegeben, dass keine Datei doppelt gezählt wird; die Datei mit zehn Kopien wurde gegen das Detailprotokoll geprüft.

Dieses Dokument hat keine Datei gelesen, verändert oder verschoben und enthält **keine Lösch-, Verschiebe-, Archivierungs-, Cloud- oder Umsortierungsanweisungen**. Es ergänzt den Leitfaden `plans/drafts/duplicate-resolution-guide.md` und widerspricht ihm nicht. `git diff --check` ist sauber.

