"""
Pydantic models for the AI Columnist Service.

Defines the request and response schemas for opinion-based
analysis article generation. Used by the columnist endpoint.
"""

from typing import List
from pydantic import BaseModel, Field


class ColumnistRequest(BaseModel):
    """
    Request payload for the POST /columnist/generate endpoint.

    Fields:
        topic: The subject the columnist should write about.
        research: Research data from the Research Service to base analysis on.
    """

    topic: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="The topic for the opinion/analysis article",
        examples=["Future of AI in Education"],
    )
    research: str = Field(
        ...,
        min_length=1,
        description="Research data from the Research Service",
    )


class ColumnistResponse(BaseModel):
    """
    Response payload from the POST /columnist/generate endpoint.

    Contains the full opinion article package: headline, opinion body,
    future trends analysis, pros/cons lists, and recommendations.
    """

    headline: str = Field(
        ...,
        description="Attention-grabbing headline for the opinion article",
    )
    opinion_article: str = Field(
        ...,
        description="Full opinion-based analysis article body",
    )
    future_trends: str = Field(
        ...,
        description="Analysis of future trends related to the topic",
    )
    pros: List[str] = Field(
        ...,
        description="List of advantages / positive aspects",
    )
    cons: List[str] = Field(
        ...,
        description="List of disadvantages / risks / concerns",
    )
    recommendations: List[str] = Field(
        ...,
        description="Actionable recommendations for the reader",
    )
