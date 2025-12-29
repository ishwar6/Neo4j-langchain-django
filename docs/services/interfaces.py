from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class DocumentPayload:
    document_id: int
    title: str
    content: str
    summary: str


class DocumentRepository(Protocol):
    def upsert(self, payload: DocumentPayload) -> None:
        ...

    def delete(self, document_id: int) -> None:
        ...


class DocumentSummarizer(Protocol):
    def summarize(self, content: str) -> str:
        ...
