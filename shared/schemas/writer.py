"""Pydantic models for the AI Writer Service."""

from pydantic import BaseModel, Field


class WriterRequest(BaseModel):
    """Request payload for the /generate endpoint."""

    topic: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="The article topic",
        examples=["AI in Education"],
    )
    research: str = Field(
        ...,
        min_length=1,
        description="Research notes and data to base the article on",
    )


class WriterResponse(BaseModel):
    """Response payload from the /generate endpoint."""

    headline: str = Field(..., description="Generated article headline")
    summary: str = Field(..., description="Article summary / abstract")
    article: str = Field(..., description="Full article body")
    seo_title: str = Field(..., description="SEO-optimized page title")
    meta_description: str = Field(..., description="Meta description for search engines")
