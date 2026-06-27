"""
Fact-Check Service — Business Logic Layer.

Validates articles by sending them through the LLM provider
for consistency checks, date/number verification, and confidence scoring.
"""

import json
import logging
import re

from shared.prompts import FACT_CHECK_PROMPT
from shared.schemas import FactCheckResponse
from shared.exceptions import LLMResponseError
from shared.utils.llm_base import BaseLLMProvider

from fact_check_service.app.repositories.repository import FactCheckRepository

logger = logging.getLogger(__name__)


class FactCheckService:
    """
    Core business logic for article fact-checking.

    Uses the injected LLM provider to verify articles and
    produce structured verification reports.
    """

    def __init__(
        self,
        llm_provider: BaseLLMProvider,
        repository: FactCheckRepository,
    ) -> None:
        """
        Initialize FactCheckService.

        Args:
            llm_provider: The configured LLM provider instance.
            repository: Repository for future data persistence.
        """
        self.llm = llm_provider
        self.repository = repository

    async def verify_article(self, article: str, topic: str) -> FactCheckResponse:
        """
        Verify the factual accuracy of an article.

        Sends the article through the LLM with a structured fact-check
        prompt and parses the JSON response into a FactCheckResponse.

        Args:
            article: The full article text to verify.
            topic: The article topic for context.

        Returns:
            FactCheckResponse with status, confidence score, issues, and recommendations.
        """
        logger.info("Starting fact-check | topic='%s' | article_length=%d", topic, len(article))

        # Generate verification via LLM
        prompt = FACT_CHECK_PROMPT.format(topic=topic, article=article)
        raw_response = await self.llm.generate(prompt)
        logger.debug("Raw fact-check response | length=%d", len(raw_response))

        # Parse the structured JSON response
        response = self._parse_verification_response(raw_response)

        # Placeholder: persist to database in future phases
        # await self.repository.save(response)

        return response

    def _parse_verification_response(self, raw_response: str) -> FactCheckResponse:
        """
        Parse the LLM's JSON response into a FactCheckResponse.

        Handles potential formatting issues (markdown code blocks, etc.)
        with fallback defaults.

        Args:
            raw_response: The raw text from the LLM.

        Returns:
            Parsed FactCheckResponse.

        Raises:
            LLMResponseError: If the response cannot be parsed at all.
        """
        # Strip markdown code block wrappers if present
        cleaned = raw_response.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            logger.warning(
                "Failed to parse fact-check JSON, using fallback | error=%s",
                exc,
            )
            # Fallback: return a conservative response
            return FactCheckResponse(
                status="flagged",
                confidence_score=50,
                issues=["Unable to parse detailed verification results from LLM"],
                recommendations=[
                    "Manual review recommended",
                    "Consider re-running the fact-check",
                ],
            )

        # Validate and clamp values
        confidence = data.get("confidence_score", 50)
        if not isinstance(confidence, (int, float)):
            confidence = 50
        confidence = max(0, min(100, int(confidence)))

        status = data.get("status", "flagged")
        if status not in ("verified", "flagged", "rejected"):
            # Derive from confidence score
            if confidence >= 80:
                status = "verified"
            elif confidence >= 50:
                status = "flagged"
            else:
                status = "rejected"

        issues = data.get("issues", [])
        if not isinstance(issues, list):
            issues = []

        recommendations = data.get("recommendations", [])
        if not isinstance(recommendations, list):
            recommendations = []

        return FactCheckResponse(
            status=status,
            confidence_score=confidence,
            issues=[str(i) for i in issues],
            recommendations=[str(r) for r in recommendations],
        )
