"""Pydantic models for the Research Service."""

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """Request payload for the /research endpoint."""

    topic: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="The topic to research",
        examples=["AI in Education"],
    )


class ResearchResponse(BaseModel):
    """Response payload from the /research endpoint."""

    topic: str = Field(..., description="The researched topic")
    research: str = Field(..., description="Generated research notes and analysis")
    references: list[str] = Field(
        default_factory=list,
        description="List of generated references and sources",
    )
