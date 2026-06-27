"""
Dependency Injection for the AI Columnist Service.

Provides service layer instances configured with the active LLM provider.
FastAPI's Depends() system calls these functions to inject dependencies
into route handlers automatically.
"""

from functools import lru_cache

from shared.config import get_settings
from shared.utils import get_llm_provider

from app.services.service import ColumnistService


@lru_cache()
def get_columnist_service() -> ColumnistService:
    """
    Create and return a ColumnistService instance with the configured LLM provider.

    How it works:
    1. get_settings() reads the .env file and returns the Settings singleton.
    2. get_llm_provider() uses the LLM_PROVIDER setting to create the right
       provider (Ollama, Groq, Gemini, or NVIDIA).
    3. ColumnistService receives the provider and creates its sub-agents.

    Uses @lru_cache to ensure only one instance is created per process,
    which is the standard pattern across all services in this project.
    """
    settings = get_settings()
    llm_provider = get_llm_provider(settings)
    return ColumnistService(llm_provider=llm_provider)
