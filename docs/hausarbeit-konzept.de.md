# Konzept: Pitwall AI

## 1. Arbeitstitel

Pitwall AI: Ein hybrider deutschsprachiger Formula-1-Wissensassistent mit Tool Calling und Retrieval-Augmented Generation.

## 2. Motivation und Problemstellung

Sprachmodelle formulieren Antworten flüssig, können bei historischen Statistiken aber plausible falsche Werte erzeugen. Pitwall AI trennt überprüfbare API-Daten von semantischem Hintergrundwissen und macht Quellen sichtbar.

## 3. Zielgruppe und Use Case

Zielgruppe sind Studierende, interessierte Zuschauer und Lehrende. Der Use Case ist die deutschsprachige Beantwortung von Fragen zu Rennen, Fahrern, Konstrukteuren, Kalendern und Wertungen.

## 4. Forschungsfrage

Verbessert die hybride Kombination aus validierten Tools und lokalem Wissenskorpus gegenüber einer Baseline ohne externe Quellen die fachliche Korrektheit und Nachvollziehbarkeit?

## 5. Anforderungen

Funktional sind Chat, Quellenanzeige, API-Abfragen, semantische Suche, Synchronisierung und Baseline/Hybrid-Vergleich. Nichtfunktional sind Typisierung, Reproduzierbarkeit, Fehlertoleranz, Datenschutz, keine Secrets im Repository und testbare Schnittstellen.

## 6. Foundation Model

Das konkrete Modell wird über `OPENAI_MODEL` konfiguriert, da verfügbare Modelle kontenabhängig sind. Die Responses API unterstützt Tool Calling; ein konkreter Evaluationstyp muss nach der Durchführung dokumentiert werden.

## 7. Wissenskorpus

Jolpica liefert strukturierte Daten. Ergänzende Erklärungen zu Wertungen, Punkten, Qualifying und Sprint werden als lokale Dokumente mit Provenienz erfasst. Embeddings werden mit `text-embedding-3-small` erzeugt.

## 8. Advanced-GenAI-Techniken

Zum Einsatz kommen Function Calling, RAG, semantische Suche, Prompt-Kontexttrennung und eine Baseline für den Vergleich.

## 9. Systemarchitektur

Die Anwendung besteht aus Streamlit, Assistant Service, validierten Tools, Jolpica-Adapter, Dokumentaufbereitung und Chroma. Das Architekturdiagramm steht in `docs/architecture.md`.

## 10. Implementierung

Die Python-Module sind vollständig typisiert und über Pydantic-Modelle verbunden. Retry, Timeouts, stabile IDs und gemockte Tests reduzieren technische Risiken.

## 11. Evaluation

20 deutsche Fragen werden nach Kategorie ausgeführt. Gemessen werden Tool-Auswahl, Quellen, Datenstand, Faktenabdeckung, unbelegte Behauptungen, Fehler und Dauer. **Echte Ergebnisse sind nach dem Evaluationslauf einzutragen.**

## 12. Risiken und Grenzen

API-Ausfälle, veraltete Daten, mehrdeutige Namen, Modelländerungen und kleine Stichproben begrenzen die Aussagekraft. Live-Tracking, Wetter und Prognosen sind nicht Teil des MVP.

## 13. Datenschutz und Recht

Keine Schlüssel oder Telemetrie werden gespeichert. Fragen werden zur Generierung an den konfigurierten OpenAI-Dienst übertragen. Die Jolpica-Attribution und die institutionellen Datenschutzvorgaben sind zu beachten. Das Projekt ist kein offizielles Formula-1-Produkt.

## 14. Reflexion und Ausblick

Nach der Evaluation sollten Fehlerfälle analysiert, das Korpus erweitert und alternative Modelle oder lokale Embeddings geprüft werden. **Konkrete Verbesserungen sind nach den Ergebnissen zu ergänzen.**

## 15. Pitchdeck mit acht Folien

1. Problem und Motivation; 2. Zielgruppe und Use Case; 3. Systemidee; 4. Tool Calling; 5. RAG und Daten; 6. Demo und Evaluation; 7. Risiken und Datenschutz; 8. Ergebnis und Ausblick.

## 16. Demo für 5 bis 10 Minuten

Zuerst eine geprüfte Siegerfrage, danach eine Wertungstabelle, anschließend eine Wissensfrage zu Punkten und schließlich eine absichtlich mehrdeutige Frage. Zum Schluss werden Quellen, Datenstand, Hybrid/Baseline und eine Korpus-Synchronisierung gezeigt.
