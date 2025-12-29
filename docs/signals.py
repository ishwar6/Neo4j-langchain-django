from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Document
from .services.document_service import DocumentService
from .services.interfaces import DocumentPayload
from .services.neo4j_repository import Neo4jDocumentRepository
from .services.summarizer import OpenAISummarizer


def _service() -> DocumentService:
    return DocumentService(
        repository=Neo4jDocumentRepository(),
        summarizer=OpenAISummarizer(),
    )


@receiver(post_save, sender=Document)
def sync_document(sender: type[Document], instance: Document, **kwargs: object) -> None:
    payload = DocumentPayload(
        document_id=instance.id,
        title=instance.title,
        content=instance.content,
        summary=instance.summary,
    )
    _service().sync_to_neo4j(payload)


@receiver(post_delete, sender=Document)
def delete_document(sender: type[Document], instance: Document, **kwargs: object) -> None:
    if instance.id:
        _service().remove_from_neo4j(instance.id)
