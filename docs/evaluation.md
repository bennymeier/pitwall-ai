# Evaluation

## Research question

Does a hybrid assistant with verified tools and local retrieval answer German Formula 1 questions more accurately and traceably than a model-only baseline?

## Design

Run the 20 questions in `evaluation/questions.json` in Baseline and Hybrid modes. Tool ground truth is obtained from Jolpica during the run; no historical result is hard-coded as expected truth. Record routing, source presence, data-status presence, fact coverage, unsupported claims, errors, and latency.

Manual reviewers score factual correctness, completeness, traceability, source relation, understandability, and hallucination severity. Model-based judging may be used only as a supplement to human review and must not replace verified data comparison.

## Interpretation and limitations

Compare paired questions, aggregate by category, and inspect failures. API downtime, model version changes, incomplete prompts, and retrieval quality can influence results. The project does not claim general performance from this small educational benchmark. Actual scores must be added after execution.
