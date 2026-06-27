"""Pydantic models for the Fact-Check Service."""

from pydantic import BaseModel, Field


class FactCheckRequest(BaseModel):
    """Request payload for the /verify endpoint."""

    article: str = Field(
        ...,
        min_length=1,
        description="The article text to fact-check",
    )
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="The article topic for context",
        examples=["AI in Education"],
    )


class FactCheckResponse(BaseModel):
    """Response payload from the /verify endpoint."""

    status: str = Field(
        ...,
        description="Verification status (e.g. verified, flagged, rejected)",
        examples=["verified"],
    )
    confidence_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence score from 0 to 100",
    )
    issues: list[str] = Field(
        default_factory=list,
        description="List of identified issues or inconsistencies",
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Suggested corrections or improvements",
    )
