"""
LLM Provider Manager — shared utilities.

Exports the factory function and base class for all services to use.
"""

from shared.utils.llm_base import BaseLLMProvider
from shared.utils.llm_factory import get_llm_provider

__all__ = ["BaseLLMProvider", "get_llm_provider"]
