"""
Columnist Agent — Top-Level Orchestrator.

Coordinates the full opinion article generation pipeline by
delegating to specialised sub-agents:

  1. OpinionAgent  → opinion article body
  2. TrendAgent    → future trends analysis

The ColumnistAgent itself does NOT call the LLM directly.
Instead, it assembles the final ColumnistResponse from the
outputs of its sub-agents and the ColumnistService (which
handles pros/cons, recommendations, and headline).

Think of it as the "conductor" of the columnist orchestra.
"""

import logging

from shared.schemas import ColumnistResponse
from app.services.service import ColumnistService

logger = logging.getLogger(__name__)


class ColumnistAgent:
    """
    Top-level agent that orchestrates the opinion article pipeline.

    Delegates business logic to ColumnistService, which internally
    coordinates the OpinionAgent, TrendAgent, and LLM calls for
    structured data (pros/cons, recommendations, headline).
    """

    def __init__(self, service: ColumnistService) -> None:
        """
        Initialize the ColumnistAgent.

        Args:
            service: The ColumnistService that contains all business logic.
        """
        self.service = service

    async def generate(self, topic: str, research: str) -> ColumnistResponse:
        """
        Execute the full columnist pipeline.

        This is the single entry point called by the route handler.
        It delegates everything to the service layer and returns
        the assembled response.

        Args:
            topic: The subject for the opinion article.
            research: Research data from the Research Service.

        Returns:
            ColumnistResponse with headline, opinion article,
            future trends, pros, cons, and recommendations.
        """
        logger.info("ColumnistAgent starting pipeline | topic='%s'", topic)

        # Delegate to the service layer (which coordinates sub-agents)
        result = await self.service.generate_column(topic=topic, research=research)

        logger.info("ColumnistAgent pipeline complete | topic='%s'", topic)
        return result
