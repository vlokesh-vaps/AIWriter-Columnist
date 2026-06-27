"""Shared prompt templates for all services."""

from shared.prompts.research_prompts import RESEARCH_PROMPT, REFERENCES_PROMPT
from shared.prompts.writer_prompts import (
    HEADLINE_PROMPT,
    ARTICLE_PROMPT,
    SUMMARY_PROMPT,
    SEO_TITLE_PROMPT,
    META_DESCRIPTION_PROMPT,
)
from shared.prompts.fact_check_prompts import FACT_CHECK_PROMPT
from shared.prompts.columnist_prompts import (
    OPINION_ARTICLE_PROMPT,
    TREND_ANALYSIS_PROMPT,
    PROS_CONS_PROMPT,
    RECOMMENDATIONS_PROMPT,
    COLUMNIST_HEADLINE_PROMPT,
)

__all__ = [
    "RESEARCH_PROMPT",
    "REFERENCES_PROMPT",
    "HEADLINE_PROMPT",
    "ARTICLE_PROMPT",
    "SUMMARY_PROMPT",
    "SEO_TITLE_PROMPT",
    "META_DESCRIPTION_PROMPT",
    "FACT_CHECK_PROMPT",
    "OPINION_ARTICLE_PROMPT",
    "TREND_ANALYSIS_PROMPT",
    "PROS_CONS_PROMPT",
    "RECOMMENDATIONS_PROMPT",
    "COLUMNIST_HEADLINE_PROMPT",
]

