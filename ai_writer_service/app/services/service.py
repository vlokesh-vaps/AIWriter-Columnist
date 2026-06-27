"""
AI Writer Service — Business Logic Layer.

Orchestrates the article generation pipeline through the LLM provider:
headline → article → summary → SEO title → meta description.
"""

import logging

from shared.prompts import (
    HEADLINE_PROMPT,
    ARTICLE_PROMPT,
    SUMMARY_PROMPT,
    SEO_TITLE_PROMPT,
    META_DESCRIPTION_PROMPT,
)
from shared.schemas import WriterResponse
from shared.utils.llm_base import BaseLLMProvider

from app.repositories.repository import ArticleRepository

logger = logging.getLogger(__name__)


class WriterService:
    """
    Core business logic for article generation.

    Runs a sequential pipeline of LLM calls to produce a complete
    article package. All LLM interaction goes through the provider manager.
    """

    def __init__(
        self,
        llm_provider: BaseLLMProvider,
        repository: ArticleRepository,
    ) -> None:
        """
        Initialize WriterService.

        Args:
            llm_provider: The configured LLM provider instance.
            repository: Repository for future data persistence.
        """
        self.llm = llm_provider
        self.repository = repository

    async def generate_article(self, topic: str, research: str) -> WriterResponse:
        """
        Generate a complete article package from topic and research.

        Pipeline:
        1. Generate headline
        2. Generate article body
        3. Generate summary
        4. Generate SEO title
        5. Generate meta description

        Args:
            topic: The article topic.
            research: Research notes to base the article on.

        Returns:
            WriterResponse with all generated content.
        """
        logger.info("Starting article generation pipeline | topic='%s'", topic)

        # Step 1: Generate headline
        headline_prompt = HEADLINE_PROMPT.format(topic=topic, research=research)
        headline = await self.llm.generate(headline_prompt)
        logger.debug("Headline generated: '%s'", headline[:100])

        # Step 2: Generate article body
        article_prompt = ARTICLE_PROMPT.format(topic=topic, research=research)
        article = await self.llm.generate(article_prompt)
        logger.debug("Article generated | length=%d", len(article))

        # Step 3: Generate summary
        summary_prompt = SUMMARY_PROMPT.format(topic=topic, article=article)
        summary = await self.llm.generate(summary_prompt)
        logger.debug("Summary generated | length=%d", len(summary))

        # Step 4: Generate SEO title
        seo_title_prompt = SEO_TITLE_PROMPT.format(topic=topic, headline=headline)
        seo_title = await self.llm.generate(seo_title_prompt)
        logger.debug("SEO title generated: '%s'", seo_title[:80])

        # Step 5: Generate meta description
        meta_desc_prompt = META_DESCRIPTION_PROMPT.format(
            topic=topic, headline=headline, summary=summary
        )
        meta_description = await self.llm.generate(meta_desc_prompt)
        logger.debug("Meta description generated | length=%d", len(meta_description))

        # Build response
        response = WriterResponse(
            headline=headline,
            summary=summary,
            article=article,
            seo_title=seo_title,
            meta_description=meta_description,
        )

        # Placeholder: persist to database in future phases
        # await self.repository.save(response)

        logger.info("Article generation pipeline complete | topic='%s'", topic)
        return response
