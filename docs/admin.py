from django.contrib import admin, messages

from .models import Document
from .services.document_service import DocumentService
from .services.neo4j_repository import Neo4jDocumentRepository
from .services.summarizer import OpenAISummarizer


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")
    search_fields = ("title", "content")
    actions = ("summarize_documents",)
    readonly_fields = ("created_at", "updated_at")

    def summarize_documents(self, request, queryset):
        service = DocumentService(
            repository=Neo4jDocumentRepository(),
            summarizer=OpenAISummarizer(),
        )
        summarized = 0
        for document in queryset:
            try:
                document.summary = service.generate_summary(document.content)
                document.save(update_fields=["summary", "updated_at"])
                summarized += 1
            except ValueError as exc:
                self.message_user(request, str(exc), level=messages.ERROR)
                return
        self.message_user(request, f"Summarized {summarized} documents.")

    summarize_documents.short_description = "Summarize selected documents"
