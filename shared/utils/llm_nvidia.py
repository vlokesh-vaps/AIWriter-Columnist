"""
NVIDIA NIM LLM Provider — uses raw HTTP requests via httpx.

NVIDIA NIM exposes an OpenAI-compatible REST API, so we use
the chat/completions endpoint directly.
"""

import logging
from typing import Any

import httpx

from shared.exceptions import LLMConnectionError, LLMResponseError
from shared.utils.llm_base import BaseLLMProvider

logger = logging.getLogger(__name__)


class NvidiaProvider(BaseLLMProvider):
    """LLM provider for NVIDIA NIM using direct HTTP requests."""

    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        """
        Initialize NvidiaProvider.

        Args:
            api_key: NVIDIA NIM API key.
            base_url: NVIDIA NIM base URL (e.g. https://integrate.api.nvidia.com/v1).
            model: Model name (e.g. meta/llama-3.1-8b-instruct).
        """
        if not api_key:
            raise ValueError("NVIDIA_API_KEY is required when using the NVIDIA provider")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        logger.info("NvidiaProvider initialized | url=%s | model=%s", self.base_url, self.model)

    async def generate(self, prompt: str) -> str:
        """
        Generate text using NVIDIA NIM's OpenAI-compatible endpoint.

        Args:
            prompt: Input prompt string.

        Returns:
            Generated text response.
        """
        url = f"{self.base_url}/chat/completions"
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 4096,
            "temperature": 0.7,
        }

        logger.debug("NVIDIA request | model=%s | prompt_length=%d", self.model, len(prompt))

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
        except httpx.ConnectError as exc:
            logger.error("NVIDIA connection failed: %s", exc)
            raise LLMConnectionError(provider="nvidia", detail=str(exc)) from exc
        except httpx.HTTPStatusError as exc:
            logger.error("NVIDIA HTTP error: %s", exc)
            raise LLMResponseError(provider="nvidia", detail=str(exc)) from exc
        except httpx.TimeoutException as exc:
            logger.error("NVIDIA request timed out: %s", exc)
            raise LLMConnectionError(provider="nvidia", detail="Request timed out") from exc

        try:
            data = response.json()
            text: str = data["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError) as exc:
            logger.error("NVIDIA response parse error: %s", exc)
            raise LLMResponseError(provider="nvidia", detail="Failed to parse response JSON") from exc

        if not text.strip():
            raise LLMResponseError(provider="nvidia", detail="Empty response received")

        logger.debug("NVIDIA response received | length=%d", len(text))
        return text.strip()
