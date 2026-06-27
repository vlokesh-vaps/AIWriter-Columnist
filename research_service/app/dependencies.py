"""
Dependency injection for the Research Service.

Provides service layer instances configured with the active LLM provider.
"""

from functools import lru_cache

from shared.config import get_settings
from shared.utils import get_llm_provider

from research_service.app.services.service import ResearchService
from research_service.app.repositories.repository import ResearchRepository


@lru_cache()
def get_research_service() -> ResearchService:
    """
    Create and return a ResearchService instance with the configured LLM provider.

    Uses lru_cache to ensure a single instance per process.
    """
    settings = get_settings()
    llm_provider = get_llm_provider(settings)
    repository = ResearchRepository()
    return ResearchService(llm_provider=llm_provider, repository=repository)
