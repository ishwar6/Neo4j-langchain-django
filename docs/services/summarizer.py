from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .interfaces import DocumentSummarizer


@dataclass(frozen=True)
class OpenAISummarizer(DocumentSummarizer):
    def summarize(self, content: str) -> str:
        api_key = settings.LANGCHAIN["OPENAI_API_KEY"]
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for summarization.")

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You summarize documentation for internal knowledge bases. "
                    "Keep summaries concise, actionable, and in plain language.",
                ),
                ("human", "Summarize the following documentation:\n\n{content}"),
            ]
        )
        model = ChatOpenAI(
            api_key=api_key,
            model=settings.LANGCHAIN["MODEL_NAME"],
            max_tokens=settings.LANGCHAIN["MAX_TOKENS"],
            temperature=0.2,
        )
        chain = prompt | model
        response = chain.invoke({"content": content})
        return response.content.strip()
