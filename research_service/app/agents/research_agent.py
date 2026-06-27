"""
Research Agent — Thin Orchestration Layer.

Delegates actual work to ResearchService. This class exists as an
extension point for future multi-agent workflows and complex orchestration.
"""

import logging

from app.services.service import ResearchService
from shared.schemas import ResearchResponse

logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    Research agent that orchestrates the research pipeline.

    Currently a thin wrapper around ResearchService. In future phases,
    this will coordinate multiple sub-agents (source discovery,
    statistics fetching, reference building).
    """

    def __init__(self, service: ResearchService) -> None:
        """
        Initialize the ResearchAgent.

        Args:
            service: The ResearchService instance for business logic.
        """
        self.service = service

    async def research(self, topic: str) -> ResearchResponse:
        """
        Execute the research pipeline for a topic.

        Args:
            topic: The topic to research.

        Returns:
            ResearchResponse with generated research data.
        """
        logger.info("ResearchAgent starting pipeline | topic='%s'", topic)
        result = await self.service.generate_research(topic=topic)
        logger.info("ResearchAgent pipeline complete | topic='%s'", topic)
        return result