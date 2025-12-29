from django.core.management.base import BaseCommand

from docs.models import Document
from docs.services.document_service import DocumentService
from docs.services.interfaces import DocumentPayload
from docs.services.neo4j_repository import Neo4jDocumentRepository
from docs.services.summarizer import OpenAISummarizer


class Command(BaseCommand):
    help = "Sync all documents from Django to Neo4j."

    def handle(self, *args, **options):
        service = DocumentService(
            repository=Neo4jDocumentRepository(),
            summarizer=OpenAISummarizer(),
        )
        count = 0
        for document in Document.objects.all():
            payload = DocumentPayload(
                document_id=document.id,
                title=document.title,
                content=document.content,
                summary=document.summary,
            )
            service.sync_to_neo4j(payload)
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Synced {count} documents to Neo4j."))
