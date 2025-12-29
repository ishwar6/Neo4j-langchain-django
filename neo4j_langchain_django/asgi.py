"""ASGI config for neo4j_langchain_django project."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neo4j_langchain_django.settings")

application = get_asgi_application()
