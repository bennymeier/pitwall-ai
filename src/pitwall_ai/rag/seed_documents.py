"""Curated local Formula 1 background knowledge."""

from pitwall_ai.models import KnowledgeDocument

SEED_DOCUMENTS = [
    ("concept-standings", "Die Fahrerwertung zählt die Punkte einzelner Fahrer. Die Konstrukteurswertung zählt die Punkte der beiden Fahrer eines Teams zusammen."),
    ("concept-points", "Im normalen Grand Prix erhalten die bestplatzierten Fahrer Punkte nach dem offiziellen Punkteschema. Sprint-Wochenenden haben ein zusätzliches Sprint-Rennen mit eigener Punktevergabe."),
    ("concept-qualifying", "Das Qualifying bestimmt die Startaufstellung. In drei Abschnitten scheiden Fahrer aus; die schnellste Runde entscheidet die jeweilige Position."),
    ("concept-sprint", "Ein Sprint ist ein kürzeres Rennen innerhalb ausgewählter Formel-1-Wochenenden. Er ergänzt den Grand Prix und kann eigene Meisterschaftspunkte vergeben."),
]


def get_seed_documents() -> list[KnowledgeDocument]:
    """Return stable local documents for core Formula 1 concepts."""
    return [
        KnowledgeDocument(
            document_id=document_id,
            text=text,
            metadata={"data_type": "background_knowledge", "source": "local-curated", "document_id": document_id},
        )
        for document_id, text in SEED_DOCUMENTS
    ]
