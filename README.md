# Neo4j + Django Admin + LangChain Summaries

This project provides a Django admin experience for managing documentation while syncing each document to Neo4j and generating summaries with LangChain.

## Features

- **Django Admin** for CRUD on documentation.
- **Neo4j sync** on create/update/delete to keep graph data in sync.
- **LangChain summarization** with OpenAI models for concise summaries.
- **SOLID-friendly design** with repository and service layers.

## Architecture (SOLID)

- `docs/services/interfaces.py` defines contracts for repositories and summarizers.
- `Neo4jDocumentRepository` handles graph persistence (single responsibility).
- `OpenAISummarizer` handles only summarization.
- `DocumentService` orchestrates dependencies via constructor injection.

## Project Layout

```
neo4j_langchain_django/
  settings.py
  urls.py
  wsgi.py
  asgi.py
manage.py
docs/
  admin.py
  apps.py
  models.py
  signals.py
  services/
    document_service.py
    interfaces.py
    neo4j_repository.py
    summarizer.py
  management/commands/sync_neo4j.py
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
export DJANGO_SECRET_KEY="your-secret"
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="password"
export OPENAI_API_KEY="your-openai-key"
```

4. Run migrations:

```bash
python manage.py migrate
```

5. Create a superuser and start the server:

```bash
python manage.py createsuperuser
python manage.py runserver
```

6. Go to `/admin/` and manage documents.

## Neo4j Data Model

Each `Document` is synced as a `Document` node with properties:

- `document_id`
- `title`
- `content`
- `summary`
- `updated_at`

## Summarization

From Django admin, select documents and run **Summarize selected documents**. This will:

1. Call the LangChain `OpenAISummarizer`.
2. Store the summary back into the Django model.
3. Trigger the Neo4j sync via signals.

## Management Command

Resync all Django documents to Neo4j:

```bash
python manage.py sync_neo4j
```

## Notes

- The summarization requires a valid `OPENAI_API_KEY`.
- For large documents, adjust `SUMMARY_MAX_TOKENS`.
