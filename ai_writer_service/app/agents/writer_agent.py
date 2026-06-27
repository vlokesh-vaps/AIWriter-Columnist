"""
Writer Agent — Thin Orchestration Layer.

Delegates to WriterService. This class replaces the old Ollama-coupled
implementation with a provider-agnostic approach.
"""

import logging

from app.services.service import WriterService
from shared.schemas import WriterResponse

logger = logging.getLogger(__name__)


class WriterAgent:
    """
    Writer agent that orchestrates the article generation pipeline.

    Currently a thin wrapper around WriterService. In future phases,
    this will coordinate multiple sub-agents (headline, SEO, etc.).
    """

    def __init__(self, service: WriterService) -> None:
        """
        Initialize the WriterAgent.

        Args:
            service: The WriterService instance for business logic.
        """
        self.service = service

    async def generate(self, topic: str, research: str) -> WriterResponse:
        """
        Execute the article generation pipeline.

        Args:
            topic: The article topic.
            research: Research notes to base the article on.

        Returns:
            WriterResponse with generated content.
        """
        logger.info("WriterAgent starting pipeline | topic='%s'", topic)
        result = await self.service.generate_article(topic=topic, research=research)
        logger.info("WriterAgent pipeline complete | topic='%s'", topic)
        return result