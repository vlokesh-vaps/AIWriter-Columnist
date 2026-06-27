"""
Research Service — FastAPI Application.

Accepts a topic and generates structured research data
including research notes, references, and statistics.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from shared.config import get_settings
from shared.exceptions import ServiceError, LLMProviderError
from shared.logging import setup_logging

from research_service.app.routes.research import router as research_router

# ── Settings & Logging ────────────────────────────────────────────────────
settings = get_settings()
logger = setup_logging("research_service", level=settings.LOG_LEVEL)


# ── Lifespan ──────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown logic."""
    logger.info(
        "Research Service starting | env=%s | llm_provider=%s",
        settings.ENVIRONMENT,
        settings.LLM_PROVIDER,
    )
    yield
    logger.info("Research Service shutting down")


# ── FastAPI App ───────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Newsroom — Research Service",
    description=(
        "Research service for the AI Newsroom Platform. "
        "Accepts a topic and generates comprehensive research notes, "
        "references, and statistics summaries using LLM-powered analysis."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────
app.include_router(research_router, tags=["Research"])


# ── Exception Handlers ───────────────────────────────────────────────────
@app.exception_handler(LLMProviderError)
async def llm_provider_error_handler(request: Request, exc: LLMProviderError) -> JSONResponse:
    """Handle LLM provider errors with structured error response."""
    logger.error("LLM Provider Error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "llm_provider_error",
            "message": exc.message,
            "provider": exc.provider,
        },
    )


@app.exception_handler(ServiceError)
async def service_error_handler(request: Request, exc: ServiceError) -> JSONResponse:
    """Handle general service errors."""
    logger.error("Service Error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "service_error",
            "message": exc.message,
        },
    )


@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for unhandled exceptions."""
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred",
        },
    )
