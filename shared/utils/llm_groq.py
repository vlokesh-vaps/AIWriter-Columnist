"""
Groq LLM Provider — uses the official Groq SDK.

The Groq SDK follows the OpenAI client pattern with async support.
"""

import logging

from shared.exceptions import LLMConnectionError, LLMResponseError
from shared.utils.llm_base import BaseLLMProvider

logger = logging.getLogger(__name__)


class GroqProvider(BaseLLMProvider):
    """LLM provider for Groq using the official groq SDK."""

    def __init__(self, api_key: str, model: str) -> None:
        """
        Initialize GroqProvider.

        Args:
            api_key: Groq API key.
            model: Model name (e.g. llama-3.3-70b-versatile).
        """
        if not api_key:
            raise ValueError("GROQ_API_KEY is required when using the Groq provider")

        self.api_key = api_key
        self.model = model
        logger.info("GroqProvider initialized | model=%s", self.model)

    async def generate(self, prompt: str) -> str:
        """
        Generate text using the Groq SDK.

        Args:
            prompt: Input prompt string.

        Returns:
            Generated text response.
        """
        # Import here to avoid import errors when Groq is not the active provider
        try:
            from groq import AsyncGroq
        except ImportError as exc:
            raise LLMConnectionError(
                provider="groq",
                detail="groq package is not installed. Run: pip install groq",
            ) from exc

        logger.debug("Groq request | model=%s | prompt_length=%d", self.model, len(prompt))

        try:
            client = AsyncGroq(api_key=self.api_key)
            chat_completion = await client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
            )
        except Exception as exc:
            logger.error("Groq API error: %s", exc)
            raise LLMConnectionError(provider="groq", detail=str(exc)) from exc

        try:
            text: str = chat_completion.choices[0].message.content or ""
        except (IndexError, AttributeError) as exc:
            logger.error("Groq response parse error: %s", exc)
            raise LLMResponseError(provider="groq", detail="Failed to parse response") from exc

        if not text.strip():
            raise LLMResponseError(provider="groq", detail="Empty response received")

        logger.debug("Groq response received | length=%d", len(text))
        return text.strip()
