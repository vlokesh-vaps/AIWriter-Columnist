"""
LLM Provider Factory.

Routes LLM requests to the configured provider based on the
LLM_PROVIDER environment variable. This is the single entry point
for obtaining an LLM provider instance.
"""

import logging

from shared.config import Settings
from shared.utils.llm_base import BaseLLMProvider

logger = logging.getLogger(__name__)

# Supported provider identifiers
_SUPPORTED_PROVIDERS = {"ollama", "groq", "gemini", "nvidia"}


def get_llm_provider(settings: Settings) -> BaseLLMProvider:
    """
    Factory function that returns the configured LLM provider.

    Reads `settings.LLM_PROVIDER` and instantiates the corresponding
    provider class with credentials from the settings.

    Args:
        settings: Application settings instance.

    Returns:
        A concrete BaseLLMProvider implementation.

    Raises:
        ValueError: If the provider name is not supported.
    """
    provider_name = settings.LLM_PROVIDER.lower()

    if provider_name not in _SUPPORTED_PROVIDERS:
        raise ValueError(
            f"Unsupported LLM provider: '{provider_name}'. "
            f"Supported: {', '.join(sorted(_SUPPORTED_PROVIDERS))}"
        )

    logger.info("Initializing LLM provider: %s", provider_name)

    if provider_name == "groq":
        from shared.utils.llm_groq import GroqProvider
        return GroqProvider(
            api_key=settings.GROQ_API_KEY or "",
            model=settings.GROQ_MODEL,
        )

    elif provider_name == "ollama":
        from shared.utils.llm_ollama import OllamaProvider
        return OllamaProvider(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
        )

    elif provider_name == "gemini":
        from shared.utils.llm_gemini import GeminiProvider
        return GeminiProvider(
            api_key=settings.GEMINI_API_KEY or "",
            model=settings.GEMINI_MODEL,
        )

    elif provider_name == "nvidia":
        from shared.utils.llm_nvidia import NvidiaProvider
        return NvidiaProvider(
            api_key=settings.NVIDIA_API_KEY or "",
            base_url=settings.NVIDIA_BASE_URL,
            model=settings.NVIDIA_MODEL,
        )

    # This should never be reached due to the check above
    raise ValueError(f"Unsupported LLM provider: '{provider_name}'")
