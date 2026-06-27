"""
Gemini LLM Provider — uses the official Google GenAI SDK.

Uses the google-genai package for async interaction with Gemini models.
"""

import logging

from shared.exceptions import LLMConnectionError, LLMResponseError
from shared.utils.llm_base import BaseLLMProvider

logger = logging.getLogger(__name__)


class GeminiProvider(BaseLLMProvider):
    """LLM provider for Google Gemini using the google-genai SDK."""

    def __init__(self, api_key: str, model: str) -> None:
        """
        Initialize GeminiProvider.

        Args:
            api_key: Google Gemini API key.
            model: Model name (e.g. gemini-2.0-flash).
        """
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required when using the Gemini provider")

        self.api_key = api_key
        self.model = model
        logger.info("GeminiProvider initialized | model=%s", self.model)

    async def generate(self, prompt: str) -> str:
        """
        Generate text using the Google GenAI SDK.

        Args:
            prompt: Input prompt string.

        Returns:
            Generated text response.
        """
        try:
            from google import genai
        except ImportError as exc:
            raise LLMConnectionError(
                provider="gemini",
                detail="google-genai package is not installed. Run: pip install google-genai",
            ) from exc

        logger.debug("Gemini request | model=%s | prompt_length=%d", self.model, len(prompt))

        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
        except Exception as exc:
            logger.error("Gemini API error: %s", exc)
            raise LLMConnectionError(provider="gemini", detail=str(exc)) from exc

        try:
            text: str = response.text or ""
        except (AttributeError, ValueError) as exc:
            logger.error("Gemini response parse error: %s", exc)
            raise LLMResponseError(provider="gemini", detail="Failed to parse response") from exc

        if not text.strip():
            raise LLMResponseError(provider="gemini", detail="Empty response received")

        logger.debug("Gemini response received | length=%d", len(text))
        return text.strip()
