# Data and Knowledge Corpus

Jolpica is the primary source for seasons, schedules, results, drivers, circuits, and standings. The API endpoint and retrieval timestamp are stored with every document. Raw responses remain in `data/raw/`; normalized JSON documents are in `data/processed/`.

Documents are currently record-sized rather than arbitrarily split. This preserves race and standings context and keeps provenance simple. Each item has a stable SHA-256-derived ID, data type, season, optional race, endpoint, and ID metadata. Chroma stores embeddings and documents under `data/vector_store/`.

OpenAI `text-embedding-3-small` is the default configured embedding model. Synchronization is repeatable because upsert uses stable IDs. Data quality remains dependent on API completeness, identifier matching, and the selected season range. Missing corpus data is reported rather than fabricated.
