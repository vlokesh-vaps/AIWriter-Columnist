"""
Research Service — Business Logic Layer.

Handles research generation by orchestrating LLM calls through
the provider manager. Never calls LLM APIs directly.
"""

import logging

from shared.prompts import RESEARCH_PROMPT, REFERENCES_PROMPT
from shared.schemas import ResearchResponse
from shared.utils.llm_base import BaseLLMProvider

from app.repositories.repository import ResearchRepository

logger = logging.getLogger(__name__)


class ResearchService:
    """
    Core business logic for research generation.

    Uses the injected LLM provider to generate research notes
    and references for a given topic.
    """

    def __init__(
        self,
        llm_provider: BaseLLMProvider,
        repository: ResearchRepository,
    ) -> None:
        """
        Initialize ResearchService.

        Args:
            llm_provider: The configured LLM provider instance.
            repository: Repository for future data persistence.
        """
        self.llm = llm_provider
        self.repository = repository

    async def generate_research(self, topic: str) -> ResearchResponse:
        """
        Generate comprehensive research for a given topic.

        Performs two LLM calls:
        1. Generate research notes and analysis.
        2. Generate a list of references.

        Args:
            topic: The topic to research.

        Returns:
            ResearchResponse with research notes and references.
        """
        logger.info("Generating research | topic='%s'", topic)

        # Step 1: Generate research notes
        research_prompt = RESEARCH_PROMPT.format(topic=topic)
        research_text = await self.llm.generate(research_prompt)
        logger.debug("Research notes generated | length=%d", len(research_text))

        # Step 2: Generate references
        references_prompt = REFERENCES_PROMPT.format(topic=topic)
        references_text = await self.llm.generate(references_prompt)
        references = [
            ref.strip()
            for ref in references_text.strip().split("\n")
            if ref.strip()
        ]
        logger.debug("References generated | count=%d", len(references))

        # Build response
        response = ResearchResponse(
            topic=topic,
            research=research_text,
            references=references,
        )

        # Placeholder: persist to database in future phases
        # await self.repository.save(response)

        return response
