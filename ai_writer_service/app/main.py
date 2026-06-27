"""
AI Writer Service — FastAPI Application.

Receives topic and research data, then generates a complete article
package including headline, article body, summary, SEO title,
and meta description.
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

from app.routes.writer import router as writer_router

# ── Settings & Logging ────────────────────────────────────────────────────
settings = get_settings()
logger = setup_logging("ai_writer_service", level=settings.LOG_LEVEL)


# ── Lifespan ──────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown logic."""
    logger.info(
        "AI Writer Service starting | env=%s | llm_provider=%s",
        settings.ENVIRONMENT,
        settings.LLM_PROVIDER,
    )
    yield
    logger.info("AI Writer Service shutting down")


# ── FastAPI App ───────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Newsroom — AI Writer Service",
    description=(
        "AI Writer service for the AI Newsroom Platform. "
        "Receives topic and research data, then generates a complete "
        "article package with headline, body, summary, and SEO metadata."
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
app.include_router(writer_router, tags=["Writer"])


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
