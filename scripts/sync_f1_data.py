"""Synchronize configured Formula 1 seasons."""

from pathlib import Path

from pitwall_ai.api.jolpica_client import JolpicaClient
from pitwall_ai.config import get_settings
from pitwall_ai.rag.ingestion import sync_season
from pitwall_ai.rag.vector_store import VectorStore


def main() -> None:
    """Run the configured synchronization."""
    settings = get_settings()
    end = int(settings.f1_end_season) if settings.f1_end_season != "current" else 2026
    with JolpicaClient(settings.jolpica_base_url) as client:
        store = VectorStore(settings.chroma_path)
        for season in range(settings.f1_start_season, end + 1):
            count = sync_season(client, season, Path("data/raw"), Path("data/processed"), store)
            print(f"Synchronized {season}: {count} documents")


if __name__ == "__main__":
    main()
