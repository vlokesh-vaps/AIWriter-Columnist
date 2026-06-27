"""
AI Columnist Service — Business Logic Layer.

Orchestrates the full opinion article generation pipeline:

  1. Generate headline          (LLM call)
  2. Generate opinion article   (via OpinionAgent)
  3. Generate future trends     (via TrendAgent)
  4. Extract pros and cons      (LLM call → JSON parse)
  5. Extract recommendations    (LLM call → JSON parse)

All LLM interaction goes through the shared BaseLLMProvider interface,
so the service works identically with Ollama, Groq, Gemini, or NVIDIA.
"""

import json
import logging
from typing import List

from shared.prompts import (
    COLUMNIST_HEADLINE_PROMPT,
    PROS_CONS_PROMPT,
    RECOMMENDATIONS_PROMPT,
)
from shared.schemas import ColumnistResponse
from shared.utils.llm_base import BaseLLMProvider

from app.agents.opinion_agent import OpinionAgent
from app.agents.trend_agent import TrendAgent

logger = logging.getLogger(__name__)


# ── Helper: Safe JSON Parsing ─────────────────────────────────────────────

def _parse_json_safely(raw_text: str, fallback_key: str) -> dict:
    """
    Try to parse JSON from raw LLM output.

    LLMs sometimes wrap their JSON in markdown code fences (```json … ```)
    or add extra text. This helper strips common wrappers before parsing.

    Args:
        raw_text: The raw string returned by the LLM.
        fallback_key: If parsing fails, return {fallback_key: [raw_text]}.

    Returns:
        Parsed dict, or a fallback dict with the raw text.
    """
    # Strip leading/trailing whitespace
    text = raw_text.strip()

    # Remove markdown code fences if present (```json ... ```)
    if text.startswith("```"):
        # Find the end of the opening fence line
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1:]
        # Remove closing fence
        if text.endswith("```"):
            text = text[:-3].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        logger.warning(
            "Failed to parse JSON from LLM output. "
            "Using raw text as fallback | key='%s'",
            fallback_key,
        )
        # Return the raw text wrapped in a list so callers always get a list
        return {fallback_key: [text]}


# ── Service Class ─────────────────────────────────────────────────────────

class ColumnistService:
    """
    Core business logic for opinion article generation.

    Coordinates two sub-agents (OpinionAgent, TrendAgent) and makes
    additional LLM calls for structured data extraction (headline,
    pros/cons, recommendations).
    """

    def __init__(self, llm_provider: BaseLLMProvider) -> None:
        """
        Initialize the ColumnistService and its sub-agents.

        Args:
            llm_provider: The configured LLM provider instance.
        """
        self.llm = llm_provider

        # Create sub-agents — each gets the same LLM provider
        self.opinion_agent = OpinionAgent(llm_provider)
        self.trend_agent = TrendAgent(llm_provider)

        logger.info("ColumnistService initialized with sub-agents")

    # ── Main Pipeline ─────────────────────────────────────────────────────

    async def generate_column(
        self, topic: str, research: str
    ) -> ColumnistResponse:
        """
        Run the full columnist pipeline and return the assembled response.

        Pipeline steps (run sequentially to stay beginner-friendly):
          1. Headline
          2. Opinion article  (via OpinionAgent)
          3. Future trends    (via TrendAgent)
          4. Pros and cons    (direct LLM call → JSON parse)
          5. Recommendations  (direct LLM call → JSON parse)

        Args:
            topic: The article topic.
            research: Research data from the Research Service.

        Returns:
            ColumnistResponse with all generated content.
        """
        logger.info("Starting columnist pipeline | topic='%s'", topic)

        # ── Step 1: Generate headline ─────────────────────────────────────
        headline = await self._generate_headline(topic, research)
        logger.debug("Headline generated: '%s'", headline[:100])

        # ── Step 2: Generate opinion article (delegate to OpinionAgent) ───
        opinion_article = await self.opinion_agent.generate_opinion(
            topic, research
        )
        logger.debug("Opinion article generated | length=%d", len(opinion_article))

        # ── Step 3: Generate future trends (delegate to TrendAgent) ───────
        future_trends = await self.trend_agent.analyze_trends(topic, research)
        logger.debug("Future trends generated | length=%d", len(future_trends))

        # ── Step 4: Extract pros and cons ─────────────────────────────────
        pros, cons = await self._generate_pros_cons(topic, research)
        logger.debug("Pros=%d, Cons=%d", len(pros), len(cons))

        # ── Step 5: Extract recommendations ───────────────────────────────
        recommendations = await self._generate_recommendations(topic, research)
        logger.debug("Recommendations=%d", len(recommendations))

        # ── Assemble the response ─────────────────────────────────────────
        response = ColumnistResponse(
            headline=headline,
            opinion_article=opinion_article,
            future_trends=future_trends,
            pros=pros,
            cons=cons,
            recommendations=recommendations,
        )

        logger.info("Columnist pipeline complete | topic='%s'", topic)
        return response

    # ── Private Helper Methods ────────────────────────────────────────────

    async def _generate_headline(self, topic: str, research: str) -> str:
        """Generate a headline using the COLUMNIST_HEADLINE_PROMPT."""
        prompt = COLUMNIST_HEADLINE_PROMPT.format(
            topic=topic, research=research
        )
        return await self.llm.generate(prompt)

    async def _generate_pros_cons(
        self, topic: str, research: str
    ) -> tuple[List[str], List[str]]:
        """
        Generate pros and cons lists by prompting the LLM for JSON.

        Returns:
            A tuple of (pros_list, cons_list).
        """
        prompt = PROS_CONS_PROMPT.format(topic=topic, research=research)
        raw = await self.llm.generate(prompt)

        # Parse the JSON response
        data = _parse_json_safely(raw, fallback_key="pros")
        pros = data.get("pros", ["No pros could be generated"])
        cons = data.get("cons", ["No cons could be generated"])

        return pros, cons

    async def _generate_recommendations(
        self, topic: str, research: str
    ) -> List[str]:
        """
        Generate a list of recommendations by prompting the LLM for JSON.

        Returns:
            A list of recommendation strings.
        """
        prompt = RECOMMENDATIONS_PROMPT.format(topic=topic, research=research)
        raw = await self.llm.generate(prompt)

        # Parse the JSON response
        data = _parse_json_safely(raw, fallback_key="recommendations")
        return data.get("recommendations", ["No recommendations could be generated"])
