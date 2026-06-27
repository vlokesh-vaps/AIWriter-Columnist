"""
AI Columnist Service — Route Handlers.

Defines two endpoints:
  • POST /columnist/generate — Generate a full opinion article package.
  • GET  /columnist/health   — Service health check.
"""

import logging
from datetime import datetime

from fastapi import APIRouter, Depends

from shared.config import get_settings
from shared.schemas import ColumnistRequest, ColumnistResponse, HealthResponse

from app.config import SERVICE_NAME, SERVICE_VERSION
from app.dependencies import get_columnist_service
from app.services.service import ColumnistService

logger = logging.getLogger(__name__)

# Create the router with a URL prefix so all endpoints start with /columnist
router = APIRouter(prefix="/columnist")


# ── POST /columnist/generate ─────────────────────────────────────────────

@router.post(
    "/generate",
    response_model=ColumnistResponse,
    summary="Generate opinion article package",
    description=(
        "Receives a topic and research data, then generates a complete "
        "opinion article package including headline, opinion body, "
        "future trends, pros/cons, and recommendations."
    ),
)
async def generate(
    request: ColumnistRequest,
    service: ColumnistService = Depends(get_columnist_service),
) -> ColumnistResponse:
    """
    Generate a full opinion article package.

    This endpoint is the main entry point for the AI Columnist Service.
    It accepts a topic and research data, runs the five-step pipeline,
    and returns the assembled response.

    Args:
        request: ColumnistRequest with topic and research data.
        service: Injected ColumnistService instance (via FastAPI Depends).

    Returns:
        ColumnistResponse with headline, opinion article, future trends,
        pros, cons, and recommendations.
    """
    logger.info("Generate request received | topic='%s'", request.topic)

    # Run the full columnist pipeline
    result = await service.generate_column(
        topic=request.topic,
        research=request.research,
    )

    logger.info("Column generation completed | topic='%s'", request.topic)
    return result


# ── GET /columnist/health ────────────────────────────────────────────────

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the health status of the AI Columnist Service.",
)
async def health_check() -> HealthResponse:
    """
    Return the current health status of the service.

    This is used by Docker health checks, load balancers, and
    monitoring systems to verify the service is running.
    """
    settings = get_settings()
    return HealthResponse(
        status="healthy",
        service=SERVICE_NAME,
        version=SERVICE_VERSION,
        timestamp=datetime.utcnow(),
        llm_provider=settings.LLM_PROVIDER,
    )
