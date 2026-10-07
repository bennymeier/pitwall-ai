# Evaluationsanleitung

## Forschungsfrage

Beantwortet ein hybrider Assistent mit geprüften Werkzeugen und lokalem Wissensabruf deutschsprachige Formel-1-Fragen korrekter und nachvollziehbarer als eine reine Modell-Baseline?

## Versuchsaufbau

Die 20 Fragen aus `evaluation/questions.json` werden jeweils in den Modi Baseline und Hybrid gestellt. Die Referenzdaten für Werkzeugaufrufe werden während des Laufs über Jolpica abgerufen; historische Ergebnisse sind nicht als erwartete Wahrheiten fest codiert. Erfasst werden die Werkzeugauswahl, Quellen- und Datenstandhinweise, Faktenabdeckung, unbelegte Behauptungen, Fehler und Antwortzeiten.

Der Evaluationslauf wird mit `python scripts/evaluate.py` gestartet. Die Rohdaten werden in `evaluation/results/evaluation.csv` gespeichert. Der Bericht für den Lauf vom 07.10.2026 liegt unter [`evaluation-report.md`](evaluation-report.md) und enthält Kennzahlen sowie die Werkzeugaufrufe je Frage. Die Bewertungsfelder für eine manuelle Inhaltsprüfung werden nicht automatisch ausgefüllt.

Manuelle Prüfende bewerten sachliche Richtigkeit, Vollständigkeit, Nachvollziehbarkeit, Quellenbezug, Verständlichkeit und Schwere möglicher Halluzinationen. Eine modellbasierte Bewertung darf die menschliche Prüfung ergänzen, aber keinen Abgleich mit verifizierten Daten ersetzen.

## Interpretation und Grenzen

Verglichen werden die jeweils gepaarten Fragen; Ergebnisse sollten nach Kategorie zusammengefasst und Fehlverläufe einzeln untersucht werden. API-Ausfälle, Modellversionswechsel, unvollständige Eingabeaufforderungen und die Qualität des Wissensabrufs können die Resultate beeinflussen. Der kleine Testkatalog erlaubt keine allgemeine Aussage über die Leistungsfähigkeit des Systems.

## Evaluationslauf vom 07.10.2026

Der aktuelle Lauf umfasst ebenfalls 20 Fragen in beiden Modi und 40 Antworten. Die CSV-Datei wurde am 07.10.2026 um 20:07 Uhr aktualisiert.

| Messgröße | Baseline | Hybrid |
| --- | ---: | ---: |
| Quellenhinweis bei 16 quellenpflichtigen Fragen | 0/16 (0 %) | 12/16 (75 %) |
| Konkrete Quelle namentlich genannt | 0/16 (0 %) | 7/16 (43,75 %) |
| Datenstand oder Abrufzeit erwähnt | 0/16 (0 %) | 7/16 (43,75 %) |
| Erwartetes Werkzeug ausgewählt | Nicht verfügbar | 13/16 (81,25 %) |
| Kein Werkzeug bei erwarteter Klärung oder Ablehnung | 4/4 (100 %) | 4/4 (100 %) |
| Werkzeugantworten mit ausschließlich erfolgreichen Ergebnissen | 0/0 | 12/14 (85,71 %) |
| Mittlere Antwortzeit | 4,59 s | 10,58 s |
| Laufzeitfehler | 0 | 0 |

Die drei verfehlten Werkzeugrouten waren Q09, Q14 und Q15. Q14 rief statt der Rennergebnisse den Saisonkalender ab; bei Q09 und Q15 wurde kein Werkzeug aufgerufen. Die Kennzahlen zu Quellen- und Datenstandhinweisen beruhen auf Textmustern und bewerten nicht die inhaltliche Richtigkeit. Eine manuelle Bewertung steht für diesen Lauf noch aus. Der vollständige Fragen- und Werkzeugbericht ist unter [`evaluation-report.md`](evaluation-report.md) abgelegt.
