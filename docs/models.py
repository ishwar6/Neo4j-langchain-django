from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
