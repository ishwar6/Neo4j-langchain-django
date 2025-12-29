from __future__ import annotations

from dataclasses import asdict

from django.conf import settings
from neo4j import GraphDatabase

from .interfaces import DocumentPayload, DocumentRepository


class Neo4jDocumentRepository(DocumentRepository):
    def __init__(self) -> None:
        self._uri = settings.NEO4J["URI"]
        self._user = settings.NEO4J["USER"]
        self._password = settings.NEO4J["PASSWORD"]

    def upsert(self, payload: DocumentPayload) -> None:
        query = """
        MERGE (doc:Document {document_id: $document_id})
        SET doc.title = $title,
            doc.content = $content,
            doc.summary = $summary,
            doc.updated_at = datetime()
        """
        params = asdict(payload)
        self._execute_write(query, params)

    def delete(self, document_id: int) -> None:
        query = "MATCH (doc:Document {document_id: $document_id}) DETACH DELETE doc"
        self._execute_write(query, {"document_id": document_id})

    def _execute_write(self, query: str, params: dict[str, object]) -> None:
        driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        try:
            with driver.session() as session:
                session.execute_write(lambda tx: tx.run(query, **params))
        finally:
            driver.close()
