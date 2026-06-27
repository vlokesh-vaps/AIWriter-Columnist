"""
Trend Agent — Generates future trend analysis.

This agent focuses on identifying and analyzing emerging trends
related to a topic. It uses the TREND_ANALYSIS_PROMPT template
and delegates text generation to the shared LLM provider.

It is one of several agents coordinated by the ColumnistAgent.
"""

import logging

from shared.utils.llm_base import BaseLLMProvider
from shared.prompts import TREND_ANALYSIS_PROMPT

logger = logging.getLogger(__name__)


class TrendAgent:
    """
    Agent that generates future trend analysis.

    Identifies 3-5 major trends for a topic and explains their
    expected impact over the next 3-5 years.
    """

    def __init__(self, llm_provider: BaseLLMProvider) -> None:
        """
        Initialize the TrendAgent.

        Args:
            llm_provider: The configured LLM provider instance.
        """
        self.llm = llm_provider

    async def analyze_trends(self, topic: str, research: str) -> str:
        """
        Generate a future trends analysis for the given topic.

        Steps:
        1. Fill in the TREND_ANALYSIS_PROMPT template.
        2. Send the prompt to the LLM.
        3. Return the generated analysis text.

        Args:
            topic: The subject to analyze trends for.
            research: Research data that grounds the predictions.

        Returns:
            The generated trend analysis text (string).
        """
        logger.info("TrendAgent analyzing trends | topic='%s'", topic)

        # Build the prompt from the template
        prompt = TREND_ANALYSIS_PROMPT.format(topic=topic, research=research)

        # Send to the LLM provider
        result = await self.llm.generate(prompt)

        logger.info(
            "TrendAgent complete | topic='%s' | length=%d",
            topic,
            len(result),
        )
        return result
