"""Pydantic model for health check responses."""

from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Standard health check response used by all services."""

    status: str = Field(default="healthy", description="Service health status")
    service: str = Field(..., description="Name of the service")
    version: str = Field(default="0.1.0", description="Service version")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Current server timestamp",
    )
    llm_provider: str = Field(default="unknown", description="Active LLM provider")
