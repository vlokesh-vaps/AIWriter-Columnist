"""
Abstract base class for all LLM providers.

Every provider implementation must inherit from BaseLLMProvider
and implement the `generate` method. The rest of the application
must ONLY interact with LLMs through this interface.
"""

from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """
    Abstract base class defining the contract for LLM providers.

    All LLM calls in the platform go through this interface,
    ensuring provider-agnostic code in services and agents.
    """

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """
        Generate a text response from the LLM.

        Args:
            prompt: The input prompt string to send to the LLM.

        Returns:
            The generated text response as a string.

        Raises:
            LLMConnectionError: If the provider cannot be reached.
            LLMResponseError: If the provider returns an invalid response.
        """
        ...
