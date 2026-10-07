# Evaluationsbericht: Baseline vs. Hybrid

**Durchgeführt am:** 07.10.2026, Datensatz zuletzt aktualisiert um 20:07 Uhr  
**Umfang:** 20 Fragen in zwei Modi, insgesamt 40 Antworten  
**Datengrundlage:** [evaluation.csv](evaluation.csv)

## Ergebnisübersicht

| Messgröße | Baseline | Hybrid |
| --- | ---: | ---: |
| Quellenhinweis bei quellenpflichtigen Fragen | 0/16 (0 %) | 12/16 (75 %) |
| Konkrete Quelle namentlich genannt | 0/16 (0 %) | 7/16 (43,75 %) |
| Datenstand oder Abrufzeit erwähnt | 0/16 (0 %) | 7/16 (43,75 %) |
| Erwartetes Werkzeug ausgewählt | nicht verfügbar | 13/16 (81,25 %) |
| Kein Werkzeug bei erwarteter Klärung oder Ablehnung | 4/4 (100 %) | 4/4 (100 %) |
| Tool-Antworten mit ausschließlich erfolgreichen Ergebnissen | 0/0 | 12/14 (85,71 %) |
| Mittlere Antwortzeit | 4,59 s | 10,58 s |
| Laufzeitfehler | 0 | 0 |

## Werkzeugaufrufe je Frage

| ID | Frage | Erwartung | Hybrid: tatsächliche Werkzeuge | Routing |
| --- | --- | --- | --- | --- |
| Q01 | Wer gewann den Großen Preis von Monaco 2024? | `get_race_results` | `get_race_results` | korrekt |
| Q02 | Wie wurde Max Verstappen beim Rennen in Spa 2023 platziert? | `get_race_results` | `get_season_schedule`, `get_race_results` | korrekt |
| Q03 | Wie lautete die Fahrerwertung nach 2023? | `get_driver_standings` | `get_driver_standings` | korrekt |
| Q04 | Welche Konstrukteure belegten 2020 die ersten drei Plätze? | `get_constructor_standings` | `get_constructor_standings` | korrekt |
| Q05 | In welchem Land liegt Suzuka? | `get_circuit_information` | `get_circuit_information` | korrekt |
| Q06 | Welche Rennen gab es in der Saison 2022? | `get_season_schedule` | `get_season_schedule` | korrekt |
| Q07 | Vergleiche Hamilton und Verstappen zwischen 2021 und 2024. | `compare_drivers` | `compare_drivers`, `get_driver_standings` (4 Aufrufe) | korrekt |
| Q08 | Welche Rennen gewann Verstappen 2022? | `get_driver_season_results` | `get_driver_season_results` (2 Aufrufe), `get_driver_information`, `get_driver_standings` (2 Aufrufe), `get_race_results` (2 Aufrufe), `search_knowledge_base` (2 Aufrufe) | korrekt |
| Q09 | Was ist der Unterschied zwischen Fahrer- und Konstrukteurswertung? | `search_knowledge_base` | kein Werkzeug | **abweichend** |
| Q10 | Wie funktioniert die Punktevergabe in der Formel 1? | `search_knowledge_base` | `search_knowledge_base` (2 Aufrufe) | korrekt |
| Q11 | Was ist ein Sprint-Wochenende? | `search_knowledge_base` | `search_knowledge_base` | korrekt |
| Q12 | Wer gewann 2024? | Klärung, kein Werkzeug | kein Werkzeug | korrekt |
| Q13 | Wie wird das Wetter beim nächsten Rennen? | Ablehnung, kein Werkzeug | kein Werkzeug | korrekt |
| Q14 | Auf welcher Strecke fand der Große Preis von Belgien 2023 statt? | `get_race_results` | `get_season_schedule` | **abweichend** |
| Q15 | Welche Nationalität hat Lewis Hamilton? | `get_driver_information` | kein Werkzeug | **abweichend** |
| Q16 | Was ist Ferrari als Konstrukteur? | `get_constructor_information` | `get_constructor_information`, `search_knowledge_base` | korrekt |
| Q17 | Wann findet das nächste verfügbare Rennen statt? | `get_season_schedule` | `get_season_schedule` | korrekt |
| Q18 | Wer startete beim Rennen in Bahrain 2024 von Pole? | `get_race_results` | `get_race_results` (2 Aufrufe), `search_knowledge_base` (2 Aufrufe) | korrekt |
| Q19 | Wer gewinnt die Fußball-WM 2026? | Ablehnung, kein Werkzeug | kein Werkzeug | korrekt |
| Q20 | Vergleiche die beiden Fahrer. | Klärung, kein Werkzeug | kein Werkzeug | korrekt |

## Einordnung

Hybrid erzeugte häufiger Quellen- und Datenstandhinweise als Baseline. Das erwartete Werkzeug wurde in 13 von 16 Werkzeugfragen aufgerufen; die drei Abweichungen waren Q09, Q14 und Q15. Bei Q14 wurde statt der Rennergebnisse der Saisonkalender abgefragt, bei Q09 und Q15 erfolgte kein Werkzeugaufruf. Bei den vier Fragen, die eine Klärung oder Ablehnung ohne Werkzeug erforderten, routeten beide Modi korrekt.

Die mittlere Antwortzeit von Hybrid lag in diesem Lauf rund sechs Sekunden über Baseline. Von 14 Hybrid-Antworten mit Werkzeugaufruf hatten 12 ausschließlich erfolgreiche Werkzeugergebnisse. Es wurden keine Laufzeitfehler protokolliert.

Die Quellen-, Quellenname- und Datenstandwerte beruhen auf automatischen Textmustern. Sie belegen weder die tatsächliche noch die korrekte Verwendung einer Quelle. Die manuellen Bewertungsfelder für Richtigkeit, Vollständigkeit, Nachvollziehbarkeit, Verständlichkeit und Halluzination sind im CSV leer. Dieser Lauf erlaubt daher keine Aussage über einen allgemeinen Gewinn an faktischer Korrektheit.