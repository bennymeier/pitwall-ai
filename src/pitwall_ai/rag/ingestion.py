"""Synchronize Jolpica data into raw, processed, and vector storage."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pitwall_ai.api.jolpica_client import JolpicaClient
from pitwall_ai.rag.document_builder import build_documents
from pitwall_ai.rag.seed_documents import get_seed_documents
from pitwall_ai.rag.vector_store import VectorStore


def sync_season(client: JolpicaClient, season: int, raw_path: Path, processed_path: Path, store: VectorStore) -> int:
    """Synchronize a season schedule and standings into local storage."""
    schedule = client.get_season_schedule(str(season))
    standings = client.get_driver_standings(str(season))
    payload: dict[str, Any] = {"retrieved_at": datetime.now(timezone.utc).isoformat(), "schedule": schedule, "standings": standings}
    # Keep the original API payload separate from the smaller searchable documents.
    raw_path.mkdir(parents=True, exist_ok=True)
    processed_path.mkdir(parents=True, exist_ok=True)
    (raw_path / f"{season}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    documents = build_documents("schedule", schedule, f"{client.base_url}/{season}.json", season)
    documents += build_documents("driver_standings", standings, f"{client.base_url}/{season}/driverstandings.json", season)
    documents += get_seed_documents()
    for document in documents:
        (processed_path / f"{document.document_id}.json").write_text(document.model_dump_json(indent=2), encoding="utf-8")
    if documents:
        store.upsert(documents)
    return len(documents)
