"""
AI Writer Service — Route Handlers.

Defines the /generate and /health endpoints.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Depends

from shared.config import get_settings
from shared.schemas import WriterRequest, WriterResponse, HealthResponse

from app.config import SERVICE_NAME, SERVICE_VERSION
from app.dependencies import get_writer_service
from app.services.service import WriterService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/generate",
    response_model=WriterResponse,
    summary="Generate article content",
    description="Receives topic and research, generates headline, article, summary, and SEO metadata.",
)
async def generate(
    request: WriterRequest,
    service: WriterService = Depends(get_writer_service),
) -> WriterResponse:
    """
    Generate a complete article package from topic and research.

    Args:
        request: WriterRequest with topic and research data.
        service: Injected WriterService instance.

    Returns:
        WriterResponse with headline, article, summary, SEO title, meta description.
    """
    logger.info("Generate request received | topic='%s'", request.topic)
    result = await service.generate_article(
        topic=request.topic,
        research=request.research,
    )
    logger.info("Article generation completed | topic='%s'", request.topic)
    return result


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the health status of the AI Writer Service.",
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