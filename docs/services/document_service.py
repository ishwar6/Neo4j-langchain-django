from __future__ import annotations

from dataclasses import dataclass

from .interfaces import DocumentPayload, DocumentRepository, DocumentSummarizer


@dataclass
class DocumentService:
    repository: DocumentRepository
    summarizer: DocumentSummarizer

    def sync_to_neo4j(self, payload: DocumentPayload) -> None:
        self.repository.upsert(payload)

    def remove_from_neo4j(self, document_id: int) -> None:
        self.repository.delete(document_id)

    def generate_summary(self, content: str) -> str:
        return self.summarizer.summarize(content)
