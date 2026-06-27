"""
Opinion Agent — Generates the opinion article body.

This agent is responsible for a single task: taking a topic and
research data and producing an opinionated analysis article through
the LLM provider.

It is one of several agents coordinated by the ColumnistAgent.
"""

import logging

from shared.utils.llm_base import BaseLLMProvider
from shared.prompts import OPINION_ARTICLE_PROMPT

logger = logging.getLogger(__name__)


class OpinionAgent:
    """
    Agent that generates opinion-based analysis articles.

    Uses the OPINION_ARTICLE_PROMPT template and delegates the
    actual text generation to the injected LLM provider.
    """

    def __init__(self, llm_provider: BaseLLMProvider) -> None:
        """
        Initialize the OpinionAgent.

        Args:
            llm_provider: The configured LLM provider instance
                          (Ollama, Groq, Gemini, or NVIDIA).
        """
        self.llm = llm_provider

    async def generate_opinion(self, topic: str, research: str) -> str:
        """
        Generate an opinion article for the given topic.

        Steps:
        1. Fill in the OPINION_ARTICLE_PROMPT template with topic & research.
        2. Send the prompt to the LLM provider.
        3. Return the raw generated text.

        Args:
            topic: The subject to write about.
            research: Research data to base the opinion on.

        Returns:
            The generated opinion article text (string).
        """
        logger.info("OpinionAgent generating opinion | topic='%s'", topic)

        # Build the prompt by inserting topic and research into the template
        prompt = OPINION_ARTICLE_PROMPT.format(topic=topic, research=research)

        # Call the LLM provider — this works the same for every provider
        result = await self.llm.generate(prompt)

        logger.info(
            "OpinionAgent complete | topic='%s' | length=%d",
            topic,
            len(result),
        )
        return result
