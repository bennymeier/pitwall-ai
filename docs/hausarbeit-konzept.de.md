# Arbeitsskizze: Pitwall AI

## 1. Arbeitstitel

**Pitwall AI**  
Hybrider Formel-1-Wissensassistent: geprüfte Werkzeugaufrufe plus lokaler Wissensabruf (RAG).

## 2. Warum das Thema?

- Sprachmodelle antworten flüssig, können bei historischen Statistiken aber überzeugend klingende falsche Zahlen liefern.
- Idee: API-Daten und Hintergrundwissen getrennt behandeln; Quellen und Datenstand sichtbar machen.
- Nicht nur antworten lassen, sondern nachvollziehbar machen, worauf die Antwort beruht.

## 3. Für wen und wofür?

- Zielgruppe: Studierende, interessierte Zuschauerinnen und Zuschauer, Lehrende.
- Typische Fragen: Rennen, Fahrer, Konstrukteure, Kalender und Wertungen.
- Sprache der Oberfläche: Deutsch.

## 4. Meine Leitfrage

Verbessert die Kombination aus geprüften Werkzeugen und lokalem Wissenskorpus gegenüber einer Baseline ohne externe Quellen die fachliche Richtigkeit und Nachvollziehbarkeit?

## 5. Was soll die Anwendung können?

- Chat mit Quellenanzeige
- Jolpica-Abfragen für strukturierte Renndaten
- Semantische Suche im lokalen Wissenskorpus
- Baseline und Hybrid vergleichbar machen
- Daten synchronisieren und Ergebnisse reproduzierbar speichern
- Schnittstellen testbar halten; Fehler abfangen; keine Zugangsdaten einchecken

## 6. Sprachmodell

- Modell über `OPENAI_MODEL` konfigurierbar; Verfügbarkeit hängt vom API-Konto ab.
- Die Responses API übernimmt die Werkzeugaufrufe.
- Für den Bericht Modell und Laufdatum festhalten.

## 7. Daten und Wissenskorpus

- Jolpica: strukturierte Renndaten.
- Lokale Erklärtexte: Wertungen, Punkte, Qualifying und Sprint.
- Quellenangaben und Abrufzeitpunkt möglichst mitführen.
- Einbettungsmodell: `text-embedding-3-small`.

## 8. Verwendete KI-Verfahren

- Werkzeugaufrufe für Daten, die überprüfbar sein müssen
- RAG und semantische Suche für erklärendes Hintergrundwissen
- Systemanweisung und abgerufenen Kontext getrennt halten
- Baseline als Vergleich ohne externe Quellen

## 9. Grober Aufbau

`Streamlit -> AssistantService -> OpenAI Responses API -> geprüfte Werkzeuge -> JolpicaClient`

Für Wissensfragen zusätzlich: `AssistantService -> VectorStore -> Chroma`.  
Das ausführlichere [Architekturdokument](architecture.md) zeigt den Datenfluss.

## 10. Umsetzung

- Python-Module typisieren und Daten mit Pydantic-Modellen validieren.
- Wiederholungsversuche und Zeitlimits für externe Aufrufe.
- Stabile Kennungen für gespeicherte Dokumente.

## 11. Auswertung: aktueller Stand

- 20 Fragen, jeweils Baseline und Hybrid; Lauf vom 07.10.2026.
- Hybrid wählte bei 13 von 16 Werkzeugfragen das erwartete Werkzeug.
- Quellenhinweis: 12/16; Datenstand erwähnt: 7/16.
- Kein Werkzeug bei erwarteter Rückfrage oder Ablehnung: 4/4; keine Laufzeitfehler.
- Diese Kennzahlen prüfen Routing und Textmarker, nicht die faktische Richtigkeit.
- Nächster Schritt: Antworten manuell auf Richtigkeit, Vollständigkeit und Halluzinationen prüfen.
- Details: [Evaluationsbericht](evaluation-report.md).

## 12. Risiken und bewusst außerhalb des Umfangs

- API-Ausfälle, veraltete Daten und mehrdeutige Namen.
- Modelländerungen und kleine Stichprobe schränken die Aussagekraft ein.
- Echtzeitverfolgung, Wetter und Vorhersagen sind nicht Teil des ersten Umfangs.

## 13. Datenschutz und rechtliche Hinweise

- Keine API-Schlüssel ins Repository aufnehmen.
- Fragen werden zur Antwortgenerierung an den konfigurierten OpenAI-Dienst gesendet.
- Quellenangabe zu Jolpica und Vorgaben der Hochschule beachten.
- Kein offizielles Formel-1-Produkt.

## 14. Als Nächstes

- Die Routing-Abweichungen aus Q09, Q14 und Q15 untersuchen.
- Manuelle Bewertung ergänzen; erst danach Aussagen zur Korrektheit treffen.
- Bei Bedarf Wissenskorpus erweitern und alternative Modelle oder lokale Einbettungen prüfen.

## 15. Mögliche Präsentation: acht Folien

1. Problem und Motivation
2. Zielgruppe und Anwendungsszenario
3. Systemidee
4. Werkzeugaufrufe
5. RAG und Daten
6. Vorführung und Auswertung
7. Risiken und Datenschutz
8. Ergebnisse und Ausblick

## 16. Vorführung: fünf bis zehn Minuten

1. Eine Siegerfrage mit Quellenbeleg stellen.
2. Eine Wertungstabelle abrufen.
3. Eine Wissensfrage zu Punkten stellen.
4. Eine absichtlich mehrdeutige Frage stellen.
5. Quellen, Datenstand, Baseline/Hybrid und Synchronisierung des Wissenskorpus zeigen.