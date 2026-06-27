"""
Dependency injection for the AI Writer Service.

Provides service layer instances configured with the active LLM provider.
"""

from functools import lru_cache

from shared.config import get_settings
from shared.utils import get_llm_provider

from app.services.service import WriterService
from app.repositories.repository import ArticleRepository


@lru_cache()
def get_writer_service() -> WriterService:
    """
    Create and return a WriterService instance with the configured LLM provider.

    Uses lru_cache to ensure a single instance per process.
    """
    settings = get_settings()
    llm_provider = get_llm_provider(settings)
    repository = ArticleRepository()
    return WriterService(llm_provider=llm_provider, repository=repository)
