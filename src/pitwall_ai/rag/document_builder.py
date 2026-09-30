"""Transform Jolpica responses into stable knowledge documents."""

import hashlib
import json
from typing import Any

from pitwall_ai.models import KnowledgeDocument


def stable_document_id(document_type: str, payload: dict[str, Any]) -> str:
    """Create a deterministic identifier from normalized document content."""
    # Stable IDs let repeated syncs update the same records instead of duplicating them.
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    digest = hashlib.sha256(f"{document_type}:{encoded}".encode()).hexdigest()[:20]
    return f"{document_type}-{digest}"


def build_documents(document_type: str, records: list[dict[str, Any]], endpoint: str, season: int | None = None) -> list[KnowledgeDocument]:
    """Create searchable documents with provenance metadata from API records."""
    documents: list[KnowledgeDocument] = []
    for record in records:
        race_name = record.get("raceName") or record.get("Circuit", {}).get("circuitName")
        document_id = stable_document_id(document_type, record)
        text = json.dumps(record, ensure_ascii=False, indent=2)
        metadata: dict[str, str | int | None] = {
            "data_type": document_type,
            "season": season,
            "race": race_name,
            "endpoint": endpoint,
            "document_id": document_id,
        }
        documents.append(KnowledgeDocument(document_id=document_id, text=text, metadata=metadata))
    return documents
