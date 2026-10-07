# Evaluationslauf

Durchgeführt am **07.10.2026 um 20:07 Uhr** mit dem konfigurierten Modell `gpt-6-luna`.

**Umfang:** 20 Fragen in den Modi Baseline und Hybrid, insgesamt 40 Antworten.

## Automatische Kennzahlen

| Messgröße | Baseline | Hybrid |
| --- | ---: | ---: |
| Erwartetes Werkzeug gewählt (16 Fragen mit erwartetem Werkzeugaufruf) | 0/16* | 13/16 |
| Kein Werkzeug bei erwarteter Klärung oder Ablehnung (4 Fragen) | 4/4 | 4/4 |
| Quellenhinweis bei erforderlicher Quelle (16 Fragen) | 0/16 | 12/16 |
| Explizite Quellenbenennung (16 Fragen) | 0/16 | 7/16 |
| Datenstand erwähnt (16 Fragen) | 0/16 | 7/16 |
| Werkzeugantworten mit ausschließlich erfolgreichen Ergebnissen | 0/0 | 12/14 |
| Mittlere Antwortzeit | 4,59 s | 10,58 s |
| Laufzeitfehler | 0 | 0 |

\* Der Baseline-Modus hat keinen Werkzeugzugriff. `0/16` beschreibt daher den erwarteten Unterschied zwischen den Modi und keinen Fehler bei einer möglichen Werkzeugauswahl.

## Fragen und Werkzeugaufrufe

„Erwartet“ bezeichnet das Werkzeug oder Verhalten aus dem Evaluationskatalog. In der Baseline wurden bei keiner Frage Werkzeuge aufgerufen.

| # | Frage | Erwartet | Hybrid: Werkzeugaufruf | Bewertung |
| --- | --- | --- | --- | --- |
| Q01 | Wer gewann den Großen Preis von Monaco 2024? | `get_race_results` | `get_race_results` | korrekt |
| Q02 | Wie wurde Max Verstappen beim Rennen in Spa 2023 platziert? | `get_race_results` | `get_season_schedule`, `get_race_results` | korrekt |
| Q03 | Wie lautete die Fahrerwertung nach 2023? | `get_driver_standings` | `get_driver_standings` | korrekt |
| Q04 | Welche Konstrukteure belegten 2020 die ersten drei Plätze? | `get_constructor_standings` | `get_constructor_standings` | korrekt |
| Q05 | In welchem Land liegt Suzuka? | `get_circuit_information` | `get_circuit_information` | korrekt |
| Q06 | Welche Rennen gab es in der Saison 2022? | `get_season_schedule` | `get_season_schedule` | korrekt |
| Q07 | Vergleiche Hamilton und Verstappen zwischen 2021 und 2024. | `compare_drivers` | `compare_drivers`, `get_driver_standings` (4×) | korrekt |
| Q08 | Welche Rennen gewann Verstappen 2022? | `get_driver_season_results` | `get_driver_season_results` (2×), `get_driver_information`, `get_driver_standings`, `get_race_results` (2×), `search_knowledge_base` (2×) | korrekt |
| Q09 | Was ist der Unterschied zwischen Fahrer- und Konstrukteurswertung? | `search_knowledge_base` | kein Werkzeug | abweichend |
| Q10 | Wie funktioniert die Punktevergabe in der Formel 1? | `search_knowledge_base` | `search_knowledge_base` (2×) | korrekt |
| Q11 | Was ist ein Sprint-Wochenende? | `search_knowledge_base` | `search_knowledge_base` | korrekt |
| Q12 | Wer gewann 2024? | Rückfrage | kein Werkzeug | korrekt |
| Q13 | Wie wird das Wetter beim nächsten Rennen? | Ablehnung | kein Werkzeug | korrekt |
| Q14 | Auf welcher Strecke fand der Große Preis von Belgien 2023 statt? | `get_race_results` | `get_season_schedule` | abweichend |
| Q15 | Welche Nationalität hat Lewis Hamilton? | `get_driver_information` | kein Werkzeug | abweichend |
| Q16 | Was ist Ferrari als Konstrukteur? | `get_constructor_information` | `get_constructor_information`, `search_knowledge_base` | korrekt |
| Q17 | Wann findet das nächste verfügbare Rennen statt? | `get_season_schedule` | `get_season_schedule` | korrekt |
| Q18 | Wer startete beim Rennen in Bahrain 2024 von Pole? | `get_race_results` | `get_race_results` (2×), `search_knowledge_base` (2×) | korrekt |
| Q19 | Wer gewinnt die Fußball-WM 2026? | Ablehnung | kein Werkzeug | korrekt |
| Q20 | Vergleiche die beiden Fahrer. | Rückfrage | kein Werkzeug | korrekt |

## Auffälligkeiten

- Drei der 16 toolpflichtigen Fragen verfehlten im Hybrid-Modus das erwartete Routing: Q09 rief kein Werkzeug auf, Q14 wählte `get_season_schedule` statt `get_race_results`, und Q15 rief kein Werkzeug auf.
- Das erwartete Verhalten ohne Werkzeug wurde bei allen vier Klärungs- bzw. Ablehnungsfällen eingehalten.
- Bei 12 von 14 Antworten mit Werkzeugaufrufen waren alle Werkzeug-Ergebnisse erfolgreich. Es wurden keine Laufzeitfehler protokolliert.
- Die mittlere Antwortzeit lag im Hybrid-Modus bei 10,58 Sekunden und in der Baseline bei 4,59 Sekunden.

## Einordnung und Grenzen

Quellenhinweis, Quellenname und Datenstand sind automatisierte Textmuster-Prüfungen. Sie belegen weder die tatsächliche Nutzung einer Quelle noch die sachliche Richtigkeit einer Antwort. Die Ergebnisse enthalten keine manuelle Bewertung von Korrektheit, Vollständigkeit, Nachvollziehbarkeit oder Halluzinationen. Aus diesem kleinen Evaluationskatalog lässt sich daher keine allgemeine Aussage zur faktischen Überlegenheit eines Modus ableiten.
