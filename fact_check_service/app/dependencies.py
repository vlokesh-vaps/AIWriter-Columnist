"""
Dependency injection for the Fact-Check Service.

Provides service layer instances configured with the active LLM provider.
"""

from functools import lru_cache

from shared.config import get_settings
from shared.utils import get_llm_provider

from fact_check_service.app.services.service import FactCheckService
from fact_check_service.app.repositories.repository import FactCheckRepository


@lru_cache()
def get_fact_check_service() -> FactCheckService:
    """
    Create and return a FactCheckService instance with the configured LLM provider.

    Uses lru_cache to ensure a single instance per process.
    """
    settings = get_settings()
    llm_provider = get_llm_provider(settings)
    repository = FactCheckRepository()
    return FactCheckService(llm_provider=llm_provider, repository=repository)
