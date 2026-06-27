"""
Ollama LLM Provider — uses raw HTTP requests via httpx.

Communicates with a local or remote Ollama server's REST API.
"""

import logging
from typing import Dict

import httpx

from shared.exceptions import LLMConnectionError, LLMResponseError
from shared.utils.llm_base import BaseLLMProvider

logger = logging.getLogger(__name__)


class OllamaProvider(BaseLLMProvider):
    """LLM provider for Ollama using direct HTTP requests."""

    def __init__(self, base_url: str, model: str) -> None:
        """
        Initialize OllamaProvider.

        Args:
            base_url: Ollama server URL (e.g. http://localhost:11434).
            model: Model name to use (e.g. llama3).
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        logger.info("OllamaProvider initialized | url=%s | model=%s", self.base_url, self.model)

    async def generate(self, prompt: str) -> str:
        """
        Generate text using Ollama's /api/chat endpoint.

        Args:
            prompt: Input prompt string.

        Returns:
            Generated text response.
        """
        url = f"{self.base_url}/api/chat"
        payload: dict = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        }

        logger.debug("Ollama request | model=%s | prompt_length=%d", self.model, len(prompt))

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
        except httpx.ConnectError as exc:
            logger.error("Ollama connection failed: %s", exc)
            raise LLMConnectionError(provider="ollama", detail=str(exc)) from exc
        except httpx.HTTPStatusError as exc:
            logger.error("Ollama HTTP error: %s", exc)
            raise LLMResponseError(provider="ollama", detail=str(exc)) from exc
        except httpx.TimeoutException as exc:
            logger.error("Ollama request timed out: %s", exc)
            raise LLMConnectionError(provider="ollama", detail="Request timed out") from exc

        try:
            data = response.json()
            # /api/chat returns {"message": {"role": "assistant", "content": "..."}}
            message = data.get("message", {})
            text: str = message.get("content", "")
        except (ValueError, KeyError) as exc:
            logger.error("Ollama response parse error: %s", exc)
            raise LLMResponseError(provider="ollama", detail="Failed to parse response JSON") from exc

        if not text.strip():
            raise LLMResponseError(provider="ollama", detail="Empty response received")

        logger.debug("Ollama response received | length=%d", len(text))
        return text.strip()

