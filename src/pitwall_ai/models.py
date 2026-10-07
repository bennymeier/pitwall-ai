"""Shared typed domain models."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class SourceMetadata(BaseModel):
    """Describe where a result or knowledge document came from."""

    source_type: Literal["api", "knowledge_base", "model"]
    endpoint: str = ""
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)
    document_id: str | None = None


class ToolResult(BaseModel):
    """Represent a safe, structured tool response."""

    success: bool
    data: Any = None
    error: str | None = None
    source: SourceMetadata


class KnowledgeDocument(BaseModel):
    """Represent one searchable corpus document."""

    document_id: str
    text: str
    metadata: dict[str, str | int | float | None]


class SearchResult(BaseModel):
    """Represent one semantic search hit."""

    text: str
    metadata: dict[str, Any]
    distance: float | None = None
