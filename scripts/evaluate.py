"""Create an evaluation CSV template without inventing ground truth."""

import csv
import json
from pathlib import Path


def main() -> None:
    """Write one row per evaluation question for later execution."""
    questions = json.loads(Path("evaluation/questions.json").read_text(encoding="utf-8"))
    output = Path("evaluation/results/evaluation.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["id", "mode", "routing_correct", "source_present", "data_status_present", "facts_present", "unsupported_claims", "error", "latency_seconds", "manual_correctness", "manual_completeness", "manual_traceability", "manual_understandability", "manual_hallucination"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for question in questions:
            for mode in ("Baseline", "Hybrid"):
                writer.writerow({"id": question["id"], "mode": mode})
    print(f"Created evaluation template: {output}")


if __name__ == "__main__":
    main()
