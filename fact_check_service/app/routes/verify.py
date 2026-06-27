"""
Fact-Check Service — Route Handlers.

Defines the /verify and /health endpoints.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Depends

from shared.config import get_settings
from shared.schemas import FactCheckRequest, FactCheckResponse, HealthResponse

from app.config import SERVICE_NAME, SERVICE_VERSION
from fact_check_service.app.dependencies import get_fact_check_service
from fact_check_service.app.services.service import FactCheckService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/verify",
    response_model=FactCheckResponse,
    summary="Verify article content",
    description="Validates an article for factual consistency, date/number accuracy, and generates a confidence score.",
)
async def verify(
    request: FactCheckRequest,
    service: FactCheckService = Depends(get_fact_check_service),
) -> FactCheckResponse:
    """
    Verify the factual accuracy of an article.

    Args:
        request: FactCheckRequest with article text and topic.
        service: Injected FactCheckService instance.

    Returns:
        FactCheckResponse with verification status, confidence score, issues, and recommendations.
    """
    logger.info("Verify request received | topic='%s'", request.topic)
    result = await service.verify_article(
        article=request.article,
        topic=request.topic,
    )
    logger.info(
        "Verification completed | topic='%s' | status=%s | score=%d",
        request.topic,
        result.status,
        result.confidence_score,
    )
    return result


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the health status of the Fact-Check Service.",
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
