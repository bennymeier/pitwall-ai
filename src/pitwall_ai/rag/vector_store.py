"""Optional Chroma-backed vector store."""

from pathlib import Path
from typing import Any

from pitwall_ai.models import KnowledgeDocument, SearchResult


class VectorStore:
    """Persist and search corpus documents with Chroma when initialized."""

    def __init__(self, path: Path, embedding_function: Any = None) -> None:
        """Initialize a persistent store without requiring one to exist."""
        self._collection = None
        # The corpus is optional, so a missing Chroma setup should not block API-backed chat.
        try:
            import chromadb
            from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

            client = chromadb.PersistentClient(path=str(path))
            function = embedding_function or OpenAIEmbeddingFunction(
                api_key=None, model_name="text-embedding-3-small"
            )
            self._collection = client.get_or_create_collection("pitwall_knowledge", embedding_function=function)
        except Exception:
            self._collection = None

    @property
    def available(self) -> bool:
        """Return whether the persistent collection is usable."""
        return self._collection is not None and self._collection.count() > 0

    def upsert(self, documents: list[KnowledgeDocument]) -> None:
        """Insert or replace documents by their stable identifiers."""
        if self._collection is None:
            raise RuntimeError("The vector store is not initialized.")
        self._collection.upsert(
            ids=[document.document_id for document in documents],
            documents=[document.text for document in documents],
            metadatas=[document.metadata for document in documents],
        )

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        """Search the corpus and return bounded, untrusted context."""
        if self._collection is None:
            return []
        result = self._collection.query(query_texts=[query], n_results=min(limit, 10))
        texts = result.get("documents", [[]])[0]
        metadata = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        return [SearchResult(text=text, metadata=meta, distance=distance) for text, meta, distance in zip(texts, metadata, distances)]
