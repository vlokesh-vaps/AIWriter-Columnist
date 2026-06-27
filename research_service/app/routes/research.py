"""
Research Service — Route Handlers.

Defines the /research and /health endpoints.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Depends

from shared.config import get_settings
from shared.schemas import ResearchRequest, ResearchResponse, HealthResponse

from app.config import SERVICE_NAME, SERVICE_VERSION
from research_service.app.dependencies import get_research_service
from research_service.app.services.service import ResearchService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/research",
    response_model=ResearchResponse,
    summary="Generate research data",
    description="Accepts a topic and returns structured research notes, references, and statistics.",
)
async def research(
    request: ResearchRequest,
    service: ResearchService = Depends(get_research_service),
) -> ResearchResponse:
    """
    Generate comprehensive research data for a given topic.

    Args:
        request: ResearchRequest with the topic to research.
        service: Injected ResearchService instance.

    Returns:
        ResearchResponse with research notes and references.
    """
    logger.info("Research request received | topic='%s'", request.topic)
    result = await service.generate_research(topic=request.topic)
    logger.info("Research completed | topic='%s'", request.topic)
    return result


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the health status of the Research Service.",
)
async def health_check() -> HealthResponse:
    """Return service health status."""
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        service=SERVICE_NAME,
        version=SERVICE_VERSION,
        timestamp=datetime.utcnow(),
        llm_provider=settings.LLM_PROVIDER,
    )