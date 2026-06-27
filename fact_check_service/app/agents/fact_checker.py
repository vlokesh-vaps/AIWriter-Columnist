"""
Fact-Checker Agent — Thin Orchestration Layer.

Delegates to FactCheckService. This class replaces the old Ollama-coupled
implementation with a provider-agnostic approach.
"""

import logging

from fact_check_service.app.services.service import FactCheckService
from shared.schemas import FactCheckResponse

logger = logging.getLogger(__name__)


class FactChecker:
    """
    Fact-checker agent that orchestrates the verification pipeline.

    Currently a thin wrapper around FactCheckService. In future phases,
    this will coordinate multiple verification sub-agents.
    """

    def __init__(self, service: FactCheckService) -> None:
        """
        Initialize the FactChecker.

        Args:
            service: The FactCheckService instance for business logic.
        """
        self.service = service

    async def verify(self, article: str, topic: str) -> FactCheckResponse:
        """
        Execute the fact-check pipeline for an article.

        Args:
            article: The article text to verify.
            topic: The article topic for context.

        Returns:
            FactCheckResponse with verification results.
        """
        logger.info("FactChecker starting pipeline | topic='%s'", topic)
        result = await self.service.verify_article(article=article, topic=topic)
        logger.info("FactChecker pipeline complete | topic='%s' | status=%s", topic, result.status)
        return result